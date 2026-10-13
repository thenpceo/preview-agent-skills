#!/usr/bin/env python3
"""
preview-provenance: connect clips in an edit to the Preview takes they came from.

Three commands, stdlib only, read-only against Preview:

  index    build/refresh a per-project map  takeId -> (ETag, size, canvas, model, ...)
  whereis  "here is a clip (or a take id): where did it come from?"
  incut    "which Preview takes are actually in this Premiere sequence?"

Matching needs no downloads: Preview's storage answers HEAD with Content-Length and an
ETag equal to the file's MD5 (verified 2026-10-11). A local file is matched by MD5+size.
Files whose name already contains a take id (k57...) are resolved directly and then
verified the same way when the file is present.

Requires: Python 3.9+, the Preview CLI logged in (`preview auth status`).
"""
import argparse, concurrent.futures, datetime, gzip, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
import urllib.request
import xml.etree.ElementTree as ET

TAKE_RE = re.compile(r'k57[a-z0-9]{29}')
STORAGE = 'https://fajl.fellini.app/'
APP = 'https://app.preview.io'
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.environ.get('PREVIEW_PROVENANCE_CACHE') or os.path.join(HERE, 'cache')
TICKS = 254016000000  # Premiere ticks per second
UA = {'User-Agent': 'Mozilla/5.0 preview-provenance'}
SEARCH_QUERIES = ['video', 'shot', 'scene', 'close up', 'wide shot', 'medium shot', 'dialogue', 'man', 'woman',
                  'group of people', 'product', 'can', 'tv', 'party', 'outdoor', 'interior', 'night', 'day',
                  'animal', 'reaction', 'walking', 'sitting', 'end card', 'logo', 'opening', 'edit']

# ----------------------------------------------------------------------------- CLI plumbing

def find_cli():
    """PREVIEW_CLI env var, then `preview` on PATH, then the npm global root."""
    p = os.environ.get('PREVIEW_CLI')
    if p and os.path.exists(p):
        return p
    for name in ('preview', 'preview.exe', 'preview.cmd'):
        w = shutil.which(name)
        if w:
            return w
    try:
        root = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True, shell=(os.name == 'nt')).stdout.strip()
        for cand in (os.path.join(root, '@previewio', 'cli', 'bin', 'preview.exe'),
                     os.path.join(root, '@previewio', 'cli', 'bin', 'preview')):
            if root and os.path.exists(cand):
                return cand
    except Exception:
        pass
    sys.exit('Preview CLI not found. Install it, put `preview` on PATH, or set PREVIEW_CLI=<path to the preview executable>.')

CLI = None

def _decode(raw):
    for enc in ('utf-8-sig', 'utf-16'):
        try:
            return json.loads(raw.decode(enc))
        except Exception:
            pass
    raise RuntimeError('unparseable CLI output: ' + raw[:200].decode('latin1'))

def cli(*args, allow_fail=False):
    global CLI
    CLI = CLI or find_cli()
    r = subprocess.run([CLI, *args, '--json'], capture_output=True, env=dict(os.environ, PREVIEW_CLI_SKIP_UPDATE='1'))
    if not r.stdout.strip():
        if allow_fail:
            return {'ok': False, 'error': r.stderr.decode('latin1')[:300]}
        sys.exit(f'preview {" ".join(args[:3])}: no output. stderr: {r.stderr.decode("latin1")[:300]}')
    env = _decode(r.stdout)
    if not env.get('ok', True) and not allow_fail:
        sys.exit(f'preview {" ".join(args[:3])} failed: {json.dumps(env.get("error"))[:400]}')
    return env

def tool(name, inp, allow_fail=False):
    fd, p = tempfile.mkstemp(suffix='.json'); os.close(fd)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(inp, f)
    try:
        return cli('tools', 'run', name, '--file', p, allow_fail=allow_fail)
    finally:
        os.unlink(p)

def listish(data, key):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        v = data.get(key)
        if isinstance(v, list):
            return v
    return []

# ----------------------------------------------------------------------------- hashing / HEAD

def head(storage_key):
    url = STORAGE + storage_key
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, method='HEAD', headers=UA), timeout=60)
        return r.headers.get('ETag', '').strip('"').lower(), int(r.headers.get('Content-Length') or 0)
    except Exception as e:
        return None, None

def local_md5(path):
    h = hashlib.md5(); n = 0
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b); n += len(b)
    return h.hexdigest(), n

def remote_sha256(storage_key):
    """Full download (only for --full-hash sanity checks). Returns (sha256, size)."""
    h = hashlib.sha256(); n = 0
    with urllib.request.urlopen(urllib.request.Request(STORAGE + storage_key, headers=UA), timeout=300) as r:
        for b in iter(lambda: r.read(1 << 20), b''):
            h.update(b); n += len(b)
    return h.hexdigest(), n

def local_sha256(path):
    h = hashlib.sha256(); n = 0
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b); n += len(b)
    return h.hexdigest(), n

# ----------------------------------------------------------------------------- index

def index_path(pid):
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, f'{pid}.json')

def load_index(pid):
    p = index_path(pid)
    if os.path.exists(p):
        return json.load(open(p, encoding='utf-8'))
    return {'projectId': pid, 'updated': None, 'takes': {}, 'canvases': {}, 'scenes': {}}

def save_index(ix):
    ix['updated'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    tmp = index_path(ix['projectId']) + '.tmp'
    json.dump(ix, open(tmp, 'w', encoding='utf-8'))
    os.replace(tmp, index_path(ix['projectId']))

def record_from_take(t):
    gd = t.get('generationData') or {}
    md = t.get('metadata') or {}
    return {
        'takeId': t.get('_id'), 'kind': t.get('kind'), 'canvasId': t.get('canvasId'), 'sceneId': t.get('sceneId'),
        'created': t.get('_creationTime'), 'storageKey': t.get('storageKey'), 'createdBy': t.get('createdBy'),
        'model': gd.get('model'), 'duration': gd.get('duration'), 'resolution': gd.get('resolution'),
        'prompt': (gd.get('prompt') or '')[:300],
        'metaType': md.get('type'), 'originTakeId': (md.get('data') or {}).get('originTakeId'),
    }

def canvas_name(ix, pid, canvas_id):
    if not canvas_id:
        return '?'
    if canvas_id not in ix['canvases']:
        env = tool('getCanvasContext', {'projectId': pid, 'canvasId': canvas_id}, allow_fail=True)
        ix['canvases'][canvas_id] = (env.get('data') or {}).get('name') or canvas_id
    return ix['canvases'][canvas_id]

def cmd_index(a):
    pid, _ = resolve_project(a.project)
    ix = load_index(pid)
    takes = ix['takes']
    stories = listish(cli('stories', 'list', '--project-id', pid).get('data'), 'stories')
    scenes = []
    for s in stories:
        for sc in listish(cli('scenes', 'list', '--story-id', s['_id']).get('data'), 'scenes'):
            scenes.append(sc); ix['scenes'][sc['_id']] = {'title': sc.get('title'), 'story': s.get('name')}
    print(f'{len(stories)} shotlists, {len(scenes)} sequences', flush=True)
    new = 0
    kinds = ['video', 'image'] if a.kind == 'both' else [a.kind]
    for sc in scenes:
        for kind in kinds:
            env = cli('takes', 'list', '--scene-id', sc['_id'], '--kind', kind, '--limit', '250', allow_fail=True)
            for t in listish(env.get('data'), 'takes'):
                if t.get('_id') and t.get('storageKey') and t['_id'] not in takes:
                    takes[t['_id']] = record_from_take(t); new += 1
        print(f'  {sc.get("title")!s:40.40} total {len(takes)}', flush=True)
    if a.deep:
        # Semantic search is the only way past the newest-250 cap. Generic words miss most takes, so
        # "snowball": use the prompts of takes we already know as queries; every query returns up to 100
        # neighbours; keep going per sequence until a round adds nothing new.
        def search(q, scene_id):
            env = tool('searchProjectContext', {'projectId': pid, 'query': q[:300], 'kinds': ['take'], 'sceneId': scene_id,
                                                'hasMedia': True, 'limit': 100}, allow_fail=True)
            data = env.get('data')
            return {h.get('refId') for h in data if h.get('refId')} if isinstance(data, list) else set()
        unknown = set()
        for sc in scenes:
            sid = sc['_id']
            seen_q = set(); known_here = {k for k, v in takes.items() if v.get('sceneId') == sid}
            frontier = [v.get('prompt') or '' for k, v in takes.items() if v.get('sceneId') == sid and v.get('prompt')]
            frontier = [q for q in frontier if len(q) > 15][:a.deep_rounds * 20] or ['video', 'shot', 'scene']
            rounds = 0
            while frontier and rounds < a.deep_rounds:
                rounds += 1; new_ids = set()
                qs = [q for q in frontier if q not in seen_q][:20]
                seen_q.update(qs)
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
                    for ids in ex.map(lambda q: search(q, sid), qs):
                        new_ids |= (ids - known_here - unknown)
                if not new_ids:
                    break
                unknown |= new_ids
                # fetch the newcomers now so their prompts can seed the next round
                def fetch(tid):
                    t = get_take(tid)
                    return tid, (record_from_take(t) if t.get('storageKey') else None)
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
                    fetched = list(ex.map(fetch, sorted(new_ids)))
                frontier = []
                for tid, rec in fetched:
                    if rec:
                        takes[tid] = rec; known_here.add(tid); new += 1
                        if rec.get('prompt') and len(rec['prompt']) > 15:
                            frontier.append(rec['prompt'])
                print(f'  deep {sc.get("title")!s:36.36} round {rounds}: +{len(new_ids)} (sequence total {len(known_here)})', flush=True)
            save_index(ix)
    todo = [k for k, v in takes.items() if not v.get('etag') and v.get('storageKey')]
    print(f'{new} new takes; HEAD-ing {len(todo)} for ETag/size', flush=True)
    done = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
        for tid, (etag, ln) in zip(todo, ex.map(lambda k: head(takes[k]['storageKey']), todo)):
            if etag:
                takes[tid]['etag'] = etag; takes[tid]['length'] = ln
            done += 1
            if done % 200 == 0:
                save_index(ix); print(f'  {done}/{len(todo)}', flush=True)
    save_index(ix)
    n_etag = sum(1 for v in takes.values() if v.get('etag'))
    print(f'index saved: {index_path(pid)}  takes={len(takes)} with-etag={n_etag}')

# ----------------------------------------------------------------------------- resolution

PROJECT_ID_RE = re.compile(r'k97[a-z0-9]{29}')

def resolve_project(name_or_id):
    """Accept a Preview project id or a (case-insensitive, partial) project name."""
    if PROJECT_ID_RE.fullmatch(name_or_id or ''):
        return name_or_id, None
    projects = listish(cli('projects', 'list').get('data'), 'projects')
    q = (name_or_id or '').lower().replace(' ', '')
    hits = [p for p in projects if q and q in (p.get('name') or '').lower().replace(' ', '')]
    exact = [p for p in hits if (p.get('name') or '').lower().replace(' ', '') == q]
    if len(exact) == 1:
        hits = exact
    if len(hits) == 1:
        return hits[0]['_id'], hits[0].get('name')
    names = sorted((p.get('name') or '?') for p in projects)
    if not hits:
        sys.exit(f'No Preview project matches {name_or_id!r}. Projects: {names}')
    sys.exit(f'Ambiguous project {name_or_id!r}: {[h.get("name") for h in hits]}')

def find_prprojs(spot, roots, client=None, max_depth=6):
    """Find Premiere projects on the mounted share whose filename contains <spot> (case-insensitive)."""
    found = []
    skip = ('adobe premiere pro', '$recycle.bin', 'system volume information', 'node_modules')
    for root in roots:
        base_depth = root.rstrip('/' + os.sep).count(os.sep) + root.rstrip('/' + os.sep).count('/')
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            depth = dirpath.count(os.sep) + dirpath.count('/') - base_depth
            if depth >= max_depth:
                dirnames[:] = []
            else:
                dirnames[:] = [d for d in dirnames if not d.lower().startswith(skip) and not d.startswith('.')]
            for f in filenames:
                if f.lower().endswith('.prproj') and spot.lower() in f.lower():
                    fp = os.path.join(dirpath, f)
                    if not client or client.lower().replace(' ', '') in fp.lower().replace(' ', ''):
                        found.append(fp)
    found.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    return found

def ensure_index(pid, auto=True):
    ix = load_index(pid)
    if not ix['takes'] and auto:
        print(f'No take index for project {pid} yet; building one (a few minutes, HEAD requests only)...', file=sys.stderr, flush=True)
        cmd_index(argparse.Namespace(project=pid, kind='both', deep=False, deep_rounds=0))
        ix = load_index(pid)
    return ix


def by_etag(ix):
    m = {}
    for tid, v in ix['takes'].items():
        if v.get('etag'):
            m.setdefault((v['etag'], v.get('length')), []).append(tid)
    return m

def get_take(tid):
    env = cli('takes', 'get', '--take-id', tid, allow_fail=True)
    return (env.get('data') or {}).get('take') or {}

def origin_chain(tid):
    """Follow duplicate -> originTakeId. Returns list of full take records, original last."""
    chain, seen, cur = [], set(), tid
    while cur and cur not in seen and len(chain) < 8:
        seen.add(cur); t = get_take(cur)
        if not t:
            break
        chain.append(t)
        md = t.get('metadata') or {}
        cur = (md.get('data') or {}).get('originTakeId') if md.get('type') == 'duplicate' else None
    return chain

def jst(ms):
    if not ms:
        return '?'
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M')

def resolve_file(path, ix, want_verify=True):
    """Return dict: ids (candidate take ids), method, verified (True/False/None), md5, size."""
    base = os.path.basename(path)
    m = TAKE_RE.search(base)
    out = {'file': path, 'ids': [], 'method': None, 'verified': None, 'md5': None, 'size': None, 'exists': os.path.exists(path)}
    if out['exists']:
        out['md5'], out['size'] = local_md5(path)
    if m:
        out['ids'] = [m.group(0)]; out['method'] = 'id-in-filename'
        if out['exists'] and want_verify:
            rec = ix['takes'].get(m.group(0))
            key = rec.get('storageKey') if rec else (get_take(m.group(0)).get('storageKey'))
            if key:
                etag, ln = head(key)
                out['verified'] = (etag == out['md5'] and ln == out['size']) if etag and re.fullmatch(r'[0-9a-f]{32}', etag) and ln is not None else None
                out['remote_etag'] = etag
        return out
    if out['exists']:
        ids = by_etag(ix).get((out['md5'], out['size'])) or []
        if ids:
            out['ids'] = ids; out['method'] = 'md5-match'; out['verified'] = True
        else:
            out['method'] = 'no-match'
    else:
        out['method'] = 'file-missing'
    return out

def pick_original(ids, ix):
    """Among ids sharing bytes, prefer a non-duplicate; else the oldest."""
    recs = [(tid, ix['takes'].get(tid) or {}) for tid in ids]
    gens = [r for r in recs if r[1].get('metaType') != 'duplicate']
    pool = gens or recs
    pool.sort(key=lambda r: r[1].get('created') or 0)
    return pool[0][0]

def frame_ref(gd, key):
    """startFrame/endFrame may be stored as <key>TakeId / <key>AssetId / <key>={takeId,type}."""
    v = gd.get(key + 'TakeId') or gd.get(key + 'AssetId')
    if v:
        return v
    v = gd.get(key)
    if isinstance(v, dict):
        return f"{v.get('type') or 'ref'}:{v.get('takeId') or v.get('assetId') or v.get('id')}"
    return v

def deep_link(pid, canvas_id, tid):
    return f'{APP}/project/{pid}/canvas/{canvas_id}?take_view={tid}' if canvas_id else f'{APP}/project/{pid}'

def describe_take(pid, ix, tid, full=True):
    """Collect everything about one take: chain to original, provenance, context.
    With full=False and the take in the index, no CLI call is made at all."""
    if not full:
        rec = ix['takes'].get(tid)
        if rec:
            chain_ids = [tid]; cur = rec
            while cur and cur.get('metaType') == 'duplicate' and cur.get('originTakeId') and cur['originTakeId'] not in chain_ids and len(chain_ids) < 8:
                chain_ids.append(cur['originTakeId']); cur = ix['takes'].get(cur['originTakeId'])
            if cur:  # whole chain known from the index
                oid = chain_ids[-1]
                return {'takeId': tid, 'originalTakeId': oid, 'isDuplicate': len(chain_ids) > 1, 'duplicateChain': chain_ids,
                        'kind': cur.get('kind'), 'canvasId': cur.get('canvasId'), 'canvas': canvas_name(ix, pid, cur.get('canvasId')),
                        'sceneId': cur.get('sceneId'), 'created': jst(cur.get('created')), 'createdBy': cur.get('createdBy'),
                        'model': cur.get('model'), 'duration': cur.get('duration'), 'resolution': cur.get('resolution'),
                        'aspectRatio': None, 'audioEnabled': None, 'cost': None, 'prompt': cur.get('prompt'),
                        'videoReferenceMode': None, 'startFrame': None, 'endFrame': None, 'resolvedReferences': None,
                        'link': deep_link(pid, cur.get('canvasId'), oid), 'linkAsPlaced': deep_link(pid, rec.get('canvasId'), tid),
                        'handle': f'@take:{{{oid}}}', 'ingredients': [], 'parents': [], 'visualCaption': None, 'tags': None}
    chain = origin_chain(tid)
    if not chain:
        return {'takeId': tid, 'error': 'take not found'}
    orig = chain[-1]
    oid = orig['_id']
    gd = orig.get('generationData') or {}
    d = {
        'takeId': tid, 'originalTakeId': oid, 'isDuplicate': len(chain) > 1,
        'duplicateChain': [c['_id'] for c in chain],
        'kind': orig.get('kind'), 'canvasId': orig.get('canvasId'), 'canvas': canvas_name(ix, pid, orig.get('canvasId')),
        'sceneId': orig.get('sceneId'), 'created': jst(orig.get('_creationTime')), 'createdBy': orig.get('createdBy'),
        'model': gd.get('model'), 'duration': gd.get('duration'), 'resolution': gd.get('resolution'),
        'aspectRatio': gd.get('aspectRatio'), 'audioEnabled': gd.get('audioEnabled'), 'cost': gd.get('cost'),
        'prompt': gd.get('prompt'), 'videoReferenceMode': gd.get('videoReferenceMode'),
        'startFrame': frame_ref(gd, 'startFrame'),
        'endFrame': frame_ref(gd, 'endFrame'),
        'resolvedReferences': gd.get('resolvedReferences'),
        'link': deep_link(pid, orig.get('canvasId'), oid),
        'linkAsPlaced': deep_link(pid, chain[0].get('canvasId'), tid),
        'handle': f'@take:{{{oid}}}',
        'ingredients': [], 'parents': [], 'visualCaption': None, 'tags': None,
    }
    if full:
        prov = (tool('getTakeProvenance', {'takeId': oid}, allow_fail=True).get('data') or {})
        pt = prov.get('take') or {}
        d['ingredients'] = pt.get('ingredients') or []
        d['parents'] = [p.get('handle') or p.get('takeId') for p in (prov.get('parents') or [])]
        d['visualCaption'] = pt.get('visualCaption')
        ctx = (tool('getTakeContext', {'takeId': oid}, allow_fail=True).get('data') or {})
        d['tags'] = ctx.get('tags')
        d['visualCaption'] = d['visualCaption'] or ctx.get('visualCaption')
        # name the ingredient assets
        for ing in d['ingredients']:
            if ing.get('kind') == 'asset' and ing.get('id'):
                a = (cli('assets', 'get', '--asset-id', ing['id'], allow_fail=True).get('data') or {})
                a = a.get('asset') or a
                ing['name'] = a.get('name')
            elif ing.get('kind') == 'take' and ing.get('id'):
                t = ix['takes'].get(ing['id']) or record_from_take(get_take(ing['id']))
                ing['name'] = f"{t.get('kind')} take, {t.get('model')}, {jst(t.get('created'))}"
    return d

def md_take(d):
    L = [f"## {d['handle']}"]
    if d.get('error'):
        return L + [f"- {d['error']}"]
    L.append(f"- Open in Preview: {d['link']}")
    if d['isDuplicate']:
        L.append(f"- The file's take `{d['takeId']}` is a duplicate; original generation is `{d['originalTakeId']}` (chain: {' -> '.join(d['duplicateChain'])}). As placed: {d['linkAsPlaced']}")
    L.append(f"- Canvas: {d['canvas']}  | generated: {d['created']}  | kind: {d['kind']}")
    L.append(f"- Model: {d['model']}  | {d['duration']}  | {d['resolution']}  | {d['aspectRatio']}  | audio: {d['audioEnabled']}  | credits: {d['cost']}")
    if d.get('videoReferenceMode'):
        L.append(f"- videoReferenceMode: {d['videoReferenceMode']}")
    if d.get('startFrame') or d.get('endFrame'):
        L.append(f"- startFrame: {d.get('startFrame')}  endFrame: {d.get('endFrame')}")
    if d['ingredients']:
        L.append('- Ingredients (Preview provenance): ' + ', '.join(f"`{i.get('handle')}`" + (f" = **{i.get('name')}**" if i.get('name') else '') for i in d['ingredients']))
    if d['parents']:
        L.append('- Parents (edit/extend sources): ' + ', '.join(f'`{p}`' for p in d['parents']))
    if d['tags']:
        L.append(f"- Tags: {d['tags']}")
    L.append('- Prompt:'); L.append('  ```'); L.append('  ' + (d['prompt'] or '').strip().replace('\n', '\n  ')); L.append('  ```')
    if d['visualCaption']:
        L.append(f"- Preview's visual caption: {d['visualCaption'][:700]}")
    return L

def project_of_take(tid):
    t = get_take(tid)
    return t.get('projectId'), t

def cmd_whereis(a, link_only=False):
    target = a.target
    pid = None
    if getattr(a, 'project', None):
        pid, _ = resolve_project(a.project)
    # a take id, or a filename carrying one, tells us the project by itself
    m = TAKE_RE.fullmatch(target) or TAKE_RE.search(os.path.basename(target))
    if m and not pid:
        pid, _ = project_of_take(m.group(0))
        if not pid:
            sys.exit(f'Take {m.group(0)} not found in Preview (deleted, or no access).')
    if not pid:
        # human-named file: try every cached project index
        cached = [f[:-5] for f in os.listdir(CACHE_DIR) if f.endswith('.json')] if os.path.isdir(CACHE_DIR) else []
        md5, size = (local_md5(target) if os.path.exists(target) else (None, None))
        for cand in cached:
            if (md5, size) in by_etag(load_index(cand)):
                pid = cand
                break
        if not pid:
            sys.exit('This file has no take id in its name and is not in any cached project index. '
                     'Add --project "<Preview project name>" so the right project can be indexed.')
    # an id-named target needs no index at all; only content matching does
    ix = load_index(pid) if m else ensure_index(pid)
    if TAKE_RE.fullmatch(target):
        ids, res = [target], None
    else:
        res = resolve_file(target, ix)
        ids = res['ids']
        if not ids:
            if res['method'] == 'file-missing':
                sys.exit(f'File not found and no take id in the name: {target}')
            sys.exit(f'No take in the index matches this file (md5 {res["md5"]}, {res["size"]} bytes). '
                     f'Either it is not a Preview download (re-encode, trim, asset), or it is older than the index reaches: '
                     f'run `index --project {pid} --deep` once and retry.')
    tid = pick_original(ids, ix) if len(ids) > 1 else ids[0]
    if link_only:
        chain = origin_chain(tid)
        orig = chain[-1] if chain else {}
        oid = orig.get('_id', tid)
        note = ('   (WARNING: file bytes differ from this take)' if res and res['verified'] is False else '   (bytes not verified)' if res and res['verified'] is None else '')
        print(deep_link(pid, orig.get('canvasId'), oid) + note)
        return
    d = describe_take(pid, ix, tid)
    if a.json:
        print(json.dumps({'projectId': pid, 'resolution': res, 'candidates': ids, 'take': d}, indent=1))
        return
    L = [f"# {os.path.basename(target)}"]
    if res:
        v = {True: 'VERIFIED byte-identical (MD5 + size match Preview storage)',
             False: 'WARNING: local file differs from the take media (re-encode, trim, or wrong id)',
             None: 'not verified (file missing or remote metadata unavailable)'}[res['verified']]
        L.append(f"- Resolved by: {res['method']}  | {v}")
        if len(ids) > 1:
            L.append(f"- Same bytes exist under {len(ids)} take ids: {', '.join(ids)}")
    L += md_take(d)
    print('\n'.join(L))

def cmd_link(a):
    cmd_whereis(a, link_only=True)

# ----------------------------------------------------------------------------- premiere

def parse_prproj(path):
    """Return (sequences, media_paths). sequences: {name: [ {start,end,track,path,clipName} ]}."""
    with gzip.open(path, 'rb') as f:
        raw = f.read()
    root = ET.fromstring(raw)
    byid = {}
    for el in root.iter():
        if 'ObjectID' in el.attrib: byid[('id', el.attrib['ObjectID'])] = el
        if 'ObjectUID' in el.attrib: byid[('uid', el.attrib['ObjectUID'])] = el
    def deref(el):
        if el is None: return None
        if 'ObjectRef' in el.attrib: return byid.get(('id', el.attrib['ObjectRef']))
        if 'ObjectURef' in el.attrib: return byid.get(('uid', el.attrib['ObjectURef']))
        return el
    def media_path(el, depth=0, seen=None):
        seen = seen if seen is not None else set()
        if el is None or depth > 12 or id(el) in seen: return None
        seen.add(id(el))
        if el.tag == 'Media':
            for k in ('ActualMediaFilePath', 'FilePath'):
                n = el.find(k)
                if n is not None and n.text: return n.text
            t = el.find('Title')
            return ('[title] ' + t.text) if t is not None and t.text else None
        for ch in list(el):
            r = media_path(deref(ch) if ('ObjectRef' in ch.attrib or 'ObjectURef' in ch.attrib) else ch, depth + 1, seen)
            if r: return r
        return None
    def ticks(el, tag):
        n = el.find(tag) if el is not None else None
        try: return int(n.text)
        except Exception: return None
    seqs = {}
    for seq in root.iter('Sequence'):
        if not ('ObjectID' in seq.attrib or 'ObjectUID' in seq.attrib): continue
        name = seq.findtext('Name') or '?'
        rows = []
        tgs = seq.find('TrackGroups')
        if tgs is None: continue
        for tg in tgs.findall('TrackGroup'):
            second = deref(tg.find('Second'))
            if second is None: continue
            kind = 'V' if second.tag.startswith('Video') else 'A'
            tracks = second.find('TrackGroup/Tracks') if second.find('TrackGroup/Tracks') is not None else second.find('Tracks')
            if tracks is None: continue
            for ti, tr in enumerate(tracks.findall('Track')):
                track = deref(tr)
                if track is None: continue
                items = track.find('ClipTrack/ClipItems/TrackItems') if track.find('ClipTrack/ClipItems/TrackItems') is not None else track.find('ClipItems/TrackItems')
                if items is None: continue
                for it in items.findall('TrackItem'):
                    ti_el = deref(it)
                    if ti_el is None: continue
                    cti = ti_el.find('ClipTrackItem')
                    base = cti.find('TrackItem') if cti is not None else ti_el.find('TrackItem')
                    start = ticks(base, 'Start') or 0
                    end = ticks(base, 'End')
                    sub = deref(cti.find('SubClip')) if cti is not None else None
                    clip = deref(sub.find('Clip')) if sub is not None else None
                    p = media_path(clip) or media_path(sub) or media_path(ti_el) or '?'
                    cname = (clip.findtext('Name') if clip is not None else None) or (sub.findtext('Name') if sub is not None else '') or ''
                    rows.append({'start': start / TICKS, 'end': (end or 0) / TICKS, 'track': f'{kind}{ti + 1}', 'path': p, 'clipName': cname})
        rows.sort(key=lambda r: (r['track'][0] != 'V', r['start'], r['track']))
        seqs[name] = rows
    return seqs

def local_roots(extra):
    """Places where the media share may be mounted on THIS machine: explicit --media-root(s) first,
    then every drive letter (Windows) or /Volumes/* (macOS) or /mnt/* /media/* (Linux)."""
    roots = list(extra or [])
    if os.name == 'nt':
        import string
        roots += [c + ':' + os.sep for c in string.ascii_uppercase if os.path.exists(c + ':' + os.sep)]
    else:
        for base in ('/Volumes', '/mnt', '/media', os.path.expanduser('~')):
            if os.path.isdir(base):
                roots += [os.path.join(base, d) for d in sorted(os.listdir(base))]
    return roots

def split_mount(p):
    """Strip drive/mount prefixes, retaining the share-relative path."""
    parts = [x for x in re.split(r'[\\/]+', p) if x != '']
    if len(parts) > 1 and parts[0] == 'Volumes':
        return parts[2:]
    if parts and re.fullmatch(r'[A-Za-z]:', parts[0]):
        return parts[1:]
    if len(parts) > 1 and parts[0] in ('mnt', 'media'):
        return parts[2:]
    return parts

_reloc_cache = {}
def relocate(p, roots):
    """Find the file the .prproj refers to on this machine, whatever drive/mount it was saved with."""
    if p in _reloc_cache:
        return _reloc_cache[p]
    out = p
    if not os.path.exists(p) and p != '?':
        rel = split_mount(p)
        found = None
        for root in roots:
            for tail in (rel, rel[1:]):  # rel[1:] covers a share mounted one level deeper
                if not tail:
                    continue
                cand = os.path.join(root, *tail)
                if os.path.exists(cand):
                    found = cand; break
            if found:
                break
        out = found or p
    _reloc_cache[p] = out
    return out

def pick_sequence(seqs, wanted):
    names = list(seqs)
    if wanted:
        hits = [n for n in names if wanted.lower() in n.lower()]
        if len(hits) == 1: return hits[0]
        if not hits: sys.exit(f'No sequence matches {wanted!r}. Sequences: {names}')
        exact = [n for n in hits if n.lower() == wanted.lower()]
        if exact: return exact[0]
        sys.exit(f'Ambiguous sequence {wanted!r}: {hits}')
    numbered = [(int(m.group(1)), n) for n in names for m in [re.search(r'_(\d{3})$', n)] if m]
    if numbered:
        return max(numbered)[1]
    sys.exit(f'Cannot pick a sequence automatically. Use --sequence. Sequences: {names}')

def cmd_sequences(a):
    seqs = parse_prproj(a.prproj)
    for n, rows in seqs.items():
        v = sum(1 for r in rows if r['track'].startswith('V'))
        print(f'{n!s:50.50} video clips {v:4d}  audio clips {len(rows) - v:4d}')

def cmd_incut(a):
    pid, pname = resolve_project(a.project)
    ix = ensure_index(pid)
    roots = local_roots(a.media_root)
    seqs = parse_prproj(a.prproj)
    name = pick_sequence(seqs, a.sequence)
    rows = [r for r in seqs[name] if a.audio or r['track'].startswith('V')]
    for r in rows:
        r['local'] = relocate(r['path'], roots)
    missing = sorted({r['local'] for r in rows if r['local'] != '?' and not os.path.exists(r['local'])})
    if missing:
        print(f'{len(missing)} referenced files not found on this machine (pass --media-root <mount of the share>):', file=sys.stderr)
        for m in missing[:10]:
            print('   ', m, file=sys.stderr)
    files = sorted({r['local'] for r in rows if r['local'] != '?'})
    print(f'sequence {name}: {len(rows)} clip instances, {len(files)} unique files', file=sys.stderr, flush=True)
    results = {}
    def work(f):
        res = resolve_file(f, ix)
        tid = None
        if res['ids']:
            tid = pick_original(res['ids'], ix) if len(res['ids']) > 1 else res['ids'][0]
        entry = {'resolution': res, 'take': None}
        if tid:
            entry['take'] = describe_take(pid, ix, tid, full=not a.brief)
            if a.full_hash and res['exists']:
                key = (ix['takes'].get(entry['take']['originalTakeId']) or {}).get('storageKey') or get_take(entry['take']['originalTakeId']).get('storageKey')
                if key:
                    rs, rn = remote_sha256(key); ls_, ln = local_sha256(f)
                    entry['fullHash'] = {'remote_sha256': rs, 'local_sha256': ls_, 'identical': rs == ls_ and rn == ln}
        return f, tid, entry
    # canvas names are cached in the index; warm them single-threaded first to avoid duplicate calls
    for cid in sorted({v.get('canvasId') for v in ix['takes'].values() if v.get('canvasId')} & {ix['takes'][TAKE_RE.search(os.path.basename(f)).group(0)]['canvasId'] for f in files if TAKE_RE.search(os.path.basename(f)) and TAKE_RE.search(os.path.basename(f)).group(0) in ix['takes']}):
        canvas_name(ix, pid, cid)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for i, (f, tid, entry) in enumerate(ex.map(work, files), 1):
            results[f] = entry
            st = res_method = entry['resolution']['method'] + (f" -> {tid}" if tid else '')
            print(f'  [{i}/{len(files)}] {os.path.basename(f)!s:60.60} {st}', file=sys.stderr, flush=True)
    results = {f: results[f] for f in files}
    save_index(ix)  # persists any canvas names learned
    # ---- write outputs
    out = a.out or os.path.join(os.getcwd(), 'incut-' + re.sub(r'[^A-Za-z0-9_.-]+', '_', name))
    os.makedirs(out, exist_ok=True)
    stem = os.path.join(out, re.sub(r'[^A-Za-z0-9_.-]+', '_', name))
    json.dump({'sequence': name, 'prproj': a.prproj, 'generated': datetime.datetime.now().isoformat(timespec='seconds'),
               'clips': rows, 'files': results}, open(stem + '.json', 'w', encoding='utf-8'), indent=1)
    L = [f'# {name}: Preview takes in this cut', '',
         f'Source `{a.prproj}` (saved {datetime.datetime.fromtimestamp(os.path.getmtime(a.prproj)).strftime("%Y-%m-%d %H:%M")}), read-only. '
         f'Generated {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}. Matching = MD5+size against Preview storage ETag; no media downloaded'
         + (' except the --full-hash SHA-256 double check.' if a.full_hash else '.'), '',
         '## Timeline', '', '| in | out | trk | file | take (original) | canvas | generated | model | open |', '|--:|--:|:--|:--|:--|:--|:--|:--|:--|']
    for r in rows:
        e = results.get(r['local']) or {}
        t = e.get('take') or {}
        L.append(f"| {r['start']:.2f} | {r['end']:.2f} | {r['track']} | `{os.path.basename(r['local'])}` | "
                 f"{('`' + t['originalTakeId'] + '`') if t else '-'} | {t.get('canvas', '-') if t else '-'} | {t.get('created', '-') if t else '-'} | "
                 f"{t.get('model', '-') if t else '-'} | {('[open](' + t['link'] + ')') if t else '-'} |")
    L += ['', '## Unique files', '', '| file | status | take (original) | also as | canvas | model / dur | open |', '|:--|:--|:--|:--|:--|:--|:--|']
    counts = {'verified': 0, 'unverified': 0, 'mismatch': 0, 'unmatched': 0}
    for f, e in results.items():
        res, t = e['resolution'], e.get('take')
        if t:
            if res['verified'] is True: st, k = 'matched, byte-identical', 'verified'
            elif res['verified'] is False: st, k = 'ID in name but FILE DIFFERS from take media', 'mismatch'
            else: st, k = 'matched by id in name (bytes not verified)', 'unverified'
            if e.get('fullHash'):
                st += ', SHA-256 ' + ('identical' if e['fullHash']['identical'] else 'DIFFERS')
            also = [x for x in res['ids'] if x != t['originalTakeId']] + [x for x in t['duplicateChain'] if x != t['originalTakeId']]
            L.append(f"| `{os.path.basename(f)}` | {st} | `{t['originalTakeId']}` | {', '.join(sorted(set(also))) or ''} | {t['canvas']} | {t.get('model')} / {t.get('duration')} | [open]({t['link']}) |")
        else:
            k = 'unmatched'
            why = {'no-match': 'not a Preview take in the index (asset, re-encode, or needs `index --deep`)', 'file-missing': 'file not found on disk'}.get(res['method'], res['method'])
            L.append(f"| `{os.path.basename(f)}` | {why} | | | | | |")
        counts[k] += 1
    L += ['', f"Summary: {counts['verified']} verified, {counts['unverified']} by-name-only, {counts['mismatch']} mismatches, {counts['unmatched']} unmatched of {len(results)} files.", '']
    if not a.brief:
        L += ['## Recipes (one per original take)', '']
        seen = set()
        for r in rows:
            t = (results.get(r['local']) or {}).get('take')
            if t and t['originalTakeId'] not in seen:
                seen.add(t['originalTakeId']); L += md_take(t) + ['']
    open(stem + '.md', 'w', encoding='utf-8').write('\n'.join(L))
    links = sorted({t['link'] for e in results.values() for t in [e.get('take')] if t})
    open(stem + '-links.txt', 'w', encoding='utf-8').write('\n'.join(links) + '\n')
    print(f"wrote {stem}.md  {stem}.json  {stem}-links.txt", file=sys.stderr)
    print(f"Summary: {counts['verified']} verified, {counts['unverified']} by-name-only, {counts['mismatch']} mismatches, {counts['unmatched']} unmatched of {len(results)} files.")

def cmd_cut(a):
    """`cut "Client Project" SpotA`: Preview project by name + spot name -> newest Premiere cut -> takes in it."""
    pid, pname = resolve_project(a.project)
    roots = local_roots(a.media_root)
    # Walk one root at a time, shallow first, system drive last, and stop at the first root with hits.
    # Remember where the project was found so the next call is instant.
    memo_path = os.path.join(CACHE_DIR, 'prproj-locations.json')
    os.makedirs(CACHE_DIR, exist_ok=True)
    memo = json.load(open(memo_path, encoding='utf-8')) if os.path.exists(memo_path) else {}
    key = (a.spot + '|' + (a.client or '')).lower()
    hits = [h for h in memo.get(key, []) if os.path.exists(h)]
    if not hits:
        sysdrive = (os.environ.get('SystemDrive') or 'C:').upper()
        ordered = sorted(roots, key=lambda r: r.upper().startswith(sysdrive))
        for depth in (4, 6):
            for root in ordered:
                hits = find_prprojs(a.spot, [root], client=a.client, max_depth=depth)
                if hits:
                    break
            if hits:
                break
        if hits:
            memo[key] = hits
            json.dump(memo, open(memo_path, 'w', encoding='utf-8'), indent=1)
    else:
        hits.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    if not hits:
        sys.exit(f'No saved Premiere project found for {a.spot!r}. Pass --media-root or use incut with an explicit .prproj path.')
    a.prproj = hits[0]
    a.project = pid
    print(f'Preview project: {pname or pid}', file=sys.stderr)
    print(f'Premiere project: {a.prproj}', file=sys.stderr)
    cmd_incut(a)

# ----------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(prog='provenance', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('index', help='build/refresh the project take index (ETag/size per take)')
    p.add_argument('--project', required=True, help='Preview project name or id'); p.add_argument('--kind', choices=['video', 'image', 'both'], default='both')
    p.add_argument('--deep', action='store_true', help='also snowball through searchProjectContext to reach takes older than the newest 250 per sequence')
    p.add_argument('--deep-rounds', type=int, default=8, help='max snowball rounds per sequence (default 8)')
    p.set_defaults(fn=cmd_index)
    p = sub.add_parser('whereis', help='clip path or take id -> original take, recipe, deep link')
    p.add_argument('target'); p.add_argument('--project', help='Preview project name or id (optional when the filename carries a take id)')
    p.add_argument('--json', action='store_true')
    p.set_defaults(fn=cmd_whereis)
    p = sub.add_parser('link', help='clip path or take id -> just the Preview provenance link')
    p.add_argument('target'); p.add_argument('--project', help='Preview project name or id (optional when the filename carries a take id)')
    p.set_defaults(fn=cmd_link, json=False)
    p = sub.add_parser('sequences', help='list sequences in a .prproj'); p.add_argument('prproj'); p.set_defaults(fn=cmd_sequences)
    p = sub.add_parser('cut', help='by names: cut "Client Project" SpotA -> takes in the newest Premiere cut of that spot')
    p.add_argument('project', help='Preview project name (or id)'); p.add_argument('spot', help='part of the .prproj filename, e.g. SpotA, SpotB')
    p.add_argument('--client', help='restrict the .prproj search to paths containing this client folder name')
    p.add_argument('--sequence', help='name or substring; default = highest _NNN')
    p.add_argument('--out', help='output folder (default ./incut-<sequence>)'); p.add_argument('--audio', action='store_true', help='include audio tracks')
    p.add_argument('--brief', action='store_true', help='skip provenance/recipe calls (faster)')
    p.add_argument('--full-hash', action='store_true', help='sanity check: also download each matched take and compare SHA-256')
    p.add_argument('--media-root', action='append', help='where the media share is mounted here; repeatable. Default: scan all drives/volumes')
    p.set_defaults(fn=cmd_cut)
    p = sub.add_parser('incut', help='which takes are in a given .prproj sequence')
    p.add_argument('prproj'); p.add_argument('--project', required=True, help='Preview project name or id'); p.add_argument('--sequence', help='name or substring; default = highest _NNN')
    p.add_argument('--out', help='output folder (default ./incut-<sequence>)'); p.add_argument('--audio', action='store_true', help='include audio tracks')
    p.add_argument('--brief', action='store_true', help='skip provenance/recipe calls (faster)')
    p.add_argument('--full-hash', action='store_true', help='sanity check: also download each matched take and compare SHA-256')
    p.add_argument('--media-root', action='append', help='where the media share is mounted here (e.g. "Z:/" or "/Volumes/MediaShare"); repeatable. Default: scan all drives/volumes')
    p.set_defaults(fn=cmd_incut)
    a = ap.parse_args()
    a.fn(a)

if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    main()

#!/usr/bin/env python3
"""Preflight/apply/undo an explicitly verified delivery filename mapping."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path


def checksum(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def save(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(record, indent=2) + '\n')
    os.replace(temporary, path)


def paths(root, row):
    directory = Path(row.get('directory') or '.')
    if directory.is_absolute():
        raise ValueError('directory must be relative to --root')
    folder = (root / directory).resolve()
    if folder != root and root not in folder.parents:
        raise ValueError('Directory escapes the requested root')
    names = [row['original_name'], row['new_name']]
    if any(not name or name in ('.', '..') or '/' in name or '\\' in name for name in names):
        raise ValueError('Filenames must be nonempty single path components')
    if names[0] == names[1]:
        raise ValueError('Original and new filenames are identical')
    return folder / names[0], folder / names[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--undo', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error('Root directory is unavailable; check the mount/path')

    if args.undo:
        record = json.loads(args.report.read_text())
        if record['root'] != str(root):
            parser.error('Report belongs to a different root')
        selected = [row for row in record['rows'] if row['renamed']]
        if not selected:
            parser.error('Report has no applied renames to undo')
        for row in selected:
            original, renamed = paths(root, row)
            if original.exists() or not renamed.is_file() or renamed.is_symlink():
                raise ValueError('Undo source missing or original name collision: ' + row['original_name'])
            if checksum(renamed) != row['sha256']:
                raise ValueError('Undo refused: bytes differ for ' + row['new_name'])
        for row in reversed(selected):
            original, renamed = paths(root, row)
            os.rename(renamed, original)
            row['renamed'] = False
            save(args.report, record)
        record['status'] = 'undone'
        save(args.report, record)
        print(json.dumps(dict(undone=len(selected), report=str(args.report))))
        return

    if not args.plan:
        parser.error('--plan is required for preflight/apply')
    with args.plan.open(newline='', encoding='utf-8-sig') as handle:
        reader = csv.DictReader(handle)
        required = {'directory', 'original_name', 'new_name'}
        if not required.issubset(reader.fieldnames or []):
            parser.error('CSV needs directory, original_name, new_name columns')
        rows = list(reader)
    if not rows:
        parser.error('Plan is empty')
    sources, destinations = set(), set()
    for row in rows:
        original, renamed = paths(root, row)
        source_key, target_key = str(original).casefold(), str(renamed).casefold()
        if source_key in sources or target_key in destinations:
            raise ValueError('Duplicate source/destination filename')
        sources.add(source_key); destinations.add(target_key)
        if not original.is_file() or original.is_symlink():
            raise ValueError('Missing source or unsupported symlink: ' + row['original_name'])
        if renamed.exists():
            raise ValueError('Target already exists: ' + row['new_name'])
        row.update(sha256=checksum(original), bytes=original.stat().st_size, renamed=False)
    record = dict(root=str(root), status='dry_run', rows=rows)
    if args.report.exists():
        old = json.loads(args.report.read_text())
        if old.get('status') != 'dry_run' or old.get('root') != str(root) or old.get('rows') != rows:
            raise ValueError('Report already records another run; use a new report path')
    save(args.report, record)
    if not args.apply:
        print(json.dumps(dict(preflight=len(rows), applied=0, report=str(args.report))))
        return

    record['status'] = 'applying'
    save(args.report, record)
    try:
        for row in rows:
            original, renamed = paths(root, row)
            if renamed.exists() or checksum(original) != row['sha256']:
                raise ValueError('Source or destination changed after preflight')
            os.rename(original, renamed)
            row['renamed'] = True
            save(args.report, record)
        for row in rows:
            _, renamed = paths(root, row)
            if checksum(renamed) != row['sha256']:
                raise ValueError('Renamed file bytes changed')
        record['status'] = 'complete'
        save(args.report, record)
    except Exception:
        record['status'] = 'failed'
        save(args.report, record)
        raise
    print(json.dumps(dict(renamed=len(rows), sha256_verified=len(rows), report=str(args.report))))


if __name__ == '__main__':
    main()

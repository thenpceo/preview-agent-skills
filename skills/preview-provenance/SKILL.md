---
name: preview-provenance
description: Trace local exported clips and saved Premiere sequences to their Preview takes, provenance links, prompts and references with the bundled read-only helper. Use paths, take IDs, or project/spot names; no media downloads by default.
---

# Preview Provenance

Use `scripts/provenance.py` to identify where a clip came from, retrieve its Preview recipe/link, or map the video files used in a saved Premiere sequence. It never generates, tags, moves, uploads or edits Preview records and never writes the Premiere project. It writes local indexes/reports.

## Resolve the source and scope

- Python 3.9+ and a signed-in Preview CLI are required. Check account/access before querying a project; use `PREVIEW_CLI` for a nonstandard executable.
- Mounted media must be accessible locally. Use `--media-root` for the intended share; stored Mac/Windows paths can be remapped to that mount.
- Prefer an explicit `.prproj` and `--sequence` when the actual current cut is known. The helper's newest-file/highest `_NNN` heuristics are discovery aids, not editorial authority. Report the chosen file/sequence and verify it with existing context before claiming it is the current cut.
- Run commands from this skill folder. Set `PREVIEW_PROVENANCE_CACHE` to a local cache destination if needed. Never publish project caches, reports, private prompts or media merely to share this skill.

## Commands

```sh
# A known saved project and sequence
python3 scripts/provenance.py sequences "/path/to/edit.prproj"
python3 scripts/provenance.py incut "/path/to/edit.prproj" --project "Client Project" --sequence "SPOTA_003" --media-root "/path/to/share" --out "/path/to/report"

# Discover by project and spot name; confirm the returned file/sequence
python3 scripts/provenance.py cut "Client Project" SpotA --media-root "/path/to/share"

# A clip or actual take ID
python3 scripts/provenance.py link "/path/to/clip.mp4" --project "Client Project"
python3 scripts/provenance.py whereis "/path/to/clip.mp4" --project "Client Project" --json
```

A filename containing a recognizable take ID can resolve its project directly. Human-renamed files need the appropriate project index. `--brief` skips full recipe/provenance lookups. Reports include timeline, unique file matches, recipes and Preview links.

## Match evidence and limits

- **Byte-identical:** local MD5/size match usable storage metadata. Quote the exact take/link with this evidence.
- **ID in name but file differs:** the filename's take is a candidate source; changed bytes prevent byte-identity verification.
- **Unverified:** missing local media or unavailable/unusable remote metadata; do not call it a mismatch.
- **Unmatched:** outside the index, transformed media, other assets or unknown source. Say unknown, not conclusively “not from Preview.”

Duplicated takes are traced to an original with the placed copies retained in the report. A direct take link, provenance or an artist tag is not creative sign-off; use the project review records for approvals.

Initial indexing uses CLI metadata and HEAD requests; later runs reuse local cache. The checked helper's sequence enumeration is capped at 250 newest takes. For missing older human-renamed sources, use `index --project "Client Project" --deep` if within scope, then retry; semantic indexing is not guaranteed complete. Verify live CLI capabilities rather than treating the cap as permanent.

`--full-hash` deliberately downloads matched take media for a SHA-256 comparison. Use only when that additional verification/download is requested. Re-encoded, trimmed or externally edited files need a separate source-lineage/similarity audit; exact-byte matching cannot establish their full relationship.

The parser reads saved gzipped Premiere XML. Unsaved edits, unsupported nested structures, missing media and ambiguous sequence selection remain explicit limits. Do not alter project state or silently generate substitutes to fill provenance gaps.

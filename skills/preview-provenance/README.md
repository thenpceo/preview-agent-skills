# Preview Provenance

Traces clips on a mounted media share and saved Premiere cuts back to Preview take links and recipes. Read-only against Preview and Premiere; local indexes and reports are created. No media downloads by default.

Install the complete `preview-provenance` folder in your agent's skills directory. Read [SKILL.md](SKILL.md) for scope, commands and evidence rules.

## Requirements

Python 3.9+ (standard library only), the Preview CLI installed and signed into your own account, and local access to the relevant media. Set `PREVIEW_CLI` for an executable outside PATH and `PREVIEW_PROVENANCE_CACHE` for a custom local cache directory.

## Examples

```sh
python3 scripts/provenance.py link "/path/to/clip.mp4" --project "Client Project"
python3 scripts/provenance.py whereis "/path/to/clip.mp4" --project "Client Project" --json
python3 scripts/provenance.py sequences "/path/to/edit.prproj"
python3 scripts/provenance.py incut "/path/to/edit.prproj" --project "Client Project" --sequence "SPOTA_003" --media-root "/path/to/share" --out "/path/to/report"
python3 scripts/provenance.py cut "Client Project" SpotA --media-root "/path/to/share"
```

The `cut` discovery command may choose a recently modified project/highest-numbered sequence. Confirm that source before describing it as the current edit. Use `incut` with an explicit project/sequence for precise audits. Paths stored on another machine are mapped by share-relative path; explicit mount roots keep the search scoped.

## What verification means

The helper compares local bytes with usable Preview storage ETag/size metadata, follows duplicate-to-original relationships and retrieves recipes/provenance. Missing metadata remains unverified. Unknown/re-encoded/trimmed clips are not conclusively identified by exact-byte matching. Use a separate lineage audit for transformed files.

A link is source evidence, not approval. The tool does not update tags, approval status, library assets or the editorial project. `--full-hash` is an opt-in full-media SHA-256 comparison and downloads the matched sources.

Runtime caches and reports contain private project data. They are not included in this public skill and must stay outside shared packages.

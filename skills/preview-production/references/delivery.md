# Presentations, exports and delivery

Use [Project workflow](project-workflow.md) for producer responsibilities and [Change and approval checks](change-and-approval-checks.md) for exact-version decisions. The producer owns release. Agents prepare/verify authorized packages and distinguish prepared, exported, sent and accepted.

## Select the right purpose and take

A review deck may contain nominated pending work labeled with version/status. A final approved release needs required coverage and valid configured approvals for its purpose. Use the owning production item plus exact current submission/last approved IDs, not canvas dates or a green tag. Preserve the prior approved package when preparing a revision.

Verify the displayed/selected take before export: it can change while browsing alternates. Group download, selected files, sequence export and shotlist export are different scopes. Choose the requested one and compare files to the recorded IDs.

[Shotlist export](https://docs.preview.io/preview/settings-menu#export) creates media plus FCPXML, with selected/stacked alternates, audio, review burn-in and frame-rate options. [Sequence export](https://docs.preview.io/preview/scene-timeline) narrows the scope. Use selected takes for the agreed package; stacked alternates are for an explicitly intended internal handoff. UI availability does not establish a CLI export endpoint or editor compatibility. Verify the intended importer when timeline delivery matters.

Acquire the original through supported download/export/media URLs, not a resized thumbnail. Inspect dimensions, duration, frame rate and readable files. Do not download simply to work around display restrictions. Record source clip/timecodes/handles for performance-based VFX.

## Library filing is a different operation

Typed Character/Location/Prop promotion uses configured reference approval and exact variation attachments. General assets/folders store reusable files. Canvas groups and external storage folders are neither.

Inspect saveTakeToAssets/createAssetFolder/moveAssetsToFolder/updateAsset when filing general assets. Saving a take reuses underlying storage; folders should exist before filing. Folder moves do not move cards or confer approval. Resolve existing destinations before creating duplicates. See [Project Library](https://docs.preview.io/preview/project-library).

## External packages and names

Choose the actual authorized storage root at kickoff. Cloud URLs are not automatically mounted local paths; verify the real mount when needed. File by job / script-or-location scope / phase / item or package. Date working rounds and frozen review/release packs, not automatically reset daily canvases.

Keep a stable review index with Preview scope/sequence links and separate current-review and last-approved package pointers. A round package may combine unchanged earlier approvals with revised candidates, each labeled. Notifications point to the index/records; they are not a second source of truth. Sharing, invites and sending media need explicit authorization for that destination.

Media convention: `Client_Script_Item_v###_YYYYMMDD.ext`.

- Item is stable shot ID or Type-Description: SH01, CHAR-PersonA, LOC-LocationA-Wide, PROP-ObjectA.
- CHAR/LOC/PROP already identify references; omit separate SHEET, REF and phase fields. Use LOOKDEV-Description for temporary exploration and COMMON for shared assets.
- Increment per named item across phases; date is version creation. Phase lives in sequence/folder. Location canvases do not replace the creative Script filename field.
- Preserve meaningful state/angle descriptors. Approval belongs in records, not repeated “final-final” renaming.

Example: `CLIENT_ScriptA_SH01_v003_20261013.mp4`. Preview's native filename template may use positional Sequence/Shot/Take tokens; map exported names to stable titles/take IDs instead of treating positions as script IDs. Preserve missing-shot numbers and original A/B/insert identities. Separate source_shot from export_sequence in a mapping if delivery order differs.

## Package and handoff evidence

Include media, requested review material, approval evidence, recipe/source-workflow links and a [delivery manifest](../assets/delivery-manifest.csv) mapping filenames to exact Preview IDs. Measure files/checksums and verify archive member count/integrity. Keep native source projects in the agreed source folders; a prompt alone does not preserve Blender/Photoshop/Comfy inputs.

Agents derive [selects](../assets/current-selects.csv) from explicit Preview decisions and reconcile differences. Do not export an arbitrary displayed alternate as approved. Track sent only with transmission evidence and accepted only with the relevant response; an exported ZIP proves neither. Name missing approvals/coverage or stale references precisely and prepare other unblocked work.

## Reversible rename helper

Inventory only the requested folders. Record original names/take IDs, bytes, dimensions and SHA-256; inspect source images and lineage against stable item names before making a CSV map. Preflight missing files, duplicate destinations, collisions and numbering. The helper validates file operations, not visual identity or authority.

~~~sh
python3 scripts/rename_delivery.py --root "/absolute/delivery/root" --plan rename-plan.csv --report rename-report.json
python3 scripts/rename_delivery.py --root "/absolute/delivery/root" --plan rename-plan.csv --report rename-report.json --apply
python3 scripts/rename_delivery.py --root "/absolute/delivery/root" --report rename-report.json --undo
~~~

Default is read-only preflight. Apply writes a reversible report before renaming, rejects collisions and rechecks bytes; undo verifies checksums before restoring. Use [rename-plan.csv](../assets/rename-plan.csv) schema, with relative directories and single-component filenames. An unmounted drive, cached thumbnail or partial download is not a completed original file.

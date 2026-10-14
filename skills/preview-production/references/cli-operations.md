# CLI and MCP operations

Checked against CLI 0.2.1 on 2026-10-13. Discover each interface independently; its live schema and host instructions take precedence. Use supported tools rather than private endpoints or editor stores. Production decisions/authorization are governed by [Change and approval checks](change-and-approval-checks.md).

## Setup and discovery

[Official CLI/MCP setup](https://docs.preview.io/preview/cli). Install/sign in only as part of authorized setup, using the intended account; never package credentials.

~~~sh
npm install -g @previewio/cli
preview auth login
preview context whoami --json
preview context current-org --json
preview projects list --json
~~~

The inspected package requires Node 18+. Resolve the executable if outside PATH. Hosted connector: `https://mcp.preview.io/mcp`. For requested local connector configuration, inspect `preview mcp init --print` before applying a supported `--target`; it is not routine production work.

Use `PREVIEW_CLI_SKIP_UPDATE=1` per invocation for reproducible checks instead of changing global update preferences. Read version/help/catalog and only relevant schemas:

~~~sh
PREVIEW_CLI_SKIP_UPDATE=1 preview --version
PREVIEW_CLI_SKIP_UPDATE=1 preview tools list --json
PREVIEW_CLI_SKIP_UPDATE=1 preview tools schema createScene --json
~~~

Prefer JSON request files with `preview tools run TOOL --file request.json --json`. JSON commonly uses an ok/data envelope: inspect exit status and error/needs_input outcomes, retain receipts and read back changes. A successful transport is not a successful mutation.

## Resolve native records

~~~sh
preview projects get --project-id "$PROJECT_ID" --json
preview canvases list --project-id "$PROJECT_ID" --json
preview stories list --project-id "$PROJECT_ID" --json
preview scenes list --story-id "$SHOTLIST_ID" --json
preview shots list --scene-id "$SEQUENCE_ID" --json
preview library list --project-id "$PROJECT_ID" --json
preview takes get --take-id "$TAKE_ID" --json
~~~

Use product names in conversation: shotlist (storyId), sequence (sceneId), canvas/Studio (canvasId). They are distinct. Search with searchProjectContext/resolveEntityReference, then retrieve focused getStoryContext/getSceneContext/getShotContext/getCanvasContext/getTakeContext/getTakeProvenance. Follow useful source relationships from discovery rather than stopping at broad name lists.

Paginate context/list results as indicated. listCanvasGroups returns empty groups and at most ten member take IDs per group; follow nextOffset and do not mistake samples for full membership. Canvas output comes from listCanvasTakes; listSceneTakes is sequence metadata and may include unassigned files. Inspect actual output, lineage and assignments before choosing references or a current take.

Generation schemas currently require the active canvasId. sceneId stores metadata and does not redirect output. Activate/verify the intended canvas through the supported interface when required; do not pass a different canvas hoping it changes the UI. groupId must be a returned group on that canvas, not a generationSessionId.

## Structure and shared metadata

For the **first write to a new/template shotlist**, inspect createScene and use `reconcileStarter: true` when supported. It atomically reuses the unused starter and IDs, creates in an empty shotlist, or returns `needs_input` without writes if meaningful content exists. On needs_input, read the existing structure and resolve placement with the user. Never retry automatically with false to bypass that result; false is for an intentionally authorized append. Known shots can be created with the sequence in the same call.

Inspect createCanvas/renameCanvas, createStory, createScene/updateScene, batchCreateShots and batchUpdateShots for the intended change. batchUpdateShots currently accepts 2–20 records; use updateShot for one. Omitted fields are unchanged; nullable fields clear when null. Assignment/link arrays replace their lists, so preserve unrelated members unless replacement is intended. Fields include title, brief, internal_note, shotType, cameraMovement, assigneeIds, dueDatetime, characterIds/locationIds/propIds and action/dialogue metadata. Camera movement enum uses `track`, not `tracking`.

Retrieve actual project status/tag IDs. `updateShotStatus` currently maps only todo/in_progress/review/complete; it does not expose every custom menu state. Use a supported full-status field when offered or the normal UI for the exact project label/ID. Native menu categories and CLI status types differ; do not invent a category such as review or confuse Internally Approved with complete. Custom menu/category and canvas-section layout controls may need UI; recheck current support.

assignTakeToShot/batchAssignTakesToShots bind existing files; they do not move cards. **A take has one shot assignment per shotlist.** Inspect current assignments before moving it to another item in the same shotlist; preserve other scopes and resolve any conflicting nomination. Do not copy a take solely to dodge this limit. Use distinct required deliverable takes or supported source/reference links for inputs. Verify the displayed/select-for choice separately when APIs do not expose it.

One shot can receive multiple takes; batch assignment may repeat its shotId for distinct takes. Use this for required A/B/C assets under one logical shot. Description maps to brief in the inspected shot/sequence schemas. createStory currently has no description field: recheck live support/UI, and do not invent a payload property. If unavailable, put the short shotlist purpose in its existing guide or lead-owned overview note. For an authorized consolidation, save rows, preserve full old briefs in Notes, attach/verify any donor assets before retiring redundant rows through supported removal, and retain a source-ID/part mapping. Prefer recoverable retirement and verify the actual operation; do not assume native restore support. Compare substantive metadata when get/list DTOs differ, without ignoring content conflicts. Do not assume take assignment preserves the displayed choice or exact approvals.

## Typed references and attachments

Use listLibraryItems/getLibraryItemContext before creating duplicates. Read variants, attachments, usage and returned referenceToken values. Inspect the actual chosen source; never infer attachment identity from indices, ID order or labels. Reuse returned canonical tokens exactly instead of constructing library tokens.

createLibraryItem creates master metadata, not a generation or approval. updateLibraryItem manages name/details. Read the existing default's returned index, then use renameVariant to rename Default to `V001`; do not create a duplicate. addVariant creates sibling version/look folders such as `V002` or `Pajamas V001` and returns the index. Descriptive deltas and exact review decisions go into the entity's shared Details, labeled by folder name. Its variantDescription is omitted/empty in the checked schema. Preserve existing folders and attachments.

Save artist-selected images directly into the intended version folder before review: attachImageToLibraryItem for generated takes, attachUploadedImageToLibraryItem for uploaded sources, or copyLibraryItemAttachment to reuse a stored image without duplicating bytes. Pass the exact intended variantName/index and verify returned attachments and source preservation. Multiple images are supported per folder. These operations are submission/storage, not creative approval. linkLibraryItemToShot connects master metadata; it is not media approval. Reference sequence assignment is not a prerequisite.

Before a new prompt, resolve the latest populated numeric version in the requested base/look family through getLibraryItemContext. Use that folder's/attachments' returned canonical tokens and verify resolved images/model limits; a bare master token does not guarantee latest-folder selection. Record folder name/index, exact IDs and pending/approved state in the recipe. See [Versioned reference library](versioned-reference-library.md).

General assets use createAssetFromUpload/saveTakeToAssets/folders; they are different from typed references. SaveTakeToAssets reuses underlying storage without copying bytes. Resolve the folder before filing. Uploaded storage keys and asset/take IDs have different purposes; use exact returned values.

~~~sh
preview media upload-file --file "/absolute/path/reference.png" --json
preview takes upload --scene-id "$SEQUENCE_ID" --canvas-id "$CANVAS_ID" --storage-key "$STORAGE_KEY" --kind image --file-name reference.png --json
~~~

Upload only within the authorized destination/scope. Group placement is separate and may require UI.

## Scripts and the shared guide

Use listScripts before creating duplicates. getScriptContext reads persisted synchronized content; unsaved editor text and pending suggestions are excluded. Read as needed using offset/limit (currently up to 50000), optionally scene-outline/sceneId. Continue with the same documentVersion as expectedVersion; restart from offset 0 if it changes. Partial pages are not a complete source.

writeScript replaces the entire document with Fountain/plain screenplay text and synchronizes it to live editors. It currently has no conditional version-write field. Read complete content, save the prior version, verify authority for the replacement, re-read immediately before writing, and stop if changed. Do not overwrite unsaved human work or pending suggestions. This CLI path needs no Tiptap hash/editor calls, even if another tool description mentions an editor workflow.

For a human-facing how-to, adapt [workflow-guide.md](../assets/workflow-guide.md). Fountain `!` forces action/Text so standalone uppercase labels are not mistaken for character dialogue; `**bold**` labels and blank lines provide readable formatting. Markdown heading markers are not a promise of native heading blocks. Verify actual rendered formatting plus persisted content; native Scripts support five screenplay block types and inline formatting. Keep the guide separate from the screenplay. Import uploaded screenplay files with importScript using the named destination and its emptiness rules; do not repeat uncertain imports blindly.

## Generation, costs and recovery

Inspect batchGenerateImages/batchGenerateVideos and model capabilities immediately before use. Checked batches accept 1–20 items; one item is a valid batch. Model limits/settings/destination determine batching. Use canonical @take/@asset or returned library tokens in prompts when supported. There is no generic references array in the checked schemas; start/end frame and motion-video fields have distinct roles. Do not inject worker-owned threadId.

The checked video schema supports **`videoReferenceMode: "edit"`** for models whose capabilities allow video editing. It re-renders one supported-length clip referenced in the prompt, without start/end frames; duration/cost derive from the source even if duration says otherwise. `reference` is the default. Check actual model support, clip and stored mode/bindings; an edit prompt alone is insufficient. Unsupported exact UI modes/Quick Actions/masks/worlds need supported UI, not guessed flags.

~~~sh
preview tools schema estimateGenerationCost --json
preview tools run estimateGenerationCost --file estimate.json --json
preview tools run batchGenerateImages --file batch-images.json --json
preview tools run waitForGeneration --file wait.json --json
~~~

Set multiShotCount to intended count for cost preflight. Keep requested count, preflight estimate, submission estimate/charge and actual billed credits distinct. Use returned Camera Bag/style IDs and permitted values; preset catalogs do not support every prose camera choice.

After timeout inspect the saved returned IDs and activity/provenance before retrying. Wait only on the actual new takes, especially for reused sessions. Cancel when explicitly requested or when an active run is verified misconfigured, through the supported cancel operation; cancellation is best effort, not evidence of a refund. Follow host generation-card contracts and queued-only task boundaries.

`scripts/discover_preview.py` captures help/catalog/core schemas read-only; `--schemas` focuses it and `--all-schemas` expands it. Keep captures private and outside the shareable skill. Technical flags do not grant task authorization or creative acceptance.

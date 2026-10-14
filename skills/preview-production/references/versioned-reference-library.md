# Versioned reference library

Use this workflow for Characters, Locations and Props. The library is the home for selected reference images and their review; a reference shotlist/sequence is not a staging requirement. Film shots still use Production sequences and statuses.

## Master entries and version folders

Create one stable master entry for each character, location, prop or scene extras group. Rename its existing Default folder to `V001`, preserving images and identity; do not add a second `V001` merely because the first folder was implicit. These UI folders use Preview's variation APIs. Version naming is our workflow convention, not a native version-history or approval feature.

Artists explore on the canvas, then save the images they like directly into `V001` for review. Keep the source takes on the board and retain their IDs/links. Multiple images fit in one folder: character angles/details, location coverage, prop views or different members of an extras group. Extra views of the same version go in that folder too; review the added images explicitly.

For an iteration, create `V002`, then `V003`, and so on under the same master. Put the revised images there and retain earlier folders and decisions. Include still-valid images needed for that version's usable set alongside the changes, copying attachments by reference where supported. Do not overwrite an older version or silently mix images from earlier folders into a new prompt.

## Named looks and states

Wardrobe or other deliberate states are sibling version folders beneath the same master entry, not separate characters or nested version trees:

```text
Characters / Main Character
  V001
  V002
  Pajamas V001
  Pajamas V002
  Evening Clothes V001

Locations / Main Location
  V001
  V002
  Night V001

Props / Main Prop
  V001
  Damaged V001
```

Use the agreed descriptive look/state name followed by `V###`. Version numbers advance independently within each family: `Pajamas V002` does not replace the base `V002`. Several angles of the same look/version share its folder.

## Extras are a group

Use one Character master for each needed background ensemble, such as `Scene Extras`, `Seville Tourists`, `Flamenco Band`, `Boat Guests`, `Atrium Guests` or `Tapas Patrons`. Do not create a top-level character per background extra by default. Preserve individually required principal roles.

If four extras are needed, store their four member images together in that group's `V001`, or store one composite showing all four. Either approach is supported by this workflow; artists choose based on the intended shot/model. Label members and specify who does what when the shot needs individual performance mapping. Multiple files are separate people in this case, not different views of one person.

One group does not turn several images into one model reference slot. Inspect the live model limit: four individual images consume four slots; a single composite is one image. Reference inclusion does not guarantee the model renders every member correctly. Compositing or generating a test is separate work and requires the applicable authorization.

## Review the images in their folder

Saving a selected image in the library is submission for review, not approval. Keep the current version's owner, review state, exact image IDs, feedback and decision evidence in the entry's shared Details/description, labeled by folder name. Link the original file/canvas comments when folder or library-image comments are unavailable. Do not invent native folder status fields.

For each version, retain current submission and last-approved image set separately, with approver, date, purpose/brief validity and source links. A revision starts pending review and does not inherit an earlier decision. An added view needs its own review; prior decisions remain tied to the exact images they covered. Review shared assets once and reuse the master entry across shots.

The latest folder is the current working reference even while review is pending; label those inputs provisional. Latest and approved are separate facts. If a specific run or release requires approved references, verify the exact selected set or report the pending approval dependency. Do not silently fall back to an older approved folder. Final approved delivery still requires the configured decisions.

Do not create a separate References sequence merely to review these folders. Retain existing sequence records, media and decisions as history unless the user authorizes a live migration or removal. Updating this skill alone does not authorize that migration.

## Select the latest version when tagging

For a new prompt, choose the master entry, then the latest populated `V###` folder in the intended base/look family. Compare the numeric version, not creation date, row order or alphabetical placement. Empty future placeholders are not usable references. Read current folder indices, attachments and actual images; duplicate populated version names need resolution before choosing.

Preview's documented `@` picker lets you drill into variations and images. A bare master-entry tag can resolve the default rather than the latest named folder; this skill cannot change Preview's routing. In UI, explicitly choose the latest folder and required images. In CLI/MCP, read `getLibraryItemContext` and reuse that folder's or those attachments' returned canonical reference tokens exactly. Verify the selected chips/resolved inputs and image count against the model limit. Never mix all historical folders or base and named looks just because they share a master.

Select all images from that current folder when they are required and fit the model; otherwise choose the needed members/views or an authorized composite. Record master ID, look, folder name/index, exact attachment/take IDs, canonical tokens and review state in the recipe. Keep historical generations bound to their original inputs. Reuse for a new run re-resolves the current version; an explicitly requested historical version or approved baseline is pinned and recorded as an exception.

Product sources: [Project Library](https://docs.preview.io/preview/project-library), [Referencing with @](https://docs.preview.io/preview/at-references). The version naming, group identity and direct-folder review process are team conventions.

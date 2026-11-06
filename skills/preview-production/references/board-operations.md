# Canvas UI, staging and comments

Read [Project workflow](project-workflow.md) for script/milestone/daily-group conventions and [Change and approval checks](change-and-approval-checks.md) before altering established work. This file covers supported UI mechanics and evidence.

## Script categories and milestone canvases

Canvas categories appear as Sections in the observed canvas picker. Use one per script and keep milestone canvases inside it. The observed normal UI supports Section actions → Rename and Canvas actions → Move to → existing section. Category moves change navigation membership, not the contents of the canvas. Verify every existing canvas remains under its intended script. Retire a former category only after confirming it is empty. Alphabetical sorting can use numbered milestone titles such as `Script A · 01 References`. Recheck live tools for category support before choosing UI; do not invent a section API or rebuild canvases to work around missing support.

## Resolve the actual canvas

Verify canvas/group IDs, representative files, exact source references and assignments. Refresh after human changes or duplication: copies can have new IDs. A matching thumbnail/name is not identical lineage. Checked CLI lists/targets groups but lacks precise card-coordinate/group-layout mutations; recheck live support before choosing UI.

Use normal computer-use UI, or human help when UI is unavailable. Do not edit DOM styles/editor stores, invent geometry flags or use undocumented clipboard payloads. Create/rename daily groups within the delegated work, and **always use the group-level Organize action for the active group**. Preserve unrelated groups, notes and canvas positions; a documentation update alone does not authorize reorganizing live boards.

## Groups and placement

[Groups](https://docs.preview.io/preview/groups) can be created through canvas context menu or selected-file Group actions. Normal UI supports names/colors, links, duplication, export, ungrouping and group generation targeting. A Collapse group control was observed in the checked UI; use it when available for earlier daily groups. Flat groups are the workflow's organizing unit, with no nested groups.

Enter targets the group's generation session in Files view; the prompt-box group chip changes destination. That session ID is not the shape groupId used by generation tools. Ungroup retains files; recover accidental grouping with normal Undo/Ungroup and inspect the result.

Use pasted text headings and sticky notes for brief/index/handoff. To save member files to library, use supported Add to/file operations for selected reference sources, with review state recorded separately; a group is not a Character/Location/Prop entry.

[Next Take Box](https://docs.preview.io/preview/next-take-box) is a UI placement target. Its grid width can cause a row to settle below the intended point; group targeting uses group placeholders. After new takes are placed, use Organize on the intended group and verify its chronological grid. Leave unrelated groups unchanged.

For each new working date, put the new same-scope group immediately to the right of its predecessor, aligned at the top with enough space to avoid overlap. Use `YYYY-MM-DD - ScriptName - item/scope - initials`; reuse today's matching group rather than creating another feedback round.

The documented group menu offers **Set max columns** and **Organize**, which arranges files into a grid. Use that auto-organize control, then verify oldest-to-newest reading order across rows (left to right, then top to bottom) from take creation timestamps. The docs do not promise a chronological sort option: inspect the live UI/API and use only supported ordering controls. If the resulting order cannot be corrected through supported controls, report that limitation instead of claiming it is sorted or inventing an API. Stable ties can retain current order. Newer completion/import times do not make an older source take a new generation.

Verify membership, chronology, non-overlap and retained unrelated work in the native canvas. Capture useful screenshot/geometry evidence. A take count or local contact sheet does not prove native ordering. Delete only identified unusable throwaways within authorized work; keep mediocre and good takes. Inspect whether the current Delete action removes a canvas shape or the underlying take, and check review/library/downstream usage before deletion. Never delete a whole group to remove a few bad takes.

## File surfaces and recovery

- **Files view:** this canvas's output feed; stage/filter large batches without putting all exploration on canvas.
- **History:** project-wide files/uploads/worlds, including media absent from the current board.
- **File View:** one-file inspector for actual media, prompt/settings, references, provenance and comparisons.
- **Library:** typed reusable entries/variations and general file folders; external filesystem exports are separate copies.

Photoshop returns may appear in History without placement. Find/inspect the returned take before copying, saving or assigning it; missing canvas placement is not a failed sync. Provenance records derivation, not acceptance.

## Comments

[Comments](https://docs.preview.io/preview/comments) can attach to a canvas file or sit on empty space. They support image attachments, mentions and threaded replies. Canvas drawings/arrows/lines/boxes provide spatial feedback; they are not File View drawing tools. Moving a canvas file retains attached comments.

File View → Comments supports synchronized pins for **generated files**, not reference/library images. Its Comments tab must be active to pin. For unsupported sources use an adjacent canvas comment with exact ID/link. Retrieve discussion in the Comments sidebar; keep feedback/replies on the original version/thread and decision summaries in Production Notes. Follow project approval policy before resolving a decision or changing official status.

## UI failures

Read the host's computer-use documentation; get fresh state after navigation/scale changes and do not reuse stale coordinates. Stop competing when the human takes over. Use a separately permitted controlled surface when available.

After repeated unreliable drags/timeouts, preserve the exact pending row/take/selection list and last verified state. Continue independent authorized data work or local preparation. A device lock or disconnected UI can require human action; elapsed time is not approval or proof of completion. Report remaining native layout/export work clearly.

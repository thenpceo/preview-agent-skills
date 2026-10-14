# Project workflow

Adapt this preferred structure to the brief and existing setup. Read [Change and approval checks](change-and-approval-checks.md) before altering established work or recording decisions. Commands belong in [CLI operations](cli-operations.md); maintain shared Preview records rather than a second custom tracker.

## Lead: set up the job

1. **Choose scripts and milestones.** Create one canvas category per creative script. Inside each category, create persistent canvases for that script's milestones: References / First Frames / Animation, or Previz + Lookdev / Animation / Final VFX. Use globally clear titles such as `Script A · 01 References`, `Script A · 02 First Frames`, `Script A · 03 Animation`; numeric prefixes keep the intended order under alphabetical sorting. A one-script job still has one script category. Organize its locations as groups or named rows inside the milestone canvases; add a location-specific continuation canvas only when the lead explicitly chooses it. Canvas categories and shotlist sequences are separate structures.
2. **Inspect and adapt.** Replace confirmed untouched placeholders within setup authorization. Preserve intentional sequences, canvases, groups, shot names and library identities unless their modification is explicit. Create the actual required count rather than forcing two canvases/three sequences on every job.
3. **Match shotlists.** Start with one shotlist per script, with a sequence per independently reviewed deliverable. Preserve an established, agreed location-based review split unless the user requests a change; changing canvas categories alone does not authorize rebuilding the review breakdown. The basic template has References, First Frames and Animation. Complex jobs may need Previz, Lookdev Frames, Location Studies, Clean Plates, AI Draft and Final VFX. One milestone canvas may support several deliverable sequences. A location still, 10-second study and clean angle need separate slots if separately accepted. Optional worlds/scans get slots when required.
4. **Define stable names first.** Agree script shot IDs/descriptions and asset IDs. Preserve them across phases; row positions are not production identities. Keep editorial order in shot sequences and an explicit full-film assembly order when split by location. Reference-view items are not film shots.
5. **Brief and assign.** Fill purpose/acceptance criteria, framing/angle, movement/lens intent, action/dialogue, duration and interior/exterior where relevant. Link source media and define roles: appearance, composition, geography, acting, timing or motion. Link Character/Location/Prop entries. Set real assignee/priority/due date when known; record reviewer/dependency/next action. Start required work To Do and leave unknowns explicit.
6. **Precreate reusable metadata.** Create typed identities/locations/props and deliberate states before approved media exists. Record extras' associated locations and reuse their identity when they move. Speaking roles may have approved voices with verified model binding. Candidate media remains in review until configured approval.
7. **Prepare canvases.** Use flat groups, pasted headings and sticky brief/active-work/handoff notes. Reference canvases may separate LOC, CHAR and PROP rounds; frame/animation groups may cover single shots or batches with named rows. Reference Sandbox stores context/exploration; Archive retains older work. These are layout conventions, not library identities.
8. **Configure review and delivery.** Record internal reviewer, reference approver, final creative approver and producer/release owner. Map existing tags/statuses before changes. Choose external storage root/specs and publish an adapted workflow-guide Script without replacing the screenplay or another person's guide.

[project-setup.json](../assets/project-setup.json) is an optional specification, not an API payload. The lead's agent builds/maintains shared records directly. Script edits do not automatically update shots; reconcile the breakdown after brief changes.

## Artist: iterate, nominate, hand off

Open the assigned scope/phase item. Read brief, current candidate, last approval, comments and exact approved attachments. Resolve active canvas/group. Start from the actual take/provenance rather than a remembered prompt.

Group naming: `YYYY-MM-DD - scope/item - [phase when needed] - R##[-B##] - initials`.

Example: `2026-10-13 - LOC-LocationA - R01-B02 - AB`. Date is pass start; handoff timestamps record later activity. Initials identify pass author; assignee identifies current ownership.

Each row holds one named view/character/prop/shot; attempts go left to right. R00 is initial work. R01 includes only feedback changes; unchanged approvals stay in their owning slots. Round is not filename version v001. Continue a crowded round in B02, collapse completed groups or archive deliberately. Keep canvases across days; if an occasional continuation is needed, retain the earlier canvas and update the active link. Preserve manual placement; never use Organize/Tidy up on existing layouts.

Working tags: In Progress, Interesting, Rejected, Needs Review, Final. These are shared project tags; use Author filtering for personal browsing. Final is an artistic nomination. Reuse equivalent existing tags without silently relabeling the project's menu.

Submit the existing take through Select for or supported assignment tools. Confirm shotlist, sequence and stable item, deliberately display the candidate, set Needs Review, and record exact version/link plus what changed/needs a decision. Assignment neither requires download/reupload nor moves its card. Keep the last valid approved choice separately. Submit useful choices, not all generation history.

Revise from exact feedback and reuse the recipe into the correct round/batch. Change only requested variables. Save effective prompt, model/settings, precise reference versions/roles, parent take IDs and actual start/end/motion/edit bindings; external work needs native source/workflow versions. Verify inputs after Reuse: a prompt alone is incomplete.

Before shift end, update Notes with candidate, last approval/validity, active group, recipe/source paths, feedback/blocker, next action/owner, updated timestamp and live job IDs. Someone else should resume without private chat history. Use [handoff](../assets/handoff.json) and [recipe](../assets/recipe.json) templates when useful.

## Reference review and promotion

One owning References item per independently reviewable asset/view/state. Four location views need four review slots but may all attach to one Location variation. Approved sets may combine unchanged R00 and revised R01 views. Keep existing slots across rounds; shared assets have one approval owner and other scopes reuse their library entries.

Draft metadata can exist early. After configured approval, attach the exact approved media to its intended variation, preserve source take/review links and record mapping/evidence. Variations describe Day/Evening, wardrobe or narrative state; iterations belong to history. Use specific approved attachments in prompts, not every library image. Baselines are recorded sets/snapshots; do not assert a native sequence lock or library approval field.

## Review: comments and decisions

For generated takes, open File View → Comments and pin feedback to the relevant image area. Canvas comments attach to files or sit beside groups; drawings/arrows/boxes are canvas-comment features. Retrieve threads through Comments sidebar, reply in the original thread and tag the owner when useful. For references/library images where File View pins are unsupported, comment beside the canvas source with its exact ID/link. Production Notes carry item briefs, decision summaries and next action.

Name version, what stays, what changes, next owner and whether approval is blocked. Video feedback includes timecodes. Example: “SH08 v003 — keep framing; warm lighting and remove the background person.” Resolve only checked fixes; a newly rendered take does not close review.

Follow configured status authority. Record exact-version evidence/date/approver; the producer/agent may enter a genuine decision received elsewhere. Presentation, completion or green tags are not decisions. Reference, frame and animation approvals are independent.

Keep two explicit fields:

- **Current submission:** exact take/version/link, phase and review status.
- **Last approved:** exact take/version/link, phase/state, approver/evidence/date and valid for current brief yes/no.

Displayed alternates can change during browsing. Do not use that display alone as the approval record or erase older decisions on resubmission.

## Producer: presentation, feedback, release

Production's synced Shotlist provides ownership/status/notes, Storyboard visual review, and Kanban/status filters queues. Useful shared views include My Open Items, Needs Internal Review, Awaiting Final Approval, Changes Requested and Final Approved. Missing/conflicting-current checks need an exact-ID audit; do not invent a dedicated filter.

Retrieve presentation media from the exact nominated item/take. Label pending work with version/status; record Preview link/take ID with slides or manifest so feedback returns to that asset. Final release needs valid exact approvals for its purpose. [Delivery](delivery.md) covers selection, export, storage and naming.

Leave feedback on take threads and summarize action/owner in Notes. Record source and exact version for meeting decisions before status changes. Messaging links point to shared records; sending messages or creating review links is a separately authorized action.

For Final VFX using live-action/graybox source, record clip, shot bounds, frame rate, handles and occlusions. Source performance/timing/gestures/eyeline/camera govern acting and motion; approved environments govern appearance/space. Previz or AI stand-ins remain planning sources unless explicitly assigned another role.

## Names and records

Media: `Client_Script_Item_v###_YYYYMMDD.ext`. Item is a stable shot ID or Type-Description: SH08, CHAR-PersonA, LOC-LocationA-Wide, PROP-ObjectA. Types already identify references; omit separate SHEET/REF/phase tokens. Use LOOKDEV-Description for temporary exploration and COMMON for shared script assets. Version increments per named item across phases; date is creation. Phase belongs in sequence/storage folder; location based canvases do not replace the Script filename field.

Notes, recipes, [current-selects.csv](../assets/current-selects.csv) and [delivery-manifest.csv](../assets/delivery-manifest.csv) preserve exact IDs/decisions. Agents derive/reconcile these from Preview rather than maintaining a competing tracker. Freeze review/release package versions; a stable index keeps current-review and last-approved pointers separate.

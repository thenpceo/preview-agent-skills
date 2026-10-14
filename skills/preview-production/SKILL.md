---
name: preview-production
description: Set up and manage Preview projects, canvas workflows, shotlists, reference libraries, generation, review, artist handoffs, and delivery using CLI/MCP and supported UI. Use for preview.io production work, not macOS Preview or deployment previews.
---

# Preview Production

Keep each deliverable's identity, current submission, approved version, recipe and next owner discoverable in the shared project. This skill covers project management and technical production. Resolve the user's account, project, team, storage and capabilities at runtime.

## Choose relevant instructions

| Request | Read |
| --- | --- |
| Set up/restructure a job; coordinate artists; maintain status or library references | [Project workflow](references/project-workflow.md) and [Change and approval checks](references/change-and-approval-checks.md) |
| Create, rename, replace, merge, delete or approve existing records | [Change and approval checks](references/change-and-approval-checks.md) before mutation |
| Use CLI/MCP; recover context, inputs or Scripts | [CLI operations](references/cli-operations.md) |
| Work on canvas layout, round groups, staging or comments | [Board operations](references/board-operations.md) |
| Prepare prompts, references, source edits or visual QA | [Production lessons](references/production-lessons.md) and the generation section below |
| Prepare presentations, exports, packages or filenames | [Delivery](references/delivery.md) |

Load only what the task needs. [Documentation guide](references/documentation-guide.md) maps official docs; [sources](references/sources.md) distinguishes verified capabilities from conventions. [README](README.md) covers installation and examples.

## Project model

Promote this default, adapting it to the job:

**Project → script canvas categories → persistent milestone canvases → dated, initialed round groups → named item rows → attempts.**

**Project → one shotlist per script/location scope → deliverable sequences → named shots/reference review items → assigned takes and official status.**

These are parallel structures: a canvas category does not contain a sequence. Each script category contains that script's milestone canvases, such as References / First Frames / Animation; other jobs may use Previz + Lookdev / Animation / Final VFX. Name canvases unambiguously, for example `Script A · 01 References`, `Script A · 02 First Frames`, `Script A · 03 Animation`; ordinal prefixes keep milestones in order under alphabetical sorting. Matching shotlists connect visual work to production records. Start with one shotlist per script; retain an agreed location split when it serves review without automatically restructuring it. Locations are work groups or named item rows inside milestone canvases, with shared approved library references. Date groups and review packages instead of resetting canvases daily. Assignees identify ownership; canvases are shared by script and milestone rather than artist. Apply this convention to new setups; migrate existing categories only when authorized.

| Product concept | Technical identity | Meaning |
| --- | --- | --- |
| Project | projectId | Production container |
| Canvas/Studio | canvasId | Project visual workspace |
| Shotlist | storyId | Independent sequences/shots |
| Sequence | sceneId | Ordered review items; not a canvas |
| Shot/review item | shotId | Stable title, brief, owner, status, references and takes |
| Take/file | takeId | Exact media, inputs and lineage |
| Canvas group | groupId | Visible work container; not generationSessionId |
| Character/Location/Prop | library item + variation | Reusable identity/set/object and deliberate visual states |
| General asset/folder | assetId + folder name | Reusable files; distinct from typed entries and groups |
| Script | scriptId | Screenplay or guide; edits do not update the breakdown automatically |

Keep stable script shot IDs in titles across phases; row positions may change. **One logical film shot gets one sequence row.** Put required A/B/C panels or parts in its succinct Description/brief and attach their media to that same row; do not create separate SH07A/SH07B or Panel 7A/7B rows. Give shotlists/sequences a short purpose description where supported, and put detailed workflow, feedback and lineage in Notes. For a multipart shot, record the required asset set and exact selections/approvals per part; a displayed take alone does not establish full coverage. Read [Project workflow](references/project-workflow.md) for examples and safe consolidation. Typed library entries may exist as draft metadata at setup. Promote their approved attachments only after the configured reference approval, with one owning review item per shared asset/state.

## Essential checks

1. **Inspect before changing.** Resolve the account, organization, project, scope, canvas/group and records. Classify structure as unused placeholder, established work or uncertain. Preserve established work; ask a focused add/modify/replace question if the change is not already explicit. Empty media does not prove a record is disposable.
2. **Respect existing authorization.** Proceed with reads and authorized additions. Do not ask again for an exact change already approved. Setup permits adapting confirmed untouched placeholders, not silently replacing a lead's sequence, canvas, shot breakdown, library entry, Script or review decisions.
3. **Configure approval authority.** Find the reference approver, internal reviewer, final creative approver and producer/release owner. A common arrangement is producer approval for references and director approval for film shots; use the actual project policy. If authority or exact-version approval is missing, ask before promotion or an approval transition. Do not invent native approval fields or hardcode roles across jobs.
4. **Preserve candidate and approval separately.** Record current submission and last approved take for item, phase, state and brief. A revision does not inherit approval. Tags, filename “final,” newest date, rightmost position, provenance and provider completion are not human decisions.
5. **Keep manual layout.** Do not use Organize group/Tidy up on existing artist layouts. Create new groups through supported UI when delegated. No nested groups, hidden editor-state writes or invented coordinate fields. Read [board operations](references/board-operations.md) before visual changes.
6. **Nominate the existing take.** Assign it to the matching review item, confirm the displayed choice, set Needs Review and record recipe/next action. Keep unchanged approvals across rounds. Library promotion preserves the source take and owning review record.
7. **Protect shared edits.** Re-read before replacement, merge only requested fields and preserve unrelated notes/media/owners. Stop on conflicts. Whole-document Script writes need a saved prior version and specific overwrite authorization. Rollback guidance does not grant permission to remove unrelated work.
8. **Report evidence accurately.** Prepared, queued, completed, visually checked, internally accepted, finally approved, exported, sent and accepted are separate states. Verify native readbacks and actual pixels/UI-only selections where needed. The producer owns release; agents record genuine decisions and execute authorized operations.

When a check needs a question, identify the exact existing record or missing decision and the consequence. Ask only for the unresolved choice and continue independent preparation. The full decision table and question examples are in [Change and approval checks](references/change-and-approval-checks.md).

## Generation and technical execution

Use CLI/MCP for supported data operations and generation, and normal UI for features absent from current schemas. Check live help, fields and model limits; old examples do not establish current access or prices.

Before a paid run, verify the authorized scope/settings/inputs/count/spend, selected reference versions, destination and model. A complete authorized batch can cover its constituent calls; extra variants/retries need authorization covering them. Preparing a composer or installing this skill does not authorize credits.

Prepare all ready independent items and batch them when settings/destination match. Respect the live item cap; split for cap, incompatible settings/destinations or unfinished dependencies. Save request, estimate and receipt. After timeout inspect returned job/take IDs before retrying; never repeat successful items to make a cleaner batch.

Reference maps identify each source's role: identity, geography, object, composition, performance or motion. Use canonical returned tokens and actual start/end/motion/edit bindings. An opening still is one instant. Preserve requested source performance/timing and change only named variables in source-faithful edits. Verify native Edit through its supported setting; prose alone does not activate it.

For likeness refusals, present the supported agreement/check flow and wait for actual human agreement. Do not accept terms for the user or evade refusals through another model/reference.

Follow host generation-card instructions. A queued-only assignment ends after verified submission and a resumable handoff. Otherwise verify completion and useful-size visual quality as required. If UI fails, report pending selection/layout/export work and continue independent authorized work; never fabricate endpoints.

## Portable resources

- [Project setup](assets/project-setup.json): script categories, milestone canvases, review scopes, owners, approval policy, coverage and destinations.
- [Handoff](assets/handoff.json), [recipe](assets/recipe.json), [selects register](assets/current-selects.csv), [delivery manifest](assets/delivery-manifest.csv): exact-version lineage/decisions derived from Preview, not a competing tracker.
- [Workflow guide](assets/workflow-guide.md): generic human-facing guide to adapt into a project Script; keep the creative screenplay separate.
- Request/run templates under `assets/` are illustrative. Replace placeholders and validate live schemas. Never bundle credentials or real production IDs into the skill.

`scripts/discover_preview.py` captures CLI capabilities without project mutations. `scripts/rename_delivery.py` preflights/applies/undoes an authorized, source-verified filename map with checksums; it does not infer identity or grant approval.

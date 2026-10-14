# Official documentation guide

This topic map links official documentation without redistributing the manual. Use the current [documentation index](https://docs.preview.io/llms.txt) to discover added pages. Follow live interfaces/schemas for exact fields and [sources.md](sources.md) for verification dates.

## Foundation and production structure

| Page | When to use it |
| --- | --- |
| [Browse Preview Docs](https://docs.preview.io/) | Starting portal and current documentation map. |
| [Get started](https://docs.preview.io/preview/getting-started) | Project-to-canvas-to-shotlist workflow, reusable assets, review and export. |
| [Studio](https://docs.preview.io/preview/canvas-overview) | Canvas/Files switching, staging output, notes, collaborators, and canvas sections. Canvases belong to the project. |
| [Sequence Timeline](https://docs.preview.io/preview/scene-timeline) | Assign/reorder takes and shots, multiple shotlists, sequence management and scoped export. A duplicated shotlist copies assigned takes; a duplicated sequence starts with empty shots. |
| [Production](https://docs.preview.io/preview/shotlists-overview) | Synced Shotlist, Storyboard and Kanban views; metadata, filters, bulk actions, assignees and status. |
| [Scripts](https://docs.preview.io/preview/scripts) | Separate block-based screenplays, import, library mentions, AI suggested edits. Script text isn't directly linked to generation/shot structure; maintain the breakdown explicitly. |
| [Credits](https://docs.preview.io/preview/purchase-credits) | Current cost displays, credit purchase locations and billing. Read current pricing rather than freezing a dollars-to-credits assumption in a run. |
| [CLI/MCP](https://docs.preview.io/preview/cli) | Official installation, sign-in, hosted connector, local client configuration and structured automation. CLI/MCP use the signed-in account's access and credits. |

CLI/MCP provide supported production data operations; these UI pages are not a catalog of CLI endpoints. Discover exact CRUD, generation, assignment, and asset schemas in the installed client.

## Generating and refining

| Page | When to use it |
| --- | --- |
| [Prompt Box](https://docs.preview.io/preview/prompt-box-overview) | Model/settings/reference limits, audio, negative prompts, start/end frames and credit preflight. The prompt box is hidden while Preview Agent's panel is open. |
| [Preview Agent](https://docs.preview.io/preview/agent) | Native creative/planning assistant, Ask/Auto modes, reference selection and co-authored take history. Native approval mode is not the external agent's authorization policy. |
| [Referencing with @](https://docs.preview.io/preview/at-references) | Saved library items, folders/variations and images; one model reference slot per image. Explicitly select the latest intended version folder under our workflow. Pending generations aren't valid dependent references. |
| [Next Take Box](https://docs.preview.io/preview/next-take-box) | UI placement target, grid width and camera-follow. Placement may snap below to fit a row; group targeting uses its own placeholders instead. |
| [Quick Actions](https://docs.preview.io/preview/quick-actions) | Exact built-in character sheets, coverage, beats, production-design and related presets. The documented character preset produces 11 panels. Generic library creation or hand-prompted generation isn't that preset. |
| [Quick Styles & Camera Bag](https://docs.preview.io/preview/quick-styles) | Reusable styling/camera presets. Documented UI controls use Nano Banana Pro and select one treatment at a time; use live catalog IDs for structured settings. |
| [Generate World](https://docs.preview.io/preview/generate-world) | Environment image to navigable world, then Capture Take. A UI/world workflow, not a guessed image-generation flag. Environment-only input works best. |
| [Inpaint](https://docs.preview.io/preview/inpainting) | Local image edits with painted mask, references and current inpaint models. This UI mode exits when leaving the canvas/sequence; no promise that a CLI mask field exists. |
| [Upscaling](https://docs.preview.io/preview/upscaling) | Current Topaz/Magnific provider panels, output dimensions and settings-dependent credit costs. Running this is a separate paid operation, not routine file export. |
| [Edit in Photoshop](https://docs.preview.io/preview/edit-in-photoshop) | Image round-trip through the plugin, save and Sync Back. Returned edits may require recovery/placement from History; validate the actual new take. |
| [ComfyUI plugin](https://docs.preview.io/preview/comfy-ui-plugin) | Load Preview media in ComfyUI and send output to a chosen group through its supported ingest/upload node. Separate plugin installation/auth, not a standard CLI command. |

The native-agent page describes a smaller per-run limit than the checked CLI batch schema. These are different interfaces: honor each live cap rather than applying one everywhere. Current CLI image/video batch cap was 20.

The checked CLI 0.2.1 video schema supports videoReferenceMode=edit for models advertising video editing, with a supported source clip and no start/end frames. Inspect current model capabilities and [CLI operations](cli-operations.md) whenever exact Edit behavior matters.

## Reviewing and organizing

| Page | When to use it |
| --- | --- |
| [File Toolbar](https://docs.preview.io/preview/file-toolbar) | Reuse prompt, references, compare, download, tags and multi-selection. Video actions include frame extraction, trim, speed and auto-split; they aren't image inpainting. |
| [File View](https://docs.preview.io/preview/preview-window) | One-file full-size inspection, prompt/settings/cost, lineage, references and comments. Images have split/fade/side-by-side comparison. |
| [Project Library](https://docs.preview.io/preview/project-library) | Characters/locations/props and multi-image variation folders. The product describes meaningful looks; our [versioned library convention](versioned-reference-library.md) names these folders V001/V002 and Pajamas V001/V002 for submission and review. |
| [History](https://docs.preview.io/preview/history) | Whole-project recovery, cross-studio files and worlds. Removing a canvas display isn't the same as deleting library/project data. |
| [Groups](https://docs.preview.io/preview/groups) | Create before large runs, enter/target a group, grid/column controls, duplicate/export/ungroup. Save selected member files to the library rather than assuming a group-level entity. |
| [Tags](https://docs.preview.io/preview/tags) | Project-wide color tags and tag management in canvas/Files. The documented limit is ten tags per project; verify live constraints and reuse established tags. |
| [Command Palette](https://docs.preview.io/preview/command-palette) | Selection-aware actions and fast navigation/search via Cmd/Ctrl+K. IDs can locate takes; inspect selection before destructive keyboard shortcuts. |

File View is the inspector; Files view is a canvas output feed. Keep those names distinct. Context/provenance retrieval is a good structured path for metadata; the UI comparison tools are a good visual path.

## Collaboration and delivery

| Page | When to use it |
| --- | --- |
| [Comments](https://docs.preview.io/preview/comments) | File/canvas pins, drawings, replies and external review feedback. Read concrete requests and their visibility; a metadata flag isn't acceptance. |
| [Project menu](https://docs.preview.io/preview/settings-menu) | Active-shotlist export, selected/stacked alternates, audio/burn-in/frame-rate settings, project settings and deletion controls. |
| [Sharing](https://docs.preview.io/preview/sharing) | Collaborator access versus account-free review links, password/link controls. Verify scope/roles and explicit sharing authorization before creating/sending access. |
| [Project Analytics](https://docs.preview.io/preview/project-analytics) | Team/model/activity spend, remaining credits and projections. Useful for billing checks; preflight estimates aren't substitutes for recorded usage. |

Sharing, invites, paid generation/upscaling, and destructive actions aren't implied by preparing a local skill or review package. Do requested reversible work; prepare a concrete reviewable action before asking for genuinely missing authorization.

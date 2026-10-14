# Preview Production skill

One portable skill for project setup, artist canvas work, reference libraries, generation, reviews, producer handoffs and delivery in Preview. It combines production workflow with CLI/MCP mechanics and checks for existing work and actual approvals.

## Install and invoke

Unzip the complete preview-production folder so SKILL.md is directly inside it.

- Codex: copy to ~/.codex/skills/ or the configured skill directory.
- Claude Code: copy to ~/.claude/skills/ or the project's .claude/skills/.
- Other skill-capable agents: install the complete folder using their loader. Otherwise give the agent SKILL.md and access to relative resources.

Preserve a prior installed copy before upgrading. Invoke `$preview-production`, or let the agent select it for relevant Preview work. No second workflow skill or private project is required.

Use your own Preview account and authorized project. The [official CLI/connector guide](https://docs.preview.io/preview/cli) covers npm installation and sign-in; the hosted MCP endpoint is https://mcp.preview.io/mcp. The inspected CLI needs Node 18+; optional standard-library helpers need Python 3.9+. Board UI needs a supported computer-use tool or human assistance; this skill does not install one.

## What is configurable

Choose actual scripts, milestone canvases, review scopes, names/counts, shots/reference coverage, assignees, reviewers, reference/final approvers, producer, storage root and output specs. The default is Project → script categories → milestone canvases → dated, initialed round groups. References / First Frames / Animation are example milestones; adapt them to the deliverables. Locations can have work groups/rows within a milestone canvas and reusable library entries. Producer reference approval and director shot approval is an example authority policy, confirmed per job.

Agents inspect existing structure before writes. They adapt confirmed unused placeholders within authorized setup, ask before unrequested changes to established work, and verify exact approval before promoting reference media or marking final decisions. Draft library metadata can be created earlier. Installing the skill does not authorize paid generation, live migrations, sharing or sending media.

## Example requests

> Use $preview-production to set up this new project with Script A and Script B categories, each containing References, First Frames and Animation canvases. Use script-prefixed titles and numbered milestones for clear ordering. Inspect existing records first, adapt untouched placeholders, and preserve established work. Build matching script shotlists with deliverable sequences, briefs, references and assignments without generating media.

> Use $preview-production to prepare a revision of SH04 from its current take and feedback. Preserve the last approved choice, recover the full recipe and target the active round group. Report the proposed run separately from submission.

> Use $preview-production to audit character candidates for reference approval. Create missing draft identities; promote only exact versions accepted by the configured approver and record source/review links.

> Use $preview-production to assemble a producer review package from nominated versions, clearly label pending decisions, and create a manifest. Do not send it until the destination is authorized.

## Resources and validation

SKILL.md routes to focused instructions. assets/project-setup.json is a setup specification, not an API request. assets/workflow-guide.md is a generic human-facing guide to adapt into a project Script. Other templates capture recipes, handoffs, current/approved choices, generation runs and delivery filenames. Replace placeholders and inspect current schemas before tool calls.

scripts/discover_preview.py captures capabilities without production writes. scripts/rename_delivery.py preflights/applies/undoes an explicitly verified filename mapping with checksums. Keep runtime captures, credentials and actual production data outside this folder when sharing it.

Read-back and visual verification remain necessary. The instructions guide agent behavior; they do not add native approval enforcement or locks to Preview.

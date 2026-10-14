# Preview Agent Skills

Reusable skills for planning and running Preview projects, reviewing work, handing it off, and tracing exported clips back to their source takes.

## Download

**[Download both skills](https://github.com/thenpceo/preview-agent-skills/releases/latest/download/preview-skills.zip)**

| Skill | What it does | Download |
| --- | --- | --- |
| Preview Production | Project setup, canvases and revision rounds, typed references, generation, approvals, artist handoffs and producer delivery. | [preview-production.zip](https://github.com/thenpceo/preview-agent-skills/releases/latest/download/preview-production.zip) |
| Preview Provenance | Traces local clips and saved Premiere cuts back to exact Preview takes, prompts, references and source lineage. | [preview-provenance.zip](https://github.com/thenpceo/preview-agent-skills/releases/latest/download/preview-provenance.zip) |

These links point to the latest published release. Use the [release page](https://github.com/thenpceo/preview-agent-skills/releases/latest) for version notes and SHA-256 checksums.

## Install

Unzip the bundle. Copy each complete skill folder into your agent's skills directory:

- **Codex:** `~/.codex/skills/`
- **Claude Code:** `~/.claude/skills/`, or your project's `.claude/skills/`
- **Other agents:** use their skill loader, or provide `SKILL.md` and its relative supporting files.

Back up an existing installed copy before upgrading. Use your own Preview account and project access. The skills include no credentials, project caches or production media.

## Use

Ask the agent to use `$preview-production` for setup, production, review or delivery, and `$preview-provenance` for “where did this clip come from?” or “which takes are in this saved cut?”

For example:

> Use $preview-production to set up this job with a category per script and the agreed milestone canvases inside each. Inspect existing records, preserve established work, and confirm approval authority before promoting references.

> Use $preview-provenance to inspect this saved Premiere sequence and map its clips to Preview take links and recipes. Keep unmatched or transformed media explicit.

The default canvas hierarchy is **Project → script categories → milestone canvases → dated, initialed revision groups**. The lead adapts milestones to the actual job. Matching script shotlists contain deliverable sequences for review. Established projects are reorganized only when explicitly authorized.

The production skill separates artist selections, exact-version approval and release. The provenance skill identifies source lineage; it does not establish approval.

## Requirements

Use a supported Preview CLI/MCP connection. Optional Python helpers require Python 3.9+; provenance needs the CLI signed into the appropriate account and the media share mounted locally. Precise canvas UI work needs supported computer use or human assistance.

Production instructions guide agent behavior rather than adding native locks or permissions to Preview. Installing either skill does not authorize paid runs, project migrations, invitations or sending media.

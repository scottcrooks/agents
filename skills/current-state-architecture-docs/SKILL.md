---
name: current-state-architecture-docs
title: Current-State Architecture Docs
description: Generate deterministic architecture current-state docs from repository evidence
model: gpt-5.3-codex
---

# Current-State Architecture Docs

Generate architecture docs from current repository state and implementation logs.

## Inputs

- `mode` (optional):
  - `rolling` (default): include logs from the last 14 days
  - `full`: include all implementation logs
- `days` (optional): rolling window size; default `14`
- `repo_root` (optional): repository root; default current working directory

## Required Behavior

1. Collect evidence before synthesis.
2. Use deterministic ordering for all listed content.
3. Write both outputs:
   - `docs/architecture/current-state/YYYY-MM-DD_current-state.md`
   - `docs/architecture/current-state/latest.md`
4. Update `latest.md` atomically.
5. Include source evidence references in output.

## Runbook

From the target repository root:

```bash
# Default rolling mode (14 days)
/home/scott/.agents/skills/current-state-architecture-docs/scripts/render_current_state.sh

# Rolling mode with explicit window
/home/scott/.agents/skills/current-state-architecture-docs/scripts/render_current_state.sh --mode rolling --days 21

# Full regeneration from all implementation logs
/home/scott/.agents/skills/current-state-architecture-docs/scripts/render_current_state.sh --mode full
```

Freshness check:

```bash
/home/scott/.agents/skills/current-state-architecture-docs/scripts/check_freshness.sh --max-age-days 7
```

## Notes

- This skill is portable and does not require repo-specific Makefile targets.
- If `services.yaml` is missing, service registry section is emitted as unavailable.

## Worktree Tracking
When starting work in a worktree, run: `mono worktree tag IN_PROGRESS`
- If blocked on user input or external dependency, run: `mono worktree tag NEEDS_INPUT`
- Before final handoff, run: `mono worktree tag DONE`
- Use lowercase `--state` filters when reviewing queue health:
  - `mono worktree list --state active`
  - `mono worktree list --state needs-input`
  - `mono worktree list --state done`

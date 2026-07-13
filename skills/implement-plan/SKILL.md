---
name: implement-plan
description: Execute or resume an approved implementation plan across one or more validated slices, persisting through recoverable work and ending only at explicit ledger-backed slice boundaries, manual checkpoints, blockers, or plan completion.
---

# Implement Plan

Execute the approved plan in order. Treat the plan as the execution contract and its companion status ledger as the resume and boundary authority.

## Execution mode

Choose and record one mode in the ledger before mutating code:

- `boundary-driven` (default): execute one or more slices. A completed slice permits a handoff but does not require one; either hand back at that boundary or activate the next slice and continue.
- `single-slice`: complete exactly one slice and hand back. Use only when the user explicitly limits the run to one slice.
- `continuous`: continue across completed slices until the whole plan completes, a plan-defined manual checkpoint is reached, or a hard blocker is established.

Use `continuous` or `single-slice` only when the user explicitly requests that scope. Otherwise use `boundary-driven`. All modes are suitable for low-reasoning execution because no mode permits a mid-slice handoff.

## Boundary state machine

The ledger must contain these metadata fields:

```markdown
- Execution mode: `boundary-driven`
- Boundary state: `active`
- Boundary evidence: none
- Validation: not run
- Blocker attempts: none
- Unblock condition: none
```

Allowed boundary states are:

- `active`: work is still in progress. A final response is forbidden.
- `slice_complete`: the active slice is fully implemented and validated. Final response is allowed in `boundary-driven` or `single-slice` mode.
- `manual_checkpoint`: the plan explicitly requires user verification before further work.
- `hard_blocker`: the next concrete plan action cannot proceed without unavailable authority, external state, a user-only decision, or a material scope/design change.
- `plan_complete`: every slice and final validation requirement is complete.
- `cancelled`: the user explicitly cancelled or replaced this plan, and the ledger records that instruction.

Before any final response, update the ledger to a permitted boundary state and run:

```bash
python3 <implement-plan-skill-directory>/scripts/plan_boundary_check.py \
  --plan <plan-path> \
  --ledger <ledger-path>
```

The successful boundary check must be the final tool action before the final response. If it fails, continue the active tool-use loop. Never describe a failed boundary check as a blocker.

When the implement-plan `Stop` hook is installed, it mechanically applies the same check whenever Codex attempts to end a turn. A rejected stop automatically continues the turn with the guard failure as the next prompt. Keep the ledger accurate because the hook, not a status-only final response, decides whether the turn may end.

## Hard-blocker test

Record `hard_blocker` only when all three conditions hold:

1. The condition prevents the next concrete action in the active slice.
2. At least one safe, in-scope resolution was attempted or no such attempt is possible.
3. The ledger records concrete evidence, attempted resolutions, and the exact unblock condition.

Unrelated dirty or committed changes are not blockers unless they overlap required edits or make required validation impossible. Preserve them and continue. A recoverable test failure, long-running command, large slice, progress update, or resolvable repository uncertainty is not a blocker.

## User steering during a slice

A correction, question, or added instruction during an active slice does not cancel the plan. Address it, reread the ledger, set `Boundary state` back to `active` if necessary, and resume the slice in the same turn. Stop only if the user explicitly cancels, replaces, or materially changes the plan.

If the user explicitly cancels or replaces the plan, mark the active slice and overall status `cancelled`, record the user instruction as `Boundary evidence`, set a concrete `Next action`, set `Boundary state` to `cancelled`, and run the boundary check.

## Start or resume

1. Read the implementation plan fully.
2. Read the ledger path named by the plan before broad repository exploration.
3. If no ledger path exists, derive `thoughts/plan-status/<plan-name>.status.md` and initialize it before the first code mutation.
4. Add or normalize the boundary metadata fields without discarding existing history.
5. Select the ledger's `in_progress` slice, otherwise the next `pending` slice.
6. Confirm the slice objective, required changes, validation, completion signal, and any manual checkpoint.
7. Set the slice to `in_progress`, set `Boundary state` to `active`, and maintain a `Remaining requirements` checklist copied or faithfully derived from the slice.

Stop before coding only when ambiguity or a repository contradiction materially changes scope, sequencing, or validation. Record it as a hard blocker only when it passes the hard-blocker test.

## Active slice loop

While `Boundary state` is `active`:

1. Read the next unmet item from `Remaining requirements`.
2. Perform the next concrete tool action.
3. Inspect the result and update the checklist and ledger notes.
4. Continue through recoverable errors and tightly related prerequisites.
5. Run plan-required and repository-standard validation.
6. Fix and rerun failed validation until it passes or a hard blocker is established.

Every non-terminal commentary update must be followed by a concrete tool call in the same turn. A passing intermediate check is progress, not completion. Do not end with a status summary, check result, partial edit summary, or an offer to continue.

## Reaching a boundary

For slice completion:

1. Verify every planned edit, cleanup item, validation requirement, and completion signal against the repository.
2. Run the required boundary validation in the plan's specified order.
3. Mark every `Remaining requirements` item complete.
4. Record validation commands and outcomes in the slice and top-level `Validation` field.
5. Mark the slice `complete` and record the next pending slice or plan completion.
6. In `single-slice` mode, set `Boundary state` to `slice_complete` and run the boundary check.
7. In `continuous` mode, mark the next slice `in_progress`, reset the boundary fields to `active`/`none`, create its checklist, and continue. If no slice remains, set `plan_complete` and run the boundary check.
8. In `boundary-driven` mode, make the continuation decision only after the slice is complete. A boundary permits a handoff; it does not require one. To hand back, set `slice_complete` and run the boundary check. To continue, activate the next slice, reset boundary fields to `active`/`none`, create its checklist, and make the next tool call.

Do not stop merely because validation passed, the slice was lengthy, or a progress summary is available. If ending the turn, end because the ledger proves the slice boundary is complete.

For a manual checkpoint:

1. Confirm the active slice explicitly defines the checkpoint.
2. Record completed automated validation and exact user verification instructions.
3. Mark the slice `manual_checkpoint`, set the ledger boundary state accordingly, and run the boundary check.
4. Wait for explicit user confirmation. On confirmation, restore the slice and boundary to `in_progress`/`active` and continue.

For a hard blocker:

1. Apply the hard-blocker test.
2. Mark the slice `blocked`.
3. Fill `Boundary evidence`, `Blocker attempts`, and `Unblock condition` with concrete values.
4. Set `Boundary state` to `hard_blocker` and run the boundary check.

## Scope and communication

- Do not re-plan, reopen approved tradeoffs, broaden scope, or skip validation unless the plan is contradicted and the user approves an adjustment.
- Read upstream research/design artifacts only when the active slice needs them.
- Keep the user informed with concise commentary tied to implementation, validation, or a real boundary.
- Keep implementation ownership in the main agent. Do not use parallel fan-out; use at most one read-only subagent for a narrow question when direct inspection is inefficient.
- Preserve unrelated user changes.

## Final report protocol

Always end a completed turn with exactly these five tags in this order, with no prose before or after them. This format applies inside Sonata and in standalone skill use; it remains human-readable in both contexts.

```xml
<turnSummary>...</turnSummary>
<turnErrors>...</turnErrors>
<automatedValidation>...</automatedValidation>
<manualValidation>...</manualValidation>
<remainingSlices>...</remainingSlices>
```

Use a self-closing tag whenever a section is empty, and never omit a tag. Put the human-readable work summary in `turnSummary`, errors or blockers in `turnErrors`, and completed automated checks in `automatedValidation`.

`remainingSlices` is a machine continuation signal:

- Populate it only with the next concrete implementation slice that can start autonomously and immediately.
- `<remainingSlices/>` means Sonata must not issue another implementation continuation.
- Never put “no slices remain,” plan-completion bookkeeping, PR-review guidance, work requiring external input, or explanatory prose in it.

Boundary mappings are exact:

- A completed slice with another autonomous slice: populate `remainingSlices` with that next slice. `manualValidation` is normally empty; in AFK mode a genuine remaining slice still controls continuation even if contradictory manual validation text is present.
- An interactive `manual_checkpoint`: populate `manualValidation` with the concrete actions available now and use `<remainingSlices/>`.
- `plan_complete`: use both `<manualValidation/>` and `<remainingSlices/>`.
- AFK review-time checks carried by the plan never become a `manual_checkpoint` or final-report `manualValidation`; leave them in the plan for PR generation.

The final report's `turnSummary` must name the boundary state, active/completed slice, ledger update, and validation result or exact unblock condition.

---
name: implement-plan
description: Execute or resume an approved plan in validated slices, including through a Codex goal, maintaining its status ledger and checking each handoff boundary.
---

# Implement Plan

Execute the approved plan in order. Treat the plan as the execution contract and its companion status ledger as the resume and boundary authority.

Implementation runs on Luna; the caller configures the model and reasoning effort. Choose effort according to the work; stopping rules do not establish reasoning sufficiency. Resolve implementation details within the approved design; surface material missing decisions instead of inventing them.

## Execution context

Preserve `Automation mode: afk` or `Automation mode: interactive` under the plan's `## Execution Context` and ledger's `## Metadata`. An explicit caller instruction is authoritative; otherwise use the plan's mode, defaulting to `interactive` if absent. Fill missing mode fields and reconcile any mismatch before execution. AFK mode permits no blocking manual checkpoint or human-gated remaining requirement. Keep optional review-time checks in the plan for PR review.

Choose and record implementation's separate execution mode in the ledger. Use an explicit caller selection first, otherwise preserve the recorded mode; default to `continuous` when neither supplies one:

| Execution mode | Continuation rule |
| --- | --- |
| `continuous` (default) | Continue until plan completion, a plan-defined manual checkpoint, or a hard blocker; honor explicit user requests to stop. |
| `boundary-driven` (only on explicit request or already recorded) | At a completed slice, either hand back or activate the next slice and continue. |
| `single-slice` (only on explicit request) | Complete exactly one slice and hand back. |

## Goal execution

`/goal implement-plan <plan-path>` is sufficient. Its objective is to execute the plan in `continuous` mode until the plan is complete or verified human intervention is required. Reconcile an inherited ledger mode with that request unless the user explicitly limits execution. `/goal $implement-plan <plan-path>` has the same meaning. Do not require the user to restate acceptance criteria, validation, scope, ledger instructions, or these stopping conditions.

- Derive the goal's stopping conditions from the plan and companion ledger. Preserve the plan's non-goals and PR/review boundaries. Complete the goal when the boundary checker accepts either:
  - **Finished implementation:** `Overall status: complete` and `Boundary state: plan_complete`, with all slices, acceptance criteria, and required final/cross-slice validation supported by evidence.
  - **Human intervention required:** `Overall status: blocked` and `Boundary state: hard_blocker` passing the hard-blocker test, or a plan-defined interactive `manual_checkpoint` requiring user confirmation. Record what was attempted, why autonomous progress cannot continue, and the exact input or action needed.
- Use available goal tools to inspect the matching active goal and maintain its lifecycle. Create a goal only when explicitly requested; an ordinary skill invocation remains usable without one. Do not replace an unrelated active goal or expand the plan to satisfy a broader objective without resolving the mismatch.
- On automatic continuation, follow the same start/resume procedure against the saved plan and ledger. Resume unmet work rather than restarting or asking for a new prompt.
- Mark the matching goal complete after one of those stopping conditions is verified. At a human-intervention boundary, completion means this autonomous run has finished; keep the ledger `blocked` or `manual_checkpoint`, preserve unfinished slices, and report that the implementation remains incomplete. Do not mark the plan complete or keep automatically retrying a verified human dependency.
- A completed slice, report, recoverable failure, or ledger update alone does not satisfy the goal. Automatic continuation must not bypass required user input. Honor user pause/cancellation and budget controls without treating them as achieved stopping conditions.
- For an explicitly limited goal, such as one named slice, derive completion from that authorized subset and record the remaining plan work honestly. Do not broaden it into a whole-plan goal.

## Start or resume

1. Read the plan fully and its named ledger before broad repository exploration. If no ledger path exists, derive `thoughts/plan-status/<plan-name>.status.md` and initialize it before code mutation.
2. Confirm the plan covers its acceptance criteria, relevant behavior/contracts, files/symbols, patterns, dependencies, validation command/working directory/setup, completion signals, and any manual checkpoints. Resolve a material gap through targeted evidence or the hard-blocker test below; do not broadly re-plan.
3. Reconcile plan and ledger slice numbers, names, and order without discarding execution history. Both must use consecutive top-level numbered entries starting at 1 under `Execution Slices` and `Slice Status`. Fill missing metadata, including automation mode, current/last completed slice, validation, boundary evidence, blocker attempts, unblock condition, next action, and timestamp.
4. Resume the `in_progress` slice, or the recorded `manual_checkpoint`/`blocked` slice once its resume/unblock condition is satisfied. Otherwise select the next `pending` slice and confirm its dependencies are complete. Do not bypass a waiting slice to start later work; a completed/cancelled plan has no active slice.
5. Set the slice and overall status to `in_progress`, boundary state to `active`, and boundary evidence/blocker attempts/unblock condition to `none`. Populate `Remaining requirements` from the active slice's implementation, validation, completion requirements, and applicable plan-wide constraints. Include any explicitly required reference reading; keep the checklist scoped to that slice.

## Active slice loop

While the boundary state is `active`, a final response is forbidden:

1. Read any reference sections explicitly required by the active slice before dependent edits. Read the next unmet requirement and perform the next concrete action.
2. Inspect the result, update the checklist and execution notes, and continue through recoverable errors and related prerequisites.
3. Run the planned behavioral checks and repository-standard validation in the specified order, using the authoritative aggregate command exclusively where required. Record commands, working directories, and outcomes. Fix failures caused by the requested change and rerun affected checks; do not broaden work to unrelated failures.
4. Verify acceptance behavior and relevant negative paths, including newly required coverage. A passing boundary check or unrelated existing test suite is not proof of functional correctness.
5. Once every slice requirement is satisfied, update the ledger using the transition contract below.

Every non-terminal commentary update must be followed by a concrete tool call in the same turn.

## Durable progress and context compaction

- Keep the plan saved on disk as the stable execution contract. Persist progress in its companion ledger after meaningful implementation milestones, validation results, and slice transitions, not only when ending a turn.
- Record completed and remaining work, relevant decisions or user corrections, latest validation evidence, and the next concrete action in the ledger's checklist and execution notes. Keep enough detail to resume a partially implemented slice without relying on chat memory.
- Do not rely on automatic compaction to write files or provide an opportunity to save first. Before deliberately requesting compaction, save the current ledger.
- After compaction, reread the ledger, the plan's scope and applicable shared constraints, and the active slice before further edits. Check relevant working-tree changes and any still-running command against the saved state; reconcile actual progress without repeating completed work or claiming unrun checks passed.
- Compaction is not a stopping boundary. Resume the same execution mode and continue from the next unmet requirement.

## Boundary transition contract

At every transition, update `Current slice`, `Last completed slice`, `Next action`, `Last updated`, per-slice timestamps, and validation results. `Next action` must describe the actual resume, unblock, review, or completion action; do not leave it as `none`.

| Boundary state | Slice and overall status | Required evidence and continuation |
| --- | --- | --- |
| `active` | Active slice and overall `in_progress` | To continue after a completed slice, activate the next slice, replace its checklist, and reset boundary evidence/blocker fields. |
| `slice_complete` | Completed slice `complete`; overall `in_progress` when work remains | Check all active requirements; set concrete `Boundary evidence` naming the completed slice and acceptance evidence; record top-level `Validation`. Only `boundary-driven` and `single-slice` may hand back here. |
| `plan_complete` | Every slice and overall `complete` | Complete final/cross-slice validation and acceptance-criteria coverage; check all remaining requirements; set concrete `Boundary evidence` and top-level `Validation`. Use this state when no slices remain, including in `single-slice` mode. |
| `manual_checkpoint` | Checkpoint slice and overall `manual_checkpoint` | Interactive mode only. The active slice must define `Manual verification checkpoint: [instructions]`. Record automated results and exact operator actions/expected results as `Boundary evidence`. Resume only on explicit confirmation. |
| `hard_blocker` | Active slice and overall `blocked` | Pass the hard-blocker test; record concrete `Boundary evidence`, `Blocker attempts`, and `Unblock condition`. |
| `cancelled` | Active slice and overall `cancelled` | Record explicit user cancellation/replacement in `Boundary evidence` and the concrete next action. |

After a slice completes, apply the execution mode's continuation rule. Before any final response, reach a permitted boundary and run:

```bash
python3 <implement-plan-skill-directory>/scripts/plan_boundary_check.py \
  --plan <plan-path> \
  --ledger <ledger-path>
```

The successful check must be the final verification action before the final response. After it, only applicable goal lifecycle updates and the final report may follow; if code, plan, ledger, or validation evidence changes, rerun the check. If it fails, repair the artifact inconsistency and rerun it; checker rejection itself is not a hard blocker. The check establishes structural agreement and recorded boundary evidence, not whether code works. When installed, the `Stop` hook applies the same check and automatically continues a rejected stop.

### Completed-ledger example

For a plan with one slice named `Reject updates by non-owners`, these are the completion fields. Preserve the ledger's other metadata and history:

```markdown
## Metadata
- Plan: thoughts/plans/YYYY-MM-DD-owner-check.md
- Automation mode: afk
- Overall status: complete
- Execution mode: continuous
- Boundary state: plan_complete
- Boundary evidence: Slice 1 satisfies AC1 owner success and AC2 non-owner rejection with unchanged data.
- Validation: Repository-root `make check` passed, including the new ownership cases and final regression checks.
- Blocker attempts: none
- Unblock condition: none
- Current slice: none
- Last completed slice: 1. Reject updates by non-owners
- Next action: Review the completed change.
- Last updated: [actual ISO timestamp]

## Remaining Requirements
- [x] Implement AC1 and AC2 using the existing ownership pattern.
- [x] Add acceptance and negative-path coverage; run slice and final validation.
- [x] Confirm all acceptance criteria have passing evidence.

## Slice Status
1. Reject updates by non-owners
   - Status: `complete`
   - Validation result: `make check` passed; AC1 and AC2 assertions passed.
```

## Hard-blocker test

Record `hard_blocker` only when all three conditions hold:

1. The condition prevents the next concrete action in the active slice.
2. At least one safe, in-scope resolution was attempted or no such attempt is possible.
3. The ledger records concrete evidence, attempted resolutions, and the exact unblock condition.

Unrelated dirty or committed changes are not blockers unless they overlap required edits or make required validation impossible. Preserve them and continue. A recoverable test failure, long-running command, large slice, progress update, or resolvable repository uncertainty is not a blocker.

## User steering during a slice

A correction, question, or added instruction does not cancel the plan. Address it, reread the ledger, restore `active` if necessary, and resume the slice in the same turn. If the user explicitly cancels/replaces the plan or materially changes its scope, follow the transition contract or surface the decision required; preserve completed work and the recorded instruction.

## Scope and communication

- Do not re-plan, reopen approved tradeoffs, broaden scope, or skip validation unless the plan is contradicted and the user approves an adjustment.
- Read upstream research/design artifacts when explicitly required by the active slice or needed to clarify a material point. Do not skip named reading prerequisites or treat an unread reference as evidence that a requirement is satisfied.
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

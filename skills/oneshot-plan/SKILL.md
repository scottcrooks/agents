---
name: oneshot-plan
description: Turn a bounded request or research artifact into an executable implementation plan and status ledger without separate design or outline phases.
---

# Oneshot Plan

Produce an execution-ready plan in one pass. Internally perform only the research, design, and outlining needed to remove implementation ambiguity; do not create separate research, design, or outline artifacts.

## Model and execution context

The caller selects Luna, Sol, or Astra for planning according to problem complexity. Routine changes with a clear local pattern suit Luna; interacting components and consequential tradeoffs may warrant Sol; conflicting evidence or difficult design reasoning may warrant Astra. Do not switch models yourself. All three must produce the same execution-sufficient contract for Luna implementation; vary discovery effort, not the handoff quality bar.

Honor an explicit `Automation mode: afk` or `Automation mode: interactive`; otherwise use `interactive`. Record the mode in both artifacts. This is separate from implementation's execution mode (`boundary-driven`, `single-slice`, or `continuous`). In AFK mode, use automated checks and include no blocking manual checkpoint or human-gated ledger requirement. Optional PR-review checks may be listed under `Review-time manual validation`; they are not completion requirements.

## Operating contract

- Treat the ticket or request as the scope boundary.
- Aim for the minimum viable change that fully satisfies the ticket.
- Preserve explicit non-goals and avoid speculative extensibility, unrelated cleanup, new abstractions, or broader redesign.
- Prefer existing repository patterns, interfaces, dependencies, and validation commands.
- Inspect enough code and repository guidance to name concrete touchpoints and avoid implementation rediscovery.
- Prefer thin vertical slices with automated validation between slices.
- Emit the same implementation-plan and status-ledger artifacts used by `create-plan`.

## Input

Accept any one of:

- A ticket or issue
- A bounded implementation request
- Existing research
- A combination of these

If the input is inaccessible or does not identify a concrete desired outcome, stop and ask for the missing input.

## Workflow

### 1. Establish the minimum viable outcome

- Extract the acceptance criteria, constraints, non-goals, and expected behavior.
- Separate requirements from suggestions in the ticket.
- Identify the smallest end-to-end change that meets all acceptance criteria.
- Treat adjacent improvements as non-goals unless required for correctness or validation.

### 2. Inspect targeted repository context

- Read repository instructions and the files directly implicated by the request.
- Read supplied research and its evidence context. Compare its commit, branch, and relevant working-tree changes with the current repository. Recheck affected findings when files have changed; preserve still-valid evidence rather than repeating the whole investigation.
- For every research open question relevant to implementation, resolve it from current evidence, record why it does not affect this scope, or apply the escalation rules below. Research `status: complete` is not an implementation-readiness signal.
- Find existing implementation and test patterns before proposing a new design.
- Identify the authoritative aggregate verification command. Use it exclusively when repository instructions declare one.
- Keep discovery targeted; do not perform broad research when local evidence resolves the plan.

### 3. Resolve design inline

- Follow an existing repository pattern when it satisfies the ticket and current constraints.
- When multiple architectures appear viable, first resolve the choice by finding the closest established pattern and selecting it.
- Prefer the option with the smallest change surface and lowest new conceptual overhead.
- Record consequential choices briefly under `Inline Decisions`.
- Close material behavior and contract decisions before handoff: inputs/outputs, permissions, data ownership, state changes, and failure behavior where relevant. Luna must not have to invent them during implementation.
- Do not create separate design or outline documents.

### 4. Check escalation triggers

Escalate only when a material trigger cannot be resolved from authoritative repository evidence:

- No existing pattern resolves multiple materially different viable architectures.
- Acceptance criteria or product behavior are materially ambiguous.
- The change requires an unapproved public API, schema, data migration, or cross-system contract decision.
- Rollout or backward-compatibility risk requires an owner decision.
- Security, privacy, compliance, or destructive-data implications lack an established policy or safe precedent.
- The minimum viable change cannot be determined without changing ticket scope.

For a trigger:

1. Attempt to resolve it using repository instructions, existing patterns, tests, ADRs, and linked ticket context.
2. If resolved, record the evidence and continue.
3. If unresolved, stop before writing the plan or ledger. Report the exact decision, viable options, evidence inspected, and a concise recommendation. Ask the user or responsible owner to decide.

Do not use escalation merely because implementation is complex or requires several files.

### 5. Build the executable plan

- Default to 1-4 thin vertical slices; use one slice when that is sufficient.
- Assign acceptance criteria stable labels such as `AC1` and map every criterion to its owning slices and validation evidence.
- For each slice include its observable outcome, acceptance criteria, dependencies, concrete files/symbols, selected implementation/test pattern, planned change, validation, and completion signal.
- Validation must name the repository command, working directory, necessary setup or fixtures, behavior and negative paths being checked, and expected evidence. Passing an unrelated existing suite is not evidence for new behavior; plan the necessary coverage within the slice.
- Use focused interface or data examples only when they remove material ambiguity; do not prescribe a full patch.
- Include manual verification only when automation genuinely cannot manage the relevant risk.
- Use the exact field `Manual verification checkpoint: none` when no blocking checkpoint is required. Otherwise put a nonempty reason on that field's first line, followed by setup, operator actions, expected results, and resume condition in its continuation. AFK mode always uses `none`.
- Carry forward only execution-critical evidence.

### 6. Write compatible artifacts

Write:

- `thoughts/plans/YYYY-MM-DD-descriptive-name.md`
- `thoughts/plan-status/YYYY-MM-DD-descriptive-name.status.md`

Use today’s date and the same descriptive name for both.

The plan must contain:

```markdown
# Implementation Plan: [Topic]

## Execution Context
- Automation mode: [afk | interactive]

## Scope
- [Minimum viable outcome]
- [Explicit non-goals]

## Acceptance Criteria
| Criterion | Required observable behavior | Owning slices | Validation evidence |
| --- | --- | --- | --- |
| AC1 | [Behavior] | 1 | [Check and expected result] |

## Input Artifacts
- Ticket/Request: [reference or inline prompt]
- Research: [path or `incorporated inline`]
- Design Doc: `incorporated inline`
- Structured Outline: `incorporated inline`

## Research Anchor
- [Execution-critical repository findings with file references]
- [Inherited constraints and scope boundary]
- [Research freshness check and disposition of relevant open questions]

## Inline Decisions
- [Decision, selected existing pattern, and evidence]

## Status Ledger Path
- `thoughts/plan-status/YYYY-MM-DD-descriptive-name.status.md`

## Execution Strategy
- [Why this is the minimum viable change]
- [Slice structure and validation approach]

## Execution Slices
1. [Slice]
   - Objective: [Observable outcome; acceptance criteria AC1, ...]
   - Dependencies: [Earlier slices or none]
   - Key touchpoints: [Files/symbols and implementation/test pattern references]
   - Planned change: [Concrete behavior, relevant interfaces, and failure semantics]
   - Automated validation: [Command, working directory, setup/fixtures, behaviors checked, expected evidence]
   - Completion signal: [Observable acceptance evidence]
   - Manual verification checkpoint: none

## Cross-Slice Validation
- [Behavior, edge-case, regression, and repository command checks]

## Testing Coverage
- [Unit/component and integration/end-to-end coverage]

## Pattern Application
- [Existing pattern and how it constrains the change]
```

Initialize the ledger as:

```markdown
# Plan Status: [Topic]

## Metadata
- Plan: [plan path]
- Research: [research path or `incorporated inline`]
- Automation mode: [same as plan]
- Overall status: `not_started`
- Execution mode: `boundary-driven`
- Boundary state: `active`
- Boundary evidence: none
- Validation: not run
- Blocker attempts: none
- Unblock condition: none
- Current slice: [first slice]
- Last completed slice: none
- Next action: [start slice 1]
- Last updated: [ISO timestamp]

## Remaining Requirements
- [ ] [First-slice implementation requirement]
- [ ] [First-slice validation requirement]
- [ ] [First-slice completion signal]

## Slice Status
1. [Slice]
   - Status: `pending`
   - Started at: not started
   - Completed at: not completed
   - Validation result: not run
   - Notes: none
```

Add all remaining slices to `Slice Status`, preserving the plan's exact slice numbers, names, and order. Use consecutive top-level numbered entries starting at 1 in both artifacts. Use only `pending | in_progress | complete | manual_checkpoint | blocked | cancelled`.

The initialized ledger is not a valid implementation stopping boundary. At completion, `implement-plan` must record concrete `Boundary evidence` and `Validation`, check all remaining requirements, and set `Overall status: complete` when the plan is finished. The boundary checker verifies artifact consistency; functional correctness still requires the planned behavioral checks.

### Slice detail example

This illustrative slice shows the required specificity; derive actual files and commands from the target repository:

```markdown
1. Reject updates by non-owners
   - Objective: AC1 permits owner updates; AC2 rejects non-owners without changing data.
   - Dependencies: none
   - Key touchpoints: src/api/update.py:update_item; tests/api/test_update.py; follow the ownership check in src/api/delete.py:delete_item.
   - Planned change: Check ownership before saving. Reuse the existing 403 response; retain the owner success response.
   - Automated validation: From the repository root, run `make check` using its existing disposable database fixture. Add owner-success and non-owner-403 cases; the rejected case must assert stored data is unchanged. Expect all checks to pass.
   - Completion signal: Both acceptance cases pass; existing delete behavior remains covered.
   - Manual verification checkpoint: none
```

## Quality bar

- The plan fully satisfies the ticket with the smallest justified change surface.
- Every important choice is supported by an existing pattern or recorded inline decision.
- Concrete files, components, interfaces, and tests are named where they reduce execution risk.
- Each slice has a specific validation path and completion signal.
- The plan and ledger are compatible with `implement-plan`.
- No unresolved escalation trigger remains.
- Every acceptance criterion maps to implementation and meaningful validation; no material behavior or contract decision is left to the executor.
- Automation modes agree, slice numbers/names/order match, and checkpoint fields use the exact syntax above.
- After writing both artifacts, report their paths and the key scope assumption.

When evaluating changes to this workflow, use [the evaluation protocol](references/workflow-evaluation.md). It separates research, planning, implementation, and end-to-end performance; it is not required reading for ordinary plan creation.

---
name: oneshot-plan
description: Turn a bounded request, research artifact, or resolved design into an executable implementation plan and status ledger without requiring separate design or outline phases.
---

# Oneshot Plan

Produce an execution-ready plan in one pass. Reuse supplied research and resolved designs; internally perform only the additional research, design, and outlining needed to remove implementation ambiguity. Do not create separate research, design, or outline artifacts.

## Model and execution context

The caller selects Luna, Sol, or Astra for planning according to problem complexity. Routine changes with a clear local pattern suit Luna; interacting components and consequential tradeoffs may warrant Sol; conflicting evidence or difficult design reasoning may warrant Astra. Do not switch models yourself. All three must produce the same execution-sufficient contract for Luna implementation; vary discovery effort, not the handoff quality bar.

Honor an explicit `Automation mode: afk` or `Automation mode: interactive`; otherwise use `interactive`. Record the mode in both artifacts. This is separate from implementation's execution mode (`boundary-driven`, `single-slice`, or `continuous`). In AFK mode, use automated checks and include no blocking manual checkpoint or human-gated ledger requirement. Optional PR-review checks may be listed under `Review-time manual validation`; they are not completion requirements.

## Operating contract

- Treat the ticket or request as the scope boundary. When planning from a supplied design, inherit its resolved behavior, contracts, constraints, and non-goals unless the user explicitly supersedes them.
- Aim for the minimum change that fully satisfies the accepted scope. Tight scope means excluding unnecessary work, not dropping required behavior or weakening the chosen design.
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
- A resolved design document, with any linked research
- A combination of these

A design document is optional. A bounded request, ticket, or research artifact is sufficient; do not require the user to run a separate design or outline phase. When no design is supplied, resolve the necessary design decisions inline using repository evidence and the escalation rules below.

If the input is inaccessible or does not identify a concrete desired outcome, stop and ask for the missing input.

## Workflow

### 1. Establish the minimum viable outcome

- Extract the acceptance criteria, constraints, non-goals, and expected behavior.
- For a supplied design, read it fully and identify whether the request covers the whole design or an explicitly selected part. Do not silently plan only the easiest portion; make any requested subset and its exclusions explicit.
- Separate requirements from suggestions in the ticket.
- Identify the smallest end-to-end change that meets all acceptance criteria.
- Treat adjacent improvements as non-goals unless required for correctness or validation.

### 2. Inspect targeted repository context

- Read repository instructions and the files directly implicated by the request.
- Read supplied research and its evidence context. Compare its commit, branch, and relevant working-tree changes with the current repository. Recheck affected findings when files have changed; preserve still-valid evidence rather than repeating the whole investigation.
- With a supplied design, use its linked research and source references as targeted evidence anchors. Verify the touchpoints and patterns needed for execution; do not repeat the full research or design process.
- For every research open question relevant to implementation, resolve it from current evidence, record why it does not affect this scope, or apply the escalation rules below. Research `status: complete` is not an implementation-readiness signal.
- Find existing implementation and test patterns before proposing a new design.
- Identify the authoritative aggregate verification command. Use it exclusively when repository instructions declare one.
- Keep discovery targeted; do not perform broad research when local evidence resolves the plan.

### 3. Resolve design inline or preserve a supplied design

- When a resolved design is supplied, translate its decisions into execution constraints. Do not reselect architecture, reintroduce rejected alternatives, or add features it explicitly excludes in pursuit of a smaller or more general solution.
- Resolve incidental implementation choices from current repository evidence. If evidence contradicts a material design decision, explain the conflict and use the escalation rules below rather than silently changing the design.
- Without a supplied design, resolve the necessary design inline using the following criteria.
- Follow an existing repository pattern when it satisfies the ticket and current constraints.
- When multiple architectures appear viable, first resolve the choice by finding the closest established pattern and selecting it.
- Prefer the option with the smallest change surface and lowest new conceptual overhead.
- Record execution-critical inherited decisions and consequential new implementation choices briefly under `Inline Decisions`. Link to deeper rationale and alternatives analysis rather than repeating it; a reference must not replace a binding behavioral rule.
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
- Each slice should fit one focused implementation pass plus meaningful validation. Split independently verifiable outcomes when one slice would require building several substantial behaviors at once; do not compress a whole feature into a slice merely to meet the default count.
- Preserve explicit PR/review boundaries and their dependency order in the plan and ledger. Use as many slices within those boundaries as the accepted scope needs; the default slice count is not a cap or a reason to collapse separately reviewable PRs. Earlier PRs must not depend on work assigned to later ones.
- Assign acceptance criteria stable labels such as `AC1` and map every criterion to its owning slices and validation evidence.
- For each slice include its observable outcome, acceptance criteria, dependencies, concrete files/symbols, selected implementation/test pattern, planned change, validation, and completion signal.
- Validation must name the repository command, working directory, necessary setup or fixtures, behavior and negative paths being checked, and expected evidence. Passing an unrelated existing suite is not evidence for new behavior; plan the necessary coverage within the slice.
- Organize and name test directories, files, and suites by the component, behavior, or user workflow they exercise, following repository conventions. Do not encode delivery chronology with slice numbers or names.
- Assign test delivery and validation to slices in the plan and ledger. Later slices should extend the relevant existing suites and fixtures instead of creating a new test area for each slice.
- Use focused interface or data examples only when they remove material ambiguity; do not prescribe a full patch.
- Include manual verification only when automation genuinely cannot manage the relevant risk.
- Use the exact field `Manual verification checkpoint: none` when no blocking checkpoint is required. Otherwise put a nonempty reason on that field's first line, followed by setup, operator actions, expected results, and resume condition in its continuation. AFK mode always uses `none`.
- Carry forward only execution-critical evidence.
- Put every execution-critical behavioral rule in the plan: required outcomes, contracts, invariants, failure semantics, and exclusions. Keep shared rules in a compact plan-level section and identify which apply to each slice; keep slice-specific instructions with the slice. Do not rely on the executor voluntarily revisiting the design to discover requirements.
- Link to specific design sections for deeper rationale, alternatives, and reference examples rather than copying them wholesale. If execution requires reading a particular source or reference section, make that a named prerequisite of the owning slice and state what it informs. Generic instructions such as "follow the design" or "inherit all behavior" do not replace concrete requirements.

Before writing, check the handoff against the accepted input:
- Map every in-scope design/request requirement, including material edge cases and exclusions, to an explicit plan instruction, owning slice, and validation evidence where applicable.
- Check that the plan, relevant shared constraints, and active slice tell the executor what to change and how to establish correctness without mining an upstream document for missing behavior. Repair omissions instead of adding a blanket design reference.
- Keep length proportional to the instructions needed for correct execution. A shorter plan than its design is acceptable; brevity is not a reason to remove required behavior or validation.

### 6. Write compatible artifacts

Write:

- `thoughts/plans/YYYY-MM-DD-descriptive-name.md`
- `thoughts/plan-status/YYYY-MM-DD-descriptive-name.status.md`

Use today’s date and the same descriptive name for both.

Initialize the ledger's execution mode as `continuous` unless the caller explicitly selects another mode. This does not change the separate automation mode or remove required validation and checkpoints.

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
- Design Doc: [supplied path or `incorporated inline`]
- Structured Outline: `incorporated inline`

## Research Anchor
- [Execution-critical repository findings with file references]
- [Inherited constraints and scope boundary]
- [Research freshness check and disposition of relevant open questions]

## Inline Decisions
- [Inherited design decision and section reference, or new implementation choice with evidence]

## Status Ledger Path
- `thoughts/plan-status/YYYY-MM-DD-descriptive-name.status.md`

## Execution Strategy
- [Why this is the minimum viable change]
- [Slice structure and validation approach]
- [Explicit PR/review boundaries and their dependencies, when supplied]

## Execution Slices
1. [Slice]
   - Objective: [Observable outcome; acceptance criteria AC1, ...]
   - Dependencies: [Earlier slices or none]
   - Review boundary: [Owning PR/review boundary, when specified]
   - Key touchpoints: [Files/symbols and implementation/test pattern references]
   - Planned change: [Concrete behavior, interfaces, invariants, failure/edge-case semantics, applicable shared constraints, and exclusions]
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
- Design Doc: [supplied path or `incorporated inline`]
- Automation mode: [same as plan]
- Overall status: `not_started`
- Execution mode: `continuous`
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
   - Review boundary: [Same owning PR/review boundary as the plan, when specified]
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

- The plan fully satisfies the accepted scope with the smallest justified change surface and preserves any supplied design's requirements and exclusions.
- Every important choice is supported by the supplied design, an existing pattern, or a recorded inline decision.
- The supplied design remains linked, and explicit PR/review boundaries are preserved in both artifacts. Section references provide deeper context without replacing executable slice requirements.
- Execution-critical requirements are explicit in the plan and assigned to slices; neither a blanket reference nor the executor's initiative to reread the design is needed to discover required behavior.
- Concrete files, components, interfaces, and tests are named where they reduce execution risk.
- Each slice has a specific validation path and completion signal.
- The plan and ledger are compatible with `implement-plan`.
- No unresolved escalation trigger remains.
- Every acceptance criterion maps to implementation and meaningful validation; no material behavior or contract decision is left to the executor.
- Automation modes agree, slice numbers/names/order match, and checkpoint fields use the exact syntax above.
- After writing both artifacts, report their paths and the key scope assumption.

When evaluating changes to this workflow, use [the evaluation protocol](references/workflow-evaluation.md). It separates research, planning, implementation, and end-to-end performance; it is not required reading for ordinary plan creation.

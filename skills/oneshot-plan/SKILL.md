---
name: oneshot-plan
description: Turn a bounded ticket, request, or research artifact directly into a minimum-viable executable implementation plan and companion status ledger without requiring separate design or outline phases. Use for small, well-scoped work that should follow existing codebase patterns and produce the same plan artifacts as create-plan.
---

# Oneshot Plan

Produce an execution-ready plan in one pass. Internally perform only the research, design, and outlining needed to remove implementation ambiguity; do not create separate research, design, or outline artifacts.

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
- Find existing implementation and test patterns before proposing a new design.
- Identify the authoritative aggregate verification command. Use it exclusively when repository instructions declare one.
- Keep discovery targeted; do not perform broad research when local evidence resolves the plan.

### 3. Resolve design inline

- Follow an existing repository pattern when it satisfies the ticket and current constraints.
- When multiple architectures appear viable, first resolve the choice by finding the closest established pattern and selecting it.
- Prefer the option with the smallest change surface and lowest new conceptual overhead.
- Record consequential choices briefly under `Inline Decisions`.
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
- For each slice include its objective, concrete touchpoints, planned change, automated validation, and completion signal.
- Include manual verification only when automation genuinely cannot manage the relevant risk.
- In `Automation mode: afk`, include no manual checkpoint or human-gated ledger requirement.
- Carry forward only execution-critical evidence.

### 6. Write compatible artifacts

Write:

- `thoughts/plans/YYYY-MM-DD-descriptive-name.md`
- `thoughts/plan-status/YYYY-MM-DD-descriptive-name.status.md`

Use today’s date and the same descriptive name for both.

The plan must contain:

```markdown
# Implementation Plan: [Topic]

## Scope
- [Minimum viable outcome]
- [Explicit non-goals]

## Input Artifacts
- Ticket/Request: [reference or inline prompt]
- Research: [path or `incorporated inline`]
- Design Doc: `incorporated inline`
- Structured Outline: `incorporated inline`

## Research Anchor
- [Execution-critical repository findings with file references]
- [Inherited constraints and scope boundary]

## Inline Decisions
- [Decision, selected existing pattern, and evidence]

## Status Ledger Path
- `thoughts/plan-status/YYYY-MM-DD-descriptive-name.status.md`

## Execution Strategy
- [Why this is the minimum viable change]
- [Slice structure and validation approach]

## Execution Slices
1. [Slice]
   - Objective
   - Key touchpoints
   - Planned change
   - Automated validation
   - Completion signal
   - Manual verification checkpoint only if necessary

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

Add all remaining slices to `Slice Status`. Use only `pending | in_progress | complete | manual_checkpoint | blocked | cancelled`.

## Quality bar

- The plan fully satisfies the ticket with the smallest justified change surface.
- Every important choice is supported by an existing pattern or recorded inline decision.
- Concrete files, components, interfaces, and tests are named where they reduce execution risk.
- Each slice has a specific validation path and completion signal.
- The plan and ledger are compatible with `implement-plan`.
- No unresolved escalation trigger remains.
- After writing both artifacts, report their paths and the key scope assumption.

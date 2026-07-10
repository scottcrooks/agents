---
name: create-plan
description: Expand a structured outline into an executable implementation plan with sequencing, validation, and explicit testing coverage
---

# Create Plan

Use this skill when the user wants a fully executable implementation plan from an existing structured outline.

This skill should answer: exactly how do we execute this safely and verify it worked?

Operating contract:
- The structured outline is the required primary input artifact for this phase.
- Expand the structured outline into a complete execution plan without re-opening design exploration.
- Preserve explicit links to the structured outline, design doc, and research doc so execution can follow a stable artifact chain.
- Carry forward only the execution-critical context from upstream artifacts; do not restate the entire research or design history.
- Do not broaden scope beyond what the upstream artifacts and research boundary establish.
- Prefer vertical execution slices over horizontal layer-by-layer plans unless the upstream artifacts explicitly require another structure.
- Default to 3-7 thin execution slices. Prefer more small slices over fewer large ones when both are viable.
- Build validation into the plan between slices so each major increment is tested before moving on.
- Prefer automated checkpoints as the default verification path for every slice.
- Continue executing as many slices as can be validated automatically before handing back for human verification.
- Only require human verification when automation is genuinely insufficient for the risk being managed.
- When human verification is required, include exact verification instructions, expected outcomes, and the reason automation does not fully cover that slice.
- Reserve and record a companion status ledger path for resumed execution progress.

The output of this skill should be execution-sufficient with linked anchors. It must not force the implementer to rediscover the codebase, but it also should not inline the entire design doc or research when a compact digest plus explicit artifact links will do.

## Boundaries

This skill should include:
- Concrete implementation steps
- Sequencing
- Validation steps
- Specific test activities
- Explicit input artifact links for research, design, and outline
- A compact research digest with only execution-critical findings
- A companion status ledger path and initialized ledger stub
- Enough carried-forward context that the plan can be executed safely without broad rediscovery
- Concrete targets such as files, components, interfaces, and integration points when relevant to execution
- Automated validation steps derived from the repository where possible
- Thin vertical slices or similarly incremental execution chunks when the work can be structured that way
- Manual verification checkpoints only where user-visible behavior, workflows, or operational outcomes cannot be covered sufficiently by automation
- Detailed human verification instructions whenever a manual checkpoint is included

This skill may include:
- Concrete validation activities such as verifying behaviors, confirming edge cases, and regression-testing affected pathways

This skill does not require:
- Full test code, unless the user explicitly asks for it

Code snippets in this phase:
- Include code snippets only when they materially reduce ambiguity in the execution plan or show how to apply a referenced pattern from the upstream artifacts
- Prefer targeted snippets for tricky interfaces, data shapes, sequencing-sensitive changes, or pattern application points
- Keep snippets focused and bounded rather than trying to provide full implementations
- Do not include full test code unless the user explicitly asks for it

## Initial Response

When invoked:

1. If the user provided a structured outline:
   - Read the structured outline fully
   - Read the design doc as needed to recover rationale that was intentionally compressed out of the outline
   - Read research only as needed to confirm boundaries or constraints
   - Preserve the outline path, design doc path, and research doc path for the final plan
   - Use the structured outline as the primary source for plan shape
   - Do not broaden scope beyond what the research established unless the user explicitly asks for more research
2. If no upstream artifact was provided, ask for:
   - The structured outline
   - Any verification requirements or rollout constraints

## Workflow

### 1. Lock the execution scope

- Confirm the implementation target from the input artifacts
- Preserve stated non-goals and constraints
- Preserve the upstream artifact chain and make missing links a blocking error before finalizing the plan
- Call out any missing prerequisite information before writing the plan
- Pull forward any assumptions, constraints, and rationale that are required for safe execution

### 2. Expand the outline into executable work

- Break each phase into concrete implementation steps
- Sequence the steps in a safe order
- Name the concrete files, components, interfaces, integration points, dependencies, and risk areas only where they materially reduce execution risk
- Expand the compressed outline into actionable detail without re-opening high-level design debates
- Inline only the critical context needed to perform the work safely; rely on linked upstream artifacts for deeper rationale
- Make the execution order specific enough that an implementer can follow it directly
- Prefer end-to-end vertical slices that deliver a thin but testable increment before expanding breadth
- Default to 3-7 thin slices. Each slice should usually fit one focused implementation pass plus validation.
- Prefer more small slices over fewer large slices when scope can be split cleanly
- Avoid defaulting to horizontal sequencing like database first, then services, then frontend, unless the upstream artifacts explicitly require that shape
- Make each slice small enough that verification can happen before the next slice begins
- Each slice should include only the objective, key touchpoints, planned change, validation, completion signal, and any required manual checkpoint
- Prefer grouping consecutive slices under agent execution when their checkpoints can be satisfied automatically without operator intervention

### 3. Define verification

- Include explicit validation steps for the intended behavior
- Tie verification to the execution so the reader knows how to confirm each major part worked
- Derive automated validation steps from the repository when possible
- Look for checks that are common for the tech stack in use
- Prefer checks defined in repository sources such as `README`, `Makefile`, `package.json`, language-specific project files, or similar project entry points
- If the repository does not define checks explicitly, infer the most likely automated validation based on the tech stack and existing conventions
- Default to automated validation per slice before proposing any manual checkpoint
- Treat missing automation as a gap to close when it is realistic to add or adapt a test, script, fixture, or command within the slice
- State specific test activities such as:
  - Verify X behavior
  - Confirm Y edge case
  - Regression-test Z pathway
- Include manual or automated verification guidance where relevant
- State success criteria clearly enough that the implementer can tell whether the change is complete
- Prefer automated checks after each slice and call out the exact command, test target, or script to run
- Add manual verification checkpoints only when correctness depends on user-visible behavior, cross-system effects, or subjective confirmation that automation alone will not cover well
- Defer handoff for human verification until the latest safe slice boundary, so the agent completes as much implementation work as possible first
- For each manual checkpoint, state:
  - Why human verification is still required
  - Prerequisites or setup data
  - Exact operator actions in order
  - Expected results and failure signals
  - Whether the checkpoint is blocking for the next slice
- Make it clear which validation happens before proceeding to the next slice
- Make it clear whether the agent should continue automatically after a checkpoint or pause for operator confirmation

### 4. Define the status ledger

- Reserve a companion status ledger path under `thoughts/plan-status/` using the same date and descriptive name as the plan plus a `.status.md` suffix
- Write an initialized ledger stub alongside the plan
- Make the ledger the mutable execution-state artifact while keeping the plan mostly stable
- Include per-slice entries in the ledger with:
  - Slice name
  - Status: `pending | in_progress | complete | blocked`
  - Started at
  - Completed at
  - Validation result
  - Notes limited to execution facts

### Subagent usage

- Do not spawn subagents by default. Build the plan from the structured outline, linked upstream artifacts, and targeted direct inspection.
- Do not use parallel fan-out for plan creation.
- Use at most one read-only subagent only when a specific execution-critical gap cannot be resolved efficiently through targeted direct inspection.
- Keep that task narrow: one code path, interface, validation command, or existing pattern. Forbid further delegation.
- Prefer `codebase-pattern-finder` for one concrete implementation or test pattern and `codebase-analyzer` for one precise code path or interface.
- Require concrete file:line references and a concise result. Do not delegate broad discovery, plan synthesis, or duplicate questions.
- If no subagent is needed, proceed directly to writing the plan.

### 5. Use patterns correctly

Patterns become concrete only where needed in this phase.

- Convert relevant pattern guidance into actionable execution steps
- Reuse existing patterns when they reduce risk or preserve consistency
- Do not add pattern-driven work that is outside the chosen scope

## Output

Write the implementation plan to:

- `thoughts/plans/YYYY-MM-DD-descriptive-name.md`
- Use today's date in `YYYY-MM-DD` format
- Use a short kebab-case descriptive name

Also initialize the companion status ledger at:

- `thoughts/plan-status/YYYY-MM-DD-descriptive-name.status.md`

Produce the implementation plan with this shape:

```markdown
# Implementation Plan: [Topic]

## Scope
- [What is being implemented]
- [Non-goals or exclusions]

## Input Artifacts
- Research: [path]
- Design Doc: [path]
- Structured Outline: [path]

## Research Anchor
- [4-8 execution-critical findings carried forward from research]
- [Critical citation or concrete reference]
- [Explicit scope boundary inherited from research]

## Status Ledger Path
- `thoughts/plan-status/YYYY-MM-DD-descriptive-name.status.md`

## Execution Strategy
- [Vertical slices or other chosen structure]
- [Why this thin-slice shape reduces risk]
- [Why human handoff occurs at this boundary instead of earlier]

## Execution Slices
1. [Slice]
   - Objective
   - Key touchpoints
   - Planned change
   - Automated validation
   - Completion signal
   - Manual verification checkpoint if needed, with exact operator instructions
2. [Slice]
   - Objective
   - Key touchpoints
   - Planned change
   - Automated validation
   - Completion signal
   - Manual verification checkpoint if needed, with exact operator instructions

## Cross-Slice Validation
- Verify [X behavior]
- Confirm [Y edge case]
- Regression-test [Z pathway]
- Run [repo-derived automated check]
- [Explicit success check or completion signal]

## Testing Coverage
- [Unit or component coverage]
- [Integration or end-to-end coverage]
- [Manual validation only if automation is insufficient, with detailed operator instructions]
- [Automated checks derived from README, Makefile, package.json, or equivalent repo sources]

## Pattern Application
- [Pattern]
- [How it changes execution decisions]
```

Initialize the companion status ledger with this shape:

```markdown
# Plan Status: [Topic]

## Metadata
- Plan: [path]
- Research: [path]
- Overall status: `not_started`
- Current slice: [first slice]
- Last completed slice: none
- Next action: [start slice 1]
- Last updated: [ISO timestamp]

## Slice Status
1. [Slice]
   - Status: `pending`
   - Started at: not started
   - Completed at: not completed
   - Validation: not run
   - Notes: none
2. [Slice]
   - Status: `pending`
   - Started at: not started
   - Completed at: not completed
   - Validation: not run
   - Notes: none
```

## Quality Bar

- The plan should be executable without inventing missing steps
- Preserve the research, design, and outline links explicitly so execution has a deterministic artifact chain
- Sequencing should reduce risk and make validation possible after each major change
- Verification should be specific enough to detect regressions
- Automated validation should come from the repository's actual tooling and conventions whenever possible
- Each slice should have an explicit automated checkpoint unless the plan explains why that is not possible
- Default to 3-7 thin slices with minimal repeated context and only execution-critical detail
- The plan should maximize uninterrupted agent execution and avoid handing back to a human until a real human-only gate is reached
- The output should include implementation details, execution order, verification steps, and explicit testing coverage
- Any code snippets should clarify execution-critical details or referenced pattern application without replacing the plan with a full patch
- The plan and ledger together should let an implementer resume without broad rediscovery
- If unresolved design questions remain, stop and resolve them before finalizing the plan
- Prefer plans that move in vertical, testable slices with validation between increments
- Include manual verification checkpoints only where appropriate, and make them precise enough that another operator can execute them without improvising
- After writing the plan and ledger, provide both paths, summarize important assumptions, and ask for review before handoff to `implement-plan`

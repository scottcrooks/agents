---
name: implementation-plan
description: Expand a structured outline into an executable implementation plan with sequencing, validation, and explicit testing coverage
---

# Implementation Plan

Use this skill when the user wants a fully executable implementation plan from an existing structured outline.

This skill should answer: exactly how do we execute this safely and verify it worked?

Operating contract:
- The structured outline is the required primary input artifact for this phase.
- Expand the structured outline into a complete execution plan without re-opening design exploration.
- Carry forward enough context that the final plan is self-sufficient during execution.
- Do not broaden scope beyond what the upstream artifacts and research boundary establish.
- Prefer vertical execution slices over horizontal layer-by-layer plans unless the upstream artifacts explicitly require another structure.
- Build validation into the plan between slices so each major increment is tested before moving on.
- Include manual verification checkpoints when human confirmation is the safest or clearest way to validate behavior.

The output of this skill must be fully executable without requiring the reader to consult the design doc, structured outline, or research during execution. Any context needed to execute safely should be carried forward into the plan itself.

## Boundaries

This skill should include:
- Concrete implementation steps
- Sequencing
- Validation steps
- Specific test activities
- Enough carried-forward context that the plan can be executed on its own
- Concrete targets such as files, components, interfaces, and integration points when relevant to execution
- Automated validation steps derived from the repository where possible
- Vertical slices or similarly incremental execution chunks when the work can be structured that way
- Manual verification checkpoints where user-visible behavior, workflows, or operational outcomes need human confirmation

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
   - Use the structured outline as the primary source for plan shape
   - Do not broaden scope beyond what the research established unless the user explicitly asks for more research
2. If no upstream artifact was provided, ask for:
   - The structured outline
   - Any verification requirements or rollout constraints

## Workflow

### 1. Lock the execution scope

- Confirm the implementation target from the input artifacts
- Preserve stated non-goals and constraints
- Call out any missing prerequisite information before writing the plan
- Pull forward any assumptions, constraints, and rationale that are required for safe execution

### 2. Expand the outline into executable work

- Break each phase into concrete implementation steps
- Sequence the steps in a safe order
- Name the concrete files, components, interfaces, integration points, dependencies, and risk areas where relevant
- Expand the compressed outline into actionable detail without re-opening high-level design debates
- Inline the critical context needed to perform the work so the reader does not need to refer back to prior artifacts
- Make the execution order specific enough that an implementer can follow it directly
- Prefer end-to-end vertical slices that deliver a thin but testable increment before expanding breadth
- Avoid defaulting to horizontal sequencing like database first, then services, then frontend, unless the upstream artifacts explicitly require that shape
- Make each slice small enough that verification can happen before the next slice begins

### 3. Define verification

- Include explicit validation steps for the intended behavior
- Tie verification to the execution so the reader knows how to confirm each major part worked
- Derive automated validation steps from the repository when possible
- Look for checks that are common for the tech stack in use
- Prefer checks defined in repository sources such as `README`, `Makefile`, `package.json`, language-specific project files, or similar project entry points
- If the repository does not define checks explicitly, infer the most likely automated validation based on the tech stack and existing conventions
- State specific test activities such as:
  - Verify X behavior
  - Confirm Y edge case
  - Regression-test Z pathway
- Include manual or automated verification guidance where relevant
- State success criteria clearly enough that the implementer can tell whether the change is complete
- Prefer automated checks after each slice where possible
- Add manual verification checkpoints after slices when correctness depends on user-visible behavior, cross-system effects, or subjective confirmation that automation alone will not cover well
- Make it clear which validation happens before proceeding to the next slice

### Subagent usage

- Read the structured outline yourself before spawning any subagents
- CRITICAL: Every spawned subagent must have `$caveman` enabled in its initial prompt/context
- Use subagents to preserve main-context focus by delegating narrow discovery tasks needed to make the plan executable
- Prefer `codebase-pattern-finder` when you need concrete examples of existing implementation or test patterns to carry forward into the plan
- Prefer `codebase-analyzer` when you need a precise explanation of a specific code path, integration point, or interface
- Give subagents tightly scoped tasks such as "find existing test patterns for this workflow" or "analyze how this integration currently works"
- Ask subagents to report back with concrete file:line references, relevant snippets, and concise summaries
- Use subagent findings to refine concrete steps and repo-derived validation, then carry the needed context into the final plan

### 4. Use patterns correctly

Patterns become concrete only where needed in this phase.

- Convert relevant pattern guidance into actionable execution steps
- Reuse existing patterns when they reduce risk or preserve consistency
- Do not add pattern-driven work that is outside the chosen scope

## Output

Write the implementation plan to:

- `thoughts/plans/YYYY-MM-DD-descriptive-name.md`
- Use today's date in `YYYY-MM-DD` format
- Use a short kebab-case descriptive name

Produce the implementation plan with this shape:

```markdown
# Implementation Plan: [Topic]

## Scope
- [What is being implemented]
- [Non-goals or exclusions]

## Execution Context
- [Constraint that materially affects execution]
- [Assumption or dependency the implementer must know]

## Execution Strategy
- [Vertical slices or other chosen structure]
- [Why this execution shape reduces risk]

## Execution Slices
1. [Slice]
   - Objective
   - Concrete implementation steps
   - Dependencies or file/component touchpoints
   - Automated validation
   - Manual verification checkpoint if needed
2. [Slice]
   - Objective
   - Concrete implementation steps
   - Dependencies or file/component touchpoints
   - Automated validation
   - Manual verification checkpoint if needed

## Implementation Details
- [Specific component or file area and what changes]
- [Integration point or dependency]

## Cross-Slice Validation
- Verify [X behavior]
- Confirm [Y edge case]
- Regression-test [Z pathway]
- Run [repo-derived automated check]
- [Explicit success check or completion signal]

## Testing Coverage
- [Unit or component coverage]
- [Integration or end-to-end coverage]
- [Manual validation if needed]
- [Automated checks derived from README, Makefile, package.json, or equivalent repo sources]

## Pattern Application
- [Pattern]
- [How it changes execution decisions]
```

## Quality Bar

- The plan should be executable without inventing missing steps
- Sequencing should reduce risk and make validation possible after each major change
- Verification should be specific enough to detect regressions
- Automated validation should come from the repository's actual tooling and conventions whenever possible
- The output should include implementation details, execution order, verification steps, and explicit testing coverage
- Any code snippets should clarify execution-critical details or referenced pattern application without replacing the plan with a full patch
- The reader should not need any other artifact to execute the plan safely
- If unresolved design questions remain, stop and resolve them before finalizing the plan
- Prefer plans that move in vertical, testable slices with validation between increments
- Include manual verification checkpoints where appropriate instead of pretending automation fully covers the risk

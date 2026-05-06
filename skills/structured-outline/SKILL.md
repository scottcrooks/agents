---
name: structured-outline
description: Convert a chosen design into a high-level execution outline with phases, dependencies, validation areas, and pattern guidance
---

# Structured Outline

Use this skill when the design has been chosen and the user wants the top-level shape of execution without implementation detail.

This skill should answer: what is the shape of the plan?

Operating contract:
- Start this skill in `$caveman` mode automatically.
- If `$caveman` is already active from earlier context, preserve it through this skill and across later skill handoffs.
- Do not turn `$caveman` off unless the operator explicitly says `stop caveman` or `normal mode`.
- If the operator asks for more detail, provide it in `$caveman` style unless they explicitly turn the mode off.
- The design doc is the primary source artifact for this phase.
- Preserve the chosen design as plan structure rather than re-evaluating architecture.
- Preserve execution shape without introducing implementation detail.
- Carry forward relevant pattern references as guidance for the eventual implementation plan.
- Do not broaden scope beyond what the design doc and research boundary establish.
- A design doc alone is sufficient input to begin this phase.
- If the design doc leaves any execution-shaping question unresolved, stop and ask the user before writing the outline.
- Default to vertical slices when the design doc does not already make the execution approach clear.
- Only choose a non-vertical execution shape when there is a strong, explicit reason grounded in the design doc, hard constraints, or the nature of the work.
- If a strong reason exists to avoid vertical slices, explain that reasoning briefly and ask the user for feedback before finalizing the outline.

## Boundaries

This skill should include:
- Major phases or workstreams
- High-level ordering and dependencies
- Validation areas
- What behaviors and user-visible outcomes will be tested
- Reviewable test case shape expressed in a BDD style when helpful
- Relevant pattern references that should guide the eventual implementation plan
- The intended execution approach, such as vertical slices versus horizontal layering, when that affects the outline shape
- Small illustrative code snippets when they materially help the reviewer understand the pattern the plan intends to follow

This skill should not include:
- Implementation details
- Exact file changes
- Exact commands
- Step-by-step instructions
- Test code

Code snippets in this phase:
- Prefer short, focused code snippets when they help the reviewer quickly understand an existing pattern the outline is likely to follow
- Keep snippets illustrative rather than implementation-ready
- Use snippets to show pattern shape, boundaries, or integration style, not to specify exact edits
- Pair each snippet with a brief explanation of why that pattern is relevant to the outline
- Do not include enough code detail that the outline becomes an implementation plan or task list

Someone reading the result should understand the execution shape, but should not be able to implement directly from this artifact alone.

## Initial Response

When invoked:

0. Enter or preserve `$caveman` mode immediately for the main skill response.
   - Carry `$caveman` forward across any later skill invocation unless the operator explicitly turns it off.

1. If the user provided a design doc:
   - Read the design doc fully
   - Read research only as needed to confirm scope boundaries or preserve critical constraints
   - Treat the design doc as the primary source artifact for this phase
   - Do not broaden scope beyond what the research established unless the user explicitly asks for more research
   - Try to derive the outline directly from the design doc first
   - If the design doc leaves unclear sequencing, dependency, validation, scope-boundary, or execution-approach questions that materially affect the outline, ask the user before drafting
2. If no design context was provided, ask for:
   - The design doc
   - Any hard sequencing constraints
   - Any required validation or delivery milestones

Required gating before drafting:
- You must know the selected design well enough to shape execution without re-deciding architecture
- You must know the major sequencing and dependency assumptions needed to structure the outline
- If any execution-shaping question remains open, ask the user first instead of guessing

## Workflow

### 1. Confirm the chosen design

- Extract the selected approach and the constraints that affect sequencing
- Preserve any explicit decisions that change how work should be grouped
- Compress design reasoning into execution shape rather than carrying forward full design detail
- Identify any unresolved execution-shaping questions from the design doc, such as unclear phase boundaries, ambiguous dependencies, missing validation expectations, missing sequencing constraints, or unclear slice strategy
- If those questions materially change the shape of the outline, stop and ask the user before continuing
- If execution approach is not specified, assume vertical slices because they support incremental stubs, proof-of-concept work, and validation along the way
- If the design doc or constraints strongly indicate a different structure, explain the reason briefly and ask the user for feedback before finalizing the outline

### Subagent usage

- This phase should usually work directly from the design doc without subagents
- CRITICAL: If you spawn any subagent, include `$caveman` in its initial prompt/context
- Only use a subagent if a narrowly scoped clarification is needed to preserve an important boundary, dependency, or pattern reference
- If needed, prefer a single focused task that reports back with concise findings rather than broad exploration

### 2. Shape the plan

- Break the work into major phases or workstreams
- Show dependencies and ordering at a high level
- Keep granularity coarse enough that it describes structure, not implementation
- Do not invent missing sequencing decisions just to complete the outline
- Prefer vertical-slice workstreams that each carry a thin end-to-end path through the system, along with any stub, proof-of-concept, or validation activity needed to de-risk that slice
- Avoid defaulting to horizontal phases like database first, then services, then frontend, unless the user or design doc explicitly requires that structure

### 3. Define validation areas

- Describe what will be tested or validated, not test code or detailed test implementation
- Focus on behavior, user-visible outcomes, coverage areas, and risk surfaces
- Frame validation so the reviewer can inspect test cases and overall system behavior, not just inferred unit-test coverage
- Prefer BDD-style validation descriptions such as given/when/then or scenario-oriented outcome statements when that makes the review sharper
- Do not include test code or exact commands
- If required validation areas are unclear and that uncertainty would change the outline structure, ask the user before writing

### 4. Use patterns correctly

Patterns are guidance in this phase.

- Carry forward relevant patterns from the design doc or research
- Reference them as constraints or shaping guidance for the future implementation plan
- When helpful, include a small snippet from an existing pattern so the reviewer can see the shape being referenced without opening links
- Do not convert pattern guidance into concrete edit steps here

## Output

Only after required execution-shaping questions are resolved:

Write the structured outline to:

- `thoughts/outlines/YYYY-MM-DD-descriptive-name.md`
- Use today's date in `YYYY-MM-DD` format
- Use a short kebab-case descriptive name

Produce the outline with this shape:

```markdown
# Structured Outline: [Topic]

## Selected Direction
- [Chosen design summarized briefly]

## Execution Approach
- [Vertical slices or other chosen structure]
- [Why this shape fits the work]

## Major Phases / Workstreams
1. [Phase or workstream]
   - Purpose
   - Key dependency notes
2. [Phase or workstream]
   - Purpose
   - Key dependency notes

## Ordering / Dependency Structure
- [What must happen first]
- [What can proceed in parallel]

## Validation Areas
- [Behavior or integration area to validate]

## Test Coverage Shape
- [BDD-style behavior or scenario family to validate at a high level]
- [What overall behavior the reviewer should inspect, independent of test implementation]

## Pattern References
- [Pattern]
- [How it should guide the eventual plan]
- [Optional short illustrative snippet and why it matters]
```

## Quality Bar

- Preserve execution shape without drifting into implementation
- Keep sequencing explicit at the phase level
- Make validation coverage visible even when details are deferred
- Make behavior-oriented review visible so the reader can assess expected outcomes without reading test code
- Prefer test coverage descriptions that read like reviewable scenarios rather than implementation-centric test buckets
- Use code snippets only when they clarify pattern intent better than links alone
- Do not include code snippets that would let the reader implement directly from the outline
- Someone reading the outline should understand the shape of execution, but should not be able to implement directly from it
- Do not write the outline if unresolved questions would materially change phase structure, ordering, dependencies, or validation areas
- Do not write the outline if the execution approach is materially unclear
- Prefer outlines that organize work as vertical slices with incremental validation unless there is a clear reason not to
- When deviating from vertical slices, make that deviation explicit and ask the user for feedback before finalizing the outline
- If the user wants executable steps next, hand off naturally to `implementation-plan`

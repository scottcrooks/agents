---
name: structured-outline
description: Convert a chosen design into a high-level execution outline with phases, dependencies, validation areas, and pattern guidance
---

# Structured Outline

Use this skill when the design has been chosen and the user wants the top-level shape of execution without implementation detail.

This skill should answer: what is the shape of the plan?

Operating contract:
- The design doc is the primary source artifact for this phase.
- Preserve the chosen design as plan structure rather than re-evaluating architecture.
- Preserve execution shape without introducing implementation detail.
- Carry forward relevant pattern references as guidance for the eventual implementation plan.
- Do not broaden scope beyond what the design doc and research boundary establish.

## Boundaries

This skill should include:
- Major phases or workstreams
- High-level ordering and dependencies
- Validation areas
- What will be tested
- Relevant pattern references that should guide the eventual implementation plan

This skill should not include:
- Implementation details
- Exact file changes
- Exact commands
- Step-by-step instructions
- Test code

Code snippets in this phase:
- Do not include code snippets
- If a pattern must be referenced, describe it at a structural level instead of embedding code

Someone reading the result should understand the execution shape, but should not be able to implement directly from this artifact alone.

## Initial Response

When invoked:

1. If the user provided a design doc:
   - Read the design doc fully
   - Read research only as needed to confirm scope boundaries or preserve critical constraints
   - Treat the design doc as the primary source artifact for this phase
   - Do not broaden scope beyond what the research established unless the user explicitly asks for more research
2. If no design context was provided, ask for:
   - The design doc
   - Any hard sequencing constraints
   - Any required validation or delivery milestones

## Workflow

### 1. Confirm the chosen design

- Extract the selected approach and the constraints that affect sequencing
- Preserve any explicit decisions that change how work should be grouped
- Compress design reasoning into execution shape rather than carrying forward full design detail

### Subagent usage

- This phase should usually work directly from the design doc without subagents
- Only use a subagent if a narrowly scoped clarification is needed to preserve an important boundary, dependency, or pattern reference
- If needed, prefer a single focused task that reports back with concise findings rather than broad exploration

### 2. Shape the plan

- Break the work into major phases or workstreams
- Show dependencies and ordering at a high level
- Keep granularity coarse enough that it describes structure, not implementation

### 3. Define validation areas

- Describe what will be tested or validated, not test code or detailed test implementation
- Focus on coverage areas and risk surfaces
- Do not include test code or exact commands

### 4. Use patterns correctly

Patterns are guidance in this phase.

- Carry forward relevant patterns from the design doc or research
- Reference them as constraints or shaping guidance for the future implementation plan
- Do not convert pattern guidance into concrete edit steps here

## Output

Write the structured outline to:

- `thoughts/outlines/YYYY-MM-DD-descriptive-name.md`
- Use today's date in `YYYY-MM-DD` format
- Use a short kebab-case descriptive name

Produce the outline with this shape:

```markdown
# Structured Outline: [Topic]

## Selected Direction
- [Chosen design summarized briefly]

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
- [What will be tested at a high level]

## Pattern References
- [Pattern]
- [How it should guide the eventual plan]
```

## Quality Bar

- Preserve execution shape without drifting into implementation
- Keep sequencing explicit at the phase level
- Make validation coverage visible even when details are deferred
- Do not include code snippets that would let the reader implement directly from the outline
- Someone reading the outline should understand the shape of execution, but should not be able to implement directly from it
- If the user wants executable steps next, hand off naturally to `implementation-plan`

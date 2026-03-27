---
name: design-doc
description: Turn research into a proposed solution by evaluating alternatives, tradeoffs, decisions, and relevant patterns
---

# Design Doc

Use this skill to turn research into a high-level design recommendation.

Core question: what should we do, and why this approach over the alternatives?

Operating contract:
- Research is the authoritative boundary for scope and problem framing.
- Do not expand scope beyond research unless the user explicitly asks for more research.
- This skill produces design decisions, not execution instructions.

## Boundaries

This skill should include:
- Problem framing derived from the supplied research
- Constraints that materially affect the solution
- Candidate approaches
- A recommended approach
- Tradeoffs
- Resolved questions and decisions
- Relevant pattern references and why they apply or do not apply

This skill should not include:
- Implementation task lists
- File-by-file edits
- Detailed sequencing
- Step-by-step execution instructions

Code snippets in this phase:
- Include a code snippet only when it materially helps explain a pattern fit, tradeoff, or architectural choice
- Keep snippets short and illustrative rather than implementation-ready
- Do not include enough code detail that the document becomes an execution plan

## Initial Response

When invoked:

1. If the user provided research docs, tickets, or file paths:
   - Read them fully before doing anything else
   - Treat that research as the source of truth for problem framing
   - Do not rewrite or expand the research phase itself
   - Do not broaden scope beyond what the research established unless the user explicitly asks for more research
2. If no supporting context was provided, ask for:
   - The research document or ticket
   - Any constraints or non-goals
   - Any existing patterns or prior implementations that should be considered as supporting references

## Workflow

### 1. Establish the problem from research

- Summarize the problem the research actually supports
- Pull out constraints, non-goals, and assumptions
- Identify the decisions that still need to be made
- Keep the artifact at a high architectural level rather than drifting into implementation planning

### 2. Evaluate candidate approaches

- Identify the realistic solution options
- Compare them against the constraints from the research
- Call out where an option introduces complexity, risk, or future maintenance cost

### 3. Use patterns correctly

Patterns are inputs to design evaluation in this phase.

- Reference existing code or documented patterns when they help assess an approach
- Explain why a pattern fits, partially fits, or does not fit
- Use pattern references to support tradeoff analysis, not to prescribe implementation steps
- Use codebase evidence only to evaluate approaches within the researched boundary, not to perform a new discovery or planning pass

### Subagent usage

- Read directly provided critical artifacts yourself before spawning any subagents
- Use subagents to preserve main-context focus by delegating narrow, specific documentation tasks
- Prefer `codebase-pattern-finder` when you need concrete examples of an existing pattern or similar implementation
- Prefer `codebase-analyzer` when you need a precise explanation of how a specific component or code path works
- Give subagents a tightly scoped task such as "analyze this code path" or "find examples of this pattern and report back with file:line references"
- Ask subagents to report findings back with concrete file:line references and concise summaries
- Verify surprising or conflicting findings before using them in the design doc

### 4. Resolve open questions

- Resolve design questions wherever the research and bounded pattern evidence allow
- If something remains unresolved, stop and ask only the specific question needed to make the design decision
- Continue the design discussion until all design-relevant open questions are resolved
- Do not carry unresolved questions into the final artifact unless the user explicitly wants a decision log with open items

## Output

Write the design document to:

- `thoughts/designs/YYYY-MM-DD-descriptive-name.md`
- Use today's date in `YYYY-MM-DD` format
- Use a short kebab-case descriptive name

Produce the design document with this shape:

```markdown
# Design Doc: [Topic]

## Problem Framing
- [What the research says we need to solve]

## Constraints
- [Constraint]

## Candidate Approaches
1. [Approach]
   - Why it could work
   - Why it may not fit
2. [Approach]
   - Why it could work
   - Why it may not fit

## Recommendation
- [Recommended approach]
- [Why it is preferred]

## Tradeoffs
- [Benefit vs cost]

## Decisions / Resolved Questions
- [Decision and rationale]

## Referenced Patterns
- [Pattern or file/reference]
- [Why it applies or why it does not]
```

## Quality Bar

- Keep the artifact focused on solution choice and rationale
- Every recommendation should trace back to research, constraints, or observed patterns
- Avoid implementation detail unless it is necessary to explain a tradeoff
- Any code snippets should stay at architectural illustration level, not implementation level
- Do not finalize the design doc while required design decisions remain unresolved
- Treat this document as compressed context for later phases rather than as an executable plan
- If the user wants execution shape next, hand off naturally to `structured-outline`

---
name: design-doc
description: Turn research into a proposed solution by evaluating alternatives, tradeoffs, decisions, and relevant patterns
---

# Design Doc

Use this skill to turn research into a high-level design recommendation.

Core question: what should we do, and why this approach over the alternatives?

Operating contract:
- A linked research doc is mandatory input for this skill.
- Research is the authoritative boundary for scope and problem framing.
- The resulting design doc must preserve an explicit link to the research artifact so later phases can follow the same grounding chain.
- Do not expand scope beyond research unless the user explicitly asks for more research.
- This skill produces design decisions, not execution instructions.
- This skill is artifact-first: when research and an actionable design prompt exist, write the best supported design doc, then ask for review.
- The actionable design prompt may come from either:
  - the user's stated outcome in chat
  - a linked Jira ticket or issue that clearly describes the requested change or decision
- If the user only supplies research and no actionable design question, and no linked Jira ticket or issue states the desired change clearly enough, ask for their idea before drafting anything.
- This skill must make tradeoffs explicit: do not present conclusions as settled without showing what was considered, what was rejected, and why.
- Use explicit assumptions and review questions instead of requiring a preliminary conversation when repository evidence supports a useful draft.

## Boundaries

This skill should include:
- Explicit input artifact links for downstream phases
- Problem framing derived from the supplied research
- Research-derived constraints that shape the design
- Constraints that materially affect the solution
- Candidate approaches
- A recommended approach
- Tradeoffs
- Resolved questions and decisions
- Relevant pattern references and why they apply or do not apply
- Small illustrative code snippets when they materially help explain a pattern fit, tradeoff, or recommendation

This skill should not include:
- Implementation task lists
- File-by-file edits
- Detailed sequencing
- Step-by-step execution instructions

Code snippets in this phase:
- Prefer short, focused code snippets when they materially help the reviewer understand a pattern fit, tradeoff, or architectural choice
- Keep snippets short and illustrative rather than implementation-ready
- Pair each snippet with a brief explanation of why it supports the recommendation or comparison
- Do not include enough code detail that the document becomes an execution plan

## Initial Response

When invoked:

1. If the user provided research docs, tickets, or file paths:
   - Read them fully before doing anything else
   - Treat that research as the source of truth for problem framing
   - Preserve the research artifact path for the final design doc
   - Do not rewrite or expand the research phase itself
   - Do not broaden scope beyond what the research established unless the user explicitly asks for more research
   - After reading, determine whether there is an actual design decision to make
   - If a linked Jira ticket or issue clearly states the requested change, desired outcome, or decision to be made, treat that ticket or issue as the actionable design prompt
   - If the research describes current state or background only, and neither the user nor a linked Jira ticket or issue has stated what should change, ask for their idea instead of drafting a design doc
   - Do not infer a proposed solution or fabricate a target decision merely because research was provided; use only what is explicit in the user's request or linked Jira ticket or issue
2. If no supporting context was provided, ask for:
   - The linked research document
   - Any constraints or non-goals
   - Any existing patterns or prior implementations that should be considered as supporting references
3. If the request does not include a linked research doc:
   - Stop and ask for the linked research doc before doing design work
   - Do not substitute ad hoc chat context, memory, or fresh discovery for the required research artifact
   - Do not draft, outline, or recommend solutions until that linked research doc is available

Required gating before drafting:
- You must have a linked research doc
- You must know what is being proposed, changed, or decided
  - This may come from the user's message or from a linked Jira ticket or issue
- If either required input is missing, ask only for the missing input
- Derive key tradeoffs from research, constraints, and bounded pattern evidence when possible
- Record uncertain priorities or assumptions in the document for review instead of blocking a useful draft

## Workflow

### 1. Establish the problem from research

- Preserve the research artifact path and any ticket or issue path that materially framed the work
- Summarize the problem the research actually supports
- Pull out constraints, non-goals, and assumptions
- Identify the decisions that still need to be made
- Keep the artifact at a high architectural level rather than drifting into implementation planning

### 2. Evaluate candidate approaches

- Identify the realistic solution options
- Compare them against the constraints from the research
- Call out where an option introduces complexity, risk, or future maintenance cost
- Explicitly state the tradeoffs between options, not just their standalone pros or cons
- If one option is preferred only under certain priorities, state the assumed priority, explain its effect, and flag it for review
- Do not collapse multiple plausible approaches into a single recommendation without first comparing them in plain language
- Present viable options and their comparison in the design document before converging on a recommendation

### 3. Use patterns correctly

Patterns are inputs to design evaluation in this phase.

- Reference existing code or documented patterns when they help assess an approach
- Explain why a pattern fits, partially fits, or does not fit
- When helpful, include a small snippet from an existing pattern so the reviewer can quickly see the shape being referenced instead of relying on links alone
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
- When a reasonable default exists, state the assumption and its effect on the recommendation
- Carry unresolved, non-blocking questions into `Assumptions / Questions for Review`
- Ask before writing only when missing information makes any recommendation speculative or would require inventing the target change
- Treat feedback after the first artifact as the default iteration point

### 5. Write, then request review

- Write the design doc once required inputs exist and a defensible recommendation can be made
- Include assumptions and focused review questions in the artifact
- After saving, summarize the recommendation and rejected alternatives, provide the path, and ask for feedback
- Apply subsequent feedback by updating the same artifact

## Output

Write the design document to:

- `thoughts/designs/YYYY-MM-DD-descriptive-name.md`
- Use today's date in `YYYY-MM-DD` format
- Use a short kebab-case descriptive name

Produce the design document with this shape:

```markdown
# Design Doc: [Topic]

## Input Artifacts
- Research: [path]
- Ticket/Issue: [path, if applicable]

## Problem Framing
- [What the research says we need to solve]

## Research-Derived Constraints
- [Constraint from research]

## Constraints
- [Additional design constraint]

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

## Assumptions / Questions for Review
- [Assumption made to produce the draft]
- [Focused question whose answer could change the recommendation]

## Referenced Patterns
- [Pattern or file/reference]
- [Why it applies or why it does not]
- [Optional short illustrative snippet and why it matters]
```

## Quality Bar

- Keep the artifact focused on solution choice and rationale
- Preserve the research grounding chain with an explicit `## Input Artifacts` section
- Every recommendation should trace back to research, constraints, or observed patterns
- Refuse to proceed if no linked research doc was provided
- Avoid implementation detail unless it is necessary to explain a tradeoff
- Use code snippets when they clarify pattern intent or tradeoff reasoning better than references alone
- Any code snippets should stay at architectural illustration level, not implementation level
- Do not invent a target change or decision merely to produce a document
- Do not finalize the design doc if neither the user nor a linked Jira ticket or issue has provided the idea, target change, or decision under discussion
- Cover tradeoffs explicitly in the artifact
- Present multiple viable options in the artifact before recommending one
- Recommendations must include at least one rejected alternative and the reason it was not chosen
- Treat this document as compressed context for later phases rather than as an executable plan
- If the user wants execution shape next, hand off naturally to `structured-outline`

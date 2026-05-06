---
name: design-doc
description: Turn research into a proposed solution by evaluating alternatives, tradeoffs, decisions, and relevant patterns
---

# Design Doc

Use this skill to turn research into a high-level design recommendation.

Core question: what should we do, and why this approach over the alternatives?

Operating contract:
 - Start this skill in `$caveman` mode automatically.
 - If `$caveman` is already active from earlier context, preserve it through this skill and across later skill handoffs.
 - Do not turn `$caveman` off unless the operator explicitly says `stop caveman` or `normal mode`.
 - If the operator asks for more detail, provide it in `$caveman` style unless they explicitly turn the mode off.
- A linked research doc is mandatory input for this skill.
- Research is the authoritative boundary for scope and problem framing.
- Do not expand scope beyond research unless the user explicitly asks for more research.
- This skill produces design decisions, not execution instructions.
- This skill is discussion-first: do not jump straight to writing a design doc unless there is a concrete idea, proposed change, or design decision to evaluate.
- The actionable design prompt may come from either:
  - the user's stated outcome in chat
  - a linked Jira ticket or issue that clearly describes the requested change or decision
- If the user only supplies research and no actionable design question, and no linked Jira ticket or issue states the desired change clearly enough, ask for their idea before drafting anything.
- This skill must make tradeoffs explicit: do not present conclusions as settled without showing what was considered, what was rejected, and why.
- This skill must not write the design doc until the user has explicitly approved moving from discussion into artifact creation.

## Boundaries

This skill should include:
- Problem framing derived from the supplied research
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

0. Enter or preserve `$caveman` mode immediately for the main skill response.
   - Carry `$caveman` forward across any later skill invocation unless the operator explicitly turns it off.

1. If the user provided research docs, tickets, or file paths:
   - Read them fully before doing anything else
   - Treat that research as the source of truth for problem framing
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
- You must know the key tradeoffs to evaluate, either from the user or from follow-up discussion
- If either is missing, ask concise questions and continue the design conversation before producing the artifact
- You must have explicitly discussed the most relevant tradeoffs in the conversation
- If you found multiple viable options, you must have presented those options to the user before drafting
- You must have explicit user approval to write the design document

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
- Explicitly state the tradeoffs between options, not just their standalone pros or cons
- If one option is preferred only under certain priorities, surface that dependency and ask the user to choose the priority when it is not already clear
- Do not collapse multiple plausible approaches into a single recommendation without first comparing them in plain language
- If you find more than one viable option, present the options to the user explicitly before converging on a recommendation
- Make the option review visible in the conversation, not just in the final document

### 3. Use patterns correctly

Patterns are inputs to design evaluation in this phase.

- Reference existing code or documented patterns when they help assess an approach
- Explain why a pattern fits, partially fits, or does not fit
- When helpful, include a small snippet from an existing pattern so the reviewer can quickly see the shape being referenced instead of relying on links alone
- Use pattern references to support tradeoff analysis, not to prescribe implementation steps
- Use codebase evidence only to evaluate approaches within the researched boundary, not to perform a new discovery or planning pass

### Subagent usage

- Read directly provided critical artifacts yourself before spawning any subagents
- CRITICAL: Every spawned subagent must have `$caveman` enabled in its initial prompt/context
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
- Treat the interaction as iterative by default: discuss tradeoffs with the user when the recommendation depends on product intent, priorities, or ambiguous constraints
- A research doc alone is not evidence that the user wants the design artifact immediately; if intent is missing, ask first
- If the recommendation depends on choosing between competing values like speed, simplicity, consistency, flexibility, or operational risk, explicitly discuss that tradeoff with the user before finalizing the decision

### 5. Get approval before writing

- After discussing options and tradeoffs, summarize the recommended direction and the rejected alternatives in the conversation
- Ask the user explicitly whether they want you to write the design doc now
- Do not create or update `thoughts/designs/...` until the user answers yes or otherwise gives clear approval
- If the user wants more discussion, continue iterating instead of writing

## Output

Only after explicit user approval:

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
- [Optional short illustrative snippet and why it matters]
```

## Quality Bar

- Keep the artifact focused on solution choice and rationale
- Every recommendation should trace back to research, constraints, or observed patterns
- Refuse to proceed if no linked research doc was provided
- Avoid implementation detail unless it is necessary to explain a tradeoff
- Use code snippets when they clarify pattern intent or tradeoff reasoning better than references alone
- Any code snippets should stay at architectural illustration level, not implementation level
- Do not finalize the design doc while required design decisions remain unresolved
- Do not finalize the design doc if neither the user nor a linked Jira ticket or issue has provided the idea, target change, or decision under discussion
- Do not finalize the design doc if tradeoffs were not explicitly covered
- Do not finalize the design doc if multiple viable options were found but not presented to the user
- Do not write the design doc without explicit user approval
- Recommendations must include at least one rejected alternative and the reason it was not chosen
- Treat this document as compressed context for later phases rather than as an executable plan
- If the user wants execution shape next, hand off naturally to `structured-outline`

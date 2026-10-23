---
name: design-doc
description: Discuss research-grounded design choices and tradeoffs, resolve open questions with the user, then document the proposed design
---

# Design Doc

Use this skill to turn research into a reviewable design for the proposed solution.

Core question: how should the proposed solution work, and why is this design appropriate?

Operating contract:
- A linked research doc is mandatory input for this skill.
- Research is the authoritative boundary for scope and problem framing.
- The resulting design doc must preserve an explicit link to the research artifact so later phases can follow the same grounding chain.
- Do not expand scope beyond research unless the user explicitly asks for more research.
- This skill produces design decisions and enough detail to review how the solution works. The implementation plan owns concrete edits and execution instructions.
- Treat backward compatibility as opt-in. Unless the user, research, or an accepted external constraint explicitly requires it, prefer a clean breaking change that replaces old interfaces, schemas, behaviors, and mechanisms instead of preserving parallel paths.
- Do not confuse breaking compatibility with ignoring correctness or required data safety. Preserve or convert existing data only when the accepted scope says it must survive the change.
- Discuss the proposed design, choices, and tradeoffs with the user before writing the document. Resolve open design questions first; the artifact records the resulting design rather than serving as the first discussion of it.
- The actionable design prompt may come from either:
  - the user's stated outcome in chat
  - a linked Jira ticket or issue that clearly describes the requested change or decision
- If the user only supplies research and no actionable design question, and no linked Jira ticket or issue states the desired change clearly enough, ask for their idea before drafting anything.
- Consider credible alternative approaches and present their tradeoffs alongside those of the proposed approach. Keep the proposed design central without manufacturing options to meet a quota or reopening an accepted direction.
- Use research and bounded pattern evidence to resolve factual questions. Bring remaining design choices and uncertain priorities to the user rather than silently choosing defaults and recording them as open questions in a draft.

## Boundaries

This skill should include:
- Explicit input artifact links for downstream phases
- Problem framing derived from the supplied research
- Research-derived constraints that shape the design
- Constraints that materially affect the solution
- The proposed design, including behavior, responsibilities, boundaries, and interactions
- Meaningful alternatives and the rationale for the chosen approach
- Tradeoffs
- Resolved questions and decisions
- Reference architecture where useful: relevant existing patterns and focused snippets showing how the feature fits them
- Relevant failure behavior, risks, and evidence that would validate the design

This skill should not include:
- Implementation task lists
- File-by-file edits
- Detailed sequencing
- Step-by-step execution instructions
- Complete implementations, exhaustive code scaffolding, or test code

Design detail describes what the system does, which responsibility owns it, and how the parts interact. Planning detail prescribes how to build it: exact edits, internal helpers, task order, commands, and test implementation. Include a contract or data shape when it materially affects design review; leave incidental names and implementation choices to the plan.

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

Required inputs before evaluating approaches:
- You must have a linked research doc
- You must know what is being proposed, changed, or decided
  - This may come from the user's message or from a linked Jira ticket or issue
- If either required input is missing, ask only for the missing input
- Derive key tradeoffs from research, constraints, and bounded pattern evidence when possible

Before writing the document:
- Present the proposed design, credible alternatives, and their tradeoffs to the user
- Resolve open design questions using evidence and user discussion
- Preserve decisions already settled in the conversation or accepted upstream artifacts; do not require redundant confirmation
- Do not write a draft with unresolved design questions or use assumptions to disguise decisions that still need the user's input

## Workflow

### 1. Establish the problem from research

- Preserve the research artifact path and any ticket or issue path that materially framed the work
- Summarize the problem the research actually supports
- Pull out constraints, non-goals, and assumptions
- Identify the decisions that still need to be made
- Establish the behavior and system boundaries the proposed design needs to explain, without choosing implementation tasks

### 2. Evaluate candidate approaches

- Evaluate credible alternatives at the decisions that materially affect the design. Present that comparison to the user before writing, then preserve it in the document; there is no required number of options
- Compare them against the constraints from the research
- Call out where an option introduces complexity, risk, or future maintenance cost
- Penalize compatibility layers, adapters, versioned paths, dual writes, and staged migrations unless compatibility is an explicit requirement
- Prefer direct replacement and deletion of superseded mechanisms when breaking changes are allowed
- Explicitly state the tradeoffs between options, not just their standalone pros or cons
- If one option is preferred only under certain priorities, explain that dependency and resolve uncertain priorities with the user before writing
- For each credible approach, including the proposed one, explain its benefits, costs, risks, and fit against the constraints. State why the proposed approach's tradeoffs are preferable and why alternatives were not chosen, at depth proportional to the decision rather than designing each in full
- If constraints leave one viable approach, explain why; do not invent rejected alternatives or pad every decision into a two- or three-option table
- If the user or upstream artifacts already selected an approach, preserve that decision and focus on its design. Discuss alternatives only where a material choice remains open

### 3. Develop the proposed design

Work out the proposed design for discussion before creating the artifact. It will be the substantive center of the document: a recommendation, feature list, or collection of pros and cons is not a sufficient design. Explain the following where they materially affect this feature; omit irrelevant concerns rather than adding empty sections:

- **Behavior and flows:** Walk through the key user or system journeys from entry to observable outcome. Include relevant alternate and failure paths, so reviewers can assess the actual experience rather than infer it from component names
- **Architecture and responsibilities:** Describe the participating components, what each owns, and how they interact. Distinguish existing mechanisms, changes to them, and justified new responsibilities. For cross-boundary features, include a compact diagram or responsibility table when it makes the design easier to review
- **Contracts and state:** Explain the information crossing important boundaries, state ownership, lifecycle, validation authority, and important invariants. Use a focused contract or data-shape example when prose leaves a material ambiguity; do not enumerate every field or helper by default
- **Failure and operational behavior:** Define relevant failure, recovery, concurrency, security, or external-effect semantics introduced by this design. Address compatibility and data conversion only when required by the accepted scope
- **Verification:** Describe the observable outcomes and important negative paths that would demonstrate the design works. Leave test cases, test code, and commands to downstream planning

Resolve material design choices here rather than assigning them to a future PR or the implementation plan. Leave incidental implementation choices open. If evidence cannot support a material decision, explain the gap and its consequence to the user and resolve it before writing the document.

### 4. Ground the design in reference architecture and patterns

Reference architecture makes the proposed design concrete through relevant codebase or documented patterns. It is not a file layout, edit list, or implementation recipe.

- Select patterns that explain how this feature should fit the system, such as an existing state-ownership boundary, request flow, integration contract, or composition style
- Reference concrete code or documentation and explain what the design reuses, adapts, or intentionally departs from, and why
- Include focused existing-code excerpts or illustrative snippets when they help reviewers assess the pattern and its application without opening every reference. A list of links alone is insufficient when the pattern's mechanics are central to the design
- Distinguish an observed existing pattern from a proposed adaptation. Show only the part needed to explain the design; do not write a complete implementation or prescribe exact edits
- A diagram can show component responsibilities or interactions; snippets can show the relevant pattern in code. Use either or both where helpful, without adding them to satisfy a format
- Tie each example to the feature's behavior or architectural choice. Do not add generic pattern catalogs or incidental boilerplate
- Use bounded codebase evidence to ground the proposed design within the researched scope, without starting a new discovery or planning pass

### Subagent usage

- Read directly provided critical artifacts yourself before spawning any subagents
- Use subagents to preserve main-context focus by delegating narrow, specific documentation tasks
- Use the [flow tracing and reuse guidance](../research-codebase/references/flows-and-reuse.md) for concrete existing patterns or precise code-path explanations within the researched boundary
- Give subagents a tightly scoped task such as "analyze this code path" or "find examples of this pattern and report back with file:line references"
- Ask subagents to report findings back with concrete file:line references and concise summaries
- Verify surprising or conflicting findings before using them in the design doc

### 5. Discuss choices and resolve open questions with the user

- Present the proposed behavior and architecture, the credible approaches considered, each approach's tradeoffs, and your recommendation with its rationale
- Include relevant reference patterns or focused snippets in the discussion when they help the user assess a choice; do not reserve all substantive design detail for the document
- Resolve factual questions from research and bounded pattern evidence. Ask the user about remaining design decisions, uncertain priorities, and assumptions that could affect the solution
- Make questions concrete: explain what needs deciding, the relevant tradeoffs, and your recommended answer where supported. Group related questions without manufacturing choices or a fixed option count
- Incorporate the user's answers and discuss any consequential new questions until no open design question remains. Wait for needed answers before writing; a recommendation or unanswered question is not a resolved decision
- Distinguish design decisions from incidental implementation choices intentionally left to the plan. Do not label a material contract or ownership decision an implementation detail merely to defer it
- Reuse decisions already made in the conversation or accepted upstream artifacts. If no open design questions remain, summarize the settled choices and tradeoffs before writing without adding a redundant approval step

### 6. Write the resolved design

- Write the design doc only after the choices and tradeoffs have been presented and open design questions have been resolved
- Record the resulting decisions, rationale, and established or agreed assumptions. Do not append an unresolved-design-questions section
- After saving, summarize the documented design, provide the path, and invite feedback on whether it accurately captures the discussion
- Apply subsequent feedback by updating the same artifact

## Output

Write the design document to:

- `thoughts/designs/YYYY-MM-DD-descriptive-name.md`
- Use today's date in `YYYY-MM-DD` format
- Use a short kebab-case descriptive name

Use this shape as a guide. Keep the input links explicit and the proposed design substantive; combine or omit other sections that do not help review this feature. Scale detail to the design's complexity rather than to a fixed length or option count.

```markdown
# Design Doc: [Topic]

## Input Artifacts
- Research: [path]
- Ticket/Issue: [path, if applicable]

## Problem Framing
- [What the research says we need to solve, desired outcomes, and non-goals]

## Constraints and Assumptions
- [Research-derived or explicitly accepted constraints and their sources]
- [Established or agreed assumptions that shape the proposal]

## Proposed Design
[Chosen approach and why it fits, summarized briefly]

### Behavior and Key Flows
[How the feature works end to end, including relevant alternate outcomes]

### Architecture and Responsibilities
[Participating components, ownership, interactions, and existing versus changed boundaries]
[Diagram or responsibility table where it helps]

### Contracts, State, and Failure Behavior
[Material contracts, state ownership, invariants, and relevant failure/recovery semantics]
[Focused examples where needed to make the design reviewable]

### Reference Architecture and Patterns
[Relevant existing pattern, concrete source reference, and how this feature follows or adapts it]
[Focused code excerpt or illustrative snippet where it clarifies the design]

## Alternatives and Tradeoffs
- [Credible approaches, including the proposed one: benefits, costs, risks, and constraint fit]
- [Why the proposed approach's tradeoffs are preferable and why alternatives were not chosen]
- [If the direction is settled or only one approach is viable, explain that without inventing options]

## Decisions / Resolved Questions
- [Decision and rationale]

## Risks and Validation
- [Material risk and observable evidence that would validate the proposed behavior]

## Implementation Choices Left to Planning
- [Optional: incidental implementation choices that do not alter the resolved design]
```

## Quality Bar

- A reviewer can understand and challenge how the proposed solution works without inventing its material behavior or architecture
- The selected design receives the depth; alternatives support the rationale without crowding it out
- Preserve the research grounding chain with an explicit `## Input Artifacts` section
- Every recommendation should trace back to research, constraints, or observed patterns
- Refuse to proceed if no linked research doc was provided
- Present design choices and each approach's tradeoffs to the user and resolve open design questions before writing the artifact
- Provide enough behavioral and architectural detail for design review while leaving concrete edits, internal code organization, sequencing, and test implementation to the plan
- Reference architecture and snippets explain relevant patterns and their application to this feature; they do not prescribe an implementation
- Do not invent a target change or decision merely to produce a document
- Do not finalize the design doc if neither the user nor a linked Jira ticket or issue has provided the idea, target change, or decision under discussion
- Cover tradeoffs explicitly in the artifact
- Present credible alternatives and the tradeoffs of each approach, including the proposed one, without imposing a count or reopening an accepted design direction
- Trace the key flows across relevant boundaries and keep behavior, responsibilities, contracts, and state semantics consistent
- The artifact records resolved design decisions; it does not defer open design questions to document review or implementation planning
- Do not preserve legacy interfaces, behavior, or implementation paths by default; require an explicit compatibility constraint to justify them
- Treat this document as the reviewable design that constrains later planning, rather than as an executable plan
- If the user wants execution shape next, hand off naturally to `structured-outline`

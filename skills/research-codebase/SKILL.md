---
name: research-codebase
description: Document codebase as-is and save point-in-time research in thoughts/research
---

# Research Codebase

Produce a point-in-time research document that explains how the codebase works today.

Research runs on Luna; the caller configures the model and reasoning effort. Produce concise evidence another engineer or planner can use without the conversation.

## Core Contract

- Your job is documentation, not design.
- Describe what exists today in code, config, docs, and directly referenced artifacts.
- Do not recommend changes unless the user explicitly asks for recommendations.
- Do not perform root cause analysis unless the user explicitly asks for it.
- Do not critique the implementation.
- The only permitted repository write is the research document under `thoughts/research/`. Do not change source, tests, configuration, dependencies, generated files, or git state.
- Implementation belongs to a subsequent phase. Record requested future implementation in the research anchor and finish the research artifact.
- Distinguish clearly between:
  - what the user, ticket, or issue claims
  - what you verified from repository evidence
  - what you could not confirm

## Deterministic Guard Rails

1. Read directly mentioned files before discovery or delegation.
2. Do lightweight local discovery yourself before spawning subagents.
3. Track inputs, flow coverage, supporting tests, unknowns, metadata, and document writing in a short checklist.
4. Never write the final document from memory alone. Base every section on collected evidence.
5. Every factual claim in `Summary`, `Detailed Findings`, and `Code References` must cite at least one file path, and line numbers when practical.
6. If evidence is missing, say `Could not confirm from available evidence.` Do not guess.
7. Keep the document schema fixed. Do not add or remove top-level sections except where explicitly allowed below.
8. Use focused subagents only when bounded parallel research materially improves coverage or context use.
9. When subagents are used, wait for all of them before synthesizing.
10. Distinguish code inspection, existing test assertions, and behavior actually observed at runtime. A test's existence does not establish that it passed.

## Default User-Facing Behavior

If the skill is invoked without a concrete research question, reply with exactly:

```text
Ready to research codebase. Send question, ticket, issue file, or area to inspect.
```

Then wait.

If the user already provided a question, start immediately.

## Required Workflow

Read anchor inputs first, then gather the evidence needed for the document.

### 1. Read Anchor Inputs First

- If the user mentioned specific files, read them fully before any delegation.
- If a Jira export, `issue.md`, spec, JSON file, or doc was provided, treat it as research framing input.
- Do not treat tickets or issues as ground truth.
- Extract:
  - the research question
  - any claimed behavior or desired outcome
  - key nouns, components, and file paths to investigate

### 2. Do Native Discovery

Before using subagents:

- If `graphify-out/graph.json` exists in the repository root, treat the graph as the preferred discovery surface for codebase orientation, architecture questions, file relationships, and likely evidence paths.
- When graph data is present, start by using graphify to narrow the search space, identify relevant components, and trace connections before falling back to broad filesystem searching.
- Use graphify for discovery, not as sole proof. Final claims in the research document still need citations to concrete repository files, and line numbers when practical.
- Find the relevant files, directories, symbols, and tests yourself.
- Build a short working map of likely evidence sources.
- Prefer current code and directly referenced docs over old research notes.
- Trace the relevant behavior from its entry point to its observable result. Inspect authorization, interfaces, state changes, persistence, and external effects only where the flow touches them.
- Inspect callers and consumers at each relevant boundary, plus the existing tests and material failure paths. Do not infer a whole flow from one implementation or test file.

Do not search prior research unless the user explicitly asked you to use it.

### 3. Check Coverage and Unknowns

- For each relevant boundary, record the files inspected, verified behavior, supporting test assertions, and any gap.
- Label evidence as code inspection, test assertion, or observed runtime result where the distinction affects the claim. Run a check only when authorized and compatible with the research write boundary; otherwise describe its assertions without claiming runtime confirmation.
- Put unresolved behavior and missing coverage in `Open Questions`, with the affected flow or requirement and why it may matter to planning. Do not choose a design to fill an evidence gap.

### 4. Delegate Focused Read-Only Research When Useful

Use parallel subagents only for bounded read-only tasks that materially improve coverage or preserve main-context focus after native discovery. Skip delegation when direct inspection is sufficient.

Preferred roles:

- `codebase-analyzer`: explain how a specific component works
- `codebase-pattern-finder`: find examples or usage sites of a known pattern
- `thoughts-locator` or `thoughts-analyzer`: only if the user explicitly referenced prior research
- `web-search-researcher`: only if the user explicitly asked for external research

Rules for delegation:

- Every subagent prompt must say the task is documentation-only.
- Every subagent prompt must forbid repository writes and implementation.
- Every subagent prompt must forbid recommendations and critiques.
- Ask each subagent for:
  - concrete findings
  - file paths
  - line numbers when available
  - unresolved questions
- Keep tasks narrow. Example: one subsystem, one flow, one pattern family.
- Do not delegate the same question twice.

Use this prompt shape, including the write and scope restrictions above:

```text
Document current implementation only. No recommendations, no critique.

Research target: [component / flow / question]
Focus: [what to verify]
Return:
- 3-7 concrete findings
- file paths for each finding
- line numbers when useful
- any unconfirmed gaps
```

### 5. Synthesize Only After All Research Completes

When all evidence is collected:

- prioritize live repository evidence
- separate claims from verified behavior
- collapse overlapping subagent findings
- remove speculation
- preserve only useful citations

Before writing, confirm you can answer:

- What was asked?
- What files prove the answer?
- What remains unconfirmed?

If any of those are unclear, do one more targeted pass before writing.

### 6. Gather Metadata

From the repository root:

- run `mono metadata`
- collect current date/time with timezone
- collect git commit hash
- collect branch name
- collect repository name
- collect researcher name from metadata output if available

If `mono metadata` is unavailable or fails, gather the commit and branch with `git rev-parse HEAD` and `git branch --show-current`, the repository name from the root directory, and the timestamp with timezone from the system clock. Use the caller identity if available; otherwise record `researcher: unknown` and explain the missing metadata. For detached HEAD or unavailable git metadata, record the actual condition instead of inventing values. Metadata-tool failure alone does not prevent saving the research.

Record relevant uncommitted changes as part of the evidence context; a commit hash alone does not identify a dirty working tree. `status: complete` means the investigation is finished, not that all questions are resolved or implementation is ready.

Filename rules:

- Write under `thoughts/research/`
- Use `YYYY-MM-DD-ENG-XXXX-description.md` when a ticket exists
- Use `YYYY-MM-DD-description.md` when no ticket exists
- `description` must be short kebab-case and topic-specific

Examples:

- `2025-01-08-ENG-1478-parent-child-tracking.md`
- `2025-01-08-authentication-flow.md`

### 7. Write the Research Document

Use this exact top-level structure and order. Do not invent new top-level headings except optional sections explicitly marked below.

```markdown
---
date: [ISO timestamp with timezone]
researcher: [name]
git_commit: [commit hash]
branch: [branch name]
repository: [repository name]
topic: "[user question or concise topic]"
tags: [research, codebase, component-a, component-b]
status: complete
last_updated: [YYYY-MM-DD]
last_updated_by: [name]
---

# Research: [topic]

## Research Question
[the user question in plain language]

## Research Anchor
[ticket, issue file, or input that framed the investigation]

## Summary
- 4-8 bullets
- each bullet must describe verified current behavior
- each bullet must include at least one citation

## Ticket or Issue Claims
[include only if a ticket or linked issue was provided]
- claim 1
- claim 2

## Detailed Findings

### Flow and Coverage
- [Relevant entry point, boundary sequence, and observable result, with citations]
- [Existing test assertions and material failure paths, with citations]
- [Evidence context: relevant uncommitted changes and limits of static/runtime evidence]

### [Area 1]
- what exists
- how it behaves
- where it connects
- citations

### [Area 2]
- what exists
- how it behaves
- where it connects
- citations

## Code References
- `path/to/file.ext:123` - what this evidence shows
- `another/file.ts:45` - what this evidence shows

## Architecture Notes
- current patterns or boundaries that are directly evidenced
- current conventions that are directly evidenced

## Referenced Prior Research
[include only if the user explicitly asked for prior research to be incorporated]
- `thoughts/research/example.md` - why it was relevant

## Open Questions
- [Unresolved item, affected flow or requirement, and potential consequence for planning]
- `Could not confirm from available evidence.` when applicable
```

Formatting rules:

- Use short bullets, not long paragraphs.
- Each `Detailed Findings` area should usually have 2-5 bullets.
- Describe current behavior and uncertainty. Keep design recommendations out unless explicitly requested.
- `Architecture Notes` must describe observed patterns only.
- `Open Questions` may be empty only if everything was fully confirmed. If empty, write `None.`
- Terse writing is good. Missing evidence is not.

### Evidence Rules

- Cite local file paths throughout the document.
- Add line numbers whenever practical.
- If GitHub permalinks are available, you may include them in addition to local references, but do not block on this.
- Never include a claim without supporting evidence.

### Writing Standard

The document must be useful to another engineer who has not read the conversation.

That means it must be:

- self-contained
- point-in-time
- explicit about evidence
- explicit about uncertainty

### Stop Conditions Before Saving

Do not save the document until all are true:

- the research question is stated clearly
- all summary bullets are evidence-backed
- ticket claims are separated from verified findings
- code references are concrete
- open questions are explicit rather than implied
- the relevant flow, supporting tests, and material failure paths are covered or explicitly marked unconfirmed
- metadata fields contain observed values or explicit unavailable/unknown conditions, not placeholders

### 8. Present Findings to the User

After saving the document:

- give a concise summary
- include the saved document path
- mention 2-4 high-value file references
- mention any key unresolved questions

### 9. Follow-Up Research

If the user asks a follow-up question on the same topic:

- append to the same document
- update `last_updated`
- update `last_updated_by`
- add `last_updated_note: "Added follow-up research for [brief description]"`
- append a new section:

```markdown
## Follow-up Research [ISO timestamp]
```

- repeat the same evidence discipline for the follow-up section

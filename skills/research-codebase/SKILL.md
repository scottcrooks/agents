---
name: research-codebase
title: Research Codebase
description: Document codebase as-is and save point-in-time research in thoughts/research
model: gpt-5.4-mini
---

# Research Codebase

Produce a point-in-time research document that explains how the codebase works today.

This skill must work reliably with `gpt-5.4-mini` at medium reasoning. Favor deterministic execution over cleverness.

## Caveman Mode

- Canonical style rule: Activate `$caveman` once at skill start (or preserve it if already active) and keep it active for the entire skill run, including user-facing updates, intermediate summaries, subagent prompts, and follow-up answers.
- Emit the literal `$caveman` token at most once per agent session. After activation, maintain the style implicitly.
- Do not turn `$caveman` off unless the operator explicitly says `stop caveman` or `normal mode`.
- Do not repeatedly re-issue or prepend the literal `$caveman` token before later messages, checklists, summaries, or prompt templates.
- Do not let `$caveman` weaken evidence quality or document completeness.
- Keep saved research documents concise, but not fragmentary. The document must remain readable to another engineer.

## Core Contract

- Your job is documentation, not design.
- Describe what exists today in code, config, docs, and directly referenced artifacts.
- Do not recommend changes unless the user explicitly asks for recommendations.
- Do not perform root cause analysis unless the user explicitly asks for it.
- Do not critique the implementation.
- Distinguish clearly between:
  - what the user, ticket, or issue claims
  - what you verified from repository evidence
  - what you could not confirm

## Mini-Model Guard Rails

These rules are mandatory. They exist to keep output consistent under a smaller model.

1. Read directly mentioned files before doing anything else.
2. Do lightweight local discovery yourself before spawning subagents.
3. Use a checklist and complete steps in order.
4. Never write the final document from memory alone. Base every section on collected evidence.
5. Every factual claim in `Summary`, `Detailed Findings`, and `Code References` must cite at least one file path, and line numbers when practical.
6. If evidence is missing, say `Could not confirm from available evidence.` Do not guess.
7. Keep the document schema fixed. Do not add or remove top-level sections except where explicitly allowed below.
8. Prefer 2-5 focused subagents over many vague ones.
9. Wait for all subagents before synthesizing.
10. Keep synthesis concrete. Avoid generic architecture prose that is not grounded in files.

## Default User-Facing Behavior

If the skill is invoked without a concrete research question, reply with exactly:

```text
Ready to research codebase. Send question, ticket, issue file, or area to inspect.
```

Then wait.

If the user already provided a question, start immediately.

## Required Workflow

Follow these steps in order.

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

- Find the relevant files, directories, symbols, and tests yourself.
- Build a short working map of likely evidence sources.
- Prefer current code and directly referenced docs over old research notes.

Do not search prior research unless the user explicitly asked you to use it.

### 3. Make a Small Research Checklist

Create a checklist for yourself covering:

- anchor inputs read
- primary code paths to inspect
- supporting docs/config to inspect
- subagent tasks to delegate
- metadata gathering
- document writing

Keep the checklist short and execution-oriented.

### 4. Delegate Focused Read-Only Research

Use parallel subagents for bounded read-only tasks after native discovery.

Preferred roles:

- `codebase-analyzer`: explain how a specific component works
- `codebase-pattern-finder`: find examples or usage sites of a known pattern
- `thoughts-locator` or `thoughts-analyzer`: only if the user explicitly referenced prior research
- `web-search-researcher`: only if the user explicitly asked for external research

Rules for delegation:

- Every subagent prompt must say the task is documentation-only.
- Every subagent prompt must forbid recommendations and critiques.
- Activate caveman for the subagent once if needed, then maintain it implicitly.
- Ask each subagent for:
  - concrete findings
  - file paths
  - line numbers when available
  - unresolved questions
- Keep tasks narrow. Example: one subsystem, one flow, one pattern family.
- Do not delegate the same question twice.

Use this prompt shape:

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
- unresolved item
- `Could not confirm from available evidence.` when applicable
```

Formatting rules:

- Use short bullets, not long paragraphs.
- Each `Detailed Findings` area should usually have 2-5 bullets.
- Do not include recommendation language such as `should`, `could`, `better`, `improve`, or `fix` unless quoting user input.
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
- metadata fields are filled with real values, not placeholders

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

## Important Notes

- Always do fresh codebase research.
- Prior research is supplemental only when explicitly requested.
- Keep the main agent focused on synthesis and coordination.
- Use subagents for narrow deep dives, not for the whole task.
- Document what is true now, not what might be true.
- If a requested area cannot be verified, say so plainly.

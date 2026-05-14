---
name: interrogate-research
title: Interrogate Research
description: "Use an existing thoughts/research document as the primary anchor for a focused series of codebase questions. Use when the goal is analysis only: start from prior research, stay scoped to the researched area, re-verify only what is needed, and do not implement changes."
model: gpt-5.4-mini
---

# Interrogate Research

Use an existing research artifact as the entrypoint for follow-up questions about a codebase.

This skill is for analysis only. It exists to avoid re-exploring unrelated parts of the repository when grounded research already exists, even if that research was produced in another context window or another workflow.

## Caveman Mode

- Canonical style rule: Activate `$caveman` once at skill start (or preserve it if already active) and keep it active for the entire skill run, including user-facing updates, intermediate summaries, subagent prompts, and follow-up answers.
- Emit the literal `$caveman` token at most once per agent session. After activation, maintain the style implicitly.
- Do not turn `$caveman` off unless the operator explicitly says `stop caveman` or `normal mode`.
- Do not repeatedly re-issue or prepend the literal `$caveman` token before later messages, checklists, summaries, or prompt templates.
- Do not let `$caveman` reduce evidence quality or scope discipline.

## Core Contract

- Start from one or more existing research artifacts.
- Prefer `thoughts/research/` when available, but also accept pasted research, notes, issue writeups, or other grounded analysis artifacts.
- Treat the research document as the primary anchor, not as unquestionable truth.
- Answer the user's questions with the minimum additional code exploration needed.
- Stay inside the researched surface area unless evidence forces expansion.
- Do not implement changes.
- Do not recommend changes unless the user explicitly asks for recommendations.
- Distinguish clearly between:
  - what the research document claims
  - what you freshly verified from repository evidence
  - what remains unconfirmed

## Default User-Facing Behavior

If no research artifact or topic is provided, reply with exactly:

```text
Ready to interrogate research. Send a research document or notes and your questions.
```

Then wait.

If the user provides a topic but not a research artifact, first locate likely matching research documents and ask the user to pick one if multiple strong candidates exist.

## Required Workflow

Follow these steps in order.

### 1. Read the Research Anchor First

- Read the provided research artifact fully before doing any new discovery.
- Extract:
  - the original research question
  - the components, files, and flows already identified
  - explicit citations that narrow where to look next
  - any stated gaps or uncertainty

### 2. Build a Tight Question Map

For the current user questions, decide:

- which questions are already answered directly by the research
- which questions need fresh verification
- which questions would require expanding beyond the researched area

Prefer a short internal checklist over broad exploration.

### 3. Re-Verify Minimally

- Re-open only the files needed to answer the questions.
- Prefer files already cited in the research artifact.
- Expand outward only when the cited evidence is stale, incomplete, or ambiguous.
- If the answer would require broad rediscovery, stop and say that the current research anchor is insufficient.

### 4. Keep the Scope Honest

- Do not drift into unrelated architecture review.
- Do not repeat a full research pass.
- Do not infer behavior from the research document alone when the code can be checked quickly.
- If repository behavior conflicts with the research artifact, say so explicitly and trust live evidence over the prior write-up.

### 5. Answer in Grounded Q&A Form

For each user question:

- give the direct answer first
- cite the research artifact when relevant
- cite fresh code evidence when used
- note any uncertainty or missing proof

If several questions share the same evidence, reuse the same citations instead of re-explaining the whole subsystem.

## Delegation

Use subagents only when a question needs targeted read-only verification that can be kept narrow.

If you delegate:

- activate caveman for the subagent once if needed, then maintain it implicitly
- say the task is analysis only
- forbid implementation and recommendations
- pass the research artifact path or excerpt and the exact question subset
- ask for concrete findings with file citations

Good delegation targets:

- one component named in the research artifact
- one flow mentioned but not fully proven
- one pattern or usage family referenced by the research artifact

Do not delegate the entire interrogation task.

## Output Rules

- Be concise.
- Keep caveman style active for the full response.
- Stay anchored to the user's questions.
- Prefer bullets grouped by question.
- Call out drift explicitly:
  - `Answered from research anchor`
  - `Re-verified from live code`
  - `Could not confirm from available evidence`

## When To Stop And Recommend A New Research Pass

Say a fresh `research_codebase` run is the better tool when:

- the existing research artifact is outdated relative to current code
- the new questions span multiple areas not covered by the research
- the cited files no longer represent the current behavior
- answering well would require broad discovery again

In that case, do not implement anything. Ask for a new research pass scoped to the missing area, or ask the user for a better grounding artifact.

---
name: implement-plan
title: V2 Implement Plan
description: Execute an existing implementation plan slice-by-slice with validation and human checkpoints where required
model: gpt-5.3-codex
---

# V2 Implement Plan

Use this skill when the user already has an implementation plan and wants the agent to carry it out carefully.

This skill should answer: how do we execute the approved plan safely, in order, and with the right validation between increments?

Operating contract:
- Canonical style rule: Always enable and use `$caveman` mode for this skill run, even if it was not active before invocation. Apply it before any analysis, reads, planning, execution, or tool calls, and keep it for every user-facing message (initial response, progress, validation, blockers, manual checkpoints, final handoff) and any spawned subagent prompts. Never leave `$caveman` mode during this skill.
- Emit the literal `$caveman` token at most once per agent session. After activation, maintain the style implicitly.
- Do not repeatedly re-issue or prepend the literal `$caveman` token before later messages, checklists, summaries, or prompt templates.
- Canonical manual-checkpoint rule: When the implementation plan defines a manual verification checkpoint, treat it as a hard gate. Stop and wait for explicit user confirmation in the conversation before any further coding, validation, or slice advancement.
- The implementation plan is the required primary input artifact for this phase.
- Treat the implementation plan as the source of truth for execution shape, sequencing, and validation expectations.
- Do not reopen design exploration or rewrite the plan unless the codebase contradicts it or the user asks to change it.
- Prefer vertical slices and execute one slice at a time.
- Run automated validation at the slice boundaries described by the plan. Plan checks must include applicable repository-standard checks.
- Pause for human verification only when human input is required (for example: plan-defined manual checkpoints, ambiguity needing user decision, or contradiction/scope decision requiring confirmation).
- Do not broaden scope beyond what the implementation plan, structured outline, design doc, and research boundary establish.

The output of this skill is executed work in the repository, not a new planning artifact. The agent should keep the user informed, execute the plan incrementally, and stop at the right checkpoints.

## Boundaries

This skill should include:
- Executing implementation steps from the approved plan
- Reading upstream artifacts only as needed to recover context required for safe execution
- Plan-defined automated checks including applicable repo-standard checks
- Manual verification pauses only when human input is required
- Mandatory stop-and-wait behavior per the Canonical manual-checkpoint rule
- Progress updates tied to slice completion and validation status

This skill should not include:
- Re-planning the work from scratch
- Reopening design tradeoff discussions unless the codebase or user feedback makes the plan invalid
- Expanding scope beyond the approved plan
- Skipping validation to save time
- Treating manual validation checkpoints as optional, implicit, or auto-approved (see Canonical manual-checkpoint rule)

Code snippets in this phase:
- Avoid long code samples in chat
- Show a short snippet only when it helps explain a blocker, a contradiction in the plan, or a proposed adjustment
- Prefer making the change in the repository over describing it abstractly

## Initial Response

When invoked:

0. Enter or preserve `$caveman` mode immediately for the main skill response.
   - This is required by the Canonical style rule in Operating contract.
   - This happens before all other numbered steps in this section.

1. If the user provided an implementation plan:
   - Read the implementation plan fully
   - Read the structured outline, design doc, or research only if the plan references them or if more context is needed to execute safely
   - Summarize the execution strategy briefly, including the slice order and validation model
   - Determine the current slice state (for resumed runs, validate which slice is currently active/incomplete before proceeding)
   - Begin execution from the earliest incomplete slice unless the plan requires a user checkpoint before coding
2. If no implementation plan was provided, ask for:
   - The implementation plan path
   - Any current execution status, such as partially completed slices or known blockers

Required gating before executing a slice:
- You must understand the slice objective, the relevant files or components, and the validation expected before moving on
- If the plan is ambiguous in a way that materially affects execution, stop and ask the user instead of guessing
- If the codebase materially contradicts the plan, stop and explain the contradiction before proceeding

## Workflow

### 1. Read and lock context

- Read the implementation plan fully before making changes
- Identify the current slice, its dependencies, and its validation requirements
- Pull forward only the context needed to execute the current slice safely
- If prior slices appear already complete in the repo, verify that before skipping ahead (this is required to determine current slice on resumed runs)

### 2. Execute one slice at a time

- Start with the earliest incomplete slice
- Implement the concrete steps for that slice
- Follow existing codebase patterns wherever the plan expects consistency
- Keep the work scoped to the current slice unless a tightly related prerequisite is unavoidable
- Avoid jumping ahead to later slices before the current slice is validated

### 3. Validate before advancing

- Run the automated checks called for by the plan, including applicable repo-standard checks
- Report validation results clearly after each slice
- If automated validation fails, fix the issue or explain the blocker before moving on
- If the plan includes a manual verification checkpoint, apply the Canonical manual-checkpoint rule
- If additional manual verification seems useful but is not required by the plan, report it as an optional recommendation and continue without pausing

### 4. Handle contradictions and ambiguity

- If the implementation plan and codebase disagree, do not silently choose one
- Explain the contradiction with concrete file references
- Propose the smallest plan adjustment needed to proceed
- Wait for user confirmation when the adjustment changes scope, sequencing, or validation expectations

### 5. Communicate progress

- Tell the user which slice is in progress
- Tell the user when a slice is complete and what validation passed
- Make it explicit when you are pausing for manual verification or user input
- Keep updates concise and tied to execution state, not generic narration
- Keep every progress update in `$caveman` style (see Canonical style rule)

## Subagent usage

- Read the implementation plan yourself before spawning any subagents
- CRITICAL: Activate caveman for a spawned subagent once if needed, then maintain it implicitly
- Use subagents only for narrow execution-support tasks such as finding an existing pattern, understanding a specific interface, or investigating a blocker
- Prefer `codebase-pattern-finder` for concrete examples to follow during implementation
- Prefer `codebase-analyzer` for precise explanations of current code behavior or integration points
- Ask subagents for concise findings with file:line references and only the context needed for the current slice

## Quality Bar

- Work should follow the implementation plan's slice order unless there is a verified reason not to
- Each slice should end with explicit validation status
- Automated checks should come from the plan or the repository's real tooling, not generic guesses when better evidence exists
- Plan validation should include applicable repo-standard checks, not only ad hoc or partial checks
- Manual verification pauses should occur only when human input is required
- Manual checkpoints must follow the Canonical manual-checkpoint rule
- The user should always know whether the agent is implementing, validating, blocked, or waiting on them
- If the plan is wrong or incomplete, stop and resolve that explicitly instead of improvising a new plan silently
- User-facing style must stay in `$caveman` for the whole skill run (see Canonical style rule)

---
name: v2_implement_plan
title: V2 Implement Plan
description: Execute an existing implementation plan slice-by-slice with validation and human checkpoints where required
model: gpt-5.3-codex
---

# V2 Implement Plan

Use this skill when the user already has an implementation plan and wants the agent to carry it out carefully.

This skill should answer: how do we execute the approved plan safely, in order, and with the right validation between increments?

Operating contract:
- Start this skill in `$caveman` mode automatically.
- If `$caveman` is already active from earlier context, preserve it through this skill and across later skill handoffs.
- Do not turn `$caveman` off unless the operator explicitly says `stop caveman` or `normal mode`.
- If the operator asks for more detail, provide it in `$caveman` style unless they explicitly turn the mode off.
- Keep `$caveman` active for every user-facing message in this skill:
  - initial summary
  - progress updates
  - validation results
  - blocker reports
  - manual-checkpoint pauses
  - final handoff
- Do not let message length, long-running execution, repeated rounds, or context switching cause style drift out of `$caveman`.
- The implementation plan is the required primary input artifact for this phase.
- Treat the implementation plan as the source of truth for execution shape, sequencing, and validation expectations.
- Do not reopen design exploration or rewrite the plan unless the codebase contradicts it or the user asks to change it.
- Prefer vertical slices and execute one slice at a time.
- Run automated validation at the slice boundaries described by the plan.
- Pause for human verification when the plan calls for manual checkpoints or when user-visible behavior cannot be validated confidently by automation alone.
- Do not broaden scope beyond what the implementation plan, structured outline, design doc, and research boundary establish.

The output of this skill is executed work in the repository, not a new planning artifact. The agent should keep the user informed, execute the plan incrementally, and stop at the right checkpoints.

## Boundaries

This skill should include:
- Executing implementation steps from the approved plan
- Reading upstream artifacts only as needed to recover context required for safe execution
- Repo-derived automated checks
- Manual verification pauses when appropriate
- Progress updates tied to slice completion and validation status

This skill should not include:
- Re-planning the work from scratch
- Reopening design tradeoff discussions unless the codebase or user feedback makes the plan invalid
- Expanding scope beyond the approved plan
- Skipping validation to save time

Code snippets in this phase:
- Avoid long code samples in chat
- Show a short snippet only when it helps explain a blocker, a contradiction in the plan, or a proposed adjustment
- Prefer making the change in the repository over describing it abstractly

## Initial Response

When invoked:

0. Enter or preserve `$caveman` mode immediately for the main skill response.
   - Carry `$caveman` forward across any later skill invocation unless the operator explicitly turns it off.

1. If the user provided an implementation plan:
   - Read the implementation plan fully
   - Read the structured outline, design doc, or research only if the plan references them or if more context is needed to execute safely
   - Summarize the execution strategy briefly, including the slice order and validation model
   - Begin execution from the first slice unless the plan requires a user checkpoint before coding
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
- If prior slices appear already complete in the repo, verify that before skipping ahead

### 2. Execute one slice at a time

- Start with the earliest incomplete slice
- Implement the concrete steps for that slice
- Follow existing codebase patterns wherever the plan expects consistency
- Keep the work scoped to the current slice unless a tightly related prerequisite is unavoidable
- Avoid jumping ahead to later slices before the current slice is validated

### 3. Validate before advancing

- Run the automated checks called for by the plan and any closely related repo-standard checks needed to catch obvious regressions
- Report validation results clearly after each slice
- If automated validation fails, fix the issue or explain the blocker before moving on
- If the plan includes a manual verification checkpoint, stop after automated checks pass and ask the user to verify before continuing
- If manual verification is appropriate even though the plan did not spell it out, explain why and ask before advancing

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
- Keep every progress update in `$caveman` style unless the Auto-Clarity Exception applies or the operator explicitly turns the mode off

## Subagent usage

- Read the implementation plan yourself before spawning any subagents
- CRITICAL: Every spawned subagent must have `$caveman` enabled in its initial prompt/context
- Use subagents only for narrow execution-support tasks such as finding an existing pattern, understanding a specific interface, or investigating a blocker
- Prefer `codebase-pattern-finder` for concrete examples to follow during implementation
- Prefer `codebase-analyzer` for precise explanations of current code behavior or integration points
- Ask subagents for concise findings with file:line references and only the context needed for the current slice

## Quality Bar

- Work should follow the implementation plan's slice order unless there is a verified reason not to
- Each slice should end with explicit validation status
- Automated checks should come from the plan or the repository's real tooling, not generic guesses when better evidence exists
- Manual verification pauses should be respected rather than skipped
- The user should always know whether the agent is implementing, validating, blocked, or waiting on them
- If the plan is wrong or incomplete, stop and resolve that explicitly instead of improvising a new plan silently
- User-facing style must stay in `$caveman` for whole skill run unless the Auto-Clarity Exception applies or the operator explicitly turns it off

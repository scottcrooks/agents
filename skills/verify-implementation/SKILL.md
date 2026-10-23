---
name: verify-implementation
description: Verify an implemented change set for plan conformance and general correctness, repair clear gaps and regressions directly, and report evidence and unresolved decisions. Use after implementation or simplification to check promised outcomes and defects introduced or exposed by the changes.
---

# Verify Implementation

Own bringing the implementation into agreement with the approved plan and reviewing the full change set for correctness. Establish what the plan promises, trace those promises through the actual implementation, and look for defects introduced or exposed by the changes even when they are unrelated to plan requirements. Repair concrete gaps and defects, then verify the result. Authorship and which stage introduced a gap do not determine whether it should be repaired.

## Execution profile

Designed for GPT-6 Luna with high reasoning effort. The caller selects `gpt-6-luna` and `high`; skill instructions do not change the runtime model. Keep execution in the current agent without automatic delegation or model escalation.

Use the requirement-to-evidence map below as the work queue, alongside any correctness defects found in the change set. For each requirement or defect, trace the implementation, establish any gap, repair it when the correction is clear, and record the relevant check. Keep separate coverage of the full change set so a requirement-focused review does not skip changed files or regressions. Continue independent work when one item needs an external decision. Keep this working state compact; no separate status document is required.

## Establish the requirements

Read the supplied plan fully, including acceptance criteria, constraints, exclusions, and required validation. Use linked design decisions and other artifacts only as needed to interpret binding requirements. A status ledger or checked box is a claim to verify, not evidence of completion.

If no plan is supplied, use one unambiguously identified by the current task or PR. If none is identifiable, ask for its location while continuing independent repository inspection, base resolution, and correctness review. Repair clear defects that do not depend on the missing plan. Do not invent requirements or make plan-dependent repairs without the plan.

Treat required outcomes and explicit accepted decisions as binding. File lists, example code, and implementation recipes are guidance unless explicitly required. An equivalent implementation can satisfy the plan after refactoring; do not restore an obsolete implementation shape merely because it appeared in the plan. Respect explicit caller-approved changes that supersede the plan and identify them in the report.

Build a compact requirement-to-evidence map. Include material obligations in the plan's body as well as its acceptance checklist. For each, identify the expected observable outcome, relevant implementation path, available verification, and status: verified, unmet, or unverified. An unmet requirement has concrete evidence of missing or incorrect behavior; an unverified requirement lacks sufficient evidence. Record a blocker separately when a decision or unavailable prerequisite prevents progress. Keep this map in the working review or final report unless the caller requests an artifact.

## Establish the implementation scope

Read repository instructions and inspect the initial working tree. Preserve unrelated and concurrent user changes. Invoking this skill authorizes local repairs; publication and external actions require separate authorization.

Resolve the comparison base from an explicit caller selection, the PR's actual base, an established stack parent, or the repository default, in that order. A feature branch's remote upstream is not necessarily its PR base. Pin the merge base with `HEAD` for a branch comparison; use an exact commit directly when requested. Resolve material ambiguity before dependent edits and disclose stale local references.

Inspect the full current change against that base, including committed, staged, unstaged, and untracked non-ignored files. Account for every changed hunk and relevant caller or contract; split truncated reads. Use the requirements map to search for missing implementation even when no corresponding file or hunk exists. Existing unchanged behavior can satisfy a requirement and need not be reimplemented.

## Trace the promised behavior

For each requirement, follow the relevant path from entry point to observable result. Include UI states, frontend behavior, client/server contracts, domain logic, persistence, and external effects only where the promised outcome touches them. Check that the parts connect: individually correct functions do not establish a working user flow.

Check happy paths and relevant negative paths, including permissions, input validation, failure behavior, recovery, and lifecycle transitions where required by the plan or necessary for its promised behavior. Trace beyond the first failure so an early defect does not hide another missing obligation. Do not turn every conceivable edge case into a new requirement.

Look for missing behavior, incorrect results, unwired paths, contradictory cross-layer assumptions, explicit non-goal violations, and broken established contracts in the affected flows. A plan conformance finding must identify the applicable requirement or constraint, concrete repository evidence, and user-visible or contractual consequence. Missing tests alone are not a behavioral defect, though explicitly required test deliverables remain obligations.

Do not infer conformance from a plan checklist, matching filenames, a passing unrelated suite, or tests that merely reproduce the implementation's assumptions. Verify that assertions demonstrate the promised result and relevant failure behavior.

## Review change set correctness

Review every changed hunk and its interactions for concrete defects introduced or exposed by the changes, including regressions in behavior outside the plan's promised flows. Trace affected callers, shared state, and established contracts as needed to assess the consequences. Plan conformance does not establish correctness, and a defect does not need to violate an explicit acceptance criterion to belong in this pass.

For each defect, establish the triggering conditions, concrete repository evidence, how the change causes or exposes it, and the observable consequence. Prioritize by severity and impact; a serious introduced bug must prevent completion even when every plan requirement is satisfied. Keep correctness findings with their repair and verification status alongside the requirements map without inventing new plan requirements.

Keep the review bounded to the change set and its effects. Pre-existing defects that the change neither worsens nor exposes, style preferences, speculative hardening, and optional refactoring remain outside this pass.

## Repair clear gaps

Fix established plan gaps and change set correctness defects directly with the smallest sufficient correction. Include missing implementation and necessary changes outside the original diff when they are required to deliver the approved outcome or correct a defect caused or exposed by the change. Use existing patterns and mechanisms. Do not hand an actionable repair back to an earlier stage merely because it was found here.

Keep optional simplification, speculative hardening, unrelated pre-existing defects, and architectural redesign outside this pass. Add compatibility paths or other machinery only when needed for a binding requirement or an established correctness defect. Avoid reverting valid simplifications when their behavior satisfies the plan and preserves correctness.

If the plan is materially ambiguous, contradictory, or conflicts with an established contract or explicit architectural decision, identify the exact decision needed rather than silently choosing a new product behavior or following an unsafe instruction. Continue independent verification and repairs. Stop repeating blocked attempts when new information or authorization is required.

Do not rewrite acceptance criteria, weaken checks, or mark implementation slices complete to make the result appear conformant. If a designated verification section exists, record actual evidence there without changing upstream requirements or implementation history.

## Verify and conclude

Run the plan's applicable required checks and repository-required validation. Use focused behavioral checks that demonstrate each affected requirement and correctness repair; reuse existing tests where sufficient and add or update lasting coverage only when a meaningful risk is otherwise unprotected or the plan explicitly requires it. Temporary checks can establish behavior without becoming committed tests. Avoid tests that merely mirror implementation details. Record actual commands, working directories, and outcomes. Distinguish code inspection from executed behavioral evidence.

After repairs, review the resulting change against the same pinned base, including newly touched files and their interactions. Reconcile the complete requirement map and correctness findings, check for regressions caused by the repairs, and rerun affected validation. Continue until all obligations and correctness defects are resolved and verified or remaining items have precise unresolved evidence or blockers. A confirmed gap or defect is not a reason to stop reviewing other requirements or changes.

Report completion only when the implementation scope and requirements are fully covered, no material plan gap or correctness defect remains, and required validation has passed. Otherwise report the result as incomplete, distinguishing confirmed gaps and defects, missing verification, unrelated check failures, and external decisions. Describe coverage as plan verification and change set correctness review; do not claim a comprehensive codebase or security audit.

Return a concise human-readable report, or the caller's compatible format, containing:

- The plan and any caller-approved superseding requirements, selected base, and pinned comparison SHA.
- A compact requirement-to-evidence summary showing what was verified and what remains unmet or unverified. Group related requirements when this preserves traceability.
- Change set correctness findings, their severity and consequences, and repair or verification status, including any that are independent of plan requirements.
- Repairs made, with the behavior restored and relevant locations.
- Validation commands and outcomes, plus any unresolved gap or exact decision needed.

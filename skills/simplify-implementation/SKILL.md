---
name: simplify-implementation
description: Refactor an implemented change set for simplicity, reuse existing mechanisms, remove unnecessary defensive code and abstractions, and reduce PR scope while preserving required behavior. Use for a simplification pass after implementation or when asked to simplify an existing PR. Checking implementation against a plan is a separate task.
---

# Simplify Implementation

Own the next version of the implementation. Challenge the need for its complexity, make justified simplifications directly, and verify the result. The output is a simpler implementation, not a critique handed back to its author. Authorship and which stage introduced a problem do not determine whether it can be improved.

Do not locate, read, or validate an implementation plan. Plan conformance belongs to a separate stage. Establish required behavior from the caller's stated constraints, existing contracts, callers, tests, and relevant product or API documentation. The incoming implementation is evidence of current behavior, not proof that every mechanism is necessary.

## Execution profile

Designed for GPT-6 Luna with high reasoning effort. The caller selects `gpt-6-luna` and `high`; skill instructions do not change the runtime model. Keep execution in the current agent without automatic delegation or model escalation.

Keep a compact working checklist: pinned base and full change inventory; files and hunks inspected; simplifications applied, retained with a reason, or awaiting a decision; and validation results. Work through coherent areas, applying and checking small changes before continuing. Keep the checklist internal unless the caller requests an artifact. Uncertainty about one candidate does not stop independent simplifications.

## Establish the change set

Read repository instructions and inspect the initial working tree. Identify the requested implementation and preserve unrelated or concurrent user changes. Invoking this skill authorizes local refactoring; publishing changes requires separate authorization.

Resolve the comparison base from an explicit caller selection, the PR's actual base, an established stack parent, or the repository default, in that order. Do not confuse a feature branch's remote upstream with its PR base. For a branch comparison, pin its merge base with `HEAD`; use an exact commit directly when explicitly requested. If the base is materially ambiguous, resolve it before making dependent edits. Disclose reliance on stale local references.

Review the full current change against that pinned base, including committed, staged, unstaged, and untracked non-ignored files. A diff against `HEAD` alone misses implementation already committed on the branch. Record the starting diff summary so the final report can compare the incoming and simplified implementation against the same base. Account for untracked files separately when Git diff summaries omit them.

Inspect every changed hunk and relevant callers and contracts. Split truncated output into smaller reads. For a large change, work through coherent areas and then trace their interactions. Read unchanged code to find reuse opportunities and understand behavior; keep edits outside the change set limited to what a concrete simplification requires. Workflow artifacts are not refactoring targets.

## Challenge complexity

Ask what would disappear if each mechanism were removed, and what real requirement or failure would then go unmet. Look for:

- **Unnecessary abstraction:** pass-through wrappers, one-use general frameworks, speculative extension points, excessive configuration, indirection, and fragmented functions that make one operation harder to follow. Inline or consolidate when that actually removes complexity. Retain abstractions that hide meaningful complexity or centralize a real invariant.
- **Existing solutions:** search the repository and capabilities of dependencies already in use before maintaining a parallel helper, component, validation mechanism, cache, or state machine. Confirm matching semantics, lifecycle, and failure behavior before reuse. Avoid adding a dependency merely to shorten a small piece of code.
- **Excessive defensive behavior:** repeated validation inside a trusted flow, impossible-state branches, silent fallbacks, redundant retries, broad catches, and compatibility paths without an established consumer or constraint. Trace the trust boundary and reachable states before removing checks. Retain protections for real external input, authorization, data integrity, concurrency, and established operational requirements.
- **Duplicated knowledge:** stored values that can be derived, synchronized copies of state, repeated decisions, and competing execution paths. Prefer one authoritative representation. Some local duplication is simpler than a shared abstraction with incompatible callers.
- **Excess PR scope:** incidental formatting, unrelated cleanup, unused flexibility, unnecessary public exports, dependencies, configuration, and machinery added for hypothetical needs. Remove additions that do not support the requested outcome. Do not shrink the diff by reverting required behavior or moving work into an unrequested follow-up.
- **Disproportionate supporting code:** elaborate test fixtures, mocks of internal implementation details, redundant documentation, and generated churn. Simplify alongside production code while retaining meaningful behavioral coverage and required generated artifacts.

Minimize concepts, branches, coupling, and review effort. Line and file counts are supporting evidence, not quotas. Do not compress readable code, hide complexity in another file, spread it across callers, or introduce an abstraction solely to produce a smaller diff. Do not manufacture edits when the implementation is already appropriately simple.

## Refactor directly

For each candidate, establish the concrete complexity cost, the simpler replacement, and evidence that required behavior survives. Check the proposed replacement for new coupling, hidden lifecycle assumptions, or loss of useful clarity. Apply material improvements with established behavior; ordinary implementation choices do not need a handoff or permission question.

Preserve externally observable behavior and established constraints. Do not silently remove features, weaken contracts, or overturn an explicit architectural decision to make the code shorter. If a promising simplification needs a material behavior decision, report that exact decision and continue independent work. Do not add speculative hardening or adjacent features during this pass.

Remove superseded paths, unused helpers, imports, configuration, and obsolete test scaffolding created by the refactor. Avoid retaining duplicate implementations as a precaution. Preserve unrelated user work; revert only edits attributable to this simplification pass when an attempted refactor fails.

## Verify and finish

Run focused behavioral checks and repository-required validation appropriate to the changed paths. Reuse existing tests where they demonstrate the affected contracts; update or add lasting coverage only when a meaningful risk is otherwise unprotected. Temporary behavioral checks can supply evidence without becoming committed tests. Do not add tests that merely mirror the new implementation. Record actual commands and outcomes, and disclose unavailable checks or unrelated failures.

Review the entire resulting change against the same pinned base, including newly touched files and interactions. Check that simplifications have not moved complexity elsewhere or removed required behavior. Repair regressions introduced by this pass and rerun affected checks. Repeat when new material opportunities or defects are found; stop when a complete pass finds no further justified simplifications and relevant validation passes. Do not churn among equivalent implementations.

Return a concise report, using the caller's compatible format when supplied:

- What was simplified and which complexity or PR scope it removed.
- Validation performed and its results or limitations.
- The comparison base and incoming versus final diff size, including relevant untracked files. Explain a size increase when it buys a material simplification.
- Any unresolved decision or incomplete coverage that prevents claiming completion.

If no justified simplification exists, say so. Do not imply that this pass established conformance to a plan or completed a comprehensive defect or security audit.

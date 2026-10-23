---
name: diagnose
description: Investigate a concrete bug or performance regression when the user asks to diagnose, reproduce, debug, or repair it. Use for clear debugging intent, not general codebase explanation, descriptions of error handling, hypothetical failures, or incidental mentions that something is broken.
---

# Diagnose

Find the cause of the reported failure using evidence, then repair it when that is part of the request. Match the effort to the uncertainty and impact. A diagnostic signal can be an existing command, observation, trace, or temporary probe; it does not need to become a committed test.

## Recognize the request

Activate for an actual request to investigate a failure or regression. Decide from the user's intended task, not keywords such as "broken," "error," or "not working." A codebase question about how a failure path works does not by itself authorize a debugging and repair workflow.

Preserve the requested scope. If the user asks for diagnosis only, explain the cause and supporting evidence. If repair is requested or already authorized, carry it through. Read relevant repository instructions, code, and existing architectural decisions; no issue-tracker setup or domain glossary is required.

## Establish a useful signal

Identify the expected behavior, actual symptom, triggering conditions, and relevant environment. Inspect available code, logs, callers, configuration, and recent changes before asking for information that may already be available.

Use the cheapest reliable way to observe the reported failure. Prefer an existing command, test, request, captured trace, or focused manual step. If necessary, construct a small temporary harness or targeted instrumentation. Keep disposable artifacts outside the repository where practical. Avoid adding dependencies or permanent test infrastructure to begin an investigation.

Confirm that the signal represents the user's failure. Reduce irrelevant setup when useful, while retaining the conditions that cause the problem. For intermittent failures, record trigger conditions and reproduction rates; do not require perfect determinism. For performance regressions, establish comparable baseline measurements and inspect timings, profiles, or query plans before changing the code.

If reproduction is unavailable, continue useful inspection of the relevant path and available artifacts. Distinguish a proven cause from a supported hypothesis. Ask for the exact missing input or access only when it prevents meaningful progress; do not claim a fix was verified without observing the affected behavior.

## Test explanations against evidence

Form explanations that predict an observable result. Investigate the strongest supported explanation first and consider alternatives when the evidence remains ambiguous. Do not manufacture a fixed number of hypotheses or impose a presentation checkpoint before investigating.

Choose probes that distinguish the explanations: inspect values or state, replay an input, compare configurations or versions, use a debugger, or add narrowly targeted logging. Change one relevant variable at a time where practical. Keep track of temporary changes so they can be removed.

Trace the failure through real callers and dependencies. Find the violated assumption, incorrect state transition, or other causal mechanism before treating a nearby symptom as the root cause. Prefer a small correction to defensive fallbacks that conceal the problem.

## Repair and verify when authorized

Apply the smallest correction that addresses the established cause and preserves required behavior. Keep unrelated cleanup, speculative hardening, and architectural redesign outside the repair.

Replay the original scenario and check relevant neighboring behavior. Use existing focused checks and repository-required validation. Record what was actually run and its outcome; static inspection and an unrelated passing suite do not prove that the reported failure is resolved.

### Decide whether lasting test coverage is useful

A permanent regression test is optional. Add or extend one when it captures a meaningful recurring risk through a stable observable contract and existing coverage does not already protect that behavior. Prefer extending a relevant existing test over creating a new fixture or suite.

Do not add tests simply because a fix was made. Avoid tests that mirror the patch, assert private implementation details, or add mock and fixture machinery disproportionate to the risk. Do not redesign production interfaces solely to make this fix testable.

Temporary reproduction steps, a focused command, or an existing behavioral check may be sufficient verification. There is no required test-before-fix ordering. If permanent coverage is justified, ensure its assertions exercise the real failure and confirm it passes with the correction.

## Finish with evidence

Remove temporary instrumentation, harnesses, and artifacts created for this investigation. Preserve user changes and useful existing coverage. Report the cause, any correction, validation performed, and remaining uncertainty.

When a limitation in the architecture materially contributed to the failure, state the concrete finding for the operator to consider separately. Do not automatically start another workflow, create tickets, or require a post-mortem, commit, or PR.

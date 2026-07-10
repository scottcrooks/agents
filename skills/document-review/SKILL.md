---
name: document-review
description: Review immutable workflow documents for material issues and return an approval or concrete fixes. Use for AFK or human-requested review of design-doc and structured-outline artifacts, especially when the review criteria must distinguish architectural decisions from execution sequencing while preserving a strict caller-provided verdict format.
---

# Document Review

Review the supplied document as a decision gate. Apply shared materiality rules, then use the document-type criteria below.

## Review contract

1. Identify the document type from the caller's stage or artifact metadata. Do not infer a different type from headings alone.
2. Review only the supplied immutable revision. Do not inspect or critique a newer working-tree version unless explicitly requested.
3. Treat accepted scope and explicit upstream decisions as constraints. Flag contradictions; do not silently redesign them.
4. Block only issues that materially affect correctness, safety, scope, feasibility, downstream execution, or required validation.
5. Do not block on taste, prose style, optional hardening, speculative future needs, or preferences already resolved upstream.
6. Return the exact machine-readable response format requested by the caller. Do not add prose, Markdown, or a second verdict outside that format.

If required inputs are absent or the caller's response contract cannot be followed, return a failure verdict in the caller's requested format with the missing information stated concretely.

## Design document criteria

For a `design-doc` artifact, determine whether the proposed design is ready to constrain later planning:

- The problem, goals, non-goals, and affected system boundaries are clear and mutually consistent.
- The recommendation follows from repository evidence and respects documented domain decisions.
- Important alternatives are considered, with reasons for rejecting them.
- State ownership, lifecycle transitions, failure behavior, recovery, and external side effects are explicit where relevant.
- Compatibility, migration, rollout, and observability consequences are addressed when the change introduces them.
- Risks and tradeoffs are honest, and unresolved decisions that would materially alter implementation are surfaced.
- The verification strategy can demonstrate the promised behavior at appropriate seams.

Require fixes when implementation would otherwise need to invent a material architectural decision, when the recommendation contradicts its constraints, or when a significant failure mode has no defined behavior.

## Structured outline criteria

For a `structured-outline` artifact, determine whether it is a faithful, executable decomposition of the approved direction:

- The outline preserves upstream design decisions and explicitly records any authorized superseding direction.
- Work is divided into coherent vertical slices or phases that produce verifiable behavior, rather than disconnected technical layers.
- Ordering and dependencies are correct; foundational contracts precede consumers, while independent work is identified accurately.
- Each slice names its behavioral outcome, affected boundaries, and validation evidence without over-prescribing incidental implementation details.
- Cross-cutting concerns such as compatibility, migration, recovery, issue synchronization, and UI behavior appear in the slices that own them.
- The validation shape covers lifecycle invariants, negative paths, historical compatibility, and the end-to-end user journey where relevant.
- Scope is complete enough for planning but does not smuggle in unrelated refactors or reopen settled architecture.

Require fixes when the outline omits a material design consequence, sequences dependent work incorrectly, cannot be implemented and verified incrementally, or contradicts the approved direction.

## Verdict discipline

Approve when no material blocking issue remains. A non-blocking suggestion is not a reason to require fixes and should be omitted when the caller permits only a verdict tag.

When fixes are required, provide the smallest concrete set of corrections that would make the exact revision approvable. State what is wrong, why it is material, and what the document must clarify or change. Do not prescribe unrelated implementation work.

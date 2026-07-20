---
name: document-review
description: Review immutable workflow documents for completeness, simplicity, and material correctness, then return an approval or concrete fixes. Use for AFK or human-requested review of design-doc and structured-outline artifacts, especially when checking end-to-end UX, frontend/backend responsibilities, or whether a proposal adds unnecessary machinery while preserving a strict caller-provided verdict format.
---

# Document Review

Review the supplied document as a decision gate. Apply shared materiality rules, then use the document-type criteria below.

## Review contract

1. Identify the document type from the caller's stage or artifact metadata. Do not infer a different type from headings alone.
2. Review only the supplied immutable revision. Do not inspect or critique a newer working-tree version unless explicitly requested.
3. Treat accepted scope and explicit upstream decisions as constraints. Flag contradictions; do not silently redesign them.
4. Block only issues that materially affect correctness, safety, scope, feasibility, downstream execution, or required validation.
5. Do not block on taste, prose style, optional hardening, speculative future needs, or preferences already resolved upstream.
6. Treat backward compatibility as opt-in. Unless the caller, accepted scope, or an external constraint explicitly requires it, prefer a clean breaking replacement and do not require legacy behavior, adapters, versioning, dual paths, or staged migration.
7. Keep compatibility separate from correctness and required data safety. Require existing data to survive only when the accepted scope says it must.
8. Return the exact machine-readable response format requested by the caller. Do not add prose, Markdown, or a second verdict outside that format.

If required inputs are absent or the caller's response contract cannot be followed, return a failure verdict in the caller's requested format with the missing information stated concretely.

## Governing review tests

Apply these tests before the document-type criteria:

1. **Trace the promised outcome.** Map each material requirement and user outcome through every relevant boundary: entry point, UX states, frontend behavior, client/server contract, backend/domain behavior, persistence or external effects, and observable result. Do not require layers the change does not touch.
2. **Test completeness.** Check happy paths and relevant loading, empty, validation, permission, failure, retry, cancellation, recovery, and accessibility states. Check data ownership, lifecycle, security, and operational consequences where the proposal introduces them. Check migration and compatibility only when explicitly required.
3. **Test cross-layer consistency.** Ensure UI behavior, API contracts, validation, authorization, error semantics, state transitions, and stored data agree. Flag behavior assigned to no layer, duplicated across layers without reason, or dependent on an undefined contract.
4. **Test minimum sufficient complexity.** Ask whether existing concepts, components, services, and infrastructure can meet the accepted requirements. Require justification for each new abstraction, dependency, service, datastore, background process, state machine, or compatibility path. Flag parallel mechanisms, premature generalization, and flexibility with no current requirement. When a new mechanism replaces an old one, require removal of the old path; require coexistence or migration only for an explicit compatibility or data-survival constraint.
5. **Test decision closure and verifiability.** Ensure implementation does not need to invent a material product or architectural decision and that the proposed evidence can prove the end-to-end outcome and important negative paths.

Treat simplicity as the least complexity that fully satisfies the accepted requirements and constraints, not the fewest components or shortest description. Treat completeness as coverage of material behavior, not exhaustive speculation. Never respond to an omission by proposing a broader system than the requirement needs.

## Design document criteria

For a `design-doc` artifact, determine whether the proposed design is ready to constrain later planning:

- The problem, goals, non-goals, and affected system boundaries are clear and mutually consistent.
- The recommendation follows from repository evidence and respects documented domain decisions.
- Important alternatives are considered, with reasons for rejecting them.
- The recommendation reuses existing mechanisms where they are sufficient, and every material increase in conceptual or operational complexity earns its place against a concrete requirement.
- User journeys and system responsibilities are described end to end, with frontend, backend, data, and external-system boundaries explicit where relevant.
- State ownership, lifecycle transitions, failure behavior, recovery, and external side effects are explicit where relevant.
- When compatibility is explicitly required, its migration and rollout consequences are addressed; otherwise the design cleanly replaces and removes superseded behavior.
- Risks and tradeoffs are honest, and unresolved decisions that would materially alter implementation are surfaced.
- The verification strategy can demonstrate the promised behavior at appropriate seams.

Require fixes when implementation would otherwise need to invent a material architectural decision, when the recommendation contradicts its constraints, or when a significant failure mode has no defined behavior.

## Structured outline criteria

For a `structured-outline` artifact, determine whether it is a faithful, executable decomposition of the approved direction:

- The outline preserves upstream design decisions and explicitly records any authorized superseding direction.
- Work is divided into coherent vertical slices or phases that produce verifiable behavior, rather than disconnected technical layers.
- Ordering and dependencies are correct; foundational contracts precede consumers, while independent work is identified accurately.
- Each slice names its behavioral outcome, affected boundaries, and validation evidence without over-prescribing incidental implementation details.
- Frontend, backend, contract, data, and external-effect changes appear together in the slices that produce their user-visible behavior, where relevant.
- Cross-cutting concerns such as authorization, accessibility, recovery, observability, issue synchronization, and UX states appear in the slices that own them; compatibility and migration appear only when explicitly required.
- The validation shape covers lifecycle invariants, contract boundaries, negative paths, and the end-to-end user journey, plus historical compatibility only when it is a requirement.
- Scope is complete enough for planning but does not smuggle in unrelated refactors or reopen settled architecture.

Require fixes when the outline omits a material design consequence, sequences dependent work incorrectly, cannot be implemented and verified incrementally, or contradicts the approved direction.

## Verdict discipline

Approve when no material blocking issue remains. A non-blocking suggestion is not a reason to require fixes and should be omitted when the caller permits only a verdict tag.

When fixes are required, provide the smallest concrete set of corrections that would make the exact revision approvable. State what is wrong, why it is material, and what the document must clarify or change. Do not prescribe unrelated implementation work.

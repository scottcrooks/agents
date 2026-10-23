---
name: improve-codebase-architecture
description: Find architectural improvements that hide complexity behind simpler interfaces, deepen shallow modules, and consolidate scattered responsibilities. Use to investigate refactoring opportunities across module boundaries and return concrete findings for the operator to act on.
---

# Improve Codebase Architecture

Find places where changing the structure of the code would make real behavior easier to understand, use, change, and verify. Ground opportunities in existing callers and responsibilities. This skill owns investigation and findings; the operator handles ticket creation and subsequent implementation. Keep repository inspection read-only.

A deep module hides substantial complexity behind an interface that is simple to use correctly. That interface includes everything a caller must know: inputs, ordering, state, configuration, and failure behavior. Depth comes from reducing those obligations, not increasing implementation size. A seam is a place where responsibilities meet or behavior can be substituted; follow it to see which side actually owns the complexity.

## Follow the complexity

Start with the requested area or flow and read repository instructions. Inspect relevant architectural decisions and domain documentation when present; no glossary, setup workflow, plan, or new documentation is required to begin. Use the project's familiar names.

Trace real entry points, callers, implementations, dependencies, and tests. Follow the flow across seams rather than judging isolated files. Look for:

- Callers coordinating several modules, knowing their internals, or repeating setup, validation, ordering, cleanup, and error handling.
- Responsibilities split across wrappers and small modules that must be understood or changed together.
- Derived or duplicated state, competing sources of truth, and rules repeated across layers.
- Public interfaces exposing internal options or lifecycle details that could be owned inside the implementation.
- Parallel mechanisms where an existing utility, module, framework capability, or dependency already provides the needed behavior.
- Tests that require extensive internal mocking or assembly because no useful boundary owns the behavior being tested.

Keep exploration bounded to the request. State what was inspected and any coverage limits; do not imply a repository-wide assessment from a small sample.

## Establish a simpler design

For each candidate, identify the concrete maintenance or caller burden and show what would disappear after the refactor. Consider removing indirection, consolidating responsibilities that change together, deriving state, reusing an existing mechanism, or moving coordination behind a smaller interface.

Apply the deletion test: if removing a wrapper leaves callers equally simple, it may not earn its place. If removing a module scatters its responsibilities across callers, it is hiding useful complexity. Check the complete resulting flow; relocating complexity does not remove it.

Assess candidates using the actual callers and constraints:

- Show how callers would use the proposed interface and which decisions the implementation would own. Include a small before/after example when it clarifies the improvement.
- Reduce the total complexity of the interface, implementation, and callers. Avoid combining independent responsibilities into a large module with flags for unrelated uses.
- Preserve useful boundaries for data ownership, authorization, deployment, dependency isolation, and independent change. A thin module can serve one of these purposes; one implementation does not automatically make a seam unnecessary.
- Confirm that reuse matches the required semantics and lifecycle. Do not force different behaviors into a shared abstraction merely because their code looks similar.
- Choose dependency and test strategies from the actual risk. Ports, adapters, injection, and mocks must solve a concrete problem; external I/O alone does not require a new abstraction.

Compare alternatives only when they expose a meaningful tradeoff. Do not invent designs, require parallel agents, or target a number of opportunities. Report when the existing structure earns its complexity.

## Return concrete opportunities

Prioritize by demonstrated benefit and likely change cost. For each opportunity, explain:

- **Evidence:** the relevant files, symbols, callers, and tests, with line references where practical.
- **Current burden:** the decisions or coordination callers must handle, the knowledge repeated across modules, or the responsibilities that must change together.
- **Refactoring direction:** what would be removed, combined, reused, or moved behind a simpler interface, and where responsibilities would live.
- **Expected improvement:** which obligations, branches, duplicated rules, or dependencies would disappear. Explain why the complete flow becomes simpler.
- **Constraints and verification:** behavior and useful boundaries to preserve, material tradeoffs, relevant existing checks, and any unresolved assumption or decision.

Make each finding understandable without the conversation, with enough scope to distinguish a coherent improvement from adjacent cleanup. Group tightly related changes that deliver one simplification; keep independent outcomes separate. Do not expand a finding into a full implementation plan or prescribe a ticket format.

Before reporting, trace the proposed responsibility change through the affected callers and failure paths. Check that it would remove complexity rather than relocate it, preserve required behavior, and retain meaningful test coverage. Use existing tests as evidence of assertions, not proof that execution passed. Distinguish static inspection from observed behavior, and state any evidence gaps.

Return findings directly in the caller's requested format. Leave source, tests, configuration, documentation, and git state unchanged. Stop when the requested area is covered and the opportunities are supported by evidence; a clean assessment with no worthwhile opportunity is a valid result.

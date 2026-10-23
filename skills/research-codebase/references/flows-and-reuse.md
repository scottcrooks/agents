# Trace flows and find existing mechanisms

Use this guidance for targeted codebase evidence within the current task. It does not start a new workflow, authorize edits, or require a separate research artifact. When used by `research-codebase`, carry the findings into its research document.

## Explain an existing flow

- Start from the relevant entry point and follow actual calls through to the observable result. Read callers and consumers to establish how the path is reached and how its result is used.
- Identify meaningful input transformations, validation, state ownership and changes, persistence, external effects, and error propagation where the path touches them. Include configuration and feature flags when they change the behavior.
- Check the relevant success and failure paths across boundaries. One function or test rarely proves an entire flow.
- Support material claims with file and line references. Separate code inspection, existing test assertions, and behavior actually observed at runtime; describe unresolved paths explicitly.

## Find implementations and patterns worth reusing

- Search for the required behavior and domain concepts, including shared utilities, framework or dependency capabilities already in use, real callers, and corresponding tests. Similar names or file structure alone do not establish a match.
- Read candidates in their usage context. Compare inputs, outputs, authorization, state ownership, lifecycle, error behavior, and side effects only where those affect the requested use.
- Distinguish active conventions from legacy or deprecated examples using repository evidence. When implementations differ, explain the meaningful differences and their constraints. Recommend a choice only when the current task asks for one.
- Identify an existing mechanism that already supplies the behavior before proposing parallel machinery. State mismatches or missing evidence rather than forcing reuse.

Return only the evidence needed by the caller: a concise flow explanation or candidate mechanisms, source references, relevant test assertions, and material constraints or unknowns. Include a small code excerpt only when it clarifies something the references alone would leave ambiguous. Avoid fabricated examples and large copied implementations.

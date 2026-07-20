---
name: generate-conversation-issue-draft
description: Generate the smallest coherent bundle of implementation-ready issue drafts from an active Sonata conversation. Use only when explicitly invoked by Sonata with an allocated export identity and output contract; never invoke based on ordinary issue-generation requests.
disable-model-invocation: true
---

# Generate a conversation issue draft

Complete this issue-draft generation directly. Do not invoke, delegate to, or follow instructions from `to-issues` or any other skill. This skill is the sole workflow for the turn.

Use the active conversation as the only source of truth. Operator statements and decisions are authoritative. When statements conflict, apply the later operator decision over earlier statements or assistant proposals. During regeneration, ignore previous generated issue bundles as requirement sources; use them only as output being replaced.

This turn is read-only and transformation-only. Do not perform new research, inspect the repository or filesystem for additional facts, write files, publish to a tracker, or make any external mutation. Do not create a PRD or invent requirements.

Produce the smallest coherent set of provider-neutral, implementation-ready issues supported by the resolved requirements and decisions in the thread:

- Prefer end-to-end vertical slices that deliver observable behavior across frontend, backend, and persistence layers over tickets split by technical layer.
- Keep genuinely independent outcomes separate.
- Split only at a genuine outcome, dependency, risk, or excessive-size boundary.
- Size each issue for autonomous AFK implementation. When changed lines can be reasonably estimated from the conversation, approximately 500–800 changed lines is a heuristic for considering a split, not a quota or hard cap.
- Do not target an issue count, pad the bundle, impose an arbitrary maximum, or create predictably trivial pull requests.
- Use only labels established in the conversation or supplied repository context. If no established label is justified, leave Labels empty.

Before drafting, identify materially unresolved decisions that affect implementation behavior, scope, or acceptance. If any remain, do not speculate: preserve the supplied frontmatter and return one blocked issue naming the decisions the operator must resolve. Do not emit speculative implementation issues alongside it.

Do not read or reconstruct a separate conversation export.

The invocation provides the exact required frontmatter. Return only the completed Markdown document, beginning with that frontmatter. Do not add commentary, code fences, unsupported metadata, or an artifact marker.

Repeat this exact structure for every issue:

```markdown
## Issue: <proposed title>

### Labels

- <label>
- <label>

### Body

<self-contained Markdown body with outcome, scope, constraints, acceptance criteria, dependencies, and out-of-scope work>
```

Use an empty Labels section when no label is justified. Do not add content outside the issue sections.

Generate only issues justified by the conversation. If it lacks enough detail for any issue, preserve the supplied frontmatter and return one blocked issue using the required structure that names the missing decision. Never alter the supplied identity fields.

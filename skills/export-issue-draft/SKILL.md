---
name: export-issue-draft
description: Export a Sonata-tagged conversation issue source into one provider-neutral Markdown issue artifact. Use only when explicitly invoked by Sonata with conversationIssueSource JSON and an assigned outbox; never invoke for ordinary issue drafting or publication requests.
disable-model-invocation: true
---

# Export an issue draft

Use only the tagged `conversationIssueSource` JSON supplied by Sonata. It is the complete source of truth.

Create a concise, provider-neutral issue proposal with a useful title and a self-contained Markdown body. Preserve the supplied `conversationId` and `exportId` in the frontmatter. Do not include provider, project, team, routing, credential, or workflow fields.

Write the result to `issue.md.partial` in the assigned outbox, then atomically rename it to `issue.md`. The version-1 frontmatter must contain exactly:

```yaml
formatVersion: 1
exportId: <the supplied exportId>
conversationId: <the supplied conversationId>
title: <non-empty title>
```

Follow the frontmatter with a non-empty Markdown body. Finish with exactly `<artifact path="issue.md" mediaType="text/markdown"/>` and no surrounding response text.

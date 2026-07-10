---
name: code-review
description: Review staged, unstaged, and untracked non-ignored Git working changes before commit, returning an AFK-safe JSON verdict and actionable defect findings. Use only when the user explicitly invokes `$code-review`; never invoke implicitly for general review, implementation, commit, or pull-request tasks.
---

# Code Review

Review the current working changes as a narrow pre-commit quality gate. Find concrete defects
introduced or materially worsened by the change. Do not modify files.

## Collect the review set

Run the bundled `scripts/collect_review_set.py` with Python 3 while the current directory is the
target repository. Resolve the script path from this skill directory; do not assume the target
repository contains the script. Use its JSON manifest as the coverage ledger.

Include staged changes, unstaged tracked changes, and untracked files not excluded by Git
ignore rules. Include deletions, renames, and partially staged files. Exclude every file inside
a directory named `thoughts` from the review set.

Account for every manifest entry before returning a verdict. Inspect every changed hunk, but
load unchanged context only when needed to establish behavior. Do not mistake an inability to
review a binary file for evidence of a defect.

## Read intent selectively

Treat files beneath `thoughts/` only as optional intent context. Search them when changed names,
symbols, issue references, or unclear behavior identify a likely relevant document. Do not load
the whole directory by default, and never produce a finding against a thoughts file.

Treat executable behavior, tests, repository documentation, and established contracts as stronger
evidence than aspirational intent notes.

## Scale the review

Inspect the manifest before loading the complete patch.

- For a small working set, review the complete patch directly.
- For a larger working set, group files into semantic slices such as API and callers, domain
  behavior, persistence, UI, tests, and deployment.
- Review slices rather than arbitrary line-count chunks.
- Prioritize authorization, validation, persistence, migrations, concurrency, error paths, public
  interfaces, state transitions, compatibility, and destructive operations.
- Finish with an integration pass across slices and verify that every manifest entry was covered.

Run focused tests or checks when they materially improve confidence. Do not require exhaustive
validation when targeted inspection establishes the result.

## Apply the AFK finding standard

Admit a finding only when all of the following are true:

1. The working change introduces or materially worsens the problem.
2. Repository evidence supports a realistic failure path.
3. The impact is concrete rather than stylistic, preferential, or speculative.
4. A specific, localized correction can be described.

Use these severities:

- `p0`: Likely catastrophic impact, such as a security compromise, irreversible widespread data
  loss, or severe production outage.
- `p1`: A concrete material failure in an expected path, such as broken core behavior,
  authorization bypass, data corruption, reliable crash, incompatible interface change, invalid
  migration, or deployment failure.
- `p2`: A real but limited defect, uncommon edge-case failure, or localized operational weakness.

Omit style, naming, formatting, organization preferences, optional refactors, cleanup, generic
test suggestions, speculative risks, and pre-existing problems unaffected by the change. Missing
tests or unavailable validation are not findings without evidence of an actual defect. Omit all
`p3`-level feedback.

Only `p0` and `p1` findings block. Include at most the three most material, high-confidence `p2`
findings so the implementation agent can make safe localized corrections without creating a long
review loop. P2 findings never change an approved verdict and do not require re-review.

## Return JSON only

Return exactly one valid JSON object with this shape:

```json
{
  "verdict": "approved",
  "findings": [
    {
      "id": "CR-1",
      "severity": "p2",
      "file": "path/to/file.go",
      "line": 42,
      "title": "Concise description of the defect",
      "evidence": "Repository evidence establishing the failure path.",
      "impact": "Concrete result when the failure occurs.",
      "suggested_fix": "The smallest acceptable correction direction.",
      "verification": "A focused way to verify the correction."
    }
  ]
}
```

Set `verdict` to `blocked` if any finding has severity `p0` or `p1`; otherwise set it to
`approved`. Order findings by severity and then impact. Assign identifiers sequentially as `CR-1`,
`CR-2`, and so on. Use a repository-relative path. Use `null` for `line` only when no meaningful
line exists.

When there are no findings, return exactly `{"verdict":"approved","findings":[]}`.

Output only the JSON object. Do not use Markdown fences, introductory text, summaries, comments,
or text after the object. Do not add undocumented fields.

---
name: code-review
description: Review Git changes for concrete defects and return an AFK-safe JSON verdict with P0/P1 blocking and limited P2 advisory findings. Use only when explicitly invoked as $code-review, including Sonata AFK terminal review sessions with a pinned target and workflow artifacts; never invoke implicitly for general review, implementation, commit, or pull-request tasks.
---

# Code Review

Review the requested Git change set as a narrow quality gate. Find concrete defects introduced or materially worsened by the change. Do not modify files.

## Select the review mode

Use pinned AFK mode when the caller supplies a target containing `stageAttemptId`, `baseCommit`, `headSha`, and `checksum`. Otherwise use interactive pre-commit mode.

### Interactive pre-commit mode

Run `scripts/collect_review_set.py` with Python 3 from the target repository. Review staged, unstaged, and untracked non-ignored changes relative to `HEAD`.

### Pinned AFK mode

1. Echo the caller's target exactly in the final JSON.
2. Verify that `git rev-parse HEAD` equals `target.headSha`. If it does not, return a blocked P1 finding explaining that the pinned target is stale.
3. Run `scripts/collect_review_set.py --base <target.baseCommit>` from the target repository. This includes committed, staged, unstaged, and untracked publishable changes relative to the pinned base.
4. Treat supplied workflow artifacts as intent and acceptance context. They may contain research, design, outline, or plan decisions. Do not report findings against artifact files.
5. Review the collected worktree state. Sonata revalidates the checksum after the verdict; do not recompute or replace the caller's checksum.

Treat every checksum as a new full-snapshot review. A previous verdict or a familiar
`stageAttemptId` may provide context, but it must not narrow the review to files changed since the
last verdict or to the area of the previous finding. Re-account for the complete current manifest.

## Cover the review set

Use the collector's JSON manifest as the coverage ledger. Exclude every file inside a directory named `thoughts` from findings and the executable review set.

Account for every manifest entry. Inspect every changed hunk, loading unchanged context only when needed. Do not mistake an inability to inspect a binary file for evidence of a defect.

Keep an internal ledger of the files and changed hunks inspected. Tool-output truncation is
incomplete coverage, not a reason to infer that the omitted patch is safe. If any diff or file read
is truncated, split it into smaller semantic or per-file reads and inspect the omitted content
before returning.

For a large set, group files into semantic slices such as domain behavior, persistence, API and callers, UI, tests, and deployment. Finish with an integration pass across slices.

Prioritize authorization, validation, persistence, migrations, concurrency, error paths, public interfaces, state transitions, compatibility, and destructive operations. Run focused checks only when they materially improve confidence.

## Complete defect discovery

A confirmed blocker is not a stopping condition. Continue through the complete manifest and return
all independent, high-confidence P0 and P1 findings in the current snapshot. The three-finding
limit applies only to P2 findings.

Use this discovery loop before producing the verdict:

1. Review every semantic slice and collect candidate defects without finalizing after the first
   confirmed finding.
2. Make an integration pass through changed entry points, callers, state transitions, and visible
   user flows. Trace each expected path past its first failure point so one early break does not
   hide a second defect in the same flow.
3. For every confirmed finding, mentally apply the smallest suggested correction and trace the
   affected flow again. If that correction exposes another defect already present in the reviewed
   snapshot, report the additional defect or broaden the finding to the complete root cause. Do
   not report a problem that would be introduced only by a hypothetical future implementation.
4. After the latest new candidate, perform one final independent search for additional defects
   across the coverage ledger. Return only when that pass produces no new qualifying finding and
   every manifest entry is accounted for.

On a re-review, evaluate the whole refreshed snapshot using the same loop. Verify prior fixes, but
do not assume the previous review exhausted unchanged files or adjacent behavior.

## Apply the finding standard

Admit a finding only when all are true:

1. The reviewed change introduces or materially worsens the problem.
2. Repository evidence supports a realistic failure path.
3. The impact is concrete, not stylistic, preferential, or speculative.
4. A specific, localized correction can be described.

Use these severities:

- `p0`: Likely catastrophic impact such as security compromise, irreversible widespread data loss, or severe production outage.
- `p1`: Concrete material failure in an expected path such as broken core behavior, authorization bypass, data corruption, reliable crash, incompatible interface change, invalid migration, or deployment failure.
- `p2`: Real but limited defect, uncommon edge-case failure, or localized operational weakness.

Only P0 and P1 findings block. Include at most the three most material, high-confidence P2 findings. P2 findings never change an approved verdict and do not require re-review.

Omit style, naming, formatting, organization preferences, optional refactors, cleanup, generic test suggestions, speculative risks, and pre-existing problems. Missing tests or unavailable validation are not findings without evidence of a defect. Omit P3 feedback.

## Return JSON only

Return exactly one JSON object. In interactive mode omit `target`. In pinned AFK mode include it exactly as supplied.

```json
{
  "target": {
    "stageAttemptId": "run-1/implement-plan-1",
    "baseCommit": "base-sha",
    "headSha": "head-sha",
    "checksum": "sha256:opaque-pinned-value"
  },
  "verdict": "blocked",
  "findings": [
    {
      "id": "CR-1",
      "severity": "p1",
      "file": "path/to/file.ts",
      "line": 42,
      "title": "Concise defect title",
      "evidence": "Repository evidence establishing the failure path.",
      "impact": "Concrete result when the failure occurs.",
      "suggested_fix": "Smallest acceptable correction direction.",
      "verification": "Focused way to verify the correction."
    }
  ]
}
```

Set `verdict` to `blocked` if and only if at least one finding is P0 or P1; otherwise use `approved`. Order findings by severity and impact. Assign IDs sequentially as `CR-1`, `CR-2`, and so on. Use repository-relative paths and `null` for `line` only when no meaningful line exists.

When there are no findings, return `{"verdict":"approved","findings":[]}` in interactive mode, or the same object with the exact `target` included in pinned AFK mode.

Output only JSON. Do not use Markdown fences or add undocumented fields.

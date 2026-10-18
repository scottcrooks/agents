# Quick workflow evaluation

Use this protocol when comparing skill revisions or planning models. Ordinary research, planning, and implementation do not require an evaluation run.

## Controlled inputs

- Choose representative bounded tasks across routine local changes, interacting components, and difficult design decisions. Include relevant negative paths, stale research, unresolved evidence, and resume/manual-checkpoint cases where they occur in real work.
- For each task, freeze the starting repository revision, permitted scope, acceptance criteria, environment/setup, and independent behavioral checks. Record relevant working-tree changes as well as the commit.
- Review reference research for factual accuracy and flow coverage, and a reference plan for decision closure and executable validation. Do not treat one model's unreviewed output as the reference answer.
- Record the actual model identifier, reasoning effort, skill revision, tool/harness configuration, and inputs for every run. Preserve current reasoning effort for the baseline; change it separately from skill wording so the effect can be attributed.
- Run each stage in a fresh context with only its normal prompt, supplied artifacts, repository, and instructions. Do not supply hidden conversation context or leak the reference answer into the evaluated run.
- Use isolated local workspaces and the same permitted resources. Keep internal code and data within the authorized environment. A comparative evaluation does not authorize external uploads or production effects.

## Stage comparisons

| Run | Fixed input | Evaluated output |
| --- | --- | --- |
| Luna research | Task and starting repository | Evidence accuracy, relevant flow/failure/test coverage, explicit unknowns |
| Luna / Sol / Astra planning | Same task, reviewed research, and starting repository | Scope, closed decisions, acceptance coverage, executable slices and ledger |
| Luna implementation | Reviewed plan, initialized ledger, and starting repository | Acceptance behavior, negative paths, scope adherence, validation and ledger accuracy |
| Complete chain | Same task and starting repository | Luna research → each planning model → Luna implementation |

Compare current and candidate skill text on the same task set. Repeat runs (for example, three per configuration) to expose variability; increase the sample before drawing conclusions about small differences. Run both stage-isolated and complete-chain comparisons: isolated success can hide information lost at a handoff.

## Outcomes to record

- Independently verified acceptance behavior, omitted requirements, and regressions. A self-reported completion or passing ledger check is not a functional pass.
- Unsupported research claims and missed boundaries; distinguish static code evidence, test assertions, and observed runtime results.
- Material decisions left to the executor, unplanned rediscovery, stale-evidence repairs, and scope changes.
- Human interventions, avoidable escalations, retries, and boundary-check repairs. Record whether each originated in research, planning, implementation, or the harness; do not penalize a correct escalation for genuinely missing authority.
- Elapsed time, tool calls, available token/cost metrics, and total cost per successfully completed task, including failed attempts and retries. Record unavailable metrics as unavailable.

## Decision rule

Set acceptance thresholds before comparing runs. Reject revisions that materially reduce correctness or scope adherence. Among configurations that meet the quality bar, prefer the lowest total cost and latency for the complete task. Report counts, task mix, repetitions, and unresolved limitations; do not infer measured model efficacy from a static review, synthetic boundary tests, or one successful run.

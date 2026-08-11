# R5.7 Better STM archive path mapping

本文件记录 `PR-better-archive` 对 R5.7 / Better STM-facing 资产的迁移映射。粒度是 **asset-level mapping**：每一行对应 asset map 中明确要求归档的文件或目录资产；目录资产下的所有子文件均随目录整体迁移，未在迁移过程中改写历史内容。

## 1. 资产级映射

| asset_id | 原 active 路径 | archive 新路径 | 状态 | 当前替代入口 |
|---|---|---|---|---|
| A-011 | `experiment_design/evaluation_logic.md` | [experiment_design/evaluation_logic.md](./experiment_design/evaluation_logic.md) | archived historical evaluation logic | [../../experiment_design/README.md](../r7_issue_lifecycle_scaffold/experiment_design/README.md), [../../story/claim_evidence_map.md](../r8_story_pre_rebuild/story/claim_evidence_map.md) |
| A-006 | `experiment_design/quality_model/` | [experiment_design/quality_model/](./experiment_design/quality_model/) | archived Better STM definition / repair target taxonomy | [../../story/task_boundary.md](../r8_story_pre_rebuild/story/task_boundary.md), future `PR-issue-ledger` |
| A-007 | `experiment_design/metrics/objective_metric_framework.md` | [experiment_design/metrics/objective_metric_framework.md](./experiment_design/metrics/objective_metric_framework.md) | archived objective metrics framework | [../../experiment_design/metrics/README.md](../r7_issue_lifecycle_scaffold/experiment_design/metrics/README.md), future `PR-eval-rubric` |
| A-008 | `experiment_design/protocols/` | [experiment_design/protocols/](./experiment_design/protocols/) | archived Better adjudication prompt / schema | future `PR-eval-rubric` |
| A-009 | `experiment_design/better_adjudication_dry_run/` | [experiment_design/better_adjudication_dry_run/](./experiment_design/better_adjudication_dry_run/) | archived constructed `STM_k` answer-key suite | future calibration only; not active method evidence |
| A-010 | `experiment_design/repair_target_adjudication/` | [experiment_design/repair_target_adjudication/](./experiment_design/repair_target_adjudication/) | archived static adjudication dry-run | future source-level issue taxonomy design may cite as historical caution only |
| A-011 | `experiment_design/eligibility/` | [experiment_design/eligibility/](./experiment_design/eligibility/) | archived Better STM eligibility | future `PR-loop-io` / `PR-exp-protocol` must redefine eligibility |
| A-004/A-005 | `experiment_design/scope/` | [experiment_design/scope/](./experiment_design/scope/) | archived R5.5/R5.6/R5.7 scope handoff | [../../story/model_scope.md](../r8_story_pre_rebuild/story/model_scope.md) |
| A-011/A-012 | `pipeline/evaluation/` | [pipeline/evaluation/](./pipeline/evaluation/) | archived R4/R5.7 evaluation gate / schemas / dry-run examples / blind outputs | [../../pipeline/evaluation/README.md](../../pipeline/evaluation/README.md), future `PR-eval-rubric` |
| A-015/R5.7.4 | `pipeline/representation/reports/r5_7_4_adjudication_fcstm_exports/` | [pipeline/representation/reports/r5_7_4_adjudication_fcstm_exports/](./pipeline/representation/reports/r5_7_4_adjudication_fcstm_exports/) | archived R5.7.4 standalone adjudication baseline `.fcstm` bundles for `0001` / `0018` | [../../pipeline/representation/README.md](../../pipeline/representation/README.md); future pilot must re-register source trace before reuse |
| A-015/R5.7.4 | `pipeline/representation/reports/r5_7_4_adjudication_baseline_bundles/` | [pipeline/representation/reports/r5_7_4_adjudication_baseline_bundles/](./pipeline/representation/reports/r5_7_4_adjudication_baseline_bundles/) | archived R5.7.4 / R5.7.5 logical symlink fan-in for adjudication baseline bundles | [../../pipeline/representation/README.md](../../pipeline/representation/README.md); not active representation contract |
| A-013 | `reports/2026-07-02-17-02-42-r5-7-1-evaluation-logic.md` | [reports/2026-07-02-17-02-42-r5-7-1-evaluation-logic.md](./reports/2026-07-02-17-02-42-r5-7-1-evaluation-logic.md) | archived R5.7.1 report | [../../reports/SUMMARY.md](../../reports/SUMMARY.md) |
| A-013 | `reports/2026-07-03-02-16-16-r5-7-2-better-stm-target-contract.md` | [reports/2026-07-03-02-16-16-r5-7-2-better-stm-target-contract.md](./reports/2026-07-03-02-16-16-r5-7-2-better-stm-target-contract.md) | archived R5.7.2 report | [../../reports/SUMMARY.md](../../reports/SUMMARY.md) |
| A-013 | `reports/2026-07-03-21-18-25-r5-7-3-objective-metric-framework.md` | [reports/2026-07-03-21-18-25-r5-7-3-objective-metric-framework.md](./reports/2026-07-03-21-18-25-r5-7-3-objective-metric-framework.md) | archived R5.7.3 report | [../../reports/SUMMARY.md](../../reports/SUMMARY.md) |
| A-013 | `reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md` | [reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md](./reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md) | archived R5.7.4 report | [../../reports/SUMMARY.md](../../reports/SUMMARY.md) |
| A-013 | `reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md` | [reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md](./reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md) | archived R5.7.5 constructed report | [../../reports/SUMMARY.md](../../reports/SUMMARY.md) |
| A-013 | `reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md` | [reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md](./reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md) | archived R5.7.5 blind report | [../../reports/SUMMARY.md](../../reports/SUMMARY.md) |

## 2. 文件数复验

迁移后可用以下命令复验目录级文件数：

```bash
find project_1_llm_state_machine_modeling/paper_stm_repair/archive/r5_7_better_stm_snapshot/experiment_design -type f | wc -l
find project_1_llm_state_machine_modeling/paper_stm_repair/archive/r5_7_better_stm_snapshot/pipeline/evaluation -type f | wc -l
find project_1_llm_state_machine_modeling/paper_stm_repair/archive/r5_7_better_stm_snapshot/pipeline/representation -type f | wc -l
find project_1_llm_state_machine_modeling/paper_stm_repair/archive/r5_7_better_stm_snapshot/pipeline/representation -type l | wc -l
find project_1_llm_state_machine_modeling/paper_stm_repair/archive/r5_7_better_stm_snapshot/reports -type f | wc -l
```

当前迁移快照统计：

| archive 子树 | regular files | symlinks |
|---|---:|---:|
| `experiment_design/` | 42 | 0 |
| `pipeline/evaluation/` | 818 | 0 |
| `pipeline/representation/` | 19 | 4 |
| `reports/` | 6 | 0 |
| payload total | 885 | 4 |
| snapshot total including this README/PATH_MAPPING | 887 | 4 |

> Symlink note：`pipeline/representation/reports/r5_7_4_adjudication_baseline_bundles/bundles/` 下 4 个 symlink 均属于 historical logical bundle fan-in。`0001` / `0018` 指向本 archive 内 R5.7.4 standalone exports；`0000` / `0045` 指向 active R4.5 selected-smoke representation exports。后续若重构 active R4.5 路径，必须同步保持这些 historical links 可读，或以单独 archive-maintenance PR 物化其目标。

## 3. 复用限制

1. 本 mapping 只证明历史证据未丢失，不证明 archive 资产仍可作为 active protocol。
2. 后续若要迁移某个字段、schema 或 prompt discipline，必须在新的 source-level issue lifecycle PR 中重新定义，并在 PR body / comment 说明为什么迁移。
3. `pipeline/evaluation/` 中的 diagnostic / scenario schema 不得直接恢复为 active schema；必须由 `PR-issue-ledger` / `PR-eval-rubric` 用新字段重建。

# evaluation/ — 两份 v0 schema 的残留脚手架（**不是论文的评测**）

> 🔴 **别被目录名骗了。paper1 的评测不在这里。**
>
> | 你想找 | 去哪 |
> | :-- | :-- |
> | 实验结果、命中率、`hit@k`、多报统计 | [../../discover_matrix/](../../discover_matrix/) |
> | 判定口径、命中判据、台账规则 | [../../discover_matrix/docs/protocol/](../../discover_matrix/docs/protocol/) |
> | 给导师的自包含全量报告 | [../../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) |
> | 旧 Better STM evaluation gate 全树 | [../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/](../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/) |

本目录现在只剩两份 v0 JSON Schema、它们的 fixture 与门禁测试。它诞生于 2026-07 的「source-level issue lifecycle」设计阶段，用于冻结 issue ledger 与 source trace 的字段合同。后来实际的评测改由 [../../discover_matrix/](../../discover_matrix/) 以台账 + 判定表的方式承担，本目录**没有再往下建**，也不参与任何一格实验。

⚠️ **原先写在这里的后续路线已作废。** paper1 收窄为 issue discover 单独成篇（repair 另立后续论文），因此「Discover → 多轮 Repair-Confirm → B-final → post-Confirm export → closure/regression」这条链**不再是主线**，`closure` / `regression` 也不再是待建的评测终点。

## 有什么

| 项 | 状态 | 入口 |
| :-- | :-- | :-- |
| source issue ledger schema v0 | 已定义 | [schemas/source_issue_ledger.schema.json](./schemas/source_issue_ledger.schema.json) |
| source issue ledger fixtures | 6 个合同 fixture | [fixtures/source_issue_ledger/](./fixtures/source_issue_ledger/) |
| source trace schema v0 | 已定义 | [schemas/source_trace.schema.json](./schemas/source_trace.schema.json) |
| source trace fixtures | 6 个合同 fixture | [fixtures/source_trace/](./fixtures/source_trace/) |
| 门禁测试 | 45 个 | [tests/](./tests/) |
| closure rubric / regression protocol / judge prompt / baseline contract | 未定义，且**不再计划在此定义** | — |

本目录**没有 `src/`**，不含任何可执行方法代码；两份 schema 的消费方是 fixture 与测试本身。

两份 schema 的设计报告（属稳定合同说明，不是实验结果）：[2026-07-08-10-15-00-pr-issue-ledger-contract.md](../../reports/2026-07-08-10-15-00-pr-issue-ledger-contract.md)、[2026-07-08-14-03-59-pr-source-trace-contract.md](../../reports/2026-07-08-14-03-59-pr-source-trace-contract.md)；对应设计入口 [../../experiment_design/issue_lifecycle/](../../archive/r7_issue_lifecycle_scaffold/experiment_design/issue_lifecycle/) 与 [../../experiment_design/source_trace/](../../archive/r7_issue_lifecycle_scaffold/experiment_design/source_trace/)。

## 怎么用

```bash
P=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline
PYTHONPATH=$P/readiness_audit/src:$P/representation/src:$P/conversion/src \
python -m pytest $P/evaluation/tests
```

无需 `.env`，不调用 provider。

## 禁止误读

1. 不把 archived `EVALUATION_GATE.md` 当作 active gate。
2. 不把 archived `better_stm_checklist.schema.json` 或 `can_claim_better_stm` 当作 active endpoint。
3. 不把 archived dry-run examples 或 blind judge outputs 写成真实运行证据。
4. 不把本目录的两份 v0 schema 当成论文评测口径——**论文的判定口径在 [../../discover_matrix/docs/protocol/](../../discover_matrix/docs/protocol/)**。

## 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-08-11 | 按 issue discover 收窄口径重写导引：删除 Repair-Confirm / B-final / closure 主线表述，改为指向 `discover_matrix/` 作为真实评测入口。 |
| 2026-07-17 00:32:36 | active scaffold 对齐一次 Discover、多轮 Repair-Confirm、B-final 与 C source audit；删除旧 loop-io 路由。（该路线已于 2026-08-11 作废） |
| 2026-07-08 14:03:59 | `PR-source-trace` 新增 source trace schema、六个合同 fixture 与 pytest gate。 |
| 2026-07-08 10:15:00 | `PR-issue-ledger` 新增 source issue ledger schema、六个合同 fixture 与 pytest gate。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后重建 placeholder；旧 R4/R5.7 evaluation directory 已冷归档。 |

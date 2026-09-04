# pipeline/evaluation — 历史 v0 schema

本目录只保留 2026-07 的两份 v0 JSON Schema、fixture 与门禁测试，供历史 provenance 复核。它不参与 v60/current 或 X1v2 baseline 的评测，也不是论文的结果或复算入口。当前评测包为 [evaluation/](../../evaluation/README.md)，当前结果为 [v61 归档](../../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)，冻结判定定义见 [issue #195 snapshot](../../judge/src/paper_stm_judge/resources/semantic_judge_issue_195.snapshot.md)。

本目录原先的 Discover → Repair-Confirm → B-final → post-Confirm export → closure/regression 设计已经归档，不能被读作当前计划或待建 endpoint。

## 有什么

| 项 | 状态 | 入口 |
| :-- | :-- | :-- |
| source issue ledger schema v0 | 已定义 | [schemas/source_issue_ledger.schema.json](./schemas/source_issue_ledger.schema.json) |
| source issue ledger fixtures | 6 个合同 fixture | [fixtures/source_issue_ledger/](./fixtures/source_issue_ledger/) |
| source trace schema v0 | 已定义 | [schemas/source_trace.schema.json](./schemas/source_trace.schema.json) |
| source trace fixtures | 6 个合同 fixture | [fixtures/source_trace/](./fixtures/source_trace/) |
| 门禁测试 | 45 个 | [tests/](./tests/) |
| closure rubric / regression protocol / judge prompt / baseline contract | 未定义，且**不再计划在此定义** | — |

本目录没有 `src/`，不含当前方法、Judge 或 evaluation 代码；两份 schema 的消费方是 fixture 与测试本身。

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
4. 不把本目录的两份 v0 schema 当成当前论文评测口径；当前口径、指标与复算由 [evaluation/](../../evaluation/README.md) 和 [v61 归档](../../final_results/v61_source_divergence_vs_x1v2_baseline/README.md) 固定。

## 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-08-11 | 按 issue discover 收窄口径重写导引：删除 Repair-Confirm / B-final / closure 主线表述，改为指向 `discover_matrix/` 作为真实评测入口。 |
| 2026-07-17 00:32:36 | active scaffold 对齐一次 Discover、多轮 Repair-Confirm、B-final 与 C source audit；删除旧 loop-io 路由。（该路线已于 2026-08-11 作废） |
| 2026-07-08 14:03:59 | `PR-source-trace` 新增 source trace schema、六个合同 fixture 与 pytest gate。 |
| 2026-07-08 10:15:00 | `PR-issue-ledger` 新增 source issue ledger schema、六个合同 fixture 与 pytest gate。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后重建 placeholder；旧 R4/R5.7 evaluation directory 已冷归档。 |

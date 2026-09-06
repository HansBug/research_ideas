# Paper STM Evaluation

`paper-stm-evaluation` 负责 provider-free 的评测和报告：headline comparison 读取已经完成的 method 与人工裁定制品、ledger 和冻结参考数据，计算并验证跨 arm 指标。所有 validity、relation、D/A、K/N/I 和成分分析先由人工完成；evaluation 不参与发现，也不重新裁定，只做结构校验、机械汇总和算术复算。method 不 import evaluation。隔离的 predicate-gold 子模块可以执行和重放预冻结 evaluation-only query，边界见下文。

## 指标所有权

| 指标 | 含义与分母 |
| --- | --- |
| hit@1 / overall FULL | round-level expected row 的 `FULL` 数，当前主宇宙为 435 行 |
| hit@3 | 每条 expected 在 3 个 round 中至少一次 `FULL`，分母 145 |
| hit@all | 每条 expected 在 3 个 round 中均为 `FULL`，分母 145 |
| L2 | 仅 ledger 的 L2 expected；当前分母分别为 117 round-level row 或 39 expected |
| report-based precision | `VALID_KNOWN + VALID_NOVEL` 除以全部 report；`INVALID` report 才进入 ordinary FP |
| K/N/I | 人工裁定后的 report-level 与 root-cause cluster-level 的 `VALID_KNOWN`、`VALID_NOVEL`、`INVALID` 汇总 |
| W-on-hits | 对每条 `FULL` expected 聚合其 supporting report 的最高 W；分母是 FULL hits，不是 finding 数 |
| predicate execution usage | registry 中产生至少一条 terminal receipt 的 distinct predicate-ID 覆盖；v60 为 12/19 |
| cost | method 调用、token、cache、retry 与 cost eligibility；缺少可定价 usage 时不以估算值补齐 |

W 不依赖 19 谓词体系。X1v2 的 predicate usage 不适用，但其 W 来自 512 条冻结 finding 的两轮独立逐条审计；evaluation 将此 finding-level 结果按冻结 `full_report_ids` 聚合为 hit-level max-W。

## 归档复算

权威入口是 `paper_stm_evaluation.final_results_archive`。该命令只读归档并核查 schema、映射、hash、链接和离线复算，不调用 provider，也不依赖未跟踪 `runs/`。

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

当前结论和机器可读汇总在 [v61 归档](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)（复算脚本 `discover_matrix/docs/generations/v61/evaluate_rq3.py` 与 `evaluate_full.py`）；下列命令验证 v60 人工评测归档（仪器校准参照）的结构完整性。`pipeline.evidence_discovery.reporting.final_results_archive` 仅是兼容入口，不是新的 evaluation 所有权。

### Paper-facing predicate summary

v60 的 registry 有 19 个谓词，分为 Structure (6)、Topology (4)、Trajectory
simulation (4) 和 Bounded verification (5) 四族。冻结 v60 method summary 显示，
12 个 distinct predicate IDs 产生过 terminal receipt；current v4 canonical
decisions 显示，8 个 distinct predicate IDs 至少绑定到一条 report-bound finding。
两者的分母都是 registry 的 19 个 ID，但统计单位不同，不能解释为 finding、W2、hit
或缺陷类型覆盖率。X1v2 没有同构 predicate binding/receipt schema，因此该项为
N/A，不是零。

fair-comparison summary 同时保留 `825/1271` report-bound binding rows 和
`303/825` legacy `coverage_class` marker，作为行级审计诊断；它们
不替代上面的 12/19、8/19 distinct-ID 指标。逐条 property/input 审计及其详细
能力审计属于 evaluation-only 材料，不是 paper1 方法输入或主结果。

## Internal predicate-backend audit (evaluation-only)

[predicate gold v1](../discover_matrix/ledger_v2/predicate_gold_v1/README.md) 是当前 145 条 ledger 义务的 method-independent 内部能力审计 overlay。它保存属性、typed input、执行和 receipt 记录，用于 evaluation-only 的复核；不属于 paper1 主叙事，也不构成 method 的输入、expected-predicate 覆盖承诺或 discovery 约束。evaluation 可以调用冻结 method backend 或 pyfcstm-native evaluation-only oracle 来执行、重放和验证已冻结 query；依赖方向只能是 evaluation -> frozen backend。method 不得 import、打包或读取 gold。

gold 的 provider-free 工具负责 canonical/schema/TSV/summary 校验、47 条 executable exact/proxy 的 defective/control 全量 replay、manifest/hash 检查，以及冻结 v60 expected-vs-actual 成分分析。expected-vs-actual 只解释 predicate/input 使用；不同但 sound、归因正确且完成执行的 method 证据不会因不复现 gold ID 而降级。gold 不重算或改写 FULL/PARTIAL hit、W、K/N/I。

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/src:. \
python -m paper_stm_evaluation.predicate_gold_release validate \
  --canonical project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/predicate_gold_v1.json \
  --inventory project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/inventory.json \
  --summary project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/summary.json \
  --tsv project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/predicate_gold_v1.tsv \
  --schema project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/predicate_gold_v1.schema.json \
  --review-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/review \
  --active-review-manifest project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/review/active_review_manifest.json
```

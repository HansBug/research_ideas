# 归档字段与指标口径

## 制品关系

`raw/<side>/method/` 与 `raw/<side>/judge/` 是从冻结运行制品复制的结构化审计面；它们不由本目录内的 reporting 工具修改。`derived/recomputed_summary.json` 是唯一的派生汇总，生成器为 `pipeline.evidence_discovery.reporting.final_results_archive`。`reference/ledger.json` 只由 evaluator 用于识别 expected issue 和 L2，不进入 method 输入。

每侧 `archive_manifest.json` 列出原始审计文件、字节数和 `sha256`。顶层 `archive_manifest.json` 覆盖 raw、reference 和当时的派生文件；最终的 `publication_manifest.json` 覆盖除自身外的整个目录，包括报告和审查记录。`validate` 同时验证 side manifests、publication manifest（存在时）和离线重算结果。

## Universe 与 hit

- pair universe：54 个 pair；round universe：每个 pair 3 轮，共 162 个 method cells。
- expected universe：145 个 ledger issue；round-level expected universe：`145 * 3 = 435`。
- `round_level_full`（报告中的 overall hit@1/FULL）：435 个 round-level expected 中 Judge 判为 `FULL` 的数量。
- `hit_at_3`：145 个 expected issue 中，三轮至少一次 `FULL` 的数量。
- `hit_at_all`：145 个 expected issue 中，三轮全部 `FULL` 的数量。
- L2 指标使用 39 个 L2 expected issue；round-level L2 分母为 117。
- `match_counts` 将 round-level non-FULL 拆为 `PARTIAL`（`supported=true`）和 `NONE`（`supported=false`）。

## K/N/I 与 cluster

Judge report 的正式 validity 字段为 `VALID_KNOWN`、`VALID_NOVEL` 和 `INVALID`。report-level precision 为：

```text
(VALID_KNOWN + VALID_NOVEL) / (VALID_KNOWN + VALID_NOVEL + INVALID)
```

cluster-level 先以 `pair_id + round + root_cause_cluster_key` 分组。一个 cluster 含 `VALID_KNOWN` 时计 `VALID_KNOWN`；不含 `VALID_KNOWN`、但含 `VALID_NOVEL` 时计 `VALID_NOVEL`；仅含 `INVALID` 时计 `INVALID`。cluster precision 使用 valid/total。`VALID_NOVEL`、ledger-unmatched report 与 `PARTIAL` 都不是 FP；本归档中 semantic FP 对应 `INVALID`。

## W 与谓词

v60 的 `full_hit_max_witness` 对每个 `FULL` expected row 取其 supporting witness 中最高的 `W2`、`W1` 或 `W0`，分母是 FULL hit 数，而非全部 finding。`w2_all_expected` 的分母为 435，二者不能互换。

`predicate_table` 按冻结 registry 的 19 个 ID 给出：

- `candidate_route_count`：带该 predicate 的 issue-candidate evidence record 数；pass-only receipt 不会增加该计数。
- `precise_binding_count`：前一类 evidence record 中 `binding.precise=true` 的数目。
- `receipt_count`：已验证 `PredicateExecutionReceipt` 数；这是 route/receipt 审计面。
- `terminal_execution_count` 与 `executed_pass`/`executed_violation`：真实 backend terminal receipt 的数量及其结果。
- `input_contract_missing`、`out_of_fragment`、`failure_kinds`：未形成 terminal W2 的结构化退化原因。
- `witness_counts`：该 predicate 支持的 W0/W1/W2 finding 数；它不是 FULL-hit max-W 分布。

19 个 registry predicate 是冻结实现全集；`planned_predicates` 是本次 full-scale-15 的 15 个计划 ID；实际使用是其中 terminal receipt 大于零的 ID 数。X1v2 不具有同构的 19 谓词 receipt schema，因此其 W 与 predicate 统计为 `not_applicable`。

## 成本和已知缺口

method 与 Judge 成本必须分开读取。`method_cost_eligible`/`judge_cost_eligible` 决定该记录成本能否视为完整可定价总额。v60 Judge 的 `judge_recorded_usd` 只是已记录成本，因 10 个应计费调用缺 usage 而 `judge_cost_eligible=false`。X1v2 的 corrected method-cost audit 与 Judge composite 都标记为 eligible。任何缺失项按 manifest 的 `known_data_gaps` 和报告说明披露，不能写成零或用推算补齐。

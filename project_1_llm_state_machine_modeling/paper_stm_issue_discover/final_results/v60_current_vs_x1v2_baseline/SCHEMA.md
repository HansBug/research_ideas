# 归档字段与指标口径

## 制品关系

`raw/<side>/method/` 与 `raw/<side>/judge/` 是从冻结运行制品复制的结构化审计面；它们不由本目录内的 reporting 工具修改。`derived/recomputed_summary.json` 是唯一的派生汇总，生成器为 `pipeline.evidence_discovery.reporting.final_results_archive`。`reference/ledger.json` 只由 evaluator 用于识别 expected issue 和 L2，不进入 method 输入。

每侧 `archive_manifest.json` 列出原始审计文件、字节数和 `sha256`，并记录 `generator`、`generation_command` 与 `generated_at_utc`。顶层 `archive_manifest.json` 覆盖 raw、reference 和派生文件；最终的 `publication_manifest.json` 覆盖除自身外的整个目录，包括报告和审查记录。`validate` 同时验证 side manifests、top-level manifest、publication manifest（存在时）、manifest/summary/provenance schema、archive-relative provenance 映射、Markdown 本地链接和离线重算结果。Markdown 链接可指向同一仓库的稳定文件，但不得回指临时 `runs/`。

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

本目录保存的是冻结 Judge v3.2 输出，不是 2026-08-29 后按 D0/A0 边界完成的全量人工真值。
现行语义要求：作者源承重事实成立后，有存活的被违反义务才是 D2/D1；事实成立但义务
不成立是 D0；事实不成立或只在派生表示中成立而归错制品是 A0。D0/A0 都应为 I，只有
D2/D1 才能按 relation 进入 K/N。因而本归档的 K/N/I 数字必须标为冻结 Judge 输出，不能
把 `VALID_NOVEL` 逐条等同于已由人确认的新缺陷。逐条复核应作为新审计层追加，不改写 raw。

追加审计有两个互补层次：[106 条 frozen I 的完整逐条复审](./reviews/11_v60_invalid_manual_reaudit.md)
给出 strict `D2/D1/D0/A0 = 5/15/10/76` 和局部 corrected `K/N/I = 8/12/86`；
[444 条 frozen N 的后置复核](./reviews/12_v60_valid_novel_posthoc_reaudit.md) 给出精确机械
归并、45 条 confirmed N→I 下界，以及未完成第二审的候选/估计范围。前者是全量人工复审，
后者不是 444 条全量最终裁决。组合敏感性必须明确假设审计集合互不重叠，不得替换
`derived/recomputed_summary.json` 的冻结指标。

## W 与谓词

W 是 finding 的证据/见证强度，而不是 19 谓词专属字段。W0 没有足够具体、可核对的模型元素或路径定位；W1 已定位 state、transition、guard、action、缺失边、模型片段或有限路径，但没有该方法产生且在精确制品上终止求值的对象；W2 还需要原方法产生的可执行对象、运行期 terminal receipt、精确 artifact hash 和 terminal result。later Judge 的事实核验不能倒灌形成 method W2。

v60 的 `full_hit_max_witness` 对每个 `FULL` expected row 取其 supporting witness 中最高的 `W2`、`W1` 或 `W0`，分母是 FULL hit 数，而非全部 finding。`w2_all_expected` 的分母为 435，二者不能互换。X1v2 的 `witness` 来自 `derived/x1v2_witness_level_audit.json`：两名独立 reviewer 对全部 512 条冻结 finding 逐条阅读原始 finding、hash-verified NL/PlantUML 和 record；其 `paper1.x1v2-witness-review-packet.v2` 审阅包不包含 Judge 路径、hash、validity、expected relation 或 ledger ID，Judge 关联只在双审后用于 evaluator 聚合。`paper1.x1v2-witness-level-audit.v3` 保留两次 review；pane5 裁决实际 W-level 分歧，或在 archive 内独立 review 明确指出共同误标时记录受 allowlist 限制的 `post_review_correction`。`derived/x1v2_full_hit_max_witness_audit.json` 只对 `expected_outcomes[].full_report_ids` 聚合，绝不以 `partial_report_ids` 抬高 FULL hit。

`predicate_table` 按冻结 registry 的 19 个 ID 给出：

- `candidate_route_count`：带该 predicate 的 issue-candidate evidence record 数；pass-only receipt 不会增加该计数。
- `precise_binding_count`：前一类 evidence record 中 `binding.precise=true` 的数目。
- `receipt_count`：已验证 `PredicateExecutionReceipt` 数；这是 route/receipt 审计面。
- `terminal_execution_count` 与 `executed_pass`/`executed_violation`：真实 backend terminal receipt 的数量及其结果。
- `input_contract_missing`、`out_of_fragment`、`failure_kinds`：未形成 terminal W2 的结构化退化原因。
- `witness_counts`：该 predicate 支持的 W0/W1/W2 finding 数；它不是 FULL-hit max-W 分布。

19 个 registry predicate 是冻结实现全集；`planned_predicates` 是本次 full-scale-15 的 15 个计划 ID；实际使用是其中 terminal receipt 大于零的 ID 数。X1v2 不具有同构的 19 谓词 receipt schema，因此其 predicate usage、pass/violation 与 terminal receipt 统计为 `not_applicable`；X1v2 的 W 仍以人工回溯审计独立报告。

## 成本和已知缺口

method 与 Judge 成本必须分开读取。`method_cost_eligible`/`judge_cost_eligible` 决定该记录成本能否视为完整可定价总额。v60 Judge 的 `judge_recorded_usd` 只是已记录成本，因 10 个应计费调用缺 usage 而 `judge_cost_eligible=false`。X1v2 的 corrected method-cost audit 与 Judge composite 都标记为 eligible。任何缺失项按 manifest 的 `known_data_gaps` 和报告说明披露，不能写成零或用推算补齐。

# Predicate gold v1 leakage/compliance 与 active-doc 审计

审计结论分成两部分：method/runtime/package 防泄漏通过；active 文档发布面未闭合，因此本轮总体为 `FAIL`。这个 `FAIL` 不涉及 canonical 数据或执行结果，只表示 pane5 在最终发布前还要补文档入口和 evaluation 边界。

## 结论

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| method source、prompt-bearing module、routing、resource 是否引用 gold | PASS | `method/**` 禁止词扫描无命中；AST import violations 为空 |
| method 包与 release 是否带入 evaluation/gold | PASS | `pyproject.toml` 只包含 `paper_stm_method*`、`utils*`；release allowlist 排除 evaluation、ledger、expected answers |
| 实际构建的 method release | PASS | 71 个 payload 文件；gold/ledger 禁止词零命中；provider/billable call 均为 0 |
| gold 与 method 的依赖方向 | PASS | 只存在 evaluation -> frozen method backend/compiler；不存在 method -> evaluation/gold |
| registry `118/145` 口径 | PASS | registry 明写 `planned_mapping_not_new_method_measurement`；13 个文档命中全是 history/provenance，active 为 0 |
| 旧 126 条 `expected_issue_set.json` | PASS | 33 个文档命中全是 history/provenance，active 为 0 |
| “145 条全部精准可执行” | PASS | 扫描命中 0 |
| canonical gold 入口 | FAIL | gold 根目录缺 README，ledger/discover 入口未链接新 overlay |
| active 导航与状态 | FAIL | 顶层 README/STATUS/SUMMARY 和 current-facing inventory 尚未登记 gold |
| evaluation 文档边界 | FAIL | 未说明 gold replay、expected-vs-actual、单向依赖与不改 hit/W/KNI 的边界 |

完整机器记录见 [leakage_docs_review_v1.json](./leakage_docs_review_v1.json)，逐文件清单见 [documentation_inventory.tsv](../../documentation_inventory.tsv)。inventory 共 414 行，其中 active 197、history 217；8 行为待修 active 文档。

## 防泄漏证据

method 的 package discovery 只包含 `paper_stm_method*` 和 `utils*`，package data 只有 `resources/*.json` 与 `release_manifest.json`。`method/release_allowlist.json` 进一步显式排除 `evaluation`、`ledger`、`expected_answers`、`baseline`、`final_results`、`runs`、`archive` 和 `legacy`。

本轮还在 `/tmp` 构建了一份 allowlisted method release。生成 manifest 的 SHA-256 为 `f05b7b57c51531936007bdcdea20d78f7f6d9eb6b67b41ef877702b97172cd10`；release 内没有 `predicate_gold`、`expected_issue_set`、`discover_matrix/ledger_v2`、`UNSUPPORTED_EXACT` 或 `gold_property`。evaluation gold runner 会调用冻结的 method backend/compiler 复放性质，这个方向是允许的；反向 import 不存在。

定向回归结果：

```text
test_method_tree_does_not_reference_gold_directory  PASS
test_current_ledger_has_no_embedded_gold_fields      PASS
2 passed in 0.16s
```

本轮读取时的关键 hash：ledger `b5a38d3d...2d0e36`，旧 126 provenance `2f5d07c2...12e1`，registry `38fa2e80...15ca`，method tree manifest `9c5e047f...a9bc`。这些路径均无工作树修改。

## 旧口径处置

`118/145` 仍可出现在两种地方：冻结 registry 的 planned snapshot，或已明确标为 historical/superseded 的运行和审查记录。它没有在 active 文档中被称为逐条执行 gold。旧 126 条只出现在 provenance、archive、历史代次或带明确历史说明的旧 protocol 语境中。

扫描没有发现任何文档宣称 145 条全部为精准、可执行 gold。这里的 PASS 只检查表述和边界，不替代 145 条语义、receipt 或 replay 的独立验收。

## Pane5 待修 active docs

| 路径 | 位置 | 必要修正 |
| --- | ---: | --- |
| `discover_matrix/ledger_v2/predicate_gold_v1/README.md` | 文件缺失 | 新建 gold 入口，链接 canonical JSON/schema/TSV、summary、receipts、review、manifest 和复算命令 |
| `discover_matrix/ledger_v2/README.md` | 5 | 将 `predicate_gold_v1.json` 标为当前 expected-property/typed-input overlay；`ledger.json` 仍是义务台账 |
| `discover_matrix/README.md` | 5 | 在职责表加入 gold 层，同时说明它不是 headline 结果源 |
| `README.md` | 21 | 增加 evaluation-only gold 导航，并明确 method/Judge 不读取 |
| `STATUS.md` | 7 | 仅在全部 gold gate 关闭后加入最终状态和 canonical 链接 |
| `SUMMARY.md` | 5 | 增加导航行，不复制状态分布数字 |
| `evaluation/README.md` | 21 | 说明 validator/replay/expected-vs-actual、单向依赖和不改 hit/W/KNI |
| `release/documentation_audit/current_facing_markdown_inventory.md` | 5 | 将 gold README/protocol/report 纳入 current/public surface |

这些修正都应发生在最终数字和 manifest hash 冻结之后，且只能改文档与发布索引，不能把 gold 接进 method/runtime/prompt/routing。

## 执行边界

本审计只新增 JSON、MD 和 TSV 三份审计产物。`method_reruns=0`、`judge_reruns=0`、`provider_experiment_calls=0`、`54x3_reruns=0`；没有修改 method、registry、prompt、routing、raw、Judge、ledger、canonical semantic decision 或现有文档。

# Predicate gold v1 leakage/compliance 与 active-doc 复审 v2

Reviewer ID: `codex:pane5-predicate-gold-v1-leakage-docs-r2`

结论：**FAIL**。method 防泄漏、冻结边界、旧口径、入口修复和最新 publication-path
过滤均已 PASS；剩余 FAIL 是缺失 gold release manifest，以及两处 active README 对
evaluation 执行边界的表述冲突。完整机器记录见
[`leakage_docs_review_v2.json`](./leakage_docs_review_v2.json)，逐文件清单见
[`documentation_inventory.tsv`](../../documentation_inventory.tsv)。

## 结果

| check | status | 结论 |
| --- | --- | --- |
| method import/read/package leakage | PASS | 50 个 method Python 文件、388 个 import 无 gold/evaluation 反向依赖；71-file method release 无 gold/ledger token |
| frozen boundary | PASS | registry、ledger、旧 126 provenance、canonical gold、method/runtime、raw、Judge 未被本审计修改 |
| registry `118/145` | PASS | active 3 处均明确是 `planned_mapping_not_new_method_measurement`，不是执行 gold；history 13 处保留原始语境 |
| 旧 126 `expected_issue_set.json` | PASS | active 3 处均明确是 provenance/not current；history 33 处不因保存原话判 FAIL |
| “145 条全部精准” | PASS | 命中 0；`145/145 已裁决`没有被写成 `145/145 exact` |
| v1 canonical/navigation FAIL | PASS | 原 DOC-04、DOC-05 已关闭；七个入口文件都能到 gold README |
| v1 evaluation 文档缺口 | PASS | replay、expected-vs-actual、单向依赖和不改 hit/W/KNI 已写明 |
| publication path collector | PASS | 最新过滤排除 rejected review path；定向合同测试 6/6 PASS |
| gold release manifest | **FAIL** | `predicate_gold_v1/manifest.json` 不存在；2 个 active 链接失效，manifest validator 无法运行 |
| evaluation 职责表述 | **FAIL** | active 摘要写“不执行 predicate/只读取制品”，后文又正确写 evaluation 执行 gold query/replay，缺少 discovery-time 限定 |

inventory 共 422 行：active 205、history 217、FAIL 6 行。active Markdown 共检查
2191 个仓库内相对链接，只有以下两个失效，目标相同：

- `discover_matrix/ledger_v2/predicate_gold_v1/README.md:25 -> manifest.json`
- `discover_matrix/ledger_v2/predicate_gold_v1/predicate_gold_report_cn.md:173 -> manifest.json`

## V1 关闭情况

| v1 check | v2 disposition | 证据 |
| --- | --- | --- |
| DOC-04 canonical gold entry | CLOSED PASS | `discover_matrix/README.md:7-13`、`ledger_v2/README.md:7-16`、gold `README.md:1-25` |
| DOC-05 navigation/status | CLOSED PASS | `README.md:19-28`、`STATUS.md:14`、`SUMMARY.md:13`、current-facing inventory `:29-32` |
| DOC-06 evaluation boundary | CLOSED PASS | `evaluation/README.md:33-48` 已补齐原要求；当前措辞冲突另记 DOC-08 |

## 剩余 FAIL

1. **PUB-02 / HIGH：publication manifest 未封存。**

   - `discover_matrix/ledger_v2/predicate_gold_v1/README.md:25`
   - `discover_matrix/ledger_v2/predicate_gold_v1/predicate_gold_report_cn.md:173-176`
   - `discover_matrix/ledger_v2/predicate_gold_v1/annotation_guide.md:145-147`
   - 缺失文件：`discover_matrix/ledger_v2/predicate_gold_v1/manifest.json`

   pane5 应使用当前已通过 rejected-path 测试的 collector 生成 manifest，显式纳入预期的
   current docs/horizontal reviews，再运行 `manifest-validate`、link scan 和 release tests。
   不能只删链接，因为 active 文档同时声称 release 已封存。

2. **DOC-08 / MEDIUM：evaluation execution scope 表述冲突。**

   - `README.md:42`：写 evaluation “只读取完成的制品”。
   - `evaluation/README.md:3`：写 evaluation “不参与 predicate 执行”。
   - `evaluation/README.md:35-37`：正确写 evaluation 执行、重放 gold query。

   前两处应限定为“不参与 discovery-time/method predicate execution”，并保留
   evaluation-only gold replay 例外、单向依赖和 gold/method 隔离。

## 机械复验

| command/check | result |
| --- | --- |
| predicate-gold canonical release validator | PASS，145 条；8/5/34/98/0 |
| 6 个 leakage/publication 定向 pytest | PASS，`6 passed in 2.50s` |
| active Markdown relative-link scan | FAIL，2191 checked / 2 missing，均为 `manifest.json` |
| gold `manifest-validate` | FAIL，`FileNotFoundError` |
| allowlisted method release scan | PASS，71 files，provider/billable 0，forbidden token 0 |

本审计没有运行 method、Judge、provider、15x1 或 54x3，也没有修改 canonical、protocol、
registry、prompt、routing、raw、Judge 或被审文档。

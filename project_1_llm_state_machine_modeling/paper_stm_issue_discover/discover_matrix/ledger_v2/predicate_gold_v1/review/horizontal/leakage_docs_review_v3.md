# Predicate gold v1 leakage/compliance closure re-review v3

Reviewer ID: `codex:pane5-predicate-gold-v1-leakage-docs-r3`

最终结论：**FAIL**。DOC-08、manifest 缺失、两个失效链接、rejected-path、旧口径和
method/package leakage 均已关闭为 PASS；唯一剩余项是 manifest 在本轮要求的 inventory
刷新之前封存，导致写后恰有一个 hash 失配。机器记录见
[`leakage_docs_review_v3.json`](./leakage_docs_review_v3.json)，逐文件清单见
[`documentation_inventory.tsv`](../../documentation_inventory.tsv)。

## Closure

| v2 finding | v3 status | 证据 |
| --- | --- | --- |
| DOC-08 evaluation 职责冲突 | CLOSED PASS | `README.md:42`、`evaluation/README.md:3,35-37` 已区分 headline evaluation、discovery-time method execution 与 evaluation-only gold replay |
| PUB-02 manifest 缺失 | CLOSED PASS | `predicate_gold_v1/manifest.json` 已存在，1623 个条目 |
| PUB-02 active broken links | CLOSED PASS | 205 个 active 文件、2192 个仓库内相对链接、missing 0 |
| PUB-02 final manifest hash closure | **FAIL** | 00:55Z manifest 绑定 closure 前 inventory hash；最终 disposition 刷新后只剩该文件 1 个 mismatch |

`README.md:42` 与 `evaluation/README.md:3` 的修正没有改变依赖方向：method/Judge 仍不
import evaluation，gold 仍只允许 evaluation -> frozen backend，不参与 discovery-time method
predicate execution，也不改 hit、W 或 K/N/I。

## 唯一 FAIL

`discover_matrix/ledger_v2/predicate_gold_v1/manifest.json` 中绑定：

- JSON pointer：`/files/<repository_path=.../predicate_gold_v1/documentation_inventory.tsv>/sha256`
- manifest expected：`sha256:01917ff3f4f13545ab9d2052b041f6be994622d3a4482b75bf12ead1104abe18`
- refreshed inventory actual：`sha256:9a7002ed233037d799294b8effc50248e16361e7e90ae32f057a878d9bacf055`

用户指定的 00:55Z manifest（payload `af335...`）对 `01917...` inventory 的
1623/1623 hash 全部通过；最终 closure disposition 写入后独立遍历为 1622/1623，
唯一 mismatch 就是本任务要求刷新的 inventory。pane5 需要在 inventory 最终化后重新生成
`manifest.json` 并运行 `manifest-validate`。若 closure review 也需要纳入发布证据，宜将其作为
detached post-seal attestation，避免“review 哈希 manifest、manifest 又哈希 review”的循环。

## 其余检查

| check | status | result |
| --- | --- | --- |
| release collector rejected-path exclusion | PASS | manifest rejected-path 0；定向合同测试通过 |
| targeted leakage/publication pytest | PASS | `6 passed in 2.50s` |
| active Markdown links | PASS | 2192 checked / 0 missing |
| registry `118/145` | PASS | active 3 处均明确是 planned snapshot；history 13 |
| old 126 `expected_issue_set.json` | PASS | active 3 处均明确是 provenance/not current；history 33 |
| 145-all-exact overclaim | PASS | 0 |
| method textual/import leakage | PASS | forbidden token 0；50 Python files / 388 imports / violations 0 |
| materialized method release | PASS | 71 files；provider/billable 0；gold/ledger token 0 |
| canonical validator | PASS | 145/145；8/5/34/98/0 未变 |

inventory 共 422 行：active 205、history 217、FAIL 1 行。该 FAIL 指向 manifest 的封存
顺序，不指向任何 canonical decision 或 active 文档内容。

本审计没有运行 method、Judge、provider、15x1 或 54x3，也没有修改 canonical、protocol、
method/runtime、registry、prompt、routing、raw、Judge 或被审文档。

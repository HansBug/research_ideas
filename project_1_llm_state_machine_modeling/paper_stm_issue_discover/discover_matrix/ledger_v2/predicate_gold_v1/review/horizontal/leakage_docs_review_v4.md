# Predicate gold v1 detached post-seal attestation v4

Reviewer ID: `codex:pane5-predicate-gold-v1-leakage-docs-r4`

最终结论：**PASS**。本文件与对应 JSON 是 detached post-seal attestation，刻意不进入
它所验证的 `manifest.json`。封存 manifest 的 payload SHA-256 为
`d883d9d3f5259a396df47db1b9d345856da2a26465380d9fc24a5eacd8f5f542`，文件 SHA-256 为
`f7024d6a8d03c7f83704ae8ab6c82a66938f406422beea2dea56c3943ad869c4`。

## 封存闭合

| check | status | evidence |
| --- | --- | --- |
| manifest payload | PASS | 独立 canonical JSON hash 与 `manifest_sha256` 一致 |
| manifest paths/hashes | PASS | 1625 条，路径唯一且排序；`manifest-validate` 为 1625/1625 |
| v3 + inventory 封存 | PASS | v3 JSON/MD 两条、inventory 一条，当前 bytes 与 manifest hash 一致 |
| detached 边界 | PASS | manifest 中 v4 路径为 0；v4 不参与被审 digest |
| rejected-path exclusion | PASS | collector 1587 条唯一 current path、rejected 0；manifest rejected 0 |

被封存的前置证据哈希：

- `documentation_inventory.tsv`: `9a7002ed233037d799294b8effc50248e16361e7e90ae32f057a878d9bacf055`
- `leakage_docs_review_v3.json`: `f98401bc0021f9aad8095bebb3d3fe5bccf41c4cd1f53ee1fe11e6ec80f63dd1`
- `leakage_docs_review_v3.md`: `f786358854838e790986ecd3d3503b7e805f07c92a48438ea904c43e2c4e9a1e`

v3 与 inventory 保留的是封存前检查结论；v4 作为封存后的独立证明关闭该时序问题，
不回写或覆盖历史审计记录。

## Receipt-bound evaluator

| file | status | SHA-256 |
| --- | --- | --- |
| `predicate_gold_execution.py` | PASS | `6bfc31798f2c110d6941bc81dbd62a113c889978a9a646ee8c3b79b1ee8ae6de` |
| `predicate_gold_relation_oracle.py` | PASS | `ec905fcc5e1ed696e2c840fdb37fcee2032065c2a52ae8bff4bb83b8c43aadb0` |
| `predicate_gold_static_oracle.py` | PASS | `d0c447664c7315ce8790bc9ceeac8e3c4831972bc048ae7b3b67293b7e5f7c10` |
| `predicate_gold_native_contract.py` | PASS | `2b2903f4715964b60d8c01416435fcc6bd3faf13e50bfce17c106c6468fdda8b` |

四个文件的当前 bytes、manifest 条目和 canonical/receipt source binding 一致。独立遍历
145 条 canonical record 的 10300 个 source ref、1042 个唯一 path/hash binding，missing 0、
mismatch 0。

## 文档与防泄漏

| check | status | result |
| --- | --- | --- |
| active Markdown links | PASS | 205 个 active inventory 文件中 185 个 Markdown；2192 个相对链接，missing 0 |
| registry `118/145` | PASS | active 3 处均明确为 `planned_mapping_not_new_method_measurement`，不是 executed gold coverage |
| old 126 | PASS | active 3 处均明确为 provenance/history，不是当前 ledger 或 gold |
| all-145-exact | PASS | 0 个明确过度声明；当前口径为 exact 13、proxy 34、unsupported 98 |
| method textual leakage | PASS | forbidden-token 文件 0 |
| method import leakage | PASS | 50 个 Python 文件、388 个 import，违规 0 |
| method package leakage | PASS | package discovery 仅 `paper_stm_method*`/`utils*`；allowlist 排除 evaluation、ledger、expected answers、Judge 和 results |

旧口径证据位于 `discover_matrix/ledger_v2/README.md:16`、
`predicate_gold_v1/CHANGELOG.md:16-18`、`predicate_gold_v1/README.md:34-36` 和
任务根 `README.md:19`。method/package 边界位于 `method/pyproject.toml:28-36`、
`method/release_allowlist.json:160-172` 与 `scripts/release/build_method_release.py:162-181`。

## Validator

| validator | status | result |
| --- | --- | --- |
| publication manifest | PASS | 1625 files |
| canonical release | PASS | 145/145；8 EXACT、5 COMPOSITE、34 PROXY、98 UNSUPPORTED、0 BLOCKED |
| source evidence | PASS | 10300 refs；missing 0；mismatch 0 |
| frozen boundary | PASS | registry、ledger、old-126 provenance 和 canonical gold 哈希未变 |

本次仅执行 provider-free 的读取、hash、链接、AST、collector 和 validator 检查；没有运行
method、Judge、provider、15x1 或 54x3，也没有修改 manifest、inventory、canonical、protocol、
method/runtime、registry、prompt、routing、raw 或 Judge 制品。

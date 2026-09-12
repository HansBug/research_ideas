# Predicate gold v1

本目录是当前 145 条 `ledger_v2` issue 的 evaluation-only expected-predicate gold。唯一
canonical 事实源是 [`predicate_gold_v1.json`](predicate_gold_v1.json)；表格、报告和
unsupported 清单均由 provider-free 生成器从该 JSON 机械导出。

当前裁决为：精准可执行 13/145，其中 `EXACT_FALSE=8`、
`COMPOSITE_EXACT_FALSE=5`；
`SOUND_FALSE_PROXY=34`；
`UNSUPPORTED_EXACT=98`；
`BLOCKED_EXECUTION=0`。精准与 proxy
执行共 47 条，坏制品 `false`、positive control `true`、replay match
均为 47/47。

## 当前入口

- [中文审计报告](predicate_gold_report_cn.md)
- [canonical JSON](predicate_gold_v1.json) / [JSON Schema](predicate_gold_v1.schema.json) / [TSV 镜像](predicate_gold_v1.tsv)
- [状态与交叉分布](summary.json)
- [98 条 unsupported 清单](unsupported_exact.md) / [JSON](unsupported_exact.json) / [TSV](unsupported_exact.tsv)
- [冻结 v60 expected-vs-actual 离线分析](expected_vs_actual_v60.json) / [TSV](expected_vs_actual_v60.tsv)
- [精准性协议](predicate_gold_protocol.md) / [标注指南](annotation_guide.md)
- [19 谓词能力审计](predicate_semantics_capability_audit.md) / [JSON](predicate_semantics_capability_audit.json)
- [claim-to-source matrix](academic_claim_to_source_matrix.json) / [学术横向复核](review/horizontal/academic_review_v2.md)
- [当前 review 选择](review/active_review_manifest.json) / [发布 manifest](manifest.json)
- [变更说明](CHANGELOG.md)

## 边界

这里的 `exact` 指在声明的 FCSTM 语义、scope 和环境假设下，项目逐条确认
`O <=> P`，并不表示存在统一的 `S < G < R < V` 精准度排序。`O => P` 只计
sound falsifier/proxy；`P => O` 和无可证明蕴含不计 exact。

旧 registry 的 `118/145 = 81.4%` 是冻结的
`planned_mapping_not_new_method_measurement` 设计期汇总，不是逐条执行验证过的 gold coverage。
旧 126 条 `provenance/expected_issue_set.json` 只保留作来源证据，不能替代当前 145 条台账或本 overlay。

gold 不改变 hit、W、K/N/I，也不要求 method 复现同一个 predicate ID。它没有进入 method
registry、prompt、routing 或 package data。本次没有运行 method、Judge、provider、15x1 或 54x3。

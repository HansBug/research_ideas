# fixtures/ — 人类可读 issue lifecycle fixture 说明

本目录只保存 synthetic micro-fixture 的人类可读说明。机器可校验版本位于 [../../../pipeline/evaluation/fixtures/source_issue_ledger/](../../../../../pipeline/evaluation/fixtures/source_issue_ledger/)。

## fixture 列表

| fixture | 覆盖分支 | machine JSON |
|---|---|---|
| [expression_debt_folded_event](./expression_debt_folded_event/README.md) | folded event / expression debt 只能 candidate。 | [JSON](../../../../../pipeline/evaluation/fixtures/source_issue_ledger/expression_debt_folded_event.json) |
| [confirmed_guard_mismatch](./confirmed_guard_mismatch/README.md) | NL-grounded confirmed guard mismatch。 | [JSON](../../../../../pipeline/evaluation/fixtures/source_issue_ledger/confirmed_guard_mismatch.json) |
| [raw_internal_inconsistency_confirmed](./raw_internal_inconsistency_confirmed/README.md) | raw-internal inconsistency 第二 confirmed path。 | [JSON](../../../../../pipeline/evaluation/fixtures/source_issue_ledger/raw_internal_inconsistency_confirmed.json) |
| [conversion_artifact_rejected](./conversion_artifact_rejected/README.md) | conversion artifact rejected。 | [JSON](../../../../../pipeline/evaluation/fixtures/source_issue_ledger/conversion_artifact_rejected.json) |
| [out_of_scope_timed_case](./out_of_scope_timed_case/README.md) | timed-like out-of-scope。 | [JSON](../../../../../pipeline/evaluation/fixtures/source_issue_ledger/out_of_scope_timed_case.json) |
| [insufficient_evidence_candidate](./insufficient_evidence_candidate/README.md) | vague NL / insufficient evidence。 | [JSON](../../../../../pipeline/evaluation/fixtures/source_issue_ledger/insufficient_evidence_candidate.json) |

## 维护规则

- JSON 是事实源；本目录 README 不覆盖 JSON verdict。
- fixture 是合同校准，不是真实实验结果。
- 不要把 synthetic fixture 写成 method effectiveness evidence。

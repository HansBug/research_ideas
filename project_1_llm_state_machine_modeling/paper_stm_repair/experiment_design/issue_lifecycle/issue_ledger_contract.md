# Issue ledger contract v0

## 1. 合同对象

`source_issue_ledger.schema.json` 约束的是一个 case-level issue ledger。每个 ledger 对应一个 `NL + raw/source STM_0` case 或一个 synthetic contract fixture。

## 2. machine-verifiable 事实源

机器事实源位于：

- schema：[../../pipeline/evaluation/schemas/source_issue_ledger.schema.json](../../pipeline/evaluation/schemas/source_issue_ledger.schema.json)
- fixtures：[../../pipeline/evaluation/fixtures/source_issue_ledger/](../../pipeline/evaluation/fixtures/source_issue_ledger/)
- tests：[../../pipeline/evaluation/tests/test_source_issue_ledger_schema.py](../../pipeline/evaluation/tests/test_source_issue_ledger_schema.py)

本目录只解释合同语义，不替代 JSON / pytest。

## 3. 关键字段

| 字段 | 含义 |
|---|---|
| `ledger_id` | ledger 稳定 ID。 |
| `case_id` | case 或 synthetic fixture ID。 |
| `ledger_scope` | `contract_fixture` / `pilot_candidate` / `formal_experiment_candidate` 等范围。 |
| `issue_id` | 后续 repair runner 必须绑定的最小对象。 |
| `confirmation_status` | issue 当前状态。 |
| `confirmation_evidence_path` | confirmed issue 的证据路径；非 confirmed 默认 `not_applicable`。 |
| `source_element_refs` | raw/source 元素引用；具体 trace schema 留给 `PR-source-trace`。 |
| `nl_evidence` | NL 证据。raw-internal path 可为空，但必须有 rationale。 |
| `source_stm_evidence` | raw/source STM 证据。 |
| `behavior_evidence` | typed behavior evidence reference，不嵌入完整 run record。 |
| `attribution_boundary` | 区分 source-level issue 与 conversion / representation artifact。 |
| `downstream_repair_allowed` | 后续 repair runner 的 gate。 |

## 4. repair eligibility gate

只有满足以下条件的 issue 才能进入后续 repair：

```text
confirmation_status == confirmed
and downstream_repair_allowed == true
and attribution_boundary.source_level_claim_allowed == true
```

非 confirmed 状态必须 `downstream_repair_allowed=false` 且 `confirmation_evidence_path=not_applicable`；反向地，`downstream_repair_allowed=true` 必须推出 `confirmation_status=confirmed`。

## 5. 后续 PR 不得绕过的规则

1. `PR-discover-confirm` 不能把 candidate 直接当 confirmed；folded event / expression debt 默认只能 candidate，除非后续被重分类为具体 source-level behavioral issue。
2. `PR-repair-runner` 不能修没有 `confirmed issue_id` 的泛化目标。
3. `PR-raw-export` 必须能把 change / patch 回指到 issue。
4. `PR-closure-audit` 必须保留 closed / partial / not closed / regression / unjudgeable，而不能删除失败项。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-08 09:52:31 | 初始化 issue ledger 字段语义与 repair eligibility gate。 |

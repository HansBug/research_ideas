# Issue ledger contract v0

## 1. 合同对象

`source_issue_ledger.schema.json` 约束的是一个 case-level issue ledger。每个 ledger 对应一个 `NL + raw/source STM_0` case 或一个 synthetic contract fixture。

## 2. machine-verifiable 事实源

机器事实源位于：

- schema：[../../pipeline/evaluation/schemas/source_issue_ledger.schema.json](../../../../pipeline/evaluation/schemas/source_issue_ledger.schema.json)
- fixtures：[../../pipeline/evaluation/fixtures/source_issue_ledger/](../../../../pipeline/evaluation/fixtures/source_issue_ledger/)
- tests：[../../pipeline/evaluation/tests/test_source_issue_ledger_schema.py](../../../../pipeline/evaluation/tests/test_source_issue_ledger_schema.py)

本目录只解释合同语义，不替代 JSON / pytest。

## 3. 关键字段

| 字段 | 含义 |
|---|---|
| `ledger_id` | ledger 稳定 ID。 |
| `case_id` | case 或 synthetic fixture ID。 |
| `ledger_scope` | `contract_fixture` / `pilot_candidate` / `formal_experiment_candidate` 等范围。 |
| `issue_id` | 后续 repair runner 必须绑定的最小对象。 |
| `confirmation_status` | issue 当前状态。 |
| `confirmation_evidence_path` | confirmed issue 的证据路径；非 confirmed 默认 `not_applicable`。`nl_grounded_behavioral_issue` 必须有 NL/source/typed behavior 三类强证据，`raw_internal_inconsistency` 必须保持 `nl_evidence=[]`。 |
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

## 5. 后续阶段不得绕过的规则

1. Discover 不能把 candidate 直接当 confirmed；folded event / expression debt 默认只能 candidate，除非同一 Discover assessment 有足够 source-level behavior evidence 支撑重分类。
2. Repair 不能对没有 `confirmed issue_id` 的泛化目标执行 `fix`；对不可 fix 的 pending root 必须给出可审计 reject 理由。
3. Confirm 只审查本轮 disposition 与已发布模型；不能回 Discover、修改旧记录或把 B-confirm accept 直接当 source closure。
4. canonical source export 必须能把每个 exported semantic root 与 accepted change 回指到 issue chain 和 disposition；不允许从裸 `.fcstm` 反推或用 textual minimal patch 替代 correspondence ledger。
5. C closure audit 必须保留 closed / partial / not closed / regression / unjudgeable，而不能删除失败项。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-17 00:32:36 | 将旧 PR slug 规则改为 Discover/Repair/Confirm/C 阶段合同，保留 v0 repair eligibility gate。 |
| 2026-07-08 09:52:31 | 初始化 issue ledger 字段语义与 repair eligibility gate。 |

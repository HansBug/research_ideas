# source_trace/GUIDE.md — source trace 合同维护规范

> 本 GUIDE 维护的是 legacy `source_trace.v0` synthetic fixtures。Issue #161 后 active PlantUML working bundle 的 identity trace 由 [R4.5 representation contract](../../pipeline/representation/README.md) 约束；两者同名的 `projection_status` 不得跨合同解释。active identity trace 不授权 Repair、final export 或 closure。

## 1. 默认阅读顺序

处理 source trace 相关任务时，默认按以下顺序阅读：

1. [../issue_lifecycle/README.md](../issue_lifecycle/README.md)：确认 #150 source issue ledger 的 status / evidence gate。
2. [README.md](./README.md)：确认 source trace 的职责边界。
3. [source_trace_contract.md](./source_trace_contract.md)：确认 v0 字段、relation 与 attribution gate。
4. [fixtures/README.md](./fixtures/README.md)：理解六类 synthetic contract fixture。
5. [../../pipeline/evaluation/schemas/source_trace.schema.json](../../pipeline/evaluation/schemas/source_trace.schema.json) 与 [../../pipeline/evaluation/tests/test_source_trace_schema.py](../../pipeline/evaluation/tests/test_source_trace_schema.py)：确认机器合同与 tests。

## 2. 核心纪律

source trace 只回答“raw/source 元素和中间表示元素之间是否可追踪、可投影、可支撑后续 closure claim”，不回答“模型是不是更好”。

后续 agent 必须遵守：

1. confirmed + repair-eligible issue 必须能通过 source trace 找到至少一个 `projectable` 或 `partially_projectable` trace entry。
2. `ambiguous` / `untraceable` / `conversion_artifact` trace 不能绑定 confirmed + repair-eligible issue 作为 source-level closure 主证据。
3. `conversion_artifact` trace relation 与 #150 `rejected_conversion_artifact` issue status 分层：前者描述 trace 关系，后者描述 issue confirmation 结果。
4. `normalized` 必须有 normalization evidence；否则不能称为语义保持的 trace。
5. `split` 必须记录 `projection_detail`，且默认 `closure_claim_allowed=false`。
6. v0 不允许 `merged` / `inferred`；如后续真实 pilot 需要，必须另开 PR 同步 schema、fixture、tests、report 和 source trace contract。

## 3. 与 #150 issue ledger 的连接

本 PR v0 **不修改** [../../pipeline/evaluation/schemas/source_issue_ledger.schema.json](../../pipeline/evaluation/schemas/source_issue_ledger.schema.json)。trace ledger 通过：

```text
trace_entries[].required_for_issue_ids[]
```

指向 #150 issue id。后续 consumer 应构造确定性 reverse index：

```text
issue_id -> trace_id[]
```

该 reverse index 是 v0 的 issue-to-trace 机器连接方式。若后续发现需要在 issue ledger 内增加 `trace_entry_ids[]`，必须作为单独 schema migration PR 处理，不能在消费端临时脑补。

注意：JSON Schema 无法直接读取 #150 issue ledger status，因此 `issue_binding_policy` 是 schema 层的第一道保护；pytest 与后续 consumer 必须复制 `issue_id -> trace_id[]` reverse index 检查，确保 `candidate_or_rejected_only` / `no_issue_binding` 不绑定 confirmed repair-eligible issue。

## 4. relation 与 attribution gate

| trace_relation | projection_status | source-level claim | closure claim | 说明 |
|---|---|---|---|---|
| `exact` | `projectable` | allowed | required allowed | 一一对应，必须 `closure_claim_allowed=true`，可作为后续 closure 证据候选。 |
| `normalized` | `projectable` | allowed | required allowed | 仅限有 normalization report 的语义保持规范化，必须 `closure_claim_allowed=true`。 |
| `split` | `partially_projectable` | allowed | not allowed by itself | 可定位 issue，但不能单独证明 full closure。 |
| `ambiguous` | `unprojectable` | not allowed | not allowed | 多个 source candidate 无法唯一对齐。 |
| `untraceable` | `unprojectable` | not allowed | not allowed | 中间元素无可靠 source origin。 |
| `conversion_artifact` | `not_applicable` | not allowed | not allowed | conversion / lowering / normalization artifact，不是 source-level issue repair gain。 |

## 5. 测试纪律

新增或修改 source trace schema / fixture 后，必须至少运行：

```bash
python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests/test_source_trace_schema.py -q
```

若改动 evaluation 目录，建议运行：

```bash
python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests -q
```

若改动跨 pipeline 合同，建议运行组合 smoke：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m pytest \
  project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/tests \
  project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/tests \
  project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/tests \
  project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests -q
```

## 6. Review gate

reviewer 至少检查：

1. source trace 是否回到 #150 issue ledger，而不是重新定义 issue lifecycle。
2. `required_for_issue_ids[]` 是否都能在 source issue ledger fixtures 中找到。
3. confirmed + repair-eligible issue 是否都有 positive trace coverage。
4. negative trace relation 是否被禁止进入 source-level closure 主证据。
5. 文档是否又把 trace / ledger / audit 写成 headline contribution。
6. 是否把四个 selected examples 或 archived R5.7 constructed examples 写成本 PR 必跑对象。

## 7. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-20 14:06:13 | 标明 v0 与 active `source_trace_base.v1` 的合同边界，禁止把 identity localization 误作 raw projection/closure 能力。 |
| 2026-07-08 14:03:59 | `PR-source-trace` 新增 source trace 维护规范，固定 v0 relation、reverse index 与 negative attribution gate。 |

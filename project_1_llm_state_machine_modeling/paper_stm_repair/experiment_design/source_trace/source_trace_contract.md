# Source Trace Contract v0

## 1. 合同目标

Source Trace Contract v0 定义 raw/source STM 元素与中间可执行语义表示元素之间的最小追踪记录。它服务于后续：

```text
confirmed issue -> issue-grounded repair -> raw/source projection -> closure / regression audit
```

它不定义 final metric、不定义 baseline、不运行 LLM、不证明 method effectiveness。

## 2. 顶层 ledger

Machine schema 位于 [../../pipeline/evaluation/schemas/source_trace.schema.json](../../pipeline/evaluation/schemas/source_trace.schema.json)。顶层字段：

| 字段 | 含义 |
|---|---|
| `schema_version` | 固定为 `source_trace.v0`。 |
| `trace_ledger_id` | trace ledger 唯一 id。 |
| `case_id` | 与 source issue ledger / future run record 对齐的 case id。 |
| `source_model_id` | raw/source STM id。 |
| `intermediate_model_id` | 中间表示模型 id。 |
| `trace_scope` | `contract_fixture` / `pilot_candidate` / `formal_experiment_candidate`。 |
| `trace_entries[]` | 具体 trace entries。 |
| `notes` | 人类可读限制说明。 |

## 3. trace entry 字段

| 字段 | 含义 |
|---|---|
| `trace_id` | trace entry 唯一 id。 |
| `source_elements[]` | raw/source 元素引用，可为空，仅 `untraceable` 允许空。 |
| `intermediate_elements[]` | 中间表示元素引用。 |
| `trace_relation` | v0 relation，见 §4。 |
| `projection_status` | 是否可投影回 raw/source，见 §5。 |
| `required_for_issue_ids[]` | 该 trace 支撑或关联的 #150 issue id。 |
| `issue_binding_policy` | v0 对 `required_for_issue_ids[]` 的机器可读解释：`confirmed_repair_eligible_allowed` / `candidate_or_rejected_only` / `no_issue_binding`。 |
| `attribution_boundary` | source-level claim / closure claim gate。 |
| `trace_relation_rationale` | 为什么选择该 relation。 |
| `projection_detail` | 仅 `split` 必需；说明 partial projection。 |
| `trace_evidence[]` | source fragment / normalization / conversion / negative trace 等证据。 |
| `reviewer_notes` | 人类审查说明。 |

## 4. trace relation

v0 只允许六类：

| relation | 含义 | 是否可支持 closure 主证据 |
|---|---|---|
| `exact` | source 元素与 intermediate 元素一一对应。 | 可以，仍需后续 repair/change 与 closure evidence。 |
| `normalized` | source 表达被语义保持地规范化。 | 可以，但必须有 `normalization_report`。 |
| `split` | source 元素被拆成多个 intermediate 元素。 | 不单独支持 full closure；只能支持 partial localization。 |
| `ambiguous` | intermediate 元素有多个可能 source origin。 | 不可以。 |
| `untraceable` | intermediate 元素找不到 source origin。 | 不可以。 |
| `conversion_artifact` | trace discrepancy 来自 conversion / lowering / normalization。 | 不可以。 |

v0 明确不支持 `merged` / `inferred`。原因是它们在没有真实 pilot 样例和负例 gate 前容易把弱推断包装成 source-level repair gain。若未来需要，必须单独扩展 schema、fixture、tests 和本合同。

## 5. projection status

| projection_status | 含义 | v0 使用规则 |
|---|---|---|
| `projectable` | 可以投影回 raw/source。 | 只允许 `exact` / `normalized`。 |
| `partially_projectable` | 有部分 source-level behavior 可投影，但不完整。 | v0 用于 `split`；默认不能支撑 full `closed`。 |
| `unprojectable` | 不能可靠投影。 | 用于 `ambiguous` / `untraceable`。 |
| `not_applicable` | 投影问题不适用。 | v0 用于 `conversion_artifact`。 |

`partially_projectable` 是一个保守状态。它可帮助定位 issue，但后续 closure audit 只能把它作为 partial / candidate evidence；full closure 必须另有 raw/source patch evidence 与 post-repair rediscovery 证据。

## 6. attribution boundary

`attribution_boundary` 必须包含：

| 字段 | 含义 |
|---|---|
| `source_level_claim_allowed` | 该 trace 是否可支撑 source-level issue claim。 |
| `conversion_or_lowering_related` | 该 trace 是否涉及 conversion / lowering artifact。 |
| `representation_related` | 该 trace 是否涉及中间表示相关归因。 |
| `closure_claim_allowed` | 该 trace 是否可进入后续 closure / repair-gain 主证据。 |
| `rationale` | 归因理由。 |

v0 hard gate：

1. `ambiguous` / `untraceable` / `conversion_artifact` 必须 `source_level_claim_allowed=false` 且 `closure_claim_allowed=false`。
2. `conversion_artifact` 必须 `conversion_or_lowering_related=true`。
3. `split` 可以 `source_level_claim_allowed=true`，但必须 `closure_claim_allowed=false`。
4. `exact` / `normalized` 必须 `closure_claim_allowed=true`，表示它们可进入后续 closure 主证据候选；但这仍不等于最终 closure，最终 closure 要等 repair/change 与 post-repair audit。

## 7. 与 source issue ledger 的连接

#150 issue ledger 已定义：

- [../issue_lifecycle/issue_ledger_contract.md](../issue_lifecycle/issue_ledger_contract.md)
- [../../pipeline/evaluation/schemas/source_issue_ledger.schema.json](../../pipeline/evaluation/schemas/source_issue_ledger.schema.json)

本 PR v0 不修改 source issue ledger schema。连接方式为：

```text
trace_entries[].required_for_issue_ids[] -> source_issue_ledger.issues[].issue_id
```

后续 consumer 必须通过扫描 trace ledger 构造 deterministic reverse index：

```text
issue_id -> trace_id[]
```

Cross-ledger tests 与后续 consumer 必须验证：

1. 所有 `required_for_issue_ids[]` 都能在 source issue ledger fixtures 中找到。
2. confirmed + repair-eligible issue 均有 positive trace coverage。
3. negative trace relation 不绑定 confirmed + repair-eligible issue。
4. `issue_binding_policy` 与实际 issue status 一致：positive relation 才能绑定 confirmed repair-eligible issue；negative relation 只能绑定 candidate / rejected issue 或不绑定。

## 8. issue binding policy

`issue_binding_policy` 是 schema 层可检查的 v0 保护字段，用来弥补 JSON Schema 无法直接读取 #150 issue ledger status 的限制。

| policy | 允许的 issue 绑定 | v0 relation |
|---|---|---|
| `confirmed_repair_eligible_allowed` | 可绑定 confirmed + repair-eligible issue。 | `exact` / `normalized` / `split` |
| `candidate_or_rejected_only` | 只能绑定 candidate / rejected / out-of-scope / insufficient-evidence issue，不能绑定 confirmed + repair-eligible issue。 | `ambiguous` / `conversion_artifact` |
| `no_issue_binding` | 不允许绑定任何 issue id。 | `untraceable` |

Schema 会锁定 relation 与 policy 的组合；pytest / future consumer 再通过 reverse index 检查实际 issue status。换言之，跨 ledger 语义不只停留在 fixture 测试里，后续消费端也必须复制等价检查。

## 9. `conversion_artifact` 分层说明

`trace_relation=conversion_artifact` 与 #150 的 `confirmation_status=rejected_conversion_artifact` 不是同一个字段：

| 层次 | 字段 | 含义 |
|---|---|---|
| issue ledger | `confirmation_status=rejected_conversion_artifact` | 这个 candidate issue 本身被判定为 conversion artifact，不是 source-level issue。 |
| source trace | `trace_relation=conversion_artifact` | 这个 trace discrepancy 来自 conversion / lowering / normalization。 |

如果一个 confirmed issue 的所有 source refs 只能通过 `conversion_artifact` trace 到达，则该 issue 不能作为 confirmed repair-eligible issue 进入主链路，应降级、排除或等待人工复核。

## 10. Contract fixtures

v0 synthetic fixtures 位于 [../../pipeline/evaluation/fixtures/source_trace/](../../pipeline/evaluation/fixtures/source_trace/)：

| fixture | relation | 覆盖点 |
|---|---|---|
| `exact_transition_trace.json` | `exact` | `ISSUE.GUARD.001` / `T_move` 的一一对应 trace。 |
| `normalized_guard_trace.json` | `normalized` | guard normalization + mandatory normalization evidence。 |
| `split_transition_trace.json` | `split` | `ISSUE.INTERNAL.001` 的 partial projection 与 `projection_detail`。 |
| `ambiguous_trace.json` | `ambiguous` | 多 source origin，不能 closure claim。 |
| `untraceable_element.json` | `untraceable` | 中间元素无 source origin。 |
| `conversion_artifact_trace.json` | `conversion_artifact` | conversion artifact trace 只关联 rejected issue。 |

## 11. 非目标

- 不跑真实 LLM。
- 不跑真实 repair loop。
- 不跑 #119 / R2 四个 selected examples。
- 不跑 archived R5.7 constructed examples。
- 不定义 final metric / baseline / judge prompt。
- 不实现 full round-trip converter。
- 不声称 trace success 等于 method success。

## 12. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-08 14:03:59 | 定义 Source Trace Contract v0，收紧 plan review 指出的 `merged/inferred`、reverse index、negative attribution、conversion artifact 和 partial projection 风险。 |

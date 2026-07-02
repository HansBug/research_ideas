# Repair target taxonomy v0（R5.7.2）

> **定位**：本文件冻结 R5.7.2 的修复目标分类合同，供后续 R5.7.4 dry-run、R5.7.5 handoff、R6 repair loop 与 R7/R8 结果分析继承。它不确认任何具体 pair 已经存在缺陷，不运行修复，也不报告效果。
>
> **核心纪律**：只来自 conversion / lowering / loss ledger 的现象一律先是 `candidate-only` 或 `representation caveat`；只有回到 `NL + raw STM_0 + canonical STM_0 + evidence bundle` 后，才可能升级为 confirmed repair target。

## 1. 五层裁决链

每个候选修复目标必须经过以下五层，不能从表示症状直接跳到 confirmed defect：

```text
表示症状 -> 候选语义问题 -> 确认修复目标 -> 允许修复动作 -> Better STM 证据影响
```

| 层级 | 问题 | 证据要求 | 输出 |
|---|---|---|---|
| 表示症状 | canonical / `.fcstm` / loss ledger 中看到了什么？ | conversion ledger、raw/canonical diff、parser/inspect diagnostics。 | representation symptom。 |
| 候选语义问题 | 该症状是否可能影响 state / event / guard / action / hierarchy / traceability？ | `NL`、raw `STM_0` 标签、source syntax、lexical cue。 | candidate semantic issue。 |
| 确认修复目标 | 是否有足够证据说明它需要 repair loop 修改？ | NL-grounded adjudication、场景、诊断、人工/LLM rubric。 | confirmed target / monitor / not target。 |
| 允许修复动作 | repair loop 能做什么，不能做什么？ | `repair_action_allowed` 五级单值枚举。 | 单个实例只能取 `must_fix`、`should_fix`、`monitor`、`not_repair_target`、`out_of_scope` 之一。 |
| Better STM 证据影响 | 修复后如何影响 Better gate？ | change ledger、no-regression、semantic gate。 | positive / negative / caveat evidence。 |

## 2. 字段合同

每条 taxonomy entry 至少包含以下 11 个字段，继承 [../scope/r5_6_to_r5_7_handoff_constraints.md](../scope/r5_6_to_r5_7_handoff_constraints.md) §3 的硬约束。

| 字段 | 取值 / 写法 | 用途 |
|---|---|---|
| `target_id` | 稳定 ASCII ID。 | R6 prompt、R7 ledger、报告引用。 |
| `semantic_element` | `state` / `transition` / `event_trigger` / `guard_condition` / `action_effect` / `hierarchy_pseudostate` / `traceability` / `scenario_behavior` / `temporal_cue` / `representation_artifact` / `out_of_scope_family`。 | 锁定语义层。 |
| `scope_status` | `main` / `caveat` / `supplementary_stress` / `excluded`。 | 与 T0/T0.5/T1 主张边界对齐。 |
| `time_level` | `T0` / `T0.5` / `T1+`。 | 防止 T0.5/T1 混入 headline。 |
| `structure_family` | FSM / HSM / discrete statechart subset / EFSM-lite-candidate / excluded family。 | 防止 arbitrary UML / timed automata 外推。 |
| `nl_evidence_required` | yes / no / conditional。 | 防止凭空新增语义。 |
| `representation_evidence_required` | raw `STM_0` / canonical / `.fcstm` / loss ledger / change ledger。 | 防止 attribution laundering。 |
| `repair_action_allowed` | `must_fix` / `should_fix` / `monitor` / `not_repair_target` / `out_of_scope` 中**且只能取一个值**。 | 单个 target instance 的修复动作权限；类级表只给默认值，实例 ledger 必须按 §2.2 规则裁决为单值。 |
| `better_stm_condition_impact` | G0–G6 中受影响的 gate。 | 连接 Better 判定。 |
| `conversion_artifact_risk` | low / medium / high。 | 标记可能只是 conversion / lowering artifact。 |
| `forbidden_extrapolation` | 禁止 claim 文本。 | 审稿风险防线。 |

### 2.1 `repair_action_allowed` 五级枚举

| 值 | 含义 | 例子 |
|---|---|---|
| `must_fix` | 若证据确认，repair loop 必须尝试修复，否则不能判 Better。 | NL 明确 guard，但候选把它删除。 |
| `should_fix` | 应优先修复；若不修复需在 partial 或 limitation 中解释。 | action/effect 可追溯但缺少结构化字段。 |
| `monitor` | 记录并观察，不允许自动大改。 | 仅 loss ledger 提示的 candidate-only 条件标签。 |
| `not_repair_target` | 不作为 repair loop 目标。 | 已可接受的 event abstraction。 |
| `out_of_scope` | 当前论文范围外。 | timed automata clock constraint。 |

### 2.2 类级默认值与实例级单值裁决

§3 的 taxonomy 表是**类级合同**，其中 `repair_action_allowed` 列给出该类 target 的默认单值。后续 R5.7.4 / R6 / R7 处理某个具体 pair 时，实例 ledger 仍必须记录一个且仅一个 `repair_action_allowed`，不得写成 `must_fix / should_fix` 这类集合值。若实例值不同于类级默认值，必须额外记录 `repair_action_override_reason`。

R5.7.2 采用以下 v0 分界规则：

| 实例证据状态 | `repair_action_allowed` | 例子 |
|---|---|---|
| `NL` 明确要求，raw/canonical/change 证据确认目标缺失或错误，且不修会破坏 G3/G5。 | `must_fix` | NL 明确要求异常处理迁移，`STM_k` 删除该迁移。 |
| `NL` 明确要求，目标已存在但结构化程度不足、trace 不完整或影响局部质量。 | `should_fix` | `show error` 保留在 event label 中，NL 支持其为 action/effect。 |
| 只有 loss ledger / representation symptom，尚未回到 NL + raw 证据确认。 | `monitor` | `condition_like_label_lowered_as_event` 只在 lowering ledger 中出现。 |
| 裁决后确认现有抽象可接受，或该现象不应由 repair loop 修改。 | `not_repair_target` | `lane change completed` 被确认是 completion event。 |
| 模型族、时间语义或表达能力超出当前论文 scope。 | `out_of_scope` | timed automata clock constraint / hybrid dynamics。 |


## 3. 11 类一级 taxonomy

| target_id | semantic_element | scope_status | time_level | structure_family | nl_evidence_required | representation_evidence_required | repair_action_allowed | better_stm_condition_impact | conversion_artifact_risk | forbidden_extrapolation |
|---|---|---|---|---|---|---|---|---|---|---|
| `state_structure` | state | main | T0 | FSM / HSM / discrete statechart subset | yes | raw + canonical + diagnostics | should_fix | G3 / G4 / G5 | medium | 不得把状态重命名或 normalization 当 repair gain。 |
| `transition_structure` | transition | main | T0 | FSM / HSM / discrete statechart subset | yes | raw + canonical + change ledger | should_fix | G3 / G4 / G5 | medium | 不得为通过场景删除需求相关 transition。 |
| `event_trigger` | event_trigger | main | T0 | FSM / HSM / discrete statechart subset | yes | raw label + canonical event + loss ledger | should_fix | G4 / G5 | medium | 不得把所有条件、效果都折叠为 event 后仍称 Better。 |
| `guard_condition` | guard_condition | main | T0 | FSM / HSM / discrete statechart subset / EFSM-lite-candidate | yes | raw label + canonical guard/loss + change ledger | should_fix | G3 / G4 / G5 | high | 不得无 NL 证据新增 guard；不得写完整 EFSM 覆盖。 |
| `action_effect` | action_effect | main | T0 | FSM / HSM / discrete statechart subset / EFSM-lite-candidate | yes | raw label + canonical action/loss + change ledger | should_fix | G3 / G4 / G5 | high | 不得把 UI 文本或状态名强行改成 action。 |
| `hierarchy_pseudostate` | hierarchy_pseudostate | main | T0 | HSM / discrete statechart subset | conditional | raw structure + canonical hierarchy + diagnostics | should_fix | G3 / G4 / G5 | medium | 不得用 stoppable state 代替必须瞬时通过的 pseudo-state。 |
| `traceability_grounding` | traceability | main | T0 | all in-scope families | yes | NL spans + raw/canonical element IDs + change ledger | must_fix | G2 / G5 / G6 | low | 不得把 untraced additions 写成语义改善。 |
| `scenario_behavioral_obligation` | scenario_behavior | main | T0 | all in-scope families | yes | scenario trace + diagnostics + change ledger | must_fix | G3 / G4 / G5 | low | 不得用场景通过覆盖未测需求。 |
| `temporal_cue_tick_counter_caveat` | temporal_cue | caveat | T0.5 | FSM / HSM / discrete statechart subset | yes | raw label + NL timing cue + caveat ledger | monitor | G0 / G5 | high | 不得写 timed automata、clock constraint 或 T0 headline success。 |
| `representation_only_conversion_artifact` | representation_artifact | caveat | T0 / T0.5 | all in-scope families | no | conversion ledger + loss ledger | monitor | G2 / G6 | high | 不得计 repair gain；不得直接写 confirmed defect。 |
| `out_of_scope_family` | out_of_scope_family | excluded | T1+ 或任意 | timed / hybrid / arbitrary UML / protocol FSM | conditional | source artifact + scope rationale | out_of_scope | G0 | high | 不得进入 main repair target、T0 denominator 或 method success。 |

## 4. 重点目标解释与例子

### 4.1 `guard_condition`

**代表症状**：PlantUML / raw label 中出现条件式，但 canonical 表示中只保留为 event label。

| 例子 | 初始判断 | 需要证据 | 允许动作 |
|---|---|---|---|
| `Front Distance > 10` | candidate guard。 | `NL` 是否要求距离条件决定迁移；raw label 是否写作条件而非事件名。 | confirmed 后 `should_fix` 或 `must_fix`。 |
| `dist_to_front<25 && extra_lane=true` | strong candidate guard。 | 变量比较和布尔条件是否可追溯到 `NL`。 | confirmed 后结构化 guard；缺证据时 monitor。 |
| `if door closed` | candidate guard / trigger 混合。 | `NL` 是否把 door closed 当状态条件还是触发事件。 | 裁决后再修。 |

**禁止**：仅因字符串包含 `>`、`<`、`&&` 就批量判为 confirmed guard defect。

### 4.2 `event_trigger`

**代表症状**：自然语言中的事件、条件、效果混在一个 label 中。

| 例子 | 初始判断 | 处理 |
|---|---|---|
| `lane change completed` | 多数情况下是 trigger / completion event。 | 保留 event，除非 `NL` 明确它是 action/effect 或目标状态。 |
| `Timer Expired` | timeout event 或 T0.5 timing cue。 | 若只是离散 timeout event，可保留 event；若含周期 tick/counter，进入 T0.5 caveat。 |
| `Door Closed [zero time set]` | trigger + action/effect cue。 | 裁决是否拆成 event + effect；缺证据则标为 partial 或 monitor。 |

### 4.3 `action_effect`

**代表症状**：系统输出、赋值、显示、计数器更新在 label 中丢失或被当作 event。

| 例子 | 初始判断 | 处理 |
|---|---|---|
| `show error` | action/effect cue。 | 若 `NL` 明确系统应显示错误，则 confirmed 后 `should_fix`。 |
| `print bill` | action/effect cue。 | 若是转移效果，修复为 effect；若是事件名，保留。 |
| `reset timer` | action/effect 或 T0.5 counter cue。 | 需要区分离散 counter 与真实 clock。 |

### 4.4 `hierarchy_pseudostate`

共存 event + condition / condition + condition 时，若目标表示需要中继，优先使用 pseudo-state relay，而不是可驻停 state。pseudo-state 的意义是表达瞬时结构或选择点，避免在可驻停 state 上制造伪 cycle。

R5.7.2 不要求手写 pyfcstm 内部 `__combo_*`，后续实现应优先利用 pyfcstm main 的 combo event / guard 机制；若无法表达，再由转换层明确记录 approximation 与 loss。

### 4.5 `temporal_cue_tick_counter_caveat`

T0.5 与 T1 的边界：

| 情况 | 分类 | 处理 |
|---|---|---|
| `Timer Expired` 作为离散超时事件。 | T0 或 T0.5，依证据。 | 可作为 event；必要时 caveat。 |
| 周期 tick，例如“每 5ms 更新一次”。 | T0.5。 | 可降级为离散 counter caveat，不进 T0 headline。 |
| clock constraint、real-time bound、连续时间不变量。 | T1+ / out-of-scope。 | stress / excluded，不进入 Better 主裁决。 |

## 5. 与 Better STM gate 的连接

| taxonomy 类 | 主要影响 gate | Better 判定中的作用 |
|---|---|---|
| state / transition / hierarchy | G3 no-regression、G4 improvement、G5 semantic。 | 保证结构修复不破坏需求行为。 |
| event / guard / action | G4 improvement、G5 semantic。 | 防止 label-level 可执行化掩盖语义折叠。 |
| traceability | G2 attribution、G5 semantic、G6 reporting。 | 防止 untraced additions 与 attribution laundering。 |
| scenario behavior | G3 no-regression、G4 improvement。 | 支撑行为义务和回归检查。 |
| temporal cue | G0 scope、G5 semantic。 | 区分 T0 headline、T0.5 caveat 与 T1 stress。 |
| representation artifact | G2 attribution、G6 reporting。 | 只作风险和 caveat，不直接计 repair gain。 |
| out-of-scope family | G0 scope。 | 排除主线或仅作 stress / limitation。 |

## 6. 下游 ledger 最低字段

后续 R6/R7 若把某个 target 写入 run record 或 repair ledger，至少应保留：

| 字段 | 说明 |
|---|---|
| `target_id` | 对应本 taxonomy 的一级类或细化子类。 |
| `candidate_status` | candidate-only / confirmed / rejected / monitor。 |
| `evidence_bundle_id` | 指向 `NL`、raw `STM_0`、canonical `STM_0`、loss ledger、diagnostics、scenario trace。 |
| `repair_action_allowed` | 五级枚举之一，实例级必须单值。 |
| `repair_action_override_reason` | 若实例值不同于 §3 类级默认值，说明触发 §2.2 哪条分界规则。 |
| `repair_action_taken` | no-op / structural split / guard extraction / action extraction / hierarchy repair / rollback 等。 |
| `better_gate_impact` | G0–G6 哪些 gate 受影响。 |
| `semantic_gate_verdict` | 若该 target 参与 G5 semantic gate 裁决，记录 pass / fail / partial / unknown；若未进入 G5，记录不适用理由。 |
| `adjudication_status` | rule-pass / llm-provisional / human-confirmed / conflict / unknown。 |
| `forbidden_attribution_reason` | 若不能计 repair gain，说明原因。 |

## 7. 禁止主张

1. 不把 taxonomy 写成已证明的缺陷统计。
2. 不把 `condition_like_label_lowered_as_event` 批量写成 confirmed guard defect。
3. 不把 T0.5 tick/counter 写成 timed automata 支持。
4. 不把 pyfcstm combo event 能力写成论文贡献。
5. 不把 representation-only conversion artifact 当作 repair target 或 repair gain。
6. 不让 taxonomy 后续因 R6/R7 结果好坏随意漂移；若需修订，必须由 R5.7.4/R7 dry-run findings ledger 驱动。

## 审计附录：证据链与事实源

### A.1 上游事实源清单

| 引用键 | source_id | 事实源 | 类型 | 用途 |
|---|---|---|---|---|
| [src-r56-handoff] | `r56_to_r57_handoff` | [../scope/r5_6_to_r5_7_handoff_constraints.md](../scope/r5_6_to_r5_7_handoff_constraints.md) | md | taxonomy 字段合同、candidate-only 和 claim 降级规则。 |
| [src-model-scope] | `r56_model_scope` | [../../story/model_scope.md](../../story/model_scope.md) | md | T0/T0.5/T1、模型族与禁止外推。 |
| [src-better] | `r572_better_stm` | [better_stm_definition.md](./better_stm_definition.md) | md | G0–G6 gate、三层输出模型、Better 判定接口。 |
| [src-partial] | `llms_emp_partial_ledger` | [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | jsonl | `condition_like_label_lowered_as_event` 等 representation symptom 的来源。 |

### A.2 决策键清单

| 引用键 | 来源 | 冻结结论 |
|---|---|---|
| [dec-q5] | [PR #140 Q5](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868584922) | 11 类 taxonomy、11 字段合同、五级 `repair_action_allowed`。 |
| [dec-q6] | [PR #140 Q6](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868834329) | guard/event/action folding 的证据和修复策略。 |
| [dec-q7] | [PR #140 Q7](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868890452) | T0.5 tick/counter caveat 与 T1 stress 边界。 |
| [dec-q12] | [PR #140 Q12](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4869119301) | 规则修订必须 evidence-driven。 |

### A.3 Claim-evidence map

| 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 置信度 | caveat |
|---|---|---|---|---|---|---|
| [clm-taxonomy-fields] | `R572-TAX-C1` | 每条 taxonomy entry 必须保留 11 字段。 | contract | [src-r56-handoff] §3；本文件 §2。 | high | 后续可新增字段，但不能删除最低字段。 |
| [clm-candidate-only] | `R572-TAX-C2` | representation symptom 不能直接升级为 confirmed defect。 | prohibition | [src-r56-handoff] §2/§5；本文件 §1、§4。 | high | R5.7.4 可逐例裁决。 |
| [clm-action-enum] | `R572-TAX-C3` | `repair_action_allowed` 必须取五级枚举之一。 | contract | [dec-q5]；本文件 §2.1。 | high | R6/R7 可增加细分动作字段，但枚举需兼容。 |
| [clm-t05-tax] | `R572-TAX-C4` | T0.5 tick/counter 只能 caveat 处理，不支撑 timed automata。 | scope | [dec-q7]；[src-model-scope]。 | high | T1 直接 stress / excluded。 |
| [clm-single-action] | `R572-TAX-C5` | `repair_action_allowed` 在实例 ledger 中必须是单值；类级表只给默认值，override 需记录理由。 | contract | [dec-q5]；本文件 §2.2、§3。 | high | R5.7.4/R7 可细化 override reason，但不能回到多值枚举。 |

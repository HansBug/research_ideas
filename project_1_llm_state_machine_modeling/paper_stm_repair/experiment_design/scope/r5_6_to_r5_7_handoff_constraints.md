# R5.6 -> R5.7 handoff constraints

> **定位**：本文件是 R5.6 交给 R5.7 的硬约束清单。R5.7 可以定义 Better STM 建模要求和 repair target taxonomy，但不得重新打开 R5.6 已冻结的 model scope 与 claim boundary。

## 1. R5.7 必须继承的范围决策

| 约束 ID | 约束 | R5.7 行动 |
|---|---|---|
| R56-H1 | 主实验 headline scope 限定为 T0 离散 FSM / HSM / EFSM-lite / 离散 UML-SysML statechart 子集。 | taxonomy 只能在该范围内定义 main repair target。 |
| R56-H2 | T0.5 timer-like cue 只能是 caveat / annotation。 | 可定义为 monitor / caveat，不得定义 timed automata repair target。 |
| R56-H3 | Digital Camera / T1-ish case 只作 supplementary stress / limitation。 | 可作 stress dry-run，不支撑 T0 主 claim。 |
| R56-H4 | timed automata、hybrid automata、arbitrary UML、protocol FSM 不进入 main claim。 | taxonomy 中如出现，只能列 `out_of_scope` / `related_work_only`。 |
| R56-H5 | conversion / normalization / `.fcstm` lowering 不计 repair gain。 | repair target 必须从转换后 `STM_0` 出发，三阶段归因不可省略。 |
| R56-H6 | selected smoke examples 是 dry-run / sanity panel。 | 可继续用于 dry-run，不得替代正式实验集。 |

## 2. R5.7 可讨论但不得直接升级的候选

| 候选现象 | 当前来源 | R5.6 判定 | R5.7 需要做什么 |
|---|---|---|---|
| `condition_like_label_lowered_as_event` | R4.5 / R5.5 partial ledger | representation symptom / candidate-only | 回到 NL + raw `STM_0` 判定是 trigger、guard、action 还是 acceptable abstraction。 |
| entry / exit / do activity lowering | R4.5 loss ledger | candidate semantic element | 判断是否进入 must_fix / should_fix / monitor / not_repair_target。 |
| hierarchy lowering / scope lifting | R4.5 loss ledger | conversion / representation caveat | 区分 pipeline artifact 与真实 model defect。 |
| initial inference | R4.5 loss ledger | pipeline artifact 候选 | 不得直接计为 repair gain；若影响行为，需场景证据。 |
| composite target lowering | R4.5 loss ledger | pseudo-state / hierarchy caveat | 优先检查 pseudo-state relay 与层级语义是否可保留。 |
| T0.5 timer-like cue | R5.5 cluster profile | caveat | 只能定义 annotation / monitor，不得提升为 timed automata repair。 |
| T1-ish Digital Camera | R5.5 cluster profile | supplementary stress | 可作 stress case，不作为 main metric denominator。 |

## 3. R5.7 repair target taxonomy 的最低字段

R5.7 若新增 repair target taxonomy，至少应包含以下字段：

| 字段 | 说明 |
|---|---|
| `target_id` | 稳定 ASCII ID。 |
| `semantic_element` | event / trigger / guard / action / hierarchy / pseudo-state / temporal cue / NL traceability 等。 |
| `scope_status` | `main` / `caveat` / `supplementary_stress` / `excluded`。 |
| `time_level` | T0 / T0.5 / T1+。 |
| `structure_family` | FSM / HSM / EFSM-lite / discrete statechart subset / excluded family。 |
| `nl_evidence_required` | 是否需要 NL 明示证据。 |
| `representation_evidence_required` | 是否需要 raw `STM_0` / canonical / `.fcstm` / loss ledger 证据。 |
| `repair_action_allowed` | must_fix / should_fix / monitor / not_repair_target / out_of_scope。 |
| `better_stm_condition_impact` | 影响 Better STM 五条件中的哪一条。 |
| `conversion_artifact_risk` | 是否可能只是 conversion / lowering artifact。 |
| `forbidden_extrapolation` | 不得由该 target 推出的 claim。 |

## 4. R5.7 不得做的事

1. 不得把 R5.6 excluded 的模型族重新放入 main repair target。
2. 不得把 T0.5 / T1+ 写成 timed automata 覆盖。
3. 不得把 R5.5/R5.6 的 partial / loss code 直接等价为 confirmed model defect。
4. 不得把 normalization、canonical conversion、`.fcstm` parse success 或 inspect success 写成修复收益。
5. 不得无 NL 证据凭空新增 guard/action。
6. 不得在 R5.7 运行正式 repair experiment；R5.7 只冻结语义合同和 dry-run。

## 5. Claim 降级规则

R5.7 定义 taxonomy 时必须给每类 target 同时写出 claim 强度和降级路径。最低规则如下：

| 触发条件 | claim 强度 | 必须降级为 | 禁止写法 |
|---|---|---|---|
| target 只来自 loss ledger / representation symptom，尚未回到 NL + raw `STM_0` 复核 | candidate-only | “potential repair target / representation caveat” | “confirmed defect” |
| target 只出现在 T0.5 timer-like cue | caveat / annotation | “timer-like textual cue under event abstraction” | “timed automata support” |
| target 只出现在 T1-ish / Digital Camera supplementary stress | supplementary / limitation | “stress case / limitation / appendix evidence” | “T0 main result” |
| target 可能由 normalization / conversion / `.fcstm` lowering 引入 | conversion-artifact-risk | “conversion-aware case analysis” | “repair-loop gain” |
| target 缺少 NL 明示证据 | monitor 或 not_repair_target | “needs adjudication / cannot be repaired automatically” | “system should invent missing semantics” |
| target 属于 timed / hybrid / arbitrary UML / protocol FSM | out_of_scope | “related work / future work / excluded family” | “main repair target” |

## 6. R5.7 开放问题

以下问题必须在 R5.7 中逐项关闭或显式标为未闭合，不能隐式跳过：

1. `condition_like_label_lowered_as_event` 到底是 trigger、guard、action、acceptable abstraction，还是 conversion artifact？
2. entry / exit / do activity 文本应进入 must-fix、should-fix、monitor，还是仅作为 loss ledger？
3. pseudo-state relay 与 composite target lowering 是否影响 behavior trace，还是只影响 representation readability？
4. T0.5 microwave cluster 在主实验中是仅作 caveat、单独 annotation stratum，还是从 headline denominator 中排除？
5. Digital Camera / T1-ish cluster 是否只保留 stress dry-run，还是完全排除出 R7 主协议？
6. `EFSM-lite` 的变量 / guard / action 边界是否能被 pyfcstm diagnostics 与 human rubric 可靠裁决？

## 7. 交接给 R6 / R7 的提醒

- R6：先实现 fake / replay repair loop skeleton；真实 LLM 调用前必须 `source .env` 并写 run record。
- R7：把 R5.6 scope 与 R5.7 target taxonomy 合并成主实验预注册，不得用 R8 结果反向改指标。
- R8：主结果只来自 eligible repair runs；失败、回滚、振荡、不收敛必须入账。

## 8. 事实源

| 事实源 | 用途 |
|---|---|
| [../../story/model_scope.md](../../story/model_scope.md) | R5.6 scope 与 claim boundary 真源。 |
| [2026-06-29-17-33-35-r5-5-scope-handoff.md](./2026-06-29-17-33-35-r5-5-scope-handoff.md) | R5.5 -> R5.6 handoff。 |
| [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | candidate-only / partial attribution。 |
| [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | 60 pair status / time / story role。 |
| [../../reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](../../reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md) | R5.5.2 current status 与 conversion recovery caveat。 |

# Better STM 判定合同 v0（R5.7.2）

> **定位**：本文件是 R5.7.2 冻结的 Better STM 判定合同，回答“在同一个自然语言需求 `NL` 与同一个规范化初始状态机 `STM_0` 上，候选 `STM_k` 满足什么条件时才能被判为相对更优”。它细化 R5.7.1 的评价逻辑链，不运行 repair loop，不生成 `STM_k`，不报告方法效果。
>
> **证据引用说明**：正文中的 `[src-*]`、`[dec-*]`、`[clm-*]` 是本文件内部的稳定证据键或决策键，不按数字顺序重排。

## 1. 一句话结论

Better STM 不是“可解析”“可执行”“指标更高”或“诊断更少”的同义词。R5.7.2 将 Better STM 定义为：在同一 `NL`、同一 canonical `STM_0`、同一冻结证据包和同一裁决协议下，候选 `STM_k` 通过 scope、可评价性、归因、无回归、改善、语义裁决和报告完整性七道门后，才能被判定为相对 canonical `STM_0` 的语义保真改善 [dec-q2][dec-q9]。

原始 `raw STM_0` 是需求意图、表示损失和转换归因的证据源；直接比较对象是 canonical `STM_0` 与 `STM_k`，repair gain 只能从 canonical `STM_0 -> STM_k` 开始计算 [dec-q1][dec-q2]。

## 2. 对象角色与公式

R5.7.2 采用如下 shorthand：

$$
Better_{v0}(STM_k, STM_0^{can} \mid NL, STM_0^{raw}, L_{conv}, L_{chg}, D, S, R)
$$

| 对象 | 角色 | 可支持的证据 | 禁止外推 |
|---|---|---|---|
| `NL` | 需求语义锚点。 | 判断状态、事件、guard、action、场景义务是否有需求证据。 | 不得凭 `NL` 中不存在的信息发明 guard/action。 |
| `STM_0^{raw}` | 一手原始状态机证据。 | 判断 source author / LLM 原意、PlantUML / Umple / XML 标签、转换前结构。 | 不直接作为 Better 比较层，因为 raw 未必可执行或可审计。 |
| `STM_0^{can}` | 规范化初始状态机，Better 比较起点。 | repair loop 的 baseline、诊断、场景和 change ledger 起点。 | raw -> canonical 的收益不计 repair gain。 |
| `STM_k` | repair loop 输出候选。 | 进入 gate 链与语义裁决。 | A-pass、parse ok 或单项指标改善不等于 Better。 |
| `L_{conv}` | conversion / normalization / lowering ledger。 | 归因 representation loss、candidate-only symptom、转换风险。 | 不得写成 repair-loop 贡献。 |
| `L_{chg}` | canonical `STM_0 -> STM_k` change ledger。 | 判断变更是否来自 repair loop、是否影响语义、是否可回滚。 | 无法归因的变化不得计入 repair gain。 |
| `D` | parse / semantic / design / sim 等诊断集合。 | hard gate、结构化反馈、负证据。 | 诊断减少不能单独证明语义更优。 |
| `S` | 冻结场景 / 回归套件。 | no-regression 与行为义务证据。 | 场景通过率不能覆盖未测需求。 |
| `R` | 人工 / LLM-as-Judge / 结构化裁决量表。 | NL-grounded semantic adjudication。 | LLM 裁决不是 gold；冲突需要人工升级。 |

本文件沿用 R5.6 的状态机抽象作为判定锚点，模型对象定义以 [../../story/model_scope.md](../../../../story/model_scope.md) 为准 [src-model-scope]：

$$
M = (S, s_0, E, V, T, H, A, \tau)
$$

迁移写作：

$$
t = (s, e, g, a, s')
$$

其中 $e$ 是 trigger / event，$g$ 是离散且可追溯的 guard 谓词，$a$ 是 action / effect，$\tau$ 是模型元素到 `NL` 或 raw `STM_0` 片段的 traceability。`.fcstm` / `pyfcstm` 只是实验介质，不定义论文贡献，也不反向定义模型范围 [src-model-scope]。

## 3. 七道 gate 链

R5.7.2 将旧版五条必要条件细化为七道可审计 gate。任一 gate 失败都不得计为 Better；某些 gate 失败还会让该 run 失去进入 Better 裁决的资格 [dec-q2][dec-q4]。

| Gate | 中文名 | 通过条件 | 不通过时的去向 | 不能说明什么 |
|---|---|---|---|---|
| G0 | scope gate | 样例被路由为 `main_t0`、`caveat_t05`、`stress_t1` 或 `excluded_out_of_scope`。T0 才能进入 headline Better 主线；T0.5 只能在 caveat 层讨论；T1 只作 stress / limitation。 | `excluded_out_of_scope` 或 supplementary stress；T0.5 进入 caveat ledger。 | scope 通过不代表模型正确。 |
| G1 | A gate | `STM_0^{can}` 与 `STM_k` 都具备足够结构、来源、诊断、证据链和可审计记录。 | `stm0_readiness_failure` 或 `stmk_repair_failure`。 | A-pass 不代表 Better。 |
| G2 | attribution gate | 候选变化可追溯为 canonical `STM_0 -> STM_k` 的 repair-loop 输出，且与 raw -> canonical 的转换收益分开。 | `protocol_or_provenance_invalid`，或在 attribution ledger 中标为不能计 repair gain。 | 无法归因不能写成 unknown success。 |
| G3 | no-regression gate | 冻结场景、trace、safety-relevant behavior、核心结构和关键需求义务不退化。 | `not_better` 或 `stmk_repair_failure`。 | 无回归不代表已有改善。 |
| G4 | improvement gate | 至少一个预注册维度有正向改善，例如 blocking diagnostics 减少、结构覆盖改进、traceability 提升、场景义务更一致。 | `not_better`。 | 单项改善不能替代语义裁决。 |
| G5 | semantic gate | `NL + raw STM_0 + canonical STM_0 + STM_k + change ledger` 共同支持改善，且不判 semantic drift、over-repair、under-repair 或语义折叠。 | `not_better`、`partial` 或 `unknown`。 | LLM provisional verdict 不是 gold。 |
| G6 | reporting gate | 输出进入 success / failure / partial / unknown / scope / attribution ledger，证据包完整可复验。 | `protocol_or_provenance_invalid`；不得进入主统计。 | 报告完整不代表成功。 |

这条 gate 链的核心意图是防止三类洗白：把转换收益洗成 repair gain、把 metric improvement 洗成语义改善、把失败 / partial / unknown 从分母中洗掉 [dec-q5][dec-q9][src-eval-logic]。

## 4. 三层输出模型

R5.7.2 不采用扁平七状态 verdict，而采用三层输出模型，避免把 scope、运行有效性和语义更优混在一个字段里 [dec-q4]。

### 4.1 `scope_routing_status`

| 值 | 含义 | 论文位置 |
|---|---|---|
| `main_t0` | 离散 FSM / HSM / 离散 statechart 子集；可进入 headline 候选分母。 | 主表候选。 |
| `caveat_t05` | timer-like cue / tick / discrete counter abstraction caveat；可在 caveat 层讨论 Better，但不进入 T0 headline。 | caveat 表 / 附表。 |
| `stress_t1` | T1-ish / Digital Camera 等 stress case。 | supplementary stress / limitation。 |
| `excluded_out_of_scope` | timed / hybrid / arbitrary UML / protocol FSM 等当前范围外模型族。 | related work / future work / exclusion ledger。 |

### 4.2 `run_validity_status`

| 值 | 含义 | 典型原因 |
|---|---|---|
| `valid_run` | 可进入 Better 语义裁决。 | G0–G3/G6 的最低证据链成立。 |
| `stm0_readiness_failure` | 初始 canonical `STM_0` 不具备作为 repair 起点的可评价性。 | source 缺失、结构不可审计、baseline hash 缺失。 |
| `stmk_repair_failure` | repair 输出候选失效。 | `STM_k` schema-invalid、parse fail、关键结构破坏、生成空模型。 |
| `protocol_or_provenance_invalid` | 协议或归因证据失效。 | change ledger 缺失、raw->canonical 改善被混入 repair gain、run record 不完整。 |

R5.7.2 删除常规 outcome 中的 `not_attributable` 表述，避免误读为“一个正常失败状态”。不可归因属于 `protocol_or_provenance_invalid` 或 attribution ledger 的禁入事实，不进入 Better success denominator [dec-q4]。

### 4.3 `better_adjudication_outcome`

| 值 | 含义 | 最低证据 |
|---|---|---|
| `better` | 相对 canonical `STM_0` 有可归因、无关键回归、语义保真的改善。 | G0–G6 全部通过，且 G5 正向。 |
| `not_better` | 候选可评价，但没有改善或存在明确语义退化 / 过修 / 欠修。 | G3/G4/G5 失败且证据足够。 |
| `partial` | 有局部改善或候选 target，但存在 caveat、表示损失、证据未闭合或非主线层级限制。 | 证据支持部分现象，但不足以判 Better。 |
| `unknown` | 证据不足、裁决冲突或无法可靠判断。 | 已说明缺失证据与下一步补证路径。 |

## 5. 硬拒绝与需要裁决的边界

### 5.1 必须硬拒绝为非 Better 的情况

| 情况 | 默认 outcome | 理由 |
|---|---|---|
| `STM_k` 为通过测试删除需求相关行为。 | `not_better` 或 `stmk_repair_failure` | 违反 no-regression / semantic gate。 |
| 诊断减少但 guard / action / state 语义偏离 `NL`。 | `not_better` | 指标改善不能覆盖 semantic drift。 |
| 场景通过但新增无 trace 的关键行为。 | `not_better` 或 `unknown` | traceability / grounding 不闭合。 |
| 把 `NL` 明示条件、效果全部塞入 event label，且 source / NL 支持其应为 guard/action。 | `not_better` 或 `partial` | 语义折叠破坏模型元素结构。 |
| raw -> canonical 的 normalization 修复被当作 `STM_0 -> STM_k` 改善。 | `protocol_or_provenance_invalid` | attribution laundering。 |
| run record、baseline hash、candidate hash 或 change ledger 缺失。 | `protocol_or_provenance_invalid` | 不可审计。 |

### 5.2 必须进入 `partial` / `unknown` 而不能直接判缺陷的情况

| 情况 | 默认 outcome | 下一步 |
|---|---|---|
| 只有 loss ledger 记录 `condition_like_label_lowered_as_event`，尚未回到 `NL + raw STM_0`。 | `partial` / candidate-only | 在 R5.7.4 或 R7 裁决 trigger / guard / action / acceptable abstraction。 |
| T0.5 tick / timeout cue 可用离散 counter 抽象解释，但没有 timed automata 语义。 | `partial` 或 caveat-level judgement | 单列 T0.5 caveat，不进 T0 headline。 |
| LLM-as-Judge 与规则检查冲突。 | `unknown` | 人工审计升级，记录冲突原因。 |
| 指标改善但语义证据不充分。 | `unknown` 或 `partial` | 补 NL evidence、raw STM evidence、场景或人工裁决。 |

## 6. guard / event / action 语义折叠纪律

R5.7.2 采用“source syntax + lexical cue + NL evidence + representation evidence”四证合一的判定方式 [dec-q6]。

| 现象 | 初始处理 | 什么时候成为 repair target | 什么时候只是 caveat / monitor |
|---|---|---|---|
| `Front Distance > 10` 被 lowering 为 named event。 | candidate-only。 | `NL` 或 raw label 明确表达条件，且迁移语义需要 guard 才能区分行为。 | source 本来就是事件名，或条件只是自然语言触发短语。 |
| `dist_to_front<25 && extra_lane=true` 作为 event label。 | candidate-only，强 guard cue。 | 变量比较和布尔条件可追溯到 `NL`，且 action/transition 选择依赖它。 | 只作为不可自动修复的复杂表达式，进入 monitor。 |
| `lane change completed` 作为 event。 | 默认 trigger。 | 只有 `NL` 明确其应为 effect/result 状态而非触发。 | 维持 event，记录 trace。 |
| `show error`、`print bill` 作为迁移标签。 | action/effect cue。 | `NL` 明确它是系统输出 / side effect。 | 若只是状态名或 UI 文本，需人工裁决。 |

修复动作原则：confirmed guard/action folding 是 semantic gate 的负证据；repair 应尽量恢复结构化 `event + guard + effect`，同时保留原始标签 trace。若目标表示需要组合条件，应使用 pyfcstm main 的组合表达式语义，而不是手写 `__combo_*` 伪状态 [dec-q6]。

当前 pyfcstm 子模块为 `5f811a0f / v0.4.0`，远端 main 已出现 combo event 相关能力；未来真实执行必须显式 pin / update 依赖。R5.7.2 只记录语义合同与语法示例，不把 pyfcstm 能力写成论文贡献 [dec-q6]。

合法示例（作为下游实现参考，非本文贡献）：

```fcstm
S -> T : E1 + [x > 0];
S -> T :: E1 + [x > 0] + E2;
S -> T : [x > 0];
S -> T : [x > 0] + [y > 0];
S -> T : /Bus.E2 + [x > 0];
S -> T :: E1 + [x > 0] effect { flag = 1; };
```

禁止示例：

```fcstm
S -> T : E1 if [x > 0];
```

## 7. T0.5 caveat 判定

T0.5 不进入 T0 headline，但可以在 caveat 层被评价 [dec-q7]。R5.7.2 采用以下纪律：

1. 明确 timeout event、周期 tick / counter、模糊时间提示三类对象。
2. 周期 tick 若可降级为离散计数器，可作为 `caveat_t05` 下的有限修复目标或 monitor。
3. T0.5 的任何改善都不得写成 timed automata、clock constraint、real-time verification 或 T0 headline success。
4. T1 直接进入 `stress_t1` / out-of-scope stress，不进入 Better 主裁决。

## 8. pair / cluster 报告纪律

`llms-emp` 必须报告为 10 个 NL clusters / 60 个 generated STM pairs [dec-q8]。

| 层级 | 用途 | Better 判定方式 |
|---|---|---|
| pair-level | 一个 `<NL, canonical STM_0, STM_k>` repair attempt。 | gate 链逐 pair 裁决。 |
| cluster-level | 同一 NL 下 6 个 LLM-generated `STM_0` 的需求级分组。 | 汇总 6 个 pair 的分布，例如 any / majority / all；不得假装 6 个独立需求。 |
| LLM-family | source STM bias / 初始错误分布辅助分析。 | 只能做辅助解释，不作为论文核心贡献。 |

主论文可以用 cluster-level 展示需求覆盖和 source STM bias，用 pair-level 展示 run / repair attempt 结果；二者必须同时保留，避免 cherry-picking [dec-q8]。

## 9. 客观指标与语义裁决的位置

客观指标是 supporting evidence，不是 verdict [dec-q9]。R5.7.2 只冻结指标权限上限，完整指标框架交给 R5.7.3。

R5.7.3 已在 [../metrics/objective_metric_framework.md](../metrics/objective_metric_framework.md) 冻结客观代理指标框架 v0：五级 `metric_permission`、entry schema、G0--G6 gate × metric matrix、分母 / reference / 偏序、anti-gaming 风险和 baseline 迁移边界。本文件的 G5 semantic gate 权限不因此降低；任何 metric improvement 仍必须回到语义裁决。

| 指标层 | 可用作 | 不可用作 |
|---|---|---|
| executability / hard gate | A gate、run validity。 | Better STM 充分条件。 |
| structural coverage | improvement gate 的候选证据。 | 无需语义裁决的成功率。 |
| behavioral scenario | no-regression 与局部改善证据。 | 覆盖全部需求的证明。 |
| change discipline | attribution 与 over-repair 风险证据。 | 方法有效性主结果。 |
| F1 / accuracy | 只有存在 adjudicated reference target 时才可使用。 | 默认质量总分。 |

若后续规则或指标需要修订，必须优先由 R5.7.4 真实 dry-run 发现驱动；没有 dry-run 证据的修订只能标为 provisional，不得静默改写 v0 合同 [dec-q12]。

## 10. 裁决协议接口

R5.7.2 采用分层裁决 [dec-q10]：

1. 规则检查处理 hard facts：scope、A gate、ledger 完整性、parse/schema、明显删除行为、明显无 trace 新增。
2. LLM-as-Judge 只能给结构化 provisional verdict，必须输出证据引用、置信度和冲突项。
3. 人工裁决处理冲突、低置信度、headline success audit、以及 LLM 与规则不一致的样例。
4. 每次裁决必须携带完整 evidence bundle：`NL`、raw `STM_0`、canonical `STM_0`、`STM_k`、conversion ledger、change ledger、diagnostics、scenario trace、rubric output。


## 11. G5 semantic gate rubric v0

R5.7.2 不执行真实裁决，但为了让 R5.7.4 可以 dry-run，G5 semantic gate 必须至少输出以下 v0 rubric 字段。所有字段都必须引用 evidence bundle 中的 `NL`、raw `STM_0`、canonical `STM_0`、`STM_k`、conversion ledger、change ledger、diagnostics 或 scenario trace；不能只给自然语言印象。

| 字段 | 取值 | 判定含义 | 证据来源 |
|---|---|---|---|
| `nl_grounding_confidence` | high / medium / low / missing | 候选变化是否能回到 `NL` 或 raw `STM_0` 明示证据。 | `NL` span、raw label、traceability map。 |
| `semantic_drift_risk` | none / minor / major / fatal | `STM_k` 是否偏离原需求语义。 | `NL`、raw/canonical/候选 diff、scenario trace。 |
| `over_repair_indicator` | none / suspected / confirmed | 是否为通过检查删除、简化或改写需求相关行为。 | change ledger、no-regression trace、人工/LLM rubric。 |
| `under_repair_indicator` | none / suspected / confirmed | 是否仍保留关键缺陷或只修了表示层症状。 | diagnostics、taxonomy target、scenario evidence。 |
| `guard_action_fidelity` | preserved / improved / degraded / unknown | event / guard / action 是否比 canonical `STM_0` 更忠实且更结构化。 | raw label、taxonomy裁决、candidate diff。 |
| `traceability_delta` | improved / unchanged / degraded / unknown | 元素到 `NL` / raw source 的 trace 是否改善。 | trace map、untraced additions ledger。 |
| `semantic_gate_verdict` | pass / fail / partial / unknown | G5 的结构化结论。 | 上述字段合成。 |

v0 合成规则：

1. 若 `semantic_drift_risk=fatal`、`over_repair_indicator=confirmed` 或 `traceability_delta=degraded` 且影响关键需求，`semantic_gate_verdict=fail`。
2. 若 `nl_grounding_confidence=missing`，且候选变化涉及新增 guard/action/state 行为，`semantic_gate_verdict=unknown` 或 `partial`，不得判 pass。
3. 若 `guard_action_fidelity=degraded` 且 `NL` / raw evidence 支持结构化 guard/action，`semantic_gate_verdict=fail` 或 `partial`。
4. 若 `under_repair_indicator=confirmed`，且对应 taxonomy target 的实例级 `repair_action_allowed=must_fix`，`semantic_gate_verdict=fail`；若实例级 `repair_action_allowed=should_fix` 或证据只支持局部欠修，`semantic_gate_verdict=partial`，并必须在 failure / partial ledger 中记录未闭合 target。
5. 只有 `nl_grounding_confidence` 至少为 medium、无 major/fatal drift、无 confirmed over-repair、无 confirmed under-repair、且无关键 trace degradation 时，才允许 `semantic_gate_verdict=pass`。
6. LLM-as-Judge 只能生成 provisional rubric；规则冲突、low confidence、headline success 和代表性 failure 必须人工升级。

## 12. 与 repair target taxonomy 的关系

[repair_target_taxonomy.md](./repair_target_taxonomy.md) 定义哪些现象可成为 repair target、monitor、representation caveat 或 out-of-scope。Better STM 判定使用 taxonomy 的结果，但不把 taxonomy entry 自动当作 confirmed defect。最小链路为：

```text
表示症状 -> 候选语义问题 -> 确认修复目标 -> 允许修复动作 -> Better STM 证据影响
```

只有完成这条链路，并通过本文件 G0–G6，候选 `STM_k` 才可能被判为 Better。

## 13. 下游接口

| 阶段 | 继承本文件什么 | 不得做什么 |
|---|---|---|
| R5.7.3 | 已冻结 [../metrics/objective_metric_framework.md](../metrics/objective_metric_framework.md)：指标族、entry schema、分母、偏序、scope、anti-gaming 和 baseline 迁移。 | 不得把 F1 / accuracy / scenario pass / target closure / cost 单独写成 Better。 |
| R5.7.4 | 用真实或准真实样例 dry-run 本 gate 链和 taxonomy，记录 dry-run findings ledger。 | 不得把 dry-run 写成 repair effectiveness。 |
| R5.7.5 | 把 gate、taxonomy、metrics、dry-run findings 合成 R6/R7 handoff。 | 不得无证据修改 v0 合同。 |
| R6 | 实现 fake / replay repair loop skeleton 与 run record。 | 不得把 pre-repair normalization 当作修复步骤。 |
| R7/R8 | 冻结正式协议、真实运行和结果报告。 | 不得让失败 / partial / unknown 从分母消失。 |

## 审计附录：证据链与事实源

### A.1 上游事实源清单

| 引用键 | source_id | 事实源 | 类型 | 用途 |
|---|---|---|---|---|
| [src-eval-logic] | `r571_evaluation_logic` | [../evaluation_logic.md](../evaluation_logic.md) | md | R5.7.1 claim 类型、分母、A 层、归因边界、指标位置、失败报告纪律。 |
| [src-model-scope] | `r56_model_scope` | [../../story/model_scope.md](../../../../story/model_scope.md) | md | T0/T0.5/T1、模型族、状态机抽象、禁止外推。 |
| [src-r56-handoff] | `r56_to_r57_handoff` | [../scope/r5_6_to_r5_7_handoff_constraints.md](../scope/r5_6_to_r5_7_handoff_constraints.md) | md | R5.7 taxonomy 最低字段、candidate-only 纪律、scope 继承。 |
| [src-taxonomy] | `r572_repair_target_taxonomy` | [repair_target_taxonomy.md](./repair_target_taxonomy.md) | md | 修复目标分类、字段合同、repair_action_allowed 单值纪律、折叠处理。 |
| [src-case] | `llms_emp_case_matrix` | [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../../../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | jsonl | 10×6 denominator、time level、conversion/readiness 当前事实。 |

### A.2 决策键清单

| 引用键 | 来源 | 冻结结论 |
|---|---|---|
| [dec-q1] | [PR #140 Q1](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868188123) | raw `STM_0` 是 source evidence；Better 比较对象是 canonical `STM_0` vs `STM_k`。 |
| [dec-q2] | [PR #140 Q2](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868298209) | 固定 G0–G6 gate 链。 |
| [dec-q3] | [PR #140 Q3](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868355697) | 硬拒绝与需裁决边界，parse/metric 不得掩盖 semantic drift。 |
| [dec-q4] | [PR #140 Q4](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868521779) | 采用三层输出模型，不用扁平 verdict。 |
| [dec-q5] | [PR #140 Q5](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868584922) | 11 类 repair target 与 11 字段合同、五级 `repair_action_allowed`。 |
| [dec-q6] | [PR #140 Q6](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868834329) | guard/event/action folding 的处理与 pyfcstm combo 语法注意。 |
| [dec-q7] | [PR #140 Q7](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868890452) | T0.5 tick/counter caveat 可讨论，T1 不进入 Better 主裁决。 |
| [dec-q8] | [PR #140 Q8](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868946209) | cluster / pair 双层报告。 |
| [dec-q9] | [PR #140 Q9](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4868983703) | 客观指标只作 supporting evidence。 |
| [dec-q10] | [PR #140 Q10](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4869021866) | 规则 + LLM-as-Judge provisional + 人工冲突裁决。 |
| [dec-q11] | [PR #140 Q11](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4869062578) | R5.7.2 仅放代表性说明例子，系统性 dry-run 留给 R5.7.4。 |
| [dec-q12] | [PR #140 Q12](https://github.com/HansBug/research_ideas/pull/140#issuecomment-4869119301) | 下游接口与 evidence-driven revision 纪律。 |

### A.3 Claim-evidence map

| 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 置信度 | caveat |
|---|---|---|---|---|---|---|
| [clm-better-not-metric] | `R572-BETTER-C1` | Better STM 不能由 parse ok、inspect ok、诊断减少或单项指标改善单独推出。 | prohibition | [src-eval-logic] §7；本文件 §3、§9。 | high | R5.7.3 可定义指标，但不能改变 verdict 权限。 |
| [clm-raw-role] | `R572-BETTER-C2` | raw `STM_0` 是 source evidence，不是 Better 直接比较层。 | decision | [dec-q1]；本文件 §2。 | high | raw 仍必须用于归因和语义裁决。 |
| [clm-gate-chain] | `R572-BETTER-C3` | Better 判定采用 G0–G6 gate 链。 | decision | [dec-q2]；本文件 §3。 | high | R5.7.4 dry-run 后可提出 v1 修订，但需 evidence-driven。 |
| [clm-t05] | `R572-BETTER-C4` | T0.5 可在 caveat 层讨论 tick/counter，但不进入 T0 headline。 | decision | [dec-q7]；[src-model-scope]。 | high | 不支持 timed automata claim。 |
| [clm-evidence-driven-revision] | `R572-BETTER-C5` | 后续规则/指标修订应由真实 dry-run findings 驱动。 | protocol | [dec-q12]；本文件 §9、§13。 | high | R5.7.2 自身只冻结 v0 合同。 |
| [clm-output-model] | `R572-BETTER-C6` | Better STM 采用三层输出模型，`protocol_or_provenance_invalid` 不进入普通 Better outcome。 | decision | [dec-q4]；本文件 §4。 | high | R7/R8 可落成 schema，但不得回退到扁平 verdict。 |
| [clm-rubric-v0] | `R572-BETTER-C7` | G5 semantic gate 至少需要 v0 rubric 字段，供 R5.7.4 dry-run。 | protocol | [dec-q10]；本文件 §11。 | medium | 取值和冲突规则可由 R5.7.4 findings 修订。 |
| [clm-example-boundary] | `R572-BETTER-C8` | R5.7.2 的例子只是合同说明，不是系统 dry-run 或 repair effect。 | prohibition | [dec-q11]；本文件 §5、§13。 | high | R5.7.4 才产生正式 dry-run findings。 |

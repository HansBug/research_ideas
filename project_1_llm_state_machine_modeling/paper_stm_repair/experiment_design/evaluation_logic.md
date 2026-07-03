# R5.7.1 评价逻辑链与主张边界

> **定位**：本文件是 R5.7.1 的长期事实源，回答“本论文怎样从 `<NL, STM_0>`、修复目标、候选 `STM_k` 和评价证据走到方法有效性主张”。它冻结评价逻辑链、claim boundary、分母纪律、证据强度、归因边界、失败报告纪律和下游接口；不实现 repair loop，不生成 `STM_k`，不报告方法效果。
>
> **证据引用说明**：正文中的 `[src-*]`、`[clm-*]`、`[dec-*]`、`[cmd-*]` 是文末审计附录中的稳定 ASCII 证据键，不按数字重排。
> **R5.7.2 更新入口**：Better STM gate 链、三层输出模型和 repair target taxonomy 已细化到 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 与 [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md)。本文件仍是 R5.7.1 的评价逻辑链事实源；R5.7.2 不重开本文件冻结的分母、claim boundary 与 attribution boundary。
> **R5.7.3 更新入口**：客观代理指标框架已细化到 [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md)。R5.7.3 只定义指标如何作为 gate evidence / trigger / report-only / forbidden，不改变本文件冻结的“指标不能单独判 Better STM”纪律。

## 1. 一句话结论

R5.7.1 将第一篇论文的评价目标定义为：在同一个自然语言需求 `NL` 和同一个规范化初始状态机 `STM_0` 上，检验后续 repair loop 产生的候选 `STM_k` 是否具备可追溯证据、无关键回归、且可归因于修复循环的语义保真改善；转换、规范化、`.fcstm` / `pyfcstm` inspect 成功、客观指标单项改善或静态准备度都不能单独支持 Better STM 或 repair effectiveness 主张 [dec-q5][dec-q6][src-better-stm]。

本文件当前只支持 task / scope、readiness、protocol / evaluation 和 limitation / negative evidence 类型主张；repair effectiveness、Better STM 成功率和强泛化主张必须等待 R6/R7/R8 真实修复运行、change ledger、failure ledger 和语义裁决证据闭合后才能写入论文主结论 [dec-q2][src-status]。

## 2. 评价逻辑链

R5.7.1 冻结的评价链路如下：

```text
论文主张
  -> 任务边界：给定 NL 与已有 STM_0 的 repair / refinement
  -> 数据单元：NL cluster、<NL, STM_0> pair、T0/T0.5/T1 scope
  -> 表示桥：raw STM_0 -> canonical STM_0，只计 readiness，不计 repair gain
  -> 修复目标证据：NL 证据 + raw STM_0 证据 + representation / loss 证据
  -> 候选 STM_k：后续 R6/R7 产生，本文件不产生
  -> Better STM 判定：R5.7.2 已细化为 G0–G6 gate、三层输出模型和 repair target taxonomy；本文件只冻结其上游逻辑
  -> 客观指标与语义裁决：R5.7.2 已冻结指标权限上限与 semantic gate，R5.7.3 继续细化客观指标框架
  -> 论文结论：T0 主线结果、T0.5 caveat、T1 stress、failure / partial / unknown / limitation
```

这条链路的核心约束是：评价不是为了给状态机打一个总分，而是为了证明修复方法是否在同一输入对 `<NL, STM_0>` 上产生了有证据、无回归、可归因的改善 [dec-q6][src-better-stm]。

## 3. 数据单元与分母纪律

### 3.1 cluster 与 pair

`llms-emp-stm-subset` 固定表述为 **10 个唯一 NL clusters × 6 个 LLM-generated `STM_0` = 60 pairs**。cluster-level 表示需求级覆盖，pair-level 表示具体初始状态机制品的 repair attempt；60 pairs 不能写成 60 个独立需求，LLM 维度只用于 source STM bias、初始错误分布和修复难度辅助分析 [dec-q3][clm-denominator]。

| 层级 | 定义 | 用途 | 禁止写法 |
|---|---|---|---|
| `NL cluster` | 同一个自然语言需求及其 6 个 LLM 输出的父单元。 | requirement-level coverage、scope / time-level 统计。 | 把 6 个输出当成 6 个独立需求。 |
| `pair` | 一个 `<NL, STM_0>` 制品，通常对应一个 LLM-generated PlantUML pair。 | artifact-level A 层准入、repair attempt、failure / unknown ledger。 | 只按 cluster 报告而掩盖 source STM 差异。 |
| `LLM family` | 生成 `STM_0` 的来源模型。 | 辅助分析 source STM bias / 修复难度。 | 写成本论文核心贡献或独立泛化结论。 |

### 3.2 四层分母

R5.7.1 采用四层分母，避免失败样例从结果中消失 [dec-q4][dec-q7]。

| 分母层 | 定义 | 当前 `llms-emp` 事实 | 论文用途 |
|---|---|---|---|
| pre-registered pool | 预注册或拟纳入的完整样本池。 | 10 clusters / 60 pairs。 | 资源画像、失败与局限总账；不是 success 分母。 |
| scope pool | 按模型族和时间等级过滤后的 scope 上限。 | T0 = 8 clusters / 48 pairs；T0.5 = 1 cluster / 6 pairs；T1 = 1 cluster / 6 pairs。 | T0 是 headline main 的 pre-eligibility 上限；T0.5/T1 进附表 / caveat。 |
| evaluation-eligible pool | 通过 A 层 artifact-level gate、可进入 Better STM 判定的对象。 | 需 R5.7.2/R7 冻结；当前不能用 48 pairs 直接代替。 | 主结果候选分母。 |
| success / failure / unknown | eligible repair runs 中经语义裁决后的状态。 | 需 R6/R7/R8 真实运行；当前为空。 | repair effectiveness、failure analysis、limitation。 |

`T0 headline main = 8 clusters / 48 pairs` 只能表示 scope / pre-eligibility 上限，不能写成 evaluation-eligible denominator 或 Better STM success denominator [dec-q4][src-model-scope]。

### 3.3 T0 / T0.5 / T1 写法

| 时间等级 | R5.7.1 写法 | 可支撑 claim | 禁止外推 |
|---|---|---|---|
| T0 | 离散 FSM / HSM / 离散 UML-SysML statechart 子集，是 headline main scope 上限。 | 后续 T0 主表；仍需 A 层、repair run 和 Better STM 裁决。 | 不能自动等于最终 eligible / success。 |
| T0.5 | timer-like cue / tick / 离散 counter abstraction 的限定讨论。 | caveat / annotation / limited discussion；可说明周期 tick 可降级为计数器。 | 不支撑 timed automata、clock constraints 或 real-time verification。 |
| T1 | supplementary stress / limitation / negative evidence。 | appendix、stress、limitation。 | 不进入 T0 headline main result。 |

## 4. A 层硬准入

A 层是 **artifact-level 可评价性门槛**，不是 dataset-level 纳入标准 [dec-q1]。

| 对象 | A 层含义 | A-fail 去向 | A-pass 不能说明什么 |
|---|---|---|---|
| `STM_0` | 初始制品是否具备足够的结构、来源、诊断和证据链，能作为 repair 起点。 | readiness / failure / limitation ledger；不进 Better STM 主统计。 | 不代表初始模型语义正确。 |
| `STM_k` | 候选制品是否可解析、可审计、无基础阻塞，能进入 Better STM 语义裁决。 | repair failure / rollback / unknown ledger。 | 不代表候选更优。 |

A-pass 只说明“可被评价”，不说明“更好”。A-fail 样例必须保留在失败 / 准备度 / 局限台账中，不能静默删除；但它们不得进入 Better STM success 分母 [dec-q1][dec-q7]。

## 5. claim 类型与证据强度

R5.7.1 将论文 claim 分为五类 [dec-q2]。

| claim 类型 | 当前是否可写 | 最低证据 | 安全写法 | 禁止写法 |
|---|---:|---|---|---|
| task / scope claim | 可以 | story、scope、seed profile、model scope。 | “本文研究 `<NL, STM_0> -> STM_k` 反馈驱动修正任务”。 | 写成一轮式 `NL -> STM` 生成论文。 |
| readiness claim | 可以 | canonical / parse / inspect、seed readiness、转换画像。 | “seed pool 已进入可审计表示链路”。 | 写成 repair success。 |
| protocol / evaluation claim | 可以 | A 层、Better STM 定义、评价逻辑链、失败报告纪律。 | “我们定义可审计评价协议”。 | 写成方法已经产生更优状态机。 |
| repair effectiveness claim | 当前不可以 | R6/R7/R8 真实 repair run、change ledger、semantic adjudication、failure ledger。 | R5.7.1 只能写 future claim / evidence required。 | 写成功率、提升率、Better STM 主结果。 |
| limitation / negative evidence claim | 可以 | partial / failure / out-of-scope / unknown ledger、scope caveat。 | “T1 仅作 stress；T0.5 仅作 counter abstraction caveat”。 | 静默删除失败样例或把 caveat 混入主线成功。 |

## 6. conversion / normalization 与 repair gain 归因边界

所有改善必须按三阶段归因 [dec-q5][src-better-stm]。

```text
raw STM_0 -> canonical STM_0 -> STM_k
```

| 阶段差值 | 含义 | 是否计 repair gain |
|---|---|---:|
| raw `STM_0` -> canonical `STM_0` | conversion、normalization、SCXML export、representation lowering、人工/规则化准备。 | 否。只能计 readiness / representation bridge。 |
| canonical `STM_0` -> `STM_k` | 后续 repair loop 产生的候选变化。 | 只有通过 change-level attribution、NL 证据、无回归和 Better STM 判定后才可计。 |
| `.fcstm` parse / inspect ok | 可机检表示和工具可读性。 | 否。只能作为 A 层或 readiness 的支持证据。 |

R6/R7/R8 每次 run 必须保留 change / attribution ledger，至少记录 source artifact、canonical baseline hash、candidate hash、change type、证据来源、是否可计 repair gain 和禁止归因理由。无法归因时标为 `unknown`，不得计入主修复收益 [dec-q5][dec-q7]。

## 7. 客观指标与语义裁决

客观指标只能作为 supporting evidence，不能单独判 Better STM [dec-q6]。

R5.7.3 已将这一权限上限细化为 [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md)：每个指标必须声明 `metric_permission`、`denominator_layer`、`aggregation_level`、`ordering_relation`、`scope_applicability`、anti-gaming 风险和语义裁决接口；这些指标仍只进入 G0--G6 evidence bundle，不替代 G5 semantic adjudication。

| 指标层 | 例子 | 偏序方向示例 | 只能说明 | 不能单独说明 |
|---|---|---|---|---|
| hard gate | parse valid、schema valid、A-pass。 | true 优于 false。 | 制品可进入后续评价。 | 语义更好。 |
| structural element | state / transition / guard / action 覆盖。 | 预注册目标上 recall / precision 更高通常更好。 | 结构代理证据改善。 | 无需语义裁决的 Better STM。 |
| traceability | element-to-NL coverage、untraced additions。 | traced coverage higher；untraced additions fewer。 | 需求可追踪性改善。 | 新增语义一定正确。 |
| scenario / behavior | 场景 pass rate、trace mismatch。 | 预注册场景通过且关键回归不退化。 | 场景证据改善。 | 覆盖全部需求或消除 semantic drift。 |
| cost / stability | token、iteration、rollback、oscillation。 | 成本低、振荡少通常更好。 | 可用性 / 稳定性证据。 | 覆盖语义质量。 |

禁止 metric-only claims：parse ok、inspect ok、diagnostics fewer、总 F1 更高、scenario pass rate 更高、text similarity 更高、conversion success、低 token cost 等单项指标或总分，都不得单独支持 Better STM 或方法有效性结论 [dec-q6]。

## 8. failure / partial / unknown / out-of-scope 报告纪律

所有非成功状态都必须进入可审计台账，不能静默删除 [dec-q7]。

| 状态 | 定义 | 主表位置 | 附表 / ledger 位置 | 注意 |
|---|---|---|---|---|
| `failure` | 明确失败，例如 A-fail、repair loop 生成非法 STM、语义回归、回滚、不收敛。 | 不计 success。 | failure / rollback / limitation ledger。 | 可支撑方法边界和负证据。 |
| `partial` | 可进入流程但有 caveat / representation loss / candidate symptom。 | 若通过 A 层可进入后续评价。 | partial / caveat ledger。 | 不等于失败，也不等于成功。 |
| `unknown` | 证据不足、无法归因、语义裁决无法达成。 | 不计 success。 | unknown ledger。 | 不强行归类。 |
| `out_of_scope` | 不属于 T0 headline main，例如 T1 stress 或 excluded family。 | 不进 T0 主线。 | supplementary stress / limitation / related work。 | 不删除，不混入主线。 |

论文主表应报告 T0 主线 eligible / success；附表或 ledger 报告 partial、failure、unknown、T0.5、T1、A-fail 等完整边界信息。失败样例不能从 denominator 中消失 [dec-q7]。

## 9. R5.7.1 与后续阶段边界

R5.7.1 只冻结评价逻辑链与 claim boundary，不抢后续子 PR 的细节职责 [dec-q8]。

| 阶段 | 本文件提供什么 | 后续阶段负责什么 |
|---|---|---|
| R5.7.2 | A 层、scope、归因、failure reporting 和 Better STM 判定上游逻辑。 | 已在 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 与 [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md) 冻结 Better STM gate 链、三层输出模型、repair target taxonomy、语义裁决门和拒绝条件。 |
| R5.7.3 | 指标只能 supporting evidence、不能 metric-only verdict。 | 已在 [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md) 冻结客观代理指标框架、指标族、偏序方向、适用边界、anti-gaming 风险和 baseline 迁移边界。 |
| R5.7.4 | dry-run 的目标：验证标准可执行性，而不是 repair 效果。 | 用真实 / 准真实样例做静态 dry-run。 |
| R5.7.5 | R6/R7 必须继承的 claim boundary、分母、ledger 和 run record 要求。 | 合成可执行 handoff。 |
| R6/R7/R8 | repair gain 起点、ledger 字段、失败报告纪律和禁止外推。 | 实现/运行 repair loop、冻结协议、报告结果。 |

## 10. 决策台账

| 议题 ID | 状态 | 冻结结论 | 事实源 / 记录 | 下游影响 |
|---|---|---|---|---|
| Q1 | frozen | A 层是 artifact-level 可评价性门槛；A-fail 入台账但不进 Better STM 主统计。 | [dec-q1] | R5.7.2 A 层、R5.7.3 denominator、R7 eligibility。 |
| Q2 | frozen | claim 分为 task/scope、readiness、protocol/evaluation、repair effectiveness、limitation/negative evidence；当前不支持 repair effectiveness 主张。 | [dec-q2] | story claim 降级、R7/R8 结果写法。 |
| Q3 | frozen | `10 NL clusters × 6 LLM-generated STM_0 = 60 pairs`；cluster / pair 双层报告。 | [dec-q3][clm-denominator] | 指标分层、主结果表、source STM bias 辅助分析。 |
| Q4 | frozen | T0 是 headline main scope 上限；T0.5 是 tick/counter caveat；T1 是 supplementary stress。 | [dec-q4][src-model-scope] | scope README、taxonomy、R7 主表 / 附表。 |
| Q5 | frozen | raw -> canonical 不计 repair gain；repair gain 从 canonical `STM_0 -> STM_k` 开始，且需 change-level attribution。 | [dec-q5][src-better-stm] | R6 run record、R7/R8 归因表。 |
| Q6 | frozen | 客观指标只能 supporting evidence，不能单独判 Better STM。 | [dec-q6] | R5.7.2 语义裁决门、R5.7.3 指标框架。 |
| Q7 | frozen | failure / partial / unknown / out-of-scope 全部进入台账；partial 是 caveat candidate，unknown 不强行归类。 | [dec-q7] | R5.7.2 输出状态、R7/R8 failure ledger。 |
| Q8 | frozen | R5.7.1 不越界；R5.7.2--R5.7.5 分别负责判定细则、指标、dry-run 和 handoff。 | [dec-q8] | 后续 staged PR 职责边界。 |

## 11. 禁止外推清单

| 禁止写法 | 原因 | 安全写法 |
|---|---|---|
| “60 个独立需求”。 | 60 是 10 NL clusters × 6 LLM 输出的嵌套结构。 | “10 NL clusters and 60 LLM-generated initial STM artifacts”。 |
| “T0 48 pairs 是最终成功分母”。 | 48 只是 scope / pre-eligibility 上限。 | “T0 pre-eligibility scope contains 8 clusters / 48 pairs”。 |
| “T0.5 证明 timed automata 支持”。 | T0.5 只允许 tick / counter abstraction caveat。 | “timer-like cue under discrete event / counter abstraction”。 |
| “conversion / `.fcstm` 成功说明 repair 有效”。 | 表示桥只计 readiness。 | “conversion readiness / evaluability”。 |
| “指标总分更高就是 Better STM”。 | 客观指标不能替代语义裁决。 | “metric improvement as supporting evidence, subject to semantic adjudication”。 |
| “当前阶段已经证明方法有效”。 | 尚无真实 `STM_k` 与 repair run。 | “evaluation protocol and readiness are established; effectiveness remains to be evaluated”。 |
| “失败样例可以删除”。 | 会造成 cherry-picking。 | “failure / partial / unknown / out-of-scope ledger”。 |

## 审计附录：证据链与事实源

### A.1 上游事实源清单

| 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-status] | `paper_stm_repair_status` | [../STATUS.md](../STATUS.md) | md | 当前尚未运行真实 repair loop、尚无 `STM_k` 或 Better STM 主结果。 | §1、§6、§7。 |
| [src-model-scope] | `r5_6_model_scope` | [../story/model_scope.md](../story/model_scope.md) | md | T0/T0.5/T1、模型族、主线 scope、禁止外推。 | §1–§6；审计附录。 |
| [src-r56-handoff] | `r5_6_to_r5_7_handoff` | [scope/r5_6_to_r5_7_handoff_constraints.md](./scope/r5_6_to_r5_7_handoff_constraints.md) | md | R5.7 必须继承的硬约束、candidate-only 纪律。 | R56-H0–H7、§5。 |
| [src-better-stm] | `better_stm_definition` | [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) | md | Better STM 原五条件、三阶段归因、parse / executable 不等于 Better；当前已由 R5.7.2 G0–G6 gate 链细化。 | §2–§12。 |
| [src-r572-better] | `r572_better_stm_definition` | [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) | md | R5.7.2 Better STM gate 链、三层输出模型、硬拒绝、T0.5 caveat、semantic gate。 | §1–§12。 |
| [src-r572-taxonomy] | `r572_repair_target_taxonomy` | [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md) | md | R5.7.2 repair target taxonomy、11 字段合同、五级 repair_action_allowed、candidate-only 纪律。 | §1–§7。 |
| [src-case] | `llms_emp_case_matrix` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | jsonl | 60 pair、conversion status、time level、story role、parse / inspect / canonical status。 | JSONL rows；`raw_pair_id`、`nl_cluster_id`、`conversion_status`、`time_level`。 |
| [src-cluster] | `llms_emp_cluster_profiles` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) | jsonl | 10 cluster、time level、structure family、story role。 | JSONL rows；`nl_cluster_id`、`time_level`、`structure_family`。 |
| [src-partial-ledger] | `llms_emp_partial_attribution` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | jsonl | partial attribution、candidate-only 与 pipeline artifact 区分。 | JSONL rows；`primary_attribution`、`r5_7_candidate_only`。 |
| [src-r552-report] | `r5_5_2_recovery_report` | [../reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](../reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md) | md report | 当前 `llms-emp` 16 converted / 44 partial / 0 blocked；blocked recovery 不计 repair gain。 | 核心结论与审计附录。 |
| [src-profile-report] | `llms_emp_main_seed_profile` | [../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md) | md report | 10 cluster × 6 LLM 历史画像、行为特征矩阵、loss code。 | §1.1–§1.3、§7；当前状态数字以 [src-r552-report] 为准。 |
| [dec-q1] | `r571_q1_decision` | [PR #139 Q1 comment](https://github.com/HansBug/research_ideas/pull/139#issuecomment-4853665152) | github-comment | A 层硬准入决策来源。 | 用户确认 A1+B1+C1+D1。 |
| [dec-q2] | `r571_q2_decision` | [PR #139 Q2 comment](https://github.com/HansBug/research_ideas/pull/139#issuecomment-4853753946) | github-comment | claim 类型决策来源。 | 五层 claim；当前不支持 repair effectiveness。 |
| [dec-q3] | `r571_q3_decision` | [PR #139 Q3 comment](https://github.com/HansBug/research_ideas/pull/139#issuecomment-4853849851) | github-comment | cluster / pair 口径决策来源。 | 10×6 嵌套结构。 |
| [dec-q4] | `r571_q4_decision` | [PR #139 Q4 comment](https://github.com/HansBug/research_ideas/pull/139#issuecomment-4863809909) | github-comment | T0/T0.5/T1 分母与 scope 决策来源。 | T0 主线、T0.5 counter caveat、T1 stress。 |
| [dec-q5] | `r571_q5_decision` | [PR #139 Q5 comment](https://github.com/HansBug/research_ideas/pull/139#issuecomment-4863831930) | github-comment | repair gain 归因边界决策来源。 | raw -> canonical 不计 repair gain。 |
| [dec-q6] | `r571_q6_decision` | [PR #139 Q6 comment](https://github.com/HansBug/research_ideas/pull/139#issuecomment-4863915870) | github-comment | 客观指标与语义裁决关系决策来源。 | 指标只能 supporting evidence。 |
| [dec-q7] | `r571_q7_decision` | [PR #139 Q7 comment](https://github.com/HansBug/research_ideas/pull/139#issuecomment-4863949843) | github-comment | failure / partial / unknown / out-of-scope 报告纪律来源。 | 全部进入台账。 |
| [dec-q8] | `r571_q8_decision` | [PR #139 Q8 comment](https://github.com/HansBug/research_ideas/pull/139#issuecomment-4863982252) | github-comment | R5.7.1 与后续阶段边界来源。 | R5.7.2--R5.7.5 分工。 |

### A.2 Claim-evidence map

| 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-denominator] | `R571-C1` | `llms-emp` 是 10 NL clusters × 6 LLM-generated `STM_0` = 60 pairs。 | count | [src-case] rows；[src-cluster] rows。 | [cmd-r571-counts] | high | 不能写成 60 个独立需求。 |
| [clm-current-status] | `R571-C2` | 当前 `llms-emp` 为 16 converted / 44 partial / 0 blocked，60/60 canonical / parse / inspect ok。 | count | [src-case] fields `conversion_status`、`canonical_status`、`parse_status`、`inspect_status`。 | [cmd-r571-counts] | high | 只说明 readiness，不说明 repair success。 |
| [clm-t0-scope] | `R571-C3` | T0 headline main scope 上限是 8 clusters / 48 pairs；T0.5 与 T1 各 1 cluster / 6 pairs。 | count / classification | [src-case]、[src-cluster] fields `time_level`。 | [cmd-r571-counts] | high | T0 上限不是最终 eligible / success denominator。 |
| [clm-no-repair-gain] | `R571-C4` | conversion / normalization / `.fcstm` inspect success 不计 repair gain。 | prohibition | [src-better-stm] §3–§5；[src-r56-handoff] R56-H5。 | 人工复验 + [cmd-r571-counts] | high | R6/R7 仍需真实 change ledger。 |
| [clm-no-effectiveness-yet] | `R571-C5` | 当前不能写 repair effectiveness、Better STM 成功率或强泛化 claim。 | prohibition | [src-status] §1、§6；[dec-q2]。 | 人工复验 | high | 未来 R6/R7/R8 可在证据闭合后升级。 |
| [clm-failure-ledger] | `R571-C6` | failure / partial / unknown / out-of-scope 必须进入台账，不能静默删除。 | protocol | [dec-q7]、[src-model-scope] §6。 | 人工复验 | high | R7/R8 需落到正式 run record / ledger schema。 |
| [clm-r572-gate] | `R571-C7` | R5.7.2 已把 Better STM 细化为 G0–G6 gate、三层输出模型和 repair target taxonomy，但仍不产生 repair effectiveness 主张。 | protocol | [src-r572-better]、[src-r572-taxonomy]。 | 人工复验 | high | 只是协议冻结，不是 `STM_k` 或 success rate。 |

### A.3 复验命令

```bash
# [cmd-r571-counts]
python - <<'PY'
import json, collections, pathlib
base = pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair')
case = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
clusters = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl').read_text().splitlines() if l.strip()]
print('pairs', len(case), 'clusters', len({r['nl_cluster_id'] for r in case}))
print('conversion_status', collections.Counter(r['conversion_status'] for r in case))
print('canonical_status', collections.Counter(r['canonical_status'] for r in case))
print('parse_status', collections.Counter(r['parse_status'] for r in case))
print('inspect_status', collections.Counter(r['inspect_status'] for r in case))
print('pair_time', collections.Counter(r['time_level'] for r in case))
print('cluster_time', collections.Counter(r['time_level'] for r in clusters))
print('story_role', collections.Counter(r['r5_6_story_role'] for r in case))
PY
```

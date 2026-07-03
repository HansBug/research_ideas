# experiment_design/SUMMARY.md — 实验设计总账

## 1. 当前状态

本目录已按 R5.5.1 路径重构为 `scope/`、`quality_model/`、`eligibility/`、`protocols/`、`metrics/` 五个子路径，并在 R5.7.1 新增 [evaluation_logic.md](./evaluation_logic.md) 作为评价逻辑链与主张边界事实源。R5.7.2 已在 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 与 [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md) 冻结 Better STM gate 链、三层输出模型、硬拒绝边界、语义裁决接口和修复目标分类合同；`scope/` 已新增 R5.5 handoff 草案 [scope/2026-06-29-17-33-35-r5-5-scope-handoff.md](./scope/2026-06-29-17-33-35-r5-5-scope-handoff.md)，并在 R5.6 新增 [../story/model_scope.md](../story/model_scope.md) 与 [scope/r5_6_to_r5_7_handoff_constraints.md](./scope/r5_6_to_r5_7_handoff_constraints.md)，冻结 story-level model scope 和 R5.7 交接约束：当前有样例支撑的主线限于 T0 离散 FSM/HSM/离散 UML-SysML statechart 子集，EFSM-lite 不进入 headline，只作为当前 0 独立样例的 future taxonomy candidate / 语义维度标签，T0.5 只作 caveat，Digital Camera / T1-ish 只作 supplementary stress。eligibility、protocols 仍只冻结职责入口；metrics 已在 R5.7.3 冻结客观代理指标框架 v0；R5.7.4 已在 [repair_target_adjudication/README.md](./repair_target_adjudication/README.md) 与 [../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md](../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md) 中完成四例静态裁决 dry-run，但不伪造尚未完成的主实验协议、最终阈值或真实效果；R5.7.1--R5.7.4 均不报告 repair effectiveness、`STM_k` 或 Better STM 成功率。

## 1.1 R5.7.1 评价逻辑链冻结结论

| 主题 | 冻结结论 | 后续入口 |
|---|---|---|
| claim 类型 | 区分 task / scope、readiness、protocol / evaluation、repair effectiveness、limitation / negative evidence；当前阶段不能写 repair effectiveness。 | [evaluation_logic.md](./evaluation_logic.md) |
| 数据单元 | `llms-emp` 写作口径是 10 NL clusters × 6 LLM-generated `STM_0` = 60 pairs；cluster 表示需求级覆盖，pair 表示 artifact-level repair attempt。 | [evaluation_logic.md](./evaluation_logic.md)、[../story/model_scope.md](../story/model_scope.md) |
| 分母纪律 | T0 = 8 clusters / 48 pairs 只是 headline scope / pre-eligibility 上限；最终 eligible 和 success 分母等 R7/R8 冻结。 | [evaluation_logic.md](./evaluation_logic.md)、[scope/README.md](./scope/README.md) |
| 归因边界 | raw -> canonical 的 conversion / normalization / `.fcstm` inspect 收益不计 repair gain；repair gain 只能从 canonical `STM_0 -> STM_k` 且经 change ledger 裁决后计算。 | [evaluation_logic.md](./evaluation_logic.md)、[quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) |
| 客观指标 | 客观指标只能作为 supporting evidence；任何单一指标或总分都不能替代 NL-grounded semantic adjudication。 | [evaluation_logic.md](./evaluation_logic.md)、[metrics/README.md](./metrics/README.md) |
| 失败报告 | failure / partial / unknown / out-of-scope 必须进入台账；partial 是带 caveat 的可评价候选，不等于失败也不等于成功。 | [evaluation_logic.md](./evaluation_logic.md)、[eligibility/README.md](./eligibility/README.md) |

## 1.2 R5.7.2 Better STM 与 repair target 冻结结论

| 主题 | 冻结结论 | 后续入口 |
|---|---|---|
| Better 比较对象 | raw `STM_0` 是 source evidence；直接比较对象是 canonical `STM_0` vs `STM_k`；repair gain 从 canonical `STM_0 -> STM_k` 开始。 | [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) |
| gate 链 | Better STM 判定采用 G0 scope、G1 A gate、G2 attribution、G3 no-regression、G4 improvement、G5 semantic、G6 reporting。 | [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) |
| 输出模型 | 采用 `scope_routing_status`、`run_validity_status`、`better_adjudication_outcome` 三层输出；不可归因进入 `protocol_or_provenance_invalid`，不作为普通 Better outcome。 | [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md)、[eligibility/README.md](./eligibility/README.md) |
| repair target taxonomy | 冻结 11 类一级 target、11 字段合同、实例级单值 `repair_action_allowed` 与“表示症状 -> 候选语义问题 -> 确认修复目标 -> 允许修复动作 -> Better 证据影响”链路。 | [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md) |
| guard/event/action folding | `condition_like_label_lowered_as_event` 等现象只能先作 candidate-only；必须回到 `NL + raw STM_0 + canonical STM_0 + evidence bundle` 裁决，不能批量写成 confirmed defect。 | [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md)、[protocols/README.md](./protocols/README.md) |
| T0.5 / T1 | T0.5 tick / counter 可作 caveat 层讨论；T1 只作 stress / limitation；二者都不进入 T0 headline success。 | [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md)、[scope/README.md](./scope/README.md) |
| 指标权限 | 客观指标只作 supporting evidence；R5.7.3 只能在该权限上限内定义指标族和偏序方向。 | [metrics/README.md](./metrics/README.md) |
| 规则修订 | 后续规则 / 指标修订必须由 R5.7.4 或 R7 真实 dry-run findings 驱动；无 finding 的修改只能标 provisional。 | [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) |


## 1.3 R5.7.3 客观代理指标冻结结论

| 主题 | 冻结结论 | 后续入口 |
|---|---|---|
| 指标权限 | 冻结五级 `metric_permission`：`hard_gate / supporting_evidence / trigger_only / report_only / forbidden`；任何指标都不能单独产生 Better verdict。 | [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md) |
| entry schema | 每个指标必须声明指标族、gate、分母、聚合层、reference、偏序、scope、headline 权限、证据源、风险、语义裁决、禁止外推、冻结状态和下游 owner。 | [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md) |
| 指标族 | 冻结 readiness、provenance、diagnostics、structural element、traceability、scenario behavior、semantic target closure、cost stability、baseline/textual background 等 v0 指标族。 | [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md) |
| gate matrix | 指标必须落到 R5.7.2 的 G0--G6 gate × metric matrix，不另起 overall score / weighted score。 | [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md)、[quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) |
| reference / 分母 | 不设统一 gold STM；P/R/F1 只在有合法 reference set 时使用；target closure、scenario、run、scope 不得跨层混用分母。 | [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md) |
| anti-gaming | 显式记录 semantic deletion、guard/action/event folding、over/under repair、trace loss、conversion laundering、hierarchy loss、scenario overfitting 等风险。 | [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md) |
| baseline 迁移 | `llms_emp` 与 Structure/Event 只作为指标思想来源；不迁移源论文数值，不把文本相似度、compile/pass@k 或 conversion success 写成质量结论。 | [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md) |
| 仍未冻结 | numeric thresholds、statistical test、effect size、final eligibility、primary/secondary endpoints、success denominator 和真实 repair effectiveness 仍由 R7/R8 冻结。 | [metrics/README.md](./metrics/README.md) |

## 1.4 R5.7.4 静态裁决 dry-run 结论

| 主题 | 冻结结论 | 后续入口 |
|---|---|---|
| dry-run 定位 | R5.7.4 只验证 taxonomy 与 metric permission 能否消费真实 `llms-emp` 样例；不生成 `STM_k`，不产生正式 `valid_run` 或 `better`。 | [repair_target_adjudication/README.md](./repair_target_adjudication/README.md)、[../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md](../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md) |
| 四例覆盖 | 覆盖 `0000` T0 condition-like HSM、`0001` T0 low-noise FSM、`0045` T0.5 Microwave caveat、`0018` T1 Digital Camera stress。 | [repair_target_adjudication/README.md](./repair_target_adjudication/README.md) |
| R6/R7 handoff | R6/R7 前必须补齐 `STM_k`、change ledger 和 canonical / `.fcstm` evidence bundle；0001 / 0018 当前缺 standalone `.fcstm`，0000 / 0045 selected hash 与 seed-sweep hash 不同。 | [../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md](../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md) |

## 2. 研究问题草案

下表来自重构前 `experiment_design/README.md` 的上游实验约束，仍是草案，不是正式协议。

| RQ | 问题 | 需要的证据 | 安全降级写法 |
|---|---|---|---|
| RQ1 | 初始 `STM_0` 的主要缺陷类型是什么？ | parse / semantic / guard / action / hierarchy / behavior 缺陷统计 | 若样本少，写成 pilot characterization |
| RQ2a | 不同反馈来源能发现哪些结构、语义或行为问题？ | diagnostics 类型、feedback source、未闭合缺陷 | 若覆盖有限，写成 feedback coverage 分析 |
| RQ2b | 反馈输入修正循环后，哪些缺陷能被关闭，哪些会引入回归或振荡？ | 修复前后诊断、rejected repair、rollback、oscillation、non-convergence | 若不稳定，重点报告失败模式 |
| RQ3 | 场景 / 仿真反馈是否发现静态检查难以发现的行为缺陷？ | scenario pass/fail、trace mismatch、simulation-only defects | 若证据弱，写为补充反馈来源 |
| RQ4 | 自动修正是否产生相对更优 STM？ | G0–G6 gate 逐项台账、canonical `STM_0` vs `STM_k`、人工 / 结构化裁决、回归检查 | 任一 gate 失败，不计入 Better STM，只报告失败 / partial / unknown / 局限 |
| RQ5 | seed 来源如何影响修正效果？ | prior artifact、弱 prompt、旧模型、学生 / 人工 seed 分层 | 来源不足时，降级为探索性分析 |
| RQ6 | 转换规范化风险是什么？ | 转换成功率、不可映射字段、转换前 / 后 / 修正后诊断 | 若转换器很薄，写为 artifact limitation |

RQ1--RQ3 支撑“结构化反馈有什么用”；RQ4 支撑或否定 Better STM 主结果；RQ5 支撑来源与泛化讨论；RQ6 防止转换收益与修正收益混淆。

## 3. 评价门顺序

评价门必须先于真实修正预演冻结。不能先看修正结果，再修改指标、阈值、主结果纳入规则或统计表字段。

```text
资产盘点 -> 样本冻结 -> 转换合同 -> 诊断/场景/评价门 v0 -> 修正循环预演 -> 正式协议与对照矩阵 -> 论文写作
```

### 3.1 评价门至少冻结什么

| 项 | 说明 |
|---|---|
| 诊断类别 | parse / semantic / design / scenario 等最小分类 |
| 场景 / 回归套件 | 预演使用的确定性场景和回归入口 |
| 评价量表草案 | 与 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 的 G0–G6 gate 和 semantic adjudication 对应 |
| 主结果纳入规则草案 | 哪些 run 进入 pilot，哪些只能作失败案例 |
| 统计表骨架 | 后续正式协议继承，不允许被结果任意重写 |

### 3.2 正式协议至少冻结什么

| 项 | 说明 |
|---|---|
| 最终 RQ 与指标 | 继承评价门，不得因结果好坏任意替换 |
| 对照 / 消融 | no-repair seed、regenerate-from-NL、no structured feedback、可运行 repair baseline、转换器-aware analysis |
| 人工裁决协议 | 裁决者、blindness、冲突处理、记录方式 |
| 主结果 eligibility | schema-invalid、replay-invalid、partial run、provider failure 的纳入 / 排除规则 |
| 降级写法 | 效果有限、样本不足、失败率高时的安全表述 |

## 4. 未完成项

1. `scope/` 已有 R5.6 story-level model scope 与 R5.7 handoff constraints，但尚未冻结最终样本层、最终 RQ 版本或主实验 protocol。
2. `quality_model/` 已冻结 R5.7.2 Better STM gate 与 repair target taxonomy v0，并已由 R5.7.4 四例静态 dry-run 做可执行性校验；正式 target closure 仍需 R6/R7。
3. `eligibility/` 已接收 R5.7.1 A 层 artifact-level gate 和 R5.7.2 三层输出方向，但尚未冻结 R7 run eligibility、failure handling 和 provider drift 正式协议。
4. `protocols/` 已接收 R5.7.1 change ledger / failure ledger 与 R5.7.2 semantic adjudication evidence bundle 要求，但尚未冻结真实 LLM 修正、对照、人工裁决或回滚协议。
5. `metrics/` 已冻结 R5.7.3 客观代理指标框架 v0，但尚未冻结 numeric thresholds、statistical test、effect size、final eligibility、primary / secondary endpoints、最终成功分母或真实 repair effectiveness。

## 5. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-07-03 23:44:12 | R5.7.4 新增 [repair_target_adjudication/README.md](./repair_target_adjudication/README.md) 与 [../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md](../reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md)，完成四例静态裁决和 metric permission dry-run；该更新不代表 repair loop 已运行。 |
| 2026-07-03 21:18:25 | R5.7.3 新增 [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md)，冻结客观代理指标框架 v0、五级指标权限、entry schema、G0--G6 gate matrix、分母 / reference / anti-gaming 纪律和 baseline 迁移边界；该更新不代表 repair loop 已运行。 |
| 2026-07-03 02:16:16 | R5.7.2 新增 [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md)，并将 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 从五条最低必要条件扩展为 Better STM gate 链、三层输出模型、硬拒绝边界、T0.5 caveat、指标权限和 semantic adjudication 接口；该更新不代表 repair loop 已运行。 |
| 2026-07-02 17:02:42 | R5.7.1 新增 [evaluation_logic.md](./evaluation_logic.md)，冻结评价逻辑链、claim 类型、分母纪律、A 层准入、归因边界、客观指标位置、失败报告纪律和 R5.7.2--R5.7.5 下游接口；该更新不代表 repair loop 已运行。 |
| 2026-06-30 14:46:44 | R5.6 新增并补强 [../story/model_scope.md](../story/model_scope.md) 与 [scope/r5_6_to_r5_7_handoff_constraints.md](./scope/r5_6_to_r5_7_handoff_constraints.md)，冻结 model scope / claim boundary、状态机抽象定义、Better STM 核心判据与 R5.7 继承约束；该更新不代表 repair loop 已运行。 |
| 2026-06-29 19:55:45 | R5.5.2 更新当前 scope 事实：`llms-emp` 当前 16 converted / 44 partial / 0 blocked；T0 主线与 Digital Camera supplementary stress 不变。 |
| 2026-06-29 17:33:35 | 新增 [scope/2026-06-29-17-33-35-r5-5-scope-handoff.md](./scope/2026-06-29-17-33-35-r5-5-scope-handoff.md)，把 R5.5 `proceed_with_supplementary` scope decision 落到 experiment design 路径。 |
| 2026-06-29 01:54:30 | 按 R5.5.1 路径重构建立 `experiment_design/` 三件套和五个子路径，将 Better STM 定义移动到 `quality_model/`。 |

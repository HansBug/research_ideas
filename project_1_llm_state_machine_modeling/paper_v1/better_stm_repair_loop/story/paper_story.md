# Paper Story：反馈驱动状态机模型修正

## 1. Working title（草案）

中文草案：**面向控制系统需求的反馈驱动状态机模型修正**

英文草案：**Feedback-Driven Repair of State-Machine Models from Natural-Language Requirements and Initial Artifacts**

> 标题草案不得包含 `fcstm`、`pyfcstm` 或 “new DSL”。最终标题等 R7 论文骨架阶段再定。

## 2. One-sentence thesis

给定控制系统自然语言需求和一个初始状态机 `STM_0`，本文研究能否通过无人化的确定性诊断、轻量形式化 / 静态检查、场景仿真反馈和回归约束，自动提出、验收或回滚候选修复，从而得到相对于同一 `STM_0` 更可检查、更可执行且不语义退化的 `STM_k`。

## 3. Task boundary

| 项 | R0 冻结口径 |
|---|---|
| 输入 | 自然语言需求 `NL` + 初始状态机 `STM_0`。 |
| 输出 | 修正后的候选 `STM_k`，以及诊断、场景、修正、验收、拒绝和回滚证据。 |
| 方法内范围 | `STM_i -> diagnostics / feedback -> repair candidate -> regression / scenario checks -> accept / reject / rollback -> STM_{i+1}`。 |
| 方法外范围 | `NL -> STM_0` 的种子构造；只记录来源与配置，不作为主贡献。 |
| 人的角色 | 人类可参与 benchmark、参考裁决与最终审计；修正运行内部不作为人在回路方法。 |
| 评价对象 | 相对同一 `STM_0` 的 `STM_k`，不是“从零生成最佳 STM”。 |

详细边界见 [task_boundary.md](./task_boundary.md)。

## 4. Problem gap

已有工作已经覆盖多种自然语言到 FSM / UML state machine / SysML behavior / Umple / Mermaid / TTool 等状态机或行为模型生成路线。因此，继续把论文主线写成“首个 `NL -> STM` 生成方法”风险很高，也不符合 2026-06-12 导师定调。

新的 gap 是：即使能够得到一个初始状态机，实际研究和工程使用仍需要面对状态缺失、迁移错误、guard/action 不一致、不可执行、场景行为偏差、修复回归和语义漂移等问题。仅生成一个描述性模型不足以支撑可审计改进；需要把状态机制品规范化到可机检、可执行的形式，并围绕诊断、仿真和回归构造自动修正协议。

## 5. Technical challenge

1. **初始状态机来源异质**：既有工作、弱 prompt、旧模型或人工 / 学生种子可能具有不同格式、语义粒度和缺陷类型。
2. **诊断减少不等于语义更好**：修正可能通过删除需求行为、过拟合场景或改坏 guard/action 来降低错误数。
3. **反馈来源异构**：parse / semantic / design diagnostics、场景仿真、回归检查和人工裁决关注不同失败模式，需要明确接受 / 拒绝规则。
4. **转换与修正收益必须拆分**：格式转换、人工规范化或 seed 清洗带来的变化不能算作 repair loop 的贡献。
5. **失败本身是重要结果**：拒绝修复、回滚、振荡、不收敛和语义漂移都必须作为评测对象，而不是被最终成功样例掩盖。

## 6. Method insight

核心洞察不是“更复杂的 prompt 能生成更好的状态机”，而是：**一旦初始状态机被约束为可机检、可执行、语义边界明确的制品，确定性诊断和场景仿真就能转化为结构化反馈，从而把 LLM 的开放式修改限制在可验收、可回滚的修正循环内。**

## 7. Method stages（草案）

| 阶段 | 作用 | 所属后续 PR |
|---|---|---|
| Seed / artifact intake | 记录 `NL`、原始状态机制品、来源、格式和转换风险。 | R1/R2 |
| Minimal conversion / normalization | 将纳入样本转换为内部可检查、可执行表示；记录信息损失。 | R3 |
| Diagnostics and scenario feedback | 运行解析、语义、设计和场景 / 仿真检查；冻结评价门。 | R4 |
| Automated repair loop | 生成候选修复，执行回归检查，接受、拒绝或回滚。 | R5 |
| Evaluation and ablation | 比较 `STM_0`、`STM_k`、重生成、自修正和有限可运行基线。 | R6 |
| Manuscript skeleton | 把 story、方法、实验和局限写成论文骨架。 | R7 |

## 8. Contribution directions（待证据闭合）

| 贡献方向 | 当前可写程度 | 需要后续证据 |
|---|---|---|
| 任务定义 | 可以写：定义 `<NL, STM_0> -> Better STM` 的反馈驱动修正任务。 | R0/R6 进一步固定评价协议。 |
| 可机检、可执行表示的反馈载体作用 | 可以写为必要铺垫；不能写成新 DSL 贡献。 | R3/R4 展示诊断和仿真接口如何工作。 |
| 自动修正协议 | 可以写为方法设计；不能写“必然提升”。 | R5/R6 的接受、拒绝、回滚和失败统计。 |
| 评价协议与对照矩阵 | 可以规划；不能提前报结果。 | R4/R6 冻结指标、阈值、样本和对照。 |

## 9. Claims to make now

1. 本文研究对象是 `<NL, STM_0> -> STM_k` 的反馈驱动状态机修正，而不是单纯 `NL -> STM` 生成。
2. `NL -> STM_0` 是 seed construction / baseline source / related work，不是主贡献。
3. 语义增强、可机检、可执行状态机表示是支撑反馈循环的必要实验载体。
4. `Better STM` 必须通过预注册条件操作化，并且可以被反例推翻。
5. 旧 baseline 资产需要重排为 seed source、converter pressure、error taxonomy、limited comparison 和 related work evidence。

## 10. Claims to be careful about

1. “形式化反馈”：当前更安全写法是轻量形式化 / 静态检查 / deterministic diagnostics，而不是完整 model checking。
2. “自动化”：仅限定 repair run 内无人化；benchmark、reference、adjudication 和 final audit 仍可有人类参与。
3. “改进”：必须相对于同一转换后 `STM_0`，并满足 [better_stm_definition.md](../experiment_design/better_stm_definition.md) 的条件。
4. “baseline”：不能把不可运行、不可转换或数据缺失的 prior work 强行写成 direct executable baseline。

## 11. Claims to avoid

- 首个或最强 `NL -> STM` 方法。
- 提出新 DSL / `fcstm` 是论文核心贡献。
- 完整形式化验证、soundness 或 model checking guarantee。
- 自动修正一定提升质量或 outperform baseline。
- baseline 已经被排除，或无需对照 / 消融。
- run record、工程留痕或框架拆分本身支撑论文方法贡献。

## 12. Reviewer risks

| 风险 | 等级 | R0 应对 |
|---|---:|---|
| 旧 `NL -> STM` story 回流 | C | 在 [task_boundary.md](./task_boundary.md) 和 [claim_evidence_map.md](./claim_evidence_map.md) 中明确禁止。 |
| `fcstm` 被误写成新 DSL 贡献 | C | 在 [terminology_policy.md](./terminology_policy.md) 中设置 forbidden wording。 |
| 只报成功、不报失败 | I | 在 `Better STM` 定义中纳入拒绝、回滚、振荡和不收敛。 |
| converter 改善冒充 repair 改善 | I | 后续 R3/R6 必须记录转换前、转换后、修正后三阶段台账。 |
| R0 提前写结果型 claim | I | 本文件只写“研究 / 评估 / 探究”，不写结果。 |

# S0b 方向冻结：Path-1 第一篇论文方向冻结

本文档是 PR-S0 / S0b 的方向冻结产物，用于把 S0a 已通过的 story 门禁落实为后续写作、样本、oracle、基线、实验和投稿路线的共同约束。它不是最终论文初稿，也不是实验结果报告；所有结果型表述仍必须等待后续 G3/G5 证据闭合。

上游真源：

- S0a story：[`story/paper_story.md`](./story/paper_story.md)
- 术语边界：[`story/terminology_policy.md`](./story/terminology_policy.md)
- 论断门禁：[`story/claim_evidence_map.md`](./story/claim_evidence_map.md)
- 基线总账：[`baselines/SUMMARY.md`](./baselines/SUMMARY.md)
- 投稿出口背景门禁：[`story/venue_readiness_gate.md`](./story/venue_readiness_gate.md)
- 执行计划：[`experiment_design/execution_plan.md`](./experiment_design/execution_plan.md)

## 1. 冻结后的论文方向

### 1.1 一句话方向

本文研究自然语言控制系统需求到状态机模型生成任务中，是否可以把 LLM 输出约束到**可机检、可执行的状态机表示**，并用确定性诊断、场景级仿真反馈和结构化修复决策构成可评估的生成-反馈-修复闭环。

这句话是研究方向，不是实验结论。它只能支持“研究 / 分析 / 评估”这类问题表达，不能在实验闭合前改写成质量提升、优于现有工作或已达到投稿级质量的结论。

### 1.2 当前最安全的工作标题候选

候选英文标题只作为 S5 写作输入，不代表最终投稿标题：

> Executable Feedback for LLM-Based State-Machine Modeling from Control-System Requirements

标题刻意避免 `fcstm` / `pyfcstm` / DSL 命名，也避免暗示首创性或结果优势。

## 2. 研究范围：本文做什么 / 不做什么

### 2.1 输入与输出范围

- **输入**：自然语言控制系统需求、系统说明或可抽取控制逻辑的文本片段；主实验样本后续由 S2 冻结。
- **输出**：可解析、可诊断、可仿真的状态机模型，重点覆盖 states、transitions、guards、actions、variables、hierarchical states 等组件维度。
- **反馈信号**：解析 / 语义 / 设计诊断，场景级仿真通过或失败、轨迹、修复请求、接受或拒绝决策、差异和修复后回归检查。
- **任务定位**：面向控制系统需求的 LLM 状态机建模，不是通用软件建模自动化，也不是完整形式化验证。

### 2.2 支持范围

- 单控制器或主监督控制器。
- FSM / EFSM / HSM 风格的状态-迁移模型。
- 可通过确定性解析、语义检查、设计诊断和仿真执行形成反馈的 T0 或弱时间依赖样本。
- 可用人工组件级裁决评估状态、迁移、guard、action、变量和行为证据质量的样本。

### 2.3 明确排除范围

- 并行区域、历史伪状态、大规模时间自动机、分布式多控制器协议证明。
- 完整 LTL / CTL / BMC / 定理证明 / 工业认证级验证。
- 把提示工程、RAG、few-shot、agent 编排或具体 LLM provider 包装成论文主贡献。
- 把工程过程材料写进方法或贡献主线；必要复现信息只在制品、附录或实验披露中按投稿出口要求保留。

## 3. 四个必须正面处理的最接近工作

S1a 已经证明，本文不能再依赖“LLM 从自然语言生成状态机”或“反馈闭环首创”这类 novelty。后续引言、相关工作、贡献和审稿回应必须正面承认下列四个最接近工作：

| 最接近工作 | 已覆盖能力 | 对本文方向的约束 | 本文可保留的边际问题 |
|---|---|---|---|
| Structure/Event SMF | 同任务自然语言到 UML 状态机，结构化提示，事件 / 结构驱动建模，组件级评价 | 禁止把“自然语言到状态机 / UML SM 生成”写成空白领域 | 研究可执行目标表示作为确定性诊断与仿真反馈的实验底座 |
| LLMs for EMP | SysML 行为模型生成，规则 / 人工检查反馈，再生成，人工评审 | 禁止声称行为模型反馈闭环首创 | 区分确定性诊断、场景仿真与结构化修复决策的组合与消融 |
| TTool-AI | 自然语言到 SysML/TTool，JSON / 语法 / 约束工具反馈，TTool 工件 | 禁止声称工具反馈首创，也不能误写为既有工作没有工具反馈 | 把解析 / 语义 / 设计诊断作为受控闭环中的一种可复核反馈信号 |
| Designing FSMs | 合成自然语言到 CSV DFSM / Mealy，oracle、区分轨迹、checking-sequence repair | 禁止声称轨迹 / oracle repair 首创 | 研究场景候选生成、确定性仿真执行和结构化修复决策的组合 |

后续 S1b 必须把这四项放在相关工作第一层；S3 至少尝试其中一个同样本近似基线计划，若不可行则必须给出可复核降级理由。

## 4. 贡献边界

### 4.1 允许保留的贡献方向

以下是 S0b 冻结后的允许方向，进入论文前仍需由 [`story/claim_evidence_map.md`](./story/claim_evidence_map.md) 控制证据状态：

1. **可机检 / 可执行状态机表示作为反馈评估底座**：不是提出新建模语言，而是把输出约束到能被确定性工具解析、诊断和执行的表示。
2. **确定性诊断反馈**：把解析、语义、设计诊断作为可复核反馈信号纳入建模 / 修复闭环，并在消融中评估其边际作用。
3. **场景级仿真反馈**：由 LLM 生成场景候选，由确定性仿真器执行，得到通过 / 失败与轨迹作为行为证据。
4. **结构化修复决策**：用 fix request、accept/reject、diff 和回归检查组织修复过程，避免把无约束 regenerate 当成 repair 证据。
5. **基线感知的受控评估**：用冻结样本、人工组件级裁决、B0-B5 / EXT 消融和最接近工作分层，避免不可比横向排名。

### 4.2 明确禁止的贡献写法

下列写法禁止进入标题、摘要、引言、贡献条目、图注和面向审稿人的总结；只允许在策略文档或禁用论断表中作为反例出现：

- `first NL-to-STM` / `first LLM state-machine generation`
- `first feedback loop` / `first tool feedback` / `first trace repair`
- `new DSL` / `new modeling language` / `FCSTM as the contribution`
- `we improve model quality` / `we outperform prior work` / `we achieve better performance` 等未由主实验支持的结果提升论断
- “prior work only draws diagrams” 或 “prior work lacks feedback” 这类会被四个最接近工作直接反驳的泛化表述
- “formal feedback equals formal verification / model checking” 这类形式化过度论断

## 5. `fcstm` / `pyfcstm` 的位置冻结

`fcstm` / `pyfcstm` 在本文中只作为实现 / 制品 / 附录层面的内部载体：

- 可以用于说明原型编码、解析器、诊断、仿真器、制品版本和复现实验依赖。
- 不作为标题、摘要、引言主概念或贡献名称。
- 不要求审稿人接受一个新的 DSL；论文主文统一使用“可机检、可执行状态机表示”等任务语义术语，英文稿中再转写为 machine-checkable and executable state-machine representation。
- 与 UML / SysML / Umple / TTool 的关系只能写成表示能力、反馈来源和评测协议差异，不能写成替代式战争。

## 6. S0 对后续 PR 的约束

S0b 是 S2/S3/S4/S5 的方向前置条件，不是孤立文档。后续 PR 必须按下列方式消费本文件：

| 后续阶段 | S0b 约束 | 若不满足则 |
|---|---|---|
| S1b 相关工作 / 最接近工作矩阵 | 四个最接近工作必须第一层出现；不得把 private GT、missing code、missing prompt 写成既有工作弱点，只能写可比性 / 可复现性边界；若后续实际触发 Requirements Engineering Journal 切换，S1b 需补足 requirements-to-model、controlled natural language、requirements validation 等 RE 语境文献，但该补充不阻塞当前 SoSyM 主线的 S1b 准备 | 不得进入 S3 基线复现实验设计 |
| S2 样本登记 / oracle 协议 | 样本必须服务当前范围：控制系统需求、可执行状态机表示、可组件级裁决；oracle 必须支持状态、迁移、guard、action、变量和行为证据 | 不得冻结主样本或写平均性能论断 |
| S3 可执行基线 / 消融 | B0-B5 / EXT 必须围绕诊断、场景反馈、结构化修复决策的边际贡献；至少一个最接近工作的近似基线需要有计划或降级说明 | 不得进入主实验运行或结果写作 |
| S4 pilot / 主实验 | 只运行已冻结样本、预算、oracle、纳入 / 排除规则下的实验；结果只能支撑 claim map 中对应待证据项 | 不得升级为稿件可支撑论断 |
| S5 论文初稿 | 摘要、引言和贡献必须回查本文件、术语策略和 claim-evidence map；不得出现首创、DSL、无证据提升或工程过程贡献回潮 | 不得进入强审闭环 |

## 7. S0b 本身不跑四例真实 agent-loop

本阶段不运行真实四例 agent-loop、pilot 或主实验。原因是 S0b 只冻结方向、范围、abstract v0 与投稿出口路线；真实运行依赖 S2 样本 / oracle 和 S3 基线 / 消融条件。若此时运行，只能产生不可进入主统计的临时 smoke 证据，反而容易诱导无证据结果论断。

## 8. 自检清单

- [x] 是否先承认四个最接近工作，而不是把它们藏到泛泛相关工作？
- [x] 是否避免把本文写成“首个 NL 到状态机生成”或“首个反馈闭环”？
- [x] 是否把 `fcstm` / `pyfcstm` 降到实现 / 制品层面，而非论文主概念？
- [x] 是否没有任何无结果支撑的提升 / 优越性论断？
- [x] 是否把确定性诊断、场景级仿真和结构化修复决策说成可评估的反馈来源，而非完整形式化验证？
- [x] 是否明确 S0 对 S2/S3/S4/S5 的阻塞依赖？

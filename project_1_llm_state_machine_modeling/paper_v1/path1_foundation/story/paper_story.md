# Path-1 Paper Story

## Working title

**Executable Formal Feedback for LLM-Based State-Machine Modeling from Control-System Requirements**

标题只是工作名。正式投稿前需要根据目标 venue 和实验结果再压缩。

## Thesis

中文工作口径：本文研究可执行形式化反馈是否能提升 LLM 从自然语言控制系统需求生成状态机模型的质量；当前 foundation 只负责规划形式化状态机表示、生成-检查-仿真-修复闭环，以及后续冻结样本、人工评审、消融实验和近期 baseline 对比所需的证据门禁，不提前声明结果型结论。

候选英文口径仅供后续 `abstract_v0.md` 改写时参考，不能直接复制进摘要：

> We study whether executable formal feedback can improve LLM-based state-machine modeling from natural-language control-system requirements. The manuscript may only claim empirical improvements after the benchmark, human adjudication, ablations, and recent-baseline comparisons are completed.

## Task Boundary

- **Input**：自然语言控制系统需求、系统说明或从论文/案例中抽取的控制逻辑片段。
- **Output**：结构化、可解析、可执行、可审计的形式化状态机模型，至少覆盖 states、transitions、guards、actions、hierarchical states 等组件。
- **Supported settings**：单控制器或主监督控制器；FSM / EFSM / HSM；T0 或弱时间依赖样本；可通过 parse / semantic / inspect / simulation 形成反馈。
- **Out-of-scope settings**：并行 region、history pseudo-state、大规模 timing automata、完整 LTL/BMC/model checking、跨多个控制器的分布式协议证明。

## Gap

近期 LLM-for-modeling 工作已经能从自然语言生成 UML / SysML / Umple / Mermaid / TTool / protocol FSM 等状态机族模型，且部分工作已经包含 prompt chaining、RAG、few-shot、工具反馈、语法 / schema 检查、oracle trace 或自动修复循环。因此本文的 gap 不能写成“无人做 NL→STM”或“无人做反馈闭环”。在 9 个五绿 direct baseline 的反证压力下，本文只保留三个更窄的缺口：

1. **离线生成为主**：许多方法生成图、代码或协议状态机后再做人工 / F1 / 语法 / schema / oracle 评估；但面向控制系统需求的可执行状态机语义、确定性诊断、仿真 trace 与修复证据链通常没有被统一纳入同一实验协议。
2. **反馈语义偏浅**：已有反馈先例可以修语法、schema、PlantUML/TTool/Umple 格式、oracle trace 或部分一致性；但 transition guard/action、变量、层次状态、恢复路径与 scenario behavior 的可执行反馈仍需要更清楚的边界、消融和人工裁决。
3. **证据链不足**：prompt、raw output、修复历史、scenario、diff、eligibility、human adjudication 和失败样本如果不能形成 run record，就很难抵抗 reviewer 对 cherry-pick、公平性、oracle 和 provider drift 的挑战。

## Technical Challenge

1. **自然语言语义和可执行模型语义之间存在粒度差**：需求描述可能分散在文本中，状态、事件、guard、action 并不直接成表。
2. **状态机组件之间有依赖级联**：state 错会连带 transition / guard / action 错，简单逐槽位生成容易产生局部看似正确但整体不可执行的模型。
3. **形式化反馈不能过度承诺**：parse / semantic / inspect / simulation 可以提高模型质量，但不能被写成完整形式验证或 theorem proving。
4. **LLM agent 修复容易振荡**：需要 FixLog、run record、scenario provenance 和 human adjudication 支撑可审计修复，而不是只报告最终模型。

## Method Insight

把 LLM 的语义生成能力与确定性工具的可执行反馈分层：LLM 负责解释需求、生成模型、生成场景和提出修复；确定性工具负责解析、语义构建、轻量设计诊断和场景仿真。反馈以结构化 run record 和 fix log 进入下一轮，使模型质量改进具备可审计证据链。

## System / Method Stages

论文不需要暴露所有工程 stage ID，但方法可解释为四段：

1. **Generate**：LLM 从 NL 生成形式化状态机模型。
2. **Check**：确定性工具执行 parse、semantic、inspect、轻量一致性诊断。
3. **Simulate**：LLM 生成需求相关 scenario，确定性 simulator 执行并记录 trace。
4. **Repair / Review**：LLM 基于 fix requests、FixLog、NL 和检查/仿真证据接受或拒绝修复，并重新验证。

## Contributions

1. **Formalized executable state-machine representation**：定义适合 LLM 生成、工具检查和仿真执行的状态机表示，用于承载 states、transitions、guards、actions、hierarchical states 和变量/动作边界。
2. **Feedback-guided agentic modeling loop**：设计 generate-check-simulate-repair loop，将 parse/semantic/design diagnostics 与 executable simulation feedback 结构化返回给 LLM。
3. **Auditable run-record and repair evidence chain**：记录 prompt、raw output、stage trace、scenario、fix request、repair decision、diff、verdict 和 eligibility，支撑实验复现与失败分析。
4. **Controlled evaluation protocol for Path-1 hard comparison**：构建冻结样本、component-level human adjudication、ablation 和 recent baseline matrix，评估 formal feedback 对模型质量、稳定性和可审计性的贡献。
5. **Empirical analysis across agent orchestration conditions**：将自建 agent-loop 与成熟 coding-agent skill route 作为实验条件分析，而不是把某个 agent 框架本身当作贡献。

## Evidence Already Available

- `method/` 已完成 LangGraph full staged runtime、stage API、run record、tests 与 retained four-case evidence，见 [../method/README.md](../../../method/README.md) 和 [../method/STATUS.md](../../../method/STATUS.md)。
- `baselines/` 当前 main 入口是 [../../../baselines/SUMMARY.md](../../../baselines/SUMMARY.md)；后续 baseline 冻结前必须吸收 `main` 中 PR [#92](https://github.com/HansBug/research_ideas/pull/92) 已合入的 2025-2026 arXiv 再摸排增量，并逐篇吸收 9 个五绿 direct baseline 的输入、输出、方法、反馈/验证、数据/复现性和能力上限，避免 related-work / baseline matrix 过期或过浅。
- PR #9 已形成 323 sample selection、Top-15 / Backup-15、30 条 NL expansion 和 2 个 early historical early reference draft STM 经验，已在 [sample_assets.md](../dataset_selection/sample_assets.md) 中压缩迁移。
- issue #67 已定义 2026 夏季 Path-1 投稿冲刺 gate：按 CCF-A 论文标准打磨，优先投 CCF-B 期刊；默认主投 SoSyM regular rolling，ASE Journal / Requirements Engineering Journal regular rolling 作备投。具体见 [venue_readiness_gate.md](./venue_readiness_gate.md)。

## Evidence Still Missing Before Result-Level Writing

- 冻结 main sample registry：全量 9/101 或预注册降级样本。
- `>=4` 个 mandatory closest prior works（`Structure/Event SMF`、`llms_emp`、`TTool-AI`、`Designing FSMs`）的正式对齐矩阵，其中 `>=1` 个 same-sample approximate baseline。
- Direct / structured / no-feedback / partial-feedback / full-method 消融的可执行 pipeline。
- `>=2` 名独立 human annotator 的 blind component-level adjudication、agreement 与仲裁记录。
- 主实验结果、variance / repeat policy、failure taxonomy、artifact package。

## Baseline-Aware Positioning

9 个五绿 direct baseline 已经覆盖 NL / 文档到 FSM、UML state machine、SysML behavior、Umple、Mermaid statechart、TTool/SysML 和 protocol FSM 的主要路线。它们已经提供 single prompt、few-shot、RAG、CoT、prompt chaining、ensemble、fine-tuning、工具反馈、语法 / schema 检查、部分 repair 和专家参考评估。本文差异必须从“能否生成状态机”收缩为“可执行形式化反馈、仿真 trace、修复证据链和可审计实验协议是否带来边际贡献”。详细章节大纲和反证门见 [paper_outline.md](./paper_outline.md)。

## Related Work Positioning

本稿应同时定位在三条线之间：

1. **LLM for model generation**：自然语言到 UML/SysML/Statechart/FSM/Umple 等模型。
2. **Requirements-to-formal/executable models**：结构化需求、受控自然语言、状态机或反应系统建模与验证。
3. **Agentic feedback / repair for modeling artifacts**：用工具反馈、仿真、模型检查或 human/LLM review 修复模型工件。

本稿的差异点不是“第一个用 LLM 画状态机”，而是把可执行形式化反馈和可审计 repair/run record 放进 NL-to-state-machine modeling loop，并用 baseline hard comparison 评估其边际贡献。

## Target venue posture

本稿当前目标不是直接冲 TSE / TOSEM，而是用 CCF-A 论文标准准备一篇可被 SoSyM / ASE Journal / Requirements Engineering Journal 这类 CCF-B rolling journal 接收的稳健论文。也就是说，story 可以选择更贴合 SoSyM 的建模叙事，但 novelty、baseline、oracle、artifact、threats 与写作完整度必须按 A 类 reviewer 的挑战强度准备；不能因为目标是 B 类期刊就降低实验和证据标准。

## Claims to Make（必须先过 claim_evidence_map gate）

以下只是后续可争取的论文 claim 类型，不是当前 result claim。进入 Abstract / Introduction 前必须回到 [claim_evidence_map.md](./claim_evidence_map.md) 判定状态，并满足对应实验 gate。

- 本方法支持从 NL 生成可解析、可执行、可审计的形式化状态机模型。
- 确定性检查和仿真反馈能形成可复现的模型质量诊断与修复证据链。
- 与 direct / structured prompting 和 recent LLM-for-modeling baselines 相比，本方法可在更丰富组件维度上进行公平评估。
- Agent orchestration 应作为实验条件接受评估；只有在 E1/E2 或后续复现实验完成后，才能讨论其对模型质量、稳定性和可审计性的影响。

## Claims to Be Careful About

- “formal feedback” 只能指 parse / semantic / inspect / simulation 等可执行反馈，不等于完整 formal verification。
- 如果外部 baseline 无法公平复现，只能写 approximate / evidence-only comparison，不能写 strict head-to-head。
- 如果样本量不足或 human agreement 不够，主 claim 需要降级为 pilot / diagnostic finding。
- E2 skill route 质量高时，必须解释这既包含成熟 agent 能力，也包含本研究工具底座贡献。

## Claims to Avoid

- 不写 “first NL-to-state-machine modeling method”。
- 不写 “first feedback loop for LLM state-machine generation”。
- 不写 “prior work only draws diagrams / lacks structured outputs”。
- 不写 “solves NL-to-state-machine modeling”。
- 不写 “same benchmark / same protocol 打赢所有 prior work”。
- 不写 “LLM judge 是最终 oracle”。
- 不写 “已完成 BMC / LTL / theorem proving”。
- 不把 `fcstm`、LangGraph、Codex、Claude 或某个框架写成核心学术贡献。
- 不把 PR #9 的 sample selection / early historical early reference drafts 直接当作最终实验结果。

## Reviewer Risks

详见 [reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)。当前最高风险是：baseline 公平性、reference / sample bias、LLM-assisted annotation 透明度、样本规模、human adjudication 独立性、claim-evidence 对齐，以及“目标投 CCF-B 但证据标准未达到 CCF-A reviewer 预期”的 readiness 风险。

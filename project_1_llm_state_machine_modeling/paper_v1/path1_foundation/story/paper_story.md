# Path-1 Paper Story

## Working title

**Executable Feedback for LLM-Based State-Machine Modeling from Control-System Requirements**

标题只是工作名。正式投稿前由后续 S0b / PR-S0-Direction 根据新 story、目标 venue 和真实实验结果再压缩。标题、摘要和 contribution 候选中不得主打 `FCSTM` / `pyfcstm` / `new DSL`。

## Thesis

中文工作口径：本文研究在自然语言控制系统需求到状态机模型生成任务中，是否可以通过**形式化且可执行、可机检的状态机模型表示**，把 LLM 的初始生成转化为可由确定性工具诊断、由场景驱动仿真执行、并由结构化修复决策迭代改进的闭环，从而在冻结样本、人工组件级裁决和 baseline-aware protocol 下检验模型质量与修复稳定性是否产生可防守的边际变化。

候选英文口径仅供后续 `abstract_v0.md` 改写时参考，不能直接复制进摘要：

> We study whether constraining LLM outputs to a machine-checkable and executable state-machine representation enables deterministic diagnostics, scenario-level simulation feedback, and structured repair decisions for control-system requirements, and evaluate its effect on model quality under frozen samples, human adjudication, and baseline-aware evaluation.

这句话是研究问题和 story anchor，不是结果声明。进入 Abstract / Introduction 前必须等待 G3/G5 证据闭合；在此之前不得改写为 “we improve quality” 或 “we show improvement”。

## Task Boundary

- **Input**：自然语言控制系统需求、系统说明或从论文 / 案例中抽取的控制逻辑片段；正式实验优先 Path-1 9 系统 / 101 需求或预注册降级样本。
- **Output**：结构化、可解析、可执行的状态机模型，覆盖 states、transitions、guards、actions、hierarchical states、变量和动作边界等论文评价维度。
- **Feedback signals**：parse、semantic、inspect / design diagnostics、scenario-level simulation pass/fail、trace、fix request、accept/reject decision、diff 和 FixLog。
- **Supported settings**：单控制器或主监督控制器；FSM / EFSM / HSM；T0 或弱时间依赖样本；可以通过 deterministic diagnostics 与 simulator 形成可审计反馈。
- **Out-of-scope settings**：并行 region、history pseudo-state、大规模 timed automata、完整 LTL/BMC/model checking、theorem proving、工业认证级 verification、跨多个控制器的分布式协议证明。
- **Implementation naming**：内部可使用 `pyfcstm` / internal DSL / prototype encoding；论文主文应称为 formalized / executable / machine-checkable state-machine representation，不把 `fcstm` 写成新概念或新 DSL 贡献。

## Gap

PR #94 / S1a 已经证明：近期 baseline 覆盖 NL -> FSM / UML state machine / SysML behavior / Umple / TTool / protocol FSM，以及 prompt chaining、RAG、few-shot、tool feedback、oracle / trace repair、rule-based checking regeneration 和专家评估。因此本文不能再用“首个 NL-to-STM”或“首个 feedback loop”讲 novelty。

S0a 后可防守的 gap 收窄为：

1. **目标表示的可执行反馈角色尚未被系统评估**：Structure/Event SMF 等工作已覆盖 NL -> UML state machine 与结构化 prompt；本文不争“会生成状态机”，而研究把目标表示约束为可解析、可诊断、可仿真的实验底座后，feedback loop 对质量、可执行性和修复稳定性的边际作用。
2. **tool feedback 已存在，但 feedback source 与修复决策的数据流仍需拆解**：LLMs for EMP 和 TTool-AI 已覆盖 behavior-model rule/manual checking、syntax / constraint feedback；本文只能主张 deterministic diagnostics 是闭环中的可审计信号之一，并通过 ablation 区分 parse / semantic / simulation / full repair 的边际作用。
3. **trace / oracle repair 已存在，但 scenario-level simulation feedback 的定位不同**：Designing FSMs 已覆盖 oracle / checking-sequence / trace repair；本文不能声称首个 trace repair，只能研究 LLM 生成 scenario candidates、deterministic simulator 执行、再把 pass/fail 与 trace 作为反馈信号的组合。
4. **evaluation protocol 需要 baseline-aware 与 claim-aware**：不同 prior work 的输入、输出、GT、工具链、prompt / code 公开程度和人工预算不一致；本文必须把 strict / same-sample approximate / near / evidence-only 分层写入实验设计，而不是强行横向排名。
5. **证据链需要支撑失败样本和 provider drift 审计**：run record / audit trail 对复核、打假和排障必要，但不是 paper contribution；它服务于结果可信度和 artifact，而不是 novelty 本身。

## Technical Challenge

1. **自然语言语义与可执行模型语义之间存在粒度差**：需求描述中的状态、事件、guard、action、变量和恢复路径往往分散出现，不能直接转成状态机表格。
2. **状态机组件错误具有级联性**：state 漏失会连带 transition / guard / action 错误；只看 slot F1 或图形渲染可能掩盖行为层面的不可执行缺陷。
3. **反馈能力必须被精确定义**：parse / semantic / inspect / simulation 可提供轻量、可执行反馈，但不能被夸大为 complete model checking 或 theorem proving。
4. **LLM 修复可能振荡或过修**：需要 fix request、accept/reject decision、diff、FixLog 和修复后回归检查，避免把 regenerate 当成有依据的 repair。
5. **baseline 公平性难以自动成立**：closest prior works 的 artifact、GT、prompt、模型预算和人类反馈预算不完全公开；必须通过 same-sample approximate / near / evidence-only 降级策略保护学术可信度。

## Method Insight

把 LLM 的语义解释能力与确定性工具的可执行反馈分层：LLM 负责解释需求、生成模型、生成 scenario candidates 和提出修复；确定性工具负责解析、语义构建、轻量设计诊断和仿真执行。反馈以结构化 fix request / FixLog 进入下一轮；run record 记录每轮输入、输出、失败、修复和 eligibility，作为实验复核与 artifact 可信度支撑。

这一路线强调：现有方法已经可以生成状态机族工件，但实际可用性还需要可执行反馈、可诊断失败和可审计修复；本文把语义生成与确定性执行分离，再用受控实验检验反馈边际贡献。

## System / Method Stages

论文主文不必暴露全部工程 stage ID，可解释为四段：

1. **Represent / Generate**：LLM 从 NL 生成 formal-executable、machine-checkable state-machine representation。
2. **Diagnose**：deterministic parser、semantic builder 和 design inspector 产生 parse / semantic / design diagnostics。
3. **Simulate**：LLM 生成需求相关 scenario candidates；deterministic simulator 执行模型并记录 pass/fail、trace 和行为证据。
4. **Repair / Decide**：LLM 基于 NL、diagnostics、scenario trace 和 FixLog 提出修复；结构化 accept/reject、diff 与回归检查决定是否进入下一轮。
5. **Evaluate baseline-aware**：在 frozen samples、human component adjudication、B0-B5 / EXT 消融和 closest-work carve-out 下评估上述反馈链路，而不是把异构 prior work 强行同榜排名。

## Contributions

以下是 S0a 冻结后的**允许贡献方向**，不是当前 result claim。每条贡献进入 manuscript 前都必须在 [claim_evidence_map.md](./claim_evidence_map.md) 中具备 `baseline_coverage`、`marginal_claim`、`forbidden_softened_claims`、证据状态和 safe wording。

1. **Formalized executable state-machine representation as an evaluation substrate**：把 LLM 输出约束到可解析、可诊断、可仿真的状态机表示，以承载后续反馈闭环。边际定位：相对 NL-to-UML / SysML / Umple / protocol FSM baseline，本文不争“会生成状态机”，而争“目标表示作为可执行反馈实验底座”。
2. **Deterministic diagnostics feedback for modeling artifacts**：把 parse、semantic、inspect / design diagnostics 作为可审计反馈信号接入建模 / 修复闭环。边际定位：相对 TTool-AI / LLMs for EMP 等 tool-feedback 工作，本文不声称 tool feedback 首创，只评估它在本任务和表示下的作用。
3. **Scenario-level simulation feedback**：由 LLM 生成 scenario candidates，由 deterministic simulator 执行并产生 pass/fail、trace 和行为证据。边际定位：相对 Designing FSMs 的 oracle / trace repair，本文不声称 trace repair 首创，只研究 scenario generation + simulator execution 作为反馈信号的组合。
4. **Structured repair-decision data flow**：用 fix request、accept/reject、diff、FixLog 和回归检查组织修复过程。边际定位：相对 regenerate、auto-correction 和 trace repair，本文主张修复决策被结构化记录并进入受控评估，而非“修复”本身首创。
5. **Baseline-aware controlled evaluation protocol**：用 frozen samples、component-level human adjudication、B0-B5 / EXT 消融和 direct / same-sample approximate / near / evidence-only 分层 baseline 检验反馈边际贡献。

E1/E2 只作为 agent orchestration condition / RQ dimension：同一方法底座分别运行在自建 agent-loop 与成熟 coding-agent skill route 上，用于分析质量、稳定性、成本和失败模式差异；它不是 Hybrid 方法贡献。

## Evidence Already Available

- `method/` 已完成 LangGraph full staged runtime、stage API、run record、tests 与 retained four-case evidence，见 [../../../method/README.md](../../../method/README.md) 和 [../../../method/STATUS.md](../../../method/STATUS.md)。这些证明方法底座和 run record 能运行，但不等同主实验结果。
- PR #94 / S1a 已形成九个 direct baseline 的总账与逐篇文件，见 [../baselines/SUMMARY.md](../baselines/SUMMARY.md) 和 [../baselines/papers/](../baselines/papers/)。其中 Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs 是 S0a 后必须正面处理的 mandatory closest works。
- PR #9 已形成 323 sample selection、Top-15 / Backup-15、30 条 NL expansion 和 2 个 historical early reference draft 经验，已在 [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md) 中压缩迁移；这些是 historical / stress-test assets，不是当前结果。
- issue [#67](https://github.com/HansBug/research_ideas/issues/67) 已定义投稿节奏：按 CCF-A 论文标准打磨，2026 夏季优先投 CCF-B rolling journal；但最终 `target_venue_decision.md` 留给 S0b。

## Evidence Still Missing Before Result-Level Writing

- 冻结 main sample registry：优先 9 系统 / 101 需求，或预注册降级样本。
- 完成 `>=4` mandatory closest works 的 formal related-work / baseline matrix，并至少落地 `>=1` 个 same-sample approximate baseline。
- 完成 B0-B5 / EXT 条件的可执行 pipeline、模型预算、反馈预算和 eligibility filter。
- 完成 `>=2` 名独立 human annotator 的 blind component-level adjudication、agreement 与仲裁记录。
- 完成主实验结果、variance / repeat policy、failure taxonomy、artifact package 和 provider/model/prompt/raw output 的脱敏 run record。

## Baseline-Aware Positioning

S1a 的九个 direct baseline 已经覆盖 NL / 文档到 FSM、UML state machine、SysML behavior、Umple、Mermaid statechart、TTool/SysML 和 protocol FSM 的主要路线，并覆盖 single prompt、few-shot、RAG、CoT、prompt chaining、ensemble、fine-tuning、工具反馈、语法 / schema 检查、部分 repair 和专家参考评估。本文差异必须收缩为：在控制系统需求与可执行状态机表示上，deterministic diagnostics、scenario-level simulation feedback 与 structured repair decision 是否带来质量边际贡献。

详细 related-work / baseline 分层见 [../evidence/baseline_and_related_work_matrix.md](../evidence/baseline_and_related_work_matrix.md)。

## Related Work Positioning

Related Work 第一节必须先承认四个 mandatory closest works，而不是把它们藏在泛泛 LLM / MBSE 段落中：

1. **Structure/Event SMF**：约束 same-task NL -> UML state machine / structured prompt novelty。
2. **LLMs for EMP**：约束 SysML behavior model feedback / regeneration novelty。
3. **TTool-AI**：约束 tool syntax / constraint feedback novelty。
4. **Designing FSMs**：约束 oracle / trace / checking-sequence repair novelty。

后续再分层讨论 protocol FSM、Umple / code generation、automotive statechart、MBSE artifacts、classical requirements-to-executable-model / CNL / formal methods。不得把不可复现、私有 GT 或 prompt/code 缺失写成 prior work weakness；只能写作 comparability / reproducibility boundary。

## Target venue posture

S0a 不决定最终投稿期刊。当前 posture 是：按 CCF-A reviewer 强度准备 novelty、baseline、oracle、artifact、threats 和 writing completeness，优先面向 CCF-B rolling journal 的 fit-first 路线。具体目标出口、SoSyM / ASEJ / REJ 切换条件和 `target_venue_decision.md` 由后续 S0b / PR-S0-Direction 在新 story 冻结后完成；[venue_readiness_gate.md](./venue_readiness_gate.md) 只作为 readiness 背景和 S0b 输入。

## Claims to Make（必须先过 claim_evidence_map gate）

以下只是后续可争取的论文 claim 类型，不是当前 result claim：

- 本研究面向 NL 控制系统需求到状态机模型生成，并把输出约束为 machine-checkable / executable representation。
- 该表示支持 deterministic diagnostics、scenario-level simulation feedback 和 structured repair decision 的闭环组织。
- 本研究将通过 frozen sample、human adjudication、B0-B5 / EXT 消融和 closest-work baseline-aware protocol 检验反馈边际贡献。
- E1/E2 可作为 agent orchestration condition 分析质量、稳定性、成本和失败模式，但不作为独立 contribution。

## Claims to Be Careful About

- “formal feedback” 只能指 parse / semantic / inspect / simulation 等可执行反馈，不等于完整 formal verification。
- “executable representation” 是方法底座和实验约束，不是新 DSL 贡献。
- 如果外部 baseline 无法公平复现，只能写 approximate / near / evidence-only comparison。
- 如果样本量、human agreement 或 external baseline 不足，主 claim 必须降级为 pilot / diagnostic / protocol finding。
- 如果 E2 skill route 质量高，必须解释这既包含成熟 agent 能力，也包含本研究工具底座；不能把 Codex/Claude/skill 本身写成贡献。

## Claims to Avoid

- 不写 “first NL-to-state-machine modeling method”。
- 不写 “first feedback loop for LLM state-machine generation”。
- 不写 “first scenario-based feedback” 或 “first deterministic diagnostics loop”。
- 不写 “prior work only draws diagrams / lacks structured outputs”。
- 不写 “prior trace repair lacks …” 这类暗示 Designing FSMs 不存在 trace repair 的柔化 first claim。
- 不写 “we improve quality / we show improvement / we improve repair stability”，除非 G3/G5 结果证据已闭合。
- 不写 “solves NL-to-state-machine modeling”。
- 不写 “same benchmark / same protocol 打赢所有 prior work”。
- 不写 “LLM judge 是最终 oracle”。
- 不写 “已完成 BMC / LTL / theorem proving”。
- 不把 `fcstm`、`pyfcstm`、LangGraph、Codex、Claude、run record 或 prompt template 写成核心学术贡献。
- 不把 PR #9 selection / expansion / historical early reference drafts 直接当作最终实验结果。

## Reviewer Risks

详见 [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)。当前最高风险是：baseline carve-out 不充分、soft novelty 回潮、`fcstm` 命名负担、formal overclaim、sample/reference bias、oracle weak、external baseline fairness、run-record-as-contribution 回潮，以及旧 S0 / venue-first 路线从入口文档回潮。

# Path-1 Claim-Evidence Map

## 1. 使用方式

本文件控制后续 Abstract / Introduction / Contribution 中所有强 claim。任何新 claim 在进入 manuscript 前必须落到下表之一。

状态口径：

- **Foundation-supported**：当前 foundation 已可支持的任务边界、方法基础设施、历史资产索引或计划性表述；适合进入 planning / method overview，不等于结果 claim。
- **Manuscript-supported**：主实验、human adjudication、baseline 对齐和 artifact 已完成后才可进入 Abstract / Introduction 的结果型 claim。
- **Planned**：本 PR 已规划但尚无结果证据；可以写进 execution plan，不能写成当前论文已完成事实。
- **Forbidden**：当前证据不支持或与导师定调冲突，禁止写入论文主线。

硬规则：依赖 frozen sample、human adjudication、ablation、external baseline 或实验数字的句子，在 G3/G5 通过前只能是 **Planned**，不能作为 Abstract / Introduction 的 ready wording。

## 2. Claim status table

| Claim | 状态 | 当前证据 | 进入 manuscript 还需什么 | 允许写法 |
|---|---|---|---|---|
| 本研究面向 NL 控制系统需求到状态机模型生成任务。 | Foundation-supported | project_1 研究定位、sources / Path-1 / Path-2 资料、导师讨论文档 | 正式 manuscript 中定义输入输出和范围 | “we study NL-to-state-machine modeling for control-system requirements” |
| 当前方法底座已有可解析、可执行的形式化状态机表示和 agent-loop 基础设施。 | Foundation-supported | [../../../method/README.md](../../../method/README.md)、pyfcstm / method stage API、run evidence | paper 中弱化 `fcstm` 名称，说明表示能力而非 DSL novelty | “our infrastructure uses a formalized/executable state-machine representation” |
| 当前方法底座能将 deterministic checks 与 simulation feedback 放入 LLM 建模闭环。 | Foundation-supported | [../../../method/README.md](../../../method/README.md)、[../../../method/STATUS.md](../../../method/STATUS.md)、LG-M1 run records | 主实验 ablation 支撑边际贡献，并正面对比已有 feedback-loop baseline | “the implemented loop supports formal feedback and executable simulation feedback” |
| run record / FixLog 提供可审计证据链。 | Foundation-supported | method run-record contract、LG-M1 final evidence、仓库 run record 规范 | artifact package 中给最小复现命令 | “the infrastructure records stage traces, repairs, and eligibility for auditability” |
| PR #9 提供了可复用的 Path-1 sample selection assets。 | Foundation-supported | [sample_assets.md](../dataset_selection/sample_assets.md)、PR #9 分支资产 | 正式 sample registry 重核 | “historical candidate pool and stress-test assets” |
| 本稿当前投稿策略是按 CCF-A 标准打磨并优先投 CCF-B rolling journal。 | Foundation-supported | issue #67、[venue_readiness_gate.md](./venue_readiness_gate.md)、ccf_venues 中 SoSyM / ASEJ / REJ 入口 | S0 产出 `target_venue_decision.md`，投前人工复核 author guidelines | “we prepare the manuscript against a high-rigor review standard while targeting a fit-first CCF-B journal route” |
| 本稿已经达到 CCF-A 论文标准或投稿级质量。 | Planned | 当前只有 foundation gate，没有完整实验、稿件和 strong review closeout | G3 主实验、G4 完整稿、G5 C/I closeout、G6 artifact package | G5 前禁止写成完成事实；只能写“readiness gate is defined” |
| 本文通过 frozen benchmark、human adjudication、ablation 和 recent baselines 完成评估。 | Planned | 本 PR 只有计划；[experiment_inventory.md](../experiment_design/experiment_inventory.md) 仍标注待正式实验 | G2 sample/oracle freeze、G3 main experiment、G5 review closeout、9 个 direct baseline absorption gate | 只能写“we plan / will evaluate after freeze”；不能写“we evaluate” |
| 本方法提升了 LLM 状态机建模质量。 | Planned | 当前只有 method infrastructure 和代表性 run evidence | 主实验结果、baseline 对比、human adjudication | 结果出来前只能写研究问题：“whether feedback improves...” |
| 本文是首个 NL / 文档到状态机生成方法。 | Forbidden | 9 个五绿 direct baseline 已覆盖 FSM、UML/SysML state machine、Umple、Mermaid、TTool、protocol FSM 等路线 | 不可升级；只能作为 related work 背景 | 禁止写；可改成“we study executable feedback for NL-to-state-machine modeling” |
| 本文是首个将 feedback loop 用于 LLM 状态机 / 行为模型生成的方法。 | Forbidden | Designing FSMs、LLMs for EMP、TTool-AI 已有 oracle / model-checking rules / tool feedback / repair loop 先例 | 不可升级；只能限定为本文反馈组合和审计协议差异 | 禁止写“first feedback loop”；可写“integrates deterministic checking and simulation into an auditable loop” |
| 近期 baseline 只是画图，没有结构化输出或专家评估。 | Forbidden | CSV DFSM、Umple、PlantUML/SysML、TTool JSON/XML、3GPP transition tuple、专家 reference / F1 / Likert 均已存在 | 必须逐篇核验，不能概括性贬低 | 禁止写；应写具体 task / feedback / artifact 差异 |
| 本文的 novelty 是 RAG / few-shot / prompt chaining / agent 编排本身。 | Forbidden | Umple、Structure/Event、FlowFSM、SpecGPT、Pushing Envelope 已覆盖这些 prompt / agentic 路线 | 只有在作为条件或 baseline 时可写 | 禁止作为核心贡献；只能作为实验条件或对照 |
| 我们在同一 benchmark 上超过所有 prior work。 | Forbidden | 当前没有 strict same benchmark | 即使有 approximate baseline 也需限定 | 禁止写 |
| Formal feedback 等于完整形式化验证 / model checking。 | Forbidden | 当前主要是 parse / semantic / inspect / simulation | 若未来接入 BMC/LTL 需另写 | 禁止写 |
| LLM-as-Judge 是主 oracle。 | Forbidden | 当前 formal paper protocol 必须 human adjudication 为主 | LLM judge 只可辅助且必须披露 | 禁止写 |
| E1/E2 构成 Hybrid 方法贡献。 | Forbidden | 导师讨论已明确不主打 Hybrid | E1/E2 作为 agent orchestration conditions | 禁止写 |
| PR #9 selection / expansion / early refs 是当前 paper result。 | Forbidden | PR #9 是 historical sprint evidence | 正式 paper 需重核样本和 oracle | 禁止写 |

## 3. Contribution-to-evidence map

| Contribution | Foundation evidence already available | Evidence required before manuscript result claim | Risk if missing |
|---|---|---|---|
| Formalized executable state-machine representation | method / pyfcstm / parser / simulator / examples | representation definition、syntax subset、component extraction、limitations | 被质疑只是私有 DSL |
| Feedback-guided modeling loop | LangGraph runtime、stage API、run record、four-case retained evidence | ablation B2-B5、failure taxonomy、representative successful and failed runs | 被质疑只是 prompt engineering |
| Auditable repair evidence chain | FixLog / run record design、LG-M1 docs | artifact package、example trace、eligibility filter | 被质疑不可复现 |
| Controlled evaluation protocol | eval protocol 历史基础、Path-1 5-component 口径 | frozen samples、至少两名独立 human annotators、blind coding、agreement、baseline runners | 被质疑 oracle weak |
| External baseline comparison | baselines corpus 91 papers，含 9 个五绿 direct baseline | 9 个 direct baseline absorption report、same-sample / approximate / evidence-only matrix and results | 被质疑缺少相关工作、误述 prior work 或 cherry-pick |

## 4. Abstract / introduction guardrails

### Foundation 阶段可以写

- “We study whether executable formal feedback can improve LLM-based state-machine modeling from control-system requirements.”
- “The current infrastructure supports an agent workflow that generates, checks, simulates, and repairs executable state-machine models.”
- “This foundation specifies the benchmark, human adjudication, ablations, and baseline comparisons required before result-level claims can be made.”

### G3/G5 之前不能作为完成事实写入摘要

- “We evaluate the approach through a frozen control-system benchmark.”
- “The method improves component-level F1 over recent baselines.”
- “Human adjudication confirms the generated models are better.”

这些句子只有在样本、oracle、主实验、baseline 和 strong review 全部完成后，才能升级为 **Manuscript-supported**。

### 禁止句式

- “Our method is the first LLM method for NL-to-state-machine generation.”
- “Our method is the first feedback loop for LLM-based state-machine generation.”
- “Prior work only draws diagrams and lacks structured outputs.”
- “Our method solves state-machine modeling from natural language.”
- “We outperform prior work on the same benchmark.”
- “The LLM judge proves model correctness.”
- “The DSL itself is the main contribution.”

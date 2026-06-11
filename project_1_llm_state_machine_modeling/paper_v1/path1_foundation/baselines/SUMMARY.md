# Path-1 S1a 九大 Baseline 专项总账

## 0. 总览

本文件是 Path-1 第一篇论文 S1a 的 baseline 专项总账，汇总九个五绿 direct baseline 的方法框架、资产与可复现性、生成流程内反馈、事后评测证据、同样本可比性、claim 风险和 S1b/S3 handoff。

本文件不是最终 Related Work 文本，不直接声明论文结果。所有结论均应回到 [`papers/`](./papers/) 下逐篇文件及原始 baseline 目录核验。

> **S0a supersession note（PR #96）**：本总账中的 baseline coverage、closest-work facts、source pointers 与 same-sample approximate / near / evidence-only / boundary 分层继续作为 S1b/S3 输入；但涉及 `DSL`、`质量提升 / improvement`、`contribution` 的旧 story wording 已被 S0a 的 [`../story/terminology_policy.md`](../story/terminology_policy.md)、[`../story/claim_evidence_map.md`](../story/claim_evidence_map.md) 与 [`../story/paper_story.md`](../story/paper_story.md) 覆盖。后续不得直接复用本文件旧 wording 作为 title / abstract / contribution / result claim。

## 1. 九大 baseline 总览

| # | slug | 标题 | 年份 | venue / 类型 | 原始目录 | 逐篇文件 | 当前 S1a 定位 |
|---:|---|---|---:|---|---|---|---|
| 1 | `designing-fsm-specifications-from-requirements-gpt4` | Designing FSMs Specifications from Requirements with GPT 4.0 | 2026 | arXiv | [原始目录](../../../baselines/designing-fsm-specifications-from-requirements-gpt4/) | [逐篇](./papers/designing-fsm-specifications-from-requirements-gpt4.md) | mandatory closest；trace/oracle repair 反证 |
| 2 | `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | Structure- and Event-Driven Frameworks for State Machine Modeling with LLMs | 2026 | arXiv | [原始目录](../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/) | [逐篇](./papers/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models.md) | mandatory closest；优先 same-sample approximate |
| 3 | `agentic-flow-finite-state-machine-extraction-prompt-chaining` | An Agentic Flow for Finite State Machine Extraction using Prompt Chaining | 2025 | arXiv | [原始目录](../../../baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/) | [逐篇](./papers/agentic-flow-finite-state-machine-extraction-prompt-chaining.md) | evidence-only / near；agentic flow 反证 |
| 4 | `automated-extraction-protocol-state-machines-3gpp-specifications` | Automated Extraction of Protocol State Machines from 3GPP Specifications | 2025 | arXiv | [原始目录](../../../baselines/automated-extraction-protocol-state-machines-3gpp-specifications/) | [逐篇](./papers/automated-extraction-protocol-state-machines-3gpp-specifications.md) | evidence-only / near；长规格 + ensemble 反证 |
| 5 | `req` | Automotive Statechart Generation from Natural Language Requirements | 2025 | Master's thesis | [原始目录](../../../baselines/req/) | [逐篇](./papers/req.md) | evidence-only；汽车工业私有数据 |
| 6 | `umple` | Exploring How Well Llama3 can Generate State Machines Represented in Umple | 2025 | Master's thesis | [原始目录](../../../baselines/umple/) | [逐篇](./papers/umple.md) | near / possible approximate；RAG/Umple 可执行性 |
| 7 | `llms_emp` | Generating SysML Behavior Models via LLMs | 2025 | Internetware | [原始目录](../../../baselines/llms_emp/) | [逐篇](./papers/llms_emp.md) | mandatory closest；STM 子集优先复核 |
| 8 | `pushing-the-generative-envelope-mbse-artifacts` | Pushing the Generative Envelope of MBSE Artifacts | 2025 | RANLP | [原始目录](../../../baselines/pushing-the-generative-envelope-mbse-artifacts/) | [逐篇](./papers/pushing-the-generative-envelope-mbse-artifacts.md) | evidence-only；prompt technique / SME 评估 |
| 9 | `ttool-ai` | TTool-AI / Automatic System Modeling with AI | 2024 | tool / paper artifact | [原始目录](../../../baselines/ttool-ai/) | [逐篇](./papers/ttool-ai.md) | mandatory closest；tool feedback / TTool artifact |

定性总结：九篇 baseline 的时间集中在 2024–2026 年，说明 Path-1 的 novelty 空间已经从“有没有 LLM 生成状态机”转移到“在什么输入、表示、反馈和评测协议下生成状态机”。当前必须正面处理四个 mandatory closest works（Designing FSMs、Structure/Event SMF、LLMs for EMP、TTool-AI），并把 FlowFSM、SpecGPT、REQ、Umple、Pushing Envelope 作为协议、汽车、代码生成和 MBSE prompt 技术的边界证据。

## 2. 表 A：方法框架总表

> 本表压缩自逐篇文件 §2。`agent/prompt tag` 为多选标签；详情以逐篇文件为准。

定性总结：九篇 baseline 已覆盖从 single/few-shot prompt、structured prompt、prompt chaining、ensemble、RAG/fine-tuning 到 tool-feedback loop 的主要形态。Path-1 后续不能把贡献写成“首次用 LLM 从 NL 生成状态机”或“首次 agentic/prompt chaining”；更稳的定位应是：在控制系统需求的冻结样本上，系统评估可机检 / 可执行状态机表示、deterministic diagnostics、scenario-level feedback 与 structured repair decision 对 STM 生成质量、可执行性和修复稳定性的边际作用。实验协议另需保留 run record，用于复核、打假和排障。方法上最接近的是 `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models`、`llms_emp`、`ttool-ai` 和 `designing-fsm-specifications-from-requirements-gpt4`。

| slug | 输入 NL | 任务目标 | agent/prompt tag | LLM 模型四元组 | 输出 STM 类型与能力 | 人在回路角色 |
|---|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | synthetic English DFSM descriptions | NL -> CSV DFSM/Mealy + repair | structured prompt; tool-feedback loop | GPT-4 / GPT-4o；provider OpenAI；精确版本依原文/仓库 | CSV DFSM/Mealy；确定状态转移，可做 oracle/trace 等价比较；不覆盖层次/时间 | 主要自动；GT/oracle 由作者生成 |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | 8 个 reactive-system NL descriptions | NL -> UML state machine | single/few-shot; structure-driven; event-driven; hybrid | GPT-4o、Claude 3.5 Sonnet | UML state machine；支持 states/transitions/guards/actions 槽位评测；执行语义较轻 | 生成流程自动；参考解/评测为作者构建 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | RFC protocol documents | RFC -> protocol FSM/rulebook | prompt chaining; multi-stage agent | Llama / DeepSeek distill 系模型；provider/API 口径原文未完全明确 | Protocol FSM/rulebook；协议状态/消息/条件；非控制系统 STM | 评测依赖人工/GT；流程内人工不明 |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | 3GPP Release 17 specifications | 规格 -> protocol FSM | CoT; structured prompt; ensemble | GPT-4o、DeepSeek V3、Qwen Turbo、Claude Sonnet 4、Gemini 2.5 Pro（按原文/逐篇文件核验；具体 provider 与版本不可自动外推） | NAS/NGAP/PFCP protocol FSM；长文档状态抽取 | GT 专家构建；生成流程人工不明 |
| `req` | Volvo / Car Weaver automotive requirements | NL -> Mermaid statechart | fine-tuning; synthetic data; NLP preprocessing | GPT-3.5、GPT-4、GPT-4o fine-tuned | Mermaid statechart；可视化状态图，语义/执行能力有限 | 数据/评审高度依赖专家；不可无人工复现 |
| `umple` | NL requirements descriptions | NL -> Umple state machine code | zero-shot; one-shot; RAG | Llama 3 8B | Umple state machine code；可编译/可执行，面向软件建模 | 评测/样本构建有人；生成策略可自动运行 |
| `llms_emp` | SysML behavior model NL descriptions | NL -> PlantUML SysML behavior models | structured prompt; feedback regeneration; RAG/示例 | GPT-4、GPT-4o、Kimi、Claude 3 Haiku、Llama3.1、DeepSeek-v3 | PlantUML SysML STM/ACT/SD；STM 子集可比 | 人工评分/错误标注；生成阶段主要自动 |
| `pushing-the-generative-envelope-mbse-artifacts` | short system descriptions | NL -> SysML v2 requirements/state machine diagrams | zero/one/few-shot; CoT; temperature comparison | Mixtral-8x7B-Instruct、Llama-3-Smaug-8B | SysML v2 state machine diagrams；小样本、偏图形/文本工件 | SME 事后评估；生成阶段人工不明 |
| `ttool-ai` | NL system specifications | NL -> SysML/TTool models | knowledge injection; structured JSON; tool-feedback loop | ChatGPT / `gpt-3.5-turbo`；示例 response 为 `gpt-3.5-turbo-16k-0613`；OpenAI API；GPT-4 仅见于相关工作/背景引用，未见用于本文实验 | SysML block/internal/state machine + TTool XML；工具可解析、可仿真/评估 | 质量评分/案例构建有人；工具反馈 loop 较强 |

## 3. 表 B：资产与可复现性总表

定性总结：九篇 baseline 的 artifact 状态差异很大，真正可作为后续实验设计依据的不是“是否发表了指标”，而是输入、GT、prompt/code、输出和评测表能否被冻结。当前最有 same-sample approximate 潜力的是 `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` 的 8-case artifact 与 `llms_emp` 的 STM 子集 / parquet 资产；`ttool-ai` 和 `umple` 有工具生态价值但需要处理 provider drift、工具链安装和 benchmark 缺失；`req`、SpecGPT、FlowFSM、Pushing Envelope 更适合作为 evidence-only / near related work。后续 S3 不应把私有 GT 或未公开代码的工作强行升级为 executable baseline。

| slug | Reference / GT | 数据与 artifact | 已有本地复现资产 | 可复现路径 | 主要 blocker |
|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | synthetic oracle / generated_text / CSV | GitHub `nl2fsm` 可访问，结果文本部分可得 | 无独立本地 reproduction | 可近似复刻 synthetic pipeline | release/license/依赖锁不足，API drift |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | 8 reference solutions + F1 workbook | 4open artifact / ZIP / workbook 可访问 | 无本地冻结副本 | external 8-case same-sample approximate 优先；不是 Path-1 101-case 主样本同样本 | 需冻结 artifact 与输出归一 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | 作者 GT 未公开 | GitHub 仓库壳，RFC 输入公开 | 无 | evidence-only；可用 RFC 重建近似任务 | 源码/GT/rulebook 未公开 |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | 作者私有 GT | 3GPP specs 公开，无代码/GT | 无 | evidence-only / near | Release 锁定、GT 私有、无代码 |
| `req` | Volvo / Car Weaver 私有 statecharts | 原始数据/代码未公开 | 无 | evidence-only；方法可迁移性待评估 | 私有工业数据、专家评审不可复核 |
| `umple` | thesis benchmark 未公开；官方 Umple 示例可重建 | 无论文专属仓库；Umple 工具公开 | `reproduction-2026-04-15-local-toolchain` local toolchain smoke 已审计；不等于 thesis Llama3/RAG/pass@k 复现 | near / possible approximate | benchmark bundle、RAG 语料和输出未打包 |
| `llms_emp` | Drive 数据 + 本地 parquet | Google Drive 可达，本地 parquet 已冻结 | parquet 数据资产 | STM 子集可作为 approximate 候选 | 生成 pipeline 源码未公开，Drive 需复核 |
| `pushing-the-generative-envelope-mbse-artifacts` | 论文内小样本/SME | 无独立数据包/输出包 | 无 | evidence-only | 样本少，无 artifact |
| `ttool-ai` | GitHub artifact + `results.ods` | ttool-ai repo 可访问 | 无完整本地 reproduction | near / possible tool-based comparison | 需安装 TTool，provider drift |

## 4. 表 C：生成流程内反馈总表

定性总结：流程内反馈是 Path-1 novelty 风险最高、也最需要精确定义的维度。已有工作已经覆盖 trace/oracle repair（Designing FSMs）、rule/manual checking feedback regeneration（LLMs for EMP）和 tool syntax/constraint feedback（TTool-AI），因此本文不能声称“首次反馈闭环”。当前可防守的差异在于：本文把内部实现承载的 deterministic diagnostics、scenario simulation、修复请求决策与 FixLog 组织成面向控制系统 STM 生成质量、可执行性和修复稳定性分析的闭环。实验协议另需保留 run record，用于记录过程、排查失败和支撑结果复核。写作时必须继续严格区分 in-loop feedback 与 post-hoc evaluation；schema/JSON/PlantUML/TTool syntax 不能被写成完整 formal verification。

| slug | 静态/schema | 编译/可执行性 | oracle/trace | 仿真执行 | 形式化验证 | 人类过程反馈 | 结论 |
|---|---|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | in-loop CSV/schema 约束 | 无 | in-loop oracle / distinguishing / checking sequence repair | 无系统仿真 | 无性质模型检查；SAT-based mining 属于 fault-model repair / oracle-testing feedback | 无明确流程内人工 | 强 in-loop trace/oracle repair baseline |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | post-hoc 槽位解析/比对 | 无 | post-hoc reference F1 | 无 | 无 | 无明确流程内人工 | prompt framework，无执行反馈闭环 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | 中间 rulebook 结构化 | 无 | post-hoc GT F1 | 无 | 无 | 不明 | prompt chaining，不是 verification loop |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | JSON/tuple 结构化；ensemble | 无 | post-hoc expert GT F1 | 无 | 无 | GT 专家构建，不是流程反馈 | 长规格抽取，无公开 in-loop verifier |
| `req` | Mermaid render / 数据处理主要 post-hoc | 无 | 专家评估 post-hoc | 无 | 无 | 专家评审 post-hoc | 不应写成自动反馈闭环 |
| `umple` | Umple syntax / compile 可能作为评测 | post-hoc pass@k / 可执行性 | 无 | 无 | 无 | 无明确流程内人工 | 可执行性检查偏评测，不确认 in-loop |
| `llms_emp` | PlantUML format + rule/manual SysML grammar/semantic/consistency error feedback；Phase-II rule feedback | PlantUML format 可检查，但非可执行 STM 语义 | post-hoc human review / reference F1 | simulation trace/counterexample 是未来方向，不是已接入 | 规则/人工检查，非完整 model checking 或 formal verification | 人工检查/评分主要 post-hoc，不是交互式生成反馈 | closest feedback-regeneration work |
| `pushing-the-generative-envelope-mbse-artifacts` | 无 | 无 | 无 | 无 | 无 | SME post-hoc | prompt technique / evaluation-only |
| `ttool-ai` | in-loop JSON/SysML/TTool syntax/constraint feedback | TTool 转换/解析主要作为工具可接受性反馈 | post-hoc 质量评分 | simulator 是 post-hoc grading / 案例分析，不作为 LLM loop 的仿真反馈 | TTool verification/simulation 是工具背景能力；论文 loop 主要用 JSON/syntax/constraints，非完整 model checking | 质量评分 post-hoc | closest tool-feedback work |

## 5. 表 D：事后评测与证据强度总表

定性总结：现有 baseline 的事后证据从 strong 到 weak 分布不均：`structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` 有公开 reference/workbook，`llms_emp` 有本地可复核 parquet，`ttool-ai` 有 artifact 和结果表；但 `req`、SpecGPT、FlowFSM 和 Pushing Envelope 的 GT、专家评审或样本规模限制明显。Path-1 论文应避免用不同任务、不同输出表示、不同 GT 口径的分数做直接横向排名；更合理的做法是把这些证据用于 capability boundary、claim-to-avoid 和 baseline selection rationale。

| slug | 事后指标 / 评测 | GT 来源 | 证据强度 | 注意事项 |
|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | benchmark scores / oracle comparison | synthetic oracle | medium | artifact 非完整 release |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | component F1 workbook | reference solutions | strong | 8 个样本，artifact 可访问 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | FTP/RTSP TP-FP-FN/F1 | 作者 GT | weak-medium | GT 未公开 |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | NAS/NGAP/PFCP F1 | 专家 GT | medium | GT 私有，输入 specs 公开 |
| `req` | 定量结果 + 专家评审 | Volvo/Car Weaver 私有 | weak-medium | 数据私有 |
| `umple` | ICP/EUCP/pass@k/CodeBLEU | thesis benchmark | medium | benchmark 未公开，工具公开 |
| `llms_emp` | grammar accuracy / semantic F1 / human review | Drive + human review parquet | strong | 本地已有 parquet，但 pipeline 未公开 |
| `pushing-the-generative-envelope-mbse-artifacts` | METEOR + SME feedback | 小样本人工/文本指标 | weak | 样本很少 |
| `ttool-ai` | quality score / `results.ods` | artifact repo | medium-strong | 需安装工具核验复现 |

## 6. 表 E：同样本近似与可比性决策

定性总结：当前可比性结论是“少数 approximate、少数 near、大部分 evidence-only”。`structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` 应作为优先 external 8-case same-sample approximate 候选，但不能等同 Path-1 101-case 主样本；`llms_emp` STM 子集可作为第二候选，但需要 eligibility flag 处理“requirements inferred from models”的输入差异；`designing-fsm-specifications-from-requirements-gpt4` 更适合作为 repair/trace 近邻；`ttool-ai` 和 `umple` 可做工具/代码生成近似比较但成本较高。后续 S3 需要显式冻结输入归一、输出映射、模型预算、人工预算和反馈预算，不能只写“复现某 baseline”。

| slug | 输入可同样本性 | 输出可归一性 | 模型预算 | 人在回路预算 | 反馈预算 | GT 可得性 | 决策 |
|---|---|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | 部分；偏 synthetic DFSM | CSV DFSM 可映射到 flat STM | 可替代但需预算说明 | 低人工 | trace/oracle repair 强 | synthetic oracle | near / repair baseline 候选 |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | 可尝试；NL reactive descriptions 接近 | UML slots 可映射 | GPT-4o/Claude 可比 | 低人工 | 无 in-loop feedback | reference solutions 公开 | external 8-case same-sample approximate 优先；不是 Path-1 101-case 主样本同样本 |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | 不同；RFC 长文档 | protocol FSM 部分可映射 | open-weight / hosted provider 口径不同 | 不明 | prompt chaining | GT 未公开 | evidence-only / near |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | 不同；3GPP 长规格 | protocol FSM 部分可映射 | 多模型 ensemble 不同 | GT 专家 | ensemble/JSON | GT 私有 | evidence-only / near |
| `req` | 领域接近但数据私有 | Mermaid statechart 部分可映射 | fine-tuned GPT 不可复刻 | 高人工/私有专家 | 无明确 in-loop | 私有 | evidence-only |
| `umple` | 可尝试；NL requirements | Umple state machine 可映射 | Llama3 8B 可替代 | 低人工 | compile mostly eval | benchmark 未公开 | near / possible approximate |
| `llms_emp` | 可尝试 STM 子集 | PlantUML SysML STM 可映射 | 多模型可替代 | human review post-hoc | checker feedback 可近似但需区分 rule/manual checking | parquet 可用 | same-sample approximate 候选；requirements inferred from models 部分需 eligibility flag，不能等同自然产生的控制需求 |
| `pushing-the-generative-envelope-mbse-artifacts` | 小样本，不适合主样本 | SysML diagrams 难归一 | open models 不同 | SME post-hoc | 无 | 小样本 | evidence-only |
| `ttool-ai` | 可小规模近似 | TTool XML / SysML 可映射但成本高 | GPT-3.5 turbo provider drift 明显；不得按 GPT-4 预算配置 | 质量评分 post-hoc | tool feedback 可近似 | artifact 可用 | near / possible tool comparison |

## 7. 表 F：Claim 风险与 handoff 总表

定性总结：九篇 baseline 对 Path-1 的最大价值不是提供一个可以直接跑的单一竞品，而是明确哪些强 claim 不能写。必须避免 `first NL-to-STM`、`first agentic flow`、`first trace/repair feedback`、`first tool feedback`、`first behavior-model feedback regeneration`、`prior work only draws diagrams` 等表述。可保留的主线应收敛为：在控制系统需求与可机检 / 可执行状态机表示上，对结构化生成、deterministic diagnostics、scenario-level feedback 与修复决策进行系统化设计与评测。实验协议中的 run record 只用于复核、打假和排障，不写入 contribution bullets。S1b 写 Related Work 时应把四个 mandatory closest works 放在显著位置，而不是藏在泛泛 LLM/MBSE 段落中。

| slug | 打穿的 claim | 可保留的弱化表述 | S1b handoff | S3 handoff | 风险等级 |
|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | first NL-to-FSM；first trace repair | 我们聚焦控制需求、可执行 STM schema 与 scenario-level 反馈；run record 仅作实验记录 | mandatory closest | repair/trace baseline 设计；不得写“首次 trace/repair feedback” | C/I |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | first NL-to-UML SM；prompt framework novelty | 我们比较可执行反馈 loop 与 prompt-only/structured prompt | mandatory closest；全文核验 | external 8-case approximate candidate；S3 优先候选 | C/I |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | first agentic flow / prompt chaining | 我们不主张 agentic flow 首创，强调控制系统可执行反馈 | related work / evidence | no strict baseline | I |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | first long-spec FSM extraction；ensemble novelty | 我们限定控制需求与可执行修复，不覆盖协议规格抽取首创 | protocol FSM evidence | no strict baseline | M/I |
| `req` | first automotive statechart generation | 正面承认汽车 NL requirements -> statechart + fine-tuning + expert evaluation 已有；私有数据只作为 comparability blocker | automotive evidence-only | no strict baseline | I |
| `umple` | first RAG/few-shot state-machine code generation | 我们强调可机检 / 可执行状态机表示与 scenario-level feedback，而非 RAG 首创；run record 仅作实验记录 | related work | possible approximate | M/I |
| `llms_emp` | first behavior-model feedback regeneration / model-checking feedback | 引用时必须写为 rule-based checking feedback；我们比较 executable diagnostics、scenario trace 与 FixLog；run record 仅作实验证据链 | mandatory closest；全文核验 | same-sample approximate candidate；需 eligibility flag | C/I |
| `pushing-the-generative-envelope-mbse-artifacts` | prompt technique novelty | 我们不把 prompt trick 作为核心贡献 | prompt-technique evidence | no strict baseline | M |
| `ttool-ai` | first tool-integrated SysML/TTool feedback | 我们不主张工具反馈首创；严格区分 TTool 背景能力与 LLM loop 中 JSON/syntax/constraint feedback | mandatory closest；全文核验 | possible tool comparison | C/I |

## 8. Reviewer 全文核验清单

以下清单是 S1b/S3 和 PR review 的强制入口，防止后续写作误用本总账的压缩结论：

1. `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models`：必须全文核验 Approach、Evaluation、Threats、Conclusion；它已覆盖非结构化 NL 到 UML state machine 与多种 prompt framework，S3 优先作为 external 8-case approximate candidate。
2. `llms_emp`：必须全文核验数据集构建、Phase-I/II、Table 11、讨论与局限；作者的 model-checking / formal wording 在本文中必须落到 rule-based checking feedback，不得写成完整模型检查、counterexample trace 或仿真反馈。
3. `ttool-ai`：必须全文核验 Algorithm 1、state machine generation、feedback loop、evaluation setting；严格区分 TTool 背景 verification/simulation 能力与论文实际 LLM loop。
4. `designing-fsm-specifications-from-requirements-gpt4`：必须全文核验四类 repair、distinguishing/checking sequence、SAT-based mining；Path-1 不能写“首次 trace/repair feedback”。
5. `req` 与 `umple`：至少核验方法、结果、资产边界、人在回路和可复现性；私有数据 / benchmark 缺失只作为可比性 blocker，不作为 prior weakness。
6. 本目录 review 不需要运行四个 agent-loop 例子；它的验收目标是学术事实准确、source pointer 可追溯、novelty 风险可控。

## 9. PR #92 census 边界审计

定性总结：PR #92 census 说明 2025–2026 年 LLM + formal/behavior modeling 的邻域正在快速扩张，但 exact STM direct baseline 与 formal-spec / process-model / property-generation / role-control / RL-DFA 边界必须分清。S1a 的九大 direct baseline 只收 NL / 文档 / 需求 / RFC / specification 到 FSM-family / statechart / UML/SysML state machine / protocol state machine 的近同构输出；TLA+、PAT、Event-B、Petri net、BPMN、LTL/STL 等应进入 S1b 的 related-work breadth 和 boundary discussion，不能混入 S3 的 STM generation baseline。

PR #92 新增的 arXiv census 不只包含九大 direct baseline，也包含 RFSeek、CFSM、LANTERN / RL-DFA、TLA+、Petri net、BPMN / process model、LTL / STL、PAT / Event-B 等 strong-near / boundary 条目。S1a 的处理原则是：九大 exact STM direct baseline 之外的条目进入 S1b boundary / related-work 观察，不得混入本目录九大 direct baseline，也不得作为 S3 strict executable baseline。下表 source pointer 中 `C:` 均指向 `../../../baselines/arxiv-census-2025-2026-stm-candidates.md`。

| census 分组 | census source pointer | 当前去向 | 不混入九大 direct baseline 的理由 | S1b / S3 handoff |
|---|---|---|---|---|
| PR #92 三个 P0 direct：Designing FSMs、SpecGPT、FlowFSM | `C:23-25`, `C:53` | 已纳入本目录九大 direct baseline 的逐篇盘点 | 三篇均满足 NL / 文档 / 需求 / RFC / specification 到 FSM-family 输出；其中 SpecGPT / FlowFSM 是 protocol FSM 近同构，Designing FSMs 是 CSV DFSM | S1b 作为 direct / mandatory closest 或 protocol-FSM evidence；S3 只在各逐篇文件许可范围内做 near / approximate |
| RFSeek | `C:26`, `C:54` | `near / boundary evidence` | RFC -> provenance-linked protocol state/event summary，输出接近 protocol FSM summary，但目标是可视摘要与审计，不是直接生成可执行 STM / UML state machine | S1b 放入 protocol-spec extraction / provenance-linked summary 近邻；S3 不作为 strict baseline，除非后续单独设计 summary-to-STM adapter |
| CFSM role-playing | `C:27`, `C:55` | `background / boundary` | NL profile -> CFSM / CPFSM，形式上状态-迁移同构，但任务域是角色扮演内部状态控制，不是软件/控制系统建模 | S1b 可用于说明 FSM-family 在 LLM agent/role control 中扩散；S3 不纳入同样本比较 |
| LANTERN / RL-DFA | `C:28`, `C:55` | `background / boundary` | NL task -> DFA 服务 reinforcement-learning transfer；输出是学习/控制策略内部表示，不是需求到软件状态机 | S1b 只作为行为模型边界；S3 不纳入 baseline |
| TLA+ / PAT / Event-B | `C:29`, `C:48-49`, `C:56` | `strong formal-method neighbor` | NL -> TLA+ / PAT / Event-B 属于形式规格或模型检查生态，强相关但不是 STM-family direct output；不能与 exact STM direct baseline 混称 | S1b 放入 formal specification / verification-adjacent related work；S3 不作为 STM generation baseline，但可用于讨论 stronger formal-method comparison boundary |
| Petri net / CIR+CVN | `C:30`, `C:56` | `strong behavior-model neighbor` | LLM + Petri-net verification 关注并发行为与验证，输出/语义基础不是 UML/SysML/pyfcstm 状态机 | S1b 用于并发行为与验证近邻；S3 不混入 STM baseline |
| BPMN / process model 系列 | `C:31-38`, `C:56` | `strong process-model neighbor` | 文本到 BPMN / executable process model / workflow benchmark 与状态机生成同属行为建模，但输出是 process/workflow 语义，不是 exact STM | S1b 单列 process-model generation 近邻；S3 不作为 STM baseline，可作为 related-work breadth 证据 |
| LTL / STL / ClarifySTL | `C:39-41`, `C:56` | `property-generation / requirement-formalization neighbor` | NL requirements -> LTL/STL formulas 或 requirements clarification，输出是性质/时序逻辑而非状态-迁移模型 | S1b 放入 property / requirement formalization 相关工作；S3 不纳入 STM 生成 baseline，可为 Path-2/性质生成讨论保留入口 |

Source 口径来自 PR #92 census：direct baseline 只认 NL / 文档 / 需求 / RFC / specification -> UML/SysML State Machine / Statechart / FSM / EFSM / LTS / protocol state machine / 近同构状态-迁移模型；BPMN、process model、TLA+、Petri net、Event-B、PAT/CSP#、LTL/STL、角色/强化学习内部 FSM/DFA 等只能作为强行为近邻或 related work，不混称 exact STM direct baseline（`C:16-17`）。

## 10. 更新日志与剩余风险

定性总结：当前剩余风险主要不是目录结构或字段缺失，而是后续写作阶段可能误读本总账的压缩结论：把 near/evidence-only 工作写成 strict baseline、把 post-hoc 指标写成 in-loop feedback、把 TTool/PlantUML/JSON 语法检查写成 formal verification、或把不可复现 artifact 当成 prior work 弱点。后续每次进入 S1b/S3 前都应回到逐篇文件核验 source pointer，并把新增证据以更新日志形式回写。

| 时间 | 更新 | 剩余风险 |
|---|---|---|
| 2026-06-11 18:05:00 | 响应 PR #96 codex reviewer I-1：将 §11 与前文定性总结中的 `DSL` / `质量提升` / contribution 旧 wording 改为 S0a 口径；新增 supersession note，明确只继承 baseline facts / 分层结论，story wording 由 S0a claim / terminology gate 覆盖 | 需复审确认本总账不再与 S0a 的 `fcstm` 弱化、no-result-claim、run-record 降级策略冲突 |
| 2026-06-10 23:35:00 | 响应用户贡献定位纠偏：将 run record / audit trail 从论文贡献与 story 主线中降级为实验复核、打假和排障证据链；贡献表述收敛到 LLM4STMModeling 的可机检 / 可执行状态机表示、deterministic diagnostics、scenario-level feedback 与修复决策 | 需聚焦复审确认 SUMMARY 与逐篇文件不再把 audit trail / run record 写成学术贡献，且没有削弱必要的实验可复核要求 |
| 2026-06-10 23:10:00 | 响应 Claude reviewer I 级问题：修正 §9 `TLA+ / PAT / Event-B` census source pointer `C:47-49` 为 `C:48-49`；补充各表格小节定性总结和 §11 全局结论与建议 | 需三路 reviewer 重新强审确认新增定性判断未引入事实错误、过强 claim 或 baseline 定位偏差 |
| 2026-06-10 22:28:00 | 响应 codex reviewer I 级问题：纠正 TTool-AI 模型口径，并把 PR #92 census boundary audit 从总口径补成逐条去向/source pointer 表 | 已由 23:10 记录补充 Claude I 级 source pointer 修复和全局定性总结；仍需本轮三路复审 |
| 2026-06-10 22:05:00 | 九篇逐篇文件已回填；根据内部三路审计收紧 llms_emp / ttool-ai / Designing FSMs 等高风险口径，补充 reviewer 全文核验清单 | 已由 22:28 记录补充 boundary audit 与 TTool-AI 口径修复 |
| 2026-06-10 21:32:00 | 初始化 S1a baseline 专项总账骨架 | 已被本轮九篇逐篇回填取代；历史记录保留 |


## 11. 全局结论与后续建议

### 11.1 当前 baseline 局面总括

九大 baseline 已经足以证明：Path-1 第一篇论文不能依赖“LLM 能从 NL 生成状态机”这类泛化 novelty。近两年已有工作覆盖了 NL -> UML state machine、NL / requirements -> statechart、RFC / 3GPP specifications -> protocol FSM、NL -> Umple code、SysML behavior model generation、MBSE artifact generation 以及 TTool/SysML 工具集成。本文的学术空间应收敛到更窄但更可防守的研究问题：**面向控制系统需求的可机检 / 可执行状态机表示中，deterministic diagnostics、scenario-level feedback 与 structured repair decision 对 STM 模型质量、可执行性和修复稳定性的边际作用是什么**。这里仍是待实验检验的 research question，不是结果型 improvement claim。实验协议另需保留 run record，用于过程复核、打假和排障，但它不作为论文贡献点。

### 11.2 对论文 story 的建议

1. Related Work 第一层应先承认 direct NL-to-STM / FSM-family 工作已经存在，再解释它们在输入域、输出语义、反馈来源、可复现性和实验记录完整性上的差异。
2. Contribution 不应写成“提出首个 LLM 状态机生成方法”，也不应写成“提出新 DSL”。更安全的候选写法是：在受控协议下评估以可机检 / 可执行状态机表示、deterministic diagnostics、scenario feedback 与 structured repair decision 为核心的 LLM4STMModeling 生成-反馈-修复闭环；结果型 wording 必须等待 S3/G3 与 G5 证据闭合。
3. Method 叙事应突出 LLM4STMModeling 的反馈数据流：NL / NL_zh、可机检 / 可执行状态机表示、diagnostics、scenario pass/fail、fix request、accept/reject、diff 与 final status；`pyfcstm` / internal DSL 只在 implementation / artifact / appendix 中作为实现载体说明，run record 放在实验协议 / 复现性部分，作为排障和证据保全机制，不进入贡献模块。
4. Experiment 叙事应把 same-sample approximate、near baseline 和 evidence-only related work 分开呈现，避免用不可比较的输出/GT/人工预算强行横向排名。
5. Limitations 应主动说明：部分 prior work 的 GT / code / prompt / expert data 不公开，因此不能做 strict executable baseline；这不是 prior work 的方法弱点，而是本文 baseline fairness 的边界条件。

### 11.3 对 S1b / S3 的直接建议

| 后续阶段 | 建议动作 | 理由 |
|---|---|---|
| S1b related work | 建立 closest-work matrix，优先放入 Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs | 四者分别约束 NL->UML SM、behavior model feedback、tool feedback、trace/oracle repair 的 novelty 边界 |
| S1b boundary discussion | 单列 protocol FSM、formal specification、process model、property generation 近邻 | 防止审稿人认为本文遗漏 2025–2026 年快速扩张的 LLM + formal/behavior modeling 邻域 |
| S3 baseline design | 优先尝试 Structure/Event SMF 的 external 8-case approximate；第二候选为 LLMs for EMP STM 子集 | 两者资产可复核性和任务接近度最高，但都不能直接等同 Path-1 101-case 主样本 |
| S3 fairness protocol | 冻结输入归一、输出映射、模型预算、人工预算、反馈预算和 eligibility filter | 防止 reviewer 质疑 baseline 不公平或混入 post-hoc feedback |
| Paper claim gate | 每条 novelty claim 都回查表 F 和逐篇 §7 | 避免 Abstract / Introduction 被 prior work 直接打穿 |

### 11.4 当前不可越过的红线

- 不写 `first NL-to-STM`、`first LLM state machine generation`、`first agentic FSM flow`。
- 不写 `first feedback loop` 或 `first trace/repair feedback`。
- 不把 rule-based checking、JSON schema、PlantUML parse、TTool syntax/constraint feedback 写成完整 formal verification。
- 不把 private GT、missing code、missing prompt 写成 prior work weakness；只能写为 comparability / reproducibility blocker。
- 不把 post-hoc GT F1、expert score、SME rubric 写成生成流程内反馈。
- 不把 PR #92 的 TLA+ / PAT / Event-B / Petri net / BPMN / LTL/STL boundary works 混入九大 exact STM direct baseline。

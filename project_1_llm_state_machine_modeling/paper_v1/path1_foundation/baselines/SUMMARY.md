# Path-1 S1a 九大 Baseline 专项总账

## 0. 总览

本文件是 Path-1 第一篇论文 S1a 的 baseline 专项总账，汇总九个五绿 direct baseline 的方法框架、资产与可复现性、生成流程内反馈、事后评测证据、同样本可比性、claim 风险和 S1b/S3 handoff。

本文件不是最终 Related Work 文本，不直接声明论文结果。所有结论均应回到 [`papers/`](./papers/) 下逐篇文件及原始 baseline 目录核验。

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

## 2. 表 A：方法框架总表

> 本表压缩自逐篇文件 §2。`agent/prompt tag` 为多选标签；详情以逐篇文件为准。

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
| `ttool-ai` | NL system specifications | NL -> SysML/TTool models | knowledge injection; structured JSON; tool-feedback loop | GPT-4 / GPT-3.5 turbo 口径需逐篇核实 | SysML block/internal/state machine + TTool XML；工具可解析、可仿真/评估 | 质量评分/案例构建有人；工具反馈 loop 较强 |

## 3. 表 B：资产与可复现性总表

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
| `ttool-ai` | 可小规模近似 | TTool XML / SysML 可映射但成本高 | GPT 口径需核实 | 质量评分 post-hoc | tool feedback 可近似 | artifact 可用 | near / possible tool comparison |

## 7. 表 F：Claim 风险与 handoff 总表

| slug | 打穿的 claim | 可保留的弱化表述 | S1b handoff | S3 handoff | 风险等级 |
|---|---|---|---|---|---|
| `designing-fsm-specifications-from-requirements-gpt4` | first NL-to-FSM；first trace repair | 我们聚焦控制需求、可执行 STM schema 与 scenario trace/run record | mandatory closest | repair/trace baseline 设计；不得写“首次 trace/repair feedback” | C/I |
| `structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models` | first NL-to-UML SM；prompt framework novelty | 我们比较可执行反馈 loop 与 prompt-only/structured prompt | mandatory closest；全文核验 | external 8-case approximate candidate；S3 优先候选 | C/I |
| `agentic-flow-finite-state-machine-extraction-prompt-chaining` | first agentic flow / prompt chaining | 我们不主张 agentic flow 首创，强调控制系统可执行反馈 | related work / evidence | no strict baseline | I |
| `automated-extraction-protocol-state-machines-3gpp-specifications` | first long-spec FSM extraction；ensemble novelty | 我们限定控制需求与可执行修复，不覆盖协议规格抽取首创 | protocol FSM evidence | no strict baseline | M/I |
| `req` | first automotive statechart generation | 正面承认汽车 NL requirements -> statechart + fine-tuning + expert evaluation 已有；私有数据只作为 comparability blocker | automotive evidence-only | no strict baseline | I |
| `umple` | first RAG/few-shot state-machine code generation | 我们强调 pyfcstm/run-record/scenario feedback 而非 RAG 首创 | related work | possible approximate | M/I |
| `llms_emp` | first behavior-model feedback regeneration / model-checking feedback | 引用时必须写为 rule-based checking feedback；我们比较 executable diagnostics、scenario trace、FixLog 与 run record | mandatory closest；全文核验 | same-sample approximate candidate；需 eligibility flag | C/I |
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

PR #92 新增的 arXiv census 不只包含九大 direct baseline，也包含 TLA+、Petri net、BPMN、LTL/STL、CFSM、RL-DFA、RFSeek 等 strong-near / boundary 条目。S1a 当前结论：这些工作应进入 S1b 的 boundary / related-work 观察，而不得混入九大 exact STM direct baseline。正式执行时需逐条在本节补 source pointer；当前总账只记录处理口径。

## 10. 更新日志与剩余风险

| 时间 | 更新 | 剩余风险 |
|---|---|---|
| 2026-06-10 22:05:00 | 九篇逐篇文件已回填；根据内部三路审计收紧 llms_emp / ttool-ai / Designing FSMs 等高风险口径，补充 reviewer 全文核验清单 | 仍需 PR 三路异构 reviewer 对事实准确性、source pointer 和措辞进行全文复审 |
| 2026-06-10 21:32:00 | 初始化 S1a baseline 专项总账骨架 | 已被本轮九篇逐篇回填取代；历史记录保留 |

# Baseline 与 Related Work 对齐矩阵（S0a 草案）

本文档把 [../baselines/SUMMARY.md](../baselines/SUMMARY.md) §11 与九篇 `papers/*.md` 的 baseline 审计压缩为 Path-1 第一篇论文的 Related Work / baseline 分层草案。它不是最终 Related Work 成稿，也不是实验 runner 设计；它用于防止后续论文把不可比较工作硬当 direct baseline，或把已被 closest works 覆盖的能力重新包装成 novelty。

## 1. 分类口径与红线

### 1.1 分层口径

| 层级 | 定义 | 可用于什么 | 不可用于什么 |
|---|---|---|---|
| Same-sample approximate | 输入样本、输出对象和评价维度可映射到本文 protocol，但仍需归一化输出、预算与 rubric | 主结果中的外部 baseline / closest comparison | 宣称严格 replication 或同 benchmark SOTA |
| Near baseline | 任务接近，但输入上下文、工具依赖、输出语义、artifact 或 GT 不完全可比 | Related Work 差异、辅助实验、小规模 tool comparison | 与本文 full method 直接排名 |
| Evidence-only | prior work 能力重要，但因 private data、missing code/prompt、领域差异、输出 mismatch 或 oracle 不公开而不可公平重跑 | novelty carve-out、趋势说明、限制讨论 | 写成 prior work 方法弱点或失败 |
| Boundary/background | 形式化方法、协议 FSM、property generation、TLA+/Petri net/BPMN 等相邻邻域 | 背景与 reviewer 风险覆盖 | 混称 exact STM direct baseline |

### 1.2 写作红线

1. 不写 `first NL-to-STM`、`first LLM state-machine generation`、`first feedback loop`、`first trace repair`。
2. 不把 PlantUML / TTool / Umple / CSV parse、JSON schema、rule-based checking 写成完整 formal verification。
3. 不把 post-hoc GT F1、expert score 或 SME rubric 写成生成流程内 feedback。
4. 不把 private GT、缺代码、缺 prompt、artifact 漂移写成 prior work weakness；只能写成 comparability / reproducibility boundary。
5. 不把内部执行日志、`pyfcstm`、LangGraph / Codex / Claude、prompt chaining / RAG / few-shot 写成 paper contribution。

## 2. Mandatory closest works：Related Work 第一层

Related Work 第一节必须显式列出以下四项，并逐项给出本文边际差异。它们同时约束 RQ、Method、Experiment 和 claim wording。

| Mandatory closest work | 证据来源 | 已覆盖能力 | 本文允许保留的边际 | Baseline 放置 | 必须避免的 claim |
|---|---|---|---|---|---|
| Structure/Event SMF | [papers/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models.md](../baselines/papers/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models.md) | 非结构化 reactive-system NL → UML state machine；结构驱动、事件驱动、hybrid prompting；组件级 F1；8 个外部案例与 artifact | 本文不争自由文本到 UML SM 生成；只讨论控制系统需求下 executable target representation 如何支撑 deterministic diagnostics、scenario simulation 与 structured repair decision | **Same-sample approximate 首选**：复用其 8-case 或借其 component rubric；需标明非 Path-1 101-case 主样本 | “自由文本到状态机无人做过”；“prompt 分解本身是 novelty” |
| LLMs for EMP | [papers/llms_emp.md](../baselines/papers/llms_emp.md) | NL → PlantUML / SysML behavior models；107 behavior models、36 STM；RAG/spec injection；PlantUML/SysML rule feedback 与 regeneration | 本文需要把 rule/checking feedback 与 executable scenario trace feedback 区分；边际是 diagnostics + simulation + structured repair decision 的组合协议 | **Same-sample approximate 候选**：优先抽 STM 子集；需要说明部分需求由模型反推、checker/pipeline 不完整公开 | “首次 tool feedback / feedback regeneration”；“已有工作没有行为模型反馈” |
| TTool-AI | [papers/ttool-ai.md](../baselines/papers/ttool-ai.md) | ChatGPT + TTool/MBSE；NL → SysML block/internal/state machine diagrams；JSON/constraint/TTool syntax feedback loop；公开 XML/ODS artifact | 本文不争工具集成；边际是控制需求 executable loop、scenario-level simulation as in-loop feedback、structured fix decision 与 baseline-aware evaluation | **Near / possible tool comparison**：可小规模冻结 TTool repo/ODS 后做 XML-to-STM adapter；不建议主 same-sample exact | “首次 MBSE 工具集成”；“首次自动反馈修复 SysML 状态机”；误把 TTool 背景 simulator/model checker 当作论文 in-loop feedback |
| Designing FSMs | [papers/designing-fsm-specifications-from-requirements-gpt4.md](../baselines/papers/designing-fsm-specifications-from-requirements-gpt4.md) | 合成英文 NL → CSV DFSM/Mealy；oracle diff、distinguishing sequence、checking sequence、fault-model repair | 本文不能声称 trace/repair 首创；差异限定为控制系统需求、guard/action/变量等 richer STM schema、scenario candidates + deterministic simulator execution + structured repair decision | **Mandatory closest / near repair-oriented synthetic smoke**：适合测试 trace/repair ideas；不是 Path-1 101-case same-sample baseline | “首次 oracle/trace repair”；“LLM 从需求到 FSM repair 无先例” |

## 3. 九篇 direct baseline 的分层去向

| Work | 当前层级 | 已有能力摘要 | 本文使用方式 | 降级 / 边界原因 |
|---|---|---|---|---|
| Structure/Event SMF | Same-sample approximate | NL → UML SM；components F1；8-case artifact | closest baseline 与 Related Work 第一层 | 非控制系统安全/时间 STM；无 in-loop compile/simulation/formal repair |
| LLMs for EMP | Same-sample approximate candidate | NL → SysML behavior；STM 子集；rule feedback regeneration | STM 子集复用、feedback taxonomy 对比 | PlantUML/SysML rule checking 不等于 executable scenario feedback；pipeline/checker 不完整公开 |
| Designing FSMs | Near / repair-oriented synthetic smoke | 合成 NL → flat DFSM；oracle/trace/fault repair | trace/repair carve-out；可作 repair diagnostics smoke，不作主 baseline 排名 | 合成模板文本、flat Mealy、oracle-rich，不代表 Path-1 控制系统需求 |
| TTool-AI | Near / possible tool comparison | TTool/SysML state machine generation；JSON/constraint feedback；artifact | MBSE tool-feedback closest work；可小规模 adapter | state machine 依赖 block context；评分主观；tool/provider drift |
| Umple / Llama3 | Near baseline | NL → Umple state machine code；zero-shot / one-shot / RAG | structured / RAG prompting baseline 或 citation contrast | 数据、模型、目标语法与本项目不同；RAG/few-shot 不是本文 novelty |
| Automotive statechart generation | Evidence-only | 私有汽车需求 → Mermaid statechart；微调 + Volvo expert review | domain motivation；说明汽车状态图生成已存在 | private data / GT / fine-tuning detail，不能公平重跑；不可写成方法弱点 |
| Pushing the Generative Envelope | Evidence-only / prompt-technique boundary | 短系统描述 → SysML v2 requirements / state machine artifacts；prompt 技巧比较 | MBSE artifact trend 与 prompt-technique carve-out | 小样本 / output mismatch；不作为 strict STM baseline |
| FlowFSM | Evidence-only / protocol FSM boundary | RFC 长文档 → protocol FSM/rulebook；prompt chaining / agentic flow | 长文档与 agentic flow 已有先例 | 协议 FSM 领域、artifact/GT 边界；不混入 exact control STM direct baseline |
| SpecGPT | Evidence-only / protocol FSM boundary | 3GPP 规格 → protocol FSM；CoT / ensemble / JSON checking / expert GT | 长规格 FSM 抽取 carve-out | protocol semantics 与控制 STM 不同；GT/span evidence 不完全公开 |

## 4. Baseline-aware experiment contract

正式 S3 之前至少满足以下 contract：

1. **至少一个 external same-sample approximate baseline**：优先 Structure/Event SMF；备选 LLMs for EMP STM 子集。
2. **预算表必须冻结**：输入上下文、example/RAG、模型 ID、temperature、反馈轮数、human budget、tool budget、输出归一化、样本 / 运行纳入排除规则。
3. **同一层级才可比较**：same-sample approximate 可以进入主结果表；near work 只能做辅助 / 小规模工具对比；evidence-only 只能进入 Related Work 和 threat。
4. **不可复现要中性描述**：private GT / missing prompt / missing pipeline / provider drift 只影响 strict replication，不作为 prior work 缺陷。
5. **主结果不能只有 internal ablation**：若无外部 baseline，论文必须降级为 protocol / diagnostic study，不写优于 prior work。
6. **post-hoc 与 in-loop 分开**：GT F1、expert score、simulator grading 只有在明确进入再生成 prompt 时才算 in-loop feedback。

## 5. Related Work 章节建议结构

### 5.1 Closest LLM-to-state-machine and feedback works

按 §2 四个 mandatory closest works 展开，每段固定回答：

1. 该 work 的输入、输出、反馈、评测与 artifact。
2. 它已经打穿本文哪些 novelty claim。
3. 本文剩余边际：executable representation + deterministic diagnostics + scenario-level simulation + structured repair decision + controlled baseline protocol。
4. 该 work 在实验中属于 same-sample approximate、near 还是 evidence-only。

### 5.2 Near LLM modeling and MBSE/code-generation works

放 Umple、Automotive statechart、Pushing Envelope 等。重点说明 prompt/RAG/few-shot、领域 statechart、SysML/MBSE artifact generation 已存在；本文不把这些作为 novelty。

### 5.3 Long-document / protocol FSM extraction

放 FlowFSM、SpecGPT 等。重点说明长规格、prompt chaining、CoT/ensemble、JSON checking、专家 GT 已覆盖相邻能力；因为 protocol semantics 和 GT/artifact 边界，不强行做 direct baseline。

### 5.4 Formal modeling and verification background

放 CNL → formal model、timed/reactive systems、UPPAAL/NuSMV/Coq/TLA+/Event-B/Petri net/BPMN/property generation 等背景。写作目标是说明 rigor lineage，而不是把本文轻量 executable feedback 夸大为 complete formal verification。

## 6. Claim wording gate

| 风险 claim | 已被谁覆盖 / 约束 | 安全写法 |
|---|---|---|
| LLM 首次从 NL 生成状态机 | Structure/Event SMF、Designing FSMs、Umple、Automotive、TTool-AI | “LLM-based state-machine generation has been studied; we focus on executable feedback and structured repair decisions.” |
| 首次在生成过程中使用工具反馈 | LLMs for EMP、TTool-AI | “We use deterministic diagnostics as one auditable feedback signal and study its interaction with scenario simulation.” |
| 首次 trace / oracle repair | Designing FSMs | “Trace- and oracle-based repair exists for synthetic DFSMs; our setting differs in scenario generation, deterministic simulation, and richer control-state components.” |
| prior work 只是画图 | Structure/Event SMF、LLMs for EMP、TTool-AI 都有 machine-readable/tool-backed elements | “Prior work differs in execution target, feedback type, and evaluation protocol.” |
| prior work 不可复现所以弱 | 多篇受 private GT / code / prompt / provider drift 限制 | “Strict replication is blocked; we classify the work as evidence-only or near and avoid direct ranking.” |

## 7. 当前事实依据清单

- PR #96 body：S0a 定调、四个 mandatory closest works、禁止 claim、S0a/S0b 分工。
- [../baselines/SUMMARY.md](../baselines/SUMMARY.md) §11：九篇 baseline 全局结论、story 建议、S1b/S3 建议与红线。
- [Structure/Event SMF 审计](../baselines/papers/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models.md)：direct NL→UML SM、8-case artifact、无 in-loop simulation/formal repair。
- [LLMs for EMP 审计](../baselines/papers/llms_emp.md)：SysML behavior generation、STM 子集、rule feedback regeneration、simulation traces/counterexamples 属 future direction。
- [TTool-AI 审计](../baselines/papers/ttool-ai.md)：TTool/SysML tool feedback loop、simulator/model checker 是工具背景或 post-hoc grading，不等于 generation loop 中的 simulation feedback。
- [Designing FSMs 审计](../baselines/papers/designing-fsm-specifications-from-requirements-gpt4.md)：合成 DFSM、oracle/trace/checking-sequence/fault-model repair、不能外推到真实控制系统需求。

## 8. 主 session 仍需复核的风险

1. **最终 same-sample baseline 选择**：Structure/Event SMF 与 LLMs for EMP STM 子集都需要后续 runner / adapter / budget freeze 后才能定案。
2. **citation metadata gate**：本文档使用本地审计文件，不替代 manuscript `references.bib` 和 citation verification。
3. **adapter feasibility**：UML/Umple/PlantUML/TTool XML/CSV DFSM 到本文表示的映射可能改变评分对象，需单独写 normalization protocol。
4. **human oracle burden**：component-level adjudication 与 scenario relevance 判断需冻结 rubric 和 agreement 统计，否则 baseline comparison 仍不可防守。
5. **formal wording**：后续正文必须持续区分 deterministic diagnostics / simulation feedback 与 complete formal verification。

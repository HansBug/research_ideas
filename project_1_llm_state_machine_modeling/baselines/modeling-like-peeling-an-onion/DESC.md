# 像剥洋葱一样建模 / Modeling Like Peeling an Onion: Layerwise Analysis-Driven Automatic Behavioral Model Generation

## 基本信息

- **标题**：Modeling Like Peeling an Onion: Layerwise Analysis-Driven Automatic Behavioral Model Generation
- **中文标题**：像剥洋葱一样建模：基于逐层分析的自动行为模型生成
- **作者**：Yike Huang, Ming Hu, Xiaohong Chen, Zhi Jin, Shuyuan Xiao
- **单位**：East China Normal University / Shanghai Key Laboratory of Trustworthy Computing；Wuhan University；Peking University
- **发表**：2026 IEEE/ACM 48th International Conference on Software Engineering (ICSE '26)，Research Track，2026-04-12 至 2026-04-18，Rio de Janeiro, Brazil
- **DOI**：10.1145/3744916.3787806。当前可能尚未激活，需后续复核 ACM/DOI/publisher/author page。
- **链接**：[ICSE 2026 official page](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/278/Modeling-Like-Peeling-an-Onion-Layerwise-Analysis-Driven-Automatic-Behavioral-Model-)
- **PDF 来源记录**：用户于 2026-06-08 提供本地原文 PDF；当前不宣称有公开下载 URL，若后续确认 ACM/DOI/publisher/author page 再补。

**代码/仓库获取方式**：
- 原文 Data Availability 声称相关源代码和数据集可通过 [https://github.com/reg-repo/LATO](https://github.com/reg-repo/LATO) 获取。
- 原文还说明最终 prompt templates 已在 artifact repository 中公开。本轮仅依据原文记录该入口，未额外声明公开 PDF 下载 URL。

**数据集获取方式**：
- 原文 Data Availability 声称相关 datasets 与代码同在 [https://github.com/reg-repo/LATO](https://github.com/reg-repo/LATO)。
- 论文使用四个开放来源数据集和两个真实工业系统数据集；FSD 与 RAC 是作者新构造 / 收集的工业场景数据，原文没有在正文中给出除 GitHub artifact 之外的独立下载入口。

## 简报

这篇论文提出 LATO，一个面向文本需求的 LLM 行为建模 pipeline。它把人类需求工程师处理复杂需求时的“逐层拆解”策略转写成三个模块：Key Activity Identifier、Layer-wise Relation Extractor、Behavioral Model Constructor，目标是从自然语言需求中抽取活动、逐层恢复条件 / 循环 / 并发等嵌套关系，并生成可执行 UML activity diagrams。

- **输入**：自然语言 / textual requirements，包含顺序、条件、循环、并发以及多层嵌套的行为描述。
- **方法**：LLM layerwise analysis；结合 few-shot、CoT、静态 prompt templates、FastCoRef、Stanford CoreNLP 和 PlantUML syntax checker，形成抽取、检查、反馈、重生成闭环。
- **输出**：PlantUML diagram code 与可执行 UML activity diagrams。

```text
自然语言需求
  -> 关键活动识别 + 逐层关系抽取 + 行为模型构造
  -> PlantUML 代码 / executable UML activity diagram
```

实验覆盖 6 个数据集、共 541 个 scenario。作者报告 LATO 相比 zero-shot、few-shot、CoT baseline 在节点抽取和关系抽取上整体更优，节点 $F1$ 最大相对提升 71.1%，关系 $F1$ 最大相对提升 52.4%，各数据集 syntactic / structural pass rate 保持在 96.67% 以上。主要不足是输出为 UML activity diagram 而非状态机族模型，且迭代式 pipeline 带来更多 API 调用和延迟成本。

## 研究问题与动机

### 问题背景

论文把 behavioral models 视为需求与实现之间的桥梁，并列举 state machines、activity diagrams、sequence diagrams 等行为模型。作者认为，传统人工行为建模依赖需求工程师的形式化建模经验，在复杂系统、快速迭代和需求规模增长的背景下，效率、准确性和可扩展性都存在瓶颈。

### 核心问题

现有自动化方法可以从文本需求生成行为模型，但在处理复杂嵌套行为关系时仍容易失败。论文特别强调多层控制逻辑，例如 loop 内部嵌套 parallel branches、条件分支内嵌认证流程等结构。普通 LLM prompting 往往生成语法上可运行但语义上遗漏、错连或过度简化的模型。

### 研究动机

作者观察到，专业分析人员不会一次性从复杂文本中直接抽出完整模型，而是先识别基本活动，再逐层拆解关系，最后做一致性检查。LATO 的动机就是把这种专家式分层分析过程嵌入 LLM workflow，让 LLM 不只做一次性模型生成，而是在有结构约束和工具反馈的 pipeline 中逐层完成行为建模。

### 研究目标

论文目标是为复杂 textual requirements 自动生成准确、完整、语法合规的 executable UML activity diagrams，并验证该方法在跨领域数据集、工业系统场景、不同 seed 和不同 LLM 上是否稳健。

## 核心方法

### 方法概述

LATO 采用固定 pipeline，而不是动态 agent 交互。三个主模块按时间顺序执行：

1. Key Activity Identifier：从需求文本中识别原子活动。
2. Layer-wise Relation Extractor：按层提取 sequence、condition、fork/concurrency、loop 等关系。
3. Behavioral Model Constructor：把活动和层次关系整合为 PlantUML 代码，并生成 UML activity diagrams。

每个模块都采用“LLM Core Reasoning + External Tool-assisted”的设计。LLM 负责语义理解和生成，外部工具负责 coreference、依存 / 句法证据或 PlantUML 编译反馈。

### Key Activity Identifier

该模块包含 Activity Extractor、Activity Filter 和 Activity Calibrator。

- Activity Extractor 使用结构化 prompt 要求 LLM 输出 atomic activity names，格式为 JSON array，不附加解释。
- Activity Filter 使用 FastCoRef 2.1.6 处理代词和指代关系，过滤不在原始需求中落地的冗余活动。
- Activity Calibrator 让 LLM 在多轮约束循环中对照原文和 coreference information 检查遗漏、错误合并、过度简化等问题；若通过则输出 `[OK]`，否则输出修订后的 activity list。

这一阶段的反馈机制属于 LLM 自校准 + coreference 工具辅助，不是形式化验证。

### Layer-wise Relation Extractor

该模块是 LATO 的核心贡献，包含 Framework Extractor、Layer Populator 和 Layer Inspector。

- Framework Extractor 先抽取顶层逻辑骨架，识别 condition、sequence、concurrency、loop 等关系，并把尚有内部复杂性的节点标为 `to be decomposed`。
- Layer Populator 对 `to be decomposed` 节点递归填充具体活动内容，逐层展开，直到没有需要继续拆解的节点。
- Layer Inspector 使用 Stanford CoreNLP 4.5.10 的 parse tree 证据检查当前层的分支数量、执行顺序、嵌套结构定位和整体语义一致性；发现偏差时生成 diagnostic report，反馈给 Layer Populator 触发 repopulation。

这一过程形成 extraction-population-inspection-repopulation 闭环，是论文所谓“像剥洋葱一样”逐层建模的主要来源。

### Behavioral Model Constructor

该模块包含 Structure Analyzer、Model Generator 和 Syntax Checker。

- Structure Analyzer 整合前两阶段得到的 activities 与 hierarchical relations，形成结构化中间表示。
- Model Generator 使用 LLM 将中间表示转为 PlantUML diagram code。
- Syntax Checker 使用 PlantUML command-line tool v1.2025.4 的编译反馈检查语法错误和结构缺陷，并把错误位置、类型和修正建议反馈给 Model Generator，触发 generate-check-regenerate 循环。

这里的验证重点是 PlantUML 语法合规、连通性和结构完整性。原文没有把该步骤描述为模型检查、时序逻辑验证或仿真验证。

### LLM / agent 设置

原文使用的 LLM 设置如下：

- RQ1、RQ2、RQ3 选择 DeepSeek-V3 作为 base model，用于隔离方法贡献。
- RQ4 比较 GPT-4、GPT-4o、GPT-4.1、Qwen3-8b、Qwen3-14b、Qwen3-32b、GLM-4-flash、GLM-4-air、GLM-4-plus、DeepSeek-V3。
- 所有 baseline 与 LATO 使用统一 sampling：temperature = 0.75，top_p = 1，maximum completion tokens 调整到足够生成完整输出。
- Prompt templates 使用 few-shot examples 与 CoT reasoning，经 held-out development set 多轮调优后固定为静态模板。
- 原文没有说明使用 RAG，也没有说明采用多智能体协作；它更接近模块化 LLM pipeline，而不是 agent swarm。

### 反馈 / 验证机制

LATO 包含三类反馈：

1. 活动抽取阶段：Activity Calibrator 对照原文和 coreference 信息修正活动列表。
2. 关系抽取阶段：Layer Inspector 用 Stanford CoreNLP 句法证据生成诊断，反馈给 Layer Populator。
3. 模型构造阶段：Syntax Checker 用 PlantUML 编译反馈驱动重新生成。

这些机制提升了语义一致性、结构完整性和语法通过率，但原文未提供状态可达性、时间约束、LTL/CTL 性质或模型检查层面的 formal verification。

## 实验与评估

### 数据集

论文在 6 个数据集上评估，共 541 个 scenario：

| 数据集 | 规模 | 嵌套层级 | 领域 |
|---|---:|---|---|
| FSD: Functional Scenario Descriptions | 116 | 3-7 | Embedded System |
| RAC: Real Automotive Case | 20 | 2-6 | Automotive Industry |
| PURE | 99 | 1-3 | Information System, Gaming, Networking 等 |
| BP: Business Process Dataset | 30 | 1-3 | Business Software |
| US: User Stories Dataset | 220 | 1-2 | Recycling System, Traffic Control 等 |
| LMC: Ten Lockheed Martin Cyber-Physical Challenges | 56 | 1-3 | Cyber-physical System |

FSD 与 RAC 是作者从真实工业项目中构造 / 收集的场景数据：FSD 来自 embedded system 文档和项目工件，RAC 来自汽车领域工业合作方。所有数据集的 activity diagrams 由三名软件工程和行为建模领域专家用 PlantUML 人工标注，原文报告 Cohen's kappa 在所有标注维度上超过 0.8。

### 对比方法与指标

对比方法包括 zero-shot prompting、few-shot prompting 和 Chain-of-Thought prompting。LLM baseline 与 LATO 在相同数据和相同 base LLM 下比较。

评价指标分两层：

- 元素层：behavioral node 与 behavioral relation 的 precision、recall、$F1$。
- 系统层：Pass Rate，要求生成 PlantUML 代码可解析，并满足结构有效性，包括连通性和控制流 source / target 完整性。

语义匹配使用 all-MiniLM-L6-v2 embedding，阈值 0.85 由 0.50 到 0.95 的 grid search 选出。

### 主要实验结果

RQ1 显示 LATO 在多数数据集上优于 zero-shot、few-shot 和 CoT。原文报告：

- behavioral node extraction 的 $F1$ 最大相对提升 71.1%，平均提升 19.0%；
- behavioral relation extraction 的 $F1$ 最大相对提升 52.4%，平均提升 20.0%；
- pass rate 在所有数据集上至少为 96.67%。

RQ2 显示 few-shot example seed 对 LATO 影响较小。以 RAC 为测试集时，Seed B / C 相比 Seed A 的 N-$F1$ 最大下降 2.61%，R-$F1$ 波动不超过 3.47%，pass rate 约保持在 0.97。

RQ3 消融实验表明三个模块都有贡献。去掉 Constructor 时下降最大：N-$F1$ 下降 16.05%，R-$F1$ 下降 33.06%，pass rate 下降 4.04%。这说明最终结构整合和 PlantUML 生成 / 检查闭环对完整输出影响很大。

RQ4 显示底座 LLM 能力会影响 LATO 表现。GPT-4.1 在 N-recall 和 pass rate 上表现突出，DeepSeek-V3 整体排名靠前；Qwen3 与 GLM-4 系列在节点指标上有竞争力，但 relation extraction 表现差异更明显。

### 方法优势

LATO 的优势主要来自三点：

1. 不直接一次性生成模型，而是先抽 activity，再逐层拆 relation，最后整合为 diagram。
2. 对复杂嵌套结构更稳健，尤其适合 condition / loop / fork 混合的 textual requirements。
3. 用工具反馈约束 LLM 输出，降低完全自由生成带来的语法错误和结构断裂。

### 方法的局限性

原文明确或间接暴露的局限包括：

1. 迭代式设计增加 API calls 和 latency，准确率提升伴随计算资源成本。
2. 方法面向通用需求文本，高度专业领域仍可能需要 RAG 或 domain knowledge embedding。
3. 工业案例数量有限，尚未充分覆盖超大规模、高耦合或安全关键系统。
4. 评估主要是聚合指标，缺少按 relation type 或 nesting pattern 的细粒度分析。
5. 输出为 UML activity diagram，不是状态机 / Statechart / timed automaton；对 Project 1 的 STM 生成任务只能提供近邻方法借鉴。

## 与本研究的关系

### 相关性分析

`BASELINE评估` 建议：`🟠`。

理由是：这篇论文的输入和 LLM 方法与 Project 1 很接近，都是从自然语言需求出发，用 LLM 生成可执行建模工件；但它的输出是 UML activity diagrams / PlantUML activity diagram code，不是状态机、Statechart、SysML state machine 或 timed automaton。因此它不能算 exact STM direct baseline，也不应评为 `🟢`。

如果后续总表把 UML activity diagram 作为“状态机族近邻行为模型”单独纳入口径，也可以谨慎考虑 `🟡`；但在当前 baselines 规则下，更稳妥的评估是 `🟠`，即弱相关但方法借鉴价值高。

### 四条件建议

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 论文核心任务是 LLM-assisted automatic behavioral model generation |
| NL 输入 | 🟢 | 输入为 textual requirements / natural language descriptions |
| LLM 方法 | 🟢 | 使用 layerwise LLM pipeline、few-shot、CoT 和工具反馈 |
| STM 族输出 | 🟡 | 输出是 executable UML activity diagrams，属于近邻行为模型，不是 exact STM |

### 可借鉴之处

1. Layer-wise Relation Extractor 可迁移到 Project 1 的状态机建模，特别适合处理需求中的嵌套条件、循环、并发和异常分支。
2. `to be decomposed` 的递归中间表示可作为状态机生成前的结构化需求表示。
3. Syntax Checker 的 generate-check-regenerate 模式可迁移为 pyfcstm parser / semantic diagnostics 驱动的状态机修复闭环。
4. 分阶段评价节点、关系和 pass rate 的方式，可启发 Project 1 将状态、迁移、guard、action、层次结构分开计量。

### 存在的不足与改进空间

1. Activity diagram 的语义重点是活动流，不是状态驻留、事件触发迁移、guard/action、层次状态或正交区域。
2. 原文没有处理时间约束、定时自动机语义、安全性质、活性性质或模型检查。
3. Pass Rate 主要来自 PlantUML 语法和结构检查，不能替代 Project 1 所需的 DSL parse / semantic gate / verification readiness。
4. 论文数据集虽含 embedded、automotive、cyber-physical 场景，但并非围绕控制系统状态机规范生成设计。

### 对本研究的启发

Project 1 可以吸收 LATO 的“逐层结构分析 + 工具诊断反馈”思想，但输出侧需要改造成 STM-specific pipeline：自然语言需求先转为状态、事件、guard、action、层次 / 并发结构，再通过 pyfcstm 等结构化 diagnostics 约束生成，而不是停留在 activity diagram code。

## 重要的相关工作

### 1. 重要的前身类工作

- Riddle et al. 1978, Behavior modelling during software design：原文在框架设计部分引用该工作，作为“专家行为建模实践”与 human expert workflow 的前身来源之一。LATO 不是直接复现该论文算法，而是借用专家式行为建模过程来设计 LLM pipeline。
- Yang et al. 2014, A Systematic Literature Review of Requirements Modeling and Analysis for Self-adaptive Systems：原文在框架设计部分与 Riddle et al. 一起用于支撑从 human expert modeling practice 中抽取通用框架的动机。

### 2. 直接参与实验的 baseline

- Zero-shot prompting：将 textual requirements 直接输入 LLM 生成模型，用作 RQ1 对比。
- Few-shot prompting：提供需求文本到模型的若干 input-output examples，再让 LLM 生成目标模型，用作 RQ1 对比。
- Chain-of-Thought prompting：在 few-shot 基础上加入思考步骤示例，用作 RQ1 对比。

这些是 prompting strategy baseline，不是特定状态机生成论文。原文按 Kojima et al. 2022、Brown et al. 2020、Wei et al. 2022 和 Zheng et al. 2024 的 prompt 结构构造三类 baseline prompts。

### 3. 提供了重要论证的工作

- Ferrari et al. 2024, Model Generation with LLMs: From Requirements to UML Sequence Diagrams：原文用其说明 LLM 能从需求生成 UML sequence diagrams，但也存在内容遗漏等问题；它支撑 LATO 对复杂行为模型生成的研究必要性。
- Jahan et al. 2024, Automated Derivation of UML Sequence Diagrams from User Stories：原文把它作为 LLM-based modeling methods 的代表，说明 generative AI 能辅助 UML sequence diagram 生成。
- Wang et al. 2024, How LLMs Aid in UML Modeling：原文把它作为 novice analysts 借助 LLM 生成 sequence diagrams 的证据。
- Kourani et al. 2024, Process modeling with large language models：原文把它作为 LLM 生成 / 精化 BPMN 或 Petri-net 模型的相关工作，用于说明 LLM 建模潜力与质量控制方向。

这些工作共同支撑了“LLM 已能做简单建模，但缺少复杂嵌套行为关系系统解决方案”的论证。

### 4. 在技术上提供了支持的工作

- Otmazgin et al. 2022, F-coref：LATO 的 Activity Filter 使用 FastCoRef 2.1.6 进行 coreference resolution，以处理文本中的代词和指代关系。
- Qi et al. 2018, Universal Dependency Parsing from Scratch：LATO 的 Layer Inspector 集成 Stanford CoreNLP 4.5.10，根据 parse tree 证据检查分支数量、执行顺序和嵌套结构。
- Roques and PlantUML Contributors 2025, PlantUML Software：LATO 的 Syntax Checker 使用 PlantUML command-line tool v1.2025.4 检查生成 diagram code 的语法和结构问题。
- Powers 2020, Evaluation: from precision, recall and F-measure：原文在评价指标和 matching 阈值说明中引用，用于 precision、recall、F-measure 等指标背景。

### 5. 其他重要工作

- De Biase et al. 2024, Completion of SysML state machines from Given-When-Then requirements：原文将其作为 rule-based behavioral modeling 相关工作，说明 Given-When-Then 到 SysML transition templates 的传统方向。该工作与 Project 1 更接近 STM，但不是 LATO 的直接实验 baseline。
- Zhu et al. 2023, TAG: UML Activity Diagram Deeply Supervised Generation from Business Textural Specification：原文把它作为 ML-based 方法和 BP 数据集来源之一，说明从 business text 到 UML activity diagram 的监督生成方向。
- Mavridou et al. 2020, The Ten Lockheed Martin Cyber-Physical Challenges：原文使用 LMC 作为 cyber-physical system requirements benchmark 来源之一。
- Ferrari et al. 2017, PURE: A Dataset of Public Requirements Documents：原文使用 PURE 作为跨领域 public requirements documents 来源。
- Dalpiaz and Sturm 2020, Conceptualizing Requirements Using User Stories and Use Cases：原文使用 User Stories dataset 作为实验数据来源。

## 文献分类总结

LATO 位于“自然语言需求 -> 行为模型”的 LLM 建模链条上。它的直接创新不是提出新的 UML activity diagram 语义，而是将专家式分层分析转化为 LLM pipeline，并用 coreference、dependency parsing 和 PlantUML syntax checking 约束生成过程。

对 Project 1 来说，它是高价值近邻工作：输入与方法高度相关，尤其适合作为“复杂嵌套关系如何被 LLM 分层拆解”的方法参照；但输出不是 STM，实验 gate 也不是状态机语义验证，因此不能作为 exact STM direct baseline。

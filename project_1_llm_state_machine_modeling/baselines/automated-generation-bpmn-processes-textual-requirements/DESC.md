# 从文本需求自动生成 BPMN 流程 / Automated Generation of BPMN Processes from Textual Requirements

## 基本信息

- **标题**：Automated Generation of BPMN Processes from Textual Requirements
- **中文标题**：从文本需求自动生成 BPMN 流程
- **作者**：Quentin Nivon、Gwen Salaün
- **单位**：Univ. Grenoble Alpes、CNRS、Grenoble INP、Inria、LIG, Grenoble, France
- **发表**：ICSOC 2024, Proceedings Part I；Springer LNCS 15404，页 185-201；Springer 卷出版年份为 2025
- **DOI**：10.1007/978-981-96-0805-8_14
- **链接**：[DOI 页面](https://doi.org/10.1007/978-981-96-0805-8_14)；[作者 PDF](https://convecs.inria.fr/doc/publications/Nivon-Salaun-24-b.pdf)；[GIVUP 工具页](https://quentinnivon.github.io/pages/givup.html)

**代码/仓库获取方式**：
- 原文说明方法由 Java 工具实现，并嵌入 Web server 后端；论文给出的在线入口是 [GIVUP 工具页](https://quentinnivon.github.io/pages/givup.html)，当前会重定向到 `https://lig-givup.imag.fr`。
- 原文未提供公开源码仓库链接。工具页可见密码输入框，因此工具是否可由外部读者直接完整复现实验未确认。

**数据集获取方式**：
- 原文使用 200 个流程文本描述做实验，其中 25% 来自文献资料，包含 PET dataset 和会议论文等；75% 由 9 名用户手工编写，其中 5 名专家、4 名新手。
- 原文未提供这 200 个描述及期望 BPMN 结果的公开下载链接。PET dataset 是部分来源线索，但不能等同于本文完整 benchmark。

## 简报

本文解决的问题是：给定一段用自然语言非正式描述业务流程任务及其顺序约束的文本，自动生成满足这些约束的 BPMN 流程模型。它不是状态机生成论文，而是一个“文本需求到行为流程模型”的近邻 LLM 建模工作。

- **输入**：自然语言文本需求，描述业务流程中的任务、顺序、并行、互斥选择和循环等约束；任务名称可预先标注，但不是方法运行的硬性前提。
- **方法**：微调 GPT-3.5-turbo-0125，将文本中的任务排序约束抽取为类似正则表达式的内部约束语言；再解析为 AST，经过图构造、循环处理、AST 合并、选择处理和模式化转换，生成 BPMN。
- **输出**：BPMN 流程，覆盖事件、任务、sequence flow、并行网关、互斥网关和循环等控制流构件。

```text
输入层：自然语言业务流程需求
  -> 方法层：fine-tuned GPT-3.5 抽取约束表达式 -> AST -> 有向图/循环/选择处理 -> AST-to-BPMN 模式转换
  -> 输出层：BPMN 业务流程模型
```

实验在 200 个流程描述上比较本文工具、ProMoAI、Gemini 和 GPT-4-turbo。本文工具取得 78.5% 有效、8% 歧义有效、13.5% 无效，平均执行时间 4.07 秒；但输出是 BPMN 而非 STM，因此对 Project 1 只能评为强近邻的 `🟠`。

**可比字段快照**：

- **输入**：自然语言业务流程需求，描述任务及其排序约束。
- **输出**：BPMN 流程。
- **输出模型类型**：BPMN 2.0 控制流 / activity diagram 子集，包含任务、事件、sequence flow、并行网关、互斥网关和循环；非状态机族模型。
- **使用的 LLM**：fine-tuned GPT-3.5-turbo-0125；Gemini 和 GPT-4-turbo 只作为直接 LLM 对比对象。
- **主要方法**：LLM 抽取约束表达式，AST/图算法合并顺序、并行、选择和循环约束，再用 AST-to-BPMN 模式转换生成流程。
- **反馈/验证机制**：表达式语法约束、结构化转换约束和两名 BPMN 专家人工评审；原文未确认自动模型检查/修复闭环。
- **数据集/benchmark**：200 个文本描述；原文未提供完整公开下载链接。
- **代码/数据开放性**：在线工具页公开，源码仓库与完整实验数据集原文未提供/未确认。

## 研究问题与动机

### 问题背景

BPMN 是业务流程建模的事实标准之一，但其语法较丰富，非专家直接绘制正确、结构良好的 BPMN 流程并不容易。普通建模工具允许用户自由绘制流程图，却不一定系统性保证语法、语义或需求一致性。

### 核心问题

本文关注的核心问题是：如何从非正式自然语言流程描述中提取任务及其排序依赖，并自动合成为一个完整 BPMN 流程。这里的“排序依赖”不只包含顺序执行，还包含并行、互斥选择和循环。

### 研究动机

论文希望降低 BPMN 建模门槛，使非专家可以通过文本描述得到 BPMN 流程；同时也为专家减少从零绘图的负担。作者选择让 LLM 负责自然语言理解，把后续模型构造交给显式的 AST、图算法和模式转换，从而避免直接让 LLM 输出复杂 BPMN XML。

### 研究意义

对 LLM 建模研究而言，本文的意义在于把 LLM 限定在“文本约束抽取”阶段，再用可解释的中间语言和确定性转换管线生成模型。这种设计比直接让 LLM 生成完整图模型更可控，也更容易定位错误来源。

### 现有方法的局限性

原文指出，已有文本到 BPMN 工作常要求用户使用受限 DSL 或半结构化文本，或者只抽取活动、参与者、依赖等片段，后续仍需人工拼装流程。直接使用通用 LLM 生成 BPMN XML 也不可靠，因此本文采用 fine-tuned GPT + AST/图转换的混合路线。

### 研究目标

本文目标是自动把文本需求转换为完整 BPMN 流程，并在工具中端到端展示结果。它没有把目标定义为状态机、Statechart 或 SysML 状态机生成，也没有把控制系统需求作为主要应用域。

## 核心方法

### 方法概述

方法分为三大阶段：

1. 使用微调后的 GPT-3.5 从文本需求中抽取任务排序约束，输出一个或多个内部表达式。
2. 将表达式解析为 AST，再把多个 AST 中分散的约束合并到一个统一 AST。
3. 对最终 AST 应用固定的 BPMN 转换模式，递归生成 BPMN 流程。

### 输入与中间约束语言

输入是对业务流程的自然语言描述。用户可以显式命名任务，例如给任务写缩写，但论文明确说明这不是运行前提。为了表达文本中的行为约束，论文定义了一种类似正则表达式的内部语言，用操作符表达：

- `|`：互斥选择。
- `&`：并行。
- `<`：顺序依赖。
- `*`：循环。
- `,`：列出互相受约束的元素。

该语言用于覆盖论文支持的 BPMN 控制流子集，不是通用状态机 DSL。

### LLM/agent 设置

- **使用的 LLM**：GPT-3.5-turbo-0125。
- **训练方式**：fine-tuning，当前训练规模为 400 个示例。
- **prompt 结构**：训练样例包含 system prompt、user prompt 和 assistant prompt。system prompt 描述 GPT 应从文本需求中抽取任务排序约束并按指定语言输出；user prompt 对应文本需求；assistant prompt 对应期望约束表达式。
- **few-shot / CoT / RAG**：原文未明确使用 few-shot、CoT 或 RAG 作为推理时方法变量。
- **agent 设置**：原文没有多智能体、工具调用 agent 或自动规划 agent。LLM 只负责把文本转换为约束表达式，后续由确定性程序处理。

### AST 与图构造

每个 GPT 返回的约束表达式会被解析为 AST。由于一个文本需求可能产生多个表达式，论文先从 AST 中抽取顺序约束对，构造有向图，再用传递约简去掉冗余约束。若图中存在环，系统将其解释为流程循环，并计算入口节点、出口节点、必经路径和可选路径。

### AST 合并、选择与循环处理

在得到经循环处理的有向图后，工具按深度优先方式把任务逐步插入统一 AST。插入时会计算左边界节点和右边界节点，以决定当前任务与已有 AST 中任务的顺序或并行关系。互斥选择则通过替换或插入 `|` 节点处理。循环结构会被保存为内部结构，并在 AST 中使用相应循环节点表达。

### AST 到 BPMN 的转换

最终 AST 通过四类模式递归转换为 BPMN：

1. 顺序模式。
2. 并行模式。
3. 选择模式。
4. 循环模式。

转换采用自底向上的方式，先生成任务节点，再逐层把 BPMN 子流程组合起来。最终模型由 Web 工具渲染，论文提到使用 `bpmn.io` 显示 BPMN 结果。

### 反馈/验证机制

本文没有形成 Project 1 意义上的“生成-形式化验证-修复”闭环。可确认的检查与反馈主要有三类：

1. **语法约束**：GPT 输出需要符合内部表达式语法；实验中 200 个例子均得到语法正确的表达式。
2. **结构化转换约束**：AST、图、循环和模式转换保证输出落在本文支持的 BPMN 控制流子集内。
3. **人工评审**：实验中两名 BPMN 专家判断生成流程是否与文本需求一致，并将结果分为有效、歧义有效和无效。

工具页当前可见“Temporal logic property”输入区域，但论文正文没有把模型检查作为已完成实验闭环。结论部分只把“由文本时序逻辑性质驱动的 model checking”列为可能改进方向。

## 实验与评估

### 数据集

实验使用 200 个文本描述：

- 25% 来自文献资料，原文举例包括 PET dataset 和会议论文等。
- 75% 由 9 名工具使用者手写，其中包括 5 名专家和 4 名新手。
- 所有 200 个主实验样例都预先命名了任务。
- 原文还测试了不带任务名称的 raw descriptions，观察到 24% 的准确率损失。

### 评估指标

实验主要评估：

- 生成流程是否与文本需求和评审专家预期一致。
- 生成结果是否歧义但仍可接受。
- 生成结果是否无效。
- 平均执行时间。

### 实验设置

对比对象包括：

- 本文工具。
- ProMoAI。
- Gemini。
- GPT-4-turbo。

ProMoAI 按在线工具原样使用。Gemini 和 GPT-4-turbo 被要求根据文本描述生成 BPMN 流程的文本表示，而不是直接输出 BPMN XML。

### 主要实验结果

| 工具/模型 | 有效 | 歧义有效 | 无效 | 平均执行时间 |
|---|---:|---:|---:|---:|
| 本文工具 | 78.5% | 8% | 13.5% | 4.07 秒 |
| ProMoAI | 50% | 8.7% | 41.2% | 24.7 秒 |
| Gemini | 32.2% | 8.1% | 59.7% | 8.32 秒 |
| GPT-4-turbo | 66.6% | 21.1% | 12.2% | 19.2 秒 |

作者认为本文工具在生成质量和执行时间上都最好。对 13.5% 无效结果的进一步分析显示，它们通常接近期望流程，只缺少少量约束或存在少量误解。作者也提醒，Gemini 和 GPT-4-turbo 的结果可能被高估，因为它们没有直接生成 BPMN XML，而是生成文本形式，由专家视觉分析。

### 方法优势

- 把 LLM 输出限制在简洁的任务排序约束语言中，而不是直接生成完整 BPMN XML。
- 通过 AST 和图算法显式处理顺序、并行、选择和循环。
- 支持从非正式自然语言描述到完整 BPMN 流程的自动生成。
- 相比 ProMoAI 和直接调用 LLM，实验中有效率与平均执行时间更优。

### 方法的局限性

- 任务名称预先给定时效果更好；无任务名称输入导致 24% 准确率损失。
- 错误主要来自 GPT 未抽取出文本约束或误解约束。
- 支持的是 BPMN 控制流子集，并非完整 BPMN 语义。
- 原文未提供完整实验数据集公开下载链接，也未提供源码仓库。
- 没有将形式化模型检查或自动修复闭环纳入正文实验。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：`🟠`。**

理由是：本文满足“自然语言需求输入”和“LLM 方法”两个核心条件，并且输出是行为/控制流模型；但最终工件是 BPMN 流程，不是状态机、Statechart、SysML 状态机或本项目直接目标中的 STM 族模型。因此它不能作为 Project 1 的 exact STM direct baseline，只能作为强近邻 baseline 或 related-work 方法参照。

四条件建议如下：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 明确使用 fine-tuned GPT-3.5 辅助模型生成。 |
| NL输入 | 🟢 | 输入是自然语言业务流程需求。 |
| LLM方法 | 🟢 | LLM 负责抽取任务排序约束，是 pipeline 的关键阶段。 |
| STM族输出 | 🟡 | BPMN 控制流具有行为建模邻近性，但不是 STM/Statechart/SysML 状态机。 |

### 研究定位与差异化

本文与 Project 1 的共同点在于：都关注从非形式化文本需求到可机读行为模型的自动化转换，并且都避免纯自然语言结果停留在不可验证状态。差异在于：Project 1 的目标是状态机结构化建模，尤其关心状态、事件、守卫条件、层次并发和控制系统行为语义；本文目标是业务流程 BPMN，核心元素是任务、sequence flow 和 gateway。

### 可借鉴之处

- **约束中间语言**：让 LLM 输出受限表达式，再由确定性程序生成模型，可降低直接图模型生成的不可控性。
- **AST/图混合管线**：用 AST 表示局部表达式，用图合并跨表达式约束，对 Project 1 的多约束合并有借鉴价值。
- **错误边界清晰**：错误可区分为 LLM 抽取失败、表达式歧义、约束合并问题和模型转换问题。
- **评审口径**：有效、歧义有效、无效三分法可迁移到状态机模型评审，尤其适合处理自然语言需求本身存在歧义的情况。

### 存在的不足与改进空间

- BPMN 输出不能直接作为 STM 对照结果，不能用来评价状态、转移、事件、守卫和动作的完整提取能力。
- 方法没有覆盖控制系统中常见的时间约束、安全约束、连续变量或状态不变式。
- 本文没有自动验证与修复闭环，专家评审仍是主要正确性判定方式。
- 数据集未公开，复现实验和横向对比存在阻碍。

### 对本研究的启发

Project 1 可以借鉴“LLM 只负责语义抽取，结构化模型由确定性管线合成”的设计。对于状态机生成，可以让 LLM 输出受限的状态、事件、条件、动作和转移约束，再通过 parser、semantic checker、模型构造器和验证反馈闭环生成最终 STM。这比直接让 LLM 输出完整状态机更利于可追踪、可修复和可审计。

## 重要的相关工作

### 1. 重要的前身类工作

- **Ivanchikj 等，2020，From Text to Visual BPMN Process Models: Design and Evaluation，MODELS 2020 [10]**：原文第 5 节将其作为文本到 BPMN 的相似目标工作。该方法设计 DSL 及语法，用户需写符合语法的规格，再经 DSL parser 抽取 traces，并通过 process mining 算法转换为 BPMN。本文与其目标相似，但强调输入可为自然语言而非受限 DSL。
- **Honkisz、Kluza、Wiśniewski，2018，A Concept for Generating Business Process Models from Natural Language Description，KSEM 2018 [8]**：原文第 5 节将其作为自然语言到 BPMN 的早期流程生成路线。该方法用 subject-verb-object 和 gateway 关键词抽取任务、参与者及网关信息，再转为内部 spreadsheet 格式和 BPMN。本文认为该方法仍依赖部分格式化文本，且主要支持顺序和选择。
- **Sintoris、Vergidis，2017，Extracting Business Process Models Using NLP Techniques，KSEM 2017 [15]**：原文第 5 节把它作为从自然语言规格抽取业务流程的理论路线。其重点是活动和依赖抽取，后续仍需要人工干预；本文则试图自动生成完整 BPMN 流程。

### 2. 直接参与实验的 baseline

- **Kourani、Berti、Schuster、van der Aalst，2024，ProMoAI: Process Modeling with Generative AI [14]**：原文第 4 节将 ProMoAI 作为在线可用对比工具。实验中 ProMoAI 在 200 个描述上得到 50% 有效、8.7% 歧义有效、41.2% 无效，平均执行时间 24.7 秒。
- **Google Team，2024，Gemini: A Family of Highly Capable Multimodal Models [4]**：原文第 4 节将 Gemini 作为直接 LLM 对比对象。Gemini 被提示生成 BPMN 流程文本表示，实验得到 32.2% 有效、8.1% 歧义有效、59.7% 无效。
- **OpenAI 等，2024，GPT-4 Technical Report [5]**：原文第 4 节将 GPT-4-turbo 作为直接 LLM 对比对象。GPT-4-turbo 得到 66.6% 有效、21.1% 歧义有效、12.2% 无效，但作者提醒其结果可能因只生成文本表示而被高估。

### 3. 提供了重要论证的工作

- **Vidgof、Bachhofner、Mendling，2023，Large Language Models for Business Process Management: Opportunities and Challenges [16]**：原文第 5 节引用其对 LLM 在 BPM lifecycle 中各阶段应用机会的讨论，用于支撑 LLM 可辅助 BPM 任务的研究背景。
- **Klievtsova 等，2023，Conversational Process Modelling，BPM 2023 [12]**：原文第 5 节用其说明对话式流程建模工具链可以包含任务抽取、逻辑抽取、BPMN layout 和 refinement，但该工作重点限制在任务抽取。本文相对强调端到端生成 BPMN。
- **Bellan、van der Aa、Dragoni、Ghidini、Ponzetto，2022，PET: An Annotated Dataset for Process Extraction from Natural Language Text Tasks [3]**：原文第 4 节说明实验描述中 25% 来自文献资料，包括 PET dataset。它提供了本文实验数据来源的一部分，但不是本文完整 benchmark。

### 4. 在技术上提供了支持的工作

- **Aho、Garey、Ullman，1972，The Transitive Reduction of a Directed Graph，SIAM Journal on Computing [1]**：原文第 3.2 节在有向图构造后使用传递约简，去除冗余顺序约束。
- **Kleene，1951，Representation of Events in Nerve Nets and Finite Automata [11]**：原文第 1 节和第 2.3 节用其作为类似正则表达式中间语言的理论线索。
- **Knuth，1969，The Art of Computer Programming, Volume 2 [13]**：原文第 1 节和第 2.4 节引用其支持 AST 表示和算法处理。
- **ISO/IEC，2013，International Standard 19510, BPMN [9]**：原文第 2.1 节以 BPMN 2.0 标准界定本文支持的控制流构件。
- **bpmn.io**：原文第 4 节说明 Web 工具最终用 `bpmn.io` 渲染生成的 BPMN 流程；它是实现展示层支撑，不是论文算法贡献。

### 5. 其他重要工作

- **Bellan、Dragoni、Ghidini，2022，Extracting Business Process Entities and Relations from Text Using Pre-trained Language Models and In-Context Learning，EDOC 2022 [2]**：原文第 5 节将其作为用 in-context learning 抽取流程实体和关系的相关工作。其结果仍是流程片段，需要人工拼装；本文试图自动形成完整 BPMN。
- **Fill 等，2023，Conceptual Modeling and Large Language Models，EMISAJ 2023 [7]**：原文第 5 节引用其通过 DSL 预训练 LLM 理解 BPMN 语义并抽取任务关系的路线。本文认为其支持语法受限，尤其没有覆盖循环。
- **Falcone、Salaün、Zuo，2021，Semi-automated Modelling of Optimized BPMN Processes，SCC 2021 [6]**：原文第 2.3 节提到某些工作使用任务对表示顺序约束。本文认为这种形式表达能力有限，难以覆盖选择和循环。

## 文献分类总结

本文位于“自然语言业务流程描述 -> BPMN 行为流程模型”的 LLM 辅助建模链条上。它继承了文本到 BPMN、流程实体抽取、BPMN DSL 和 BPM 生命周期中 LLM 应用等相关工作，但把 LLM 限制在约束抽取阶段，再通过 AST 和图算法合成完整 BPMN。

在 Project 1 baseline 体系中，它应作为“强近邻但非 STM”论文保留。它能提供中间语言、AST 合并、约束管线和评审口径方面的方法借鉴，但不能被写成状态机直接生成 baseline。

## 参考文献

[1] A. V. Aho, M. R. Garey, and J. D. Ullman. 1972. The Transitive Reduction of a Directed Graph. SIAM Journal on Computing. https://doi.org/10.1137/0201008

[2] P. Bellan, M. Dragoni, and C. Ghidini. 2022. Extracting Business Process Entities and Relations from Text Using Pre-trained Language Models and In-Context Learning. EDOC 2022. https://doi.org/10.1007/978-3-031-17604-3_11

[3] P. Bellan, H. van der Aa, M. Dragoni, C. Ghidini, and S. P. Ponzetto. 2022. PET: An Annotated Dataset for Process Extraction from Natural Language Text Tasks. Lecture Notes in Business Information Processing. https://doi.org/10.1007/978-3-031-16168-1_19

[4] Google Team et al. 2024. Gemini: A Family of Highly Capable Multimodal Models. https://arxiv.org/abs/2312.11805

[5] OpenAI et al. 2024. GPT-4 Technical Report. https://arxiv.org/abs/2303.08774

[6] Y. Falcone, G. Salaün, and A. Zuo. 2021. Semi-automated Modelling of Optimized BPMN Processes. SCC 2021. https://doi.org/10.1109/SCC53864.2021.00059

[7] H.-G. Fill et al. 2023. Conceptual Modeling and Large Language Models: Impressions From First Experiments With ChatGPT. EMISAJ 2023. https://doi.org/10.18417/emisa.18.3

[8] K. Honkisz, K. Kluza, and P. Wiśniewski. 2018. A Concept for Generating Business Process Models from Natural Language Description. KSEM 2018. https://doi.org/10.1007/978-3-319-99365-2_8

[9] ISO/IEC. 2013. International Standard 19510, Information technology, Business Process Model and Notation. https://www.iso.org/standard/62652.html

[10] A. Ivanchikj et al. 2020. From Text to Visual BPMN Process Models: Design and Evaluation. MODELS 2020. https://doi.org/10.1145/3365438.3410990

[11] S. C. Kleene. 1951. Representation of Events in Nerve Nets and Finite Automata. Automata Studies. https://www.rand.org/pubs/research_memoranda/RM704.html

[12] N. Klievtsova, J.-V. Benzin, T. Kampik, J. Mangler, and S. Rinderle-Ma. 2023. Conversational Process Modelling: State of the Art, Applications, and Implications in Practice. BPM 2023. https://doi.org/10.1007/978-3-031-41620-0_19

[13] D. E. Knuth. 1969. The Art of Computer Programming, Volume 2: Seminumerical Algorithms. Addison-Wesley. https://www-cs-faculty.stanford.edu/~knuth/taocp.html

[14] H. Kourani, A. Berti, D. Schuster, and W. M. P. van der Aalst. 2024. ProMoAI: Process Modeling with Generative AI. https://arxiv.org/abs/2403.04327

[15] K. Sintoris and K. Vergidis. 2017. Extracting Business Process Models Using Natural Language Processing Techniques. KSEM 2017. https://doi.org/10.1007/978-3-319-63558-3_12

[16] M. Vidgof, S. Bachhofner, and J. Mendling. 2023. Large Language Models for Business Process Management: Opportunities and Challenges. https://arxiv.org/abs/2304.04309

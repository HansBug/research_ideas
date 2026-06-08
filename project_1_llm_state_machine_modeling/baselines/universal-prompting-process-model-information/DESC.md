# 面向自然语言文本流程模型信息抽取的通用提示策略 / A Universal Prompting Strategy for Extracting Process Model Information from Natural Language Text Using Large Language Models

## 基本信息

- **标题**：A Universal Prompting Strategy for Extracting Process Model Information from Natural Language Text Using Large Language Models
- **中文标题**：面向自然语言文本流程模型信息抽取的通用提示策略
- **作者**：Julian Neuberger, Lars Ackermann, Han van der Aa, Stefan Jablonski
- **单位**：University of Bayreuth; University of Vienna
- **发表**：Conceptual Modeling, Springer Nature Switzerland, 2024, pp. 38--55
- **DOI**：10.1007/978-3-031-75872-0_3
- **链接**：[DOI](https://doi.org/10.1007/978-3-031-75872-0_3)；[开放 PDF](https://hanvanderaa.com/wp-content/uploads/2024/09/ER2024-A-Universal-Prompting-Strategy-for-Extracting-Process-Model-Information-from-Natural-Language-Text-using-Large-Language-Models.pdf)

**代码/仓库获取方式**：
- 原文在摘要脚注、实验设置和结论中明确说明代码、prompts、数据和 LLM answers 公开，并给出 GitHub 分支入口：[JulianNeuberger/llm-process-generation/tree/er2024](https://github.com/JulianNeuberger/llm-process-generation/tree/er2024)。

**数据集获取方式**：
- 论文实验使用 PET、DECON、ATDP 三个已有流程信息抽取数据集；原文说明本研究的代码、prompts 和 data 通过同一 GitHub 分支公开。
- PET 来自 Bellan et al. 的 PET dataset，并使用 Neuberger et al. 扩展的 ER 数据；DECON 来自 van der Aa et al. 的自然语言 Declare 约束抽取数据；ATDP 来自 Quishpi et al. 的文本流程描述注释数据。具体下载结构以公开仓库和原始数据集论文为准。

## 简报

本文研究如何用 LLM 从自然语言业务流程描述中抽取可用于流程模型生成的信息。它不是直接生成状态机，而是把文本中的活动、参与者、数据对象、实体指代和关系抽取出来，再用启发式算法展示这些信息可以服务于流程模型生成。

- **输入**：自然语言流程描述文本，包括业务流程说明、规则规程、工作指令等文本源。
- **方法**：面向 Mention Detection、Entity Resolution、Relation Extraction 的模块化 prompt strategy，包含 context、task description、restrictions、格式约束、few-shot 示例和若干消融验证过的提示组件。
- **输出**：流程模型信息抽取结果，例如 activities/actions、actors、data objects、entity resolution 结果、flow/performer/uses relations、Declare constraints 等；论文还用启发式算法展示从抽取信息生成流程模型的可行性。

```text
自然语言流程描述
  -> 通用模块化 LLM prompt + 输出格式约束 + few-shot 示例
  -> 流程元素/实体/关系/约束抽取结果
  -> 可进一步生成 BPMN 或 declarative process model 信息
```

研究动机是传统流程信息抽取长期依赖 rule-based 或小数据集机器学习方法，难以处理语言变体、跨句关系、隐式信息和小样本问题。方法创新在于系统化设计并消融验证面向流程信息抽取的通用 prompt 结构，而不是只做单个模型的演示。实验覆盖 PET、DECON、ATDP 三个数据集和八个 LLM，主要结论是 GPT-4o 等 LLM 能在多个任务上达到或超过既有 rule-based / ML baseline，最高可带来约 8% 的绝对 $F_1$ 提升。不足在于输出不是 STM 族模型，且仍存在 prompt 组件交互、幻觉、商业 API 成本和数据集质量限制。

## 研究问题与动机

### 问题背景

业务流程模型在企业流程设计、实现、执行和分析中很常见，但人工建模耗时。已有自动化流程模型生成通常先从自然语言文本中抽取流程相关信息，再把这些信息转成 BPMN、Declare 等流程建模语言。相比端到端 text-to-model，这种两阶段方法便于用信息抽取指标评估，也便于把抽取结果复用于不同目标语言、合规检查、形式化推理或流程查询。

### 核心问题

论文聚焦三个已建立的流程信息抽取子任务：

- **Mention Detection**：识别文本中与流程相关的 mention，例如 activity/action、actor、data/business object。
- **Entity Resolution**：识别不同 mention 是否指向同一流程实体，例如代词与前文对象的对应关系。
- **Relation Extraction**：识别 mention 之间的有向关系，例如 performer、uses、flow，或把 declarative process modeling 中的 constraint extraction 视为一种关系抽取。

### 研究动机

原文指出流程文本具有语言变体、上下文线索、长距离关系、隐式/歧义信息、文本长度影响和小数据集等挑战。传统 rule-based 方法可解释但迁移困难；机器学习方法受限于训练数据稀缺。LLM 具备零样本/少样本泛化能力，但也带来输出控制困难、输入呈现依赖、黑箱性、数据无感知和实验成本等新问题。因此，论文的目标是设计并验证一种可跨任务、跨数据集、跨 LLM 使用的流程信息抽取提示策略。

### 研究定位

这篇论文与 Project 1 的共同点是“自然语言文本 -> 结构化建模信息”的 LLM 建模链路；差异是它的目标工件是 BPM/流程建模信息，而不是状态机、Statechart、SysML 状态机或带时间/守卫语义的 STM。因此它是强行为/流程模型近邻，不是 exact STM direct baseline。

## 核心方法

### 方法概述

论文提出的 prompt structure 由三个模块组成：

- **Context**：把 LLM 设定为 business process modelling expert，并给出流程信息抽取任务的高层语境。
- **Task Description**：定义需要抽取的 mention type、relation type 和抽取步骤，形成面向任务的 meta language；示例中包括 activity、actor、actor performer relation。
- **Restrictions**：给出额外规则、消歧提示、严格输出格式和 few-shot 示例，用于提高可解析性并减少类型混淆。

该策略不是一次性直接生成流程图，而是先得到结构化抽取结果。论文随后用启发式算法展示抽取信息可被用于 process model generation，但核心贡献仍是 LLM-based process information extraction。

### LLM/Agent 设置

论文实验覆盖八个 LLM：

- GPT-4o
- GPT-4-2024-04-09
- GPT-4-0125-preview
- GPT-3.5-0125
- Claude 3 Opus
- Claude 3 Sonnet
- Llama 3 70B Instruct
- Qwen1.5 72B Chat

主要结果表使用 GPT-4o，temperature 设为 0，top-p 按 OpenAI 推荐保持不变。模型比较实验同样把各模型 temperature 设为 0。论文还测试了把 baseline prompt 拆成多个高度专门化 prompts 的做法，并称这些 prompts 为 agents：例如先由一个 agent 抽取 Actions，再把结果传给抽取 Actors 和 Business Objects 的 agents，以利用元素间依赖。该 agent 式拆分在 PET 的 MD 和 RE 任务上各带来约 +0.08 的绝对 $F_1$ 提升。

### Prompt 组件与反馈机制

论文显式讨论并实验了以下提示组件：

- persona：指定“流程建模专家”角色。
- context manager：限制任务语境，降低无关背景和幻觉风险。
- meta language creation：定义 mention/relation/constraint 类型。
- chain of thought：把抽取拆成 mention 抽取、relation 抽取、解释与事实列表等步骤。
- reflection：要求简要解释抽取结果，支持人工检查。
- fact check list：要求生成流程事实列表，用于 prompt engineering 和数据清理。
- formalized output format：用 pipe-separated tuple 等固定格式约束输出。
- format examples：提供输出格式示例。
- disambiguation hints：针对活动边界、actor 判定等易混类型给出规则。
- few-shot prompting：动态加入 raw textual process description 与期望输出样例。

反馈/验证机制主要体现在三层：一是严格格式与 parser 统计 parsing errors；二是 reflection/fact list 帮助 human-in-the-loop 检查抽取是否合理；三是通过与人工标注 gold standard 计算 precision、recall、$F_1$。论文不包含形式化验证、模型检查、仿真验证或自动修复闭环。

### 输出格式与模型类型

输出不是状态机族模型，而是流程模型生成所需的信息抽取结果。按数据集和任务不同，输出包括：

- PET：activities、actors、data objects 等 mention，ER 结果，以及 flow、uses、actor performer 等关系。
- DECON：与 Declare process modeling 相关的 constraint extraction 结果。
- ATDP：actions、conditions、entities、events 以及扩展约束类型。

因此，输出模型类型可概括为“流程模型信息抽取结构化元组 / declarative process constraint 信息”，不是 STM、Statechart、SysML 状态机、BPMN 图本体或可直接执行的形式模型。

## 实验与评估

### 数据集 / Benchmark

论文使用三个公开流程信息抽取数据集：

- **PET**：45 个文档，是论文称为当前最大的数据集，标注了 BPMN 建模有用的信息，包括 7 类 mention 和 6 类 relation，并包含跨句关系。论文使用 Neuberger et al. 2023 中带 ER 数据的扩展版本。
- **DECON**：17 个文本流程描述，标注 5 类 Declare constraint，支持 negated、unary 和 binary constraints；只包含至少描述一个 constraint 的句子。
- **ATDP**：18 个文本流程描述，与 DECON 有较大重叠，但包含不描述 constraint 的句子，并扩展到 8 类 constraint；还提供 actions、conditions、entities、events 标注。

### 评估指标

论文使用 precision、recall 和 $F_1$。正确性判定遵循各对比工作的原始评估方式，以保证和对应 baseline 的比较公平。

### 实验设置

实验包括四类：

- 在 PET、DECON、ATDP 上评估优化后的 prompt，并与当前最佳 rule-based / ML approaches 比较。
- 在 PET 的 MD 和 RE 任务上比较八个 LLM。
- 对 prompt 组件做 ablation study，观察移除 format examples、meta language、CoT、disambiguation、reflection、fact list 等组件后的效果和 parsing errors。
- 在 PET 上用 gpt-4o-2024-05-13、1-shot 设置重复 5 次，评估非确定性对结果稳定性的影响。

### 主要实验结果

关键结果包括：

- 在 PET 上，GPT-4o 相比 baseline 对 MD、ER、RE 分别带来约 5%、22%、17% 的绝对 $F_1$ 提升。
- 在 DECON 上，GPT-4o 的 RE 相比 rule-based baseline 最高提升约 8% 绝对 $F_1$。
- 在 PET 的 RE 任务上，GPT-4o zero-shot 即能达到或超过用 36 个人工标注文档训练的机器学习 baseline。
- 模型比较显示 GPT-4 系列和 Claude 3 Opus 表现较强；Llama 3 70B Instruct 在 few-shot 设置下接近 Claude 3 Sonnet，适合作为不能发送数据到商业 API 时的本地开放权重候选。
- 消融实验显示 format examples、meta language、CoT、disambiguation 和合理的描述具体性对性能或可解析性有用；persona 和 context manager 对该任务影响较小；reflection 与 fact list 对最终抽取分数未必总是正向，但对 prompt engineering、数据清理和人工审查有价值。
- 稳定性实验中，PET 的 MD 平均 $F_1$ 约 0.70、标准差 0.003，RE 平均 $F_1$ 约 0.89、标准差 0.002，论文据此认为结果波动不足以威胁结论有效性。

### 方法优势

- 充分利用 LLM 在小样本、语言变体、歧义和跨句推理上的能力，降低对大规模人工标注训练集的依赖。
- 严格输出格式和 format examples 降低 parser failure，是流程信息抽取进入后续自动建模管线的关键条件。
- 多模型、多数据集和消融实验比单模型演示更稳健。
- reflection 可辅助 human-in-the-loop 发现 gold standard 错误或歧义样本。

### 方法局限性

- 原文承认 prompt 组件列表可能不完备，组件之间的交互没有被 ablation study 完整覆盖。
- Qwen1.5 和 Llama 3 等模型会出现不存在的 entity/relation type 幻觉，few-shot 可缓解但不能完全消除。
- 商业高性能 LLM 的 token 成本限制大规模应用；开放权重或较便宜模型需要更多样例才能接近最佳表现。
- 数据集来源仍偏有限，未来需要检验跨领域泛化。
- 论文没有提供形式化验证、模型检查、仿真闭环或面向缺陷的自动修复机制。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **理由**：论文任务是 natural language text -> process model information extraction，并提出 universal prompting strategy；它与 Project 1 的“自然语言需求 -> 结构化建模工件”高度邻近，也同样重视 prompt、few-shot、输出格式约束、LLM 稳定性和数据集评测。但是论文输出不是状态机族模型，而是 BPM/Declare 流程建模所需的信息抽取元组和约束信息，因此不能算 `🟢` direct STM baseline，也不应误写成 exact STM direct baseline。

### 四条件建议

| 条件 | 建议 | 说明 |
|---|---|---|
| LLM4Modeling | 🟢 | 使用 LLM 从自然语言中抽取建模信息，并服务于流程模型生成。 |
| NL输入 | 🟢 | 输入明确是自然语言流程描述文本。 |
| LLM方法 | 🟢 | 核心方法是模块化 prompt strategy，并系统评估多个 LLM。 |
| STM族输出 | 🟡 | 输出是流程模型信息/Declare 约束等行为流程建模信息，不是 STM/Statechart/SysML 状态机。 |

### 可借鉴之处

- 可借鉴其“先抽取结构化建模信息，再生成模型”的两阶段路线，用于降低 Project 1 直接从需求到状态机的输出不可控风险。
- 可借鉴严格格式说明、format examples、meta language 和 parser error 统计，约束 LLM 输出为可机器处理的中间表示。
- 可借鉴多模型评估、zero/one/three-shot 对比、消融实验和重复运行稳定性评估，用于设计 Project 1 的 baseline audit。
- 可借鉴 reflection/fact list 作为人工审查、标注纠错和数据清理的辅助证据，但不能把它等同于形式化验证。

### 存在的不足与改进空间

- 目标语义缺少状态机的状态、事件、guard、transition、层次/并发、时间约束等核心元素。
- 论文的后续模型生成只作为启发式展示，不是严格定义的 STM 生成算法。
- 评估指标主要来自信息抽取，不覆盖状态机可执行性、可达性、确定性、死锁、活性或安全性质。
- 对控制系统或安全关键系统没有专门建模和验证设置。

### 对本研究的启发

Project 1 可以把该工作视作强近邻方法参照：它证明 LLM 在小样本自然语言建模信息抽取中具有竞争力，也说明格式约束、元语言定义和少样本示例对结构化输出至关重要。但 Project 1 若要形成 direct baseline，需要进一步把输出目标转向 STM 族模型，并补足状态机语义、控制系统需求、形式化检查和生成-验证-修复闭环。

## 重要的相关工作

### 1. 重要的前身类工作

- **Friedrich, Mendling, Puhlmann, 2011, Process model generation from natural language text, CAiSE**：原文在 related work 中称其为 seminal work，使用句法特征和词汇数据库信息识别句子和文档层面的模式，用于 BPMN model creation。它是“自然语言 -> 流程模型生成”路线的经典前身，说明本论文仍处在从文本抽取流程建模信息的研究链条中。
- **Bellan, Dragoni, Ghidini, 2022, Extracting business process entities and relations from text using pre-trained language models and in-context learning, EDOC**：原文将其作为已有 LLM-based approach，指出其局限包括只覆盖 activities、participants、performs relation 和 direct-consequences relation 等子集，缺少严格输出格式，且只评估 PET 的 7/45 个描述。本文直接针对这些局限做更系统的 prompt 和实验。
- **Neuberger, Ackermann, Jablonski, 2023, Beyond rule-based named entity recognition and relation extraction for process model generation from natural language text, CoopIS**：原文使用该工作的 ML extraction pipeline 作为 PET 上的主要 baseline，并使用其扩展 PET ER 数据。它是作者团队的直接前身之一。

### 2. 直接参与实验的 baseline

- **PET baseline, Bellan et al. 2022 / Neuberger et al. 2023**：PET 数据集上的当前最佳方案包括 conditional random fields 进行 MD、pre-trained neural co-reference resolver 进行 ER、decision tree ensemble 进行 RE。本文用这些报告分数作为 PET 对比。
- **DECON baseline, van der Aa et al. 2019, Extracting declarative process models from natural language, CAiSE**：该工作提出 rule-based 方法，结合多种 NLP 技术和 typed dependency relations 从自然语言中抽取 Declare constraints。本文把它作为 DECON 上 RE 的 rule-based baseline。
- **ATDP baseline, Quishpi, Carmona, Padro, 2020, Extracting annotations from textual descriptions of processes, BPM**：该工作提出基于 typed dependency structures 的 rule-based pattern ensemble，用于 MD 和 constraint extraction。本文在 ATDP 上与其比较。

### 3. 提供了重要论证的工作

- **Davies et al., 2006, How do practitioners use conceptual modeling in practice?, Data & Knowledge Engineering**：原文用其支撑流程模型在实践中的重要性。
- **van der Aalst, 2016, Process Mining - Data Science in Action, Springer**：原文用其作为 BPM/process mining 背景支撑，说明流程模型与流程分析的基础地位。
- **Franceschetti et al., 2023, A characterisation of ambiguity in BPM, ER**：原文在挑战部分引用其说明 BPM 文本中 ambiguity 的问题。
- **Bender et al., 2021, On the dangers of stochastic parrots, ACM FAccT**：原文在结果讨论中引用其说明 LLM 可能合成语言上合理但任务上错误的输出，是讨论幻觉和输出可靠性的背景。

### 4. 在技术上提供了支持的工作

- **White et al., 2023, A prompt pattern catalog to enhance prompt engineering with ChatGPT, arXiv**：原文用其 prompt pattern catalog 支撑 persona、context manager、meta language creation、reflection 等 prompt design patterns。
- **Min et al., 2023, Recent advances in natural language processing via large pre-trained language models, ACM Computing Surveys**：原文用其支撑 few-shot prompting 和“good prompt can be worth hundreds of labeled data points”等 LLM/NLP 经验。
- **Wei et al., 2022, Chain-of-thought prompting elicits reasoning in large language models, NIPS**：原文用其支撑 CoT 对复杂推理任务的作用。
- **Tornberg, 2024, Best practices for text annotation with large language models, arXiv**：原文用其支撑文本标注场景中的 LLM prompt best practices。
- **Dubois et al., 2024, AlpacaFarm, NeurIPS**：原文用 AlpacaEval 排名选择模型比较中的候选 LLM。

### 5. 其他重要工作

- **van der Aa et al., 2018, Checking process compliance against natural language specifications using behavioral spaces, Information Systems**：原文在引言中提到抽取信息可用于 compliance checking 和 formal reasoning，是流程信息抽取结果的下游用途背景。
- **Leopold et al., 2019, Searching textual and model-based process descriptions based on a unified data format, Software and Systems Modeling**：原文将其作为抽取信息可服务于 process querying 的例子。
- **Pesic, Schonenberg, van der Aalst, 2007, Declare, EDOC**：为 DECON/ATDP 中 declarative process constraints 提供建模背景。
- **Sukthanker et al., 2020, Anaphora and coreference resolution: A review, Information Fusion**：原文在 Entity Resolution 定义中引用，用于说明 ER 与 co-reference/anaphora resolution 的关系。

## 文献分类总结

本文处在“自然语言流程描述 -> 流程信息抽取 -> 流程模型生成/分析”的 BPM 文献链条中。它继承了 Friedrich et al. 的自然语言流程模型生成方向、DECON/ATDP/PET 等数据集和传统 rule-based / ML extraction baseline，同时把 LLM prompt engineering 系统引入流程信息抽取任务。

在 Project 1 baseline 体系中，它应归为“泛建模 / 行为流程模型近邻”，而不是“直接状态机生成”。其价值主要在于提示策略、结构化输出约束、few-shot 设计、多模型评测和稳定性/消融方法；其限制则是输出语义不覆盖 STM 族模型，缺少状态机形式语义和验证闭环。

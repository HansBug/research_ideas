# 大语言模型业务过程建模评估：框架、基准与自改进分析 / Evaluating Large Language Models on Business Process Modeling: Framework, Benchmark, and Self-Improvement Analysis

## 基本信息

- **标题**：Evaluating Large Language Models on Business Process Modeling: Framework, Benchmark, and Self-Improvement Analysis
- **中文标题**：大语言模型业务过程建模评估：框架、基准与自改进分析
- **作者**：Humam Kourani, Alessandro Berti, Daniel Schuster, Wil M. P. van der Aalst
- **单位**：Fraunhofer Institute for Applied Information Technology FIT；RWTH Aachen University；Process Intelligence Solutions
- **发表**：arXiv preprint, 2024
- **DOI**：原文未提供正式出版 DOI
- **链接**：https://arxiv.org/abs/2412.00023；PDF: https://arxiv.org/pdf/2412.00023

**代码/仓库获取方式**：
- 论文正文说明全部数据与结果可在 GitHub 获取，仓库为 https://github.com/humam-kourani/EvaluatingLLMsProcessModeling。
- 论文还介绍了支持该框架的 ProMoAI Web 工具，入口为 https://promoai.streamlit.app/。
- 本轮核验到 GitHub 仓库 README，其说明该仓库提供论文补充材料；由于 GitHub 匿名 REST API 命中限流，未逐文件核验仓库内部目录结构。

**数据集获取方式**：
- Benchmark 数据、实验结果与自改进实验材料按论文正文指向同一 GitHub 仓库获取：https://github.com/humam-kourani/EvaluatingLLMsProcessModeling。
- 原文描述的 benchmark 包含 20 个业务过程，每个过程配有自然语言过程描述、ground-truth POWL 过程模型和由 ground-truth 模型模拟得到的事件日志。

## 简报

这篇论文评估 LLM 从自然语言业务过程描述生成控制流过程模型的能力，并在同一框架下加入 benchmark 与自改进策略分析。它的核心不是状态机建模，而是 BPMN/Petri 网/POWL 业务过程建模；但它覆盖了“自然语言输入、LLM 生成结构化行为模型、执行/验证反馈、自改进”的完整链条，因此是 `project_1` 的强行为建模近邻。

- **输入**：自然语言业务过程描述；评测阶段还向 prompt 提供随机排序的 ground-truth 活动标签，用于标准化标签并支持自动 conformance checking。
- **方法**：通过 role prompting、POWL 知识注入、few-shot 示例、negative prompting、受限 Python 代码生成、执行校验、错误处理循环和用户反馈循环生成过程模型。
- **输出**：Python 代码生成的 POWL 中间模型，并可导出为 BPMN 或 Petri net。
- **输出模型类型**：业务过程控制流模型；POWL 是带控制流算子的部分序工作流语言，可转换为 BPMN/Petri net，不是状态机、Statechart 或 SysML 状态机。
- **实验设计**：用 20 个业务过程 benchmark 横评 16 个 LLM，并用 fitness、precision 及二者调和平均构成质量分数；另评估 self-evaluation、input optimization、output optimization 三种自改进策略。
- **结论与不足**：Claude-3.5-Sonnet、O1 系列和 Gemini-1.5-Pro-002 在质量和错误处理上表现较强；输出自优化对低质量初始输出更有潜力。局限是只覆盖控制流视角，未覆盖数据、资源、操作语义，也没有直接生成控制系统状态机。

```text
自然语言过程描述 + 活动标签
  -> LLM prompt engineering + 受限代码生成 + 错误/反馈循环
  -> POWL 中间过程模型
  -> BPMN / Petri net 导出与 conformance checking 评估
```

## 研究问题与动机

### 问题背景

业务过程建模是 BPM 的核心活动，传统上需要人工理解流程并掌握 BPMN、Petri net 等建模语言。LLM 具备自然语言理解和代码生成能力，因此可用于把文本流程描述转化为结构化过程模型。

### 核心问题

1. LLM 能否从自然语言业务过程描述生成高质量控制流过程模型。
2. 不同闭源和开放权重 LLM 在同一过程建模框架下的质量、错误处理和时间效率差异如何。
3. LLM 是否能通过自评估、输入自优化或输出自优化提升生成模型质量。

### 研究动机

作者此前提出过 LLM-based process modeling framework，本论文在此基础上扩展出更系统的 20 过程 benchmark、16 个 LLM 横评和自改进策略实验，目标是为 BPM 中的自动化过程建模建立更可复查的评测基础。

### 现有方法的局限性

原文指出，传统从文本抽取过程信息的方法多依赖 NLP、text mining、计算语言学或领域特定语言；已有 LLM/BPM 工作也包含过程发现、过程查询、对话式建模和过程模型理解，但缺少以 ground-truth 模型和事件日志为基础的过程建模质量评估。

### 研究目标

论文希望提供一个从自然语言到过程模型的自动化框架、一个覆盖多领域和多结构复杂度的 benchmark，以及一组可用于分析 LLM 自改进能力的实验。

## 核心方法

### 方法概述

框架从用户提供的自然语言过程描述开始，构造包含任务指令、POWL 知识、示例和约束的 prompt，要求 LLM 生成可执行 Python 代码。系统抽取并执行该代码，用预定义 `ModelGenerator` 函数创建 POWL 模型；若代码抽取、执行或 POWL 校验失败，则进入错误处理循环，把错误信息和历史对话重新提交给 LLM 修复。成功生成后，模型可以显示或导出为 BPMN/Petri net，用户也可给出文本反馈触发 refinement loop。

### 过程表示：POWL 中间模型

作者选择 Partially Ordered Workflow Language 作为中间表示，原因包括：

1. POWL 相比直接生成 BPMN/Petri net 更容易提供 soundness 保证。
2. POWL 的层次结构支持递归组合子模型，适合由 LLM 生成代码构造。
3. POWL 支持选择、循环和部分序依赖，表达能力强于 process tree，并能导出为 BPMN 或 Petri net。

需要注意的是，POWL/Petri net 与状态机都刻画行为结构，但本文目标模型仍是业务过程模型，不是 STM 族模型。

### Prompt Engineering

论文明确使用以下策略：

1. **Role prompting**：要求 LLM 扮演过程建模专家和 process owner，既理解常见流程构造，也能在描述有空缺时补足合理细节。
2. **Knowledge injection**：注入 POWL 语言知识、组件语义和预定义模型生成函数的使用方式。
3. **Few-shot learning**：提供过程描述到 Python/POWL 代码的示例对。
4. **Negative prompting**：明确要求避免常见建模错误，例如错误地把局部活动做成选择，而不是把完整路径建成选择。

### 代码生成、执行与安全约束

框架要求 LLM 生成受限 Python 代码，并通过预定义函数创建 POWL 模型。为降低执行 LLM 代码的风险，系统限制其只能使用预定义函数，并检查代码是否符合提示中的编码规则，不允许使用可能带来安全风险的外部库或构造。

### 反馈与验证机制

论文包含两类反馈/验证机制：

1. **运行时错误处理**：把 critical errors 和 adjustable errors 区分处理。critical errors 会反复提示 LLM 修复，直到成功或达到最大尝试次数；adjustable errors 若 LLM 多轮仍未修复，可由框架自动调整。
2. **模型质量评估**：通过 ground-truth POWL 模型模拟事件日志，再用 PM4Py 计算生成模型相对于日志的 fitness 与 precision，并以调和平均作为质量分数。

### LLM/Agent 设置

本文没有多 agent 体系，也没有独立规划 agent。LLM 被作为单个代码生成与修复模型调用。

横评的 16 个 LLM 包括：

1. OpenAI：GPT-4、GPT-4o、GPT-4o-Mini、O1-Preview、O1-Mini。
2. Google：Gemini-1.5-Pro-002、Gemini-1.5-Flash-002。
3. Anthropic：Claude-3.5-Sonnet。
4. Mistral AI：Mistral-Large-2、Codestral、Mixtral-8x22B。
5. Meta/DeepInfra：Llama-3.1-405B-Instruct、Llama-3.2-90B-Vision-Instruct。
6. Nvidia/DeepInfra：Llama-3.1-Nemotron-70B-Instruct。
7. Alibaba Cloud/DeepInfra：Qwen2.5-72B-Instruct。
8. Microsoft/DeepInfra：WizardLM-2-8x22B。

### 自改进策略

论文评估三种 LLM self-improvement：

1. **Self-evaluation**：每个过程生成 4 个候选模型，再让 LLM 根据 general criteria 或 conformance-based criteria 选择最佳候选。
2. **Self-optimization of input**：让 Gemini-1.5-Pro-002 改写和丰富长、中、短三类过程描述，再比较改写前后的生成质量。
3. **Self-optimization of output**：初始模型生成后，要求 LLM 对照原始描述只在确有收益时改进模型；实验对象为 Gemini-1.5-Pro-002、Gemini-1.5-Flash-002 和 GPT-4o。

## 实验与评估

### 数据集 / benchmark / 案例系统

benchmark 包含 20 个过程，记作 p1 到 p20：

1. 2 个过程改编自作者前作，包括 order handling process 和 hotel service process。
2. 18 个过程由作者构造，覆盖 manufacturing、healthcare、finance、logistics、customer service 等多种业务域。
3. 描述长度为 79 到 230 词、525 到 1567 字符。
4. ground-truth 模型活动数为 8 到 26。
5. 结构覆盖 choices、loops、partial orders，并故意保留部分并发/顺序歧义以测试 LLM 推断能力。

每个过程配有自然语言描述、ground-truth POWL 模型和由 ground-truth 模型模拟得到的事件日志。

### 评估指标

论文用 conformance checking 评估生成模型质量：

1. 从 ground-truth POWL 模型模拟事件日志。
2. 每个决策点按均匀分布处理，循环最多执行 2 次，以避免无限日志。
3. 每个唯一 trace variant 至少包含一个实例。
4. 用 PM4Py 计算 fitness 和 precision。
5. 质量分数取 fitness 与 precision 的调和平均；越接近 1，说明与 ground-truth 日志越一致。

### 实验设置

评测阶段为避免活动标签差异影响 conformance checking，prompt 中加入 ground-truth 日志的活动标签列表，并随机排序，要求 LLM 使用相同标签生成模型。该设置有利于自动化定量评估，但也意味着输入不再是纯自然语言描述。

错误处理设置为：adjustable errors 最多给 10 轮修复机会；超过后框架尝试自动修复；之后若仍有错误，再给 5 轮。15 轮后仍无法生成有效模型则记为失败。

### 主要实验结果

错误处理方面：

1. Claude-3.5-Sonnet 平均 1.35 次迭代，20 个过程里 16 个一次成功，无失败。
2. O1-Mini、O1-Preview 和 Gemini-1.5-Pro-002 平均迭代次数低于 2 或接近 2，也没有失败。
3. Mixtral-8x22B 和 Codestral 各出现 1 个 15 轮后失败案例。
4. WizardLM-2-8x22B 平均迭代次数最高，为 5.2，但没有 critical failure。

质量方面：

1. Ground truth 平均质量分数为 0.98。
2. Claude-3.5-Sonnet 平均 0.93，排名第一。
3. O1-Preview 为 0.92，O1-Mini 为 0.91。
4. Gemini-1.5-Pro-002 为 0.87。
5. Llama-3.1-405B-Instruct 为 0.86，Llama-3.1-Nemotron-70B-Instruct 为 0.83。
6. GPT-4、GPT-4o 和 GPT-4o-Mini 分别为 0.76、0.76 和 0.74。
7. Gemini-1.5-Flash-002、Codestral、WizardLM-2-8x22B 和 Mixtral-8x22B 位于 0.72 到 0.73 区间。

时间效率方面：

1. Gemini-1.5-Flash-002 平均总时间 14.51 秒，单轮 4.03 秒，速度最快但质量较低。
2. Claude-3.5-Sonnet 平均总时间 23.63 秒且质量最高。
3. Gemini-1.5-Pro-002 平均总时间 24.86 秒，质量和效率平衡较好。
4. O1-Preview 单轮较慢但因错误处理效率高，总体质量强。

自改进方面：

1. Self-evaluation 对 Gemini-1.5-Pro-002 有提升，平均质量从 0.86-0.88 提升到 0.91；但对 Gemini-1.5-Flash-002 反而略降到 0.72。
2. Input optimization 不稳定：长描述从 0.87 降到 0.79，中等长度描述从 0.75 升到 0.82，短描述从 0.78 降到 0.72。
3. Output optimization 最有潜力：Gemini-1.5-Flash-002 从 0.73 升到 0.76，GPT-4o 从 0.76 升到 0.81；Gemini-1.5-Pro-002 基本持平。

### 方法优势

1. 把 LLM 代码生成、模型执行、错误处理和 conformance checking 接成闭环。
2. POWL 中间表示降低了直接生成 BPMN/Petri net 时出现不 sound 模型的风险。
3. Benchmark 不只看自然语言回答，而是评估可执行、可导出、可 conformance check 的结构化模型。
4. 对多家供应商和开放权重模型进行横评，有较高复现实验设计价值。

### 方法的局限性

1. 输出是业务过程模型，不是状态机族模型。
2. 评测时向 LLM 提供活动标签，降低了纯自然语言建模难度。
3. 框架主要覆盖 control-flow perspective，未覆盖业务过程的数据、资源和操作语义视角。
4. 作者没有纳入成本评估，理由是 LLM 价格变化过快。
5. 自评估和输入自优化结果依赖模型与任务设置，不能直接泛化到控制系统状态机建模。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **四条件建议**：LLM4Modeling 🟢；NL输入 🟡；LLM方法 🟢；STM族输出 🟡。
- **Direct baseline 关系**：否。本文输出不是状态机、Statechart 或 SysML 状态机，不能作为 exact STM direct baseline。
- **Near baseline 关系**：强。本文从自然语言生成结构化行为模型，并有错误处理、反馈循环、ground-truth benchmark 和 conformance checking 评估，和 `project_1` 的“生成-验证-修复”方法链高度邻近。
- **Related-work 关系**：强。本文可作为 LLM4Modeling、行为/过程模型 benchmark、自改进策略、模型质量自动评估和复现实验设计的重要相关工作。

它应被保留为“LLM business process modeling framework/benchmark/self-improvement”的近邻工作，而不是写成状态机 direct baseline。BPMN、Petri net 和 POWL 虽然都刻画行为控制流，但目标语义、建模对象和评测任务与控制系统状态机仍不同。

### 可借鉴之处

1. **中间表示设计**：POWL 的 soundness 保证说明，可用受约束中间 DSL 降低 LLM 直接生成复杂模型的错误率。
2. **错误处理闭环**：critical/adjustable error 分层有助于区分“必须回到 LLM 修复”的错误和“可由后处理自动修复”的错误。
3. **活动标签标准化**：为可自动评测牺牲一部分自然语言自由度，这对 `project_1` 设计可控 benchmark 有启发。
4. **conformance checking 质量分数**：fitness、precision 与调和平均可迁移为状态机行为一致性评估思路。
5. **自改进实验设计**：分别测试自评估、输入自优化和输出自优化，有助于拆解“LLM 自修复”到底在哪个环节有效。

### 存在的不足与改进空间

1. 没有面向控制系统、嵌入式系统或安全关键系统。
2. 没有时间约束、层次并发状态机、guard/action、事件触发语义或 STM 专用结构。
3. 没有模型检查器意义上的安全/活性性质验证；conformance checking 针对的是过程日志一致性。
4. Benchmark 的 ground-truth 活动标签进入 prompt 后，不能完全代表“从非形式化需求直接生成模型”的难度。
5. 代码和数据虽然有 GitHub 入口，但本轮未逐文件确认每个输入、输出和 raw result 的完整可复现性。

### 对本研究的启发

`project_1` 可借鉴本文的三点：第一，用受控 DSL 或结构化 API 降低 LLM 生成非法模型的概率；第二，把错误诊断、自动修复和 LLM 修复分层；第三，为 benchmark 设计 ground truth、行为日志/轨迹、结构标签和自动评分指标。但在论文表述中必须明确，本文是过程建模近邻，不是 STM 直接 baseline。

### 研究定位与差异化

本文最适合放在“LLM 生成行为/过程模型”的相关工作链条中。与 `project_1` 相比，它的输入较接近，方法链较接近，验证思想较有价值，但输出模型类型和目标领域不同，因此建议评为 🟠，而不是 🟢 或 🟡。

## 重要的相关工作

### 1. 重要的前身类工作

- **Kourani et al., 2024, Process Modeling with Large Language Models**：这是本文直接扩展的前作。原文在引言和相关工作中明确说明，本文在此前 LLM-based process modeling framework 的基础上增加更大的 benchmark、更多 LLM 和自改进策略分析。
- **Kourani and van Zelst, 2023, POWL: Partially Ordered Workflow Language**：为本文的中间表示提供基础。本文选择 POWL 是因为其层次结构、soundness 保证和到 BPMN/Petri net 的导出能力。
- **Kourani et al., 2024, ProMoAI: Process Modeling with Generative AI**：为本文框架提供工具支持。本文第 4 节说明 ProMoAI 支持 Google、OpenAI 和 DeepInfra 等 provider，并允许用户生成、查看、下载和反馈改进过程模型。

### 2. 直接参与实验的 baseline

- **16 个 LLM 作为横评对象**：实验直接比较 GPT-4、GPT-4o、GPT-4o-Mini、O1-Preview、O1-Mini、Gemini-1.5-Pro-002、Gemini-1.5-Flash-002、Claude-3.5-Sonnet、Mistral-Large-2、Codestral、Mixtral-8x22B、Llama-3.1-405B-Instruct、Llama-3.2-90B-Vision-Instruct、Llama-3.1-Nemotron-70B-Instruct、Qwen2.5-72B-Instruct 和 WizardLM-2-8x22B。
- **Ground-truth POWL 模型与模拟事件日志**：它们不是算法 baseline，但在实验中构成质量评分的参照物。生成模型通过 conformance checking 与 ground-truth 日志比较。

原文没有把传统 NLP-to-BPMN 方法作为定量对比 baseline；这些工作主要出现在 related work 中用于定位问题背景。

### 3. 提供了重要论证的工作

- **Bellan et al., 2020, A qualitative analysis of the state of the art in process extraction from text**：支撑“从文本抽取过程信息”已有研究脉络。
- **Goncalves et al., 2011, Let me tell you a story - on how to build process models**：代表从文本构造过程模型的早期 NLP/text mining 路线。
- **Friedrich et al., 2011, Process model generation from natural language text**：代表自然语言到 BPMN 生成的经典工作。
- **Sholiq et al., 2022, Generating BPMN diagram from textual requirements**：支撑文本需求到 BPMN 图生成方向。
- **Ivanchikj et al., 2020, From text to visual BPMN process models**：作为 text-to-BPMN process model 设计与评估的相关基础。
- **Busch et al., 2023 与 Vidgof et al., 2023**：支撑 LLM 在 BPM 中的机会、挑战和 prompt engineering 讨论。
- **Fill et al., 2023 与 Muff and Fill, 2024**：支撑 LLM 在概念建模中的潜力与局限讨论。

### 4. 在技术上提供了支持的工作

- **BPMN 与 Petri net 文献**：BPMN 和 Petri net 是本文最终导出的标准过程模型表示，支撑其与 BPM 社区工具链对接。
- **Conformance checking 文献**：Dunzer et al. 的综述用于支撑 conformance checking 评估思路；Berti and van der Aalst 的 token-based replay、Munoz-Gama and Carmona 的 precision 指标和 PM4Py 工具支撑具体质量计算。
- **Prompt engineering 文献**：expert prompting、knowledge injection、few-shot learning 和 negative prompting 相关文献分别支撑本文的 prompt 设计策略。
- **Self-evaluation / non-determinism 文献**：Zhang et al. 的 self-evaluation 研究与 Song et al. 对 LLM 非确定性的讨论，为第 6 节自改进实验提供依据。

### 5. 其他重要工作

- **PM-LLM-Benchmark**：原文将其作为 process mining/BPM 任务上 LLM benchmark 的相关工作，并指出本文与其不同之处在于使用过程描述、ground-truth 模型和事件日志进行更客观的模型质量评估。
- **BPM/Process mining 基础文献**：van der Aalst 的 process mining 书籍提供业务过程发现、符合性检查和改进的背景。
- **BERT-log 与语义感知 process mining benchmark**：这些工作支撑 LLM/NLP 在过程监控、异常检测、语义任务中的扩展背景，但不是本文方法组件。

## 文献分类总结

- **研究定位**：LLM 驱动的业务过程建模框架、benchmark 与自改进策略评估。
- **任务类型**：自然语言业务过程描述到结构化过程模型的自动生成与修复。
- **输入工件**：自然语言过程描述；评测时附加标准化活动标签；benchmark 内部还包含 ground-truth POWL 和模拟事件日志。
- **输出工件**：POWL 模型及可导出的 BPMN/Petri net。
- **输出模型类型**：业务过程控制流模型，不是 STM 族模型。
- **使用的LLM**：16 个闭源/API 与开放权重托管模型，覆盖 OpenAI、Google、Anthropic、Mistral、Meta、Nvidia、Alibaba Cloud、Microsoft 等来源。
- **主要方法**：prompt engineering + 受限 Python 代码生成 + POWL 中间表示 + 执行校验 + 错误处理循环 + 用户反馈循环 + conformance checking 评估。
- **反馈/验证机制**：代码执行与 POWL 校验、错误修复 prompt、用户文本反馈、PM4Py fitness/precision 质量评分。
- **数据集/benchmark**：20 个业务过程、ground-truth POWL 模型和模拟事件日志；论文指向公开 GitHub 仓库。
- **代码/数据获取方式**：GitHub artifact: https://github.com/humam-kourani/EvaluatingLLMsProcessModeling。
- **是否面向控制系统或安全关键系统**：否，主要面向 BPM/business process modeling。
- **BASELINE评估**：🟠。
- **Project 1 关系**：强行为/过程建模近邻，评测与复现价值高；可支撑 benchmark 设计、LLM 反馈闭环和验证评分方法，但不能作为状态机 direct baseline。

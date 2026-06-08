# 基于需求的 LLM Simulink 模型切片 / Requirements-Driven Slicing of Simulink Models using LLMs

## 基本信息

- **标题**：Requirements-Driven Slicing of Simulink Models using LLMs
- **中文标题**：基于需求的 LLM Simulink 模型切片
- **作者**：Dipeeka Luitel, Shiva Nejati, Mehrdad Sabetzadeh
- **单位**：加拿大渥太华大学电气工程与计算机科学学院
- **发表**：2024 IEEE 32nd International Requirements Engineering Conference Workshops (REW 2024)，AIRE 2024 workshop，页码 72--82
- **DOI**：10.1109/REW61692.2024.00014
- **链接**：[DOI](https://doi.org/10.1109/REW61692.2024.00014)；[arXiv:2405.01695](https://arxiv.org/abs/2405.01695)；[PDF](https://arxiv.org/pdf/2405.01695)

**代码/仓库获取方式**：
- 原文未提供公开代码或仓库获取链接。
- 原文描述了 Simulink 模型转文本、prompt 构造、LLM 输出 SID 列表、补全可执行切片等流程，但未给出可复现脚本、仓库、artifact DOI 或补充材料入口。

**数据集获取方式**：
- 原文实验使用 Lockheed Martin 的公开 CPS Simulink benchmark 中的 Effector Blender 与 Tustin Integrator 模型，并引用 Mavridou 等人在 IEEE RE 2020 的 benchmark 论文。
- 原文未提供该 benchmark 的直接下载链接，也未给出本文实验 prompt、需求文本、生成切片或 40 个测试用例的公开下载入口。

## 简报

本文研究的问题是：给定一个图形化 Simulink 模型和一条自然语言需求，如何用 LLM 自动识别满足该需求所需的 Simulink block，并构造对应的模型切片。该任务面向安全关键 CPS 模型审查和认证场景，目标是减少审查者为了检查某条需求而阅读整个模型的工作量。

- 输入：图形化 Simulink 模型、自然语言需求、prompt 模板、可选训练示例、模型转文本的 verbosity 级别。
- 方法：先把 Simulink XML/块图信息转成文本，再用 ChatGPT over GPT-4.0-classic 在 zero-shot、N-shot 或 chain-of-thought prompt 下输出相关 block 的 SID 列表，最后用确定性规则补齐 Inport/Outport、Goto/From 等边界块并处理悬空输入，生成可编译模型切片。
- 输出：针对单条自然语言需求的 Simulink 模型切片，即原 Simulink block diagram 的相关子模型；不是 Stateflow、状态机、Statechart 或形式化 DSL。

```text
自然语言需求 + 图形化 Simulink 模型
        -> 模型转文本 + prompt 构造 + LLM 识别相关 SID
        -> 可编译 Simulink 模型切片
```

研究动机是，传统需求到设计模型的追踪和切片往往依赖人工 trace links，而 Simulink 模型在安全关键 CPS 中常规模大、审查成本高。方法创新在于把“需求”和“模型”都转为文本，让 LLM 直接在二者之间建立需求相关 block 的隐式关联，再由后处理构造 sound slice。实验使用 Effector Blender 作为训练示例来源、Tustin Integrator 作为评估模型，比较 3 种模型文本粒度和 3 种 prompting 策略。结论是 medium verbosity 加 chain-of-thought 或 zero-shot 的配置产生最多准确切片；不足是实验只覆盖一个训练模型、一个测试模型和一个 LLM，且切片正确性依赖测试而非穷尽形式验证。

## 研究问题与动机

### 问题背景

Simulink 是 CPS 和控制系统领域常用的块图建模环境，常用于动态系统、控制逻辑和软件设计建模。安全认证和设计审查需要确认模型是否满足安全需求，但一条需求通常只涉及模型中的一小部分 block。若审查者必须阅读完整模型，成本高且容易出错。

### 核心问题

本文要解决的是 requirements-driven model slicing：对一条自然语言需求 $R$，从给定 Simulink 模型中找出足以判断该需求是否满足的相关 block 子集，并生成对应的可执行 Simulink 子模型。

该问题与 Project 1 的相似点在于输入包含自然语言需求，且 LLM 需要理解控制系统模型结构。关键差异是，本文输出是已有 Simulink 模型的需求相关切片，不是从自然语言需求生成新的状态机模型。

### 研究动机

已有 Simulink/SysML 切片和追踪方法通常需要人工建立 trace links，或者依赖传统 NLP/静态切片规则。LLM 有可能直接把自然语言需求和模型文本表示放在同一 prompt 中处理，从而弱化对人工 traceability 的依赖。

### 研究目标

本文目标包括：

1. 设计一种把 Simulink block diagram 转成 LLM 可处理文本的方式。
2. 比较不同文本粒度对 LLM 切片结果的影响。
3. 比较 zero-shot、N-shot、chain-of-thought 三类 prompting 策略。
4. 用 Simulink 测试框架评估生成切片是否保留原模型对需求的满足或违反判断。

## 核心方法

### 方法概述

论文提出一个三阶段 pipeline：

1. **Simulink 模型转文本**：利用 Simulink 已有 XML 风格文本表示，按 high、medium、low 三种 verbosity 提取 block 信息。
2. **LLM 识别相关 block**：把模型文本、需求文本、prompt 模板和可选示例组合成 prompt，要求 LLM 输出满足需求所需 block 的 SID 列表。
3. **构造模型切片**：根据 LLM 输出的 SID 列表保留相关 block，再补齐可编译性所需边界 block，并用常量块处理悬空输入。

### 输入与中间表示

- **自然语言输入**：待分析的 Simulink 需求语句，例如 Tustin 模型中关于 reset、initial condition、top/bottom limits 和 output 的自然语言需求。
- **模型输入**：已有图形化 Simulink 模型，包括 block type、block name、SID、block properties、连接和部分图形布局信息。
- **中间文本表示**：
  - high verbosity：保留 block 属性和视觉渲染坐标等信息。
  - medium verbosity：保留语法和语义相关 block 属性，去掉视觉渲染信息。
  - low verbosity：主要保留 block name、type、SID 等基础轮廓。

### LLM/agent 设置

- **使用的 LLM**：ChatGPT over GPT-4.0-classic。
- **agent 设置**：原文未使用多 agent 或自主 agent loop；LLM 只作为 prompt-based block selector。
- **温度设置**：实验使用 ChatGPT 默认 temperature，原文说明约为 0.7，以保留一定响应多样性。
- **重复运行**：每个 prompt 配置重复 3 次，并额外取 3 次输出的 union 生成组合切片。
- **prompting 策略**：zero-shot、N-shot、chain-of-thought。
- **few-shot / CoT / RAG / 自反思**：包含 N-shot 和 CoT；未使用 RAG；未描述自反思或 LLM 自动修复闭环。

### Prompt 构造

Prompt 模板包含：

1. Tip 对 model slicing 的定义。
2. 待切片 Simulink 模型的文本表示。
3. 可选训练示例。
4. 要求 LLM 解析 Simulink 模型并抽取满足指定需求的 block 与 SID。
5. 具体自然语言需求。
6. 要求输出 block id 列表。

N-shot 示例包含训练模型文本、训练需求和正确 slice 的 block SID 列表。CoT 示例额外包含推理步骤，解释为何某些 block 类别与需求相关。

### 切片构造与可执行性修补

LLM 输出的 `BlockList` 不直接等于最终模型切片。方法会加入若干 edge cases：

1. 为了输入输出完整性加入必要的 Inport 和 Outport。
2. 对 Goto/From 这类成对 block，如果一端被选中则补齐另一端。
3. 对切片中悬空输入端口加入 constant block。
4. constant block 的值通过执行原模型的一组随机测试输入获取，作为被切掉部分的近似替代。

### 反馈/验证机制

本文没有把测试失败结果反馈给 LLM 进行迭代修复，也没有形式化模型检查闭环。验证机制主要是后验评估：

1. 先检查生成切片能否编译和执行。
2. 再使用已有 Simulink 测试框架比较原模型与切片在需求 fitness function 上的 polarity 是否一致。
3. 若原模型和切片对同一测试用例都满足或都违反需求，则认为该测试用例上切片保持需求判断。
4. 额外识别 vacuous satisfaction，避免空切片因蕴含式需求而被误判为准确。

## 实验与评估

### 数据集 / benchmark

实验使用 Lockheed Martin CPS Simulink benchmark 中的两个模型：

| 模型 | 用途 | 简述 | block 数 | 输入数 | 输出数 | 需求数 |
|---|---|---|---:|---:|---:|---:|
| Effector Blender | 训练示例 | 为车辆计算最优 effector configuration 的控制器 | 95 | 1 | 7 | 3 |
| Tustin Integrator | 测试/评估 | 计算时间积分的数值模型 | 57 | 5 | 10 | 5 |

数据集/benchmark 可获取性：原文说明该 benchmark 是 public-domain，但本文没有提供直接下载链接；本文自身的 prompt、LLM 原始输出、切片文件和测试用例也未提供公开获取入口。

### 实验设置

实验变量为：

1. 模型文本粒度：high、medium、low。
2. Prompting 策略：chain-of-thought、N-shot、zero-shot。
3. 需求：Tustin 模型的 5 条自然语言需求。
4. 重复：每个配置重复 3 次，并构造 3 次结果的 union。

总运行数：

1. 单次迭代切片：$9 \times 5 \times 3 = 135$。
2. union 切片：$9 \times 5 = 45$。
3. 总切片数：180。

评估中还为 Tustin 生成了 40 个测试用例，用于比较原模型与切片的需求 fitness polarity。

### 评估指标

- **可编译/可执行性**：切片是否能在 Simulink 中编译和执行。
- **准确性**：切片与原模型在需求 fitness function 上的正负 polarity 是否一致，且不是 vacuous satisfaction。
- **简洁性**：准确切片包含的 block 数量，反映切片是否只保留必要 block。

### 主要实验结果

- 所有 Tustin 切片都可以编译和执行。
- 180 个切片中有 83 个被评为准确。
- 取 3 次 LLM 输出的 union 往往比单次输出更准确；45 个 union 切片中只有 3 个不准确。
- medium verbosity 表现最好，在 60 个切片中有 28 个不准确，优于 high verbosity 的 30 个不准确和 low verbosity 的 38 个不准确。
- low verbosity 容易丢失必要语义，产生最多 vacuous slices。
- high verbosity 会把视觉渲染等无关细节放入 prompt，可能增加 hallucination 或错误 block 选择。
- N-shot 切片通常更简洁，但不准确率最高，因此论文不建议以简洁性牺牲准确性。
- medium verbosity + chain-of-thought 与 medium verbosity + zero-shot 是论文认为最有效的两类配置。
- 平均来看，准确切片约把 Tustin 的搜索空间从 57 个 block 缩小到 10.8 个 block，约为原模型的五分之一。

### 方法优势

1. 不要求人工预先建立需求到 block 的 trace links。
2. 能把图形化 Simulink 模型转成文本后交给 LLM 处理，降低 LLM 直接处理图形模型的难度。
3. 把 LLM 的非结构化能力限制在 SID 选择任务中，最终切片仍由确定性后处理构造。
4. 明确比较了模型文本粒度和 prompting 策略，对后续 LLM 建模任务有可迁移价值。

### 方法局限性

1. 实验规模小，只使用一个训练模型和一个测试模型。
2. 只使用一个 LLM，无法判断不同模型提供商或不同 GPT 版本下的稳定性。
3. 评估依赖有限测试用例，不是穷尽验证；原文明确说明不能最终证明切片满足需求。
4. 没有开放代码、prompt、LLM 原始输出或实验切片，复现性受限。
5. 输出不是状态机族模型，无法直接作为 Project 1 的 exact STM generation baseline。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：🟠。**

理由是：本文确实满足“自然语言需求 + LLM 方法 + 控制系统模型工件”的关键条件，并且任务是从自然语言需求定位相关模型结构；但其输出是 Simulink 模型切片，不是状态机、Statechart、Stateflow、SysML 状态机或形式化 STM/DSL。因此它不能作为 Project 1 的直接状态机生成 baseline，只能作为弱相关/邻近 baseline。

四条件建议：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 明确使用 ChatGPT/GPT-4.0-classic 对 Simulink 模型工件执行建模分析任务。 |
| NL输入 | 🟢 | 每次切片由自然语言需求驱动。 |
| LLM方法 | 🟢 | 核心 block 选择依赖 LLM prompt 输出 SID 列表。 |
| STM族输出 | 🟠 | 输出是 Simulink block/data-flow slice，属于控制系统模型工件与 trace/slicing 支撑证据；它不是 Stateflow、状态机、Statechart 或强行为近邻输出。 |

### 可借鉴之处

1. **模型即文本**：把 Simulink XML/block 属性转成不同粒度文本，为 Project 1 的工具 DSL prompt 设计提供近邻经验。
2. **LLM 输出受控化**：让 LLM 输出 SID 列表，再由确定性程序构造有效模型，可借鉴到“LLM 生成候选结构 + 工具修补/验证”的架构。
3. **verbosity 消融**：high/medium/low 模型文本粒度对准确性的影响，提示 Project 1 不应把所有模型细节无筛选塞入 prompt。
4. **测试式验证剖面**：虽然不是形式化验证，但其 compile、execute、fitness polarity、vacuity 检查可以启发状态机生成后的行为一致性评估。

### 存在的不足与改进空间

1. 本文没有生成新的状态机模型，也没有输出形式化可验证 DSL。
2. 未确认使用 Stateflow 或状态机族输出，不能误写成 exact STM direct baseline。
3. 对 LLM 输出错误没有自动反馈修复，只是在实验阶段评估切片准确性。
4. 缺少公开 artifact，使 prompt、切片和测试结果难以直接复用。
5. 只验证一个测试模型，尚不足以支持跨控制系统类别的结论。

### 对本研究的启发

Project 1 可以把本文作为“自然语言需求到已有控制系统模型相关子结构”的近邻工作，用于论证 LLM 在控制系统建模工件上可执行结构定位和受控输出。但 Project 1 的目标更进一步：从非形式化需求生成结构化状态机模型，并纳入形式语义、约束和验证闭环。因此本文更适合作为 related-work/near baseline，而非直接对比的 exact STM baseline。

## 重要的相关工作

### 1. 重要的前身类工作

- **Tip, 1994, A survey of program slicing techniques**：原文采用该工作对 model slicing/slicing criterion 的定义作为 prompt 模板开头，用来向 LLM 说明切片任务。
- **Nejati 等, 2011/2012, SafeSlice 相关工作**：原文将 SafeSlice 作为 SysML traceability 与 design slicing 前身，指出这些工作依赖人工 traceability，而本文尝试用 LLM 自动化需求到模型 block 的关联。
- **Mavridou 等, 2020, The ten Lockheed Martin cyber-physical challenges**：提供本文实验所用 Lockheed Martin CPS Simulink benchmark 的来源线索，其中包含 Tustin 等模型。

### 2. 直接参与实验的 baseline

- 原文未提供传统切片方法、非 LLM 方法或其他 LLM 方法的逐项结果对比。实验主要是本文方法内部不同 verbosity 和 prompting strategy 的消融比较。

### 3. 提供了重要论证的工作

- **Alenazi 等, 2020, safety requirements and state-based design models tracing**：原文用该类工作说明已有安全需求到状态设计模型追踪可借助 mutation 和 model checking，但与本文不同，本文聚焦 Simulink block 切片且不先建立显式 trace links。
- **Nejati 等, 2016, SysML requirements/design change impact analysis**：支撑“需求变更影响分析和模型切片都在识别模型元素相关性”这一定位。
- **Arora 等, 2015, natural language requirements change impact analysis** 与 **Hajri 等, 2018, product-line use case model change impact analysis**：用于说明 NLP 和模型分析曾用于需求变更影响分析，但本文目标是需求到 Simulink block 的切片。

### 4. 在技术上提供了支持的工作

- **Brown 等, 2020, Language Models are Few-Shot Learners**：支撑 GPT/ChatGPT 能进行 prompt-based learning 的技术背景。
- **Liu 等, 2023, Pre-train, Prompt, and Predict**：支撑 zero-shot、few-shot、chain-of-thought 等 prompting 策略背景。
- **Nejati 等, 2019; Matinnejad 等, 2014/2017/2019, Simulink testing framework**：本文使用既有 Simulink requirements testing 框架，通过 fitness function 和测试输入评估切片与原模型对需求判断的一致性。
- **Beer 等, 1997, vacuity detection**：支撑本文识别 vacuous satisfaction 的评估注意事项。

### 5. 其他重要工作

- **Griebl 等, 2023, block-based programs and language models**：原文把该工作作为“把图形化 block-based 程序转成文本后用语言模型分析”的邻近工作，但强调本文对象是 Simulink，任务是需求驱动切片。
- **Zhao 等, 2017; Guo 等, 2017, traceability recovery with embeddings/deep learning**：原文用这些工作说明机器学习已用于 traceability recovery，而本文探索 LLM 对 trace links 或模型切片的潜力。
- **Clarke 等, 2001; Henzinger 等, 1998; Alur 等, 1995/2011**：支撑本文关于 Simulink/hybrid systems 形式化模型检查局限的讨论。

## 文献分类总结

本文位于“需求驱动的模型切片 / traceability / LLM 辅助建模工件分析”交叉位置。它继承了 program/model slicing 的任务定义，使用 Lockheed Martin CPS Simulink benchmark 和既有 Simulink testing framework 进行评估，并把 LLM 用作自然语言需求到 Simulink block 的结构选择器。

在 Project 1 baseline 体系中，本文应归为“LLM-assisted model slicing / 控制系统模型工件近邻”。它对 Project 1 有方法借鉴价值，尤其是模型转文本粒度、受控 LLM 输出、后处理构造和测试式验证；但由于输出不是状态机族模型，不能归为 exact STM direct baseline。证据不足或原文未提供的信息包括：公开代码、实验数据下载入口、完整 prompt/response、是否存在 Stateflow/状态机输出，以及跨多个 Simulink benchmark 的泛化结果。

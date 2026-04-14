# 面向状态机建模的结构驱动与事件驱动大语言模型框架 / Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models

## 基本信息

- **标题**：Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models
- **中文标题**：面向状态机建模的结构驱动与事件驱动大语言模型框架
- **作者**：Samer Abdulkarim, Evan Boyd, Karl Bridi, Alec Tufenkjian, Boqi Chen, Gunter Mussbacher
- **单位**：McGill University, Department of Electrical and Computer Engineering
- **发表**：arXiv 预印本（`cs.SE`），2026-03-31
- **DOI**：10.48550/arXiv.2604.00275
- **链接**：https://arxiv.org/abs/2604.00275

**代码/仓库获取方式**：
- 原文在参考文献 `[18]` 中给出匿名工件入口：[anonymous.4open.science/r/llm_state_machine_modeling](https://anonymous.4open.science/r/llm_state_machine_modeling/)
- 正文未给出实名 GitHub / Zenodo 仓库；当前更明确的公开入口就是上述匿名 artifact 页面

**数据集获取方式**：
- 原文同样通过匿名工件页提供 paper artifacts；正文说明实验使用了 `8` 个非结构化 reactive-system descriptions 及其专家参考状态机
- 正文未给出单独命名的数据集主页；若匿名 artifact 后续失效，则需要联系作者获取实验材料

## 简报

本文关注的问题是：能否直接从**非结构化自然语言需求/系统描述**自动生成 UML 状态机，而不再依赖 `GWT`、use case 或其他先验结构化输入。作者把状态机生成拆成四条路线：`Single-Prompt Baseline`、`Structure-Driven SMF`、`Event-Driven SMF`、`Hybrid Approach`，并对 `states / transitions / guards / actions / hierarchical states / parallel regions / history states` 做了逐项 `precision / recall / F1` 评测。

- **输入**：非结构化英文 reactive-system description
- **方法**：单提示直接生成，或通过结构驱动/事件驱动多步 prompting 逐步构造状态机；`Hybrid` 先给出单提示 Umple 草稿，再用结构驱动步骤迭代细化
- **输出**：UML state machine（单提示直接输出 `Umple`；多步框架先输出 `HTML tables`，再经后处理整理为状态机）

```text
非结构化自然语言系统描述
  -> {Single-Prompt | Structure-Driven SMF | Event-Driven SMF | Hybrid}
  -> LLM 逐步生成/细化状态机元素 + 规则式后处理
  -> UML state machine
```

一句话结论：这是目前仓库里最贴近“自由文本 -> 状态机”主任务的直接 baseline 之一，但即便是 `Claude 3.5 Sonnet`，单提示总体 `F1 = 0.7029`，`actions / parallel regions / history states` 仍明显偏弱，离完全自动化还有距离。

## 研究问题与动机

### 问题背景

UML 状态机是软件工程中描述动态行为的重要建模工件，但传统流程高度依赖经验建模者从自然语言需求中手工恢复状态、事件、守卫和动作。已有自动化方法通常要求更结构化的需求表示，例如日志、执行轨迹或 `Given-When-Then` 风格输入，而不是直接面对自由文本。

### 核心问题

作者试图回答三个层次的问题：

1. 单次 prompting 是否已经足够支持从非结构化需求直接生成 UML 状态机。
2. 对非推理型 LLM 来说，把任务拆成结构驱动或事件驱动的多步流程，是否能提升状态机质量。
3. 这些多步流程是否也能自然迁移到推理型 LLM 上。

### 研究动机

核心动机很直接：如果 LLM 能从非结构化需求稳定恢复状态机，那么建模过程就不必先经过 `use case / GWT / DSL` 这类中间规整层，状态机设计可以更接近“从原始需求直接落到行为模型”的理想流程。这也是本文对 `project_1` 最有价值的地方。

### 研究意义

这篇论文的意义主要有三点：

1. 它把任务定义明确推进到“非结构化 NL -> UML state machine”，比很多仍依赖结构化输入的工作更贴近本课题。
2. 它不仅比较整体状态机质量，还把状态机拆成 `states / transitions / guards / actions` 等细粒度槽位，能直接告诉我们哪一类语义最难。
3. 它同时比较非推理型与推理型 LLM，说明“多步框架是否有用”并不是统一结论，而与模型类型密切相关。

## 核心方法

### 方法概述

框架输入是非结构化自然语言系统描述，输出是 UML 状态机。作者比较四种生成策略：

1. `Single-Prompt Baseline`
   - 用 `2-shot/3-shot` prompt 一次性让 LLM 直接输出完整 `Umple` 状态机。
2. `Structure-Driven SMF`
   - 按状态机组成元素线性拆步，如先找 states/events，再找 parallel regions，再找 transitions、guards、actions 等。
3. `Event-Driven SMF`
   - 先找状态骨架和事件，再逐个事件追问其在各状态中的处理方式，最后合并为统一状态机。
4. `Hybrid Approach`
   - 先用 `Single-Prompt` 生成完整 `Umple` 草稿，再把该草稿附加进 `Structure-Driven SMF` 的后续 prompts 中，作为“同事给出的 baseline 草稿”来细化。

### 关键技术

#### 1. 单提示直接生成

单提示基线强调让 LLM 一次性恢复完整上下文，包括：

- states
- transitions
- guards
- actions
- hierarchical states
- parallel regions
- history states

这个策略最大优势是全局上下文完整，尤其适合本身就具备较强一步推理与代码生成能力的模型。

#### 2. 结构驱动多步生成

`Structure-Driven SMF` 把复杂任务拆成“按状态机元素分层恢复”的过程。这样做的目标是降低每一步的认知负载，让 LLM 先把结构骨架补齐，再逐步补条件和动作，从而改善 recall。

#### 3. 事件驱动多步生成

`Event-Driven SMF` 假设状态机天然围绕事件展开，因此先识别事件，再逐个事件追问：

- 哪些状态会响应该事件
- 会触发哪些迁移
- 是否附带守卫或动作

它的优点是有机会覆盖更多 event-specific behaviors，但缺点也明显：容易在多轮合并时引入重复、冲突和过生成。

#### 4. Hybrid 组合策略

作者认为纯多步流程可能在分解过程中丢失全局上下文，所以 `Hybrid` 先保留单提示草稿的整体性，再借助结构驱动步骤查漏补缺。这个思路与“先出 skeleton，再定向修补”的路线非常接近。

### 模型与提示设置

- **非推理型 LLM**：`GPT-4o`
- **推理型 LLM**：`Claude 3.5 Sonnet`
- **温度设置**：
  - 大多数步骤使用 `0.01`
  - 在状态/事件发现这类更依赖发散性的步骤使用 `0.5`
- **few-shot 设置**：
  - 多步框架使用 `2-shot`
  - 单提示基线使用 `3-shot`
- **输出格式**：
  - 单提示：`Umple`
  - 多步框架：`HTML tables` + 严格后处理

## 实验与评估

### 数据集

- **数据/案例**：`8` 个 reactive-system scenarios
- **来源类型**：本科建模课程项目/作业题 + 专家参考解
- **制作方法**：每个问题都包含非结构化英文系统描述和专家绘制的参考 UML 状态机
- **代表案例**：`Dishwasher`、`Chess Clock`、`Printer`、`Spa Manager`、`Bread Maker`、`Thermomix TM6`、`W-UMPLE`、`SSC7`

### 评估指标

作者对七类状态机成分分别手工比对：

1. `states`
2. `transitions`
3. `guards`
4. `actions`
5. `hierarchical states`
6. `parallel regions`
7. `history states`

整体和分项都计算 `precision / recall / F1`。

### 实验设置

- **比较维度**：
  1. 单提示下推理型 vs 非推理型 LLM
  2. 多步框架对 `GPT-4o` 的提升
  3. 多步框架对 `Claude 3.5 Sonnet` 的可迁移性
- **后处理**：对多步框架输出的 `HTML tables` 做严格规则式后处理
- **评估方式**：人工与 ground-truth UML state machines 对照评审

### 主要实验结果

#### 1. 单提示基线已经很强，但还不够自动化

- `Claude 3.5 Sonnet` 单提示整体 `F1 = 0.7029`
- `GPT-4o` 单提示整体 `F1 = 0.5431`
- 两个模型在 `states` 上都较强：
  - Claude `0.8991`
  - GPT-4o `0.8038`
- `transitions` 中等：
  - Claude `0.7502`
  - GPT-4o `0.5741`
- `guards` 明显下降：
  - Claude `0.5645`
  - GPT-4o `0.2348`
- `actions` 最难：
  - Claude `0.1633`
  - GPT-4o `0.0000`

#### 2. 多步框架对 GPT-4o 有帮助

对非推理型 `GPT-4o`：

- `Single-Prompt`：整体 `F1 = 0.5431`
- `Structure-Driven SMF`：整体 `F1 = 0.6260`
- `Event-Driven SMF`：整体 `F1 = 0.3735`
- `Hybrid`：整体 `F1 = 0.6559`

其中 `Hybrid` 最好，尤其改善了：

- `transitions`：`0.7107`
- `guards`：`0.4240`
- `actions`：`0.3436`
- `hierarchical states`：`0.7928`

作者将其归因于：`Hybrid` 和 `Structure-Driven` 明显提高了 recall，而没有像 `Event-Driven` 那样付出过大的 precision 损失。

#### 3. 多步框架对 Claude 3.5 Sonnet 不成立

对推理型 `Claude 3.5 Sonnet`：

- `Single-Prompt`：整体 `F1 = 0.7029`
- `Structure-Driven SMF`：整体 `F1 = 0.5026`
- `Event-Driven SMF`：整体 `F1 = 0.3052`
- `Hybrid`：整体 `F1 = 0.6336`

也就是说，推理型模型最好的结果反而来自“精心设计的一次性完整 prompt”，而不是多轮分解流程。作者认为这些多步流程可能干扰了推理型模型自身已有的内部 step-by-step reasoning。

### 方法优势

1. 任务定义直接命中“非结构化需求 -> 状态机”。
2. 不只给整体准确率，而是细到状态机槽位级别的 `F1`。
3. 对比了推理型与非推理型 LLM，结论比“一个框架打天下”更可信。
4. `Hybrid` 提供了一个很有启发性的折中思路：先保住全局草稿，再局部修补。

### 方法的局限性

1. 数据集只有 `8` 个案例，且来自本科课程，外部效度有限。
2. 评估依赖人工判分，存在主观性。
3. 单提示与多步框架输出语法不同：一个是 `Umple`，一个是 `HTML tables`，比较并非完全同构。
4. `actions / parallel regions / history states` 仍然偏弱，离真实工业建模还有差距。
5. 尚未接入模型检查、仿真、形式验证或控制系统特有约束闭环。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟢
- **评估理由**：输入是非结构化自然语言系统描述，输出是 UML 状态机，且论文明确比较了不同生成框架对状态机核心槽位的恢复能力。这与 `project_1` 的“自然语言自动生成状态机模型”任务直接同构。
- **与本研究的主要差异**：
  1. 论文面向一般 reactive-system 建模，而不是控制系统专用状态机。
  2. 论文没有显式建模时间约束、安全约束、层次并发语义的工业强语义变体。
  3. 论文重点在 prompting framework，而不是生成后验证/修复闭环。

### 可借鉴之处

1. 把状态机任务拆成 `states / transitions / guards / actions` 分槽位评测，这对 `project_1` 的评测设计很有用。
2. `Hybrid` 路线很适合作为“先生成完整草稿，再按结构化子任务修补”的 baseline。
3. 对推理型与非推理型模型采取不同工作流，而不是强行统一 pipeline，这一点很重要。

### 存在的不足与改进空间

1. 缺少控制系统语义槽位，如时间、故障、安全、互锁、模式切换。
2. 没有把生成结果继续接到形式化验证或反例驱动修复。
3. 数据规模偏小，且案例复杂度仍有限。
4. 评估仍然是“与专家参考解对齐”，还没有进入可执行语义层面的行为验证。

### 对本研究的启发

这篇论文最直接的启发是：真正的 direct baseline 已经出现，而且它证明了“自由文本 -> 状态机”在今天并非空想，但 guard、action 和复杂层次结构仍然是主要瓶颈。因此，`project_1` 如果要做出实质性超越，不能只停在“也能生成状态机”，而应重点回答以下问题：

1. 如何让控制系统语义槽位比这篇论文恢复得更完整。
2. 如何把生成过程与验证/修复闭环接起来。
3. 如何在状态机骨架、事件结构、守卫/动作细化之间设计更稳的协同流程。

## 重要的相关工作

### 1. 重要的前身类工作

- `Completion of SysML state machines from Given-When-Then requirements`：代表“结构化需求 -> 状态机补全”的前身路线，说明状态机自动化长期存在，但往往依赖规整输入。
- 早期 `software process / behavioral model inference` 工作：更多从日志、轨迹或结构化数据中恢复状态机，而不是直接从自由文本建模。

### 2. 直接参与论证的 baseline/邻近工作

- `Automated domain modeling with large language models`
- `On the assessment of generative AI in modeling tasks: an experience report with ChatGPT and UML`
- `On the use of GPT-4 for creating goal models`
- `Automated derivation of UML sequence diagrams from user stories`

这些工作共同构成了作者对“LLM 已能做多种建模任务，但状态机仍缺直接研究”的论证背景。

### 3. 提供了重要论证的工作

- `Multi-step Iterative Automated Domain Modeling with Large Language Models`
  - 说明把复杂建模任务拆成多轮 LLM 交互是合理方向。
- `Chain-of-Thought prompting`、`Tree-of-Thought`
  - 为多步 prompting 的理论依据提供支撑。

### 4. 在技术上提供了支持的工作

- `Umple`
  - 为单提示基线提供可执行、结构化的状态机代码输出载体。
- `ProtocolGPT`
  - 说明 LLM 已被用于从协议实现中恢复状态机，但它的输入是源码，不是自然语言需求。

### 5. 其他重要工作

- `On the use of large language models in model-driven engineering`
  - 提供 broader MDE 视角下的定位。
- `Using LLMs for use case modelling of IoT systems`
  - 说明 use-case 建模已有探索，但仍与“直接生成状态机”存在任务差异。

## 文献分类总结

- **类别**：直接生成
- **BASELINE评估**：🟢
- **输入**：非结构化自然语言系统描述
- **输出**：UML 状态机
- **输出模型类型**：UML state machine
- **使用的LLM**：GPT-4o、Claude 3.5 Sonnet
- **主要方法**：比较 `Single-Prompt`、`Structure-Driven SMF`、`Event-Driven SMF`、`Hybrid` 四种生成框架，并按状态机槽位计算 `precision / recall / F1`

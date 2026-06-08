# 面向形式化验证的ChatGPT模型转换：从UML状态图到Rebeca模型 / Harnessing ChatGPT for Model Transformation in Software Architecture: From UML State Diagrams to Rebeca Models for Formal Verification

## 基本信息

- **标题**：Harnessing ChatGPT for Model Transformation in Software Architecture: From UML State Diagrams to Rebeca Models for Formal Verification
- **中文标题**：面向形式化验证的软件架构模型转换：利用ChatGPT从UML状态图生成Rebeca模型
- **作者**：Zahra Moezkarimi, Kevin Eriksson, Albin Alm Johansson, Alessio Bucaioni, Marjan Sirjani
- **单位**：Mälardalen University, School of Innovation, Design and Engineering, Västerås, Sweden
- **发表**：2025 IEEE 22nd International Conference on Software Architecture Companion (ICSA-C), Odense, Denmark, 2025年3月31日-4月4日
- **DOI**：10.1109/ICSA-C65153.2025.00061
- **链接**：https://doi.org/10.1109/ICSA-C65153.2025.00061；作者机构PDF：https://www.ipr.mdu.se/pdf_publications/7130.pdf

**代码/仓库获取方式**：
- 论文脚注和正文给出公开 replication package：https://github.com/gnowin/UML-To-Rebecca-Dataset
- 本次核验中，该 GitHub 仓库的 `HEAD` 可访问。
- 仓库记录了实验使用的提示、ChatGPT-4 输出、数据样例和转换结果；原文未声称提供独立可复用的完整自动化工具链。

**数据集获取方式**：
- 数据集随 replication package 公开：https://github.com/gnowin/UML-To-Rebecca-Dataset
- 数据集包含 7 个 Rebeca 示例及其对应的 UML 状态图转换，示例来自 Rebeca 官网、手册、论文和既有 Rebeca 示例。
- 论文说明 UML 状态图是作者从已有 Rebeca 模型人工反向构造得到，并加入 metadata 以补充 UML 状态图本身无法表达的 Rebeca 信息。

## 简报

**解决的问题**：论文探索能否用 ChatGPT-4 将已有 UML 状态图转换为 Rebeca 形式模型，从而把 UML 中较弱的形式语义桥接到 Rebeca / Afra 支持的形式化验证环境。它的输入不是自然语言需求，而是 PlantUML 文本化的 UML state diagrams 及必要 metadata；输出是 Rebeca actor-based formal model / code，用于 Afra 编译、模型检查和与人工 ground truth 对比。

- **输入**：PlantUML 格式 UML state diagrams；few-shot 示例中的 UML 状态图与对应 Rebeca 代码；为弥补 UML 状态图信息不足而加入的 metadata，例如 message calls、timing primitives、constructor 初始化消息和部分 conditional statements。
- **方法**：先从已有 Rebeca 模型人工构建 UML 状态图数据集，再设计 UML 状态图到 Rebeca 概念映射，最后用 ChatGPT-4 few-shot prompting 执行模型转换，并用 Afra 编译 / model checking 与 ground truth 对照分析结果。
- **输出**：Rebeca 模型 / Rebeca code，包含 reactive classes、knownrebecs、statevars、message servers、main section 等可进入 Afra 的形式化验证工件。

```text
输入层：PlantUML UML state diagrams + metadata + few-shot translation examples
  -> 方法层：ChatGPT-4 few-shot model transformation + Afra compile/model-check feedback + ground truth comparison
  -> 输出层：Rebeca actor-based formal model/code for formal verification
```

**研究动机**：UML 是事实上的通用建模语言，但 UML diagrams 缺少足够强的形式语义，难以直接做形式化验证。Rebeca 面向并发反应式系统并支持模型检查，但从 UML 到 Rebeca 的传统转换通常需要多个 UML 图和 Rebeca 专业知识，工业应用门槛高。论文希望用 LLM 降低从架构模型到可验证形式模型的转换成本。

**方法创新**：论文不是从自然语言生成状态机，而是把 LLM 用作软件架构模型转换器；它提出一个三阶段流程：dataset preparation、LLM transformation、evaluation。核心经验是 UML state diagrams alone 不足以生成准确 Rebeca 模型，必须加入 metadata 才能让 ChatGPT-4 推断关键架构细节。

**实验设计**：作者构造 7 个 Core / Timed Rebeca 示例的数据集，并用 ChatGPT-4 做 few-shot 转换。实验设置包括 2 个训练示例生成 LCR Leader Election，以及 5 个训练示例后同时生成 Sender Receiver 和 Ticket Service。生成结果先在 Afra 中检查编译，能编译后执行 model checking，再与原始 Rebeca ground truth 做整体概念对比、逐行对比和加权分析。

**结论与不足**：ChatGPT-4 能生成结构接近的 Rebeca 模型，但生成结果不能直接一次性在 Afra 中编译通过，需要人工修正语法错误、缺失 main section 细节、queue size、非确定性表达和不属于 Rebeca 的概念。Sender Receiver 示例有 39/48 行正确，普通正确率 85%，加权成功率 69%；Ticket Service 普通正确率 77%，加权成功率 67%。论文结论是 few-shot ChatGPT-4 对 UML 状态图到 Rebeca 转换有潜力，但远未达到全自动可靠转换。

## 研究问题与动机

### 问题背景

软件架构设计需要建模、分析和验证系统设计。UML 能提供通用可视化表达，但 UML 的形式语义不足使其难以直接支撑模型检查。Rebeca 是面向并发反应式系统的 actor-based modeling language，具备 formal verification 支持，并可通过 Afra 进行模型开发、属性指定、模型检查和反例可视化。

已有 UML 到 Rebeca 的工作通常依赖 UML profile、ReUML 或多类 UML 图组合，要求建模者理解 Rebeca 的 reactive objects、message servers、asynchronous messages、queue size、main section 等概念。论文的动机是评估 ChatGPT-4 是否能减少这种专业知识负担，让架构师从已有 UML state diagram 更低成本地得到可验证的 Rebeca 模型。

### 核心问题

论文围绕三个核心问题展开：

1. 只用 UML state diagrams 是否足以推断 Rebeca 模型。
2. ChatGPT-4 在 few-shot 示例引导下能否生成可编译、可模型检查的 Rebeca code。
3. 哪些 Rebeca 概念无法从 UML state diagram 中可靠恢复，需要额外 metadata 或人工反馈。

### 研究动机

这篇论文的关键动机不是“自然语言需求到状态机”，而是“已有 UML 状态机工件到形式化验证模型”的低代码转换。它把 LLM 放在 MDE / model transformation 任务中，用于缓解 UML 的弱形式语义与 Rebeca 的高专业门槛之间的落差。

### 现有方法的局限性

原文指出，UML 缺少形式语义；已有 UML-to-Rebeca 方法通常需要多个 UML diagrams 或修改后的 UML profile；UML state diagrams 本身无法表达 main function、environment variables、message server 中的 state variables、timing primitives、constructor 初始行为、发送给其他 rebecs 的 message calls 等信息。因此，单靠状态图很难稳定恢复完整 Rebeca 模型。

## 核心方法

### 方法概述

论文采用三阶段研究流程：

1. **Dataset Preparation**：从已有 Rebeca examples 出发，先在 Afra 中核验 / 修正示例，再人工翻译成 UML state diagrams，形成 UML 状态图与 Rebeca ground truth 的配对数据集。
2. **Transformation with LLMs**：用 ChatGPT-4 做 zero-shot / few-shot 探索，重点采用 few-shot prompt，把若干 UML state diagram 与对应 Rebeca code 作为示例，再要求模型为新的 PlantUML 输入生成 Rebeca code。
3. **Evaluation**：用 Afra 对生成模型做 compilation check 和 model checking，再与 ground truth 做概念级、逐行级和加权分数对比。

### 输入与中间表示

输入的 UML state diagrams 使用 PlantUML 文本语法表示，因为 ChatGPT-4 的输入需要文本化。普通 UML 状态图组件被限制为 states、initial states、transitions、transition triggers 和 transition effects，以降低转换复杂度。

论文发现 UML state diagrams alone 不足，因此引入 metadata。metadata 写在 transition effects 中，采用接近 Rebeca code 的语法，主要包含：

1. 不直接对应 state variables 的条件语句。
2. 发送给 known rebecs 的 message calls。
3. constructor 中发出的初始化消息。
4. delay 和 after 等 timing primitives；deadline 在当前转换中未考虑。

### UML状态图到Rebeca的概念映射

论文定义了面向该数据集的 UML state diagram 到 Rebeca mapping：

- 每个 reactive class 对应一个 UML state diagram。
- UML states 对应影响状态的 statevars 取值组合。
- message servers 对应 transition triggers。
- transition effects 对应 message server body 中执行的内容，并可承载 metadata。
- initial pseudostate 到初始状态的 transition 可表示 constructor 中发送的 messages。
- final state 对应 Rebeca 中可能形成 deadlock 的终止，不适合作为需要 formal verification 的模型终点。
- self transition 对应 msgsrv 到达但 statevars 未改变的情形。

### LLM/agent设置

论文使用 ChatGPT-4 / GPT-4，并说明二者在文中互换使用。实验通过 ChatGPT 界面交互，关闭了“improve the model for everyone”选项，以避免模型从当前实验历史中继续学习。论文未使用多智能体、工具调用 agent 或自动规划 agent。

Prompt 的基本结构是 few-shot translation：

1. 开头指令要求将 PlantUML diagram 翻译为 Rebeca code。
2. 提供多个 `Input: {PlantUML diagram}` 与 `Output: {Corresponding Rebeca code}` 示例。
3. 最后给出新的 PlantUML 输入，并留空输出，要求 ChatGPT-4 按示例模式生成对应 Rebeca model。

### 是否使用few-shot、CoT、RAG、反馈或修复闭环

- **few-shot**：使用，是核心实验策略。
- **zero-shot**：论文摘要和方法中提到探索过 zero-shot，但主要报告 few-shot 结果。
- **CoT**：原文未明确说明使用 chain-of-thought。
- **RAG**：正文未实现 RAG，只在 future work 中提出可结合 RAG 技术改进转换。
- **自动反馈循环**：未实现完全自动反馈闭环；Afra 的编译与模型检查用于分析和人工修正。
- **修复闭环**：有人工修正步骤。生成模型无法编译时，作者与原始 Rebeca 模型对比并修复错误，再执行 model checking。

### 输出格式

输出是 Rebeca 模型 / Rebeca code，可包含 Core Rebeca 和 Timed Rebeca 构造。模型应包含 reactiveclass、knownrebecs、statevars、constructor、msgsrv、main 等 Rebeca 结构，并在通过编译后进入 Afra 做 model checking。

## 实验与评估

### 数据集

论文数据集包含 7 个 Rebeca 示例及对应 UML state diagram：

1. Dining Philosophers，Core Rebeca，来自 Rebeca Homepage。
2. Producer Consumer，Core Rebeca，来自 Rebeca Homepage。
3. LCR Leader Election，Core Rebeca，来自 Rebeca Homepage。
4. Sender Receiver，Core Rebeca，来自 Rebeca Homepage。
5. Ticket Service，Timed Rebeca，来自 Rebeca Handbook。
6. Train Door Controller，Timed Rebeca，来自论文。
7. Train-Bridge Controller，Core Rebeca，来自 Rebeca Homepage。

作者先选择已有 Rebeca examples，使用 Afra 核验；部分旧版本示例存在小语法错误、deadlock 或 queue overflow，作者在进入转换流程前做了修正。由于不存在现成 UML state diagram / Rebeca 配对数据集，UML 状态图由作者从 Rebeca 模型人工生成。

### 评估指标

论文使用以下评估方式：

1. **Compilation check**：生成的 Rebeca code 是否能在 Afra 中编译。
2. **Model verification**：编译成功后用 Afra model checking 验证。
3. **Comparison with ground truth**：与数据集中原始 Rebeca model 做概念级和逐行级对比。
4. **Line-by-line quantitative analysis**：统计 Correct、Incorrect、Added、Improved、Not In Place、Not Exist 等差异类别。
5. **Weighted success rate**：给不同差异类型赋权，例如 Correct +1、Incorrect -1、Improved +1、Not In Place -1.5、Not Exist -2。

### 实验设置

论文报告两个主要设置：

1. 使用 Dining Philosophers 和 Train Bridge Controller 作为 few-shot prompt 中的训练示例，要求 ChatGPT-4 为 LCR Leader Election 的 UML state diagram 生成 Rebeca model。
2. 将训练示例扩展为 Train Door Controller、Dining Philosophers、LCR Leader Election、Train Bridge Controller 和 Consumer Producer，并要求 ChatGPT-4 在同一 prompt 中生成 Sender Receiver 和 Ticket Service 的 Rebeca models。

### 主要实验结果

第一个设置中，LCR Leader Election 的生成代码不完全可用，需要修复 3 行代码，且 main section 中 rebecs 的实例化不符合 Rebeca 语法。

第二个设置中，Sender Receiver 和 Ticket Service 的生成 Rebeca models 都不能直接在 Afra 中编译。Ticket Service 只有少量语法错误；Sender Receiver 包含 ChatGPT-4 错误引入的非 Rebeca 概念。两者在修正后可以继续运行和验证。

常见发现包括：

1. ChatGPT-4 通常能生成正确数量和相近命名的 message servers。
2. ChatGPT-4 能初始化正确数量和名称的 rebecs。
3. ChatGPT-4 会添加不必要的 environment variables。
4. queue size 不在 UML state diagrams 中给出，因此 ChatGPT-4 会猜测该属性。
5. ChatGPT-4 对 Rebeca 非确定性值处理较差。
6. main section 中的代码和概念未在 UML state diagrams 中表示，因此该部分错误符合预期。

逐行定量结果为：

| 示例 | LoC | Correct | 普通正确率 | 加权成功率 |
|---|---:|---:|---:|---:|
| Sender Receiver | 48 | 39 | 85% | 69% |
| Ticket Service | 31 | 24 | 77% | 67% |

### 方法优势

1. 任务对象是状态机相关工件到形式化验证模型的转换，和模型驱动工程中的验证桥接问题高度相关。
2. 论文把 prompt、生成输出和数据集放入公开 replication package，有利于复现和后续比较。
3. 论文明确揭示了 UML state diagrams 的信息缺口，并用 metadata 作为可操作的补充机制。
4. Afra 编译和 model checking 使输出不是纯文本生成物，而是能进入形式化工具链的 Rebeca artifact。

### 方法的局限性

1. 生成过程尚非全自动；模型输出需要人工修正后才能编译和验证。
2. 数据集仅 7 个示例，且由 Rebeca 反向构造 UML 状态图，存在规模和方向性偏差。
3. 输入不是自然语言需求，而是已有 UML 状态图加 metadata；因此不能直接衡量自然语言到状态机建模能力。
4. 同时包含 Core Rebeca 和 Timed Rebeca 可能使 ChatGPT-4 难以区分两类语义。
5. ChatGPT-4 非确定性输出影响可复现性。
6. 原文未提供完整自动修复闭环，也未报告 RAG / fine-tuning 的实际结果。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：🟡**

这篇论文应评为 `🟡 相关但非直接 baseline`，倾向“近邻 formal transformation”。理由如下：

1. 它确实围绕状态机族工件：输入是 UML state diagrams / PlantUML，输出是 Rebeca formal model，用于形式化验证。
2. 它使用 GPT-4 / ChatGPT-4 执行模型转换，属于 LLM4Modeling / LLM-assisted model transformation。
3. 但它不是 `project_1` 的 exact STM direct baseline，因为输入不是自然语言软件需求，而是已有 UML 状态图及 metadata；输出也不是给用户查看的 UML / SysML 状态机本身，而是 Rebeca actor-based formal verification model。
4. 它比泛 UML / class diagram / sequence diagram 工作更接近 `project_1`，因为状态机工件是核心输入，且输出可用于 formal verification。

**四条件建议**：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 使用 ChatGPT-4 / GPT-4 进行模型转换。 |
| NL输入 | 🟠 | 输入主要是 PlantUML UML state diagrams + metadata，不是自然语言需求；自然语言只出现在提示指令中。 |
| LLM方法 | 🟢 | few-shot prompting 是核心方法变量。 |
| STM族输出 | 🟢 | 输入为 UML 状态图，输出为状态相关的 Rebeca formal model / code，可服务于状态行为验证。 |

### 可借鉴之处

1. **metadata 设计**：论文清楚说明哪些语义无法从 UML 状态图直接恢复，可为 `project_1` 设计“需求补充槽位 / 模型元素约束槽位”提供线索。
2. **验证反馈**：Afra 编译和 model checking 说明 LLM 生成模型应进入结构化验证工具，而不是仅靠人工阅读判断正确性。
3. **ground truth 构造**：从形式模型反向构造状态图虽然有偏差，但能形成可控的配对 benchmark，可借鉴为小规模方法调试集。
4. **错误分类**：main section、queue size、non-determinism、environment variables 等错误说明 LLM 容易在未显式输入的语义上猜测。

### 存在的不足与改进空间

1. `project_1` 的核心任务是从非形式化控制系统需求生成结构化状态机模型；本文从已有 UML 状态图出发，任务入口不同。
2. 论文的 metadata 由研究者设计并人工加入，还没有证明普通架构师能稳定提供这些信息。
3. 输出是 Rebeca code，不是本研究首要目标中的层次化、带 guard/action/time constraint 的状态机 DSL；需要额外映射才能进入 `project_1` 的比较表。
4. Afra 反馈没有形成自动化 counterexample-guided repair loop，仍偏实验分析和人工修正。

### 对本研究的启发

对 `project_1` 而言，这篇论文的价值主要在于“生成后验证桥接”和“状态机语义缺口显式化”。它提示后续方法不能假设 LLM 能凭自然语言或状态图自动补全所有执行语义；应把 initialization、message/event queue、guard 条件、跨对象通信、时间原语和 verification property 等信息作为可审计字段显式建模。

### 研究定位与差异化

该论文不应被写成 `NL -> STM` direct baseline，也不应被误归为 BPMN、activity diagram、Rebeca 背景或泛 UML 工作。更准确的定位是：

```text
已有 UML state diagrams / PlantUML + metadata
  -> ChatGPT-4 few-shot model transformation
  -> Rebeca actor-based formal model/code for Afra verification
```

因此，它是 `project_1` 的 near baseline / related formal transformation work，而不是 exact direct baseline。

## 重要的相关工作

### 1. 重要的前身类工作

**Sirjani and Alavizadeh / Alavizadeh 等关于 UML 到 Rebeca 的工作**
原文在引言和相关工作中说明，已有工作使用 UML profile 表示 reactive objects 和 asynchronous communication，并系统生成 Rebeca code；2007 年进一步形成 ReUML tool，用于大系统和子系统通信建模。这些工作是本文“UML -> Rebeca”研究链条的直接前身，但依赖多个 UML diagrams 和较强 Rebeca 专业知识。本文的差异是聚焦 UML state diagrams，并尝试用 ChatGPT-4 降低转换门槛。

**Djukanovic, 2019, Mapping UML Diagrams to the Reactive Object Language (Rebeca)**
原文说明 Djukanovic 提供了 UML 到 Rebeca 的 conceptual mapping，覆盖多数 Rebeca 元素，但未实现自动转换工具，且重点在 sequence、class、object diagrams。本文借鉴其 mapping 思路，但把任务限定为 UML state diagrams，并构建自己的状态图到 Rebeca 映射规则。

### 2. 直接参与实验的baseline

原文没有设置外部方法 baseline，也没有与传统 UML-to-Rebeca 工具做量化对比。实验中的“对比对象”主要是人工 ground truth Rebeca models：ChatGPT-4 生成结果与数据集中原始 Rebeca code 对照，评估编译、模型检查和逐行差异。

### 3. 提供了重要论证的工作

**OMG UML 2.5.1 标准**
原文引用 UML 标准来说明 UML 是广泛使用的通用建模语言，并区分 structural diagrams 与 behavioral diagrams。本文选择 UML state diagrams 作为输入对象，正是因为状态图能表达对象 / 系统在不同时间点的状态与状态迁移。

**André 等, 2023, Formalizing UML State Machines for Automated Verification - A Survey**
原文相关工作引用该 survey 说明，已有 UML state machine formalization 方法尝试将状态图转换为有形式语义的语言或模型检查器输入，但没有一种方法覆盖所有 UML state diagram feature set；部分方法支持 timing，部分有 tool support，许多面向旧 UML 版本。这为本文探索新的 LLM-assisted transformation 提供了问题背景。

**Bucaioni 等, 2024, ChatGPT 编程能力相关研究**
原文相关工作提到 Bucaioni 等使用 240 个 Java / C++ LeetCode 编程问题研究 ChatGPT 是否能替代人类程序员，结论是 ChatGPT 在简单和中等题上表现较好，但难题上仍不足。本文将其作为 ChatGPT 代码生成能力和局限性的背景证据，但原文参考文献列表中该条题名 / venue 信息提取不完整。

### 4. 在技术上提供了支持的工作

**Rebeca 语言与工具链相关文献**
原文引用 Sirjani 的 Rebeca 理论、应用与工具论文，以及 Core Rebeca、Timed Rebeca、Hybrid Rebeca、PTRebeca 和 Rebeca User Manual 等资料，作为建模语言与验证工具链基础。本文实验依赖 Rebeca actor-based semantics、message servers、knownrebecs、statevars、timing primitives 和 Afra model-checking tool。

**Prompt engineering 与 few-shot learning 文献**
原文引用 prompt engineering 和 few-shot learning 相关文献，用来支撑为什么用少量示例引导 GPT-4 执行特定模型转换任务。本文的 prompt 由指令、多个 UML/Rebeca 示例对和待转换 PlantUML 输入组成。

### 5. 其他重要工作

**UML 与形式化方法集成 / UML 到 Event-B 转换**
原文相关工作提到 UML 与形式化方法集成、UML 到 Event-B 转换等研究，用于说明 UML formalization 是长期问题，且许多方法关注 class diagrams、sequence diagrams 或其他 UML 视图，而不是本文聚焦的 state diagrams 到 Rebeca。

**Noy and Zhang, 2023, generative AI productivity evidence**
原文引用该研究作为生成式 AI 可能提高生产力的背景论证。它不直接参与本文方法或实验，只提供 LLM 进入软件工程工作流的外部动机。

## 文献分类总结

这篇论文处于“UML 状态机工件 -> 形式化验证模型”的研究链条上。其前身包括传统 UML-to-Rebeca、ReUML、UML state machine formalization survey 和 Rebeca 工具链；其新增贡献是把 ChatGPT-4 few-shot prompting 放入模型转换流程，并用公开 replication package 记录数据、提示和输出。

在 `project_1` baseline 体系中，它最适合归为 `🟡 近邻 formal transformation`：有状态机工件、有 LLM 建模方法、有形式化验证落点，但输入不是自然语言需求，输出也不是直接用于人类建模编辑的 UML/SysML STM，而是 Rebeca formal model。因此它适合作为“生成后形式化转换 / 验证桥接”的对照和启发，不适合作为 `NL -> STM` direct baseline。

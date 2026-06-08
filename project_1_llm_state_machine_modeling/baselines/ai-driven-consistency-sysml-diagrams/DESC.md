# SysML 图的一致性 AI 驱动方法 / AI-Driven Consistency of SysML Diagrams

## 基本信息

- **标题**：AI-Driven Consistency of SysML Diagrams
- **中文标题**：SysML 图的一致性 AI 驱动方法
- **作者**：Bastien Sultan, Ludovic Apvrille
- **单位**：LTCI, Télécom Paris, Institut Polytechnique de Paris
- **发表**：MODELS 2024, ACM/IEEE 27th International Conference on Model Driven Engineering Languages and Systems, 2024-09-22 至 2024-09-27, Linz, Austria, pages 149--159
- **DOI**：10.1145/3640310.3674079
- **链接**：
  - DOI：https://doi.org/10.1145/3640310.3674079
  - 作者 PDF：https://perso.telecom-paristech.fr/apvrille/docs/models2024_sultan.pdf
  - TTool-AI 页面：https://ttool.telecom-paris.fr/ttoolai.html
  - Zenodo 工件：https://zenodo.org/records/12794339

**代码/仓库获取方式**：
- 论文将实现描述为 TTool-AI 的扩展；TTool-AI 是 TTool 中的 AI 建模助手，TTool-AI 页面说明其可通过 OpenAI、MistralAI 或兼容 OpenAI JSON 接口的自托管模型使用。
- 论文脚注给出了若干 TTool 源码路径，包括 `AIUseCaseDiagram.java`、`AIBlockConnAttribWithSlicing.java`、`AIDiagramCoherency.java` 和 `AIDiagramCoherencyWithFormalRules.java`。这些路径位于 TTool 公共 GitLab：https://gitlab.telecom-paris.fr/mbe-tools/TTool/
- Zenodo 工件记录为开放软件工件，标题为 `linuxisnotunix/ttool-ai: Final artifacts release for Models'24 paper AI-Driven Consistency of SysML Diagrams.`，版本为 `6`，关联 GitHub 入口为 https://github.com/linuxisnotunix/ttool-ai/tree/6。

**数据集获取方式**：
- 论文第 5 节说明实验输入数据、生成模型和复现实验指南已公开在 Zenodo 工件中；论文脚注给出的概念 DOI 为 https://doi.org/10.5281/zenodo.11936921，当前记录入口为 https://zenodo.org/records/12794339。
- 工件包含三个系统案例的规格与 TTool 模型文件：automotive braking system、space-based system、dynamic positioning system。原文没有把它定义为通用 benchmark，而是作为论文三案例复现实验工件。

## 简报

**解决的问题**：论文关注由 LLM 生成或人工维护的 SysML 多视图模型中，一致性如何被自动检测与修复。它的核心输入是自然语言系统规格以及由 TTool-AI 生成或已有的 SysML 用例图和块图；方法是把形式化一致性规则、TTool 语法检查、OpenAI GPT 和必要的人类工程师反馈组合成迭代闭环；输出是经过一致性检测与部分修复后的 SysML 用例图、块图和不一致列表。

- **输入**：自然语言系统规格；SysML use case diagrams；SysML block diagrams；由 TTool 导出的紧凑文本图表示；可注入的内部一致性与跨图一致性规则。
- **方法**：TTool-AI 扩展；UCD/BD 并行生成；规则检查与 TTool syntax checker；LLM 生成 JSON 格式的不一致列表；用户选择相关不一致后触发重新生成和修复。
- **输出**：TTool GUI 中的 SysML 用例图和块图；JSON 不一致列表；修正后的 UCD/BD；论文没有把状态机图作为本次实验输出主体。

```text
输入层：自然语言系统规格 + UCD/BD 文本表示 + 一致性规则
  -> 方法层：TTool-AI + OpenAI GPT + 语法/规则检查 + 人类选择反馈
  -> 输出层：一致性问题列表 + 修正后的 SysML 用例图/块图
```

**研究动机**：UML/SysML 设计通常包含多个视图，用例图描述系统分析层面的 actor/use case，块图描述设计层面的结构，状态机图描述算法行为。多视图一致性本来就难维护；LLM 生成模型时还会因为上下文长度、分步生成和随机性引入新的内部或跨图不一致。因此，仅依赖人工检查或传统规则难以覆盖 LLM 建模链条中的语义不一致。

**方法创新**：论文在 TTool-AI 基础上加入三类机制：第一，给 SysML 用例图和块图定义形式化对象与面向 LLM 常见错误的一致性规则；第二，把规则注入提示、静态检查和 by-construction 图生成中，约束 UCD/BD 内部一致性；第三，用 LLM 对 UCD 与 BD 的跨图一致性进行检测，并把检测出的不一致反馈到图重生成流程中。

**实验设计**：论文使用三个案例系统：automotive braking system、space-based system 和 dynamic positioning system。每个系统生成两个 UCD 与两个 BD，并对 UCD/BD 组合执行不一致检测与修复。automotive 和 space-based 系统的图生成使用 GPT-3.5，dynamic positioning system 的图生成使用 GPT-4；不一致检测与修复使用 GPT-4；工具版本为 TTool 3.0 beta build 14731。

**结论与不足**：在三案例评估中，方法共检测到 69 个有效不一致，另有 6 个错误检测；论文报告 92% 的检测结果是相关不一致，平均自动修复 87% 的不一致。局限包括：跨图规则注入会让 LLM 过度关注显式规则而忽视其他一致性问题；环境块类型未导出到文本表示，导致部分判断依赖 LLM 推断；评估仅覆盖三个相对简单案例，且只评估 UCD/BD 两类图之间的一致性。

## 研究问题与动机

### 问题背景

SysML 建模通常同时维护分析视图、结构视图和行为视图。论文在引言中明确提到 UCD、class/block diagrams 和 SMD 分别承担不同建模职责，而这些视图之间的一致性对系统正确性很关键。传统 consistency rule 能处理预先定义的约束，但对语义距离更远的跨视图问题、同义命名问题和 LLM 分步生成带来的内部不一致覆盖不足。

### 核心问题

论文要解决的是：在 TTool-AI 这类 LLM 辅助 SysML 建模环境中，如何自动检测并修正 UCD 与 BD 内部及二者之间的一致性问题。这里的一致性包括：

- UCD 内部是否至少包含 actor 与 use case，actor/use case 是否命名合理，边类型是否合法，actor 是否连接到 use case。
- BD 内部是否至少包含 block，block/attribute/method/signal 命名是否唯一，类型和连接是否合法。
- UCD/BD 跨图是否满足 actor 与 environment block 对应、environment block 不互相连接、environment block 至少连接 system block 等规则。

### 研究动机

TTool-AI 已能从自然语言规格生成 SysML BDs 和 SMDs，但生成结果仍可能需要人工 refinement 才能提高一致性；同时原框架尚不支持所有 SysML 图的 AI 生成。本文扩展 TTool-AI，一方面补入 UCD 生成能力，另一方面把生成后的一致性检测与修复纳入闭环。

### 研究目标

论文目标不是从自然语言直接生成状态机，而是构建一个面向 SysML 多视图的一致性管理框架。它服务于“生成后检测/修复”阶段：LLM 先生成或读取图，再由规则、TTool checker 和 LLM 共同识别并修复不一致。

## 核心方法

### 方法概述

方法基于 TTool-AI 扩展，底层 LLM 为 OpenAI GPT-4-turbo 和 GPT-4o；评估中还使用了 GPT-3.5 和 GPT-4。总体流程分为三组阶段：

- `U1-U5`：从自然语言规格生成 UCD，并在提示、语法/一致性分析和图构造阶段处理 UCD 内部一致性。
- `B1-B5`：从自然语言规格生成 BD，可使用已有分析图作为输入，并在提示、语法/一致性分析和图构造阶段处理 BD 内部一致性。
- `C1-C3`：把 UCD 和 BD 导出为紧凑文本表示，注入跨图一致性规则和 JSON 输出格式约束，要求 LLM 返回不一致列表，再把这些不一致交给用户选择并反馈到重新生成流程。

### 形式化对象与一致性规则

论文为 UCD 定义了四元组形式的 use case diagram，为 BD 定义了包含 block、description、link、communication semantics 与 connection 的六元组形式。其规则列表不是完整 SysML 语义规则库，而是面向 LLM 常见生成错误的定向规则。

- UCD 内部规则包括 `RU1-RU10`，例如至少有一个 actor 和一个 use case、link 涉及的元素必须存在、actor 名称应以名词开头、use case 名称应以动词开头、actor-use case 边应是 association 等。
- BD 内部规则包括 `RB1-RB12`，例如 block 非空、block/attribute/method/signal 名称唯一、attribute/method/signal 参数类型限于 boolean 或 integer、signal 必须是 input 或 output、连接必须涉及已存在 block 和 signal。
- UCD/BD 跨图规则包括 `RC1-RC3`，聚焦 environment blocks：两个 environment blocks 不应互连；每个 environment block 至少连接一个 system block；每个 environment block 应对应 UCD 中的一个 actor。

### LLM/agent 设置

论文没有使用多智能体框架。它使用 TTool-AI 中的单一 LLM 请求/响应闭环：

- UCD 与 BD 生成请求包含自然语言规格、输出语法约束和部分一致性规则。
- LLM 输出结构化 JSON，TTool 再进行 syntax/consistency analysis。
- 若分析失败，TTool 根据错误重新构造请求并回到生成阶段。
- 用户可分析建议图，要求增强、重新生成或接受图。
- 跨图一致性检测请求包含系统规格、UCD/BD 紧凑文本表示、JSON 输出格式约束和可选形式化规则。

原文说明该过程可以在全部不一致解决、达到时间限制或达到最大迭代次数时结束；用户在闭环中决定哪些不一致需要处理，也可以加入额外约束，例如要求至少包含若干 actor 和 use case。

### 反馈/验证机制

论文中的反馈与验证机制主要是半形式化一致性检查，不是完整的模型检查性质验证：

- **规则注入**：部分规则直接进入 prompt，提前约束 LLM 输出。
- **TTool syntax checker**：检查生成图的语法错误。
- **一致性分析**：在 UCD/BD 生成后检查部分内部规则。
- **by-construction enforcement**：在 TTool GUI 图生成阶段强制满足若干规则。
- **LLM inconsistency detection**：把 UCD/BD 文本表示交给 GPT，返回 JSON 不一致列表。
- **人类选择反馈**：用户判断哪些不一致相关，并将其纳入下一轮生成或修复提示。

TTool 本身支持 simulation 和 model checking，论文第 2.3 节把这作为 TTool 背景能力；但本文实验没有把 SMD 性质验证、模型检查反例或仿真轨迹作为核心评价闭环。

### 输出格式与模型类型

本论文的主要输出不是状态机族模型，而是：

- SysML use case diagram；
- SysML block diagram；
- UCD/BD 的紧凑文本导出表示；
- JSON 格式不一致列表；
- 修正后的 UCD/BD。

论文提到 TTool-AI 当前实现支持 UCD、BD 和 SMD，也讨论未来评估 UCD 与 SMD 的跨一致性；但本文的实证评估集中在 UCD 和 BD。

## 实验与评估

### 数据集 / 案例系统

论文使用三个系统案例：

- **Automotive braking system**：来自欧洲项目的自动刹车系统案例。
- **Space-based system**：来自另一个欧洲项目的空间系统案例。
- **Dynamic positioning system**：论文详细展开的船舶动态定位系统案例，规格涉及 anemometer、IMU、GNSS、azimuth thrusters、bow thrusters、console 和 controller。

Zenodo 工件为每个系统提供 `md` 规格文件和 `xml` TTool 模型文件。原文没有声称这些案例构成通用公开 benchmark，也没有给出大规模训练集。

### 评估指标

论文评估三类过程：

- **model generation**：生成两个 BDs 和两个 UCDs per case study。
- **inconsistency detection**：使用 GPT-4 检测 UCD/BD 之间和各图内部残留的不一致。
- **inconsistency correction**：在剔除错误检测项后，把不一致列表反馈给生成过程，更新 UCD/BD。

表 4 区分 internal inconsistencies、external inconsistencies、errors 和 corrected inconsistencies。错误检测不会计入有效不一致总数，也不会进入修复阶段。

### 实验设置

- Automotive braking system 与 space-based system 的图生成使用 GPT-3.5。
- Dynamic positioning system 的图生成使用 GPT-4。
- 不一致检测与修复使用 GPT-4。
- 工具版本为 TTool 3.0 beta, build 14731。
- 每个系统生成两个 UCD 和两个 BD，并评估不同 UCD/BD 配对。

### 主要实验结果

论文报告：

- 方法平均每个 BD 检测到 4 个不一致，每个 UCD 检测到 1.7 个不一致。
- 全部评估中有 6 个不一致被错误识别，占检测结果的 8%；换言之，92% 的检测结果被认为是相关不一致。
- 平均自动修复 87% 的不一致，外部跨图不一致的修复率略高。
- 汇总表中有效不一致总数为 69，修复量为 60.5/69。出现 `0.5` 是因为作者对部分修复给出半分计数。

### 方法优势

- 将传统规则检查和 LLM 语义判断结合起来，能覆盖部分纯规则难以捕获的命名、对应关系和语义一致性问题。
- 在 TTool-AI 的自然语言到 SysML 生成框架上补入 UCD 生成与跨图一致性环节，形成从生成到检测再到修复的闭环。
- Zenodo 工件公开了输入、模型和复现实验指导，使三案例结果可追踪。

### 方法局限性

- 规则注入存在焦点偏置：当跨图规则被加入 consistency request 后，LLM 倾向于只关注这些规则而忽略其他一致性问题。
- BD 文本导出没有包含 system/environment block 类型，导致部分跨图规则判断依赖 LLM 从规格和 UCD 中推断。
- 当前修复策略一次性提供整个不一致列表，作者认为逐条处理不一致可能提高修复率。
- 实验规模小，三个案例图相对简单；复杂模型可能需要分解/重组策略。
- 本文只评估 UCD 与 BD 的跨图一致性，没有评估 UCD/SMD 或 BD/SMD 的一致性。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：🟠。**

这篇论文与 Project 1 有明确邻近关系，但不构成 exact STM direct baseline。理由如下：

- 它使用 LLM 参与 SysML 建模，并且直接继承 TTool-AI 的自然语言到 SysML 图生成基础设施。
- 它的重点是 UCD/BD 的内部与跨图一致性检测、修复和生成后反馈，而不是从自然语言需求直接生成状态机、Statechart 或 SysML state machine。
- 状态机图只作为 TTool-AI 已支持或未来可扩展的图类型被提到；本文实验主体是 use case diagrams 和 block diagrams。
- 因此它更适合作为 Project 1 的“生成后一致性/repair infrastructure”相关工作，而不能列为直接状态机生成 baseline。

### 四条件建议

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟡 | LLM 明确用于 SysML 图生成、检测与修复，但论文主任务是 UCD/BD 一致性管理，不是状态机建模主任务。 |
| NL输入 | 🟢 | 生成 UCD/BD 的入口是自然语言 system specification。 |
| LLM方法 | 🟢 | 使用 OpenAI GPT 系列模型，且方法核心包含 LLM 请求、JSON 输出、错误反馈和重生成。 |
| STM族输出 | 🟠 | 输出主体是 SysML UCD/BD 和不一致列表；SMD 只作为 TTool-AI 支持或未来扩展对象出现。 |

### 可借鉴之处

- 可借鉴“规则 + LLM + 工具 checker + 人类选择”的混合反馈环，用于 Project 1 的状态机生成后校验与修复。
- 可借鉴紧凑文本图表示，减少把图模型送入 LLM 时的 token 成本。
- 可借鉴把错误分为内部一致性、跨图一致性和错误检测三类，便于后续 run record 记录与 eligibility 过滤。
- 可借鉴 Zenodo 工件化方式，为每个案例保留输入规格、生成模型、检测结果和复现实验说明。

### 存在的不足与改进空间

- 没有直接给出 STM 生成质量指标，也没有与状态机参考模型做结构化对比。
- 反馈信号主要是一致性规则和 LLM 描述性不一致列表，不是模型检查 counterexample、trace 或时序性质验证结果。
- 人类仍需判断哪些不一致要纳入修复提示，尚未形成完全自动化 repair policy。
- 对复杂系统、层次状态机、并发状态机、时间约束和控制系统安全性质的支持仍未在本文中验证。

### 对本研究的启发

对 Project 1 来说，本文最有价值的位置是“状态机生成之后如何检测与修复模型不一致”。它提示我们：如果状态机生成方法输出多个视图或多阶段制品，应把生成结果转成稳定、紧凑、可审计的文本表示，再用规则检查、语义判断和修复循环维护一致性。但在 baseline 总账中，必须把它标为 🟠，避免把 UCD/BD consistency work 误写成 STM direct baseline。

## 重要的相关工作

### 1. 重要的前身类工作

**Apvrille and Sultan (2024), System Architects Are not Alone Anymore: Automatic System Modeling with AI, MODELSWARD 2024**

- **主要内容**：提出 TTool-AI，从自然语言系统规格生成 SysML BDs 和 SMDs，并通过自动反馈循环减少人工 refinement。
- **原文位置**：第 2.2 节和第 4 节明确说明本文构建在 TTool-AI 之上；第 4 节说明 BD 生成阶段 B1-B5 已在 TTool-AI 中实现。
- **与本文关系**：这是本文最直接的前身工作。本文补入 UCD 生成和 UCD/BD 一致性检测修复闭环。
- **对 Project 1 的意义**：TTool-AI 是更接近状态机生成 baseline 的前身；本文则是其一致性/修复扩展。

**TTool / AVATAR / SysML formal verification 相关工作**

- **主要内容**：TTool 是开源 MDE 框架，支持 SysML 图形和文本建模、代码生成、仿真和模型检查。相关引用包括 Pedroza et al. (2011) 的 AVATAR，Knorreck et al. (2013) 的 system-level design space exploration，以及 Calvino and Apvrille (2021) 的 direct model-checking of SysML models。
- **原文位置**：第 2.3 节介绍 TTool 背景能力。
- **与本文关系**：提供工具基础设施和语法检查/图生成环境，但本文实验核心不是 TTool 的模型检查能力。

### 2. 直接参与实验的 baseline

**原文未提供外部自动化 baseline。**

论文的评估是三案例内部评估：生成 UCD/BD，检测不一致，再尝试修复不一致。表 4 统计 internal/external inconsistencies、errors 和 corrected inconsistencies；没有与其他一致性检查工具、其他 LLM 框架或人工 baseline 做直接对照。

### 3. 提供了重要论证的工作

**Torre, Labiche, Genero, and Elaasar (2018), A Systematic Identification of Consistency Rules for UML Diagrams, Journal of Systems and Software**

- **主要内容**：系统识别 UML 图一致性规则。
- **原文位置**：第 2.1 节引用其系统性工作，说明已有大量规则式一致性研究；第 3.2 节中部分规则来源也与其相关。
- **与本文关系**：支撑“规则式方法有效但只能覆盖预定义规则”的问题定位。

**Torre, Labiche, and Genero (2014), UML Consistency Rules: a Systematic Mapping Study, EASE 2014**

- **主要内容**：系统映射 UML 一致性规则研究。
- **原文位置**：第 2.1 节作为规则式方法综述依据。
- **与本文关系**：证明 UML/SysML 一致性规则有既有研究基础，但仍不足以覆盖 LLM 生成图中的新错误类型。

**Cámara, Troya, Burgueño, and Vallecillo (2023), On the Assessment of Generative AI in Modeling Tasks: an Experience Report with ChatGPT and UML, Software and Systems Modeling**

- **主要内容**：研究 GPT 生成 UML class diagrams 的表现，指出 syntactically correct 不代表 semantic consistency 充分。
- **原文位置**：第 2.2 节引用其发现，说明 GPT 可生成语法正确模型但常需迭代 refinement。
- **与本文关系**：支撑本文为什么需要自动一致性检测与修复闭环。

### 4. 在技术上提供了支持的工作

**OpenAI GPT-4 Technical Report (2023)**

- **主要内容**：GPT-4 技术报告。
- **原文位置**：第 2.2 节以 OpenAI GPT 作为 LLM 背景；第 4 节说明本文使用 OpenAI GPT-4-turbo 和 GPT-4o。
- **与本文关系**：提供底层 LLM 能力来源，但论文方法贡献在 TTool-AI 集成、规则和反馈流程。

**Ibrahim et al. (2010), On well-formedness rules for UML use case diagram, WISM 2010**

- **主要内容**：UML use case diagram well-formedness rules。
- **原文位置**：表 1 中 RU4、RU5、RU6、RU10 等规则引用或派生自该工作。
- **与本文关系**：为 UCD 内部一致性规则提供部分规范依据。

**Sultan et al. (2023), W-Sec 与 AMULET 相关工作**

- **主要内容**：作者团队关于 SysML block diagram 定义、安全 countermeasure 影响分析和 SysML 模型 mutation 的工作。
- **原文位置**：第 3.1.2 节说明本文 block diagrams definitions derive from references [24, 25]。
- **与本文关系**：为 BD 形式化定义提供前置定义，而不是直接实验 baseline。

### 5. 其他重要工作

**Berglund (2024), Assessing Strategies for Behaviour Consistency Checking Using LLMs, B.Sc. Thesis**

- **主要内容**：探索用 LLM 维护 UML activity diagrams 与对应生成源码之间的一致性。
- **原文位置**：第 2.4 节作为相关区域工作出现。
- **与本文关系**：说明 LLM consistency checking 已有邻近探索，但本文声称尚无公开研究聚焦模型视图内部与跨视图一致性。

**Li and Shin (2024), Mutation-Based Consistency Testing for Evaluating the Code Understanding Capability of LLMs, CAIN 2024**

- **主要内容**：检测 source code 与自然语言描述之间的一致性。
- **原文位置**：第 2.4 节作为 LLM 检测不一致的相关方向。
- **与本文关系**：提供“LLM 可用于一致性检测”的邻近证据，但对象不是 SysML 多视图模型。

**Ma, Kelsen, and Glodt (2015), A generic model decomposition technique and its application to the Eclipse modeling framework, Software & Systems Modeling**

- **主要内容**：模型分解技术。
- **原文位置**：第 6 节讨论复杂模型 scalability 时引用。
- **与本文关系**：作为未来扩展复杂模型时的分解/重组策略线索。

## 文献分类总结

本文位于 TTool-AI 研究链条的后续扩展位置：TTool-AI 解决自然语言到 SysML 图的自动生成，本文进一步处理 LLM 生成 SysML 图之后的内部一致性和跨图一致性问题。它依赖三类基础：UML/SysML consistency rule 文献、TTool/AVATAR/SysML 工具基础设施、OpenAI GPT 及相关 LLM 建模经验研究。

在 Project 1 baseline 体系中，它应归为“生成后一致性检测与修复基础设施”或“TTool-AI adjacent work”。它对状态机建模研究有方法借鉴价值，尤其是反馈闭环、规则注入、JSON 不一致列表和公开工件化；但由于输出主体是 UCD/BD 而非 STM/SMD，不能归入 exact STM direct baseline，建议总账评估为 🟠。

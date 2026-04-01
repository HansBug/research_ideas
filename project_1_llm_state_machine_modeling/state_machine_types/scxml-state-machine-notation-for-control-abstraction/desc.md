# 状态图 XML：控制抽象的状态机记法 / State Chart XML (SCXML): State Machine Notation for Control Abstraction

## 基本信息

- 标题：State Chart XML (SCXML): State Machine Notation for Control Abstraction
- 中文标题：状态图 XML：控制抽象的状态机记法
- 作者：W3C Voice Browser Working Group
- 发表：W3C Recommendation, 2015
- DOI：原文未提供
- 链接：https://www.w3.org/TR/scxml/
- 形式主义：SCXML
- 主类：🧩
- 描述客体：🎛️
- 所属领域：💻
- 论文角色：标准规范
- 工具/实现获取方式：规范提到实现报告与测试套件，但本标准正文不附带统一处理器下载入口。
- 标准/格式获取方式：官方 W3C Recommendation 页面、Schema 与事件 I/O 处理器定义即标准获取入口。

## 简报

SCXML 的核心价值不在于重新发明状态机语义，而在于把 Harel 风格层次状态机做成可交换、可执行的 XML 承载格式。它同时覆盖 `<state>`、`<parallel>`、`<transition>`、`<history>`、`<datamodel>`、`<send>/<invoke>` 等构件，是状态机从图形建模走向运行时与互操作的重要桥梁。

- 形式主义定位：层次状态机的 XML 执行与交换载体。
- 构造方式简述：通过 XML 元素声明状态、并行区、迁移、历史、数据模型和可执行内容。
- 基础设施与场景简述：W3C 提供 recommendation、schema、event I/O processors、implementation report 和 test suite，适合作为执行载体和互操作格式。

```text
事件驱动控制需求 -> 层次状态机结构 -> SCXML XML 文档 -> 解释执行/集成互操作
```

## 形式主义定义与核心对象

### 定义对象

该规范面向一般-purpose event-based state machine，强调的是事件驱动控制逻辑如何以统一 XML 结构表达并执行。

### 核心抽象

核心结构由 `<scxml>` 容器、`<state>`、`<parallel>`、`<transition>`、`<initial>`、`<final>`、`<history>` 以及 `Executable Content` 与 `Data Model` 组成。

为了便于分析，可以把一个 SCXML 文档压成：

$$
X = (S, s_0, T, \eta_0, Q_{ext}, Q_{int})
$$

上式中的符号逐项解释如下：

1. `S` 是由 `<state>` / `<parallel>` / `<final>` / `<history>` 构成的状态树。
2. `s_0` 由 `<scxml>` 的 `initial` 入口决定。
3. `T` 是由 `<transition>` 元素给出的迁移集合。
4. `\eta_0` 是初始 datamodel 赋值。
5. `Q_{ext}`、`Q_{int}` 分别是外部和内部事件队列。

### 一个最小例子与通俗解释

一个最小例子是“门锁状态机”的 SCXML 表达：

1. `<state id="locked">` 中放一条 `<transition event="coin" target="unlocked"/>`。
2. `<state id="unlocked">` 中放一条 `<transition event="push" target="locked"/>`。
3. 如果再配一个 `<datamodel>` 变量计数开门次数，就能把简单状态切换和数据更新放在同一份 XML 文档里。

通俗解释是：`SCXML` 相当于把层次状态机写成一份标准化 XML。人脑看的是状态、事件和嵌套关系；机器看的是统一标签、统一算法和统一事件队列，所以它既能表达 `Statechart` 式结构，又能直接交给执行器运行。

### 运行 / 接受 / 转移语义

SCXML 的运行时状态不是单点，而是一个 legal state configuration：

$$
C \subseteq S
$$

规范明确要求：

$$
C \in \mathrm{Legal}(X)
$$

其核心约束包括：

1. 恰有一个顶层子状态处于配置中。
2. 至少有一个 atomic state 处于配置中。
3. 若某个 compound state 在 `C` 中，则其恰有一个活动子状态在 `C` 中。
4. 若某个 `<parallel>` 在 `C` 中，则其所有子区域都在 `C` 中。

在事件 `e` 和当前配置 `C` 下，规范定义最优转移集：

$$
\mathrm{Opt}(C,e)
$$

它由 descendant-priority 和 document-order 共同决定。一次 microstep 即执行该最优转移集：

$$
(C,\eta,Q_{int}) \xRightarrow{\mu_e} (C',\eta',Q_{int}')
$$

而一次 macrostep 是若干 microstep 的闭包，直到内部事件队列为空且无 `NULL` 使能迁移：

$$
(C,\eta,Q_{int},e) \xRightarrow{\mathrm{macro}} (C^*,\eta^*,\emptyset)
$$

上述执行语义中的符号逐项解释如下：

1. `C` 是当前活动状态配置。
2. `\mathrm{Legal}(X)` 是关于文档 `X` 的合法配置集合。
3. `e` 是当前待处理事件。
4. `\mathrm{Opt}(C,e)` 是在配置 `C` 下针对事件 `e` 选出的最优转移集。
5. `\eta` 是当前 datamodel 变量环境。
6. `Q_{int}` 是内部事件队列。
7. `\xRightarrow{\mu_e}` 表示一次 microstep。
8. `\xRightarrow{\mathrm{macro}}` 表示一次 macrostep，也就是若干 microstep 的闭包。
9. `C^*` 与 `\eta^*` 是 macrostep 结束后的最终配置和最终数据环境。
10. `\emptyset` 表示内部事件队列被清空。

### 语义边界

SCXML 仍然是离散事件状态机，不是连续或概率模型。它擅长承载层次状态机、事件处理和外部通信，但其时序能力主要依赖外部事件与定时发送，不等价于显式时钟自动机。

### 关键性质与判定边界

SCXML 最关键的语义性质是 run-to-completion：每个外部事件触发恰好一个 macrostep，期间外部事件不会插入当前处理过程。

$$
e \in Q_{ext} \Rightarrow \text{one macrostep per external event}
$$

这条 RTC 约束中的符号逐项解释如下：

1. `Q_{ext}` 是外部事件队列。
2. `e \in Q_{ext}` 表示事件 `e` 来自环境输入。
3. `one macrostep per external event` 表示每个外部事件都触发且只触发一轮完整的 run-to-completion 处理。

规范还明确给出两个边界：

1. 优先级由“更深源状态优先，其次文档顺序优先”固定下来。
2. microstep 必须终止，但 macrostep 允许因内部事件链而不终止。

因此 SCXML 的工程价值不只是 XML 载体，而是它把 `Statecharts` 那种容易歧义的执行细节收束成了可实现的处理算法。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | `<state>`、`<final>` 等元素直接表达模式。 |
| 事件 / 触发 | 强支持 | 事件选择与执行迁移是核心。 |
| 守卫 / 数据 | 支持 | `cond`、`<datamodel>`、`<assign>` 等支持数据驱动。 |
| 层次 | 强支持 | 复合状态与嵌套结构是核心。 |
| 并发 / 同步 | 支持 | `<parallel>` 表达并行子状态。 |
| 时间约束 | 部分支持 | 依赖事件/发送机制，不是显式时钟模型。 |
| 连续动态 / 随机性 | 不支持 | 无连续流和概率语义。 |
| 可执行 / 可验证性 | 强支持 | 是为执行环境设计的标准化表示。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 合法配置 | `$C \in \mathrm{Legal}(X)$` | 当前活动状态集必须满足层次/并行一致性。 |
| 最优转移集 | `$\mathrm{Opt}(C,e)$` | 由优先级与冲突消解决定本步要执行哪些转移。 |
| microstep | `$(C,\eta,Q_{int}) \xRightarrow{\mu_e} (C',\eta',Q_{int}')$` | 执行一次最优转移集。 |
| macrostep | `$(C,\eta,Q_{int},e) \xRightarrow{\mathrm{macro}} (C^*,\eta^*,\emptyset)$` | 一个外部事件对应一整轮内部闭包执行。 |
| run-to-completion | `one external event \Rightarrow one macrostep` | 执行器的核心调度语义。 |

## 构造方式与承载格式

### 建模入口

建模入口是 XML 文档结构，而不是纯图形编辑。设计者显式声明状态树、并行区、事件转移和数据模型。

### 机器可处理承载方式

机器可处理承载方式就是 SCXML XML 本身；规范还定义了算法、schema、datamodel 与 event I/O processors。

### 交换与互操作

这是 SCXML 的核心价值之一。它以统一标记语言承载层次状态机，使不同执行器、浏览器语音框架和嵌入式集成系统可以围绕同一文档交换行为模型。

## 配套基础设施

- 建模/编辑工具：规范未绑定单一编辑器。
- 解析/交换/元模型支持：提供 schema 和标准 XML 表达。
- 仿真/执行支持：规范直接定义解释算法与 conforming processors。
- 验证/分析支持：正文不定义验证器，但标准格式便于外接分析工具。
- 代码生成/转换支持：正文未强制规定。
- 标准化或社区生态：W3C Recommendation、Implementation Report、Test Suite 构成成熟基础设施。

## 适用场景与需求前提

### 适用场景

适用于需要标准化交换、运行时解释执行或跨组件集成的事件驱动控制逻辑，例如语音交互、嵌入式 UI 流程、服务编排状态控制。

### 需求前提

1. 需求能抽象成事件驱动状态机。
2. 需要明确的数据上下文、事件处理和动作执行。
3. 希望状态机有稳定文本载体，便于交换和部署。

### 不适用或高成本场景

若核心问题在严密实时验证、连续动力学或高性能数值控制，SCXML 不是最直接的理论模型。

## 与相邻形式主义的关系

相对 `Statecharts`，SCXML 提供标准化文本载体；相对 `UML State Machine`，它更偏执行与集成，而不是通用建模元模型；相对 `Timed Automata`，它没有显式时钟判定语义。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合作为 `project_1` 最终输出工件或中间交换工件，因为它把状态机从“图”变成了“可直接处理的标准文件”。

### 作为目标形式主义还是中间表示

更适合作为目标交付格式或执行载体。

### 对需求到模型生成的启发

在 LLM 建模链路中，可以先生成结构化层次状态机，再投影为 SCXML 文档，以获得可执行和可互操作的输出。

### 现实限制

如果后续验证强依赖显式实时时钟或混成语义，SCXML 本身仍需映射到更强的分析模型。

## 重要的相关工作

### 奠基或前身工作

- Harel Statecharts。
- CCXML。

### 同类型或同家族工作

- 各类层次状态机执行器。

### 标准 / 格式 / 工具链工作

- W3C Schema、Implementation Report、Test Suite、Event I/O Processors。

### 与本研究关系最紧的工作

- 状态机文本化生成、运行时执行和跨工具互操作。

## 文献分类总结

- 主类：🧩
- 描述客体：🎛️
- 所属领域：💻
- 形式主义：SCXML
- 论文角色：标准规范
- 核心功能：以 XML 形式承载可执行层次状态机。
- 关键特性：状态/并行/历史/迁移/数据模型/可执行内容/外部通信。
- 构造方式：`<scxml>` 文档 + 核心元素 + datamodel + executable content。
- 基础设施：W3C Recommendation、Schema、实现报告、测试套件。
- 适用场景：需要标准文本载体与互操作的事件驱动控制逻辑。
- 需求前提：需求可表达成层次事件状态机并需要稳定交换格式。
- 状态：🟢

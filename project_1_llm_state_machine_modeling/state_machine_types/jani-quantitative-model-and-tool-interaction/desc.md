# JANI：定量模型与工具互操作 / JANI: Quantitative Model and Tool Interaction

## 基本信息

- 标题：JANI: Quantitative Model and Tool Interaction
- 中文标题：JANI：定量模型与工具互操作
- 作者：Carlos E. Budde，Christian Dehnert，Ernst Moritz Hahn，Arnd Hartmanns，Sebastian Junges，Andrea Turrini
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 151-168，2017
- DOI：`10.1007/978-3-662-54580-5_9`
- 链接：https://doi.org/10.1007/978-3-662-54580-5_9
- 形式主义：`jani-model / jani-interaction`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：定量验证领域的统一 JSON 模型格式与工具交互协议
- 工具/实现获取方式：原文明确说明完整规范、模型库和持续演化入口由 `jani-spec.org` 维护，并列出多个已接入工具。
- 标准/格式获取方式：核心承载是 `jani-model` JSON 模型格式与 `jani-interaction` JSON client-server 协议。

## 简报

这篇论文的核心价值，是把原本各自为政的 quantitative verification 工具链，收束到一个足够轻、足够机器友好的中立交换层上。`JANI` 不再尝试用一门巨大的人类建模语言统一世界，而是把“带变量的自动机网络 + JSON + 同步向量 + 工具消息协议”固定成一套实现成本低、互操作性高的中间层。

- 形式主义定位：定量模型交换格式与工具协议，不是新的自动机理论分支。
- 构造方式简述：高层语言先被编译成 `jani-model` 的自动机网络 JSON，再通过 `jani-interaction` 驱动分析、转换和结果返回。
- 基础设施与场景简述：依托 `jani-spec.org`、JSON、同步向量、transient variables 和 client-server 协议，服务 `Storm`、`ePMC`、`Modest`、`Momba` 等 quantitative toolchain 的互操作。

```text
high-level model -> jani-model JSON -> jani-interaction session -> analyzer / transformer / UI -> result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `jani-model` 的自动机网络语义。
2. 全局/局部变量、transient variables 与 indexed assignments。
3. synchronisation vectors。
4. `jani-interaction` 的工具查询、配置、分析与结果交换消息。
5. `DTMC/CTMC/MDP/PTA/MA/STA/SHA` 等定量模型家族。

### 核心抽象

论文把 `JANI` 描述成“带变量的 `SHA` 网络及其特例”的直接 JSON 表示。可保守整理为：

$$
J = (\mathcal{A}, V, Sync, Init, Prop, Ext)
$$

上式中的符号逐项解释如下：

1. `\mathcal{A}` 是并行执行的自动机集合。
2. `V` 是全局与局部变量集合。
3. `Sync` 是同步向量和输入使能动作集合。
4. `Init` 是初始状态与变量初始化信息。
5. `Prop` 是附着在模型上的性质表达。
6. `Ext` 是版本和扩展机制。
7. 这组符号是对论文结构的保守归纳，不是原文显式给出的统一元组。

论文明确给出 `JANI` 支持的模型族范围：

$$
\mathrm{Types}(J) = \{\mathrm{DTMC}, \mathrm{CTMC}, \mathrm{MDP}, \mathrm{CTMDP}, \mathrm{MA}, \mathrm{TA}, \mathrm{PTA}, \mathrm{STA}, \mathrm{SHA}\}
$$

上式中的符号逐项解释如下：

1. `DTMC` 和 `CTMC` 是离散/连续时间马尔可夫链。
2. `MDP` 和 `CTMDP` 是带非确定性的马尔可夫决策过程。
3. `MA` 是 Markov automata。
4. `TA`、`PTA`、`STA`、`SHA` 分别对应 timed、probabilistic timed、stochastic timed 与 stochastic hybrid automata。
5. 这是论文图示和正文直接列出的支持范围。

同步向量是 `JANI` 的关键构件。对三个自动机的多方同步，论文直接给出：

$$
[a;a;a]
$$

上式中的符号逐项解释如下：

1. 三个 `a` 表示三个自动机都在同一动作标签上同步。
2. 这对应 `CSP`/`PRISM` 风格的 multi-way synchronisation。
3. 这是论文正文直接给出的例子。

对 `CCS` 风格二元同步，论文给出：

$$
\{[a!;a?;],[a?;a!;],[a!;;a?],[a?;;a!],[;a!;a?],[;a?;a!]\}
$$

上式中的符号逐项解释如下：

1. `a!` 和 `a?` 分别表示发送和接收。
2. 三元向量中的空位表示该自动机不参与这次同步。
3. 整个集合枚举了三个自动机之间所有可能的二元配对。

### 一个最小例子与通俗解释

一个最小直觉例子就是三个自动机一起在动作 `a` 上同步：

1. 如果要表达“这三个模块必须同时推进”，就放一个同步向量 `[a;a;a]`。
2. 如果只想表达“任意两个模块做 send/receive 同步”，就列一组 `a!/a?` 向量。
3. 如果同步时要传值，就让发送方先把值写入 transient variable，再让接收方按更大的 assignment index 读取。

通俗地说，`JANI` 不是让大家都改说同一种 DSL，而是先约定“中间交换件长什么样、工具之间怎么说话”。它更像定量验证世界的一个稳定插口。

### 运行 / 接受 / 转移语义

论文描述的核心执行语义是：

1. 自动机边可以独立执行，也可以按同步向量一起执行。
2. 同步边上的赋值默认原子执行。
3. 若赋值带 index，则同 index 原子、不同 index 按编号顺序执行。
4. transient variables 不进入状态向量，前后都会被清空，因此可用于低成本值传递。

### 语义边界

边界同样很清楚：

1. `JANI` 是 interchange layer，不是让用户手写的重型建模语言。
2. 它追求的是“易解析、易生成、易扩展”，不是“语法上最优雅”。
3. 分析能力最终仍由接入的后端工具决定。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 核心结构 | `$J = (\mathcal{A}, V, Sync, Init, Prop, Ext)$` | `JANI` 组织的是带变量的自动机网络及其属性。 |
| 模型族范围 | `$\mathrm{Types}(J) = \{\mathrm{DTMC},\ldots,\mathrm{SHA}\}$` | 同一交换层覆盖离散、实时时钟到随机混成模型。 |
| 多方同步 | `$[a;a;a]$` | 统一表达 `CSP/PRISM` 风格 multi-way synchronisation。 |
| 二元同步 | `$\{[a!;a?;],\ldots,[;a?;a!]\}$` | 统一表达 `CCS` 风格 send/receive 配对。 |
| 值传递 | `$t:=v$ at index $i,\ l:=t$ at index $i'>i$` | 用 transient variable 和 indexed assignment 实现同步传值。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 自动机位置与变量构成模型状态。 |
| 事件 / 触发 | 很强 | 动作标签和同步向量是一等对象。 |
| 守卫 / 数据 | 很强 | 带变量、表达式、transient value passing。 |
| 层次 | 弱支持 | 主体不是层次状态机语言。 |
| 并发 / 同步 | 很强 | 自动机网络并发和同步向量是核心。 |
| 时间约束 | 很强 | 直接覆盖 `TA/PTA/STA/SHA`。 |
| 连续动态 / 随机性 | 很强 | 支持概率、随机时间和混成扩展。 |
| 可执行 / 可验证性 | 很强 | 目标就是跨工具分析、转换和竞赛互操作。 |

### 形式化问题与性质

1. `JANI` 的关键贡献不是再发明一个求解器，而是把模型和工具接口稳定下来。
2. 同步向量和 transient variables 使它比简单 guarded-command 交换格式更灵活。
3. `jani-interaction` 让分析过程本身也能以语言无关协议稳定暴露出来。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 从 `PRISM`、`Modest`、`GreatSPN` 等前端语言或工具导出模型。
2. 生成 `jani-model` JSON。
3. 通过 `jani-interaction` 查询工具能力、发送分析任务、获得结果。
4. 必要时再转回高层语言或交给 UI/benchmark 框架。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `jani-model` JSON 文档；
2. `jani-interaction` JSON 消息；
3. version / extension points；
4. tool capabilities、analysis tasks 和 result payloads。

### 交换与互操作

这篇论文的互操作重点在于：

1. `jani-model` 统一模型表示；
2. `jani-interaction` 统一工具调用协议；
3. higher-level language 到 `JANI` 的自动转换；
4. 不同 analyzer、transformer、UI 之间的稳定连接。

## 配套基础设施

- 建模/编辑工具：`PRISM`、`Modest Toolset`、`Momba` 等可作为 `JANI` 前端或后端。
- 解析/交换/元模型支持：`jani-model` JSON、版本机制、扩展机制、模型库。
- 仿真/执行支持：依赖具体后端；`JANI` 自身提供的是交换层而不是单一 simulator。
- 验证/分析支持：原文明确列出多个已支持工具，含 `Storm`、`ePMC`、`Modest Toolset` 等。
- 代码生成/转换支持：重点是 model-to-model 转换和 tool invocation，不是部署代码生成。
- 标准化或社区生态：`jani-spec.org`、共享规范、模型库与竞赛导向的工具合作生态。

## 适用场景与需求前提

### 适用场景

适合需要跨多个 quantitative verification 工具复用模型、批量实验、竞赛基准共享、统一前后端接口的场景。

### 需求前提

1. 模型能自然落成“自动机网络 + 变量 + 同步”骨架。
2. 团队更关心互操作和复用，而不是绑定单一专用 DSL。
3. 后续分析任务确实需要跨工具或跨工作流迁移。

### 不适用或高成本场景

如果模型根本不属于 automata-like quantitative family，或者团队只用单一封闭工具，`JANI` 的收益会明显下降。

## 与相邻形式主义的关系

相对 [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)，这里给的是底层交换格式和协议，而 `Momba` 是其上层 Python 工作流；相对 [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)，`Modest Toolset` 是平台，`JANI` 是跨平台插口；相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，`PRISM` 是具体后端和语言，而 `JANI` 是更中立的 interchange layer。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合被看成 `project_1` 后续“生成-验证-修复”闭环里的中间交换层：前端可以生成统一 JSON，中后端再按需要挂接不同验证器。

### 作为目标形式主义还是中间表示

更像中间表示和工具互操作标准，而不是最终目标形式主义。

### 对需求到模型生成的启发

1. LLM 若要服务多个验证后端，统一中间格式比直接面向单一工具更稳。
2. 同步向量和 transient variables 提供了很好的“机器友好承载”思路。
3. 可扩展 JSON 比一次性固定死的大而全 DSL 更适合持续演化。

### 现实限制

它解决的是“怎么交换与调用”，不是“怎么自动得到正确模型”。

## 重要的相关工作

1. [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)：`JANI` 上层的 Python 工作流。
2. [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)：定量平台本体。
3. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：概率实时模型检查平台与语言锚点。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 归类理由：主贡献是 `jani-model` 与 `jani-interaction` 这套交换层和协议层基础设施，而不是新的单体状态机本体或单一求解方法。

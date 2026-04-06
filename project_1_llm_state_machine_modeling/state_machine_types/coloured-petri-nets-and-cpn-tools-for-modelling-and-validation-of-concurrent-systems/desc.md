# 着色 Petri 网与 CPN Tools / Coloured Petri Nets and CPN Tools for Modelling and Validation of Concurrent Systems

## 基本信息

- 标题：Coloured Petri Nets and CPN Tools for modelling and validation of concurrent systems
- 中文标题：着色 Petri 网与 CPN Tools：并发系统建模与验证
- 作者：Kurt Jensen，Lars Michael Kristensen，Lisa Wells
- 发表：*International Journal on Software Tools for Technology Transfer*，9(3-4):213-254，2007
- DOI：`10.1007/s10009-007-0038-x`
- 链接：https://doi.org/10.1007/s10009-007-0038-x
- 形式主义：`Coloured Petri Nets / CPN Tools`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 论文角色：工业级建模与分析工具链总览
- 工具/实现获取方式：原文明确说明 `CPN Tools` 可从其 web pages 免费获取许可，并提供 GUI、simulation、state-space、performance-analysis 与 visualization 工具。
- 标准/格式获取方式：承载方式是图形化 `CPN` 模型加 `CPN ML` 声明与 inscriptions；原文未提供中立交换标准。

## 简报

这篇论文的价值不只是回顾 `CPN` 语义，而是把 `CPN Tools` 这条成熟工具线完整摆出来。它一方面讲清 `Coloured Petri Nets` 如何用 colour sets、typed variables、arc expressions、hierarchical modules 和 time 来压并发系统；另一方面把 `CPN Tools` 的 GUI、simulation、state-space analysis、performance analysis 和 visualization 串成一条真正可用的工程链。

- 形式主义定位：`Coloured Petri Nets` 的成熟建模与分析工具链总览，而不是新的网模型。
- 构造方式简述：用 places、transitions、arcs、colour sets、typed variables 和 `CPN ML` inscriptions 搭模型，再通过 GUI 操作、仿真、状态空间与性能分析验证行为。
- 基础设施与场景简述：依托 `CPN Tools` 的 palette/menu GUI、state-space engine、query functions、performance monitors 与 domain-specific visualization，服务协议、工作流、资源共享和一般并发系统。

```text
并发系统需求 -> CPN places/transitions + CPN ML inscriptions -> executable CPN model -> simulation / state space / performance analysis / visualisation
```

## 形式主义定义与核心对象

### 定义对象

论文直接围绕以下对象组织 `CPN`：

1. places、transitions 和 arcs 构成 net structure。
2. colour sets 定义每个 place 能承载的 token 类型。
3. tokens 与 markings 描述系统状态。
4. typed variables、constants 与 arc expressions 用 `CPN ML` 表示。
5. hierarchical modules、time 和 analysis/visualisation facilities 作为工具扩展层。

### 核心抽象

论文没有把 `CPN` 再次压成单行 textbook 定义，但结合 Sec. 2.1-2.5 的内容，可保守整理为：

$$
CPN = (P, T, A, \Sigma, V, C, G, E, I)
$$

上式中的符号逐项解释如下：

1. `P` 是 places 集合。
2. `T` 是 transitions 集合。
3. `A` 是 arcs 集合。
4. `\Sigma` 是 colour sets 集合。
5. `V` 是 typed variables 集合。
6. `C : P \to \Sigma` 为每个 place 指派 colour set。
7. `G : T \to Expr` 为 transition 指派 guard（本文示例里常被省略成 `true`）。
8. `E : A \to Expr` 为每条 arc 指派 `CPN ML` expression。
9. `I : P \to MS_\Sigma` 为每个 place 给出初始 marking。

其中 `MS_\Sigma` 表示以 colour values 为元素的 multiset。论文里 `1\`(1,"COL") ++ 1\`(2,"OUR")` 这类写法就是在构造 marking multiset。

### 一个最小例子与通俗解释

论文一开始就给了 stop-and-wait simple protocol：

1. `PacketsToSend`、`NextSend`、`A/B/C/D`、`NextRec`、`DataReceived` 这几个 place 分别存发送端、网络和接收端状态。
2. packet token 是 `(sequence_number, payload)` 这样的 pair colour。
3. `SendPacket`、`TransmitPacket` 等 transitions 用 arc expressions 搬运 token。
4. 若网络丢包或乱序，重传逻辑就通过 markings 的变化自然表现出来。

通俗地说，`CPN` 就像“会搬运带类型数据的 Petri 网”。普通 `Petri Net` 只看 token 个数，而 `CPN` 让 token 自带值，transition 既能消费/产生 token，也能算变量、拼表达式，所以一个网就能同时表达控制流和数据流。

### 运行 / 接受 / 转移语义

论文把 enabling 和 occurrence 讲得很工程化。对一个 marking `M` 和 transition `t`，在 binding `b` 下的使能条件可保守写成：

$$
\forall a=(p,t)\in A_{in}:\ E(a)\langle b \rangle \le M(p)
$$

上式中的符号逐项解释如下：

1. `A_{in}` 是所有输入 arc 的集合。
2. `a=(p,t)` 表示从 place `p` 指向 transition `t` 的 arc。
3. `E(a)\langle b \rangle` 是在绑定 `b` 下求值后的 arc expression，对应一个 multiset。
4. `M(p)` 是当前 place `p` 上的 marking。
5. `\le` 表示 multiset inclusion，即输入 place 上必须至少有足够的 token multiset。

一旦发生，就得到新 marking：

$$
M' = M - E_{in}\langle b \rangle + E_{out}\langle b \rangle
$$

上式中的符号逐项解释如下：

1. `E_{in}\langle b \rangle` 是所有输入 arc 在绑定 `b` 下求值后的 token multiset 总和。
2. `E_{out}\langle b \rangle` 是所有输出 arc 在绑定 `b` 下求值后的 token multiset 总和。
3. `M'` 是 firing 之后的新 marking。

论文还强调：

1. 双向 arc 可以简写成一进一出两条同表达式弧。
2. hierarchy 允许把 net 组织成 modules。
3. time 概念允许 token 带时间戳并进入 timed simulation / performance analysis。

### 语义边界

这篇论文也清楚说明了它的边界：

1. `CPN` 擅长离散事件并发系统，不是连续动力学模型。
2. 数据表达能力很强，但前提是能压进 `CPN ML` / Standard ML 风格表达式。
3. 工具线很成熟，但交换格式仍主要依赖工具生态，而不是中立标准。
4. 性能分析和 state-space analysis 都很强，但模型规模仍可能受 state explosion 影响。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `CPN` 骨架 | `$CPN = (P, T, A, \Sigma, V, C, G, E, I)$` | 把网结构、数据类型、表达式和初始 marking 收进同一模型。 |
| 使能条件 | `$\forall a=(p,t)\in A_{in}: E(a)\langle b \rangle \le M(p)$` | transition 必须在当前 marking 中找到足够的 token multiset。 |
| firing 结果 | `$M' = M - E_{in}\langle b \rangle + E_{out}\langle b \rangle$` | 发生后按 arc expressions 消费并生成 token。 |
| 分层组织 | `$\text{model} = \text{modules} + \text{substitution transitions}$` | 大模型可模块化。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 直接表达系统状态。 |
| 事件 / 触发 | 强支持 | transitions 是离散事件。 |
| 守卫 / 数据 | 很强 | colour sets、typed variables、`CPN ML` expressions 是核心。 |
| 层次 | 强支持 | substitution transitions / modules 是工具主线之一。 |
| 并发 / 同步 | 很强 | `Petri Net` 并发语义是母线。 |
| 时间约束 | 支持 | timed CPN 和 performance analysis 明确支持。 |
| 连续动态 / 随机性 | 不支持 | 主体仍是离散事件网。 |
| 可执行 / 可验证性 | 很强 | simulation、state space、query、performance、visualisation 一体化。 |

### 形式化问题与性质

1. `CPN` 的关键增强点不是“多几个网元”，而是把 typed data 和 ML 风格表达式嵌进 token/arc 语义。
2. `CPN Tools` 把 hierarchy、simulation、verification 和 performance analysis 串成了统一工作流。
3. 论文对非专家最有价值的地方是把 enabling / occurrence 讲成了“有类型、有绑定、有 multiset”的执行模型。

## 构造方式与承载格式

### 建模入口

原文中的典型建模入口是：

1. 先画 places、transitions、arcs。
2. 再声明 colour sets、variables、constants。
3. 给 places 写初始 markings，给 arcs 写 expressions。
4. 若模型大，再引入 hierarchical modules / substitution transitions。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `CPN Tools` 图形模型。
2. `CPN ML` declarations 与 inscriptions。
3. simulation monitors、state-space queries 和 performance collectors。

### 交换与互操作

这篇论文的重点不在中立交换标准，而在同一工具链内部的多分析后端：

1. 同一模型既可仿真，也可做 state-space analysis。
2. 性能分析和可视化直接消费同一执行轨迹或状态空间。
3. hierarchy 与 GUI 操作让大模型维护更现实。

## 配套基础设施

- 建模/编辑工具：`CPN Tools` GUI，核心交互是 palettes 与 marking menus。
- 解析/交换/元模型支持：`CPN ML` 声明和图形 net 模型共用统一内部表示；原文未提供中立交换标准。
- 仿真/执行支持：interactive simulation、automatic simulation、breakpoint monitors。
- 验证/分析支持：state-space construction、query functions、model checking。
- 代码生成/转换支持：本文重点不在代码生成，但支持 syntax check 和部分 code generation 工作流。
- 标准化或社区生态：免费许可、在线帮助、案例和教程构成了成熟的研究与教学生态。

## 适用场景与需求前提

### 适用场景

适合协议、并发软件、工作流、资源共享系统、离散事件生产系统，以及需要同时表达控制流和数据流的网模型场景。

### 需求前提

1. 系统核心是离散事件并发，而不是连续微分方程。
2. token 上的数据能用有限 typed values / expressions 表达。
3. 希望保留 hierarchy、可执行仿真和状态空间验证。
4. 可以接受较重的工具化建模过程。

### 不适用或高成本场景

如果核心问题是连续控制、复杂实时时钟约束或必须使用中立 XML 交换标准，单靠 `CPN Tools` 本身不够。

## 与相邻形式主义的关系

相对 [petri-nets-properties-analysis-and-applications/desc.md](../petri-nets-properties-analysis-and-applications/desc.md)，`CPN` 把普通 token 扩成 typed token 并显著增强数据表达；相对 [a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md](../a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md)，本文讲的是建模与分析工具链而不是交换标准；相对 [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)，它覆盖面更广，但对 timed-arc 语义没有后者那样专注。

## 与本研究的关系

### 对 Project 1 的价值

它证明了 `Petri Net` 路线如果要进入真正可用的工程链，必须同时考虑语言、工具、状态空间分析和可视化，而不是只停留在理论 tuple。

### 作为目标形式主义还是中间表示

对并发/资源流问题，它可以直接作为目标形式主义；对更一般的需求建模链，也适合作为高表达力中间表示。

### 对需求到模型生成的启发

1. 生成时不能只吐 place/transition 结构，还要吐 colour sets、variables、arc expressions 和 hierarchy。
2. 若后续要接验证，应尽量让模型保留可计算的 bindings、markings 和 queries。
3. 工具可用性很大程度取决于交互和可视化，而不只是语言本体。

### 现实限制

`CPN` 的表达力和工具能力都很强，但建模门槛也高；对纯控制状态机任务，未必是最轻量的选择。

## 重要的相关工作

- [petri-nets-properties-analysis-and-applications/desc.md](../petri-nets-properties-analysis-and-applications/desc.md)：普通 `Petri Net` 母线。
- [coloured-petri-nets/desc.md](../coloured-petri-nets/desc.md)：着色网理论入口。
- [a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md](../a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md)：`Petri Net` 交换格式母线。
- [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)：时间扩展网的专门 IDE / verifier。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Coloured Petri Nets / CPN Tools`
- 论文角色：工业级建模与分析工具链总览


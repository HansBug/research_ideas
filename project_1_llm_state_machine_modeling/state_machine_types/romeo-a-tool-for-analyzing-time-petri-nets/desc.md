# ROMEO：Time Petri Net 分析工具 / Romeo: A Tool for Analyzing Time Petri Nets

## 基本信息

- 标题：Romeo: A Tool for Analyzing Time Petri Nets
- 中文标题：ROMEO：Time Petri Net 分析工具
- 作者：Guillaume Gardey，Didier Lime，Morgan Magnin，Olivier H. Roux
- 发表：*Computer Aided Verification*，pp. 418-423，2005
- DOI：`10.1007/11513988_41`
- 链接：https://pagesperso.ls2n.fr/~roux-o/fichiers/conf/glmr-cav-2005.pdf
- 形式主义：`Time Petri Nets / Scheduling-TPNs / Romeo`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：time-Petri-net analyzer / translation bridge
- 工具/实现获取方式：原文明确给出 `Romeo` 下载入口，并说明支持 `Linux`、`MacOSX` 和 `Windows`。
- 标准/格式获取方式：原文明确支持 `TPN / Scheduling-TPN` 图形建模，并可生成 `Uppaal`、`Kronos`、`Hytech` 输入；未给独立中立交换标准。

## 简报

这篇论文的价值，在于把 `Time Petri Net` 的几条常见分析路线真正串起来了。`Romeo` 不只是一个 `TPN` editor，它同时覆盖 on-line simulation、reachability checking、observer-based verification，以及 `TPN -> TA`、`Scheduling-TPN -> SWA` 的翻译桥，使 `TPN` 可以直接接到 `Uppaal`、`Kronos`、`Hytech` 等验证后端。

- 形式主义定位：面向 `Time Petri Nets` 与 `Scheduling-TPNs` 的分析工具链，而不是新的时间网本体。
- 构造方式简述：输入 `TPN` 或 `Scheduling-TPN`，工具内部使用 marking reachability、state class graph、DBM / polyhedra、timed-bisimilar translation。
- 基础设施与场景简述：依托 `TCL/Tk` GUI、`Gpn/Mercutio` 计算模块、observer checking 与 `Uppaal/Kronos/Hytech` 后端，服务实时嵌入式调度、带抢占任务和时序约束的并发控制。

```text
TPN / Scheduling-TPN -> SCG / DBM / polyhedra -> reachability / observers / TA-SWA translation -> Uppaal / Kronos / Hytech
```

## 形式主义定义与核心对象

### 定义对象

论文的主体虽然是工具，但其工作对象非常明确：

1. `Time Petri Nets (TPNs)`。
2. `Scheduling-TPNs`，即在 `TPN` 上显式建模 task activation / suspension 的扩展。
3. marking reachability、state class graphs 与翻译后的 `Timed Automata / Stopwatch Automata`。

### 核心抽象

结合本文与本库已有 `TPN` 条目，可把 `Romeo` 的核心输入对象保守写成：

$$
N = (P, T, Pre, Post, M_0, I_s)
$$

上式中的符号逐项解释如下：

1. `P` 是库所集合。
2. `T` 是变迁集合。
3. `Pre` 与 `Post` 给出输入/输出弧。
4. `M_0` 是初始 marking。
5. `I_s` 把每个变迁映到 firing interval。

论文特别强调 `Romeo` 会把 `TPN` 翻译成与原模型 timed-bisimilar 的 `Timed Automata`，可保守写成：

$$
N \sim_t A_N
$$

上式中的符号逐项解释如下：

1. `N` 是原始 `TPN`。
2. `A_N` 是由 `Romeo` 生成的 `Timed Automata`。
3. `\sim_t` 表示 timed bisimilarity。

对在线 reachability checking，论文给出的典型性质形如：

$$
M(P_1) = 1 \lor M(P_3) \ge 3
$$

上式中的符号逐项解释如下：

1. `M` 是当前 marking。
2. `P_1`、`P_3` 是 places。
3. 该公式是 `Romeo` 可直接检查的 marking property 示例。

### 一个最小例子与通俗解释

最小直觉可以这样理解：

1. 一个 transition 在 `TPN` 里不是“满足就立刻 firing”，而是有一个可触发时间区间。
2. 如果任务被抢占，`Scheduling-TPN` 还要记住已经执行了多久。
3. `Romeo` 一边在原网里做 state space / observer checking，一边还能把同一模型翻译到 `Timed Automata` 或 `Stopwatch Automata`。
4. 这样一来，原本属于 `TPN` 世界的模型，就能借用 `Uppaal`、`Kronos`、`Hytech` 的时序检查能力。

通俗地说，`Romeo` 像“时间网和定时自动机之间的翻译兼分析总线”。你既可以直接看网，也可以把它送到更强的时间自动机后端。

### 运行 / 接受 / 转移语义

论文把 bounded `TPN` 的核心抽象固定在 state class graph 上。可保守写成：

$$
C = (M, D)
$$

上式中的符号逐项解释如下：

1. `M` 是 marking。
2. `D` 是关于使能变迁时间信息的约束域。
3. `Romeo` 的 SCG、DBM 与 polyhedra 方法都围绕这样的抽象状态展开。

`Scheduling-TPN` 到 `SWA` 的翻译则可以保守写成：

$$
S_N \sim_t W_N
$$

上式中的符号逐项解释如下：

1. `S_N` 是原始 `Scheduling-TPN`。
2. `W_N` 是生成的 `Stopwatch Automaton`。
3. 文中强调即使采用 over-approximating semi-algorithm，所得 `SWA` 仍与原模型 timed-bisimilar。

### 语义边界

这篇论文的边界也很清楚：

1. 主轴是 `TPN / Scheduling-TPN`，不是一般 `Hybrid Automata`。
2. `TPN` 的任意状态可达性与有界性在一般情形下仍不可判定，工程上依赖 bounded nets。
3. observer-based temporal property checking 对建模者有额外门槛。
4. 工具的强项是时间网与 translation bridge，不是通用交换标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 时间网骨架 | `$N = (P, T, Pre, Post, M_0, I_s)$` | 固定 `Romeo` 处理的核心对象。 |
| marking property | `$M(P_1) = 1 \lor M(P_3) \ge 3$` | 论文示例中的在线 reachability 检查。 |
| `TPN -> TA` 保真 | `$N \sim_t A_N$` | 翻译到 `Timed Automata` 时保持 timed bisimilarity。 |
| `Scheduling-TPN -> SWA` 保真 | `$S_N \sim_t W_N$` | 抢占扩展可翻到 `Stopwatch Automata`。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 是离散骨架。 |
| 事件 / 触发 | 强支持 | transition firing 是核心事件。 |
| 守卫 / 数据 | 部分支持 | 核心是 firing intervals、allocation 与 priority，而不是一般复杂数据。 |
| 层次 | 不支持 | 主体不是 hierarchy。 |
| 并发 / 同步 | 很强 | `Petri Net` 并发语义是母线。 |
| 时间约束 | 很强 | `TPN` 与 `Scheduling-TPN` 都以时间窗口为核心。 |
| 连续动态 / 随机性 | 不支持 | 不讨论一般连续 ODE 或概率 firing。 |
| 可执行 / 可验证性 | 很强 | on-line / off-line checking、translation bridge 都具备。 |

### 形式化问题与性质

1. `Romeo` 的最大价值不只是 reachability，而是把 `TPN` 接进 `TA/SWA` 模型检查生态。
2. `Scheduling-TPN` 这条线使“抢占与恢复”从网建模直接落到 stopwatch semantics。
3. 对 `TCTL` 这类量化时间性质，`Romeo` 给出的不是自造 checker，而是高保真翻译桥。

## 构造方式与承载格式

### 建模入口

论文中的典型入口是：

1. 用 GUI 绘制 `TPN` 或 `Scheduling-TPN`。
2. 在线跑 simulation 或 reachability。
3. 若需要更强检查，则翻译到 `TA/SWA`。
4. 交给 `Uppaal`、`Kronos`、`Hytech` 等后端。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Romeo` 图形建模输入。
2. SCG / DBM / polyhedra 内部表示。
3. `Uppaal` / `Kronos` 输入格式。
4. `Hytech` 输入格式。

### 交换与互操作

这篇论文的互操作是核心卖点之一：

1. `TPN -> TA` translation。
2. `Scheduling-TPN -> SWA` translation。
3. observer-based properties 与 temporal logic backends 的衔接。

## 配套基础设施

- 建模/编辑工具：`TCL/Tk` GUI，用于编辑与设计 `TPN / Scheduling-TPN`。
- 解析/交换/元模型支持：`Gpn` 与 `Mercutio` 计算模块；无中立交换标准。
- 仿真/执行支持：on-line simulation。
- 验证/分析支持：reachability checking、observers、SCG、DBM、polyhedra、`TCTL` 间接验证。
- 代码生成/转换支持：重点是到 `Uppaal`、`Kronos`、`Hytech` 的模型翻译，而不是代码生成。
- 标准化或社区生态：论文明确把 `Romeo` 放在 `Tina`、`Oris`、`Uppaal`、`Kronos`、`Hytech` 等工具生态中对比。

## 适用场景与需求前提

### 适用场景

适合实时并发流程、带抢占调度任务、嵌入式时序控制，以及希望把 `TPN` 接到时间自动机验证后端的场景。

### 需求前提

1. 系统本体更像 token / resource flow。
2. 时间要求可落到 transition firing intervals。
3. 若需要抢占语义，则必须显式建模任务激活 / 暂停关系。
4. 若要借助外部 model checker，团队需接受 translation-based workflow。

### 不适用或高成本场景

如果系统更自然的是层次状态机、接口协议或一般连续控制，`Romeo` 并不是首选入口。

## 与相邻形式主义的关系

相对 [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)，`Romeo` 更强调 `TPN -> TA/SWA` 翻译桥；相对 [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)，它更贴近经典 `TPN / Scheduling-TPN`；相对 [a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md](../a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md)，它解决的是分析与翻译，不是中立交换格式。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果 `project_1` 最终输出的是时间网而不是纯状态图，也仍然可以顺利接到成熟的 timed / stopwatch verification 工具链。

### 作为目标形式主义还是中间表示

对并发时序资源流场景，它可以是直接目标形式主义；对一般控制状态机，更适合作为验证后端。

### 对需求到模型生成的启发

1. 生成阶段要显式区分 places、transitions、markings 与 firing intervals。
2. 若系统有抢占恢复，必须把 allocation / priority 等调度语义补进模型，而不能只画普通 `TPN`。
3. translation-based verification 说明同一需求可以同时服务多个后端，不必把所有性质绑定在单一工具里。

### 现实限制

`Romeo` 很强，但它要的是结构化时间网，而不是通用状态机或黑盒调度器。

## 重要的相关工作

- [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)：经典 `TPN` analysis environment。
- [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)：更偏 `Timed-Arc Petri Net` 的 IDE 与验证路线。
- [time-petri-nets/desc.md](../time-petri-nets/desc.md)：`TPN` 的模型本体与 state-class 方法母线。
- [a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md](../a-primer-on-the-petri-net-markup-language-and-isoiec-15909-2/desc.md)：Petri 网标准交换格式路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Time Petri Nets / Scheduling-TPNs / Romeo`
- 论文角色：time-Petri-net analyzer / translation bridge

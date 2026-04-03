# 用参数化定时自动机验证存储电路通用架构 / Timed Verification of the Generic Architecture of a Memory Circuit Using Parametric Timed Automata

## 基本信息

- 标题：Timed Verification of the Generic Architecture of a Memory Circuit Using Parametric Timed Automata
- 中文标题：用参数化定时自动机验证存储电路通用架构
- 作者：Remy Chevallier，Emmanuelle Encrenaz-Tiphene，Laurent Fribourg，Weiwen Xu
- 发表：*Research Report LSV-06-14*，Laboratoire Specification et Verification，2006
- DOI：当前目录保存的是报告版；相关公开版本可见 `10.1007/11867340_9`（FORMATS 2006）与 `10.1007/s10703-008-0061-x`（期刊扩展版）
- 链接：https://doi.org/10.1007/11867340_9
- 形式主义：`Parametric Timed Automata / HYTECH Memory-Circuit Model`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：参数化时序验证 / `Parametric Timed Automata` 分支代表应用条目
- 工具/实现获取方式：原文明确使用 `HYTECH` 做 reachability analysis，并把结果与 `HSIM` 电路仿真作对照；未提供独立公开代码仓库。
- 标准/格式获取方式：承载方式是 wire/latch timed automata、线性参数约束和 `HYTECH` 多面体分析；原文未给交换标准。

## 简报

这篇论文的价值，在于它不是简单拿 `Timed Automata` 去验一个电路，而是把“门级延时未知但有区间”的现实设计问题稳定压成了 `Parametric Timed Automata`。作者把商业存储器 `SPSMALL` 的关键时序路径拆成 wire 和 latch 自动机，用参数 `l_i^\uparrow, u_i^\uparrow, l_i^\downarrow, u_i^\downarrow` 表示内部延时，再用 `HYTECH` 推出一组线性约束，直接回答“哪些参数范围能保证 datasheet 上的写时序成立”。

- 形式主义定位：这是 `Timed Automata -> Parametric Timed Automata` 的代表应用条目，重点在“参数综合 + datasheet 约束导出”。
- 构造方式简述：先把输入信号和内部元件建成 timed automata，再把门延时提升为参数，最后对两周期写操作做符号可达性分析，推出 `Assumption / Final` 约束。
- 基础设施与场景简述：依托 `HYTECH`、多面体符号状态、`HSIM` 电路仿真和存储器时序规格，服务 memory-circuit response-time verification。

```text
datasheet 时序需求 + 元件延时区间 -> wire/latch PTA -> symbolic reachability -> 线性参数约束 -> 写时序 / setup 时间验证
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. 输入信号 `CK`、`D`、`WEN` 的 timed automata。
2. `wire` 与 `latch` 元件的局部自动机。
3. 延时参数 `l_i^\uparrow, u_i^\uparrow, l_i^\downarrow, u_i^\downarrow`。
4. 用于测量全局时间的时钟 `s`。
5. 从 reachability 结果中抽取出的 `Assumption(D^\uparrow)` 与 `Final(D^\uparrow)` 线性约束。

### 核心抽象

原文先回顾 timed automata 的状态语义：状态写成 `(l, v)`，其中 `l` 是 location，`v` 是时钟赋值。结合原文对参数化延时的处理，可保守整理出本文实际使用的 `PTA` 骨架：

$$
M = (L, l_0, C, P, E, Inv)
$$

上式中的符号逐项解释如下：

1. `L` 是位置集合。
2. `l_0` 是初始位置。
3. `C` 是时钟集合，例如局部元件时钟和全局时钟 `s`。
4. `P` 是延时参数集合，对应各内部元件的上下界。
5. `E` 是带 guard、同步和 reset 的迁移集合。
6. `Inv` 是位置不变式，里面允许出现参数化线性约束。

原文明确写出的 timed automata 时间语义是：

$$
(l, v) \xrightarrow{t} (l, v + t)
$$

前提是对任意 `0 \le t' \le t` 都满足当前位置的不变式。离散步可以保守写成：

$$
(l, v) \xrightarrow{e} (l', v')
$$

其中 `v` 满足边 `e` 上的 guard，且 `v'` 由 `v` 对部分时钟 reset 后得到。

论文最关键的不是这套基础语义，而是把 reachability 结果压成参数不等式。对 `D` 上升沿写操作，作者给出：

$$
u_3^\downarrow + u_{15}^\downarrow + u_8^\downarrow + \max\{u_7^\uparrow, u_7^\downarrow\} \le twrite_{max}
$$

上式中的符号逐项解释如下：

1. `u_i^\uparrow, u_i^\downarrow` 是第 `i` 个元件传播上升/下降沿的最大延时。
2. `twrite_{max}` 是 datasheet 给出的写响应时间上界。
3. 整个不等式说明：只要内部参数满足这组上线性约束，写路径就不会超时。

### 一个最小例子与通俗解释

原文给出的最小局部构件其实就是一个 `wire`：

1. 输入 `d` 出现上升沿后，经过 `[l^\uparrow, u^\uparrow]` 的延时，输出 `o` 才能出现上升沿。
2. 自动机用一个局部时钟 `c` 记录“从输入变化到现在已过多久”。
3. 位置 invariant 用 `c \le u^\uparrow` 限定最迟传播时刻，离开边 guard 用 `c \ge l^\uparrow` 限定最早传播时刻。
4. 如果把 `l^\uparrow, u^\uparrow` 都当成参数而不是常数，就得到最小的参数化定时元件模型。

通俗地说，这篇论文像是在问：“芯片内部每根线和每个锁存器到底能慢到什么程度，datasheet 还能不失真？”`PTA` 的作用就是把这个问题从手工猜 critical path 变成符号推导。

### 运行 / 接受 / 转移语义

整块 `SPSMALL` memory 由输入信号自动机与元件自动机同步组合而成。信号传播通过共享离散迁移同步，例如 `d^\uparrow` 触发 wire automaton 进入中间位置，再在参数约束允许的时间窗内发出 `o^\uparrow`。

两周期写操作的关键结论被整理成两类公式：

$$
\mathrm{Assumption}(D^\uparrow)
$$

$$
\mathrm{Final}(D^\uparrow) : f(l,u) \le t_{CK \to Q^\uparrow}^{D^\uparrow,WEN^\downarrow} \le g(l,u)
$$

它们的意义分别是：

1. `Assumption` 约束外部 setup / cycle 参数和内部延时参数之间必须满足什么关系；
2. `Final` 约束在这些前提下，真实写响应时间会落在哪个参数化区间内。

### 语义边界

这篇论文也清楚暴露了 `PTA` 路线的边界：

1. 完整模型的参数很多，原文一开始就有 `34` 个参数，直接整体 reachability 不可行。
2. 因此作者必须把电路切成三段分别分析再组合。
3. 工具假设主要是线性参数约束和多面体可达集表示。
4. 它适合 timing-constraint synthesis，不直接处理复杂功能逻辑或非线性电路动态。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 参数化模型骨架 | `$M = (L, l_0, C, P, E, Inv)$` | 把元件延时从常数提升为参数。 |
| 时间步 | `$(l, v) \xrightarrow{t} (l, v+t)$` | 在 invariant 内进行连续时间流逝。 |
| 结果约束 | `$\mathrm{Final}(D^\uparrow): f(l,u) \le t \le g(l,u)$` | reachability 输出的是响应时间参数区间。 |
| 写时序上界 | `$u_3^\downarrow + u_{15}^\downarrow + u_8^\downarrow + \max\{u_7^\uparrow, u_7^\downarrow\} \le twrite_{max}$` | 给出 datasheet 写响应时间成立的充分条件。 |
| 结构化求解 | `$\mathrm{Assumption}(D^\uparrow)$` | 通过逐步 refinement 消去 bad states。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | wire、latch、输入信号都被压成显式位置。 |
| 事件 / 触发 | 强支持 | 上升沿/下降沿传播是核心离散事件。 |
| 守卫 / 数据 | 强支持 | guard、不变式和参数化上下界是主体。 |
| 层次 | 不支持 | 主要是平面元件组合。 |
| 并发 / 同步 | 强支持 | 元件间通过共享离散信号同步。 |
| 时间约束 | 强支持 | 参数化传播延时和 setup/cycle 约束就是核心。 |
| 连续动态 / 随机性 | 不支持 | 不建模物理电流方程本身，只建模时序抽象。 |
| 可执行 / 可验证性 | 强验证 | `HYTECH` 可进行参数化符号可达性分析。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先识别 write/read 路径上的关键 wire、latch 和输入信号。
2. 为每类元件建立局部 timed automaton。
3. 把传播延时写成参数上下界，而不是定值。
4. 通过 `HYTECH` 分析两周期写操作的可达状态并抽取线性约束。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. wire automaton 与 latch automaton。
2. 参数化 guard / invariant。
3. 全局时钟 `s` 与观测标志 `Q`。
4. `Assumption / Final` 形式的多面体约束。

### 交换与互操作

互操作重点在：

1. 从电路元件级描述到 timed automata 的抽象映射；
2. 从 reachability 结果回写到 datasheet 参数不等式；
3. 与 `HSIM` 仿真结果做数值对照验证。

## 配套基础设施

- 建模/编辑工具：原文主要依赖数学建模和 `HYTECH` 输入模型。
- 解析/交换/元模型支持：无统一 XML/JSON；核心是参数化 automata 与线性约束。
- 仿真/执行支持：工程对照侧使用 `HSIM` 进行电路仿真。
- 验证/分析支持：`HYTECH` 多面体 reachability analysis。
- 代码生成/转换支持：支持从局部电路元件结构转换到 automata 组合模型。
- 标准化或社区生态：属于 `Timed Automata` 的参数综合分支，生态更接近 `HYTECH/IMITATOR` 路线而非通用交换格式。

## 适用场景与需求前提

### 适用场景

适合 memory circuit、asynchronous circuit、embedded timing path 分析，以及那些“内部传播延时未知但有约束区间”的时序验证问题。

### 需求前提

1. 关键元件和关键路径必须可抽象为有限 automata。
2. 延时不确定性需要能写成线性上下界参数。
3. 主要问题是 response time / setup timing，而不是复杂功能 correctness。
4. 系统规模需要允许分段分析与约束重组。

### 不适用或高成本场景

若系统依赖强非线性电路行为、连续电流细节或大规模全芯片整体分析，这条 `PTA + HYTECH` 路线会很快失控。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文不是新增时钟语义，而是把延时常数参数化，从而稳定补出了 `Parametric Timed Automata` 分支；相对 [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)，这里增加的是参数维度而不是冻结时钟；相对 [Timed-automata based schedulability analysis for distributed firm real-time systems: a case study](../timed-automata-based-schedulability-analysis-for-distributed-firm-real-time-systems-a-case-study/desc.md)，本文做的是符号参数约束提取，而不是对给定点参数做 point-wise feasibility analysis。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文非常适合 `project_1` 中“从需求抽时序，再推模型参数边界”的路线，因为它直接展示了如何把文本式 datasheet 约束回写成形式模型上的参数空间。

### 作为目标形式主义还是中间表示

对存在不确定时延、平台未定或需要参数综合的场景，它可以直接作为目标形式主义；对一般控制需求，它更常作为高保真中间验证表示。

### 对需求到模型生成的启发

1. 需求抽取时要显式标出“未知但有上下界”的时间量。
2. 若文本里反复出现 setup / hold / response time，这些更适合参数而不是常数。
3. 输出不一定非得是单个模型，也可以是“模型 + 可行参数区域”。

### 现实限制

参数化建模会迅速放大状态空间，因此自动化管线必须优先做分解、剪枝和关键路径识别。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文的所有时钟与位置语义都建立在经典 `TA` 上。
- `Verification of timed circuits with symbolic delays`：原文直接承接这类参数化时延分析思路。
- `UPPAAL in a Nutshell` 与 `KRONOS`：原文把它们作为实时时序验证工具线背景，实际求解则选用 `HYTECH`。

## 文献分类总结

- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 形式主义：`Parametric Timed Automata / HYTECH Memory-Circuit Model`
- 论文角色：参数化时序验证 / `Parametric Timed Automata` 分支代表应用条目
- 核心功能：从 memory circuit 的参数化 timed model 中综合 datasheet 约束
- 关键特性：参数化传播延时、wire/latch automata、symbolic reachability、线性约束提取
- 构造方式：元件级 automata 建模 + 参数化 guard/invariant + 分段 reachability refinement
- 基础设施：`HYTECH`、`HSIM`，原文未提供公开仓库
- 适用场景：存储电路与异步时序路径验证
- 需求前提：延时不确定性需可写成线性参数上下界，关键路径需可结构化抽取
- 状态：🟢

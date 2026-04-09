# Tempo：Timed Input/Output Automata 形式化工具箱 / Tempo: A Toolkit for The Timed Input/Output Automata Formalism

## 基本信息

- 标题：Tempo: A Toolkit for The Timed Input/Output Automata Formalism
- 中文标题：Tempo：Timed Input/Output Automata 形式化工具箱
- 作者：Nancy Lynch，Laurent Michel，Alexander A. Shvartsman
- 发表：*Proceedings of the First International ICST Conference on Simulation Tools and Techniques for Communications, Networks and Systems*，2008
- DOI：`10.4108/ICST.SIMUTOOLS2008.3105`
- 链接：https://groups.csail.mit.edu/tds/papers/Lynch/simulationworks.pdf
- 形式主义：`Tempo / Timed Input/Output Automata (TIOA)`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：TIOA language + integrated toolkit
- 工具/实现获取方式：原文明确说明 `Tempo Toolkit` 的 `Linux / Windows / Mac OS X` beta releases 可从 `www.veromodo.com` 下载。
- 标准/格式获取方式：承载方式是 `Tempo` 语言规范文件，配套 `Uppaal` 与 `PVS` 翻译模块；原文未给独立于 Tempo 的中立交换标准。

## 简报

这篇论文的价值不只是“给 `Timed I/O Automata` 配一个 simulator”，而是把 `TIOA` 从理论形式主义推进成一门可写、可调试、可翻译、可做 paired simulation 的语言与 IDE。`Tempo` 显式支持 vocabulary、signature、states、transitions、trajectories、invariants、schedules、simulate blocks，以及到 `Uppaal` 和 `PVS` 的桥接。

- 形式主义定位：基于 `Timed Input/Output Automata` 的专用建模语言与工具链，而不是单纯的 timed-interface 理论综述。
- 构造方式简述：用 `Tempo` 文本语言描述 automaton 的 actions、state、transitions 与 trajectories，再借助 simulator、static analysis、`Uppaal` 翻译和 `PVS` 翻译验证行为。
- 基础设施与场景简述：依托 `Tempo` 语言、IDE、debugger-like simulator、paired simulation 和 `Uppaal/PVS` adapters，服务 distributed / concurrent / timed systems 的规格化与验证。

```text
TIOA idea -> Tempo language specification -> simulator / schedule / paired simulation -> Uppaal / PVS / theorem-backed analysis
```

## 形式主义定义与核心对象

### 定义对象

论文把 `Tempo` 的建模对象固定为一类带时间的 I/O automata：

1. 输入、输出、内部动作签名。
2. 离散状态变量。
3. 离散转移。
4. trajectories，即离散步之间的连续时间演化。
5. invariants、simulation relations 与 schedules。

### 核心抽象

结合论文对 language constructs 的描述，可把一个 `Tempo` automaton 保守写成：

$$
\mathcal{A} = (\Sigma_{in}, \Sigma_{out}, \Sigma_{int}, X, \Theta, D, \mathcal{T})
$$

上式中的符号逐项解释如下：

1. `\Sigma_{in}`、`\Sigma_{out}`、`\Sigma_{int}` 分别是输入、输出、内部动作集合。
2. `X` 是状态变量集合。
3. `\Theta` 是初始状态条件。
4. `D` 是离散 transitions 集合。
5. `\mathcal{T}` 是 trajectories 集合。

论文中 `Fischer` 例子最关键的 trajectory 约束写成：

$$
\dot{now} = 1
$$

并且存在 stop condition：

$$
\exists i : process.\ now = lastset[i]
$$

上式中的符号逐项解释如下：

1. `now` 是当前时间变量。
2. `lastset[i]` 是与 process `i` 相关的 deadline。
3. 该约束表示时间可以流逝，但不能越过当前生效 deadline。

论文还给出典型 invariant：

$$
\forall i \neq j.\ pc[i] \neq pccrit \lor pc[j] \neq pccrit
$$

上式中的符号逐项解释如下：

1. `pc[i]` 是 process `i` 的 program counter。
2. `pccrit` 表示处于 critical section。
3. 该不变式就是 Fischer mutual exclusion 的形式化表达。

### 一个最小例子与通俗解释

论文整篇围绕 Fischer timed mutual exclusion 做展示，这个例子非常适合说明 `Tempo`：

1. 每个 process 都是一个带 program counter 的 timed I/O behavior。
2. `Tempo` 允许把 shared variable `turn`、时间变量 `now`、deadline 变量 `lastset` 一起写进状态。
3. discrete transitions 负责 `try/test/set/check/crit/exit` 等动作。
4. trajectories 负责“时间如何流逝”以及“何时必须停下来执行离散动作”。

通俗地说，`Tempo` 像“给 TIOA 写代码的语言”。它既保留了 automata 的严谨骨架，也提供了程序员能读懂的结构化文本语法和调试式 simulator。

### 运行 / 接受 / 转移语义

论文最强调的就是 `Tempo` 对离散和连续两种演化都显式建模：

1. `transitions` 描述 discrete actions。
2. `trajectories` 描述离散步之间允许的时间演化。
3. `schedules` 用来解析 simulator 中的 nondeterminism。

对 paired simulation，论文给出关系 `R(s,u)` 来驱动高层 / 低层 automata 的联动执行，可保守写成：

$$
R(s, u)
$$

上式中的符号逐项解释如下：

1. `s` 是高层 automaton 的状态。
2. `u` 是低层 automaton 的状态。
3. `R` 是两者之间的 simulation relation。
4. simulator 可据此驱动“实现是否跟得上抽象规格”的配对执行。

### 语义边界

这篇论文的边界也很清楚：

1. `Tempo` 语言本身表达力很强，但并非所有自动化后端都能处理其全部子语言。
2. `Uppaal` 与 `PVS` 翻译模块各自只覆盖适合自身的子集。
3. simulator 通过 schedules 解决 nondeterminism，并不意味着语言本体变成 deterministic。
4. 它更适合 distributed / timed interaction 建模，不直接服务连续 ODE 控制。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 语言骨架 | `$\mathcal{A} = (\Sigma_{in}, \Sigma_{out}, \Sigma_{int}, X, \Theta, D, \mathcal{T})$` | `Tempo` 中一个 automaton 的核心对象。 |
| 时间流逝 | `$\dot{now} = 1$` | trajectory 中时间变量的连续演化。 |
| 轨迹停止条件 | `$\exists i : process.\ now = lastset[i]$` | 不能越过 deadline。 |
| 互斥不变式 | `$\forall i \neq j.\ pc[i] \neq pccrit \lor pc[j] \neq pccrit$` | Fischer 例子的 safety property。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 状态变量与 program counters 是核心。 |
| 事件 / 触发 | 很强 | input/output/internal actions 明确分层。 |
| 守卫 / 数据 | 强支持 | precondition、effect 与 typed state variables 均可表达。 |
| 层次 | 弱支持 | 重点不是 hierarchy，而是 composition / abstraction。 |
| 并发 / 同步 | 很强 | 面向 distributed / concurrent systems。 |
| 时间约束 | 很强 | trajectories、deadlines、timeouts 是语言一等对象。 |
| 连续动态 / 随机性 | 弱连续 / 不随机 | 主要是时间轨迹，不是一般混成 ODE；不讨论概率。 |
| 可执行 / 可验证性 | 很强 | simulator、paired simulation、`Uppaal` 与 `PVS` 翻译都具备。 |

### 形式化问题与性质

1. `Tempo` 的核心不是单个 tool，而是“语言 + simulator + formal-backend bridge”的完整链路。
2. schedules 机制说明它非常重视“如何具体执行一个 nondeterministic timed model”。
3. paired simulation 把 abstraction relation 直接做进 simulator，这是很多普通 DSL 没有的能力。

## 构造方式与承载格式

### 建模入口

论文中的典型入口是：

1. 写 vocabulary / types。
2. 写 automaton signature。
3. 定义 states、transitions、trajectories。
4. 追加 invariants、schedules、simulate blocks。
5. 选择 simulator、`Uppaal` 或 `PVS` 后端。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Tempo` 文本语言文件。
2. simulator schedules。
3. `Uppaal` translation。
4. `PVS` translation。

### 交换与互操作

这篇论文的互操作主要体现在：

1. `Tempo -> Uppaal`。
2. `Tempo -> PVS`。
3. paired simulation 用 relation 把 high-level / low-level specs 连在一起。

## 配套基础设施

- 建模/编辑工具：`Tempo` IDE 与文本编辑器工作流。
- 解析/交换/元模型支持：compiler 做 syntax 与 static semantic analysis；无中立交换标准。
- 仿真/执行支持：simulator、schedules、paired simulation。
- 验证/分析支持：invariant checking、`Uppaal` model checking、`PVS` theorem proving。
- 代码生成/转换支持：论文提到未来考虑 distributed code generation，但当前主线仍是验证。
- 标准化或社区生态：`VeroModo` 发行、`Eclipse Rich Client Platform` GUI、`Uppaal/PVS` adapters 构成主要生态。

## 适用场景与需求前提

### 适用场景

适合 distributed algorithms、communication protocols、embedded timed interaction systems，以及需要同时保留 abstraction relation 与 timed behavior 的规格化场景。

### 需求前提

1. 系统需能表达成 input/output/internal action 结构。
2. 时间要求主要表现为 trajectories、timeouts、deadlines，而不是连续物理动力学。
3. 团队愿意以 formal specification 语言而非普通代码来描述系统。
4. 若要自动验证，模型还要落在 `Uppaal` 或 `PVS` 对应可处理子集内。

### 不适用或高成本场景

如果系统核心是连续控制、Petri 网资源流，或者团队只想要轻量事件状态图，`Tempo` 会偏重。

## 与相邻形式主义的关系

相对 [the-theory-of-timed-input-output-automata/desc.md](../the-theory-of-timed-input-output-automata/desc.md)，`Tempo` 是语言与工具化落地；相对 [an-introduction-to-input-output-automata/desc.md](../an-introduction-to-input-output-automata/desc.md)，它是在 I/O automata 上显式补时间与开发环境；相对 [on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md](../on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md)，它更偏 timed I/O specification language，而不是 modal interface workbench。

## 与本研究的关系

### 对 Project 1 的价值

它证明了接口/交互导向的 timed state-machine family 不必只停留在理论层，也可以落成带 simulator、debugger 和 formal backend bridge 的工程化语言。

### 作为目标形式主义还是中间表示

对 distributed / protocol-like timed systems，它可以是直接目标语言；对一般控制系统，更像某类交互抽象的中间表示。

### 对需求到模型生成的启发

1. 如果后续生成目标是交互式 timed model，必须显式区分输入、输出、内部动作。
2. 时间演化不一定非要压成 clocks + guards，也可以像 `Tempo` 一样通过 trajectories 单独建模。
3. abstraction relation 若想进入闭环验证，最好在语言层就有位置，而不是事后人工补。

### 现实限制

`Tempo` 很强，但它对形式化规格撰写能力和后端子集约束都有要求，不是轻量级状态图编辑器。

## 重要的相关工作

- [the-theory-of-timed-input-output-automata/desc.md](../the-theory-of-timed-input-output-automata/desc.md)：`TIOA` 的理论母线。
- [an-introduction-to-input-output-automata/desc.md](../an-introduction-to-input-output-automata/desc.md)：`I/O Automata` 的无时间基础骨架。
- [on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md](../on-weak-modal-compatibility-refinement-and-the-mio-workbench/desc.md)：接口理论 workbench 路线。
- [interface-automata/desc.md](../interface-automata/desc.md)：更偏接口组合与兼容性的模型本体。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`Tempo / Timed Input/Output Automata (TIOA)`
- 论文角色：TIOA language + integrated toolkit

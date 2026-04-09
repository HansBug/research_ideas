# UPPAAL 教程 / A Tutorial on Uppaal

## 基本信息

- 标题：A Tutorial on Uppaal
- 中文标题：UPPAAL 教程
- 作者：Gerd Behrmann，Alexandre David，Kim G. Larsen
- 发表：*Formal Methods for the Design of Real-Time Systems*，LNCS 3185，pp. 200-236，2004
- DOI：`10.1007/978-3-540-30080-9_7`
- 链接：https://doi.org/10.1007/978-3-540-30080-9_7
- 形式主义：`Timed Automata / UPPAAL Network`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：工具教程 / verification toolbox
- 工具/实现获取方式：原文明确给出 `UPPAAL` 工具主页 `http://www.uppaal.com/`，并说明工具由 Aalborg University 与 Uppsala University 联合开发，GUI 以 `Java` 实现、验证引擎以 `C++` 实现。
- 标准/格式获取方式：承载方式是 `UPPAAL` templates、全局/局部 declarations、locations、edges、guards、invariants、channels 与查询语言；原文未提供独立于 `UPPAAL` 的中立交换标准。

## 简报

这篇论文的价值不在于重新提出 `Timed Automata`，而在于把 `UPPAAL` 这一条最成熟的工程工具线讲清楚。它一方面收束了工具实际支持的 timed-automata 口径，例如整数变量、urgent/committed locations、binary/broadcast channels 和 `CTL` 子集查询；另一方面又给出 train-gate、Fischer protocol 等可直接复用的建模模式，所以它更像“把定时自动机真正变成可操作工程载体”的稳定入口。

- 形式主义定位：面向 `Timed Automata` 建模、仿真与模型检查的经典工具教程，而不是新的时间自动机理论。
- 构造方式简述：把系统拆成多个 templates，声明 clocks / integers / channels，用 locations、guards、resets 和 invariants 描述行为，再用 `A[] / E<>` 一类查询式验证性质。
- 基础设施与场景简述：依托 editor、simulator、verifier 三个核心界面，以及 symbolic zone-based engine，服务协议分析、实时控制、嵌入式调度与模型驱动测试前端。

```text
实时需求 -> timed automata templates -> network + declarations + queries -> simulator / verifier -> counterexample or proof
```

## 形式主义定义与核心对象

### 定义对象

原文围绕以下对象组织 `UPPAAL`：

1. 单个 timed automaton。
2. 由多个 automata 组成的 network。
3. 时钟约束、整数变量与同步通道。
4. urgent / committed locations。
5. `CTL` 子集风格的查询语言。

### 核心抽象

论文直接给出了 `UPPAAL` 所采用的 timed automaton 形式：

$$
A = (L, l_0, C, Act, E, Inv)
$$

上式中的符号逐项解释如下：

1. `L` 是 location 集合。
2. `l_0` 是初始 location。
3. `C` 是 clocks 集合。
4. `Act` 是 actions、co-actions 与内部 `\tau` 动作集合。
5. `E` 是边集合。
6. `Inv` 为每个 location 指派 invariant。

其中边集合满足：

$$
E \subseteq L \times Act \times B(C) \times 2^C \times L
$$

上式中的符号逐项解释如下：

1. `B(C)` 是由 clocks 组成的 guard 约束集合。
2. `2^C` 表示本次跳转要 reset 的 clocks 子集。
3. 一条边由源 location、动作、guard、reset 集合和目标 location 组成。

对多个 automata，论文把系统语义整理成一个转移系统：

$$
\llbracket N \rrbracket = (S, s_0, \rightarrow)
$$

上式中的符号逐项解释如下：

1. `N = A_1 \parallel \cdots \parallel A_n` 表示 automata network。
2. `S` 是所有可达全局状态的集合。
3. `s_0` 是由所有 template 初始 location 与初始 clock valuation 组成的初始状态。
4. `\rightarrow` 同时覆盖 delay steps 与 action/synchronisation steps。

### 一个最小例子与通俗解释

论文一开始就用一个非常适合入门的 lamp example：

1. `Lamp` automaton 只有 `off / low / bright` 三个位置。
2. `User` automaton 随机发送 `press!`。
3. `Lamp` 通过 clock `y` 区分“第二次按键是否足够快”，再决定是否进入 `bright`。
4. 把两个 automata 并起来后，就能直接检查“快速双击是否一定可达 bright”等性质。

通俗地说，`UPPAAL` 里的模型就像“会计时的并发状态机网络”：每个局部状态机各自演化，但所有 clocks 同步流逝，只有 guard、invariant 和 synchronisation 允许的动作才能发生。

### 运行 / 接受 / 转移语义

论文把单个 timed automaton 的语义写成由 location 与 clock valuation 构成的状态：

$$
(l, u) \xrightarrow{a} (l', u[r := 0])
$$

上式中的符号逐项解释如下：

1. `l` 与 `l'` 分别是源和目标 location。
2. `u` 是当前的 clock valuation。
3. `a` 是执行的动作或同步动作。
4. `r` 是本次跳转被 reset 的 clock 集合。
5. 该跳转要求当前 valuation 满足 guard，且目标 location 的 invariant 可被满足。

对时间流逝，语义可保守写成：

$$
(\bar{l}, u) \xrightarrow{d} (\bar{l}, u + d)
$$

上式中的符号逐项解释如下：

1. `\bar{l}` 是 network 的 location vector。
2. `d \in \mathbb{R}_{\ge 0}` 是流逝的时间。
3. `u + d` 表示所有 clocks 同步前进 `d`。
4. 时间步必须始终保持当前 active locations 的 invariants 成立。

论文还系统说明了 `UPPAAL` 的四类核心查询：

$$
A[]\ \varphi,\quad E<>\ \varphi,\quad E[]\ \varphi,\quad A<>\ \varphi
$$

上式中的符号逐项解释如下：

1. `A[] \varphi` 表示所有路径上始终满足 `\varphi`。
2. `E<> \varphi` 表示存在一条路径最终到达满足 `\varphi` 的状态。
3. `E[] \varphi` 表示存在一条路径始终满足 `\varphi`。
4. `A<> \varphi` 表示所有路径最终都会到达满足 `\varphi` 的状态。

### 语义边界

`UPPAAL` 的口径也很明确：

1. 主体是 `Timed Automata` network，而不是一般混成系统。
2. 数据支持主要是 bounded integers、arrays 与 structured data types，不是任意无限数据。
3. 查询语言是 `CTL` 子集，而不是完整时序逻辑超集。
4. 连续动力学若超出 clocks 与离散变量的表达能力，就必须另行抽象。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单个 TA 骨架 | `$A = (L, l_0, C, Act, E, Inv)$` | 固定 `UPPAAL` 中单个 automaton 的核心对象。 |
| 边定义 | `$E \subseteq L \times Act \times B(C) \times 2^C \times L$` | 每条边同时携带 action、guard 与 reset 集合。 |
| network 语义 | `$\llbracket N \rrbracket = (S, s_0, \rightarrow)$` | 多 template 系统最终被解释为一个全局转移系统。 |
| 离散跳转 | `$(l, u) \xrightarrow{a} (l', u[r := 0])$` | guard 成立时执行动作并 reset clocks。 |
| 时间流逝 | `$(\bar{l}, u) \xrightarrow{d} (\bar{l}, u + d)$` | 所有 clocks 同步流逝，且 invariants 始终为真。 |
| 查询语义 | `$A[]\ \varphi,\ E<>\ \varphi,\ E[]\ \varphi,\ A<>\ \varphi$` | 固定 `UPPAAL` 最常用的性质表达方式。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | location / template / network 是工具主骨架。 |
| 事件 / 触发 | 强支持 | binary/broadcast channels 与 guards 共同驱动跳转。 |
| 守卫 / 数据 | 强支持 | clocks、bounded integers、arrays 和 expressions 都可进 guard/update。 |
| 层次 | 弱支持 | 论文主体是平铺 templates，不直接提供层次状态机语法。 |
| 并发 / 同步 | 很强 | network semantics 与 channels 是核心。 |
| 时间约束 | 很强 | invariants、guards、urgency 与 delay semantics 都以 clocks 为中心。 |
| 连续动态 / 随机性 | 不支持 | 连续微分方程与概率不在本文主线。 |
| 可执行 / 可验证性 | 很强 | editor、simulator、verifier 三位一体。 |

### 形式化问题与性质

1. `UPPAAL` 不是只接受理论定义，而是收束出一套可编辑、可仿真、可验证的 timed-automata 口径。
2. urgent/committed locations 说明它对工程建模很重视，而不只是 textbook TA。
3. query language 的刻意收束换来了高可用的自动验证体验。
4. 论文末尾的 modeling patterns 让它不只是工具介绍，还成为后续建模实践的模式库。

## 构造方式与承载格式

### 建模入口

原文中的典型建模入口是：

1. 声明全局/局部 clocks、variables 与 channels。
2. 为每个 process/template 画 locations、edges 与 labels。
3. 通过 parameters 与 multiple instantiation 形成 network。
4. 再写查询语句检查 reachability / safety / liveness。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UPPAAL` template 模型。
2. declarations 区中的 clock、integer、array 与 channel 声明。
3. locations 上的 invariants 与 urgent/committed 标记。
4. verifier 所消费的查询表达式。

### 交换与互操作

这篇论文的互操作重点不是开放交换标准，而是：

1. editor、simulator、verifier 共用同一模型。
2. counterexample 可以直接回灌到 simulator。
3. 建模模式和 queries 可以复用于 testing、scheduling、protocol verification 等多类任务。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` editor。
- 解析/交换/元模型支持：`UPPAAL` 模型、templates、declarations 与 queries 共用统一内部表示；原文未提供中立交换标准。
- 仿真/执行支持：simulator 支持 symbolic / random / guided simulation。
- 验证/分析支持：verifier 支持 reachability、invariance、liveness 风格查询。
- 代码生成/转换支持：这篇教程不以代码生成见长，重点是 verification-oriented modeling。
- 标准化或社区生态：`UPPAAL` 已形成持续演化的大学与工具社区生态，是 timed automata 最稳定的工具主线之一。

## 适用场景与需求前提

### 适用场景

适合协议、实时控制器、调度器、嵌入式软件和需要显式 timing guards / deadlines 的离散反应式系统。

### 需求前提

1. 系统主要行为可抽象为有限 modes + clocks + discrete variables。
2. 关键 correctness 目标能写成 reachability、invariance 或 eventuality 一类查询。
3. 连续部分若存在，必须先被离散化到 clocks/guards 层面。
4. 工程团队能接受显式的 template + query 建模方式。

### 不适用或高成本场景

如果系统核心是复杂连续动力学、富数据结构语义或需要完整开放交换标准，直接用本文这套 `UPPAAL` 口径会比较吃力。

## 与相邻形式主义的关系

相对 [Timed Automata](../a-theory-of-timed-automata/desc.md) 等模型本体条目，这篇论文讲的是工具落地；相对 [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md) 这类后续 `UPPAAL` 分支工作，它更像共同母线；相对 `IMITATOR`，它强调固定参数下的 verification，而不是参数综合。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文直接说明：如果 `project_1` 最终希望把 LLM 生成的状态机接到成熟验证链路，`UPPAAL` 是最值得优先兼容的 timed-automata 基础设施之一。

### 作为目标形式主义还是中间表示

对实时验证任务，它可以直接作为目标形式主义；对更一般的需求到模型工作流，它也很适合做“可验证的中间表示”。

### 对需求到模型生成的启发

1. 生成的状态机若想进入验证器，必须把 clocks、guards、invariants 和同步动作显式结构化。
2. 查询语言设计不能过度贪大，稳定、可自动化比理论完备更重要。
3. 建模模式库很关键，后续 LLM 生成不应只生成语法，还应对齐成熟 pattern。

### 现实限制

`UPPAAL` 的成功也提醒我们：高可用工具链往往建立在“刻意收束”的语言设计上。若生成的中间表示过于宽泛，反而不利于接上成熟 verifier。

## 重要的相关工作

- [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)：代表 `Timed Automata` 族的模型本体母线。
- [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)：展示 `UPPAAL` 工具线如何延伸到在线测试。
- [imitator-ii-a-tool-for-solving-the-good-parameters-problem-in-timed-automata/desc.md](../imitator-ii-a-tool-for-solving-the-good-parameters-problem-in-timed-automata/desc.md)：与本文同属时间自动机工具线，但聚焦参数综合而非固定模型验证。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / UPPAAL Network`
- 论文角色：工具教程 / verification toolbox

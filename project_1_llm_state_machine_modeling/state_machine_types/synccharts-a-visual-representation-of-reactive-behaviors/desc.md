# SyncCharts：反应式行为的可视化表示 / SyncCharts: A Visual Representation of Reactive Behaviors

## 基本信息

- 标题：SyncCharts: A Visual Representation of Reactive Behaviors
- 中文标题：SyncCharts：反应式行为的可视化表示
- 作者：Charles Andre
- 发表：I3S Technical Report RR 95-52, revision RR 96-56, 1996
- DOI：原文未提供
- 链接：http://www-sop.inria.fr/members/Charles.Andre/CA%20Publis/SYNCCHARTS/overview.html
- 形式主义：SyncCharts
- 主类：📦
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：图形语言
- 工具/实现获取方式：原文明确说明任意 `SyncCharts` 都可自动翻译为等价 `Esterel` 程序，但未附独立下载工具包。
- 标准/格式获取方式：核心承载是 `SyncCharts` 的图形语法，以及与 `Esterel` 模块之间的等价翻译关系；原文未给出 XML/JSON 一类开放交换格式。

## 简报

`SyncCharts` 的价值在于把“控制系统里真正高频的 preemption”提升成图形状态机的一等公民。它延续 `Statecharts` 的层次和并行表示、吸收 `Argos` 的同步语义，同时把强中止、弱中止、挂起、本地信号和正常终止这些细节做成了明确的语法原语，并允许直接翻译到 `Esterel`。

- 形式主义定位：面向实时/反应式控制逻辑的同步图形状态机语言。
- 构造方式简述：用 macrostate、constellation、star 和带 trigger/effect 的 arcs 描述层次、并行与 preemption。
- 基础设施与场景简述：以同步语义为底座，可自动翻译到 `Esterel`，适合控制导向和中断驱动的反应式系统。

```text
反应式控制需求 -> SyncCharts stars / macrostates -> 同步 instant semantics -> Esterel 程序 / 验证与实现
```

## 形式主义定义与核心对象

### 定义对象

论文要解决的问题不是普通状态切换，而是：

1. 在图形表示里清楚表达强/弱 preemption。
2. 在层次与并行结构中支持本地信号和同步广播。
3. 让图形模型与同步文本语言 `Esterel` 共用同一语义底座。

### 核心抽象

原文把一个 `SyncCharts` 的层次结构写成三类组件组成的树：

$$
T_\Gamma = (M_\Gamma, C_\Gamma, S_\Gamma, \succ)
$$

上式中的符号逐项解释如下：

1. `M_\Gamma` 是 macrostate 集合，对应并行组合边界。
2. `C_\Gamma` 是 constellation 集合，对应一个 `OR` 状态图。
3. `S_\Gamma` 是 star 集合，对应可进入、可被中止的状态节点。
4. `\succ` 是树中的直接后继关系：macrostate 指向 constellations，constellation 指向 stars，star 再指向其 body macrostate。

弧对象被定义为：

$$
a = \langle a_{type}, a_{mod}, a_{trig}, a_{eff} \rangle
$$

其中：

1. `a_{type}` 表示 weak abortion、strong abortion、normal termination、suspension 或 initial。
2. `a_{mod}` 表示 immediate 或 delayed。
3. `a_{trig}` 是触发用的 compound signal。
4. `a_{eff}` 是转移时发射的 effect signals。

语义层面，论文先给出同步反应系统行为映射：

$$
B : I^* \to O^*
$$

其中：

1. `I^*` 是输入事件历史。
2. `O^*` 是输出事件历史。
3. `B` 表示从输入历史到输出历史的确定性行为函数。

进一步，内部过程的单步反应写成：

$$
p \xrightarrow{I/O} p'
$$

这里：

1. `p` 是当前过程。
2. `I` 是当前 instant 的输入事件集合。
3. `O` 是该 instant 发射的输出事件集合。
4. `p'` 是下一个 instant 继续执行的剩余过程。

### 一个最小例子与通俗解释

论文最早的例子就是 `SR` 触发器：

1. 两个状态 `OFF` 和 `ON`。
2. 输入信号是 `set` 与 `reset`。
3. 活动状态在每个 instant 持续发射对应输出信号 `OFF` 或 `ON`。
4. 若希望 `set` 具有更高优先级，则用 immediate/strong preemption 画出从 `OFF` 到 `ON` 的切换。

通俗解释是：`SyncCharts` 不只是“画状态圆圈和箭头”，而是在说“本 instant 到底先停谁、谁还能执行这一下、哪些本地信号会在同一 instant 继续触发后续切换”。

### 运行 / 接受 / 转移语义

`SyncCharts` 的核心假设是 perfect synchrony：刺激与反应在同一逻辑 instant 发生，信息可瞬时广播。

对 trigger 的求值，论文把复合信号 `\sigma` 在事件 `e` 下的真假写成：

$$
e \models \sigma \iff \llbracket \sigma \rrbracket_e = \mathrm{tt}
$$

上式中的符号逐项解释如下：

1. `e` 是当前 instant 中出现的信号集合。
2. `\sigma` 是由信号、合取、析取、否定构成的 compound signal。
3. `\llbracket \sigma \rrbracket_e` 是在 `e` 下对 `\sigma` 的布尔求值。

在过程层，strong/weak preemption 的区别是：

1. strong abortion 会在当前 instant 的主体执行前剥夺执行权。
2. weak abortion 会让主体在当前 instant 先执行完，再在 instant 末尾被中止。
3. suspension 则冻结当前过程，等待后续恢复。

### 语义边界

`SyncCharts` 采用的不是物理时间语义，而是同步逻辑时间：

1. 它天然适合事件驱动、抢占密集的控制系统。
2. 它不直接表达连续动力学。
3. 它依赖同步假设，因此与异步消息系统的建模直觉不同。

### 关键性质与判定边界

原文最重要的工程性质包括：

1. preemption 被语法化区分为 strong / weak / suspension，不再靠口头约定解释。
2. parallel constellations 通过 macrostate 同步组合，正常终止需要各分支都到 final stars。
3. 图形模型可系统翻译成等价 `Esterel` 程序，从而复用同步语言的工具链。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | star 是核心状态节点，状态中可持续发射输出。 |
| 事件 / 触发 | 强支持 | compound signals 和 local signals 是主触发机制。 |
| 守卫 / 数据 | 部分支持 | 主要以信号组合为中心，不强调复杂数据变量。 |
| 层次 | 强支持 | star 的 body 可以再细化为 macrostate。 |
| 并发 / 同步 | 强支持 | macrostate 内多个 constellations 并行且同步。 |
| 时间约束 | 部分支持 | 支持逻辑 instant 与 immediate/delayed preemption，但不是显式时钟自动机。 |
| 连续动态 / 随机性 | 不支持 | 面向纯同步离散反应式逻辑。 |
| 可执行 / 可验证性 | 强支持 | 可自动翻译到 `Esterel`，便于执行和验证。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 层次骨架 | `$T_\Gamma = (M_\Gamma, C_\Gamma, S_\Gamma, \succ)$` | `SyncCharts` 由 macrostate、constellation、star 三层树结构组成。 |
| 弧对象 | `$a = \langle a_{type}, a_{mod}, a_{trig}, a_{eff} \rangle$` | 一条 arc 同时编码类型、立即/延迟、触发和输出效果。 |
| 行为函数 | `$B : I^* \to O^*$` | 模型把输入事件历史确定地映射成输出事件历史。 |
| 单步反应 | `$p \xrightarrow{I/O} p'$` | 一个逻辑 instant 内，过程接收输入并产生输出后重写为新过程。 |
| trigger 求值 | `$e \models \sigma \iff \llbracket \sigma \rrbracket_e = \mathrm{tt}$` | compound signal 是否满足由当前事件集合决定。 |

## 构造方式与承载格式

### 建模入口

建模入口是 `SyncCharts` 图形记号：star、constellation、macrostate、trigger/effect 标注的 arcs，以及可选的 `Esterel` 文本 refinement。

### 机器可处理承载方式

原文强调双承载：

1. 图形 `SyncCharts` 结构。
2. 可翻译得到的等价 `Esterel` 程序。

### 交换与互操作

论文强调的是“图形到 `Esterel` 的语义互通”，而不是开放交换标准。

## 配套基础设施

- 建模/编辑工具：原文聚焦表示法与语义本身，未描述成熟独立编辑器生态。
- 解析/交换/元模型支持：支持从 `SyncCharts` 自动翻译到 `Esterel`。
- 仿真/执行支持：可通过等价 `Esterel` 程序执行。
- 验证/分析支持：可借助同步语言工具链分析。
- 代码生成/转换支持：主要依赖 `Esterel` 路线。
- 标准化或社区生态：偏研究型，不像 `SCXML` 那样有开放标准组织。

## 适用场景与需求前提

### 适用场景

适合中断驱动、preemption 密集、层次与并行都明显的实时反应式控制逻辑。

### 需求前提

1. 需求可以接受同步逻辑时间假设。
2. 模式切换和抢占规则比复杂数据处理更核心。
3. 希望图形表示和同步文本实现之间可以相互映射。

### 不适用或高成本场景

对数据密集、连续控制律主导或开放异步协议主导的系统，`SyncCharts` 不是最自然的第一选择。

## 与相邻形式主义的关系

相对 `Statecharts`，它把 preemption 语义讲得更硬；相对 `Argos`，它更强调图形表达；相对 `SFC/Grafcet`，它的层次和本地信号更强；相对 `SCXML`，它更像同步语言前端而不是开放交换格式。

## 与本研究的关系

### 对 Project 1 的价值

它说明“控制系统状态机”完全可以不是一般 UML 式状态图，而是强同步、强抢占的专用目标语言。

### 作为目标形式主义还是中间表示

更适合作为反应式控制子系统的目标形式主义，也可作为生成后再落到 `Esterel` 的中间桥梁。

### 对需求到模型生成的启发

当需求文字明显体现“立即抢占、暂停恢复、局部广播、并行子图同步结束”时，`SyncCharts` 比普通平面状态机更贴近语义。

### 现实限制

其生态和交换格式不如现代工业标准成熟，但其 preemption 语义非常值得借鉴。

## 重要的相关工作

### 奠基或前身工作

- `Statecharts`
- `Argos`
- `Esterel`

### 同类型或同家族工作

- `Safe State Machines`
- 同步反应式图形语言

### 标准 / 格式 / 工具链工作

- `Esterel` 编译与验证工具链
- 工业控制中的 `Grafcet` / `SFC`

### 与本研究关系最紧的工作

- 面向抢占型控制需求的专用状态机载体。

## 文献分类总结

- 主类：📦
- 描述客体：🎛️
- 所属领域：⏱️
- 形式主义：SyncCharts
- 论文角色：图形语言
- 核心功能：把同步、层次、并行和 preemption 一起压进统一图形状态机语言。
- 关键特性：strong/weak abortion、suspension、local signals、macrostate hierarchy、`Esterel` translation。
- 构造方式：star / constellation / macrostate 图形结构 + compound-signal arcs + 同步过程语义。

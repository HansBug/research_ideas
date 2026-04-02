# 协调用于机器人任务与系统的 rFSM 状态图 / Coordinating Robotic Tasks and Systems with rFSM Statecharts

## 基本信息

- 标题：Coordinating Robotic Tasks and Systems with rFSM Statecharts
- 中文标题：协调用于机器人任务与系统的 rFSM 状态图
- 作者：Markus Klotzbuecher, Herman Bruyninckx
- 发表：*Journal of Software Engineering for Robotics*, 3(1):28-56, 2012
- DOI：`10.6092/JOSER_2012_03_01_P28`
- 链接：https://aisberg.unibg.it/handle/10446/86206
- 形式主义：`rFSM Statecharts`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：机器人协调 DSL / OROCOS statecharts
- 工具/实现获取方式：原文明确说明提供了 real-time capable 的 `rFSM` reference implementation，并与 `OROCOS/RTT` 宽松集成；论文未给出稳定独立仓库链接。
- 标准/格式获取方式：原文直接给出了 `rFSM` 的 `Ecore` 结构模型、`OCL` 约束、`UML` 风格图形记法和可执行 DSL 语义；没有单独 XML/JSON 标准。

## 简报

这篇论文的核心贡献是把机器人软件里的“协调逻辑”从普通计算组件里剥离出来，单独交给一种受约束的 statechart 方言来表达。作者不是沿用完整 Harel statecharts，而是裁掉了并行状态等在机器人实时系统里容易引入语义歧义的元素，保留 `state / transition / connector` 三个核心对象，并给出一个可执行的 `rFSM` 语义。这样，`rFSM` 成为一种专门面向机器人 coordination 的状态机载体，而不是泛图形建模工具。

- 形式主义定位：面向机器人 coordination 的受限 statechart / DSL，而不是通用大而全 UML 状态机。
- 构造方式简述：用层次 `state`、`transition`、`connector` 组织协调逻辑，以 guard、entry/exit、doactivity 和 internal transition 描述可抢占行为。
- 基础设施与场景简述：依托 `OROCOS/RTT`、可执行 DSL、`Ecore + OCL` 结构约束，服务机器人组件协调与任务切换。

```text
机器人 coordination 需求 -> rFSM statechart -> executable DSL / OROCOS integration -> 运行时 step semantics
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. `state`：可为 leaf state 或 composite state。
2. `transition`：从源节点到目标节点的有向转移。
3. `connector`：用于 initial / junction / entry / exit 语义的统一连接器。
4. `guard`：布尔守卫，用于决定转移是否 enabled。
5. `effect`：转移时执行的 side-effect。
6. `entry` / `exit` actions：进入或离开状态时执行的动作。
7. `doactivity`：状态持续活动期间执行的可中断计算。
8. `internal transition`：不离开当前状态的内部反应。
9. `step`：推进状态机执行的原子操作。
10. `structural priority`：自上而下寻找 enabled transition 的优先级规则。

### 核心抽象

根据原文 “only three model elements: states, transitions and connectors” 的定义，可直接整理 `rFSM` 模型为：

$$
R = (S, C, T, s_{\mathrm{root}})
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合，包含 leaf state 与 composite state。
2. `C` 是 connector 集合，用于 initial / entry / exit / junction 等连接语义。
3. `T` 是转移集合。
4. `s_{\mathrm{root}}` 是根状态，整个 `rFSM` 总在一个顶层状态之内，从而保持可组合性。

原文明确要求一个 well-formed 且 active 的 `rFSM` “exactly one leaf state must be active”，因此其活动配置可写为：

$$
|\mathrm{LeafActive}(R)| \in \{0,1\}
$$

上式中的符号逐项解释如下：

1. `\mathrm{LeafActive}(R)` 是当前处于激活态的叶子状态集合。
2. 正常稳定态下应恰有一个叶子状态处于激活态。
3. 转移过程中短暂允许为 `0`。

论文还把转移建模为带 guard 和 effect 的有向边，因此单个转移可保守写成：

$$
t = (n_{\mathrm{src}}, g_t, a_t, n_{\mathrm{tgt}})
$$

上式中的符号逐项解释如下：

1. `n_{\mathrm{src}}` 与 `n_{\mathrm{tgt}}` 分别是源节点和目标节点。
2. `g_t` 是 Boolean 守卫函数。
3. `a_t` 是转移 effect。
4. 节点 `n` 既可以是状态，也可以是 connector。

### 一个最小例子与通俗解释

论文用 gripper coordination 给了一个很好的最小例子：

1. 初始进入 `opening`，执行 `open_gripper()`。
2. 收到 `e_close` 后转到 `closing`。
3. 如果收到 `e_open`，就从 `closing` 返回 `opening`。
4. 如果在 `closing` 中收到 `e_tactile` 且 `gripper_closed = false`，则进入 `grasping`。
5. 在 `grasping` 中丢失接触或收到释放命令，就退出并重新打开夹爪。

通俗地说，`rFSM` 像“专门给机器人协调逻辑瘦身过的 statechart”：它保留层次、抢占、entry/exit、内部转移这些真正有用的协调语义，但故意不把并行状态那类容易把实时行为搞复杂的元素放进核心模型。

### 运行 / 接受 / 转移语义

论文给出的核心运行语义是：调用一次 `step`，收集当前事件，按 top-down 顺序寻找第一个 enabled transition 并执行。可保守整理为：

$$
\mathrm{step}(R, E) = \mathrm{exec}\bigl(\min_{\prec}\{ t \in T \mid g_t(E)=\mathrm{true} \}\bigr)
$$

上式中的符号逐项解释如下：

1. `E` 是自上次 `step` 以来累计的事件集合。
2. `g_t(E)=\mathrm{true}` 表示转移 `t` 在当前事件与守卫条件下被使能。
3. `\prec` 是 structural priority，对应“源状态越高，优先级越高”的搜索顺序。
4. `\mathrm{exec}` 表示执行选中的转移及其 entry/exit/effect 链路。

对持续活动 `doactivity`，论文采用 codel 级可抢占语义，可保守表示为：

$$
\mathrm{do}(s) = \langle c_1, c_2, \ldots, c_m \rangle
$$

上式中的符号逐项解释如下：

1. `c_i` 是最小不可中断执行单元 `codel`。
2. `doactivity` 可以在 `codel` 边界被安全中断。
3. 这样可避免直接抢占线程带来的非确定性和危险行为。

### 语义边界

`rFSM` 的边界同样很清楚：

1. 它是 coordination statechart，不是完整 UML state machine 的替代品。
2. 它明确排除了 parallel state element，而改用 loosely coupled distributed state machines。
3. 它关注 executable model 和实时友好性，不追求最宽泛的 statechart 表达能力。
4. 它主要用于机器人 coordination，而不是一般业务流程图。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$R = (S, C, T, s_{\mathrm{root}})$` | `rFSM` 核心只保留 states、transitions、connectors。 |
| 活动配置 | `$|\mathrm{LeafActive}(R)| \in \{0,1\}$` | 正常时始终只有一个 leaf state 处于激活态。 |
| 转移对象 | `$t = (n_{\mathrm{src}}, g_t, a_t, n_{\mathrm{tgt}})$` | 每条边由守卫和 effect 控制。 |
| 执行语义 | `$\mathrm{step}(R, E) = \mathrm{exec}(\min_{\prec}\{ t \in T \mid g_t(E) \})$` | 以 structural priority 选择第一个 enabled transition。 |
| 安全中断 | `$\mathrm{do}(s)=\langle c_1,\ldots,c_m \rangle$` | 持续活动在 `codel` 粒度可中断。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | leaf / composite state 是核心模型元素。 |
| 事件 / 触发 | 强支持 | 事件集合由 `step` 收集并触发转移。 |
| 守卫 / 数据 | 强支持 | Boolean guard 是转移使能的核心条件。 |
| 层次 | 强支持 | 通过 composite state 实现层次与可组合性。 |
| 并发 / 同步 | 弱支持 | 明确排除 parallel states，改用分布式 state machines。 |
| 时间约束 | 弱支持 | 可表达 time-events，但不是 timed automata 风格时钟系统。 |
| 连续动态 / 随机性 | 不支持 | 连续控制与概率行为不在核心模型中。 |
| 可执行 / 可验证性 | 强执行、较强结构约束 | 有 executable DSL、`Ecore` 模型和 `OCL` 约束。 |

### 形式化问题与性质

1. `rFSM` 最重要的设计决策是“主动减法”：把在机器人协调里最容易引入实现歧义的并行状态拿掉。
2. top-down `take first` 语义让 transition priority 直接可见，减少大状态图里“到底哪条边先走”的不确定性。
3. 可执行模型统一了 simulation 和 runtime，避免很多“仿真能跑，真机语义不一致”的问题。
4. `Ecore + OCL` 使它不仅是画图语言，也是可约束的机器可处理元模型。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 先识别机器人 coordination concern，而不是把协调逻辑埋进普通组件。
2. 用 hierarchy 把高层协调和局部 mode 划开。
3. 用 transitions + guards + effects 表示事件驱动切换。
4. 用 connectors 组织 composite transitions 和初始入口。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `Ecore` 结构模型。
2. `OCL` 约束。
3. `UML` 风格图形 notation。
4. executable `rFSM` DSL。
5. 与 `OROCOS/RTT` 的运行时集成。

### 交换与互操作

互操作重点在：

1. `rFSM` 自身强调 composability，顶层模型总可嵌入到更大的状态机中。
2. 通过分布式 state machines 而非 parallel states 来实现多组件协同。
3. 与 `OROCOS/RTT` 的 loose integration 说明其目标是进入现有机器人软件栈，而不是自成封闭环境。

## 配套基础设施

- 建模/编辑工具：原文直接给出 `rFSM` reference implementation、图形化 statechart notation 和 `Ecore` 元模型。
- 解析/交换/元模型支持：`Ecore + OCL` 是最明确的机器可处理结构承载。
- 仿真/执行支持：作者强调 simulation 与 real system 统一为 executable model。
- 验证/分析支持：结构约束、transition ownership、initial connector existence 等都通过 `OCL` 给出。
- 代码生成/转换支持：原文更强调 executable DSL 与运行时，而不是面向外部代码生成链。
- 标准化或社区生态：与 `UML`、`SCXML`、`Stateflow` 等相邻模型兼容讨论充分，但 `rFSM` 本身是领域化方言。

## 适用场景与需求前提

### 适用场景

适合机器人组件协调、行为切换、异常恢复、可抢占任务控制，以及需要明确分离 computation 和 coordination 的 `OROCOS/ROS` 类系统。

### 需求前提

1. 系统中确实存在独立的 coordination concern。
2. 行为切换主要由离散事件、守卫和状态层次驱动。
3. 团队接受“多个松耦合状态机协同”，而不是一个巨大的并行状态图。
4. 需要可执行、可约束、实时友好的 statechart 语义。

### 不适用或高成本场景

若问题本身需要显式并发区域、复杂共享变量语义或连续物理演化，则 `rFSM` 会偏弱；它更适合 coordination，而不是全能行为建模。

## 与相邻形式主义的关系

相对 Harel statecharts，`rFSM` 更克制，主动移除了 parallel states；相对 UML State Machines，它减少了 variation points；相对 `SCXML` 或 `Stateflow` 这类更宽泛的工业载体，它更聚焦机器人 coordination 和 executable semantics；相对 `SMACH/FlexBE` 这类运行时库，它更强调语义最小核与结构约束。

## 与本研究的关系

### 对 Project 1 的价值

`rFSM` 非常直接地服务 `project_1`：它告诉我们，面向机器人控制系统时，目标状态机不一定要追求最大表达力，反而应该优先保留对 coordination 最关键的语义核。

### 作为目标形式主义还是中间表示

`rFSM` 既可以作为机器人协调任务的目标形式主义，也可以作为更复杂运行时框架下的中间协调表示。

### 对需求到模型生成的启发

1. 需求抽取时要显式区分 computation 与 coordination。
2. 对机器人任务，层次、可抢占、entry/exit 和内部转移比 parallel states 更常构成第一优先级。
3. 自动生成状态机时，结构约束和执行语义必须一起生成，不能只生成图。

## 重要的相关工作

- Harel Statecharts：`rFSM` 的直接语义来源之一。
- UML State Machines：`rFSM` 借用了图形记法和部分语义，但主动削减了 variation points。
- `SCXML`、`Stateflow`、`SFC`：论文都拿来做过对比。
- `OROCOS/RTT`：`rFSM` reference implementation 的实际运行时宿主。

## 文献分类总结

- 这是一篇 `📦` 类机器人协调 DSL 条目，重点在于把 statechart 缩减成一个适合 coordination 的最小可执行核。
- 它描述的主要客体是机器人控制/协调逻辑，因此记为 `🎛️`；整体语境是机器人软件与运行时集成，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“如何把需求生成出来的状态机做成语义清晰、结构受约束且可执行的协调模型”。

# RoboChart：机器人应用功能行为的建模与验证 / RoboChart: modelling and verification of the functional behaviour of robotic applications

## 基本信息

- 标题：RoboChart: modelling and verification of the functional behaviour of robotic applications
- 中文标题：RoboChart：机器人应用功能行为的建模与验证
- 作者：Alvaro Miyazawa, Pedro Ribeiro, Wei Li, Ana Cavalcanti, Jon Timmis, Jim Woodcock
- 发表：*Software & Systems Modeling*, 18(5):3097-3149, 2019
- DOI：`10.1007/s10270-018-00710-z`
- 链接：https://doi.org/10.1007/s10270-018-00710-z
- 形式主义：`RoboChart`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：机器人 DSL / 形式语义与验证工具链
- 工具/实现获取方式：原文明确给出 `RoboTool`，作为一组 Eclipse plug-ins，支持图形/文本建模、well-formedness checking、`CSP-M` 语义生成与 `FDR` 验证；文中给出 York `RoboTool` 下载地址。
- 标准/格式获取方式：承载方式是 `RoboChart` metamodel、graphical/textual editor、内部 textual representation 与自动生成的 `CSP-M`；原文未给行业标准交换格式。

## 简报

`RoboChart` 的目标不是简单地“给机器人也画状态机”，而是把机器人控制常见的 UML-like state machine 习惯，收缩成一个更小、更严谨、更适合自动验证的 DSL。它保留了 roboticists 熟悉的状态机建模方式，但显式补上 metamodel、well-formedness rules、timed primitives 和 `CSP` / `tock-CSP` 语义，从而把建模、验证和后续代码生成放进同一条工具链。

- 形式主义定位：面向机器人控制器的 restricted-`UML` 状态机 DSL，而不是一般软件状态图全语法。
- 构造方式简述：以 module / robotic platform / controller / state machine 四层组织模型，在 machine 内使用 state、junction、transition、clock、event、action language 和 timed primitives。
- 基础设施与场景简述：依托 `RoboTool`、`FDR`、`CSP-M` / `tock-CSP`、Eclipse graphical editor 和后续 code generation，服务 foraging、chemical detection、swarm / controller verification 等机器人应用。

```text
机器人需求 -> RoboChart module / controller / machine -> metamodel + well-formedness + CSP semantics -> RoboTool / FDR -> 验证 / 动画 / 代码生成
```

## 形式主义定义与核心对象

### 定义对象

`RoboChart` 的核心对象是机器人模块中的状态机，但它并不只关心 machine 本体，还显式建模：

1. robotic platform：硬件可提供的事件、变量和操作。
2. controller：封装若干 state machine。
3. state machine：描述离散行为。
4. timed/action language：描述状态动作、通信和时间约束。

### 核心抽象

结合论文对 machine metamodel 的说明，可保守整理单个 `RoboChart` machine 为：

$$
R = (N, n_0, T, V, E, C, O)
$$

上式中的符号逐项解释如下：

1. `N = S \cup J` 是节点集合，由 states 与 junctions 构成。
2. `n_0 \in J` 是 initial junction。
3. `T` 是 transition 集合。
4. `V` 是局部变量和常量集合。
5. `E` 是 machine 声明或需要的 events 集合。
6. `C` 是 clocks 与 deadline/time-bound 相关对象集合。
7. `O` 是 machine 需要调用的 operations 集合。

论文对 machine 结构的关键口径是：

$$
t = (src, trg, trig, guard, act, ddl)
$$

其中：

1. `src`、`trg` 分别是 transition 的源节点与目标节点。
2. `trig` 是 trigger。
3. `guard` 是 condition。
4. `act` 是 transition action。
5. `ddl` 是 deadline 或可用性时间约束。

### 一个最小例子与通俗解释

论文用 `DTP` foraging controller 举了一个很典型的例子：

1. `Exploring` 状态不断执行 `Explore()`。
2. 收到 `collected` 事件后转入 `GoToNest`。
3. 若已经到达 nest 并 `stored` 成功，则转入 `GoToSource`。
4. 若等待转移太久，则经过 `GoToNestDirectly` 再回到 source 搜索。
5. 在 `Neighbourhood` 中，收集到物体就增大 partition；超时则减小 partition 并回到 `Exploring`。

通俗地说，`RoboChart` 像是“把机器人控制图画出来，但每个 state、trigger、clock、接口和时间界都是真的，并且能自动翻成验证器吃得懂的数学模型”。

### 运行 / 接受 / 转移语义

在 `RoboChart` 中，state 是 stable 的，而 junction 必须立即离开。其一步转移可保守写成：

$$
(n, \sigma, \tau) \xrightarrow{e} (n', \sigma', \tau') \iff \exists\, t=(n,n',e,g,a,d)\in T,\ e \land g(\sigma,\tau)
$$

上式中的符号逐项解释如下：

1. `n`、`n'` 是当前节点与下一节点。
2. `\sigma` 是变量环境。
3. `\tau` 是 clocks / time valuation。
4. `e` 是触发事件。
5. `g` 是 transition guard。
6. `a` 是 transition / state action 对环境的更新。
7. `d` 是与 transition 关联的 deadline 约束。

junction 的核心语义边界则可写成：

$$
j \in J \Rightarrow \neg \mathrm{stable}(j)
$$

这表示 junction 不能像普通 state 一样停留等待外部事件；其 outgoing transition 也因此受 well-formedness 规则约束，不能依赖新的外部触发。

论文的更高层语义是把 `RoboChart` 自动映射到 `CSP` / `tock-CSP`：

$$
\llbracket R \rrbracket_{\mathrm{CSP}}
$$

其中：

1. `\llbracket \cdot \rrbracket_{\mathrm{CSP}}` 是 RoboTool 自动生成的过程代数语义。
2. untimed 版本面向 `CSP-M` / `FDR`。
3. timed 版本面向 `tock-CSP`，用于时序性质验证。

### 语义边界

`RoboChart` 的边界同样很明确：

1. 它是 restricted `UML`-style robotics DSL，不追求覆盖 UML 全语法。
2. 它显式排除了会大幅增加语义复杂度的一些一般 UML 机制，例如并行 states。
3. 它更强调离散功能行为与时间原语，不直接建模连续动力学。
4. 它的优势在可验证、可分析，而不是快速随手画图。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| machine 骨架 | `$R = (N, n_0, T, V, E, C, O)$` | `RoboChart` machine 明确包含节点、转移、变量、事件、时钟和操作依赖。 |
| transition 结构 | `$t = (src, trg, trig, guard, act, ddl)$` | trigger、guard、action、deadline 都是一级对象。 |
| 运行一步 | `$(n,\sigma,\tau)\xrightarrow{e}(n',\sigma',\tau')$` | 语义可映射到明确的状态转移关系。 |
| 形式化语义 | `$\llbracket R \rrbracket_{\mathrm{CSP}}$` | RoboTool 自动生成 `CSP` / `tock-CSP` 以做验证。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | state machine 是核心行为构件。 |
| 事件 / 触发 | 强支持 | typed events、triggers 和 controller-level event relay 都明确建模。 |
| 守卫 / 数据 | 强支持 | variables、guards、pre/postconditions 和 action language 完整。 |
| 层次 | 支持 | composite state 和 machine/container 层次明确。 |
| 并发 / 同步 | 部分支持 | controller 可封装多个 machine，但 machine 内不支持任意 UML parallel states。 |
| 时间约束 | 强支持 | clocks、wait、bounds、deadlines 是 DSL 原生构件。 |
| 连续动态 / 随机性 | 不支持 | 重点是离散功能行为；连续部分需在更外层建模。 |
| 可执行 / 可验证性 | 强支持 | well-formedness、`CSP` 语义、`FDR` 验证、后续 code generation 都在同一工具链。 |

### 形式化问题与性质

1. `RoboChart` 的关键价值是“限制表达力以换取可验证性”，这和一般 UML 工具路线不同。
2. junction cover、typing、naming 等 well-formedness 被显式写成规则，而不是隐含在工具里。
3. `CSP` 只是前端验证承载，背后真正想固定的是语言自身语义。
4. 它非常适合作为“高可信机器人状态机”载体，而不只是教学式图形语言。

## 构造方式与承载格式

### 建模入口

建模入口主要有三层：

1. module / robotic platform / controller / machine 分层声明。
2. machine 中定义 states、junctions、transitions、events、variables、clocks。
3. 在 state / transition action 中使用 `RoboChart` action language。

### 机器可处理承载方式

机器可处理承载包括：

1. RoboTool 的内部 textual representation。
2. graphical diagrams。
3. 自动生成的 `CSP-M` / `tock-CSP` 脚本。

### 交换与互操作

`RoboChart` 不追求通用 XML 标准；互操作重点在：

1. 与 `FDR`、`Isabelle/HOL`、`CSP` 工具链对接。
2. 以 library / reference 方式复用 machine。
3. 后续自动代码生成与 `ROS` / robotic platform 对接。

## 配套基础设施

- 建模/编辑工具：`RoboTool` 图形/文本编辑器，基于 Eclipse、Xtext、Sirius。
- 解析/交换/元模型支持：完整 metamodel、well-formedness validation、type checking。
- 仿真/执行支持：后续路线包含 animation 与 code generation，但本文主线是验证。
- 验证/分析支持：自动生成 `CSP-M` / `tock-CSP`，使用 `FDR` 做 deadlock、timelock、refinement 等检查。
- 代码生成/转换支持：文中已说明具备自动 code generation 路线，后续继续扩展。
- 标准化或社区生态：研究型 DSL，但文档、手册和 case studies 完整。

## 适用场景与需求前提

### 适用场景

适合安全要求较高、需要对机器人控制器做明确建模和自动验证的场景，如 foraging、chemical detection、timed mission control、controller correctness 检查等。

### 需求前提

1. 控制逻辑可以抽成离散 state machine。
2. 需要把时间预算、deadline、事件接口写进模型。
3. 团队愿意使用受限 DSL 换取形式语义与验证收益。
4. 平台接口、controller 边界和 state-level actions 能够显式列出。

### 不适用或高成本场景

若任务主要目标只是快速原型或简单脚本集成，`RoboChart` 可能过重；若问题核心是连续动力学细节，则还需要其他模型与其组合。

## 与相邻形式主义的关系

相对 `UML State Machine`，它是面向机器人和验证的受限 profile；相对 `MissionLab`、`RAFCON`、`YASMIN` 这类执行导向框架，它更强调形式语义和验证；相对 timed automata，它更贴近 roboticists 熟悉的状态机建模语境。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文非常接近 `project_1` 的目标：它证明了面向机器人场景的状态机 DSL 可以同时满足“熟悉的建模接口”和“可自动验证的形式语义”。

### 作为目标形式主义还是中间表示

在高可信机器人场景中，它可以直接作为目标形式主义；在更广泛的需求到模型流程中，它也可作为一个非常强的验证中间表示。

### 对需求到模型生成的启发

1. 用受限子集替代“全量 UML”通常更适合自动化。
2. 时间原语和 well-formedness 规则必须从语言层纳入，而不是事后补。
3. `metamodel + semantics + tool support` 三者缺一不可。

## 重要的相关工作

- `UML State Machine` 与其形式化路线：`RoboChart` 直接建立在这条线上，但做了 robotics-specific 收束。
- `MissionLab`、`FlexBE`、`Stateflow` 等工具：论文显式拿来比较其语义和验证能力。
- `Timed Automata`、`CSP`：分别为时间与过程语义提供了关键支撑。

## 文献分类总结

- 这是一篇 `📦` 类高价值条目，既是状态机 DSL，也是形式语义与验证工具链论文。
- 其描述客体是机器人功能控制逻辑，因此记为 `🎛️`；应用语境是机器人/CPS，因此记为 `🌡️`。
- 对 `project_1` 来说，它是连接“专用状态机语言”和“自动验证”两条主线的代表性材料。

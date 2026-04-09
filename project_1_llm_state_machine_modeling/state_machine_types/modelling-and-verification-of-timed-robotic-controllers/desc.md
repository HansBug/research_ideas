# 机器人定时控制器的建模与验证 / Modelling and Verification of Timed Robotic Controllers

## 基本信息

- 标题：Modelling and Verification of Timed Robotic Controllers
- 中文标题：机器人定时控制器的建模与验证
- 作者：Pedro Ribeiro, Alvaro Miyazawa, Wei Li, Ana Cavalcanti, Jon Timmis
- 发表：*Integrated Formal Methods*, pp. 18-33, 2017
- DOI：`10.1007/978-3-319-66845-1_2`
- 链接：https://doi.org/10.1007/978-3-319-66845-1_2
- 形式主义：`RoboChart`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：定时机器人状态机语义 / 形式化建模语言
- 工具/实现获取方式：原文明确指出 `RoboTool` 已经机械化实现 `RoboChart -> tock-CSP` 编码，可用 `FDR` 检查 timed properties。
- 标准/格式获取方式：承载方式是 `RoboChart` 的图形状态机、时间原语、`RoboTool` 生成的 `tock-CSP`/`CSP` 语义；原文未给独立 XML/JSON 标准。

## 简报

这篇论文的重要性在于，它把 `RoboChart` 从“看起来像机器人常用状态图的 DSL”推进成了一个真正带 timed semantics 的形式化语言。论文不是简单说“加几个时钟就好”，而是明确给出 clock、deadline、budget、`since(C)`、`sinceEntry(S)`、`wait(d)` 这些时间原语，再把整套模型编到 `Timed CSP` / `tock-CSP` 里，用 `RoboTool` 和 `FDR` 做自动检查。

- 形式主义定位：面向机器人控制器的 timed state-machine DSL，而不是一般性的 timed automata 理论模型。
- 构造方式简述：以 module / robotic platform / controller / state machine 组织模型，在 transition、action 和 state 上加入时间预算、deadline 与 clock primitives。
- 基础设施与场景简述：依托 `RoboTool`、`Timed CSP`、`tock-CSP`、`FDR`，服务 swarm transport、chemical detector、obstacle avoidance 等 timed robotic controllers。

```text
机器人需求 -> RoboChart timed state machine -> clock / deadline / wait primitives -> tock-CSP semantics -> FDR verification
```

## 形式主义定义与核心对象

### 定义对象

论文给出的核心对象包括：

1. robotic platform：抽象机器人对外提供的 events、operations 和 variables。
2. controller：封装一个或多个 state machine。
3. state machine：描述控制器的离散行为。
4. clock 与 timed primitive：支持 `#C`、`since(C)`、`sinceEntry(S)`、`wait(d)`、deadline。
5. `Timed CSP` / `tock-CSP` semantics：支撑 refinement 和 model checking。

### 核心抽象

结合论文对 RoboChart timed metamodel 的说明，可将单个 timed machine 保守整理为：

$$
R = (S, J, s_0, E, V, C, Tr, \Delta)
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `J` 是 junction 集合。
3. `s_0 \in J` 是初始 junction。
4. `E` 是事件集合。
5. `V` 是局部变量与常量集合。
6. `C` 是时钟集合。
7. `Tr` 是转移集合。
8. `\Delta` 是时间构件集合，包含 budget、deadline 与 timed expressions。

单个转移可整理为：

$$
tr = (src, trg, e, g, a, d)
$$

其中：

1. `src`、`trg` 是源与目标状态或 junction。
2. `e` 是触发事件，可以为空。
3. `g` 是 guard，可含 `since(C)` 或 `sinceEntry(S)`。
4. `a` 是转移动作。
5. `d` 是与动作或事件相关的时间预算 / deadline 信息。

论文列出的代表时间原语可保守写成：

$$
\Delta \supseteq \{\#C,\ \mathrm{since}(C),\ \mathrm{sinceEntry}(S),\ \mathrm{Wait}(d),\ \mathrm{deadline}(e,d),\ \mathrm{deadline}(A,d)\}
$$

上式中的符号逐项解释如下：

1. `#C` 表示复位时钟 `C`。
2. `since(C)` 表示自上次复位以来经过的时间。
3. `sinceEntry(S)` 表示进入状态 `S` 以来的时间。
4. `Wait(d)` 表示显式等待 / budget。
5. `\mathrm{deadline}(e,d)` 表示事件 `e` 的 deadline 约束。
6. `\mathrm{deadline}(A,d)` 表示动作 `A` 的 deadline 约束。

### 一个最小例子与通俗解释

论文先用“方形轨迹 + obstacle avoidance”举例：

1. 机器人默认在 `MovingForward` 中前进。
2. 如果探测到障碍，就复位时钟并切到避障或转向状态。
3. 用 `since(C)==5` 限定直线运动持续多久。
4. 用 `sinceEntry(Turning)==2` 限定转向持续多久。
5. 用 `stop <{0}` 或 `moveForward(linear) <{0}` 记录某些操作应被立即接受。

通俗地说，`RoboChart` 在这里做的事情就是：把“机器人平时画在论文里的状态图”补成一张真正能说清楚“等多久、什么时候必须发生、什么算超时”的可验证状态机。

### 运行 / 接受 / 转移语义

论文把 `RoboChart` 映射到 `Timed CSP` / `tock-CSP`。单步 timed transition 可保守写成：

$$
(s, \sigma, \tau) \xrightarrow{e} (s', \sigma', \tau') \iff \exists\, (s,s',e,g,a,d)\in Tr,\ e \land g(\sigma,\tau)
$$

上式中的符号逐项解释如下：

1. `s`、`s'` 是当前状态与后继状态。
2. `\sigma`、`\sigma'` 是转移前后的变量环境。
3. `\tau`、`\tau'` 是时钟赋值。
4. `e` 是触发事件。
5. `g(\sigma,\tau)` 要求 guard 在当前数据与时钟环境下成立。
6. `a` 是动作，`d` 则给动作或事件附加时间约束。

高层语义则由 `Timed CSP` 给出：

$$
\llbracket R \rrbracket_{\mathrm{TCSP}} \Rightarrow \llbracket R \rrbracket_{\mathrm{tock}}
$$

上式中的符号逐项解释如下：

1. `\llbracket R \rrbracket_{\mathrm{TCSP}}` 是 RoboChart 的 `Timed CSP` 语义。
2. `\llbracket R \rrbracket_{\mathrm{tock}}` 是其在 `tock-CSP` 中的离散时间编码。
3. 论文通过这条编码链把 timed primitives 落到 `FDR` 可处理的检查对象上。

### 语义边界

这篇论文中的 `RoboChart` 边界非常明确：

1. 它是机器人 DSL，不是一般 timed automata 的直接替代品。
2. 它优先保留 roboticists 熟悉的状态机建模界面，而不是追求最小抽象。
3. 时间被设计成机器人场景友好的 budget/deadline 语义，而不是纯同步时钟网络。
4. 它强调 refinement 与工具支持，而不是只给一个理论定义就结束。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed machine 骨架 | `$R = (S, J, s_0, E, V, C, Tr, \Delta)$` | 机器不仅有状态与事件，还显式包含 clocks 与时间原语。 |
| 转移结构 | `$tr = (src, trg, e, g, a, d)$` | 事件、守卫、动作和时间约束都是一级对象。 |
| 单步执行 | `$(s,\sigma,\tau)\xrightarrow{e}(s',\sigma',\tau')$` | 转移依赖事件、数据和时钟赋值。 |
| 语义映射 | `$\llbracket R \rrbracket_{\mathrm{TCSP}} \Rightarrow \llbracket R \rrbracket_{\mathrm{tock}}$` | 通过 `tock-CSP` 进入 `FDR` 检查链。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 以 UML-like state machine 为核心。 |
| 事件 / 触发 | 强支持 | 事件触发与 event deadline 都是一级机制。 |
| 守卫 / 数据 | 强支持 | guards 可同时依赖变量和时间原语。 |
| 层次 | 支持 | controller 可封装多个 machine，状态图也支持层次结构。 |
| 并发 / 同步 | 部分支持 | controller 可含多个 machine，但论文重点在单机 timed semantics。 |
| 时间约束 | 强支持 | `clock`、`since`、`sinceEntry`、`wait`、deadline 是核心贡献。 |
| 连续动态 / 随机性 | 不支持 | 聚焦离散 timed controllers。 |
| 可执行 / 可验证性 | 强验证 | 可自动生成 `tock-CSP` 并用 `FDR` 检查。 |

### 形式化问题与性质

1. 论文真正补上的不是“又一个状态机语法”，而是 timed primitive 的精确定义和 tool-backed semantics。
2. 与一般 UML 或论文插图式状态图相比，它让时间预算和 deadline 能直接写进状态机本体。
3. `RoboTool` 的机械化编码说明该语言从设计之初就是为了自动验证，而不是手工翻译。
4. 这篇工作直接奠定了后续 `RoboChart` 设计-验证-实现路线的 timed 语义基础。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 定义 robotic platform 的事件、变量与操作。
2. 定义 controller 与其中的 state machines。
3. 在 states、transitions 和 actions 上加入 timed primitives。
4. 通过 `RoboTool` 图形编辑器构造模型。

### 机器可处理承载方式

原文体现出的机器可处理承载方式包括：

1. `RoboChart` 图形状态机模型。
2. 其 timed metamodel。
3. `RoboTool` 自动生成的 `Timed CSP` / `tock-CSP` 语义。

### 交换与互操作

互操作重点在：

1. 平台与 controller 通过 robotic platform 抽象解耦。
2. 语义层与 `FDR` / `CSP` 工具链对接。
3. 后续可进一步映射到 theorem proving 或 simulation/deployment 路线。

## 配套基础设施

- 建模/编辑工具：`RoboTool` 图形编辑器。
- 解析/交换/元模型支持：timed metamodel、clock primitive、validation 规则。
- 仿真/执行支持：论文主线是建模与验证，执行/部署尚不是重点。
- 验证/分析支持：`Timed CSP`、`tock-CSP`、`FDR`，并面向 refinement。
- 代码生成/转换支持：已经有机械化语义编码，后续面向证明与执行转换。
- 标准化或社区生态：研究型 DSL，生态集中在 `RoboChart` / `RoboTool` / `CSP` 链。

## 适用场景与需求前提

### 适用场景

适合存在明确时间预算、deadline、等待窗口或超时条件的机器人控制器设计与验证场景，例如 swarm coordination、chemical detector、timed obstacle avoidance 等。

### 需求前提

1. 控制逻辑可以抽象成离散状态机。
2. 时间要求能表达成 clock-based guards、budgets 或 deadlines。
3. 团队愿意采用专用 DSL 以换取语义清晰和可验证性。
4. 平台接口、事件与操作能事先抽成 robotic platform。

### 不适用或高成本场景

如果主要需求是连续动力学精确建模、复杂优化调度或不依赖状态机的行为生成，这个版本的 `RoboChart` 不是主战场；它更适合 timed discrete controller。

## 与相邻形式主义的关系

相对 `Timed Automata`，它更贴近机器人控制实践和模块化接口；相对 `UML`/`RobotML`，它把时间预算和 deadline 直接拉进语言本体；相对后续 2019 与 2024 的 `RoboChart` 工作，这篇论文是 timed semantics 的关键前身。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文非常关键，因为它证明专用机器人状态机语言可以同时保持“图形建模习惯”和“可精确定义时间语义”。

### 作为目标形式主义还是中间表示

在有定时约束的高可信机器人控制场景中，它可以直接作为目标形式主义；在更一般流程中，它也非常适合作为验证中间表示。

### 对需求到模型生成的启发

1. 时间需求不应被留到后续验证阶段临时补充，而应在状态机语言里原生表达。
2. 平台抽象与 controller 抽象分离，有助于复用同一控制逻辑到不同机器人平台。
3. 如果目标是自动验证，语义落地到现有验证器的机械化编码必须从一开始就设计好。

## 重要的相关工作

- `Timed Automata` 与 `UPPAAL`：提供定时验证的经典理论与工具背景。
- `RobotML`、`UML-MARTE`、`UML-RT`：都是机器人 / 实时系统建模的邻近路线，但时间表达或验证支撑方式不同。
- `GenoM`、`Orccad`：代表更偏执行语言或机器人中间件的另一路工程化建模方案。

## 文献分类总结

- 这是一篇 `📦` 类高价值条目，重点在机器人定时状态机 DSL 的语义和验证支撑，而不是纯 timed automata 理论。
- 其描述客体是机器人控制逻辑，因此记为 `🎛️`；论文语境面向机器人/CPS，因此记为 `🌡️`。
- 对 `project_1` 来说，它是 `RoboChart` 这条“机器人专用状态机 + 形式验证”支线的基础节点。

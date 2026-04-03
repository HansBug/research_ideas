# 在机器人中使用有限状态自动机 / Using Finite State Automata in Robotics

## 基本信息

- 标题：Using Finite State Automata in Robotics
- 中文标题：在机器人中使用有限状态自动机
- 作者：Richard Balogh, David Obdržálek
- 发表：SensorWiki / `robotics.sk` 开放会议论文（`RiE 2018` Malta 投稿版）, 2018
- DOI：原文未提供
- 链接：https://robotics.sk/go/FSM/finite-state-automata.pdf
- 形式主义：`Educational Robotics FSM`
- 主类：🧩 经典离散状态机
- 对象类型：🧪 应用/案例
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：教育机器人控制 / `FSM` 应用教程
- 工具/实现获取方式：原文直接给出 `C` 语言实现、transition table matrix、Microsoft MakeCode Block language、`micro:bot` 机器人套件、`MART Friday Bot` 竞赛机器人与 `Stateflow / Arduino / JavaScript` 等实现线索；未给出统一代码仓库。
- 标准/格式获取方式：原文没有定义独立交换标准，主要承载方式是有向图状态图、transition matrix table、`switch-case` 代码和 Block language 控制图。

## 简报

这篇论文不是在发明新状态机类型，而是在证明：**普通 `FSM` 本身就足以承载大量入门级乃至中等复杂度机器人控制任务**。作者从最基本的五元组定义出发，先给电源开关和密码锁，再把 line following 与 `MART Friday Bot` 这样的真实机器人行为组织成状态机，强调其对可读性、可维护性和调试性的价值。

- 形式主义定位：面向教育机器人与竞赛机器人的通用 `FSM` 控制方法，核心是把离散行为阶段、触发条件和动作输出显式建模。
- 构造方式简述：既可用图形式状态图，也可用 transition table、`C` 语言 `switch-case` 或 Block language 编码实现。
- 基础设施与场景简述：依托 `C`、MakeCode、`micro:bot`、`MART Friday Bot` 和常见入门机器人硬件，服务 line follower、物体搬运与竞赛行为组织。

```text
传感器输入 -> FSM 当前状态 -> transition / table lookup -> 电机 / 执行输出
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. 基本有限状态机 `A = (S, \Sigma, \delta, s_0, F)`。
2. 状态集合 `S`，对应控制阶段，例如 `OnLine / TooLeft / TooRight / Lost`。
3. 输入字母表 `\Sigma`，对应按钮、线传感器、碰撞传感器等离散事件。
4. 转移函数 `\delta`，决定在给定状态与输入下跳转到哪个状态。
5. transition table matrix，实现 `FSM` 的一种代码承载方式。
6. 与状态关联的输出动作，例如 `goStraight`、`goLeft`、`setOutput` 等。

### 核心抽象

论文直接给出了经典 `FSM` 五元组：

$$
A = (S, \Sigma, \delta, s_0, F)
$$

上式中的符号逐项解释如下：

1. `S` 是有限、非空的状态集合。
2. `\Sigma` 是有限、非空的输入符号集合。
3. `\delta : S \times \Sigma \to S` 是状态转移函数。
4. `s_0 \in S` 是初始状态。
5. `F \subseteq S` 是终止状态集合。

论文还给出了 transition matrix 的典型实现：

$$
\mathrm{nextState} = \mathrm{stateTable}[\mathrm{currentState}][\mathrm{transition}]
$$

上式中的符号逐项解释如下：

1. `\mathrm{stateTable}` 是按“状态 × 输入事件”索引的二维表。
2. `\mathrm{currentState}` 是当前状态。
3. `\mathrm{transition}` 是当前读到的离散输入。
4. `\mathrm{nextState}` 是下一状态。

对于 line following 示例，状态集合可进一步整理为：

$$
Q_{\mathrm{line}} = \{\mathrm{OnLine}, \mathrm{TooRight}, \mathrm{TooLeft}, \mathrm{Lost}\}
$$

上式中的符号逐项解释如下：

1. `\mathrm{OnLine}` 表示机器人正对轨迹。
2. `\mathrm{TooRight}` 表示机器人偏右，需要左转。
3. `\mathrm{TooLeft}` 表示机器人偏左，需要右转。
4. `\mathrm{Lost}` 表示两线传感器都无法确认轨迹。

### 一个最小例子与通俗解释

最小例子可以直接用 line follower：

1. 两个线传感器读取到黑线 / 白地组合。
2. 若左传感器压线、右传感器离线，则进入 `TooRight`，输出 `goLeft`。
3. 若右传感器压线、左传感器离线，则进入 `TooLeft`，输出 `goRight`。
4. 若两个传感器都对准轨迹，则进入 `OnLine`，输出 `goStraight`。
5. 若都没读到有效轨迹，则进入 `Lost` 并停止或进入恢复逻辑。

通俗地说，这个模型像一个“离散反应开关板”：机器人不是每次都从零开始计算复杂策略，而是先问“我现在在哪个模式下”，再根据当前输入切换模式并发出动作。

### 运行 / 接受 / 转移语义

论文里的运行语义可以压缩为：

$$
(s_t, \sigma_t) \xrightarrow{\delta} s_{t+1} \xrightarrow{\lambda} u_t
$$

上式中的符号逐项解释如下：

1. `s_t` 是当前状态。
2. `\sigma_t` 是当前离散输入。
3. `s_{t+1}` 是转移后的状态。
4. `\lambda` 表示与新状态或状态-输入对绑定的输出动作逻辑。
5. `u_t` 是电机或执行器输出。

对于 code lock 或 table-driven 实现，其语义等价于用数组替代 `if-else` 链：

$$
\delta(s, \sigma) = \mathrm{stateTable}[s][\sigma]
$$

这说明论文的重点不是改变 `FSM` 理论，而是展示不同实现方式如何让机器人控制代码更易维护。

### 语义边界

这个模型的边界包括：

1. 它聚焦入门和中等复杂度机器人控制，不试图覆盖复杂连续控制或高维规划。
2. 论文主要强调工程可读性与教学价值，而不是形式验证。
3. `FSM` 在这里大多是扁平结构；复杂场景需要进一步扩展到 `HFSM` 或异步状态机。
4. 当任务超出 regular / finite-memory 模式时，单纯 `FSM` 会明显不足。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基本 `FSM` 定义 | `$A = (S, \Sigma, \delta, s_0, F)$` | 机器人控制核心可用标准有限状态机表达。 |
| 转移函数 | `$\delta : S \times \Sigma \to S$` | 当前状态与输入共同决定下一状态。 |
| 表驱动实现 | `$\mathrm{nextState} = \mathrm{stateTable}[\mathrm{currentState}][\mathrm{transition}]$` | transition table 可替代长串 `if-else`。 |
| line follower 状态集 | `$Q_{\mathrm{line}} = \{\mathrm{OnLine}, \mathrm{TooRight}, \mathrm{TooLeft}, \mathrm{Lost}\}$` | 入门机器人任务可直接落成离散模式。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | line follower、code lock、竞赛机器人都用明确状态组织。 |
| 事件 / 触发 | 强支持 | 按钮、传感器、电平输入等都是显式离散事件。 |
| 守卫 / 数据 | 中等支持 | 主要是离散输入和简单触发条件，数据结构较轻。 |
| 层次 | 弱支持 | 论文主体是扁平 `FSM`，只在相关工作中提到 `HFSM`。 |
| 并发 / 同步 | 弱支持 | 不强调并发控制。 |
| 时间约束 | 弱支持 | 仅提到 timer 作为 transition 条件，没有时钟语义。 |
| 连续动态 / 随机性 | 不支持 | 连续控制被抽象为状态输出动作。 |
| 可执行 / 可验证性 | 强执行、有限验证 | 很适合直接编码执行，但形式验证不是重点。 |

### 形式化问题与性质

1. 论文真正回答的是“为什么在机器人里用普通 `FSM` 就已经很有工程价值”。
2. 对教育和竞赛机器人，状态机最大的价值是让代码结构与行为结构一致。
3. transition table matrix 是很实用的承载方式，因为它把行为结构显式化了。
4. 对自动建模任务来说，这类条目提供了“最小可工作状态机”的清晰起点。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 先画状态图，把行为分成有限个模式。
2. 再确定输入集合与转移条件。
3. 最后选择 `switch-case`、transition table 或 Block language 落地。
4. 在真实机器人上把状态输出绑定到电机 / 伺服动作。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. 图形式 `FSM`。
2. tree / table 表示法。
3. `C` 语言 `switch-case`。
4. transition matrix table。
5. Microsoft MakeCode Block language。

### 交换与互操作

互操作重点在：

1. 传感器读数先被离散化成输入符号。
2. 状态机根据输入更新 `currentState`。
3. 新状态触发电机 / 执行器输出。
4. 在更复杂的机器人中，可把状态机与模拟器、`Stateflow` 或外部库联用。

## 配套基础设施

- 建模/编辑工具：状态图、`C` 编译环境、MakeCode Block language。
- 解析/交换/元模型支持：transition table、手写状态图与轻量状态机库；原文未给统一元模型标准。
- 仿真/执行支持：`micro:bot`、`MART Friday Bot`、竞赛机器人和文中提到的 `Stateflow` / simulator 路线。
- 验证/分析支持：主要依靠仿真和实机调试，不是形式验证框架。
- 代码生成/转换支持：原文提到可借助 `Stateflow` 与各类状态机库，但未给统一自动生成链。
- 标准化或社区生态：依托教育机器人、Arduino/JavaScript 状态机库和竞赛社区实践。

## 适用场景与需求前提

### 适用场景

适合 line following、简单抓取搬运、竞赛机器人、教育机器人课程和那些能被少量离散模式稳定描述的控制任务。

### 需求前提

1. 任务具有清晰的离散阶段和有限记忆特征。
2. 传感器输入可被离散化成有限事件。
3. 输出动作可由当前状态或状态-输入对直接决定。
4. 不需要复杂规划、长程记忆或连续动力学推理。

### 不适用或高成本场景

若任务需要复杂层次结构、多 agent 协调、连续动力学约束或概率推理，平坦 `FSM` 会很快变得笨重，需要升级到 `HFSM`、行为树或更强形式主义。

## 与相邻形式主义的关系

相对 `HFSM`、`SMACH`、`RAFCON` 这类工程运行时，它更像最低门槛的离散控制骨架；相对 `Stateflow`，它更轻量也更易手写；相对行为树，它不强调 tick-based reevaluation，而强调显式模式切换。

## 与本研究的关系

### 对 Project 1 的价值

这篇条目的价值在于，它给 `project_1` 提供了一个非常清楚的基线：当需求本身已经足够离散时，最普通的 `FSM` 其实就足够成为目标输出。

### 作为目标形式主义还是中间表示

对简单机器人任务，它可以直接作为目标形式主义；对复杂控制系统，它更适合作为解释性强、易于生成的中间表示。

### 对需求到模型生成的启发

1. 需求文本里的“如果传感器这样，就执行那样”非常适合直接映射到平坦 `FSM`。
2. 自动生成时，transition table 是很自然的机器可处理输出。
3. 若目标用户是教学或原型开发场景，生成简洁 `FSM` 反而比生成复杂模型更有价值。

## 重要的相关工作

- `Stateflow`：论文明确提到可用于状态机审计和仿真。
- `Pyro` toolkit：文中作为更复杂机器人 `FSM` 应用的示例。
- 层次 / 异步状态机机器人案例：论文在结论中举为更高阶路线。
- Canadian Space Agency autonomy techniques：作为 `FSM` 在真实自主场景中被测试过的佐证。

## 文献分类总结

- 这是一篇 `🧩` 类普通 `FSM` 应用条目，重点在机器人控制中的使用方法，而不是新运行时或新 DSL。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；虽然带有教育属性，但对象始终是实体机器人行为，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“最小离散控制需求可以如何直接落成普通 `FSM`”的基线证据。

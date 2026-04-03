# 面向多移动机器人协调的 Petri 网在线控制器 / A Petri Net On-Line Controller for the Coordination of Multiple Mobile Robots

## 基本信息

- 标题：A Petri Net On-Line Controller for the Coordination of Multiple Mobile Robots
- 中文标题：面向多移动机器人协调的 Petri 网在线控制器
- 作者：Faustina Hwang
- 发表：Master of Engineering thesis, Memorial University of Newfoundland, 2000
- DOI：原文未提供
- 链接：https://hdl.handle.net/20.500.14783/9162
- 形式主义：`Petri Net On-Line Controller + Automatic Net Generation`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：多移动机器人协调 / Petri 网在线离散事件控制
- 工具/实现获取方式：原文明确实现了 `Visual C++` Petri Net Generator / Interpreter、图形监控和 reachability 分析模块；未提供公开仓库。
- 标准/格式获取方式：承载方式是高层任务描述、resource places、自动生成的 `PN` 子网和运行时解释器；原文未提供独立交换格式。

## 简报

这篇论文的价值，在于把 Petri 网真正推进到“运行中的多机器人协调器”层面。作者不是只做离线建模，而是把高层 marker-based task description 自动翻译成 Petri 网，再让解释器在运行时发机器人指令、接收反馈、更新 marking。其建模焦点也很明确：共享道路、共享路口、互斥资源、在线等待与继续执行。这使它比单纯的 Petri 网分析论文更接近可执行 supervisory controller。

- 形式主义定位：面向多移动机器人共享资源协调的 `Petri Net` 应用模型，而不是一般工作流仿真。
- 构造方式简述：先把 road segments / intersections 建成 resource places，再按任务描述自动拼装 robot-specific subnets，最后用 interpreter 运行。
- 基础设施与场景简述：依托 Petri Net Generator、Petri Net Interpreter、graphical monitoring 和 marker-based navigation 示例，服务多机器人在线调度与运行时协调。

```text
高层任务描述 -> 资源位 + 机器人子网 -> 自动生成 Petri 网控制器 -> 解释器发命令 / 收反馈 -> 在线协调与监控
```

## 形式主义定义与核心对象

### 定义对象

论文处理的对象包括：

1. places、transitions、arcs、weights 与 marking。
2. 共享 road segments / intersections 资源。
3. 每个机器人的任务描述序列。
4. 自动生成的子网与全局资源 place。
5. 在线解释器中的 deterministic / stochastic transitions。

### 核心抽象

原文给出的 Petri 网基本定义是：

$$
PN = (P, T, A, W, M_0)
$$

上式中的符号逐项解释如下：

1. `P` 是 place 集合。
2. `T` 是 transition 集合。
3. `A \subseteq (P \times T) \cup (T \times P)` 是弧集合。
4. `W` 是弧权函数。
5. `M_0` 是初始 marking。

变迁使能与 firing 语义可以压成：

$$
t \text{ enabled } \iff \forall p \in I(t),\ M(p) \ge w(p,t)
$$

$$
M'(p) = M(p) - w(p,t) + w(t,p)
$$

上式中的符号逐项解释如下：

1. `I(t)` 是 transition `t` 的输入 place 集合。
2. `M(p)` 是当前 marking 下 place `p` 的 token 数。
3. `w(p,t)` 是从 place 到 transition 的输入弧权重。
4. `w(t,p)` 是从 transition 到 place 的输出弧权重。
5. firing 后，输入 token 被消耗、输出 token 被产生。

论文后面还给出 state equation 观点，可压缩为：

$$
M_k = M_{k-1} + A u_k
$$

上式中的符号逐项解释如下：

1. `M_k` 是第 `k` 次 firing 后的 marking。
2. `A` 是 incidence matrix。
3. `u_k` 是表示本轮 fired transition 的 firing vector。

### 一个最小例子与通俗解释

论文里最直观的例子是两个机器人共享道路和路口：

1. place `R2` 和 `R3` 表示两段道路资源，place `I1` 表示路口资源。
2. 每个资源 place 默认只有一个 token，表示“钥匙只有一把”。
3. 某机器人要穿过路口时，必须先拿到 `I1` 和目标道路 `R3` 的 token。
4. 如果目标资源还没空出来，就走 `STOP` 分支等待；一旦 token 回来，再继续执行 `TOM6`。

通俗地说，这个模型像一套“道路钥匙系统”：谁先拿到 token，谁就先占路；没拿到的人不能硬闯，只能在 Petri 网里等。

### 运行 / 接受 / 转移语义

论文除了标准 Petri firing 规则，还把 transition 分成两类：

1. deterministic transition：带有固定 firing time，并在 firing 时向机器人发送任务命令。
2. stochastic transition：等待机器人反馈事件发生，再完成 firing。

因此在线语义不是单纯的 token 演化，而是：

1. deterministic transition 负责“下发动作”。
2. stochastic transition 负责“等待动作完成”。
3. marking 的变化因此同步反映了控制状态与执行反馈。

### 语义边界

这篇论文的边界比较清楚：

1. 核心是离散事件协调，不处理连续控制律。
2. 当前实现主要面向 marker-based navigation。
3. 时间 Petri Nets、Colored Petri Nets 等只在扩展方向里讨论。
4. 安全假设较强，例如资源互斥和停车距离可由环境与机器人底层保证。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基本网定义 | `$PN = (P, T, A, W, M_0)$` | 在线控制器的结构骨架。 |
| 使能条件 | `$M(p) \ge w(p,t)$` | 只有资源满足时，机器人动作才可触发。 |
| firing 更新 | `$M'(p) = M(p) - w(p,t) + w(t,p)$` | token 演化规则。 |
| 资源互斥 | 单 token resource places | 道路与路口的唯一占用。 |
| reachability | `R(M_0)` | 可用于检查冲突或死锁 marking 是否可达。 |
| state equation | `$M_k = M_{k-1} + A u_k$` | 提供矩阵化分析入口。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 直接表示系统运行状态。 |
| 事件 / 触发 | 强支持 | 任务命令与反馈事件分别进入不同 transition 类型。 |
| 守卫 / 数据 | 部分支持 | 主要通过资源 place / inhibitor arcs 表达条件。 |
| 层次 | 弱支持 | 当前重点是自动生成子网，而不是层次网。 |
| 并发 / 同步 | 强支持 | 共享资源、互斥和等待是核心。 |
| 时间约束 | 弱支持 | 只支持有限 firing time，完整 timed / stochastic PN 仍在后续工作。 |
| 连续动态 / 随机性 | 弱支持 | stochastic transitions 只表示等待时长不确定，不建模连续动力学。 |
| 可执行 / 可验证性 | 强支持 | 同时支持在线解释执行和 reachability 分析。 |

### 形式化问题与性质

1. 论文的核心不是“又一个 Petri 网例子”，而是把网结构自动生成和运行时解释器绑在一起。
2. resource places 是其协调多机器人共享道路/路口的关键抽象。
3. deterministic / stochastic transition 的区分让网结构能直接承接“下发命令 / 等待反馈”的控制闭环。
4. reachability 分析因此不只是离线证明，也可以反哺高层任务描述修订。

## 构造方式与承载格式

### 建模入口

建模入口遵循以下顺序：

1. 给出环境资源描述，例如 roads / intersections。
2. 给出每个机器人的高层 marker 序列。
3. 创建 resource places。
4. 根据两类基本场景自动生成 robot subnets：同一路段内移动、穿越路口移动。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. 高层 marker-based task description。
2. resource places。
3. 自动生成的 category-1 / category-2 子网结构。
4. Petri Net Interpreter 中的 deterministic / stochastic transition 语义。

### 交换与互操作

互操作重点在于：

1. 任务描述如何被翻译成网结构。
2. Petri 网 firing 如何映射到 robot commands。
3. 机器人反馈如何重新驱动 transition 完成。

## 配套基础设施

- 建模/编辑工具：原文实现了 `Visual C++` Petri Net 软件、graphical UI 与自动生成器。
- 解析/交换/元模型支持：有内部数学表示与图形表示，但未给公开 schema。
- 仿真/执行支持：支持在线解释执行、图形 token 监控和 proof-of-concept 演示。
- 验证/分析支持：reachability tree、boundedness、liveness 等 Petri 分析入口。
- 代码生成/转换支持：高层任务描述到控制网的自动生成是本文核心贡献之一。
- 标准化或社区生态：依托 Petri Net 与多机器人离散事件控制研究生态。

## 适用场景与需求前提

### 适用场景

适合多移动机器人在共享通道、共享路口、共享工位中的在线协调，尤其是任务可被切成一串显式导航与占用操作的场景。

### 需求前提

1. 环境可抽象成有限资源与互斥占用关系。
2. 高层任务可写成 marker 或 waypoint 序列。
3. 机器人有底层控制器负责完成单步导航动作。
4. 停车与等待动作在物理上可被可靠执行。

### 不适用或高成本场景

如果系统高度连续、环境过于开放、或者资源约束无法离散成 place / token，这套在线 `PN` 控制器的建模成本会很高。

## 与相邻形式主义的关系

相对 [petri-net-based-multi-robot-task-coordination-from-temporal-logic-specifications/desc.md](../petri-net-based-multi-robot-task-coordination-from-temporal-logic-specifications/desc.md)，本文更强调高层任务到在线控制器的自动生成，而非从 `LTL` 合成 supervisor；相对 [a-petri-net-model-for-an-open-path-multi-agv-system/desc.md](../a-petri-net-model-for-an-open-path-multi-agv-system/desc.md)，它更偏运行时解释器与 proof-of-concept 控制；相对 [distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md](../distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md)，它更早、更原始，但已经把自动生成与在线执行串起来了。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求天然包含共享资源、互斥访问和运行时等待逻辑时，Petri 网比普通 `FSM` 更自然，也更容易承接在线监督控制。

### 作为目标形式主义还是中间表示

对多机器人资源协调任务，它可以直接作为目标形式主义；对更一般的控制系统，它也很适合作为“并发资源层”的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应显式识别资源、占用规则和等待条件。
2. LLM 生成并发协调模型时，应优先把“互斥资源”映射为 places / tokens，而不是硬塞进 guard 条件。
3. 对任务说明较结构化的场景，可以直接尝试从高层描述自动拼网，而不必人工逐条画图。

## 重要的相关工作

- [petri-net-based-multi-robot-task-coordination-from-temporal-logic-specifications/desc.md](../petri-net-based-multi-robot-task-coordination-from-temporal-logic-specifications/desc.md)：更现代的多机器人 `PN + supervisor` 路线。
- [a-petri-net-model-for-an-open-path-multi-agv-system/desc.md](../a-petri-net-model-for-an-open-path-multi-agv-system/desc.md)：面向共享道路/AGV 的资源占用建模。
- [distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md](../distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md)：把 Petri 网进一步接入 `ROS/PNML/TINA` 工具链。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值应用条目，核心贡献是把多移动机器人协调任务自动翻译成可在线解释执行的 Petri 网控制器。
- 其描述客体是并发资源流与互斥占用，因此记为 `🏭`；论文语境是移动机器人协同运行，因此记为 `🌡️`。
- 对 `project_1` 来说，它补足了“共享资源 + 在线等待 + 反馈驱动执行”这一类需求的 Petri 网证据。

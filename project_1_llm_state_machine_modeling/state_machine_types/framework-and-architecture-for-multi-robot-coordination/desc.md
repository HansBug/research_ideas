# 面向多机器人协同的框架与体系结构 / A Framework and Architecture for Multi-Robot Coordination

## 基本信息

- 标题：A Framework and Architecture for Multi-Robot Coordination
- 中文标题：面向多机器人协同的框架与体系结构
- 作者：Rafael Fierro, Aveek Das, John Spletzer, Joel Esposito, Vijay Kumar, James P. Ostrowski, George Pappas, Camillo J. Taylor, Yerang Hur, Rajeev Alur, Insup Lee, Greg Grudic, Ben Southall
- 发表：The International Journal of Robotics Research, 21(10-11):977-995, 2002
- DOI：`10.1177/0278364902021010981`
- 链接：https://doi.org/10.1177/0278364902021010981
- 形式主义：`CHARON` / multi-robot coordination architecture
- 主类：🌊 混成/随机扩展
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：应用框架 / 软件架构
- 工具/实现获取方式：原文给出 `CHARON` 高层语言、附录代码、面向对象实时软件架构和 `GRASP Clodbuster` 机器人实验平台，但未提供公开仓库下载入口。
- 标准/格式获取方式：原文承载是 `CHARON` 的文本式 agent/mode 代码、共享变量与通信通道；未提供独立交换标准。

## 简报

这篇论文不是单独重新定义一套纯理论混成自动机，而是把 `CHARON` 作为一个面向真实机器人协同任务的层次化混成状态机载体来落地。它用 `agent` 描述体系结构，用 `mode` 描述控制行为，再把每个 mode 下的连续动力学、离散切换和通信条件放进一个统一的软件架构中，服务搜索、避障、编队、协同定位和协同操纵等多机器人任务。

- 形式主义定位：面向多机器人协同控制的层次化混成状态机语言与软件架构。
- 构造方式简述：以 `agent` 层次、`mode` 嵌套、守卫迁移、微分/代数约束、不变式和共享变量/通信通道联合构造。
- 基础设施与场景简述：依托 `CHARON` 文本 DSL、多线程对象架构、视觉估计器与控制器模块，直接服务 networked robotic systems。

```text
任务需求 -> robot agents / control-estimator hierarchy -> CHARON modes + continuous dynamics -> 多机器人协调 / 编队 / 避障 / 协同感知
```

## 形式主义定义与核心对象

### 定义对象

论文把每个机器人视为一个具有有限行为模式、连续状态演化和离散切换条件的混成 agent；多个机器人再通过并行组合、共享信息和协调 agent 形成团队。

### 核心抽象

结合论文对 `CHARON` 的 agent/mode 结构描述，可保守整理出如下对象：

$$
\mathcal{H} = (A, M, V_d, V_a, T, F, I)
$$

上式中的符号逐项解释如下：

1. `A` 是 agent 集合，例如 coordination agent、robot-group agent、robot agent、sensor/actuator sub-agent。
2. `M` 是 mode 集合，每个 mode 都可再嵌套子 mode。
3. `V_d` 是离散变量集合，例如 `role`、`wallDetected`、`obstacleDetected`。
4. `V_a` 是模拟量变量集合，例如位置、朝向、速度和角速度。
5. `T` 是带守卫和动作的 mode 迁移集合。
6. `F` 是每个 mode 内的连续流约束、代数约束和外部函数。
7. `I` 是各 mode 或 agent 层级上的 invariants。

论文显式给出机器人在控制模式 `q` 下的连续行为：

$$
\dot{\mathbf{x}} = f_q(\mathbf{x}, \mathbf{u}), \quad \mathbf{u} = k_q(\mathbf{x}, \mathbf{z}), \quad q \in Q
$$

上式中的符号逐项解释如下：

1. `\mathbf{x}` 是机器人连续状态向量。
2. `\mathbf{u}` 是控制输入向量。
3. `\mathbf{z}` 是传感器或通信渠道提供的外部信息。
4. `Q` 是有限控制模式集合。
5. `f_q` 表示 mode `q` 下的状态演化方程。
6. `k_q` 表示 mode `q` 下的控制律。

离散切换可保守写成：

$$
\mathrm{enabled}(q \rightarrow q') \iff guard_{q,q'}(\mathbf{z}, V_d)
$$

其中：

1. `guard_{q,q'}` 是由事件、布尔检测量或角色变量组成的迁移条件。
2. 只有当前 mode 为 `q` 且守卫满足时，才允许切换到 `q'`。

### 一个最小例子与通俗解释

论文给出的最直观例子是 leader/follower 双机器人：

1. `ControllerTop` 下有 `LeaderMode` 与 `FollowerMode` 两个子 mode。
2. 若 `role == lead`，机器人进入 leader；若 `role == follow`，进入 follower。
3. 在 leader 内部，`goToGoal`、`wallFollowing`、`obstacleAvoidance` 三个子 mode 之间根据 `wallDetected` 与 `obstacleDetected` 切换。
4. follower 则根据 leader 的位置、姿态和速度执行 separation-bearing control。

通俗地说，`CHARON` 像“给每台机器人装上一棵带连续动力学的层次状态机树”，树上每个节点既能写状态切换，也能写微分方程，多台机器人的树还能再并行拼起来。

### 运行 / 接受 / 转移语义

论文中的关键直觉是：当前激活 mode 决定连续演化方程，而守卫迁移决定何时更换控制律。对 follower，附录给出了一个直接的不变式：

$$
|l-l_d| \le \delta_L \land |\psi-\psi_d| \le \delta_{\Psi}
$$

上式中的符号逐项解释如下：

1. `l` 是当前 leader-follower 距离。
2. `l_d` 是期望距离。
3. `\psi` 是当前相对方位。
4. `\psi_d` 是期望相对方位。
5. `\delta_L` 与 `\delta_{\Psi}` 是允许偏差。

若处于 follower mode，则还会执行例如下式的连续控制：

$$
\dot{x} = v \cos(\theta), \quad \dot{y} = v \sin(\theta), \quad \dot{\theta} = \omega
$$

其中：

1. `x,y` 是机器人位置。
2. `v` 是线速度。
3. `\theta` 是朝向。
4. `\omega` 是角速度。

### 语义边界

这篇论文的 `CHARON` 使用边界很明确：

1. 强项是层次行为切换、并行 agent、连续控制律和通信协同。
2. 它是面向运行时架构和控制构造的语言，不是开放交换标准。
3. 论文本身没有给出一般可判定子类，而是强调工程建模和后续 reachability analysis 方向。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| agent/mode 骨架 | `$\mathcal{H} = (A, M, V_d, V_a, T, F, I)$` | `CHARON` 同时编码结构层级、行为层级与连续约束。 |
| 连续动力学 | `$\dot{\mathbf{x}} = f_q(\mathbf{x}, \mathbf{u}),\ \mathbf{u} = k_q(\mathbf{x}, \mathbf{z})$` | 当前 mode 选定控制律与状态演化。 |
| 模式切换 | `$\mathrm{enabled}(q \rightarrow q') \iff guard_{q,q'}(\mathbf{z}, V_d)$` | 守卫条件触发 leader/follower、避障/沿墙等切换。 |
| 跟随约束 | `$|l-l_d| \le \delta_L \land |\psi-\psi_d| \le \delta_{\Psi}$` | follower mode 用 invariant 保持期望编队几何关系。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `mode` 是核心抽象，且支持嵌套和默认 entry/exit。 |
| 事件 / 触发 | 强支持 | 切换由角色变量、传感器检测量和通信条件触发。 |
| 守卫 / 数据 | 强支持 | 布尔守卫、共享变量、局部变量和外部函数都进入切换逻辑。 |
| 层次 | 强支持 | agent 层次和 mode 层次同时存在。 |
| 并发 / 同步 | 强支持 | 支持 agent 并行组合以及 estimator/control 并发。 |
| 时间约束 | 部分支持 | 依赖连续流和 invariant，不是显式 clock automata。 |
| 连续动态 / 随机性 | 强支持 / 不支持 | 强支持连续动力学和代数约束；原文未涉及随机性。 |
| 可执行 / 可验证性 | 强支持 | 已落到多线程实时架构，形式语义可支撑后续 reachability analysis。 |

### 形式化问题与性质

1. 机器人团队被看成并行 agent 组合，而不是单个大状态机。
2. mode 内允许写 differential constraints、algebraic constraints 和 invariants。
3. 默认 entry/exit、history retention 和 weak pre-emption 使它比平面 `FSM` 更适合复杂机器人协同。
4. 论文明确把 reachability analysis 作为下一步，而不是在本文中给出普适可判定性结论。

## 构造方式与承载格式

### 建模入口

建模入口分为两层：

1. 体系结构层用 `agent` 描述机器人组、协调器、控制器、估计器和硬件接口。
2. 行为层用 `mode` 描述 leader/follower、避障、沿墙、跟随等控制模式。

### 机器可处理承载方式

原文给出了可直接执行和复用的 `CHARON` 文本代码骨架，包括：

1. `agent` 声明和实例化。
2. `mode` 定义、默认迁移、显式 `trans` 规则。
3. `diff`、`alge`、`inv` 约束。
4. 外部 `Java` 函数声明。

### 交换与互操作

`CHARON` 更像研究型 DSL 与软件架构中间表示，而不是开放 XML/JSON 交换格式。论文没有给出跨工具交换标准，但给出了稳定的文本承载方式和代码生成方向。

## 配套基础设施

- 建模/编辑工具：原文核心是 `CHARON` 文本语言和与之对应的软件对象架构。
- 解析/交换/元模型支持：通过 agent/mode 语法、共享变量和通信通道形成可解析结构；原文未说明独立元模型标准。
- 仿真/执行支持：多线程实时软件架构、视觉估计器、控制器模块和机器人平台共同构成执行环境。
- 验证/分析支持：论文强调形式语义与 reachability analysis 潜力，但未给出现成模型检查器。
- 代码生成/转换支持：作者明确提到正在从高层语言自动生成控制与仿真代码。
- 标准化或社区生态：依托 `CHARON` 与 hybrid systems 理论线，工程生态偏研究型。

## 适用场景与需求前提

### 适用场景

适合多机器人协同、编队保持、避障、协同定位、协同操纵和其他带离散行为切换的物理系统控制任务。

### 需求前提

1. 需求能够明确分解为有限行为模式。
2. 每个模式下存在可写成微分/代数约束的连续控制律。
3. 系统需要显式表示通信、共享信息或多 agent 并行。
4. 希望把高层 deliberative 行为与低层 reactive 行为放进同一层次框架。

### 不适用或高成本场景

如果问题只需要纯离散协议分析、开放标准交换或简单业务流程，`CHARON` 会显得过重；若目标是成熟工业标准互操作，它也不如 `SCXML`、`UML` 等载体直接。

## 与相邻形式主义的关系

相对经典 `Hybrid Automata`，它把 agent 层次和软件架构写得更具体；相对 `Statecharts`，它显式加入连续动力学和代数约束；相对行为式机器人架构，它把 mode 切换与形式语义收束在同一语言里。

## 与本研究的关系

### 对 Project 1 的价值

它提供了一个很强的“应用侧证据”：当目标系统是真实物理控制对象时，层次状态机需要和连续动力学、通信结构、估计器/控制器分层一起生成，而不是只生成平面图。

### 作为目标形式主义还是中间表示

对多机器人或混成控制任务，它可以直接作为目标形式主义；在更一般的研究链中，也很适合作为从需求状态机走向混成控制模型的后端表示。

### 对需求到模型生成的启发

如果需求中反复出现“角色切换”“避障/跟随/到点”“共享感知”“编队几何约束”这类词，直接生成为 agent+mode 的混成结构，比单一 `FSM` 更贴近最终实现。

### 现实限制

论文给出的基础设施偏研究原型，缺乏广泛工业标准和公开交换格式；若要接入常见工具链，通常还需要额外翻译。

## 重要的相关工作

### 奠基或前身工作

- `Hybrid Automata`
- `Statecharts`
- 行为式机器人控制与 subsumption 传统

### 同类型或同家族工作

- `CHARON` 语言本体论文
- 多 agent hybrid control programs
- 分层机器人架构如 `3T`、`CLARAty`

### 标准 / 格式 / 工具链工作

- `CHARON` 文本 DSL 与附录代码
- 后续 code generation / reachability analysis 路线

### 与本研究关系最紧的工作

- 它展示了状态机在多智能体物理系统里的真实落点：不仅要表达状态切换，还要同时表达连续控制和通信结构。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`CHARON` / multi-robot coordination architecture
- 论文角色：应用框架 / 软件架构
- 核心功能：把多机器人控制模式、连续动力学和通信协调统一进层次化混成状态机架构。
- 关键特性：agent/mode 双层次、并行组合、连续流约束、共享信息触发切换。
- 构造方式：`CHARON` 文本 DSL + `diff/alge/inv` 约束 + 多线程软件对象架构。

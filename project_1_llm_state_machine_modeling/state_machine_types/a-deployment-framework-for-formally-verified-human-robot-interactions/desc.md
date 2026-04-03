# 面向形式化验证人机交互的部署框架 / A Deployment Framework for Formally Verified Human-Robot Interactions

## 基本信息

- 标题：A Deployment Framework for Formally Verified Human-Robot Interactions
- 中文标题：面向形式化验证人机交互的部署框架
- 作者：Livia Lestingi，Mehrnoosh Askarpour，Marcello M. Bersani，Matteo Rossi
- 发表：*IEEE Access*，9:136616-136635，2021
- DOI：`10.1109/ACCESS.2021.3117852`
- 链接：https://doi.org/10.1109/ACCESS.2021.3117852
- 形式主义：`Stochastic Hybrid Automata (SHA) Network / Model-to-Code Deployment Framework`
- 主类：🌊 混成/随机扩展
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：助残/医疗场景人机交互部署框架 / `SHA` 到 `ROS` 部署单元的模型到代码映射
- 工具/实现获取方式：原文明确使用 `UPPAAL SMC`、`ROS`、`CoppeliaSim` 和 `TurtleBot3` 相关部署链，论文给出部署架构与映射规则；原文未提供独立公开仓库。
- 标准/格式获取方式：承载方式是 `SHA` network、`ROS` topics、deployment unit 映射函数和 simulation/deployment workflow；原文未给统一交换标准。

## 简报

这篇论文处理的是一个在机器人研究里很少被真正打通的问题：设计时用形式化模型证明的人机交互任务，如何不丢语义地落到 `ROS` 部署与 3D 仿真里。作者把服务机器人、人体疲劳、电池、控制器和网络延迟统一建成 `SHA` network，在设计时用 `UPPAAL SMC` 估计 mission success 概率，再把其中一个可部署子集自动翻译成 `ROS` 节点、topics 和 agent scripts，形成“分析 -> 代码 -> 真实/虚拟验证”的闭环。

- 形式主义定位：这是混成/随机扩展主干上的应用型条目，核心价值是给 `SHA` 提供了面向 assistive robotics 的 model-to-code deployment bridge。
- 构造方式简述：先用 `SHA` 网络建模 humans、robot、battery 和 orchestrator，再定义从 `HA` 子集到 deployment unit 的映射函数，最后通过 `ROS` middleware 和模拟器执行。
- 基础设施与场景简述：依托 `UPPAAL SMC`、`ROS`、`CoppeliaSim` 和可穿戴传感/移动机器人平台，服务于医疗辅助、服务机器人和 human-in-the-loop 场景。

```text
interactive mission specification -> SHA network + SMC -> mapping function to deployment units -> ROS middleware / simulation -> runtime validation and model refinement
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 基础 `Hybrid Automaton`。
2. 在其上增加随机时延与随机转移的 `Stochastic Hybrid Automaton`。
3. 由 robot、human、battery、orchestrator 组成的 `SHA` network。
4. 用于发布命令与感知数据的 `ROS` middleware layer。
5. 从 `HA` 子集到 deployment unit 的映射函数。

### 核心抽象

论文首先给出 `HA` 的定义：

$$
A = (L, W, F, I, C, E, l_{ini})
$$

上式中的符号逐项解释如下：

1. `L` 是 locations 集合。
2. `W` 是实值变量集合，其中 clocks、dense counters 和 constants 都是特例。
3. `F` 是给各 location 赋 flow conditions 的函数。
4. `I` 是给各 location 赋 invariants 的函数。
5. `C` 是 channels 集合。
6. `E` 是边集合，边上带 guards、updates 和同步标签。
7. `l_{ini}` 是初始位置。

在此基础上，论文把 `SHA` 定义为：

$$
A_s = (A, \mu, P_{*,c})
$$

上式中的符号逐项解释如下：

1. `A` 是底层的 `HA`。
2. `\mu` 为各状态分配时间延迟的概率测度。
3. `P_{*,c}` 描述在 channel `c` 上满足 guard 后转向不同 location 的概率。
4. 因而 `SHA` 不仅有混成流和离散切换，还显式建模时间延迟和转移结果的不确定性。

论文中 robot 的连续动力学以 flow conditions 形式给出，例如速度 `V` 的分段演化：

$$
\dot{V} =
\begin{cases}
a_{max} & xhop_i = rstart \\
0 & xhop_i = rmov \\
-a_{max} & xhop_i = rstop
\end{cases}
$$

上式中的符号逐项解释如下：

1. `V` 是机器人速度变量。
2. `a_{max}` 是最大加速度常量。
3. `rstart / rmov / rstop` 分别对应加速、巡航和减速操作位置。
4. 这说明模型不是纯 timed automata，而是真正含 continuous dynamics 的 hybrid model。

论文还定义了从 `HA` 到部署单元的映射函数。按文意可保守记为：

$$
\mathbf{1}: A \mapsto D
$$

$$
D = (\Sigma, \Gamma, \Omega, S, T, B, \sigma_{ini})
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是 agent states 集合。
2. `\Gamma` 是部署侧变量集合，含 sensors、constants、clocks 和 physical variables。
3. `\Omega` 是物理规律或其仿真实现。
4. `S` 是条件表达式集合。
5. `T` 是 `ROS` topics 集合。
6. `B` 是控制流语句 / callback 规则集合。
7. `\sigma_{ini}` 是初始部署状态。
8. 这一定义对应原文 deployment unit 的结构化软件实体。

### 一个最小例子与通俗解释

论文里的 running example 是一个医疗辅助场景：

1. 两个 humans 需要 robot 提供不同服务，一个是 Human-Follower，另一个是 Human-Leader。
2. 机器人、电池和人体疲劳都在模型中显式存在。
3. 设计时先用 `SHA` network 和 `SMC` 估计“在时限内成功服务所有人”的概率。
4. 如果结果满意，再把该模型映射成 `ROS` topics、publisher/subscriber、agent scripts，并在 `CoppeliaSim` 里执行。

通俗地说，这像“先把机器人、人和电池都建成会流动、会随机延迟的混成状态机，再自动翻译成 `ROS` 系统”。这样设计时验证过的结构不会在部署时完全走样。

### 运行 / 接受 / 转移语义

论文中的系统运行有两层语义：

1. 形式模型层：
   - `SHA` 中每个状态 `(l, \nu)` 同时带 location 和变量赋值。
   - 时间延迟由 `\mu` 决定，离散切换结果由概率权重 `P_{*,c}` 决定。
2. 部署层：
   - controllable switch 映射为 orchestrator 通过 `ROS` topic 下发命令。
   - uncontrollable switch 对应物理量达到 guard / invariant 边界后触发的状态改变。

因此，该框架不是简单 code generation，而是把 formal model 中的同步、计时、流条件和随机成分分摊到 `ROS` nodes、queue models 和物理/用户输入上共同实现。

### 语义边界

这篇论文的边界主要在于：

1. 可直接部署的是 `SHA` 的一个受限子集，不是任意 hybrid/stochastic model。
2. 只有 human behavior 和 ROS queue delay 等部分真正利用了随机特性，其余许多 automata 实际退化为纯 `HA`。
3. 真实部署仍依赖具体机器人厂家和硬件接口。
4. human 自主行为在 formal model 里只能被近似，而不能完全精确预测。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `HA` 定义 | `$A = (L, W, F, I, C, E, l_{ini})$` | 给 deployment approach 奠定混成自动机基础。 |
| `SHA` 定义 | `$A_s = (A, \mu, P_{*,c})$` | 在 `HA` 上加入随机时延与概率切换。 |
| 速度 flow 条件 | `$\dot{V} = a_{max}, 0, -a_{max}$` | 机器人运动是连续流，不是纯离散跳转。 |
| 映射函数 | `$\mathbf{1}: A \mapsto D$` | 把 formal model 变成可部署软件单元。 |
| 部署单元 | `$D = (\Sigma, \Gamma, \Omega, S, T, B, \sigma_{ini})$` | 描述 `ROS` 侧的状态、变量、topics 与控制规则。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | robot、human、battery、controller 均有显式 locations。 |
| 事件 / 触发 | 强支持 | 命令、传感更新、用户动作和队列事件都可触发跳转。 |
| 守卫 / 数据 | 强支持 | guards、dense counters、sensor readings 和 physical variables 全都显式存在。 |
| 层次 | 部分支持 | 系统按 agent/network 分解，但不是层次状态机。 |
| 并发 / 同步 | 强支持 | 多 automata 通过 channels 和 `ROS` topics 协同。 |
| 时间约束 | 强支持 | clocks、polling 周期、bounded/unbounded delays 都被显式建模。 |
| 连续动态 / 随机性 | 强支持 | 这是本文的核心。 |
| 可执行 / 可验证性 | 强支持 | 既能做 `UPPAAL SMC`，又能部署到 `ROS`/仿真环境。 |

### 形式化问题与性质

1. 论文真正补出的不是某个单一 `SHA` 应用，而是“混成/随机模型怎样可靠地过桥到 `ROS` 部署”。
2. 它说明服务机器人里 human autonomy、battery discharge、network delays 这三类因素可以被统一进 `SHA` network。
3. 部署闭环让 design-time verification 和 run-time validation 不再割裂。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 描述场景配置、交互模式和服务流程。
2. 生成 humans、robot、battery 和 orchestrator 的 `SHA`。
3. 为连续变量写 flow conditions，为随机部分写 delay/outcome distributions。
4. 做 `SMC` 评估任务成功概率与关键物理变量。
5. 若通过，则把 deployable 子集映射到 `ROS` deployment units。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `SHA` network。
2. `UPPAAL SMC` 模型与性质。
3. `ROS` topics / publishers / subscribers。
4. `CoppeliaSim` 中的 agent scripts 和 queue automata。

### 交换与互操作

互操作重点在：

1. formal channels 如何映射到 `ROS` topics。
2. clocks 和 sensor polling 如何转成 deployment-time variables 与 sleep/polling 机制。
3. human stochasticity 在 formal model 中如何由真实用户输入或传感推断替换。

## 配套基础设施

- 建模/编辑工具：`UPPAAL SMC` 与作者的 model-driven configuration workflow。
- 解析/交换/元模型支持：有显式的 model-to-code mapping principle，但无独立统一元模型标准。
- 仿真/执行支持：`ROS`、`CoppeliaSim`、TurtleBot3 相关部署链。
- 验证/分析支持：统计模型检查、success probability 区间估计、关键变量期望值分析。
- 代码生成/转换支持：支持把 deployable `SHA` 子集转成 `ROS` 节点与 scripts。
- 标准化或社区生态：依托 `ROS`、`UPPAAL` 和服务机器人中间件生态。

## 适用场景与需求前提

### 适用场景

适合 assistive robotics、医疗辅助、人机交互导引、服务机器人任务以及需要把 formal model 真正部署出去的混成/随机控制应用。

### 需求前提

1. 场景可分解为 humans、robot、battery、controller 等有限 agents。
2. 关键物理量可被写成 flow conditions 或离散更新。
3. 随机因素主要集中于 human behavior、通信延迟或任务完成时间。
4. 目标不仅是验证，还要后续仿真/部署。

### 不适用或高成本场景

如果系统完全没有连续动力学和随机成分，只做纯离散协议，采用 `SHA` 部署桥反而会过重。

## 与相邻形式主义的关系

相对 [Formal Verification of ROS-Based Robotic Applications Using Timed-Automata](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)，本文强调 human behavior、battery 和部署桥，因此需要 `SHA` 而不只是 `TA`；相对 [A Hybrid Automata Approach for Monitoring the Patient in the Loop in Artificial Pancreas Systems](../a-hybrid-automata-approach-for-monitoring-the-patient-in-the-loop-in-artificial-pancreas-systems/desc.md)，这里更强调 deployment framework 而不是单一医疗监测模型；相对 [A Hybrid Systems-Based Hierarchical Control Architecture for Heterogeneous Field Robot Teams](../a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md)，这里更关注服务机器人 HRI 与 code generation。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果未来想做“需求 -> 模型 -> 验证 -> 部署 -> 回流修正”的闭环，单有验证还不够，模型还要能映射到真实执行架构。

### 作为目标形式主义还是中间表示

对 HRI/CPS 场景，它可以作为目标形式主义之一；对一般控制系统研究，它更像高保真中间表示和部署桥。

### 对需求到模型生成的启发

1. 需求里涉及 human fatigue、battery、motion profile 时，应优先考虑混成/随机扩展而不是普通状态机。
2. 模型生成时最好同步标注哪些子模型未来需要部署，哪些只用于分析。
3. “formal model 的随机近似”和“真实人类输入”的差异应被视为后续修模入口。

## 重要的相关工作

- [Formal Verification of ROS-Based Robotic Applications Using Timed-Automata](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)：纯 `TA` 路线上的 `ROS` 验证。
- [A Hybrid Automata Approach for Monitoring the Patient in the Loop in Artificial Pancreas Systems](../a-hybrid-automata-approach-for-monitoring-the-patient-in-the-loop-in-artificial-pancreas-systems/desc.md)：医疗场景里的混成自动机应用。
- [A Hybrid Systems-Based Hierarchical Control Architecture for Heterogeneous Field Robot Teams](../a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md)：田间多机器人混成控制架构。
- [A Human Operator Model for Medical Device Interaction Using Behavior-Based Hybrid Automata](../a-human-operator-model-for-medical-device-interaction-using-behavior-based-hybrid-automata/desc.md)：人的行为进入混成模型的另一路线。

## 文献分类总结

- 这是一篇 `🌊` 类应用型条目，核心价值是把 `SHA` 网络、统计验证和 `ROS` 部署桥接成一个闭环。
- 它描述的是 human-robot interaction 场景中的物理与生理变量，因此记为 `🌡️`；研究语境同样属于 `CPS / 物理系统建模`，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它最重要的启发是：形式模型若想进入“验证后继续修正”的研究主线，最好从一开始就保留可部署语义。

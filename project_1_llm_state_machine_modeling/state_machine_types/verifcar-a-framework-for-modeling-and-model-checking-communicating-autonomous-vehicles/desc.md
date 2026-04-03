# 面向通信型自动驾驶车辆的定时自动机验证框架 / VerifCar: a framework for modeling and model checking communicating autonomous vehicles

## 基本信息

- 标题：VerifCar: a framework for modeling and model checking communicating autonomous vehicles
- 中文标题：面向通信型自动驾驶车辆的建模与模型检验框架
- 作者：Johan Arcile, Raymond Devillers, Hanna Klaudel
- 发表：*Autonomous Agents and Multi-Agent Systems*, 33(3):353-381, 2019
- DOI：`10.1007/s10458-019-09409-x`
- 链接：https://doi.org/10.1007/s10458-019-09409-x
- 形式主义：`Timed Automata Network for Communicating Autonomous Vehicles`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：自动驾驶通信决策 / 定时自动机应用框架与模型检验
- 工具/实现获取方式：原文明确使用 `UPPAAL`，并给出 `VerifCar` 源材料入口 `https://forge.ibisc.univ-evry.fr/jarcile/VerifCar/`。
- 标准/格式获取方式：承载方式是环境自动机、车辆/基础设施自动机、时钟、broadcast channel、离散化后的车辆状态和指标计算；无独立交换格式。

## 简报

这篇论文的关键贡献，不在于又把车辆画成几个 box，而是在自动驾驶通信场景下，给出了一套可跑模型检验的 `Timed Automata` 网络骨架。作者把环境采样、车辆决策、广播通信、协商和路侧基础设施都压进一个 `TA` 网络里，再用 `CTL/TCTL` 风格查询去评估安全、效率、交通流畅性，以及通信延迟和故障注入对决策算法的影响。

- 形式主义定位：面向 communicating autonomous vehicles 的定时自动机应用框架，不是纯协议模型，也不是纯车辆动力学模型。
- 构造方式简述：先离散化道路和车辆状态，再用一个环境自动机加多个 agent 自动机表示 update / decision / communication 周期。
- 基础设施与场景简述：依托 `UPPAAL`、broadcast synchronization、predicted timed trajectories、`TTC` 指标和 `VerifCar` 源材料，服务自动驾驶关键场景验证。

```text
road + vehicle state abstraction + communication delays -> timed automata network -> CTL/TCTL queries + indicators -> safety / robustness / fluidity assessment
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. 道路离散坐标和车道拓扑。
2. 车辆的离散位置、纵向/横向速度、加速度和邻居知识。
3. 表示环境更新节拍的环境自动机。
4. 表示每辆车或基础设施 agent 的决策/通信自动机。
5. 时钟、broadcast channel 与通信延迟参数。
6. 用于评价安全的 `TTC` 等指标。

### 核心抽象

原文没有把 `VerifCar` 写成一个单一元组，下面给出基于正文定义的保守整理：

$$
\mathcal{V} = (A_0, A_1, \ldots, A_n,\ C_0, C_1, \ldots, C_n,\ k,\ update,\ decision,\ communicate)
$$

上式中的符号逐项解释如下：

1. `A_0` 是环境自动机。
2. `A_i` 是第 `i` 个 agent 自动机，可以是车辆，也可以是基础设施。
3. `C_0,\ldots,C_n` 是与各自动机绑定的 clocks。
4. `k` 是 broadcast channel。
5. `update`、`decision`、`communicate` 是在迁移上触发的动作函数。

这不是原文逐字给出的总元组，而是对其框架组件的保守汇总；原文直接给出的，是环境模板和 agent 模板的结构。

环境自动机 `A_0` 的关键时间约束是：

$$
C_0 \le S,\qquad C_0 \ge S
$$

上式中的符号逐项解释如下：

1. `C_0` 是环境更新时钟。
2. `S` 是环境更新周期。
3. 当 `C_0 \ge S` 时触发 `update()` 并重置 `C_0`。

对每个 agent 自动机 `A_i`，决策节拍与通信延迟分别满足：

$$
C_i \le freq_i,\qquad C_i \ge freq_i
$$

$$
C_i \le MIN\_comm\_delay_i,\qquad C_i \ge MAX\_comm\_delay_i
$$

上式中的符号逐项解释如下：

1. `C_i` 是 agent `i` 的本地时钟。
2. `freq_i` 是 agent 做决策的固定周期。
3. `[MIN\_comm\_delay_i, MAX\_comm\_delay_i]` 是通信从发送到被接收的非确定时间区间。
4. 因此 `VerifCar` 的时间结构不是一条全局大钟，而是环境更新和各 agent 周期共同作用。

### 一个最小例子与通俗解释

最小直觉例子可以理解成两辆接近路口的车：

1. 每辆车都周期性读取自己和邻居的状态。
2. 决策模块给出“保持车道”“变道”“减速”等动作意图。
3. 该意图先通过 broadcast 通知其他车辆，但接收有不确定延迟。
4. 环境自动机随后更新所有车辆的位置和速度，再检查是否出现冲突或过小的 `TTC`。

通俗地说，`VerifCar` 像是在 `UPPAAL` 里搭了一个“交通仿真骨架”，但与普通仿真不同，它把“延迟可能多大、哪种竞争次序会发生、会不会刚好导致危险”都纳入了穷尽式检查。

### 运行 / 接受 / 转移语义

原文明确说明所有 agent 通过 broadcast 同步：

$$
k! \Rightarrow \text{all available } k? \text{ transitions fire simultaneously}
$$

上式中的符号逐项解释如下：

1. `k!` 是环境自动机或某个 agent 发出的 broadcast 发送。
2. `k?` 是其他 automata 上可用的接收迁移。
3. 同步发生意味着中间没有别的动作插入，也没有时钟推进。

安全指标方面，论文用二维 `TTC` 检查碰撞风险。保守整理后，其核心判定可写成：

$$
TTC(A,B) = \inf \{\, t \ge 0 \mid I_x(t) \cap I_y(t) \neq \emptyset \,\}
$$

上式中的符号逐项解释如下：

1. `A,B` 是两辆车。
2. `I_x(t)` 是它们在 `x` 方向上可能发生矩形重叠的时间区间。
3. `I_y(t)` 是 `y` 方向上的对应时间区间。
4. 若两个时间区间有交，左边界就是 `TTC`；若无交，则视为 `+\infty`。

在验证层，论文以 `CTL` 风格查询表达目标，例如可以保守写成：

$$
AG(TTC > 0)
$$

或

$$
EF(\text{collision})
$$

上式中的符号逐项解释如下：

1. `AG` 检查所有路径上全局成立的安全性质。
2. `EF` 检查是否存在一条路径最终到达某个坏状态。
3. 这正是 `UPPAAL` 在 `VerifCar` 中承担的角色。

### 语义边界

这篇论文的边界比较清晰：

1. 它抽象掉了车辆精细动力学和车体旋转，只保留离散网格上的位置、速度与加速度。
2. 重点是通信延迟、决策频率和交通冲突，而不是底层控制器设计。
3. 车辆知识通过紧凑变量编码，不存完整轨迹历史。
4. 框架适合少量车辆的关键情境穷尽验证，不适合大规模交通微观仿真。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 环境更新周期 | `$C_0 \le S,\ C_0 \ge S$` | 控制离散环境采样节拍。 |
| agent 决策周期 | `$C_i \le freq_i,\ C_i \ge freq_i$` | 保证车辆按固定频率重算动作。 |
| 通信延迟 | `$[MIN\_comm\_delay_i, MAX\_comm\_delay_i]$` | 显式建模广播消息延迟。 |
| broadcast 语义 | `$k! / k?$` | 环境更新优先于并发 decision。 |
| 预测轨迹 | timed trajectories | 用少量变量编码未来意图。 |
| 安全指标 | `$TTC(A,B)$` | 用于 safety/robustness 查询。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 环境状态和 agent 本地状态都由 automata locations 与变量承载。 |
| 事件 / 触发 | 强支持 | update、decision、communication 都是显式触发。 |
| 守卫 / 数据 | 强支持 | guards 大量依赖 clocks、位置、速度和邻居知识。 |
| 层次 | 弱支持 | 主要是并列 automata 网络，不强调层次状态机。 |
| 并发 / 同步 | 强支持 | broadcast synchronization 是主体。 |
| 时间约束 | 强支持 | 周期、延迟、指标采样都由时钟约束表达。 |
| 连续动态 / 随机性 | 弱连续、弱随机 | 物理量被离散化；非确定性来自 delay 和决策竞争。 |
| 可执行 / 可验证性 | 强验证 | 直接面向 `UPPAAL` 查询与指标计算。 |

### 形式化问题与性质

1. 论文真正补出的，是“如何把通信型自动驾驶系统压成可检验的 `TA` 网络”，而不是单篇场景脚本。
2. 使用 broadcast 而不是 handshake，显著减少了中间无意义状态。
3. 通过 `TTC`、robustness、fluidity 等指标，模型不只检查“会不会撞”，还可比较决策策略优劣。
4. 因此它是 `Timed Automata` 主干在自动驾驶通信验证方向上的强应用侧证。

## 构造方式与承载格式

### 建模入口

建模入口通常是：

1. 离散化道路和车辆位置。
2. 为每辆车定义状态记录、目标路线和邻居知识变量。
3. 用 `A_i` 建模周期决策与通信。
4. 用 `A_0` 建模全局环境更新。
5. 选择 `CTL/TCTL` 查询和指标函数进行模型检验。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `UPPAAL` timed automata templates。
2. clocks 与 broadcast channel。
3. 预测 timed trajectories 的紧凑编码。
4. `TTC`、robustness、traffic fluidity 等指标。

### 交换与互操作

互操作重点在：

1. 车辆如何通过 broadcast 交换意图。
2. 基础设施 agent 如何共享同一自动机骨架。
3. 离散化车辆状态如何支撑后续 query 与指标计算。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：以 timed-automata 模板和代码变量为主，无独立交换标准。
- 仿真/执行支持：重点是模型检查，不是高保真连续仿真。
- 验证/分析支持：`CTL/TCTL` 风格查询、`TTC`、fault injection、negotiation/infrastructure variants。
- 代码生成/转换支持：原文未提供从模型到控制代码的自动生成。
- 标准化或社区生态：`Timed Automata` 与 `UPPAAL` 生态成熟；论文给出 `VerifCar` 源材料入口。

## 适用场景与需求前提

### 适用场景

适合车道变换、并线、路口、环岛等少量车辆关键情境下的决策策略验证，尤其适合研究通信延迟、协商和基础设施辅助对安全与效率的影响。

### 需求前提

1. 车辆状态可以接受离散化。
2. 决策是周期性的，且通信延迟可参数化。
3. 验证重点在高层决策与冲突，而不是底层控制律精度。
4. 查询目标可以写成安全、可达性或指标阈值性质。

### 不适用或高成本场景

若要验证大规模路网、连续高精度车辆动力学或感知噪声分布，`VerifCar` 这种离散化 `TA` 网络会很快遇到状态爆炸和建模精度瓶颈。

## 与相邻形式主义的关系

相对 [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)，本文从通信总线提升到了通信型自动驾驶系统；相对 [multi-robot-planning-a-timed-automata-approach/desc.md](../multi-robot-planning-a-timed-automata-approach/desc.md)，它额外把广播延迟、协商和路侧基础设施纳入模型；相对 [transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)，它更偏运行中多车交互验证，而不是计划后处理。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求里同时包含周期决策、显式通信和时间安全约束时，`Timed Automata` 仍然是一个很强的目标或中间表示。

### 作为目标形式主义还是中间表示

对高层自动驾驶决策验证，它可以直接作为目标形式主义；对更完整自动驾驶系统，也可作为“决策与通信层”的中间表示，下接连续控制器。

### 对需求到模型生成的启发

1. LLM 若要生成自动驾驶类状态机，必须显式区分环境更新、agent 决策和消息传播三个时序层。
2. 通信延迟不应只出现在注释里，而要变成时钟和 guard。
3. 需求中若出现“安全距离”“碰撞时间裕量”等指标，应尽早映射成可查询的形式化量。

## 重要的相关工作

- [timed-automata-approach-to-can-verification/desc.md](../timed-automata-approach-to-can-verification/desc.md)：定时自动机在实时通信系统验证中的经典应用。
- [multi-robot-planning-a-timed-automata-approach/desc.md](../multi-robot-planning-a-timed-automata-approach/desc.md)：多机器人规划方向的 `TA` 应用。
- [transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)：机器人计划时序约束修正方向的 `TA` 应用。

## 文献分类总结

- 这是一篇 `⏱️` 类高价值应用条目，核心贡献是把通信型自动驾驶系统压成可检验的 `Timed Automata` 网络框架。
- 其描述客体主要是处于道路环境中的车辆系统，因此记为 `🌡️`；论文语境也明显属于自动驾驶 `CPS`，因此记为 `🌡️`。
- 对 `project_1` 来说，它补足了“周期决策 + 广播通信 + 安全时间指标”这一类需求到 `Timed Automata` 的落地证据。

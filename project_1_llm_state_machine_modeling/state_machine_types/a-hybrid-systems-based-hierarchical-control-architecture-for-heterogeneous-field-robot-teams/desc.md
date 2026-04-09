# 面向异构田间机器人团队的基于混成系统的分层控制架构 / A Hybrid Systems-Based Hierarchical Control Architecture for Heterogeneous Field Robot Teams

## 基本信息

- 标题：A Hybrid Systems-Based Hierarchical Control Architecture for Heterogeneous Field Robot Teams
- 中文标题：面向异构田间机器人团队的基于混成系统的分层控制架构
- 作者：Chanyoung Ju, Hyoung Il Son
- 发表：*IEEE Transactions on Cybernetics*, 53(3):1802-1815, 2023
- DOI：`10.1109/TCYB.2021.3133631`
- 链接：https://doi.org/10.1109/TCYB.2021.3133631
- 形式主义：`Hybrid Automata + Supervisory Control`
- 主类：🌊 混成/随机扩展
- 对象类型：🧪 应用/案例
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：混成系统应用架构 / 分层监督控制
- 工具/实现获取方式：原文明确使用 `MATLAB`、`TCT`、physics-based simulator（`V-REP`）实现高低层控制闭环，并给出 modular supervisor 设计流程。
- 标准/格式获取方式：承载方式是 hybrid automata、DES automata、specification automata 与 modular supervisor；原文未给独立 XML/JSON 交换标准。

## 简报

这篇论文的核心，不是“再给多机器人做一个分层控制框架”，而是把 `CTS + DES + hybrid automata + supervisory control` 真正压成一套能跑在异构田间机器人团队上的控制架构。高层用离散事件和 supervisor 管任务、优先级和安全逻辑，低层用连续控制器管 `UAV/UGV` 的动力学，二者通过信息通道和控制逻辑通道耦合。论文的重点恰恰在这种“连续动力学 + 离散任务逻辑”之间的结构性拼接。

- 形式主义定位：面向异构机器人协作控制的 `Hybrid Automata` 应用框架，而不是单纯的连续控制器设计。
- 构造方式简述：先分别建 `UAV/UGV` 的 hybrid automata plant，再设计六个 behavior specifications，最后综合 modular supervisors 并与低层控制器组成 HSHC。
- 基础设施与场景简述：依托 `MATLAB`、`TCT`、`V-REP`、distributed swarm control 和 modular supervisor，服务农业田间的 `UAV + UGV` 协同 mapping / navigation / obstacle avoidance。

```text
协作任务需求 -> hybrid automata plant + specification automata -> modular supervisor synthesis -> CTS low-level control + DES high-level control -> 物理仿真验证
```

## 形式主义定义与核心对象

### 定义对象

论文同时使用了两层形式化对象：

1. 高层 `DES` automaton，用于 supervisor synthesis。
2. 低层 `CTS` 动力学模型，用于 `UAV/UGV` 连续控制。
3. 把二者接起来的 `Hybrid Automaton`。
4. 针对控制目标设计的 specification automata。
5. 由 `SCT` 求得的 modular supervisors。

### 核心抽象

论文先回顾高层离散 plant 的 automaton：

$$
A = (E, \Sigma, \eta, E_0, E_m)
$$

上式中的符号逐项解释如下：

1. `E` 是离散状态集合。
2. `\Sigma` 是事件集合。
3. `\eta` 是状态转移函数。
4. `E_0` 是初始状态。
5. `E_m` 是 marker states，也就是期望达到的目标状态集合。

随后论文把混成 plant 明确写为：

$$
G_h = (E, X, \Sigma, U, F, \phi, Inv, Guard, \rho, E_0, X_0)
$$

上式中的符号逐项解释如下：

1. `E` 是离散状态集合。
2. `X` 是连续状态集合。
3. `\Sigma` 是事件集合。
4. `U` 是允许的控制输入集合。
5. `F` 是向量场，决定连续状态如何随控制输入演化。
6. `\phi` 是离散状态转移函数。
7. `Inv` 是不变式条件集合，限制某离散状态下连续状态必须满足的条件。
8. `Guard` 是守卫条件集合，决定何时允许离散跳转。
9. `\rho` 是 reset 函数，规定跳转时连续状态如何重置。
10. `E_0` 是初始离散状态。
11. `X_0` 是初始连续状态。

针对整支异构团队，论文把 plant 写成：

$$
G_{plant} = G_A \parallel G_{B1} \parallel G_{B2}
$$

上式中的符号逐项解释如下：

1. `G_A` 是 `UAV` 的 hybrid automaton。
2. `G_{B1}`、`G_{B2}` 是两台 `UGV` 的 hybrid automata。
3. `\parallel` 表示并行组合后的整体 plant。

### 一个最小例子与通俗解释

论文里最直观的最小片段是：

1. `UAV` 在 `A1:Idle`、`A2:Arming`、`A3:Hovering`、`A4:Flying`、`A5:Avoiding` 之间切换。
2. `UGV` 在 `B1:Stationary`、`B2:Navigation`、`B3:Safety`、`B4:Formation` 之间切换。
3. 当 `UGV` 发现障碍物时，事件触发 `B2 -> B3`，high-level supervisor 允许 obstacle avoidance 相关 controllable event。
4. low-level controller 再根据连续距离、速度和期望轨迹去实际完成避障与编队。

通俗地说，这类 hybrid automata 像“上面一个离散调度脑，下面一套连续运动身体”：上层决定“现在该飞、该避障、该编队还是该收尾”，下层负责把这些模式真正变成速度、位置和姿态变化。

### 运行 / 接受 / 转移语义

高层 supervisor 语义由监督控制给出。论文写出受控 plant：

$$
S/A = (X \times A, \Sigma, \delta \times \eta, (x_0, a_0), X_m \times A_m)
$$

上式中的符号逐项解释如下：

1. `S` 是 supervisor automaton。
2. `A` 是 plant automaton。
3. `\delta \times \eta` 表示 supervisor 与 plant 的同步受控演化。
4. `(x_0, a_0)` 是联合初始状态。
5. `X_m \times A_m` 是联合目标状态。

论文对 controllability 给出经典条件：

$$
(\forall s,\sigma)\; s \in L(S),\ \sigma \in \Sigma_{uc},\ s\sigma \in L(A) \Rightarrow s\sigma \in L(S)
$$

上式中的符号逐项解释如下：

1. `L(S)` 是 supervisor 允许的语言。
2. `L(A)` 是 plant 可能产生的语言。
3. `\Sigma_{uc}` 是 uncontrollable events。
4. 含义是：只要 plant 能发生的不可控事件出现了，supervisor 也必须允许它。

论文把 modular supervisor 与 centralized supervisor 的关系写成：

$$
\bar{S} = \bar{S}_1 \wedge \bar{S}_2 \wedge \cdots \wedge \bar{S}_m
$$

上式中的符号逐项解释如下：

1. `\bar{S}` 是集中式 supervisor 的合法语言视角。
2. `\bar{S}_j` 是第 `j` 个 modular supervisor。
3. `\wedge` 是 meet product，也就是语言交汇意义下的联合控制结果。

### 语义边界

这篇论文的边界也很清楚：

1. hybrid automata 主要承担“模式 + 连续条件”的系统建模职责，不做复杂 reachability decidability 分析。
2. supervisor synthesis 只在高层离散事件层进行。
3. 低层控制器仍靠传统连续控制和 swarm control 实现。
4. 论文验证重点是 simulation-based feasibility，而不是对整个 hybrid plant 做符号模型检查。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 离散 plant | `$A = (E, \Sigma, \eta, E_0, E_m)$` | 高层任务逻辑先被写成离散 automaton。 |
| 混成 plant | `$G_h = (E, X, \Sigma, U, F, \phi, Inv, Guard, \rho, E_0, X_0)$` | 同时建模离散模式、连续状态与跳转条件。 |
| 整体团队 | `$G_{plant} = G_A \parallel G_{B1} \parallel G_{B2}$` | `UAV + UGV + UGV` 通过并行组合形成全局 plant。 |
| 受控系统 | `$S/A = (X \times A, \Sigma, \delta \times \eta, (x_0,a_0), X_m \times A_m)$` | supervisor 与 plant 同步形成受控闭环。 |
| 可控性 | `$(\forall s,\sigma)\ s \in L(S),\ \sigma \in \Sigma_{uc},\ s\sigma \in L(A) \Rightarrow s\sigma \in L(S)$` | 不可控事件不能被 supervisor 非法禁止。 |
| 模块化一致性 | `$\bar{S} = \bar{S}_1 \wedge \cdots \wedge \bar{S}_m$` | modular supervisors 应与 centralized supervisor 等价或兼容。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `UAV/UGV` 都有显式离散模式。 |
| 事件 / 触发 | 强支持 | mission received、obstacle detected、free space、network connected 等都是一级对象。 |
| 守卫 / 数据 | 强支持 | 距离、速度、高度和障碍条件进入 guard / invariant。 |
| 层次 | 强支持 | 高层 supervisor 与低层 controller 分层，且 supervisor 可模块化。 |
| 并发 / 同步 | 强支持 | 多机器人并行、formation / network 事件、plant 并行组合。 |
| 时间约束 | 部分支持 | 论文更强调事件与模式，而非 clock automata 风格显式时钟。 |
| 连续动态 / 随机性 | 强连续、无随机 | 连续动力学是核心，随机性不是重点。 |
| 可执行 / 可验证性 | 强执行、强结构验证 | 可综合 modular supervisor，并在 physics-based simulator 中验证。 |

### 形式化问题与性质

1. 论文真正补出的，是“混成系统模型怎样落到可综合的 supervisor 架构”，而不仅是给混成机器人画一张状态图。
2. 它把 `policy -> specification automata -> supremal controllable sublanguage -> modular supervisors` 这条链打通了。
3. `Hybrid Automata` 在这里承担的是结构桥梁角色：把连续 plant 和离散控制目标放在同一框架里。
4. 相比只讲低层控制律的机器人论文，它更接近状态机 / 自动机主干文库所关心的“模式切换与控制逻辑表达”。

## 构造方式与承载格式

### 建模入口

建模入口分成三层：

1. 用 `CTS` 为 `UAV/UGV` 写动力学与低层控制。
2. 用 automata / hybrid automata 为 plant 写离散模式和连续条件。
3. 用 specification automata 表达控制目标、优先级和协作策略。

### 机器可处理承载方式

论文体现出的机器可处理承载方式包括：

1. `GA`、`GB` 等 hybrid automata 图。
2. `H_i` 行为 specification automata。
3. `TCT` 可综合的 supervisor 模型。
4. `MATLAB` 与 simulator 间的 control logic / information channel。

### 交换与互操作

互操作不是开放标准，而是控制架构上的对接：

1. high-level supervisor 通过 control logic channel 驱动 low-level controller。
2. low-level plant 通过 information channel 回传状态、测量值和事件。
3. `TCT`、`MATLAB`、simulator 共同组成可运行的验证闭环。

## 配套基础设施

- 建模/编辑工具：离散模型与 supervisor synthesis 使用 `TCT`，连续控制与系统实现使用 `MATLAB`。
- 解析/交换/元模型支持：原文主要通过自建 hybrid automata / specification 模型与通道接口衔接，未提供开放元模型。
- 仿真/执行支持：physics-based simulator（`V-REP`）用于闭环验证。
- 验证/分析支持：controllability、nonblocking、nonconflictness 检查，以及事件/状态轨迹分析。
- 代码生成/转换支持：原文重点是 supervisor synthesis 与仿真集成，不强调自动代码生成。
- 标准化或社区生态：依托 `SCT`、hybrid systems 和 robotics simulation 生态，工程标准化较弱。

## 适用场景与需求前提

### 适用场景

适合存在“高层任务逻辑 + 低层连续控制”双重结构的多机器人协作系统，例如农业、巡检、灾害响应和异构编队。

### 需求前提

1. 任务可抽成有限个离散模式与可观察事件。
2. 机器人动力学可由连续状态与控制输入表示。
3. 协作目标能够写成 specification automata。
4. 系统允许通过 supervisor 对 controllable events 做使能/禁止。

### 不适用或高成本场景

如果系统没有清晰模式边界、事件集难以定义，或者低层连续控制器本身就不稳定，那么 HSHC 的高层 supervisor 优势很难发挥；对极大规模 hybrid plant，建模和调试成本也会迅速上升。

## 与相邻形式主义的关系

相对 [The Theory of Hybrid Automata](../the-theory-of-hybrid-automata/desc.md)，本文更偏工程实现与 supervisory control；相对 [A Framework and Architecture for Multi-Robot Coordination](../framework-and-architecture-for-multi-robot-coordination/desc.md) 里的 `CHARON`，它更强调 `SCT` 与 modular supervisor，而不是语言/架构层的 mode/agent 设计；相对一般 `FSM` 机器人监督器，它把连续动力学与 guard/invariant 拉进了模型本体。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文给了一个非常直接的证据：当控制系统既有离散协作逻辑，又有连续物理动力学时，目标形式主义不能只停在普通 `FSM`，而需要至少能够桥接 hybrid / supervisory 语义。

### 作为目标形式主义还是中间表示

它更适合作为高复杂度控制系统的目标形式主义或高保真中间表示，而不是最轻量的文档级交付模型。

### 对需求到模型生成的启发

1. 需求生成时应显式区分 policy/specification、离散 plant、连续 plant 与 control channels。
2. 高层控制目标最好先抽为可综合的 specification automata，而不是直接写进低层控制代码。
3. 对 LLM 建模来说，hybrid 场景的关键不是“多写连续公式”，而是把模式、事件、guard 和低层控制接口对齐。

## 重要的相关工作

- [The Theory of Hybrid Automata](../the-theory-of-hybrid-automata/desc.md)：给出混成自动机的理论主干。
- [Hybrid Automata for Formal Modeling and Verification of Cyber-Physical Systems](../hybrid-automata-for-cps/survey.md)：从 `CPS` 视角总结混成模型与工具谱系。
- [A Framework and Architecture for Multi-Robot Coordination](../framework-and-architecture-for-multi-robot-coordination/desc.md)：同样面向多机器人，但更偏 `CHARON` 架构语言。

## 文献分类总结

- 这是一篇 `🌊` 类高价值应用条目，重点在 `Hybrid Automata + Supervisory Control` 如何共同承担异构机器人协作控制。
- 其描述客体是带连续动力学的物理机器人系统，因此记为 `🌡️`；论文语境同样是 `CPS / physical systems`，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它是“普通离散状态机不够时，如何升到 hybrid / supervisory 级别”的典型参考。

# 基于网中网建模与仿真的多机器人运动规划 / Multi-robot Motion Planning based on Nets-within-Nets Modeling and Simulation

## 基本信息

- 标题：Multi-robot Motion Planning based on Nets-within-Nets Modeling and Simulation
- 中文标题：基于网中网建模与仿真的多机器人运动规划
- 作者：Sofia Hustiu, Joaquín Ezpeleta, Cristian Mahulea, Marius Kloetzer
- 发表：*Robotics and Autonomous Systems*, 197:105287, 2026
- DOI：`10.1016/j.robot.2025.105287`
- 链接：https://doi.org/10.1016/j.robot.2025.105287
- 形式主义：`High-Level robot team Petri Net (HLrtPN) / Nets-within-Nets`
- 主类：🕸️
- 描述客体：🏭
- 所属领域：🌡️
- 论文角色：异构多机器人任务规划 / `Nets-within-Nets` 应用形式化
- 工具/实现获取方式：原文明确使用 `Renew` 对 `HLrtPN` 系统建模与仿真；文中给出逐步实现指南，但未附公开仓库。
- 标准/格式获取方式：承载方式是 `SpecOPN`、`RobotOPN`、system net、`GEF` 与 `Renew` 的网中网实现；无独立交换标准。

## 简报

这篇论文的价值，在于它不是再把所有机器人和任务硬压成一个大 `PN`，而是利用 `Nets-within-Nets` 的层次结构，把“机器人网”和“任务规格网”都作为 token 挂到一个更高层的 system net 里。作者把这个框架命名为 `High-Level robot team Petri Net (HLrtPN)`，再用 `Global Enabling Function (GEF)` 保证机器人移动、区域容量和任务规格推进三者同步成立。

- 形式主义定位：面向异构多机器人全局任务规划的 `Petri` 并发模型，不是单机控制器或纯 MILP 规划器。
- 构造方式简述：先把任务公式转成 `SpecOPN`，再为每类机器人建 `RobotOPN`，最后通过 system net 与 `GEF` 做同步。
- 基础设施与场景简述：依托 `Nets-within-Nets`、`Renew`、co-safe `LTL` 与 hospital-style 多机器人任务案例，服务异构团队的高层规划。

```text
co-safe LTL mission + heterogeneous robot models -> SpecOPN / RobotOPN -> system net + GEF -> HLrtPN simulation -> feasible team trajectories
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. `Buchi` 自动机及其 `SpecOPN` 表示。
2. 每类机器人的 `RobotOPN`。
3. 以 object nets 为 token 的 system net。
4. 区域容量多重集 `\mu_{cap}`。
5. 机器人实际占用多重集 `\mu_{occ}`。
6. 用于同步三层语义的 `GEF`。

### 核心抽象

任务规格首先用 `Buchi` 自动机表示：

$$
B = (S, S^0, \Sigma_B, \to_B, F)
$$

上式中的符号逐项解释如下：

1. `S` 是自动机状态集合。
2. `S^0` 是初始状态集合。
3. `\Sigma_B` 是输入字母表。
4. `\to_B` 是迁移关系。
5. `F` 是接受状态集合。

规格对象网被定义为：

$$
\mathrm{Spec} = \langle P, P_f, T, F, \lambda \rangle
$$

其中：

1. `P` 是 place 集合。
2. `P_f` 是 final places。
3. `T` 是 transitions。
4. `F` 是弧集合。
5. `\lambda^\land(t)` 给每个 transition 赋一个关于原子命题的布尔公式。

机器人对象网则写成：

$$
o = \langle P, T, F, h, \lambda, \gamma \rangle
$$

上式中的符号逐项解释如下：

1. `P` 与工作空间 cells 一一对应。
2. `T` 表示机器人可执行的 cell-to-cell 运动。
3. `F` 是弧集合。
4. `h^\land` 给 places 标注区域命题。
5. `\lambda^\land(t_i)=h(t_i^\bullet)^\land`，把运动后到达区域对应的命题贴到转移上。
6. `\gamma: P \to \mathcal{P}` 是 place 到工作空间 cell 的关联函数。

论文的总框架 `HLrtPN` 定义为：

$$
N = \langle \bar P, \bar T, O, S, Vars, \bar F, W, \mu_{cap} \rangle
$$

其中：

1. `\bar P=\{Rb,Ms\}` 分别保存 robot object nets 与 specification net。
2. `\bar T=\{t_1,t_2,\dots,t_s\}` 是 system net transitions。
3. `O` 是全部 `RobotOPN` 系统的集合。
4. `S` 是 `SpecOPN` 系统。
5. `Vars` 是 system net 在弧上绑定 object nets 的变量集合。
6. `W` 是弧 inscription function。
7. `\mu_{cap}` 是各 cell 可同时容纳机器人数的 capacity multiset。

### 一个最小例子与通俗解释

论文用一个非常直观的例子来解释 `HLrtPN`：

1. 任务是 `\Diamond b_3`，即只要有机器人进入绿色区域即可满足。
2. system net 中 place `Rb` 里放多个 `RobotOPN` token，place `Ms` 里放一个 `SpecOPN` token。
3. 某个机器人若从 free space 走到 `y_3` 区域，其 `RobotOPN` 转移、system net 转移和 `SpecOPN` 中标有 `b_3` 的转移必须同步触发。
4. 只有 `GEF` 判定容量、占用和规格条件都满足时，这次同步 firing 才被允许。

通俗地说，这个模型像“上层总控网管着一群会动的小网和一个任务网”，不是谁想走就走，而是得同时满足位置容量和任务逻辑。

### 运行 / 接受 / 转移语义

在状态 `\langle m,\mu_{occ}\rangle` 下，system net transition `t \in \bar T` 的可使能条件可以压缩为：

$$
\mathrm{enabled}(t)
\iff
t^S \text{ enabled in } \mathrm{SpecOPN}
\land
\forall j \le i,\ t^{o_j} \text{ enabled in } o_j
\land
\mathrm{GEF}(\mu_{occ}, \mu_{cap}, t^S, (t^{o_1},\dots,t^{o_i}))=\mathrm{True}
$$

上式中的符号逐项解释如下：

1. `t^S` 是与 system net transition 同步的规格转移。
2. `t^{o_j}` 是第 `j` 个机器人对象网中同步触发的转移。
3. `\mu_{occ}` 记录各原子命题当前有多少机器人占用。
4. `GEF` 是允许真正同步 firing 的总守卫。

`GEF` 的核心检查逻辑可保守整理为：

$$
\chi[P_j] \le \mu_{cap}[P_j],\quad
b_j \in t^S_\land \Rightarrow \mu'_{occ}[b_j] \ge 1,\quad
\neg b_j \in t^S_\land \Rightarrow \mu'_{occ}[b_j]=0
$$

其中：

1. `\chi` 是模拟 firing 之后按 workspace cell 统计的 occupancy multiset。
2. 第一条约束确保任何 cell 都不超容量。
3. 第二条约束确保 `SpecOPN` transition 要求为真的命题在 firing 后确实为真。
4. 第三条约束确保要求为假的命题在 firing 后不会被错误激活。

### 语义边界

这篇论文的边界主要是：

1. 当前只考虑 co-safe `LTL` 任务。
2. 规划解是高层运动序列，默认低层控制器能执行。
3. 方法主体依赖仿真搜索，不保证全局最优。
4. 重点是异构团队与层次建模，不是细粒度连续运动学。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `Buchi` 自动机 | `$B = (S, S^0, \Sigma_B, \to_B, F)$` | 任务公式先进入自动机主干。 |
| `SpecOPN` | `$\mathrm{Spec} = \langle P, P_f, T, F, \lambda \rangle$` | 任务再转成可同步的 Petri 表示。 |
| `RobotOPN` | `$o = \langle P, T, F, h, \lambda, \gamma \rangle$` | 每类机器人各自保留运动能力拓扑。 |
| `HLrtPN` | `$N = \langle \bar P, \bar T, O, S, Vars, \bar F, W, \mu_{cap} \rangle$` | system net + object nets 的总框架。 |
| 同步使能 | `$\mathrm{GEF}(\mu_{occ}, \mu_{cap}, t^S, (t^{o_1},...,t^{o_i}))$` | 真正决定这次团队动作是否允许。 |
| 容量与命题守卫 | `$\chi[P_j] \le \mu_{cap}[P_j]$` 等 | 用容量与任务命题共同约束团队规划。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | system net、任务网和机器人网三层状态同时存在。 |
| 事件 / 触发 | 强支持 | firing 同步与区域命题变化是核心。 |
| 守卫 / 数据 | 强支持 | `GEF`、容量、多重集与命题标签共同决定转移。 |
| 层次 | 强支持 | `Nets-within-Nets` 层次是论文主体。 |
| 并发 / 同步 | 强支持 | 多机器人与任务网同步推进。 |
| 时间约束 | 弱支持 | 当前主线不在显式时间网分析。 |
| 连续动态 / 随机性 | 弱支持 | 低层连续控制被抽象掉，随机性未建模。 |
| 可执行 / 可验证性 | 强执行、强建模 | 可在 `Renew` 中仿真，且结构清晰可追踪。 |

### 形式化问题与性质

1. 论文最重要的增量，是给异构多机器人任务规划补了一个真正分层的 `Petri` 形式。
2. `GEF` 使 `HLrtPN` 不只是“网中网画法”，而是带明确同步语义的规划机制。
3. 相比把所有机器人压成一个平面大网，这个框架更容易随机器人类型扩展。
4. 因而它已经足够稳定，可以视作 `Petri Nets` 主干下的新代表性分支节点。

## 构造方式与承载格式

### 建模入口

建模入口通常是：

1. 先把任务公式转成 `Buchi` 自动机，再转成 `SpecOPN`。
2. 为每类机器人建立 `RobotOPN`。
3. 构造只含 `Rb` 与 `Ms` 的 system net。
4. 定义容量多重集和 `GEF`。

### 机器可处理承载方式

原文直接给出的机器可处理承载方式包括：

1. `SpecOPN` 与 `RobotOPN` 元组。
2. `HLrtPN` 总框架元组。
3. `GEF` 算法输入输出。
4. `Renew` 中的 `Nets-within-Nets` 仿真模型。

### 交换与互操作

互操作重点在：

1. 任务规格网与机器人对象网如何通过 system net 同步。
2. 容量与占用信息如何跨层反馈给 `GEF`。
3. 新增机器人类型时，只需新增对应 `RobotOPN` 而不必重建整个全局模型。

## 配套基础设施

- 建模/编辑工具：`Renew`。
- 解析/交换/元模型支持：依赖 `Nets-within-Nets` 建模环境，无独立交换标准。
- 仿真/执行支持：`Renew` 直接承担仿真与轨迹搜索。
- 验证/分析支持：通过 `GEF` 和 `SpecOPN` 保证任务逻辑与容量约束。
- 代码生成/转换支持：原文未给自动代码生成。
- 标准化或社区生态：依托高层 `Petri` 网和 `Nets-within-Nets` 研究线。

## 适用场景与需求前提

### 适用场景

适合异构多机器人系统、任务需体现同步访问/顺序访问/区域容量限制、且希望保留层次结构的高层规划问题。

### 需求前提

1. 工作空间可离散成有限 cells 或 regions of interest。
2. 任务可写成 co-safe `LTL`。
3. 机器人能力差异主要能体现在可达区域与对象网拓扑上。
4. 低层控制器能执行高层给出的区域间移动。

### 不适用或高成本场景

若系统重点在连续动力学、精细时延或概率不确定性，这套 `HLrtPN` 还需要继续叠加其他形式主义。

## 与相邻形式主义的关系

相对 [Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)，本文显著强化了层次结构和异构机器人建模；相对 [Distributed Petri Nets for Model-Driven Verifiable Robotic Applications in ROS](../distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md)，本文更偏高层任务-机器人同步框架，而不是 `ROS` 结构化验证工具链；相对 [On Multirobot Path Planning Based on Petri Net Models and LTL Specifications](../on-multi-robot-path-planning-based-on-petri-net-models-and-ltl-specifications/desc.md)，本文走 `NwN + simulation`，后者走 `quotient/composed PN + MILP`。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明，当需求天然带有“多主体 + 层次结构 + 区域容量约束”时，`Petri` 主干可以比普通 `FSM` 更自然地承接这些并发信息。

### 作为目标形式主义还是中间表示

对多机器人高层任务规划，它可以直接作为目标形式主义；对一般控制软件，它也很适合作为并发协调层的中间表示。

### 对需求到模型生成的启发

1. 任务规格和机器人能力可分成不同 object nets 生成。
2. “谁能去哪里、多少机器人能同时去”可以被显式抽成多重集约束。
3. 若后续要做闭环修复，`GEF` 提供了很清晰的冲突来源。

## 重要的相关工作

- [Petri Nets: Properties, Analysis and Applications](../petri-nets-properties-analysis-and-applications/desc.md)：本文的上位 Petri 主干。
- [Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)：同样面向多机器人，但层次结构更弱。
- [Distributed Petri Nets for Model-Driven Verifiable Robotic Applications in ROS](../distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md)：同属 `Petri` 网在机器人中的应用，但目标更偏 `ROS` 工具链。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值主干应用条目，核心贡献是提出稳定命名的 `HLrtPN` 多层 Petri 框架。
- 它的描述客体是多机器人并发移动与任务资源协调，因此记为 `🏭`；论文语境落在机器人/CPS 高层规划，因此记为 `🌡️`。
- 对 `project_1` 来说，它为“多主体协同需求如何映射到层次化并发网模型”提供了非常直接的样板。

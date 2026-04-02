# 基于 Petri 网模型与 LTL 规格的多机器人路径规划 / On Multirobot Path Planning Based on Petri Net Models and LTL Specifications

## 基本信息

- 标题：On Multirobot Path Planning Based on Petri Net Models and LTL Specifications
- 中文标题：基于 Petri 网模型与 LTL 规格的多机器人路径规划
- 作者：Sofia Hustiu, Cristian Mahulea, Marius Kloetzer, Jean-Jacques Lesage
- 发表：*IEEE Transactions on Automatic Control*, 69(9):6373-6380, 2024
- DOI：`10.1109/TAC.2024.3386024`
- 链接：https://doi.org/10.1109/TAC.2024.3386024
- 形式主义：`Composed Petri Net + Quotient RMPN + Büchi Petri Net`
- 主类：🕸️
- 描述客体：🏭
- 所属领域：🌡️
- 论文角色：多机器人路径规划 / `Petri Net + LTL` 组合建模
- 工具/实现获取方式：原文明确以 `MILP` 求解 prefix/suffix 与投影问题，但未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `RMPN`、Quotient `PN`、`Büchi PN`、Composed `PN` 与 `MILP`；无独立交换标准。

## 简报

这篇论文的关键点，不是单纯“用 `Petri Net` 表示机器人环境”，而是把机器人运动网和 `LTL` 规格对应的 `Büchi` 网合成一个新的 `Composed Petri Net`，再在这个组合网的 reduced model 上搜索 prefix/suffix 解，最后投影回原始环境网得到无碰撞轨迹。这样做的好处是：规格推进与机器人移动被放到同一个 `PN` 框架里，同时模型规模又通过 quotient reduction 控制住。

- 形式主义定位：面向多机器人路径规划与时序任务满足的 `Petri` 应用模型，不是一般 workflow 或执行器条目。
- 构造方式简述：先建 `Robot Motion Petri Net (RMPN)`，再建 `Büchi PN`，再合成 `Composed PN`，最后用两层 `MILP` 求解。
- 基础设施与场景简述：依托 `RMPN`、Büchi 自动机、Quotient `PN`、`MILP` 和 collision-avoidance projection，服务带全局 `LTL` 任务的多机器人路径规划。

```text
环境 PN + LTL -> Büchi automaton / Büchi PN -> Composed PN -> reduced-model prefix/suffix -> projection -> collision-free trajectories
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. `Robot Motion Petri Net (RMPN)`。
2. 对应任务公式的 `Büchi` 自动机。
3. `Büchi Petri Net`。
4. `Quotient PN` 与 `Composed PN`。
5. 基于 prefix/suffix 的 accepted run。
6. 两层 `MILP` 规划与投影。

### 核心抽象

机器人运动网定义为：

$$
Q = \langle N, m_0, Y, h \rangle,\quad N = \langle P, T, Post, Pre \rangle
$$

上式中的符号逐项解释如下：

1. `P` 是对应工作空间 cells 的 places。
2. `T` 是机器人从一个 cell 移到另一个 cell 的 transitions。
3. `Post` 与 `Pre` 是后/前关联矩阵。
4. `m_0[p]` 是初始时部署在 cell `p` 中的机器人数量。
5. `h: P \to 2^Y` 把 places 映射到 regions of interest。

其基本状态方程是：

$$
\tilde m = m + C \cdot \sigma
$$

其中：

1. `C = Post - Pre` 是 token flow matrix。
2. `m` 是当前 marking。
3. `\tilde m` 是目标 marking。
4. `\sigma` 是 firing count vector。

论文同时使用 `Büchi` 自动机：

$$
B = (S, S^0, \Sigma_B, \to_B, F)
$$

上式中的符号逐项解释如下：

1. `S` 是自动机状态集合。
2. `S^0` 是初始状态集合。
3. `\Sigma_B` 是输入集合。
4. `\to_B` 是迁移关系。
5. `F` 是 final states。

再将其转成 `Büchi PN`，并进一步组合成：

$$
Q_C = \langle \langle P_C, T_C, Pre_C, Post_C \rangle, m_0^C, Y, h \rangle
$$

这里：

1. `Q_C` 同时包含 quotient 机器人网、`Büchi PN` 和 active/inactive observation places。
2. 其目标是在统一 marking 空间中同时推进“机器人位置”和“规格满足进度”。

### 一个最小例子与通俗解释

论文中的例子很适合解释这套模型：

1. 两个机器人在带三个 ROI 的环境中运动。
2. 任务要求最终访问 `y_1`、`y_2`、`y_3`，并要求 `y_1` 与 `y_2` 先同步激活。
3. 单看机器人移动网时，很多路径都能走；但一旦和 `Büchi PN` 合成，就只有那些能让规格状态同步推进的 firing 序列才是可接受的。
4. 之后还要投影回原始 `RMPN`，并插入 intermediate markings 来避免碰撞。

通俗地说，这个模型像“给多机器人交通网再叠一个任务验收网”，任何动作序列都得同时让这两张网一起前进。

### 运行 / 接受 / 转移语义

`Büchi` 自动机的 accepted run 仍采用 prefix/suffix 结构：

$$
\mathrm{run} = \mathrm{prefix},\ \mathrm{suffix},\ \mathrm{suffix},\dots
$$

原文在 reduced model 上的规划，要求在 `2k` 步后把 `Composed PN` 带到 final `Büchi` place，可保守写成：

$$
m_i^C - m_{i-1}^C - C_C \cdot \sigma_i^C = 0
$$

$$
m_{2k}^C[p_f^B] = 1
$$

上式中的符号逐项解释如下：

1. `m_i^C` 是 `Composed PN` 第 `i` 步 marking。
2. `C_C` 是 `Composed PN` 的 token flow matrix。
3. `\sigma_i^C` 是第 `i` 步 firing vector。
4. `p_f^B` 是 final `Büchi` place。

论文的关键技巧，是让奇偶步分别承担不同语义：

1. 奇数步主要推进 Quotient `PN` 中的机器人移动。
2. 偶数步推进 `Büchi PN` 中的规格状态。
3. 求得 reduced-model run 后，再通过第二个 `MILP` 投影回原始 `RMPN`。

### 语义边界

这篇论文的边界很清楚：

1. 当前聚焦 co-safe `LTL` 任务。
2. 机器人连续控制被抽象成 `RMPN` 中的 cell-to-cell 转移。
3. 算法是 sound 但 not complete。
4. 求解强依赖 `MILP`，复杂度落在 `NP-hard`。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `RMPN` | `$Q = \langle N, m_0, Y, h \rangle$` | 机器人运动首先被写成不随机器人数变化的 Petri 网。 |
| 状态方程 | `$\tilde m = m + C \cdot \sigma$` | 用标准 `PN` 线性代数骨架表达可达 marking。 |
| `Büchi` 自动机 | `$B = (S, S^0, \Sigma_B, \to_B, F)$` | `LTL` 规格的自动机主干。 |
| `Composed PN` | `$Q_C = \langle \langle P_C,T_C,Pre_C,Post_C \rangle, m_0^C, Y, h \rangle$` | 统一耦合机器人移动与规格推进。 |
| `MILP` 状态更新 | `$m_i^C - m_{i-1}^C - C_C \cdot \sigma_i^C = 0$` | reduced model 上的 prefix/suffix 搜索。 |
| 终态要求 | `$m_{2k}^C[p_f^B] = 1$` | 规划必须真正达到任务接受状态。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `RMPN`、`Büchi PN` 与 `Composed PN` 共同描述系统状态。 |
| 事件 / 触发 | 强支持 | firing 序列直接决定机器人移动和任务推进。 |
| 守卫 / 数据 | 强支持 | ROI labels、active/inactive observations 与 `MILP` 约束共同作用。 |
| 层次 | 部分支持 | 有 quotient / composed 两层，但不走 `Nets-within-Nets` 层次。 |
| 并发 / 同步 | 强支持 | 多机器人并发与规格同步是主体。 |
| 时间约束 | 弱支持 | 主体不是显式时钟，而是逻辑与碰撞约束。 |
| 连续动态 / 随机性 | 弱支持 | 连续控制被抽象，随机性未建模。 |
| 可执行 / 可验证性 | 强验证 | `MILP` 保证路径和规格同时可满足。 |

### 形式化问题与性质

1. 论文最重要的增量，是把 `PN` 运动模型与 `LTL/Büchi` 规格放进一个真正统一的组合网里。
2. quotient reduction 让模型规模不至于直接爆炸。
3. 第二层 projection `MILP` 明确解决了 reduced model 与真实无碰撞轨迹之间的差距。
4. 它因此是 `Petri` 主干上一条很成熟的“逻辑任务 + 多机器人规划”应用路线。

## 构造方式与承载格式

### 建模入口

建模入口通常是：

1. 用 `RMPN` 建模机器人在环境中的移动能力。
2. 把 `LTL` 公式转换为 `Büchi` 自动机，再转为 `Büchi PN`。
3. 对 `RMPN` 做 quotient reduction。
4. 组合成 `Composed PN` 并求 prefix/suffix 与 projection。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `RMPN` 的 `Pre/Post/C` 矩阵。
2. `Büchi PN`。
3. `Composed PN` 的 active/inactive observation places。
4. 两个 `MILP` 求解问题。

### 交换与互操作

互操作重点在：

1. 机器人运动网与规格网如何通过 observation places 绑定。
2. quotient model 解如何投影回原始环境模型。
3. reduced-model 可行解如何经 projection 变成真正无碰撞轨迹。

## 配套基础设施

- 建模/编辑工具：原文重点是数学模型与 `MILP` 求解，不依赖固定图形建模器。
- 解析/交换/元模型支持：有稳定的 `PN` 矩阵化表示，但无统一交换标准。
- 仿真/执行支持：重点不在运行时执行器，而在离线规划。
- 验证/分析支持：prefix/suffix 搜索、collision-free projection 与 soundness 论证。
- 代码生成/转换支持：原文未给自动代码生成。
- 标准化或社区生态：依托 `Petri Nets`、`LTL/Büchi` 与优化求解研究线。

## 适用场景与需求前提

### 适用场景

适合多机器人路径规划、任务含顺序与同步访问约束、且希望把逻辑任务与运动网络一起求解的场景。

### 需求前提

1. 环境可抽象成有限 cells 和 ROI labels。
2. 高层任务可写成 co-safe `LTL`。
3. 机器人移动能力可抽成 `RMPN`。
4. 系统可以接受 `MILP` 级离线求解开销。

### 不适用或高成本场景

若环境高度连续、时序约束极复杂、或在线重规划频繁，这套 quotient/composed `PN + MILP` 方法的代价会偏高。

## 与相邻形式主义的关系

相对 [Petri Net Based Multi-Robot Task Coordination from Temporal Logic Specifications](../petri-net-based-multi-robot-task-coordination-from-temporal-logic-specifications/desc.md)，本文更强调路径规划与 quotient/composed `PN`；相对 [Multi-robot Motion Planning based on Nets-within-Nets Modeling and Simulation](../multi-robot-motion-planning-based-on-nets-within-nets-modeling-and-simulation/desc.md)，本文不走 `Nets-within-Nets` 层次，而是走 `Composed PN + MILP`；相对 [A Petri Net On-Line Controller for the Coordination of Multiple Mobile Robots](../a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md)，本文更偏离线规划和逻辑规格绑定。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求里已经明确写出全局顺序/同步访问规则时，`Petri Net` 完全可以和 `LTL` 规格一道成为目标建模形式，而不是只做执行器。

### 作为目标形式主义还是中间表示

对多机器人逻辑规划，它可以直接作为目标形式主义；对更一般系统，也可以作为“并发任务层 + 逻辑约束层”的中间表示。

### 对需求到模型生成的启发

1. ROI 与 cell 抽象可以先于逻辑规格生成。
2. `LTL` 到 `Büchi PN` 的翻译，是把自然语言任务接到并发网模型的重要桥梁。
3. 若后续要做模型修复，reduced model 与 projection 之间的不一致是很好的错误证据来源。

## 重要的相关工作

- [Petri Nets: Properties, Analysis and Applications](../petri-nets-properties-analysis-and-applications/desc.md)：本文的基础网模型来源。
- [Petri Net Based Multi-Robot Task Coordination from Temporal Logic Specifications](../petri-net-based-multi-robot-task-coordination-from-temporal-logic-specifications/desc.md)：同样连接 `Petri Net` 与 temporal logic，但对象与求解方式不同。
- [Multi-robot Motion Planning based on Nets-within-Nets Modeling and Simulation](../multi-robot-motion-planning-based-on-nets-within-nets-modeling-and-simulation/desc.md)：同属多机器人 `Petri` 主干的最新应用路线。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值应用条目，核心贡献是提出 `Composed PN + Quotient PN + projection MILP` 的逻辑任务规划链路。
- 它的描述客体是多机器人并发路径与资源占用，因此记为 `🏭`；论文语境位于机器人/CPS 路径规划，因此记为 `🌡️`。
- 对 `project_1` 来说，它为“如何把逻辑任务直接压进并发网并产出团队轨迹”提供了很强的应用侧证。

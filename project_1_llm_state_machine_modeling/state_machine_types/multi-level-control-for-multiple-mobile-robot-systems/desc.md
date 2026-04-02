# 多移动机器人系统的多层控制 / Multi-level control for multiple mobile robot systems

## 基本信息

- 标题：Multi-level control for multiple mobile robot systems
- 中文标题：多移动机器人系统的多层控制
- 作者：Elzbieta Roszkowska、Piotr Makowski-Czerski、Lukasz Janiec
- 发表：*Discrete Event Dynamic Systems*, 33(4): 425-453, 2023
- DOI：`10.1007/s10626-023-00383-x`
- 链接：https://doi.org/10.1007/s10626-023-00383-x
- 形式主义：`DES/CTS Hybrid MMRS Control`
- 主类：🌊
- 描述客体：🌡️
- 所属领域：🌡️
- 论文角色：多移动机器人分层控制 / DES + 连续运动混成架构
- 工具/实现获取方式：原文给出三层控制架构、仿真系统和差速小车控制公式，但未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 deterministic automata、资源分配模型、`APF` 与差速机器人运动学；原文未定义独立交换标准。

## 简报

这篇论文把多移动机器人协调明确写成一个三层混成控制系统：顶层是离散事件 supervisor，控制机器人何时切换 stage；中层是本地 motion-mode supervisor，用状态机与 `APF` 保证同 cell/sector 内的局部通过；底层则是差速机器人的连续运动控制。也就是说，它不是只做路径规划，也不是只做低层避障，而是把离散阶段逻辑和连续运动控制用同一套架构接起来。

- 形式主义定位：这是典型的 `DES + CTS` 混成控制条目，重点是多机器人共享空间中的离散阶段约束与连续运动执行耦合。
- 构造方式简述：先把机器人路径切成 sectors 或 cells，再构建 deterministic automata 级 supervisor，随后为局部通行建立 motion-mode state machine 与 `APF` 控制。
- 基础设施与场景简述：依托 `DES` supervisory control、差速机器人模型和 `Artificial Potential Field`，适用于共享二维工作空间的多机器人协同运输与配送。

```text
机器人任务路径 -> sectors / cells -> stage-transition automaton -> local motion-mode control + APF -> differential-drive execution
```

## 形式主义定义与核心对象

### 定义对象

论文的核心对象包括：

1. 多移动机器人系统 `MMRS` 的离散阶段表示。
2. 机器人路径 sectors / cells 之间的冲突关系。
3. 顶层 supervisor 的 deterministic automaton。
4. 中层 motion-mode state machine 与 `APF` 局部协调器。
5. 底层差速机器人的连续运动学。

### 核心抽象

原文先给出 deterministic automaton：

$$
G = (S, E, \Gamma, f, s_0, S_M)
$$

上式中的符号逐项解释如下：

1. `$S$` 是系统状态集合。
2. `$E$` 是事件集合，每个事件都对应某个机器人完成一次 stage 转移。
3. `$\Gamma : S \to 2^E$` 是可行事件函数。
4. `$f$` 是状态转移函数。
5. `$s_0$` 是初始状态。
6. `$S_M$` 是标记终态集合。

对基于 path sectors 的冲突建模，论文定义了 stage conflict relation：

$$
(z_i^k, z_j^l) \in \xi \iff i \ne j \land d_{min}(p_i^k, p_j^l) < a_i + a_j
$$

上式中的符号逐项解释如下：

1. `$z_i^k$` 是机器人 `$A_i$` 的第 `$k$` 个 stage。
2. `$p_i^k$` 是与该 stage 对应的路径 sector。
3. `$a_i$` 是机器人 `$A_i$` 的圆盘半径。
4. `$d_{min}(p_i^k, p_j^l)$` 是两个 sectors 之间的最小距离。
5. 该式表示：若两段路径离得不够远，它们在 supervisor 看来就是冲突 stage。

在 `\xi`-MMRS 中，顶层可行事件函数可整理为：

$$
\Gamma(s_1,\ldots,s_n) = \{ e_i \mid s_i < m_i \land \forall j,\ (z_i^{s_i+1}, z_j^{s_j}) \notin \xi \}
$$

上式中的符号逐项解释如下：

1. `$s_i$` 是机器人 `$A_i$` 当前 stage 的编号。
2. `$m_i$` 是其终点 stage 编号。
3. `$e_i$` 表示 `$A_i$` 进入下一个 stage 的事件。
4. 该式确保任何机器人在进入下一段之前，都不会与其他机器人当前 stage 冲突。

### 一个最小例子与通俗解释

最小例子可以理解成“两台机器人要穿过同一片共享区域”：

1. 顶层 supervisor 先判断它们的下一个 stage 是否冲突。
2. 如果冲突，就只允许其中一台先进入。
3. 进入共享区后，本地 motion-mode controller 决定加速、减速、等待或绕行。
4. 底层差速控制器再把这些模式变成左右轮速度。

通俗地说，这个系统像“一个交通管制员 + 一个车道内避障副驾 + 一个真正踩油门转方向盘的底盘控制器”。它比纯 FSM 多出来的是连续空间、速度和机器人几何关系。

### 运行 / 接受 / 转移语义

在局部连续控制层，论文采用人工势场。吸引势场与斥力势场分别为：

$$
U_{att}(X) = \frac{1}{2} k \rho^2(X, X_g)
$$

$$
U_{rep}(X) = \frac{1}{2}\eta \left( \frac{1}{\rho(X,X_o)} - \frac{1}{\rho_o} \right)
$$

上式中的符号逐项解释如下：

1. `$X=(x,y)$` 是机器人当前位置。
2. `$X_g$` 是当前目标点，如 cell 出口或待访问位置。
3. `$X_o$` 表示障碍或另一台机器人。
4. `$\rho(\cdot,\cdot)$` 是距离函数。
5. `$k$` 和 `$\eta$` 是缩放参数。
6. `$\rho_o$` 是障碍影响半径。
7. 上式只在 `$\rho(X,X_o) \le \rho_o$` 时激活；若超出影响半径，斥力势场按 `0` 处理。

合力写成：

$$
F(X) = F_{rep}^{border}(X) + F_{rep}^{other\ robot}(X) + F_{att}^{goal}(X)
$$

上式中的符号逐项解释如下：

1. 第一项来自 cell 边界。
2. 第二项来自另一台共享 cell 的机器人。
3. 第三项来自当前目标点。
4. 合力方向决定下一步局部运动方向。

在底层，差速机器人运动学写成：

$$
\dot{x} = v \cos \theta,\quad \dot{y} = v \sin \theta,\quad \dot{\theta} = \omega
$$

$$
\dot{\theta} = \omega = \frac{v_r - v_l}{D}
$$

$$
v = \frac{v_l + v_r}{2}
$$

上式中的符号逐项解释如下：

1. `$q=(x,y,\theta)$` 是机器人位姿，上一式分别给出了其三个分量的导数。
2. `$v$` 是平台线速度，`$\omega$` 是角速度。
3. `$v_l, v_r$` 分别是左右轮线速度。
4. `$D$` 是两轮中心距。
5. 顶层离散许可和中层局部模式最终都要落实为 `$v_l, v_r$`。

### 语义边界

这篇论文的边界在于：

1. 顶层离散逻辑假定路径和 stage 划分可预先给出。
2. 局部连续控制依赖 `APF` 参数整定，不能保证对所有几何布局都最优。
3. 连续层主要是运动学与势场，不是高保真动力学模型。
4. 论文重点是控制架构和可行性比较，不是通用 hybrid automata 工具链。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| supervisor automaton | `$G = (S, E, \Gamma, f, s_0, S_M)$` | 顶层离散控制骨架。 |
| stage 冲突 | `$(z_i^k, z_j^l) \in \xi \iff d_{min}(p_i^k, p_j^l) < a_i + a_j$` | 通过几何关系定义冲突 stage。 |
| 可行事件 | `$\Gamma(s_1,\ldots,s_n)=\{e_i \mid \cdots\}$` | 只允许无冲突的 stage 转移发生。 |
| 势场吸引项 | `$U_{att}(X)=\frac{1}{2}k\rho^2(X,X_g)$` | 让机器人朝目标移动。 |
| 势场合力 | `$F(X)=F_{rep}^{border}+F_{rep}^{other\ robot}+F_{att}^{goal}$` | 同时考虑边界、他车和目标。 |
| 差速运动学 | `$\dot{q}=[\cos\theta,\sin\theta,0]^Tv + [0,0,1]^T\omega$` | 把离散控制决策映射到连续执行。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | stage、motion mode 和底层位姿模式都被显式区分。 |
| 事件 / 触发 | 强支持 | stage 转移和授权消息是顶层事件。 |
| 守卫 / 数据 | 强支持 | 冲突关系、cell 资源和几何位置都进入 guard。 |
| 层次 | 强支持 | central supervisor、local supervisor、robot control 三层结构非常明确。 |
| 并发 / 同步 | 强支持 | 多机器人并发运行，由 supervisor 约束同步进入共享区。 |
| 时间约束 | 部分支持 | 强调连续时间运动执行，但不是 deadline 风格实时逻辑。 |
| 连续动态 / 随机性 | 强连续、无随机 | 重点是 `APF` 与差速机器人连续运动。 |
| 可执行 / 可验证性 | 强执行、部分验证 | 离散层有形式模型，连续层可仿真执行。 |

### 形式化问题与性质

1. 论文真正解决的是“离散空间共享规则”和“连续运动执行”之间如何接缝。
2. 顶层模型提供 collision-free / deadlock-free 约束，底层提供可执行的差速控制。
3. `APF` 让本地通过控制不必完全回退到中央重规划。
4. 对混成主干而言，它是一篇典型的工程架构条目，而不是新命名的自动机子类。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 把机器人路径离散成 sectors 或由 cells 诱导出的 stages。
2. 为这些 stages 建立 deterministic automaton 级 supervisor。
3. 为共享 cell 或 sector 设计 motion-mode state machine。
4. 用 `APF` 与差速机器人控制器落实连续执行。

### 机器可处理承载方式

原文涉及的承载方式包括：

1. `MMRS` 的 deterministic automata。
2. `RAS` 风格资源分配建模。
3. `APF` 势场函数。
4. 差速底盘的连续运动学方程。

### 交换与互操作

论文没有定义通用交换标准，但给出了清晰的分层接口：

1. 顶层 supervisor 向机器人发送 stage 进入许可。
2. 中层根据许可切换 motion mode。
3. 底层把 mode 转成轮速命令。

## 配套基础设施

- 建模/编辑工具：原文以理论模型和仿真系统为主，未给专用建模器。
- 解析/交换/元模型支持：无独立交换标准。
- 仿真/执行支持：有多场景仿真实验，底层控制假定可部署到差速机器人。
- 验证/分析支持：离散层给出碰撞避免与死锁避免逻辑，连续层通过仿真评估。
- 代码生成/转换支持：原文未提供自动代码生成。
- 标准化或社区生态：依托 `DES` supervisory control、资源分配系统与移动机器人控制三条成熟研究线。

## 适用场景与需求前提

### 适用场景

适合仓储配送、园区物流、巡检等多机器人共享二维空间的场景，尤其适合既要保证离散任务完成，又要考虑局部连续避障和通行控制的系统。

### 需求前提

1. 每台机器人的路径可预先规划并离散成 stages。
2. 机器人占用空间可近似成圆盘。
3. 共享区冲突关系或 cell 资源关系可显式枚举。
4. 机器人底盘可由连续控制器执行速度/姿态命令。

### 不适用或高成本场景

若环境高度动态、路径无法预先离散，或机器人动力学远超差速近似，这一架构的抽象成本会明显升高。

## 与相邻形式主义的关系

相对 [formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md](../formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md)，本文更强调分层 supervisor 架构而非参数综合；相对 [a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md](../a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md)，本文更细地展开了 `MMRS` 的 stage/cell 资源建模与本地通行控制；相对 [a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md](../a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md)，它不走 `Petri` 路线，而是把离散 supervisor 与连续运动控制耦合得更紧。

## 与本研究的关系

### 对 Project 1 的价值

它说明多机器人需求往往天然是“离散任务阶段 + 连续运动执行”的双层对象，若只生成纯离散状态机会丢掉关键约束。

### 作为目标形式主义还是中间表示

对移动机器人协同控制，这种分层混成架构本身就可以是目标形式主义；对一般需求建模，它也适合作为高层 FSM 与底层控制之间的中间桥梁。

### 对需求到模型生成的启发

1. 需求抽取时要同时捕捉 stage、共享空间、冲突关系和执行底盘类型。
2. 进入共享区的许可逻辑与局部避障逻辑应分层表示，而不是混成一团自然语言。
3. 对机器人系统而言，“死锁避免”和“碰撞避免”通常不是同一个控制层的问题。

### 现实限制

本文的连续控制仍以 `APF` 和差速底盘为主，通用性强于精度，但离更复杂 `CPS` 控制仍有距离。

## 重要的相关工作

- [formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md](../formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md)：早期多机器人混成建模代表。
- [a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md](../a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md)：更偏 heterogeneous field robots 的层次混成控制。
- [a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md](../a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md)：同样处理多机器人协调，但走并发网监督控制路线。

## 文献分类总结

- 这是一篇 `🌊` 类应用条目，核心贡献是把 `DES` supervisory control、局部 `APF` 与差速底盘控制合成一套可执行的多机器人混成架构。
- 其主要描述对象是带连续运动学的物理机器人系统，因此记为 `🌡️`；场景仍属于 `CPS / 物理系统建模`，因此领域记为 `🌡️`。
- 对状态机族演化树而言，它补强的是 `Hybrid Automata / DES+CTS` 主干的工程应用证据，不单独挂成新节点。

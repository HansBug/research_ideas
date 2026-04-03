# 基于正则化混成自动机的行为机器人学 / Behavior Based Robotics Using Regularized Hybrid Automata

## 基本信息

- 标题：Behavior Based Robotics Using Regularized Hybrid Automata
- 中文标题：基于正则化混成自动机的行为机器人学
- 作者：Magnus Egerstedt, Karl Henrik Johansson, John Lygeros, Shankar Sastry
- 发表：*Proceedings of the 38th IEEE Conference on Decision and Control*, Vol. 4, pp. 3400-3405, 1999
- DOI：`10.1109/CDC.1999.827799`
- 链接：https://doi.org/10.1109/CDC.1999.827799
- 形式主义：`Regularized Hybrid Automata / Behavior-Based Mobile-Robot Control`
- 主类：🌊 混成/随机扩展
- 对象类型：🧪 应用/案例
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：移动机器人行为控制 / 正则化混成自动机应用建模
- 工具/实现获取方式：原文明确在 `Nomad 200` 移动机器人与 `Nserver` 仿真器上实现并测试，但未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `Hybrid Automata`、potential-field vector fields、switching surface 与 regularized node；无独立交换标准。

## 简报

这篇论文想解决的问题很具体，也很典型：行为机器人学里常见的 `goal attraction` 和 `obstacle avoidance` 如果采用硬切换，会引入严重 chattering；如果做平滑融合，性能很好，但离散模式边界又不够清晰，难以进入自动机分析。作者的办法，是先承认“每个行为对应一个混成自动机节点”这一直观建模法，然后正面处理由硬切换带来的 `Zeno` 现象，通过 `Filippov` 型 regularization 在切换面上加入额外节点，使模型既保留可分析的离散行为结构，又避免时间阻塞。

- 形式主义定位：这是 `Hybrid Automata` 在 behavior-based mobile robotics 中的应用条目，重点是把行为切换系统规整成可分析的 regularized hybrid automaton。
- 构造方式简述：先把每个行为建成一个节点，再由 switching surface 触发跳转；若在边界上出现 `Zeno` 切换，则引入带 `Filippov` 滑移流的 extra node 做 regularization。
- 基础设施与场景简述：依托 `Nomad 200`、`Nserver`、potential fields 和混成自动机语义，服务点到点导航中的目标吸引与避障行为协调。

```text
goal attraction / obstacle avoidance -> hard-switch hybrid automaton -> Zeno boundary -> regularized sliding node -> analyzable robot controller
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 表示不同行为模式的离散节点。
2. 机器人位置等连续状态变量。
3. switching surfaces 与基于距离的行为切换条件。
4. `Zeno` 执行与 `Zeno time`。
5. 基于 `Filippov` 解的 regularized sliding node。
6. `Nomad 200` 上的 goal attraction / obstacle avoidance 例子。

### 核心抽象

论文给出的混成自动机定义是：

$$
H = (Q, X, I, f, E)
$$

上式中的符号逐项解释如下：

1. `Q` 是离散状态或行为模式集合。
2. `X` 是连续变量集合，例如机器人平面位置与朝向。
3. `I` 是初始状态集合。
4. `f` 描述各离散模式下的连续流。
5. `E` 描述离散跳转关系。

原文随后定义 hybrid execution：

$$
\chi = (\tau, q, x)
$$

上式中的符号逐项解释如下：

1. `\tau` 是 hybrid time trajectory，也就是一串连续时间区间。
2. `q` 是沿轨迹变化的离散模式。
3. `x` 是沿轨迹变化的连续状态。
4. 执行必须同时满足初始条件、离散演化和连续演化。

论文把 `Zeno` 现象定义为“无限执行但不是 admissible”，可压缩成：

$$
T_Z = \sum_i (t_i' - t_i) < \infty
$$

上式中的符号逐项解释如下：

1. `t_i` 与 `t_i'` 是第 `i` 个连续演化区间的起止时间。
2. `T_Z` 是所有这些区间时长之和。
3. 若执行包含无限多次离散切换，但总时间仍有限，就出现 `Zeno`。
4. 这正是硬切换行为系统在边界上抖振时的形式化刻画。

论文对点到点导航场景中的 obstacle avoidance 行为写成：

$$
\dot z = f_{OA}(z),\quad z = (x,y)^T
$$

上式中的符号逐项解释如下：

1. `z` 是机器人平面位置向量。
2. `f_{OA}` 是避障行为生成的连续向量场。
3. 它在距离障碍物小于安全阈值 `d_{OA}` 时激活。

regularization 的关键，是在切换边界加入滑移流节点。原文给出的组合形式可整理为：

$$
f_S = \alpha f_{OA} + (1-\alpha) f_{GA},\quad \alpha \in [0,1]
$$

并选择 `\alpha` 使得：

$$
f_S \perp f_{OA}
$$

上式中的符号逐项解释如下：

1. `f_{GA}` 是 goal attraction 行为的向量场。
2. `f_S` 是新增 regularized node 上的滑移动力学。
3. `\alpha` 是两种行为场的凸组合系数。
4. 通过合适选择 `\alpha`，轨迹沿切换边界滑行，而不在两侧无限抖动。

### 一个最小例子与通俗解释

论文里的最小例子就是“机器人去目标点，但遇到障碍物”：

1. 当机器人离障碍物足够远时，激活 `goal attraction` 节点，朝目标点前进。
2. 当机器人进入障碍物安全距离 `d_{OA}` 内时，切换到 `obstacle avoidance` 节点，沿排斥场转向。
3. 如果只做硬切换，机器人可能在边界上来回切太快，形成 `Zeno`。
4. 正则化以后，系统在边界上进入额外的 sliding 节点，沿边界平顺滑动，再择机离开。

通俗地说，这就像给“想去目标”和“必须避障”之间的争执加了一个调解模式，不再让控制器在两种意见之间无限抖动。

### 运行 / 接受 / 转移语义

这篇论文的运行语义非常清楚：

1. 每个离散节点对应一个行为与其连续向量场。
2. 连续状态在当前节点内按 `f_q` 演化。
3. 一旦碰到 switching surface，就发生离散跳转。
4. 若边界两侧向量场都把状态推向边界，则硬切换系统会形成 `Filippov` 型 `Zeno`。
5. regularization 通过引入 extra node，把原本“无限快切换”的现象改写成单节点上的连续滑移。

对本文的 regularized behavior system，可保守整理为：

$$
H_r = (Q \cup \{q_S\}, X, I, \tilde f, \tilde E)
$$

这里是根据论文结构做的保守归纳，其中：

1. `q_S` 是为滑移行为加入的 regularized node。
2. `\tilde f` 在原有 `f` 基础上加入 `f_S`。
3. `\tilde E` 在原有跳转关系上加入进入和离开 `q_S` 的边。
4. 这样模型仍是混成自动机，但不再在关键边界处阻塞时间。

### 语义边界

这篇论文的边界主要体现在：

1. 它关注的是 behavior-based control 中的切换与 regularization，不是一般混成自动机判定问题。
2. 机器人模型被简化为固定纵向速度、直接可控航向的运动学系统。
3. 重点是 `goal attraction + obstacle avoidance` 这一类典型切换行为，不是完整任务规划栈。
4. 对 `Zeno` 的处理主要围绕 `Filippov` 型滑移，而不是所有可能的混成异常行为。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 混成自动机元组 | `$H = (Q, X, I, f, E)$` | 每个行为模式都有离散节点和连续流。 |
| hybrid execution | `$\chi = (\tau, q, x)$` | 系统运行同时包含时间分段、离散模式和连续状态。 |
| `Zeno` 时间 | `$T_Z = \sum_i (t_i' - t_i) < \infty$` | 表达“有限时间内无限次切换”的病态行为。 |
| 避障向量场 | `$\dot z = f_{OA}(z)$` | 机器人在避障模式下按排斥场运动。 |
| 正则化滑移流 | `$f_S = \alpha f_{OA} + (1-\alpha) f_{GA}$` | 在边界上构造平滑的替代连续流。 |
| 正则化模型 | `$H_r = (Q \cup \{q_S\}, X, I, \tilde f, \tilde E)$` | 通过额外节点消解 `Zeno` 问题。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个行为就是一个显式离散节点。 |
| 事件 / 触发 | 强支持 | 距离阈值与 switching surface 触发模式切换。 |
| 守卫 / 数据 | 强支持 | 切换条件依赖几何距离与边界关系。 |
| 层次 | 弱支持 | 主体是少量 behavior nodes，不强调层次嵌套。 |
| 并发 / 同步 | 弱支持 | 重点不在并发，而在行为切换与正则化。 |
| 时间约束 | 部分支持 | 时间通过 execution 与 `Zeno time` 进入，而非 clocks。 |
| 连续动态 / 随机性 | 强连续、无随机 | 连续向量场是主角，随机性未建模。 |
| 可执行 / 可验证性 | 强执行、可分析 | 在 `Nomad 200` 与 `Nserver` 上实现，并能用混成语义解释性能。 |

### 形式化问题与性质

1. 论文真正补的是“行为控制为什么能被建成可分析自动机，而不是只有经验调参”。
2. 它把行为切换的病态现象直接上升成 `Zeno hybrid automaton` 问题。
3. regularization 让硬切换模型与平滑性能之间获得折中。
4. 因而它是 `Hybrid Automata` 主干上一条非常稳定、且能命名为 `Regularized Hybrid Automata` 的应用分支。

## 构造方式与承载格式

### 建模入口

建模入口可概括为：

1. 先识别机器人控制中的基本 behaviors。
2. 为每个 behavior 构造连续向量场。
3. 根据几何距离或边界关系定义 switching surfaces。
4. 检查是否出现 `Zeno`，必要时添加 regularized sliding node。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. 混成自动机节点图。
2. potential-field 连续向量场。
3. switching surface 与 `Filippov` regularization 公式。
4. `Nomad 200 / Nserver` 仿真实验配置。

### 交换与互操作

互操作重点在：

1. 行为控制器如何映射到自动机节点。
2. 机器人运动学如何进入连续流。
3. 正则化节点如何与原始行为节点衔接而不破坏控制含义。

## 配套基础设施

- 建模/编辑工具：原文以混成自动机理论和行为控制器设计为主，未依赖特定图形编辑器。
- 解析/交换/元模型支持：无统一交换格式，主要是自动机图与向量场公式。
- 仿真/执行支持：`Nserver` 仿真器与 `Nomad 200` 真实机器人。
- 验证/分析支持：通过 `Zeno`、`Filippov` regularization 和轨迹表现分析设计质量。
- 代码生成/转换支持：原文未给自动代码生成链。
- 标准化或社区生态：依托混成系统、滑模 / `Filippov` 与行为机器人学研究线。

## 适用场景与需求前提

### 适用场景

适合移动机器人导航、避障、目标跟踪这类“少量行为模式 + 明确切换边界 + 连续运动控制”的场景。

### 需求前提

1. 系统可拆成有限个核心 behaviors。
2. 每个 behavior 都能写出稳定的连续向量场。
3. 切换边界能用距离、几何或状态条件显式表达。
4. 主要痛点在 hard switching 引起的 chattering / `Zeno`，而不是高层任务规划。

### 不适用或高成本场景

如果系统包含大量高层离散任务、复杂非局部决策或强随机感知不确定性，只靠这种低层 behavior-based regularized automaton 并不够。

## 与相邻形式主义的关系

相对 [The Theory of Hybrid Automata](../the-theory-of-hybrid-automata/desc.md)，本文不是理论总论，而是把行为机器人控制压成可分析的混成模型；相对 [A Hybrid Control Approach to Action Coordination for Mobile Robots](../a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md)，本文更早、更直接地把 `Zeno` 与 regularization 放到舞台中央；相对 [A Human Operator Model for Medical Device Interaction Using Behavior-Based Hybrid Automata](../a-human-operator-model-for-medical-device-interaction-using-behavior-based-hybrid-automata/desc.md)，二者都强调 behavior-based 混成建模，但本文的对象是移动机器人动力学，不是人在环交互行为。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求天然呈现为“若接近障碍则避让，否则朝目标移动”这种模式切换控制逻辑时，`Hybrid Automata` 不只是验证载体，也能成为直接的目标模型。

### 作为目标形式主义还是中间表示

对移动机器人行为协调，它可以直接作为目标形式主义；对更复杂系统，也可以作为“连续控制层”的中间表示。

### 对需求到模型生成的启发

1. 自然语言中的行为模式非常适合先抽成离散节点。
2. 若存在切换边界与连续控制律，就不应退化成普通 `FSM`。
3. 一旦发现模型存在高频抖振或边界冲突，regularization 本身就可以成为自动修复方向。

## 重要的相关工作

- [The Theory of Hybrid Automata](../the-theory-of-hybrid-automata/desc.md)：本文所有建模都建立在标准混成自动机元组和 execution 语义上。
- [A Hybrid Control Approach to Action Coordination for Mobile Robots](../a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md)：同样面向 goal attraction / obstacle avoidance，但更偏控制实现。
- [A Human Operator Model for Medical Device Interaction Using Behavior-Based Hybrid Automata](../a-human-operator-model-for-medical-device-interaction-using-behavior-based-hybrid-automata/desc.md)：展示 behavior-based 混成建模在另一类应用对象上的延伸。

## 文献分类总结

- 这是一篇 `🌊` 类应用型条目，核心贡献是把 behavior-based mobile-robot control 规整成可分析的 `Regularized Hybrid Automata`。
- 它描述的是带连续动力学的机器人运动与切换控制，因此客体记为 `🌡️`，领域也记为 `🌡️`。
- 对 `project_1` 来说，它非常适合支撑“需求中的行为模式切换 + 连续控制”这一建模分支，并且给出了 `Zeno -> regularization` 这一明确修复线索。

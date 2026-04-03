# 面向移动机器人导航的混成多控制器架构 / Hybrid and Multi-controller Architecture for Autonomous System - Application to the Navigation of a Mobile Robot

## 基本信息

- 标题：Hybrid and Multi-controller Architecture for Autonomous System - Application to the Navigation of a Mobile Robot
- 中文标题：面向移动机器人导航的混成多控制器架构
- 作者：Amani Azzabi, Marwa Regaieg, Lounis Adouane, Othman Nasri
- 发表：*Proceedings of the 11th International Conference on Informatics in Control, Automation and Robotics*, pp. 491-497, 2014
- DOI：`10.5220/0005065404910497`
- 链接：https://doi.org/10.5220/0005065404910497
- 形式主义：`Hybrid Automaton + Multi-controller Navigation Architecture`
- 主类：🌊 混成/随机扩展
- 对象类型：🧪 应用/案例
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：移动机器人导航 / 混成自动机应用与 reachability 验证
- 工具/实现获取方式：原文明确使用 `MATLAB` 工具箱 `INTLAB`、Taylor interval integration 和 hybrid bounding method；未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 unicycle 运动学、两类控制律、混成自动机六元组和 interval reachability 算法；无独立交换格式。

## 简报

这篇论文的重点，不是再讲一次“机器人有避障和到目标两种模式”，而是把这种多控制器切换结构明确建成一个 `Hybrid Automaton`，并进一步用区间可达性来检验导航架构的稳定性。作者把 unicycle 机器人在 cluttered environment 中的“目标吸引”和“障碍绕行”两套控制律，与一个感知驱动的 action-selection block 组合起来，再通过 hybrid bounding method 证明轨迹包络不会穿进危险区域。

- 形式主义定位：面向移动机器人多控制器切换验证的 `Hybrid Automaton` 应用模型，而不是一般仿真框架。
- 构造方式简述：先写 unicycle 连续动力学，再定义目标吸引与极限环避障控制律，最后用 guard 条件切换两个离散 mode。
- 基础设施与场景简述：依托 `Hybrid Automaton`、Lyapunov 分析、区间 Taylor 积分和 `INTLAB`，服务 cluttered environment 中的 reachability / stability verification。

```text
unicycle robot + target/obstacle controllers -> hybrid automaton -> interval reachability envelope -> stability / safety check
```

## 形式主义定义与核心对象

### 定义对象

论文处理的对象包括：

1. unicycle 机器人的连续状态 `(x, y, \theta)`。
2. 目标吸引控制器与障碍绕行控制器。
3. 由传感器信息驱动的 controller selection block。
4. 表示两种控制模式的混成自动机离散状态。
5. 通过区间可达性给出的轨迹包络。

### 核心抽象

原文先给出了机器人在参考点 `P_t` 处的 unicycle 运动学：

$$\begin{bmatrix}\dot{x} \\ \dot{y} \\ \dot{\theta}\end{bmatrix} = \begin{bmatrix}\cos \theta & - l_2 \cos \theta - l_1 \sin \theta \\ \sin \theta & - l_2 \cos \theta + l_1 \sin \theta \\ 0 & 1\end{bmatrix} \begin{bmatrix}v \\ \omega\end{bmatrix}$$

上式中的符号逐项解释如下：

1. `(x, y, \theta)` 是机器人位姿状态。
2. `v` 是线速度。
3. `\omega` 是角速度。
4. `(l_1, l_2)` 描述控制点 `P_t` 相对机器人中心的位置。

随后作者把整体控制结构写成一个六元组混成自动机：

$$
H = (Q, X, P, F, T, RI)
$$

上式中的符号逐项解释如下：

1. `Q` 是离散 mode 集合。
2. `X` 是连续状态空间。
3. `P` 是参数有界区间。
4. `F` 是各 mode 下包住真实动力学的向量场集合。
5. `T` 是离散迁移集合。
6. `RI` 是 mode 切换时的更新函数。

在本文实例中，模式集合被具体化为：

$$
Q = \{q_1, q_2\} = \{\text{Attraction to the target},\ \text{Obstacle avoidance}\}
$$

上式中的符号逐项解释如下：

1. `q_1` 表示没有进入障碍影响区时的目标吸引控制模式。
2. `q_2` 表示检测到障碍后进入的绕障控制模式。

### 一个最小例子与通俗解释

最小工作机制其实很简单：

1. 机器人默认处于 `q_1`，沿目标吸引控制器朝目标点前进。
2. 一旦某个障碍满足 `DPRO_i \le RI_i`，就切换到 `q_2`。
3. 在 `q_2` 中，机器人跟随 limit-cycle vector field 绕开障碍。
4. 当再次满足 `DPRO_i > RI_i` 时，回到 `q_1`，继续朝目标点前进。

通俗地说，这个模型像一个“二档混成巡航系统”：平时开“去目标”档，碰到障碍就自动切到“绕障”档；而论文做的关键工作，是证明这两个档位反复切换时，整体轨迹仍然被安全包络住。

### 运行 / 接受 / 转移语义

目标吸引控制器用位置误差

$$
e_x = x - x_T,\quad e_y = y - y_T
$$

定义比例控制律：

$$\begin{bmatrix}v \\ \omega\end{bmatrix} = -K \begin{bmatrix}\cos \theta & - l_1 \sin \theta \\ \sin \theta & l_1 \sin \theta\end{bmatrix}^{-1} \begin{bmatrix}e_x \\ e_y\end{bmatrix}$$

上式中的符号逐项解释如下：

1. `(x_T, y_T)` 是目标圆心。
2. `(e_x, e_y)` 是相对目标的位置误差。
3. `K > 0` 是比例增益。
4. 该控制律驱动机器人朝目标区域收敛。

其 Lyapunov 候选函数写成：

$$
V_1 = \frac{1}{2} d^2
$$

其中 `d = \sqrt{e_x^2 + e_y^2}`，表示机器人相对目标的距离。

绕障模式则使用 limit-cycle vector field：

$$\dot{x}_s = y_s + x_s (R_c^2 - x_s^2 - y_s^2),\quad \dot{y}_s = -x_s + y_s (R_c^2 - x_s^2 - y_s^2)$$

上式中的符号逐项解释如下：

1. `(x_s, y_s)` 是以收敛圆心为参考的局部坐标。
2. `R_c` 是收敛圆半径。
3. 该场定义了顺时针或逆时针绕障轨迹。

作者为整体控制结构给出的切换 guard 是：

$$t_{q_1 q_2}: DPRO_i \le RI_i,\qquad t_{q_2 q_1}: DPRO_i > RI_i$$

其中：

1. `DPRO_i` 是机器人到障碍 `i` 的某种感知距离指标。
2. `RI_i` 是障碍影响区半径。
3. 它们共同决定模式切换。

### 语义边界

这篇论文的语义边界很清楚：

1. 它只建模两类高层控制模式，不覆盖更复杂任务层次。
2. 重点是连续动力学与模式切换，不讨论概率性或通信协议。
3. 传感不确定性通过区间状态进入 reachability，不是通过随机模型进入。
4. 目标是稳定性与可达包络验证，而不是最优轨迹规划。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| unicycle 动力学 | `$\dot{z} = f(z,u)$` | 给出移动机器人连续状态演化。 |
| 混成自动机 | `$H = (Q, X, P, F, T, RI)$` | 把控制器切换显式化。 |
| 模式集合 | `$Q = \{q_1, q_2\}$` | 仅含目标吸引与障碍绕行两档。 |
| 目标误差控制 | `$(e_x,e_y)$` 与比例控制律 | 证明目标吸引模式渐近稳定。 |
| limit-cycle 绕障 | `$(\dot{x}_s,\dot{y}_s)$` | 定义障碍周围连续轨迹。 |
| reachability 包络 | hybrid bounding | 用区间方法包住所有可能轨迹。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 离散模式与连续状态共同存在。 |
| 事件 / 触发 | 中等支持 | 模式切换由障碍距离阈值触发。 |
| 守卫 / 数据 | 强支持 | `DPRO_i` 与 `RI_i` 明确作为 guard。 |
| 层次 | 弱支持 | 仅两层：控制模式选择 + 连续控制器。 |
| 并发 / 同步 | 不强调 | 主体是单机器人。 |
| 时间约束 | 部分支持 | 关注 reachability over time，但无 clocks。 |
| 连续动态 / 随机性 | 强连续、弱随机 | 连续 ODE 是核心；不确定性以区间而非概率进入。 |
| 可执行 / 可验证性 | 强验证 | 可做 reachability over-approximation 与稳定性验证。 |

### 形式化问题与性质

1. 论文真正补出的，不是“有两个控制器”这个常识，而是“如何把两控制器切换骨架稳定地放进混成自动机并验证”。
2. 目标吸引与绕障控制分别有局部 Lyapunov 论证。
3. 整体安全性依赖 hybrid automaton + interval analysis 组合，而不是纯仿真。
4. 因而它是 `Hybrid Automata` 主干在移动机器人导航方向上的稳定应用侧证。

## 构造方式与承载格式

### 建模入口

建模入口遵循以下顺序：

1. 写出 unicycle 运动学。
2. 为目标吸引和障碍绕行分别设计控制律。
3. 用感知距离阈值设计 action selection block。
4. 将两套控制律和切换条件封装进 `Hybrid Automaton`。
5. 通过区间积分算法求可达包络。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. unicycle ODE。
2. `HA` 六元组。
3. Taylor interval integration。
4. hybrid bounding algorithm。

### 交换与互操作

互操作重点在：

1. 传感器如何给出障碍距离区间。
2. 控制器如何把连续误差映射为 `v/\omega`。
3. hybrid automaton 如何把两套控制律和切换 guard 统一承载。

## 配套基础设施

- 建模/编辑工具：原文没有专门图形编辑器，模型主要以数学定义给出。
- 解析/交换/元模型支持：无独立 XML/JSON/元模型标准。
- 仿真/执行支持：提供数值仿真与包络计算。
- 验证/分析支持：`hybrid bounding method`、Taylor interval integration、reachability analysis。
- 代码生成/转换支持：原文未提供自动代码生成。
- 标准化或社区生态：依托 `Hybrid Automata`、Lyapunov 分析和区间分析研究线；明确使用 `MATLAB/INTLAB`。

## 适用场景与需求前提

### 适用场景

适合存在有限控制模式切换、连续运动学必须保留、且需要对“切换后是否仍稳定/安全”进行形式验证的移动机器人导航问题。

### 需求前提

1. 机器人连续动力学可写成显式 ODE。
2. 控制模式数量有限，且切换 guard 可由传感器阈值表达。
3. 环境不确定性可保守地写成区间。
4. 验证目标是 reachability / stability，而不是全局最优规划。

### 不适用或高成本场景

如果系统有大量离散任务层次、复杂多机器人通信或强随机环境，仅靠这种二模态混成自动机很快就会不够用。

## 与相邻形式主义的关系

相对 [a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md](../a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md)，本文更强调 reachability 验证和区间包络；相对 [verification-of-periodically-controlled-hybrid-systems-application-to-an-autonomous-vehicle/desc.md](../verification-of-periodically-controlled-hybrid-systems-application-to-an-autonomous-vehicle/desc.md)，它不关心周期控制节拍，而更关心 mode switching navigation；相对 [a-modular-hybrid-system-architecture-for-autonomous-urban-driving/desc.md](../a-modular-hybrid-system-architecture-for-autonomous-urban-driving/desc.md)，它是更轻量的双模态导航架构。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提供了一个很清晰的例子：当需求里同时出现“连续运动学”“多控制器切换”“障碍感知阈值”时，普通离散状态机已经不够，需要显式提升到混成自动机。

### 作为目标形式主义还是中间表示

对移动机器人导航验证，它可以直接作为目标形式主义；对更复杂的机器人任务系统，它也可以作为底层运动控制层的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时要显式识别控制模式切换条件。
2. 不应只生成离散状态图，还要补上各 mode 下的连续方程。
3. 若用户后续关心安全包络，区间分析所需的不确定性范围也应在需求阶段被收集。

## 重要的相关工作

- [a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md](../a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md)：更早的移动机器人混成协调路线。
- [a-modular-hybrid-system-architecture-for-autonomous-urban-driving/desc.md](../a-modular-hybrid-system-architecture-for-autonomous-urban-driving/desc.md)：自动驾驶情境下的层次混成架构。
- [verification-of-periodically-controlled-hybrid-systems-application-to-an-autonomous-vehicle/desc.md](../verification-of-periodically-controlled-hybrid-systems-application-to-an-autonomous-vehicle/desc.md)：强调周期控制结构的另一条混成验证路线。

## 文献分类总结

- 这是一篇 `🌊` 类高价值应用条目，核心贡献是把多控制器移动机器人导航压成可做区间可达性验证的 `Hybrid Automaton`。
- 其描述客体是连续运动中的物理机器人，因此记为 `🌡️`；论文语境也落在机器人 `CPS`，因此记为 `🌡️`。
- 对 `project_1` 来说，它补足了“控制器切换 + 连续运动学 + reachability 验证”这一类需求到混成模型的证据。

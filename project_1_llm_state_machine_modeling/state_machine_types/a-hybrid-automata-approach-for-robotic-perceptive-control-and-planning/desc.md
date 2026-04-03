# 面向机器人感知控制与规划的混成自动机方法 / A Hybrid Automata Approach for Robotic Perceptive Control and Planning

## 基本信息

- 标题：A HYBRID AUTOMATA APPROACH FOR ROBOTIC PERCEPTIVE CONTROL AND PLANNING
- 中文标题：面向机器人感知控制与规划的混成自动机方法
- 作者：Yu Sun, Ning Xi
- 发表：*IFAC Proceedings Volumes*, Vol. 38, No. 1, pp. 778-783, 2005
- DOI：`10.3182/20050703-6-CZ-1902.00530`
- 链接：https://doi.org/10.3182/20050703-6-CZ-1902.00530
- 形式主义：`Hybrid Perceptive Automata / Hybrid Perceptive Framework`
- 主类：🌊 混成/随机扩展
- 对象类型：🧪 应用/案例
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：机器人感知控制与路径规划 / 混成自动机应用架构
- 工具/实现获取方式：原文给出 hybrid language、perceptive automata、hierarchical task/action/motion planner 的形式结构和稳定性结论，但未提供公开代码或工具仓库。
- 标准/格式获取方式：承载方式是 `Hybrid Language`、perceptive/hybrid/hierarchical automata 元组和 Lyapunov 切换条件；无独立交换格式。

## 简报

这篇论文把机器人感知控制写成一个“离散任务/动作 + 连续参考轨迹”耦合的混成自动机体系。作者先定义 hybrid language 与 perceptive automaton，再把 task scheduler、action planner 和 motion planner 都建成混成自动机/层次自动机，并用多 Lyapunov 函数讨论切换稳定性；当感知参考被障碍等 unexpected event 阻断时，系统通过离散切换转入新任务，再回到原任务轨迹。

- 形式主义定位：它属于 `Hybrid Automata` 在机器人感知控制与路径规划上的应用条目，重点是 hybrid perceptive reference 与任务/动作/运动三层切换。
- 构造方式简述：先把 task/action/reference 都扩成带数值参数的 hybrid language，再用 perceptive/hybrid/hierarchical automata 组织模式切换和连续输出。
- 基础设施与场景简述：原文主要以数学模型和稳定性证明呈现，应用场景是移动操作机器人在搬运任务中遇到障碍后切换到 obstacle avoidance 并恢复原路径。

```text
任务/动作/感知参考 -> hybrid language -> perceptive / hybrid / hierarchical automata -> controller switching + unexpected-event handling -> stable reference evolution
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. task set、action set 与 task/action reference sets。
2. hybrid language `L_H`。
3. perceptive automaton、hybrid automaton 和 hierarchical automaton。
4. task scheduler、action planner、motion planner 三层控制器。
5. Lyapunov-like switching stability 条件与 unexpected event recovery。

### 核心抽象

原文先定义 perceptive automaton：

$$
M_e = (Q, \Sigma, \Sigma_R, \delta, Q_0, \eta, O)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是离散状态集合。
2. `$\Sigma$` 是离散控制输入集合。
3. `$\Sigma_R$` 是 reference input 集合。
4. `$\delta$` 是状态转移函数。
5. `$Q_0$` 是初始状态集合。
6. `$\eta$` 是输出函数。
7. `$O$` 是输出集合。

对应的转移/输出关系写成：

$$
q_j = \delta(q_i, \sigma_j),\qquad O_k = \eta(q_i, \sigma_k)
$$

其中 `$q_i,q_j \in Q$`，`$\sigma_j \in \Sigma$`，`$\sigma_k \in \Sigma_R$`。

混成自动机进一步加入连续变量：

$$
M_H = (Q, X, \Sigma, \delta, Q_0, \eta, O)
$$

$$
q_j = \delta(q_i, \sigma_j, X),\qquad O_k = \eta(q_i, \sigma_i, X)
$$

上式中的符号逐项解释如下：

1. `$X$` 是连续变量集合。
2. 离散输入 `$\sigma_j$` 和连续变量 `$X$` 一起决定 mode transition。
3. 输出函数 `$\eta$` 也可依赖当前 mode 和连续状态。

层次结构被写成：

$$
M_h = (Q_U, Q_{EM}, \Sigma_U, \Sigma_{EM}, \delta_U, \delta_{EM}, Q_{U0}, Q_{EM0}, O)
$$

上式中的符号逐项解释如下：

1. `$Q_U$` 是上层自动机节点集合。
2. `$Q_{EM}$` 是嵌入到上层节点中的子自动机状态集合。
3. `$\Sigma_U,\Sigma_{EM}$` 分别是上层/嵌入层输入集合。
4. `$\delta_U,\delta_{EM}$` 分别是两层转移函数。
5. `$Q_{U0},Q_{EM0}$` 是两层初始状态集合。

### 一个最小例子与通俗解释

论文的移动操作机器人例子可以抽成这样一个最小流程：

1. 默认任务是“去目标点搬运物体”，task scheduler 输出 `T1(...)`。
2. action planner 生成对应动作 `A1(...)`，motion planner 按连续参考 `s` 输出轨迹。
3. 若障碍物阻断参考演化，则触发 unexpected event，task scheduler 切到 `T2(m_o,n_o,l_o)`。
4. action planner 进入 obstacle avoidance 对应状态，motion planner 切换到新的连续向量场。
5. 脱离阻塞区域后再回到原任务轨迹，继续完成搬运。

通俗地说，这个模型像“带连续轨迹记忆的层次状态机”：高层决定当前做哪个任务，中层决定用哪类动作，底层每个 mode 里真的跑连续控制器；遇到障碍时先切模式绕开，再把原来的参考轨迹接回来。

### 运行 / 接受 / 转移语义

论文把 task scheduler、action planner 和 motion planner 都实例化为混成感知自动机，例如：

$$
M_{TaskSch} = (Q, \Sigma_T^H, \Sigma_{RT}^H, X, \delta, Q_0, \eta, O_{TaskSch})
$$

$$
M_{ActPlan} = (Q, \Sigma_T^H, \Sigma_{RA}^H, X, \delta, Q_0, \eta, O_{ActPlan})
$$

$$
M_{MotPlan} = (Q, \Sigma_A^H, s, X, \delta, Q_0, \eta, O_{MotPlan})
$$

上式中的符号逐项解释如下：

1. `$\Sigma_T^H,\Sigma_{RT}^H,\Sigma_{RA}^H,\Sigma_A^H$` 是由任务、任务参考、动作参考、动作集合扩展出来的 hybrid language alphabets。
2. `$s$` 是连续 perceptive reference。
3. 三个自动机分别承担任务生成、动作序列规划和连续轨迹生成。

motion planner 的离散切换与连续输出分别写成：

$$
q^{MotPlan}_j = \delta(q^{MotPlan}_i, \sigma_j),\qquad \sigma_j \in \Sigma_A
$$

$$
O^{MotPlan}_k = \eta(q^{MotPlan}_i, s)
$$

其中 `$O^{MotPlan}_k` 可以是完整轨迹向量 `$\left[X(s), Y(s), \dot{X}(s), \dot{Y}(s)\right]^T$`。

对 unexpected event，原文给出的阻塞条件可保守写成：

$$
\left.\frac{ds}{dt}\right|_{s_u^h} = 0,\qquad s_u^h \notin \{STR_i, SAR_j\}
$$

上式中的符号逐项解释如下：

1. `$s_u^h$` 是发生阻塞时的 hybrid reference 点。
2. `$STR_i$` 与 `$SAR_j$` 是离散 task/action reference 值。
3. 第一式表示连续参考停止演化，第二式表示该点不是正常离散参考点。

稳定性部分，原文用 Lyapunov-like 函数约束切换序列。可保守整理为：

$$
\frac{dV_i(x(s_h))}{ds} \le 0
$$

并要求 `$V_i$` 在离散参考序列上单调不增。若所有切换序列上的各 mode 向量场都满足对应的 Lyapunov-like 条件，则系统在 Lyapunov 意义下稳定。

### 语义边界

这篇论文的边界主要有：

1. 它强调任务/动作/运动三层切换和参考演化，不是通用混成可达性算法论文。
2. 论文给的是稳定性充分条件和恢复逻辑，而不是完整自动模型检查工具链。
3. 不确定事件主要以局部阻塞和新向量场切换来处理，不是概率混成模型。
4. 更适合有明确任务层次和可设计连续控制器的机器人系统。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 感知自动机 | `$M_e = (Q, \Sigma, \Sigma_R, \delta, Q_0, \eta, O)$` | 把离散控制输入与参考触发输出分开建模。 |
| 混成自动机 | `$M_H = (Q, X, \Sigma, \delta, Q_0, \eta, O)$` | 用 mode + 连续变量共同决定切换与输出。 |
| 层次自动机 | `$M_h = (Q_U, Q_{EM}, \Sigma_U, \Sigma_{EM}, \delta_U, \delta_{EM}, Q_{U0}, Q_{EM0}, O)$` | 上层任务节点可嵌入子自动机。 |
| 参考阻塞判定 | `$\left.ds/dt\right|_{s_u^h} = 0$` | unexpected event 会让连续参考停止演化。 |
| 切换稳定性 | `$dV_i(x(s_h))/ds \le 0$` | 多 Lyapunov 函数给出切换稳定性充分条件。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 任务、动作和运动规划层都有离散 mode。 |
| 事件 / 触发 | 强支持 | 任务输入、动作输入和 unexpected event 都是显式触发。 |
| 守卫 / 数据 | 强支持 | hybrid language 把离散符号和数值参考一起带入输入。 |
| 层次 | 强支持 | 上层 automaton 可嵌入子 automata，形成 task/action/motion hierarchy。 |
| 并发 / 同步 | 部分支持 | 论文主线是层次切换，不强调多主体同步。 |
| 时间约束 | 部分支持 | 重点是参考参数 `s` 上的演化与切换稳定性，不是 clock automata。 |
| 连续动态 / 随机性 | 强连续、无随机 | 每个 mode 内有连续向量场，但不建概率语义。 |
| 可执行 / 可验证性 | 可执行建模、弱工具化 | 理论上可直接驱动控制切换，但缺少公开验证/执行工具链。 |

### 形式化问题与性质

1. 论文最有价值的部分是把“感知参考本身也可能被阻塞”这个机器人问题纳入混成状态机结构。
2. task/action/motion 三层都用 automata 建模，使控制架构本身具有统一状态机骨架。
3. Lyapunov-like 条件为 mode switching 的稳定性提供了可追溯语义约束。
4. 对 `Hybrid Automata` 主干来说，这篇论文补出了“感知参考 + 异常恢复”这一类应用侧证。

## 构造方式与承载格式

### 建模入口

建模步骤可概括为：

1. 先定义 task/action/reference 集合。
2. 把离散符号和连续参数扩成 hybrid language。
3. 为 task scheduler、action planner 和 motion planner 分别建 automaton。
4. 用层次嵌入和状态切换把三层连接起来。
5. 为 unexpected events 设计局部避障任务和回跳逻辑。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `Hybrid Language`。
2. perceptive/hybrid/hierarchical automata 元组。
3. 连续轨迹向量 `O(s)`。
4. Lyapunov-like switching 条件和 Lie-derivative 约束。

### 交换与互操作

论文没有独立交换标准，互操作主要体现在：

1. 高层任务引用通过 hybrid language 下传。
2. action planner 输出动作到 motion planner。
3. motion planner 把参考参数化轨迹输出给底层控制器。

## 配套基础设施

- 建模/编辑工具：原文未给专用编辑器或建模器。
- 解析/交换/元模型支持：没有 XML/JSON/元模型标准。
- 仿真/执行支持：论文面向机器人规划控制执行，但未给可下载运行时。
- 验证/分析支持：主要是 Lyapunov-like 稳定性分析和 Lie derivative 条件。
- 代码生成/转换支持：原文未提供自动代码生成。
- 标准化或社区生态：建立在 hybrid automata、motion description language 和 perceptive control 研究线上。

## 适用场景与需求前提

### 适用场景

适合移动机器人/移动操作机器人在动态环境中做任务切换、障碍绕行、参考轨迹恢复和连续控制切换的场景。

### 需求前提

1. 任务集合、动作集合和参考参数需要能显式结构化。
2. 每个 mode 内的连续控制律或轨迹生成器要可写成向量场/输出函数。
3. unexpected event 要能检测，并能触发离散回跳任务。
4. 系统验证目标偏稳定性和可恢复性，而不是最优性或概率风险。

### 不适用或高成本场景

当主要难点在多机器人通信协议、复杂离散资源竞争或大规模概率不确定性时，这种以 hybrid reference 和切换稳定性为中心的模型不够直接。

## 与相邻形式主义的关系

相对 [a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md](../a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md)，本文更强调 perceptive reference 和 unexpected-event recovery；相对 [hybrid-and-multi-controller-architecture-for-autonomous-system-application-to-the-navigation-of-a-mobile-robot/desc.md](../hybrid-and-multi-controller-architecture-for-autonomous-system-application-to-the-navigation-of-a-mobile-robot/desc.md)，本文的层次控制架构更明显，但工具化和 reachability 分析更弱；相对 [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)，本文是应用架构条目而不是判定性理论条目。

## 与本研究的关系

### 对 Project 1 的价值

它说明：当需求文本中同时出现“任务层切换、动作层选择、连续轨迹参考、障碍导致参考阻塞”时，普通离散状态机不够，需要把混成变量和恢复切换一并抽出。

### 作为目标形式主义还是中间表示

对机器人感知控制架构，它可以直接作为目标形式主义；对更大系统，它也适合作为运动层或执行层的混成子模型。

### 对需求到模型生成的启发

1. 需求抽取要识别哪些变量是离散任务符号，哪些变量是连续参考参数。
2. 状态机生成时要把“异常打断后如何回到原任务”显式写成回跳边。
3. 若要保证切换合理，模型中最好保留 per-mode 稳定性或单调性约束。

### 现实限制

论文模型更像可分析架构蓝图，而不是直接可落地的标准语言/工具链；若要工程化，需要额外补执行框架与模型转换层。

## 重要的相关工作

### 奠基或前身工作

1. 原文明确承接了作者此前的 perceptive frame / event-based planning and control 研究。
2. `Hybrid Automata`、Brockett motion description language 和多 Lyapunov 稳定性分析是主要理论背景。

### 同类型或同家族工作

1. [a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md](../a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md) 是更偏行为协调和 sliding regularization 的移动机器人混成路线。
2. [formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md](../formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md) 则更偏 `HyTech` 可达性分析。

### 标准 / 格式 / 工具链工作

1. 原文没有公开工具仓库或标准承载格式。
2. 其主要价值在形式化架构和稳定性条件，而不是工具生态。

### 与本研究关系最紧的工作

1. 它为“任务语言 + 混成自动机 + 异常恢复”提供了可以直接借鉴的层次模板。
2. 对 `project_1` 来说，这种模板有助于判断哪些需求必须提升到混成状态机而不能停留在 FSM。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧪 应用/案例
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Hybrid Perceptive Automata / Hybrid Perceptive Framework`
- 论文角色：机器人感知控制与路径规划 / 混成自动机应用架构
- 核心功能：用混成感知参考和层次自动机统一任务切换、动作规划、连续轨迹输出和异常恢复
- 关键特性：hybrid language、perceptive automata、hierarchical embedding、Lyapunov-like switching stability、unexpected-event recovery
- 构造方式：task/action/reference 集合 -> hybrid language -> task/action/motion 三层 automata
- 基础设施：数学模型 + 稳定性分析，缺少公开工具链
- 适用场景：移动机器人感知控制、障碍绕行、任务恢复
- 需求前提：任务层次、动作集合和连续参考必须可结构化
- 状态：🟢

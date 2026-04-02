# 使用广义随机 Petri 网设计导航行为及其选择框架 / Design of Navigation Behaviors and the Selection Framework with Generalized Stochastic Petri Nets toward Dependable Navigation of a Mobile Robot

## 基本信息

- 标题：Design of Navigation Behaviors and the Selection Framework with Generalized Stochastic Petri Nets toward Dependable Navigation of a Mobile Robot
- 中文标题：使用广义随机 Petri 网设计导航行为及其选择框架
- 作者：Chang-bae Moon，Woojin Chung
- 发表：*2010 IEEE International Conference on Robotics and Automation (ICRA 2010)*，pp. 2989-2994，2010
- DOI：`10.1109/ROBOT.2010.5509345`
- 链接：https://doi.org/10.1109/ROBOT.2010.5509345
- 形式主义：`GSPN-based Navigation Behavior Selection Framework`
- 主类：🕸️
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：移动机器人导航行为选择 / `GSPN` 应用建模
- 工具/实现获取方式：原文明确基于 `Player/Stage` 做仿真，并把 `DWA` 与 trajectory tracking 控制器接入 `GSPN` 选择框架；论文未提供独立公开代码仓库。
- 标准/格式获取方式：承载方式是 `GSPN` places/transitions、Poisson/Exponential rate 估计与 throughput-based behavior selection；原文未给统一交换标准。

## 简报

这篇论文要解决的问题很实用：单一导航控制器很难在所有环境都表现稳定，`DWA` 擅长动态障碍环境，但容易卡在局部最小值；tracking 擅长沿规划路径走，但在动态环境中频繁重规划。作者没有把二者简单切换，而是用 `GSPN` 把“当前选哪个行为”“planner 是否告警”“reactive 是否告警”“任务成功/失败”统一成一张随机网，并用 throughput 估计当前哪个行为更值得选。

- 形式主义定位：这是 `Petri Nets` 主干上的应用型条目，核心价值是展示 `GSPN` 如何做导航行为 arbitration，而不是只做任务流表示。
- 构造方式简述：用 places 表示行为与内部状态，用 timed/immediate transitions 表示选择、切换、告警、恢复和完成/失败，再根据导航统计量在线更新 firing rates。
- 基础设施与场景简述：依托 `GSPN`、`Player/Stage`、`DWA` 和 trajectory tracking，服务于室内移动机器人在静态/动态/门洞等混合环境中的 dependable navigation。

```text
navigation task + environment status -> GSPN behavior/status model -> throughput estimation -> tracking / DWA selection -> faster and more dependable navigation
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 用于行为选择的 `GSPN`。
2. 两个导航行为：`tracking` 与 `DWA`。
3. 两个内部状态子系统：planner normal/warning 与 reactive normal/warning。
4. 成功/失败 transition 及其 firing rates。
5. 基于 Poisson / Exponential 近似的状态估计与恢复机制。

### 核心抽象

论文没有显式给出 `GSPN` 元组，但根据 Fig.1 和 Table I，可保守整理为：

$$
N = (P, T_t, T_i, I, O, M_0, \Lambda, W)
$$

上式中的符号逐项解释如下：

1. `P` 是 places 集合，对应 `P_0 \ldots P_9` 这类导航准备、行为选择、planner/reactive 状态和成功/失败标记。
2. `T_t` 是 timed transitions 集合，如 `T_0, T_1, \ldots, T_{12}, T_{a6}, T_{a8}`。
3. `T_i` 是 immediate transitions 集合，如无条件替换和任务收尾跳转。
4. `I` 与 `O` 分别是输入弧和输出弧关系。
5. `M_0` 是初始 marking。
6. `\Lambda` 是 timed transitions 的 firing-rate 函数。
7. `W` 是 immediate transitions 的权重集合。
8. 这是基于原文图和表做的保守标准化整理。

论文明确给出导航性能估计公式：

$$
v_e = \frac{dist_{opt}}{t_{navi}}
$$

$$
\lambda_i = \frac{v_e}{dist_{opt}}
$$

$$
t_{fail} = \frac{dist_{opt}}{v_{fail}}
$$

上式中的符号逐项解释如下：

1. `dist_{opt}` 是最短路径长度。
2. `t_{navi}` 是一次导航任务的总耗时。
3. `v_e` 是经验速度，用于量化某一行为在历史任务中的平均推进效率。
4. `\lambda_i` 是转换后的 `GSPN` firing rate。
5. `v_{fail}` 是作者定义的 failure velocity，用来给失败判定设时限。
6. `t_{fail}` 以上限方式判断“导航时间过长即视为失败”。

对于 warning event 的状态估计，论文把计数过程建成 Poisson 模型：

$$
N_i \sim \mathrm{Poisson}(T_c \lambda_i)
$$

并使用：

$$
p_j(N_c \mid T_c) = e^{-\lambda_j T_c} \frac{(\lambda_j T_c)^{N_c}}{N_c!}
$$

上式中的符号逐项解释如下：

1. `N_i` 是单位时间窗内的 warning 事件计数。
2. `T_c` 是监控时间窗。
3. `\lambda_i` 是对应 warning 事件频率。
4. `p_j(N_c \mid T_c)` 是给定时间窗内观察到计数 `N_c` 的 Poisson 概率。
5. 作者用这个概率配合 token probability 推断 planner/reactive 子系统是否已经进入 warning 状态。

### 一个最小例子与通俗解释

最直观的例子就是机器人在走廊和门洞里交替导航：

1. 如果环境较静态，tracking 更适合沿最优路径走。
2. 如果障碍物很多、路径重规划频繁，planner 会进入 warning，系统就更倾向切到 `DWA`。
3. 如果 `DWA` 速度降得太低、接近局部困境，reactive 会进入 warning，系统就反过来切回 tracking。
4. 成功/失败 transition 再根据 throughput 和耗时统计更新后续选择倾向。

通俗地说，这像“把两个导航器和两个健康指示灯都塞进一张随机 Petri 网里”，让系统根据最近的导航表现自己判断该用哪套策略，而不是写死 if-else。

### 运行 / 接受 / 转移语义

运行语义可以概括为：

1. `T_0` 触发后，token 进入 `P_1`，开始本次导航任务与行为评估。
2. 若 tracking throughput 更高，则 `T_1` 使 token 进入 tracking；否则 `T_2` 进入 `DWA`。
3. planner/reactive warning 与 recovery transitions 根据计数阈值和恢复时间触发。
4. `T_9 / T_{10}` 表示两种行为下的成功完成，`T_{11} / T_{12}` 表示失败。

作者的决策标准是比较成功 transitions 的 throughput。若 `tracking` 对应 `T_9` 的 throughput 高于 `DWA` 对应 `T_{10}`，就选 tracking；反之就选 `DWA`。因此，行为选择不是静态规则，而是根据 steady-state probability 和 rate 联合得到的性能估计。

### 语义边界

这篇论文的边界主要在于：

1. `GSPN` 层只负责高层行为选择，不直接替代底层运动控制器。
2. 连续动力学细节被压缩进 `DWA` 和 tracking 控制器内部，不在 Petri 网中直接求解。
3. 环境状态估计依赖经验计数与简化统计分布。
4. 场景验证主要在仿真环境中完成。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `GSPN` 骨架 | `$N = (P, T_t, T_i, I, O, M_0, \Lambda, W)$` | 用随机网表达行为选择与内部状态。 |
| 经验速度 | `$v_e = \frac{dist_{opt}}{t_{navi}}$` | 把一次导航结果转成可更新的性能指标。 |
| 成功率映射 | `$\lambda_i = \frac{v_e}{dist_{opt}}$` | 把经验速度转成 `GSPN` firing rate。 |
| 失败时间阈值 | `$t_{fail} = \frac{dist_{opt}}{v_{fail}}$` | 导航超过该时限即记为失败。 |
| warning 事件模型 | `$N_i \sim \mathrm{Poisson}(T_c \lambda_i)$` | 用计数模型估计内部 warning 状态。 |
| Poisson 概率 | `$p_j(N_c \mid T_c) = e^{-\lambda_j T_c} \frac{(\lambda_j T_c)^{N_c}}{N_c!}$` | 给 planner/reactive warning 事件赋统计语义。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | behavior selection、planner/reactive 正常/告警和 success/failure 都是显式 places。 |
| 事件 / 触发 | 强支持 | 选择、切换、告警、恢复、完成与失败都由 transitions 建模。 |
| 守卫 / 数据 | 部分支持 | 重点是统计量与 token probability，不是复杂数据流。 |
| 层次 | 部分支持 | 有行为层和内部状态层，但不是严格层次 Petri net。 |
| 并发 / 同步 | 强支持 | `GSPN` 自然刻画多个子系统状态并发。 |
| 时间约束 | 部分支持 | timed transitions 与恢复时间存在，但不是时钟自动机式严密 deadline。 |
| 连续动态 / 随机性 | 部分随机 | 控制器本身连续，网层通过 `GSPN` 概率/速率近似其表现。 |
| 可执行 / 可验证性 | 强支持 | 可接仿真控制器并做 steady-state / throughput 分析。 |

### 形式化问题与性质

1. 作者展示的不是“Petri 网能描述导航任务”，而是“Petri 网能把多个导航控制器的选择逻辑建成可分析对象”。
2. `planner warning` 与 `reactive warning` 两个子系统让经验式行为切换有了结构化解释。
3. 通过 throughput 选行为，相当于把离散控制切换建立在随机性能估计之上。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先确定候选导航行为，如 tracking 与 `DWA`。
2. 为行为、内部状态和任务结果建立 places。
3. 为行为切换、warning/recovery、success/failure 建立 timed/immediate transitions。
4. 用仿真结果估计 `v_e`、`\lambda_i`、`t_{fail}` 和 warning 计数阈值。
5. 通过 steady-state probability 和 throughput 做 behavior selection。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `GSPN` 图模型。
2. firing rates 与 transition probabilities。
3. `Player/Stage` 导航仿真结果。
4. `DWA` 与 tracking 控制器接口。

### 交换与互操作

互操作重点在：

1. 统计导航表现如何反馈到 `GSPN` firing rates。
2. `GSPN` 决策如何切换到底层控制器。
3. planner/reactive warning 的离散状态如何从连续运动过程里抽取。

## 配套基础设施

- 建模/编辑工具：原文基于 `GSPN` 建模与性能估计方法。
- 解析/交换/元模型支持：无统一交换标准，主要是论文中的网结构和参数公式。
- 仿真/执行支持：`Player/Stage`、`DWA`、trajectory tracking。
- 验证/分析支持：steady-state probability、throughput、failure-rate 估计。
- 代码生成/转换支持：原文未给自动代码生成链。
- 标准化或社区生态：依托 `Petri Net / GSPN` 与移动机器人导航仿真生态。

## 适用场景与需求前提

### 适用场景

适合在静态与动态环境之间频繁切换的室内移动机器人导航，以及需要在多个导航行为之间做可靠 arbitration 的场景。

### 需求前提

1. 候选行为集合较小且可明确切换，如 tracking 与 `DWA`。
2. 能从运行日志中估计成功率、失败率和 warning 频次。
3. 任务结果可以用 success / failure 这类离散口径汇总。
4. 关注的是高层行为选择，而不是底层轨迹控制器设计。

### 不适用或高成本场景

如果系统需要直接优化连续控制律、全局多机器人调度或复杂资源分配，仅用这个轻量 `GSPN` 行为选择框架会不够。

## 与相邻形式主义的关系

相对 [Petri Net Robotic Task Plan Representation: Modelling, Analysis and Execution](../petri-net-robotic-task-plan-representation-modelling-analysis-and-execution/desc.md)，本文更轻、更偏导航控制器 arbitration，而不是完整任务/动作/环境三层建模；相对 [Execution Control of Robotic Tasks: A Petri Net-Based Approach](../execution-control-of-robotic-tasks-a-petri-net-based-approach/desc.md)，这里关注行为选择与性能估计，而不是任务执行监督；相对 [Petri Net Based Multi-Robot Task Coordination from Temporal Logic Specifications](../petri-net-based-multi-robot-task-coordination-from-temporal-logic-specifications/desc.md)，这里不做高层逻辑任务综合，而是面向单机器人导航策略切换。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：即使底层控制器很连续、很数值化，上层“何时切换行为”仍然可以抽成 Petri 网，并成为需求到模型生成的重要对象。

### 作为目标形式主义还是中间表示

对行为 arbitration 这类模块，它可以作为目标形式主义；对更大的机器人系统，它更适合作为高层执行管理的中间表示。

### 对需求到模型生成的启发

1. 需求里的“在动态环境中切换到更鲁棒行为”可以显式生成 warning/recovery 子网。
2. 行为选择可以绑定性能统计量，而不是只能绑定手写条件。
3. `Petri Net` 很适合表达“多个诊断子系统并发决定一个控制器切换”的模式。

## 重要的相关工作

- [Petri Net Robotic Task Plan Representation: Modelling, Analysis and Execution](../petri-net-robotic-task-plan-representation-modelling-analysis-and-execution/desc.md)：更完整的任务/动作/环境 `Petri` 建模框架。
- [Execution Control of Robotic Tasks: A Petri Net-Based Approach](../execution-control-of-robotic-tasks-a-petri-net-based-approach/desc.md)：机器人任务执行监督控制。
- [A Petri Net On-Line Controller for the Coordination of Multiple Mobile Robots](../a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md)：多移动机器人在线控制。
- [Long-Run Multi-Robot Planning under Uncertain Action Durations for Persistent Tasks](../long-run-multi-robot-planning-under-uncertain-action-durations-for-persistent-tasks/desc.md)：更强的随机 Petri / reward synthesis 路线。

## 文献分类总结

- 这是一篇 `🕸️` 类应用型条目，核心价值是用 `GSPN` 统一建模导航行为选择、内部告警状态和成功/失败统计。
- 它描述的是移动机器人导航控制器的离散切换逻辑，因此记为 `🎛️`；研究语境属于机器人导航与物理场景运行，因此记为 `🌡️`。
- 对 `project_1` 来说，这篇论文很有启发性，因为它说明了：上层行为选择不必被底层连续控制掩盖，完全可以独立生成成网模型。

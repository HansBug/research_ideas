# 基于 IMPC 的车辆超车决策监督器 / Improved MPC for trajectory planning of self-driving cars

## 论文在讲什么

这篇论文讨论的是自动驾驶车辆在动态交通环境中的避障和超车问题。作者整体方法叫 IMPC，底层还是 MPC 轨迹规划，但论文的关键点之一是把“什么时候刹车、什么时候换道、什么时候回到原车道”单独抽成了一个 FSM 决策层，由它向 MPC 提供激活函数和约束切换信号。

因此，这篇文章并不是只有连续优化公式。它把系统拆成两层：上层是 decision-making，下层是 trajectory-planning。上层根据前车距离、左侧车道占用和前后安全距离做离散判断，下层才根据这些判断去生成 S 形超车轨迹和纵横向加速度输出。

## 控制系统在文中的位置

我们关心的控制系统描述在文中属于核心功能模块，而不是附带说明。正文先讲真实驾驶场景里前车减速、左车道占用、超车完成后回归本车道这几个典型问题，再说明 FSM 如何把这些场景翻译成 `brake`、`lane change`、`continue driving` 这类离散动作，并由 `δk / γk` 驱动 MPC 切换约束。

也就是说，论文真正的结构不是“只有一个优化器，然后顺便提了个状态机”。FSM 决策层负责定义哪些 maneuver 是当前合法的、何时需要从跟车转向制动、何时可以发起换道、何时才允许结束超车返回原车道。没有这一层，后面的 MPC 就缺少可执行的离散驾驶意图。

## 对我们为什么有用

对 `sources/` 而言，这篇样本的价值在于它很好地覆盖了“离散决策层 + 连续执行层”这种常见但不容易写清的车辆控制结构。很多自动驾驶论文会把所有东西混在 trajectory planner 里，导致难以抽出明确的状态机主链；这篇则比较干净地保留了 decision layer 的状态流与 guard 条件，因此适合归到 `EFSM + T0 + 连续耦合`。

它也补充了一个比较实用的控制画像：不是纯高速巡航，也不是纯交叉口让行，而是典型的 `front vehicle / adjacent lane / rear safety` 三方约束下的超车监督器。对后续建模来说，这类样本能够帮助区分“动作切换状态机”和“纯路径优化器”的边界。

## 如果需要人工细读，建议怎么读

人工回原文时，建议先读摘要和第 `7-9` 页关于 `Obstacle avoidance trajectory planning`、`FSM-based decision-making` 的部分，优先抓住上层 FSM 的角色：它决定刹车还是超车，并把结果转成 `δk / γk`。随后直接看 Fig. 4，把 `Normal vehicle operation`、`Brake following`、`Execute lane change`、`Continue driving` 这些节点与图里的距离判定条件对应起来。

如果还要进一步补连续层实现，再回看 Sigmoid barrier 与 MPC 约束那几节，确认 FSM 输出如何变成轨迹规划器的输入。更靠后的数值实验和 HIL 验证主要用来证明性能，不是抽取 `STM.md` 时最先需要看的部分。

# 高层 maneuver assigner 与混合预测控制 / Hierarchical Hybrid Predictive Control of an Autonomous Road Vehicle

## 论文在讲什么

这篇论文讲的是一种自动驾驶高速场景下的混合预测控制框架。作者并不满足于分别给跟驰、换道或碰撞规避单独写一个控制器，而是希望用一个高层离散决策模块去统一选择当前 maneuver，再把这个选择交给下层 MPC 去执行。

因此，论文把控制框架切成上层离散 state module 与下层 continuous state module 两部分。上层 assigner 负责根据周围车辆与道路环境决定当前是 `Normal Tracking`、`Following`、`Leading` 还是 `Lane Change`，下层则据此切换对应的 MPC 设置。

## 控制系统在文中的位置

我们关心的控制系统描述是这篇论文的核心设计对象。摘要直接把 assigner 定义成 `finite state machine for decision-making`，第 2-3 节又继续展开 `FSMs`、切换规则、maneuver states 和与 MPC 的接口。

它不是“先有一个黑箱优化器，再补几个模式名”的写法，而是明确把离散 maneuver state 放在架构顶层。也正因为如此，这篇论文对 `sources/` 很有价值：它展示了怎样把连续运动规划系统的上层 supervisor 写成可追溯的离散状态机。

## 对我们为什么有用

这篇论文对样本库的价值，主要在于补充了 `🚗` 方向里一种“连续变量 guard 驱动的 EFSM”样本。相较于只写纯离散模式切换的车辆论文，它更清楚地展现了速度区间、前后车速度和换道许可条件如何作为状态切换判据进入高层控制器。

此外，它把 `S1-S4` 四个 maneuvers 与 lane-change allowance、merge/exit 需求、速度上下界这些条件直接挂钩，后续做数据集时很适合作为“离散 supervisor + 连续执行层”的桥接样本。真正应保留的是这些状态与切换条件，而不是 MPC 方程推导本身。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 1 页摘要和第 2 页 `Control Framework`，先把“高层 assigner 是 FSM、低层是 MPC”这一主结构读稳。然后直接跳到第 3-4 页 `Assigner Maneuver States`，重点读 Table 1 和 Figure 2/3 附近的文字，把 `vf / vr / vt / vlcl / vlch` 这些 guard 变量与 `S1-S4` 的含义一一对应起来。

第 4 节之后的大量 MPC 连续模型、曲率变量和优化式可以留到第二轮再读。对重建 `STM.md` 来说，第一轮最重要的是把高层 assigner 的离散状态、切换规则和 lane-change 返回逻辑固定下来。

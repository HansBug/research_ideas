# 能量受限 UAV 配送竞价与返航控制器 / Ready, Bid, Go! On-Demand Delivery Using Fleets of Drones with Unknown, Heterogeneous Energy Storage Constraints

## 论文在讲什么

这篇 AAMAS 论文研究的是按需配送场景下的 UAV fleet deployment。作者考虑的条件比较现实：不同 UAV 的真实储能能力未知且异构，订单会随机到达，系统又不能依赖精确能耗模型去做集中式规划。因此文章提出了一个 decentralised deployment strategy，把 auction-based task allocation 和 online learning 结合起来。

对我们最重要的是，作者没有把整个系统只写成学习策略黑盒，而是明确给每架 UAV 一个 finite-state machine controller。这个 controller 决定 UAV 何时等待新任务、何时投标、何时根据竞价结果接受任务、何时执行配送、何时因为电量不足而中止并返航。

## 控制系统在文中的位置

我们关心的控制系统描述在文中是主执行逻辑，而不是外层框架说明。学习算法和 bidding policy 的作用，是为这个 controller 的几条关键分支提供 guard；真正的离散主链仍由 `Wait / Bid? / Won? / Deliver / Return` 五个状态串起来。论文的 Figure 2 先把这条状态链画出来，正文 `3.1 UAV Controller` 再逐状态解释输入和迁移条件。

换句话说，这篇论文虽然来自 autonomous agents 方向，但样本并没有漂成纯多智能体博弈稿。作者把单 UAV 的离散行为组织得很清楚：接到任务公告后是否投标、投标后是否中标、中标后何时起飞配送、配送中何时因 `SoC(t) ≤ ξ SoC_takeoff` 提前中止并返回 fulfilment centre，这些都直接写进了控制链。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补的是航空配送方向里一种很有价值的 mission-control 变体。它不是常见的起降/巡航/避障 supervisor，而是把 task announcement、auction outcome、energy-aware abort 和 return-to-base 合并到一条 UAV controller 中，因此很适合作为 `EFSM + T0` 的任务执行样本。

它的另一个价值在于“扩展状态”写得非常明确。`task ID`、`parcel mass`、`delivery distance`、bid value、`SoC_takeoff` 和剩余电量阈值都直接决定迁移，这使它比只靠 nominal phase name 的 UAV mission paper 更适合做 guard 抽取和状态机自动生成实验。

## 如果需要人工细读，建议怎么读

人工回原文时，建议先读摘要和第 `3` 页的 Figure 2 与 `3.1 UAV Controller`，先把单 UAV controller 和上层 auction/learning 的分工分开。第一轮重点要抓的是五个状态、任务公告内容、投标与中标判定、以及 abort condition 如何由 `SoC` 阈值触发。

如果后续还想补 learning 细节，再回看 `3.2 Auction Policies` 以及后面的实验部分，确认 bidding policy 和 bids evaluation policy 如何影响状态转移。那些章节对理解“为什么这条控制链有效”很重要，但做 `STM.md` 时优先级仍低于 Figure 2 和 `3.1` 的离散主链。

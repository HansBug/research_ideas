# 自主水面艇多任务管理与优先级切换 / A ROS-Based GNC Architecture for Autonomous Surface Vehicle Based on a New Multimission Management Paradigm

## 论文在讲什么

这篇论文介绍的是一套基于 `ROS` 的自主水面艇 `GNC` 架构，并在此基础上扩展出一个 multimission management 机制。作者想解决的问题不是单次航线执行，而是长周期运行时同一艘无人艇要在多个任务之间切换、抢占和恢复，因此提出用 mission manager 根据优先级在多个候选 mission 之间实时决策。

论文的系统视角比较完整：既介绍载体硬件和基础导航控制，也把 mission 建模、调度和能量管理写成上层软件架构的一部分。对 `sources/` 来说，真正关键的是它没有停留在“任务调度框架”层，而是明确给出 mission state machine 的外层状态、内层任务状态机、并发任务条件和电池阈值触发的 recharge 抢占机制。

## 控制系统在文中的位置

我们关心的控制对象是这套 `M-GNC` 架构中的 mission manager。它位于基础 `GNC` 能力之上，负责决定当前应该执行哪个 mission、何时中断当前 mission、何时恢复、以及 mission 内部的任务序列怎样组织。换句话说，底层航迹控制和执行器动作只是能力，真正把“长周期自主运行”串成离散控制链的是这个 mission-level 层次状态机。

因此它是全文的主要扩展贡献，而不是一个顺带示例。作者甚至把 mission implementation 直接落到 `SMACH` 上，说明 `Run` 内部可以挂嵌套状态机，必要时还能并发执行互不冲突的任务，这种“任务级 hierarchy + concurrency”在当前文库里并不常见。

## 对我们为什么有用

这篇论文补的是 `⚙️` 方向里非常有价值的“多 mission 监督控制”样本。相比库里一些单任务机器人、单次 docking 或单次 inspection 的状态机，这里更强调在真实运行周期中如何切换任务、处理中断、恢复执行和能量优先级提升，因此更接近复杂自主系统常见的高层控制问题。

它也能明显扩展结构多样性。原文同时保住了外层 `Ready / Run / Interrupted / Terminated`、内层任务状态机、并发执行条件和 recharging mission 抢占链，这使它不只是“另一个 mission FSM”，而是一个带层次和并行语义的强结构样本。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `2` 页引言，把 multimission paradigm 的目标先弄清楚。随后直接跳到第 `9` 页的 `4.1 Mission Modeling` 和 `4.2 Mission Management`，重点看 `Figure 9`、`Figure 10` 周围的文字，先确认 mission 外层四状态、`Run` 内嵌任务状态机、并发任务条件，以及 `Interrupted` 后如何恢复。

硬件、推进器、传感器、基础导航控制等章节可以放到第二轮再看。第一次人工复核时，最值得优先锁定的是“mission manager 如何按优先级选择任务、如何支持并发和抢占、以及低电量怎样提升 recharge mission 优先级”这条高层控制主链。

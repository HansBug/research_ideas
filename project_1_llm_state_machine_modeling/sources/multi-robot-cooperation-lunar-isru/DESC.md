# 月面原位资源利用的多机器人协作控制 / Multi-robot cooperation for lunar In-Situ resource utilization

## 论文在讲什么

这篇论文研究的是 lunar In-Situ resource utilization 场景下，六台 rover 如何分工完成 volatile 搜索、挖掘、运输和倾倒任务。系统包含 Scouts、Excavators 和 Haulers 三类车，外加 central task planner 与 volatile map。论文目标不是单车导航，而是让整支机器人队伍在两小时 mission 中稳定完成搜索、停车、挖掘、装载、运输、倾倒与回充。

文章的方法部分很完整，既讲 localization、perception，也讲具体 coordination。但最有价值的是 Section `5` 里那套 autonomy framework：每台车都有 individual FSM，三种车共享一组公共状态，同时各自扩展任务状态；Excavator 在 `Excavation` 里又继续启用一套 manipulator sub-FSM。这使整篇文章形成了非常完整的层次任务监督结构。

## 控制系统在文中的位置

我们关心的控制系统描述在文中是 mission execution 的核心主线。Section `5` 不是附带讲一个“任务流程”，而是直接说明 autonomous operation consists of central task planner and decentralized FSMs to control individual robots。随后作者把 common states、specialized states、battery threshold、homing recovery、parking/dumping interaction 都逐步展开。

尤其值得注意的是，论文没有只停在 rover 级状态。Excavator 的 `Excavation` state 内部还有 `HomeArm / Search / LowerArm / Scoop / ExtendArm / Drop` 这套嵌套 arm FSM，同时 Excavator 与 Hauler 之间通过专门消息交换 parking side、approach complete、parked bin 等信息。换句话说，它同时给出了 outer mission supervisor 和 inner manipulation supervisor。

## 对我们为什么有用

它对 `sources/` 很有价值，因为这是一类少见的复杂 multi-robot HSM 样本。很多机器人比赛论文会写很多系统介绍，却不把状态骨架、任务切换和恢复条件明确列出；这篇则把 `Planning / Traverse / Localization Recovery / Emergency Charging / Parking / Dumping` 等链条写得非常清楚，还把 arm-level sub-FSM 和 inter-robot messages 一起交代出来。

它也能补强我们对“复杂任务不是只能写成流程图”的认识。这里的时间语义虽然不是 timed automata 那种强实时形式，但 `battery < 30%`、`maximum 12 scoops`、`about 20 min timeout` 都是明确工程 guard；同时 `semaphore`、parking recovery、Hauler-Excavator flags 让这篇论文兼具层次结构和协议交互语义，是很好的高复杂度正样本。

## 如果需要人工细读，建议怎么读

人工重读时，建议直接从 Section `5 Autonomous operation and coordination` 开始，先对照 Figure `6` 抓公共状态与三类 rover 的 specialized states，再看 `5.2`、`5.3`、`5.4` 分别把 Scout、Excavator、Hauler 的状态职责补完整。第一次阅读时，优先把 `Planning -> Traverse -> specialized task -> recovery/charging` 这条大主链读稳。

之后重点看 `5.3.4 Excavation state machine` 与 `5.3.5 / 5.4`，把 nested arm FSM、Hauler approach、parking verification、dumping semaphore 这些跨机器人交互读清楚。定位、地图、感知和视觉伺服的细节可以第二轮再看；它们对理解系统为什么能工作很重要，但不是第一轮重建 mission supervisor 与 excavation sub-FSM 的关键入口。

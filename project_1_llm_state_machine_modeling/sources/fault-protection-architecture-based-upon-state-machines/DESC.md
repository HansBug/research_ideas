# 航天器故障保护状态机 / Development of a Fault Protection Architecture Based Upon State Machines

## 论文在讲什么

这篇论文想解决的是航天器自主运行中的故障检测、隔离与恢复问题。作者不是从传统规则表或地面人工诊断出发，而是把故障保护架构写成 `Stateflow` 状态机块，让它接收硬件和软件状态量，再由状态机决定“现在是否有 fault、是什么类型的 fault、该触发什么 recovery action”。从整体视角看，它更像一篇把 `FDIR` 架构工程化落地到 `MATLAB/Simulink` 平台的论文。

不过它并不只是停留在“架构能这样做”的概念层。论文后半部分给了一个很具体的振动故障检测实例：先用加速度数据和 `KNN` 分类器生成 `FaultDetected` 标志，再把这个标志送入 Stateflow 图，利用 `Normal / PotentialFault / Fault` 与持续时间门槛去稳定判断故障，再把 `FaultStatus` 回传到飞行系统和遥测链路。这样一来，论文既有总体故障保护思想，也有可以直接抽样的单个状态机控制链。

## 控制系统在文中的位置

我们关注的控制系统描述在文中不是边角料，而是整篇工作的主承载体。作者把状态机作为 fault protection architecture 的核心表达方式，用它统一承接检测、隔离、恢复三个阶段。也就是说，这篇论文不是“先有别的主算法，再顺手画了个状态图”，而是明确主张用状态机来组织故障处理逻辑。

具体到样本提取层面，最值得抓的是振动故障检测 supervisor。它有清晰的输入标志、有嵌套子状态、有 `FaultPersistence / ResolutionPersistence` 这类工程级时间门槛，也有实际飞行试验中的置位与恢复过程。这比很多泛泛写 “fault management” 的航空论文更适合作为 `sources/` 文库的直接样本，因为它能形成一条完整、可追溯、可复现的故障保护状态链。

## 对我们为什么有用

这篇论文对 `sources/` 的意义，首先是补到了 `✈️` 方向里比较珍贵的“故障退化 / 恢复”类双 A 样本。仓库里飞行控制和任务模式样本不少，但真正把 fault detection 和 recovery 用离散状态链写清楚的论文并不算多；这篇正好提供了一个既能看出状态切换、又能看出工程 guard 的例子。

其次，它很适合后续做“异常处理型状态机”样本。很多控制论文只覆盖 nominal operation，而这篇明确讨论如何从 `PotentialFault` 升级到 `Fault`、如何用持续时间避免抖动、以及怎样从 `Fault` 回到 `Normal`。这类带恢复链、带防抖门槛的 supervisor，对后续做模型生成、性质提取或 defect repair 都更有区分度。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看摘要和前两页的 `FDIR` 背景，只确认论文的主张是“用状态机承接 fault protection architecture”。然后直接跳到 Stateflow 相关段落和 `Figure 12` 附近，把 `FaultDetected`、`Normal / Standby / PotentialFault / Fault`、`FaultPersistence`、`ResolutionPersistence`、`FaultStatus` 一次性圈出来，这是最核心的可提取链路。

后面再看飞行试验结果，尤其是 `FaultStatus` 在约 `10 s / 25 s / 35 s / 45 s` 左右的变化，用来验证状态机并不是纸上设计。至于加速度传感器、`KNN` 训练细节和机载硬件接线，可以放到第二轮再看；如果只是为了重构 `STM.md`，优先级远低于状态图本身和试验中的故障-恢复过程。

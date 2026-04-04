# 步行康复外骨骼的混合 FES-机器人协同控制 / Hybrid FES-Robot Cooperative Control of Ambulatory Gait Rehabilitation Exoskeleton

## 论文在讲什么
这篇论文解决的是混合外骨骼如何在步行中平衡机器人助力和电刺激肌肉驱动，并在肌肉疲劳时重新调整行为的问题。输入是 gait event、interaction torque、swing trajectory、刺激输出积分和 fatigue estimator，方法是把 `robotic joint controller`、`FES controller`、`muscle fatigue estimator` 和双层 `FSM` 组织成协同控制架构，输出是 stance / swing 阶段下的机器人刚度调节、FES 脉宽控制、学习与监测状态切换以及疲劳后的重学习。
从论文的展开方式看，输入侧主要落在 gait event、interaction torque、joint trajectory、`TTI`、stimulation pulse width 与 fatigue 指标，核心做法是 `t-FSM + c-FSM` 双层协调 + stance `PID` + swing `ILC` + `MFE` 疲劳检测，最终形成的则是 步态事件驱动的机器人刚度与 FES 协同分配、learning / monitoring 状态切换和安全回退。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是混合 `FES + robot` 步行康复外骨骼 `Kinesis` 的高层协同控制器。它负责在 stance / swing 中协调机器人和刺激肌群的贡献，并在疲劳出现时调整行为。
原文把控制器明确组织成双层状态机，例如 顶层 `t-FSM`：time-domain gait FSM，负责根据传感器检测 gait events，管理 stance / swing 相关状态、子层 `c-FSM`：cycle-domain FSM，在 swing 内部运行，每条腿各一个，包含 `learning` 与 `monitoring` 两个状态。 论文把控制分工和状态逻辑写得很完整，例如 `t-FSM` 从传感器中检测 gait events，并在腿进入 swing 时向对应腿的 `c-FSM` 广播 `new step event`、在 stance / double support，系统用 `PID` 控制 extensor muscles，以 interaction torque 为反馈避免 knee collapse、在 swing，相对于时间定义的参考轨迹，系统用 `ILC` 周期性更新刺激脉宽向量，以减小 interaction torque。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这是真实混合医疗辅助控制系统，不是 FES 综述或单纯人体动力学建模。 原文同时提供层次状态机、阶段性控制目标、学习条件、疲劳阈值和安全回退，适合直接提取为高质量自然语言状态机描述。 对“带学习期和监测期的 gait rehabilitation supervisor”这一类样本很有补样价值。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `t-FSM` 协调 `c-FSM` 的层次化写法、把 stance 和 swing 分别交给 `PID` 与 `ILC` 的控制职责分配方式、以 `TTI` 变化率和 `5% / 19%` 规则定义学习切换与疲劳管理的工程表达 这些最容易直接转成状态机自然语言描述的部分。 论文大量篇幅用于 FES 与疲劳估计的控制机理，阅读时需要和状态机主链拆开。 图中的部分状态名依赖图示理解，正文更偏解释控制职责而不是列出完整转移表。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

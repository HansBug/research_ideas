# MINDWALKER 外骨骼的设计与控制 / Design and Control of the MINDWALKER Exoskeleton

## 论文在讲什么
这篇论文解决的是截瘫辅助外骨骼如何在站立、重心转移、起步、连续步行和停步之间切换，并在横向扰动下在线调整步宽以维持稳定的问题。输入是 `CoM` 投影、IMU、关节角度、`XCoM` 偏差与 `START/STOP` 命令，方法是把高层 gait assistance 组织成九状态 `FSM`，再用 `CoM` 阈值和 `XCoM` deviation 驱动状态切换与步宽修正，输出是 active weight shift、step initiation / termination、在线 `HAA` 调整和阻抗跟踪控制。
从论文的展开方式看，输入侧主要落在 `CoM` 位置估计、IMU、关节角度、`XCoM` 偏差、`START/STOP` pushbutton，核心做法是 九状态 gait `FSM` + `CoM`-based HMI + `XCoM`-based step-width adaptation + variable impedance tracking，最终形成的则是 站立、左右 weight shift、半步起停、全步摆动、在线步宽调节和安全停步链。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是 `MINDWALKER` 下肢外骨骼的 gait assistance supervisor。它负责辅助穿戴者在双支撑、左右重心转移和步态摆动之间切换，并在扰动下在线修正步宽。
原文明确给出用于 assisted walking 的九状态 `FSM`。正文明确点名，例如 `S1`：stand、`S2`：assisted weight shift to left、`S6`：assisted weight shift to right。 论文把主链和 guard 写得很清楚，例如 `START/STOP` 可由按钮触发，但 step initiation 主要依赖 `CoM` 投影是否进入目标象限、在 standing 和 double stance 中，系统计算 sagittal 与 lateral 两个 weight-shift coefficient；当二者都低于阈值时，触发 `S2` 或 `S6` 的 assisted weight shift、从 weight-shift state 完成后，控制器自动推进到对应 swing state；按下 `STOP` 时，状态机会前往最近的 termination state，并通过 `S3` 或 `S7` 回到 `S1 stand`。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这是真实下肢外骨骼 gait assistance 控制器，不是单纯机械设计或步态分析论文。 原文直接保留了状态、触发 guard、起停链和在线步宽修正逻辑，适合直接提取为高质量自然语言状态机描述。 对“CoM trigger + online step-width adaptation”这一类平衡辅助控制样本很有补样价值。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `CoM` 双系数阈值触发下一状态的写法、`STOP -> nearest termination state -> half swing -> stand` 的工程化停步链、把在线稳定化逻辑嵌入 swing state 内部，而不是额外拆独立模式 这些最容易直接转成状态机自然语言描述的部分。 图中的部分状态名更依赖图示阅读，正文主要强调控制职责和触发条件。 论文重点是 gait assistance 主链和 lateral stability，对复杂故障模式覆盖不多。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

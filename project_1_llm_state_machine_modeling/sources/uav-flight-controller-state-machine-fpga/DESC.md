# 基于 FPGA 嵌入式系统的状态机式 UAV 飞控 / Design, Development and Implementation of a UAV flight controller based on a State Machine approach using a FPGA embedded system

## 论文在讲什么

这篇论文讨论的是一套 fixed-wing UAV flight controller 的设计与实现。作者的目标不是做复杂自主任务规划，而是面向一架固定翼无人机，基于 `FPGA` 构建一个并行嵌入式飞控系统，使其能够根据传感器输入在不同飞行模式间切换，并在异常发生时触发紧急保护。系统使用的输入包括 accelerometer、pitot、GPS、battery、RF-related alarms 等传感器与外部信号。

文章最值得关注的部分，是作者把飞控逻辑明确落成了 CPU state machine 和 emergency system。CPU 部分给出 `Takeoff-Free / Climb / Descent / Turn / Cruise / Emergency` 等状态及其输入输出对应关系；紧急系统则说明哪些异常条件会触发 alarm，alarm 如何让 CPU 跳到 `Emergency`，以及进入该状态后怎样执行电机关闭、舵面回中、等待稳定、开伞和关闭舵机的序列。

## 控制系统在文中的位置

我们关心的控制系统描述在这篇论文里是主角。虽然论文也谈 `FPGA` 并行性、模块划分和实现细节，但这些内容基本都在为飞控状态机服务。作者不是只把状态机当成一张解释图，而是真正给出了状态表、状态切换输入和状态输出，是非常典型的“工程实现型控制器说明”。

尤其值得注意的是 emergency branch。很多 UAV 论文会提到 fail-safe 或 safe landing，但真正把触发条件、判定延迟和执行动作列出来的并不多。这篇把 `three seconds timer`、alarm flag、`Emergency` 状态和 parachute sequence 连成了一条完整控制链，因此它不是只补一个普通飞行模式表，而是补到了一条明确的异常恢复样本。

## 对我们为什么有用

这篇论文对 `sources/` 的价值主要体现在两个方面。第一，它补的是航空航天方向里偏底层 flight-mode supervision 的样本，而不是 mission management、编队控制或高层任务自治。文库里已有若干 `UAV mission` 和 `formation manager` 条目，但这篇更接近“飞行模式与 fail-safe 控制”的实现层，能拉开航空方向样本的内部差异。

第二，它保住了输入到状态、状态到输出、异常到恢复的完整映射。`rst/sw1/sw2/ELE/AIL/se` 这些输入、各状态的补偿策略，以及 emergency system 的确认延迟与动作序列，都有助于后续做从自然语言到状态机的结构化建模。对于用户要求的 `FSM + T1 + 至少 1 个双 A STM` 来说，这篇是比较稳的工程飞控正例。

## 如果需要人工细读，建议怎么读

如果后续需要人工重做 `STM.md`，建议先看第 1 页摘要确认系统边界，再直接跳到第 3 页 `Table 1` 所在部分，把状态编号 `00-11`、输入条件和输出动作先整理成一张控制表。随后立刻接着读 `Emergency System` 段和第 6 页的 `Emergency System Simulation`，把“五类异常 -> `3 seconds` 确认 -> alarm -> Emergency -> 开伞序列”这条链补齐。

硬件选型、PWM 实现细节、传感器对比测试和 FPGA 资源占用可以放到第二轮再看。第一轮抽样时最重要的是先把 CPU 状态机和 emergency chain 读透，因为这两块已经足以支撑一个完整的飞控监督样本；剩下的实现细节更适合作为后续补证材料，而不是第一轮状态机抽取的主入口。

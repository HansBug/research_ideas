# 自动腹膜透析机的状态机设计 / State Machine Design for an Automated Peritoneal Dialysis Machine

## 论文在讲什么
这篇论文解决的是自动腹膜透析机如何在准备液体、注液、驻留、排液、冲洗和异常告警之间进行安全切换，并根据浊度尽早终止透析的问题。输入是模式选择、温度、流量、液位、压力、浊度、危险值和故障信号，方法是把整个 APD 流程编码成 5-bit 有限状态机和对应 I/O/转移表，输出是 `standby -> instruction -> heating -> filling -> dwelling -> draining -> loop/flush -> error` 的完整设备控制链。
从论文的展开方式看，输入侧主要落在 `S`, `DM`, `FM`, `AI`, `P`, `T`, `SD`, `F1-F4`, `L`, `PR`, `TU`, `DV`, `F`，核心做法是 FSM-based APD process design + LabVIEW interface + turbidity-triggered early termination，最终形成的则是 准备液体、注液、驻留计时、排液、循环判断、冲洗结束和 `11111` 错误告警的完整过程控制逻辑。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是自动腹膜透析机的过程控制器。它负责在不同模式和传感器条件下调度加热、注液、驻留、排液、冲洗和异常停机，并通过浊度与计时逻辑优化 session 长度。
原文把该控制器明确写成 `finite state machine`，并给出 5-bit 状态编码。关键状态包括 `S0` standby、`S1` written instructions、`S2` audible instructions。 论文把 APD 主流程和异常处理写得较清晰，例如 用户完成安全问答后进入透析模式，系统先执行 `Preparing the Solution` 与温度控制、进入 filling stage 后，持续监控液位、流量与压力；随后进入 dwelling phase，并显式启动 dwell timer、排液阶段结合 turbidity sensor 判断浊度，若液体已足够清澈则提前结束 session，否则继续 loop 或后续流程。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这篇论文给的是真实医疗设备过程控制器，不是单纯界面设计或综述。 原文保留了状态图、I/O 表、状态编码、浊度终止与错误态说明，适合直接提取成高质量自然语言状态机描述。 对“设备过程控制 + 计时 + 传感器驱动提前终止 + error state”这一类样本非常有价值。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 5-bit 状态编码与 I/O/transition table 并列呈现的方式、dwell timer 和 turbidity-triggered termination 的控制逻辑、`11111` 统一错误态与 watchdog/报警处理口径 这些最容易直接转成状态机自然语言描述的部分。 论文包含较多背景介绍与界面设计，需要聚焦第 4 节 FSM 主体。 部分状态采用编码名而非自然语言状态名，整理时需补足语义映射。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

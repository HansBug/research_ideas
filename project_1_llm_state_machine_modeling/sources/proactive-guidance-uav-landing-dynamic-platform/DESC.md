# 面向动态平台精确降落的 UAV 主动引导方法 / Proactive Guidance for Accurate UAV Landing on a Dynamic Platform: A Visual–Inertial Approach

## 论文在讲什么

这篇论文解决的是小型四旋翼如何在移动地面/海上平台上安全、平滑地完成自主降落的问题。输入是 GPS、视觉定位、IMU/Kalman filter 状态估计、平台相对位置误差和高度信息，方法是用一个四阶段有限状态机调度 GPS 跟随、视觉位置跟随、无地效接近轨迹和最后关机，输出是 `GPS following -> vision position following -> ground-effect free trajectory -> shutdown` 的完整降落监督控制链。
从论文的展开方式看，输入侧主要落在 GPS 跟随位置、视觉定位结果、`KF` 融合状态、相对位置误差、平台可见性、剩余高度，核心做法是 视觉-惯导定位 + optimized trajectory planner + four-stage landing FSM，最终形成的则是 动态平台入视野、视觉接管、无地效滑翔接近、触地前电机关断的完整 landing supervisor。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置

这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是四旋翼 UAV 的高层 landing supervisor。它负责判断何时由 GPS 跟随切换到视觉接管、何时进入接近轨迹、何时因失视或越界回退，以及何时在接近平台后关闭电机。
原文把该控制器明确写成 `finite state machine`，包含四个阶段，例如 `GPS following`、`Vision position following`、`Ground-effect free trajectory following`。 论文写清了降落主链和回退逻辑，例如 `GPS following` 先把 UAV 带到平台视场附近、一旦定位估计收敛，转入 `Vision position following`，利用视觉与融合定位维持相对位置、当 UAV 进入以 `(1.1 m behind, 0.7 m above)` 为中心、半径 `0.1 m` 的期望域时，转入 `Ground-effect free trajectory following`。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用

对 `sources/` 来说，这篇论文给的是真实 UAV 降落监督控制器，不是单纯视觉检测或路径优化论文。 原文同时保留了 FSM 阶段、切换条件、空间 guard 和 failsafe 回退逻辑，适合直接提取成高质量自然语言状态机描述。 对“移动平台回收、视觉接管、接近轨迹和 shutdown chain”这一类空地协同控制样本很有补样价值。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `GPS -> vision -> approach -> shutdown` 的分阶段接管模板、以空间位置域和高度条件定义状态切换的 guard 写法、在 approach 阶段设置越界即回退的安全控制口径 这些最容易直接转成状态机自然语言描述的部分。 论文中的低层位置估计与轨迹规划篇幅较多，需要与高层 FSM 主链分开整理。 时间语义主要体现在顺序阶段和空间条件，而非显式 timer。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

## 如果需要人工细读，建议怎么读

如果后续是为了人工复核 `STM.md`、重做案例抽取，或确认这篇论文能否稳定进入数据集，建议先看 第 1 页起的摘要与引言，只用来确认系统边界、控制对象和本文到底是在讲系统设计还是在讲方法。随后直接跳到 第 7 页起的“2.3. Finite State Machine”部分，优先人工标出状态/模式名、状态进入与退出条件、事件或 guard、局部时间量、状态内动作，以及 nominal / abnormal / hold / retreat 这类分支；最后再用 第 10 页起的“4.1. Indoor Experiment Results”部分 去核对这些状态在完整系统或实验场景里是怎样串起来的，借此区分“主控制链”与“只为实现服务的细节”。
像 第 7 页起的“3. Ground-effect free trajectory following;”部分 这类更偏低层模型、连续控制律、感知/估计、硬件实现或数学推导的内容，通常可以放到第二轮再看；除非你是在追某个阈值、guard 或时间条件到底从哪一节推出来。换句话说，这一节的目的不是复读 `STM.md`，而是在 `STM.md` 不再可靠甚至需要重做时，仍然给人工一条稳定的原文阅读顺序：先锁定系统边界，再锁定状态骨架和转移条件，最后才回头补低层推导与性能细节。

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

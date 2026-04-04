# 小型 USV 上四旋翼 UAV 自主降落的视觉引导与控制方法 / A Visual Guidance and Control Method for Autonomous Landing of a Quadrotor UAV on a Small USV

## 论文在讲什么
这篇论文解决的是四旋翼 UAV 如何在小型 USV 上完成自主接近、视觉接管与最终降落，并在目标丢失时安全悬停的问题。输入是 GNSS、视觉 marker 检测、相对位姿误差、yaw 偏差和 marker 可见性，方法是用三阶段 `FSM` 组织 `Idle -> Approaching -> Landing`，再在 Landing 内引入 event-triggered yaw control、bounding box guard 和 marker-loss failsafe，输出是完整的海上回收监督控制链。
从论文的展开方式看，输入侧主要落在 landing command、GNSS 位置、ArUco marker 检测、相对位姿误差、yaw 偏差、marker visibility，核心做法是 trajectory generation + three-stage `FSM` + event-triggered yaw/position `PID` control + `Hold` failsafe，最终形成的则是 `hover waiting -> optimized approach -> visual landing -> motor shutdown / hold recovery` 的完整降落控制流程。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是四旋翼 `UAV` 在小型 `USV` 上回收任务的高层 landing supervisor。它负责接收降落命令、管理接近轨迹、在视觉锁定后切换到 landing，并在 marker 丢失时切到安全悬停。
原文明确把飞行过程写成三阶段 `FSM`，例如 `Idle`、`Approaching`、`Landing`。 论文的高层控制链很清楚，例如 `Idle` 下，`UAV` 悬停等待地面站命令；收到 landing command 后进入 `Approaching`、`Approaching` 下，系统根据给定 waypoints 生成优化轨迹并执行跟踪；前视相机检测到着陆平台 marker 后自动切到 `Landing`、`Landing` 下，系统使用视觉引导接近平台，并在进入虚拟 bounding box 后才允许更积极的 yaw 调整，以避免平移和转向互相干扰。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这是真实 UAV-USV 回收控制器，不是单纯视觉检测或轨迹优化论文。 原文同时保留了阶段状态、进入条件、空间 guard、event-triggered control 和 recovery chain，适合直接提取为高质量自然语言状态机描述。 对“vision takeover + landing supervisor + marker-loss recovery”这一类空海协同控制样本很有补样价值。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `Idle -> Approaching -> Landing` 的分阶段 supervisor 模板、用空间 bounding box 决定何时放开 yaw 调整的 guard 写法、`marker lost for 0.3 s -> Hold -> re-detect -> Offboard` 的短时失视恢复链 这些最容易直接转成状态机自然语言描述的部分。 论文大量篇幅用于 trajectory planning 和视觉定位算法，需要与高层 `FSM` 主链拆开整理。 顶层状态数较少，但每个阶段内部的空间约束和模式回退比较关键。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

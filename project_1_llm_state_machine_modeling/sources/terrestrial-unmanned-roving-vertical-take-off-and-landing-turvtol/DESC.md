# 陆空两栖垂直起降自主载具 TURVTOL / Terrestrial Unmanned Roving Vertical Take-off and Landing (TURVTOL)

## 论文在讲什么
这篇论文解决的是一个既能地面行驶又能短时飞跃障碍的自主载具如何在无 GPS 条件下完成 driving/flying/landing/charging 任务切换的问题。输入是 path planner、battery、terrain safety、VIO、destination、slip/stuck/flip 信号，方法是设计一个 `SMACH` 层次状态机来调度 drive/fly/landing/traction-loss/dormant 多层子状态机，输出是多模态任务执行和异常恢复控制链。
从论文的展开方式看，输入侧主要落在 path planner result、battery level、safe takeoff/landing flag、destination、slip/stuck/flipped indicators，核心做法是 基于 `ROS/SMACH` 的 hierarchical FSM，联动 path planner、control loop、localization 与 terrain assessment，最终形成的则是 `drive / takeoff / hover / search_for_landing / return_to_launch / charging / sleeping` 多模态任务控制链。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是 `TURVTOL` 多模态自主载具的软件监督器。它负责决定车辆何时保持地面驱动、何时切换飞行、何时寻找安全着陆点、何时返航以及何时进入充电或休眠。
原文把高层控制明确写成 `hierarchical state machine`。顶层含，例如 `FLY_OPERATE`、`DRIVE_OPERATE`、`LANDING` 子状态机。 论文给出的控制链包含几个关键事实，例如 正常行驶时在 `NORM_DRIVE`，若 terrain 或风况使起飞不安全，就切到 `DRIVE_NO_FLY`、需要飞越障碍时进入 `TAKEOFF -> FLY -> HOVER` 等飞行操作链、需要着陆时，若周围能找到安全落点，则走 `SEARCH_FOR_LANDING -> LAND`；若找不到则进入 `RETURN_TO_LAUNCH`。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这篇论文给的是真实自主平台的任务监督逻辑，而不是抽象多机器人方法论文。 原文已经明确写出层次状态组织、低层状态表和 transition signals，适合直接转成高质量自然语言状态机样本。 对“多模态平台在地面-飞行之间切换”的建模尤其有价值，能补充当前 `sources` 中较少的 drive/fly mixed mission 样本。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 drive/fly 两大主模式加 landing/traction-loss/dormant 子状态机的层次化组织、`safe_takeoff / safe_landing / return_to_safe / low_battery / stuck / slipping` 这类 transition signals 写法、`NORM_DRIVE -> DRIVE_NO_FLY` 这种由环境安全条件触发的模式约束逻辑 这些最容易直接转成状态机自然语言描述的部分。 论文是 design paper，部分低层 state method 仍处在持续集成阶段。 许多算法实现细节落在路径规划和定位模块，不能全部当成 FSM 事实直接吸收。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

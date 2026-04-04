# 面向垃圾分拣移动机器人的状态机驱动位置/力混合控制架构 / State Machine-Based Hybrid Position/Force Control Architecture for a Waste Management Mobile Robot with 5DOF Manipulator

## 论文在讲什么
这篇论文解决的是垃圾分拣移动机器人上的 5DOF 机械臂如何在同一任务中切换位置控制与力控制来完成抓取和投放的问题。输入是目标类型、目标位姿、目标抓取力、位置误差和力误差，方法是把经典 hybrid position/force control 外包一层分层状态机 `SmHPFC`，输出是 `Main/Homing -> Position Control -> Force Control -> Drop -> New Task` 的完整 pick-and-drop 监督控制链。
从论文的展开方式看，输入侧主要落在 object type、target coordinates、gripper rotation、reference force、position error、force error、emergency stop，核心做法是 基于 `state machine + S-matrix` 的混合位置/力控制切换架构，包含 homing、position control、force control 三组子状态机，最终形成的则是 目标定位、对准、抓取、抬升、移送到回收托盘、开爪投放与异常停止控制链。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是垃圾分拣移动机器人上的 5DOF 机械臂控制器。它负责决定系统何时执行 homing、何时采用位置控制对准目标、何时切换到力控制闭合夹爪，以及何时恢复位置控制并把物体投放到回收托盘。
原文把该控制器明确写成 `state machine-based hybrid position/force control architecture (SmHPFC)`。主结构包含，例如 `Si1 Main`、`Si2 Main/Homing`、`Si3 All`。 论文给出的任务链很完整，例如 系统上电后先依次对五个 DOF 执行 `Homing`，完成后进入稳定态 `Si3`、收到新任务后，先在 `SC1` 用位置控制完成 `XOY` 平面定位与夹爪朝向对准、随后转入 `SC2/SC3`，继续完成 `OZ` 方向定位并把 gripper 控制从 position 切到 force，通过更新 `S-matrix` 执行抓取。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这篇论文给的是真实机器人执行机构监督控制器，不是泛泛的控制理论论文。 原文同时保留了状态名、状态层次、状态含义、抓取力/位置误差和控制模式切换逻辑，特别适合提取成带 guard 的自然语言状态机样本。 对“任务链驱动的 position-control / force-control 切换”这一类复杂执行器控制尤其有价值。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 主状态机 + 子状态机的层次建模方式、`定位 -> 纵向对准 -> 力控抓取 -> 抬升移送 -> 开爪投放` 的典型抓取链、`S-matrix` 更新触发控制模式切换的写法 这些最容易直接转成状态机自然语言描述的部分。 论文较强调控制架构本身，低层环境感知与目标检测细节不是主体。 时间语义主要体现为顺序阶段与稳定条件，不是显式 timer 约束。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

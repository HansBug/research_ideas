# 面向监视应用的自主无人机动态目标跟踪系统 / Dynamic Object Tracking on Autonomous UAV System for Surveillance Applications

## 论文在讲什么
这篇论文解决的是无人机在监视任务中如何根据目标相对位置执行搜索、悬停、横摆、升降、前后跟随以及失目标后的安全降落的问题。输入是 RGB 图像、深度、相对目标运动趋势、安全距离与失目标帧数，方法是设计两个并行状态机来分别处理 camera FoV 姿态/高度和 UAV 与目标的相对距离，输出是离散 waypoint/maneuver 序列。
从论文的展开方式看，输入侧主要落在 camera image、depth estimate、relative target motion、`Rsafe / Rsur`、lost-target duration，核心做法是 目标检测与跟踪之上的 parallel finite-state maneuver controller，最终形成的则是 `search / hover / sway / climb / descend / forward / backward / lost-and-await / land` 控制链。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是一个自主 surveillance UAV 系统。控制器根据目标在相机坐标系中的相对位置与动态趋势，决定无人机该搜索、悬停、横摆、升降、前后调整，还是进入失目标等待与降落模式。
原文明确说明系统有两个并行状态机，例如 一个处理 camera FoV 的姿态与高度、一个处理 UAV 与目标之间的相对距离、`Initialization`。 论文把主链写得很完整，例如 初始化后无人机起飞到固定高度，再进入 `Sway and Search` 做 360 度搜索、锁定目标后进入 `Track and Hover`，先判断目标是否静止、如果目标在画面中横向移动，则进入 `Track and Sway`；如果目标高低变化，则进入 `Track and Climb or Descend`。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这篇论文是真实 UAV 监视任务的高层 maneuver controller，不是只做感知性能比较。 论文已经把 parallel FSM、relative-position guards 和 lost-target fail-safe 讲清楚，适合直接转写为自然语言状态机样本。 该类“目标跟踪监督器”在当前文库里仍不多，能补充视觉驱动任务控制案例。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 “两个并行状态机分别处理姿态/高度与相对距离”的结构表达、`Rsafe / Rsur` 约束、`Vqmax / Vzmax / Vxmax` 动态约束与离散 maneuver 状态的结合方式、`Lost and Await -> Land` 的 fail-safe 任务回退链 这些最容易直接转成状态机自然语言描述的部分。 论文仍包含较多视觉检测、Kalman 预测和感知评估内容，需要和高层状态机事实分开看。 一部分 transition 条件通过相对运动趋势和帧级判断给出，没有像 PLC 论文那样给出更低层的离散 I/O 表。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

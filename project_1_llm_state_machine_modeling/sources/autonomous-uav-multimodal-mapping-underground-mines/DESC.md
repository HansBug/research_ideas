# 面向地下矿井多模态测绘的自主无人机 / Development of an Autonomous UAV for Multi-Modal Mapping of Underground Mines

## 论文在讲什么
这篇论文解决的是无人机如何在 GNSS 缺失、低光和狭窄地下矿井中切换手动记录、反应式探索与自主支柱扫描三种任务模式的问题。输入是 RC 指令、LiDAR 空旷方向、天花板距离、支柱角点和目标支柱位置，方法是用一个包含三个 mission block 的层次状态机来调度起飞、找自由空间、扫掠支柱和落地流程，输出是 `manual data collection / reactive exploration / supervised autonomous pillar inspection` 的统一任务监督控制链。
从论文的展开方式看，输入侧主要落在 manual RC commands、LiDAR free-space vectors、ceiling distance、pillar corners、mission profile、payload selection，核心做法是 自定义 `ROS 2` 包中的 core FSM，按 mission block 切换手动记录、反应式探索与 back-and-forth pillar inspection，最终形成的则是 独立数据记录、起飞到安全高度后的 corridor exploration、沿支柱表面的往返扫描与落地流程。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是地下矿井测绘无人机上的任务监督控制器。它负责决定无人机何时仅做手动遥控与数据记录、何时进入自主 corridor exploration，以及何时切换到受监督的 pillar inspection 扫描任务。
原文把控制软件明确写成一个 `core finite-state machine`，并给出三种 mission mode，例如 `Mission 1`：manual flight / data logging、`Mission 2`：reactive exploration、`Mission 3`：supervised autonomous inspection。 论文给出的任务控制链包括 初始 `Wait` 状态既可以进入独立的 `PayloadRecord` 数据记录模式，也可以根据用户选择切换到三类 mission 中的一类、`reactive exploration` 模式下，无人机先起飞到安全高度，再寻找最大空旷方向、调整姿态并沿 `V_cmd` 前进，直到到达结束条件或收到落地命令、`supervised autonomous pillar inspection` 模式下，系统先调节与支柱和天花板的相对距离，再通过 corner detection 与 parallel position adjustment 维持扫描几何关系。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这篇论文给的是真实地下矿井 UAV 任务监督器，不是单纯 SLAM 或点云重建论文。 原文已经把三类 mission、起飞/探索/扫描子阶段以及落地入口明确组织成 state machine，适合直接转写成自然语言状态机样本。 对“同一平台上多 mission profile 切换”的层次监督控制很有参考价值。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `manual / exploration / inspection` 三 mission 模式共存的顶层组织、`Take off -> Reach altitude -> Free Space -> Move Robot` 的轻量探索控制链、pillar inspection 中 `Adjust altitude / Adjust parallel pos / Corner Detection / Move robot` 的扫描监督逻辑 这些最容易直接转成状态机自然语言描述的部分。 论文的大量篇幅仍然用于多模态点云重建与传感器方案，不应把这些内容误当作状态机主链。 时间语义主要是阶段顺序和任务完成条件，不是显式计时约束。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

# 小型无人机自主搜索与跟踪一体化系统 / An Integrated System for Autonomous Search and Track with a Small Unmanned Aerial Vehicle

## 论文在讲什么

这篇论文解决的是小型无人机如何在无人值守条件下完成起飞、搜索、确认目标并持续跟踪的问题。输入是通信链路、剩余电量、人体检测器、面部检测器和 tracker 置信度，方法是用 `SMACH` 组织一个带并发监控的层次状态机，输出是 `TAKEOFF -> SEARCH -> INVESTIGATE -> TRACK` 的完整任务控制链。
从论文的展开方式看，输入侧主要落在 battery level、communication status、human detector、face detector、tracker confidence，核心做法是 基于 `ROS/SMACH` 的层次并发状态机，加上 `CMT` 跟踪器与 `IBVS` 视觉伺服控制，最终形成的则是 自主起飞、搜索、确认、跟踪、失跟回搜和低电量/失联受控降落控制链。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置

这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是 `Parrot AR.Drone` 小型无人机上的 search-and-track autonomy controller。它负责在 mission 中决定何时起飞、何时执行自旋或航点搜索、何时切入目标确认，以及何时进入持续跟踪或中止任务。
原文把高层控制明确写成 `Hierarchical Finite State Machine`，并使用 `SMACH` 承载。主链包括 `MONITOR`、`TAKEOFF`、`SEARCH`。 论文把主控制链写得很清楚，例如 `MONITOR` 持续运行，只要通信异常或电池低于安全阈值就触发 mission abort 和 controlled land、系统确认可以继续后进入 `TAKEOFF`，随后立刻切入 `SEARCH`、`SEARCH` 中只要人体检测器命中目标，就进入 `INVESTIGATE` 悬停确认。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用

对 `sources/` 来说，这篇论文给的是真实无人机任务监督器，不是单纯视觉算法论文。 状态机中的输入、守卫、状态动作和回退链都可直接转写成自然语言状态机描述样本。 `MONITOR` 并发安全链对后续研究异常恢复和 fail-safe 建模也很有价值。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `MONITOR` 并发安全子状态机与主任务状态机并行运行的表达、`SEARCH -> INVESTIGATE -> TRACK` 这种“先发现、再确认、再持续跟踪”的监督控制模板、tracker confidence 下降后回退 `SEARCH` 的回环式任务控制链 这些最容易直接转成状态机自然语言描述的部分。 论文重点仍有一部分落在视觉跟踪与 `IBVS` 控制实现，低层连续控制细节较多。 `SEARCH` 的低层路径规划只给出 `SPIN SEARCH` 与 `WAY POINT search` 的任务意图，没有展开更细航迹优化算法。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

## 如果需要人工细读，建议怎么读

如果后续是为了人工复核 `STM.md`、重做案例抽取，或确认这篇论文能否稳定进入数据集，建议先看 第 1 页起的摘要与引言，只用来确认系统边界、控制对象和本文到底是在讲系统设计还是在讲方法。随后直接跳到 第 2 页起的“A. Architecture for Search Identify and Track”部分，优先人工标出状态/模式名、状态进入与退出条件、事件或 guard、局部时间量、状态内动作，以及 nominal / abnormal / hold / retreat 这类分支；最后再用 第 6 页起的“A. Simulation Results”部分 去核对这些状态在完整系统或实验场景里是怎样串起来的，借此区分“主控制链”与“只为实现服务的细节”。
如果文中没有一个特别独立的“理论推导”章节，也仍然建议把所有不直接给出状态图、模式枚举、transition table、I/O/parameter 映射或实验触发顺序的部分放到第二轮再看。换句话说，这一节的目的不是复读 `STM.md`，而是在 `STM.md` 不再可靠甚至需要重做时，仍然给人工一条稳定的原文阅读顺序：先锁定系统边界，再锁定状态骨架和转移条件，最后才回头补低层实现与性能细节。

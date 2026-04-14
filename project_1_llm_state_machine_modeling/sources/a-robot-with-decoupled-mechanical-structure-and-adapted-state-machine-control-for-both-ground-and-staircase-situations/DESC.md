# 面向地面与楼梯场景的解耦机械结构机器人及其状态机控制 / A Robot with Decoupled Mechanical Structure and Adapted State Machine Control for Both Ground and Staircase Situations

## 论文在讲什么

这篇论文解决的是一个送货机器人如何在地面行驶和上下楼梯之间切换，并在楼梯场景中维持姿态、触发不同 climbing cases的问题。输入是 Mecanum wheel 编码器、EH 编码器和激光测距传感器，方法是构造一个带 `SC1-SC7` 触发条件的 stair-climbing state machine，输出是 `ground mode -> posture adjustment -> climb -> return to ground mode` 的完整顺序控制链。
从论文的展开方式看，输入侧主要落在 wheel encoder、EH encoder、laser ranging sensor distance、step-edge distance，核心做法是 基于 sensor-triggered switch conditions 的楼梯机器人状态机，最终形成的则是 地面模式、姿态调整、上楼案例切换、下楼状态流和回到 ground mode 的控制逻辑。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置

这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是一个用于 last-mile delivery 的 stair-climbing robot。控制器需要根据台阶距离和机器人姿态，在地面行驶、姿态调整和不同 stair-climbing case 之间切换。
原文的 state machine 由 `ground mode` 与多个 climbing / posture-adjustment cases 组成，并通过 `SC1-SC7` 条件触发切换。其核心状态和动作包括 `ground mode`、`Case 1`、`Case 2`。 论文把 stair-climbing 主链写得很明确，例如 系统启动后默认在 `ground mode`，只有检测到台阶且满足 `SC2` 才离开地面模式、`SC2` 触发 `Case 1` 姿态调整，使前轮靠近楼梯并让 tetrapod 落地、`SC7` 触发 `Case III`，正式开始上楼。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用

对 `sources/` 来说，这篇论文是真实机器人移动控制案例，不是抽象步态方法综述。 原文明确给出 state machine、sensor triggers 和动作切换，非常适合转写成自然语言状态机样本。 它补充了当前文库中较少的“台阶/姿态调整/多阶段 climbing”类离散控制样本。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `SC1-SC7` 这类显式传感器守卫条件写法、`ground mode -> posture adjustment -> climbing -> ground mode` 的顺序监督链、通过 front-wheel 和 wheel-leg distance 区分不同 climbing cases 的 guard 设计 这些最容易直接转成状态机自然语言描述的部分。 论文主要展开 moving upstairs，对 moving downstairs 只说明可类似建立，不如上楼链详细。 低层运动学和机械结构解释较多，需要筛掉与状态机建模无关的连续几何推导。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

## 如果需要人工细读，建议怎么读

如果后续是为了人工复核 `STM.md`、重做案例抽取，或确认这篇论文能否稳定进入数据集，建议先看 第 1 页起的摘要与引言，只用来确认系统边界、控制对象和本文到底是在讲系统设计还是在讲方法。随后直接跳到 第 8 页起的“4. State Machine for the Robot”部分，优先人工标出状态/模式名、状态进入与退出条件、事件或 guard、局部时间量、状态内动作，以及 nominal / abnormal / hold / retreat 这类分支；最后再用 第 11 页起的“5. Prototype and Experimental Results”部分 去核对这些状态在完整系统或实验场景里是怎样串起来的，借此区分“主控制链”与“只为实现服务的细节”。
如果文中没有一个特别独立的“理论推导”章节，也仍然建议把所有不直接给出状态图、模式枚举、transition table、I/O/parameter 映射或实验触发顺序的部分放到第二轮再看。换句话说，这一节的目的不是复读 `STM.md`，而是在 `STM.md` 不再可靠甚至需要重做时，仍然给人工一条稳定的原文阅读顺序：先锁定系统边界，再锁定状态骨架和转移条件，最后才回头补低层实现与性能细节。

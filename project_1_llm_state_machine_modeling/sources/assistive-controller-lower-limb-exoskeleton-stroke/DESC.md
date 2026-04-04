# 面向卒中康复下肢外骨骼的辅助控制器 / An Assistive Controller for a Lower-Limb Exoskeleton for Rehabilitation after Stroke, and Preliminary Assessment Thereof

## 论文在讲什么

这篇论文解决的是卒中后偏瘫患者在穿戴下肢外骨骼时，如何在不过度规定步态轨迹的前提下获得 stance 稳定和 swing 辅助的问题。输入是脚跟着地、腿部角速度、患侧/健侧 swing 与 stance 状态以及进入子状态后的局部时间，方法是用三大 gait state 加每态两个子状态的层次状态机来切换重力补偿、swing torque pulse 和 stance soft stop，输出是 `affected swing -> double support -> unaffected swing` 的完整辅助步态闭环。
从论文的展开方式看，输入侧主要落在 heel strike、thigh angular velocity、affected/unaffected knee angular velocity、各子状态进入后的时间 `t_a/t_b`、步态相位信息，核心做法是 三态双子态有限状态机 + gravity compensation + feedforward torque pulse + stance soft stop，最终形成的则是 患侧摆动、双支撑、健侧摆动的 gait assistance 切换，以及 swing/stance 子阶段的差异化关节辅助力矩。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置

这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是卒中康复下肢外骨骼的 gait assistance controller。它负责判断当前处于患侧摆动、双支撑还是健侧摆动，以及在各阶段中何时施加 swing assist torque、何时提供 stance soft stop。
原文把该控制器明确写成 `finite state machine`，包含三个主状态，每个主状态再细分为两个子状态，例如 `State 1`：affected-limb swing、`State 2`：double support、`State 3`：unaffected-limb swing。 论文把 gait assistance 主链写得很清楚，例如 状态机在 `affected swing -> double support -> unaffected swing` 之间按正常步态循环、`1a/1b` 与 `3a/3b` 的切换由相应 swing leg 的 knee angular velocity 符号变化驱动、从单支撑到双支撑的切换由相应 swing leg 的 heel strike 触发。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用

对 `sources/` 来说，这篇论文给的是真实康复外骨骼 gait controller，不是纯临床评估论文。 原文既保留了状态结构，也写清了切换事件和状态内的控制动作，适合提取成高质量状态机自然语言描述。 对“连续 gait phase 中的离散监督切换 + 状态内局部定时动作”这一类样本特别有价值。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 “三个 gait state + 每态两个 sub-state”的层次建模方式、用 heel strike、角速度符号变化和 thigh angular velocity 阈值构成 guard、在 swing 子状态内用局部时间驱动 torque pulse 的写法 这些最容易直接转成状态机自然语言描述的部分。 论文重点是康复辅助策略，故障恢复和异常模式链不丰富。 低层 torque equation 比较多，若只关心高层状态链需要适度压缩。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。

## 如果需要人工细读，建议怎么读

如果后续是为了人工复核 `STM.md`、重做案例抽取，或确认这篇论文能否稳定进入数据集，建议先看 第 1 页起的摘要与引言，只用来确认系统边界、控制对象和本文到底是在讲系统设计还是在讲方法。随后直接跳到 第 5 页起的“F. Structure of the State Machine”部分，优先人工标出状态/模式名、状态进入与退出条件、事件或 guard、局部时间量、状态内动作，以及 nominal / abnormal / hold / retreat 这类分支；最后再用 第 6 页起的“III. Experimental Implementation and Assessment”部分 去核对这些状态在完整系统或实验场景里是怎样串起来的，借此区分“主控制链”与“只为实现服务的细节”。
如果文中没有一个特别独立的“理论推导”章节，也仍然建议把所有不直接给出状态图、模式枚举、transition table、I/O/parameter 映射或实验触发顺序的部分放到第二轮再看。换句话说，这一节的目的不是复读 `STM.md`，而是在 `STM.md` 不再可靠甚至需要重做时，仍然给人工一条稳定的原文阅读顺序：先锁定系统边界，再锁定状态骨架和转移条件，最后才回头补低层实现与性能细节。

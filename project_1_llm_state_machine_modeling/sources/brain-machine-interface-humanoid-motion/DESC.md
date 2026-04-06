# 脑机接口驱动的人形机器人全身运动控制 / Brain-machine interfacing control of whole-body humanoid motion

## 论文在讲什么

这篇论文研究的是一个 humanoid whole-body motion 控制框架，目标是在多接触动作执行过程中，把离线接触规划、在线低层控制和脑机接口输入真正耦合起来。作者先离线规划从初始姿态到目标姿态的 contact transition sequence，再由在线 controller 逐步跟踪这些 transition posture，同时保持平衡、避免自碰撞并满足物理约束。

论文真正新颖的地方不只是“用了 EEG”，而是把脑机接口放在一个已经能自动完成大部分动作的层次控制器里。用户并不逐关节控制机器人，而是在关键的 contact-adding step 中通过脑机指令去修正中间 way-point，帮助机器人摆脱 local minimum，从而继续完成楼梯攀爬这类全身动作。

## 控制系统在文中的位置

我们关心的控制系统描述是本文的核心部分之一。Section 3 明确把 low-level controller 写成一个有限状态机：去接触时进入 `Shift CoM`，加接触时进入 `Move contact link`。这已经不是“有状态概念”的泛泛说法，而是明确点出了状态与各状态中的控制目标分配。

更重要的是，论文没有停在平面 FSM。Section 5 继续把 `Move contact link` 细化成 `Move contact link to way-point` 和 `Move contact link to goal` 两个子状态，并说明脑机指令具体修改什么量、为什么要这么改、它解决的是哪类失败模式。因此它在文中承担的是一个真实控制子系统的职责，而不是实验演示流程或脑信号分类附属说明。

## 对我们为什么有用

这篇论文对 `sources/` 的价值，在于补到了一类此前不算多见的 humanoid contact-transition HSM 样本。很多人形机器人论文主体放在动力学优化、轨迹跟踪或感知上，即使出现 mode/state 词，也未必会把主控制链交代清楚；这篇则把接触移除、接触添加、way-point 子状态和人工修正都写得很直接。

它也提供了一个很好的“人机共享低层控制”表达模板。自动控制负责 nominal path，脑机接口只在局部失败点施加修正，这与完全手动 teleoperation 或完全 autonomous motion 都不同。后续如果要训练模型理解“自动规划 + 局部人工纠偏”的状态机叙事，这篇会很有代表性。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `3` 节附近对应的正文页，把 low-level controller 的顶层状态骨架先锁定下来，重点抓 `Shift CoM`、`Move contact link`、removing/addition-contact transition 的动作语义。随后直接跳到 `Component Integration` 段落和相关图页，把 `Move contact link` 的两个子状态、way-point 触发条件和 brain command 影响的变量读清楚。

之后再看实验部分，尤其是楼梯场景、Figure `6-9` 附近对 eight commands、manual trigger、local-minimum recovery 的说明，用来核对这套 HSM 在真实任务里是如何运行的。至于 EEG 分类器、谱正则化和概率公式等内容，第一次为了重做 `STM.md` 可以放到第二轮再看，因为它们主要解释信号来源，不是第一轮抽状态机主链的关键。

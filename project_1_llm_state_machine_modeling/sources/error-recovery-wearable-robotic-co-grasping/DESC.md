# 人工主导纠错的可穿戴协同抓握控制器 / Error recovery in wearable robotic Co-Grasping: the role of human-led correction

## 论文在讲什么

这篇论文研究的是可穿戴 robotic co-grasping 设备在出现抓取错误时，人类操作者如何主导恢复。论文重点表面上是 HRI 与 error recovery，但作者并不是只做用户研究问卷，而是先明确实现了一套实际的 device controller：用户通过 `open / close / calibrate` 指令驱动 gripper，机器人和手腕共同决定抓握器开合，而系统会在“可靠抓取”和“抓取错误”两种分支之间切换。

文章特别有价值的地方在于，它把这种 wearable grasping device 的控制链写得很实。`Maintain Aperture` 负责保持当前开口、允许用户调整姿势；`Automated Open` 和 `Automated Close` 负责自动开合；控制开关决定进入 `Reliable Grasp` 还是 `Grasp Error`；一旦发生错误，设备并不会直接宣告失败，而是进入 `Transfer` 并依赖人类用手腕运动完成收尾。这正好形成一条清晰的“自动化 + 人工接管恢复”监督链。

## 控制系统在文中的位置

这套控制系统不是论文背景配角，而是整个人机实验成立的基础。作者要研究 human-led correction，就必须先把机器人何时开、何时关、何时判为可靠抓取、何时故意制造 `Grasp Error`、以及错误后如何回到下一轮抓取写成确定的状态机。没有这部分实现，后面的信任变化、工作负荷和行为分析都无法解释。

不过它在文中的角色也与传统“只讲控制性能”的医疗/助力设备论文不同。这里的 FSM 主要承担实验载体功能，用来稳定地生成可恢复错误并观察人类如何接管。因此在 `sources/` 里，它更适合作为“控制器本身足够明确、而且带有人机纠错链”的样本，而不是当成单纯的执行机构或临床效果论文。

## 对我们为什么有用

它对 `🩺` 方向的价值，在于补进了一类很少见的 assistive grasping supervisor 样本。库里已有外骨骼、义肢、步态控制和康复设备条目，但这篇强调的是“wearable grasp device + 显式错误状态 + 人类主导恢复”，结构特征明显不同，能扩展医疗/助力设备样本的状态机多样性。

它也很适合做 `FSM + T0` 的双 A 条目。这里的状态、guard 和动作都写得很清楚：开口角度目标 `95°`、可靠抓取目标约 `65°`、错误情况下仅给出 `20%-60%` 的电机贡献、再由人类补完抓握。对后续自然语言建模，这类“成功分支 / 失败分支 / 人工恢复分支”特别适合训练异常恢复链条。

## 如果需要人工细读，建议怎么读

人工重读时，建议先直接看第 `4-6` 页的 `2.1.1 Control and actuation` 与 Figure `3`。先把 `Maintain Aperture`、`Automated Open`、`Automated Close`、`Reliable Grasp`、`Grasp Error`、`Transfer` 这些状态和 `open / close` 触发链读清楚，再把 `βopengoal`、`βclosegoal` 和 `6-18°` 的错误闭合幅度补上。

之后再看实验协议和结果章节，用来确认这套控制器在实验里是如何被重复调用、错误如何被人为恢复以及这些行为怎样影响信任和工作负荷。后面的统计分析可以后读，因为对恢复状态机链条而言，最关键的还是前面的控制实现与 Figure `3` 的状态关系。

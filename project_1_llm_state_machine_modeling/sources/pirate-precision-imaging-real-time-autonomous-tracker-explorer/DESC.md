# PIRATE 海上自主追踪与观测任务状态机 / PIRATE-Precision Imaging Real-Time Autonomous Tracker & Explorer

## 论文在讲什么

这篇论文介绍的是一个用于海上目标追踪与精细成像的自主平台 `PIRATE`。系统把航迹导航、声学监听定位、视觉检测跟踪和任务级决策整合到同一套 onboard architecture 里，使平台能够在一次连续 deployment 中完成声学搜索、目标定位、追击、盘旋观察和失效返航，而不需要岸基操作员持续接管。

文中最关键的是 mission execution 部分。作者明确把这套任务执行逻辑写成一个层次化 `FSM`，顶层模式包含 `idle`、`navigation`、`tracking`、`visual processing`、`return-to-home`、`fault handling`，其内部又带导航和感知子状态，并通过 acoustic localization、vision confidence、通信超时和故障事件驱动切换。实验章节还说明了 `triangulation -> pursuit -> loiter` 这类连续追踪循环如何在实船任务中发生。

## 控制系统在文中的位置

控制系统在这篇文章里不是附带说明，而是系统架构的中心。`Raspberry Pi 4` 被明确描述为 primary mission controller，负责 autonomous mission execution、subsystem coordination 和 safety enforcement；`FSM` 也不是单独画在一张图里做点缀，而是用来组织整个平台的任务生命周期和 failsafe 逻辑。

同时，这篇论文又不是纯粹的软件架构稿。作者没有停在“有一个 mission manager”这种泛化表述，而是说明了从任意活动状态如何通过 global interrupt 立即切入 `RTH`，以及在 tracking 任务中如何围绕 polygonal listening、incremental localization、pursuit 和 loiter 进行任务级切换。因此它提供的是可以落回真实自主平台运行逻辑的控制材料。

## 对我们为什么有用

它对 `sources/` 的价值，一方面在于补了 `⚙️` 方向里比较强的自主平台任务 supervisor 样本，另一方面在于它提供了一个非常干净的 `HSM + T0` 例子。很多海事或机器人论文虽然也写任务模式，但常常只停留在框架图或行为树概念层；这篇则明确给出 `FSM`、层次化状态、事件驱动转换和全局中断机制，适合直接抽成状态机自然语言样本。

它还补充了“感知结果反过来驱动导航行为”的样本类型。这里的 acoustic localization 和 visual processing 不是独立分析模块，而是会改变后续 pursuit、loiter 和 return 行为的任务输入，这对后续研究“LLM 如何从系统描述恢复 mode-switching logic”非常有帮助。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看平台架构和 `Mission execution` 部分，也就是第 `8-10` 页附近关于 `mission controller` 和 Figure `3` 的描述，把顶层模式、层次结构和 `RTH` 全局中断先读清楚。接着跳到 tracking 相关实验页，看 `single-receiver acoustic localization` 与连续 `tracking-pursuit cycles` 的说明，把 `triangulation / pursuit / loiter` 这条任务循环和触发条件补全。

第二轮再去看视觉检测模型、benchmark 分辨率比较和更多海洋生物观测背景，这些内容有助于理解为什么要这样设计平台，但对恢复状态机主链不是刚需。如果目的是重做 `STM.md`，最优先的仍然是 mission-execution 图、Raspberry Pi 任务协调描述，以及实验里那条完整的 tracking cycle。

# 超轻压电扑翼飞行器机载飞控架构 / An Architecture for Onboard Flight Control of a Sub-Gram Piezo-Actuated Aerial Vehicle

## 论文在讲什么

这篇论文讨论的是一套超轻、压电驱动扑翼飞行器的 onboard flight-control architecture。作者同时处理了高压驱动、电机波形生成、RTOS 任务调度、姿态控制和日志记录，但对 `sources/` 最关键的是：他没有把飞控只写成连续控制器，而是显式引入了一个机载 FSM 来管理致动器安全启动、起飞、正常控制、降落和关机序列。

这使得论文里的控制对象非常清楚。它不是泛泛的 “small UAV autonomy” 或 mission-level planner，而是围绕一个具体飞行平台，说明何时先升 offset、何时再升 amplitude、何时启用姿态环、何时进入 lateral control、何时按 landing/ramp-down 顺序安全退出。对于压电执行器这类对上电和关机过程极敏感的对象，这条离散控制链本身就是系统安全的一部分。

## 控制系统在文中的位置

这里的 FSM 不是附带说明，而是整套 flight-control framework 的 supervisory backbone。第 `3.1.2` 节单独定义 `stateMachineTask`，并说明它如何解释 start/end code、如何向 `flyControllerTask` 发 mode notification、以及为什么要把高层状态机和底层 controller 分开实现。

换句话说，论文里我们关心的控制系统描述就是主控制软件的一部分。低层 PID 和波形生成当然也重要，但它们在文中更多承担“状态内动作”的角色；真正决定飞行阶段切换和硬件安全顺序的，是 `Idle / Offset Ramp / Amplitude Ramp / Liftoff / Control On / Landing / Ramp-Down` 这一整条 FSM 链。

## 对我们为什么有用

这篇论文对文库的价值在于，它补的是一种在现有航空航天样本里并不常见的控制画像：不是 mission manager，也不是故障模式管理，而是“机载执行器安全上电 + 飞行阶段切换 + 安全退出”的细粒度飞行阶段控制器。它仍然属于 `FSM + T1`，但和 CubeSat 模式管理、UAV mission HSM 或 landing-gear sequencing 的结构差异很明显。

同时，这篇的原文和描述都非常容易维持双 A。原因不是作者画了一张状态图就结束，而是状态名、电压值、状态持续时间、controller mode handoff 和任务分工都写在正文里。后续做数据集时，这类样本很适合用来训练“如何从连续控制系统文本中抽出真正的离散 phase supervisor”。

## 如果需要人工细读，建议怎么读

如果后续需要人工重读，建议先直接看 `paper_content.txt` 对应第 `27-29` 页的 `FSM Task`、`FSM States and Transitions`、`Table 3.1` 和 `Table 3.2`。第一轮先锁定状态集合、每个状态的进入条件、输出动作和 mode notification，再把 `130 V / 140 V / 100 ms / 500 ms` 这些决定 T1 语义的参数圈出来。

第二轮再回看第 `19-24` 页附近对 piezo actuator、电压放大和波形生成的说明，确认为什么 ramp-up/ramp-down 不能被当成普通附属步骤。至于更前面的背景综述和更后的实验讨论，可以放到最后；它们有助于理解平台约束，但不是重建状态机主链的首要证据。

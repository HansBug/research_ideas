# 小型无人机自主驾驶仪控制系统 / An Autonomous Autopilot Control System Design for Small-Scale UAVs

## 论文在讲什么

这篇文献讨论的是一个面向 small-scale UAV 的 fully autonomous autopilot system。作者要解决的问题不是某个单独 PID 回路，而是如何把 mission program、FMS modes 和 controller modes 组织成一套可编程、可在飞行中重配置、可支持自主起飞和着陆的飞行控制系统。

论文的展开方式相当适合样本库使用。它先说明 `AutopilotSystem`、`FMS` 和 `Controller` 之间的层次关系，再进入 command list、command types、FMS modes 和 controller modes。也就是说，读者能清楚看到高层任务序列如何驱动低层反馈控制，而不只是看到零散的飞行动作或算法模块。

## 控制系统在文中的位置

这里的控制系统就是论文主体。虽然文中提到 `Reflection Architecture` 和 ground station 组件，但这些只是承载环境；真正被详细展开的是 flight management system 如何维护 mission program、如何在命令完成后切到下一命令，以及不同命令和 mode state machine 如何给控制器下达目标。

尤其重要的是，这篇论文同时给出两层状态机。第一层是 FMS 对 command list 的序列执行，它决定现在处在 takeoff、waypoint、circle、landing 还是 jump branch。第二层是具体 mode 自己的内部状态机，例如 `CmdAltitude` 里的 `AltitudeAttain` 和 `AltitudeHold`。因此它不是简单的平面 FSM，而是很典型的航空航天任务管理分层控制结构。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补的是一个比较稀缺的“高层任务管理而非连续飞控本体”的 UAV 样本。很多无人机论文虽然写 control，但主体落在姿态、导航、视觉或鲁棒控制上，真正能直接抽成状态机自然语言文本的内容不多；这篇则把 mission-level sequencing 写得很集中。

另外，它还补了一种很适合后续建模研究的表达模式：命令对象自己带内部状态，同时又向更下层 mode state machine 发出指令。对后续做 LLM 从自然语言恢复 HSM、或分析多层状态机之间职责分配的人来说，这种 “mission command -> FMS mode -> controller mode” 的链条很有代表性。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `4-5` 页，把 `AutopilotSystem / FMS / Controller` 三层关系和 command list 的更新流程读清楚，特别是 `Update()`、`IsComplete()` 和 “transition to the next command” 这部分。只要这里读明白，就能先确定这篇论文的主控制骨架到底是 mission sequencer，而不是姿态控制器本身。

然后直接跳到第 `8-11` 页，依次看 `Jump / Circle / TakeOff / Landing` 和 `CmdAltitude`。先抓住哪些命令对应哪些 mission state，再看 `AltitudeAttain -> AltitudeHold` 这种下层 mode state machine。第 `1-3` 页 ground station 与硬件背景、以及后面的 controller implementation 细节可以留到第二轮再看；当前若要重做 `STM.md`，优先级最高的是 FMS state machine、本地命令语义和嵌套 mode machine。

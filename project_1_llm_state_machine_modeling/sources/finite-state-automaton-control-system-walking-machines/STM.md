# Finite state automaton based control system for walking machines - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：原文把 walking machine 控制系统分解成 global navigation、local navigation 和 gait sub-behaviour 三层 FSM，并给出状态职责与 guard 条件，足以形成双 A 的机器人控制样本。

## 条目 1: Hierarchical Navigation-and-Gait Supervisor for a Walking Machine
- 控制对象：通用控制领域的 walking machine / hexapod 高层导航与步态监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个 walking machine 的层次化控制系统，把全局导航、本地导航和具体步态选择分别实现成相互协作的有限状态自动机。
- 判断：算。对象是实际多足行走机器人控制系统，原文明确给出层次结构、global/local navigation 各自的状态集合、gait sub-behaviour 的状态集合，以及由传感器/状态仓库驱动的迁移条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，`Control system structure`，`paper_content.txt` 第 223-255 行
> The developed control structure divides the overall system into smaller subsystems which are arranged in a hierarchical (top-down)
> structure.
> The general communication method is such: the highest level process sends the task demand to the level below (middle level),
> which in turn sends its demand to the level below it.
> Each process in the control structure is treated as a separate finite state automaton.

#### 摘录 B
- 出处：第 4 页，`Global navigation FSM`，`paper_content.txt` 第 267-306 行
> The global navigation automaton is the highest level subsystem in the control structure and is responsible for route generation.
> SinitSystemg: This is the initial state of the automaton. It sets up the data repositories and performs a check that the robot
> system is working properly.
> SwaitUserg ... request for a new mission ... or a request to modify or stop the mission in case of a locked path.
> SinitMotiong ... communicates the next goal position to the local navigation automaton.
> Smonitorg ... prepares the basic status messages (position error, heading error, etc.) for the other processes.
> Sendg ... terminates the process.

#### 摘录 C
- 出处：第 4-5 页，`Local navigation FSM`，`paper_content.txt` 第 307-376 行
> The local navigation subsystem is the middle-level functional process in the hierarchy. It is responsible for detailed path
> navigation and gait selection.
> SloadTargetl ... requests a new target point.
> SmoveFwdl ... generates the body trajectory for a straight line motion ... transitions to the SmoveLeftl state in case an obstacle is
> detected in the forward direction.
> SmoveLeftl ... when the forward path clears, it transitions back to the SmoveFwdl state.
> SmoveRightl ... when there is no path around the obstacle from the left side, the automaton transitions to this state.
> SturnLeftl ... SturnRightl ...
> Sstopl ... ensures the robot has stopped and returns the robot to its initial configuration.

#### 摘录 D
- 出处：第 5 页，gait sub-behaviour 层说明，`paper_content.txt` 第 377-407 行
> The local navigation subsystem is also responsible for the selection of these gaits. A two-tier definition of the behaviours is used.
> The upper level (the local navigation FSM as shown in Figure 3) is an FSM which switches between one and more of these
> behaviours. The lower layer governs which type of gait to use. This two-tier description follows the concept of hierarchical FSMs.
> Stripods: This state generates the tripod gait. The FSM transitions to this state when the motion surface is relatively flat.
> Swaves: The wave gait is implemented in this state. Since this is the most stable gait, the FSM transitions to this state when a
> surface inclination is detected.

#### 摘录 E
- 出处：第 6 页，transition guard 说明，`paper_content.txt` 第 451-474 行
> OnEntry and OnExit conditions are produced within the states using the whiteboard readings.
> If the status is different from normal, then the ffault as the OnExit condition becomes valid and the state transfers to Sstopl.
> When the sensory reading indicates the obstacle on the left, fleftobs is set as valid ...
> If at least one of fleftobs and foutofcorridor is valid, the state SmoveLeftl transfers to SmoveRightl.

### 2. 基于原文整理后的自然语言描述

The walking-machine controller is organized as a hierarchy of cooperating FSMs instead of as one monolithic locomotion loop. At the top, the global navigation automaton moves through states such as `SinitSystem`, `SwaitUser`, `SinitMotion`, `Smonitor`, and `Send` to initialize repositories, receive or modify mission requests, dispatch target positions, monitor errors, and terminate on failure or stop requests. The middle local-navigation FSM then switches among `SloadTarget`, `SmoveFwd`, `SmoveLeft`, `SmoveRight`, `SturnLeft`, `SturnRight`, and `Sstop`, using obstacle detections, heading corrections, and corridor-limit checks to choose straight motion, lateral avoidance, turning, or stop handling. Beneath those motion states, a lower gait FSM selects `Stripod` on relatively flat terrain and `Swave` when surface inclination is detected, so each motion behaviour is refined into a terrain-dependent gait mode. The paper further specifies whiteboard-driven guard conditions such as `ffault`, `fleftobs`, and `foutofcorridor`, including the transfer from `SmoveLeft` to `SmoveRight` when the left path or corridor condition becomes invalid, which makes the hierarchy a concrete state-based supervisor rather than a purely architectural sketch.

### 3. 逐句溯源

1. 句子 1：The walking-machine controller is organized as a hierarchy of cooperating FSMs instead of as one monolithic locomotion loop.
   对应摘录：A
2. 句子 2：At the top, the global navigation automaton moves through states such as `SinitSystem`, `SwaitUser`, `SinitMotion`, `Smonitor`, and `Send` to initialize repositories, receive or modify mission requests, dispatch target positions, monitor errors, and terminate on failure or stop requests.
   对应摘录：B
3. 句子 3：The middle local-navigation FSM then switches among `SloadTarget`, `SmoveFwd`, `SmoveLeft`, `SmoveRight`, `SturnLeft`, `SturnRight`, and `Sstop`, using obstacle detections, heading corrections, and corridor-limit checks to choose straight motion, lateral avoidance, turning, or stop handling.
   对应摘录：C
4. 句子 4：Beneath those motion states, a lower gait FSM selects `Stripod` on relatively flat terrain and `Swave` when surface inclination is detected, so each motion behaviour is refined into a terrain-dependent gait mode.
   对应摘录：D
5. 句子 5：The paper further specifies whiteboard-driven guard conditions such as `ffault`, `fleftobs`, and `foutofcorridor`, including the transfer from `SmoveLeft` to `SmoveRight` when the left path or corridor condition becomes invalid, which makes the hierarchy a concrete state-based supervisor rather than a purely architectural sketch.
   对应摘录：E

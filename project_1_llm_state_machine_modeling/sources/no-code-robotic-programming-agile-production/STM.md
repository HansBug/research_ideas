# No-code robotic programming for agile production: A new markerless-approach for multimodal natural interaction in a human-robot collaboration context - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 multimodal no-code robotic programming system 的 whole-system FSM、三个 operation mode 及其 subordinate FSM 一起交代清楚，状态、指令与动作之间的对应关系足以形成双 A 的 HSM 样本。

## 条目 1: Teaching/teleoperation/playback multimodal programming supervisor

- 控制对象：工业自动化与离散制造领域的多模态无代码机器人编程监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 speech、finger gesture、hand gesture 管理 `Teaching / Teleoperation / Playback` 三种 operation mode 的 whole-system supervisor，并在每个 mode 内继续使用 subordinate FSM 控制具体动作。
- 判断：算。对象不是一般论文写作流程，而是一个已实现的 robotic programming and execution system main controller；原文明确说 top-level FSM integrates all modules, speech commands are transition signals, and each operation mode contains a subordinate FSM.

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，Section `3.1.1`，`paper_content.txt` 第 298-303 行
> ... the articulation of the voice command will trigger a deterministic action in the finite state machine. When a user says “take point,” the actual coordinate of the finger will be extracted in the robot path.

#### 摘录 B

- 出处：第 9-10 页，Section `4.2 Operation modes`，`paper_content.txt` 第 637-647 行
> Three operation modes have been implemented ...
> 1. Teaching mode
> 2. Teleoperation mode
> 3. Playback mode
>
> In the teaching mode, the robotic program can be created by using index finger’s gesture and voice recognition system. Teleoperation mode supports remote control of the robot ... The playback mode is used to replay the programmed robot path ...

#### 摘录 C

- 出处：第 10-11 页，Section `4.2.1` 与 `4.2.2`，`paper_content.txt` 第 661-706 行
> The voice recognition system is linked to the finite state machine and will trigger a defined action ...
>
> command “take” triggers the state machine to extract the current pose of the finger as single robot path point.
>
> ... “Begin” initializes the extraction of a spline ... “End” ends the recording process ... “Delete” triggers the system to delete the latest taken object ... “Home” stops the teaching mode and initialize the main menu (idle).
>
> In the teleoperation mode ... A voice command is used to start the interaction ... The relative position of the hand to the initial position ... is calculated and used to manipulate the robot TCP in 3D.

#### 摘录 D

- 出处：第 12-13 页，Section `4.3 System diagram and finite state machine (FSM)`，`paper_content.txt` 第 739-770 行
> A finite state machine is used to integrate and control all modules. Figure 9 shows the finite state machine of the whole system and its sub-finite state machines. Each operation mode ... is encapsulated as system module containing a subordinate finite state machine.
>
> ... The teaching state server, teleoperation state server and playback state server receive a bypass information from the finite state machine when the respected operation mode is triggered. The bypass information is used as transition signal for each sub-finite state machine ...
>
> In teleoperation mode and playback mode, a control system signal is sent to the robot immediately after it is triggered by interactions.

### 2. 基于原文整理后的自然语言描述

The multimodal no-code robotic programming platform is supervised by a top-level FSM that switches among `Teaching`, `Teleoperation`, and `Playback` operation modes, while each mode encapsulates its own subordinate FSM and supporting modules. Speech commands act as transition signals for the top-level and subordinate machines: commands such as `take point` or `take` record the current finger pose, `Begin` and `End` start and stop spline capture, `Delete` removes the latest object, and `Home` returns the system to the idle main menu. In `Teaching` mode the controller couples finger tracking with voice-triggered capture actions to build robot path points or splines; in `Teleoperation` it locks the hand reference and maps relative hand motion to TCP control; and in `Playback` it converts the recorded path into robot-specific code and deploys it with parameter updates. The implementation therefore is not just a UI flowchart: the FSM sends bypass and control signals to state servers and robot-control modules, and the paper explicitly presents the whole-system FSM plus sub-FSMs that integrate perception, speech, calibration, and robot execution.

### 3. 逐句溯源

1. 句子 1：The multimodal no-code robotic programming platform is supervised by a top-level FSM that switches among `Teaching`, `Teleoperation`, and `Playback` operation modes, while each mode encapsulates its own subordinate FSM and supporting modules.
   对应摘录：B, D
2. 句子 2：Speech commands act as transition signals for the top-level and subordinate machines: commands such as `take point` or `take` record the current finger pose, `Begin` and `End` start and stop spline capture, `Delete` removes the latest object, and `Home` returns the system to the idle main menu.
   对应摘录：A, C
3. 句子 3：In `Teaching` mode the controller couples finger tracking with voice-triggered capture actions to build robot path points or splines; in `Teleoperation` it locks the hand reference and maps relative hand motion to TCP control; and in `Playback` it converts the recorded path into robot-specific code and deploys it with parameter updates.
   对应摘录：B, C
4. 句子 4：The implementation therefore is not just a UI flowchart: the FSM sends bypass and control signals to state servers and robot-control modules, and the paper explicitly presents the whole-system FSM plus sub-FSMs that integrate perception, speech, calibration, and robot execution.
   对应摘录：D

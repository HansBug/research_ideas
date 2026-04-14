# An Autonomous Autopilot Control System Design for Small-Scale UAVs - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把小型 UAV autopilot 的 flight management system 明确写成 state machine，并给出 `Jump / Circle / TakeOff / Landing` 命令状态链与 `CmdAltitude = AltitudeAttain -> AltitudeHold` 子状态机，适合作为航空航天方向的层次控制样本。

## 备注

- 该 PDF 在主文 `1-13` 页之后拼接了另一份 NASA seminar slides。当前提取只采用前 `13` 页的 autopilot paper 主体内容，不使用后续拼接材料作为证据。

## 条目 1: Hierarchical FMS Command Sequencer for a Small-Scale UAV

- 控制对象：航空航天与飞行控制领域的小型无人机 flight management system 与 autopilot command sequencer
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 small-scale UAV 的自主驾驶仪高层任务控制器，由顶层 FMS state machine 调度 programmable command list，同时把 `TakeOff / Landing / Circle / Jump / waypoint` 等命令与 `CmdAltitude` 等内部 mode state machine 叠接起来。
- 判断：算。对象是实际 aircraft autopilot system，而不是单纯软件框架说明；原文明确写出 FMS 是 state machine、命令完成后的 transition 规则、各命令模式和 `AltitudeAttain / AltitudeHold` 子状态机。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，Section `Commands in the Flight Management System`，`paper_content.txt` 第 98-156 行
> The flight management system class is a state machine that controls the continuous feedback control system in the controller object. ... The command list is an ordered list of commands that can be programmed on the ground, or reprogrammed while the aircraft is in the air. ... At each component update callback, the FMS calls the Update() method of the active command, which updates its internal state. The FMS then checks the IsComplete() method of the command; when TRUE is returned, the FMS transitions to the next command ...

#### 摘录 B

- 出处：第 8-9 页，Sections `Command: Jump / Circle / TakeOff / Landing`，`paper_content.txt` 第 197-227 行
> The Jump command instigates an immediate transition to another command in the list. ... The Circle command controls the aircraft to fly a circle pattern of a given radius about a waypoint. ... The TakeOff command provides commands for an autonomous takeoff sequence. The FMS modes are set to a dedicated 'TakeOff' mode ... Once the rotation takeoff speed is reached, the aircraft performs a climb longitudinal maneuver ... The Landing command is used for automated landings. The aircraft is commanded to maintain a track between waypoints and command a constant descent rate until the ground sonars pick up a reading from the ground ... the flare command will institute this command based on an ultrasonic altimeter ...

#### 摘录 C

- 出处：第 10-11 页，Section `Flight Management System Modes`，`paper_content.txt` 第 248-280 行
> Each mode is associated with one or more commands to the controller, and modes can be implemented as state machines. For instance, the CmdAltitude mode ... contains an internal state machine shown in Figure 16. ... AltitudeAttain ... Update/ Set PID inputs ... AltitudeHold ... The two state machines implementing an FMS mode and a command object could be integrated into a single machine ... The reason to have two state machines is to help avoid redundant code.

### 2. 基于原文整理后的自然语言描述

The autopilot is organized around a top-level flight management system whose job is to execute a programmable ordered command list rather than hard-code one fixed mission. At each update cycle, the FMS updates the active command, checks whether that command is complete, and then transitions to the next command in the mission list, which means the command list itself behaves as a controllable mission-state sequence. Several command classes define concrete mission states and branch targets: `Jump` immediately transfers control to another command, `Circle` keeps the aircraft in a loiter pattern, `TakeOff` commands runway heading plus full-throttle climb until a safe turning altitude is reached, and `Landing` tracks the final path, descends, and triggers flare from sonar or ultrasonic height information. The architecture is hierarchical because these command objects do not only switch the top-level mission sequence; they also output FMS modes and targets to lower layers of the controller. A representative nested mode is `CmdAltitude`, which itself is implemented as an internal state machine that first runs `AltitudeAttain` and then switches to `AltitudeHold` once the commanded altitude has been reached.

### 3. 逐句溯源

1. 句子 1：The autopilot is organized around a top-level flight management system whose job is to execute a programmable ordered command list rather than hard-code one fixed mission.
   对应摘录：A
2. 句子 2：At each update cycle, the FMS updates the active command, checks whether that command is complete, and then transitions to the next command in the mission list, which means the command list itself behaves as a controllable mission-state sequence.
   对应摘录：A
3. 句子 3：Several command classes define concrete mission states and branch targets: `Jump` immediately transfers control to another command, `Circle` keeps the aircraft in a loiter pattern, `TakeOff` commands runway heading plus full-throttle climb until a safe turning altitude is reached, and `Landing` tracks the final path, descends, and triggers flare from sonar or ultrasonic height information.
   对应摘录：B
4. 句子 4：The architecture is hierarchical because these command objects do not only switch the top-level mission sequence; they also output FMS modes and targets to lower layers of the controller.
   对应摘录：A, B, C
5. 句子 5：A representative nested mode is `CmdAltitude`, which itself is implemented as an internal state machine that first runs `AltitudeAttain` and then switches to `AltitudeHold` once the commanded altitude has been reached.
   对应摘录：C

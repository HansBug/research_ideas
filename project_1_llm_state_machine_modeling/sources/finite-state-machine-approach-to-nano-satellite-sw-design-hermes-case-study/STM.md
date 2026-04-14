# A finite state machine approach to nano-satellite SW design: the HERMES case study - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 HERMES 机载软件的 `LEOP / NOM / HSAFE` 骨干模式、时间驱动启动序列和故障回退逻辑都写得较完整，可直接整理为 CubeSat 模式管理样本。

## 条目 1: LEOP-NOM-HSAFE backbone for HERMES onboard software
- 控制对象：HERMES CubeSat 机载软件的顶层模式管理与故障回退逻辑
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 CubeSat 机载软件领域的 onboard software mode manager，用于在 `LEOP`、`NOM` 和 `HSAFE` 之间切换，并在启动、调度执行和异常回退阶段协调通信、ADCS 与载荷动作。
- 判断：算，但属于航天器模式管理/故障管理级样本。对象是实际 CubeSat 机载控制软件，原文明确给出了模式集合、进入/退出条件、启动时序和 `HSAFE` 的恢复分支。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，`FSM backbone states description / Transitions among FSM states`
> The FSM backbone states description ... a nano-satellite software can be structured upon three fundamental software macro-modes, which are here called LEOP, NOM and HSAFE.
>
> The LEOP mode is entered if the time is below a threshold from the first switch-on of the on-board computer in space ... The LEOP mode is exited when the time is above this time threshold, with a transition to the HSAFE mode.
>
> The entrance to the NOM mode can be only commanded by ground ... exiting from NOM mode is dictated by contingencies, i.e. failures and non-nominal situations detected and identified on-board, triggering the transition to the HSAFE mode.
>
> The HSAFE mode can be entered from both LEOP and NOM via on-board events and can be exited with a transition to NOM via ground intervention only.

#### 摘录 B
- 出处：第 9 页，`SW-MAIN LEOP mode operational schematic`
> At first, the OBC-MAIN board switches on and performs its automatic power-up and boot procedure.
>
> Once the OBC is operative, it waits until the end of the short slot 1, it boots the UHF board ... and then it deploys the two antennas ... the board starts sending a beacon message to ground in order to acquire the first contact.
>
> After the UHF operation, the LEOP mode boots the OBC-ADCS board.
>
> Then, if the boot is successful the software commands the ADCS to activate the detumbling mode ...
>
> When the time slot 2 is concluded ... the SW commands the deployment of the spacecraft's solar arrays.

#### 摘录 C
- 出处：第 10 页，`SW-MAIN HSAFE mode operational schematic`
> The logical architecture of the HSAFE mode has a tree structure, where system checks determine branches, which finally can lead to possible actions. Two main parameters manage the functioning of the HSAFE process: the battery voltage and the ADCS status.
>
> When the system enters HSAFE, the on-board computer powers off all HERMES' telecommunication systems, puts the ADCS in standby and the payload in power-save mode.
>
> After such operations ... the process enters the main central loop, which is based on the continuous check of battery voltage and ADCS status, and that can be exited only by a ground command.
>
> Depending on the battery and ADCS status, the process may lead to five different branches ... fatal error, detumbling, desaturation, safe or nominal ADCS branches.

### 2. 基于原文整理后的自然语言描述

The HERMES onboard software backbone is organized around three major modes, `LEOP`, `NOM`, and `HSAFE`, and transitions among them are guarded by time-from-boot, ground-schedule upload, or onboard detection of failures and other non-nominal conditions. In `LEOP`, the software executes a time-tagged startup sequence that powers up the OBC, waits for slot 1 to boot the UHF board and deploy the antennas for first-contact beaconing, then boots the OBC-ADCS, commands detumbling, and at slot 2 deploys the solar arrays even if full detumbling has not yet completed. When the LEOP time threshold expires, the machine moves to `HSAFE`, while entering `NOM` is allowed only from `HSAFE` after a ground-uploaded schedule and any contingency in `NOM` forces a return to `HSAFE`. On entering `HSAFE`, the controller powers off the telecommunication systems, puts the ADCS in standby, places the payload in power-save mode, and then runs a central loop that continuously checks battery voltage and ADCS status. That loop branches into fatal-error, detumbling, desaturation, safe-ADCS, or nominal-ADCS handling and can be exited only by ground command, so the overall controller combines a time-driven launch phase, a schedule-driven nominal phase, and a fault-driven safeguarding phase.

### 3. 逐句溯源

1. 句子 1：The HERMES onboard software backbone is organized around three major modes, `LEOP`, `NOM`, and `HSAFE`, and transitions among them are guarded by time-from-boot, ground-schedule upload, or onboard detection of failures and other non-nominal conditions.
   对应摘录：A
2. 句子 2：In `LEOP`, the software executes a time-tagged startup sequence that powers up the OBC, waits for slot 1 to boot the UHF board and deploy the antennas for first-contact beaconing, then boots the OBC-ADCS, commands detumbling, and at slot 2 deploys the solar arrays even if full detumbling has not yet completed.
   对应摘录：B
3. 句子 3：When the LEOP time threshold expires, the machine moves to `HSAFE`, while entering `NOM` is allowed only from `HSAFE` after a ground-uploaded schedule and any contingency in `NOM` forces a return to `HSAFE`.
   对应摘录：A
4. 句子 4：On entering `HSAFE`, the controller powers off the telecommunication systems, puts the ADCS in standby, places the payload in power-save mode, and then runs a central loop that continuously checks battery voltage and ADCS status.
   对应摘录：C
5. 句子 5：That loop branches into fatal-error, detumbling, desaturation, safe-ADCS, or nominal-ADCS handling and can be exited only by ground command, so the overall controller combines a time-driven launch phase, a schedule-driven nominal phase, and a fault-driven safeguarding phase.
   对应摘录：A, C

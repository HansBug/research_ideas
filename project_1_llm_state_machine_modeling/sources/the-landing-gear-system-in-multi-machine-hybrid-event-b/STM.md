# The landing gear system in multi-machine Hybrid Event-B - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：起落架手柄、模拟开关和 door/gear movement machines 的切换关系很明确。

## 条目 1: Landing-gear handle and movement-actuation logic
- 控制对象：飞机起落架控制系统

### 0. 条目识别与判定

- 一句话说明：这是航空机电控制领域的 landing gear control system，用于根据手柄指令在门/起落架执行链之间切换并驱动伸出、收回和锁定相关动作。
- 判断：算。对象是实际飞机起落架控制系统，原文明确给出了 handle up/down、初始锁定状态、模拟开关阶段以及 door/gear movement machines。

### 1. 原文摘录

#### 摘录 A
- 出处：第 8 页，Requirements assumptions，对 handle 与 initial state 的说明，行 591-593
> First, we assume that the pilot controls the gear via a han-
> dlefor which handle UPmeans gear up, and handle DOWN
> means gear down. We also assume that in the initial statethe gear is down and locked, since the aircraft does not levi-

#### 摘录 B
- 出处：第 11 页，Analogical switch，对 closing/closed/reopening episodes 的说明，行 766-789
> analogical switch is open by default. When a handle event
> occurs, the switch slowly closes (which takes from time 0
> till time CLOSED_INIT ), remains closed for a period (from
> time CLOSED_INIT till time CLOSED_FIN , allowing the
> onward transmission of commands from the computers to
> the general electrovalve), and then slowly opens again (fromtime CLOSED_FIN till time OPEN ). If a handle event occurs
> part way through this process, Fig. 4shows how the behaviour
> is affected: during closing, no effect; while closed, the closed
> period is restarted; during reopening, closing is restarted froma point proportional to the remainder of the reopening period.
> A clock, clk_AnSw (clk_xxx being another naming con-
> vention, used for clocks), controls this activity. For this towork, the pilot’s handle events are further synchronised with
> analogical switch events that reset clk_AnSw to the appro-
> 7Dealing with this properly in the Conf development caused the major-
> ity of the excessive verbosity.
> 8It may be argued that the phenomenon being discussed is absent at
> level 00, so the guard could have been included there, and removed atlevel 01, but in Event-B reﬁnement, guards are strengthened ,s ot h i s
> would have prevented the 00 to 01 development step from being anEvent-B reﬁnement.priate value, depending on its value at the occurrence of the
> handle event (N. B. The pilot’s handle events reach the ana-logical switch directly, and not via the computing modules,
> this being part of the complex interaction between pilot, ana-
> logical switch, and general electrovalve).
> Two further events ( AnSw_CLOSED_INIT_reached and
> AnSw_CLOSED_FIN_reached ) mark the transitions
> between episodes: from closing to closed, and from closed
> to reopening. Since these are ‘new’ events in an Event-Breﬁnement, their STATUS is convergent, and a ( N-valued)

#### 摘录 C
- 出处：第 13 页，Level 06，对 DoorsOpen/DoorsClose/GearExtend/GearRetract machines 的说明，行 949-952
> ders gives rise to a new machine: DoorsOpen _EV,Doors
> Close _EV,GearExtend _EV,GearRetract _EV.These four
> machines are identical in structure, so only Doors
> Open_EV is written out in full. The HydraulicCylinders_

### 2. 基于原文整理后的自然语言描述

The landing gear is controlled through a handle where handle UP means gear up and handle DOWN means gear down, and the initial condition has the gear down and locked. When a handle event occurs, the analogical switch closes, remains closed for a period, and then opens again, with dedicated events marking the changes from closing to closed and from closed to reopening. The hydraulic movement logic is organized into separate machines for opening doors, closing doors, extending gear and retracting gear.

### 3. 逐句溯源

1. 句子 1：The landing gear is controlled through a handle where handle UP means gear up and handle DOWN means gear down, and the initial condition has the gear down and locked.
   对应摘录：A
2. 句子 2：When a handle event occurs, the analogical switch closes, remains closed for a period, and then opens again, with dedicated events marking the changes from closing to closed and from closed to reopening.
   对应摘录：B
3. 句子 3：The hydraulic movement logic is organized into separate machines for opening doors, closing doors, extending gear and retracting gear.
   对应摘录：C

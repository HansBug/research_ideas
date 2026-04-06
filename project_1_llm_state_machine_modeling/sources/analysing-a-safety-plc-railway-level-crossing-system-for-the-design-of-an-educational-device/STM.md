# Analysing a safety PLC railway level crossing system for the design of an educational device - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对芬兰铁路道口安全 PLC 系统的 basic/alarm/automatic/manual/fault 语义、闸杆角度监测、预警时长、40 秒维持规则和故障恢复链写得很细，是轨交道口方向质量很高的双 A `HSM + T1` 样本。

## 条目 1: Railway Level-Crossing Alarm and Barrier Supervisor

- 控制对象：轨道交通与铁路控制领域的铁路道口安全 PLC 门控监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个铁路道口安全 PLC 监督系统，用轨道区段占用、人工按钮和故障条件共同决定道口警报、红白信号、闸杆下降/升起以及故障后的限制运行逻辑。
- 判断：算。对象是实际铁路道口控制系统，原文明确给出 basic/alarm/automatic/manual/disabled/fault 语义、闸杆位置监测、预警与维持时长、人工介入按钮和多类关键故障。

### 1. 原文摘录

#### 摘录 A

- 出处：第 31 页，`8.1.3 Alarm state`，`paper_content.txt` 第 826-850 行
> When the alarm track section becomes occupied, the level crossing’s alarm bells start ringing in addition to the road signal displaying fast-flashing red lights for the Pre-alarm time. The pre-alarm time can last for a minimum of 10 seconds and for every 10m between road barriers an addition 1 seconds should be added to the pre-alarm time.
>
> After the pre-alarm time has elapsed, the level crossing barriers lower to 0º ... Once the barriers pass the 60º angle, the lights on the barrier start flashing. Once the train occupies the road section ... the alarm bells stop ringing. When the road section ... is no longer occupied the barriers rise back to 90º. Once the barriers cross over the 60º angle, the road signal’s flashing red lights stop flashing and a slow-flashing white light is displayed.
>
> In the case of a level crossing that is equipped with double barrier ... the barriers of the lanes leading away from the level crossing must be lowered 10 seconds after the barriers of the leading lanes have begun to lower.

#### 摘录 B

- 出处：第 32-33 页，`8.1.4 Automatic operation / 8.1.5 Manual operation / 8.2.1 Road signals`，`paper_content.txt` 第 856-895 行
> A level crossing is in its automatic state when the following condition apply: Only the described track sections control the alarm state ... The level crossing is not in a faulty state ... The level crossing alarm state has not been manually activated ... An interlocking system does not prevent the function of the automatic system.
>
> In the event that an alarm section becomes occupied and then subsequently becomes vacant ... the level crossing must remain in its alarm state for 40 seconds.
>
> The level crossing’s alarm state can be activated by the use of the alarm switch (TK) ... or with the use of the track side alarm button (TR ON). ... the alarm must end with the use of the TR EI button. A level crossing can be disabled by the use of operation switch (KK).
>
> In the basic state ... the signal must display a slow flashing white light ... When the level crossing is in its alarm state, the signal must display a fast-flashing red light.

#### 摘录 C

- 出处：第 34-42 页，`8.2 Configuration and components / 8.3 Level crossing analyses - Faults`，`paper_content.txt` 第 917-973 行、第 982-1005 行、第 1089-1124 行
> Barriers are monitored in the horizontal position (0º), the vertical position (90º) and in the intermediate position (60º). When power is lost the barriers automatically lower to the 60º position.
>
> When the break is de-energized the barriers lower to the 60º position and the barrier lights start flashing. ... Adjustable limit switches close as the barriers reach their end limits (0º and 90º) in addition to the intermediate position (60º).
>
> TK Switch: Alarm switch activates the level crossing alarm ... TR ON Button ... activates the level crossing alarm ... TR EI Button ... deactivates the level crossing alarm ... PAL Button ... is used to clear long alarm faults.
>
> Critical faults preventing the completion of the alarm sequence ... Long alarm fault can occur when the alarm section ... is occupied ... for over 10 min ... A level crossing with a level crossing signal should indicate “Approach with caution” and the level crossing alarm must end 20 seconds after the level crossing signal indicates “Approach with caution”.
>
> In a situation where the barriers do not lower to the 0º position in the required 10 seconds a barrier fault occurs.

### 2. 基于原文整理后的自然语言描述

The level-crossing controller is best read as a hierarchical safety supervisor with `basic`, `alarm`, `automatic`, `manual`, `disabled`, and `fault` viewpoints layered over the same crossing equipment. In the basic state the barriers stand at `90°`, the road signal shows slow-flashing white, and the bells are silent, but when an alarm section becomes occupied the controller starts bells, switches the road signal to fast-flashing red for a pre-alarm of at least `10 s` plus `1 s` per `10 m` between barriers, then lowers the barriers to `0°`; barrier lights start flashing once `60°` is crossed. Automatic operation is allowed only when track sections govern the crossing, no blocking fault is active, the alarm has not been manually latched, and no interlocking system suppresses the function; if an alarm section briefly clears without a full passage, the alarm must remain active for `40 s`. Manual operation can force the alarm via `TK` or `TR ON`, clear it via `TR EI`, disable the crossing via `KK`, and reset long-alarm faults via `PAL`, so operator interventions are explicitly separated from train-driven activation. The barrier mechanism and fault model are also explicit: the PLC monitors `0°/60°/90°` positions, de-energized power or brake loss must drop the barrier to `60°`, failure to reach `0°` within `10 s` becomes a barrier-position fault, and a long-alarm fault is triggered after `10 min` of inconsistent track occupancy before the signal is driven to `Approach with caution` and the alarm terminates after `20 s`.

### 3. 逐句溯源

1. 句子 1：The level-crossing controller is best read as a hierarchical safety supervisor with `basic`, `alarm`, `automatic`, `manual`, `disabled`, and `fault` viewpoints layered over the same crossing equipment.
   对应摘录：A, B, C
2. 句子 2：In the basic state the barriers stand at `90°`, the road signal shows slow-flashing white, and the bells are silent, but when an alarm section becomes occupied the controller starts bells, switches the road signal to fast-flashing red for a pre-alarm of at least `10 s` plus `1 s` per `10 m` between barriers, then lowers the barriers to `0°`; barrier lights start flashing once `60°` is crossed.
   对应摘录：A, B
3. 句子 3：Automatic operation is allowed only when track sections govern the crossing, no blocking fault is active, the alarm has not been manually latched, and no interlocking system suppresses the function; if an alarm section briefly clears without a full passage, the alarm must remain active for `40 s`.
   对应摘录：B
4. 句子 4：Manual operation can force the alarm via `TK` or `TR ON`, clear it via `TR EI`, disable the crossing via `KK`, and reset long-alarm faults via `PAL`, so operator interventions are explicitly separated from train-driven activation.
   对应摘录：B, C
5. 句子 5：The barrier mechanism and fault model are also explicit: the PLC monitors `0°/60°/90°` positions, de-energized power or brake loss must drop the barrier to `60°`, failure to reach `0°` within `10 s` becomes a barrier-position fault, and a long-alarm fault is triggered after `10 min` of inconsistent track occupancy before the signal is driven to `Approach with caution` and the alarm terminates after `20 s`.
   对应摘录：C

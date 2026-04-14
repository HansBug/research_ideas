# Design of PLC Control System for Automatic Door - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动门的传感输入、8 秒等待、6 秒关门、0.2 秒防夹、故障灯和急停重置都写成了明确的 PLC 逻辑链，可直接形成双 A 样本。

## 条目 1: Timed Open-Close and Anti-Pinch Door Controller
- 控制对象：楼宇机电领域的 PLC 自动滑门控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个面向商场和酒店入口的自动滑门 PLC 控制系统，用多种人体/红外/安全光栅传感器驱动开门、关门、防夹、故障停机和急停报警。
- 判断：算。对象是实际建筑机电控制系统，原文不仅说明了控制流程，还给出了传感器集合、I/O 规模、定时量和故障复位条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，`2. System Design / 3. System Hardware Design`，`paper_content.txt` 第 83-100 行、第 167-178 行
> this paper designs the most used automatic sliding door. The automatic sliding door uses the inductive switch and safety grating to realize automatic control. At the same time, the manual control is realized by using the operation buttons.
>
> This paper adopts the photoelectric sensor to collect whether the object passes the signal to the PLC, and controls the opening and closing of the automatic door through the inverter, the driving motor and the transmission device.
>
> In this paper, the sensor switch mainly uses infrared human body sensor switch, microwave radar sensor switch and safety grating.
>
> According to the estimation of the number of input and output addresses, the design selects the CPU 226 as the configured S7-200 PLC, and needs to input 12 points and 14 output points.

#### 摘录 B
- 出处：第 5 页，`Automatic control of closing and anti-clamping`，`paper_content.txt` 第 203-210 行
> the door opener I0.4 and enters the 8s timing. During the three sensors I0.6, I0.7, I1.0, if an object is detected, the timer T37 retimed.
>
> After the automatic door detects no object for 8 s, the PLC’s Q0.1, M0, V0 action, pass to the inverter a motor reversal signal and low speed running signal, a total of 6s automatic door closing, if any object is closed when the automatic door is closed I1.0 detects that the automatic door stops closing and executes the automatic door opening procedure.
>
> the automatic door uses a safety grating with a delay of only 0.2 s to prevent the object from being clamped.

#### 摘录 C
- 出处：第 5-6 页，`alarm conditions / System Verification`，`paper_content.txt` 第 211-237 行
> The automatic door appears to be operated manually or automatically (Q0.0 or Q0.2) and closed (Q0.1 or Q0.3). The door will judge by the program, the M0.1 action will stop the whole automatic door control system, the fault light Q1.1 will light up ... press the abnormal reset button I1.3 to make the automatic gate program is reset.
>
> the surrounding personnel can directly press the red emergency stop button I0.1, and the M0.0 action automatic door program stops working, and then ... the alarm light Q0.5 works simultaneously with the alarm Q0.4.
>
> The automatic door in the text is mainly composed of two control modes, manual control and automatic control of the opening and closing of the automatic door.

### 2. 基于原文整理后的自然语言描述

The automatic sliding-door controller uses a PLC-centered architecture in which photoelectric, infrared-human, microwave-radar, and safety-grating sensors feed the door-opening and door-closing logic, while a Siemens `S7-200 CPU 226` handles `12` input points and `14` output points. In automatic mode, the door-opener signal `I0.4` starts an `8 s` timing stage, and if any of the sensors `I0.6`, `I0.7`, or `I1.0` still detects an object during this stage, timer `T37` is retriggered. Once no object is detected for `8 s`, the PLC activates `Q0.1`, `M0`, and `V0` to send a reverse low-speed signal to the inverter and closes the door over `6 s`; if `I1.0` detects an object during closing, the door stops closing, reopens, and relies on a `0.2 s` safety-grating delay to prevent pinching. The same controller also detects contradictory open/close outputs as a fault condition that raises `Q1.1` and requires reset by `I1.3`, and it supports an emergency-stop branch in which `I0.1` halts the system and triggers alarms `Q0.4` and `Q0.5`.

### 3. 逐句溯源

1. 句子 1：The automatic sliding-door controller uses a PLC-centered architecture in which photoelectric, infrared-human, microwave-radar, and safety-grating sensors feed the door-opening and door-closing logic, while a Siemens `S7-200 CPU 226` handles `12` input points and `14` output points.
   对应摘录：A
2. 句子 2：In automatic mode, the door-opener signal `I0.4` starts an `8 s` timing stage, and if any of the sensors `I0.6`, `I0.7`, or `I1.0` still detects an object during this stage, timer `T37` is retriggered.
   对应摘录：B
3. 句子 3：Once no object is detected for `8 s`, the PLC activates `Q0.1`, `M0`, and `V0` to send a reverse low-speed signal to the inverter and closes the door over `6 s`; if `I1.0` detects an object during closing, the door stops closing, reopens, and relies on a `0.2 s` safety-grating delay to prevent pinching.
   对应摘录：B
4. 句子 4：The same controller also detects contradictory open/close outputs as a fault condition that raises `Q1.1` and requires reset by `I1.3`, and it supports an emergency-stop branch in which `I0.1` halts the system and triggers alarms `Q0.4` and `Q0.5`.
   对应摘录：C

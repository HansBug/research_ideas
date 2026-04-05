# Control System Design of Automatic Door Based on PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动门的开门、保持、延迟关门、防夹回开、限位停机和人工按钮分支写成了完整 PLC 逻辑链，可直接纳入双 A 样本。

## 条目 1: Sensor-Triggered Automatic Door Open-Hold-Close Controller
- 控制对象：楼宇机电领域的 PLC 自动门控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向建筑出入口的自动门 PLC 控制器，用人体感应、门位限位、反夹红外和人工按钮共同驱动开门、延迟关门、反向回开与停机逻辑。
- 判断：算。对象是明确的自动门控制系统，原文不仅说明了工作流程，还给出了门位检测、脉冲驱动、障碍回退和输入输出规模。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，`2. Working Principle`（对应 `paper_content.txt` 第 24-32 行）
> The system uses PLC as the main controller of the automatic door. When the induction detector detects someone close, the pulse signal is transmitted to PLC ... motor running forward drive door open. When the door is opened, it is judged by PLC and remains open until there is no one on the door. If there is no one on the door, PLC notify the motor as a reverse movement, in a short time to automatically close the door. In the closing process, if someone close to the probe, PLC automatically switch to the state of the door.

#### 摘录 B
- 出处：第 2 页，`3.2-3.5 Hardware Components`（对应 `paper_content.txt` 第 45-74 行）
> Two travel switches are provided ... the door opening limit switch is used for detecting the position when the door is closed completely. ... When the door is close to the limit switch, the motor runs at low speed, and the motor is controlled by the program.
>
> During the closing process, the receiver receives no light signal to generate a negative pulse, and the pulse is used as an interrupt signal of PLC, and the PLC controls the door body to move in the opposite direction.
>
> The input control signals, a total of 11 points in the PLC ... PLC output of the control signal points to 4 points.

#### 摘录 C
- 出处：第 2-3 页，`4.1 Main Program Module / 4.2 Open Subroutine and Closed Subroutine Module`（对应 `paper_content.txt` 第 77-107 行）
> When the stop button is pressed, the PLC does not respond to the closing request, and the motor stops working ... if you receive the induction signal of human body, first call door subroutine, after confirming that no one, after a period of time delay, call closed subroutine.
>
> When opening the door ... detect the motor running, turn a circle of travel variables plus one. The last door detection limit, closing signal output of the motor, to avoid when the door is fully open, motor movement.
>
> When closing the door ... the output motor drive signal, the motor reverse ... If the door is closed, the motor signal is cut off.

### 2. 基于原文整理后的自然语言描述

The automatic-door controller uses a PLC as the central decision unit and opens the door when a human-body induction detector sends a pulse indicating that someone is approaching. After opening, the controller keeps the door open while the doorway remains occupied, and once no person is detected it enters a delayed close branch that reverses the motor and closes the door automatically. Two travel switches supervise the fully-open and fully-closed positions, force low-speed motion near the limit positions, and stop the motor when the target position is reached. During closing, an infrared anti-pinch sensor emits an interrupt pulse if a person or object is detected in the doorway, causing the PLC to reverse the door body immediately and move it in the opposite direction. The same implementation also includes manual open, manual close, start, and stop button branches together with `11` PLC input points and `4` output points, so the resulting controller is a complete EFSM rather than a single nominal open-close chain.

### 3. 逐句溯源

1. 句子 1：The automatic-door controller uses a PLC as the central decision unit and opens the door when a human-body induction detector sends a pulse indicating that someone is approaching.
   对应摘录：A
2. 句子 2：After opening, the controller keeps the door open while the doorway remains occupied, and once no person is detected it enters a delayed close branch that reverses the motor and closes the door automatically.
   对应摘录：A, C
3. 句子 3：Two travel switches supervise the fully-open and fully-closed positions, force low-speed motion near the limit positions, and stop the motor when the target position is reached.
   对应摘录：B
4. 句子 4：During closing, an infrared anti-pinch sensor emits an interrupt pulse if a person or object is detected in the doorway, causing the PLC to reverse the door body immediately and move it in the opposite direction.
   对应摘录：B
5. 句子 5：The same implementation also includes manual open, manual close, start, and stop button branches together with `11` PLC input points and `4` output points, so the resulting controller is a complete EFSM rather than a single nominal open-close chain.
   对应摘录：B, C

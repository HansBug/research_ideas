# Embedded Dam Gate Control System using C and Visual Basic - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把小型水坝闸门的液位传感、阈值开闭、上下限停机、自动/手动切换和操作员控制面板写成了完整控制主链，可直接纳入双 A 样本。

## 条目 1: Water-Level Threshold Dam-Gate Auto/Manual Controller

- 控制对象：过程与环境控制领域的水坝闸门液位阈值控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向中小型水坝的 AT89S51 闸门控制系统，用五级液位传感器、继电器驱动电机、限位开关和 Visual Basic 控制面板完成自动阈值控制与手动接管。
- 判断：算。对象是明确的水坝闸门控制器，原文直接给出了液位输入、自动模式上下阈值、手动模式命令、限位停机和控制面板接口。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract 与 Introduction，`paper_content.txt` 第 32-55 行、第 76-87 行
> improper opening and closing of the dam gate according to the level of water in the dam. ... This project is a AT89S51 microcontroller based dam gate control system ... efficient operation of dam gate according to the level of water ...
>
> This system facilitates us to control the gates of a dam depending on the water level automatically. It consists of a set of sensors connected to a DC motor through an 8-bit microcontroller (AT89S51). The water level is detected based on the feedback from the mechanism used. Depending on the water level of the dam gate can be controlled using a DC motor and a personal computer.

#### 摘录 B

- 出处：第 2-5 页，`3. HARDWARE IMPLEMENTATION AND OPERATION`，`paper_content.txt` 第 172-197 行、第 210-233 行、第 320-354 行
> five sensors are used at various levels (very low,1/4,1/2,3/4,full). ... whenever water level increases or decreases and comes in contact with each sensor the corresponding transistor conducts and amplify the sensor output. ... When water reaches each and every level then respective level value programmed in microcontroller will be indicated in LCD and the operator will either open/close the gate.
>
> The proposed system uses five sensors to sense various levels of dam water. Whenever the water level rises or decreases and comes in contact of any sensor then the circuit is complete ... The output of the sensor circuit triggers the microcontroller. ... it will drive the DC motor through the motor driver relay circuit and the dam gate ... will also move and it will get opened or closed according to the water level. To operate the gates of dam at the water levels which are not supported by the system an operator can be placed at the control room to control all the operation of the dam.
>
> Four SPDT relays are used one for opening the gate, one for closing the gate, one to turn 'ON' the buzzer/alarm ... An additional feature of limit switches is also provided ... There are two limit switches attached one at top and another at bottom. ... as soon as it touches the switch then the supply to motor is cut and the gate movement stops. Similarly the mechanism works while closing of gates.

#### 摘录 C

- 出处：第 5-6 页，`5. SOFTWARE DESCRIPTION`，`paper_content.txt` 第 393-406 行、第 425-459 行
> Fig. 8 signifies the flowchart of the operation of the system in AUTO mode ... In AUTO mode the operation of dam gate is controlled by microcontroller. ... In this mode the highest level of water is assumed to be 4ft and the lowest level to be 3ft according to our model. Whenever the water level reaches the highest level (4ft) then the controller will open the gate and water level will decrease and as soon as it reaches the lowest level (3ft) the controller will close the gate.
>
> We also used Visual basic 6 software based control panel providing the operator to control the system during manual mode. According to our proposed system an operator is available to control the gates at certain conditions that the system doesn’t support.
>
> AUTO/MANUAL command is used to give the options for auto/manual operation of gate. The OPEN, CLOSE and STOP command is used for opening, closing and stopping the gate in manual mode. ... For auto mode an upper and lower limit are indicated for reference.

### 2. 基于原文整理后的自然语言描述

The dam-gate controller uses an AT89S51 microcontroller, five discrete water-level sensors, relay-driven DC-motor actuation, LCD indication, and a PC-linked Visual Basic panel to supervise gate opening and closing. Its hardware path is explicit: each water-level contact activates a transistor-amplified sensor signal, the microcontroller reads those level events, and the relay driver energizes dedicated open, close, and alarm channels to move the gate. In automatic mode, the controller applies a threshold policy with a high limit of `4 ft` and a low limit of `3 ft`: when the water reaches the high threshold it opens the gate, and when the level later falls to the low threshold it closes the gate again. At levels or situations that the automatic policy does not support, the operator can switch into manual mode through the Visual Basic panel and issue `OPEN`, `CLOSE`, or `STOP` commands while still observing the indicated upper and lower limits. Limit switches at the top and bottom cut motor power at the end positions, so the resulting sample is an EFSM with sensor-driven automatic control, manual override, and end-stop protection.

### 3. 逐句溯源

1. 句子 1：The dam-gate controller uses an AT89S51 microcontroller, five discrete water-level sensors, relay-driven DC-motor actuation, LCD indication, and a PC-linked Visual Basic panel to supervise gate opening and closing.
   对应摘录：A, B, C
2. 句子 2：Its hardware path is explicit: each water-level contact activates a transistor-amplified sensor signal, the microcontroller reads those level events, and the relay driver energizes dedicated open, close, and alarm channels to move the gate.
   对应摘录：B
3. 句子 3：In automatic mode, the controller applies a threshold policy with a high limit of `4 ft` and a low limit of `3 ft`: when the water reaches the high threshold it opens the gate, and when the level later falls to the low threshold it closes the gate again.
   对应摘录：C
4. 句子 4：At levels or situations that the automatic policy does not support, the operator can switch into manual mode through the Visual Basic panel and issue `OPEN`, `CLOSE`, or `STOP` commands while still observing the indicated upper and lower limits.
   对应摘录：B, C
5. 句子 5：Limit switches at the top and bottom cut motor power at the end positions, so the resulting sample is an EFSM with sensor-driven automatic control, manual override, and end-stop protection.
   对应摘录：B

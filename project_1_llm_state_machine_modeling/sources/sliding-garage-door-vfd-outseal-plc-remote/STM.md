# Design and Construction of a Sliding Garage Door Powered by a 3-Phase Motor Controlled by a Variable Frequency Drive (VFD) Based on an Outseal PLC, with a Remote Control as the Trigger - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出的控制链较简单，但仍完整覆盖了远程开/停/关命令、限位停机、VFD 速度设定、保护分支和断电手动回退，足以形成一个可追溯的自动门样本。

## 条目 1: Remote-Triggered Sliding Garage Door Open-Stop-Close Controller

- 控制对象：楼宇机电与电梯控制领域的 PLC 车库滑门开闭控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🧰 清洗后保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向住宅/轻工业场景的自动车库门控制器，用 Outseal PLC 接收 RF 遥控器命令，并通过 VFD、三相电机和限位开关完成开门、停门和关门过程。
- 判断：算。对象是真实车库门控制系统，原文明确给出了命令源、执行器、限位保护、速度设定和异常供电下的手动退化行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract 与 Introduction，`paper_content.txt` 第 24-37 行、第 77-88 行
> This study discusses the design and development of an automatic sliding garage door system powered by a three-phase electric motor and controlled via a Variable Frequency Drive (VFD) based on an Outseal Programmable Logic Controller (PLC). The system is engineered to enhance operational efficiency and convenience by utilizing a remote control as the primary trigger for opening and closing the door. ... The Outseal PLC serves as the central controller, integrating signals from the remote control and automatically managing the operation of both the VFD and the three-phase motor.
>
> implementing a remote control as the primary trigger adds significant value ... With a single touch, users can open or close the garage door without being near the main control system. The combination of a three-phase motor, VFD, Outseal PLC, and remote control results in a modern, responsive, and reliable garage door automation system.

#### 摘录 B

- 出处：第 2-3 页，`1.3. Research Objective / 2. MATERIALS AND METHODS`，`paper_content.txt` 第 136-154 行、第 173-221 行
> The objective of this study is to design and develop an automatic sliding garage door system ... controlled by a Variable Frequency Drive (VFD) based on an Outseal PLC, and operated via remote control. Specifically, this research aims to ... develop a control program based on the Outseal PLC to manage motor and VFD operations efficiently and safely ... Integrate a remote control system as the primary trigger for automatic door opening and closing.
>
> Variable Frequency Drive (VFD) functions to regulate the motor's speed and rotation direction flexibly, while also protecting against overload and electrical disturbances. ... Outseal PLC serves as the central control unit of the system. This PLC is programmed to manage the motor and VFD's operational logic based on input from the remote control. ... Limit Switch functions as a safety device and position indicator to determine the end points of the door during opening and closing operations.
>
> Control logic was programmed using Ladder Diagrams in Outseal Studio V3.6. The program included start/stop conditions, speed settings, and responses to remote signals and limit sensors.

#### 摘录 C

- 出处：第 3-4 页，`3. RESULT AND DISCUSSION`，`paper_content.txt` 第 234-264 行、第 286-309 行
> The system responded to signals from the remote control with an average delay of less than 1 second. The door’s open and close functions operated as commanded ... OPEN STOP CLOSE.
>
> At a VFD frequency of 3 Hz and motor speed of 90 rpm, the door took 13 seconds to open or close. At 3.5 Hz and 105 rpm, the time reduced to 11 seconds. Frequencies above 4 Hz affected speed and door inertia, causing the door to bounce upon reaching its final position or stop point.
>
> The PLC successfully managed motor sequences, read inputs from the remote and sensors, and delivered accurate outputs to the VFD. Limit sensors functioned effectively to stop door movement at the end positions. The VFD’s protection system also activated during current surges, safeguarding the motor from damage.
>
> In the event of a power outage ... the door can still be easily opened manually by simply pushing it.

### 2. 基于原文整理后的自然语言描述

The garage-door controller is centered on an Outseal PLC that receives RF remote-control commands and then drives a three-phase motor through a VFD to open, stop, or close the sliding door. Its hardware structure is explicit: the VFD provides direction and speed regulation while also handling overload and disturbance protection, and limit switches mark the end positions of the door during both opening and closing. In software, the PLC ladder program implements start/stop logic, speed settings, and reactions to both remote signals and limit-sensor feedback, so the door does not simply run blindly once a command is issued. The reported system responds to remote commands in less than one second, achieves full open/close cycles in `13 s` at `3 Hz` and `11 s` at `3.5 Hz`, and shows that frequencies above `4 Hz` produce excessive inertia and bounce at the final position. When end sensors are reached the PLC stops the motion, the VFD protection branch handles current surges, and in a full power outage the door degrades to manual push operation rather than remaining permanently locked.

### 3. 逐句溯源

1. 句子 1：The garage-door controller is centered on an Outseal PLC that receives RF remote-control commands and then drives a three-phase motor through a VFD to open, stop, or close the sliding door.
   对应摘录：A, B
2. 句子 2：Its hardware structure is explicit: the VFD provides direction and speed regulation while also handling overload and disturbance protection, and limit switches mark the end positions of the door during both opening and closing.
   对应摘录：B, C
3. 句子 3：In software, the PLC ladder program implements start/stop logic, speed settings, and reactions to both remote signals and limit-sensor feedback, so the door does not simply run blindly once a command is issued.
   对应摘录：B
4. 句子 4：The reported system responds to remote commands in less than one second, achieves full open/close cycles in `13 s` at `3 Hz` and `11 s` at `3.5 Hz`, and shows that frequencies above `4 Hz` produce excessive inertia and bounce at the final position.
   对应摘录：C
5. 句子 5：When end sensors are reached the PLC stops the motion, the VFD protection branch handles current surges, and in a full power outage the door degrades to manual push operation rather than remaining permanently locked.
   对应摘录：C

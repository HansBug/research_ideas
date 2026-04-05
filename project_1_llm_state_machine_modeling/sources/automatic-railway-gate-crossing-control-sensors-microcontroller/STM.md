# Automatic Railway Gate and Crossing Control based Sensors & Microcontroller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把两侧传感器触发的关闸、列车通过保持关闭和离站开闸链条写得较完整，并补充了微控制器到驱动电机的执行路径，能够形成双 A 的道口门控样本。

## 条目 1: Two-Sensor Railway Gate Open-Close Controller

- 控制对象：轨道交通与铁路控制领域的双传感器铁路道口门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 8052 微控制器的铁路道口控制器，用线路前侧和后侧传感器触发关闸、保持关闭和开闸恢复，并通过驱动器带动步进电机执行栏杆动作。
- 判断：算。对象是真实道口门控控制系统，原文明确说明了前后侧传感器的布置、关闸与开闸触发条件、报警指示以及微控制器到电机驱动链路。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 19-44 行
> The main objective of this paper is to manage the control system of railway gate using microcontroller ... two sensors placed on either side of the gate ... We call the sensors along the train direction as foreside sensor and the other as after side sensor. When foreside sensor gets activated ... the gate is closed and stays closed until the train crosses the gate and reaches after side sensors. When the side sensor activated ... motor turns in opposite direction and gate opens and motor stops automatically.

#### 摘录 B

- 出处：第 2 页，Introduction / Train Accident Avoidances，`paper_content.txt` 第 94-121 行
> As a train approaches the railway crossing from either side, the sensors placed at a certain distance from the gate detects the approaching train and accordingly controls the operation of the gate. When the wheels of the train moves over both tracks are shorted to ground and this acts as a signal to the microcontroller indicating train arrival. Also indicator light has been provided to alert the motorists ...
>
> When the train arrives in a particular direction the transmitter IR senses ... and generates an interrupt. When interrupt is generated the stepper motor rotates in clockwise direction. When the interrupt ends the stepper motor rotates in anti clock wise direction.

#### 摘录 C

- 出处：第 5 页，`4. Methodology`，`paper_content.txt` 第 256-287 行
> When train crosses the first sensor that is S1. Sensor S1 start incrementing to the microcontroller and microcontroller decides to close the railway crossing because the microcontroller senses that the railway crossing is open before sensing the sensors.
>
> The microcontroller decides to close the railway crossing and extract a digital signal ... which drives the relay driver ... these drivers drive the motor according to the instructions of microcontroller. The same process is repeated after crossing of the S2 sensor. This S2 sensor senses and gives an increment to microcontroller and the microcontroller opens the crossing because previously microcontroller got the instruction that the railway crossing is closed ...

#### 摘录 D

- 出处：第 5 页，`5. Result and Discussion`，`paper_content.txt` 第 304-315 行
> The automatic railway gate control at the level crossing and anti collision device. The time for which it is closed is less compared to the manually operated gates and also reduces the human labor. This type of gates can be employed in an unmanned level crossing where the chances of accidents are higher and reliable operation is required. Since the operation is automatic error due to manual operation is prevented.

### 2. 基于原文整理后的自然语言描述

The railway level-crossing controller uses a microcontroller and two directionally interpreted trackside sensors to manage a simple but explicit open-close gate sequence. When the foreside sensor `S1` detects an approaching train, the controller interprets the crossing as currently open, issues a close command, and drives the gate motor through its relay-driver chain until the barrier is shut. The gate then remains closed while the train occupies the crossing zone, and indicator signals alert road users that a train is approaching or passing. After the train reaches the after-side sensor `S2`, the controller reverses the motor direction and opens the gate automatically. In effect, the paper describes a sensor-triggered two-phase barrier supervisor: arrival closes and latches the gate, departure reopens it.

### 3. 逐句溯源

1. 句子 1：The railway level-crossing controller uses a microcontroller and two directionally interpreted trackside sensors to manage a simple but explicit open-close gate sequence.
   对应摘录：A, B
2. 句子 2：When the foreside sensor `S1` detects an approaching train, the controller interprets the crossing as currently open, issues a close command, and drives the gate motor through its relay-driver chain until the barrier is shut.
   对应摘录：A, C
3. 句子 3：The gate then remains closed while the train occupies the crossing zone, and indicator signals alert road users that a train is approaching or passing.
   对应摘录：A, B
4. 句子 4：After the train reaches the after-side sensor `S2`, the controller reverses the motor direction and opens the gate automatically.
   对应摘录：A, B, C
5. 句子 5：In effect, the paper describes a sensor-triggered two-phase barrier supervisor: arrival closes and latches the gate, departure reopens it.
   对应摘录：A, C, D

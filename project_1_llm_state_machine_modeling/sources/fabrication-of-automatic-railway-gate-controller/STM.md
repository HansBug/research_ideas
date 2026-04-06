# Fabrication of Automatic Railway Gate Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把道口前后侧传感器、红绿灯/蜂鸣器、PIC 控制器和 H-bridge 电机开闭动作串成完整的 arrival-close / departure-open 控制链，是一条清楚的铁路道口门控双 A 样本。

## 条目 1: IR-and-Inductive Railway Gate Open-Close Controller

- 控制对象：轨道交通与铁路控制领域的 PIC 道口自动门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个铁路平交口自动门控控制器，用道口前后的 `IR + inductive` 传感器触发 `close gate -> hold with warning -> open gate` 链，并通过 H-bridge 驱动直流电机完成开闭。
- 判断：算。对象是真实道口控制系统；原文明确交代了传感器布置、车路两侧信号灯切换、蜂鸣报警、PIC 主控与电机转向逻辑，不是泛泛的装置介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 13-43 行
> This paper describes the automatic railway gate control system using PIC microcontroller ... IR sensors, inductive sensors are the input components while buzzer, light indicator, DC motor and LCD display are the output components ... The first inductive sensor and IR sensor are fixed at a certain distance from the gate and the second sensors are fixed at the same certain distance after the gate. The gate is closed, when the train crosses the first IR sensor and the gate is opened, when the train crosses the second IR sensor.

#### 摘录 B

- 出处：第 1 页，Introduction，`paper_content.txt` 第 50-68 行
> This system is to manage the control system of railway gate using the microcontroller ... As a train approaches the railway crossing from either side, the sensors placed at a certain distance from the gate detects the approaching train and controls the operation of the gate. This signal is used to trigger the microcontroller for operating the gate motor, alarm system and light indicators.

#### 摘录 C

- 出处：第 2 页，Circuit Description，`paper_content.txt` 第 131-157 行
> The gate control system consists of two infrared sensors and two inductive sensors. The sensors are fixed at the certain distance on both sides of the gate ...
>
> When the inductive sensor1 senses the train, IR sensors are on state. Then IR sensor1 senses the train, microcontroller can control the drive of the gate control motor.
>
> The light signal of the car traffic is changed from Green color to Red color and the train traffic is changed from Red color to Green color. A buzzer gets activated when the train is crossing the gate and the railway gate is closed.
>
> When the train passes through the IR sensor2 ... the railway gate is opened ... train passes through the inductive sensor2. In this time, IR sensors are off state.

#### 摘录 D

- 出处：第 2 页，Working，`paper_content.txt` 第 161-169 行
> When the transistors Q1 and Q4 are closed, the motor rotates in one direction for closing the railway gate. When the transistors Q2 and Q3 are closed, the motor rotates in opposite direction for opening the railway gate. When all the transistors are opened, the motor is stopped.

### 2. 基于原文整理后的自然语言描述

The paper describes a PIC-based railway level-crossing controller that uses directional sensor events to supervise barrier closure and reopening. Two inductive sensors and two IR sensors are placed before and after the gate so that the controller can detect train arrival and train departure from both sides of the crossing. When the first-side sensing chain detects an approaching train, the PIC controller drives the gate motor into the closing direction, turns road traffic from green to red, turns train traffic from red to green, and activates the buzzer while the barrier is down. Once the train reaches the second IR sensor after crossing the gate, the controller reverses the motor direction, reopens the gate, and restores the road/train light indications; after the train passes the second inductive sensor, the IR sensing chain returns to the off state. At the actuator layer, the H-bridge implementation is explicit: `Q1/Q4` close the gate, `Q2/Q3` open it, and opening all transistors stops the motor.

### 3. 逐句溯源

1. 句子 1：The paper describes a PIC-based railway level-crossing controller that uses directional sensor events to supervise barrier closure and reopening.
   对应摘录：A, B
2. 句子 2：Two inductive sensors and two IR sensors are placed before and after the gate so that the controller can detect train arrival and train departure from both sides of the crossing.
   对应摘录：A, C
3. 句子 3：When the first-side sensing chain detects an approaching train, the PIC controller drives the gate motor into the closing direction, turns road traffic from green to red, turns train traffic from red to green, and activates the buzzer while the barrier is down.
   对应摘录：B, C
4. 句子 4：Once the train reaches the second IR sensor after crossing the gate, the controller reverses the motor direction, reopens the gate, and restores the road/train light indications; after the train passes the second inductive sensor, the IR sensing chain returns to the off state.
   对应摘录：A, C
5. 句子 5：At the actuator layer, the H-bridge implementation is explicit: `Q1/Q4` close the gate, `Q2/Q3` open it, and opening all transistors stops the motor.
   对应摘录：D

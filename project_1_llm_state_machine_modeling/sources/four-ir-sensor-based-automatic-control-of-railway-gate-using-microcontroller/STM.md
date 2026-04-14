# Four IR Sensor Based Automatic Control of Railway Gate using Microcontroller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双向列车检测、常开绿灯、来车红灯/蜂鸣/关闸、离开后开闸和 `1 s` 舵机动作延迟写成了完整的铁路道口门控链，适合形成双 A 的 `EFSM + T1` 样本。

## 条目 1: Four-IR Bidirectional Railway Gate Controller

- 控制对象：轨道交通与铁路控制领域的双向铁路道口门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 `Arduino UNO` 道口门控器，用四个红外传感器区分左右两个来车方向，并用红/绿 LED、蜂鸣器和两个舵机执行关闸、开闸、报警与恢复。
- 判断：算。对象是真实铁路道口控制系统；原文直接给出传感器-动作映射、左右方向对称逻辑、常态输出、舵机角度和 `delay(1000)`，可稳定整理成带局部定时的 EFSM。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 36-59 行
> This paper investigates based on four IR sensor automatic control of railway gate using a microcontroller system ... The operation using Arduino UNO that integrated with other circuits involved such as power supply, IR sensors, light indicators, buzzer, and gate motors. The servo motor is used to control the open and close status of the railway crossing gate. The four IR sensors are placed on the railway tracks. The gate is closed when the first one senses the train and is opened when the second one senses the train ... When the train is coming from the right side, the third and fourth sensors is performed in the same operation. The red LED is HIGH when the gate is closed and the green LED is HIGH when the gate is opened.

#### 摘录 B

- 出处：第 1-2 页，`II. System Block Diagram` 与 flowchart，`paper_content.txt` 第 82-99、109-125 行
> The system for this paper is constructed with the IR sensor for the input section and servo motor for the railway gate ... When the train crosses the first sensor, the red LED and buzzer are ON and the gate is closed. And then, that crosses the second sensor, the green LED is ON and the gate is opened ... The third and fourth sensors are performed in the same operation when the train is coming from the right sight.
>
> Step 2 : Initialize the two servo motors are 90º ... Step 4 : Initialize green LEDs ... HIGH ... If 1st and 3rd IR sensors are LOW, red LEDs are HIGH and green LEDs are LOW ... Buzzer is ON and the two servo motors are 0º ... If 2nd and 4th IR sensors are LOW, green LEDs are HIGH and red LEDs are LOW ... Buzzer is OFF and the two servo motors are 90º.

#### 摘录 C

- 出处：第 2-3 页，Software Implementation，`paper_content.txt` 第 177-187、207-254 行
> The loop function for the servo motor includes reading the input pin and triggering the output by using myservo.write ... And the delay time is one second ... myservo.write (0); ... delay (1000); myservo.write (90); ... delay (1000)
>
> The loop function for the first sensor is LOW and the second sensor is HIGH ... red LEDs ... are HIGH ... buzzer ... is HIGH and the gate is closed ... When the fourth sensor has sensed the train ... green LEDs ... are HIGH and the red is LOW. And buzzer is also LOW, the gate is opened again ... When no train is coming, all the four IR sensors are HIGH ... green LEDs are HIGH ... red LEDs are LOW ... buzzer is also LOW and the gate is opened.

#### 摘录 D

- 出处：第 3-4 页，Hardware Implementation 与 Results，`paper_content.txt` 第 273-295、318-354 行
> When the train is coming from the left side of the gate, the first sensor senses this train ... After one second, the servo motors change 90º that means the gate is closed and the buzzer is HIGH ... the train is crossing in front of the second sensor again ... green LEDs ... are HIGH and the servo motors change 0º again that means the gate is opened. When the train is coming from the right side of the gate, the third and fourth sensors are performed the same operation as the first and second ones.
>
> If the train is coming from the left side of the gate ... first sensor ... red LEDs, the buzzer is HIGH and the servo motor is 90º ... second sensor ... green LEDs, the buzzer in LOW and the servo motor is 0º ... If the nothing train is coming ... green LEDs are HIGH and the red LEDs are LOW ... the buzzer is LOW and the servo motor is 0º ...

### 2. 基于原文整理后的自然语言描述

The railway-gate controller is an Arduino-based EFSM whose normal-open condition is represented by all four IR sensors `HIGH`, green LEDs `HIGH`, red LEDs `LOW`, buzzer `LOW`, and both gate servos commanded to the open angle. For a train approaching from the left, the first IR sensor becoming active drives the warning/closure branch: the road-side red LEDs turn on, the buzzer is set `HIGH`, and after the one-second servo-delay pattern the two servo motors move to the gate-closed angle. When the same train reaches the second IR sensor, the controller opens the crossing again by turning green LEDs on, turning red LEDs and buzzer off, and writing the open angle to the two servos. For a train approaching from the right, the third sensor executes the same close-and-warn branch as the first sensor, and the fourth sensor executes the same open-and-clear branch as the second sensor.

### 3. 逐句溯源

1. 句子 1：The railway-gate controller is an Arduino-based EFSM whose normal-open condition is represented by all four IR sensors `HIGH`, green LEDs `HIGH`, red LEDs `LOW`, buzzer `LOW`, and both gate servos commanded to the open angle.
   对应摘录：A, B, C, D
2. 句子 2：For a train approaching from the left, the first IR sensor becoming active drives the warning/closure branch: the road-side red LEDs turn on, the buzzer is set `HIGH`, and after the one-second servo-delay pattern the two servo motors move to the gate-closed angle.
   对应摘录：A, B, C, D
3. 句子 3：When the same train reaches the second IR sensor, the controller opens the crossing again by turning green LEDs on, turning red LEDs and buzzer off, and writing the open angle to the two servos.
   对应摘录：A, B, C, D
4. 句子 4：For a train approaching from the right, the third sensor executes the same close-and-warn branch as the first sensor, and the fourth sensor executes the same open-and-clear branch as the second sensor.
   对应摘录：A, B, C, D

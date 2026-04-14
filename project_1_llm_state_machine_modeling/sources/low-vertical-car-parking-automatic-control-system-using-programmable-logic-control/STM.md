# Low Vertical Car Parking Automatic Control System Using Programmable Logic Control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把六槽位立体停车原型的按钮设定值、encoder 位置反馈、PLC 输出到 relay/inverter 的执行链写得比较集中，足够抽成停车位 setpoint 控制样本。

## 条目 1: Six-slot vertical parking setpoint controller

- 控制对象：六槽位立体停车原型的槽位定位与呼叫控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个立体停车平台控制器，用按钮给出目标槽位、用 rotary encoder 给出当前位置，再由 PLC 驱动电机把平台转到目标车位。
- 判断：算。对象是实际停车设备的定位控制链，原文明确写出了六个垂直车位、button/encoder 输入、relay/inverter 输出以及“按 set point 旋转到目标槽位”的闭环。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract / Introduction，`paper_content.txt` 第 9-16, 57-63 行
> A vertical car parking automatic control system using PLC is a prototype system ... with a maximum capacity of six cars which will be parked vertically. The vertical car parking automatic control system will use a Mitsubishi FX3G PLC. ... a rotary encoder ... will send pulse signal to PLC which will process the signal and measure a swivel angle. ... The results show that the fastest time period for the system to reach the set point is 4 seconds while the longest is 8 seconds ...
>
> ... the goal of this research is to be able to move the car's position in or out with a button press command.

#### 摘录 B

- 出处：第 2 页，`2. Method`，`paper_content.txt` 第 105-130 行
> PLC device ... functions as the center for automatic control of the vertical car parking system. ... The input function in the form of a button and rotary encoder is a command to be processed on the CPU. The output function is the result of the input response that has been processed on the CPU in the form of a voltage signal that is sent to the relay then gives an order to the inverter to drive the induction motor.
>
> ... The incremental type rotary encoder device functions as a position sensor ... useful for controlling and determining the angle of rotation of the induction motor. The pulse signal is connected to a PLC which can calculate so that the motor rotation angle can be determined so that the slot position and motor rotation can be adjusted.

#### 摘录 C

- 出处：第 3-5 页，`3. Result and Discussion / 4. Conclusion`，`paper_content.txt` 第 179-208, 305-323 行
> ... testing of the electronic system is carried out by testing the accuracy of the command of the tool with the actual carried out by the system. This test wants to show that the rotary encoder device has a function to read the position of the motor rotation angle and can be controlled by the PLC.
>
> ... the control system is tested to achieve the desired set point. There are 5 experiments carried out with a set point in the form of a button that is pressed according to the number labeling on the available car slot on a miniature vertical car park device.
>
> ... the vertical car park prototype can accommodate 6 cars consisting of 6 maximum capacity slots. Time required by the automatic prototype vertical car parking system is the fastest is 4 seconds and the longest is 8 seconds ... The fastest time to call a miniature car in a vertical car parking prototype is 4 seconds and the longest is 8 seconds with an average time of 5.6 seconds.

### 2. 基于原文整理后的自然语言描述

The controller operates a six-slot vertical parking prototype in which the parking platform is moved to a requested slot by a `Mitsubishi FX3G PLC`. The control input is a combination of a pressed slot-selection button and the pulse stream from an incremental rotary encoder, which the PLC uses to measure the swivel angle and thereby infer the platform's current slot position. After processing that button-plus-position input on the CPU, the PLC emits a voltage signal to a relay, the relay commands the inverter, and the inverter drives the induction motor so the platform rotates toward the requested set point. In control terms, the parking device behaves like an EFSM with a current-slot variable, a target-slot command, a motion phase while the platform is rotating, and a stop phase once the encoder feedback shows that the desired slot has been reached. The paper repeatedly tests this setpoint-tracking behavior and reports nominal calling times of roughly `4` to `8 s`, with an average around `5.6 s`, for moving the prototype to the requested slot.

### 3. 逐句溯源

1. 句子 1：The controller operates a six-slot vertical parking prototype in which the parking platform is moved to a requested slot by a `Mitsubishi FX3G PLC`.
   对应摘录：A
2. 句子 2：The control input is a combination of a pressed slot-selection button and the pulse stream from an incremental rotary encoder, which the PLC uses to measure the swivel angle and thereby infer the platform's current slot position.
   对应摘录：A, B
3. 句子 3：After processing that button-plus-position input on the CPU, the PLC emits a voltage signal to a relay, the relay commands the inverter, and the inverter drives the induction motor so the platform rotates toward the requested set point.
   对应摘录：B
4. 句子 4：In control terms, the parking device behaves like an EFSM with a current-slot variable, a target-slot command, a motion phase while the platform is rotating, and a stop phase once the encoder feedback shows that the desired slot has been reached.
   对应摘录：A, B, C
5. 句子 5：The paper repeatedly tests this setpoint-tracking behavior and reports nominal calling times of roughly `4` to `8 s`, with an average around `5.6 s`, for moving the prototype to the requested slot.
   对应摘录：A, C

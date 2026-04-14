# Automation of Railway Gate Control Using Microcontroller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路平交道口的 arrival-sense / close-gate / hold-closed / departure-sense / reopen 链条写得完整，适合作为简洁但可追踪的 `FSM + T0` 样本。

## 条目 1: Two-Sensor Railway Gate Open-Close Controller
- 控制对象：铁路平交道口自动栏杆控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向无人值守铁路平交口的自动门控控制器，利用来车侧与离车侧两组磁传感器驱动关门、保持关闭和重新开门。
- 判断：算。对象是明确的铁路道口控制系统，原文同时给出了 arrival sensor、departure sensor、1SW/2SW 位置反馈、算法步骤和过程图。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract
> We call the sensor along the train direction as ‘foreside sensor’ and the other as ‘after side sensor’. When foreside sensor gets activated, the sensed signal is sent to the microcontroller and the gate motor is turned on in one direction by relay driver and the gate is closed and stays closed until the train crosses the gate and reaches after side sensors. When after side sensor gets activated and the signal about the departure is sent to the microcontroller, motor turns in opposite direction and gate opens and motor stops.

#### 摘录 B
- 出处：第 5-6 页，Circuit Description / Algorithm
> The operation is that when the railway crossing is open then `1SW` is closed and `2SW` is opened. But when railway crossing is closed then `1SW` is opened and `2SW` is closed. By this process the microcontroller decides the opening and closing of railway crossing.
>
> 4. Check the arrival of the train in either direction by the sensors ... 5. Close the gate. 6. Change the signal for train. 7. Check the train departure by the sensors ... 8. Open the gate.

#### 摘录 C
- 出处：第 7 页，Methodology
> When a train crosses the first sensor that is `1S`, sensor `1S` start incrementing to the microcontroller and microcontroller decides to close the railway crossing ... The same process is repeated after crossing of the `2S` sensor. This `2S` sensor senses and gives an increment to microcontroller and the microcontroller opens the crossing because previously microcontroller got the instruction that the railway crossing is closed by `2SW`.

### 2. 基于原文整理后的自然语言描述

The railway level-crossing controller starts from the open-gate condition and monitors two train-direction sensors placed before and after the crossing. When the arrival-side sensor is triggered, the microcontroller commands the gate motor through relay drivers to close the barrier, and the crossing remains closed while the train occupies the protected region between the two sensors. Gate-position switches `1SW` and `2SW` report whether the barrier is currently open or closed and are used by the controller to validate the motor command. Once the departure-side sensor is triggered, the controller reverses the motor direction, reopens the gate, and stops the motor after the open position is reached. The same logic is expressed both as a short algorithm and as a process chart, making the control chain directly usable as a compact railway-gate FSM sample.

### 3. 逐句溯源

1. 句子 1：The railway level-crossing controller starts from the open-gate condition and monitors two train-direction sensors placed before and after the crossing.
   对应摘录：A, B
2. 句子 2：When the arrival-side sensor is triggered, the microcontroller commands the gate motor through relay drivers to close the barrier, and the crossing remains closed while the train occupies the protected region between the two sensors.
   对应摘录：A, B, C
3. 句子 3：Gate-position switches `1SW` and `2SW` report whether the barrier is currently open or closed and are used by the controller to validate the motor command.
   对应摘录：B
4. 句子 4：Once the departure-side sensor is triggered, the controller reverses the motor direction, reopens the gate, and stops the motor after the open position is reached.
   对应摘录：A, B, C
5. 句子 5：The same logic is expressed both as a short algorithm and as a process chart, making the control chain directly usable as a compact railway-gate FSM sample.
   对应摘录：B, C

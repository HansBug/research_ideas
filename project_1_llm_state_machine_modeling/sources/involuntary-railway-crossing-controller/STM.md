# Involuntary Railway Crossing Controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双红外检测、栏杆闭合/开启、电机方向控制和异常报警写成了一条简洁但完整的道口门控控制链。

## 条目 1: Two-Sensor Railway Gate Close-Open Controller
- 控制对象：轨道交通与铁路控制领域的双红外道口栏杆门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个铁路平交口栏杆控制器，用于根据列车接近与离开信号驱动栏杆关闭或重新开启，并在异常时触发报警。
- 判断：算。对象是实际铁路道口门控系统，原文明确给出了到达检测、离开检测、栅栏电机方向控制和异常报警逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Working of Involuntary Railway Crossing Controller & Results，`paper_content.txt` 第 67-85 行
> In this project an ATMEGA328 microcontroller is associated with two infra-red transmitters and two pair of receivers. First pair is fixed at the position from where the train arrives and second pair is placed below the train direction. When train is near 1 km of railway crossing then the first sensor will get activated and send signal to microcontroller for closing the gate of railway crossing. When the train crosses the gate than after the distance of 1 km the second sensor gets activated and sends the command to microcontroller for reopening the gate of railway crossing. The alarm system is also installed and actuated if there are mis happening and alert the driver of the train to stop immediately.

#### 摘录 B
- 出处：第 1-3 页，Block diagram / H-Bridge / Hardware unit，`paper_content.txt` 第 90-98、127-147、175-179、202-212 行
> The two sensors i.e. sensor 1 and sensor 2 also known as upside and downside sensors are connected to microcontroller for sending the signal of train arrival and departure. After the processing of microcontroller, two motor controllers also known as H bridge controller circuit is connected to a dc motor for moving the motor at a particular direction.
>
> Fig.4(a) shows ... Q1 and Q4 is turn ON and the motor ... spin in forward direction. Fig.4(b) ... Q2 and Q3 are in ON position ... the motor ... spin in backward direction.
>
> When IR sensors detect any object, it sends signal to the microcontroller. The microcontroller after processing gives instructions to H bridge controller to control the motion of dc geared motor.
>
> The hardware unit comprises of two IR sensors ... first IR sensor ... detect the arrival of train ... gives instruction to motor to close the gate ... The second sensor is placed 1km away ... the microcontroller orders the H bridge to control the motor and open the gates.

### 2. 基于原文整理后的自然语言描述

The railway crossing controller connects two infrared sensor pairs to an ATMEGA328 microcontroller so that one pair detects train approach before the crossing and the other detects train departure after the crossing. When the first sensor is activated near one kilometre before the crossing, the controller commands the gate motor to close the barrier, and when the second sensor is activated after the train passes, the controller commands the barrier to reopen. The gate motor direction is implemented through an H-bridge: one switching pattern drives the motor forward and the other drives it backward. If a mis-happening occurs, the alarm system is actuated to warn the driver, and the controller also provides a reset path for restarting the crossing unit after malfunction handling.

### 3. 逐句溯源

1. 句子 1：The railway crossing controller connects two infrared sensor pairs to an ATMEGA328 microcontroller so that one pair detects train approach before the crossing and the other detects train departure after the crossing.
   对应摘录：A, B
2. 句子 2：When the first sensor is activated near one kilometre before the crossing, the controller commands the gate motor to close the barrier, and when the second sensor is activated after the train passes, the controller commands the barrier to reopen.
   对应摘录：A, B
3. 句子 3：The gate motor direction is implemented through an H-bridge: one switching pattern drives the motor forward and the other drives it backward.
   对应摘录：B
4. 句子 4：If a mis-happening occurs, the alarm system is actuated to warn the driver, and the controller also provides a reset path for restarting the crossing unit after malfunction handling.
   对应摘录：A, B

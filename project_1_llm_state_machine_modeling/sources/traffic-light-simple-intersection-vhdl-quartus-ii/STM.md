# Implementation of Traffic Light Controlling System for a Simple Intersection with VHDL using Quartus II - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `S0-S3` 四态相位链、侧路传感器触发条件以及 `10 s / 3 s / 10 s / 3 s` 的切换时序，适合直接整理为简单路口控制 FSM。

## 条目 1: Four-State Sensor-Triggered Intersection Signal FSM

- 控制对象：主路/侧路简单路口的交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的简单路口 FSM，用侧路车辆传感器和 `S0-S3` 四个相位状态组织主路/侧路的红黄绿切换。
- 判断：算。对象是实际交通灯控制器，原文直接定义了状态 `S0-S3`、每个状态下两条道路的灯色、传感器触发条件以及黄灯/绿灯持续时间。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 34-45 行
> A simple intersection on the road is considered for the simulation of traffic signaling system. VHDL code was written in Quartus II to implement traffic light system for specific intersections on the road. The vehicles are always moving on the main road, meaning green light is always ‘1’ until there are vehicles approaching the side road. When the vehicles arrive on the side road which is sensed by sensor, then the traffic controller takes the initiative to schedule the traffic light, from green to red light in the main road and red to green light in the side road.

#### 摘录 B

- 出处：第 4-5 页，`IV. Implementation Methodology`，`paper_content.txt` 第 287-297 行、第 308-340 行
> ... there are four states of traffic lighting are defined, which are S0, S1, S2, and S3. The states, their lighting conditions, and state flow are shown in Figure 3.
>
> At start, the green light is ‘1’ (on) in the main road (R1) and the red light is ‘1’ (on) in the side road (R2), which is called state S0.
>
> When the sensor placed in the side road (R2) sense vehicle on the side road, the traffic controller warns the vehicles on the main road (R1) by turning on the yellow light. This state is called state S1. Just after 3 seconds, the green light become on in the side road (R2), which is called state S2.
>
> When there are no vehicles in the side road, the traffic controller transfer to state S0 through S3.

#### 摘录 C

- 出处：第 5-6 页，时序与仿真说明，`paper_content.txt` 第 347-356 行、第 394-413 行
> The initial state is R1G_R2R means green on in main road and red on in the side road. The source and destination state are remains same if the sensor have no data. The controller takes 10 seconds when transfer from green to yellow. Yellow to red takes 3 seconds.
>
> ... Whenever the sensor in the side road (R2) sense the presence of the vehicle ... After 3 second delay, the red and green light turn ‘high’ in the main road (R1) and side road (R2), respectively. ... The green light becomes ‘high’ for 10 second in the side road and after defined time it becomes yellow for 3 second before red light being ‘high’.
>
> When the sensor data is low (no vehicles in the side road), the green light becomes ‘high’ in the main road after specified time.

### 2. 基于原文整理后的自然语言描述

The controller models a simple intersection with a main road and a side road, and its default state `S0` keeps the main road green while the side road remains red. When the side-road sensor detects a waiting vehicle, the controller moves to `S1` to warn the main road with yellow, then after `3` seconds switches to `S2` so the main road is red and the side road is green. The side-road green interval is maintained for about `10` seconds, after which the controller enters `S3` to show side-road yellow before returning to `S0`. If the side-road sensor has no vehicle data, the source and destination state remain unchanged and the controller stays in the current main-road-priority configuration.

### 3. 逐句溯源

1. 句子 1：The controller models a simple intersection with a main road and a side road, and its default state `S0` keeps the main road green while the side road remains red.
   对应摘录：A, B, C
2. 句子 2：When the side-road sensor detects a waiting vehicle, the controller moves to `S1` to warn the main road with yellow, then after `3` seconds switches to `S2` so the main road is red and the side road is green.
   对应摘录：A, B, C
3. 句子 3：The side-road green interval is maintained for about `10` seconds, after which the controller enters `S3` to show side-road yellow before returning to `S0`.
   对应摘录：B, C
4. 句子 4：If the side-road sensor has no vehicle data, the source and destination state remain unchanged and the controller stays in the current main-road-priority configuration.
   对应摘录：C

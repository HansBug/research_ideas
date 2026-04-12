# Development of Traffic Light Control System Using Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出四路口交通灯模型、每车道双限位开关输入、红黄绿输出、基于先到车辆的车道选择，以及 `10s/20s/2s/2s` 的相位保持与安全切换规则，能形成高细节 EFSM 样本。

## 条目 1: Sensor-priority four-way traffic-light controller with adaptive green hold

- 控制对象：道路交通信号控制领域的四路口双传感优先交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个由 Omron PLC 控制的四向路口交通灯，每个车道用两个限位开关识别车辆存在和队列体量，并按传感器触发优先级动态分配绿灯。
- 判断：算。原文提供了输入、输出、车道切换逻辑和具体秒级相位时间，能支撑 `guard + timer + output` 形式的状态机描述。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> The hardware part for this project is a model of four way junction of a traffic light. Each lane has two limits switch (input) function as a sensor. Three indicator lamps with different colours (Red, Yellow and Green) are installed at each lane for represents as traffic light signal.

#### 摘录 B

- 出处：第 28 页，交通灯模型硬件说明
> Each lane also has two limit switches represent as a sensor on the road. The first sensor placed in front of lane to detect the presence car at the junction and the second sensor placed at certain length from first sensor to determine the volume of the car at that lane.

#### 摘录 C

- 出处：第 36 页，Figure 3.2 Traffic phase flowchart
> This traffic light system is working independently to change from one lane to the other lane based on which lane can activate sensor 1 fast. This traffic light system give the priority to the lane which have a car and followed by the other.

#### 摘录 D

- 出处：第 37 页，Figure 3.4 Program flowchart
> A red signal will turn to green signal if a sensor 1 is activated. If the sensor 2 is activated before a red signal turn to a green signal, a green signal will hold for a 20s and if not a green signal only hold for a 10s. A green signal will hold the that time or extend more than time if sensor 1 from other lanes are not activated. When the sensor 1 from the other lanes activate, a green signal will turn into a yellow signal for 2s and then back to red signal. For safety, the other lanes will change to a green signal after 2s.

#### 摘录 E

- 出处：第 43 页，Table 4.4 New traffic light control system phase and lane duration
> This type of traffic light system is freely changing the lane to the other lane based on the priority if any of 1st vehicles presence at traffic light junction. This traffic light system not depends on lane rotation and effective and reduces time and energy.

### 2. 基于原文整理后的自然语言描述

The four-way traffic-light PLC starts with every lane held red except the currently selected lane. For each lane, sensor 1 detects whether a vehicle is waiting at the stop line, and sensor 2, placed farther from the junction, indicates whether that lane has higher traffic volume. When a red lane activates sensor 1 before the others, the controller selects that lane and turns its signal green. If sensor 2 has also been activated before the lane turns green, the green state is held for `20` seconds; otherwise it is held for `10` seconds. If no other lane has activated sensor 1 when the green timer expires, the current lane can continue holding green. When another lane requests service, the current lane changes to yellow for `2` seconds, returns to red, waits an additional `2` seconds for safety, and then grants green to the next prioritized lane.

### 3. 逐句溯源

1. 句子 1：The four-way traffic-light PLC starts with every lane held red except the currently selected lane.
   对应摘录：A, D
2. 句子 2：For each lane, sensor 1 detects whether a vehicle is waiting at the stop line, and sensor 2, placed farther from the junction, indicates whether that lane has higher traffic volume.
   对应摘录：B
3. 句子 3：When a red lane activates sensor 1 before the others, the controller selects that lane and turns its signal green.
   对应摘录：C, D, E
4. 句子 4：If sensor 2 has also been activated before the lane turns green, the green state is held for `20` seconds; otherwise it is held for `10` seconds.
   对应摘录：D
5. 句子 5：If no other lane has activated sensor 1 when the green timer expires, the current lane can continue holding green.
   对应摘录：D
6. 句子 6：When another lane requests service, the current lane changes to yellow for `2` seconds, returns to red, waits an additional `2` seconds for safety, and then grants green to the next prioritized lane.
   对应摘录：D

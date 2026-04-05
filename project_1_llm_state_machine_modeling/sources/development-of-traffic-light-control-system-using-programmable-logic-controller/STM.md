# Development of a Traffic Light Control System Using Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了四向路口的车道优先切换逻辑，并明确补足了 `10 s / 20 s` 绿灯保持和 `2 s` 黄灯过渡。

## 条目 1: Sensor-Priority Adaptive Lane Phase

- 控制对象：道路交通信号领域的四向路口 PLC 车道优先控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个四向交通灯控制器，用于根据车道传感器的到达先后与车流体量，动态分配绿灯持续时间并在车道间切换相位。
- 判断：算。对象是实际交通信号控制系统，原文明确给出了车道传感器布置、优先切换条件以及绿灯、黄灯、红灯的时间规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 28-29 页，`2.4 Traffic light hardware / 2.5 Hardware wiring diagram`
> Each lane also has two limit switches represent as a sensor on the road. The first sensor placed in front of lane to detect the presence car at the junction and the second sensor placed at certain length from first sensor to determine the volume of the car at that lane. From this combination of sensor, we will know the expected time for green signal when each lane change to the green signal.

#### 摘录 B

- 出处：第 35-37 页，`3.3 Program development`
> A flowchart in figure 3.2 shows about how the lane changes to the other lane for a green signal. This traffic light system is working independently to change from one lane to the other lane based on which lane can activate sensor 1 fast. This traffic light system give the priority to the lane which have a car and followed by the other ... A red signal will turn to green signal if a sensor 1 is activated. If the sensor 2 is activated before a red signal turn to a green signal, a green signal will hold for a 20s and if not a green signal only hold for a 10s ... When the sensor 1 from the other lanes activate, a green signal will turn into a yellow signal for 2s and then back to red signal. For safety, the other lanes will change to a green signal after 2s.

#### 摘录 C

- 出处：第 42-44 页，`4.3 Traffic light control system analysis / 4.4 Simulation in the real world`
> Since in the beginning, this project objective is to develop a new traffic light control system and reduce traffic congestion at the junction ... this project development a traffic light control system ... is freely changing the lane to the other lane based on the priority if any of 1st vehicles presence at traffic light junction ... The average volume of traffic at junction must be verified because from this data we know where sensor 2 will place at that lane ... The other criterion is time for a green signal on when only sensor 1 activates or sensor 2 also activate ... 50M: 10s, 20s.

### 2. 基于原文整理后的自然语言描述

Each approach lane is monitored by two sensors: `sensor 1` detects the first waiting vehicle at the stop line, and `sensor 2` is placed farther upstream to estimate whether the queue volume is larger. The controller grants priority to the lane whose `sensor 1` is activated first, so the phase order is no longer a fixed round-robin cycle but a demand-driven lane selection process. Once a lane is selected, the signal turns from red to green, and the green interval is held for ten seconds if only `sensor 1` was active or for twenty seconds if `sensor 2` had also been activated before the lane received green. When another lane requests service, the current green phase changes to yellow for two seconds, then to red, and only after this two-second safety gap does the next lane become green.

### 3. 逐句溯源

1. 句子 1：Each approach lane is monitored by two sensors: `sensor 1` detects the first waiting vehicle at the stop line, and `sensor 2` is placed farther upstream to estimate whether the queue volume is larger.
   对应摘录：A
2. 句子 2：The controller grants priority to the lane whose `sensor 1` is activated first, so the phase order is no longer a fixed round-robin cycle but a demand-driven lane selection process.
   对应摘录：B, C
3. 句子 3：Once a lane is selected, the signal turns from red to green, and the green interval is held for ten seconds if only `sensor 1` was active or for twenty seconds if `sensor 2` had also been activated before the lane received green.
   对应摘录：B, C
4. 句子 4：When another lane requests service, the current green phase changes to yellow for two seconds, then to red, and only after this two-second safety gap does the next lane become green.
   对应摘录：B

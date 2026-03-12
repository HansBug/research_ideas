# Smart Traffic Control System Using PLC And Scada - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：正文明确给出了密度优先与按当前交通状况切换红黄绿的控制意图，但具体状态时序较分散。

## 条目 1: Density-Driven Priority Signal Control
- 控制对象：四岔路口交通灯优先控制器

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的 PLC 路口控制器，用于根据各车道车流密度动态调整红黄绿灯的优先级和持续时间。
- 判断：算。对象是实际交通灯控制系统，原文给出了车道密度、优先级和信号灯切换依据，但更多细节留在实现与示意图中。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 13-22 行
> Smart traffic control system is a modern engineering technology, which is intended to measure traffic density by counting the number of vehicles in each lane. In this system PLC takes a data from sensors and checks the priorities. ... To calculate the vehicle densities in a lane at a 4-way lane cross and then give the priority automatically using a program. The lights [green, yellow, red] ON & OFF time is depend on the specific priorities which can be decided by logic program.

#### 摘录 B
- 出处：第 7 页，Conclusion，`paper_content.txt` 第 496-513 行
> The designed and implementation of this technique is directly targeted for traffic management ... These intelligent systems provide a way for the lights to change from red to green based on current traffic conditions. The sensors are interfaced with Delta PLC Module. This interface is synchronized with the whole process of the traffic system.

### 2. 基于原文整理后的自然语言描述

The smart traffic controller counts vehicles in each lane and sends the sensor data to the PLC for priority evaluation. The PLC logic assigns priorities automatically for a four-way intersection and adjusts the ON/OFF times of the green, yellow, and red lights according to the detected lane densities. Signal changes from red to green are therefore synchronized with current traffic conditions rather than being fixed in advance.

### 3. 逐句溯源

1. 句子 1：The smart traffic controller counts vehicles in each lane and sends the sensor data to the PLC for priority evaluation.
   对应摘录：A
2. 句子 2：The PLC logic assigns priorities automatically for a four-way intersection and adjusts the ON/OFF times of the green, yellow, and red lights according to the detected lane densities.
   对应摘录：A
3. 句子 3：Signal changes from red to green are therefore synchronized with current traffic conditions rather than being fixed in advance.
   对应摘录：B

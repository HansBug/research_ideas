# Smart Traffic Control System Using PLC And Scada - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：正文明确给出了密度优先与按当前交通状况切换红黄绿的控制意图，但具体状态时序较分散。

## 条目 1: Density-Driven Priority Signal Control
- 控制对象：四岔路口交通灯优先控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟠 C（只有主链）
- 描述细节充实度：🟠 C（只有主链）
- 数据集角色：🧰 清洗后保留
- 趋同标签：✨ 未见强趋同

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

The smart traffic controller counts vehicles in each lane and sends the sensor data to the PLC for priority evaluation at a four-way intersection. The PLC program uses timer instructions together with the detected lane priorities to change the ON/OFF times of the green, yellow, and red lights. In this way, signal changes from red to green are synchronized with current traffic conditions instead of remaining fixed in advance, and the SCADA layer is used to monitor and supervise the same process.

### 3. 逐句溯源

1. 句子 1：The smart traffic controller counts vehicles in each lane and sends the sensor data to the PLC for priority evaluation at a four-way intersection.
   对应摘录：A
2. 句子 2：The PLC program uses timer instructions together with the detected lane priorities to change the ON/OFF times of the green, yellow, and red lights.
   对应摘录：A, B
3. 句子 3：In this way, signal changes from red to green are synchronized with current traffic conditions instead of remaining fixed in advance, and the SCADA layer is used to monitor and supervise the same process.
   对应摘录：B

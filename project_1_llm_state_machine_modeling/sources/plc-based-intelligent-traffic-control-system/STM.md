# PLC Based Intelligent Traffic Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接说明了四种运行模式、传感器优先级判断、相位顺序与中断/定时两类触发条件，可作为交通灯控制样本。

## 条目 1: Priority-Based Signal Phasing with Sensor Interrupts
- 控制对象：PLC 智能交通信号控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的智能交通灯控制器，用于根据车辆检测结果决定各方向相位优先级和放行时长。
- 判断：算。对象是实际交通灯控制系统，原文给出了传感器检测、优先级计算和相位开放顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 11-18, 21-32 行
> The system developed is able to sense the presence or absence of vehicles within certain range by setting the appropriate duration for the traffic signals to react accordingly. By employing mathematical functions to calculate the appropriate timing for the green signal to illuminate, the system can help to solve the problem of traffic congestion.
>
> The new timing scheme that was implemented promises an improvement in the current traffic light system and this system is feasible, affordable and ready to be implemented especially during peak hours, off hours and pedestrians.
>
> The PLC checks the status of the sensors. The system resolution is depend on the output provided by the sensors, Then PLC checks the priorities and then provide output signal to the traffic lights poles for ON or OFF the Red, yellow or Green lights and ON time is depend on the specific priorities. The roads are opened in that manner that east road, west road, north road and then south road is open.

#### 摘录 B
- 出处：第 1-2 页，Section 2 Overview / 2.1 Traffic Control System / 2.4，`paper_content.txt` 第 83-100, 142-154 行
> The ability to collect the information of the busy tracks by sensors and providing the output to PLC. The ability to take decision against the information and change the time according to the priorities.
>
> The signal phases and cycle length are depend on the traffic flow on the desired track. The system responds to interrupts or timing base system and open the desired signal according to the priority requirement.
>
> The intelligent traffic control system works in four different modes are Normal flow, peak time, off time and manual operation. Peak time and off time modes are depended on the sensors outputs then change the status. Our intelligent traffic control system totally depend on the sensors output and take decisions.

#### 摘录 C
- 出处：第 2 页，Section 2.7 / 2.8，`paper_content.txt` 第 175-195 行
> Practically Inductive Loops are used as sensors to detect the presence of vehicles on intersections. Its basic function is to provide interrupts to controller unit. ... Detector unit sends an interrupt signal to controller unit.
>
> In prototype design Photo electric sensors are used ... As the basic function of induction loop in Intelligent Traffic Control System is used to provide an interrupt signal to controller unit. We use Photo electric sensors rather then induction loops. In our design, photo electric sensors provide an interrupt signal to controller unit. In case when vehicle reaches in front of sensors, then it provides an interrupt.

### 2. 基于原文整理后的自然语言描述

The intelligent traffic controller works in four modes, namely normal flow, peak time, off time, and manual operation, with peak-time and off-time behaviour changing according to the sensor outputs. In the sensor-driven modes, the PLC collects busy-track information, checks priorities, and adjusts both the signal phase or cycle length and the green ON time according to the traffic flow on the desired track. The desired signal can be opened either by an interrupt condition or by the timing-base system, and the nominal opening order described in the paper is east road, west road, north road, and then south road. In the practical system induction loops provide the interrupt signal, while the prototype replaces them with photoelectric sensors that raise the same controller interrupt when a vehicle reaches the sensing zone.

### 3. 逐句溯源

1. 句子 1：The intelligent traffic controller works in four modes, namely normal flow, peak time, off time, and manual operation, with peak-time and off-time behaviour changing according to the sensor outputs.
   对应摘录：B
2. 句子 2：In the sensor-driven modes, the PLC collects busy-track information, checks priorities, and adjusts both the signal phase or cycle length and the green ON time according to the traffic flow on the desired track.
   对应摘录：A, B
3. 句子 3：The desired signal can be opened either by an interrupt condition or by the timing-base system, and the nominal opening order described in the paper is east road, west road, north road, and then south road.
   对应摘录：A, B
4. 句子 4：In the practical system induction loops provide the interrupt signal, while the prototype replaces them with photoelectric sensors that raise the same controller interrupt when a vehicle reaches the sensing zone.
   对应摘录：C

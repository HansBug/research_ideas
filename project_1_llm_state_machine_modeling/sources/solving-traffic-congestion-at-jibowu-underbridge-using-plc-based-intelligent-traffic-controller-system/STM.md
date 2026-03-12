# Solving Traffic Congestion at Jibowu Underbridge, Lagos Using PLC-Based Intelligent Traffic Controller System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文对正常定时控制、传感器拥堵覆盖和应急车辆优先模式都有清楚描述，可直接整理为交通灯控制样本。

## 条目 1: Timed Operation with Congestion and Emergency Override
- 控制对象：城市路口 PLC 智能交通灯控制系统

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的智能路口控制器，用于在正常定时控制、拥堵优先和应急车辆优先之间切换。
- 判断：算。对象是实际交通灯控制系统，原文明确给出了定时模式、传感器覆盖条件和应急车辆处理方式。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 24-31 行
> The sensor is attached to monitor the congestion level in each lane, quickly assessing the number of vehicles in less than 2 seconds. Based on this information, a signal is sent to activate the Green light for the lane with the highest vehicle count, while signaling Red for the other lanes. ... This system effectively manages the presence of emergency vehicles by turning all signals red, except for one, when an emergency vehicle approaches.

#### 摘录 B
- 出处：第 5 页，Figure 3-6 说明，`paper_content.txt` 第 187-206 行
> Figure 3 and Figure 4 depict scenarios where the traffic control system operates based on set time intervals. ... the yellow LED on lane 2 and lane 4 blinks after a preset time, indicating that the green LED on these lanes will soon turn on ... Figure 5 showcases a situation where lane 1 and lane 3 experience heavy traffic, prompting the sensors to override the normal timing program to prioritize the flow of vehicles on these lanes. ... Figure 6 illustrates a scenario where lane 2 is congested, and the sensors override the regular timing program to facilitate the clearance of traffic on that road.

### 2. 基于原文整理后的自然语言描述

Under normal operation, the PLC traffic controller runs on preset timing intervals and blinks the yellow signal before switching the next pair of lanes to green. When the lane sensors detect heavy congestion, they override the normal timing program and prioritize the congested lane pair so that queued vehicles can be cleared first. The same controller also supports an emergency mode in which all signals turn red except the lane reserved for the approaching emergency vehicle.

### 3. 逐句溯源

1. 句子 1：Under normal operation, the PLC traffic controller runs on preset timing intervals and blinks the yellow signal before switching the next pair of lanes to green.
   对应摘录：B
2. 句子 2：When the lane sensors detect heavy congestion, they override the normal timing program and prioritize the congested lane pair so that queued vehicles can be cleared first.
   对应摘录：A, B
3. 句子 3：The same controller also supports an emergency mode in which all signals turn red except the lane reserved for the approaching emergency vehicle.
   对应摘录：A

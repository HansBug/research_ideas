# Design and Implementation of Intelligent Traffic Control System using Programmable Logic Controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对 primary/open-loop 与 secondary/closed-loop 的切换、传感器反馈和优先服务关系描述完整，适合直接入账。

## 条目 1: Primary Timing with One-Cycle Sensor Override
- 控制对象：四向环岛交通灯 PLC 控制器

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的四向路口控制器，用于在正常定时控制和基于拥堵反馈的优先控制之间切换。
- 判断：算。对象是实际交通灯控制系统，原文明确写出 primary/secondary control、传感器反馈和覆盖规则。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section 2.2/2.3，`paper_content.txt` 第 275-278 行
> From the developed logical program embedded in the microcontroller of the PLC, the four tracks of the road traffic light will function in an open-loop state. But performs a secondary control when there is dense traffic.

#### 摘录 B
- 出处：第 5 页，Section 2.3.1/2.5 Principles，`paper_content.txt` 第 342-346, 390-400 行
> The model developed for the road access is based on two control measures – open-loop control is under a normal condition where the lights are triggered to allow or stop access using a preset time while the closed-loop control energizes the system based on a monitored condition.
>
> The conventional road traffic light system works relative to the principle of an open-loop system. ... The secondary control parameter has been designed to run on the primary control so depending on the signal from the feedback system, it overrides the open-loop control and has the closed-loop control actuated for only one cycle of output.

#### 摘录 C
- 出处：第 5 页，Section 2.6 Program Testing，`paper_content.txt` 第 404-412 行
> The signal going through the output ports ... controls the road traffic light indicator on each road track. ... Output ports O:0/0 and O:0/1 will be controlled by the input port I:0/1 and the output ports O:0/2 and O:0/3 will be controlled by the input port O:0/2.

### 2. 基于原文整理后的自然语言描述

The four-road PLC controller runs in an open-loop timing state during normal traffic conditions. When the feedback sensors detect dense or stalled traffic, a secondary control overrides the primary timing and actuates closed-loop priority control for one output cycle. The controller maps sensor inputs from the monitored road tracks to specific output ports so that the congested pair receives priority service while the remaining tracks continue in their normal state.

### 3. 逐句溯源

1. 句子 1：The four-road PLC controller runs in an open-loop timing state during normal traffic conditions.
   对应摘录：A, B
2. 句子 2：When the feedback sensors detect dense or stalled traffic, a secondary control overrides the primary timing and actuates closed-loop priority control for one output cycle.
   对应摘录：B
3. 句子 3：The controller maps sensor inputs from the monitored road tracks to specific output ports so that the congested pair receives priority service while the remaining tracks continue in their normal state.
   对应摘录：C

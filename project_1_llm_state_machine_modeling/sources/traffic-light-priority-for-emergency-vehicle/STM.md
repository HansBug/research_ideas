# Traffic Light Priority for Emergency Vehicle - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接描述了应急优先模式对标准灯序的覆盖，以及基于传感器和 ambulance detection 的触发方式。

## 条目 1: Ambulance Detection Override
- 控制对象：道路交通信号领域的应急车辆优先模式控制器

### 0. 条目识别与判定
- 一句话说明：这是一个应急优先交通灯控制器，用于在检测到救护车等紧急车辆时覆盖常规灯序并切换为优先放行。
- 判断：算。对象是实际交通信号控制系统，原文明确写出了触发、覆盖标准模式和改为绿灯的机制。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Introduction, 行 40-42
> When activated, the system can override the standard traffic light pattern, allowing emergency vehicles to pass through the intersection safely and efficiently.

#### 摘录 B
- 出处：第 2 页，Conventional systems, 行 83-85
> proximity sensors on the road. This sensor gives data about the traffic on the road. According to the sensor data the traffic signals are controlled.

#### 摘录 C
- 出处：第 2 页，ML-based ambulance detection, 行 107-110
> trained deep-learning model, which will detect the presence of an ambulance on the scene. Once an ambulance is detected, the system will communicate with the traffic light controller and change the traffic light to green, allowing the ambulance to pass through the intersection quickly ...

### 2. 基于原文整理后的自然语言描述

The emergency-priority controller can override the normal traffic-light pattern when the priority mode is activated. Traffic signals are controlled from road sensor data, and a trained deep-learning model is used to detect an ambulance in the scene. Once an ambulance is detected, the system communicates with the traffic-light controller and changes the signal to green so that the vehicle can pass quickly through the intersection.

### 3. 逐句溯源

1. 句子 1：The emergency-priority controller can override the normal traffic-light pattern when the priority mode is activated.
   对应摘录：A
2. 句子 2：Traffic signals are controlled from road sensor data, and a trained deep-learning model is used to detect an ambulance in the scene.
   对应摘录：B, C
3. 句子 3：Once an ambulance is detected, the system communicates with the traffic-light controller and changes the signal to green so that the vehicle can pass quickly through the intersection.
   对应摘录：C

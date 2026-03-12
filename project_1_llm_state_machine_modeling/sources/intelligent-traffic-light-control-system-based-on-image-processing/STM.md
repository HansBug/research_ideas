# Intelligent Traffic Light Control System Based on Image Processing - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接围绕四车道密度、红黄绿时间分配和救护车检测来描述交通灯控制目标，适合整理为相位分配逻辑样本。

## 条目 1: Four-Lane Density and Ambulance Priority
- 控制对象：道路交通信号领域的图像处理交通灯控制系统

### 0. 条目识别与判定
- 一句话说明：这是一个交叉口信号控制器，用于感知四个车道的车辆密度并动态分配红、黄、绿灯时长，同时识别救护车。
- 判断：算。对象是实际交通灯控制系统，原文明确写了按车流密度改变各车道灯时以及对救护车检测的控制目的。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 30-40
> Real-time traffic control entails calculating the amount of time each lane requires to reduce traffic congestion, as well as the timing of each red, green, and yellow light. This is accomplished by sensing the density of vehicles across four lanes. ... The same amount of time on green lights wastes resources and stresses drivers, as well as for ambulance detection. The goal of this project is to regulate traffic lights using security cameras installed at intersections using image matching techniques, Python programming, Open CV, and image processing concepts.

#### 摘录 B
- 出处：第 2 页，Introduction, 行 62-67
> Pre-timed traffic lights are the most common type of traffic light ... They are pre-programmed to wait for a predetermined amount of time after every change in signal. As a result, even if the traffic density in a specific lane is the lowest, users must wait for an extended period of time for their turn to receive the green light, and when it is their turn to leave, it causes other lanes to wait even longer.

#### 摘录 C
- 出处：第 8 页，Conclusion, 行 245-246
> This project entails the creation of an efficient traffic signal controller that detects the presence of vehicles on the road and estimates traffic density. With this method, we can better identify the ambulance in traffic.

### 2. 基于原文整理后的自然语言描述

The controller senses vehicle density across four lanes and computes the red, green, and yellow timing required by each lane instead of using a fixed pre-timed cycle. Low-density lanes should not hold green time unnecessarily while other approaches continue waiting. The same vision-based controller also detects ambulances in traffic so that emergency movement can be identified within the signal control process.

### 3. 逐句溯源

1. 句子 1：The controller senses vehicle density across four lanes and computes the red, green, and yellow timing required by each lane instead of using a fixed pre-timed cycle.
   对应摘录：A, B
2. 句子 2：Low-density lanes should not hold green time unnecessarily while other approaches continue waiting.
   对应摘录：B
3. 句子 3：The same vision-based controller also detects ambulances in traffic so that emergency movement can be identified within the signal control process.
   对应摘录：A, C

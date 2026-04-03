# Intelligent Traffic Light Control System Based on Image Processing - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接围绕四车道密度、红黄绿时间分配和救护车检测来描述交通灯控制目标，适合整理为相位分配逻辑样本。

## 条目 1: Four-Lane Density and Ambulance Priority
- 控制对象：道路交通信号领域的图像处理交通灯控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟠 C（只有主链）
- 描述细节充实度：🟠 C（只有主链）
- 数据集角色：🧰 清洗后保留
- 趋同标签：✨ 未见强趋同

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

#### 摘录 D
- 出处：第 4-6 页，`3. PROPOSED SYSTEM / 4. DESIGN METHODOLOGY / 5. AMBULANCE DETECTION`，行 132-140, 194-209
> It is feasible to forecast the precise time on traffic signal timers if we use a closed loop system with cameras. We propose an image analysis-based solution for automating traffic signal control. Instead of using electrical sensors, the system detects cars using photographs. A camera will be installed near the traffic light.
> ...
> Image comparison by subtraction is a simple and effective method for detecting differences between two images ...
> ...
> Ambulance detection using image processing is a technology that aims to automatically detect the presence of ambulances in images using computer vision algorithms ... Once trained, the algorithm can be used to detect ambulances in real-time ...

### 2. 基于原文整理后的自然语言描述

The controller senses vehicle density across four lanes and computes the red, green, and yellow timing required by each lane instead of using a fixed pre-timed cycle. It is explicitly designed as a closed-loop camera-based controller, where traffic images taken near the signal are processed rather than relying on fixed timing alone. The image-processing path includes image comparison by subtraction to detect lane differences and traffic presence, and the same vision pipeline is extended to ambulance detection. As a result, low-density lanes should not hold green time unnecessarily while the controller can also identify ambulances inside the traffic stream.

### 3. 逐句溯源

1. 句子 1：The controller senses vehicle density across four lanes and computes the red, green, and yellow timing required by each lane instead of using a fixed pre-timed cycle.
   对应摘录：A, B
2. 句子 2：It is explicitly designed as a closed-loop camera-based controller, where traffic images taken near the signal are processed rather than relying on fixed timing alone.
   对应摘录：D
3. 句子 3：The image-processing path includes image comparison by subtraction to detect lane differences and traffic presence, and the same vision pipeline is extended to ambulance detection.
   对应摘录：C, D
4. 句子 4：As a result, low-density lanes should not hold green time unnecessarily while the controller can also identify ambulances inside the traffic stream.
   对应摘录：B, C

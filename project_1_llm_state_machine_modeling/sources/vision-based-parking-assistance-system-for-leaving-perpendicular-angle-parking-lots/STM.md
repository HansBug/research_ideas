# Vision-based Parking Assistance System for Leaving Perpendicular and Angle Parking Lots - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接给出离位倒车辅助检测模块的 `FSM`、CAN-Bus guard 条件与 warning 触发逻辑，原文和描述都能稳定维持双 A。

## 条目 1: Backing-Out Warning Module FSM

- 控制对象：智慧停车领域的离位倒车辅助检测与告警控制模块
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于车载摄像头和 CAN-Bus 信号的离位倒车辅助控制模块，用手动激活、倒挡、车速和转向角共同决定检测模块是否进入告警状态。
- 判断：算。对象是实际停车辅助控制模块，原文明确给出 `INIT_STATE / PRE_DETECTION / DETECTION` 以及触发与退出条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 8-14 行
> In this paper a new vision-based Advanced Driver Assistance System (ADAS) is proposed to automatically warn the driver in such scenarios. A monocular gray-scale camera is installed at the back-right side of the vehicle. A Finite State Machine (FSM) defined according to three CAN-Bus variables and a manual signal provided by the user is used to handle the activation/deactivation of the detection module.

#### 摘录 B

- 出处：第 2 页，Section III `SYSTEM DESCRIPTION`，`paper_content.txt` 第 143-160 行
> From the CAN-Bus we obtain the next variables: steering angle, car speed and current gear. These variables are used to trigger on/off the detection module according to the Finite State Machine (FSM) described in Fig. 4. As can be observed the system has to be firstly activated by the user. Then the system waits until the car has been put into reverse gear and the detection module is then triggered on. The system stops if one of the following conditions are met: (1) vehicle speed is greater than 5km/h or (2) steering angle is greater than 10 degrees with respect to the zero reference position or (3) reverse gear is deactivated.

#### 摘录 C

- 出处：第 2 页，Section II `RELATED WORK`，`paper_content.txt` 第 126-131 行
> The resulting feature vectors are modeled assuming a normalized multivariate Gaussian distribution for two types of scenarios (classes): oncoming traffic and free road. Bayes decision theory is then used by means of discriminant functions based on the minimum error rate that assumes equal prior probabilities. Finally, if the p.d.f. of the oncoming traffic class is larger than free traffic class p.d.f, the system triggers a warning signal that alerts the driver of oncoming traffic.

#### 摘录 D

- 出处：第 3 页，Fig. 4 `FSM for detection module`，`paper_content.txt` 第 172-180 行
> INIT_STATE
> PRE_DETECTION No user activation / User activation
> DETECTION ... Reverse gear ON ... |Steering angle| <= 10º ... Speed <= 5km/h ... Warning

### 2. 基于原文整理后的自然语言描述

The parking-assist controller is activated only after a manual user request and then stays in a pre-detection stage until reverse gear is engaged. Once reverse gear is on, the module enters the detection state and uses CAN-Bus steering-angle, vehicle-speed, and gear signals to decide whether the warning logic is allowed to remain active. Detection is enabled only while reverse gear stays active, vehicle speed remains at or below `5 km/h`, and the absolute steering angle remains within `10°`; otherwise the module deactivates the detection chain. Inside the detection state, the vision pipeline classifies the adjacent lane as either oncoming traffic or free road, and a warning is issued whenever the oncoming-traffic probability exceeds the free-road probability.

### 3. 逐句溯源

1. 句子 1：The parking-assist controller is activated only after a manual user request and then stays in a pre-detection stage until reverse gear is engaged.
   对应摘录：A, B, D
2. 句子 2：Once reverse gear is on, the module enters the detection state and uses CAN-Bus steering-angle, vehicle-speed, and gear signals to decide whether the warning logic is allowed to remain active.
   对应摘录：A, B, D
3. 句子 3：Detection is enabled only while reverse gear stays active, vehicle speed remains at or below `5 km/h`, and the absolute steering angle remains within `10°`; otherwise the module deactivates the detection chain.
   对应摘录：B, D
4. 句子 4：Inside the detection state, the vision pipeline classifies the adjacent lane as either oncoming traffic or free road, and a warning is issued whenever the oncoming-traffic probability exceeds the free-road probability.
   对应摘录：C, D

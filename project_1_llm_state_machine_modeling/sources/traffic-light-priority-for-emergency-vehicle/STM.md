# Traffic Light Priority for Emergency Vehicle - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽以视觉检测方案为主，但正文仍明确给出了标准灯序、救护车检测触发、对应车道切绿和未检测时保持常规序列的控制链。

## 条目 1: Ambulance Detection Override
- 控制对象：道路交通信号领域的应急车辆优先模式控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟠 C（只有主链）
- 描述细节充实度：🟠 C（只有主链）
- 数据集角色：🧰 清洗后保留
- 趋同标签：🔁 强趋同（G2 应急车辆交通灯优先）

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
- 出处：第 3-4 页，Methodology / Results，行 220-229, 255-262
> Now the video will be provided as input to the model. So as our model is trained to detect the ambulance using images, we must convert the video into frames ... If the ambulance is detected the traffic light will turn green and the traffic will be released. If the ambulance is not detected in the image, then the traffic lights work normally without any changes. ... The ambulance will appear in any of the four lanes randomly and when it comes to the traffic signal, the traffic light turns from red to green for the respective lane.

#### 摘录 D
- 出处：第 4 页，Results，行 231-239
> when the video is provided to it, it detects the ambulance in the frame and draws a boundary box, and gives a label as an emergency if an ambulance is detected in that given boundary box. If an ambulance is not detected in that given boundary box, then a class label names non-emergency will be given.

### 2. 基于原文整理后的自然语言描述

The emergency-priority controller normally leaves the traffic lights in their standard operating pattern and only overrides that pattern when priority mode is activated. A camera at the intersection provides video that is converted into frames, and a trained deep-learning model classifies each frame as emergency or non-emergency by detecting the ambulance in the scene. When an ambulance is detected, the controller communicates with the traffic-light controller and changes the respective lane from red to green so that traffic is released for the emergency vehicle. If no ambulance is detected, the non-emergency case is kept and the traffic lights continue to work normally without any change.

### 3. 逐句溯源

1. 句子 1：The emergency-priority controller normally leaves the traffic lights in their standard operating pattern and only overrides that pattern when priority mode is activated.
   对应摘录：A, C
2. 句子 2：A camera at the intersection provides video that is converted into frames, and a trained deep-learning model classifies each frame as emergency or non-emergency by detecting the ambulance in the scene.
   对应摘录：C, D
3. 句子 3：When an ambulance is detected, the controller communicates with the traffic-light controller and changes the respective lane from red to green so that traffic is released for the emergency vehicle.
   对应摘录：C
4. 句子 4：If no ambulance is detected, the non-emergency case is kept and the traffic lights continue to work normally without any change.
   对应摘录：C, D

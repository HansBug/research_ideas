# Fuzzy Logic Control of Autonomous Vehicles for Parallel Parking Maneuver - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把并联泊车划分成三步，并说明每一步都配置独立模糊控制器，结构非常适合顺序控制样本。

## 条目 1: Three-Step Parallel Parking Process
- 控制对象：智慧停车领域的自主车辆并联泊车控制器

### 0. 条目识别与判定
- 一句话说明：这是一个自主车辆并联泊车控制器，用于扫描停车位、执行倒车入位并在末段前进微调位置。
- 判断：算。对象是实际自动泊车控制器，原文明确写出了停车过程的分步结构和每一步的目标。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，parking process description, 行 88-98
> the parking process was divided into three steps and a fuzzy controller was designed for each of the steps. The three steps are: 1) parking space scanning while reaching a ready to reverse position, 2) reversing the vehicle into the parking space, and 3) adjusting the vehicle forward inside the parking space. In the ﬁrst step, the vehicle is navigated forward to reach a ready-to-reverse position with the vehicle’s orientation parallel to the available space. The parking space is also scanned using either image sensors or ultrasonic sensors.

#### 摘录 B
- 出处：第 5 页，parallel parking steps, 行 120-124
> In the second step of parallel parking, the vehicle is ﬁrst backed up into the parking space with an increasing θ until its right rear wheel is at a certain distance from the boundary SE of the space. Then the vehicle is backed up with decreasing θ until one of the rear wheels is very close to the boundary BK of the space. In the third step the vehicle is moved forward to adjust its position inside the space.

### 2. 基于原文整理后的自然语言描述

The parking controller divides the whole parallel-parking process into three steps, and a dedicated fuzzy controller is designed for each step. First, the vehicle moves forward to a ready-to-reverse position while scanning the candidate parking space with image or ultrasonic sensors. Next, the vehicle reverses into the space with a changing orientation angle until the rear wheel reaches the desired boundary distance, and finally it moves forward to adjust its position inside the parking space.

### 3. 逐句溯源

1. 句子 1：The parking controller divides the whole parallel-parking process into three steps, and a dedicated fuzzy controller is designed for each step.
   对应摘录：A
2. 句子 2：First, the vehicle moves forward to a ready-to-reverse position while scanning the candidate parking space with image or ultrasonic sensors.
   对应摘录：A
3. 句子 3：Next, the vehicle reverses into the space with a changing orientation angle until the rear wheel reaches the desired boundary distance, and finally it moves forward to adjust its position inside the parking space.
   对应摘录：B

# Design and Simulation of Small Space Parallel Parking Fuzzy Controller - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文有清楚的“先检测车位，再按 Ackerman 反向模型执行泊车”的控制流程，但正文主要通过控制模型展开。

## 条目 1: Parking-Space Detection and Reverse Parking Control
- 控制对象：智慧停车领域的并联泊车控制器

### 0. 条目识别与判定
- 一句话说明：这是一个并联泊车控制器，用于先检测附近车位，再根据车辆反向运动学模型和模糊控制器完成倒车入位。
- 判断：算，但属于模型控制级样本。对象是实际泊车控制器，不过显式状态更多体现在检测和倒车两个阶段。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Section 2.1, 行 49-54
> Before the car automatically stopping into the parking spaces, it must be detected around the parking spaces. The image sensor or ultrasonic sensor is installed around car to detect the parking spaces. ... If the parking space is large enough, the parking spaces will be the parking space of smart car.

#### 摘录 B
- 出处：第 2-3 页，Section 2.2.2, 行 117-124
> Car reversing model under the simplified model. Two wheels of car were controlled with two motors and two control chips respectively in the paper, and wheels rotational angle were determined by the Ackerman angle. ... Automatic parallel parking algorithm is based on kinematic model of the car. In building kinematic model of the car, first of all model parameters need to be determined.

### 2. 基于原文整理后的自然语言描述

The controller first detects candidate parking spaces around the vehicle by using image or ultrasonic sensors and accepts a space only when it is large enough for the smart car. After a feasible space has been identified, the automatic parallel parking algorithm drives the reverse manoeuvre from a kinematic car model in which the wheel rotation is determined by the Ackerman angle.

### 3. 逐句溯源

1. 句子 1：The controller first detects candidate parking spaces around the vehicle by using image or ultrasonic sensors and accepts a space only when it is large enough for the smart car.
   对应摘录：A
2. 句子 2：After a feasible space has been identified, the automatic parallel parking algorithm drives the reverse manoeuvre from a kinematic car model in which the wheel rotation is determined by the Ackerman angle.
   对应摘录：B

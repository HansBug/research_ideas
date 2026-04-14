# DEVELOPMENT OF 360 DEGREES AUTONOMUS AND MANUAL FIRE FIGHTING ROBOT - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 autonomous/manual 顶层模式、探火导航、避障、灭火和人工接管写成了清晰的层次监督控制，是机器人任务监督方向很扎实的双 A `HSM + T0` 样本。

## 条目 1: Autonomous-manual fire-fighting mission supervisor

- 控制对象：通用控制与消防机器人领域的自主/手动探火、避障与灭火监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个以 `Arduino Mega + flame sensors + ultrasonic + temperature/smoke sensors + water pump + servo nozzle + Bluetooth` 实现的消防机器人任务监督器。
- 判断：算。对象是实际消防机器人控制系统，原文明确写出了 autonomous/manual 双模式、火源检测、障碍规避、泵与喷嘴动作以及人工蓝牙接管链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 18-38 行
> This project focuses on designing and implementing a multi-functional robot capable of detecting, navigating toward, and extinguishing fire autonomously, while also allowing manual control through Bluetooth communication. ... The robot operates in two modes: automatic and manual. In automatic mode, it independently detects fire, navigates toward it, and extinguishes it without human intervention. In manual mode, the robot can be controlled remotely via Bluetooth ...

#### 摘录 B

- 出处：第 2 页，`Methodology`，`paper_content.txt` 第 113-122 行
> The robot is capable of 360-degree fire detection using strategically placed flame sensors ... In autonomous mode, the robot navigates toward the fire while avoiding obstacles using ultrasonic sensing and motor control through L298N drivers. Once it reaches a safe distance, the water pump is activated, and a servo motor controls the nozzle to spray water effectively. In manual mode, the robot can be controlled via Bluetooth commands from a mobile device.

#### 摘录 C

- 出处：第 3-5 页，`Obstacle Avoidance / Fire Extinguishing System / Environmental Monitoring / Communication System`，`paper_content.txt` 第 151-160 行、第 171-185 行、第 213-224 行
> If an obstacle is detected within 15 cm, the robot immediately stops to prevent collision and ensure safe navigation.
>
> When fire is detected within a certain range, the robot immediately stops and activates the water pump. The servo motor rotates the nozzle in a left, right, and center sweeping motion.
>
> The module receives manual control commands from a mobile device. ... The robot can operate in automatic mode, where it detects fire and moves toward it to extinguish it, or in manual mode, where it is controlled via Bluetooth commands.

#### 摘录 D

- 出处：第 6-7 页，`Results / Conclusion`，`paper_content.txt` 第 239-250 行、第 265-276 行
> In autonomous mode, it successfully navigated toward the fire source by following sensor-based directional logic. The ultrasonic sensor ensured safe movement by detecting obstacles and preventing collisions. The fire extinguishing system, including a water pump and servo-controlled nozzle, efficiently suppressed small fires. In manual mode, the robot responded accurately to Bluetooth commands ...
>
> The robot was able to successfully detect fire from all directions using multiple flame sensors, ensuring complete 360-degree coverage and quick response to fire incidents.

### 2. 基于原文整理后的自然语言描述

The fire-fighting robot is organized around a two-mode supervisor that switches between autonomous firefighting and Bluetooth-driven manual control. In automatic mode, the flame-sensor ring provides 360-degree direction cues, and the robot navigates toward the fire while the ultrasonic sensor stops motion whenever an obstacle appears within 15 cm. Once the robot reaches a safe extinguishing distance, the water pump turns on and the servo nozzle sweeps left, right, and center to cover the fire area. Temperature and smoke sensing add emergency-triggered alarm behavior, while manual mode lets a remote operator command robot motion and firefighting actions through Bluetooth.

### 3. 逐句溯源

1. 句子 1：The fire-fighting robot is organized around a two-mode supervisor that switches between autonomous firefighting and Bluetooth-driven manual control.
   对应摘录：A, C
2. 句子 2：In automatic mode, the flame-sensor ring provides 360-degree direction cues, and the robot navigates toward the fire while the ultrasonic sensor stops motion whenever an obstacle appears within 15 cm.
   对应摘录：B, C, D
3. 句子 3：Once the robot reaches a safe extinguishing distance, the water pump turns on and the servo nozzle sweeps left, right, and center to cover the fire area.
   对应摘录：B, C, D
4. 句子 4：Temperature and smoke sensing add emergency-triggered alarm behavior, while manual mode lets a remote operator command robot motion and firefighting actions through Bluetooth.
   对应摘录：A, C

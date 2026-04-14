# Automatic Vehicle Washing System using Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把车辆检测、三段喷洗、输送带移动和刷洗定时链写成了带秒数的顺序控制器，可以直接作为工业顺序控制样本。

## 条目 1: Timed Three-Stage Vehicle Washing and Brush Cycle

- 控制对象：自动洗车设备的输送、喷水、喷洗涤剂、二次冲洗与刷洗控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是工业自动化与离散制造领域的洗车设备顺序控制器，用 proximity sensor、conveyor、三路喷淋和 brush motor 组织车辆清洗过程。
- 判断：算。对象是实际洗车系统，原文既给出了工位顺序，也给出了多段定时值、传感器触发和执行件输出，不是只剩原理性流程介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract / Introduction，`paper_content.txt` 第 11-20 行、第 32-46 行
> Automatic vehicle washer system has three capital processes namely washing, cleansing and drying. ... Proximity sensors are used for detecting the vehicle ... As soon as the vehicle is sensed, the functioning of conveyor assembly invokes. With the predefined time delay, the conveyor gets suspend.
>
> Washing also involves three processes where the clean water is sprayed over the vehicle initially then the detergent water is sprayed and again, the normal water is sprayed. This is then followed by cleaning. ... the ladder logic is developed according to the working of the washer using timer delays.

#### 摘录 B

- 出处：第 2-3 页，`4 Proposed Methodology`，`paper_content.txt` 第 188-203 行、第 205-217 行、第 219-227 行
> When the sensor senses the vehicle, the conveyor starts to rotate ... the conveyor stops its movement and the sprinkler will start to sprinkle water over the vehicle. ... Time delay of 50 seconds is given which is required to spray the water over the vehicle ...
>
> ... the conveyor moves along with the vehicle at a distance of 30cm, and is programmed by a time delay of 10s. Now the water along with the soap or detergent is sprayed over the vehicle ... the time delay of 10s is required to spray the soap water ...
>
> ... the spraying of clean water over the vehicle ... This process will make the vehicle completely clean. Immediately after completing this process of washing with clean water for 10 sec, the conveyor starts to move with vehicle.

#### 摘录 C

- 出处：第 3 页，`5 Ladder Logic`，`paper_content.txt` 第 261-285 行
> Step-1: When the start switch (I1) is energized, the conveyor (Q1) starts rotating.
> Step-2: The conveyor stops rotating when the proximity sensor (I2) is sensed.
> Step-3: The fresh water (Q2) starts to flow for a time period of 10 seconds once the conveyor is stopped.
> Step-4: The conveyor moves for a time period of 4 seconds. Detergent water (Q3) sprayed for 5 seconds.
> Step-5: Again, there is a movement of conveyor for 2 seconds following the flow of fresh water (Q4) for 15 seconds.
> Step-6: Once the flow has stopped the brushing process (Q5) is carried over for 20 seconds.

### 2. 基于原文整理后的自然语言描述

The washing controller starts when a vehicle is detected, drives the conveyor into position, and then stops the conveyor so the first fresh-water wash can run for its programmed interval. After that initial wash, the conveyor advances the vehicle and the system enters a detergent-spray stage, then a second clean-water stage, with each stage guarded by its own programmed duration and conveyor movement. The ladder-logic sequence makes those timings explicit as conveyor start/stop, water spray, detergent spray, conveyor re-positioning, and final brushing outputs. In effect, the system behaves as a timed multi-stage washer in which proximity detection starts the cycle and the process returns to motion only after each spray or brush interval completes.

### 3. 逐句溯源

1. 句子 1：The washing controller starts when a vehicle is detected, drives the conveyor into position, and then stops the conveyor so the first fresh-water wash can run for its programmed interval.
   对应摘录：A, B, C
2. 句子 2：After that initial wash, the conveyor advances the vehicle and the system enters a detergent-spray stage, then a second clean-water stage, with each stage guarded by its own programmed duration and conveyor movement.
   对应摘录：A, B, C
3. 句子 3：The ladder-logic sequence makes those timings explicit as conveyor start/stop, water spray, detergent spray, conveyor re-positioning, and final brushing outputs.
   对应摘录：C
4. 句子 4：In effect, the system behaves as a timed multi-stage washer in which proximity detection starts the cycle and the process returns to motion only after each spray or brush interval completes.
   对应摘录：A, B, C

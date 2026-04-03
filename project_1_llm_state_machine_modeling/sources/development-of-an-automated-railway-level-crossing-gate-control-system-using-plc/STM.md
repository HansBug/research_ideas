# Development of an Automated Railway Level Crossing Gate Control System using PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出了到达/离开检测、障碍物覆盖逻辑以及闸门开闭和路侧/轨侧信号切换，已经足以构成完整的道口门控样本。

## 条目 1: Sensor-Based Railway Crossing Gate Control
- 控制对象：铁路道口平交口的 PLC 门控系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是轨道交通领域的铁路道口门控控制器，用于在列车接近和离开道口时驱动栏杆开闭，并在道口存在障碍物时维持安全防护。
- 判断：算。对象是实际铁路平交口控制系统，原文给出了列车到达/离开检测、障碍物检测和门控自动化目标。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 18-25
> The existing conventional railway crossing gate control system in Bangladesh is being operated manually which causes increasing amount of accidents at the crossings due to the carelessness in manual operation. Also, manual mechanism is time consuming. The gate controlling mechanism should be carried out ensuring safety to the road users and guarantying less time during gate opening and closing process. In this work, a prototype road and rail line model with automated railway level crossing gate controlling mechanism has been designed and implemented. At the train’s level crossing arrival and departure side, a set of photoelectric sensors are strategically placed. Also for detecting any obstacles, reflective type photoelectric sensors are used strategically.

#### 摘录 B
- 出处：第 4-7 页，System Architecture / Flow charts，行 170-205
> Three reflective type Photo Electric Sensor are used in this work. One sensor is used in Rail Track side for detecting Train ... one in road side for detecting Train while exiting the level crossing and one for detecting obstacle on level crossing track. ... Firstly, train can be detected within 10 seconds using Reflective Type Photo Electric Sensor. As the PLC unit receives signal from sensor, then at road side, red signal will be ON instructing the vehicles and passersby to stop. Also, level crossing gate barrier also closes normally. However, if the train is not detected by sensor ... at roadside green signal will be ON indicating the vehicles and passersby to pass the road.

#### 摘录 C
- 出处：第 7 页，Flow chart for obstacle detection，行 205-210
> if there is any obstacle present on roadside, PLC unit gets the valid input from obstacle sensor and train will be stopped by train operator seeing the train red light. This red light will stay ON until any obstacle is removed. In this situation, gate also opens.

### 2. 基于原文整理后的自然语言描述

The PLC crossing controller uses three reflective photoelectric sensors: an arrival-side train sensor, an exit-side train sensor, and an obstacle sensor at the road crossing. When the arrival sensor detects a train, the PLC turns the road-side green signal off, turns the road-side red signal on, and drives the barrier motors so that the crossing gate closes. While the train is on the crossing, the controller keeps monitoring the obstacle sensor, and if an obstacle is detected it turns on the train-side red warning light and reopens the gate until the obstacle is removed. After the train is detected at the departure side and no obstacle remains, the controller restores the normal road-side green condition and opens the barrier again.

### 3. 逐句溯源

1. 句子 1：The PLC crossing controller uses three reflective photoelectric sensors: an arrival-side train sensor, an exit-side train sensor, and an obstacle sensor at the road crossing.
   对应摘录：A, B
2. 句子 2：When the arrival sensor detects a train, the PLC turns the road-side green signal off, turns the road-side red signal on, and drives the barrier motors so that the crossing gate closes.
   对应摘录：B
3. 句子 3：While the train is on the crossing, the controller keeps monitoring the obstacle sensor, and if an obstacle is detected it turns on the train-side red warning light and reopens the gate until the obstacle is removed.
   对应摘录：C
4. 句子 4：After the train is detected at the departure side and no obstacle remains, the controller restores the normal road-side green condition and opens the barrier again.
   对应摘录：B, C

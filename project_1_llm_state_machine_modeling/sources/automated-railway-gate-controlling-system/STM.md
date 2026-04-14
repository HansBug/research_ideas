# Automated Railway Gate Controlling System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把超声列车检测、卡阻检测、红/绿灯、报警器和闸杆同步控制连成一条条件清晰的时序链，并给出 `1 km / 10 m / 1 s / 0.5 s / 10 s` 等参数，满足双 A 要求。

## 条目 1: Ultrasonic train/stuck detection gate controller

- 控制对象：轨道交通与铁路控制领域的超声列车检测与卡阻报警道口门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用超声传感器检测列车接近和道路卡阻的铁路平交口门控系统，根据列车距离、卡阻状态和通过状态联动闸杆、红绿灯和报警器。
- 判断：算。对象是实际铁路道口控制器，原文同时给出传感器部署、定时触发、卡阻判定周期、闸杆动作和状态表，不是单纯的装置总览。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 8-23 行
> This paper aims to provide an automatic railway gate at the level crossing ... by using the train and stuck detection on the level crossing, generating corresponding alert signal and controlling the gate. The solution is provided by developing a train and stuck detection module, light signaling module, alarm module, railway gate controller and a controller module ... Then the controller unit detects whether the obstacle is train or stuck and takes required steps by controlling the gate.

#### 摘录 B

- 出处：第 2-3 页，`III. Proposed Railway Gate Controlling System`，`paper_content.txt` 第 176-223 行
> These ultrasonic sensors are placed near the rail line at both side of the level crossing ... the control unit switches on the red light, generates alarm and pull down the gate immediately ... If passes the controller switches on the green light, stops generation of alarm and pull the gate up ... If the ultrasonic sensor placed at the middle of the level crossing receives the reflected sound continuously for a certain period then stuck is detected.

#### 摘录 C

- 出处：第 3 页，`B. The Train and Stuck detection` / `C. Detection of Stuck`，`paper_content.txt` 第 243-269 行
> The pair of sensors are placed one Km apart from the level crossing and distance between two sensors of a pair is 10m ... If no obstacle is found then the sensors are triggered at the time interval of 1s seconds. If any obstacle is found by any sensor the system triggers the sensor repeatedly at 0.5s second interval.
>
> The sensor is triggered in every second. The received signal of the receiver is analyzed in every 10 seconds. If all transmitted signals are reflected and received by the receiver then the controller decides that there is a stuck on the level crossing.

#### 摘录 D

- 出处：第 3-4 页，`D. Warning and light signal generation` / `E. Rail gate controlling` / `Table 1`，`paper_content.txt` 第 271-296, 321-334 行
> When a train is found, the controller starts generating alarm sound, switches off the green signal and switches on the red signal ... The gate is always up position and when a train comes towards the level crossing the rail gate is pulled down. When the train passes ... the gate is pulled up.
>
> Train coming but distance between level crossing and train <=1km but no stuck on level crossing: Off / On / Red / Down. Train passing level crossing: Off / On / Red / Down. Train passed level crossing: Off / Off / Green / Up.

### 2. 基于原文整理后的自然语言描述

The railway-gate controller combines train detection and stuck-vehicle detection by using four ultrasonic sensors near the track and an additional middle sensor at the level crossing. Two sensors on each side are positioned `1 km` from the crossing and `10 m` apart, and the controller interprets simultaneous same-side detection as an approaching train. Under normal conditions the sensors are triggered every `1` second, but once an obstacle is found the sampling interval is tightened to `0.5` seconds; meanwhile, the middle sensor is analyzed every `10` seconds to decide whether a vehicle is stuck on the crossing. When a train is detected, the controller turns the road signal red, starts the alarm, and pulls the gate down; after the train passes, it immediately stops the alarm, restores the green signal, and lifts the gate. The state table further distinguishes `train > 1 km`, `train <= 1 km`, `train passing`, `train passed`, and `stuck on the level crossing`, making the gate, signal, and alarm outputs explicit for each condition.

### 3. 逐句溯源

1. 句子 1：The railway-gate controller combines train detection and stuck-vehicle detection by using four ultrasonic sensors near the track and an additional middle sensor at the level crossing.
   对应摘录：A, B
2. 句子 2：Two sensors on each side are positioned `1 km` from the crossing and `10 m` apart, and the controller interprets simultaneous same-side detection as an approaching train.
   对应摘录：C
3. 句子 3：Under normal conditions the sensors are triggered every `1` second, but once an obstacle is found the sampling interval is tightened to `0.5` seconds; meanwhile, the middle sensor is analyzed every `10` seconds to decide whether a vehicle is stuck on the crossing.
   对应摘录：C
4. 句子 4：When a train is detected, the controller turns the road signal red, starts the alarm, and pulls the gate down; after the train passes, it immediately stops the alarm, restores the green signal, and lifts the gate.
   对应摘录：B, D
5. 句子 5：The state table further distinguishes `train > 1 km`, `train <= 1 km`, `train passing`, `train passed`, and `stuck on the level crossing`, making the gate, signal, and alarm outputs explicit for each condition.
   对应摘录：D

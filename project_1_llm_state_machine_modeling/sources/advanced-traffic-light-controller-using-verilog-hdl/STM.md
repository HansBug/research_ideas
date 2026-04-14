# An Advanced Traffic Light Controller using Verilog HDL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把交通灯写成了基于计时器、车流传感器、应急车辆优先和摄像抓拍联动的 `FSM` 控制器，原文与描述都足够支撑双 A 交通样本。

## 条目 1: Sensor-Prioritized Traffic-Light FSM with Emergency and Camera Override

- 控制对象：道路交通信号控制领域的密度感知、应急优先与抓拍联动交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 `Verilog` 实现的交通灯有限状态机，用绿黄计时、车流密度传感、应急车辆声学检测和红灯抓拍逻辑来控制路口信号切换。
- 判断：算。对象是实际交通灯控制器，不是通用 `FPGA` 流程论文；原文明确写出了 `FSM` 建模、计时器驱动切换、传感器决定通行时长、应急车辆优先分支和摄像抓拍联动。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Section `II. FSM Modeling and State Diagram`，`paper_content.txt` 第 63-94 行
> The traffic light controller is a sequential circuit and is modeled as a finite state machine ... The transition from one state to other is dependent on the timer.
>
> When the state machine is in a particular state, first of all, the green light corresponding to a particular lane glows for the duration as predefined by the user. Afterwards, the yellow light ... is turned on for a predefined specific duration ... Once the timer counts down completely, the machine switches to the next state.

#### 摘录 B

- 出处：第 2-4 页，`TLC Flow Chart / Four Road Traffic Structure / Six Road Traffic Structure`，`paper_content.txt` 第 96-141、181-249 行
> The yellow light is split into two phases as yellow signal1 (Y1) and yellow signal2 (Y2). Pedestrian will be “OFF” in yellow signal1 (Y1) and pedestrian will be “ON” in yellow signal2 (Y2) ...
>
> If any one of the road's IR sensor is sensed, respective time is given as per the no. of sensors ... When provided pass time for a particular traffic is about to finish and still vehicles are available on current traffic road then current pass signal turns red only if vehicle on other road is sensed, otherwise current traffic road signal remains green.
>
> State S22 is for allowing the traffic of road in which emergency vehicle is sensed ... State S1 is executed only if no road is having emergency vehicle. State S1 checks the activated sensor with priority of checking sequence a, b, c, d, e, f and accordingly pass time is given ...

#### 摘录 C

- 出处：第 4 页，`Provision of Allowing Emergency Vehicles / Camera module / Conclusion`，`paper_content.txt` 第 237-284 行
> Here an emergency vehicle is detected by using the sound sensors ... controller checks whether the detected sound signal is from the same road and then allows the traffic to flow until emergency vehicle has passed ... After passing of emergency vehicle default sequence of traffic flow continues.
>
> If along with the allowed traffic, traffic of a restricted road is trying to cross the respective RC sensor then logic 1 is provided to camera module and it captures images ...
>
> The main feature of this study is the dynamic traffic pass time allocation and provision to detect the emergency vehicles like ambulance, fire brigade etc, giving them priority to pass first and then traffic resumes normally.

### 2. 基于原文整理后的自然语言描述

The controller is an explicitly modeled FSM for traffic-actuated intersections rather than a fixed-cycle lamp driver. Its base sequence gives one road a timer-bounded green interval, then yellow, then red before service moves to the next road, and in the four-road flow the yellow phase is further split into `Y1` and `Y2` so pedestrian permission can be separated from the first warning phase. Sensor activations determine the pass time and can keep the current road green when other roads are empty, while the six-road state diagram introduces a default sensor-check state `S1` and an emergency branch rooted at `S22` for ambulance or fire-vehicle priority. The same controller also monitors `RC` sensors so red-light violations trigger the camera module, and once an emergency vehicle has passed the machine returns to the default traffic sequence.

### 3. 逐句溯源

1. 句子 1：The controller is an explicitly modeled FSM for traffic-actuated intersections rather than a fixed-cycle lamp driver.
   对应摘录：A
2. 句子 2：Its base sequence gives one road a timer-bounded green interval, then yellow, then red before service moves to the next road, and in the four-road flow the yellow phase is further split into `Y1` and `Y2` so pedestrian permission can be separated from the first warning phase.
   对应摘录：A, B
3. 句子 3：Sensor activations determine the pass time and can keep the current road green when other roads are empty, while the six-road state diagram introduces a default sensor-check state `S1` and an emergency branch rooted at `S22` for ambulance or fire-vehicle priority.
   对应摘录：B, C
4. 句子 4：The same controller also monitors `RC` sensors so red-light violations trigger the camera module, and once an emergency vehicle has passed the machine returns to the default traffic sequence.
   对应摘录：C

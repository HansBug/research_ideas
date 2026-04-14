# An Intelligent Vehicular Traffic Signal Control System with State Flow Chart Design and FPGA Prototyping - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口密度感知、绿灯持续时间映射、同密度优先顺序和故障回退到 `PCT mode` 的控制链都写得比较完整。

## 条目 1: Density-Driven Signal Phase Controller with Fault Fallback
- 控制对象：道路交通信号领域的四向路口密度感知式交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个四路口交通灯状态机控制器，按每车道三只环形传感器估计密度并动态分配绿灯时长，同时在传感器异常时退回固定周期模式。
- 判断：算。对象是实际交通灯控制系统，不是单纯 FPGA 方法论文；正文明确给出了输入传感器集合、密度等级到时长的映射、同密度服务顺序以及故障切换条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，`3.2 Traffic Density Based Control Logic / 3.4 FPGA Based State Machine`，`paper_content.txt` 第 116-157 行
> It is assumed that each lane ... have been installed with inductive loop sensors distanced at 5, 10 and 15M with Sensor-1, Sensor-2 and Sensor-3 respectively at each lane.
>
> The Fig. 2 shows the Flow Chart depicting the control logic applied in State Flow to operate as a state machine. In case of no fault the controller serves lane/s with maximum density according to sensor data as given in Table 1.
>
> The control logic accounts for the fault that can be logically detected. There are total 12 conditions (Table 2) for fault detection that override the normal VA based operation.

#### 摘录 B
- 出处：第 5 页，`Table 1. Sensor Conditions and Duration of Green Lights`，`paper_content.txt` 第 163-176 行
> Minimum i.e. Only Sensor1 is ON ... 5 Clocks/Triggers
>
> Medium i.e. Sensor1 & 2 are ON ... 10 Clocks/Triggers
>
> Maximum i.e. Sensor1, 2 & 3 are ON ... 15 Clocks/Triggers

#### 摘录 C
- 出处：第 6-8 页，`Simulation Results / Table 2 / Fig. 6-8`，`paper_content.txt` 第 181-206 行、第 213-255 行
> The relative duration and switching instants of the Red, Green and Yellow lights are observed in response to those conditions.
>
> 0==1sN&&0==2sN&&1==3sN ... PCT MODE
>
> Fig. 6 shows the response of controller when the North and South lanes both attain the same level of traffic density. The system responds by opening the North lane first and then follows the South lane.
>
> Fig.7 shows the response of the controller when different lanes are set to different levels of traffic density. The controller follows the traffic density principle by serving the lane with maximum traffic density.
>
> In response to faults the system switches to PCT mode and serves in an orderly manner and ignores the traffic density present at lanes.

### 2. 基于原文整理后的自然语言描述

The controller models a four-way intersection in which each of the North, South, East, and West lanes has three inductive-loop sensors placed at 5 m, 10 m, and 15 m, and the Stateflow logic uses these sensor combinations as the state-machine inputs. Under normal operation, the controller converts the detected density level into a green-light duration: `sensor1 only` means minimum density and a `5-clock` green, `sensor1+sensor2` means medium density and a `10-clock` green, and `sensor1+sensor2+sensor3` means maximum density and a `15-clock` green. When different lanes compete, the controller serves the lane with the highest density, and if two lanes have the same density the documented example opens the North lane first and then the South lane. If any of the twelve fault patterns appears, such as a higher-numbered sensor being active while the lower one is inactive, the controller abandons density-based operation and switches to `PCT mode`, where it serves the lanes in an orderly preset cycle and ignores density inputs.

### 3. 逐句溯源

1. 句子 1：The controller models a four-way intersection in which each of the North, South, East, and West lanes has three inductive-loop sensors placed at 5 m, 10 m, and 15 m, and the Stateflow logic uses these sensor combinations as the state-machine inputs.
   对应摘录：A
2. 句子 2：Under normal operation, the controller converts the detected density level into a green-light duration: `sensor1 only` means minimum density and a `5-clock` green, `sensor1+sensor2` means medium density and a `10-clock` green, and `sensor1+sensor2+sensor3` means maximum density and a `15-clock` green.
   对应摘录：A, B
3. 句子 3：When different lanes compete, the controller serves the lane with the highest density, and if two lanes have the same density the documented example opens the North lane first and then the South lane.
   对应摘录：C
4. 句子 4：If any of the twelve fault patterns appears, such as a higher-numbered sensor being active while the lower one is inactive, the controller abandons density-based operation and switches to `PCT mode`, where it serves the lanes in an orderly preset cycle and ignores density inputs.
   对应摘录：A, C

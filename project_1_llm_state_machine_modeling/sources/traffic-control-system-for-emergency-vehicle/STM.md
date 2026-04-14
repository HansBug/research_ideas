# Traffic Control System for Emergency Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口正常配时、RF 触发应急优先、蓝灯提示和通过后恢复常规序列都写成了完整控制链，是交通信号方向可直接入账的双 A `EFSM + T1` 样本。

## 条目 1: RF-Triggered Blue-Light Emergency Override Controller

- 控制对象：道路交通信号领域的 RF 触发应急蓝灯优先放行控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个四车道路口交通信号控制器，在常规红黄绿轮转基础上加入了基于 RF 发射器的车道级应急优先覆盖和蓝灯应急提示。
- 判断：算。对象是实际交通灯控制系统，原文明确给出了正常模式、应急模式、车道选择输入、灯色输出组合和恢复到 nominal sequence 的链路。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 23-34 行
> Urbanization is growing so rapidly due to which demand is increasing in the transportation field, hence traffic control system plays an important role is handling emergency situations and disaster management. ... This will provide effectiveness to the traffic control system in both normal and emergency situations.

#### 摘录 B

- 出处：第 3 页，`Figure 2 Flow Chart of Proposed System`，`paper_content.txt` 第 181-194 行
> It represents both normal working and the emergency working of traffic control system. If there is no signal received to receiver of traffic control system it works normally as the present traffic control system. If receiver received signal from the transmitter, then the signal where road where the ambulance wants to move will become “GREEN” and “BLUE” and other signals becomes “RED” and “BLUE” until the ambulance crosses the road.

#### 摘录 C

- 出处：第 3-4 页，`Simulation`，`paper_content.txt` 第 227-233 行、第 250-258 行
> initially the traffic signal system will be working under normal operation ... all the four lanes are working normally with red, yellow and green lights on led display. Red and green lights have the delay of 2seconds each ... the yellow lights are given the delay of 0.5 seconds.
>
> There are four push buttons provided inside the emergency vehicle representing four lanes. In case of any emergency condition then the driver will give the input to the transmitter thorough the push button that in which lane the vehicle is coming.

#### 摘录 D

- 出处：第 5 页，`Emergency Condition at Lane 1 / Conclusion`，`paper_content.txt` 第 332-362 行、第 371-381 行
> when he reaches the traffic junction, he will press the push button. ... Now lane one turns GREEN and all other lanes will become RED.
>
> lane 1 we have both GREEN and BLUE signal indicating emergency go. And all other lanes have RED and BLUE signals indicating emergency stop.
>
> Once the vehicle has cleared the intersection, the traffic signal system reverts to its regular operation. To trigger the emergency mode, a manual push button is utilized.

### 2. 基于原文整理后的自然语言描述

The junction controller normally serves four lanes in sequence with a simple engineering timer cycle in which red and green hold for `2 s` and yellow holds for `0.5 s`. Each emergency vehicle carries an RF transmitter with four lane-select push buttons, and once the driver chooses the incoming lane the receiver-side Arduino decodes that lane request and overrides the normal cycle. During the override, the requested lane is switched to `GREEN + BLUE` while every competing lane is forced to `RED + BLUE`, so the system not only clears the path but also explicitly signals that the phase change is an emergency condition. After the ambulance crosses the junction and the driver releases the push button, the controller exits the emergency mode and returns to the normal lane-by-lane traffic-light sequence.

### 3. 逐句溯源

1. 句子 1：The junction controller normally serves four lanes in sequence with a simple engineering timer cycle in which red and green hold for `2 s` and yellow holds for `0.5 s`.
   对应摘录：B, C
2. 句子 2：Each emergency vehicle carries an RF transmitter with four lane-select push buttons, and once the driver chooses the incoming lane the receiver-side Arduino decodes that lane request and overrides the normal cycle.
   对应摘录：A, C
3. 句子 3：During the override, the requested lane is switched to `GREEN + BLUE` while every competing lane is forced to `RED + BLUE`, so the system not only clears the path but also explicitly signals that the phase change is an emergency condition.
   对应摘录：B, D
4. 句子 4：After the ambulance crosses the junction and the driver releases the push button, the controller exits the emergency mode and returns to the normal lane-by-lane traffic-light sequence.
   对应摘录：B, D

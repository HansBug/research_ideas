# Traffic Light Controller System Analysis Based on FPGA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对主路/支路四状态交通灯控制器的状态集合、应急/无车 guard、倒计时逻辑和 rush-hour 配时都给出了足够完整的实现说明。

## 条目 1: Main-road/side-road emergency-and-rush-hour signal supervisor

- 控制对象：道路交通信号控制领域的主路/支路交通灯监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向主路与支路交叉口的 FPGA 交通灯控制器，用四状态状态机组织常规通行、高峰时段和主/支路应急优先逻辑。
- 判断：算。对象是真实交通灯控制系统，不是纯硬件展示；原文明确给出了 `S1-S4` 状态、`urgent_m / urgent_s` 与 `mhas_car / shas_car` guard、`mcount / scount` 倒计时以及四种场景下的持续时间。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，行 6-16
> Finally, the program is downloaded to the FPGA chip for hardware verification.
> The simulation and hardware verification results demonstrate that the traffic light control system not only achieves conventional traffic command functions but also adjusts traffic timing to some extent based on changes in traffic flow during peak and off-peak hours.
> Additionally, it includes a feature to prioritize emergency vehicles under special circumstances.

#### 摘录 B

- 出处：第 3 页，Section `2.2 Design and framework of the controller system`，行 70-79
> Include these conditions: 1. No car on the main road or branch road. 2.There is an emergency on the main road or branch road. 3.The main road is in rush hour. 4.Without special circumstances.
> ... the traffic light on the main road will keep green for 30 seconds, the traffic light on the branch road will keep green for 20 seconds, and there is a yellow light for 5 seconds after the green light ends.
> ... when the main road is in rush hour, the main road will have 90 seconds of green light, and the branch road will only have 15 seconds of green light.

#### 摘录 C

- 出处：第 8-9 页，Section `4.1.1 State machine transition logic`，行 238-266
> The first state is S1, in which the main road light is green and the branch road one is red.
> ... Then the color of the main and branch road lights turns to red and green in S3 and red and yellow in S4, respectively.
> ... During the state S1, if the urgent_m is 1, the state doesn’t change. But if the urgent_s is 1, the state will change to S2.
> ... if the mcount=0 ... the state will change to S2.
> ... before the five seconds yellow time is finished, the state remains S2. When the yellow time is finished, the mcount changes to 0 and the state changes to the S3.

#### 摘录 D

- 出处：第 9-10 页，Section `4.1.2 The counter module` / `4.1.3 The traffic light module`，行 274-307
> In normal operation, the program switches between four states: S1 (Main Road Green), S2 (Main Road Yellow), S3 (Side Road Green), and S4 (Side Road Yellow).
> ... the system continuously checks whether vehicles are present on the roads (mhas_car, shas_car) and dynamically adjusts the light duration.
> The way of countdown ... is managed using two counters: mcount for the main road and scount for the side road.
> ... In the S1 state, the light on the main road is green, and the light on the side road is red. Similarly, in the S2 state, the main road is yellow, and the side road is red.

### 2. 基于原文整理后的自然语言描述

The FPGA traffic controller is organized as a four-state supervisor in which `S1` gives green to the main road and red to the side road, `S2` switches the main road to yellow, `S3` gives green to the side road, and `S4` switches the side road to yellow. The controller is not purely cyclic, because state transitions are guarded not only by timer exhaustion but also by `urgent_m / urgent_s` emergency flags and by `mhas_car / shas_car` vehicle-presence signals, so the machine can hold a green phase, shorten a phase, or switch direction early when traffic conditions change. The timing layer maintains separate countdown variables `mcount` and `scount`, with a five-second yellow interval and scenario-specific green durations such as `30/20 s` in the normal case and `90/15 s` during rush hour. In `S1`, an emergency on the main road keeps the controller in place, while an emergency on the branch road or exhaustion of `mcount` forces a transition to `S2`; after the yellow interval finishes, the machine moves to `S3` and later symmetrically to `S4`. The traffic-light outputs are directly mapped from the current state, so the same EFSM combines phase sequencing, traffic sensing, emergency override, and countdown-based switching in one implementation.

### 3. 逐句溯源

1. 句子 1：The FPGA traffic controller is organized as a four-state supervisor in which `S1` gives green to the main road and red to the side road, `S2` switches the main road to yellow, `S3` gives green to the side road, and `S4` switches the side road to yellow.
   对应摘录：C, D
2. 句子 2：The controller is not purely cyclic, because state transitions are guarded not only by timer exhaustion but also by `urgent_m / urgent_s` emergency flags and by `mhas_car / shas_car` vehicle-presence signals, so the machine can hold a green phase, shorten a phase, or switch direction early when traffic conditions change.
   对应摘录：A, C, D
3. 句子 3：The timing layer maintains separate countdown variables `mcount` and `scount`, with a five-second yellow interval and scenario-specific green durations such as `30/20 s` in the normal case and `90/15 s` during rush hour.
   对应摘录：B, D
4. 句子 4：In `S1`, an emergency on the main road keeps the controller in place, while an emergency on the branch road or exhaustion of `mcount` forces a transition to `S2`; after the yellow interval finishes, the machine moves to `S3` and later symmetrically to `S4`.
   对应摘录：C, D
5. 句子 5：The traffic-light outputs are directly mapped from the current state, so the same EFSM combines phase sequencing, traffic sensing, emergency override, and countdown-based switching in one implementation.
   对应摘录：A, D

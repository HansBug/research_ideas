# Formal Verification of a Dependable State Machine-Based Hardware Architecture for Safety-Critical Cyber-Physical Systems: Analysis, Design, and Implementation - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无额外结构标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路道口联锁系统写成带 `N / T / C / P / Q` 五态的显式 FSM，并补了 `sensor1 / sensor2` 触发链与 CTL/LTL 安全性质。

## 条目 1: Sensor1-Sensor2 Railway Crossing Safety Cycle

- 控制对象：轨道交通与铁路控制领域的铁路道口联锁与栏杆告警控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个铁路平交口联锁控制器，持续监视 `sensor1 / sensor2 / switch`，并驱动双栏杆、灯光与 whistle 在列车进站、穿越和离开安全区时切换。
- 判断：算。对象是实际铁路 crossing/interlocking safety controller，原文明确给出状态名、输入输出、传感触发顺序以及与这些状态对应的 CTL/LTL 安全要求。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6 页，Section 3.1 Analysis of a Railway Interlocking CPS System Requirements，行 318-341
> 1. When the train is coming and arrive the sensing unit region called sensor1 ... the sensing unit will immediately be triggered and activated causing the two gates: gate1 and gate2 ... to be closed, the traffic green lights ... to be on, and the whistle to start working.
> 2. When the train is determined to be in the safety-critical interlocking zone which is represented by the distance between the sensor1 and sensor2 units, the two gates will remain in a closed status, and the red alarm lights will start flashing.
> 3. When the train arrives the sensing unit called sensor2, it will immediately be triggered on, the train considers coming out the safety-critical interlocking zone, the two gates will remain closed, the red alarm lights stop flashing, and the whistle remains on.
> 4. When the two sensing units sensor1 and sensor2 are disabled, that indicates that there is no train in the railway interlocking station, thus, the finite state machine will transition into a safe state in which the two gates will be opened, the green alarm lights are on, and the whistle becomes off.

#### 摘录 B

- 出处：第 7 页，Section 3.2 Modeling of a Railway Interlocking CPS System，行 389-423
> ● C-state, defined as enumeration “train_in_CS” means that the train has successfully arrived the safety-critical zone.
> ● P-state, defined as enumeration “train_away_CS” means that the train will eventually leave the safety-critical section.
> ● Q-state, defined as enumeration “train_out_CS” means that the train has left the safety-critical section.
>
> Referring to Fig. 7, the RIS system state is initially in “train_not_CS” state, when the train arrives at sensor1, then sensor1 will be triggered and the state becomes the “train_tries_CS” state which causes the gates to be closed, the green lights are on, and the train whistle starts working. The state machine does not transit to “train_away_CS” or “train_out_CS” states until the train arrives at sensor2 zone. Otherwise, the state remains in the safety-critical “train_in_CS” state. ... The finite state machine (FSM) diagram ... has five states that are described as follows:
> ● N-state, defined in NuSMV program as enumeration “train_not_CS” means that the train is not in the safety-critical railway interlocking section.
> ● T-state, defined as enumeration “train_tries_CS” means that the train will enter the safety-critical zone shortly.

#### 摘录 C

- 出处：第 9 页，Table 1 CTL safety properties，行 517-544
> Property1 ... The gates remain open, green lights are on, and whistle of the train is off until train arrives sensor1 and main switch is on
> Property2 ... when sensor1 is off and sensor2 is off, then gates are open, alarm lights are off, and whistle is off
> Property3 ... whenever sensor1 and main switch are active at the same time, it will eventually take the FSM into C state
> ...
> Property7 AG! (sensor1 & sensor2 & switch) The safety property which is important to verify is that sensor1, sensor2, and switch always must never be active at the same time
> Property8 G ( T ==> F C) Whenever the train is arriving the sensor1, eventually it will enter the critical zone
> Property9 G ( T ==> X( C U Q) ) Whenever the sensor1 signal is asserted, the railway interlocking state machine should move immediately to C state and remain there until the sensor1 signal is de-asserted

### 2. 基于原文整理后的自然语言描述

The railway crossing controller monitors the Boolean inputs `sensor1`, `sensor2`, and `switch`, and it drives the outputs for `gate1`, `gate2`, alarm lights, and whistle according to the train’s progress through the crossing zone. Its FSM is explicitly organized around the five states `N/train_not_CS`, `T/train_tries_CS`, `C/train_in_CS`, `P/train_away_CS`, and `Q/train_out_CS`: the system starts in `N`, moves to `T` when the train reaches `sensor1`, enters the critical-section behavior with gates closed and warning devices active, remains in the critical-section chain until `sensor2` is reached, and only returns to the safe open-gate condition after the train has left the monitored zone. The paper also gives the operational output chain in detail: `sensor1` closes both gates and starts the whistle, the in-zone phase keeps the gates closed and flashes the red alarm lights, `sensor2` stops the flashing while keeping the gates closed, and the all-sensors-off condition opens the gates and turns the whistle off. These state transitions are tied to formal safety properties requiring, among other things, that `sensor1` eventually leads to `C`, that `C` persists until the train leaves toward `Q`, and that `sensor1`, `sensor2`, and `switch` must never be active together.

### 3. 逐句溯源

1. 句子 1：The railway crossing controller monitors the Boolean inputs `sensor1`, `sensor2`, and `switch`, and it drives the outputs for `gate1`, `gate2`, alarm lights, and whistle according to the train’s progress through the crossing zone.
   对应摘录：A, B
2. 句子 2：Its FSM is explicitly organized around the five states `N/train_not_CS`, `T/train_tries_CS`, `C/train_in_CS`, `P/train_away_CS`, and `Q/train_out_CS`: the system starts in `N`, moves to `T` when the train reaches `sensor1`, enters the critical-section behavior with gates closed and warning devices active, remains in the critical-section chain until `sensor2` is reached, and only returns to the safe open-gate condition after the train has left the monitored zone.
   对应摘录：B
3. 句子 3：The paper also gives the operational output chain in detail: `sensor1` closes both gates and starts the whistle, the in-zone phase keeps the gates closed and flashes the red alarm lights, `sensor2` stops the flashing while keeping the gates closed, and the all-sensors-off condition opens the gates and turns the whistle off.
   对应摘录：A
4. 句子 4：These state transitions are tied to formal safety properties requiring, among other things, that `sensor1` eventually leads to `C`, that `C` persists until the train leaves toward `Q`, and that `sensor1`, `sensor2`, and `switch` must never be active together.
   对应摘录：C

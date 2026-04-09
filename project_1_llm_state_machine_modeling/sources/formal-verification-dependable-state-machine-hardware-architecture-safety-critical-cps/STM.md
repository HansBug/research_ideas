# Formal Verification of a Dependable State Machine-Based Hardware Architecture for Safety-Critical Cyber-Physical Systems: Analysis, Design, and Implementation - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：虽然论文主体是形式验证与容错架构，但其铁路联锁 case study 明确给出了五态 `FSM`、`sensor1/sensor2/switch` 输入、闸门/告警/whistle 输出和可追溯安全性质，足以稳定形成 `EFSM + T0` 正例。

## 条目 1: Five-state sensor-gate-whistle railway interlocking supervisor

- 控制对象：双传感道口门控与告警铁路联锁控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向铁路关键区段的联锁监督控制器，用 `sensor1 / sensor2 / switch` 判断列车是否进入或离开安全区，并控制两侧闸门、告警灯和 whistle 的输出。
- 判断：算。对象是真实铁路联锁/道口控制案例，不是单纯验证流程；原文不仅给出高层状态机，还把状态、传感器输入、执行输出和形式化安全性质一一对应起来。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 31-42 行
> ... the finite state machine is utilized to model the systems behavior which is tested by the NuSMV checker tool ... The system uses temporal logic to formulate the required properties for a railway interlocking system (RIS) as a case study ... The simulation results prove the effectiveness of the architecture for verifying critical properties and detecting design faults ...

#### 摘录 B

- 出处：第 6 页，Section `3.1 Analysis of a Railway Interlocking CPS System Requirements`，`paper_content.txt` 第 318-341 行
> When the train is coming and arrive the sensing unit region called sensor1 ... the sensing unit will immediately be triggered ... causing the two gates: gate1 and gate2 ... to be closed ... and the whistle to start working.
> When the train is determined to be in the safety-critical interlocking zone ... the two gates will remain in a closed status, and the red alarm lights will start flashing.
> When the train arrives the sensing unit called sensor2 ... the two gates will remain closed ... and the whistle remains on.
> When the two sensing units sensor1 and sensor2 are disabled ... the finite state machine will transition into a safe state in which the two gates will be opened ... and the whistle becomes off.

#### 摘录 C

- 出处：第 7 页，Section `3.2 Modeling of a Railway Interlocking CPS System Using State Machine and UML Model-based Design`，`paper_content.txt` 第 397-418 行
> Referring to Fig. 7, the RIS system state is initially in “train_not_CS” state, when the train arrives at sensor1, then sensor1 will be triggered and the state becomes the “train_tries_CS” state ... The state machine does not transit to “train_away_CS” or “train_out_CS” states until the train arrives at sensor2 zone. Otherwise, the state remains in the safety-critical “train_in_CS” state. ... input sensors: S1, S2: [0, 1], Main switch: [0, 1], output gates, gate1, gate2 ... output alarm lights ... and output alarm sound, whistle ...

#### 摘录 D

- 出处：第 8-9 页，Section `3.3 Formal Modeling and Verification of LTL/CTL Properties`，`paper_content.txt` 第 500-544 行
> The safety property which is important to be verified was “AG! (event = sensor1 & event = sensor2)” ...
> Property8 G ( T ==> F C) Whenever the train is arriving the sensor1, eventually it will enter the critical zone
> Property9 G ( T ==> X( C U Q) ) Whenever the sensor1 signal is asserted, the railway interlocking state machine should move immediately to C state and remain there until the sensor1 signal is de-asserted

### 2. 基于原文整理后的自然语言描述

The case-study railway interlocking controller monitors `sensor1`, `sensor2`, and a main `switch`, and drives two gates, alarm lights, and a whistle through a five-state finite-state machine. Its states are `train_not_CS`, `train_tries_CS`, `train_in_CS`, `train_away_CS`, and `train_out_CS`, representing no train, imminent entry, presence in the critical section, leaving, and fully cleared conditions. When the train reaches `sensor1`, the machine closes the gates and turns on warning outputs; it remains in the critical-section chain until the train reaches `sensor2` and both sensors are later de-asserted, at which point the controller returns to the safe open-gate state. The paper also formalizes safety properties such as `AG!(sensor1 & sensor2 & switch)`, `G(T ==> FC)`, and `G(T ==> X(C U Q))`, which show that the interlocking FSM is specified as a concrete control system rather than only a vague architecture sketch. Since the controller uses sensor/event guards and actuator outputs without explicit engineering timers, it fits an `EFSM + T0` profile.

### 3. 逐句溯源

1. 句子 1：The case-study railway interlocking controller monitors `sensor1`, `sensor2`, and a main `switch`, and drives two gates, alarm lights, and a whistle through a five-state finite-state machine.
   对应摘录：A, C
2. 句子 2：Its states are `train_not_CS`, `train_tries_CS`, `train_in_CS`, `train_away_CS`, and `train_out_CS`, representing no train, imminent entry, presence in the critical section, leaving, and fully cleared conditions.
   对应摘录：C
3. 句子 3：When the train reaches `sensor1`, the machine closes the gates and turns on warning outputs; it remains in the critical-section chain until the train reaches `sensor2` and both sensors are later de-asserted, at which point the controller returns to the safe open-gate state.
   对应摘录：B, C
4. 句子 4：The paper also formalizes safety properties such as `AG!(sensor1 & sensor2 & switch)`, `G(T ==> FC)`, and `G(T ==> X(C U Q))`, which show that the interlocking FSM is specified as a concrete control system rather than only a vague architecture sketch.
   对应摘录：A, D
5. 句子 5：Since the controller uses sensor/event guards and actuator outputs without explicit engineering timers, it fits an `EFSM + T0` profile.
   对应摘录：B, C, D

# Formal Verification of a Dependable State Machine-Based Hardware Architecture for Safety-Critical Cyber-Physical Systems: Analysis, Design, and Implementation - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路联锁平交口的五态门控控制器、输入输出变量和安全性质都写得很完整，足以形成一个清晰的平面 FSM 样本。

## 条目 1: Five-state interlocking gate and alarm controller

- 控制对象：轨道交通与铁路控制领域的五态联锁闸门、警灯与汽笛控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是轨道交通与铁路控制领域的平交口联锁控制器，用于根据 `sensor1 / sensor2 / switch` 管理闸门、警灯与汽笛的状态切换。
- 判断：算。对象是实际 safety-critical railway interlocking case study，原文不仅明确给出五个状态和输入输出定义，还用 CTL/LTL 性质验证状态推进和安全约束。

### 1. 原文摘录

#### 摘录 A

- 出处：第 7 页，`Fig. 7` 说明，`paper_content.txt` 第 389-423 行
> C-state, defined as enumeration “train_in_CS” means that the train has successfully arrived the safety-critical zone.
> P-state, defined as enumeration “train_away_CS” means that the train will eventually leave the safety-critical section.
> Q-state, defined as enumeration “train_out_CS” means that the train has left the safety-critical section.
> Referring to Fig. 7, the RIS system state is initially in “train_not_CS” state, when the train arrives at sensor1, then sensor1 will be triggered and the state becomes the “train_tries_CS” state which causes the gates to be closed, the green lights are on, and the train whistle starts working. The state machine does not transit to “train_away_CS” or “train_out_CS” states until the train arrives at sensor2 zone. Otherwise, the state remains in the safety-critical “train_in_CS” state.
> ... the basic parameters for the design model as follows: input sensors: S1, S2: [0, 1], Main switch: [0, 1], output gates, gate1, gate2: G1, G2: [0,1], output alarm lights: L1, L2: [0, 1], and output alarm sound, whistle: B: [0, 1].
> The finite state machine (FSM) diagram presented in Fig. 7, for the proposed railway interlocking system has five states ...

#### 摘录 B

- 出处：第 8-9 页，`Table 1 / safety properties`，`paper_content.txt` 第 454-464, 500-504, 517-526 行
> Property 8: “whenever the train is arriving the sensor1, eventually it will enter the critical section”.
> Property9: “whenever the sensor1 signal is asserted the railway interlocking state machine should move immediately to the “train-in-CS” state and remain there until the sensor1 signal is de-asserted”.
> AG! (event = sensor1 & event = sensor2), which means that sensor1 and sensor2 always must be never both “on” at the same time.
> Property2 ... Always in all paths, when sensor1 is off and sensor2 is off, then gates are open, alarm lights are off, and whistle is off
> Property3 AG((states = train_tries_CS) -> EF (states = train_in_CS)) In all paths, whenever sensor1 and main switch are active at the same time, it will eventually take the FSM into C state

### 2. 基于原文整理后的自然语言描述

The railway interlocking controller is modeled as a five-state FSM with `train_not_CS`, `train_tries_CS`, `train_in_CS`, `train_away_CS`, and `train_out_CS` states. Starting from `train_not_CS`, a `sensor1` trigger moves the machine into the approach and entry chain, closes both gates, turns on the warning lights, and starts the whistle while the train enters the safety-critical section. The controller does not advance to the leaving states until the train reaches the `sensor2` zone, and the verified CTL/LTL properties additionally require that when both sensors are inactive the gates and alarms are off, that `train_tries_CS` eventually reaches `train_in_CS`, and that `sensor1` and `sensor2` are never treated as active simultaneously. Because the state progression is driven by discrete sensor events and switch conditions rather than operational timers, the case is a `T0` railway FSM rather than a timed controller.

### 3. 逐句溯源

1. 句子 1：The railway interlocking controller is modeled as a five-state FSM with `train_not_CS`, `train_tries_CS`, `train_in_CS`, `train_away_CS`, and `train_out_CS` states.
   对应摘录：A
2. 句子 2：Starting from `train_not_CS`, a `sensor1` trigger moves the machine into the approach and entry chain, closes both gates, turns on the warning lights, and starts the whistle while the train enters the safety-critical section.
   对应摘录：A
3. 句子 3：The controller does not advance to the leaving states until the train reaches the `sensor2` zone, and the verified CTL/LTL properties additionally require that when both sensors are inactive the gates and alarms are off, that `train_tries_CS` eventually reaches `train_in_CS`, and that `sensor1` and `sensor2` are never treated as active simultaneously.
   对应摘录：A, B
4. 句子 4：Because the state progression is driven by discrete sensor events and switch conditions rather than operational timers, the case is a `T0` railway FSM rather than a timed controller.
   对应摘录：A, B

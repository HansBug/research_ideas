# A VLSI implementation of elevator control based on finite state machine using Verilog HDL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无额外结构标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三层电梯控制器直接写成 Mealy FSM，给了状态编码、方向控制变量与完整楼层迁移表。

## 条目 1: Three-Floor Mealy Elevator Transition Controller

- 控制对象：楼宇机电与电梯控制领域的三层电梯 Mealy 状态机控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Verilog 的三层电梯控制器，用楼层状态、方向信号 `EIDENTIFY` 和请求/方向控制变量 `B1/B2/B3/S1/S2/S3` 来决定驻留楼层与上下行迁移。
- 判断：算。对象是实际 elevator controller，原文明确声明其为 Mealy FSM，并给出楼层状态解释与具体转移表。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Section 2 Algorithms，行 106-137
> In our project elevator control system is a Mealy Finite state machine and the type of state encoding used is Binary encoding technique. Each floor is assigned with a state variable. Based on control inputs elevator switches between floors. We implemented our project for three floors using Verilog ...
>
> We have various control variables to determine the movement of lift i.e. whether lift is moving upwards or downwards or in the same floor. When there is no input applied lift remains in the ground floor. This can be helpful at time of emergencies or power failures because lift resumes to ground floor when there is no control input.
>
> ... EIDENTIFY is a control signal which is used to determine whether lift is moving upward or downward or lift is present in the floor ... If EIDENTIFY = “00” lift is present in the floor, if EIDENTIFY = “01” elevator moves upwards, if EIDENTIFY = “10” lift moves downwards.

#### 摘录 B

- 出处：第 2 页，State Table / Design rules，行 146-188
> If Floor is “0000001” and control signal B1 is “1” lift is present in floor 1. If Floor is “0000001” and control signal B2 is “1”, S2 is “1”, EIDENTIFY is “01” lift is moving from floor 1 to floor 2. If Floor is “0000001” and control signal B3 is “1”, S3 is “1”, EIDENTIFY is “01” lift is moving from floor 1 to floor 3. If Floor is “0000010” and control signal B2 is “1” lift is present in floor 2. If Floor is “0000010” and control signal B3 is “1”, S3 is “1”, EIDENTIFY is “01” lift is moving from floor 2 to floor 3. If Floor is “0000010” and control signal B1 is “1”, S1 is “1”, EIDENTIFY is “10” lift is moving from floor 2 to floor 1. If Floor is “0000011” and control signal B3 is “1” lift is present in floor 3. If Floor is “0000011” and control signal B2 is “1”, S2 is “1”, EIDENTIFY is “10” lift is moving from floor 3 to floor 2.
>
> ... figure 2 indicates that elevator is moving from Floor 1 to Floor 2 as B2 is “1”, S2 is “1”, EIDENTIFY is “01” ... figure 6 indicates that elevator is moving from Floor 2 to Floor 1 as B1 is “1”, S1 is “1”, EIDENTIFY is “10” ... figure 8 indicates that elevator is moving from Floor 3 to Floor 2 as B2 is “1”, S2 is “1”, EIDENTIFY is “10”.

### 2. 基于原文整理后的自然语言描述

The elevator controller is explicitly implemented as a three-floor Mealy finite state machine with binary state encoding, where each floor is represented by its own state variable and the controller decides whether the lift stays on the current floor, moves upward, or moves downward. The signal `EIDENTIFY` encodes the movement mode: `00` means the lift is currently on a floor, `01` means upward motion, and `10` means downward motion, and the paper also states that when no input is applied the lift remains at or returns to the ground floor for emergency recovery. The state table then spells out the concrete transitions: from floor `1`, `B2 + S2 + EIDENTIFY=01` triggers `1 -> 2` and `B3 + S3 + EIDENTIFY=01` triggers `1 -> 3`; from floor `2`, `B3 + S3 + EIDENTIFY=01` triggers `2 -> 3` while `B1 + S1 + EIDENTIFY=10` triggers `2 -> 1`; from floor `3`, `B2 + S2 + EIDENTIFY=10` triggers `3 -> 2`. The design rules restate these same cases one by one, so the paper provides not just a generic statement that an elevator uses an FSM, but a concrete floor-to-floor transition map with explicit control variables and direction coding.

### 3. 逐句溯源

1. 句子 1：The elevator controller is explicitly implemented as a three-floor Mealy finite state machine with binary state encoding, where each floor is represented by its own state variable and the controller decides whether the lift stays on the current floor, moves upward, or moves downward.
   对应摘录：A
2. 句子 2：The signal `EIDENTIFY` encodes the movement mode: `00` means the lift is currently on a floor, `01` means upward motion, and `10` means downward motion, and the paper also states that when no input is applied the lift remains at or returns to the ground floor for emergency recovery.
   对应摘录：A
3. 句子 3：The state table then spells out the concrete transitions: from floor `1`, `B2 + S2 + EIDENTIFY=01` triggers `1 -> 2` and `B3 + S3 + EIDENTIFY=01` triggers `1 -> 3`; from floor `2`, `B3 + S3 + EIDENTIFY=01` triggers `2 -> 3` while `B1 + S1 + EIDENTIFY=10` triggers `2 -> 1`; from floor `3`, `B2 + S2 + EIDENTIFY=10` triggers `3 -> 2`.
   对应摘录：B
4. 句子 4：The design rules restate these same cases one by one, so the paper provides not just a generic statement that an elevator uses an FSM, but a concrete floor-to-floor transition map with explicit control variables and direction coding.
   对应摘录：B

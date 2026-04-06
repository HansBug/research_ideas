# Intelligent decision-making method for vehicles in emergency conditions based on artificial potential fields and finite state machines - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把紧急工况下的车辆决策机拆成纵向与横向两层状态机，并保留了 `free driving / following / emergency braking / emergency lane changing` 及其阈值规则，是一条非常完整的 `🚗 + HSM + T0` 双 A 样本。

## 条目 1: Four-State Emergency Driving HFSM

- 控制对象：汽车与道路车辆控制领域的紧急工况自动驾驶行为决策控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向紧急驾驶场景的层次状态机决策器，用潜势场力和相对车速联合决定 `free driving / car-following / emergency braking / emergency lane changing` 四种行为。
- 判断：算。对象是自动驾驶车辆的主行为决策，而不是单纯路径规划公式；原文明确给出状态集合、状态编码、纵向/横向分层结构和 `IF-THEN` 转移规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 15-26 行
> This study presents a decision-making method based on APFs and FSMs for emergency conditions ... This study also designed the state transition rules based on the longitudinal and lateral virtual forces. It established the vehicle decision-making model based on the finite state machine ... A hierarchical vehicle state machine decision model is proposed to enhance driving safety in emergency scenarios.

#### 摘录 B

- 出处：第 2 页，Section 2.2 `Driver behavior analysis`，`paper_content.txt` 第 141-168 行
> Based on the distinct vehicle operational zones, driving behaviors under emergency conditions are categorized into free driving, car-following, emergency braking, and emergency lane changing.
>
> Free driving ... the vehicle maintains the desired speed ...
>
> Car-following ... the primary vehicle aims to ensure driving safety by modulating throttle opening and braking force ...
>
> Emergency braking ...
>
> Emergency lane changing ... encompasses two forms: braking-induced lane change and acceleration-induced lane change.

#### 摘录 C

- 出处：第 6-7 页，Section 4.1，`paper_content.txt` 第 677-708 行
> Hierarchical finite state machine (HFSM) ... comprises multiple finite-state machines ...
>
> The decision-making process for the vehicle is divided into longitudinal and lateral processes using a hierarchical state machine.
>
> The four driving behaviors ... are established as the state set for the state machine model ... the longitudinal state set consists of free driving, following mode, and emergency braking. While the lateral state set comprises emergency lane change ... the initial state of the vehicle state machine is set to free driving.
>
> state 0 signifies free driving, state 1 represents following mode, state 2 corresponds to emergency braking, and state 3 indicates emergency lane change.

#### 摘录 D

- 出处：第 7-8 页，Section 4.2-4.3，`paper_content.txt` 第 755-807 行、第 833-848 行
> If the resultant potential field force ... is less than the vehicle’s following potential field force threshold ... the target vehicle maintains the free-driving state.
>
> ... if the preceding vehicle’s speed is less than or equal to the target vehicle’s speed ... the target vehicle will transition to the car-following state.
>
> ... if the preceding vehicle’s speed is less than or equal to the target vehicle’s speed ... the target vehicle will transition to the emergency braking state.
>
> The transition of lateral decision behaviors primarily relies on the lateral decision coefficients ... If the preceding vehicle’s speed on the target lane is higher than the target vehicle’s speed ... the vehicle executes a left lane change ... or performs a right lane change.

### 2. 基于原文整理后的自然语言描述

The paper models emergency driving decisions as a hierarchical finite-state machine that separates longitudinal behavior selection from lateral lane-change decisions. At the state-set level, the controller reasons over four behaviors: `free driving`, `car-following`, `emergency braking`, and `emergency lane changing`, with state codes `0` to `3` and initial state `free driving`. The longitudinal submachine decides whether the ego vehicle should stay free-driving, switch to following, or escalate to emergency braking by comparing the resultant potential-field force against the following and emergency-braking thresholds and then checking the speed relation between the target vehicle and the preceding vehicle. The lateral submachine is activated when the lane-change coefficients indicate that a left or right evasive maneuver is possible, and it only issues the lane-change state when the target-lane preceding vehicle is fast enough to make the maneuver admissible. In other words, the paper does not merely list maneuver names; it gives a layered state machine plus explicit `IF-THEN` transition rules for how the vehicle moves between those behaviors.

### 3. 逐句溯源

1. 句子 1：The paper models emergency driving decisions as a hierarchical finite-state machine that separates longitudinal behavior selection from lateral lane-change decisions.
   对应摘录：A, C
2. 句子 2：At the state-set level, the controller reasons over four behaviors: `free driving`, `car-following`, `emergency braking`, and `emergency lane changing`, with state codes `0` to `3` and initial state `free driving`.
   对应摘录：B, C
3. 句子 3：The longitudinal submachine decides whether the ego vehicle should stay free-driving, switch to following, or escalate to emergency braking by comparing the resultant potential-field force against the following and emergency-braking thresholds and then checking the speed relation between the target vehicle and the preceding vehicle.
   对应摘录：D
4. 句子 4：The lateral submachine is activated when the lane-change coefficients indicate that a left or right evasive maneuver is possible, and it only issues the lane-change state when the target-lane preceding vehicle is fast enough to make the maneuver admissible.
   对应摘录：D
5. 句子 5：In other words, the paper does not merely list maneuver names; it gives a layered state machine plus explicit `IF-THEN` transition rules for how the vehicle moves between those behaviors.
   对应摘录：A, C, D

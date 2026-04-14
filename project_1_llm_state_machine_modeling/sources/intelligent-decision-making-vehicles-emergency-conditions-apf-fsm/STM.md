# Intelligent decision-making method for vehicles in emergency conditions based on artificial potential fields and finite state machines - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把紧急工况自动驾驶决策拆成纵向/横向两层状态机，并用人工势场阈值和相对速度规则驱动状态切换，细节足以支撑双 A 样本。

## 条目 1: Hierarchical Emergency Driving-State Machine with APF Thresholds

- 控制对象：汽车与道路车辆领域的紧急工况自动驾驶行为决策控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向自动驾驶紧急工况的分层决策控制器，用纵向/横向两层状态机结合人工势场阈值来决定自由行驶、跟驰、紧急制动和紧急换道。
- 判断：算。对象是实际自动驾驶行为决策模块，原文明确给出 HFSM 分层结构、四个驾驶状态、状态编号，以及基于 `Fap / Fcf / Feb / kl / kr / Fhc` 和相对速度的状态转移规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6 页，`4 Decision-making model considering APF and FSM`，`paper_content.txt` 第 601-688 行
> The vehicle driving states are divided into three categories: free driving, car-following, and emergency braking. Correspondingly, the longitudinal movement is divided into three levels.
>
> Hierarchical finite state machine (HFSM), an extension of FSM, is also known as a layered state machine. It comprises multiple finite-state machines and is employed for complex decision-making systems due to its logical coherence, clear structure, and enhanced processing efficiency.
>
> The decision-making process for the vehicle is divided into longitudinal and lateral processes using a hierarchical state machine. Simulink/Stateflow is utilized to create both longitudinal and lateral decision models.

#### 摘录 B

- 出处：第 7 页，`4.1 Formulation of state transition rules / Table 2`，`paper_content.txt` 第 690-715 行
> The preceding analysis encompassed the four driving behaviors of AVs under emergency conditions: free driving, car-following, emergency braking, and emergency lane change. These behaviors are established as the state set for the state machine model, wherein the longitudinal state set consists of free driving, following mode, and emergency braking, while the lateral state set comprises emergency lane change. Utilizing the developed vehicle virtual potential field forces to explore dynamic thresholds across different scenarios and incorporating surrounding vehicle speeds as conditions for state transitions, the initial state of the vehicle state machine is set to free driving.
>
> Specifically, state 0 signifies free driving, state 1 represents following mode, state 2 corresponds to emergency braking, and state 3 indicates emergency lane changing.

#### 摘录 C

- 出处：第 7-8 页，`4.2 Formulation of longitudinal state transition rules / 4.3 Formulation of lateral state transition rules`，`paper_content.txt` 第 751-807、833-848 行
> In emergencies, if the resultant potential field force between the target vehicle and the preceding vehicle in the same lane is less than the vehicle’s following potential field force threshold, the lateral decision coefficient is set to 0, and the target vehicle maintains the free-driving state.
>
> If the resultant potential field force ... falls within the range between the vehicle’s following and emergency braking thresholds ... and the preceding vehicle’s speed is less than or equal to the target vehicle’s speed, the target vehicle will transition to the car-following state.
>
> Suppose the resultant potential field force ... exceeds the emergency braking threshold ... and the preceding vehicle’s speed is less than or equal to the target vehicle’s speed, the target vehicle will transition to the emergency braking state.
>
> The transition of lateral decision behaviors primarily relies on the lateral decision coefficients. When kl = kr = 0, indicating that the vehicle maintains a straight trajectory. When kl = 1 and kr = 0 ... if the preceding vehicle’s speed on the target lane is higher than the target vehicle’s speed, then the vehicle executes a left lane change ... When kl = 0 and kr = 1 ... then the vehicle performs a right lane change.

### 2. 基于原文整理后的自然语言描述

The emergency driving decision controller is built as a hierarchical state machine that separates longitudinal and lateral decision processes while coupling both of them to artificial-potential-field thresholds derived from vehicle dynamics. Its state set contains four explicit driving behaviors, namely `free driving`, `car-following`, `emergency braking`, and `emergency lane change`, with the initial state fixed to free driving and the attributes `0 / 1 / 2 / 3` used to encode those behaviors. In the longitudinal branch, the controller compares the resultant force `Fap` against the dynamic thresholds for following and emergency braking and also checks the relative speed of the preceding vehicle to decide whether the ego vehicle stays in free driving, drops into following mode, or escalates to emergency braking. In the lateral branch, the decision coefficients `kl` and `kr` together with the lateral resultant force and the speed of the target-lane predecessor determine whether the vehicle keeps straight, executes a left emergency lane change, or executes a right emergency lane change.

### 3. 逐句溯源

1. 句子 1：The emergency driving decision controller is built as a hierarchical state machine that separates longitudinal and lateral decision processes while coupling both of them to artificial-potential-field thresholds derived from vehicle dynamics.
   对应摘录：A
2. 句子 2：Its state set contains four explicit driving behaviors, namely `free driving`, `car-following`, `emergency braking`, and `emergency lane change`, with the initial state fixed to free driving and the attributes `0 / 1 / 2 / 3` used to encode those behaviors.
   对应摘录：B
3. 句子 3：In the longitudinal branch, the controller compares the resultant force `Fap` against the dynamic thresholds for following and emergency braking and also checks the relative speed of the preceding vehicle to decide whether the ego vehicle stays in free driving, drops into following mode, or escalates to emergency braking.
   对应摘录：C
4. 句子 4：In the lateral branch, the decision coefficients `kl` and `kr` together with the lateral resultant force and the speed of the target-lane predecessor determine whether the vehicle keeps straight, executes a left emergency lane change, or executes a right emergency lane change.
   对应摘录：C

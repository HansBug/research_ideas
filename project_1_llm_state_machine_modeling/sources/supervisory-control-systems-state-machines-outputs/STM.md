# Modelling and Implementation of Supervisory Control Systems Using State Machines with Outputs - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：章节把三设备双缓存制造系统明确写成 `Mealy state machine with outputs`，给出 `b1 / b2 / b3` 触发、`a1 / a2 / a3` 输出动作以及 reduced machine 的四态七迁移，是很干净的 FSM/T0 监督控制样本。

## 条目 1: Buffer-Constrained Three-Apparatus Mealy Supervisor

- 控制对象：通用控制与离散事件控制领域的三设备双缓存制造系统 Mealy 监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个为三台 apparatus 与两个容量为 `1` 的 intermediary buffers 设计的监督控制器，用 Mealy 状态机约束设备启动时机，从而避免 overflow 与 underflow。
- 判断：算。虽然章节整体在讲 SCT 到 PLC 的落地方法，但第 `4-6` 节制造系统案例本身就是明确的控制对象，而且状态、事件、动作和 reduced machine 都写得足够细。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，Section `4. A motivation example`，`paper_content.txt` 第 163-195 行
> This system is composed of three apparatus and two intermediary buffers with a capacity of one which are available between the apparatus ... The controllable events that correspond to the start of the apparatus' operation are represented by ax, while the uncontrollable events that correspond to the end of operation are represented by bx ... Those restrictions point out the idea that it is necessary to alternate b1-a2 and b2-a3, respectively. This means that the start of operation for an apparatus (event ax+1) will only be allowed when its input buffer is loaded (event bx).

#### 摘录 B

- 出处：第 9-10 页，Section `5. Algorithm to obtain the state machine with outputs`，`paper_content.txt` 第 331-338 行
> The state machine for the manufacturing system with the proposed algorithm is shown in Figure 9, composed of 8 states and 22 state transitions. The states are named according to the apparatus that are operating at a certain point in time and the buffers that are full. The transitions are represented by the uncontrollable events, and the taken actions, if any, are separated from the transitions by a slash (/).

#### 摘录 C

- 出处：第 11-12 页，Section `6. State machine simplification`，`paper_content.txt` 第 414-441 行
> Figure 11 shows the reduced state machine for the manufacturing system. This state machine contains only four states and seven transitions. The transitions illustrated by solid lines represent the occurrence of an action ... the transitions illustrated by self-loops in dashed lines inside a current state represent that, although a transition has occurred, an action is not fired.

#### 摘录 D

- 出处：第 12 页，Section `6. State machine simplification`，`paper_content.txt` 第 448-468 行
> Consider for instance state 2 of the reduced state machine. If transition b2 occurs, the state machine evolves to state 3. In the case that transition b1 occurs, the model illustrates that situation as a self-loop ... When event b2 occurs with transition b1 already enabled, transition b1 & b2 will be activated, so that the state machine evolves to state 4 and actions a1, a2 and a3 are taken. ... Actions will be taken only when the transitions b2 & b3 or b1 & b2 & b3 become valid.

### 2. 基于原文整理后的自然语言描述

The example system is a manufacturing line made of three apparatus and two intermediate buffers of capacity one, so the controller is not free to start each machine independently. Its coordination rule is explicit: an apparatus may start only when the corresponding upstream buffer has been loaded, which is why the chapter binds `b1` to `a2` and `b2` to `a3` to prevent overflow and underflow. The first Mealy model produced by the algorithm has eight states and twenty-two transitions, and its states are named by the currently operating apparatus and the buffers that are full. The reduced implementation-oriented machine then keeps only four states and seven transitions, distinguishing action-carrying transitions from dashed self-loops that merely store the occurrence of an uncontrollable event. In the reduced model, `b2` from state 2 advances to state 3, plain `b1` is only stored as a self-loop, and the combined transition `b1 & b2` drives the machine to state 4 while firing actions `a1`, `a2`, and `a3`.

### 3. 逐句溯源

1. 句子 1：The example system is a manufacturing line made of three apparatus and two intermediate buffers of capacity one, so the controller is not free to start each machine independently.
   对应摘录：A
2. 句子 2：Its coordination rule is explicit: an apparatus may start only when the corresponding upstream buffer has been loaded, which is why the chapter binds `b1` to `a2` and `b2` to `a3` to prevent overflow and underflow.
   对应摘录：A
3. 句子 3：The first Mealy model produced by the algorithm has eight states and twenty-two transitions, and its states are named by the currently operating apparatus and the buffers that are full.
   对应摘录：B
4. 句子 4：The reduced implementation-oriented machine then keeps only four states and seven transitions, distinguishing action-carrying transitions from dashed self-loops that merely store the occurrence of an uncontrollable event.
   对应摘录：C
5. 句子 5：In the reduced model, `b2` from state 2 advances to state 3, plain `b1` is only stored as a self-loop, and the combined transition `b1 & b2` drives the machine to state 4 while firing actions `a1`, `a2`, and `a3`.
   对应摘录：D

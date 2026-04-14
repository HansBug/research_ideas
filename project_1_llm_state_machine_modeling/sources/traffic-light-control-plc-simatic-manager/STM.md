# Automation Development of Traffic Light Control via PLC based Simatic Manager - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然篇幅较短，但把四阶段交通灯顺序、`ST1-ST4` 状态变量、`TON` on-delay 定时器和初始化/计时阈值写得完整，足以形成一个交通灯 `EFSM + T1` 样本。

## 条目 1: Four-stage barrier-aware intersection PLC controller

- 控制对象：道路交通信号控制领域的四阶段交通灯与行人阻挡联动 PLC 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向十字路口交通灯的 PLC 顺序控制器，通过四个阶段在南北/东西向绿黄灯和 pedestrian barrier cut 之间切换，并用 `ST1-ST4` 状态方程和 `TON` 定时器驱动状态推进。
- 判断：算。对象是实际交通灯控制系统，而不是单纯 PLC 教程；原文明确给出了四阶段流程、每个状态变量的含义、进入/退出方程、on-delay timer 和初始化方式。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract / Introduction，`paper_content.txt` 第 8-15、18-30 行
> The critical timing operation is required to be carried out under the existence of heavy traffic conditions.
>
> The paper introduces an execution and implementation of required program to achieve the solution of mentioned problem by using developed software Simatic Manager-Step 7.
>
> The present investigation involves the operation of traffic lights at the central node of the intersection roads with references to the timing of barrier cut traffic during pedestrian traffic, and shows the timing of timers for passing and stopping vehicles.
>
> the application work involves the state equations and ladder diagram of the traffic lights, with ability of the time modification of the timers in (PLC) according to the heavy traffic in one side or the both sides of traffic node.

#### 摘录 B

- 出处：第 2 页，`2. System requirements and methodology`，`paper_content.txt` 第 91-116 行
> The ‘PLC’ program is designed to associate traffic light system operation in parallel with the barrier cut, consists of four stages:
>
> 1. At First stage, the program allows the ‘GREEN’ light to switch (ON) normally for a long time. The ‘RED’ light for pedestrian will switch on also at the same time. Instantly, the traffic light at the another intersection road will switch vice versa comparing with the first road, in addition to the barrier down at the same instant for passing period of pedestrian.
>
> 2. The second stage, connects with yellow light (stand by to stop) ...
>
> 3. The third stage is the same of the first stage except the switch on of this traffic light at two intersections roads will be vice versa ...
>
> 4. The fourth stage connects with the yellow light (H2) for moving or stands by.

#### 摘录 C

- 出处：第 3 页，`3.1 State Equation Representation`，`paper_content.txt` 第 167-190 行
> The State Equation Method can be Applied to the Traffic Light by Doing Two Steps ...
>
> ST1 = state1 – green NS
> ST2 = state2 – yellow NS
> ST3 = state3 – green EW
> ST4 = state4 – green EW
>
> ST1 =(ST1 + ST4. TON2(ST4,4s)) ...
> ST2 =(ST2 + ST1 ... TON2(ST1,4s))
> ST3 =(ST3 + ST2. TON1(ST2, 4s)) ...
> ST4 =(ST4 + ST3 ... TON2(ST4,4s))
>
> ‘TON’ indicates that is an on-delay timer, A is the input to the timer, and delay is the timer delay value.

#### 摘录 D

- 出处：第 4 页，`3.1.9 Program Instruction Set Algorithm`，`paper_content.txt` 第 219-239 行
> S1 = (S1 + S4. (TIMER.ACC ≥ 26)) ... + First Pass
>
> S2 = (S2 + S1. (TIMER.ACC ≥ 10)) ...
>
> S2 = (S2 + S2. (TIMER.ACC ≥ 13)) ...
>
> S4 = (S4 + S2. (TIMER.ACC ≥ 23)) ...
>
> Note: Putting the “First Pass” variable in the first state equation is equivalent to setting the system in state 1 during initialization.

### 2. 基于原文整理后的自然语言描述

The PLC traffic-light controller is organized as a four-stage sequence that coordinates the signal groups of two intersecting roads together with the pedestrian barrier logic. In stage 1 the north-south road keeps green while the pedestrian red stays on and the opposite road remains in the complementary state; stage 2 moves that direction into yellow; stage 3 mirrors the long-green behavior for the other road; and stage 4 applies the other yellow transition before the cycle repeats. The control program is explicitly formalized with state variables `ST1` to `ST4`, where each variable records whether one traffic phase is active and where every state update is written as a state equation derived from the state diagram. Phase changes are driven by `TON` on-delay timers with `4 s` delay terms in the transition equations, so the controller is not just a verbal sequence but an implementation-level timed EFSM. The instruction-set form further fixes accumulated timer thresholds such as `10`, `13`, `23`, and `26`, and a `First Pass` initialization forces the controller to begin in state 1 before the normal cyclic transitions continue. The paper therefore gives a complete PLC state-update chain for a timed four-stage traffic-light controller rather than a loose hardware demo.

### 3. 逐句溯源

1. 句子 1：The PLC traffic-light controller is organized as a four-stage sequence that coordinates the signal groups of two intersecting roads together with the pedestrian barrier logic.
   对应摘录：A, B
2. 句子 2：In stage 1 the north-south road keeps green while the pedestrian red stays on and the opposite road remains in the complementary state; stage 2 moves that direction into yellow; stage 3 mirrors the long-green behavior for the other road; and stage 4 applies the other yellow transition before the cycle repeats.
   对应摘录：B
3. 句子 3：The control program is explicitly formalized with state variables `ST1` to `ST4`, where each variable records whether one traffic phase is active and where every state update is written as a state equation derived from the state diagram.
   对应摘录：A, C
4. 句子 4：Phase changes are driven by `TON` on-delay timers with `4 s` delay terms in the transition equations, so the controller is not just a verbal sequence but an implementation-level timed EFSM.
   对应摘录：C
5. 句子 5：The instruction-set form further fixes accumulated timer thresholds such as `10`, `13`, `23`, and `26`, and a `First Pass` initialization forces the controller to begin in state 1 before the normal cyclic transitions continue.
   对应摘录：D
6. 句子 6：The paper therefore gives a complete PLC state-update chain for a timed four-stage traffic-light controller rather than a loose hardware demo.
   对应摘录：A, B, C, D

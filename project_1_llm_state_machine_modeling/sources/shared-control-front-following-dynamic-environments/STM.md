# A Shared-Control Framework for A Human-Robot Front-Following Behaviour in Unknown Dynamic Environments - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把前向跟随机器人中的 intent-reading、motion-cluster 共享控制和 velocity 调节组织成了带并发子状态的复合 FSM，状态、输入和输出变化都写得比较完整。

## 条目 1: Composite intent-motion front-following supervisor

- 控制对象：通用控制与形式化工具领域的前向跟随移动机器人共享控制监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是室内助行/陪行机器人前向跟随任务中的共享控制监督器，用 intent 子状态与 motion 子状态的组合来决定机器人何时观察、何时受限、何时保持正常跟随，以及相应的速度调节方式。
- 判断：算。对象是实际移动机器人跟随行为的监督控制器，原文明确给出了复合状态集合、输入事件、并发子状态语义、undecidability 处理逻辑以及速度输出在不同状态下的变化。

### 1. 原文摘录

#### 摘录 A

- 出处：第 9-10 页，`Undecidability` 与 observation 逻辑
> if at the next frame T + 1 there are m clusters such that m > n, then an undecidable situation has emerged.
>
> When undecidability is detected, the robot enters an observation state trying to infer the cluster that the user wants to move in. This intent recognition algorithm is based on a cluster scoring mechanism using the human angle ϕH.

#### 摘录 B

- 出处：第 11 页，FSM 状态与输入定义
> The actual states are { Normal-Motion_Far, Normal-Motion_Near, Observing-Motion_Far, Observing-Motion_Near, Restricted-Motion_Near, Idle}. The Idle state is shorthand for { Restricted-Restricted }.
>
> The input to the FSM are ten events ... U/U: Undecidability has been detected ... K/K: Robot is turning ... P/P: Hard persistence selects cluster ... I/I: Intention clusters are available ... M/M: Motion clusters are available.

#### 摘录 C

- 出处：第 11 页，状态对子状态与速度输出的影响
> It consists of six states and ten boolean events ... The states are composite and comprise two concurrent substates, the Intention substate and the Motion substate ...
>
> If the system is in an “observing” state ... then the robot velocity is halved in order to signal the user the beginning of the observation mode. If the system is in the “idle” state, then the velocity is nulled. In all other states the velocity remains unchanged.

#### 摘录 D

- 出处：第 10 页，shared-control authority 的切换原则
> In wide spaces motion control is transferred to the human while in narrow spaces motion control is transferred to the robot.
>
> This transfer of authority is implemented by linearly combining the cluster angle with the human angle, using a parameter “a” depending on the cluster width.

### 2. 基于原文整理后的自然语言描述

The front-following controller treats ambiguous path branching as an explicit supervision problem: when the number of feasible clusters increases from one frame to the next, the robot declares an undecidable situation and enters an observation mode that scores candidate clusters using the human-angle signal. Its finite-state machine is composite rather than flat, because each top-level state is formed from concurrent intention and motion substates; the realized combinations are `Normal-Motion_Far`, `Normal-Motion_Near`, `Observing-Motion_Far`, `Observing-Motion_Near`, `Restricted-Motion_Near`, and `Idle = Restricted-Restricted`. State transitions are driven by ten boolean inputs built from five event pairs, covering undecidability detection, robot turning, hard persistence, intention-cluster availability, and motion-cluster availability. The shared controller further uses cluster width to shift authority between the human and the robot, so wide spaces keep the path closer to human intent while narrow spaces bias the path toward robot-safe motion. Output behavior is also state dependent: entering an observing state halves the robot velocity to signal intent resolution, `Idle` nulls the velocity completely, and other states preserve the nominal speed, which makes the FSM a concrete shared-control HSM with both hierarchy and parallel structure.

### 3. 逐句溯源

1. 句子 1：The front-following controller treats ambiguous path branching as an explicit supervision problem: when the number of feasible clusters increases from one frame to the next, the robot declares an undecidable situation and enters an observation mode that scores candidate clusters using the human-angle signal.
   对应摘录：A
2. 句子 2：Its finite-state machine is composite rather than flat, because each top-level state is formed from concurrent intention and motion substates; the realized combinations are `Normal-Motion_Far`, `Normal-Motion_Near`, `Observing-Motion_Far`, `Observing-Motion_Near`, `Restricted-Motion_Near`, and `Idle = Restricted-Restricted`.
   对应摘录：B, C
3. 句子 3：State transitions are driven by ten boolean inputs built from five event pairs, covering undecidability detection, robot turning, hard persistence, intention-cluster availability, and motion-cluster availability.
   对应摘录：B
4. 句子 4：The shared controller further uses cluster width to shift authority between the human and the robot, so wide spaces keep the path closer to human intent while narrow spaces bias the path toward robot-safe motion.
   对应摘录：D
5. 句子 5：Output behavior is also state dependent: entering an observing state halves the robot velocity to signal intent resolution, `Idle` nulls the velocity completely, and other states preserve the nominal speed, which makes the FSM a concrete shared-control HSM with both hierarchy and parallel structure.
   对应摘录：C

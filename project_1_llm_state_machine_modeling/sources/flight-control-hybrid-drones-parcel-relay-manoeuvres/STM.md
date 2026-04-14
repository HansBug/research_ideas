# Flight control of hybrid drones towards enabling parcel relay manoeuvres - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把混合无人机的 rotary-wing / fixed-wing / transitional 三种控制模式统一到基于速度与倾转角的 FSM 中，并给出阈值事件表与双向过渡仿真，可直接作为双 A 航空样本。

## 条目 1: Velocity-threshold hybrid flight-mode transition controller

- 控制对象：航空航天与飞行/空管控制领域的速度阈值驱动混合无人机飞行模式切换控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 `Convergence` 倾转三旋翼混合无人机的飞行模式管理器，用参考速度、实际空速和旋翼倾角决定固定翼、旋翼与过渡控制器之间的切换。
- 判断：算。对象是实际混合飞行器的高层控制逻辑，不是单纯连续飞控器；原文明确给出 `S1/S2/S3` 三状态、输入变量 `||vref|| / vair / ā`、事件表和正反两次自动过渡仿真。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 18-26 行
> The model is then validated by designing two separate controllers for the main flight modes, rotary and fixed-wing ... The control strategy makes use of a custom hybrid control allocation technique that differentiates the control in three parts: vertical, horizontal, and transitional flight modes. Finally, a hybrid controller is proposed, using a finite state machine capable of handling logical events, with the aim to provide control logic to perform autonomous mid flight transitions.

#### 摘录 B

- 出处：第 6 页，`V. Hybrid Autopilot Controller`，`paper_content.txt` 第 586-616 行
> three different control schemes (rotary-wing, fixed-wing, and transitional) will be joined in a single controller. To overtake this issue we use a finite state machine, FSM, to handle all discrete values and logical operations.
>
> The transition method is based on velocity ... depending on both the reference velocity and the actual velocity, the controller is able to adopt the most suitable flight mode ...
>
> the input control variables used for the design of the FSM are:
> ||vref||: Reference velocity magnitude.
> vair: The actual airspeed.
> a: Rotor tilt angle.
> ... S1; S2; S3, representing each flight mode, fixed-wing, rotary-wing and transitional respectively.

#### 摘录 C

- 出处：第 6 页，`Table I EVENT BASED FSM TABLE`，`paper_content.txt` 第 617-627 行
> The event table presented in Table I shows all of the possible transitions of the FSM, using the three inputs available.
>
> ||vref|| > vrt ^ vair > vvt ... S3
> ||vref|| < vrt ^ vair < vht ... S3
> a = /2 ... S2
> a = 0 ... S1

#### 摘录 D

- 出处：第 6-7 页，`VI. Simulation`，`paper_content.txt` 第 643-651、652-699、699-705 行
> The first simulation procedure will test the performance of the hybrid controller on a positive transition ... the only human operator input is the pre-defined reference trajectory the hybrid controller handle everything else.
>
> where the reference velocity exceeds the threshold value vrt ... the UAV begins a transition ... Around t = 19 s the transition is completed, meaning that the rotor tilt angle a is fixed at 90° ...
>
> next a negative transition was simulated ... a negative step in the reference velocity occurs, bringing the reference value lower than the threshold value, vht. The UAV then is forced to reduce its speed and perform a transition to fixed-wing flight mode ...

### 2. 基于原文整理后的自然语言描述

The hybrid drone controller combines three flight-control schemes, namely fixed-wing, rotary-wing, and transitional control, under one finite-state supervisor instead of relying on manual mode switching. Its FSM uses the reference-speed magnitude `||vref||`, the actual airspeed `vair`, and the average rotor tilt angle `ā` as control variables, so the mode decision is explicitly coupled to continuous flight quantities. The machine has three states `S1/S2/S3`, corresponding to fixed-wing, rotary-wing, and transitional flight, and it enters the transitional state whenever the commanded and actual speed cross the fixed-wing or rotary-wing velocity thresholds. The event table then resolves the end of the transition by using the tilt-angle guards `ā = π/2` and `ā = 0`, which map the aircraft back to the rotary-wing or fixed-wing steady mode after the servos finish reorienting the front rotors. In simulation, both the positive and negative transitions are executed automatically from a predefined trajectory, showing that the supervisor can trigger mid-flight mode changes without human intervention while coordinating the continuous controller allocation beneath it.

### 3. 逐句溯源

1. 句子 1：The hybrid drone controller combines three flight-control schemes, namely fixed-wing, rotary-wing, and transitional control, under one finite-state supervisor instead of relying on manual mode switching.
   对应摘录：A, B
2. 句子 2：Its FSM uses the reference-speed magnitude `||vref||`, the actual airspeed `vair`, and the average rotor tilt angle `ā` as control variables, so the mode decision is explicitly coupled to continuous flight quantities.
   对应摘录：B
3. 句子 3：The machine has three states `S1/S2/S3`, corresponding to fixed-wing, rotary-wing, and transitional flight, and it enters the transitional state whenever the commanded and actual speed cross the fixed-wing or rotary-wing velocity thresholds.
   对应摘录：B, C
4. 句子 4：The event table then resolves the end of the transition by using the tilt-angle guards `ā = π/2` and `ā = 0`, which map the aircraft back to the rotary-wing or fixed-wing steady mode after the servos finish reorienting the front rotors.
   对应摘录：C
5. 句子 5：In simulation, both the positive and negative transitions are executed automatically from a predefined trajectory, showing that the supervisor can trigger mid-flight mode changes without human intervention while coordinating the continuous controller allocation beneath it.
   对应摘录：A, D

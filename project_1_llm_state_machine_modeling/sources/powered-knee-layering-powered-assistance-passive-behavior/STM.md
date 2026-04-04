# A new approach to a powered knee prosthesis: Layering powered assistance onto strictly passive prosthesis behavior - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文完整给出主动膝假肢的 `6` 态 FSM、每态 torque law、`T12/T23/.../T61` guard、活动序列表、`t > t_th` 状态定时和 gait-speed 相关 swing 规则，是强度很高的 `EFSM + T1` 样本。

## 条目 1: Six-state assist-as-needed knee controller with passive-active behavior layering
- 控制对象：主动膝假肢的六态 assist-as-needed 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向主动膝假肢的六态监督控制器，通过可重构传动和状态相关 torque law 在 resistive stance、active stance、ballistic swing 和 non-ballistic swing 之间切换，以覆盖 walking、sit-to-stand、stairs 等任务。
- 判断：算。对象是真实主动膝假肢控制器；原文直接给出状态数量、输入变量、每态 torque law、显式转移条件、任务序列表和局部定时逻辑，不是泛泛的假肢综述或实验说明。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Activity control system overview，行 156-170
> The activity controller is a six-state FSM ... Each state within the FSM has a unique transmission configuration and a unique torque control law, providing either power dissipation (passive motor control) or generalized active and emulated-passive behaviors (active motor control).
>
> Within each state, the knee torque is governed by a torque control law based on sensor inputs and control parameters that produce the following behaviors in each corresponding FSM state: (1) high-torque turbulent damping; (2) low-torque cadence-adaptive viscous damping; (3) low-torque unidirectional cadence-adaptive viscous damping that increases as the knee approaches full extension; (4) low-torque cadence-adaptive flexion torque pulse; (5) high extension torque that scales with residual hip torque and velocity; (6) low-torque PD controller with a virtual linkage between the thigh and knee joint.
>
> FSM transitions ... are governed by onboard sensing of knee angle, shank angle, shank axial force, shank axial acceleration, the walking speed estimation, and a state timer.

#### 摘录 B
- 出处：第 7 页，Table 3 and Table 4，行 196-243
> T12: Knee joint is hyperextended ... shank is rotating forward ... shank is inclined forward ... prosthesis is rapidly unloaded.
>
> T13: Prosthesis is unloaded, and F ≈ 0. Knee joint is flexed past threshold θK > θK,th.
>
> T21: Prosthesis is loaded ... prosthesis was previously unloaded ... shank rotating backward ... shank is not inclined forward.
>
> T26: Knee joint is hyperextended ... prosthesis is unloaded ... shank axial acceleration above threshold aa > aa,th.
>
> T61: Prosthesis is loaded ... or time in state beyond threshold t > tth.
>
> Controller sequence for different activities: `1` standing / stand-to-sit / backward walking; `1-2-3` level-ground and up-slope walking; `1-2-4-3` slow walking; `1-3` down-slope and down-stair walking; `1-5` sit-to-stand; `1-2-6-1-5` up-stairs walking.

#### 摘录 C
- 出处：第 8-9 页，Active stance behavior，行 247-282
> The novel active stance control law ... generalizes powered knee extension into a single torque control law that is adaptive across a range of activities that benefit from positive joint power.
>
> During the pull-up phase of stair ascent, the prosthetic ankle constrains the shank to be approximately vertical; as such, the real-time hip torque is estimated as the product of the load cell force and the sine of the knee angle.
>
> The control system uses this approximation of hip torque to deliver knee torque that is synchronized with the user’s motion.
>
> Powered knee extension is activated by the user via hip torque, which initiates a knee extension movement, which in turn is identified by the controller and used to initiate power-assisted knee extension.
>
> When knee velocity inflects, the FSM switches to resistive stance behavior.

#### 摘录 D
- 出处：第 9-10 页，Ballistic swing behavior，行 283-305
> FSM states 2–4 provide walking-speed-adaptive ballistic swing phase behavior.
>
> During swing-flexion, for walking speeds below ω0, an assistive torque is provided; for walking speeds above ω0, a resistive torque is provided.
>
> After the user has flexed the knee joint past 10°, the assistance torque begins ramping up ... At 30° of flexion, the assistance torque has reached its commanded value. After 55° of flexion, the commanded torque is zeroed so the knee joint velocity can inflect for swing-extension.
>
> The swing-extension torque control law commands a linear damping torque where the damping coefficient is a function of the walking speed and the knee angle.

### 2. 基于原文整理后的自然语言描述

The powered knee prosthesis is organized as a six-state extended state machine in which each state couples a distinct transmission configuration with a distinct torque law, allowing the controller to layer passive resistive stance, powered stance extension, ballistic swing, and non-ballistic stair swing inside one unified supervisor. Its guards are explicit and sensor-rich: transitions depend on knee angle and velocity, shank angle, shank axial force, shank axial acceleration, walking-speed estimate `ω`, and a state timer `t`, with conditions such as `θK > θK,th`, `F > Fth`, `aa > aa,th`, and `t > tth` deciding when the machine changes phase. The paper also gives activity-specific state sequences, including `1-2-3` for level walking, `1-3` for down-stair or down-slope locomotion, `1-5` for sit-to-stand, and `1-2-6-1-5` for stair ascent, so the same controller can be routed across several daily activities without redefining the state set. In active stance, the assistive extension torque is synchronized to user motion by estimating hip torque as `F * sin(θK)` and by scaling output with thigh velocity, after which the controller drops back into resistive stance when knee velocity inflects. In swing, the controller preserves ballistic behavior by switching between assistive and resistive flexion according to the crossover speed `ω0`, ramps assistance between `10°` and `30°` of flexion, zeros it after `55°`, and uses cadence-adaptive damping in swing extension, making the sample a very strong `EFSM + T1` prosthesis-control case.

### 3. 逐句溯源

1. 句子 1：The powered knee prosthesis is organized as a six-state extended state machine in which each state couples a distinct transmission configuration with a distinct torque law, allowing the controller to layer passive resistive stance, powered stance extension, ballistic swing, and non-ballistic stair swing inside one unified supervisor.
   对应摘录：A
2. 句子 2：Its guards are explicit and sensor-rich: transitions depend on knee angle and velocity, shank angle, shank axial force, shank axial acceleration, walking-speed estimate `ω`, and a state timer `t`, with conditions such as `θK > θK,th`, `F > Fth`, `aa > aa,th`, and `t > tth` deciding when the machine changes phase.
   对应摘录：A, B
3. 句子 3：The paper also gives activity-specific state sequences, including `1-2-3` for level walking, `1-3` for down-stair or down-slope locomotion, `1-5` for sit-to-stand, and `1-2-6-1-5` for stair ascent, so the same controller can be routed across several daily activities without redefining the state set.
   对应摘录：B
4. 句子 4：In active stance, the assistive extension torque is synchronized to user motion by estimating hip torque as `F * sin(θK)` and by scaling output with thigh velocity, after which the controller drops back into resistive stance when knee velocity inflects.
   对应摘录：C
5. 句子 5：In swing, the controller preserves ballistic behavior by switching between assistive and resistive flexion according to the crossover speed `ω0`, ramps assistance between `10°` and `30°` of flexion, zeros it after `55°`, and uses cadence-adaptive damping in swing extension, making the sample a very strong `EFSM + T1` prosthesis-control case.
   对应摘录：D

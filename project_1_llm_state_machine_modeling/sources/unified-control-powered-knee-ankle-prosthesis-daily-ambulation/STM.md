# Unified Control of a Powered Knee-Ankle Prosthesis Enables Walking, Stairs, Transitions, and Other Daily Ambulation Activities - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把统一控制器压成 `Contact / No Contact` 两态 `FSM`，并明确给出 `GRF` guard、`Step-Up` 接触态助力、`minimum-jerk` 摆动态轨迹与 `0.45-0.55 s` swing duration，可直接作为高质量 `EFSM + T1` 样本。

## 条目 1: Two-state unified supervisor for the Utah powered knee-ankle prosthesis
- 控制对象：`Utah Bionic Leg` 风格主动膝踝假肢的统一 ambulation controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向主动膝踝假肢的统一两态监督控制器，用地面接触状态作为唯一高层离散骨架，再在两态内部切换 stair ascent、sit-to-stand、walking 和 swing coordination 的具体控制律。
- 判断：算。对象是真实主动假肢控制器，不是纯连续轨迹优化；原文明确给出高层 `FSM`、`GRF` 触发条件、接触/离地两态下的动作生成规则以及显式 swing duration。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `II.A. Unified Controller Structure`
> The proposed unified controller uses a simple finite-state machine with two states, Contact and No Contact, to indicate if the prosthetic foot is in contact with the ground.
>
> The finite-state machine switches from Contact when the vertical ground reaction force (GRF) is above 120 N to No Contact when the GRF is below 80 N. The transition from Contact to No Contact is called toe-off (TO), and the transition from No Contact to Contact is called heel-strike (HS) ...
>
> Specific knee and ankle controllers are used in each of the two states.

#### 摘录 B
- 出处：第 4 页，Section `II.A.1) Knee Control During Contact`
> In Contact, the total commanded torque ... is the sum of three components: Step-Up torque, Biarticular torque, and Damping torque.
>
> The Step-up Torque ... is intended to provide extension torque during stair ascent, sit-to-stand transitions, and similar movements.
>
> The Step-up Torque follows a bioinspired bell-shaped profile ... starts at 0 Nm at HS ... increases until the measured knee angle matches a specified peak-torque angle ... then decreases ... reaching zero when the measured knee angle equals the ending-torque angle ...

#### 摘录 C
- 出处：第 7 页，Section `II.A.3) Knee Control During No Contact`
> During No Contact, we calculate a desired knee position and utilize a PID controller with loose gains. θKneeDes is the sum of the minimum-jerk angle and the thigh-to-knee synergy angle ...
>
> θKneeMJ aims to move the knee joint from its angle at TO to a fully extended angle in preparation for HS while mathematically maximizing smoothness ...
>
> θKneeMJ changes as a function of the knee angle at TO, the knee velocity at TO and the desired trajectory duration (tswing) ...
>
> tswing is at a maximum value of 0.55 s when θAnkleTO < −5° and decreases linearly to 0.45 s when θAnkleTO > 15°.

### 2. 基于原文整理后的自然语言描述

The unified powered prosthesis controller reduces high-level ambulation to an extended two-state FSM with `Contact` and `No Contact`, where vertical ground reaction force thresholds `>120 N` and `<80 N` define heel-strike and toe-off events. Each state encapsulates dedicated knee and ankle controllers rather than a single fixed trajectory, so the same high-level supervisor can support walking, stairs, and sit/stand behaviors. In `Contact`, the knee torque is composed of `Step-Up`, `Biarticular`, and `Damping` terms, and the bell-shaped `Step-Up` component produces extension assistance for stair ascent and sit-to-stand as a function of knee angle at heel-strike and online-adapted peak-torque geometry. In `No Contact`, the desired knee motion blends a minimum-jerk swing trajectory with a thigh-to-knee synergy term, so the knee can extend smoothly toward heel-strike while still coordinating with residual-thigh motion for activities such as stair climbing. The swing law includes an explicit local timing parameter `t_swing`, shortened from `0.55 s` to `0.45 s` as ankle plantarflexion at toe-off increases, making this a timed two-state supervisor rather than a purely untimed contact detector.

### 3. 逐句溯源

1. 句子 1：The unified powered prosthesis controller reduces high-level ambulation to an extended two-state FSM with `Contact` and `No Contact`, where vertical ground reaction force thresholds `>120 N` and `<80 N` define heel-strike and toe-off events.
   对应摘录：A
2. 句子 2：Each state encapsulates dedicated knee and ankle controllers rather than a single fixed trajectory, so the same high-level supervisor can support walking, stairs, and sit/stand behaviors.
   对应摘录：A, B
3. 句子 3：In `Contact`, the knee torque is composed of `Step-Up`, `Biarticular`, and `Damping` terms, and the bell-shaped `Step-Up` component produces extension assistance for stair ascent and sit-to-stand as a function of knee angle at heel-strike and online-adapted peak-torque geometry.
   对应摘录：B
4. 句子 4：In `No Contact`, the desired knee motion blends a minimum-jerk swing trajectory with a thigh-to-knee synergy term, so the knee can extend smoothly toward heel-strike while still coordinating with residual-thigh motion for activities such as stair climbing.
   对应摘录：C
5. 句子 5：The swing law includes an explicit local timing parameter `t_swing`, shortened from `0.55 s` to `0.45 s` as ankle plantarflexion at toe-off increases, making this a timed two-state supervisor rather than a purely untimed contact detector.
   对应摘录：C

# A new lower limb portable exoskeleton for gait assistance in neurological patients: a proof of concept study - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 MAK 外骨骼写成“顶层控制模式 + gait-phase state machine”的两层结构，给出了 support/swing 下的控制输出、M1/M3 的不同触发机制以及与对侧 swing duration 相关的速度调度，可直接作为 `HSM + T1` 样本。

## 条目 1: Mode-and-phase assistance supervisor for the MAK portable exoskeleton
- 控制对象：`MAK` 下肢便携外骨骼的 active-assistance mode supervisor 与 gait-phase state machine
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向神经系统患者步行辅助的便携外骨骼控制器，顶层有 `F0 / M1 / M3` 三种模式，激活模式下再运行 gait-phase state machine 以在 support 与 swing 间切换不同的控制律。
- 判断：算。对象是真实外骨骼控制系统，不是试验流程；原文明确给出模式层、状态机层、状态内输出与多传感器触发条件，还保留了基于对侧 swing duration 的局部时间语义。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `Sensor description of the MAK device`，行 9-16、26-32
> Since the MAK device accurately measures the angular
> position and the force exerted on the joint, it is therefore
> capable of sending position/speed and force/impedance
> control commands. Figure 2 shows the control scheme
> implemented in the device.
> Based on this general control scheme, three control
> modes (Zero Force Control mode, Mode 1 and Mode 3)
> have been implemented ...
> Modes 1 (M1) and 3 (M3) are active-assistance
> modes ... Figure 3 shows
> the state machine implemented in the device and
> the triggers required for each state transition.

#### 摘录 B
- 出处：第 4 页，Section `Sensor description of the MAK device`，行 36-54
> In the support phase, the control system uses position control, the knee is extended, and a high stiffness value is used, which can be changed according to the strength of the user so that the user can support the weight of his or her own body with the aid of the device. In the swing phase, speed control with a modifiable rigidity is also used to allow the user to apply forces in this phase.
>
> In the M1 control mode, the device detects the user’s movement to change the phase in the state machine and adapts to it within the “assist-as-needed” paradigm. M1 is used as a trigger to change the machine state based on the following data: the knee joint angle, pressure at the shoe insole and force at the knee joint.
>
> In M3, the device maintains a fixed continuous mode in which the device transitions between states in the state machine automatically. In this mode, the level of assistance remains constant. The velocity is dependent on the duration of the swing phase of the other leg.

#### 摘录 C
- 出处：第 5 页，Section `Trial procedure`，行 1-3、20-20
> trigger used by M3 to transition between states in the
> state machine is a function of the knee joint angle and
> pressure recorded from the shoe insole.
>
> Fig. 3 Control scheme of the step decision. Control scheme of the MAK device. Opposite foot: foot from the leg where the MAK device is not attached. *: Only applies for M1

#### 摘录 D
- 出处：第 6 页，Section `Measurements`，行 67-75、98-105
> The MAK is able to record data from the wearer, such
> as the knee joint position, shoe insole pressure at each
> sensor and the center of pressure (CoP). The data were
> recorded at a sampling rate of 100 Hz.
> The joint angles of the knees were determined by the
> data from the encoder embedded in the actuator assembly ...
>
> A gait cycle was defined as a cycle from heel strike to
> the following ipsilateral heel strike, which consisted of
> two phases: 1) stance phase ... and 2) swing
> phase, when the foot was off of the ground and moved
> forwards. A sensor was considered active when its measurement exceeded a given threshold value to avoid false positives.

### 2. 基于原文整理后的自然语言描述

The MAK portable exoskeleton is controlled as a two-level assistance supervisor: a top level selects among `F0`, `M1`, and `M3`, while the active-assistance modes run an internal gait-phase state machine. Inside that phase machine, the support state uses position control with an extended knee and user-adjustable high stiffness so the device can bear body weight, whereas the swing state switches to speed control with modifiable rigidity. `M1` is an assist-as-needed mode in which state transitions follow the user’s own movement through knee-angle, insole-pressure, and knee-joint-force triggers. `M3` keeps assistance constant and advances the state machine automatically from knee angle and insole pressure, with the commanded velocity explicitly depending on the swing-phase duration of the opposite leg, so the controller embeds local timing semantics rather than being purely untimed.

### 3. 逐句溯源

1. 句子 1：The MAK portable exoskeleton is controlled as a two-level assistance supervisor: a top level selects among `F0`, `M1`, and `M3`, while the active-assistance modes run an internal gait-phase state machine.
   对应摘录：A
2. 句子 2：Inside that phase machine, the support state uses position control with an extended knee and user-adjustable high stiffness so the device can bear body weight, whereas the swing state switches to speed control with modifiable rigidity.
   对应摘录：B, D
3. 句子 3：`M1` is an assist-as-needed mode in which state transitions follow the user’s own movement through knee-angle, insole-pressure, and knee-joint-force triggers.
   对应摘录：B
4. 句子 4：`M3` keeps assistance constant and advances the state machine automatically from knee angle and insole pressure, with the commanded velocity explicitly depending on the swing-phase duration of the opposite leg, so the controller embeds local timing semantics rather than being purely untimed.
   对应摘录：B, C

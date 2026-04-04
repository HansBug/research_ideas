# Design and Control of a Pneumatically Actuated Transtibial Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把气动踝关节假肢的四相步态分段、阻抗参数和基于角度/角速度阈值的实时切换条件写得很完整，可直接作为 powered ankle gait-phase 控制样本。

## 条目 1: Four-phase impedance controller for the pneumatically actuated transtibial prosthesis
- 控制对象：气动驱动经胫截肢踝关节假肢的实时步态相位控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 powered ankle prosthesis controller，用有限状态机把步态切成 `Early Stance / Middle Stance / Late Stance / Swing` 四相，并在各相位下切换不同的虚拟弹簧阻抗和推力输出。
- 判断：算。对象是真实经胫假肢控制器，原文明确给出了状态集合、切换事件、角度阈值、角速度方向和状态相关输出。

### 1. 原文摘录

#### 摘录 A
- 出处：第 7-8 页，Section `3.1 Biomechanical Analysis`
> The gait cycle is divided into four distinct stages. Event A: Heel Strike ... Phase #1 (A -> B): Early Stance (ES). Event B: Foot Flat ... Phase #2 (B -> C): Middle Stance (MS). Event C: Maximum Dorsiflexion ... Phase #3 (C -> D): Late Stance (LS). Event D: Toe Off ... Phase #4 (D -> A): Swing (SW).

#### 摘录 B
- 出处：第 8 页，Section `3.2 Impedance Modeling`
> Phase #1 (Early Stance): The ankle functions like a spring with moderate stiffness ... Phase #2 (Middle Stance): The ankle functions like a very stiff spring ... Phase #3 (Late Stance): The ankle functions like a stiff spring ... with an equilibrium position significantly less than that in the Phase #2 ... constituting the powered push-off in walking. Phase #4 (Swing): The ankle functions like a spring with very low stiffness, returning the ankle to a slightly dorsiflexed position.

#### 摘录 C
- 出处：第 8-9 页，Section `3.3 Controller Implementation`
> For the implementation of the controller, a finite-state machine is constructed and executed in real-time ... the switching conditions in this work are constructed based solely on the ankle angle signal (theta) and its derivative ... heel strike is detected according to the onset of plantarflexion ... an additional condition (theta < Theta1) is imposed ... foot flat is detected according to the onset of dorsiflexion ... maximum dorsiflexion is detected when the ankle angle exceeds ... Theta2 ... toe off is detected when the ankle angle decreases below ... Theta3.

### 2. 基于原文整理后的自然语言描述

The controller for the pneumatic transtibial prosthesis segments one walking cycle into four discrete states: `Early Stance`, `Middle Stance`, `Late Stance`, and `Swing`, anchored by the gait events `Heel Strike`, `Foot Flat`, `Maximum Dorsiflexion`, and `Toe Off`. Each state uses a different impedance law for the ankle joint, so the prosthesis behaves like a moderate spring during early stance, a very stiff energy-absorbing spring during middle stance, a lower-stiffness but more plantarflexion-biased spring during late stance to generate powered push-off, and a weak return spring during swing to bring the foot back to a slightly dorsiflexed posture. The switching logic is not driven by external foot switches but by measured ankle angle and ankle angular velocity alone, which makes the finite-state controller self-contained at the prosthesis level. In real time, heel strike is recognized by the onset of plantarflexion together with `theta < Theta1`, foot flat by the onset of dorsiflexion, maximum dorsiflexion by `theta > Theta2`, and toe off by `theta < Theta3`. The selected state then determines the target impedance torque, which is converted into desired actuator force and tracked through a PID-controlled pneumatic valve.

### 3. 逐句溯源

1. 句子 1：The controller for the pneumatic transtibial prosthesis segments one walking cycle into four discrete states: `Early Stance`, `Middle Stance`, `Late Stance`, and `Swing`, anchored by the gait events `Heel Strike`, `Foot Flat`, `Maximum Dorsiflexion`, and `Toe Off`.
   对应摘录：A
2. 句子 2：Each state uses a different impedance law for the ankle joint, so the prosthesis behaves like a moderate spring during early stance, a very stiff energy-absorbing spring during middle stance, a lower-stiffness but more plantarflexion-biased spring during late stance to generate powered push-off, and a weak return spring during swing to bring the foot back to a slightly dorsiflexed posture.
   对应摘录：B
3. 句子 3：The switching logic is not driven by external foot switches but by measured ankle angle and ankle angular velocity alone, which makes the finite-state controller self-contained at the prosthesis level.
   对应摘录：C
4. 句子 4：In real time, heel strike is recognized by the onset of plantarflexion together with `theta < Theta1`, foot flat by the onset of dorsiflexion, maximum dorsiflexion by `theta > Theta2`, and toe off by `theta < Theta3`.
   对应摘录：C
5. 句子 5：The selected state then determines the target impedance torque, which is converted into desired actuator force and tracked through a PID-controlled pneumatic valve.
   对应摘录：B, C

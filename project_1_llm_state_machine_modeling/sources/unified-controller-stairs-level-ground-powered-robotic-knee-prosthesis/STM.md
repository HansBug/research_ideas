# A Unified Controller for Natural Ambulation on Stairs and Level Ground with a Powered Robotic Knee Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 powered robotic knee prosthesis 的 `Contact / No Contact` 两态统一控制器、GRF guard、step-up torque 与 minimum-jerk swing 明确写出，可直接作为紧凑但高细节的 unified prosthesis FSM 样本。

## 条目 1: Two-state contact-no-contact controller for powered robotic knee prosthesis on level ground and stairs
- 控制对象：可同时覆盖平地与楼梯行走的主动膝假肢统一监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个主动膝假肢的二态统一控制器，用 `Contact` 和 `No Contact` 两个状态覆盖 walking 与 stair ambulation，并在状态切换时采样膝角、髋角、GRF 和 elapsed time 以连续调参。
- 判断：算。对象是真实 powered robotic knee prosthesis controller，原文明确给出状态、GRF 门限、状态内 torque / trajectory 组成以及时间相关的 swing planning。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section `A. Unified Controller`
> The proposed unified controller uses a simple finite-state machine (FSM) with two states, Contact (C) and No Contact (NC) ... When the axial ground reaction force (GRF) is greater than 60 N, the FSM switches to Contact. When the GRF is less than 20 N, the FSM switches to No Contact. Dedicated controllers are used in Contact and No Contact states. The transition between Contact and No Contact is defined as Toe Off. The transition between No Contact and Contact is defined as Toe On. The values of knee position, knee velocity, thigh position, and elapsed time, sampled at the transition between states, are used to continuously adapt the prosthesis behavior.

#### 摘录 B
- 出处：第 3-4 页，Section `A. Unified Controller`
> The Contact controller defines the desired knee torque TKnee as the sum of three components ... The first component is the step-up torque TStep-Up ... The second component ... is the biarticular torque TBiart ... The third component ... is the damping torque TDamping ... If the knee is flexing, then the flexion damping is used ... While the knee is extending, the extension damping is used.

#### 摘录 C
- 出处：第 4-5 页，Section `A. Unified Controller`
> The No Contact controller defines the desired knee position (θKneeDesired) as the sum of two components ... The first component is a minimum jerk trajectory θMJ ... given θKneeToe Off and a desired movement duration Timedes, the proposed controller calculates a trajectory that minimizes the changes in acceleration. Timedes is proportional to the duration of the previous Contact state. The second component ... is based on a synergistic movement of the thigh and knee θSyn ... KSyn is continuously adapted during the No Contact state.

#### 摘录 D
- 出处：第 6-7 页，Section `III. Results`
> At Toe On (the transition between No Contact and Contact), the knee is fully extended ... As the user rolls over the prosthesis ... TBiart increases while TDamping goes to zero, causing the knee to flex in late stance ... a minimum-jerk trajectory is generated at Toe Off, which allows for adequate clearance during swing and drives the knee to full extension in preparation for the subsequent heel strike.

### 2. 基于原文整理后的自然语言描述

The powered robotic knee prosthesis is controlled by a compact two-state EFSM in which `Contact` and `No Contact` replace activity-specific gait machines and therefore unify level walking and stair ambulation under one shared supervisory structure. The switch to `Contact` occurs when axial GRF rises above `60 N`, the switch to `No Contact` occurs when GRF falls below `20 N`, and each transition snapshots knee position, knee velocity, thigh position, and elapsed time so the controller can adapt the next state's behavior. In `Contact`, the knee torque is synthesized from a step-up term, a biarticular term linked to ankle torque and thigh posture, and a damping term whose coefficient changes according to knee velocity and pose. In `No Contact`, the desired knee motion is the sum of a minimum-jerk trajectory and a thigh-knee synergy term, where the desired swing duration is scaled from the previous `Contact` duration and the synergy gain keeps adapting during swing. The resulting controller is small in state count but rich in state-local logic, which is exactly why it is a strong STM sample for unified locomotion control rather than a trivial two-state abstraction.

### 3. 逐句溯源

1. 句子 1：The powered robotic knee prosthesis is controlled by a compact two-state EFSM in which `Contact` and `No Contact` replace activity-specific gait machines and therefore unify level walking and stair ambulation under one shared supervisory structure.
   对应摘录：A
2. 句子 2：The switch to `Contact` occurs when axial GRF rises above `60 N`, the switch to `No Contact` occurs when GRF falls below `20 N`, and each transition snapshots knee position, knee velocity, thigh position, and elapsed time so the controller can adapt the next state's behavior.
   对应摘录：A
3. 句子 3：In `Contact`, the knee torque is synthesized from a step-up term, a biarticular term linked to ankle torque and thigh posture, and a damping term whose coefficient changes according to knee velocity and pose.
   对应摘录：B
4. 句子 4：In `No Contact`, the desired knee motion is the sum of a minimum-jerk trajectory and a thigh-knee synergy term, where the desired swing duration is scaled from the previous `Contact` duration and the synergy gain keeps adapting during swing.
   对应摘录：C
5. 句子 5：The resulting controller is small in state count but rich in state-local logic, which is exactly why it is a strong STM sample for unified locomotion control rather than a trivial two-state abstraction.
   对应摘录：A, B, C, D

# Control of a Robotic Knee Exoskeleton for Assistance and Rehabilitation Based on Motion Intention from sEMG - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `ALLOR` 膝外骨骼的 `HMIR -> FSM -> low-level controllers` 主链、六类 motion class、walking 子相位调制和 `downtime / uptime` 局部时间语义，可直接提取为高质量监督控制样本。

## 条目 1: Motion-intention supervisory controller for the ALLOR robotic knee exoskeleton
- 控制对象：主动膝关节外骨骼 `ALLOR` 的中高层监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个根据 `sEMG` 识别的人体运动意图，在起立、坐下、屈伸、站立休止和步行之间切换控制模式的外骨骼监督控制器。
- 判断：算。对象是真实医疗辅助外骨骼控制器，不是康复流程；原文明确给出状态类目、组序、输出控制器映射、gait phase 参数调制和局部时间参数，能恢复成完整控制链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Figure 1 `Block diagram of the proposed system`
> The output of the HMIR is used to select a state with a finite state machine (FSM) defining both wished admittance and parameters for the velocity and trajectory low-level controllers to command the knee exoskeleton ALLOR.

#### 摘录 B
- 出处：第 4 页，Section `Finite state machinne and low level controllers`
> A finite state machine (FSM) is used to establish a model for the transitions of the sequences: siting movements G1 (SU-F/E-RSD) and standing movements G2 (RSU-W-SD), according to the user’s motion intention.
>
> Once the command of the HMIR is received, the FSM uploads the corresponding parameters ... to activate the low-level controller.
>
> The admittance controller is employed to assist the knee joint during W state and to provide knee support during RSU position. On the other hand, the velocity controller is employed to execute F/E movements, and the trajectory controller is employed to execute movements in both SD and SU states.

#### 摘录 C
- 出处：第 5 页，Section `Finite state machinne and low level controllers`
> The gait phases considered are: initial contact, defined by the heel contact; mid-stance, defined by a flat foot contact; terminal stance, defined by the heel off; and swing, defined by the foot-off.
>
> During the gait cycle, different G values for each gait sub-phase are applied. In order to obtain a smoother response, an increment of G during a time tΔ is considered.
>
> where tΔ represents the time in seconds ... For our approach, the gains have the following proportions: 4 for IC, 7 for MS, 2 for TS and 1 for SW.

#### 摘录 D
- 出处：第 5 页，Section `Finite state machinne and low level controllers`
> For the F/E state, ... the inputs qmin and qmax represent the limits of the F/E movement, and downtime and uptime define the periods of time (t) in seconds in which the leg stays at extension and flexion, respectively.
>
> Additionally, at the motion class F/E, a strategy to detect the user’s intention of stopping was included ... if the user has a intention of stopping, GFE approaches to zero, stopping the movement.

#### 摘录 E
- 出处：第 6 页，Section `Finite state machinne and low level controllers`
> Although in this approach the user’s motor intention commands the execution of the movements, to start the new desired movement it is necessary to have completed the previous movement.
>
> It is considered that the W state is completed when two steps are executed by the user ... For siting movements previous to the F/E state it is necessary to complete the SD state.

### 2. 基于原文整理后的自然语言描述

The ALLOR robotic knee exoskeleton is supervised by an intention-driven FSM that maps six motion classes, `SU`, `SD`, `F/E`, `W`, `RSU`, and `RSD`, into two admissible movement sequences `G1 = SU -> F/E -> RSD` and `G2 = RSU -> W -> SD`. Once the HMIR classifier recognizes the user’s intended class from `sEMG`, the FSM selects the corresponding low-level actuation mode, using trajectory control for `SU/SD`, velocity control for `F/E`, and admittance-based assistance for `W`, `RSU`, and `RSD`. In walking, the supervisor further refines the `W` state by distinguishing `initial contact`, `mid-stance`, `terminal stance`, and `swing`, applying phase-specific gain proportions `4/7/2/1` and ramping each gain over a computed `tΔ` so that gait assistance varies smoothly across the cycle. In the `F/E` state, the controller uses `qmin / qmax` together with `downtime / uptime` to bound the knee excursion and dwell at flexion or extension, while a torque-driven `tanh` gain lets the user slow down or stop the motion by pushing `GFE` toward zero. The supervisor only accepts a new intention after the previous action has completed, so walking must finish its required steps and sit-down must complete before the following flexion-extension sequence can begin.

### 3. 逐句溯源

1. 句子 1：The ALLOR robotic knee exoskeleton is supervised by an intention-driven FSM that maps six motion classes, `SU`, `SD`, `F/E`, `W`, `RSU`, and `RSD`, into two admissible movement sequences `G1 = SU -> F/E -> RSD` and `G2 = RSU -> W -> SD`.
   对应摘录：B
2. 句子 2：Once the HMIR classifier recognizes the user’s intended class from `sEMG`, the FSM selects the corresponding low-level actuation mode, using trajectory control for `SU/SD`, velocity control for `F/E`, and admittance-based assistance for `W`, `RSU`, and `RSD`.
   对应摘录：A, B
3. 句子 3：In walking, the supervisor further refines the `W` state by distinguishing `initial contact`, `mid-stance`, `terminal stance`, and `swing`, applying phase-specific gain proportions `4/7/2/1` and ramping each gain over a computed `tΔ` so that gait assistance varies smoothly across the cycle.
   对应摘录：C
4. 句子 4：In the `F/E` state, the controller uses `qmin / qmax` together with `downtime / uptime` to bound the knee excursion and dwell at flexion or extension, while a torque-driven `tanh` gain lets the user slow down or stop the motion by pushing `GFE` toward zero.
   对应摘录：D
5. 句子 5：The supervisor only accepts a new intention after the previous action has completed, so walking must finish its required steps and sit-down must complete before the following flexion-extension sequence can begin.
   对应摘录：E

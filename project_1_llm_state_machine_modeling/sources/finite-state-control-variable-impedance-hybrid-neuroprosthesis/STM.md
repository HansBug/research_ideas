# Finite State Control of a Variable Impedance Hybrid Neuroprosthesis for Locomotion After Paralysis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文完整给出 `VIKM-HNP` 的五态 gait-phase FSM、阈值 guard、并行 `FNS + FSM + torque controller` 结构，以及各状态下阻尼与刺激的具体控制律，可直接作为高质量混合神经假体样本。

## 条目 1: Five-state VIKM-HNP gait controller with parallel FNS supervision
- 控制对象：`VIKM-HNP` 混合神经假体中协调 `VIKM` 阻尼器与 `FNS` 刺激模式的步行监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把 `FNS` 步态刺激、`VIKM` 阻尼器和阈值式 gait-phase 判定耦合起来的混合神经假体控制器，用于在 stance 各阶段调节膝关节屈曲并在 swing 中放开关节。
- 判断：算。对象是真实混合神经假体控制器，不是方法流程；原文明确给出五个离散 gait states、状态切换 guard、并行模块和各状态下的阻尼/刺激动作。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，Section `II. Control System Design`
> Here, we present the design of a finite state machine that divides FNS-driven gait into discrete phases for feedback control to modulate stimulation and activate the VIKM to control knee motion during gait.
>
> The goal is to activate the VIKM to control knee flexion during loading response and pre-swing phases, and to lock the knee during terminal stance ... The VIKM is inactive during mid-stance and swing, when FNS controls knee motion.
>
> The control system of the VIKM-HNP has three modules which run in parallel to achieve these objectives: the FNS controller, the VIKM-HNP finite state machine, the VIKM torque controller.

#### 摘录 B
- 出处：第 4 页，Section `II.B. VIKM-HNP Finite State Machine`
> The gait cycle was split into five phases based on knee behavior ... loading response ... mid-stance ... terminal stance ... pre-swing ... swing ...
>
> The VIKM-HNP finite state machine utilized sensors mounted on the brace (knee angle) and under the feet (heel and toe ground contact) to classify the gait cycle into 5 discrete states ...
>
> The VIKM-HNP finite state machine transitioned between states using feedback from the sensors and from the FNS controller. State transitions were based on knee angle and angular velocity thresholds ...

#### 摘录 C
- 出处：第 5 页，Section `II.B. VIKM-HNP Finite State Machine`
> State 1 (loading response) began when either the ipsilateral knee extended beyond Threshold 1 ... or the ipsilateral foot contacted the ground. During State 1, the VIKM damper was activated ... Simultaneously, the VIKM-HNP controller modified the baseline FNS pattern in real time by turning off knee extensor stimulation.
>
> The controller transitioned to State 2 (mid-stance) if knee flexion passed Threshold 2 ... or the contralateral foot came off the ground. During mid-stance, knee extensor stimulation was restored while the VIKM damper was deactivated ...
>
> When the knee reached near full extension ... the damper was reactivated while FNS of the knee extensors was simultaneously deactivated as the controller moved to State 3 (terminal stance).
>
> The transition to State 4 (pre-swing) ... required both contralateral foot contact and the pre-swing feedback signal to be high ... Once the ipsilateral foot left the ground, the damper was turned off and stimulation returned to the baseline pattern to allow unencumbered knee motion during swing, after which the cycle repeats.

#### 摘录 D
- 出处：第 7 页，Section `II.C. VIKM Torque Controller`
> The torque controller operated in three different modes for loading response, terminal stance, and pre-swing.
>
> During loading response, controlled flexion is maintained up to Threshold 2 ... the damping level was increased if the knee flexion velocity exceeded Threshold 5 ...
>
> In terminal stance phase the knee was locked in full extension ... the damper was activated at maximal resistance ...
>
> Control of the VIKM during pre-swing was similar to loading response ... the MR damper was initially inactive during pre-swing phase to allow knee flexion ... if knee flexion velocity exceeded Threshold 5, the damper was activated ...

### 2. 基于原文整理后的自然语言描述

The VIKM-HNP gait supervisor is an extended finite-state controller that runs in parallel with a baseline FNS controller and a dedicated VIKM torque controller. It partitions FNS-driven walking into five discrete states, `loading response`, `mid-stance`, `terminal stance`, `pre-swing`, and `swing`, using brace-mounted knee-angle sensing, heel and toe contact sensing, and supervisory FNS feedback signals. In `loading response`, foot contact or extension beyond Threshold 1 enters the state, turns the VIKM damper on, and suppresses knee extensor stimulation; `mid-stance` restores extensor stimulation with the damper mostly off; `terminal stance` reactivates maximal resistance to lock the knee near full extension; and `pre-swing` is admitted only when contralateral foot contact and a pre-swing feedback signal are simultaneously high. Once the ipsilateral foot leaves the ground, the controller drops the damper and returns to baseline stimulation so swing can proceed without constraint. The torque layer then refines these states with mode-specific damping laws, maintaining controlled flexion in loading response, full extension locking in terminal stance, and passive-but-protected flexion in pre-swing whenever angle or velocity thresholds indicate imminent collapse.

### 3. 逐句溯源

1. 句子 1：The VIKM-HNP gait supervisor is an extended finite-state controller that runs in parallel with a baseline FNS controller and a dedicated VIKM torque controller.
   对应摘录：A
2. 句子 2：It partitions FNS-driven walking into five discrete states, `loading response`, `mid-stance`, `terminal stance`, `pre-swing`, and `swing`, using brace-mounted knee-angle sensing, heel and toe contact sensing, and supervisory FNS feedback signals.
   对应摘录：B
3. 句子 3：In `loading response`, foot contact or extension beyond Threshold 1 enters the state, turns the VIKM damper on, and suppresses knee extensor stimulation; `mid-stance` restores extensor stimulation with the damper mostly off; `terminal stance` reactivates maximal resistance to lock the knee near full extension; and `pre-swing` is admitted only when contralateral foot contact and a pre-swing feedback signal are simultaneously high.
   对应摘录：C
4. 句子 4：Once the ipsilateral foot leaves the ground, the controller drops the damper and returns to baseline stimulation so swing can proceed without constraint.
   对应摘录：C
5. 句子 5：The torque layer then refines these states with mode-specific damping laws, maintaining controlled flexion in loading response, full extension locking in terminal stance, and passive-but-protected flexion in pre-swing whenever angle or velocity thresholds indicate imminent collapse.
   对应摘录：D

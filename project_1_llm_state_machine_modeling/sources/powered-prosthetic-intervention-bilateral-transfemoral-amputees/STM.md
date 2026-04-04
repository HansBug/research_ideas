# A Powered Prosthetic Intervention for Bilateral Transfemoral Amputees - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双侧主动股骨假肢的三态 gait controller、对侧信号联锁和 `2 s` timeout 写得很清楚，可直接作为 bilateral prosthesis coordination 样本。

## 条目 1: Bilaterally coordinated three-state gait controller for powered transfemoral prostheses
- 控制对象：双侧主动股骨假肢共享 CAN 信号的并行步态监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个双侧 transfemoral powered prostheses 的并行控制器，每条腿运行 `stance / push-off / swing` 三态机，并通过对侧步态状态、步幅百分比和 timeout 条件实现跨腿联锁。
- 判断：算。对象是真实双侧假肢控制系统，原文明确给出了状态集合、触发阈值、状态内 knee/ankle 输出行为，以及 bilateral safety gating 逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4-5 页，Section `B. Walking Controller`
> The original control system for the unilateral transfemoral prosthesis consisted of a finite state-based impedance control framework ... The bilateral controller has three distinct states for the level walking gait cycle ... In the stance state, the impedance parameters are constant ... In the push-off state, the ankle impedance parameters are also constant, though the equilibrium position of the ankle is moved ... to generate the energy and motion for powered push-off.

#### 摘录 B
- 出处：第 6 页，Section `B. Walking Controller`
> During push off ... the knee angle and ankle angle have an approximately linear correlation ... This relationship is used to continuously calculate the knee equilibrium position in the push off state. As a result, the knee and ankle angles are kinematically linked in this state ... The third and final state consists of the swing phase of gait ... the swing phase of the walking controller has been reduced to a single state that executes appropriate trajectories at the knee and ankle joints ... The shape and duration of the trajectories are determined by an estimate of the cadence.

#### 摘录 C
- 出处：第 7 页，Section `C. Inter-prosthesis Communication`
> Using the control signals exchanged between the prostheses, each prosthesis implements several safety features ... Neither prosthesis can enter the push off state a second time before the contralateral prosthesis has done so. There is a 2 second time-out on this feature ... once one prosthesis has entered the push off state, the contralateral prosthesis is locked out from also entering the push off state until the ipsilateral prosthesis has reached the last 10% of the stride.

#### 摘录 D
- 出处：第 16 页，Figure `Fig. 2`
> The finite state machines executed by the prostheses. θa is the ankle joint angle, which is compared to a predetermined threshold, θth, to trigger the transition into the ankle push off state. Fs is the axial load in the prosthetic shank, which is compared to a predetermined threshold, Fth, to trigger the transition into swing. The swing state executes a trajectory and automatically reverts to the stance state when the trajectory ends, which corresponds to the percentage of stride, ρs, reaching 100%. The red conditions on the transition from State 0 to State 1 are safety conditions that are dependent upon the contralateral signals cρs and cS.

### 2. 基于原文整理后的自然语言描述

Each powered transfemoral prosthesis in the bilateral system runs a three-state gait controller with `stance`, `push-off`, and `swing` states, and both prostheses exchange synchronized control signals over CAN so that the two local state machines are coordinated rather than independent. In `stance`, both joints behave as locally passive, over-damped support elements; in `push-off`, the ankle equilibrium is shifted to a plantarflexed value while the knee equilibrium is continuously coupled to ankle angle so the user can drive synchronized knee yield and ankle power generation; and in `swing`, the controller executes cadence-dependent knee and ankle trajectories before automatically returning to `stance`. The transition into `push-off` is triggered by ankle angle thresholds but is additionally guarded by contralateral stride-percentage and contralateral-state conditions, while the transition into `swing` is triggered by shank axial load dropping below a threshold. The controller therefore extends a basic impedance FSM into an expanded bilateral machine that carries extra stride counters, contralateral state variables, and an automatic `2 s` timeout to prevent unsafe repeated push-off. This makes the paper especially valuable as a coordinated multi-controller STM sample rather than a single-limb gait-phase controller only.

### 3. 逐句溯源

1. 句子 1：Each powered transfemoral prosthesis in the bilateral system runs a three-state gait controller with `stance`, `push-off`, and `swing` states, and both prostheses exchange synchronized control signals over CAN so that the two local state machines are coordinated rather than independent.
   对应摘录：A, C
2. 句子 2：In `stance`, both joints behave as locally passive, over-damped support elements; in `push-off`, the ankle equilibrium is shifted to a plantarflexed value while the knee equilibrium is continuously coupled to ankle angle so the user can drive synchronized knee yield and ankle power generation; and in `swing`, the controller executes cadence-dependent knee and ankle trajectories before automatically returning to `stance`.
   对应摘录：A, B
3. 句子 3：The transition into `push-off` is triggered by ankle angle thresholds but is additionally guarded by contralateral stride-percentage and contralateral-state conditions, while the transition into `swing` is triggered by shank axial load dropping below a threshold.
   对应摘录：C, D
4. 句子 4：The controller therefore extends a basic impedance FSM into an expanded bilateral machine that carries extra stride counters, contralateral state variables, and an automatic `2 s` timeout to prevent unsafe repeated push-off.
   对应摘录：C, D
5. 句子 5：This makes the paper especially valuable as a coordinated multi-controller STM sample rather than a single-limb gait-phase controller only.
   对应摘录：A, B, C, D

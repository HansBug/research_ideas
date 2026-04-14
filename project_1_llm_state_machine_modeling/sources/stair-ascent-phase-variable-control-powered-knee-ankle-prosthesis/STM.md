# Stair Ascent Phase-Variable Control of a Powered Knee-Ankle Prosthesis - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 stair-ascent powered knee-ankle prosthesis 的相位估计写成 `S1-S4` FSM，状态按 `MHF / MHE / FC` 和 push-off onset 切换，能直接抽为双 A 样本；但与既有膝踝假肢相位簇较近，作为降采样保留。

## 条目 1: Four-state stair-ascent phase-variable supervisor for a powered knee-ankle prosthesis

- 控制对象：医疗设备与生命支持控制领域的主动膝踝假肢 stair-ascent 相位变量监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（膝踝假肢步态相位）

### 0. 条目识别与判定

- 一句话说明：这是一个用于主动膝踝假肢 stair ascent 的四态相位变量监督器，用 `MHF` 起止 gait cycle，并通过 `FC`、push-off onset 和 `MHE` 切换相位定义。
- 判断：算。对象是真实动力假肢控制器；原文明确给出 `S1-S4` 状态定义、转移条件、`FC` 与 `MHF` 事件、关节 virtual constraints 和低层位置控制输出。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> We build on previous phase variable-based control methods for walking and propose a stair ascent controller driven by the motion of the user's residual thigh. ... We redefine the gait cycle to begin at the point of maximum hip flexion instead of heel strike to improve the phase estimate. ... Thus, this controller allows powered knee-ankle prostheses to perform net positive mechanical work to assist stair ascent.

#### 摘录 B

- 出处：第 2 页，Section `A. Phase Variable`
> In addition, modifications to the FSM controlling the transitions between the ascending and descending equations were required. The updated state definitions and their transition criteria are shown in Fig. 3. States S1 and S2 of the FSM correspond to the descending definition of s while S3 and S4 correspond to the ascending definition. The latter part of S1 and all of S2 and S3 are part of the stance phase of the gait cycle, while S4 and the beginning of S1 capture the swing phase. This is denoted within the FSM as FC = 1 ... Successful MHF detection is denoted as MHF = 1 ...

#### 摘录 C

- 出处：第 3 页，Figure `3` caption
> S1 begins in swing after MHF has occurred and continues into stance until the onset of push-off onset where it then transitions to S2. S2 continues from push-off onset to the point of MHE where the average thigh velocity over a 40 ms window becomes positive, transitioning to S3. The state machine stays in S3 until FC = 0, where it then transitions to S4. Phase cannot decrease in S3 or S4. S4 continues until MHF = 1 and then transitions back to S1.

#### 摘录 D

- 出处：第 2-3 页，Sections `B. Virtual Constraints` and `C. Low-Level Position Control`
> A Fourier series was used to represent the average able-bodied knee and ankle kinematics as functions of gait phase, termed the virtual constraints. ... The interpolated reference knee and ankle trajectories were input to the DFT to calculate the coefficients ... Low-level position controllers for each joint enforce the reference joint angles.

### 2. 基于原文整理后的自然语言描述

The stair-ascent prosthesis controller is an EFSM that redefines the gait cycle to start and end at maximum hip flexion so that residual thigh angle can remain a usable phase variable during stair ascent. Its four states are `S1`, `S2`, `S3`, and `S4`: `S1` begins in swing after `MHF`, continues into stance, and switches to `S2` at push-off onset; `S2` continues until `MHE`; `S3` runs the remaining stance interval; and `S4` covers swing until the next `MHF` event. The guards include binary foot contact `FC`, real-time `MHF` detection, push-off onset, and a `40 ms` averaged thigh-velocity condition for detecting `MHE`. `S1-S2` use the descending phase-variable definition, `S3-S4` use the ascending definition, and phase is prevented from decreasing in `S3` and `S4` to avoid inconsistent joint commands. The state-selected phase value drives Fourier-series virtual constraints for desired knee and ankle angles, which low-level position controllers enforce to produce net-positive knee and ankle work during stair ascent.

### 3. 逐句溯源

1. 句子 1：The stair-ascent prosthesis controller is an EFSM that redefines the gait cycle to start and end at maximum hip flexion so that residual thigh angle can remain a usable phase variable during stair ascent.
   对应摘录：A, B
2. 句子 2：Its four states are `S1`, `S2`, `S3`, and `S4`: `S1` begins in swing after `MHF`, continues into stance, and switches to `S2` at push-off onset; `S2` continues until `MHE`; `S3` runs the remaining stance interval; and `S4` covers swing until the next `MHF` event.
   对应摘录：B, C
3. 句子 3：The guards include binary foot contact `FC`, real-time `MHF` detection, push-off onset, and a `40 ms` averaged thigh-velocity condition for detecting `MHE`.
   对应摘录：B, C
4. 句子 4：`S1-S2` use the descending phase-variable definition, `S3-S4` use the ascending definition, and phase is prevented from decreasing in `S3` and `S4` to avoid inconsistent joint commands.
   对应摘录：B, C
5. 句子 5：The state-selected phase value drives Fourier-series virtual constraints for desired knee and ankle angles, which low-level position controllers enforce to produce net-positive knee and ankle work during stair ascent.
   对应摘录：A, D

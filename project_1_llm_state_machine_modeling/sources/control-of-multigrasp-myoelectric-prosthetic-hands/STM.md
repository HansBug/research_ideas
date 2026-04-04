# A Method for the Control of Multigrasp Myoelectric Prosthetic Hands - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 multigrasp prosthetic hand 的 `7` 态 / `9` 姿态 event-driven control、`flexion / extension / co-contraction / rest` 输入、position/force threshold 与 actuator-subset coordination 写成了完整控制主链，可直接作为高质量 `EFSM + T0` 样本。

## 条目 1: Seven-state posture-selection controller for the multigrasp prosthetic hand
- 控制对象：多指假手的 multigrasp myoelectric coordination controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 multigrasp prosthetic hand 的离散姿态选择控制器，它用两路 `EMG`、digit position/force 与 co-contraction 事件在 `7` 个状态、`9` 个姿态之间切换，并按当前状态只激活相邻转移所需的 actuator subset。
- 判断：算。对象是真实 prosthetic hand controller，不是单纯离线分类器；原文明确给出了状态集合、输入事件、position/force guard、co-contraction 分支和状态相关 actuator coordination。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section `II`
> To coordinate the motion of the digits, the MMC incorporates an event driven finite-state control structure. The states ... include the thumb reposition (platform), point, hook, lateral pinch, thumb opposition, tip, and combined cylindrical/spherical/tripod postures ... seven states, and nine possible grasps/postures.

#### 摘录 B
- 出处：第 4 页，Section `II`
> The user navigates the state chart by four essential inputs ... flexion, extension, co-contraction, and rest. ... Co-contraction toggles between the opposition and reposition states ... relaxation ... halts movement within the state chart.

#### 摘录 C
- 出处：第 4 页，Section `II`
> Transitions within the state chart are based on logical conditions that operate on measured digit displacements ... measured digit forces, and/or measured EMG levels ... The behavior of the hand within each state is determined by a coordination controller ... The actuators which are active are always those associated with transitions to adjacent states.

#### 摘录 D
- 出处：第 4-5 页，Section `II`
> If the digit flexion or force exceeds a certain threshold ... a state transition will occur, and the hand will transition to the point posture ... If flexion continues ... digit II will continue to increase until its displacement or force exceeds a certain threshold, at which point the hand will transition to the hook posture.

#### 摘录 E
- 出处：第 6 页，Section `III`
> The EMG signals of each subject were calibrated by establishing normalization parameters and co-contraction threshold levels ... A dead band of 10% of full range was utilized ... thresholds were established for each EMG channel based on an exhaustive search.

### 2. 基于原文整理后的自然语言描述

The multigrasp prosthetic hand is controlled by an event-driven extended state machine whose discrete backbone contains `7` states covering `9` reachable grasps and postures, including `platform`, `point`, `hook`, `lateral pinch`, `opposition`, `tip`, and the combined `cylindrical / spherical / tripod` branch. The controller is driven by four EMG-level events, `flexion`, `extension`, `co-contraction`, and `rest`, where co-contraction switches the thumb between the reposition and opposition branches and rest freezes the current configuration. State transitions are guarded by measured digit displacement, measured grasp force, and EMG conditions rather than by a fixed sequence, so closure can advance from `platform` to `point` and then to `hook` only when the relevant position or force thresholds are actually exceeded. Inside each state, a coordination controller activates only the actuators associated with adjacent transitions, which couples the discrete posture graph directly to state-specific motor subsets. Before operation, the two EMG channels are normalized, a `10%` dead band is applied, and co-contraction thresholds are calibrated per user, so the posture supervisor keeps explicit control over both branch selection and transition triggering.

### 3. 逐句溯源

1. 句子 1：The multigrasp prosthetic hand is controlled by an event-driven extended state machine whose discrete backbone contains `7` states covering `9` reachable grasps and postures, including `platform`, `point`, `hook`, `lateral pinch`, `opposition`, `tip`, and the combined `cylindrical / spherical / tripod` branch.
   对应摘录：A
2. 句子 2：The controller is driven by four EMG-level events, `flexion`, `extension`, `co-contraction`, and `rest`, where co-contraction switches the thumb between the reposition and opposition branches and rest freezes the current configuration.
   对应摘录：B
3. 句子 3：State transitions are guarded by measured digit displacement, measured grasp force, and EMG conditions rather than by a fixed sequence, so closure can advance from `platform` to `point` and then to `hook` only when the relevant position or force thresholds are actually exceeded.
   对应摘录：C, D
4. 句子 4：Inside each state, a coordination controller activates only the actuators associated with adjacent transitions, which couples the discrete posture graph directly to state-specific motor subsets.
   对应摘录：C
5. 句子 5：Before operation, the two EMG channels are normalized, a `10%` dead band is applied, and co-contraction thresholds are calibrated per user, so the posture supervisor keeps explicit control over both branch selection and transition triggering.
   对应摘录：E

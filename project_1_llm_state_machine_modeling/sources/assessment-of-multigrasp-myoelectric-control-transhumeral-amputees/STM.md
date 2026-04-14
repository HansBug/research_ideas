# Assessment of a Multigrasp Myoelectric Control Approach for use by Transhumeral Amputees - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 transhumeral multigrasp prosthetic hand 的 `7` 态 event-driven state machine、`biceps / triceps / double extension` 输入、subject-specific relaxation time、`3 s` hold 与 `5 s` timeout 写成了完整控制链，可直接作为 `EFSM + T1` 双 A 样本。

## 条目 1: Seven-posture transhumeral MMC controller with double-extension switching
- 控制对象：经肱截肢多指假手的 multigrasp myoelectric control (`MMC`) controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 transhumeral multigrasp prosthetic hand 的姿态选择控制器，它用 biceps/triceps `EMG` 在七个离散姿态之间移动，并通过 double-extension 与显式 hold/timeout 规则管理 thumb branch 和任务完成判定。
- 判断：算。对象是真实 prosthetic-hand controller，不是纯实验流程；原文明确给出了状态集合、输入动作、thumb-branch 切换方法、subject-specific relaxation 时间以及 trial-level 成功/失败守卫。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，Section `II. Multigrasp Myoelectric Control`
> The MMC method involves an event driven finite-state machine that transitions between a finite set of fixed postures (states) ... Specifically, contraction of the biceps muscle (flexion) is associated with upward movement in the state chart, while contraction of the triceps muscle (extension) is associated with downward movement in the state chart ... the co-contraction event has been replaced with a double extension action to transition between the opposition and reposition states.

#### 摘录 B
- 出处：第 3 页，Section `II. Multigrasp Myoelectric Control`
> The double extension consists of fully extending the prosthesis within the opposition (or reposition) state, relaxing, and extending again to initiate automatic reposition (or opposition) of the thumb. To this end, the muscle relaxation time has been accounted for in this implementation by determining the relaxation period for each subject during the signal conditioning process.

#### 摘录 C
- 出处：第 4 页，Section `III. Methods`
> The target postures coincide with the MMC states (reposition, point, hook, lateral pinch, opposition, tip and cylindrical) ... When the virtual prosthesis closely matches the target posture (`±25%` range of motion) ... To be considered successful, a target posture must be held for `3` seconds ... if the target posture is not achieved within `5` seconds ... the transition is considered a failure.

#### 摘录 D
- 出处：第 5 页，Section `IV. Results and Discussion`
> The average overall transition times ... for the MMC were `1.86` seconds ... transitions which require opposition or reposition ... necessarily incorporate the muscle relaxation time ... In these experiments, the average muscle relaxation time was found to be `0.50` seconds.

### 2. 基于原文整理后的自然语言描述

The transhumeral multigrasp controller uses an event-driven state machine whose `7` fixed postures are `reposition`, `point`, `hook`, `lateral pinch`, `opposition`, `tip`, and `cylindrical`. Navigation is mapped directly onto upper-arm EMG: biceps contraction drives upward motion in the chart, triceps contraction drives downward motion, and the thumb branch is toggled by a double-extension action that replaces the older co-contraction event. That double extension is not instantaneous, because the implementation explicitly inserts each subject's measured muscle-relaxation period before the second extension command. In evaluation, a posture counts as successful only when the virtual prosthesis reaches the target within `±25%` of range and holds it for `3 s`, while an unreached target is aborted after `5 s` and marked as a failed transition. The controller therefore couples discrete posture states, EMG-triggered branch changes, subject-specific relaxation timing, and trial-level success or timeout guards in a single transhumeral prosthetic-hand control chain.

### 3. 逐句溯源

1. 句子 1：The transhumeral multigrasp controller uses an event-driven state machine whose `7` fixed postures are `reposition`, `point`, `hook`, `lateral pinch`, `opposition`, `tip`, and `cylindrical`.
   对应摘录：C
2. 句子 2：Navigation is mapped directly onto upper-arm EMG: biceps contraction drives upward motion in the chart, triceps contraction drives downward motion, and the thumb branch is toggled by a double-extension action that replaces the older co-contraction event.
   对应摘录：A
3. 句子 3：That double extension is not instantaneous, because the implementation explicitly inserts each subject's measured muscle-relaxation period before the second extension command.
   对应摘录：B
4. 句子 4：In evaluation, a posture counts as successful only when the virtual prosthesis reaches the target within `±25%` of range and holds it for `3 s`, while an unreached target is aborted after `5 s` and marked as a failed transition.
   对应摘录：C
5. 句子 5：The controller therefore couples discrete posture states, EMG-triggered branch changes, subject-specific relaxation timing, and trial-level success or timeout guards in a single transhumeral prosthetic-hand control chain.
   对应摘录：A, B, C, D

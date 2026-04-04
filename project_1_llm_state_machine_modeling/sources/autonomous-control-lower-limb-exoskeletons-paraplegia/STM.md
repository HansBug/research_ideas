# A Method for the Autonomous Control of Lower Limb Exoskeletons for Persons With Paraplegia - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了下肢外骨骼 `12` 状态 supervisory FSM、基于 `CoP` 与 frontal-plane lean 的切换 guard，以及 gait pause 转 standing 的局部时间规则，可直接提取为高质量状态机自然语言描述。

## 条目 1: Sit-stand-walk supervisory controller for the powered lower-limb exoskeleton
- 控制对象：面向截瘫患者的下肢动力外骨骼高层自主监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个根据用户上半身姿态、`CoP` 阈值和步态暂停时长来调度 sit/stand/walk 三类基本动作的下肢外骨骼 supervisory FSM。
- 判断：算。对象是真实下肢外骨骼控制器，不是康复流程或实验流程；原文明确给出了状态集合、步态触发 guard 和暂停转站立的局部时间逻辑，能够恢复高层控制链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section 3.2 `Finite-State Control Structure`
> The joint-level controller receives trajectory commands, as well as PD gains, from a supervisory finite-state machine (FSM), which (for sitting, standing, and walking) consists of 12 states, as shown in Fig. 3.
>
> The static states consist of sitting (S1), standing (S2), right-leg-forward (RLF) double support (S3), and left-leg-forward (LLF) double support (S4). The remaining 8 states, which transition between the four static states, include sit-to-stand (S5), stand-to-sit (S6), stand-to-walk with right half step (S7), stand-to-walk with left half step (S11), walk-to-stand with left half step (S10), walk-to-stand with right half step (S12), right step (S9), and left step (S8).

#### 摘录 B
- 出处：第 3 页，Section 3.3 `Switching Between States`
> From a state of double support (S3 or S4), the user commands the next step by moving the CoP forward, until it meets a prescribed threshold, at which point the FSM will enter either the right step or left step states, depending on which foot started forward.
>
> From a standing position (S2), the user commands a step by similarly moving the CoP forward until it meets a prescribed threshold, but also leaning to one side in the frontal plane ... leaning to the right ... will initiate a left step, while leaning to the left ... will initiate a right step.

#### 摘录 C
- 出处：第 4 页，Section 3.3 `Switching Between States`
> In order to transition from a standing state (S2) to a sitting state, the user shifts the CoP rearward, such that the CoP lies behind the user.
>
> Finally, to transition from a sitting to a standing state (S1 to S2), the user leans forward ... which shifts the CoP forward to a predetermined threshold, which initiates the transition from sitting to standing.

#### 摘录 D
- 出处：第 4 页，Section 3.3 `Switching Between States`
> Finally the transition from (either case of) double support to standing (i.e., from either S3 or S4, to S2) is based on the timing associated with crossing the CoP threshold.
>
> That is, if the CoP does not cross the CoP threshold within a given time following heel strike ... a sufficient pause during gait indicates to the system that the user wishes to stand, rather than continue walking forward.

### 2. 基于原文整理后的自然语言描述

The powered lower-limb exoskeleton is governed by a 12-state supervisory FSM that organizes sitting, standing, double-support, and stepping maneuvers for a paraplegic user. Its static backbone is formed by `S1 sitting`, `S2 standing`, `S3 right-leg-forward double support`, and `S4 left-leg-forward double support`, while eight transition states realize sit-to-stand, stand-to-sit, stand-to-walk, walk-to-stand, and left/right stepping motions. From `S2 standing`, the user initiates walking by moving the estimated center of pressure forward beyond a prescribed threshold and leaning laterally so that the unweighted leg is selected for the next half-step. From `S3/S4` double support, another forward `CoP` crossing continues the gait sequence, but if the threshold is not crossed within a given time after heel strike, the controller interprets the pause as an intent to stop and transitions to `S2 standing` instead of taking another step. Sitting and rising are likewise commanded through rearward or forward `CoP` shifts, so posture-derived guards and a local pause timer together determine the full sit-stand-walk supervisory loop.

### 3. 逐句溯源

1. 句子 1：The powered lower-limb exoskeleton is governed by a 12-state supervisory FSM that organizes sitting, standing, double-support, and stepping maneuvers for a paraplegic user.
   对应摘录：A
2. 句子 2：Its static backbone is formed by `S1 sitting`, `S2 standing`, `S3 right-leg-forward double support`, and `S4 left-leg-forward double support`, while eight transition states realize sit-to-stand, stand-to-sit, stand-to-walk, walk-to-stand, and left/right stepping motions.
   对应摘录：A
3. 句子 3：From `S2 standing`, the user initiates walking by moving the estimated center of pressure forward beyond a prescribed threshold and leaning laterally so that the unweighted leg is selected for the next half-step.
   对应摘录：B
4. 句子 4：From `S3/S4` double support, another forward `CoP` crossing continues the gait sequence, but if the threshold is not crossed within a given time after heel strike, the controller interprets the pause as an intent to stop and transitions to `S2 standing` instead of taking another step.
   对应摘录：B, D
5. 句子 5：Sitting and rising are likewise commanded through rearward or forward `CoP` shifts, so posture-derived guards and a local pause timer together determine the full sit-stand-walk supervisory loop.
   对应摘录：C, D

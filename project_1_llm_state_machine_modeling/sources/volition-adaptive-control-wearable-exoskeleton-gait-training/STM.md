# Volition-adaptive control for gait training using wearable exoskeleton: preliminary tests with incomplete spinal cord injury individuals - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `Rest / Preparation / Movement attempt / Movement` 四状态实验控制器、BMI 只在单一状态可触发的门控逻辑，以及 `20-25 s` 周期与 `10 s` movement window，可直接作为带局部时间语义的外骨骼 gait-initiation 样本。

## 条目 1: BMI-triggered gait-initiation FSM for wearable exoskeleton training
- 控制对象：结合 `BMI` 与穿戴式外骨骼 `H1` 的 gait training 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把 `BMI` 意图解码器与可穿戴外骨骼耦合起来的四状态监督控制器，用于在安全停顿窗口内只在指定时段接受 gait-initiation 触发。
- 判断：算。对象是真实 gait training 控制器，不是临床流程；原文明确给出状态集合、时长分配、单状态触发门控、无触发回退逻辑和 gait 执行窗口，能够恢复完整控制主链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section `FSM based BMI correlation with movement of the Exoskeleton, H1, and BMI system`
> This experimentation is categorized into four states with specific time assigned for each state: Rest, Preparation, Movement attempt and Movement. The time assigned to each state of the clinical protocol was defined based on the previous study ... Further, the timings of the FSM were decided by our medical team to provide enough time to rest and to perform the task in a safe and effective manner.

#### 摘录 B
- 出处：第 6 页，Figure 4 / same section
> The BMI signal is monitored only in the Movement attempt stage, which is further used as the trigger to initiate the movement of the exoskeleton. In any case, if there is no-attempt made by the patient, the machine progresses towards the resting period. Each cycle of the protocol lasts between 20-25 s, including the resting period. The movement time state comprises of the maximum duration (10 seconds) needed to complete one gait cycle (2 steps) ...

#### 摘录 C
- 出处：第 9 页，Figure 8 caption
> Gait initiation occurs with the onset of BMI trigger ... BMI triggers received at the movement attempt stage are only considered for the gait initiation. The control states indicate the transition between different states indicated in the FSM ...

#### 摘录 D
- 出处：第 10 页，Discussion of the control model
> The use of a FSM model ensured that the output from the BMI system is accessed only in the gait initiation stages ... The FSM model disregards the BMI triggers which are received outside the movement attempt state ...

### 2. 基于原文整理后的自然语言描述

The wearable exoskeleton training controller wraps the BMI decoder and the H1 exoskeleton inside a four-state supervisor with `Rest`, `Preparation`, `Movement attempt`, and `Movement` states. Each state is assigned a predefined duration chosen by the medical team, so the protocol enforces explicit pause and execution windows rather than leaving trigger handling open-ended. The BMI signal is monitored only in `Movement attempt`, and triggers received outside that state are ignored; if the patient makes no attempt, the machine falls back to the resting period instead of launching gait. Once a valid BMI trigger arrives during `Movement attempt`, gait initiation begins and the controller advances into `Movement`, whose maximum duration is `10 s` for one gait cycle of two steps. The full protocol cycle lasts about `20-25 s`, which makes the controller a timed trigger-gated exoskeleton supervisor rather than a continuously reactive decoder.

### 3. 逐句溯源

1. 句子 1：The wearable exoskeleton training controller wraps the BMI decoder and the H1 exoskeleton inside a four-state supervisor with `Rest`, `Preparation`, `Movement attempt`, and `Movement` states.
   对应摘录：A
2. 句子 2：Each state is assigned a predefined duration chosen by the medical team, so the protocol enforces explicit pause and execution windows rather than leaving trigger handling open-ended.
   对应摘录：A
3. 句子 3：The BMI signal is monitored only in `Movement attempt`, and triggers received outside that state are ignored; if the patient makes no attempt, the machine falls back to the resting period instead of launching gait.
   对应摘录：B, D
4. 句子 4：Once a valid BMI trigger arrives during `Movement attempt`, gait initiation begins and the controller advances into `Movement`, whose maximum duration is `10 s` for one gait cycle of two steps.
   对应摘录：B, C
5. 句子 5：The full protocol cycle lasts about `20-25 s`, which makes the controller a timed trigger-gated exoskeleton supervisor rather than a continuously reactive decoder.
   对应摘录：B

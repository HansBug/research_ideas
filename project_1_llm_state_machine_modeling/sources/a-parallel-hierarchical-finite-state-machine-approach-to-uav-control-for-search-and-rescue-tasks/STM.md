# A Parallel Hierarchical Finite State Machine Approach to UAV Control for Search and Rescue Tasks - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了清晰的搜索救援 UAV 高层状态流转以及并行安全飞行子层，适合整理为任务级飞行控制样本。

## 条目 1: Search-and-rescue mission flow with parallel safe-flight layer
- 控制对象：搜索救援无人机高层控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、并行
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是无人机任务控制领域的 high-level UAV controller，用于在搜索救援任务中驱动起飞、搜索、跟踪、返航和着陆，并并行维持安全飞行。
- 判断：算。对象是实际 UAV mission controller，原文明确给出了任务状态序列和并行/分层子状态组织。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，对 Search and Rescue mission FSM 的说明，行 148-178
> This position paper proposes an abstract UAV control strategy based on a parallel hierarchical finite state machine.
>
> The high-level diagram of Figure 2 has the first state (Start), that is defined to takeoff procedures.
>
> After all takeoff procedures are ended, the next state transitions are related to search and rescue the target. ... These states are described in Figure 2 by Move to Search and Look for the target respectively.
>
> After target detection, the next transition is to Track state that starts the target tracking procedures. ... In the end, after reaching all task requirements, return to base and landing states respectively.

#### 摘录 B
- 出处：第 3-4 页，对 HFSM / parallel stage 的说明，行 186-256
> we include an Emergency State, defined as an asynchronous input and assigned higher level priority for emergency situations.
>
> The parallel approach is necessary to allow all processes to run correctly in the same time, avoiding process deadlocks. The hierarchical approach has the function to handle all asynchronous inputs ... and allows a safe flight.
>
> In this experiment, we define a set of sequential and parallel processes working together. For example, a sublayer is responsible to keep the UAV flying on safe mode, that runs in parallel with the sublayer tracking target. A sublayer tracking the target is hierarchically higher than the sublayer of human face detection.
>
> after hazard handling process the system should be able to return for the last state in all sublayers.

### 2. 基于原文整理后的自然语言描述

The search-and-rescue UAV controller is organized as a parallel hierarchical finite state machine whose top-level mission states are `Start`, `Move to Search`, `Look for the target`, `Track`, `Return to base`, and `Landing`. Each high-level state owns lower-level sublayers, and the high-level layer assigns priorities to handle asynchronous inputs, including a dedicated higher-priority `Emergency State` for emergency situations. The parallel stage lets multiple task-specific FSM sublayers run together, so a safe-flight sublayer can remain active while other sublayers execute target search, face detection, or target tracking. Within this hierarchy, target tracking is above human-face detection, and if a hazard occurs the system is intended to handle the hazard and then return each sublayer to the last state from which it was interrupted.

### 3. 逐句溯源

1. 句子 1：The search-and-rescue UAV controller is organized as a parallel hierarchical finite state machine whose top-level mission states are `Start`, `Move to Search`, `Look for the target`, `Track`, `Return to base`, and `Landing`.
   对应摘录：A
2. 句子 2：Each high-level state owns lower-level sublayers, and the high-level layer assigns priorities to handle asynchronous inputs, including a dedicated higher-priority `Emergency State` for emergency situations.
   对应摘录：A, B
3. 句子 3：The parallel stage lets multiple task-specific FSM sublayers run together, so a safe-flight sublayer can remain active while other sublayers execute target search, face detection, or target tracking.
   对应摘录：B
4. 句子 4：Within this hierarchy, target tracking is above human-face detection, and if a hazard occurs the system is intended to handle the hazard and then return each sublayer to the last state from which it was interrupted.
   对应摘录：B

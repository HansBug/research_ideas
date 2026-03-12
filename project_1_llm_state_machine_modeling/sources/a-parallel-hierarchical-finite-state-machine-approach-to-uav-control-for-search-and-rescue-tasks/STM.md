# A Parallel Hierarchical Finite State Machine Approach to UAV Control for Search and Rescue Tasks - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文给出了清晰的搜索救援 UAV 高层状态流转以及并行安全飞行子层，适合整理为任务级飞行控制样本。

## 条目 1: Search-and-rescue mission flow with parallel safe-flight layer
- 控制对象：搜索救援无人机高层控制器

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
- 出处：第 4 页，对 parallel stage 的说明，行 238-256
> the UAV control steps are: UAV’s take-off; find and track a person(target); return to home; and; landing.
>
> In this experiment, we define a set of sequential and parallel processes working together. For example, a sublayer is responsible to keep the UAV flying on safe mode, that runs in parallel with the sublayer tracking target. A sublayer tracking the target is hierarchically higher than the sublayer of human face detection.

### 2. 基于原文整理后的自然语言描述

The search-and-rescue UAV controller starts in a Start state for takeoff procedures and then advances through Move to Search and Look for the target to locate the rescue target. After the target is detected, the controller transitions to a Track state to follow the target, and after the task requirements are completed it returns to base and proceeds to landing. The high-level mission flow is supported by sequential and parallel sublayers, including a safe-flight sublayer that runs in parallel with target tracking and lower-level detection activities.

### 3. 逐句溯源

1. 句子 1：The search-and-rescue UAV controller starts in a Start state for takeoff procedures and then advances through Move to Search and Look for the target to locate the rescue target.
   对应摘录：A
2. 句子 2：After the target is detected, the controller transitions to a Track state to follow the target, and after the task requirements are completed it returns to base and proceeds to landing.
   对应摘录：A
3. 句子 3：The high-level mission flow is supported by sequential and parallel sublayers, including a safe-flight sublayer that runs in parallel with target tracking and lower-level detection activities.
   对应摘录：B

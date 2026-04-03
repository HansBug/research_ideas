# Design, Formalization, and Verification of Decision Making for Intelligent Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文主体是方法论，但其 NASA `DZR` 案例把 rover 决策层 H-FSM 的相位、子状态、事件向量、持续步数条件和输出参数全部写清楚了，足以作为高质量 source 条目。

## 条目 1: DZR Hierarchical Decision-Making H-FSM
- 控制对象：NASA 自主漫游车 Dynamic Zonal Relay 阶段的决策制定应用
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 NASA 漫游车协同任务中 `DZR` 决策模块的高层 H-FSM，包含 `DriveToZone / CharacterizeZone / Relay` 三个 meta-state、叶状态级事件转移，以及 `persisted(3, ...)` 形式的局部时间窗口。
- 判断：算。虽然论文也讨论 FRET/CoCoSim 工具链，但 `DZR` 案例不是抽象示意，而是具体 autonomous agent 的决策层控制器；原文给出了功能分解、层次状态树、事件向量定义、状态转移需求和叶状态参数输出，达到 `A/A`。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-3 页 Abstract / Section II
> The approach is generally applicable to operational objectives that can be functionally decomposed and subsequently represented as Hierarchical Finite State Machines.
>
> The proposed Decision Making scheme is represented by the high-level layer of the system and is made up of a Hierarchical Finite State Machine.
>
> Meta-state: A state that contains an internal state machine with at least one sub-state.

#### 摘录 B
- 出处：第 8-9 页 Section V `Case Study`
> DZR_1 is first decomposed to be made up of three distinct phases: DriveToZone_11, CharacterizeZone_12, and Relay_13.
>
> Within DriveToZone_11, a given rover is tasked with driving to its designated zone (Drive_111) while listening to data from other rovers and transmitting back to followers (Transmit_112).
>
> Once in the designated zone, the rover transitions to CharacterizeZone_12 where the goal of the rover is to drive (Drive_121), acquire data (Acquire_122), and regularly transmit (Transmit_123).
>
> On completion of zone mapping, the rover then transitions to the Relay_13 phase where it is tasked with traversing to a relay location (ApproachRelayLoc_131), transfer data (TransferData_132), and remain idle (Idle_133).

#### 摘录 C
- 出处：第 10 页 Section V.B `FRET requirements for DM`
> Upon FSM_State_2 = DZR_Relay DM shall immediately satisfy FSM_State_3 = DZR_Relay_ApproachRelayLoc
>
> Upon(FSM_State_3=DZR_CharacterizeZone_Acquire&ED_2) DM shall at the next timepoint satisfy FSM_State_3 = DZR_CharacterizeZone_Transmit
>
> DM shall always satisfy ED_2 <=> persisted(3,F_segmentCharacterizationComplete)
>
> Whenever FSM_State_3 = DZR_CharacterizeZone_Acquire DM shall immediately satisfy (controllerType = 1 & activity = 4 & velocity = 1.0)

### 2. 基于原文整理后的自然语言描述

The decision-making application for NASA’s Dynamic Zonal Relay mission stage is implemented as a hierarchical finite state machine whose top-level meta-state `DZR_1` contains the three mission phases `DriveToZone_11`, `CharacterizeZone_12`, and `Relay_13`. Each phase is refined into leaf-level operational states: the rover first drives to its assigned zone while optionally forwarding data, then executes a characterization loop that alternates among `Drive`, `Acquire`, and `Transmit` behaviors, and finally enters a relay phase with `ApproachRelayLoc`, `TransferData`, and `Idle` states. State transitions are driven by explicitly named event-vector elements such as `ED_2`, whose truth value is itself defined by a persistence condition requiring the segment-characterization flag to hold for three consecutive decision steps. The controller also fixes low-level interface outputs at the leaf-state level; for example, in `DZR_CharacterizeZone_Acquire`, the DM layer immediately sets `controllerType = 1`, `activity = 4`, and `velocity = 1.0`. The paper additionally specifies default sub-state entry for the relay phase and the expected next-state transition from `Acquire` to `Transmit`, so the control chain is recoverable down to both sequencing and parameter handoff.

### 3. 逐句溯源

1. 句子 1：The decision-making application for NASA’s Dynamic Zonal Relay mission stage is implemented as a hierarchical finite state machine whose top-level meta-state `DZR_1` contains the three mission phases `DriveToZone_11`, `CharacterizeZone_12`, and `Relay_13`.
   对应摘录：A, B
2. 句子 2：Each phase is refined into leaf-level operational states: the rover first drives to its assigned zone while optionally forwarding data, then executes a characterization loop that alternates among `Drive`, `Acquire`, and `Transmit` behaviors, and finally enters a relay phase with `ApproachRelayLoc`, `TransferData`, and `Idle` states.
   对应摘录：B
3. 句子 3：State transitions are driven by explicitly named event-vector elements such as `ED_2`, whose truth value is itself defined by a persistence condition requiring the segment-characterization flag to hold for three consecutive decision steps.
   对应摘录：C
4. 句子 4：The controller also fixes low-level interface outputs at the leaf-state level; for example, in `DZR_CharacterizeZone_Acquire`, the DM layer immediately sets `controllerType = 1`, `activity = 4`, and `velocity = 1.0`.
   对应摘录：C
5. 句子 5：The paper additionally specifies default sub-state entry for the relay phase and the expected next-state transition from `Acquire` to `Transmit`, so the control chain is recoverable down to both sequencing and parameter handoff.
   对应摘录：C

# GN&C Sequencing for Orion Rendezvous, Proximity Operations, and Docking - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟、层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 Orion RPOD 的 `PSAM` 序列体系写成 `Phase -> Segment -> Activity -> Mode` 层次状态机，并给出了 `NRI-1h`、`20 min before TIG`、`5 min before TIG`、`RB3/RB5/RB6` 和 `Docked` 等明确转移条件，还覆盖了 `Hold_Retreat` 与 `Abort` 等离轨分支。

## 条目 1: PSAM Sequencing for Orion RPOD Operations
- 控制对象：Orion 航天器在 Gateway/EUS 交会、近距离操作与对接中的 GN&C 序列控制
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟、层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 Orion `RPOD` 任务中的高层 GN&C sequencing 设计，使用 `PSAM` 层次结构管理从远距接近、点火准备、点火执行、近距制动到对接和撤离的完整任务流程。
- 判断：算。对象是 Artemis 任务里真实航天器的软件序列控制，不是抽象流程图；原文给出了层次状态定义、阶段/段转移条件、时间窗口、手动 ATP 关口和多类 off-nominal segment，因此完全满足 `HSM + T1 + A/A`。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页 Abstract / Introduction
> The Orion spacecraft uses sequencing in the form of Phases, Segments, Activities, and Modes (PSAM) to configure Guidance, Navigation, & Control software during each portion of the mission.
>
> A state machine diagram is developed to show all PSAM states, including all possible transitions between them.

#### 摘录 B
- 出处：第 6-8 页 `ORION RPOD SEQUENCING DESIGN`
> A new Phase should be created called RPODOperations.
>
> When the range to Gateway drops below a parameterized value ... If this range is not reached by one hour before NRI, the transition will occur anyway.
>
> During the RPOD_Coast Segment ... 20 minutes before the planned Time of Ignition for a Far Range burn, FSW transitions into the RPOD_Burn_Config Segment.
>
> Finally, at 5 minutes before TIG, FSW transitions into the RPOD_Burn Segment.
>
> The transition from the RPOD_Coast Segment into the RPOD_Mid_Range Segment occurs after the final "turn to burn" (currently RB3) is complete.
>
> After RB5 is complete, FSW transitions into the RPOD_Close_Range Segment.
>
> The transition from RPOD_Close_Range Segment to the Docked Segment occurs at the end of docking when hard capture is complete.

#### 摘录 C
- 出处：第 8-9 页 `ORION RPOD SEQUENCING DESIGN`
> Before departing from EUS or Gateway, FSW transitions to the RPOD_Departure Segment.
>
> At any point prior to RB6, Orion can perform a passive flyby ... by transitioning to an RPOD_Passive_Flyby Segment.
>
> A position hold and/or retreat can be commanded ... by transitioning into one of three Segments: RPOD_Far_Range_Hold_Retreat, RPOD_Mid_Range_Hold_Retreat, or RPOD_Close_Range_Hold_Retreat.
>
> The crew can abort the approach permanently ... by transitioning into RPOD_Far_Range_Abort, RPOD_Mid_Range_Abort, or RPOD_Close_Range_Abort Segments.

### 2. 基于原文整理后的自然语言描述

The Orion RPOD guidance, navigation, and control sequencer uses a hierarchical PSAM architecture in which `Phase`, `Segment`, `Activity`, and `Mode` form nested levels of mission-state configuration. A dedicated top-level phase `RPODOperations` is introduced for rendezvous and docking, entered either when range to Gateway drops below a parameterized threshold or, failing that, one hour before `NRI`. Within this phase, the nominal far-range loop cycles through `RPOD_Coast`, `RPOD_Burn_Config`, and `RPOD_Burn`, with transitions occurring 20 minutes before each planned burn `TIG`, 5 minutes before `TIG`, and after burn/trim completion. Completion of `RB3` advances the sequencer into `RPOD_Mid_Range`, completion of `RB5` moves it into `RPOD_Close_Range`, and successful hard capture moves the system into `Docked`; undock returns the vehicle to close-range operations and later to `RPOD_Departure` for separation. The same design also encodes off-nominal branches including `Passive_Flyby`, `Hold_Retreat`, and multi-range `Abort` segments, so both nominal and contingency paths are explicitly represented in the state hierarchy.

### 3. 逐句溯源

1. 句子 1：The Orion RPOD guidance, navigation, and control sequencer uses a hierarchical PSAM architecture in which `Phase`, `Segment`, `Activity`, and `Mode` form nested levels of mission-state configuration.
   对应摘录：A
2. 句子 2：A dedicated top-level phase `RPODOperations` is introduced for rendezvous and docking, entered either when range to Gateway drops below a parameterized threshold or, failing that, one hour before `NRI`.
   对应摘录：B
3. 句子 3：Within this phase, the nominal far-range loop cycles through `RPOD_Coast`, `RPOD_Burn_Config`, and `RPOD_Burn`, with transitions occurring 20 minutes before each planned burn `TIG`, 5 minutes before `TIG`, and after burn/trim completion.
   对应摘录：B
4. 句子 4：Completion of `RB3` advances the sequencer into `RPOD_Mid_Range`, completion of `RB5` moves it into `RPOD_Close_Range`, and successful hard capture moves the system into `Docked`; undock returns the vehicle to close-range operations and later to `RPOD_Departure` for separation.
   对应摘录：B, C
5. 句子 5：The same design also encodes off-nominal branches including `Passive_Flyby`, `Hold_Retreat`, and multi-range `Abort` segments, so both nominal and contingency paths are explicitly represented in the state hierarchy.
   对应摘录：C

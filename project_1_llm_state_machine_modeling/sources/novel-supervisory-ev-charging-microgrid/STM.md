# Novel Supervisory Management Scheme of Hybrid Sun Empowered Grid-Assisted Microgrid for Rapid Electric Vehicles Charging Area - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `PV / ESS / grid / EV` 快充站写成 `overload / under-load / no-load / idle` 四模式监督器，并给出每个模式下 `PV2EV / ESS2EV / GD2EV / PV2ESS / PV2GD / GD2ESS` 的切换条件，足以形成双 A 样本。

## 条目 1: Four-scenario fast-charging microgrid supervisor

- 控制对象：过程与环境控制领域的光伏-储能-电网混合 `EV` 快充站监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个围绕 `PV power / EV demand / ESS SoC / grid tariff` 变化来切换能量流向的快充站 supervisory controller，用四个离散工作场景管理 `PV`、电池、公共电网和待充电车辆之间的功率分配。
- 判断：算。对象是真实 `EV` 充电站能量管理控制器，原文明确写出模式集合、模式进入条件，以及各模式下的功率流动作，不是只有经济性对比或容量优化结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，Introduction，`paper_content.txt` 第 181-183、222-229 行
> This requires a Supervisory Controller (SC) that controls the battery energy storage system (BESS) charging/discharging by coordinating the operation of controllable units within the station.
>
> This paper presents and develops a supervisory controller for the battery-enabled DC fast charging station based on the Supervisory Control Theory (SCT) of discrete event systems ... The supervisory control also can use a Finite State Machine (FSM) for the implementation of complex supervisory control logics which is transparent and readily implementable on industrial controllers.

#### 摘录 B

- 出处：第 13-14 页，`3.3 Operation of the Transactive Grid with REMA under Variant Scenarios`，`paper_content.txt` 第 812-820 行
> The working of the understudied system is explained in four different modes of operation depending on the solar irradiation conditions and SOC of the EV battery.
>
> (i) Overload ... EVdemand is more than PVpower
> (ii) Under load ... EVdemand is present but less than or equal to PVpower
> (iii) No-load ... PVpower is available but EVdemand is zero
> (iv) Idle condition ... both EVdemand and PVpower is zero.

#### 摘录 C

- 出处：第 14-16 页，`3.3.1-3.3.4`，`paper_content.txt` 第 821-828、883-891、926-934 行
> In the overload scenario ... PV2EV ... if the main grid is at off-peak hours, the GD2EV is energized ... if SOC is less than SOCM, then the energy bank is also accumulated by the grid (GD2ESS) ... if Avl_ESS_Pwr > EVDmd, the demand is realized by battery stacks exclusively using ESS2EV.
>
> In the under-load scenario ... the extra PV_Pwr can be injected into ESS (PV2ESS) ... if the additional PV_Pwr > Red_ESS_Pwr, the residual energy is retailed to the utility grid (PV2GD).
>
> In the idle scenario ... the recharging of ESS commences when the state charge is lower than the up-threshold and the mains are at the off-loaded condition.

### 2. 基于原文整理后的自然语言描述

The charging-station controller is organized as a four-mode energy-routing supervisor driven by `PV power`, `EV demand`, `ESS state of charge`, and grid-price context. In `Overload`, where `EVdemand > PVpower`, photovoltaic generation is sent directly to the vehicles, and the remaining demand is satisfied by `ESS2EV`, `GD2EV`, or a simultaneous `GD2ESS` valley-filling action when the grid is off-peak and the battery is still below its upper limit. In `Under-load`, where photovoltaic supply exceeds the present charging demand, the controller first prefers `PV2ESS`, then exports the residual surplus through `PV2GD` once the storage requirement is covered. In `No-load`, the same supervisor checks whether the battery is still below its upper threshold; if so, it continues with `PV2ESS` or adds `GD2ESS` when photovoltaic surplus is insufficient, and otherwise transfers all photovoltaic power to the grid. In `Idle`, where both `EVdemand` and `PVpower` are zero, the rule set starts recharging the storage bank from the mains only when the battery remains below the upper threshold and the utility side is lightly loaded. Because every mode is attached to mutually exclusive power-flow commands such as `PV2EV`, `ESS2EV`, `GD2EV`, `PV2ESS`, `PV2GD`, and `GD2ESS`, the paper gives a recoverable discrete supervisor rather than only a narrative EMS.

### 3. 逐句溯源

1. 句子 1：The charging-station controller is organized as a four-mode energy-routing supervisor driven by `PV power`, `EV demand`, `ESS state of charge`, and grid-price context.
   对应摘录：A, B
2. 句子 2：In `Overload`, where `EVdemand > PVpower`, photovoltaic generation is sent directly to the vehicles, and the remaining demand is satisfied by `ESS2EV`, `GD2EV`, or a simultaneous `GD2ESS` valley-filling action when the grid is off-peak and the battery is still below its upper limit.
   对应摘录：B, C
3. 句子 3：In `Under-load`, where photovoltaic supply exceeds the present charging demand, the controller first prefers `PV2ESS`, then exports the residual surplus through `PV2GD` once the storage requirement is covered.
   对应摘录：B, C
4. 句子 4：In `No-load`, the same supervisor checks whether the battery is still below its upper threshold; if so, it continues with `PV2ESS` or adds `GD2ESS` when photovoltaic surplus is insufficient, and otherwise transfers all photovoltaic power to the grid.
   对应摘录：B, C
5. 句子 5：In `Idle`, where both `EVdemand` and `PVpower` are zero, the rule set starts recharging the storage bank from the mains only when the battery remains below the upper threshold and the utility side is lightly loaded.
   对应摘录：B, C
6. 句子 6：Because every mode is attached to mutually exclusive power-flow commands such as `PV2EV`, `ESS2EV`, `GD2EV`, `PV2ESS`, `PV2GD`, and `GD2ESS`, the paper gives a recoverable discrete supervisor rather than only a narrative EMS.
   对应摘录：A, C

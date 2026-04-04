# Terrestrial Unmanned Roving Vertical Take-off and Landing (TURVTOL) - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 TURVTOL 多模态平台的层次状态机骨架、低层状态表和 transition signals，能够直接恢复 drive/fly/landing/charging/fault-recovery 的主控制链。

## 条目 1: Multi-modal drive-fly mission FSM for TURVTOL
- 控制对象：TURVTOL 多模态自主载具的任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个 NASA 多模态 rover/drone 平台的高层监督状态机，用于协调 drive、takeoff、flight、landing、traction-loss recovery 和 dormant charging/sleeping。
- 判断：算。对象是真实自主平台的软件控制器，不是泛泛系统架构；原文给出了层次状态机层级、最低层状态表和一整张 transition signal 表，已经达到可直接恢复控制链的程度。

### 1. 原文摘录

#### 摘录 A
- 出处：第 34 页，Section V.B `FSM Design`
> A finite state machine (FSM) has been designed and the general structure has been implemented using the ROS library SMACH.
>
> The hierarchical design is shown in Fig. 25. At a high level, the states are FLY_OPERATE and DRIVE_OPERATE.
>
> The FLY_OPERATE sub-machine contains a LANDING sub-machine.
>
> The DRIVE_OPERATE sub-machine contains a TRACTION_LOSS sub-machine ... DRIVE_OPERATE also contains the DORMANT sub-machine.

#### 摘录 B
- 出处：第 34 页，Table 4 `Descriptions of the lowest level FSM states`
> CHARGING Low battery
>
> DRIVE_NO_FLY Driving operations in circumstances where takeoff would be unsafe
>
> FLY Normal flying operations
>
> HOVER Waiting for update from path planner
>
> LAND Path planner has confirmed landing
>
> NORM_DRIVE Normal driving operations
>
> RETURN_TO_LAUNCH Cannot find safe landing location; return to known safe location (launch site)
>
> SEARCH_FOR_LANDING Assesses terrain below for safe landing location

#### 摘录 C
- 出处：第 33-36 页，Section V.B `FSM Design` / Table 5 `Descriptions of the FSM transition signals`
> when the vehicle is driving across terrain that would make it difficult for the vehicle to take off for flight, the FSM will switch from the NORM_DRIVE state to the DRIVE_NO_TAKEOFF state
>
> continue_flight Path planner sends confirmation to continue flying
>
> land Either path planner confirms landing or battery is low or there is no current destination
>
> return_to_safe Path planner confirms landing but a safe landing cannot be made within a specified search radius
>
> safe_landing Path planner confirms landing and safe landing has been ensured
>
> stuck VIO indicates that vehicle is moving less than expected

### 2. 基于原文整理后的自然语言描述

The TURVTOL autonomy engine is organized as a hierarchical state machine whose two top-level modes are `FLY_OPERATE` and `DRIVE_OPERATE`, with additional nested submachines for `LANDING`, `TRACTION_LOSS`, and `DORMANT` behavior. During normal terrestrial traversal the controller stays in `NORM_DRIVE`, but if terrain or flight conditions make takeoff unsafe it switches to `DRIVE_NO_FLY`, explicitly preventing the planner from considering airborne paths. When the mission requires an aerial maneuver, the supervisor advances through `TAKEOFF`, `FLY`, and `HOVER`, while waiting for path-planner updates and continuing to evaluate safety-related transition signals. If landing is requested, the controller either enters `SEARCH_FOR_LANDING` and then `LAND` when a safe touchdown site is available, or falls back to `RETURN_TO_LAUNCH` when no safe landing can be found within the search radius. Low battery, lack of destination, slipping, getting stuck, or flipping the vehicle all route execution into dedicated recovery or dormant states such as `CHARGING`, `SLEEPING`, `SLIPPING`, `STUCK`, and `FLIPPED`, so the abnormal chain is as explicit as the nominal drive-fly cycle.

### 3. 逐句溯源

1. 句子 1：The TURVTOL autonomy engine is organized as a hierarchical state machine whose two top-level modes are `FLY_OPERATE` and `DRIVE_OPERATE`, with additional nested submachines for `LANDING`, `TRACTION_LOSS`, and `DORMANT` behavior.
   对应摘录：A
2. 句子 2：During normal terrestrial traversal the controller stays in `NORM_DRIVE`, but if terrain or flight conditions make takeoff unsafe it switches to `DRIVE_NO_FLY`, explicitly preventing the planner from considering airborne paths.
   对应摘录：B, C
3. 句子 3：When the mission requires an aerial maneuver, the supervisor advances through `TAKEOFF`, `FLY`, and `HOVER`, while waiting for path-planner updates and continuing to evaluate safety-related transition signals.
   对应摘录：B, C
4. 句子 4：If landing is requested, the controller either enters `SEARCH_FOR_LANDING` and then `LAND` when a safe touchdown site is available, or falls back to `RETURN_TO_LAUNCH` when no safe landing can be found within the search radius.
   对应摘录：B, C
5. 句子 5：Low battery, lack of destination, slipping, getting stuck, or flipping the vehicle all route execution into dedicated recovery or dormant states such as `CHARGING`, `SLEEPING`, `SLIPPING`, `STUCK`, and `FLIPPED`, so the abnormal chain is as explicit as the nominal drive-fly cycle.
   对应摘录：B, C

# An Integrated System for Autonomous Search and Track with a Small Unmanned Aerial Vehicle - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把小型无人机的高层 autonomy 明确写成 `SMACH` 层次状态机，并清楚给出了 `MONITOR / TAKEOFF / SEARCH / INVESTIGATE / TRACK` 主链、并发安全监控、目标确认与失跟回退逻辑。

## 条目 1: Search-Investigate-Track mission controller for the sUAV
- 控制对象：小型无人机 search-and-track 任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：层次, 并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个小型无人机在自主监视任务中使用的高层任务状态机，用于调度起飞、搜索、目标确认、持续跟踪以及低电量/失联回退降落。
- 判断：算。对象是实际小型无人机的平台任务控制器，不是纯视觉算法流程；原文给出了层次状态机、并发 `MONITOR` 安全链、搜索子模式、确认条件和跟踪置信度回退规则。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Introduction / Technical Approach
> In this paper a Hierarchical Finite State machine is implemented for a search and track mission.
>
> More specifically SMACH, a python based FSM has been integrated to facilitate search and track.

#### 摘录 B
- 出处：第 3-4 页，Section II `Technical Approach`
> The three main components of the system are search, investigate and track.
>
> After an initial reset of the system where the system re-calibrates all the sensors, the system goes into MONITOR mode.
>
> This MONITOR mode runs as a concurrent state machine at all the times.
>
> If there is any communication error or the battery goes below the safe threshold, it commands the drone to abort the mission and perform a controlled land.
>
> If the MONITOR state reports that the system is ok to proceed, the TAKEOFF state makes the UAV airborne. Immediately after takeoff the system enters into SEARCH mode.

#### 摘录 C
- 出处：第 4 页，Section II `Technical Approach`
> Two methods of SEARCH have been implemented so far: SPIN SEARCH and WAY POINT search.
>
> If a human target is detected in the SEARCH state the state machine switches to INVESTIGATE mode.
>
> If both the face detector and the human detector simultaneously reports positive, then human detection is confirmed.
>
> Second, the state machine switches to TRACK mode.

#### 摘录 D
- 出处：第 5 页，Section II.B `Tracking`
> The system remains in TRACK mode while the confidence in tracking is over a predefined threshold.
>
> If the confidence of the tracker decreases below the threshold, the system reverts back to SEARCH mode.

### 2. 基于原文整理后的自然语言描述

The small-UAV autonomy controller is implemented as a hierarchical `SMACH` state machine whose main mission chain is supervised by a concurrent `MONITOR` safety state. After an initial reset and sensor recalibration, `MONITOR` continuously checks the communication link and battery status; only when it reports the system safe does the controller enter `TAKEOFF` and then immediately transition to `SEARCH`. Inside `SEARCH`, the UAV either performs `SPIN SEARCH` or `WAY POINT search` until the human detector reports a candidate target, at which point the controller switches to `INVESTIGATE` and commands the vehicle to hold a hover. If both the human detector and the face detector confirm the target, the controller initializes the tracker and enters `TRACK`, where the vehicle maintains pursuit as long as tracking confidence remains above threshold. If communication is lost, battery falls below the safe limit, or tracking confidence drops under the configured threshold, the controller aborts the current chain and either performs a controlled landing or falls back from `TRACK` to `SEARCH` for reacquisition.

### 3. 逐句溯源

1. 句子 1：The small-UAV autonomy controller is implemented as a hierarchical `SMACH` state machine whose main mission chain is supervised by a concurrent `MONITOR` safety state.
   对应摘录：A, B
2. 句子 2：After an initial reset and sensor recalibration, `MONITOR` continuously checks the communication link and battery status; only when it reports the system safe does the controller enter `TAKEOFF` and then immediately transition to `SEARCH`.
   对应摘录：B
3. 句子 3：Inside `SEARCH`, the UAV either performs `SPIN SEARCH` or `WAY POINT search` until the human detector reports a candidate target, at which point the controller switches to `INVESTIGATE` and commands the vehicle to hold a hover.
   对应摘录：C
4. 句子 4：If both the human detector and the face detector confirm the target, the controller initializes the tracker and enters `TRACK`, where the vehicle maintains pursuit as long as tracking confidence remains above threshold.
   对应摘录：C, D
5. 句子 5：If communication is lost, battery falls below the safe limit, or tracking confidence drops under the configured threshold, the controller aborts the current chain and either performs a controlled landing or falls back from `TRACK` to `SEARCH` for reacquisition.
   对应摘录：B, D

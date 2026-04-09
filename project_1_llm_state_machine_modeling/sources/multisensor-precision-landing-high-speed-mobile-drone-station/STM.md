# Multi-Sensor-Based Long-Range Precision Landing on a High-Speed Mobile Drone Station - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把移动平台精确降落明确拆成 `trajectory generation and following / deceleration / terminal descent` 三阶段，并给出 `d < l`、`ΔT1`、`ΔT2` 与 marker 丢失时的 abort 逻辑，适合作为飞行任务监督样本。

## 条目 1: Three-Phase Precision-Landing Supervisor for Mobile Drone Station

- 控制对象：高速移动无人机站上的多传感器精确降落监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个移动充电站上的无人机自主降落状态机，控制器按三阶段流程完成追赶、减速、对准和下降，并在 marker 丢失时执行搜索或中止。
- 判断：算。对象是实际飞行实验中的降落监督器，不是单纯轨迹优化模块；原文给出了状态名、进入条件、距离阈值和等待时间。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，Section 4，`paper_content.txt` 第 288-315 行
> The precision landing procedure is divided into three primary phases: (1) Trajectory generation and following, (2) Deceleration, and (3) Terminal descent with PID ... control.
>
> As the drone approaches the station ... when the distance falls below a threshold, the drone stops trajectory generation and transitions to the deceleration phase.
>
> descent commands are only issued when two conditions are satisfied ... Condition (1) has been satisfied for ΔT2.

#### 摘录 B

- 出处：第 6 页，Section 4.2，`paper_content.txt` 第 374-392 行
> once the horizontal distance between the drone and the station d falls below a threshold l, the drone stops generating the path and switches the reference point to the landing point.
>
> The drone then initiates deceleration ... employing PID control and a discretized stepwise speed limiting strategy.

#### 摘录 C

- 出处：第 6 页，Section 4.3，`paper_content.txt` 第 393-410 行
> During deceleration, if the drone detects the marker or reaches the landing point, the speed limit is lifted and the system transitions to terminal descent.
>
> After reaching hmax, if the marker remains undetected for ΔT1, the landing is aborted and the drone hovers.
>
> After the marker is detected again, the horizontal distance error stays within a threshold for ΔT2, the drone begins descending at a constant vertical speed.

### 2. 基于原文整理后的自然语言描述

The precision-landing controller is a three-state flight supervisor composed of `trajectory generation and following`, `deceleration`, and `terminal descent`. The mission starts by sending the drone to an initial point and generating a trajectory toward a landing point above the moving station; while following that path, the drone flies faster than the station by a fixed margin so it can catch up from long range. When the horizontal distance `d` falls below the threshold `l`, the controller switches from path following to a discretized deceleration state, where the speed limit is reduced in steps until the relative horizontal velocity approaches zero. If the marker is detected or the landing point is reached during deceleration, the supervisor enters `terminal descent`; otherwise it can climb to `hmax` to search, and if the marker still remains undetected for `ΔT1`, the landing is aborted and the drone hovers. Even after the marker is reacquired, descent is released only when the horizontal error has stayed within threshold for `ΔT2`, which makes the landing phase explicitly guarded by both spatial and temporal conditions.

### 3. 逐句溯源

1. 句子 1：The precision-landing controller is a three-state flight supervisor composed of `trajectory generation and following`, `deceleration`, and `terminal descent`.
   对应摘录：A
2. 句子 2：The mission starts by sending the drone to an initial point and generating a trajectory toward a landing point above the moving station; while following that path, the drone flies faster than the station by a fixed margin so it can catch up from long range.
   对应摘录：A
3. 句子 3：When the horizontal distance `d` falls below the threshold `l`, the controller switches from path following to a discretized deceleration state, where the speed limit is reduced in steps until the relative horizontal velocity approaches zero.
   对应摘录：A, B
4. 句子 4：If the marker is detected or the landing point is reached during deceleration, the supervisor enters `terminal descent`; otherwise it can climb to `hmax` to search, and if the marker still remains undetected for `ΔT1`, the landing is aborted and the drone hovers.
   对应摘录：C
5. 句子 5：Even after the marker is reacquired, descent is released only when the horizontal error has stayed within threshold for `ΔT2`, which makes the landing phase explicitly guarded by both spatial and temporal conditions.
   对应摘录：A, C

# Autonomous navigation of quadrupeds using coverage path planning with morphological skeleton maps - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `Load Map / CheckWaypoints / Check Destination / Move / Scan / ManualControl / Home` 这条 quadruped coverage supervisor 写得很清楚，还给出了 `Ttimeout`、人工接管和回家逻辑，完全够双 A。

## 条目 1: POI coverage-navigation and scan supervisor

- 控制对象：四足机器人覆盖式巡检任务中的 POI 导航与扫描监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个控制四足机器人按 skeleton map 生成的 POI 序列逐点导航、扫描、超时回退、人工接管和最终回 home 的高层任务状态机。
- 判断：算。对象是真实四足机器人导航 supervisor，而不是纯 path planner；原文直接给出状态集、阈值判断、导航超时、人工中断和回 home 逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，摘要，`paper_content.txt` 第 52-65 行
> The method uses the morphological skeleton of a prior 2D navigation map via SLAM to generate a sequence of points of interest (POIs) ... To control the high-level operation, a finite state machine (FSM) is used to switch between two modes: navigating toward a POI using Nav2 and scanning the local surroundings ... The robot managed to reach 86.5% of all waypoints across the five runs.

#### 摘录 B

- 出处：第 7 页，Section `3.3 State machine`，`paper_content.txt` 第 568-607 行
> With a FSM, we can achieve the desired autonomous navigation based on the triggers ... In State: Load Map ... analyzed to generate a list of waypoints ... Finally, it automatically transitions to ... CheckWaypoints.
>
> State: CheckWaypoints ... If there are waypoints remaining ... transitions to State: Check Destination. If there is no waypoint left, it transitions to State: Home.
>
> In State: Check Destination ... If the condition is true, it transitions to State: Scan. Otherwise, it transitions to State: Move.

#### 摘录 C

- 出处：第 7-8 页，Section `3.3 State machine`，`paper_content.txt` 第 612-640 行
> In State: Move, the robot is actuated to navigate toward the desired destination ... if the navigation process exceeds a specified timeout duration Ttimeout, it is also terminated ... if the system detects an interruption by a human operator via the joystick controller ... transition[s] to State: ManualControl.
>
> In State: Scan, the robot performs the procedure to scan the local environment ... it transitions to State: Check Waypoints.
>
> State: ManualControl allows the human operator to take over ... This state transitions to State: Scan once the operator presses a button ...
>
> In State: Home, the robot travels back to its starting position. Once the robot arrives at the starting position, it lies down on the ground and waits for new commands.

### 2. 基于原文整理后的自然语言描述

The quadruped coverage supervisor starts in `Load Map`, where it loads the prior 2D map into SLAM, extracts a waypoint list from the skeleton map, and builds an ordered route that the robot must visit. `CheckWaypoints` either pops the next waypoint into the current-destination variable or transfers execution to `Home` once the waypoint list is empty. `Check Destination` compares the robot pose with the destination pose under the tolerance `δ`; if the robot is already close enough it goes to `Scan`, otherwise it enters `Move`. In `Move`, Nav2 drives toward the waypoint until the position threshold is satisfied or the timeout `Ttimeout` expires, and any joystick interruption cancels autonomy and moves the system to `ManualControl`. After `Scan` the machine returns to `CheckWaypoints`, `ManualControl` hands control back to `Scan` when the operator confirms the placement, and `Home` returns the robot to its start point and waiting posture, so the paper exposes a full POI-visit / scan / timeout / manual-fallback / return-home FSM.

### 3. 逐句溯源

1. 句子 1：The quadruped coverage supervisor starts in `Load Map`, where it loads the prior 2D map into SLAM, extracts a waypoint list from the skeleton map, and builds an ordered route that the robot must visit.
   对应摘录：A, B
2. 句子 2：`CheckWaypoints` either pops the next waypoint into the current-destination variable or transfers execution to `Home` once the waypoint list is empty.
   对应摘录：B
3. 句子 3：`Check Destination` compares the robot pose with the destination pose under the tolerance `δ`; if the robot is already close enough it goes to `Scan`, otherwise it enters `Move`.
   对应摘录：B
4. 句子 4：In `Move`, Nav2 drives toward the waypoint until the position threshold is satisfied or the timeout `Ttimeout` expires, and any joystick interruption cancels autonomy and moves the system to `ManualControl`.
   对应摘录：C
5. 句子 5：After `Scan` the machine returns to `CheckWaypoints`, `ManualControl` hands control back to `Scan` when the operator confirms the placement, and `Home` returns the robot to its start point and waiting posture, so the paper exposes a full POI-visit / scan / timeout / manual-fallback / return-home FSM.
   对应摘录：A, B, C

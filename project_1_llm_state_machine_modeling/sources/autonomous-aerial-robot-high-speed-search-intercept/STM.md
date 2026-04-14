# Autonomous Aerial Robot for High-Speed Search and Intercept Applications - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把高速空中搜索、跟踪、接近、抓球和降落任务明确写成 mission-control FSM，并给出状态列表、事件条件和检测帧数阈值，是一条很清晰的 UAV 高层任务样本。

## 条目 1: Search-follow-catch mission controller

- 控制对象：高速搜索与拦截任务中的无人机 mission-control 控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个根据长距/短距目标检测、球检测和抓取成功事件，在 `SEARCH / FOLLOW / CATCH / LAND` 间切换的无人机任务控制器。
- 判断：算。对象是真实飞行系统的高层任务控制链，不是单独检测模块；原文明确给出状态、事件、检测帧数门槛和各状态的导航职责。

### 1. 原文摘录

#### 摘录 A

- 出处：第 19-20 页，Section `5.5 Mission Control System`
> In this work, a solution based on a FSM for the architecture designed for Challenge 1 has been implemented.
>
> The implemented FSM uses a number of states in order to control different parts of the system.

#### 摘录 B

- 出处：第 20 页，Section `5.5 Mission Control System`
> The following list summarizes the most important states used in the FSM:
>
> START_STATE ... SEARCH ... FOLLOW_LONG_RANGE ... FOLLOW_SHORT_RANGE ... CATCH_BALL ... LAND.
>
> SEARCH : The UAV does a predefined trajectory ... at very low speed and acceleration ...
>
> FOLLOW_LONG_RANGE : Every time there is a new long-range detection, the UAV moves at a high speed to a point 5 m towards the detection in the XY plane.
>
> FOLLOW_SHORT_RANGE : The UAV moves at a high speed towards the detection, maintaining 4 m from the target.
>
> CATCH_BALL : The UAV moves towards the ball detection trying to align the ball position with the gripper.

#### 摘录 C

- 出处：第 20 页，Table 1 `Example events used in the finite state machine`
> START_MISSION The human operator gives the order to the UAV to start the mission
>
> LONG_RANGE_UAV_DETECTED There are 3 detections on 5 consecutive frames from the Long-Range Detector.
>
> SHORT_RANGE_UAV_DETECTED There are 2 detections on 4 consecutive frames from the Short-Range Detector.
>
> BALL_DETECTED The ball is detected.
>
> DETECTION_LOST No new detections in 5 consecutive frames
>
> SUCCESSFUL_CATCH Ball is detected by the laser sensor inside gripper.

### 2. 基于原文整理后的自然语言描述

The aerial robot executes the search-and-intercept mission through a finite-state mission controller whose main states are `START_STATE`, `SEARCH`, `FOLLOW_LONG_RANGE`, `FOLLOW_SHORT_RANGE`, `CATCH_BALL`, and `LAND`. After initialization on the ground, the UAV enters `SEARCH`, where it flies a low-altitude semiellipse at low speed so that both UAV detectors can maximize image quality and cover the central part of the arena. When the long-range detector reports the target on `3` out of `5` consecutive frames, the FSM switches to `FOLLOW_LONG_RANGE` and commands a fast motion toward a point `5 m` ahead of the detection in the XY plane; once short-range detections are confirmed on `2` of the last `4` frames, it moves into `FOLLOW_SHORT_RANGE`, disables the long-range detector, and keeps roughly `4 m` from the target. If the ball becomes visible, the controller enters `CATCH_BALL`, aligns the gripper with the ball, and keeps following the planned trajectory even after the ball leaves the camera field of view. If detections are lost for `5` consecutive frames the mission can fall back through the detection-loss logic, whereas a positive laser reading inside the gripper raises `SUCCESSFUL_CATCH`, after which the UAV proceeds to `LAND` and terminates the mission.

### 3. 逐句溯源

1. 句子 1：The aerial robot executes the search-and-intercept mission through a finite-state mission controller whose main states are `START_STATE`, `SEARCH`, `FOLLOW_LONG_RANGE`, `FOLLOW_SHORT_RANGE`, `CATCH_BALL`, and `LAND`.
   对应摘录：A, B
2. 句子 2：After initialization on the ground, the UAV enters `SEARCH`, where it flies a low-altitude semiellipse at low speed so that both UAV detectors can maximize image quality and cover the central part of the arena.
   对应摘录：B
3. 句子 3：When the long-range detector reports the target on `3` out of `5` consecutive frames, the FSM switches to `FOLLOW_LONG_RANGE` and commands a fast motion toward a point `5 m` ahead of the detection in the XY plane; once short-range detections are confirmed on `2` of the last `4` frames, it moves into `FOLLOW_SHORT_RANGE`, disables the long-range detector, and keeps roughly `4 m` from the target.
   对应摘录：B, C
4. 句子 4：If the ball becomes visible, the controller enters `CATCH_BALL`, aligns the gripper with the ball, and keeps following the planned trajectory even after the ball leaves the camera field of view.
   对应摘录：B, C
5. 句子 5：If detections are lost for `5` consecutive frames the mission can fall back through the detection-loss logic, whereas a positive laser reading inside the gripper raises `SUCCESSFUL_CATCH`, after which the UAV proceeds to `LAND` and terminates the mission.
   对应摘录：B, C

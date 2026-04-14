# Development of an Autonomous Driving Vehicle for Garbage Collection in Residential Areas - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（任务级显式时序）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把垃圾收运车的自主驾驶明确写成一个上层 `manual / auto / emergency`、下层 `straight / left turn / right turn / wait` 的分层运动状态机，并给出动作集合、等待释放条件与 `3 m / 6 m / 10 m` 的距离门槛，足以稳定支撑双 A。

## 条目 1: Manual-auto-emergency garbage-collection driving supervisor
- 控制对象：汽车与道路车辆控制领域的垃圾收运车辆分层自主驾驶监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（任务级显式时序）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向居民区垃圾收运任务的车辆运动监督器，用顶层人工/自动/紧急模式和自动模式内部的行驶、转弯、等待子状态管理接管、异常停车、路口等待与跟车避障。
- 判断：算。对象是真实车辆控制系统而不是单纯规划框架；原文直接说“constructed an autonomous driving state machine”，并且把顶层状态、子状态、动作和安全门槛写成完整控制链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 21 页，Figure `14` 附近
> We constructed an autonomous driving state machine that defines the vehicle control state, as shown in Figure 14. This state machine represents the control-state flow of a human-intervened or autonomous driving system. In this paper, the vehicle is divided into three states: a manual state operated by a human, an auto state in which the autonomous driving system operates, and an emergency state in which the vehicle is stopped immediately.

#### 摘录 B
- 出处：第 21-22 页，Figure `14` 说明文字
> The manual state and the auto state are altered by the human or by applying the run/stop button inside the vehicle, the remote control, or the UI. ... the emergency state is switched when applying the emergency button, when an object within the emergency detection range is detected ... or when it is determined that an abnormality (fallback) has occurred in the autonomous driving system during the auto state.
>
> The auto state of the vehicle is divided into a straight, left turn, right turn, and wait. For the vehicle to be in motion, specific actions are needed: drive, low drive, keep distance, acceleration, deceleration, and stop.

#### 摘录 C
- 出处：第 22-23 页，动作与距离门槛说明
> the wait motion makes the vehicle stop and wait in a traffic situation ... configured the vehicle to stop at the stop line of the crosswalk. After waiting enough time, the vehicle releases the waiting motion.
>
> if the corresponding vehicle comes within 3 m, it is changed to Emergency Stop; if it enters within 6 m, Stop, and if it enters within 10 m, it is changed to Keep Distance action.

### 2. 基于原文整理后的自然语言描述

The garbage-collection vehicle is governed by a hierarchical motion supervisor with three top-level modes: `manual`, `auto`, and `emergency`. Human operators or the run/stop interface can switch between `manual` and `auto`, while pressing the emergency button, detecting an obstacle inside the emergency range, or triggering a fallback abnormality forces an immediate transition from `auto` to `emergency`, where the vehicle performs maximum-deceleration stopping until a human explicitly clears the condition. Inside `auto`, the controller further refines behavior into `straight`, `left turn`, `right turn`, and `wait`, and it dispatches motion actions such as `drive`, `low drive`, `keep distance`, `acceleration`, `deceleration`, and `stop` according to the global path and recognized objects. The `wait` substate is used for crosswalk and traffic situations, holding zero speed until enough waiting time has elapsed and resetting that waiting time when nearby objects are detected. Obstacle response is also quantified by lane-relative distance thresholds: an object within `10 m` triggers `keep distance`, within `6 m` triggers `stop`, and within `3 m` escalates to `emergency stop`.

### 3. 逐句溯源

1. 句子 1：The garbage-collection vehicle is governed by a hierarchical motion supervisor with three top-level modes: `manual`, `auto`, and `emergency`.
   对应摘录：A
2. 句子 2：Human operators or the run/stop interface can switch between `manual` and `auto`, while pressing the emergency button, detecting an obstacle inside the emergency range, or triggering a fallback abnormality forces an immediate transition from `auto` to `emergency`, where the vehicle performs maximum-deceleration stopping until a human explicitly clears the condition.
   对应摘录：B
3. 句子 3：Inside `auto`, the controller further refines behavior into `straight`, `left turn`, `right turn`, and `wait`, and it dispatches motion actions such as `drive`, `low drive`, `keep distance`, `acceleration`, `deceleration`, and `stop` according to the global path and recognized objects.
   对应摘录：B
4. 句子 4：The `wait` substate is used for crosswalk and traffic situations, holding zero speed until enough waiting time has elapsed and resetting that waiting time when nearby objects are detected.
   对应摘录：C
5. 句子 5：Obstacle response is also quantified by lane-relative distance thresholds: an object within `10 m` triggers `keep distance`, within `6 m` triggers `stop`, and within `3 m` escalates to `emergency stop`.
   对应摘录：C

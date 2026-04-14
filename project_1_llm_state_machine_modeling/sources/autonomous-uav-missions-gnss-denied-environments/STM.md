# An Efficient Framework for Autonomous UAV Missions in Partially-Unknown GNSS-Denied Environments - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 GNSS-denied 室内任务无人机的高层任务逻辑明确写成 `Idle / Hover / Search / Tracking / Wait for Mission / Select Action` 等状态链，并给出 `10 s` 跟踪与动作执行条件，足以形成双 A 航空任务监督样本。

## 条目 1: GNSS-Denied UAV Mission Supervisor

- 控制对象：GNSS-denied 室内竞赛无人机的高层 mission planner
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用有限状态机统筹无人机起飞、搜索移动目标、持续跟踪、等待地面站任务、执行拍照/降落动作并最终安全返航的任务级控制器。
- 判断：算。对象是真实无人机任务管理器，不是单纯软件框架说明；原文明确写出状态集合、进入条件、`10 s` 跟踪门槛、任务动作类型及回到 `Idle` 的结束链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 41-46 行
> This paper presents a framework for autonomous missions with low-cost Unmanned Aerial Vehicles (UAVs) in Global Navigation Satellite System-denied (GNSS-denied) environments. This paper presents hardware choices and software modules for localization, perception, global planning, local re-planning for obstacle avoidance, and a state machine to dictate the overall mission sequence.

#### 摘录 B

- 出处：第 11 页，`3.6. Mission Planner`，`paper_content.txt` 第 659-670 行
> The high-level mission logic is managed by means of a Finite State Machine (FSM), the representation of which is shown in Figure 4. The FSM dictates the overall UAV behavior while taking on all the challenge tasks exposed in Section 1.1. The mission starts in the Idle state. When the UAV is set to the PX4 offboard mode and receives the takeoff command, the system moves to the Hover state until the Start Search command is received, at which point the system moves into the Search state. ... When the target is found, the system moves into the Tracking state. The tracking of the target must last for 10 s; if the target is lost, the drone starts exploring again.

#### 摘录 C

- 出处：第 12 页，`3.6. Mission Planner`，`paper_content.txt` 第 675-687 行
> At this point, the Ground Control Station (GCS) can send a mission to the drone. A mission consists of a sequence of actions: either land, or take a photo. ... If the action is a land request, then the drone lands, waits 10 s, and takes off again; if the action is a photo request, the drone starts an exploration phase looking for the target that must be shot. ... When an action is completed, the system again enters the Select Action state and the loop repeats until all actions have been executed. Finally, the drone moves to a safe location (away from obstacles) and performs a final landing before returning to the Idle state.

### 2. 基于原文整理后的自然语言描述

The UAV mission planner is modeled as a finite-state supervisor that starts in `Idle`, moves to `Hover` after takeoff, and then enters `Search` to explore the partially-known GNSS-denied arena. Once the down-facing camera detects the moving target, the controller switches to `Tracking`, and it only advances if the target is tracked continuously for `10 s`; otherwise it falls back to `Search` and resumes exploration. After successful tracking, the drone enters `Wait for Mission`, accepts a list of `land` or `photo` actions from the ground station, and iterates through `Select Action` and action-execution states until every requested action is finished. A land action forces a landing, a `10 s` wait, and a new takeoff, while a photo action triggers a local exploration phase around the target cell before image capture and optional retry. When the mission queue is exhausted, the UAV relocates to a safe obstacle-free point, performs a final landing, and returns to `Idle`.

### 3. 逐句溯源

1. 句子 1：The UAV mission planner is modeled as a finite-state supervisor that starts in `Idle`, moves to `Hover` after takeoff, and then enters `Search` to explore the partially-known GNSS-denied arena.
   对应摘录：A, B
2. 句子 2：Once the down-facing camera detects the moving target, the controller switches to `Tracking`, and it only advances if the target is tracked continuously for `10 s`; otherwise it falls back to `Search` and resumes exploration.
   对应摘录：B
3. 句子 3：After successful tracking, the drone enters `Wait for Mission`, accepts a list of `land` or `photo` actions from the ground station, and iterates through `Select Action` and action-execution states until every requested action is finished.
   对应摘录：C
4. 句子 4：A land action forces a landing, a `10 s` wait, and a new takeoff, while a photo action triggers a local exploration phase around the target cell before image capture and optional retry.
   对应摘录：C
5. 句子 5：When the mission queue is exhausted, the UAV relocates to a safe obstacle-free point, performs a final landing, and returns to `Idle`.
   对应摘录：C

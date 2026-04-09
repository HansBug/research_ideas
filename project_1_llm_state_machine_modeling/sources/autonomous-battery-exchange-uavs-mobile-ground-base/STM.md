# Autonomous Battery Exchange of UAVs with a Mobile Ground Base - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行, 协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把移动地面基站的换电任务写成 `HFSM + collaborative plan TST`，不仅给出顶层执行器树，还明确展开 `find / dock / lock / switch / release / deploy` 这些跨代理链路，是很强的 `UAV mission supervisor` 样本。

## 条目 1: UAV battery-exchange mission executor

- 控制对象：航空航天与飞行/空管控制领域的移动地面基站无人机换电任务执行监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行, 协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 `SHERPA` 项目里由移动地面基站、机械臂、`rover`、`SBox` 与 `wasp` 无人机协同执行的换电任务监督器，用层次任务树和 `HFSM` 组织定位、靠近、抓取、对接、换电、释放与重新部署。
- 判断：算。对象是实际多机器人协同服务系统的任务控制器，不是单纯规划框架；原文直接给出 `HFSM`、协作执行树、代理委派关系以及完整 `change_batt` 主链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / `Collaborative Mission Framework` 引入，`paper_content.txt` 第 5-16, 147-154 行
> This paper presents the autonomous battery exchange operation for small scale UAVs, using a mobile ground base that carries a robotic arm and a service station containing the battery exchange mechanism.
>
> The design and control of the system and its components are presented in detail, as well as the collaborative software framework used to plan and execute complex missions.
>
> This section presents the distributed communication and control architecture, that enables a larger heterogeneous human-robot team to effectively work together in a robust and versatile manner, even under adverse operating conditions.

#### 摘录 B

- 出处：第 4 页，对 `SBox` 与机械臂高层规划器的说明，`paper_content.txt` 第 305-315, 459-469 行
> The SHERPA box is designed to function as the service station for docking and replenishing the wasps, as well as the computational and communications hub for the mission ... which allows to service two wasps simultaneously.
>
> The arm’s high-level planner includes a delegation module that interacts with the other agents, and a hierarchical finite-state machine (HFSM) based on the ROS decision making package, where the states of the HFSM are triggered by executors and represent the leaf nodes of the TST.

#### 摘录 C

- 出处：第 6 页，`Battery Exchange Operation` / Figure 10，`paper_content.txt` 第 485-522 行
> The battery exchange operation is a relatively simple expanded collaborative plan TST ...
>
> pick /arm
> find_wasp /arm
> disarm_wasp /wasp0
> lock_wasp /SBox
> switch_batt /SBox
> release_wasp /SBox
> move_to /rover
> dock /arm
> place_wasp /arm
> change_batt /GRA
> dock_wasp /GRA
> deploy_wasp /GRA
>
> Internal nodes of the executor represent control statements, leaf nodes represent domain specific tasks.

#### 摘录 D

- 出处：第 6 页，执行链说明，`paper_content.txt` 第 523-543 行
> The change batt executor is typically triggered by either the human operator, or fully autonomously by the UAV, which will request the battery exchange after landing when its power is running low.
>
> After accepting the delegation, the GRA expands the executor and commands the arm to localize the UAV through the find wasp executor.
>
> The dock wasp executor then in turn expands into the move to, pick, and dock executors, which command the rover to approach the UAV, and the arm to grasp and move the UAV into the docking position on the SHERPA box.
>
> The following lock wasp, switch batt, and release wasp executors are delegated to the SBox ... Finally the UAV is deployed again by placing it on the ground, and moving the GRA away from it.

### 2. 基于原文整理后的自然语言描述

The retained control object is a hierarchical mission executor for autonomous UAV battery replacement, deployed on a mobile ground base that combines a rover, robotic arm, service box, and the landed UAV. At the implementation level, the arm planner is explicitly organized as an `HFSM` whose executor-triggered states correspond to leaf tasks in a collaborative task-specification tree, while the `SBox` acts as both the docking station and the communication hub for the mission. The top-level `change_batt` executor expands into a layered task tree containing `find_wasp`, `disarm_wasp`, `dock_wasp`, `lock_wasp`, `switch_batt`, `release_wasp`, `place_wasp`, and `deploy_wasp`, with the individual tasks delegated across the `arm`, `rover`, `wasp`, `SBox`, and `GRA` agents. The most important nested branch is `dock_wasp`, which itself expands into `move_to`, `pick`, and `dock`, so the controller first brings the rover into range, then grasps the UAV, and finally inserts it into the service box. After the `SBox` locks the UAV, replaces the depleted battery, and releases it, the system places the UAV back on the ground and moves the ground base away so that both agents can resume their missions. Because the same plan uses delegation, agent-to-agent messaging, and service hardware that can support two wasps simultaneously, the published design is not just a flat sequence but a layered, cooperative mission supervisor.

### 3. 逐句溯源

1. 句子 1：The retained control object is a hierarchical mission executor for autonomous UAV battery replacement, deployed on a mobile ground base that combines a rover, robotic arm, service box, and the landed UAV.
   对应摘录：A, B
2. 句子 2：At the implementation level, the arm planner is explicitly organized as an `HFSM` whose executor-triggered states correspond to leaf tasks in a collaborative task-specification tree, while the `SBox` acts as both the docking station and the communication hub for the mission.
   对应摘录：A, B
3. 句子 3：The top-level `change_batt` executor expands into a layered task tree containing `find_wasp`, `disarm_wasp`, `dock_wasp`, `lock_wasp`, `switch_batt`, `release_wasp`, `place_wasp`, and `deploy_wasp`, with the individual tasks delegated across the `arm`, `rover`, `wasp`, `SBox`, and `GRA` agents.
   对应摘录：C, D
4. 句子 4：The most important nested branch is `dock_wasp`, which itself expands into `move_to`, `pick`, and `dock`, so the controller first brings the rover into range, then grasps the UAV, and finally inserts it into the service box.
   对应摘录：D
5. 句子 5：After the `SBox` locks the UAV, replaces the depleted battery, and releases it, the system places the UAV back on the ground and moves the ground base away so that both agents can resume their missions.
   对应摘录：D
6. 句子 6：Because the same plan uses delegation, agent-to-agent messaging, and service hardware that can support two wasps simultaneously, the published design is not just a flat sequence but a layered, cooperative mission supervisor.
   对应摘录：A, B, C

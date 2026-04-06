# Increasing the Autonomy of the Unmanned Aerial Platform - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `FCC + MC` 协同下的航路点任务流、碰撞处理和失高救援写成了三正交状态并由 supervisor 仲裁优先级，主链与异常链都足够完整。

## 条目 1: Orthogonal waypoint-reconnaissance and emergency supervisor

- 控制对象：具备任务自治能力的无人机航路点飞行、识别任务与应急处置监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是航空航天与飞行控制领域的 UAV autonomy supervisor，用于在 `FCC` 与 `MC` 协同下管理 waypoint mission、SAR reconnaissance、collision avoidance 和 altitude-loss rescue。
- 判断：算。对象是实际无人机任务控制架构中的高层状态机，不是只有 SysML 展示；原文明确写出了三正交状态、基础飞行链、风况触发的参数修改、碰撞/障碍绕避链和失高后稳定或开伞的应急分支。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，`WAYPOINT mode` 与 hazardous scenarios，`paper_content.txt` 第 312-330 行
> The figure shows the basic case - Flight in WAYPOINT mode ... autonomous scenarios are represented by the SAR Object Recognition in Autonomous Mode scenario ... Hazardous scenarios are described by the collection of UAV Collision Avoidance scenarios ... sudden loss of flight altitude ... potential air collision ... terrain obstacle.

#### 摘录 B

- 出处：第 4-5 页，`Figure 3` 对 orthogonal states 与基本序列的说明，`paper_content.txt` 第 331-365 行
> Figure 3 shows a state machine model ... The model shows three orthogonal states. Actions described in these states can be performed in parallel ... The basic scenario ... consists in going through the following states in sequence: FWM1 -> FWM2 -> FWM3 -> FWM2 -> SUP -> FWM1.

#### 摘录 C

- 出处：第 5 页，`FWM3 / FWM2` 中的风况与识别参数处理，`paper_content.txt` 第 375-386 行
> In the case when the UAV starts recognition with the use of SAR ... entry:checkWindParams() ... do:calculateFCCparams() ... In case of strong wind, the MC sends a request to the FCC to minimize the roll angle ... do:setFCCparams() ... exit:resetFCCparams().

#### 摘录 D

- 出处：第 5 页，`SUPERVISOR` 下的碰撞与失高应急序列，`paper_content.txt` 第 394-455 行
> The supervisor module is responsible for the appropriate assessment of the importance of the states ... When a dangerous situation is detected ... FWM1 -> FWM2 -> SUP -> FWM4 -> FWM2 -> SUP -> FWM1 ... When an uncontrolled loss of height is detected ... FWM1 -> FWM2 -> SUP -> FWM5 -> FWM2 -> SUP ... If the attempt to stabilize the flight fails, the parachute discharge ends the UAV flight.

### 2. 基于原文整理后的自然语言描述

The UAV autonomy model is organized as three orthogonal states that run in parallel: the waypoint-and-reconnaissance mission flow, the altitude-loss emergency branch, and the collision/terrain-hazard branch, with the `FCC` and `MC` dividing low-level flight control and mission-level reasoning. In the basic scenario, the controller cycles through `FWM1 -> FWM2 -> FWM3 -> FWM2 -> SUP -> FWM1`, which corresponds to waypoint selection, flight to the point, optional sensor configuration for recognition, threat checking, and return to the next waypoint decision. During SAR recognition, `entry:checkWindParams()`, `do:calculateFCCparams()`, `do:setFCCparams()`, and `exit:resetFCCparams()` adjust the allowable roll angle according to wind and recognition needs by having the mission computer request parameter changes in the flight computer. If the supervisor detects danger, it gives priority to the more severe branch: collision or terrain hazards route the machine through `SUP -> FWM4` for emergency avoidance, while uncontrolled altitude loss routes it through `SUP -> FWM5`, where the UAV either stabilizes flight or deploys the parachute and terminates the mission.

### 3. 逐句溯源

1. 句子 1：The UAV autonomy model is organized as three orthogonal states that run in parallel: the waypoint-and-reconnaissance mission flow, the altitude-loss emergency branch, and the collision/terrain-hazard branch, with the `FCC` and `MC` dividing low-level flight control and mission-level reasoning.
   对应摘录：A, B
2. 句子 2：In the basic scenario, the controller cycles through `FWM1 -> FWM2 -> FWM3 -> FWM2 -> SUP -> FWM1`, which corresponds to waypoint selection, flight to the point, optional sensor configuration for recognition, threat checking, and return to the next waypoint decision.
   对应摘录：B
3. 句子 3：During SAR recognition, `entry:checkWindParams()`, `do:calculateFCCparams()`, `do:setFCCparams()`, and `exit:resetFCCparams()` adjust the allowable roll angle according to wind and recognition needs by having the mission computer request parameter changes in the flight computer.
   对应摘录：C
4. 句子 4：If the supervisor detects danger, it gives priority to the more severe branch: collision or terrain hazards route the machine through `SUP -> FWM4` for emergency avoidance, while uncontrolled altitude loss routes it through `SUP -> FWM5`, where the UAV either stabilizes flight or deploys the parachute and terminates the mission.
   对应摘录：D

# Designing a Reliable UAV Architecture Operating in a Real Environment - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然整体偏 UAV 可靠性架构，但其中的 `WAYPOINT` 飞行与 collision-avoidance UML state machine 非常完整，主链、异常链、并行线程和状态内动作都给到了，可直接作为 flight-mission HSM 样本。

## 条目 1: WAYPOINT collision-avoidance mission supervisor

- 控制对象：航空航天与飞行/空管控制领域的航路点飞行与避碰任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是运行在 Mission Computer 上的 UAV mission supervisor，用于在 `WAYPOINT` 模式下串联 next-waypoint flight、传感器配置、紧急情况检测和 collision-avoidance maneuver。
- 判断：算。论文整体带有架构设计色彩，但保留下来的对象是明确的飞行任务状态机；原文给出了 use case 到 state machine 的映射、单线程/双线程实现、状态名、状态内动作以及 nominal / collision 两条执行序列。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> Examples of the transformations from user requirements modeled in the form of Use Cases to platform operation models based on State Machines and then to the final UAV operation algorithms are shown ... The presented results are based on a practical example of an algorithm for detecting an air collision situation of two platforms.

#### 摘录 B

- 出处：第 9-10 页，Section `3.2 The Modeling of an Emergency Situation` 与 Figure 2 / Figure 3
> Figure 1 shows an exemplary Use Case model that describes the flight of the UAV in the WAYPOINT mode ... The basic Use Case must include handling an emergency situation in flight, which concerns the occurrence of a potential collision of air platforms.
>
> Figure 3 shows the State Machine model ... In this model, there are two parallel threads, each affecting how the other works. The critical functions for testing emergencies are performed serially in a separate thread.
>
> `FWM1: Next waypoint selection`, `FWM2: Flight to waypoint`, `FWM3: Set the recognition sensor`, `FWM4: Collision avoidance procedure`, `SUP: supervisor`, `ExS1: UAV collision avoidance test`, `ExS2: Collision with obstacle test`.

#### 摘录 C

- 出处：第 10 页，Section `3.2 The Modeling of an Emergency Situation`
> In our case, the functions do:testCollision() and do:findWPT() are given numerical algorithms that are used to implement them.
>
> The basic scenario carried out by the UAV, which performs a flight in the route mode, consists in going through the following states in sequence:
> FWM1 -> FWM2 -> FWM3 -> FWM2 -> SUP -> FWM1
>
> An alternative processing scenario will occur when a parallel process ... will execute the testCollision() function ... At this point, an alternative scenario is realized:
> FWM1 -> FWM2 -> SUP -> FWM4 -> FWM2 -> SUP -> FWM1
>
> As part of handling emergency situations, potential collisions between aerial platforms and a collision with a terrain obstacle are tested.

### 2. 基于原文整理后的自然语言描述

The retained control object is a UAV mission supervisor for `WAYPOINT` flight that combines nominal waypoint progression with emergency collision handling inside one state-machine design. Its nominal route chain is `FWM1 Next waypoint selection -> FWM2 Flight to waypoint -> FWM3 Set the recognition sensor -> FWM2 -> SUP -> FWM1`, so waypoint selection, flight progress, sensor setup, and supervisory checking are all explicit mission states. When the emergency side detects a possible collision through `do:testCollision()`, the controller diverts into `FWM4 Collision avoidance procedure`, where `do:findWPT()` determines the avoidance waypoint before the vehicle resumes route flight. In the two-core formulation, flight-to-waypoint handling and exceptional-situation checking are separated into parallel threads, with `SUP` synchronizing the mission thread and the emergency-test thread. The emergency side also distinguishes `ExS1 UAV collision avoidance test` from `ExS2 Collision with obstacle test`, so both aircraft-conflict and terrain-obstacle checks are part of the same layered UAV HSM.

### 3. 逐句溯源

1. 句子 1：The retained control object is a UAV mission supervisor for `WAYPOINT` flight that combines nominal waypoint progression with emergency collision handling inside one state-machine design.
   对应摘录：A, B
2. 句子 2：Its nominal route chain is `FWM1 Next waypoint selection -> FWM2 Flight to waypoint -> FWM3 Set the recognition sensor -> FWM2 -> SUP -> FWM1`, so waypoint selection, flight progress, sensor setup, and supervisory checking are all explicit mission states.
   对应摘录：B, C
3. 句子 3：When the emergency side detects a possible collision through `do:testCollision()`, the controller diverts into `FWM4 Collision avoidance procedure`, where `do:findWPT()` determines the avoidance waypoint before the vehicle resumes route flight.
   对应摘录：B, C
4. 句子 4：In the two-core formulation, flight-to-waypoint handling and exceptional-situation checking are separated into parallel threads, with `SUP` synchronizing the mission thread and the emergency-test thread.
   对应摘录：B
5. 句子 5：The emergency side also distinguishes `ExS1 UAV collision avoidance test` from `ExS2 Collision with obstacle test`, so both aircraft-conflict and terrain-obstacle checks are part of the same layered UAV HSM.
   对应摘录：B, C

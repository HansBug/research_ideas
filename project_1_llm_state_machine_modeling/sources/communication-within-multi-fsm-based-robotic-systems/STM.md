# Communication Within Multi-FSM Based Robotic Systems - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：虽然论文整体同时讨论方法与通信模型，但其中的 table-tennis ball collecting robot 给出了清晰的 `search / collect / avoid` 控制层级、感知输入、输出命令和终止条件，是一个可直接入账的 `⚙️` 方向 HSM 样本。

## 条目 1: Table-tennis ball collecting robot search-collect-avoid hierarchy

- 控制对象：通用控制领域的乒乓球收集移动机器人控制子系统
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用层次 FSM 组织的移动机器人控制器，上层负责 `search / collect / avoid` 任务切换，下层通过 camera、sonar、body 和 vacuum 子系统完成目标跟踪、避障与吸附动作。
- 判断：算。虽然论文主题含通信与 LLFSM 实现方法，但正文对 ball-collecting robot 的控制对象、状态、输入缓冲、输出命令、transition function 和 terminal condition 都给出了明确证据，可直接提炼为状态机描述样本。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> The design methodology is exemplified with a rudimentary table tennis ball-collecting robot. ... The resulting system design is transformed into a system composed of a whiteboard providing communication means and logically labelled FSMs (LLFSMs) defining the system behaviour.

#### 摘录 B

- 出处：第 12 页，`7.1 Specification / Structure`
> This agent contains: the control subsystem cbc and four virtual subsystems: rbc,cam, rbc,sonar, ebc,body, ebc,vacuum ... The real receptor Rbc,cam detects balls, whilst the real receptor Rbc,sonar detects obstacles. ... The cbc commands both virtual effectors ebc,body and ebc,vacuum using the information obtained from rbc,cam and rbc,sonar.

#### 摘录 C

- 出处：第 12-13 页，`Activities`
> The activities of cbc are defined using a hierarchical FSM cFbc presented in Fig. 6. Each state of the FSM cFbc is associated with the corresponding behaviour: cBbc,search (robot searches for the balls within the environment), cBbc,collect (robot collects balls) and cBbc,avoid (robot avoids obstacles).

#### 摘录 D

- 出处：第 12-13 页，`Canonical decomposition of the transition function`
> In every iteration of the behaviour, cBbc,collect a new desired velocity of the robot is calculated ... Using the X coordinate of the centre of the ball with respect to the centre of the image, an offset is computed that is used to navigate the robot towards the ball. ... The behaviour stops iterating when the terminal condition is fulfilled: not ball_det or obst_det.

#### 摘录 E

- 出处：第 13-14 页，`Other behaviours / Implementation`
> Behaviour cBbc,search is responsible for moving the robot in search for the balls. It terminates when either a ball or an obstacle is detected. Whenever an obstacle is detected behaviour cBbc,avoid is invoked. It uses the bug algorithm for obstacle avoidance.

### 2. 基于原文整理后的自然语言描述

The ball-collecting robot is organized as a hierarchical controller whose top-level state machine switches between `search`, `collect`, and `avoid` behaviors according to ball detections and obstacle detections coming from camera and sonar subsystems. In the `search` state the robot explores the environment until either a ball or an obstacle is perceived, while `collect` drives the robot toward the detected ball by computing a body-motion command from the ball’s image offset and radius and by turning the vacuum on once the ball appears large enough. If the sonar or the terminal condition reports an obstacle during collection, the controller exits that behavior and invokes `avoid`, which uses a bug-style obstacle-avoidance routine before returning to the nominal mission flow. The system is not only state-based at the top level: each behavior is itself modeled as a submachine, so the control object is naturally hierarchical rather than a flat sequence. The paper also makes the actuator boundary explicit by routing top-level decisions into body and vacuum effectors, which preserves both the task logic and the execution interface.

### 3. 逐句溯源

1. 句子 1：The ball-collecting robot is organized as a hierarchical controller whose top-level state machine switches between `search`, `collect`, and `avoid` behaviors according to ball detections and obstacle detections coming from camera and sonar subsystems.
   对应摘录：B, C
2. 句子 2：In the `search` state the robot explores the environment until either a ball or an obstacle is perceived, while `collect` drives the robot toward the detected ball by computing a body-motion command from the ball’s image offset and radius and by turning the vacuum on once the ball appears large enough.
   对应摘录：C, D, E
3. 句子 3：If the sonar or the terminal condition reports an obstacle during collection, the controller exits that behavior and invokes `avoid`, which uses a bug-style obstacle-avoidance routine before returning to the nominal mission flow.
   对应摘录：D, E
4. 句子 4：The system is not only state-based at the top level: each behavior is itself modeled as a submachine, so the control object is naturally hierarchical rather than a flat sequence.
   对应摘录：A, C
5. 句子 5：The paper also makes the actuator boundary explicit by routing top-level decisions into body and vacuum effectors, which preserves both the task logic and the execution interface.
   对应摘录：B, D

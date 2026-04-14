# Underground Multi-robot Systems at Work: a revolution in mining - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把地下矿井 `Deployer + Stinger` 钻孔任务明确拆成 mission modules，并用 per-robot HFSM 加 ROS2 trigger message 串成顺序协同控制链，足以形成新的多机器人任务监督样本。

## 备注

- `paper_content.txt` 对 Figure `2-4` 的图中文字保留有限；本条目中的模块名与局部状态名已回 `paper.pdf` 视觉核对后写入。

## 条目 1: Trigger-Chained Deployer-Stinger Mission HFSM

- 控制对象：通用机器人与多机器人协同领域的地下矿井 `Deployer-Stinger` 协同部署与钻孔任务监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向地下矿井 drilling phase 的多机器人任务监督器，由 `Deployer` 和 `Stinger` 各自执行本机 HFSM，并通过 ROS2 trigger message 串成整体部署、锚定和钻孔流程。
- 判断：算。对象是实际地下作业机器人系统的任务级控制，而不是泛系统集成说明；原文明确给出 mission modules、per-robot HFSM、trigger pipeline，以及 `Move To DeployPose` 和 `Centering` 等关键状态。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 13-21 行
> Our proposed system utilizes Hierarchical Finite State Machine (HFSM) behaviors to structure complex task execution across heterogeneous robotic platforms. Each robot has its own HFSM behavior to perform sequential autonomy while maintaining overall system coordination, achieved by triggering behavior execution through inter-robot communication.

#### 摘录 B

- 出处：第 2 页，Section `Concept of Operation (mission)`，`paper_content.txt` 第 171-180 行
> This paper focuses on the drilling phase of the mission ... the Deployer robot uses its onboard sensors to analyze the local terrain and determine both the most suitable drilling site and the optimal deployment configuration for the Stinger robot. It then retrieves the stinger robot and, using its onboard manipulator, precisely places it at the selected location. The Stinger robot anchors itself to the tunnel surface and autonomously executes the drilling operation.

#### 摘录 C

- 出处：第 3-4 页，Section `Software Architecture and Mission Modules` / Figure `2`，`paper_content.txt` 第 252-280 行，回 PDF 图面核对
> The high-level autonomous drilling mission must be broken down into discrete software modules that correspond to specific robot behaviors. ... We utilized a high-level behavioral control strategy, HFSMs, to deploy the robots. ... the behavior control of a robot triggers the behavior control of another robot. This establishes a sequential control of the whole mission. ... Figure 2 shows the mission chain `3D Environment Mapping -> Stinger Robot Deployment Analysis -> Stinger Robot Deployment -> Stinger Robot Anchoring -> Drilling Execution -> Reposition Stinger Robot -> Mission Completed`.

#### 摘录 D

- 出处：第 5 页，Stinger behavior / evaluation，`paper_content.txt` 第 375-404 行
> The high-level behavior to control the deployment sequence of the stinger robot is shown in fig.4. The `Centering` state calls the `move motor` action server ... left stinger moves to its specified position, then right stinger moves to its specified position. After reaching desired pose, `Centering` pings the IP of Deployer to send the other trigger message. ... after picking up the Stinger robot and placing it in deployment pose, the UR10 behavior state `Move To DeployPose` sends the trigger message to the Stinger robot. Upon receiving the trigger message, the Stinger robot starts executing its own behavior.

### 2. 基于原文整理后的自然语言描述

The drilling-phase controller is organized as a hierarchical multi-robot mission supervisor rather than a single flat task script. At the mission level, the paper decomposes the underground operation into the ordered module chain `3D Environment Mapping`, `Stinger Robot Deployment Analysis`, `Stinger Robot Deployment`, `Stinger Robot Anchoring`, `Drilling Execution`, `Reposition Stinger Robot`, and `Mission Completed`. This top-level chain is hierarchical because each participating robot runs its own HFSM behavior underneath the mission modules instead of receiving one monolithic centralized command stream. Coordination is achieved through protocol-like trigger messages: once one robot finishes its current behavior, it publishes a ROS2 trigger that starts the next robot's behavior, so the complete mission becomes a trigger-chained sequential controller across robots. The paper then gives a concrete nested behavior example on the Stinger side, where the `Centering` state calls the `move motor` action server and sequentially positions the left and right anchoring legs before notifying the Deployer. It also gives the Deployer-side execution point `Move To DeployPose`, which sends the trigger that hands control from the UR10 deployment behavior to the Stinger anchoring behavior.

### 3. 逐句溯源

1. 句子 1：The drilling-phase controller is organized as a hierarchical multi-robot mission supervisor rather than a single flat task script.
   对应摘录：A, C
2. 句子 2：At the mission level, the paper decomposes the underground operation into the ordered module chain `3D Environment Mapping`, `Stinger Robot Deployment Analysis`, `Stinger Robot Deployment`, `Stinger Robot Anchoring`, `Drilling Execution`, `Reposition Stinger Robot`, and `Mission Completed`.
   对应摘录：B, C
3. 句子 3：This top-level chain is hierarchical because each participating robot runs its own HFSM behavior underneath the mission modules instead of receiving one monolithic centralized command stream.
   对应摘录：A, C
4. 句子 4：Coordination is achieved through protocol-like trigger messages: once one robot finishes its current behavior, it publishes a ROS2 trigger that starts the next robot's behavior, so the complete mission becomes a trigger-chained sequential controller across robots.
   对应摘录：A, C, D
5. 句子 5：The paper then gives a concrete nested behavior example on the Stinger side, where the `Centering` state calls the `move motor` action server and sequentially positions the left and right anchoring legs before notifying the Deployer, while the Deployer-side `Move To DeployPose` state is the handoff point that triggers the Stinger behavior.
   对应摘录：D

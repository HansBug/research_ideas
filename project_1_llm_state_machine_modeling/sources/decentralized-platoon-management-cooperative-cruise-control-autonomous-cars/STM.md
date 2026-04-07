# Decentralized Platoon Management and Cooperative Cruise Control of Autonomous Cars with Manoeuvre Coordination Message - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、并行、协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把车队编组管理明确写成“复合主状态机 + 并行距离状态机 + MCM 协议交互”的层次结构，状态名、子状态和通信依据都很完整，是高质量的车队管理 HSM 样本。

## 条目 1: Composite Able-State Platoon Manager with Parallel Distance Machine

- 控制对象：汽车与道路车辆控制领域的去中心化车队编组与跟驰状态管理器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、并行、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个依赖 `V2V + MCM` 报文的车队管理器，用一个带复合状态 `Able` 的主状态机和一个并行距离状态机共同管理“能否编队、正在加入、保持近距、退出编队”等车辆行为。
- 判断：算。对象是自动驾驶车辆的决策子系统而非通信协议本身；原文明确给出两个状态机、复合状态、子状态、并行职责和报文字段依据，完全符合 HSM 样本要求。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 8-14 行
> In this paper, based on V2V communication between automated vehicles by using Manoeuvre Coordination Message (MCM), a decentralized platoon management is designed and implemented to manage the platooning state of each vehicle and when the vehicles are in a platoon or joining one, a cruise controller is designed and implemented to guarantee the desired headway to a preceding vehicle.

#### 摘录 B

- 出处：第 5 页，Section 4.1 `Platoon Management`，`paper_content.txt` 第 310-330 行
> In this work we have used the Manoeuvre Coordination Message (MCM) ... The platoon management consists of two state machines, Platooning state machine and Distance state machine ... each vehicle ... has an implemented set of two separate state machines that cover the multiple potential states for platooning ... the distance state machine ... react[s] to a merge of other cars.

#### 摘录 C

- 出处：第 5-6 页，状态说明与 MCM 字段，`paper_content.txt` 第 333-376 行
> The platoon state machine ... If the vehicle is unable to create or join a platoon ... transition to the state “Not able” ... The state "able" is a composite state ... divided into four sub-states. “Want to form”, “Joining a platoon”, “in a platoon” and “Leaving a platoon”.  
> The state "joining" ... the distance state machine has a transition to “close distance” ...  
> these states can be implicitly extracted from the MCM message.

### 2. 基于原文整理后的自然语言描述

The proposed platoon-management module is a decentralized vehicle-cooperation controller built on top of `V2V` communication with `MCM` messages rather than on a standalone car-following heuristic. Each vehicle runs two state machines in parallel: a primary platooning machine that represents the vehicle’s current platoon status and a distance machine that manages whether normal or close headway should be maintained. The primary machine is hierarchical, because its default state `Able` is explicitly declared as a composite state and is further divided into `Want to form`, `Joining a platoon`, `In a platoon` and `Leaving a platoon`, while failure or driver deactivation leads to `Not able`. The paper also states that the other vehicle’s platooning intention is inferred from `MCM` contents such as tolerated distances and planned trajectory, so the controller couples hierarchical state logic with protocol-mediated coordination.

### 3. 逐句溯源

1. 句子 1：The proposed platoon-management module is a decentralized vehicle-cooperation controller built on top of `V2V` communication with `MCM` messages rather than on a standalone car-following heuristic.
   对应摘录：A, B
2. 句子 2：Each vehicle runs two state machines in parallel: a primary platooning machine that represents the vehicle’s current platoon status and a distance machine that manages whether normal or close headway should be maintained.
   对应摘录：B
3. 句子 3：The primary machine is hierarchical, because its default state `Able` is explicitly declared as a composite state and is further divided into `Want to form`, `Joining a platoon`, `In a platoon` and `Leaving a platoon`, while failure or driver deactivation leads to `Not able`.
   对应摘录：C
4. 句子 4：The paper also states that the other vehicle’s platooning intention is inferred from `MCM` contents such as tolerated distances and planned trajectory, so the controller couples hierarchical state logic with protocol-mediated coordination.
   对应摘录：A, C

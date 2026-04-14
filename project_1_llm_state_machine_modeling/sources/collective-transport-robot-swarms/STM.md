# Collective transport of arbitrarily shaped objects using robot swarms - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把仓储群体机器人搬运策略明确实现为 FSM，并给出搜索、招募、安全举升、集体搬运之间的状态与触发条件，适合直接进入双 A 样本主集。

## 条目 1: Swarm safe-lift and collective-transport controller

- 控制对象：工业自动化与离散制造领域的仓储群体机器人集体搬运控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向仓储大件搬运的分布式群体机器人控制器，用有限状态机组织对象搜索、对象下方聚集、安全举升判定、举升请求以及集体搬运。
- 判断：算。对象是实际物流/仓储搬运系统里的机器人控制逻辑，原文明确给出了 FSM、本地安全举升判据、lift request-response 机制以及具体状态名。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，`3.2 Collective transport strategy`，行 214-224
> As illustrated in Fig. 2, a finite-state machine (FSM) is implemented on the robots to select which behavior(s) to utilize for any given situation. ... The three main phases are object search, recruitment of sufficient agents for safe lift and transport, and collective transport.

#### 摘录 B

- 出处：第 4 页，`3.3 Criteria for a safe lift and transport`，行 225-279
> Positioned agents monitor the state of nearby agents ... Once all positioned agents have fulfilled either one of the criteria, the swarm collectively decides that it is now safe to lift and transport the object. Agent positioned near the border of the object ... records the number of visits from randomly walking agents ... Agent positioned within the object ... observes its local neighborhood ... if there are more than a predefined minimum number of positioned neighbor agents ... the agent evaluates itself to be part of a locally well-distributed group that is ready to lift and transport the object safely.

#### 摘录 C

- 出处：第 4 页，`3.4 Collective decision making`，行 287-307
> Once a positioned agent fulfills either of the previously outlined criteria, it changes into the locally safe to lift state, in which the robot initiates a collective lift request. ... Each agent that switches into the locally safe to lift state sends out a lift request to all agents underneath this specific object. All agents situated underneath the object respond to the request with either a negative ... or positive ... feedback message. ... once the last agent underneath the object has changed to the locally safe to lift state and has not received any negative feedback, the lift is initiated by a lift command.

#### 摘录 D

- 出处：第 5 页，Figure 3 文字说明，行 353-390
> Positioned agents that fulfill one of the two criteria change to the locally safe to lift state ... the lift request is rejected. The last agent fulfills either of the two criteria and switches to the safe to lift state. This agent successfully requests a collective lift as all other agents are locally ready to lift as well. Upon the successful collective lift request, the requesting agent broadcasts a lift command ... all agents collectively transport the large and arbitrarily shaped object towards the goal direction. ... Agent's states: Walk randomly / Walk randomly within the object / Positioned / Locally safe to lift / Move object.

### 2. 基于原文整理后的自然语言描述

The warehouse swarm controller is implemented as a finite-state machine that organizes robot behavior into three major phases: object search, recruitment for safe lift, and collective transport. At state level, the paper makes the robot roles explicit with the sequence `Walk randomly`, `Walk randomly within the object`, `Positioned`, `Locally safe to lift`, and `Move object`. A positioned robot is allowed to claim local readiness only after satisfying one of two safe-lift criteria: either it is near the object border and has been sufficiently visited by wandering robots, or it is inside the object area and detects enough positioned neighbors to judge the load distribution safe. Once a robot reaches `Locally safe to lift`, it launches a lift request, gathers positive or negative replies from all robots under the same object, and only after the last relevant robot is locally ready does the system broadcast the lift command and transition the group into collective transport.

### 3. 逐句溯源

1. 句子 1：The warehouse swarm controller is implemented as a finite-state machine that organizes robot behavior into three major phases: object search, recruitment for safe lift, and collective transport.
   对应摘录：A
2. 句子 2：At state level, the paper makes the robot roles explicit with the sequence `Walk randomly`, `Walk randomly within the object`, `Positioned`, `Locally safe to lift`, and `Move object`.
   对应摘录：D
3. 句子 3：A positioned robot is allowed to claim local readiness only after satisfying one of two safe-lift criteria: either it is near the object border and has been sufficiently visited by wandering robots, or it is inside the object area and detects enough positioned neighbors to judge the load distribution safe.
   对应摘录：B
4. 句子 4：Once a robot reaches `Locally safe to lift`, it launches a lift request, gathers positive or negative replies from all robots under the same object, and only after the last relevant robot is locally ready does the system broadcast the lift command and transition the group into collective transport.
   对应摘录：C, D

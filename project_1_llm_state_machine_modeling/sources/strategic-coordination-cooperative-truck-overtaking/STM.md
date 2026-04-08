# Strategic Coordination of Cooperative Truck Overtaking Maneuvers - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 cooperative truck overtaking 的战略层直接实现成带角色、距离阈值、会话同步和 timeout 投票的分布式状态机，可稳定形成双 A 协议协同样本。

## 条目 1: V2X-Synchronized Cooperative Truck Overtaking Coordinator

- 控制对象：协同卡车超车机动的战略规划层分布式协调器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是汽车与道路车辆控制领域的 cooperative truck overtaking coordinator，用 overtaker / overtaken 双角色状态任务和 `IDSM` 报文同步整条超车机动。
- 判断：算。对象是实际协同超车机动控制器，不是泛泛通信框架；原文明确给出十个状态、各角色在每个状态中的任务、基于距离的切换条件，以及通过 desired-state timeout 和一致投票实现同步转移的机制。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 8-14 行
> This paper demonstrates how a cooperative truck overtaking maneuver can be coordinated and synchronized via V2X. ... We define which abstract/atomic tasks are involved in the truck overtaking maneuver and assign them to a distributed state machine. ... The simulation of 600 overtaking scenarios demonstrates that the developed concept is adequate and that a transmission frequency of 5 Hz offers the best trade-off between channel load and maneuver quality.

#### 摘录 B

- 出处：第 4 页，`3.1 Strategic Planning`，`paper_content.txt` 第 233-280 行
> In the following, the ten states with the corresponding tasks are described:
>
> 1. Solo (not synchronized) ...
> 2. Initialization ...
> 3. Planning ...
> 4. Approach ... If the safety distance to the overtaken is ≤ 60 m change to 5.
> 5. Secure Gap (pre) ...
> 6. Lane Change (to 2) ...
> 7. Pass ...
> 8. Lane Change (to 1) ...
> 9. Secure Gap (post) ... If the safety distance to the overtaker is ≥ 50 m change to 10.
> 10. End ...
>
> In each state there are abort conditions ... the system returns to state 1.

#### 摘录 C

- 出处：第 5 页，`3.4 IDSM Message`，`paper_content.txt` 第 333-360 行
> In order to synchronize the vehicles in the distributed state machine ... the IMAGinE project designed the IMAGinE Driving Strategy Message (IDSM).
>
> ... the current session and an optional desired session are included. These contain in each case a state with the ID and Payload of the current and the desire state. In the desired state there is also a timeout, for how long can be voted for it.
>
> ... each participant in the session can send a desired state in addition to the current state. As soon as all participants send the same desired state, the system switches synchronously to this state.

### 2. 基于原文整理后的自然语言描述

The strategic planning layer models cooperative truck overtaking as a distributed state machine that runs over two explicit roles, `Overtaker` and `Overtaken`, and progresses through `Solo`, `Initialization`, `Planning`, `Approach`, `Secure Gap (pre)`, `Lane Change (to 2)`, `Pass`, `Lane Change (to 1)`, `Secure Gap (post)`, and `End`. Each state carries role-specific tasks and parameterized conditions, such as entering the pre-gap state when the distance to the overtaken truck falls to `60 m` or less, and completing the maneuver only after the post-gap grows to at least `50 m`. The machine also defines abort conditions for every state so that an impractical or prematurely terminated maneuver returns both participants to `Solo` instead of leaving them in a half-synchronized mode. Synchronization is handled through the `IDSM` message, which carries current and desired states, role assignments, payload data, and a desired-state timeout; once all participants vote for the same desired state, the transition is executed synchronously, and the paper further reports that a `5 Hz` transmission rate gives the best maneuver-quality trade-off.

### 3. 逐句溯源

1. 句子 1：The strategic planning layer models cooperative truck overtaking as a distributed state machine that runs over two explicit roles, `Overtaker` and `Overtaken`, and progresses through `Solo`, `Initialization`, `Planning`, `Approach`, `Secure Gap (pre)`, `Lane Change (to 2)`, `Pass`, `Lane Change (to 1)`, `Secure Gap (post)`, and `End`.
   对应摘录：A, B
2. 句子 2：Each state carries role-specific tasks and parameterized conditions, such as entering the pre-gap state when the distance to the overtaken truck falls to `60 m` or less, and completing the maneuver only after the post-gap grows to at least `50 m`.
   对应摘录：B
3. 句子 3：The machine also defines abort conditions for every state so that an impractical or prematurely terminated maneuver returns both participants to `Solo` instead of leaving them in a half-synchronized mode.
   对应摘录：B
4. 句子 4：Synchronization is handled through the `IDSM` message, which carries current and desired states, role assignments, payload data, and a desired-state timeout; once all participants vote for the same desired state, the transition is executed synchronously, and the paper further reports that a `5 Hz` transmission rate gives the best maneuver-quality trade-off.
   对应摘录：A, C

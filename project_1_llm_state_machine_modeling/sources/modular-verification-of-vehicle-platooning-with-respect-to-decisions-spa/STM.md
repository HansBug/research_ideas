# Modular Verification of Vehicle Platooning with Respect to Decisions, Space and Time - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：Protocol（协议/交互状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：join procedure 的通信、变道、速度/转向接管顺序明确。

## 条目 1: Joining procedure in the refined platooning architecture
- 控制对象：车队控制架构中的 joining procedure
- 状态机类型：Protocol（协议/交互状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G7 车队编入流程）

### 0. 条目识别与判定

- 一句话说明：这是自动驾驶车队控制领域的 joining procedure controller，用于让待加入车辆在 leader 确认后执行变道、切换自动控制并向 leader 回报完成。
- 判断：算。对象是实际 platooning 控制逻辑，原文给出了加入请求、leader 确认、变道、切换 speed/steering controller 以及完成确认的离散流程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section 2，对 joining/leaving procedures 的概括，行 145-148
> We here consider two of the main platooning procedures involved in joining and
> leaving a platoon. Both the joining and leaving procedures are comprised of a series
> of communications between an individual vehicle and the platoon leader aimed to ob-
> tain permission to join/leave or update the leader when the joining/leaving procedure is

#### 摘录 B
- 出处：第 6 页，Section 4，对 joining vehicle steps 的具体描述，行 232-240
> A vehicle intending to join to a platoon initially sends a joining request to the leader
> and waits for conﬁrmation from the leader. When it receives the conﬁrmation, it in-
> structs the vehicle to change lane and waits for the vehicle to send back a successful
> conﬁrmation of changing lane. After receiving the successful conﬁrmation the follower
> switches its speed controller to automatic. When the joining vehicle is close enough
> to the proceeding follower within the platoon the agent instructs the vehicle to switch
> the steering controller to automatic. Finally, the joining vehicle conﬁrms the successful
> joining procedure to the leader. When the joining vehicle receives a reply back from
> the leader, it deduces that the the joining goal has been achieved. The following code

### 2. 基于原文整理后的自然语言描述

The platooning architecture treats joining as an explicit communication procedure between an individual vehicle and the platoon leader. A vehicle that wants to join first sends a joining request to the leader and waits for confirmation; after receiving that confirmation, it instructs the vehicle to change lane and waits for a successful confirmation that the lane change has completed. Once the lane-change confirmation is received, the follower switches its speed controller to automatic, and when the joining vehicle is close enough to the proceeding follower within the platoon, the agent instructs the steering controller to switch to automatic as well. Finally, the joining vehicle confirms the successful joining procedure to the leader and waits for the leader's reply, after which it deduces that the joining goal has been achieved.

### 3. 逐句溯源

1. 句子 1：The platooning architecture treats joining and leaving as explicit procedures carried out through communication between an individual vehicle and the platoon leader.
   对应摘录：A
2. 句子 2：A vehicle that wants to join first sends a joining request to the leader and waits for confirmation; after receiving that confirmation, it instructs the vehicle to change lane and waits for a successful confirmation that the lane change has completed.
   对应摘录：B
3. 句子 3：Once the lane-change confirmation is received, the follower switches its speed controller to automatic, and when the joining vehicle is close enough to the proceeding follower within the platoon, the agent instructs the steering controller to switch to automatic as well.
   对应摘录：B
4. 句子 4：Finally, the joining vehicle confirms the successful joining procedure to the leader and waits for the leader's reply, after which it deduces that the joining goal has been achieved.
   对应摘录：B

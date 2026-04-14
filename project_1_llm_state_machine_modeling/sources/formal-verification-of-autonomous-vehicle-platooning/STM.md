# Formal verification of autonomous vehicle platooning - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Protocol（协议/交互状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：加入和离队流程都给出了逐步的授权、控制器接管/释放与确认约束。

## 条目 1: Joining procedure for a follower vehicle
- 控制对象：车队控制中的 follower joining procedure
- 状态机类型：Protocol（协议/交互状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G7 车队编入流程）

### 0. 条目识别与判定

- 一句话说明：这是自动驾驶车队控制领域的 follower-vehicle joining controller，用于在 leader 授权后完成请求、扩距协调、并线、自动控制接管和完成确认。
- 判断：算。对象是实际 platooning 控制逻辑，原文给出了加入请求、授权、变道、控制器使能和 spacing 恢复的完整协议步骤。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，Section 2.1，对 joining procedure 的描述，行 127-150
> A vehicle can join a platoon either at the end or in the middle with different control
> strategies being used. The joining procedure is as follows:
> a non-member vehicle sends a joining request to the platoon leader, expressing
> the intended position in the platoon;
> if the vehicle has requested to join from the rear, the leader sends back an agree-
> ment provided the maximum platoon length has not been reached and the platoon
> is currently in normal operation;
> if the vehicle requests to join in front of vehicle X ... the leader sends an “increase space”
> command to vehicle X, and when the leader is informed that enough spacing
> has been created (approx. 17 metres), it sends back an agreement to the joining
> vehicle;
> upon receipt of an agreement, the joining vehicle changes its lane ...
> once the vehicle is in the correct lane, its automatic speed controller is enabled
> and it approaches the preceding vehicle;
> when the vehicle is close enough to the preceding vehicle (less than 20 metres),
> its automatic steering controller is enabled and it sends an acknowledgement to
> the leader; and, ﬁnally
> the leader sends a “decrease space” command to vehicle X ... spacing has been back to normal
> (approximately 5 metres)

#### 摘录 B
- 出处：第 4 页，Section 2.1，对 joining safety requirements 的描述，行 152-159
> A vehicle must only initiate joining a platoon, i.e., changing lane, once it has
> received conﬁrmation from the leader.
> Before autonomous control is enabled, a joining vehicle must approach the pre-
> ceding vehicle, in the correct lane.
> Automatic steering controller must only be enabled once the joining vehicle is
> sufﬁciently close to the preceding vehicle.

#### 摘录 C
- 出处：第 6 页，Section 3，对 agent activity sequence 的总结，行 226-228
> Essentially, the decision-making agent’s activity proceeds in sequence: the follower
> has a goal to successfully join the platoon; it initiates changing lane, if it believes it has
> received an agreement from the leader; and the follower achieves the joining goal if it ...

### 2. 基于原文整理后的自然语言描述

To join a platoon, a non-member vehicle sends a joining request to the leader together with the intended platoon position. If the request is for the rear, the leader grants agreement only when the platoon is in normal operation and has not reached the maximum length; if the request is for a middle position, the leader first commands vehicle `X` to increase spacing and only sends agreement after the created gap is about `17` meters. After agreement, the joining vehicle performs a manual lane change, then enables automatic speed control in the correct lane to approach the preceding vehicle, and enables automatic steering only when the distance to that vehicle is less than `20` meters, at which point it sends an acknowledgement to the leader. Finally, the leader commands vehicle `X` to decrease spacing again until the normal gap of about `5` meters is restored. The agent-level safety rules therefore forbid lane change before leader confirmation and forbid autonomous steering before the vehicle is in the correct lane and sufficiently close to the preceding platoon member.

### 3. 逐句溯源

1. 句子 1：To join a platoon, a non-member vehicle sends a joining request to the leader together with the intended platoon position.
   对应摘录：A
2. 句子 2：If the request is for the rear, the leader grants agreement only when the platoon is in normal operation and has not reached the maximum length; if the request is for a middle position, the leader first commands vehicle `X` to increase spacing and only sends agreement after the created gap is about `17` meters.
   对应摘录：A
3. 句子 3：After agreement, the joining vehicle performs a manual lane change, then enables automatic speed control in the correct lane to approach the preceding vehicle, and enables automatic steering only when the distance to that vehicle is less than `20` meters, at which point it sends an acknowledgement to the leader.
   对应摘录：A, B
4. 句子 4：Finally, the leader commands vehicle `X` to decrease spacing again until the normal gap of about `5` meters is restored.
   对应摘录：A
5. 句子 5：The agent-level safety rules therefore forbid lane change before leader confirmation and forbid autonomous steering before the vehicle is in the correct lane and sufficiently close to the preceding platoon member.
   对应摘录：B, C

## 条目 2: Leaving procedure for a platoon member
- 控制对象：车队控制中的 follower leaving procedure
- 状态机类型：Protocol（协议/交互状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是自动驾驶车队控制领域的 member-leaving controller，用于在 leader 授权后增大车距、退出自动控制、变道并完成离队确认。
- 判断：算。对象是实际 platooning 控制逻辑，原文明确给出了 leaving request、authorization、spacing growth、manual takeover 和离队确认顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4-5 页，Section 2.2，对 leaving procedure 与其 safety requirements 的描述，行 160-177
> A vehicle can request to leave platoon at any time. The leaving procedure is:
> a platoon member sends a leaving request to the leader and waits for authorisation;
> upon receipt of ‘leave’ authorisation, the vehicle increases its space from the
> preceding vehicle;
> when maximum spacing has been achieved, the vehicle switches both its speed
> and steering controller to ‘manual’ and changes its lane; and, ﬁnally
> the vehicle sends an acknowledgement to the leader.
> ...
> Except in emergency cases, a vehicle must not leave the platoon without autho-
> risation from the leader.
> When authorised to leave, autonomous control should not be disabled until the
> maximum allowable platoon spacing has been achieved.

### 2. 基于原文整理后的自然语言描述

A platoon member that wants to leave first sends a leaving request to the leader and waits for authorization. After receiving `leave` authorization, it increases the spacing from the preceding vehicle while still remaining under autonomous control. Only when the maximum allowable spacing has been achieved does the vehicle switch both speed and steering control to `manual`, perform the lane change, and then send an acknowledgement to the leader. Except in emergency cases, leaving without leader authorization is forbidden, and autonomous control must remain enabled until the maximum spacing condition has been met.

### 3. 逐句溯源

1. 句子 1：A platoon member that wants to leave first sends a leaving request to the leader and waits for authorization.
   对应摘录：A
2. 句子 2：After receiving `leave` authorization, it increases the spacing from the preceding vehicle while still remaining under autonomous control.
   对应摘录：A
3. 句子 3：Only when the maximum allowable spacing has been achieved does the vehicle switch both speed and steering control to `manual`, perform the lane change, and then send an acknowledgement to the leader.
   对应摘录：A
4. 句子 4：Except in emergency cases, leaving without leader authorization is forbidden, and autonomous control must remain enabled until the maximum spacing condition has been met.
   对应摘录：A

# Formal verification of autonomous vehicle platooning - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：加入和离队流程都给出了逐步的控制约束与安全条件。

## 条目 1: Joining procedure for a follower vehicle
- 控制对象：车队控制中的 follower joining procedure

### 0. 条目识别与判定

- 一句话说明：这是自动驾驶车队控制领域的 follower-vehicle joining controller，用于在 leader 授权后完成请求、并线、接管自动控制和完成确认。
- 判断：算。对象是实际 platooning 控制逻辑，原文给出了加入请求、授权、变道、控制器使能和完成确认的完整步骤。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section 2.1，对 joining procedure 的描述，行 127-150
> A vehicle can join a platoon either at the end or in the middle with different control
> strategies being used. The joining procedure is as follows:
> 3
>
> --- Page 4 ---
> a non-member vehicle sends a joining request to the platoon leader, expressing
> the intended position in the platoon;
> if the vehicle has requested to join from the rear, the leader sends back an agree-
> ment provided the maximum platoon length has not been reached and the platoon
> is currently in normal operation;
> if the vehicle requests to join in front of (for example) vehicle X and the maxi-
> mum platoon length has not been reached, the leader sends an “increase space”
> command to vehicle X, and when the leader is informed that enough spacing
> has been created (approx. 17 metres), it sends back an agreement to the joining
> vehicle;
> upon receipt of an agreement, the joining vehicle changes its lane (changing lane
> is a manual procedure which is performed by a driver);
> once the vehicle is in the correct lane, its automatic speed controller is enabled
> and it approaches the preceding vehicle;
> when the vehicle is close enough to the preceding vehicle (less than 20 metres),
> its automatic steering controller is enabled and it sends an acknowledgement to
> the leader; and, ﬁnally
> the leader sends a “decrease space” command to vehicle X, and when the leader
> is informed that spacing has been back to normal (approximately 5 metres), it

#### 摘录 B
- 出处：第 4 页，Section 2.1，对 joining safety requirements 的描述，行 152-159
> In order to ensure a safe joining operation, the following requirements should be pre-
> served within the agent-based decision-making components of automotive platoon.
> 1. A vehicle must only initiate joining a platoon, i.e., changing lane, once it has
> received conﬁrmation from the leader.
> 2. Before autonomous control is enabled, a joining vehicle must approach the pre-
> ceding vehicle, in the correct lane.
> 3. Automatic steering controller must only be enabled once the joining vehicle is
> sufﬁciently close to the preceding vehicle.

#### 摘录 C
- 出处：第 6 页，Section 3，对 agent activity sequence 的总结，行 226-228
> Essentially, the decision-making agent’s activity proceeds in sequence: the follower
> has a goal to successfully join the platoon; it initiates changing lane, if it believes it has
> received an agreement from the leader; and the follower achieves the joining goal if it

### 2. 基于原文整理后的自然语言描述

To join a platoon, a non-member vehicle sends a joining request to the leader, waits for an agreement, changes lane, and then reports successful joining so that the leader can command spacing back to normal. A joining vehicle must not begin the lane change until it has received confirmation from the leader, and automatic steering is enabled only after the vehicle is close enough to its preceding platoon member. The follower agent therefore proceeds by pursuing the joining goal, initiating the lane change only when agreement is believed to hold, and completing the goal after the prescribed joining steps have been performed.

### 3. 逐句溯源

1. 句子 1：To join a platoon, a non-member vehicle sends a joining request to the leader, waits for an agreement, changes lane, and then reports successful joining so that the leader can command spacing back to normal.
   对应摘录：A
2. 句子 2：A joining vehicle must not begin the lane change until it has received confirmation from the leader, and automatic steering is enabled only after the vehicle is close enough to its preceding platoon member.
   对应摘录：B
3. 句子 3：The follower agent therefore proceeds by pursuing the joining goal, initiating the lane change only when agreement is believed to hold, and completing the goal after the prescribed joining steps have been performed.
   对应摘录：C

## 条目 2: Leaving procedure for a platoon member
- 控制对象：车队控制中的 follower leaving procedure

### 0. 条目识别与判定

- 一句话说明：这是自动驾驶车队控制领域的 member-leaving controller，用于在 leader 授权后增大车距、退出自动控制并完成离队确认。
- 判断：算。对象是实际 platooning 控制逻辑，原文明确给出了 leaving request、authorization、spacing growth 和手动接管顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section 2.2，对 leaving procedure 与其 safety requirements 的描述，行 160-177
> 2.2 Leaving the Platoon
> A vehicle can request to leave platoon at any time. The leaving procedure is:
> a platoon member sends a leaving request to the leader and waits for authorisa-
> tion;
> upon receipt of ‘leave’ authorisation, the vehicle increases its space from the
> preceding vehicle;
> when maximum spacing has been achieved, the vehicle switches both its speed
> and steering controller to ‘manual’ and changes its lane; and, ﬁnally
> the vehicle sends an acknowledgement to the leader.
> 4
>
> --- Page 5 ---
> The two following requirements are necessary in order to meet with the agent-based
> decision-making components of automotive platoon.
> 1. Except in emergency cases, a vehicle must not leave the platoon without autho-
> risation from the leader.
> 2. When authorised to leave, autonomous control should not be disabled until the
> maximum allowable platoon spacing has been achieved.

### 2. 基于原文整理后的自然语言描述

A platoon member requests authorisation from the leader before leaving, increases its spacing after authorisation, and only then switches its speed and steering control to manual. Except in emergency cases, a vehicle must not leave the platoon without authorisation from the leader, and autonomous control should not be disabled until the maximum allowable spacing has been achieved.

### 3. 逐句溯源

1. 句子 1：A platoon member requests authorisation from the leader before leaving, increases its spacing after authorisation, and only then switches its speed and steering control to manual.
   对应摘录：A
2. 句子 2：Except in emergency cases, a vehicle must not leave the platoon without authorisation from the leader, and autonomous control should not be disabled until the maximum allowable spacing has been achieved.
   对应摘录：A

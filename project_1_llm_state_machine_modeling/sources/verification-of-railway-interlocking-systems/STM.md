# Verification of railway interlocking systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：request-check-lock-green-release 的 route lifecycle 写得非常完整。

## 条目 1: Route lifecycle in an SSI interlocking model
- 控制对象：SSI 联锁系统中的 route lifecycle 控制逻辑

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 route lifecycle controller，用于在请求进路后检查安全条件、锁闭资源、开放信号并在列车通过后释放子进路。
- 判断：算。对象是实际 SSI 联锁系统中的 route control logic，原文给出了 route request 到 green signal、subroute locking/release 的完整生命周期。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section 2，对 route command handling 与 subroute release 的说明，行 97-110
> RKM 045 is a route going from signal KM to track 045. The interlocking handles a route command in
> the following manner:
> 1. When a route is requested, it veriﬁes whether the command is safe. This means that the track
> components (points and track circuits) requested should not be already reserved for another route
> (the points P01AM, P02BM, P04AM, P04BM, and the tracks TC01AM, TC02BM, TC04BM for
> RKM 045).
> 2. It commands the points by controlling their actuators (points P01AM, P02BM, P04AM, P04BM
> to the right positions for R KM 045).
> 3. It veriﬁes the new status of the points by comparing the command and the replied status of the
> actuators.
> 4. It then grants access to the train on the route, setting the origin signal of the route to green (KM
> for R KM 045).
> A route is composed of several segments called subroutes, corresponding to its track segments (three
> for route R KM 045). Each of them is locked when the route is set and is released when the train has

#### 摘录 B
- 出处：第 4 页，Section 3，对 route-based interlocking 的说明，行 141-147
> Our interlocking (SSI) is route based which means:
> A route must be successfully controlled by the controller before a train can run through the station.
> The routes interact with the track side components (e.g.: points, signals).
>
> --- Page 5 ---
> S. Busard, Q. Cappart, C. Limbr ´ee, C. Pecheur, P. Schaus 23
> The routes using shared resources (e.g.: points) make use of locking variables in order to prevent

#### 摘录 C
- 出处：第 6 页，Section 3，对 route modules / route request conditions and actions 的说明，行 183-220
> Route modules: The route lifecycle is described in Section 2. The route modules are a straight transla-
> tion of the application data from the SSI language to NuSMV . The state machine of a route includes
> the following states: idle, commanded, proved, and occupied by a train.
> Frame axioms module: This module performs three different tasks:
> Changing the status of the track components according to the train movements.
> Triggering a wheel detector when a track segment is occupied.
> Updating the point position after a command.
> This module depends on both the application data (routes) and the track layout (trains) to know
> when the actions must be done and what are the modiﬁcations to do.
> Given that we want to verify the consistency between the application data and the real track layout,
> we have to consider a separate source for the application data and the layout. Therefore, unlike the other
> modules, the train module is not generated from the application data.
> Put together, these modules constitute a model simulating the behaviour of an interlocking system as
> described in the application data and the behaviour of trains according to the track layout. On this model,
> we can assert and automatically check safety properties with respect to the application data. These
> properties can be expressed on the state of the trains. For example, a collision occurs if two trains are
> both located on the same segment. For instance, in Figure 2, such a collision will occur if the application
> data could allow routes R KM 045 and R CM 044 to be set together.
> 4 Automatic translation of application data
> Among all the application data, only a subset is necessary to verify the security of an interlocking system.
> The rest is either not related to the security or abstracted in our model. Let us now describe the application
> data used in our model.
> Each point can move under a set of conditions. Listing 1 shows how these conditions are represented
> in the SSI code for a particular point. There are two positions for a point: normal and reverse.4Here, the
> 4Normal stands for left and reverse for right.
>
> --- Page 7 ---
> S. Busard, Q. Cappart, C. Limbr ´ee, C. Pecheur, P. Schaus 25
> point P 01AM can be set in a normal position (P 01AM N) only if it is is free to move (U IR(01AM) f).
> There is a similar rule for the reverse position (P 01AM R) .
> 1* P_01AMN U_IR (01 AM) f /* condition for normal position */
> 2* P_01AMR U_IR (01 AM) f /* condition for reverse position */
> Listing 1: SSI code: Conditions allowing a point to move.
> Each route has a set of conditions under which the route request can be granted, and a set of actions
> that have to be done to fulﬁl the request. For example, Listing 2 states that the route from Signal CM
> to Track 044 can only be set if it is not already set (line 2) and if the points are free to be commanded
> and moved to a certain position (lines 3 and 4). The resulting actions are the setting of the route (line
> 6), the command of the points (lines 7 and 8) and the locking of the points (line 9). The route and the

### 2. 基于原文整理后的自然语言描述

When a route is requested, the interlocking first checks whether the command is safe, then commands and locks the required track components, and finally grants access by setting the origin signal of the route to green. Each subroute is locked when the route is set and is released when the train has fully freed the corresponding home track circuit. The route module therefore captures a route lifecycle made of request conditions and the actions needed to fulfil the request.

### 3. 逐句溯源

1. 句子 1：When a route is requested, the interlocking first checks whether the command is safe, then commands and locks the required track components, and finally grants access by setting the origin signal of the route to green.
   对应摘录：A
2. 句子 2：Each subroute is locked when the route is set and is released when the train has fully freed the corresponding home track circuit.
   对应摘录：A
3. 句子 3：The route module therefore captures a route lifecycle made of request conditions and the actions needed to fulfil the request.
   对应摘录：B, C

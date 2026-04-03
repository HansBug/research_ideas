# Verification of railway interlocking systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：Resource-flow（资源流/并发网模型）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：request-check-lock-green-release 的 route lifecycle 写得非常完整，并保住了状态名、资源锁闭和动作链。

## 条目 1: Route lifecycle in an SSI interlocking model
- 控制对象：SSI 联锁系统中的 route lifecycle 控制逻辑
- 状态机类型：Resource-flow（资源流/并发网模型）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G1 铁路联锁进路生命周期）

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 route lifecycle controller，用于在请求进路后检查安全条件、锁闭资源、开放信号并在列车通过后释放子进路。
- 判断：算。对象是实际 SSI 联锁系统中的 route control logic，原文给出了 route request 到 green signal、subroute locking/release 的完整生命周期。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section 2，对 route command handling 与 subroute release 的说明，行 97-116
> RKM 045 is a route going from signal KM to track 045. The interlocking handles a route command in
> the following manner:
> 1. When a route is requested, it veriﬁes whether the command is safe. This means that the track
> components ... should not be already reserved for another route
> 2. It commands the points by controlling their actuators ...
> 3. It veriﬁes the new status of the points by comparing the command and the replied status of the actuators.
> 4. It then grants access to the train on the route, setting the origin signal of the route to green.
> ...
> Each of them is locked when the route is set and is released when the train has
> fully freed the home track circuit of the subroute, releasing the corresponding points.

#### 摘录 B
- 出处：第 4-7 页，Section 3，对 route-based locking variables、state names 与 point/route actions 的说明，行 141-220
> Our interlocking (SSI) is route based which means:
> A route must be successfully controlled by the controller before a train can run through the station.
> ...
> The routes using shared resources (e.g.: points) make use of locking variables in order to prevent ...
> ...
> The state machine of a route includes
> the following states: idle, commanded, proved, and occupied by a train.
> ...
> point P 01AM can be set in a normal position ... only if it is free to move.
> ...
> The resulting actions are the setting of the route, the command of the points and the locking of the points.

### 2. 基于原文整理后的自然语言描述

The route module for `RKM 045` uses the explicit lifecycle states `idle`, `commanded`, `proved`, and `occupied by a train`. When a route request arrives, the interlocking first checks that the required points and track circuits are not already reserved for another route, then commands the points to the positions needed for the route, verifies the actuator replies, and only then sets the origin signal to green. A route is decomposed into subroutes, each subroute is locked when the route is set, and each is released only after the train has fully freed the corresponding home track circuit, releasing the associated points. Because the SSI is route-based, routes interact with signals and points through shared locking variables so that conflicting routes cannot use the same resources at the same time. Point moves are themselves guarded by freedom-to-move conditions, and a successful route action sets the route, commands the points, and locks them as part of the lifecycle.

### 3. 逐句溯源

1. 句子 1：The route module for `RKM 045` uses the explicit lifecycle states `idle`, `commanded`, `proved`, and `occupied by a train`.
   对应摘录：B
2. 句子 2：When a route request arrives, the interlocking first checks that the required points and track circuits are not already reserved for another route, then commands the points to the positions needed for the route, verifies the actuator replies, and only then sets the origin signal to green.
   对应摘录：A
3. 句子 3：A route is decomposed into subroutes, each subroute is locked when the route is set, and each is released only after the train has fully freed the corresponding home track circuit, releasing the associated points.
   对应摘录：A
4. 句子 4：Because the SSI is route-based, routes interact with signals and points through shared locking variables so that conflicting routes cannot use the same resources at the same time.
   对应摘录：B
5. 句子 5：Point moves are themselves guarded by freedom-to-move conditions, and a successful route action sets the route, commands the points, and locks them as part of the lifecycle.
   对应摘录：B

# Modelling Railway Interlocking Tables Using Coloured Petri Nets - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：Resource-flow（资源流/并发网模型）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：route set/release、冲突进路、approach locking 和 flank protection 的文字依据都较充分。

## 条目 1: Route locking and release rules from an interlocking table
- 控制对象：铁路联锁表中的 route locking / release logic
- 状态机类型：Resource-flow（资源流/并发网模型）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G1 铁路联锁进路生命周期）

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 route locking logic，用于根据联锁表决定何时允许列车进入进路、何时禁止冲突进路以及何时释放进路。
- 判断：算。对象是实际联锁控制系统中的进路控制逻辑，原文清楚给出了 route、entry signal、conflict routes、approach locking、release 和 flank protection 规则。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5-6 页，Panthong station control table example，行 176-221
> A collection of track circuits along the reserved section is called a “ route”. An
> entry signal shall be clear to let the train enter the route.
> ...
> Each row in the
> tables represents the requirement how to s et and release each route. For example,
> route 1-3(2) comprises the track circuits 1-3T, 1-71AT, 1-71BT,1-71CT,101BT,
> 111T, 62T, 112T and requires that the points 101, 111 and 112 are in normal
> position.
> ...
> The column “Requires
> Route Normal” shows conﬂict routes. A route cannot be set if any conﬂict routes
> have been set and not yet released. For route 1-3(2) the conﬂict routes are 1-3(1),16(1), 16(2), 32(1), 32(2), 3-3(1), 3-3(2), 2-4(1), 2-4(2), 4-4(1) and 4-4(2). The
> exit (starter) signal of this route is 15, and if home signal 1-3 shows green, then
> starter signal 15 shows green.

#### 摘录 B
- 出处：第 6-7 页，对 route locking / approach locking / release / flank protection 的说明，行 233-259
> Route locking. Route setting involves a collect ion of adjacent track circuits,
> points and signals.
> ...
> To assure the safety, ﬁrstly, the interlocking system veriﬁes that the
> route does not conﬂict with other routes previously set. Secondly, the points
> along the route are locked in the correct positions.
> ...
> Thirdly, the track circuits along the required route are all clear
> or unoccupied so that nothing obstructs the passage of the train. Then the entry
> signal can be cleared (showing yellow or green).
> Approach locking. After a route is set; the point is locked; and the entry
> signal is cleared, if the track circuit in front of (approaching) the entry signal
> is occupied, then the signal man cannot cancel the route and the entry signal
> by the normal procedure.
> ...
> Route 1-3(2) will be released when
> the track circuits 1-3T, 1-71AT, 1-71BT, 1-71CT, 101BT are clear; the track
> circuit 111T is occupied and then clear; and the track circuit 62T is occupied.
> Flank protection.
> ...
> route 1-3(2),
> the track circuit 61T, which is not in the route 1-3(2), shall be unoccupied.

### 2. 基于原文整理后的自然语言描述

A route is the collection of track circuits along a reserved section, and each row of the interlocking table specifies how that route is set and released. For the concrete route `1-3(2)`, the reserved section contains `1-3T`, `1-71AT`, `1-71BT`, `1-71CT`, `101BT`, `111T`, `62T`, and `112T`, requires points `101`, `111`, and `112` to be in the normal position, and cannot be set while any listed conflicting route is still set and unreleased. Route locking first checks that no conflicting route is already active, then locks the points in the required positions, verifies that the route track circuits are clear, and only then allows the entry signal to clear; for this route, if home signal `1-3` shows green then starter signal `15` also shows green. After a route is set and the entry signal is cleared, approach locking prevents normal cancellation when the approach track circuit becomes occupied. Route `1-3(2)` is released only after `1-3T`, `1-71AT`, `1-71BT`, `1-71CT`, and `101BT` are clear, `111T` has become occupied and then clear, and `62T` is occupied; flank protection additionally requires the non-route track circuit `61T` to stay unoccupied.

### 3. 逐句溯源

1. 句子 1：A route is the collection of track circuits along a reserved section, and each row of the interlocking table specifies how that route is set and released.
   对应摘录：A
2. 句子 2：For the concrete route `1-3(2)`, the reserved section contains `1-3T`, `1-71AT`, `1-71BT`, `1-71CT`, `101BT`, `111T`, `62T`, and `112T`, requires points `101`, `111`, and `112` to be in the normal position, and cannot be set while any listed conflicting route is still set and unreleased.
   对应摘录：A
3. 句子 3：Route locking first checks that no conflicting route is already active, then locks the points in the required positions, verifies that the route track circuits are clear, and only then allows the entry signal to clear; for this route, if home signal `1-3` shows green then starter signal `15` also shows green.
   对应摘录：A, B
4. 句子 4：After a route is set and the entry signal is cleared, approach locking prevents normal cancellation when the approach track circuit becomes occupied.
   对应摘录：B
5. 句子 5：Route `1-3(2)` is released only after `1-3T`, `1-71AT`, `1-71BT`, `1-71CT`, and `101BT` are clear, `111T` has become occupied and then clear, and `62T` is occupied; flank protection additionally requires the non-route track circuit `61T` to stay unoccupied.
   对应摘录：B

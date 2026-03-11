# Modelling Railway Interlocking Tables Using Coloured Petri Nets - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：route set/release、冲突进路和入口信号开放条件的文字依据很充分。

## 条目 1: Route locking and release rules from an interlocking table
- 控制对象：铁路联锁表中的 route locking / release logic

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 route locking logic，用于根据联锁表决定何时允许列车进入进路、何时禁止冲突进路以及如何释放进路。
- 判断：算。对象是实际联锁控制系统中的进路控制逻辑，原文清楚给出了 route、entry signal、conflict routes 和 set/release 规则。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Introduction，对 route / entry permission / conflict routes 的描述，行 176-189
> A collection of track circuits along the reserved section is called a “ route”. An
> entry signal shall be clear to let the train enter the route. Although the request
> to clear the entry signal is issued by the signal man, the route entry permission
> is decided by the interlocking system using safety rules and control methods
> speciﬁed in the agreed control tables. Ta bles 1 and 2 are the (partial) control
> tables for Panthong station, of which the signalling layout is shown in Fig. 1.Data in the ﬁrst column, “From”, is the route identiﬁcations which are labeled
> by the entry signal: 1-3(1); 1-3(2); 3-3(1); 3-3(2); 3-3(3); 2-4(1); 2-4(2); 4-4(1);
> 4-4(2); 4-4(3); 15(1); 15(2); 16(1); 16(2); 31(1);31(2); 32(1);32(2); 17 and 18. Dueto space limitation we show only 2 routes in Tables 1 and 2. Each row in the
> tables represents the requirement how to s et and release each route. For example,
> route 1-3(2) comprises the track circuits 1-3T, 1-71AT, 1-71BT,1-71CT,101BT,
> 111T, 62T, 112T and requires that the points 101, 111 and 112 are in normal
> position. Routes 1-3(1) and 1-3(2) specify that behind signal 1-3 two routes arepossible. Similar rule applies to routes 3-3; 2-4; and 4-4. The column “Requires
> Route Normal” shows conﬂict routes. A route cannot be set if any conﬂict routes
> have been set and not yet released. For route 1-3(2) the conﬂict routes are 1-3(1),16(1), 16(2), 32(1), 32(2), 3-3(1), 3-3(2), 2-4(1), 2-4(2), 4-4(1) and 4-4(2). The

#### 摘录 B
- 出处：第 5 页，Panthong station control table example，行 190-195
> exit (starter) signal of this route is 15, and if home signal 1-3 shows green, then
> starter signal 15 shows green.
>
> --- Page 6 ---
> 142 S. Vanit-Anunchai
> Table 1. A control table for Panthong station (part 1:Route locking)

### 2. 基于原文整理后的自然语言描述

A route is the collection of track circuits along the reserved section, and the entry signal is cleared only when route entry permission has been obtained. Each row of the interlocking table specifies how the route is set and released, including the required track circuits, point positions and conflicting routes. If any conflicting route has been set and not yet released, the route cannot be set.

### 3. 逐句溯源

1. 句子 1：A route is the collection of track circuits along the reserved section, and the entry signal is cleared only when route entry permission has been obtained.
   对应摘录：A
2. 句子 2：Each row of the interlocking table specifies how the route is set and released, including the required track circuits, point positions and conflicting routes.
   对应摘录：A, B
3. 句子 3：If any conflicting route has been set and not yet released, the route cannot be set.
   对应摘录：A

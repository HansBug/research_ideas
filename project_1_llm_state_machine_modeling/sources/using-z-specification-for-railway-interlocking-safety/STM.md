# USING Z SPECIFICATION FOR RAILWAY INTERLOCKING SAFETY - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Resource-flow（资源流/并发网模型）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：联锁系统的组件状态、关键不变式和 route rule 参数都可追溯；虽然运行生命周期主要以结构约束方式给出，但当前条目已达到主数据集核心保留线。

## 条目 1: Component-state view of an interlocking system
- 控制对象：铁路联锁系统的组件级状态描述
- 状态机类型：Resource-flow（资源流/并发网模型）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 component-state model of an interlocking system，用于通过轨道区段、道岔、信号、进路和子进路的状态组合及其不变式表示联锁安全状态。
- 判断：算，但属于组件级状态建模样本。对象是实际联锁系统，原文不仅定义了 interlocking state 的组成，还给出了 route rule 的结构参数与关键安全不变式。

### 1. 原文摘录

#### 摘录 A
- 出处：第 11 页，Section 4.2，对 state of an interlocking system 的定义，行 300-314
> Thestateofaninterlockingsystemisgenerallydeﬁnedbycombinationofparticular
> states of its components. These include mainly the following (physical) objects:
> Track circuits, dividing the track into sections and detecting their states (oc-
> cupied or clear),
> Points, steering trains across junctions and ﬁnding themselves in one of de-
> ﬁned positions (controlled plus, controlled minus or undeﬁned),
> Signals, allowing or refusing the entry of the railway vehicle onto particular
> sectionsofthetrackandsituatedinadvanceofthesectionwhichtheycontrol.
> Apart from the previous (physical) objects there are also so-called logical
> objects:
> Routesassectionsoftrackbetweentwosignals,whichproceedfromanentry
> signal to an exit signal (the route set or unset),
> Sub-routes as subsections of routes that are associated with speciﬁc track
> circuits. The concept of the route as a set of sub-routes is typical for several
> computer interlockings. The sub-route can be locked or free.

#### 摘录 B
- 出处：第 11-12 页，Section 4.2-4.3，对核心 invariant 的说明，行 315-325
> Theprocess ofdeﬁningthelocaldependencies (basedongeographic railway
> topology)mostoftenconcentratesonthefollowinginvariantconditions:
> For every track circuit, no more than one of the sub-routes passing over it
> should be locked for a route at any time,
> Ifasub-routeoveratracksectioncontainingpointsislockedforaroute,then
> the points are correctly aligned with that sub-route,
> If a route is set, then all of its sub-routes are locked,
> If a track circuit containing points is occupied, than the points are locked,
> Ifasub-routeislockedforaroute,thenallsub-routesaheadofitonthatroute
> are also locked.

#### 摘录 C
- 出处：第 12-13 页，Section 4.3，对 Z 中组件状态与 RouteRule 的表示，行 338-376
> points_position ::=cp|cm (16)
> points_state ::=cfp|cfm (17)
> tcircuit_state ::=c|o (18)
> route_state ::=s|us (19)
> sroute_state ::=f|l (20)
> To formalise the structure of a route setting rule, a number of entities must be
> concerned: theroutewhichistobeset( r),asetofconditions onpointswhichmust
> be satisﬁed before the route can be set ( p1), a set of point movements form part of
> the setting process for theroute ( p2),aset ofsub-routes whichmust befree before
> the route can be set ( d1), and a set of sub-routes which must be locked when the
> route is set ( d2).
> RouteRule
> d2: Subroute
> d1: Subroute
> p2: (Points × points_position)
> p1: (Points × points_state)
> r: Route

### 2. 基于原文整理后的自然语言描述

The state of the interlocking is modeled as a combination of component states that includes physical objects and logical routing objects: track circuits are `occupied` or `clear`, points are in controlled plus or controlled minus related states, routes are `set` or `unset`, and sub-routes are `locked` or `free`. The model is constrained by explicit invariants: at most one locked sub-route may pass over a track circuit at a time, a locked sub-route over points requires the points to be aligned correctly, a set route implies all of its sub-routes are locked, and occupied point-containing track circuits imply point locking. In the Z representation, these component states are typed as `tcircuit_state ::= c | o`, `route_state ::= s | us`, `sroute_state ::= f | l`, together with the corresponding point state/value types. A route-setting rule is then represented structurally by the route `r`, the required point-state conditions `p1`, the point movements `p2`, the sub-routes that must be free `d1`, and the sub-routes `d2` that must be locked when the route is set.

### 3. 逐句溯源

1. 句子 1：The state of the interlocking is modeled as a combination of component states that includes physical objects and logical routing objects: track circuits are `occupied` or `clear`, points are in controlled plus or controlled minus related states, routes are `set` or `unset`, and sub-routes are `locked` or `free`.
   对应摘录：A
2. 句子 2：The model is constrained by explicit invariants: at most one locked sub-route may pass over a track circuit at a time, a locked sub-route over points requires the points to be aligned correctly, a set route implies all of its sub-routes are locked, and occupied point-containing track circuits imply point locking.
   对应摘录：B
3. 句子 3：In the Z representation, these component states are typed as `tcircuit_state ::= c | o`, `route_state ::= s | us`, `sroute_state ::= f | l`, together with the corresponding point state/value types.
   对应摘录：C
4. 句子 4：A route-setting rule is then represented structurally by the route `r`, the required point-state conditions `p1`, the point movements `p2`, the sub-routes that must be free `d1`, and the sub-routes `d2` that must be locked when the route is set.
   对应摘录：C

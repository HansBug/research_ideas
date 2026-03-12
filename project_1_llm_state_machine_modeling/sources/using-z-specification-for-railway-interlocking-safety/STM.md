# USING Z SPECIFICATION FOR RAILWAY INTERLOCKING SAFETY - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：联锁系统状态由组件状态组合构成，route/sub-route 的 set/lock 逻辑可整理。

## 条目 1: Component-state view of an interlocking system
- 控制对象：铁路联锁系统的组件级状态描述

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 component-state model of an interlocking system，用于通过轨道区段、道岔、信号、进路和子进路的状态组合表示联锁系统状态。
- 判断：算，但属于组件级状态建模样本。对象是实际联锁系统，原文明确说明了 interlocking state 由各物理/逻辑对象状态组合而成。

### 1. 原文摘录

#### 摘录 A
- 出处：第 11 页，Section 4.2，对 state of an interlocking system 的定义，行 300-314
> Thestateofaninterlockingsystemisgenerallydeﬁnedbycombinationofparticular
> states of its components. These include mainly the following (physical) objects:
>  Track circuits, dividing the track into sections and detecting their states (oc-
> cupied or clear),
>  Points, steering trains across junctions and ﬁnding themselves in one of de-
> ﬁned positions (controlled plus, controlled minus or undeﬁned),
>  Signals, allowing or refusing the entry of the railway vehicle onto particular
> sectionsofthetrackandsituatedinadvanceofthesectionwhichtheycontrol.
> Apart from the previous (physical) objects there are also so-called logical
> objects:
>  Routesassectionsoftrackbetweentwosignals,whichproceedfromanentry
> signal to an exit signal (the route set or unset),
>  Sub-routes as subsections of routes that are associated with speciﬁc track
> circuits. The concept of the route as a set of sub-routes is typical for several
> computer interlockings. The sub-route can be locked or free.

### 2. 基于原文整理后的自然语言描述

The state of an interlocking system is defined by the combination of the states of its components. Track circuits are occupied or clear, points are in defined positions, routes are set or unset, and sub-routes are locked or free.

### 3. 逐句溯源

1. 句子 1：The state of an interlocking system is defined by the combination of the states of its components.
   对应摘录：A
2. 句子 2：Track circuits are occupied or clear, points are in defined positions, routes are set or unset, and sub-routes are locked or free.
   对应摘录：A

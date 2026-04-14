# Automatic generation and verification of railway interlocking control tables using FSM and NuSMV - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：Resource-flow（资源流/并发网模型）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：轨道区段、信号、道岔和 control-table row 的 route-setting 条件都写得较明确。

## 条目 1: Route-setting conditions in an interlocking control table
- 控制对象：铁路联锁控制表中的进路设定逻辑
- 状态机类型：Resource-flow（资源流/并发网模型）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G1 铁路联锁进路生命周期）

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 route-setting logic，用于在列车进路建立前检查轨道空闲、道岔位置与锁闭状态、信号颜色和冲突隔离条件。
- 判断：算。对象是实际联锁系统中的进路控制逻辑，原文给出了对象状态、进路建立前提和 control table 行的定义。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，Section 1，对 signaling objects states 与 minimum pre-settings 的说明，行 85-128
> Each of the objects in a railway can
> attain a certain number of states:
> - a track section can be either occupied or clear;
> - a three -aspect main signal can be red  (ON), yellow or green (OFF);
> - a point can be in reverse or normal position;
> ...
> In setting a route for a particular train movement ... the
> followings are the minimum pre -settings, required to be implemented and verified:
> - all tracks in the route and in the overlap should be clear
> - all points in the route and in the overlap should be set, clear, locked and checked
> - all conflicting signals and opposing signals should be ON (red)
> - all in -route signals should be OFF (clear)
> - the route should be isolated from all potential conflicting movements
> ...
> A route is defined by an entrance signal and exit signal. Each row of the table consists of the pre -
> settings require d by one particular route which can be defined in the station.

### 2. 基于原文整理后的自然语言描述

In this interlocking model, a track section is either `occupied` or `clear`, a point is in `normal` or `reverse` position, and a route is identified by its entrance and exit signals. To set a route for a train movement, all tracks in the route and overlap must be clear, all points must be set, clear, locked, and checked, all conflicting and opposing signals must remain red, the in-route signals must be clear, and the route must be isolated from conflicting movements. Each row of the interlocking control table records exactly these pre-settings for one particular route.

### 3. 逐句溯源

1. 句子 1：In this interlocking model, a track section is either `occupied` or `clear`, a point is in `normal` or `reverse` position, and a route is identified by its entrance and exit signals.
   对应摘录：A
2. 句子 2：To set a route for a train movement, all tracks in the route and overlap must be clear, all points must be set, clear, locked, and checked, all conflicting and opposing signals must remain red, the in-route signals must be clear, and the route must be isolated from conflicting movements.
   对应摘录：A
3. 句子 3：Each row of the interlocking control table records exactly these pre-settings for one particular route.
   对应摘录：A

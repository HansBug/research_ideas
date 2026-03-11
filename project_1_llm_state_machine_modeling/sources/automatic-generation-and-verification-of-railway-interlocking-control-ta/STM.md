# Automatic generation and verification of railway interlocking control tables using FSM and NuSMV - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：轨道区段、道岔、信号和进路的离散状态与进路设定条件写得很明确。

## 条目 1: Route-setting conditions in an interlocking control table
- 控制对象：铁路联锁控制表中的进路设定逻辑

### 0. 条目识别与判定

- 一句话说明：这是铁路联锁控制领域的 route-setting logic，用于在列车进路建立前检查轨道空闲、道岔位置与锁闭状态以及冲突进路隔离条件。
- 判断：算。对象是实际联锁系统中的进路控制逻辑，原文给出了对象状态、进路建立前提和控制表行的定义。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section 1，对 railway objects states 与 minimum pre-settings 的说明，行 85-103
> and axle counters), points, level crossing equipment and etc. Each of the objects in a railway can 
> attain a certain number of states:  
>  
> - a track section can be either occupied or clear;  
> - a three -aspect main signal can be red  (ON), yellow or green (OFF);  
> - a point can be in reverse or normal position;  
>  
> Figure 1 depicts a schematic view of signaling objects arrangement (signalling layout plan) in a 
> typical railway station. Each separated object in this figure is provided with a u nique identification 
> code. The layout plan of the stations is considered as the first stage of the interlocking design, based 
> on the operation requirements provided by the railway operator.  
> In setting a route for a particular train movement (i.e. a signal to become green or yellow) the 
> followings are the minimum pre -settings, required to be implemented and verified [5]:  
>  
> - all tracks in the route and in the overlap should be clear  
> - all points in the route and in the overlap should be set, clear, locked and che cked  
> - all conflicting signals and opposing signals should be ON (red)  
> - all in -route signals should be OFF (clear)  
> - the route should be isolated from all potential conflicting movements

#### 摘录 B
- 出处：第 3 页，Section 1，对 route row 的定义，行 126-128
> A route is defined by an entrance signal and exit signal. Each row of the table consists of the pre -
> settings require d by one particular route which can be defined in the station. The required settings for 
> a route between signals S1 and S9 in figure1, as one row of the interlocking control table, is shown in

### 2. 基于原文整理后的自然语言描述

In the interlocking, a track section is either occupied or clear, a point is in normal or reverse position, and a route is represented through its entrance and exit signals. Before a route can be set for a train movement, all tracks in the route and overlap must be clear, all points must be set, clear, locked and checked, in-route signals must be clear, and the route must be isolated from conflicting movements. Each row of the control table therefore records the required settings for one particular route.

### 3. 逐句溯源

1. 句子 1：In the interlocking, a track section is either occupied or clear, a point is in normal or reverse position, and a route is represented through its entrance and exit signals.
   对应摘录：A
2. 句子 2：Before a route can be set for a train movement, all tracks in the route and overlap must be clear, all points must be set, clear, locked and checked, in-route signals must be clear, and the route must be isolated from conflicting movements.
   对应摘录：A
3. 句子 3：Each row of the control table therefore records the required settings for one particular route.
   对应摘录：B

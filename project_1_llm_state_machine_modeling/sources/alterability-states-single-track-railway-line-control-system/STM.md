# Identifying Alterability States of a Single Track Railway Line Control System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文用 FSP/labeled-transition graph 明确写出单线铁路的 station、train、track 与 timetable 状态机，并用这些图分析可安全更新状态，适合作为 `🚆 + FSM + T0 + 资源互斥` 双 A 样本。

## 条目 1: Single-Track Railway Update-Safe Routing FSM

- 控制对象：轨道交通与铁路控制领域的单线铁路低流量线路 routing/update 状态机
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 FSP 图描述的单线铁路控制系统，用 station、train、track section 与 timetable 状态机保证单线资源互斥并识别控制系统更新可安全发生的状态。
- 判断：算。论文不是纯软件更新理论复述，而是把具体 railway line control system 写成可执行图模型，保留了状态、迁移、方向和资源互斥约束。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Section 1
> Figure 1 presents an example of single track line joining two stations. Station A has a shunting track and a deviation track while station B only has a deviation track.
>
> Considering two trains going respectively from station A to B and from station B to A, the deviation and shunting tracks are essential to safely handle traffic on the line.

#### 摘录 B

- 出处：第 6 页，Section 4.1
> All graphs are presented in the Finite State Process (FSP) notation and we use the LTSA tool for calculating graph composition and checking for deadlocks.
>
> The model of this case study needs to consider safety constraints. To avoid collision, two trains cannot travel in opposite directions on a same track.

#### 摘录 C

- 出处：第 6-7 页，Section 4.1
> Its initial state STATIONRAIL models the station having its shunting and deviation tracks free and having a train on the station main track.
>
> Through the transition deviation (respectively shunt), the station changes its state to having its main track free and its deviation (respectively shunting) track occupied.
>
> Transition leavedeviation (respectively leaveshunt) corresponds to a train leaving the deviation (respectively shunting) track and occupying the main track.

#### 摘录 D

- 出处：第 7 页，Figure 4 / Section 4.1
> TRAINatAtoB = (a.deviation -> TRAINatADEVIATIONtoB | a.leave -> TRAINatLINEtoB)
>
> TRAINatBtoA = (b.deviation -> TRAINatBDEVIATIONtoA | b.leave -> TRAINatLINEtoA)
>
> TRAINatAtoA = (a.deviation -> TRAINatADEVIATIONtoA | a.shunt -> TRAINatASHUNT | switchtoB -> TRAINatAtoB)

#### 摘录 E

- 出处：第 8-9 页，Section 4.2
> Analyzing the two versions of the control system graph, we can find updatable states according to the criteria of Panzica La Mana et al.
>
> States zero to six from the original graph are therefore updatable.
>
> Analyzing the two versions of the control system graph, we can find no weakly updatable states.

### 2. 基于原文整理后的自然语言描述

The single-track railway controller is modeled as a finite-state graph composition over station, train, track, and timetable components. The infrastructure case has Station A with both shunting and deviation tracks and Station B with only a deviation track, while two trains cyclically travel in opposite directions between the stations. At the station level, the controller moves from `STATIONRAIL` to states such as `STATIONDEVIATION` or `STATIONSHUNT` when a train takes the deviation or shunting track, and transitions such as `leavedeviation` or `leaveshunt` return the train to the main station track. At the train level, states such as `TRAINatAtoB`, `TRAINatLINEtoB`, `TRAINatBtoA`, and `TRAINatASHUNT` encode direction and position, with `switchtoA / switchtoB` changing the travel direction after station service. The track graph enforces the resource constraint that two trains cannot occupy or traverse the same single-track section in opposite directions at the same time. After the station-B deviation track is removed, the paper compares the old and updated control graphs and finds that states `0` to `6` are update-safe, while no weakly updatable states are found in the analyzed graph pair.

### 3. 逐句溯源

1. 句子 1：The single-track railway controller is modeled as a finite-state graph composition over station, train, track, and timetable components.
   对应摘录：B
2. 句子 2：The infrastructure case has Station A with both shunting and deviation tracks and Station B with only a deviation track, while two trains cyclically travel in opposite directions between the stations.
   对应摘录：A
3. 句子 3：At the station level, the controller moves from `STATIONRAIL` to states such as `STATIONDEVIATION` or `STATIONSHUNT` when a train takes the deviation or shunting track, and transitions such as `leavedeviation` or `leaveshunt` return the train to the main station track.
   对应摘录：C
4. 句子 4：At the train level, states such as `TRAINatAtoB`, `TRAINatLINEtoB`, `TRAINatBtoA`, and `TRAINatASHUNT` encode direction and position, with `switchtoA / switchtoB` changing the travel direction after station service.
   对应摘录：D
5. 句子 5：The track graph enforces the resource constraint that two trains cannot occupy or traverse the same single-track section in opposite directions at the same time.
   对应摘录：B
6. 句子 6：After the station-B deviation track is removed, the paper compares the old and updated control graphs and finds that states `0` to `6` are update-safe, while no weakly updatable states are found in the analyzed graph pair.
   对应摘录：E

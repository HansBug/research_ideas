# Onboard Decision-Making for Nominal and Contingency sUAS Flight - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `DMS PLAN / DMS EXECUTE` 外层监督器、飞行状态集合、A2G regain time window 和 `alternate land / land now` 分支都写成了明确的任务监督链。

## 条目 1: Plan-execute contingency flight-state supervisor

- 控制对象：UTM 城市场景下小型无人机的机载任务决策与应急处置监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是航空航天与飞行/空管控制领域的 onboard decision-maker，用于在 nominal、off-nominal、alternate land 和 land now 等飞行状态之间切换，并驱动重规划与应急相位切换。
- 判断：算。对象是实际 BVLOS 城市飞行任务的机载监督控制器，不是纯方法框架；原文明确给出了外层 `plan / execute` 主状态、内层飞行状态集合、健康/路径可行性输入和带 time window 的 contingency 处理链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-4 页，`Contribution / Decision-making flight states`，`paper_content.txt` 第 68-75 行、第 124-140 行
> Contingency management proposed in the ConOps is comprised of protocols that outline the procedures in the event of certain contingencies such as communication loss. For this point design, we implement a finite state machine (FSM) ... The transitions are changes in vehicle health, path feasibility, and clearance due to geofencing.
>
> FS NOMINAL flight is the initial accepted flight plan with full capabilities. FS OFFNOMINAL XXX flight has the same landing site as FS NOMINAL ... FS ALTERNATE LAND ... Finally, during FS LAND NOW, the vehicle immediately lands at its current location as safely as it can.

#### 摘录 B

- 出处：第 6 页，`Decision-Making State Machine`，`paper_content.txt` 第 176-184 行
> In order to separate planning and executing, two main states were created, DMS PLAN and DMS EXECUTE ... The decision-maker begins in the DMS PLAN state by calling for a trajectory ... After accepting a trajectory, it then transitions into the DMS EXECUTE state where it stays unless the flight state changes and a new trajectory must consequentially be planned.

#### 摘录 C

- 出处：第 7 页，`Decision-Making Inputs and Outputs`，`paper_content.txt` 第 196-214 行
> The monitored health metrics shown in Tab. 3 ... Navigation Health ... A2G Communication Health ... V2X Communication Health ... Path Feasibility contingencies are handled by the Local Planner ... Contingencies occur when no paths are found ... the decision-maker must determine whether a detour trajectory can be generated ... or if the safest route is to abort the mission and go to an alternate landing site or land now.

#### 摘录 D

- 出处：第 11-12 页，`A2G Communication Failure / V2X Communication Failure`，`paper_content.txt` 第 269-277 行、第 287-304 行
> This contingency has the aforementioned FS OFFNOMINAL A2G COM REGAIN mode where the vehicle flies its nominal trajectory while trying to regain A2G communication within a specified time window ... the UAS remains in a 10 second regain period before flying to an alternate landing site and declaring ALERFA.
>
> In the event of V2X communication loss, the vehicle must either fly to an alternate landing site or land now if the alternate landing site is too far ... the vehicle is already farther than the allowable distance (200m) ... the Flight State changes to 3 for FS LAND NOW ... if it is still within 200m ... changes the Flight State to FS ALTERNATE LAND.

### 2. 基于原文整理后的自然语言描述

The decision-maker is organized as an outer `DMS PLAN / DMS EXECUTE` supervisor whose inner cases are the flight states `FS NOMINAL`, `FS OFFNOMINAL NAV LOSS`, `FS OFFNOMINAL A2G COM REGAIN`, `FS ALTERNATE LAND`, and `FS LAND NOW`. It starts in `DMS PLAN`, requests a trajectory for the current flight state, accepts that trajectory, and then stays in `DMS EXECUTE` while monitoring health metrics, path feasibility, and dynamic-clearance changes that may force a new plan. When A2G communication fails, the machine enters `FS OFFNOMINAL A2G COM REGAIN`, keeps flying the nominal trajectory during a bounded regain window, and then escalates to `FS ALTERNATE LAND` with `ALERFA` if communication is not recovered in time. When V2X communication fails, the controller immediately raises the emergency phase to `DETRESFA` and chooses between `FS ALTERNATE LAND` and `FS LAND NOW` according to the 200 m distance rule and whether the alternate-land trajectory itself remains feasible.

### 3. 逐句溯源

1. 句子 1：The decision-maker is organized as an outer `DMS PLAN / DMS EXECUTE` supervisor whose inner cases are the flight states `FS NOMINAL`, `FS OFFNOMINAL NAV LOSS`, `FS OFFNOMINAL A2G COM REGAIN`, `FS ALTERNATE LAND`, and `FS LAND NOW`.
   对应摘录：A, B
2. 句子 2：It starts in `DMS PLAN`, requests a trajectory for the current flight state, accepts that trajectory, and then stays in `DMS EXECUTE` while monitoring health metrics, path feasibility, and dynamic-clearance changes that may force a new plan.
   对应摘录：B, C
3. 句子 3：When A2G communication fails, the machine enters `FS OFFNOMINAL A2G COM REGAIN`, keeps flying the nominal trajectory during a bounded regain window, and then escalates to `FS ALTERNATE LAND` with `ALERFA` if communication is not recovered in time.
   对应摘录：D
4. 句子 4：When V2X communication fails, the controller immediately raises the emergency phase to `DETRESFA` and chooses between `FS ALTERNATE LAND` and `FS LAND NOW` according to the 200 m distance rule and whether the alternate-land trajectory itself remains feasible.
   对应摘录：D

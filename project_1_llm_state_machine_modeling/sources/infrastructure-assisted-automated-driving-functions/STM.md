# Development and Verification of Infrastructure-Assisted Automated Driving Functions - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把基础设施辅助的 lane-offset / lane-change ADAS 写成基于 zone 与 target-lane 变量的 rule-based trajectory planner，并把连续轨迹跟踪接口交代清楚。

## 条目 1: Zone-aware lane-offset and lane-change trajectory planner

- 控制对象：汽车与道路车辆控制领域的基础设施辅助自动驾驶轨迹规划控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个部署在 SAE L3 级 automated mode 上的 rule-based trajectory planner，用 IVIM 消息中的 detection zone、relevance zone、lane-off-set 与 desired lane 信息驱动车辆执行偏移、避让和回到默认车道的机动。
- 判断：算。对象是实际 automated driving function，而不是单纯通信框架；原文明确写出两类 use case、zone-based 触发条件、target lane occupancy guard、Bézier 换道轨迹以及与横纵向控制器的接口。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，Use Cases，`paper_content.txt` 第 166-183、188-196 行
> In the in-lane off-set recommendation scenario ... the ego vehicle shall drive in automated mode ... in a detection zone when it receives an IVIM containing a recommended lane-off-set information ... Before entering the relevance zone ... the ego vehicle adapts the typical LKA task of tracking the center of the existing lane and transitions to driving along the same lane with the given in-lane off-set. ... Immediately after leaving the relevance zone, the ego vehicle is expected to follow the default centerline tracking task unless otherwise recommended.
>
> In the lane change recommendation scenario ... the ego vehicle shall drive in automated mode ... in a detection zone when it receives an IVIM containing a set of three relevance zones with instructions to avoid the rightmost lane ... When the ego vehicle is driving on the rightmost lane in relevance zone 1, it will change the lane to next lane if trafﬁc allows it ... In relevance zone 3, the rightmost lane is cleared and the ego vehicle uses the most appropriate lane according to the trafﬁc situation.

#### 摘录 B

- 出处：第 6-8 页，`IVIM emulation / Rule-Based Trajectory Planner`，`paper_content.txt` 第 279-290、302-317、326-338 行
> For both use case scenarios a simple emulation subsystem was developed. Its aim is to check if the ego vehicle is inside the detection or relevance zones and to provide the trajectory planner with the necessary information ... the developed emulation block checks and interprets whether the ego vehicle is inside one of these areas and consequently speciﬁes the desired lane to the trajectory planner.
>
> The planning task is accomplished by a rule-based trajectory planner (TP) ... It uses a ﬁnite state machine and a set of discrete decisions to trigger lane changes or keep the vehicle on its current lane. By default, the ego vehicle drives in the middle of the rightmost lane. If a slower vehicle prevents the ego vehicle from reaching its desired cruising speed, and the target lane is not occupied, a Bézier curve is planned to perform a lane change.
>
> The Bézier curves provide a smooth transition to initiate and ﬁnish the lane change, while the straight segment can be shortened or extended during the lane change maneuver according to the width of the target lane.

#### 摘录 C

- 出处：第 8-10 页，Simulation results，`paper_content.txt` 第 401-418、451-460 行
> Both controllers execute with a sample time of 20 ms.
>
> According to the simulated scenario, at approximately 2.5 s the ego vehicle starts the transition to the desired in-lane off-set. In this example the vehicle reaches its desired steady-state off-set value of 0.2 m at approximately 7 s ... about 4.5 s ...
>
> According to this example scenario, the ego vehicle enters the relevance zone 1 (RZ1) at about 6.6 s and the desired lane, therefore, switches from 0 to 1 ... the TP initiates immediately a lane change maneuver to lane 1, where it stays while passing the relevance zones 1 and 2 (RZ1 and RZ2). In relevance zone 3 (RZ3) the TP computes a lane change maneuver back to the original starting lane (i.e., lane 0). ... the total lane change maneuver was achieved with less than 5 s transition times between steady state driving positions.

### 2. 基于原文整理后的自然语言描述

The infrastructure-assisted driving function is an EFSM-like trajectory planner that combines C-ITS recommendation variables with highway-lane geometry and surrounding-traffic conditions. In the lane-offset use case, the ego vehicle first receives an IVIM recommendation inside a `detection zone`, then leaves ordinary lane-center tracking and enters an offset-following mode before the `relevance zone`, keeps the prescribed lateral offset while traversing that zone, and finally returns to default centerline tracking after the zone ends. In the lane-avoidance use case, the planner interprets one detection zone plus three relevance zones and changes the desired lane accordingly: if the vehicle is in the rightmost lane inside `RZ1` and traffic allows it, it moves to the next lane, stays away from the rightmost lane through `RZ1` and `RZ2`, and computes a return maneuver in `RZ3`. The rule-based planner couples this discrete zone logic to continuous motion control by generating lane-change references through two Bézier curves plus one linear segment, and the resulting commands are tracked by lateral and longitudinal controllers executing with a `20 ms` sample time. The reported simulations keep the logic operationally concrete, because the vehicle reaches a `0.2 m` in-lane offset in about `4.5 s` and completes each recommended lane change in under `5 s`.

### 3. 逐句溯源

1. 句子 1：The infrastructure-assisted driving function is an EFSM-like trajectory planner that combines C-ITS recommendation variables with highway-lane geometry and surrounding-traffic conditions.
   对应摘录：A, B
2. 句子 2：In the lane-offset use case, the ego vehicle first receives an IVIM recommendation inside a `detection zone`, then leaves ordinary lane-center tracking and enters an offset-following mode before the `relevance zone`, keeps the prescribed lateral offset while traversing that zone, and finally returns to default centerline tracking after the zone ends.
   对应摘录：A
3. 句子 3：In the lane-avoidance use case, the planner interprets one detection zone plus three relevance zones and changes the desired lane accordingly: if the vehicle is in the rightmost lane inside `RZ1` and traffic allows it, it moves to the next lane, stays away from the rightmost lane through `RZ1` and `RZ2`, and computes a return maneuver in `RZ3`.
   对应摘录：A, C
4. 句子 4：The rule-based planner couples this discrete zone logic to continuous motion control by generating lane-change references through two Bézier curves plus one linear segment, and the resulting commands are tracked by lateral and longitudinal controllers executing with a `20 ms` sample time.
   对应摘录：B, C
5. 句子 5：The reported simulations keep the logic operationally concrete, because the vehicle reaches a `0.2 m` in-lane offset in about `4.5 s` and completes each recommended lane change in under `5 s`.
   对应摘录：C

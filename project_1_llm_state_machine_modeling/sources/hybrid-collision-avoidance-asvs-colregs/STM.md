# Hybrid Collision Avoidance for ASVs Compliant With COLREGs Rules 8 and 13-17 - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自主水面船舶的 COLREGs 解释器写成了一个显式状态机，状态集合、进入/退出条件、`dCPA / tCPA / tcrit` 阈值和场景输出都足够具体，可直接形成双 A 的规则型监督控制样本。

## 条目 1: COLREGs obstacle-rule classifier for autonomous surface vessels

- 控制对象：通用控制与无人船任务领域的自主水面船舶中层碰撞规避规则分类器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 ASV 混合碰撞规避系统里的 COLREGs 规则解释器，用状态机把每个障碍船分类为 `SF / OT / HO / GW / SO / EM`，并将分类结果喂给中层 MPC 规避器。
- 判断：算。对象是实际自主船舶控制体系中的规则分类控制器，原文给出了完整状态集合、进入退出准则、由 `dCPA / tCPA / tcrit` 形成的 guard，以及仿真场景中的状态输出和对应规避动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-7 页，`4.2.1. State Machine`，行 503-527
> We propose to utilize a state machine in order to decide which COLREGs rule is active with respect to each obstacle in the vicinity of the ownship. The state machine contains the states: SF Safe state ... OT Overtaking state ... HO Head-on state ... GW Give-way state ... SO Stand-on state ... EM Emergency state. This implies that the obstacle is so close and/or behaves unpredictably, such that special considerations must be made.

#### 摘录 B

- 出处：第 7 页，`4.2.2. Entry and Exit Criteria`，行 545-607
> CPA describes the time to the point where the two vessels are the closest, and the distance to the obstacle at this point ... Given tCPA, we calculate the distance between the vessels at CPA as dCPA ... the time to the critical point tcrit can be calculated ... The state-machine entry criteria ... true if dCPA < di,enter_CPA and tCPA within thresholds ... entryEM ... true if tcrit < tEM,enter_crit and tCPA > 0.

#### 摘录 C

- 出处：第 7 页，`4.2.2. Entry and Exit Criteria`，行 612-639
> The state-machine exit criteria ... true if dCPA >= di,exit_CPA or tCPA outside thresholds ... exitEM ... true if tcrit >= tEM,exit_crit or tCPA <= 0 ... the exit criterias are obtained by negating the entry criterias, but with other thresholds in order to implement hysteresis to avoid shattering.

#### 摘录 D

- 出处：第 16 页，`Scenario 1`，行 1267-1291
> The first obstacle is in a stand-on situation ... the first obstacle is quickly considered as a stand-on situation, at which the mid-level algorithm disregards the obstacle and continues with the current speed and course ... we encounter two crossing vessels where the ownship is deemed the give-way vessel. In accordance with the COLREGs, we maneuver to starboard ... After avoiding the two give-way obstacles ... we encounter a head-on situation. This is correctly identified by the state machine as head on, and we maneuver to starboard in order to avoid collision.

### 2. 基于原文整理后的自然语言描述

The paper implements the COLREGs interpreter as an explicit state machine that classifies each nearby obstacle vessel into `SF`, `OT`, `HO`, `GW`, `SO`, or `EM`, and each state directly corresponds to a different regulatory situation for the ownship. Transitions are not based on vague narrative judgments: the machine uses geometric context together with the time to closest point of approach `tCPA`, the corresponding distance `dCPA`, and the time to a critical distance boundary `tcrit` as entry guards. The same variables also define state exits, and the exit thresholds are intentionally separated from the entry thresholds to introduce hysteresis and prevent shattering. Scenario results then validate that the state machine is operational rather than decorative: it first identifies a stand-on obstacle, then two give-way crossings that trigger starboard maneuvers, and later a head-on encounter that remains classified as head-on until the ownship has safely passed.

### 3. 逐句溯源

1. 句子 1：The paper implements the COLREGs interpreter as an explicit state machine that classifies each nearby obstacle vessel into `SF`, `OT`, `HO`, `GW`, `SO`, or `EM`, and each state directly corresponds to a different regulatory situation for the ownship.
   对应摘录：A
2. 句子 2：Transitions are not based on vague narrative judgments: the machine uses geometric context together with the time to closest point of approach `tCPA`, the corresponding distance `dCPA`, and the time to a critical distance boundary `tcrit` as entry guards.
   对应摘录：B
3. 句子 3：The same variables also define state exits, and the exit thresholds are intentionally separated from the entry thresholds to introduce hysteresis and prevent shattering.
   对应摘录：C
4. 句子 4：Scenario results then validate that the state machine is operational rather than decorative: it first identifies a stand-on obstacle, then two give-way crossings that trigger starboard maneuvers, and later a head-on encounter that remains classified as head-on until the ownship has safely passed.
   对应摘录：D

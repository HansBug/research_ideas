# An Overtaking Decision Algorithm for Networked Intelligent Vehicles based on Cooperative Perception - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把网络化智能车的超车决策直接定义成 `Free driving / Car following / Overtaking / Abort overtaking` 四态 FSM，并把风险阈值、连续步数判据和回退链都写进了正文。

## 条目 1: Cooperative-Perception Follow-Overtake-Abort FSM

- 控制对象：网络化智能车自车的超车决策与回退控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是汽车与道路车辆控制领域的超车行为决策器，用 cooperative perception 提供前车/来车估计，再由四态 FSM 决定自由行驶、跟车、超车或中止回退。
- 判断：算。对象是实际自动驾驶车辆的离散行为控制器，原文不仅画出了 FSM，还给出了状态语义、风险阈值、连续步数 guard，以及 abort 后回到 `free driving` 或 `car following` 的恢复规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 5-18 行
> This paper presents an overtaking decision algorithm for networked intelligent vehicles. The algorithm is based on a cooperative tracking and sensor fusion algorithm ... The ego vehicle is equipped with lane keeping and lane changing capabilities ... Based on the estimated distances to the leading and the oncoming vehicles and their speeds, a risk is calculated and a corresponding overtaking decision is made.

#### 摘录 B

- 出处：第 3 页，`IV. Overtaking Decision Algorithm / A. State description`，`paper_content.txt` 第 252-315 行
> Free driving / Car following / Overtaking / Abort overtaking ... Fig. 2. A FSM defining the behavior of the ego car.
>
> 1) Free driving: the car E drives freely on the road at target speed v0 while keeping centered in its lane.
>
> 2) Car following: The car E follows the car L ... maintaining a desired distance and time headway.
>
> 3) Overtaking: the car E has determined that it is safe to overtake the car L ... It changes lane and performs overtaking at its desired speed v0.
>
> 4) Abort overtaking: the risk that the car O occupies the overtaking lane has become significant, thus the car E aborts the overtaking maneuver.

#### 摘录 C

- 出处：第 3-4 页，`IV.B. Decision algorithm (FSM state transitions)`，`paper_content.txt` 第 315-338 行
> The initial FSM state is free driving. Once the car L is detected, the state is changed to car following.
>
> ... If the risk is lower or equal to the defined threshold Tstart for at least five consecutive simulation steps, the overtaking is initiated.
>
> ... If the risk exceeds the Tabort thresholds for at least two consecutive simulation steps, the state is changed to abort overtaking. Otherwise, if the overtaking is successfully finished ... the state is changed back to free driving.
>
> In the abort overtaking state ... If the car E is ahead of the car L, it accelerates and changes lane back to its driving lane ... The state is then changed back to free driving. Otherwise, it brakes and pulls behind the car L, and the state is consequently changed to car following.

### 2. 基于原文整理后的自然语言描述

The overtaking controller combines cooperative perception with a four-state FSM whose states are `Free driving`, `Car following`, `Overtaking`, and `Abort overtaking`. The machine starts in free driving and switches to car following once a slower leading vehicle is detected, while the overtaking decision itself is driven by a continuously computed risk value derived from the estimated positions and speeds of the ego, leading, and oncoming vehicles. If that risk stays at or below `Tstart` for `five consecutive simulation steps`, the controller initiates the pass; if the risk rises above `Tabort` for `two consecutive simulation steps` during the maneuver, it transitions into the abort state. In the abort branch, the controller either accelerates and returns to its lane ahead of the leading car or brakes and merges back behind it, then settles into `Free driving` or `Car following` according to the relative positions of the two vehicles.

### 3. 逐句溯源

1. 句子 1：The overtaking controller combines cooperative perception with a four-state FSM whose states are `Free driving`, `Car following`, `Overtaking`, and `Abort overtaking`.
   对应摘录：A, B
2. 句子 2：The machine starts in free driving and switches to car following once a slower leading vehicle is detected, while the overtaking decision itself is driven by a continuously computed risk value derived from the estimated positions and speeds of the ego, leading, and oncoming vehicles.
   对应摘录：A, C
3. 句子 3：If that risk stays at or below `Tstart` for `five consecutive simulation steps`, the controller initiates the pass; if the risk rises above `Tabort` for `two consecutive simulation steps` during the maneuver, it transitions into the abort state.
   对应摘录：C
4. 句子 4：In the abort branch, the controller either accelerates and returns to its lane ahead of the leading car or brakes and merges back behind it, then settles into `Free driving` or `Car following` according to the relative positions of the two vehicles.
   对应摘录：C

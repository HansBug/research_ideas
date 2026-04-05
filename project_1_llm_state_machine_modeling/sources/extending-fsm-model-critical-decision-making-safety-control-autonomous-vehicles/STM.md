# Extending the FSM Model for Critical Decision-Making and Safety Control in Autonomous Vehicles - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把场景级 meta-state 与行人避让子状态机拼成 HFSM，并把四个决策模式、距离阈值和目标加速度规则写得足够具体，可作为 `🚗` 方向的双 A 条目。

## 条目 1: Hierarchical Pedestrian-Avoidance HFSM with Four Decision Modes

- 控制对象：汽车与道路车辆控制领域的自动驾驶高层行为决策控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向自动驾驶车辆的分层行为决策控制器，上层用 meta-state 组织场景类别，下层用四态有限状态机处理行人避让时的速度决策。
- 判断：算。对象是真实自动驾驶决策模块，原文不仅强调 `HFSM` 层次结构，还明确写出 `Maintain pace / Slow down / Strong brake / Speed up` 四种模式及其基于 `QE / e / ecmf / emax / wdes` 的切换条件与输出加速度公式。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Introduction / Fig 1.1`，`paper_content.txt` 第 48-57、95-103 行
> hierarchical finite state machines are an effective approach and are often utilized to aid in vehicle decision-making.
>
> Split vehicle behavior into distinct components and create a decision-making system with a constrained state methodology.
>
> Here, we divide the behaviors of cars in any sub-scene into four distinct groups: lane shifting to the left, lane shifting to the right, accelerating ahead, and slowing down ahead.

#### 摘录 B

- 出处：第 5-6 页，`Hierarchical FSM / Meta-states`，`paper_content.txt` 第 264-297、399-408 行
> Hierarchical finite states machines (HFSM), also referred as statecharts, were designed to comfort the tedious transition waste necessary in big FSMs ...
>
> A meta-state machine builds up this hierarchical FSM ... the meta-states or "states made of states" correlate to universal scenarios and each one of them incorporates a fully effective state-machine for that unique setting.
>
> Additional meta-states might be established to satisfy evolving requirements if a single meta-state is found to be insufficient to cope with the whole class of instances it was dedicated to.

#### 摘录 C

- 出处：第 6-7 页，`The foundation procedure estimates the desired acceleration separately for each scenario`，`paper_content.txt` 第 409-427 行
> The ego vehicle's existing situation and if a pedestrian is recognized dictate when a paradigm changeover happens. All four modes' specifics are as follows:
>
> Maintain pace: In this setting, the ego car attempts to stick to the set speed wdes despite the fact it identifies no pedestrians on the road.
>
> When pedestrians are observed on the path, the Boolean variable QE is initialized to 1. The ego vehicle preserves its current velocity in the Uphold pace mode if QE is equivalent to 0 or the time benefit uadv surpasses the specified max. If not, the FSM decides on which setting should be triggered next.

#### 摘录 D

- 出处：第 7 页，`Slow down / Strong brake / Speed up`，`paper_content.txt` 第 434-463 行
> Slow down: If the duration benefits remain too tiny for the ego vehicle to move straight away, the FSM initiates the slow-down mode.
>
> Strong brake: The self-important vehicle should decelerate quicker than bcmf whenever the separation between it and the pedestrian fulfills emax < e < ecmf.
>
> Speed up: The FSM passes through this phase when the condition e < emax is fulfilled ... there doesn't seem adequate room for the ego automobile to decelerate and stay away from the pedestrian. In this instance, it makes greater sense to speed up and overtake swiftly.

### 2. 基于原文整理后的自然语言描述

The autonomous-driving decision module is organized as a hierarchical finite-state machine in which upper-level meta-states classify broad driving scenarios and delegate the concrete response logic to lower-level sub-state machines. Inside the pedestrian-avoidance branch, the local decision FSM contains four explicit modes, namely `Maintain pace`, `Slow down`, `Strong brake`, and `Speed up`, and the controller switches among them according to whether a pedestrian has been detected and how much distance or time advantage remains. The maintain-pace branch keeps the ego vehicle near the desired lane speed `wdes`, but once `QE` indicates pedestrian presence and the available time benefit is no longer sufficient, the controller leaves that nominal mode and evaluates the braking or overtaking branches. If the remaining gap still allows a comfortable yield, the system enters `Slow down`; if the gap falls into the harder braking window `emax < e < ecmf`, it enters `Strong brake`; and if the gap drops below `emax`, the controller abandons braking and commands the `Speed up` mode to pass the conflict area quickly. This makes the paper a usable `HSM + T0` sample because the hierarchy, the local state set, the switch guards, and the output acceleration policy are all stated explicitly rather than hidden inside a black-box planner.

### 3. 逐句溯源

1. 句子 1：The autonomous-driving decision module is organized as a hierarchical finite-state machine in which upper-level meta-states classify broad driving scenarios and delegate the concrete response logic to lower-level sub-state machines.
   对应摘录：A, B
2. 句子 2：Inside the pedestrian-avoidance branch, the local decision FSM contains four explicit modes, namely `Maintain pace`, `Slow down`, `Strong brake`, and `Speed up`, and the controller switches among them according to whether a pedestrian has been detected and how much distance or time advantage remains.
   对应摘录：C, D
3. 句子 3：The maintain-pace branch keeps the ego vehicle near the desired lane speed `wdes`, but once `QE` indicates pedestrian presence and the available time benefit is no longer sufficient, the controller leaves that nominal mode and evaluates the braking or overtaking branches.
   对应摘录：C
4. 句子 4：If the remaining gap still allows a comfortable yield, the system enters `Slow down`; if the gap falls into the harder braking window `emax < e < ecmf`, it enters `Strong brake`; and if the gap drops below `emax`, the controller abandons braking and commands the `Speed up` mode to pass the conflict area quickly.
   对应摘录：D
5. 句子 5：This makes the paper a usable `HSM + T0` sample because the hierarchy, the local state set, the switch guards, and the output acceleration policy are all stated explicitly rather than hidden inside a black-box planner.
   对应摘录：A, B, C, D

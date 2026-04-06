# Enhancing power quality in electrical distribution systems using a smart charging architecture - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 Smart Charger 的 `7` 态 FSM、事件/guard/action 语义以及不同电网状态下的充电功率更新规则写得很完整，可直接作为 `🌡️` 方向双 A 样本。

## 条目 1: Seven-state smart-charging supervisor from the traffic-light PQ model

- 控制对象：过程与环境控制领域的电动汽车 Smart Charger 充电功率监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是配电网约束下的 EV 智能充电监督器，用 `PQ-Indic`、用户目标 `SoC` 与插枪状态共同驱动 `7` 个离散状态之间的切换，并在每次切换时计算新的充电功率。
- 判断：算。对象是实际充电架构里的功率控制器，原文给出了完整状态集合、事件/guard/action 语义、起始与终止条件，以及各目标状态对应的充电功率更新公式。

### 1. 原文摘录

#### 摘录 A

- 出处：第 11-12 页，`Finite state machine`
> The FSM consists of seven states that are grouped to three different types:
>
> Operational states: low-red, low-yellow, green, high-yellow, and high-red state ...
>
> Standby state: The gray state models the charging state after the desired State of Charge (SoC) is reached.
>
> End state ... With maximum SoC or unplugged EV it is not longer possible to control the charging operation.

#### 摘录 B

- 出处：第 12 页，事件、guard 与起始状态说明
> The transitions in the FSM are labeled by two parts: Event and Guard. ... we have three kinds of events that can trigger the state transition: Input of a new PQ-Indic value, unplugging of the vehicle and changing of the SoC of the battery.
>
> each state transition can have an action which specifies the output of the SmartCharger. In our case, the action defines the new charging power ...
>
> The low-red state is considered as the start state ...

#### 摘录 C

- 出处：第 13-14 页，目标状态驱动的动作定义
> * -> low-red state ... the SmartCharger needs to reduce the charging power ... the decrease of the charging power is greater than 70% of the currently used charging power.
>
> * -> (low and high)-yellow states ... the change in the charging power capacity is calculated by a linear function ...
>
> * -> green state ... a linear increase or decrease of the currently used charging power is applied until the charging profile plus the safety margin is reached.
>
> * -> high-red state ... the SmartCharger must increase the charging power. Hence, a polynomial function is defined for transition to this state.
>
> * -> gray state ... only responds to highly critical grid situations by increasing the charging rate. Otherwise, the charging power is reduced continuously until it reaches Cmin again.

### 2. 基于原文整理后的自然语言描述

The Smart Charger is modeled as a seven-state EFSM whose operational core consists of `low-red`, `low-yellow`, `green`, `high-yellow`, and `high-red`, plus a `standby` state after the target charge level is reached and an `end` state for unplugged or fully charged vehicles. Its transitions are explicitly event/guard/action driven: new `PQ-Indic` values, unplugging, and `SoC` changes trigger state changes, guards decide whether the transition is allowed, and each successful transition outputs a newly computed charging power. The controller starts conservatively in `low-red`, leaves active charging for `end` when `SoC = 100` or the vehicle is unplugged, and moves into `standby` when the user-requested target `SoC` is reached. The action semantics are state-specific rather than generic: transitions into `low-red` apply a strong polynomial decrease, yellow states use linear adjustments around the user charging profile, `green` steers power toward the profile plus safety margin, `high-red` polynomially increases power, and `standby` only raises charging in highly critical grid situations while otherwise decaying toward `Cmin`. That means the controller preserves not only discrete mode names but also a clear mapping from grid-status color, battery condition, and user objective to output power adaptation, which is enough to support a detailed T0 supervision sample.

### 3. 逐句溯源

1. 句子 1：The Smart Charger is modeled as a seven-state EFSM whose operational core consists of `low-red`, `low-yellow`, `green`, `high-yellow`, and `high-red`, plus a `standby` state after the target charge level is reached and an `end` state for unplugged or fully charged vehicles.
   对应摘录：A
2. 句子 2：Its transitions are explicitly event/guard/action driven: new `PQ-Indic` values, unplugging, and `SoC` changes trigger state changes, guards decide whether the transition is allowed, and each successful transition outputs a newly computed charging power.
   对应摘录：B
3. 句子 3：The controller starts conservatively in `low-red`, leaves active charging for `end` when `SoC = 100` or the vehicle is unplugged, and moves into `standby` when the user-requested target `SoC` is reached.
   对应摘录：A, B
4. 句子 4：The action semantics are state-specific rather than generic: transitions into `low-red` apply a strong polynomial decrease, yellow states use linear adjustments around the user charging profile, `green` steers power toward the profile plus safety margin, `high-red` polynomially increases power, and `standby` only raises charging in highly critical grid situations while otherwise decaying toward `Cmin`.
   对应摘录：C
5. 句子 5：That means the controller preserves not only discrete mode names but also a clear mapping from grid-status color, battery condition, and user objective to output power adaptation, which is enough to support a detailed T0 supervision sample.
   对应摘录：A, B, C

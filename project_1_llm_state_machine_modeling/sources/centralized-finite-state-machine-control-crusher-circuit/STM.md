# Centralized Finite State Machine Control to Increase the Production Rate in a Crusher Circuit - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了破碎回路监督器的状态集合、阈值 guard、CSS 与 AF1 调整动作以及等待回稳状态，足以整理为高质量过程控制样本。

## 条目 1: CSS-and-feeder supervisory FSM for a crusher circuit
- 控制对象：铁矿石破碎回路的集中式 CSS/给料机监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是矿山过程控制场景下的 crusher-circuit supervisor，用于根据破碎机功率、料仓液位和输送带容量在 CSS 与给料机速度之间进行离散切换。
- 判断：算。对象是实际破碎回路控制系统，原文明确给出了状态集、功率/料位 guard、执行动作和动作后的等待状态。

### 1. 原文摘录

#### 摘录 A
- 出处：第 8 页，`The FSM Used in Case of Unsafe Conditions`
> The FSM used in case of the unsafe operation of the crushing circuit equipment ... works similarly to a watchdog ...
>
> the condition to reach state 1 occurs if the crusher power reaches a value greater than 120 kWh. Then, the CSS is set to 38 mm ...
>
> state 3 is reached when silos BS1 and BS2 exceed their acceptable levels. In this case, the speed of AF1 is set to 34% and new material feeding is disabled.
>
> the proposed control strategy allows the return to regular operation ... only after the defined time and the crusher power is less than 100 kWh and/or when the BS1 and BS2 levels decrease to safe values.

#### 摘录 B
- 出处：第 8-9 页，`The FSM Used in the Case of Regular Conditions`
> The FSM for regular crushing circuit operation is designed to keep the CSS at 35 mm as long as possible.
>
> if the BS2 level is less than 70%, the “decrease CSS” state is reached (state 2.2). This state always decrements the CSS by 3 mm. Thus, allowable CSS values for the crusher are 35, 38, and 41 mm.
>
> if the BS2 level increases above 70%, the speed of feeder AF1 is reduced by 10% (state 2.5).
>
> The conditions to increase CSS (state 2.4) occur when the BS2 level is increasing and higher than 80%, CB2 and CB3 conveyor belts have capacity lower than 90%, and the BS1 level is lower than 80%.

#### 摘录 C
- 出处：第 8-9 页，`regular operation / state 2.3`
> depending on the level of BS1 and capacity of conveyor belts CB2 and CB3, it is possible to increase the speed of feeder AF1 by 10% (State 2.6) ...
>
> Always after an action, the control system reaches state 2.3 operating for a while to wait for the effects of the actions taken.

### 2. 基于原文整理后的自然语言描述

The crusher-circuit supervisor is a Mealy-style finite-state controller that manipulates cone-crusher CSS and apron-feeder speed from crusher power, silo levels, and conveyor capacities instead of holding the circuit at one fixed operating point. In the unsafe-condition watchdog FSM, `state 1` is entered when crusher power exceeds 120 kWh and immediately sets CSS to 38 mm, while `state 3` is entered when silos `BS1` and `BS2` exceed their acceptable levels, forcing `AF1` to 34% and disabling new feed until power or levels return to safe values after the defined wait time. In regular operation the supervisor tries to keep CSS at 35 mm, but it enters `state 2.2` to decrease CSS by 3 mm when `BS2 < 70%`, `state 2.5` to reduce `AF1` by 10% when `BS2 > 70%`, and `state 2.4` to increase CSS when `BS2 > 80%`, both downstream conveyors stay below 90% capacity, and `BS1 < 80%`. When `BS1` and conveyor capacities permit more throughput, `state 2.6` increases `AF1` by 10% to push more material through the circuit. After every action, the controller enters `state 2.3` to wait for the plant response before deciding the next transition, so the overall FSM alternates between threshold-triggered actions and an explicit settling state.

### 3. 逐句溯源

1. 句子 1：The crusher-circuit supervisor is a Mealy-style finite-state controller that manipulates cone-crusher CSS and apron-feeder speed from crusher power, silo levels, and conveyor capacities instead of holding the circuit at one fixed operating point.
   对应摘录：A, B
2. 句子 2：In the unsafe-condition watchdog FSM, `state 1` is entered when crusher power exceeds 120 kWh and immediately sets CSS to 38 mm, while `state 3` is entered when silos `BS1` and `BS2` exceed their acceptable levels, forcing `AF1` to 34% and disabling new feed until power or levels return to safe values after the defined wait time.
   对应摘录：A
3. 句子 3：In regular operation the supervisor tries to keep CSS at 35 mm, but it enters `state 2.2` to decrease CSS by 3 mm when `BS2 < 70%`, `state 2.5` to reduce `AF1` by 10% when `BS2 > 70%`, and `state 2.4` to increase CSS when `BS2 > 80%`, both downstream conveyors stay below 90% capacity, and `BS1 < 80%`.
   对应摘录：B
4. 句子 4：When `BS1` and conveyor capacities permit more throughput, `state 2.6` increases `AF1` by 10% to push more material through the circuit.
   对应摘录：C
5. 句子 5：After every action, the controller enters `state 2.3` to wait for the plant response before deciding the next transition, so the overall FSM alternates between threshold-triggered actions and an explicit settling state.
   对应摘录：C

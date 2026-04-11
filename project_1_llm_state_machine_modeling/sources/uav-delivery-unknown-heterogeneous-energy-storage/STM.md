# Ready, Bid, Go! On-Demand Delivery Using Fleets of Drones with Unknown, Heterogeneous Energy Storage Constraints - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 UAV delivery controller 明确写成 `Wait / Bid? / Won? / Deliver / Return` 五态 machine，并把 SoC、task ID、parcel mass、delivery distance 和 abort threshold 写成转移 guard，足以形成 `EFSM + T0` 双 A 样本。

## 条目 1: Wait-bid-won-deliver-return UAV delivery controller

- 控制对象：航空航天与飞行/空管控制领域的按需配送 UAV 任务竞价与返航控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向按需配送机队的单 UAV controller，它根据任务公告、投标结果、配送成功/中止结果以及剩余电量阈值，在 `Wait / Bid? / Won? / Deliver / Return` 五个阶段之间切换。
- 判断：算。对象是实际 UAV delivery control logic，而不是抽象学习框架；原文直接声明 UAV logic is governed by a finite-state machine，并逐状态解释输入、输出与 abort condition。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Figure 2 caption，`paper_content.txt` 第 236-240 行
> Figure 2: Overview of decentralised learning-based deployment strategy and evaluation environment: (a) A UAV’s logic is governed by a finite-state machine; (b) the UAV uses a bidding policy to determine whether to bid (and an associated level of confidence) and a bids evaluation policy to determine whether its bid won; (c) upon returning from a delivery attempt, the UAV updates its bidding policy ...

#### 摘录 B

- 出处：第 3 页，`3.1 UAV Controller`，`paper_content.txt` 第 244-268 行
> A UAV begins in the Wait state, where it awaits an announcement of the next delivery task along with the task ID.
>
> When a task announcement is received, the UAV transitions to the Bid? state. In this state, it uses its bidding policy to determine whether to bid, and a bid value, reflecting its level of confidence in the bid. If the UAV opts to bid, it proceeds to the Won? state; otherwise, it returns to the Wait state.
>
> In the Won? state, the UAV broadcasts a tuple comprising (i) the task ID, (ii) its unique ID, and (iii) the bid value ... If it won, the UAV records its current state of charge, hereafter denoted as SoC takeoff, and transitions to the Deliver state. Otherwise, it returns to the Wait state.
>
> When in the Deliver state, the UAV retrieves the parcel ... and flies to the delivery destination. It either (i) reaches the destination and the delivery is successful, or (ii) meets an abort condition ... In either case, the UAV transitions to the Return state. The abort condition is set such that the UAV returns to the FC if SoC(t) ≤ ξ SoC takeoff, that is, when only a fraction ξ of its takeoff state of charge remains.

#### 摘录 C

- 出处：第 1 页，Abstract，`paper_content.txt` 第 28-43 行
> We propose a decentralised deployment strategy that combines auction-based task allocation with online learning. Each UAV independently decides whether to bid for orders based on its energy storage charge level, the parcel mass, and delivery distance. Over time, it refines its policy to bid only for orders within its capability. ... highlighting the advantages of decentralised energy-aware decision-making ...

### 2. 基于原文整理后的自然语言描述

The retained control object is a single-UAV delivery controller whose logic is explicitly implemented as a five-stage state machine with the states `Wait`, `Bid?`, `Won?`, `Deliver`, and `Return`. Its transitions are guarded by extended task and energy variables rather than by a fixed schedule: a new order announcement carries `task ID`, `parcel mass`, and `delivery distance`; the UAV then decides whether to bid, computes a bid value, and moves to `Won?` only if its learned bidding policy judges the task feasible. If the auction is won, the controller stores `SoC_takeoff` and enters `Deliver`; otherwise it falls back to `Wait` and waits for another task. Delivery is not a terminal sink state, because the UAV either completes the mission successfully or aborts when the remaining charge drops below the threshold `SoC(t) ≤ ξ * SoC_takeoff`, after which it transitions into `Return` and flies back to the fulfilment centre. The resulting controller is a clean energy-aware UAV EFSM in which mission allocation, execution, and safety-driven return are integrated into a single control loop.

### 3. 逐句溯源

1. 句子 1：The retained control object is a single-UAV delivery controller whose logic is explicitly implemented as a five-stage state machine with the states `Wait`, `Bid?`, `Won?`, `Deliver`, and `Return`.
   对应摘录：A, B
2. 句子 2：Its transitions are guarded by extended task and energy variables rather than by a fixed schedule: a new order announcement carries `task ID`, `parcel mass`, and `delivery distance`; the UAV then decides whether to bid, computes a bid value, and moves to `Won?` only if its learned bidding policy judges the task feasible.
   对应摘录：B, C
3. 句子 3：If the auction is won, the controller stores `SoC_takeoff` and enters `Deliver`; otherwise it falls back to `Wait` and waits for another task.
   对应摘录：B
4. 句子 4：Delivery is not a terminal sink state, because the UAV either completes the mission successfully or aborts when the remaining charge drops below the threshold `SoC(t) ≤ ξ * SoC_takeoff`, after which it transitions into `Return` and flies back to the fulfilment centre.
   对应摘录：B
5. 句子 5：The resulting controller is a clean energy-aware UAV EFSM in which mission allocation, execution, and safety-driven return are integrated into a single control loop.
   对应摘录：A, B, C

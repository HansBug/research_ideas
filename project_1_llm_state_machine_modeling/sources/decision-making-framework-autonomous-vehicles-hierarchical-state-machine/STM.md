# Decision making framework for autonomous vehicles driving behavior in complex scenarios via hierarchical state machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动驾驶直线路段行为决策拆成 `scenario / energy-efficiency / action` 三层状态机，并给出形式化五元组、场景划分和候选行为集合，足以支撑双 A 的 HSM 样本。

## 条目 1: Three-Layer Scenario-to-Behavior Driving HSM

- 控制对象：复杂直线路段场景下自动驾驶车辆的三级行为决策控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是汽车与道路车辆领域的自动驾驶高层行为决策机，用三级层次结构在“场景判断 -> 候选行为评估 -> 具体动作规划”之间逐层收敛。
- 判断：算。对象是实际自动驾驶车辆的决策控制器，原文明确给出三层 FSM 任务网络、有限状态机五元组、顶层场景分类以及中层候选行为集合。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> In this paper, a decision making framework based on hierarchical state machine is proposed with a top-down structure of three-layer finite state machine decision system. The upper layer classifies the driving scenario based on relative position of the vehicle and its surrounding vehicles. The middle layer judges the optimal driving behavior according to the improved energy efficiency function targeted at multiple criteria including driving efficiency, safety and the grid-based lane vacancy rate. The lower layer constructs the state transition matrix combined with the calculation results of the previous layer to predict the optimal pass way in the region.

#### 摘录 B

- 出处：第 3-4 页，Section 2.2 `FSM mission planning model`
> The FSM model is established for autonomous vehicles in straight lanes and the decisions of the state machine are divided into three layers. Such a decision framework is expressed through collaboration between the three layers, and depending on the actual traffic situation and vehicle state, a decision is made as to which specific vehicle action to perform next, and all tasks are completed only when the decisions at each tier are completed.
>
> The three task layers can be specifically represented as a scenario decision, an energy efficiency assessment decision and an execution action decision layer.

#### 摘录 C

- 出处：第 4 页，Section 2.2-2.3
> The quintet is defined as follows to build a finite state machine decision model at each task level:
>
> M(S, Σ, f, S0, F).
>
> Here, S means the set of states ... Σ means the set of input events or all situations ... f means a mapping from S×Σ to Σ ... S0 is the initial state and F is the final state.
>
> According to the distribution of vehicles around the perception of the self-driving vehicle, all scenarios are divided into three categories: no vehicle in front, no vehicle on the side, and vehicle on the side, and subdivided into sub-scenarios again on this basis.

#### 摘录 D

- 出处：第 5 页，Section 2.4
> The driving state of the vehicle can be divided into 3 kinds: the free driving state with the desired speed as the target, the lane change driving state under different acceleration, and the following driving state.
>
> ... the vehicle behavior with the highest energy efficiency value is selected by conditional judgement.

### 2. 基于原文整理后的自然语言描述

The proposed autonomous-driving decision framework is a three-layer hierarchical state machine for straight-lane traffic scenarios. Its top layer classifies the surrounding scene according to whether there is a vehicle in front and whether there are vehicles on the sides, and its middle layer evaluates candidate behaviors with an energy-efficiency function that combines safety, efficiency, and lane vacancy information. The lower layer then materializes that choice as a concrete action decision by constructing the state transition matrix for the next maneuver. The paper formalizes each task layer with the FSM quintuple `M(S, Σ, f, S0, F)`, so the controller is not just an informal mode diagram but an explicit state-event-transition model. At the behavior layer, the controller explicitly reasons over `free driving`, `lane change driving`, and `following driving`, selecting whichever behavior satisfies the current scene and optimization conditions.

### 3. 逐句溯源

1. 句子 1：The proposed autonomous-driving decision framework is a three-layer hierarchical state machine for straight-lane traffic scenarios.
   对应摘录：A, B
2. 句子 2：Its top layer classifies the surrounding scene according to whether there is a vehicle in front and whether there are vehicles on the sides, and its middle layer evaluates candidate behaviors with an energy-efficiency function that combines safety, efficiency, and lane vacancy information.
   对应摘录：A, C, D
3. 句子 3：The lower layer then materializes that choice as a concrete action decision by constructing the state transition matrix for the next maneuver.
   对应摘录：A, B
4. 句子 4：The paper formalizes each task layer with the FSM quintuple `M(S, Σ, f, S0, F)`, so the controller is not just an informal mode diagram but an explicit state-event-transition model.
   对应摘录：C
5. 句子 5：At the behavior layer, the controller explicitly reasons over `free driving`, `lane change driving`, and `following driving`, selecting whichever behavior satisfies the current scene and optimization conditions.
   对应摘录：D

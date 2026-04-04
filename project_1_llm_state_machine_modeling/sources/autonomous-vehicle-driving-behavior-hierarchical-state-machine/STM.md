# Decision Making Framework for Autonomous Vehicles Driving Behavior in Complex Scenarios via Hierarchical State Machine - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不只是泛泛提出框架，而是把直道自动驾驶决策写成三层有限状态机，明确给出 `30` 个子场景、`4` 类候选动作节点，以及下层 `state transition table / matrix` 的推导方式，足以形成双 A 的道路车辆高层决策样本。

## 条目 1: Three-Layer Straight-Lane Driving Supervisor
- 控制对象：汽车与道路车辆领域的直道自动驾驶行为决策控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个用于复杂直道路况的自动驾驶行为决策器，把场景识别、行为评价和具体执行动作拆成三层有限状态机，并进一步用动作转移表/矩阵预测下一步行为。
- 判断：算。对象是实际自动驾驶车辆的高层行为决策模块，原文不仅给出了层次结构、状态集合与状态转移函数，还写出了 `30` 个子场景、`4` 类候选动作节点及其矩阵化状态转移规则。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 9-20 行
> In this paper, a decision making framework based on hierarchical state machine is proposed with a top-down structure of three-layer finite state machine decision system. The upper layer classifies the driving scenario based on relative position of the vehicle and its surrounding vehicles. The middle layer judges the optimal driving behavior according to the improved energy efficiency function targeted at multiple criteria including driving efficiency, safety and the grid-based lane vacancy rate. The lower layer constructs the state transition matrix combined with the calculation results of the previous layer to predict the optimal pass way in the region.

#### 摘录 B
- 出处：第 3-4 页，`2.2 FSM mission planning model / 2.3 Top layer scenario decision`，`paper_content.txt` 第 207-279 行
> The FSM model is established for autonomous vehicles in straight lanes and the decisions of the state machine are divided into three layers. Such a decision framework is expressed through collaboration between the three layers, and depending on the actual traffic situation and vehicle state, a decision is made as to which specific vehicle action to perform next, and all tasks are completed only when the decisions at each tier are completed.
>
> The three task layers can be specifically represented as a scenario decision, an energy efficiency assessment decision and an execution action decision layer.
>
> According to the distribution of vehicles around the perception of the self-driving vehicle, all scenarios are divided into three categories: no vehicle in front, no vehicle on the side, and vehicle on the side, and subdivided into sub-scenarios again on this basis.

#### 摘录 C
- 出处：第 4-5 页，`finite state machine decision model / 2.4 Middle layer energy efficiency assessment`，`paper_content.txt` 第 247-259 行、第 289-315 行
> Here, `S` means the set of states ... `Σ` means the set of input events or all situations ... `f` means a mapping from `S×Σ` to `Σ`, in a certain state, the FSM will switch to a new state determined by the state transition function after a given input.
>
> The driving state of the vehicle can be divided into 3 kinds: the free driving state with the desired speed as the target, the lane change driving state under different acceleration, and the following driving state.
>
> Three driving states are required to meet the vehicle driving stability conditions and the lane change, and the following driving state are required to meet the collision safety restriction conditions.

#### 摘录 D
- 出处：第 7-8 页，`2.5 Lower layer action decision / Table 1`，`paper_content.txt` 第 513-560 行
> The following FSM state transfer table can be created ... The table defines the rules for vehicle behavior transfer ... a scenario is randomly selected to build a behavior transition table that contains three stages after the initial moment, each with four potential behavior nodes, as shown in Table 1.
>
> The specific behavior implementation is in the order of vehicle acceleration, right lane change, left lane change and deceleration.
>
> For example, if the highest energy efficiency value for the next phase is `R2` ... the vehicle behavior performed is a right lane change.
>
> ... assume that the current scenario under the best risk assessment conforms to the `R3` ... So, the next task is ... `C2`. We can see from the above that the next task is transferred to `C2` ... The specific planning task is to change the lane left at the next moment.

### 2. 基于原文整理后的自然语言描述

The autonomous-driving decision module for straight-lane scenarios is organized as a three-layer hierarchical state machine, and a driving task is considered complete only after all three layers finish their decisions collaboratively. At the top layer, the controller classifies the current situation from the surrounding-vehicle distribution into `no vehicle in front`, `no vehicle on the side`, or `vehicle on the side`, and the paper further refines these into `30` sub-scenarios as the top-layer substates. At the middle layer, the controller evaluates candidate behaviors with an energy-efficiency function that combines safety, driving efficiency, and grid-based lane vacancy, and it works with three driving-state categories: free driving toward the desired speed, lane changing under different accelerations, and following. At the lower execution layer, the paper explicitly builds a behavior transition table with three future stages and four potential behavior nodes per stage, where the concrete action order is `acceleration`, `right lane change`, `left lane change`, and `deceleration`. The next action is then selected by combining the current node with the best evaluated risk/energy result; for example, the paper shows that when the current node is `C1` and the next-phase evaluation matches `R3`, the state transfers to `C2`, meaning a left lane change at the next moment.

### 3. 逐句溯源

1. 句子 1：The autonomous-driving decision module for straight-lane scenarios is organized as a three-layer hierarchical state machine, and a driving task is considered complete only after all three layers finish their decisions collaboratively.
   对应摘录：A, B
2. 句子 2：At the top layer, the controller classifies the current situation from the surrounding-vehicle distribution into `no vehicle in front`, `no vehicle on the side`, or `vehicle on the side`, and then refines these into sub-scenarios for later decision making.
   对应摘录：A, B
3. 句子 3：At the middle layer, the controller evaluates candidate behaviors with an energy-efficiency function that combines safety, driving efficiency, and grid-based lane vacancy, and it works with three driving-state categories: free driving toward the desired speed, lane changing under different accelerations, and following.
   对应摘录：A, C
4. 句子 4：At the lower execution layer, the paper explicitly builds a behavior transition table with three future stages and four potential behavior nodes per stage, where the concrete action order is `acceleration`, `right lane change`, `left lane change`, and `deceleration`.
   对应摘录：D
5. 句子 5：The next action is then selected by combining the current node with the best evaluated risk/energy result; for example, the paper shows that when the current node is `C1` and the next-phase evaluation matches `R3`, the state transfers to `C2`, meaning a left lane change at the next moment.
   对应摘录：D

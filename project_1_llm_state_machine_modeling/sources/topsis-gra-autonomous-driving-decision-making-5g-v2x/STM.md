# Modeling and TOPSIS-GRA Algorithm for Autonomous Driving Decision-Making Under 5G-V2X Infrastructure - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文在 5G-V2X 基础设施下构造了 `global FSM + local FSM` 两层 HFSM，并把宏观场景态、局部驾驶态和状态转移排序算法写成了完整的决策骨架。

## 条目 1: Global-and-Local HFSM for 5G-V2X Driving Decisions

- 控制对象：5G-V2X 智能网联车的分层驾驶行为决策系统
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是汽车与道路车辆领域的 cerebrum-like 决策 supervisor，用全局 FSM 先判断道路场景，再用局部 FSM 细化成具体驾驶行为与候选目标点。
- 判断：算。对象是实际 ICV 自主驾驶决策模块，原文明确给出两层 HFSM、全局 `7` 态 `17` 事件、局部 `16` 态 `8` 事件，以及状态转移排序算法与反馈链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> it builds a hierarchical finite state machine (HFSM) model as well as a TOPSIS-GRA algorithm for making ICV autonomous driving decisions ...
>
> The HFSM model is composed of two layers: the global FSM model and the local FSM model. The decision of the former acts as partial input information of the latter and the result of the latter is sent forward to the local path-planning module, meanwhile pulsating feedback to the former as real-time refresh data.
>
> the global FSM model is designed as 7 driving behavior states and 17 driving characteristic events, and the local FSM model is designed as 16 states and 8 characteristic events.

#### 摘录 B

- 出处：第 5 页，Section 2.1 `Global FSM Model`
> Based on different traffic scenarios under 5G-V2X intelligent road infrastructure, the global FSM is defined as a triple array F=(S, E, Tr). Where S={S1,...,Sm} is the state set of FSM and Si ... indicates the state of start, on road, approaching an intersection, intersection, field driving, U-Turn, and stop, respectively.

#### 摘录 C

- 出处：第 7-8 页，Section 2.2 `Local FSM Model`
> this paper designs a local FSM’s state set by considering different traffic scenarios. Concretely, the set has 16 driving states, i.e., {start, lane following, acceleration, deceleration, vehicle following, overtaking vehicles, turn left to avoid obstacles, turn right to avoid obstacles, change to left lane without deceleration, change to right lane without deceleration, change to left lane with deceleration, change to right lane with deceleration, U-Turn, stop at an intersection, stop at roadside, stop at parking lots}.
>
> the local FSM model adds a candidate goal points set ... F=(S,E,Tr,V).

#### 摘录 D

- 出处：第 10 页，Section 3 `TOPSIS-GRA Algorithm for State Transition`
> the steps to design a state transition algorithm in the HFSM model are summarized as follows. First, the algorithm begins with constructing a state set and an event set for ICV self-driving to get the decision-making matrix ... then, it further fuses TOPSIS method and GRA method ... to realize states ranking.

### 2. 基于原文整理后的自然语言描述

The proposed 5G-V2X autonomous-driving controller is a two-layer hierarchical finite state machine in which a `global FSM` first recognizes the macro traffic scenario and a `local FSM` then selects the concrete driving behavior for the current situation. At the global layer, the paper defines seven scene states, including `start`, `on road`, `approaching an intersection`, `intersection`, `field driving`, `U-Turn`, and `stop`, and uses seventeen characteristic events to drive transitions among them. The local layer refines that decision into sixteen operational driving states such as `lane following`, `acceleration`, `deceleration`, `vehicle following`, `overtaking vehicles`, obstacle-avoidance turns, several lane-change variants, and three stop-related states. The local machine also carries a candidate goal-point set `V`, so state selection is directly coupled to downstream path planning rather than being a disconnected labeler. State transitions are ranked by a TOPSIS-GRA fusion algorithm, which means the controller explicitly orders candidate next states from the decision matrix instead of selecting them ad hoc.

### 3. 逐句溯源

1. 句子 1：The proposed 5G-V2X autonomous-driving controller is a two-layer hierarchical finite state machine in which a `global FSM` first recognizes the macro traffic scenario and a `local FSM` then selects the concrete driving behavior for the current situation.
   对应摘录：A
2. 句子 2：At the global layer, the paper defines seven scene states, including `start`, `on road`, `approaching an intersection`, `intersection`, `field driving`, `U-Turn`, and `stop`, and uses seventeen characteristic events to drive transitions among them.
   对应摘录：A, B
3. 句子 3：The local layer refines that decision into sixteen operational driving states such as `lane following`, `acceleration`, `deceleration`, `vehicle following`, `overtaking vehicles`, obstacle-avoidance turns, several lane-change variants, and three stop-related states.
   对应摘录：A, C
4. 句子 4：The local machine also carries a candidate goal-point set `V`, so state selection is directly coupled to downstream path planning rather than being a disconnected labeler.
   对应摘录：A, C
5. 句子 5：State transitions are ranked by a TOPSIS-GRA fusion algorithm, which means the controller explicitly orders candidate next states from the decision matrix instead of selecting them ad hoc.
   对应摘录：D

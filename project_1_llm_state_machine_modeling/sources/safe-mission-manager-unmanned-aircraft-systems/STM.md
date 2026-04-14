# Architectural Design of a Safe Mission Manager for Unmanned Aircraft Systems - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 RPAS 的安全监视、风险缓解与 contingency policy 写成了显式状态自动机与条件决策链，soft / hard contingency、`S1-S7` 状态和 procedure 列表都很完整，可直接形成 mission-level 正例。

## 条目 1: Soft/hard contingency safe mission manager

- 控制对象：航空航天与飞行/空管控制领域的 soft/hard contingency 安全任务监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 RPAS contingency management 的 safe mission manager，用 Safety Monitor 诊断风险状态，再由 Contingency Plan 依据任务约束选择 `loiter / climb / avoidance / manual / landing / termination` 等缓解动作。
- 判断：算。对象是实际航空任务管理控制器中的 contingency supervisor，不是纯风险评估流程；原文明确给出了 nominal / mitigation / termination 状态自动机、`soft` 与 `hard` 事件、`S1-S7` 状态语义以及 procedure 选择逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Abstract，`paper_content.txt` 第 49-55 行
> The resulting architecture makes a conceptual differentiation between event monitoring, decision-making on a policy for dealing with contingencies and the execution of the corresponding policy.
>
> ... we model and verify the correctness of a contingency management policy using formal methods.

#### 摘录 B

- 出处：第 18-19 页，`5.1 Detecting contingency states`，`paper_content.txt` 第 583-605 行
> The state automaton ... starts at a nominal state where no contingency events have occurred.
>
> ... when the first safety boundary is exceeded, it triggers a "soft" contingency event. Such events make the system shift into a contingency state where a given mitigation action can be planned.
>
> When the second boundary is exceeded, the Safety Monitor will raise a "hard" contingency event, which results in a state where the only feasible action is flight termination ...
>
> if the mitigation action turns out to be effective, a recovery event will bring the system back to the nominal state ...

#### 摘录 C

- 出处：第 32-34 页，`7.1.1 Decision logic / 7.2 Specification of the Contingency Plan model`，`paper_content.txt` 第 1049-1118 行
> The resulting decision logic is modeled in Fig. 10. It shows an FSM with seven states: the nominal state (S1), the flight termination state (S7), and five risk mitigation states (S2 to S6) ...
>
> Autonomous operation (S2) describes C2 link loss conditions; Degraded navigation (S3) implies reduced navigation capability due to GPS loss of performance ...
>
> The list contains four contingency procedures of a tactical nature, including: loitering, climbing to regain the signal, avoidance maneuver, and reverting to manual control; and two strategical contingency options: landing at a designated landing site, and flight termination.

#### 摘录 D

- 出处：第 35 页，`7.2.1 Decision logic`，`paper_content.txt` 第 1154-1165 行
> After the C2 link loss event, the system is in the Autonomous operation state. In this state, the goal is to minimize the time of flight "not under command" ...
>
> this can be achieved by either landing at a designated landing site, climbing to regain the signal, or performing the flight termination action.

### 2. 基于原文整理后的自然语言描述

The Safe Mission Manager is organized as a two-step contingency supervisor: a Safety Monitor first diagnoses whether the aircraft is in nominal operation, a recoverable mitigation state, or a flight-termination state, and then the Contingency Plan selects an admissible mitigation procedure for that state. In the generic safety-monitor automaton, exceeding the first safety boundary raises a `soft` contingency event and moves the system into a risk-mitigation state, while exceeding the second boundary raises a `hard` contingency event and makes flight termination the only feasible action. The concrete case study refines this into seven states: `S1` nominal operation, `S2` autonomous operation for C2 link loss, `S3` degraded navigation, `S4` degraded control, `S5` traffic alert, `S6` boundary alert, and `S7` flight termination. Once one of the mitigation states is entered, the Contingency Plan chooses among tactical procedures such as `loitering`, `climbing to regain the signal`, `avoidance maneuver`, and `reverting to manual control`, or strategical procedures such as `landing at a designated landing site` and `flight termination`, depending on the mission plan and contextual state variables. This makes the retained control object an EFSM-style mission supervisor rather than a plain FSM, because the state evolution is coupled with policy-selection variables and feasibility checks on the available contingency procedures.

### 3. 逐句溯源

1. 句子 1：The Safe Mission Manager is organized as a two-step contingency supervisor: a Safety Monitor first diagnoses whether the aircraft is in nominal operation, a recoverable mitigation state, or a flight-termination state, and then the Contingency Plan selects an admissible mitigation procedure for that state.
   对应摘录：A, B, C
2. 句子 2：In the generic safety-monitor automaton, exceeding the first safety boundary raises a `soft` contingency event and moves the system into a risk-mitigation state, while exceeding the second boundary raises a `hard` contingency event and makes flight termination the only feasible action.
   对应摘录：B
3. 句子 3：The concrete case study refines this into seven states: `S1` nominal operation, `S2` autonomous operation for C2 link loss, `S3` degraded navigation, `S4` degraded control, `S5` traffic alert, `S6` boundary alert, and `S7` flight termination.
   对应摘录：C
4. 句子 4：Once one of the mitigation states is entered, the Contingency Plan chooses among tactical procedures such as `loitering`, `climbing to regain the signal`, `avoidance maneuver`, and `reverting to manual control`, or strategical procedures such as `landing at a designated landing site` and `flight termination`, depending on the mission plan and contextual state variables.
   对应摘录：C, D
5. 句子 5：This makes the retained control object an EFSM-style mission supervisor rather than a plain FSM, because the state evolution is coupled with policy-selection variables and feasibility checks on the available contingency procedures.
   对应摘录：A, C, D

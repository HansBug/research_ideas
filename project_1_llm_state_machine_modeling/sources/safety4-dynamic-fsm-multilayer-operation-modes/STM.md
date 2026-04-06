# Towards safety4.0: A novel approach for flexible human-robot-interaction based on safety-related dynamic finite-state machine with multilayer operation modes - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多层人机协作 operation mode、安全功能 guard 以及机床上下料 use case 串成了一套动态安全有限状态机，控制对象清楚、状态和转移条件也足够具体。

## 条目 1: Multilayer HRI operation-mode safety FSM

- 控制对象：工业自动化与离散制造领域的人机协作机床上下料单元安全 operation-mode 监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是面向 human-robot collaboration 单元的安全监督器，把 `SRMS / SSM / HandGuiding / PFL / AutoMode / Stop` 等协作模式组织成多层状态图，并用安全功能束作为状态转移 guard。
- 判断：算。对象是实际 HRC 产线里的安全控制状态机，原文明确给出了状态集合、转移记号、由安全功能构成的 guard，以及机床上下料 use case 中各模式如何对应具体任务阶段。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-7 页，`3.2 Multilayer collaborative operation modes`
> every collaborative operation mode will represent one machine state to build a safety-related finite state machine properly. These collaborative states are; S3-SRMS, S4-SSM, S5-HG: GC, S6-PFL, S7-PFL: HO, S8-PP, and S9-HG: FC. ... two states represent the stop categories “S1 (Stop1) and S2 (Stop 2)”, and one state represents the automatic mode “S10 (AutoMode)”.

#### 摘录 B

- 出处：第 7-8 页，`3.4 Safety-related finite-state machine for collaborative applications`
> A transition Tn_m presents the transition from the start state Sn to the end state Sm. Every transition Tn_m consists of a couple of conditions representing the relation between safety functions and the machine state to switch from the start state to the end state.
>
> T3_1 -> (DFE ∧ SS1 ∧ SBC ∧ STO)
>
> T1_3 -> (DFE ∧ MAR)

#### 摘录 C

- 出处：第 8 页，Level 1 第二个 cluster 的状态图
> S10 (AutoMode) represents the automation mode which can be the start mode.
>
> T10_4 -> ((CFE1 ∨ CFE2 ... CFEX) ∧ SLS ∧ SSM ∧ SSR ∧ SDI)
>
> T4_1 -> (DFE) ∨ (SLS ∨ SSM ∨ SSR ∨ SDI) ∧ SS1 ∧ SBC ∧ STO
>
> T1_10 -> (DFE ∧ OPR)

#### 摘录 D

- 出处：第 9-10 页，机床上下料 use case
> the robot can work under SRMS operation mode while picking the item from storage, transporting it to the CNC, and waiting for the machining process. When the quality process starts, the robot can switch to the HandGuiding operation mode. During the final process, the robot can work under SSM while transporting the item to the maintenance station or under SRMS when the robot should transport the item to the storage back if the item's quality is fine.

### 2. 基于原文整理后的自然语言描述

The proposed HRI safety controller is organized as a multilayer state machine in which each collaborative operation mode becomes a machine state, including `S3-SRMS`, `S4-SSM`, `S5-HG:GC`, `S6-PFL`, `S7-PFL:HO`, `S8-PP`, `S9-HG:FC`, plus stop states `S1/S2` and the higher-level `S10 AutoMode`. Transitions are not narrative-only but formal guard bundles: the move from `SRMS` to `Stop1` requires `DFE ∧ SS1 ∧ SBC ∧ STO`, while recovery from `Stop1` back to `SRMS` requires the danger field to be clear and a manual restart through `MAR`. In a richer cluster, `AutoMode` can enter `SSM` only when one of the collaborative-field entries is active together with safe-motion functions such as `SLS`, `SSM`, `SSR`, and `SDI`, and it can fall back to `Stop1` when danger-field or motion-safety conditions are violated. This yields a hierarchical supervision structure where interaction level and cluster decide which subgraph is active, while individual transitions are still defined as explicit safety-function conjunctions or disjunctions. The machine-tending use case grounds these abstract states in concrete process stages: the robot picks and transports parts under `SRMS`, switches to `HandGuiding` during quality inspection, and later uses `SSM` or `SRMS` depending on whether the part is sent to maintenance or returned to storage.

### 3. 逐句溯源

1. 句子 1：The proposed HRI safety controller is organized as a multilayer state machine in which each collaborative operation mode becomes a machine state, including `S3-SRMS`, `S4-SSM`, `S5-HG:GC`, `S6-PFL`, `S7-PFL:HO`, `S8-PP`, `S9-HG:FC`, plus stop states `S1/S2` and the higher-level `S10 AutoMode`.
   对应摘录：A
2. 句子 2：Transitions are not narrative-only but formal guard bundles: the move from `SRMS` to `Stop1` requires `DFE ∧ SS1 ∧ SBC ∧ STO`, while recovery from `Stop1` back to `SRMS` requires the danger field to be clear and a manual restart through `MAR`.
   对应摘录：B
3. 句子 3：In a richer cluster, `AutoMode` can enter `SSM` only when one of the collaborative-field entries is active together with safe-motion functions such as `SLS`, `SSM`, `SSR`, and `SDI`, and it can fall back to `Stop1` when danger-field or motion-safety conditions are violated.
   对应摘录：C
4. 句子 4：This yields a hierarchical supervision structure where interaction level and cluster decide which subgraph is active, while individual transitions are still defined as explicit safety-function conjunctions or disjunctions.
   对应摘录：A, B, C
5. 句子 5：The machine-tending use case grounds these abstract states in concrete process stages: the robot picks and transports parts under `SRMS`, switches to `HandGuiding` during quality inspection, and later uses `SSM` or `SRMS` depending on whether the part is sent to maintenance or returned to storage.
   对应摘录：D

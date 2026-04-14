# Safe Performance of an Industrial Autonomous Ground Vehicle in the Supervisory Control Framework - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文按 Ramadge–Wonham DES 形式直接给出 AGV operation subsystem 的状态集、事件集、初始态、active-event 集和转移函数，原文足够完整支撑 `FSM + T0` 双 A。

## 条目 1: Three-mode AGV operation supervisor

- 控制对象：工业自动化与离散制造领域的 AGV 运行模式监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业 AGV 在 supervisory control framework 下的 operation-mode automaton，用 `emergency / reset / active` 三种运行模式和三类模式切换事件组织上层监督行为。
- 判断：算。对象是实际 AGV 的 operation subsystem，不是纯形式化方法流程；原文把自动机六元组、模式语义、可控/不可控事件和状态转移都完整列出。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 36-47 行
> A Cyberphysical system, being an autonomous guided vehicle (AGV) and having diverse applications such as thematic parks and product transfer in manufacturing units, is modeled and controlled. The models of all subsystems of the AGV are provided in discrete event systems (DES) form following the Ramadge–Wonham (R–W) framework. ... the regular languages are realized as supervisory automata in the framework of Supervisory Control Theory (SCT).

#### 摘录 B

- 出处：第 4 页，`2.2. Operation Subsystem`，`paper_content.txt` 第 208-224 行
> The DES model of the AGV operation modes is GMM = (QMM, EMM, fMM, HMM, xMM,0, QMM,m).
>
> The state set of GMM is {qMM,1, qMM,2, qMM,3}. The AGV has three different operational modes: the emergency mode, the reset mode, and the active mode. The state qMM,1 represents the emergency mode. The state qMM,2 represents the reset mode. The state qMM,3 represents the active mode.
>
> The event eMM,1 is the command to switch to reset mode. The event eMM,2 is the command to switch to active mode. The event eMM,3 is the command to switch to emergency mode.
>
> xMM,0 = qMM,1 is the initial state ...
>
> HMM(qMM,1) = {eMM,1}, HMM(qMM,2) = {eMM,2, eMM,3}, HMM(qMM,3) = {eMM,1, eMM,3}.

#### 摘录 C

- 出处：第 4 页，`2.2. Operation Subsystem`，`paper_content.txt` 第 220-229 行
> The transitions of GMM are:
> fMM(qMM,1, eMM,1) = qMM,2, fMM(qMM,2, eMM,2) = qMM,3, fMM(qMM,2, eMM,3) = qMM,1,
> fMM(qMM,3, eMM,1) = qMM,2, fMM(qMM,3, eMM,3) = qMM,2.
>
> The controllable event set is EMM,c = {eMM,1, eMM,2} and the uncontrollable event set is EMM,uc = {eMM,3}.
>
> Obviously, GMM is a nonblocking automaton.

### 2. 基于原文整理后的自然语言描述

The retained control object is the AGV operation-mode automaton `GMM`, which supervises whether the industrial vehicle is in `emergency`, `reset`, or `active` operation. The machine starts in `qMM,1`, meaning `emergency mode`, and only the reset command `eMM,1` is enabled there, so the first admissible transition is from `emergency` to `reset`. Once in `reset mode`, the supervisor either promotes the AGV to `active mode` through `eMM,2` or pushes it back to `emergency mode` through the uncontrollable event `eMM,3`, which models a forced emergency fallback. While in `active mode`, the supervisor can send the AGV back to `reset` through `eMM,1`, and an emergency signal also removes it from active operation by the transition triggered by `eMM,3`. Because the paper explicitly gives the enabled-event sets, transition function, controllability partition, initial state, and nonblocking property, the controller can be read directly as a complete three-state supervisory FSM for AGV mode management.

### 3. 逐句溯源

1. 句子 1：The retained control object is the AGV operation-mode automaton `GMM`, which supervises whether the industrial vehicle is in `emergency`, `reset`, or `active` operation.
   对应摘录：A, B
2. 句子 2：The machine starts in `qMM,1`, meaning `emergency mode`, and only the reset command `eMM,1` is enabled there, so the first admissible transition is from `emergency` to `reset`.
   对应摘录：B
3. 句子 3：Once in `reset mode`, the supervisor either promotes the AGV to `active mode` through `eMM,2` or pushes it back to `emergency mode` through the uncontrollable event `eMM,3`, which models a forced emergency fallback.
   对应摘录：B, C
4. 句子 4：While in `active mode`, the supervisor can send the AGV back to `reset` through `eMM,1`, and an emergency signal also removes it from active operation by the transition triggered by `eMM,3`.
   对应摘录：C
5. 句子 5：Because the paper explicitly gives the enabled-event sets, transition function, controllability partition, initial state, and nonblocking property, the controller can be read directly as a complete three-state supervisory FSM for AGV mode management.
   对应摘录：A, B, C

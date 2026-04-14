# Modular Supervisory Control for the Coordination of a Manufacturing Cell with Observable Faults - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把制造单元多个设备都建模成显式有限自动机，并给出状态、事件、可控/不可控事件和转移函数。当前条目选取其中最完整、最直接可复用的“旋转工作台故障容错控制器”作为代表样本，足以稳定支撑双 A。

## 条目 1: Fault-aware rotating-table manufacturing-cell controller
- 控制对象：工业自动化与离散制造领域的制造单元旋转工作台故障容错控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个制造单元中旋转工作台的故障容错离散控制器，用 `idle / moving / faulty` 三态和 `start / stop / fault / repair` 四事件来管理正常轮转、故障进入和人工修复。
- 判断：算。对象是真实制造单元设备而不是抽象方法示例；原文直接给出状态表、事件表、可控/不可控事件划分和转移函数，控制链完整而且可追溯。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页摘要
> In the present paper, a manufacturing cell in the presence of faults, coming from the devices of the process, is considered. The modular modeling of the subsystems of the cell is accomplished using appropriate finite deterministic automata. The desired functionality of the cell as well as the safety specifications are expressed through the appropriate general type supervisor forms.

#### 摘录 B
- 出处：第 4 页，Table `1` 与 Table `2`
> The set of the states is QT = {qT,1, qT,2, qT,3}. ... The states of the circular rotating table are presented in Table 1:
>
> qT,1 The table is idle
> qT,2 The table is moving
> qT,3 The table is in faulty mode
>
> The alphabet is ET = {eT,1, eT,2, eT,3, eT,4}:
> eT,1 The table starts rotating for 90°
> eT,2 The table stops rotating
> eT,3 A fault took place
> eT,4 The fault has been repaired

#### 摘录 C
- 出处：第 4 页，旋转工作台转移函数说明
> The set of the controllable events is ET,c = {eT,1, eT,4} and the set of the uncontrollable events is ET,uc = {eT,2, eT,3}. ... The values of the transition functions are fT(qT,1, eT,1) = qT,2, fT(qT,2, eT,2) = qT,1, fT(qT,2, eT,3) = qT,3 and fT(qT,3, eT,4) = qT,1.

### 2. 基于原文整理后的自然语言描述

Within the fault-aware manufacturing cell, the circular rotating table is modeled as a three-state finite automaton with states `idle`, `moving`, and `faulty`. The automaton is driven by four discrete events: `start rotating for 90°`, `stop rotating`, `fault occurred`, and `fault repaired`. Commanded start and repair are controllable events issued by the supervisory layer or maintenance personnel, whereas stopping and fault occurrence are treated as uncontrollable observable events. The transition structure is a compact fault-tolerant loop: from `idle` the table can start rotating and enter `moving`; from `moving` it can either complete the rotation and return to `idle` or enter `faulty` when a malfunction or obstruction is detected; from `faulty` it returns to `idle` only after an explicit repair event. This controller is representative of the paper’s broader supervisory-control style, where each manufacturing-cell subsystem is turned into an explicit automaton with observable fault handling.

### 3. 逐句溯源

1. 句子 1：Within the fault-aware manufacturing cell, the circular rotating table is modeled as a three-state finite automaton with states `idle`, `moving`, and `faulty`.
   对应摘录：A, B
2. 句子 2：The automaton is driven by four discrete events: `start rotating for 90°`, `stop rotating`, `fault occurred`, and `fault repaired`.
   对应摘录：B
3. 句子 3：Commanded start and repair are controllable events issued by the supervisory layer or maintenance personnel, whereas stopping and fault occurrence are treated as uncontrollable observable events.
   对应摘录：C
4. 句子 4：The transition structure is a compact fault-tolerant loop: from `idle` the table can start rotating and enter `moving`; from `moving` it can either complete the rotation and return to `idle` or enter `faulty` when a malfunction or obstruction is detected; from `faulty` it returns to `idle` only after an explicit repair event.
   对应摘录：C
5. 句子 5：This controller is representative of the paper’s broader supervisory-control style, where each manufacturing-cell subsystem is turned into an explicit automaton with observable fault handling.
   对应摘录：A

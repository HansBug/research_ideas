# An FPGA-Based Semi-Automated Traffic Control System Using Verilog HDL - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然篇幅不长，但把传统相位、应急相位、`Safe State`、`60 sec / 15 sec` 时序和四路口 flow chart 直接写成了完整控制链，可以作为一条双 A 的 `FSM + T1` 交通灯样本。

## 条目 1: Safe-State Semi-Automated Mealy Traffic Controller
- 控制对象：道路交通信号控制领域的四路口 FPGA 交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定
- 一句话说明：这是一个面向四向路口的 Mealy 交通灯控制器，用传统轮转状态、人工切入的应急状态和全黄 `Safe State` 管理车辆与斑马线放行。
- 判断：算。对象是真实交通信号控制器，原文明确给出状态类别、定时表、flow chart 和 `Safe State` 插入规则，不只是板级展示。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Introduction
> An FPGA-based Semi-automated system is introduced in this paper including a completely new feature “Safe State” to avoid sudden unwanted collision.
>
> The experimental result showed the automated change in traffic lights according to the specified timing sequences.

#### 摘录 B
- 出处：第 2 页，Section 3.1.1 / Table 1
> In this complex state, each road will have six lights (Red, Yellow, Green for going straight, Green for turning Left and Green for turning Right and Green for Zebra-crossing).
>
> Timing Sequence of Traditional States ... `60 sec` green phases alternated with `15 sec` yellow phases.

#### 摘录 C
- 出处：第 2-3 页，Section 3.1.2-3.1.3 / Table 2-3
> In some special cases, like emergency states, the controlling would be different from the traditional one.
>
> The Safe State is needed to occur between the transitions of traditional state and emergency one.
>
> Table 3: Timing Sequence for “Safe State” ... `>= 15 sec`.

#### 摘录 D
- 出处：第 3 页，Section 3.2 / Fig. 2
> Start -> Counter ON, Choose State -> Safe State: All Roads Yellow -> Traditional States: Roads Green Sequentially -> If Emergency? -> One Road Green, Others Red.

### 2. 基于原文整理后的自然语言描述

The controller is a semi-automated Mealy traffic-light machine for a four-road junction in which each road exposes straight, turn, and zebra-crossing signals. In normal operation, the machine cycles through traditional timed phases, where road groups receive `60 sec` green service windows separated by `15 sec` yellow transitions. When an emergency state is requested, the controller does not jump directly from normal cycling into the emergency phase; instead, it first inserts a `Safe State` in which all roads show yellow for at least `15 sec`, explicitly reducing collision risk during mode switching. After this interposed safe phase, the emergency mode opens one selected road while the others remain blocked. The flow chart therefore makes the overall control logic explicit as a three-part chain of `traditional cycle -> safe transition -> emergency override`, rather than a simple fixed-time signal rotator.

### 3. 逐句溯源

1. 句子 1：The controller is a semi-automated Mealy traffic-light machine for a four-road junction in which each road exposes straight, turn, and zebra-crossing signals.
   对应摘录：A, B
2. 句子 2：In normal operation, the machine cycles through traditional timed phases, where road groups receive `60 sec` green service windows separated by `15 sec` yellow transitions.
   对应摘录：B
3. 句子 3：When an emergency state is requested, the controller does not jump directly from normal cycling into the emergency phase; instead, it first inserts a `Safe State` in which all roads show yellow for at least `15 sec`, explicitly reducing collision risk during mode switching.
   对应摘录：A, C
4. 句子 4：After this interposed safe phase, the emergency mode opens one selected road while the others remain blocked.
   对应摘录：C, D
5. 句子 5：The flow chart therefore makes the overall control logic explicit as a three-part chain of `traditional cycle -> safe transition -> emergency override`, rather than a simple fixed-time signal rotator.
   对应摘录：D

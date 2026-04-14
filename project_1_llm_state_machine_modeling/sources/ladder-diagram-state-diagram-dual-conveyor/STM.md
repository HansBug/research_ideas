# Ladder Diagram based on State Diagram for Selection and Assembling Part on Dual Conveyor - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双输送带选料与装配流程写成显式 state diagram / flow-table / ladder 三层对应链，连同 `T1-T6` 定时接点、传感器条件和执行器输出一起保留，足以形成双 A 工业 PLC 顺序控制样本。

## 条目 1: Timed Dual-Conveyor Selection and Assembly Controller

- 控制对象：双输送带工位的选料、分流与装配 PLC 控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是离散制造场景里的双输送带顺序控制器，用上料、光电检测、材质旗标、定时接点、分流槽和下游输送带把“检测高度-识别材质-分流-继续装配”组织成扁平状态链。
- 判断：算。对象是实际双输送带工作单元，原文不仅说明状态图和 I/O 位，还把 `T1-T6` 定时器、`Opt/Flag` 触发条件、`CONV/Sol/Chute` 输出和 ladder 转换都写了出来。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Dual Conveyor Workcell Systems`，`paper_content.txt` 第 11-24、56-64 行
> In industry, conveyor is a means of transportation to move production materials. Conveyor not just move the goods but there are other processes such as counting the number of goods, filling the liquid and so forth because it is equipped with certain sensors and actuators.
>
> By using state diagram, the result of construction of ladder diagram is obtained by 32 rung and the program capacity is 3 KB.
>
> Figure 1 shows Dual conveyor workcell systems intended for material handling using two conveyors (top and bottom). ... dual conveyor is used as the main device that serves to process the selection and assembly of a workpiece based on the criteria of the appropriate height and type of material.

#### 摘录 B

- 出处：第 2 页，`State Diagram Design`，`paper_content.txt` 第 80-85、101-129 行
> Flow-table method or also called a state diagram is a graph that represents the event or state of a system in the form of a circle. ... The state contains the input and output information of a system written in binary digits.
>
> In this research, the design of state diagrams is described in Table 2. Begin by defining the input / output bits that will be used on dual conveyor system described in Table 1. ... Events on dual conveyor systems are also translated into tables 2 before constructing state diagrams (I / O) to facilitate their preparation. Table 2 shows the input / output status occurring in each state, from the first to the last sub process.

#### 摘录 C

- 出处：第 2 页，`Table 2 State Diagram (I/O) in Sequence`，`paper_content.txt` 第 145-160 行
> 1 Relay Start on HMDRV on
>
> 2 HTDC on HMDRV off, DISP1 on, CONV1 on
>
> 3 Opt1 on DISP1 off, CONV1 off
>
> 2 1 Opt1 on T1 Coil on
>
> 2 T1 Contact on T2 Coil on, CONV1 on
>
> 3 T2 Contact on HMDRV on, CONV1 off
>
> Metal 1 Opt2, Flag1 & Flag2 on T3 Coil on
>
> 2 T3 Contact on CONV1 on, Sol3 on, T4 Coil on
>
> 3 T4 Contact on CONV1 off, Sol3 off, Chute2 on
>
> Plastik 1 Opt2 & Flag1 on T5 Coil on
>
> 2 T5 Contact on CONV1 on, Sol2 on, T6 Coil on
>
> 3 T6 Contact on CONV1 off, Sol2 off, Chute1 on

#### 摘录 D

- 出处：第 4 页，`Arrangement of State Diagram (R/O) / Construction Ladder Diagram from State diagram`，`paper_content.txt` 第 311-356 行
> The information in the table will be used to construct a state diagram (R / O) that has a relay / output arrangement on each state.
>
> From the results of designing the state diagram obtained the use of 12 relays and 16 pieces of output. Therefore, a construction of 12 rung relays (y1 to y12) and 16 rung outputs (z1 to z16) are used. However, there are additional rung as much as 4 pieces to support the work process of dual conveyor system.
>
> Note the state (R / O) of Figure 6, relay y1 changes from off (state 1) to active (on state 2) by input x1. Then relay y1 becomes disabled when there is input x3.

### 2. 基于原文整理后的自然语言描述

The dual-conveyor workcell is controlled as a flat PLC state machine that handles part selection and assembly across the top and bottom conveyors for workpieces with different heights and material types. The paper first defines the I/O bits and arranges each subprocess into state-diagram states, including timer contacts and coils `T1-T6`, conveyor drives, display outputs, solenoids, and chute actuators. In the upper-line sequence, `Opt1` starts a timed chain through `T1` and `T2`, and `Opt2` with `Flag1/Flag2` then branches the workpiece into a metal path that drives `Sol3` and `Chute2` or a plastic path that drives `Sol2` and `Chute1` before `Opt3/Opt4` terminate the branch. The method then converts the I/O state diagram into primitive and merged flow tables and finally into relay/output ladder rungs, so the controller keeps explicit states, input-triggered transitions, timer-mediated progress, and actuator outputs all in the original control description.

### 3. 逐句溯源

1. 句子 1：The dual-conveyor workcell is controlled as a flat PLC state machine that handles part selection and assembly across the top and bottom conveyors for workpieces with different heights and material types.
   对应摘录：A
2. 句子 2：The paper first defines the I/O bits and arranges each subprocess into state-diagram states, including timer contacts and coils `T1-T6`, conveyor drives, display outputs, solenoids, and chute actuators.
   对应摘录：B, C
3. 句子 3：In the upper-line sequence, `Opt1` starts a timed chain through `T1` and `T2`, and `Opt2` with `Flag1/Flag2` then branches the workpiece into a metal path that drives `Sol3` and `Chute2` or a plastic path that drives `Sol2` and `Chute1` before `Opt3/Opt4` terminate the branch.
   对应摘录：C
4. 句子 4：The method then converts the I/O state diagram into primitive and merged flow tables and finally into relay/output ladder rungs, so the controller keeps explicit states, input-triggered transitions, timer-mediated progress, and actuator outputs all in the original control description.
   对应摘录：B, D

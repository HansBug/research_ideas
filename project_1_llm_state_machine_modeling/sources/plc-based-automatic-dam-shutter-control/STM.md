# Design of PLC Based Automatic Dam Shutter Control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然很短，但把双浮球、双闸门、蜂鸣告警和电机正反转启闭链写得很集中，足以形成过程控制方向的双 A `EFSM + T0` 样本。

## 条目 1: Two-Float Dam Gate Sequential Open-Close Controller

- 控制对象：过程与环境控制领域的双浮球双闸门水位控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `PLC` 的水闸控制器，用两个浮球传感器监测水位，并按低位、高位和双开关同时触发三种情况分别驱动 `gate 1`、`gate 2` 与蜂鸣告警及反向关门。
- 判断：算。对象是真实闸门控制系统，原文明确给出了输入开关、两级开门、双开关告警和电机正反转关门逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`III. Methodology / Ladder programming`，`paper_content.txt` 第 55-79 行
> In a given system, two float sensors are the input switches connected to the input of the PLC which gives an input signal to the PLC. ... The relay rotates the motor in two directions which we require for forward and reverse operation of dam gates.
>
> Here in this ladder diagram, the conditions of gate closing and opening are given. When the supply has started the mains will turn on at the start of the program. After that during the starting condition, the water level is below the low-level switch then the green LED will blow. After that when water touches the low-level switch it gives input PLC and then motor 1 rotates in the forward direction and opens gate 1. When the water reaches a high-level switch it gives input to PLC and motor 2 rotates in the forward direction and opens gate 2.
>
> When both level switches turn on buzzer will turn on. So after the buzzer turns on, both the motors will rotate in reverse direction and turn off both the gates.

#### 摘录 B

- 出处：第 2 页，`Working of float sensor`，`paper_content.txt` 第 95-110 行
> The float sensor can be used to measure the water level in the dam. The float sensor consists of float that moves up and down with the water level changes. As the float moves, it triggers a switch or sensor element that sends a signal to the PLC indicating the current water level.
>
> The PLC program is designed to read the input signal from the float sensor and the PLC makes decisions based on water level. The PLC automatically opens or closes the dam gates to regulate the flow of water.

#### 摘录 C

- 出处：第 2 页，`Gate control mechanism / Flowchart`，`paper_content.txt` 第 111-149 行
> In gate control system there are two doors in our system. One gate is for prior level and other is used for highest level. When the water sensed by sensor 1 the gate 1 door will be opened by DC motor.
>
> When the water sensed by the sensor 2 the gate door will be opened by another DC motor. The gate will open and close by DC motor which rotates in reverse and forward direction with help of relay.
>
> In this flowchart there are three conditions are given. At the start wait for level sensing at switch 1 and when level is sensed by switch 1 it opens the gate 1 ... After that wait for level sensing at switch 2 and when level is sensed by switch 2 it opens the gate 2 ... when water goes below level switch turns off the gate.

### 2. 基于原文整理后的自然语言描述

The dam controller is built around two float switches that feed water-level events into the PLC and let the ladder logic choose among three main operating conditions. In the initial low-water condition, the system keeps the green indicator on while both gates remain closed. When the lower-level float is triggered, the PLC drives `motor 1` forward and opens `gate 1`; when the upper-level float is later triggered, it drives `motor 2` forward and opens `gate 2`. If both level switches are active together, the buzzer branch is enabled and both motors are commanded to rotate in reverse so the two gates close again. The same logic is described again in the flowchart as a wait-for-switch-1, then wait-for-switch-2, then reverse-close sequence, which makes this a compact but explicit two-threshold gate-control EFSM rather than a vague water-level monitoring paper.

### 3. 逐句溯源

1. 句子 1：The dam controller is built around two float switches that feed water-level events into the PLC and let the ladder logic choose among three main operating conditions.
   对应摘录：A, B, C
2. 句子 2：In the initial low-water condition, the system keeps the green indicator on while both gates remain closed.
   对应摘录：A
3. 句子 3：When the lower-level float is triggered, the PLC drives `motor 1` forward and opens `gate 1`; when the upper-level float is later triggered, it drives `motor 2` forward and opens `gate 2`.
   对应摘录：A, C
4. 句子 4：If both level switches are active together, the buzzer branch is enabled and both motors are commanded to rotate in reverse so the two gates close again.
   对应摘录：A
5. 句子 5：The same logic is described again in the flowchart as a wait-for-switch-1, then wait-for-switch-2, then reverse-close sequence, which makes this a compact but explicit two-threshold gate-control EFSM rather than a vague water-level monitoring paper.
   对应摘录：B, C

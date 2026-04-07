# Design of Automated Parking System Using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：虽然原文只有短篇项目报告体量，但把起重机梳齿式立体停车的停车、取车、回原点和房主认证主链写成了完整步进序列，原文与描述都足以达到双 A。

## 条目 1: Crane-Combs Parking and Retrieval Sequence Controller

- 控制对象：智慧停车与车位管理领域的起重机梳齿式立体停车存取车顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `PLC` 的多层停车设备顺序控制器，用 `M1/M2/M3/M4` 四个电机和若干限位开关驱动起重塔、梳齿和旋转机构完成停车、取车与回原点。
- 判断：算。对象是实际机械式停车系统控制器，而不是停车信息平台；原文直接给出了停车链、取车链、回原点条件、车主安全数据输入和各步的电机/限位联动。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 8-26 行
> Sequential Control algorithms&PLC technology in design of an Automated Parking System(APS) ... The presented design utilizes the Crane type with Combs vehicle transfer system ... The movement of the crane-tower and the combs are applied using 4 DC motors ... A complete SFC (sequential flow chart) for both car parking and retrieving is done to show all various control steps in the APS. In addition, all required transition conditions between those steps were examined.

#### 摘录 B

- 出处：第 3 页，`Sequence of Operation of Crane-Tower & Combs...`，`paper_content.txt` 第 39-56 行
> 1.PLC checks empty & occupied slots in order to choose a parking spot ... the tower has to be at its home position ... 2.When PLC decide which parking spot is empty it gives a signal to motor M1 ... until combs become directly under the car ... 3.After carrying the car another limit switch stops motor M2 & energize motor M1 but in opposite direction ... 4.Motor 4 moves the tower left ... 5.At this point a limit switch stops motor 2 and energize motor 1 to move the combs forward to put the car in the parking spot. 6.When the combs reach the limit switch ... motor 2 begin to move downward until the car is settled ... 7.At this moment the PLC make the previous steps in reversed order until the tower reaches its home position ...

#### 摘录 C

- 出处：第 3 页，`Car Calling Process`，`paper_content.txt` 第 57-81 行
> When car owner comes to the park to get his car, he has to enter 1st some security data & the location of his parking position ... 1.PLC will energize motor M4 to move the tower to the left ... 3. Motor 1 moves the combs forward to parking spot until reaching its position under car ... 5.When the combs reach its initial position a limit switch stops motor 1 & energizes motor 3 which is responsible for rotating the car 180° ... 7. Motor 4 moves tower right until reaching its position in front of delivery spot ... 9. Motor 2 moves combs downward until the car reaches its delivery position ... 10.Motor 1 moves the combs backward until reaching its initial position ...

### 2. 基于原文整理后的自然语言描述

The automated parking system is a PLC-driven sequence controller for a crane-and-combs multi-storey parking mechanism rather than a general parking-management application. Before parking starts, the tower must be at the home position, the PLC chooses an empty slot, drives `M1` forward under the car, lifts the car with `M2`, retracts the combs, shifts the tower left with `M4`, raises again to the selected slot, inserts the car, lowers it into place, and then reverses the sequence back to home. During retrieval, the owner first enters security data and the parking location, after which the controller moves to the target slot, inserts and lifts the combs under the car, retracts the vehicle, rotates it `180°` with `M3`, lowers it, shifts right to the delivery spot, unloads the car, and again returns the mechanism to its initial position. Because the motion chain is written as a full step sequence with motors, limit switches, home-position constraints, and owner authentication, the paper supports a detailed EFSM/T0 parking sample.

### 3. 逐句溯源

1. 句子 1：The automated parking system is a PLC-driven sequence controller for a crane-and-combs multi-storey parking mechanism rather than a general parking-management application.
   对应摘录：A
2. 句子 2：Before parking starts, the tower must be at the home position, the PLC chooses an empty slot, drives `M1` forward under the car, lifts the car with `M2`, retracts the combs, shifts the tower left with `M4`, raises again to the selected slot, inserts the car, lowers it into place, and then reverses the sequence back to home.
   对应摘录：A, B
3. 句子 3：During retrieval, the owner first enters security data and the parking location, after which the controller moves to the target slot, inserts and lifts the combs under the car, retracts the vehicle, rotates it `180°` with `M3`, lowers it, shifts right to the delivery spot, unloads the car, and again returns the mechanism to its initial position.
   对应摘录：A, C
4. 句子 4：Because the motion chain is written as a full step sequence with motors, limit switches, home-position constraints, and owner authentication, the paper supports a detailed EFSM/T0 parking sample.
   对应摘录：A, B, C

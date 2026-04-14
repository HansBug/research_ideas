# Development of Control System for a Prefabricated Board Transfer Palletizer Based on S7-1500 PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把预制板转运码垛机的 `manual / maintenance / automatic` 外层模式与自动入库、出库、复位顺序一起写清，是一条完整的工业设备模式加顺序控制链。

## 条目 1: Manual-Maintenance-Auto Palletizer Supervisor
- 控制对象：工业自动化与离散制造领域的预制板转运码垛机模式与顺序控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于预制板在窑位与输送线之间自动转运的码垛机监督控制器，外层负责工作模式切换，内层负责自动入库、出库及复位顺序。
- 判断：算。对象是真实的 S7-1500 PLC 设备控制系统；原文既给出人工/维护/自动三种模式，又写出自动模式下的具体作业子流程、初始状态与入库出库动作链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section `3.1`，行 62-74
> When operating, the palletizer moves between kiln A and kiln B ... The palletizer takes the prefabricated board from the roller conveyor line and transports it to the designated maintenance kiln position through a series of movements, including transverse movement, lifting, opening the door, conveying, pushing, and closing the door. ... When a maintenance operation is completed, the palletizer retrieves the prefabricated board from the kiln by following a sequence of actions: opening the door, hooking, closing the door, conveying, lifting, transverse movement, and finally transferring it to the roller conveyor line ... Afterward, the palletizer resets itself to its initial state. The initial state of the palletizer is that the bracket platform is securely fixed and docked at the A1-1 kiln position ...

#### 摘录 B
- 出处：第 5 页，Section `4.2. Control Mode`，行 215-222
> The control mode of the palletizer is divided into manual mode, maintenance mode, and automatic mode. ... Manual mode is primarily utilized for scenarios requiring single-step execution ... Maintenance mode is employed for debugging and performing maintenance operations in case of device exceptions. ... Automatic mode is used for normal production, where the palletizing machine automatically carries out operations according to operation instructions issued by the HMI.

#### 摘录 C
- 出处：第 6 页，Section `4.3. Programming in Automatic Mode`，行 226-255
> The control system for palletizing adopts a structured programming approach to decompose the functions of the palletizer and write corresponding function subroutines. ... Initialization subroutine ... resetting working mode, motor protection and emergency stop faults, as well as controlling the reset of the palletizer's initial state. ... In the automatic mode, there are various operational modes, including board storage operation, board retrieval operation, frame transverse operation, platform lifting operation, transverse + lifting operation, taking board operation, and sending board operation. ... Upon pressing the automatic start button, the palletizer executes its tasks automatically in accordance with a predefined sequence of actions. ... Kiln doors opening and closing subroutine ... Push and hook template subroutine ...

### 2. 基于原文整理后的自然语言描述

The prefabricated-board transfer palletizer is supervised by an outer mode manager with `manual`, `maintenance`, and `automatic` modes. `Manual` is used for protected single-step execution, `maintenance` is used for debugging and exception handling through direct clicking operations, and `automatic` is the production mode in which the machine follows HMI-issued commands to run complete workflows. Inside the automatic branch, the controller decomposes the machine into structured subroutines for initialization, storage and retrieval tasks, frame traversal, platform lifting, kiln-door actuation, and push-hook actions. The paper also gives the concrete warehousing and retrieval sequences, such as transverse movement, lifting, opening the door, conveying, pushing, closing the door, and the reverse retrieval chain with hooking and transfer back to the roller conveyor line. After a retrieval cycle, the palletizer resets to a defined initial state at the `A1-1` kiln position, so the machine is described as a layered mode-and-sequence controller rather than a loose equipment overview.

### 3. 逐句溯源

1. 句子 1：The prefabricated-board transfer palletizer is supervised by an outer mode manager with `manual`, `maintenance`, and `automatic` modes.
   对应摘录：B
2. 句子 2：`Manual` is used for protected single-step execution, `maintenance` is used for debugging and exception handling through direct clicking operations, and `automatic` is the production mode in which the machine follows HMI-issued commands to run complete workflows.
   对应摘录：B
3. 句子 3：Inside the automatic branch, the controller decomposes the machine into structured subroutines for initialization, storage and retrieval tasks, frame traversal, platform lifting, kiln-door actuation, and push-hook actions.
   对应摘录：C
4. 句子 4：The paper also gives the concrete warehousing and retrieval sequences, such as transverse movement, lifting, opening the door, conveying, pushing, closing the door, and the reverse retrieval chain with hooking and transfer back to the roller conveyor line.
   对应摘录：A, C
5. 句子 5：After a retrieval cycle, the palletizer resets to a defined initial state at the `A1-1` kiln position, so the machine is described as a layered mode-and-sequence controller rather than a loose equipment overview.
   对应摘录：A, C

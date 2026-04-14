# Modeling and Implementation of Automatic System for Garage Control - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把车库中央控制、车载子系统、优先级缓冲与层次状态机场景模块串成了一条完整的自动泊入/取车控制链，能够稳定支撑 `HSM + T0` 双 A 样本。

## 条目 1: Priority-Buffered Garage Parking and Retrieval Supervisor
- 控制对象：智慧停车与车库管理领域的优先级缓冲式自动泊入与取车监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向自动车库的分层监督控制系统，中央子系统负责空闲车位优先级管理、开闭入口/出口门和下发路径指令，车载子系统则按分层状态机场景完成直行、转向、泊入、出库与避障。
- 判断：算。对象是明确的 garage control system，不是单纯 FPGA 教学稿；原文同时给出了中央控制职责、车位优先级缓冲、车辆路径指令和 hierarchical FSM 模块化执行方式。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Introduction，`paper_content.txt` 第 2-14、41-70 行
> The paper describes a system for garage control providing for automatic parking of arriving cars and driving them to the garage exit on requests. The system is composed of two sub-systems ... One of the basic modules providing for management and priority-driven selection of parking slots is considered in detail. ... One sub-system is responsible for the garage control, i.e. for the set of such operations as: processing and indication of the most preferable slot for parking any new car on the entrance; opening/closing the gates, providing instructions for parked cars that have to be retrieved, etc. Other sub-systems are installed inside cars and they instruct cars how to drive to the slots indicated by the first sub-system.

#### 摘录 B
- 出处：第 2 页，`General architecture of the central sub-system`，`paper_content.txt` 第 128-141 行
> There are four architectural components that are responsible for the following operations: ... Processing requests enable the system to output a sequence of instructions for arriving and exiting cars. The sequence of instructions is presented like the following: wait for opening the entrance gate; drive straight to a position A (until getting a signal from the sensor A), turn right; drive straight to a position B, turn left; drive until the slot with the number i, turn left and park the car to the slot i; ... Control of gates enables entrance and exit gates (doors) to be opened and closed.

#### 摘录 C
- 出处：第 5 页，`Car sub-systems`，`paper_content.txt` 第 506-539 行
> Car sub-systems are responsible for driving cars from their current positions to the indicated destinations and for communications with the central sub-system. The control is based on typical scenarios such as ... Direct motion ... Intelligent cruise control ... Parking to a slot ... Turning ... U-turn ... Exit from slots ... The scenarios are implemented in an extendable set of predefined modules for hierarchical FSMs. Each module generates a sequence of steps needed for carrying out the relevant operation, i.e. it analyzes the signals from sensors and sends signals to actuators that set speed of the car, provide steering control, etc.

### 2. 基于原文整理后的自然语言描述

The garage controller is organized as a layered parking-and-retrieval supervisor with a central subsystem and multiple car subsystems. At the upper layer, the central unit maintains a priority-driven buffer of free slots, opens and closes the entrance or exit gates, and emits ordered route instructions that tell an arriving vehicle when to wait, go straight, turn, and finally park into slot `i`. At the execution layer, each car subsystem follows predefined hierarchical FSM modules for direct motion, parking, turning, cruise control, and slot exit while continuously reacting to sensor signals and actuator commands. Because the paper preserves both the allocation logic and the hierarchical scenario modules that realize the route, it provides a strong `HSM + T0` parking sample rather than a thin occupancy-detection demo.

### 3. 逐句溯源

1. 句子 1：The garage controller is organized as a layered parking-and-retrieval supervisor with a central subsystem and multiple car subsystems.
   对应摘录：A
2. 句子 2：At the upper layer, the central unit maintains a priority-driven buffer of free slots, opens and closes the entrance or exit gates, and emits ordered route instructions that tell an arriving vehicle when to wait, go straight, turn, and finally park into slot `i`.
   对应摘录：A, B
3. 句子 3：At the execution layer, each car subsystem follows predefined hierarchical FSM modules for direct motion, parking, turning, cruise control, and slot exit while continuously reacting to sensor signals and actuator commands.
   对应摘录：C
4. 句子 4：Because the paper preserves both the allocation logic and the hierarchical scenario modules that realize the route, it provides a strong `HSM + T0` parking sample rather than a thin occupancy-detection demo.
   对应摘录：A, B, C

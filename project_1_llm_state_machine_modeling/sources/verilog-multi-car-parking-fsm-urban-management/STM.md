# Verilog-Based Multi-Car Parking System Using Finite State Machines for Urban Parking Management - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：原文把多车位停车门禁写成显式五态控制器，完整给出状态名、入口/出口感知、`carcount` 容量判断、认证分支和满位拒绝规则，足以形成双 A 的停车正例。

## 条目 1: Multi-Slot Password-Gated Parking Controller
- 控制对象：智慧停车领域的多车位门禁与容量控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Verilog 的停车场控制器，把车辆到达、密码校验、车位容量判断、入场放行和满位拒绝统一组织成一个多车位停车 EFSM。
- 判断：算。对象是实际停车基础设施控制器，原文明确给出 `IDLE / WAIT PASSWORD / RIGHT PASS / WRONG PASS / STOP` 五个状态、入口/出口传感器、`carcount` 容量寄存器以及 gate/display 输出链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，`A. System Design and FSM Architecture`，`paper_content.txt` 第 77-83 行
> The proposed multi -car parking system employs a Finite State Machine (FSM) architecture to manage vehicle entry,
> authentication, and exit. Designed in Verilog and implemented on an FPGA using Xilinx Vivado 20.1, the system is simulated in
> ModelSim for validation. It supports up to four parking slots, with scalability for larger configurations, using a Mealy FSM for
> efficient state transitions. The architecture ensures robust slot management in urban parking environments. The FSM includes
> five states: IDLE, WAIT PASSWORD, RIGHT PASS, WRONG PASS, and STOP.

#### 摘录 B
- 出处：第 3 页，`Fig. 1: FSM State Transition Diagram`，`paper_content.txt` 第 97-103 行
> The FSM flow, depicted in Figure 1, illustrates state transitions driven by sensor inputs and authentication outcomes. The core of
> the system revolves around a carcount register, which is used to monitor and maintain the count of occupied slots in the parking
> space.
> The system works as follows:
> When a vehicle approaches the entry point, the entry sensor detects its presence.
> The FSM checks the current value in the carcount register to determine if a slot is available.

#### 摘录 C
- 出处：第 3 页，`Fig. 1: FSM State Transition Diagram`，`paper_content.txt` 第 103-108 行
> If a slot is available (i.e., carcount < maximum slot capacity), the system:
> Authenticates the vehicle if required (e.g., RFID, QR code, number plate recognition).
> Triggers the gate to open for entry.
> Increments the carcount register by 1 to reflect the newly occupied slot.
> Updates a display unit or LED indicator to show the updated status (e.g., “1 Slot Occupied”).
> If no slots are available, the system displays a “Parking Full” message and access is automatically denied.

### 2. 基于原文整理后的自然语言描述

The controller manages parking-lot admission as one Verilog EFSM rather than as a loose combination of sensors and counters. Its main control chain is organized around five named states, `IDLE`, `WAIT PASSWORD`, `RIGHT PASS`, `WRONG PASS`, and `STOP`, so the system can branch explicitly between normal admission and rejection after an arriving vehicle is detected. Once the entry sensor sees a vehicle, the controller checks the `carcount` register to decide whether a slot is still available before it allows the admission branch to continue. If capacity remains, the controller authenticates the vehicle, opens the gate, increments `carcount`, and updates the display or LED status to reflect the new occupancy. If capacity has already reached the slot limit, the controller denies access and reports the parking-full condition instead of opening the gate.

### 3. 逐句溯源

1. 句子 1：The controller manages parking-lot admission as one Verilog EFSM rather than as a loose combination of sensors and counters.
   对应摘录：A, B
2. 句子 2：Its main control chain is organized around five named states, `IDLE`, `WAIT PASSWORD`, `RIGHT PASS`, `WRONG PASS`, and `STOP`, so the system can branch explicitly between normal admission and rejection after an arriving vehicle is detected.
   对应摘录：A
3. 句子 3：Once the entry sensor sees a vehicle, the controller checks the `carcount` register to decide whether a slot is still available before it allows the admission branch to continue.
   对应摘录：B
4. 句子 4：If capacity remains, the controller authenticates the vehicle, opens the gate, increments `carcount`, and updates the display or LED status to reflect the new occupancy.
   对应摘录：C
5. 句子 5：If capacity has already reached the slot limit, the controller denies access and reports the parking-full condition instead of opening the gate.
   对应摘录：C

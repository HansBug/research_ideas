# Design and Implementation of an Efficient Car Parking System Using Verilog for FPGA-Based Applications - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把入口/出口认证、车位检查、放行拒绝与显示更新写成了带局部等待时间的停车门禁状态链，足以形成双 A 的 EFSM 样本。

## 条目 1: Password-Gated Multi-Slot Parking Controller

- 控制对象：智慧停车与车位管理领域的多车位入口/出口门禁与车位更新控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 FPGA 停车控制器，用 `IR1 / IR2` 入口出口检测、密码校验、车位检查和显示更新来驱动放行与拒绝逻辑。
- 判断：算。对象是实际停车门禁与车位管理控制器，不是单纯平台展示；原文明确给出了传感器触发、等待密码、密码匹配、开闸、拒绝和显示更新的主状态链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 17-23 行
> This project presents the design and implementation of an efficient car parking system using Verilog for FPGA-based applications. ... the proposed system is developed to streamline parking management by automating vehicle detection, and availability monitoring in real-time. Utilizing finite state machines (FSMs) and modular design principles, the system ensures robust operation, scalability, and adaptability to varying parking lot sizes and configurations.

#### 摘录 B

- 出处：第 2 页，Section IV `Proposed Methodology`，`paper_content.txt` 第 103-114 行
> Initially, if there is no car in parking entrance, then IR1 sensor cannot detect any vehicle and LED is in OFF condition i.e. it is in IDLE state. If car enters the parking entrance, then IR1 sensor detects the vehicle and LED1 will be ON and the system enters into wait password state and its waits 3nsec. If car owner enters the password (1100) ... If it is matches the LED2 will be ON and relay will turn ON ... In parking exit state, if the car enters the parking exit, then IR2 sensor detects the vehicle ... the system enters into wait password state and its waits 3nsec.

#### 摘录 C

- 出处：第 3 页，Section IV `Proposed Methodology`，`paper_content.txt` 第 127-139 行
> The architecture includes distinct modules for entry and exit control, slot monitoring, and visual output through LEDs or 7-segment displays. These modules work together under the supervision of a central control logic designed using Finite State Machines (FSM) ... The core of the system is the FSM-based controller, which governs the sequence of operations such as detecting vehicle presence, checking slot availability, opening or closing the gate, and updating the slot counter. The FSM transitions between various states like IDLE, CHECK_SLOT, ENTRY_GRANTED, ENTRY_DENIED, and UPDATE_DISPLAY.

### 2. 基于原文整理后的自然语言描述

The parking controller starts from an `IDLE` state in which no vehicle is detected at the entrance and the gate remains closed. When `IR1` or `IR2` detects a vehicle, the machine enters a password-wait stage with a local `3 nsec` delay and compares the entered `1100` code with the stored password before any gate action is allowed. If authentication succeeds, the relay is enabled so that the gate motor opens for entry or exit; if it fails, the controller keeps waiting instead of granting access. In parallel with this authentication chain, the central FSM checks slot availability, maintains the slot counter, and updates the LED or 7-segment outputs that report parking status. The paper also explicitly names the supervisory states `IDLE`, `CHECK_SLOT`, `ENTRY_GRANTED`, `ENTRY_DENIED`, and `UPDATE_DISPLAY`, so the controller is an extended state machine rather than a simple counter.

### 3. 逐句溯源

1. 句子 1：The parking controller starts from an `IDLE` state in which no vehicle is detected at the entrance and the gate remains closed.
   对应摘录：B, C
2. 句子 2：When `IR1` or `IR2` detects a vehicle, the machine enters a password-wait stage with a local `3 nsec` delay and compares the entered `1100` code with the stored password before any gate action is allowed.
   对应摘录：B
3. 句子 3：If authentication succeeds, the relay is enabled so that the gate motor opens for entry or exit; if it fails, the controller keeps waiting instead of granting access.
   对应摘录：B
4. 句子 4：In parallel with this authentication chain, the central FSM checks slot availability, maintains the slot counter, and updates the LED or 7-segment outputs that report parking status.
   对应摘录：A, C
5. 句子 5：The paper also explicitly names the supervisory states `IDLE`, `CHECK_SLOT`, `ENTRY_GRANTED`, `ENTRY_DENIED`, and `UPDATE_DISPLAY`, so the controller is an extended state machine rather than a simple counter.
   对应摘录：C

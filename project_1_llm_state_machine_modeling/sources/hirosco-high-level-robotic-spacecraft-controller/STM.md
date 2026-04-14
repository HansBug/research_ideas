# HIROSCO - A High-Level Robotic Spacecraft Controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然以高层航天器控制架构为主，但把每个子系统必须实现的 `10` 态生命周期状态机和 supervisor 的 severity-based 错误恢复链写得很明确，足以作为 `⚙️` 方向的双 A 控制样本。

## 条目 1: Robotic Spacecraft Subsystem Lifecycle Supervisor
- 控制对象：通用控制与形式化工具领域的航天器子系统生命周期与错误恢复监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个面向 robotic spacecraft 的高层监督器，用统一的子系统状态机管理不同模式下的组件投运、实时链路建立、验证、全功能运行和错误退化。
- 判断：算。虽然论文带有架构背景，但控制对象不是软件开发流程，而是实际航天器子系统的运行生命周期与 supervisor 错误处理链，且原文给出了明确状态集和恢复动作。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，subsystem coordination，`paper_content.txt` 第 181-198 行
> ... telepresence or autonomous mode. Each of these modes requires a different set of subsystems to be operational. Some of these subsystems need to be connected to each other by real-time links. ... the autonomous mode requires a supervisor ... responsible for logging telecommands and telemetry data, monitoring all existing subsystems, global error handling and managing inter-subsystem communication. ... To simplify the commissioning of subsystems ... a finite state machine is mandatory for all subsystems.

#### 摘录 B
- 出处：第 5 页，`Figure 4: Finite state machine for subsystems`，`paper_content.txt` 第 396-455 行
> This state machine consists of ten separate states ... Each subsystem starts or stops in the state "Offline". ... During the subsequent state "Software-Init" ... The next step ... is the "Hardware-Init" state. ... The configuration of the subsystem takes place in the "Pre-Operational" state. ... After the configuration is completed, the state of a subsystem can be changed to the "Safe-Operational" state. ... After the verification is completed, the state machine can switch to the "Operational" state. ... The "Error-Operational" state secures that the hardware devices can reach a defined state after a severe error has occurred ... There are two de-initializing states and a "Post-Operational" state ...

#### 摘录 C
- 出处：第 6-7 页，supervisor event handling / practical tests，`paper_content.txt` 第 518-523 行、第 601-607 行
> ... PUS defines three severity levels for error reporting: low, medium and high. ... if the manipulator failed during a grasp action and had to be shut down ... the MCS would signal an error of high severity. The "Event Handling" must then shut down the real-time network ...
>
> ... Errors of high severity ... result in an immediate shut down of joystick and manipulator subsystem. Errors of medium severity cause the supervisor to change the state of a subsystem to safe-operational. For example, to exceed the torque limit of a joint would cause such an error.

### 2. 基于原文整理后的自然语言描述

HIROSCO organizes robotic-spacecraft operation around a supervisor that decides which subsystems must be active in modes such as telepresence or autonomous operation and that manages the required real-time links between them. To make commissioning and coordination uniform, every subsystem is required to implement the same ten-state lifecycle machine, beginning at `Offline`, then passing through `Software-Init`, `Hardware-Init`, and `Pre-Operational` before the subsystem can enter `Safe-Operational` and finally `Operational`. In `Safe-Operational`, the control algorithms are already running while actuators remain disabled so that the subsystem can be verified before full activation, whereas `Error-Operational` is reserved for bringing hardware into a defined safe condition after severe faults. The machine also includes de-initializing states and `Post-Operational` so that initialization and pre-operational actions can be revoked in an orderly way. On top of that lifecycle machine, the supervisor classifies reported events by severity: low-severity events are logged, medium-severity events drive the affected subsystem back to `Safe-Operational`, and high-severity events shut down the real-time network immediately, which the paper demonstrates by unplugging the robot or joystick in the telepresence setup.

### 3. 逐句溯源

1. 句子 1：HIROSCO organizes robotic-spacecraft operation around a supervisor that decides which subsystems must be active in modes such as telepresence or autonomous operation and that manages the required real-time links between them.
   对应摘录：A
2. 句子 2：To make commissioning and coordination uniform, every subsystem is required to implement the same ten-state lifecycle machine, beginning at `Offline`, then passing through `Software-Init`, `Hardware-Init`, and `Pre-Operational` before the subsystem can enter `Safe-Operational` and finally `Operational`.
   对应摘录：A, B
3. 句子 3：In `Safe-Operational`, the control algorithms are already running while actuators remain disabled so that the subsystem can be verified before full activation, whereas `Error-Operational` is reserved for bringing hardware into a defined safe condition after severe faults.
   对应摘录：B
4. 句子 4：The machine also includes de-initializing states and `Post-Operational` so that initialization and pre-operational actions can be revoked in an orderly way.
   对应摘录：B
5. 句子 5：On top of that lifecycle machine, the supervisor classifies reported events by severity: low-severity events are logged, medium-severity events drive the affected subsystem back to `Safe-Operational`, and high-severity events shut down the real-time network immediately, which the paper demonstrates by unplugging the robot or joystick in the telepresence setup.
   对应摘录：C

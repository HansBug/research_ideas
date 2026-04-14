# Self-Regulating Water Management System using Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了水库闸门的双浮球开关控制、`X0/X1/Y0/Y1/M0` 地址映射和重复执行的开闸-关闸流程。

## 条目 1: Dual-Float Dam Shutter Open-Close Cycle

- 控制对象：过程与环境控制领域的水库闸门 PLC 控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个水库闸门控制器，用于根据上下液位浮球信号控制闸门开闭，并允许 HMI 手动干预。
- 判断：算。对象是实际水管理控制系统，原文给出了液位输入、闸门执行输出、HMI 内部位和反复运行的开关闸流程。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstract / III. METHODOLOGY`
> The control system is designed to monitor the water levels, gates, and pumps in the water reservoir ... The PLCs are programmed to control the gates and pumps according to the water level in the dam ... The PLC, different sensors, control valves, and actuators make up the automation system for dam control ... Ladder logic programming is used to program the PLC to control the opening and closing of the control valves according to the dam's water level.

#### 摘录 B

- 出处：第 4-5 页，`A. Ladder Program / Flow process of water level controller / V. HARDWARE AND IMPLEMENTATION`
> In the program, the address X0 has been assigned to the low-level sensor of the dam, and the address X1 has been assigned to the high-level sensor of the dam. The address Y0 has been connected with the gate opening mechanism, and the address Y1 has been connected with the gate closing mechanism. The address M0 has been internally assigned to the HMI to control the gates regardless of the water level ... Fig 5 explains that the process starts by getting signal from level sensor, if NO it will wait for the sensor signal or if YES then it will proceed to next step by opening the gate. Then it will wait for second sensor signal, if NO it doesn’t close the gate, if YES then it will close the gate and this process run repeatedly ... Lead screws have been used to open the dam gate. The top and bottom levels of the dam are where the floating sensors are maintained.

### 2. 基于原文整理后的自然语言描述

The controller monitors the dam or reservoir level through two float-based level inputs and uses ladder logic to decide when the shutter mechanism should move. In the implemented I/O mapping, `X0` is the lower-level sensor, `X1` is the higher-level sensor, `Y0` drives gate opening, `Y1` drives gate closing, and `M0` is an internal HMI override that allows the operator to control the gate independently of the automatic water-level logic. The automatic sequence starts by waiting for a level signal, opens the gate when the first threshold condition is reached, and then keeps waiting for the second level signal before issuing the close command. This loop repeats continuously, while the actual mechanical movement is realized through relays, a motor, and lead-screw gate actuation.

### 3. 逐句溯源

1. 句子 1：The controller monitors the dam or reservoir level through two float-based level inputs and uses ladder logic to decide when the shutter mechanism should move.
   对应摘录：A, B
2. 句子 2：In the implemented I/O mapping, `X0` is the lower-level sensor, `X1` is the higher-level sensor, `Y0` drives gate opening, `Y1` drives gate closing, and `M0` is an internal HMI override that allows the operator to control the gate independently of the automatic water-level logic.
   对应摘录：B
3. 句子 3：The automatic sequence starts by waiting for a level signal, opens the gate when the first threshold condition is reached, and then keeps waiting for the second level signal before issuing the close command.
   对应摘录：B
4. 句子 4：This loop repeats continuously, while the actual mechanical movement is realized through relays, a motor, and lead-screw gate actuation.
   对应摘录：A, B

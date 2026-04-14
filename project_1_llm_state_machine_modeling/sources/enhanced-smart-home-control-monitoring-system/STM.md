# An Enhanced Smart Home Control And Monitoring System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 `ASM` 图、状态迁移表和优先处理伪代码，把水位、温控、火警、照明和密码门禁集成为一个较完整的 smart-home 监督控制器。

## 条目 1: Priority-Scanned Smart Home Utility and Access Controller
- 控制对象：智能家居场景下的水位、温控、烟雾、照明与密码门禁一体化控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个由 `AT89C51` 驱动的 smart-home 监督控制器，按优先顺序处理水箱液位、室温、烟雾、房间进出与密码输入，并输出泵、空调、蜂鸣器、灯光、门禁和 GSM 报警动作。
- 判断：算。对象是实际 home monitoring and control system，原文不仅有抽象 `FSM` 说明，还给出了 `ASM` 图、状态转移表符号和逐过程伪代码。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 13-29 行
> This paper proposes an enhanced smart home control and monitoring system which conserves energy by automatically controlling various home installations and appliances. The system also secures the house in real time by opening the door only when the right password is supplied and detects fire in its infancy. At the heart of the control is AT89C51 ... Appropriate sensors were chosen to monitor the processes. The output from the sensors serves as input to the microcontroller which actually controls the entire processes.

#### 摘录 B
- 出处：第 3-4 页，`The ASM Chart of the System`，`paper_content.txt` 第 214-309 行
> The design of a finite state machine starts with an abstract graphic description such as a state diagram or an ASM chart ... For the purpose of this work, an ASM chart was used for the design of the finite state machine, “an enhanced smart home control and monitoring system”.
>
> WLS = Water Level Signal ... TCS = Temperature Control Signal ... SKS = Smoke Signal ... MDS = Motion Detection Signal ... KPS = Keypad Signal.
>
> Fig.4: ASM Chart of the System ... St0 ... St1 ... St2 ... St3 ... St4 ... St5 ... St6 ... St7 ... St8 ... St9.
>
> Whenever the comparator output changes from 1 to 0 or vice versa, the present state and next state is executed and an output is generated.

#### 摘录 C
- 出处：第 5-6 页，系统过程描述，`paper_content.txt` 第 520-588 行
> Else if (SKS) then Process (Smoke); Else if (MDS) then Process (Room light); Else if (KPS) then Process (Keypad).
>
> Water: Check water level ... If level is minimum then Switch on pump ... If level is maximum then Display tank full, Switch off pump.
>
> Temperature: Check Temperature ... If (temperature) too high then Switch on “AC” Else switch off “AC”.
>
> Smoke: Check for smoke ... If (smoke sensed) then Sound an alarm Display message (LCD).
>
> Room Light: Check entrance ... If room dark then Switch on light Increment count ... Else if exit then ... Decrement count Switch off light.
>
> Keypad: Check for code ... If code correct then Grant access ... Else if allow “3” time check ... Deny access Send message Sound an alarm Display error (LCD).
>
> The AT commands is activated once the controller receives a signal from the hazard detector (smoke detector) or when the wrong keypad is supplied three times.

### 2. 基于原文整理后的自然语言描述

The enhanced smart-home controller is a priority-scanned EFSM centered on the `AT89C51`, where process variables such as `WLS`, `TCS`, `SKS`, `MDS`, and `KPS` drive transitions across a ten-state `ASM` design. At the functional level, the controller supervises five concrete sub-processes: water-level control starts and stops the pump between minimum and maximum levels, temperature control switches the air-conditioner according to the thermal reading, smoke detection raises an alarm and LCD message, room-light control uses entrance or exit events together with darkness and occupancy count, and keypad access grants or denies door opening. The access branch also carries an escalation rule absent from simpler smart-home samples: after repeated wrong-code attempts the controller denies access, sends a message, sounds an alarm, and displays an error, while smoke events can trigger GSM communication as well. This gives the paper a richer smart-home supervision chain than a single door-or-light demo because it retains both utility control and security recovery logic in one machine.

### 3. 逐句溯源

1. 句子 1：The enhanced smart-home controller is a priority-scanned EFSM centered on the `AT89C51`, where process variables such as `WLS`, `TCS`, `SKS`, `MDS`, and `KPS` drive transitions across a ten-state `ASM` design.
   对应摘录：A, B
2. 句子 2：At the functional level, the controller supervises five concrete sub-processes: water-level control starts and stops the pump between minimum and maximum levels, temperature control switches the air-conditioner according to the thermal reading, smoke detection raises an alarm and LCD message, room-light control uses entrance or exit events together with darkness and occupancy count, and keypad access grants or denies door opening.
   对应摘录：C
3. 句子 3：The access branch also carries an escalation rule absent from simpler smart-home samples: after repeated wrong-code attempts the controller denies access, sends a message, sounds an alarm, and displays an error, while smoke events can trigger GSM communication as well.
   对应摘录：C
4. 句子 4：This gives the paper a richer smart-home supervision chain than a single door-or-light demo because it retains both utility control and security recovery logic in one machine.
   对应摘录：A, B, C

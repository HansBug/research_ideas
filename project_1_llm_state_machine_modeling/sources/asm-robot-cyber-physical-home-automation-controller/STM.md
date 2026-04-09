# ASM-ROBOT: A Cyber-Physical Home Automation Controller with Memristive Reconfigurable State Machine - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把水位、温控、烟雾、感应照明与密码门禁统一写进一张 `MRASM` 迁移表，并逐段解释各 qualifier 如何驱动继电器与输出动作，足以稳定形成 `EFSM + T0` 双 A 样本。

## 条目 1: Sensor-Qualified Home Automation Process Controller
- 控制对象：楼宇机电与智能家居领域的水位、温控、烟雾、照明与门禁一体化过程控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个把水泵、温控、烟雾报警、运动感应照明和密码门锁接到同一 `MRASM` 过程控制器上的智能家居监督控制器。
- 判断：算。对象是明确的 home automation controller，不是单纯的 memristor 方法或通信框架；原文给出了状态链、输入 qualifier、继电器输出以及每条链路对应的动作语义。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 13-24 行
> Abstract—In the next 5 to 10 years, digital Artificial Intelligence with Machine Circuit Learning Algorithms (MCLA) will become the mainstream in complex automated robots. ... This work presents Cyber-Physical Home Automation System (CPHAS) using Memristive Reconfigurable Algorithmic State Machine (MRASM) chart. A process control architecture that supports Concurrent Wireless Data Streams and Power-Transfer (CWDSPT) is developed.

#### 摘录 B
- 出处：第 7 页，`TABLE I. MEMRISTIVE RECONFIGURABLE STATE MACHINE TRANSITION LINK PATH`，`paper_content.txt` 第 620-646 行
> TABLE I. MEMRISTIVE RECONFIGURABLE STATE MACHINE TRANSITION LINK PATH ... WLS TCS SKS MDS KPS ... L1 0 - - - - ST0 0000 ST0 0000 ... L2 1 - - - - ST0 0000 ST1 0001 1 ... L4 0 - - - - ST1 0001 ST2 0011 0 ... L6 - 1 - - - ST2 0011 ST3 0010 1 ... L8 - 0 - - - ST3 0010 ST4 0110 0 ... L10 - - 1 - - ST4 0110 ST5 0111 1 ... L12 - - 0 - - ST5 0111 ST6 0101 0 ... L14 - - - 1 - ST6 0101 ST7 0100 1 ... L16 - - - 0 - ST7 0100 ST8 1100 0 ... L18 - - - - 1 ST8 1100 ST9 1101 1 ... L20 - - - - 0 ST9 1101 ST0 0000 0

#### 摘录 C
- 出处：第 7-8 页，`MRASM Design Description`，`paper_content.txt` 第 650-706 行
> As depicted in Table I, the design chart for MRASM smart automation security control was further characterized using schematics capture C++ scripting. ... For instance, in link path L1 to L4, when the input qualifier, water level signal (WLS) changes its state from logic 0 to logic 1 (L1-L2), Relay1 ... is energized and the water pump turns on. ... The link path L5 to L8 depicts what happens in the temperature channel ... Relay 2 is energized and the air conditioner turns on. ... The L9-L12 depicts what happens in the smoke channel ... the Buzzer is energized and turned on. ... The link path L13-L16 depicts what happens in the motion-controlled light module ... RL3 is energized and the light turns on. ... The link path L17-L20 depicts what happens when the keypad is pressed. When pressed and the input code is correct ... the relay known as RL4 is energized and the door opens. Once the door is shut, the signal changes from logic 1 to 0, L19-L20.

### 2. 基于原文整理后的自然语言描述

The `MRASM` controller organizes home automation as one integrated sensor-qualified process instead of separate ad hoc appliance rules. Its transition table starts from `ST0` and then walks through water-level handling, temperature control, smoke alarm, motion-controlled lighting, and keypad-controlled door access, with each branch driven by one qualifier among `WLS`, `TCS`, `SKS`, `MDS`, and `KPS`. For each branch, the paper explicitly binds guard changes to actuator outputs: `WLS` toggles `RL1` and the water pump, `TCS` toggles `RL2`, `SKS` drives the buzzer, `MDS` controls `RL3` and the light, and correct keypad input drives `RL4` to open the door before returning to `ST0` when the door is shut again. Because the state-transition table and the prose explanation both preserve guards, states, outputs, and branch-local action semantics, this is a strong `EFSM + T0` smart-home process-controller sample.

### 3. 逐句溯源

1. 句子 1：The `MRASM` controller organizes home automation as one integrated sensor-qualified process instead of separate ad hoc appliance rules.
   对应摘录：A, C
2. 句子 2：Its transition table starts from `ST0` and then walks through water-level handling, temperature control, smoke alarm, motion-controlled lighting, and keypad-controlled door access, with each branch driven by one qualifier among `WLS`, `TCS`, `SKS`, `MDS`, and `KPS`.
   对应摘录：B, C
3. 句子 3：For each branch, the paper explicitly binds guard changes to actuator outputs: `WLS` toggles `RL1` and the water pump, `TCS` toggles `RL2`, `SKS` drives the buzzer, `MDS` controls `RL3` and the light, and correct keypad input drives `RL4` to open the door before returning to `ST0` when the door is shut again.
   对应摘录：B, C
4. 句子 4：Because the state-transition table and the prose explanation both preserve guards, states, outputs, and branch-local action semantics, this is a strong `EFSM + T0` smart-home process-controller sample.
   对应摘录：A, B, C

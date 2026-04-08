# FPGA Based SOC for Railway Level crossing Management System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文显式给出道口控制器的九状态 FSM，并把 RF 收包、警示、关闸、等待列车通过与反转开闸顺序写到处理链上，适合作为铁路门控双 A 样本。

## 条目 1: RF-Packet Crossing Warning and Gate Cycle

- 控制对象：轨道交通与铁路控制领域的 RF 驱动平交口预警与栏杆控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于无人值守铁路平交口的 FPGA/SOC 控制器，用 RF 收发器触发预警、关闸、列车通过等待和开闸恢复。
- 判断：算。对象是实际铁路平交口安全控制系统，原文明确说明列车靠近时的 RF 通知、九状态 FSM、红灯/蜂鸣器、栏杆电机关闭与列车通过后的反向开闸动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Introduction`，`paper_content.txt` 第 70-75 行
> Whenever the train arrives towards level crossing 15 Km ahead, the RF transmitter transmits the RF signal contains information bits to the receiver. Upon receiving the RF signal, SOC provides the warning signal to the Road crosser and this can also be used to activate the electromechanical system to close the gate. The gate will be open after the train was crossed the road.

#### 摘录 B

- 出处：第 2 页，`2.2 Finite State Machine (FSM)`，`paper_content.txt` 第 158-171 行
> FSM plays a vital role in the design, has nine states (exclude RESET and END states) of action to be carried out while functioning. Such as
> • Wait for RI (receiver interrupt signal)
> • Read the data from RF receiver
> • Forward to data processing unit
> • Enable PWM signal generator unit for generate the pulse signal close the gate step by step
> • Enable red signal and buzzer
> • Wait for train pass information from RF transceiver
> • After receive the signal enable the PWM signal open the gate
> • Enable green state

#### 摘录 C

- 出处：第 4 页，`Functioning of the circuit diagram`，`paper_content.txt` 第 296-305 行
> The core embedded system in FPGA works as the processor. It is used to control the communication device 433 MHz RF Receiver STR-433. RF transmitter mounted on the top of the train emits series of the bit packets containing the information about the train to be crossed. Upon the receiving RF data packets, processor save the information about the train, the time to be crossed and enables the buzzer to give the warning level crosser. Also it activates the motor to close the gate. After the train crossed over place, it stops the buzzer and run the motor in the reverse direction to open the gate.

### 2. 基于原文整理后的自然语言描述

The level-crossing controller is organized as a nine-state FSM that starts by waiting for a receiver interrupt from the train-mounted RF transmitter, then reads the RF packet and forwards the decoded train information to the processing unit. Once an approaching train is detected, the controller activates the warning path, drives the red signal and buzzer, and enables the PWM-driven motor sequence that closes the gate step by step. After the barrier is down, the controller remains in the waiting phase until it receives the train-pass information from the RF transceiver. It then stops the warning output, reverses the motor direction, reopens the gate, and finally returns the crossing to the green-safe state. The resulting control chain is a fully discrete receive-warn-close-wait-open-reset gate cycle driven by train RF packets rather than by a human operator.

### 3. 逐句溯源

1. 句子 1：The level-crossing controller is organized as a nine-state FSM that starts by waiting for a receiver interrupt from the train-mounted RF transmitter, then reads the RF packet and forwards the decoded train information to the processing unit.
   对应摘录：A, B, C
2. 句子 2：Once an approaching train is detected, the controller activates the warning path, drives the red signal and buzzer, and enables the PWM-driven motor sequence that closes the gate step by step.
   对应摘录：A, B, C
3. 句子 3：After the barrier is down, the controller remains in the waiting phase until it receives the train-pass information from the RF transceiver.
   对应摘录：B
4. 句子 4：It then stops the warning output, reverses the motor direction, reopens the gate, and finally returns the crossing to the green-safe state.
   对应摘录：B, C
5. 句子 5：The resulting control chain is a fully discrete receive-warn-close-wait-open-reset gate cycle driven by train RF packets rather than by a human operator.
   对应摘录：A, B, C

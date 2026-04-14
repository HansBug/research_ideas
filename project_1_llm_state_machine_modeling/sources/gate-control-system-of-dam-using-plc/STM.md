# Gate Control System of Dam using Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了浮球输入 `X000/X001`、电机正反转输出 `Y000/Y001`、蜂鸣器 `Y002` 和 `T0/T1/T2/T3` 的开-停-再开-关闭时序，能形成明确的水坝闸门控制 EFSM。

## 条目 1: Two-Stage Dam-Gate Open-Wait-Open-Close Controller

- 控制对象：过程与环境控制领域的水坝闸门 PLC 水位监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用两个浮球水位传感器驱动闸门两段开门、等待和关门的 PLC 控制器。
- 判断：算。原文详细说明输入/输出、定时器、开闭动作、蜂鸣器以及仿真结果，控制链足够完整。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract / Introduction
> The system consists of float sensors, PLC FX2N20MR, relays and DC motor; float sensors are PLC inputs and relays drive the motor forward or reverse.

#### 摘录 B

- 出处：第 3 页，系统流程说明
> If sensor1 is on, the buzzer is on and the gate opens for 2 seconds, stops for 3 seconds, then opens again for the same time; if sensor2 is on, the gate closes for 4 seconds.

#### 摘录 C

- 出处：第 3 页，`Operation of Ladder Diagram`
> When high sensor `X001` is on, `Y000` and `Y002` run the motor forward and buzzer; timer `T0` runs for 2 seconds, `T1` waits for 3 seconds, `T2` opens again for 2 seconds, and `T3` closes for 4 seconds when lower sensor `X000` is on.

### 2. 基于原文整理后的自然语言描述

The dam-gate PLC controller monitors two float sensors representing lower and higher water levels. When the higher-level sensor `X001` is triggered, outputs `Y000` and `Y002` energize the forward motor direction and buzzer, opening the gate for the first stage while timer `T0` runs for `2` seconds. After `T0` expires, the motor stops and waiting timer `T1` runs for `3` seconds; when the wait completes, `Y000` and `Y002` energize again and timer `T2` opens the gate for another `2` seconds. The gate then remains open until the lower-level sensor `X000` is reached. When `X000` is on, output `Y001` drives the reverse direction with `Y002` off, timer `T3` runs for `4` seconds, and the motor stops with the gate closed.

### 3. 逐句溯源

1. 句子 1：The dam-gate PLC controller monitors two float sensors representing lower and higher water levels.
   对应摘录：A, C
2. 句子 2：When the higher-level sensor `X001` is triggered, outputs `Y000` and `Y002` energize the forward motor direction and buzzer, opening the gate for the first stage while timer `T0` runs for `2` seconds.
   对应摘录：B, C
3. 句子 3：After `T0` expires, the motor stops and waiting timer `T1` runs for `3` seconds; when the wait completes, `Y000` and `Y002` energize again and timer `T2` opens the gate for another `2` seconds.
   对应摘录：B, C
4. 句子 4：The gate then remains open until the lower-level sensor `X000` is reached.
   对应摘录：C
5. 句子 5：When `X000` is on, output `Y001` drives the reverse direction with `Y002` off, timer `T3` runs for `4` seconds, and the motor stops with the gate closed.
   对应摘录：B, C

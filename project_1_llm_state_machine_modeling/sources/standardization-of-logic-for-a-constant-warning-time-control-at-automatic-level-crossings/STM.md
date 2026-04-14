# Standardization of Logic for a Constant Warning Time Control at Automatic Level Crossings - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动道口恒定预警时间控制器的 detector、双计数器、first-train 判定和 barrier open/close 逻辑写得完整，可直接作为铁路道口 EFSM 样本。

## 条目 1: Constant-Warning Railway Crossing Counting Logic

- 控制对象：自动道口恒定预警时间控制的 level crossing controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是铁路平交口领域的微电子 level crossing controller，用于根据 `A / E / B` 三个探测点、`AB / EB` 两个列车计数器和 first-train 判定逻辑控制 warning 开始、持续与 barrier 重新打开。
- 判断：算。对象是实际 automatic level crossing 的主控制器，原文明确给出了 passing/stopping train 的起始探测点、train counting logic、barrier open/close 判断，以及 following train 对 warning 与 brake-pattern 取消的影响。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，`2.1 Constant warning time control system for automatic level crossing`
> A typical system consists of the starting point for a passing train (detector A), the starting point for a stopping train (detector E), the stopping point (detector B), ATS-P and the level crossing controller.
>
> A passing train starts warning from detector A and a stopping train starts warning from detector E.

#### 摘录 B

- 出处：第 8 页，`3.2 Standardization of logic`
> We have utilized an already-existing microelectronic level crossing controller, and its control logic consists of three parts: (i) train count logic; (ii) warning control logic; (iii) diagnostic logic.
>
> TCL counts the numbers of trains between detectors A and B (the AB counter calculates the number) and between detectors E detector B (the EB counter). In addition, the control logic judges whether the approaching train is the first train to arrive or not, and the starting point of the warning is adjusted according to the result.

#### 摘录 C

- 出处：第 8-9 页，`3.2 Standardization of logic`
> Our logic uses the two train counters to control the warning. When the value of the AB counter is zero and that of EB is also zero, our logic stops the warning and opens the barriers. If one or both of counters AB and EB is not zero, the logic continues the warning.

#### 摘录 D

- 出处：第 9-10 页，`3.2 Standardization of logic`
> Firstly, the logic judges whether a train is the first train. Secondly, only the train type of the first train is identified and the level crossing warning commences.
>
> For the following train, the logic only detects the position and does not control warning commencement. It stops the warning only after all trains have left the level crossing control section.

### 2. 基于原文整理后的自然语言描述

The standardized railway level-crossing controller is built around three detector points, where `A` starts warning for a passing train, `E` starts warning for a stopping train, and `B` acts as the stopping point used to subtract trains from the control section. Its software logic is partitioned into train-count logic, warning-control logic, and diagnostic logic, and the train-count part maintains two explicit counters: `AB` for trains between `A` and `B`, and `EB` for trains between `E` and `B`. The controller also determines whether an approaching train is the first train, because only that first train is allowed to trigger warning commencement and train-type identification. A following train is still tracked for position, but it does not restart or recancel the warning logic by itself. Instead, barrier opening is allowed only when both counters fall back to zero, and if either `AB` or `EB` is nonzero the controller continues the warning state, which prevents incorrect reopening for the preceding train and incorrect brake-pattern cancellation for the following train.

### 3. 逐句溯源

1. 句子 1：The standardized railway level-crossing controller is built around three detector points, where `A` starts warning for a passing train, `E` starts warning for a stopping train, and `B` acts as the stopping point used to subtract trains from the control section.
   对应摘录：A
2. 句子 2：Its software logic is partitioned into train-count logic, warning-control logic, and diagnostic logic, and the train-count part maintains two explicit counters: `AB` for trains between `A` and `B`, and `EB` for trains between `E` and `B`.
   对应摘录：B
3. 句子 3：The controller also determines whether an approaching train is the first train, because only that first train is allowed to trigger warning commencement and train-type identification.
   对应摘录：B, D
4. 句子 4：A following train is still tracked for position, but it does not restart or recancel the warning logic by itself.
   对应摘录：D
5. 句子 5：Instead, barrier opening is allowed only when both counters fall back to zero, and if either `AB` or `EB` is nonzero the controller continues the warning state, which prevents incorrect reopening for the preceding train and incorrect brake-pattern cancellation for the following train.
   对应摘录：C, D

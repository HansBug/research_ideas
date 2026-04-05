# Development and implementation of a programmable logic controller and human machine interface for control and monitoring of bottling operations - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把瓶装产线写成由灌装、封盖、贴标和计数串联的 PLC 顺序控制链，并给出各阶段传感器触发、气缸/泵/电机动作和 HMI 定时参数，足以形成双 A 制造样本。

## 条目 1: Fill-Cap-Label Timed Bottling Sequence

- 控制对象：瓶装饮料产线的灌装-封盖-贴标 PLC 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 PLC 和 HMI 顺序驱动瓶子通过灌装、封盖、贴标和计数工位的离散制造控制器。
- 判断：算。对象是真实瓶装产线控制系统，原文明确列出了 `S1-S4` 传感器、`P1-P6` 气缸、泵和电机动作链，以及各阶段的 timer 设置和整周期耗时。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 25-40 行
> This study presents control and monitoring tool for bottle filling, closing, and labelling machine using Programmable Logic Controller (PLC) and Human-Machine Interface (HMI). ... The conveyor transported bottles through the filling, capping, and labeling units. Sensors were installed to detect the presence of bottles. The liquid volume was determined through time settings inputted through the HMI, and the water pump did the filling. After filling, bottles were capped ... Two DC motors handled the labeling ... The number of bottles produced was calculated using a capacitive proximity sensor and displayed on the HMI.

#### 摘录 B

- 出处：第 3 页，`2.1 Prototype Design`，`paper_content.txt` 第 194-227 行
> When the push button start is pressed, the main conveyor runs ... If the bottle is detected by the filling unit sensor (S1), the thruster ... stops the bottle, and P2 pinches the bottle. Then ... P3 ... moves down, and the water pump turns on according to the timer setting ... If the bottle is detected by the capping unit sensor (S2) ... P4 ... stops the bottle, and P5, P6A, and P6B pinch the bottle. Then ... P6C moves down, and the air impact screwdriver turns on according to the timer setting ... If the labeling unit sensor (S3) detects the bottle, the label motor turns on according to the timer setting ... If a bottle is detected by the bottle counting sensor (S4) ... add a value (+1) to the storage data.

#### 摘录 C

- 出处：第 4-5 页，`2.2 Program Design of HMI` 与 `3.4 Processing Time Measurement`，`paper_content.txt` 第 244-289 行与第 387-430 行
> The filling screen ... setting time settings on several components in stage filling ... ON SV2 ... ON SV3 ... ON water pump ... OFF SV1 & SV3 ... OFF water pump. ... The capping screen ... On solenoid 6 & impact ... Off impact ... Off solenoid valve 4. ... The labeling screen ... OFF label motor for setting the working time of the label motor. ... The measurement results show that the system requires an average time of 65.29 seconds to complete the entire process in one full iteration.

### 2. 基于原文整理后的自然语言描述

The bottling controller is a timed PLC sequence that starts when the operator presses the start button and the main conveyor carries bottles through filling, capping, labeling, and counting stations. At the filling station, sensor `S1` stops the bottle, cylinders `P1` and `P2` hold it in place, cylinder `P3` lowers the nozzle, and the water pump runs for the configured duration to achieve the target volume. At the capping station, sensor `S2` triggers `P4`, `P5`, `P6A`, and `P6B` to stop and grip the bottle, then `P6C` drives the air impact screwdriver for a timed cap-tightening action. At the labeling station, sensor `S3` activates the rotary label motor `M3` for a timed label-attachment phase and then the label conveyor `M2` wraps the label around the bottle, while sensor `S4` increments the bottle counter after the product leaves the line. All stage delays and working times are parameterized in the HMI screens, and the full filling-capping-labeling iteration takes about `65.29 s` on average.

### 3. 逐句溯源

1. 句子 1：The bottling controller is a timed PLC sequence that starts when the operator presses the start button and the main conveyor carries bottles through filling, capping, labeling, and counting stations.
   对应摘录：A, B
2. 句子 2：At the filling station, sensor `S1` stops the bottle, cylinders `P1` and `P2` hold it in place, cylinder `P3` lowers the nozzle, and the water pump runs for the configured duration to achieve the target volume.
   对应摘录：B, C
3. 句子 3：At the capping station, sensor `S2` triggers `P4`, `P5`, `P6A`, and `P6B` to stop and grip the bottle, then `P6C` drives the air impact screwdriver for a timed cap-tightening action.
   对应摘录：B, C
4. 句子 4：At the labeling station, sensor `S3` activates the rotary label motor `M3` for a timed label-attachment phase and then the label conveyor `M2` wraps the label around the bottle, while sensor `S4` increments the bottle counter after the product leaves the line.
   对应摘录：A, B
5. 句子 5：All stage delays and working times are parameterized in the HMI screens, and the full filling-capping-labeling iteration takes about `65.29 s` on average.
   对应摘录：C

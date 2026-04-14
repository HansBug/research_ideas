# Development of IoT Based Smart Irrigation System with Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把喷灌控制器的时段允许条件、土壤湿度阈值、手动/自动模式、阀门与水泵联动、以及达到目标湿度后的停灌条件写得很完整，足够形成 `🌡️` 方向的双 A 条目。

## 条目 1: Schedule-and-Moisture Gated Sprinkler Valve Controller

- 控制对象：过程与环境控制领域的土壤湿度驱动喷灌控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向花田喷灌的 PLC 控制器，用设定时段和土壤湿度阈值共同决定何时打开阀门和水泵、何时停止灌溉。
- 判断：算。对象是真实喷灌控制系统，原文不仅给出 `40%-60%` 的目标湿度范围、`08:00-10:00` 的激活时段和 `55+-5%` 的示例阈值，还明确说明 auto/manual 两种模式、阀门触发条件、以及“达到目标后关闭阀门与停泵”的控制闭环。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`Materials and Methods`，`paper_content.txt` 第 13 行
> The data range used for this research was 40% (minimum) to 60% (maximum) ... For example, if the reference limit was set at 55+-5%, and activation time was set at 08.00 - 10.00, if the soil moisture value is still within the wet reference limit (sensor reading at 58%), irrigation will not be activated even though it is within the active time duration (08.00-10.00).

#### 摘录 B

- 出处：第 6 页，`Conceptual Design`，`paper_content.txt` 第 30 行
> When the active irrigation cycle ends, the control unit compares the current soil moisture data to the reference value set by the operator. If the value is out of range (dry conditions), the control unit will command the valve to open, allowing water to flow, and stop when the duration is over. Else, the control unit would not order the valve to activate if the actual soil moisture value is within the range (wet conditions).

#### 摘录 C

- 出处：第 7-8 页，`PLC Controller and Human-Machine Interface (HMI)`，`paper_content.txt` 第 36-41 行
> There are two modes of operation, namely manual and auto. The operator may operate the solenoid valves independently in manual mode using two references: the scheduled time and the soil moisture value. Otherwise, auto mode refers to a predetermined reference value and fully delegated solenoid valve activation to the PLC controller.
>
> In AUTO mode, the irrigation will be involved when it is in the setting time ... and the average soil moisture value is below the set soil moisture reference value.

#### 摘录 D

- 出处：第 9-10 页，`Sensor calibration and verification testing / Performance testing`，`paper_content.txt` 第 47-54 行
> The moisture target is 40% - 60%, indicates that the soil is dry enough to allow the sprinkler valve if the moisture content is less than 40%. However, if the sensor value is greater than 60%, the water level is sufficient for the plants, and irrigation is not needed.
>
> The PLC controller will trigger the valve, open the pump, and water will be flowing through the irrigation pipe and sprinkler nozzle, watering the plants until the actuals reach the range. The irrigation mechanism will continue until the soil moisture value reference provided by the PLC controller is met, at which point the valve will be closed and the pump will stop supplying water through the irrigation system.

### 2. 基于原文整理后的自然语言描述

The smart irrigation controller is a PLC-based extended state machine that combines a scheduled activation window with soil-moisture feedback to decide whether irrigation should start, continue, or remain disabled. The operator configures both the active time range and the target moisture reference, and in auto mode the controller only enables irrigation when the current time lies inside the scheduled window and the measured average soil moisture is below the configured threshold. The paper uses a working range of `40%` to `60%` moisture and even gives a concrete example in which a `55+-5%` reference together with an `08:00-10:00` schedule still blocks irrigation when the current reading is `58%`. Once the soil is classified as too dry, the PLC opens the solenoid valve and starts the pump so water flows through the sprinkler network, and it keeps that watering state until the measured moisture returns to the acceptable range, after which it closes the valve and stops the pump. This is a usable `EFSM + T1` sample because the mode split, schedule guard, threshold guard, and output actions are all stated explicitly in the paper.

### 3. 逐句溯源

1. 句子 1：The smart irrigation controller is a PLC-based extended state machine that combines a scheduled activation window with soil-moisture feedback to decide whether irrigation should start, continue, or remain disabled.
   对应摘录：A, C
2. 句子 2：The operator configures both the active time range and the target moisture reference, and in auto mode the controller only enables irrigation when the current time lies inside the scheduled window and the measured average soil moisture is below the configured threshold.
   对应摘录：C
3. 句子 3：The paper uses a working range of `40%` to `60%` moisture and even gives a concrete example in which a `55+-5%` reference together with an `08:00-10:00` schedule still blocks irrigation when the current reading is `58%`.
   对应摘录：A, D
4. 句子 4：Once the soil is classified as too dry, the PLC opens the solenoid valve and starts the pump so water flows through the sprinkler network, and it keeps that watering state until the measured moisture returns to the acceptable range, after which it closes the valve and stops the pump.
   对应摘录：B, D
5. 句子 5：This is a usable `EFSM + T1` sample because the mode split, schedule guard, threshold guard, and output actions are all stated explicitly in the paper.
   对应摘录：A, B, C, D

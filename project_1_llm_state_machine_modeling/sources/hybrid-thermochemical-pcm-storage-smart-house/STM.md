# Integrated Control of Hybrid Thermochemical-PCM Storage for Renewable Heating and Cooling Systems in a Smart House - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次、显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `smart house` 中的 `TCM/PCM` 热储能系统写成上下两层的有限状态监督器，既给出 `standby / pressurization / charging / depressurization / discharging / safety` 模式集合，也给出 `2.5 bar / PR 5.5 / 90% / 5%` 等具体 guard。

## 条目 1: Hierarchical TCM-PCM smart-house thermal-storage supervisor

- 控制对象：楼宇机电与建筑能源控制领域的智能住宅热储能监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个部署在 `MiniStor smart house` 上的热储能 EMS，用上层有限状态监督器和下层局部调节器协调 `TCM reactor / PCM tanks / heat pump / solar loop` 的充放热过程。
- 判断：算。对象是真实智能住宅供热/制冷控制系统，原文明确给出高层模式集合、入退条件、时间延迟、压力与液位阈值，以及每个模式下泵、阀、压缩机和 `EEV` 的动作逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 10-11 页，`2.3 Control of the Systems (Software)`，`paper_content.txt` 第 382-401 行
> All the described submodules generate status signals that are interpreted by a state machine. This state machine governs the transitions between the system’s operational modes, based on logical conditions that combine inputs from the four submodules, physical sensors, and weather data.
>
> The MiniStor EMS implements a hierarchical, rule-based control strategy organized as a finite-state machine. The upper supervisory layer encodes the admissible operating modes of the system (standby, pressurization/pre-heat, charging, depressurization, discharging, and safety modes) and the logical conditions for transitions between them, including time delays and hysteresis bands that prevent chattering.

#### 摘录 B

- 出处：第 11-13 页，`Standby Mode` 与 Figure 9/10，`paper_content.txt` 第 453-500 行
> Standby Mode: The TCM system remains inactive when no charging or discharging command is received ...
>
> Pressurization Mode ... This mode ends when the tank pressure exceeds 2.5 bar and resumes if the compressor pressure ratio rises above 5.5.
>
> Charging Mode ... The charging process is allowed to continue as long as the receiver liquid level remains below 90% ...
>
> Once the condition PNH3 - PTCM > 0.2 bar is satisfied, the control system transitions to the discharging mode.

#### 摘录 C

- 出处：第 22-23 页，`4.2 Pressurization and Charging Phase`，`paper_content.txt` 第 791-806 行
> Prior to the initiation of the TCM charging phase, the pressurization sequence (Mode 1) from the standby mode is required ... Mode 1 terminates when the tank pressure exceeds its setpoint (~2.5 bar) and is re-entered if the measured compressor pressure ratio later surpasses its limit (e.g., PR > 5.5) or the TCM pressure falls below the threshold of 1 bar.
>
> Continuing with the charging phase ... the supervisory logic alternates between Mode 2 (charging) and Mode 1 (pressurization) to keep the TCM subsystem within its envelope, ensuring safe operation.

### 2. 基于原文整理后的自然语言描述

The MiniStor controller is organized as a hierarchical finite-state supervisor rather than as a loose set of HVAC rules. At the upper layer, the EMS admits six operating modes: `Standby`, `Pressurization/Pre-Heat`, `Charging`, `Depressurization`, `Discharging`, and `Safety`, and each transition is driven by logical expressions over sensor signals, weather data, and subsystem status. Entering `Charging` requires the reactor pressure to rise above about `2.5 bar`, while the controller returns to `Pressurization` when the compressor pressure ratio exceeds `5.5` or the TCM pressure drops below the lower threshold. During charging, the compressor remains active only while the receiver liquid level stays below `90%`; during discharging, the controller first enforces `PNH3 - PTCM > 0.2 bar`, then opens or closes the `EEV` according to the separator float switch, and keeps discharging only while receiver liquid stays above `5%`. Beyond those discrete guards, the paper also states that time delays, hysteresis bands, and minimum dwell constraints are used to avoid oscillation under solar fluctuations and varying building load. The result is a layered smart-house thermal-storage supervisor in which each mode corresponds to a reproducible configuration of pumps, valves, compressor commands, and safety interlocks.

### 3. 逐句溯源

1. 句子 1：The MiniStor controller is organized as a hierarchical finite-state supervisor rather than as a loose set of HVAC rules.
   对应摘录：A
2. 句子 2：At the upper layer, the EMS admits six operating modes: `Standby`, `Pressurization/Pre-Heat`, `Charging`, `Depressurization`, `Discharging`, and `Safety`, and each transition is driven by logical expressions over sensor signals, weather data, and subsystem status.
   对应摘录：A, B
3. 句子 3：Entering `Charging` requires the reactor pressure to rise above about `2.5 bar`, while the controller returns to `Pressurization` when the compressor pressure ratio exceeds `5.5` or the TCM pressure drops below the lower threshold.
   对应摘录：B, C
4. 句子 4：During charging, the compressor remains active only while the receiver liquid level stays below `90%`; during discharging, the controller first enforces `PNH3 - PTCM > 0.2 bar`, then opens or closes the `EEV` according to the separator float switch, and keeps discharging only while receiver liquid stays above `5%`.
   对应摘录：B
5. 句子 5：Beyond those discrete guards, the paper also states that time delays, hysteresis bands, and minimum dwell constraints are used to avoid oscillation under solar fluctuations and varying building load.
   对应摘录：A, C
6. 句子 6：The result is a layered smart-house thermal-storage supervisor in which each mode corresponds to a reproducible configuration of pumps, valves, compressor commands, and safety interlocks.
   对应摘录：A, B

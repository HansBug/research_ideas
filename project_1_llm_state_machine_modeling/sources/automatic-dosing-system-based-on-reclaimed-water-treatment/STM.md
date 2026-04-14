# Automatic dosing system based on reclaimed water treatment - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把再生水系统里的药液稀释、阀门切换、计量泵跟踪和 `P1/P2/P3` 系数计算写成了完整的 `PLC` 自动加药回路，是很扎实的过程加药控制样本。

## 条目 1: Flow-and-Water-Quality Feedback Dosing Controller

- 控制对象：过程与环境控制领域的再生水处理流量/水质反馈加药控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是河道再生水设备中的自动加药控制器，围绕电动阀、流量计、液位计、搅拌器、变频器和隔膜计量泵完成稀释、配药、投加和反馈调节。
- 判断：算。对象是实际污水/再生水加药控制系统，原文不仅给出了自动/本地两种模式，还明确写出了前馈、反馈、修正系数和 `PID` 跟踪机制。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Introduction`，`paper_content.txt` 第 7-15 行、第 25-29 行
> The automatic dosing system can replace the manual regulation mode ... through the study of sewage inlet and outlet flow, online water quality index and other factors. Fully combine feedforward control, feedback control, correction of dosing ratio and other control methods, and use PLC communication and control model to reasonably transform the dosing system ...
>
> The automatic dosing system designed in this paper can replace the manual regulation mode to achieve the purpose of intelligent sewage treatment.

#### 摘录 B

- 出处：第 2-3 页，`3.1 Overview of system design method / 3.2 Control principle`，`paper_content.txt` 第 62-80 行、第 88-99 行
> The dosing system is mainly composed of dosing system, dissolution preparation and dilution system, regulation and control system, etc.
>
> The automatic control of the whole process of dilution and dosing of the system reagent solution is realized through PLC, and the parameters can be automatically adjusted according to the waste water flow and water quality. The metering pump can realize the automatic adjustment of dosing. When the system is in PLC control mode, the full-automatic control of dilution, valve switching and dosing of metering pump can be realized according to the set parameters to realize unattended operation.
>
> The central control system compares the actual value of the dosing flowmeter with the dosing set value in real time, and then outputs the signal to the dosing pump frequency converter through the PID control system to adjust the output frequency.

#### 摘录 C

- 出处：第 3 页，`3.2.1-3.2.4`，`paper_content.txt` 第 100-127 行
> The inlet flow is controlled by the electromagnetic flowmeter, and the dosage dosing coefficient P1 is set with the inlet pump flow ... as the variable of the dosage in different process stages.
>
> Set the water quality feedback coefficient P2 (actual detection value / set value) according to the online actual value and set value of effluent quality.
>
> In order to ensure the normal dosing of process agents, the correction coefficient P3 (empirical value / theoretical value) is added.
>
> The final dosing setting value Q (m3 / h) of the automatic dosing control system is calculated according to the following formula: Q = Q1 x P1 x P2 x P3.

#### 摘录 D

- 出处：第 7 页，`4.3 Regulation control system / 4.3.1 Control requirements`，`paper_content.txt` 第 251-284 行
> The regulation control system is automatically controlled by PLC ... can display, set and modify process parameters in real time, and control the dilution and dosing of reagent solution.
>
> The whole set of reagent dosing device is automatically controlled in the whole process through PLC control equipment ... Then dilute with the designed water volume, and control the start and stop with electric valve.
>
> The system has two modes: local control (field button) and PLC control. Local control is the most priority control mode.
>
> When the system is in PLC control mode, it can realize full-automatic control of dilution, valve switching and dosing of metering pump ... The flow proportional dosing or PID closed-loop control can be selected according to the actual situation.

### 2. 基于原文整理后的自然语言描述

The reclaimed-water dosing unit is a PLC-based reagent controller that runs the whole dilution and dosing process rather than only adjusting one standalone pump. It keeps two control modes, with local control taking priority over PLC control, while industrial Ethernet and the upper computer provide remote monitoring and parameter setting. In automatic mode the upper computer computes the dosing setpoint from influent flow `Q1`, flow-dosing coefficient `P1`, effluent-quality feedback coefficient `P2`, and correction coefficient `P3`, and then sends the target to the diaphragm metering pump through the PLC. The PLC closes the loop by comparing flowmeter feedback with the set dosing value and driving the pump frequency converter through `PID` control so actual reagent flow tracks the target. Around this core loop, the controller also automates valve switching, water addition, tank-level-based dilution, agitator-based proportioning, and the selection between flow-proportional dosing and full closed-loop dosing.

### 3. 逐句溯源

1. 句子 1：The reclaimed-water dosing unit is a PLC-based reagent controller that runs the whole dilution and dosing process rather than only adjusting one standalone pump.
   对应摘录：A, B
2. 句子 2：It keeps two control modes, with local control taking priority over PLC control, while industrial Ethernet and the upper computer provide remote monitoring and parameter setting.
   对应摘录：B, D
3. 句子 3：In automatic mode the upper computer computes the dosing setpoint from influent flow `Q1`, flow-dosing coefficient `P1`, effluent-quality feedback coefficient `P2`, and correction coefficient `P3`, and then sends the target to the diaphragm metering pump through the PLC.
   对应摘录：C
4. 句子 4：The PLC closes the loop by comparing flowmeter feedback with the set dosing value and driving the pump frequency converter through `PID` control so actual reagent flow tracks the target.
   对应摘录：B, C
5. 句子 5：Around this core loop, the controller also automates valve switching, water addition, tank-level-based dilution, agitator-based proportioning, and the selection between flow-proportional dosing and full closed-loop dosing.
   对应摘录：B, D

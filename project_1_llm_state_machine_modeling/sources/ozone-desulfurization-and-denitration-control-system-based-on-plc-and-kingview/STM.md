# Design and implementation of ozone desulfurization and denitration control system based on PLC and kingview - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把锅炉烟气臭氧脱硫脱硝系统的初始化、手动/自动运行、阈值加碱、液位补水、主喷射泵与备用喷射泵切换、以及报警链写得比较成体系，是过程监督控制方向一条清晰的阈值回路样本。

## 条目 1: Manual-auto flue-gas ozone treatment supervisor

- 控制对象：过程与环境控制领域的锅炉烟气臭氧脱硫脱硝 `PLC` 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 `PLC + Kingview` 组织臭氧喷射、脱硫塔循环、碱液配置、液位补给、报警和主备喷射泵切换的烟气处理控制器。
- 判断：算。对象是实际烟气处理系统，原文直接写出初始化等待、手动/自动运行、阈值监测、加碱/补液和主备喷射泵故障切换链，不是单纯的工艺介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`3.1.2 Ozone generating module` 与 `3.1.4 Desulfurization and sale system circulation control module`，`paper_content.txt` 第 121-150 行
> The ozone generating unit is mixed with the pressurized air by the mixing device, and then it is sprayed into the ozone reactor and then mixed with the flue gas. By flue gas sensors to detect the flue gas flow, the use of PLC control module ozone injection time and injection speed gun group...
>
> ... The internal information of the tower sensor is collected in real time, including water level information in the tower, temperature inside the tower, pH of liquid in the tower and pressure inside the tower. The module is the main module of denitration of flue gas and desulfurization.

#### 摘录 B

- 出处：第 2 页，`3.1.5 sodium alkali preparation module` 与 `3.1.6 Automatic alarm system module`，`paper_content.txt` 第 152-174 行
> This module is composed of 1 set of alkali liquid preparation tank ... 2 lye booster pump (1 with one backup) and solenoid valve.
>
> ... When the PH value of the alkaline liquor is lower than 10, the bucket feeder will be manually operated with sodium hydroxide and the solenoid valve will automatically open the refill. When the PH value of the tower is less than 8, the PH controller sends the signal to the lye pump, and the lye pump is used to transport lye in the denitration system. When the liquid level of the flue gas oxidation mixing device is lower than the limit, the solenoid valve is automatically opened to replenish the circulating water in the tower.
>
> When each module values beyond the normal scope, PLC will send alarm signal... such as PLC communication error, import and export pressure value is too large, the high temperature real-time alarm information.

#### 摘录 C

- 出处：第 2-3 页，`4.1 PLC control flow chart design`，`paper_content.txt` 第 180-224 行
> The purpose of PLC control is to realize the control processing of flue gas desulfurization and desulfurization, mainly including system operation mode selection: manual mode or automatic operation mode, The flue gas is tracked in real time ... special case alarm processing and effective communication between information and so on.
>
> ... when the PLC is opened, the system is initialized. After the system initialization is completed, it is in a waiting state, waiting for the manual operation to switch or the automatic operation of PLC.
>
> Manual control mode, the operator can through the button or touch screen to adjust the following modules and control, including ozone generator, the desulfurization denitration one tower, desulfurization tower and alkali lye configuration.

#### 摘录 D

- 出处：第 3 页，手动/自动流程说明，`paper_content.txt` 第 207-243 行
> In the desulfurization and denitrification module, the touch screen on the operating cabinet can observe the nitrogen oxide content in the flue gas emissions, the change of PH value in the tower and the liquid level of desulfurization.
>
> When the desulfurization and selling tower is too low, the operator presses the liquid level control key on the touch screen, and the circulating pump 1 is started... When the PH value of the tower is less than 8, the operator presses the additive button on the touch screen, and the lye circulation pump is activated...
>
> When the nitrogen oxide concentration in the flue gas exceeds the standard, jet pump 1 can be manually open... When the jet pump 1 fails, the backup jet pump 2 can be opened. If the injection pump 2 also fails, it will issue a fault message warning to the PLC.
>
> ... the PLC will immediately monitor whether the alkali solution is needed... When the nitrogen oxide content in the fume on-line monitor is too high, the control jet pump 1 is activated until it reaches a certain level. When the jet pump 1 fails, it will send a fault alarm to the PLC and automatically start the backup injection pump 2... When the nitrogen oxide in the flue gas is stabilized to a lower value, the system will automatically close the jet pump and wait for the next program loop.

### 2. 基于原文整理后的自然语言描述

The ozone desulfurization and denitration controller initializes the PLC cabinet, enters a waiting state, and then branches into either manual or automatic operation for the flue-gas treatment plant. At the process level, flue-gas sensors determine the ozone injection time and spray speed, while tower sensors continuously collect liquid level, temperature, pH, and pressure so that the PLC can supervise the desulfurization and denitration loop. The alkali-preparation branch uses threshold logic rather than fixed timers: when the alkali-liquor `pH < 10`, the refill valve opens and sodium hydroxide is added; when the tower `pH < 8`, the lye pump transports alkali into the denitration system; and when the oxidation-mixing liquid level is low, the solenoid valve replenishes circulating water. In manual mode, the operator watches `NOx`, tower `pH`, and liquid level on the touch screen, manually starts circulation pump 1, enables additive transfer, and opens jet pump 1, while a failed primary jet pump can be replaced by backup jet pump 2. In automatic mode, the PLC monitors the same thresholds by itself: if `NOx` becomes too high it starts jet pump 1, switches to backup pump 2 on failure, closes the jet pump after the flue gas returns to a low value, and emits alarm signals whenever pressure, temperature, communication, or pump states leave the normal range.

### 3. 逐句溯源

1. 句子 1：The ozone desulfurization and denitration controller initializes the PLC cabinet, enters a waiting state, and then branches into either manual or automatic operation for the flue-gas treatment plant.
   对应摘录：C
2. 句子 2：At the process level, flue-gas sensors determine the ozone injection time and spray speed, while tower sensors continuously collect liquid level, temperature, pH, and pressure so that the PLC can supervise the desulfurization and denitration loop.
   对应摘录：A
3. 句子 3：The alkali-preparation branch uses threshold logic rather than fixed timers: when the alkali-liquor `pH < 10`, the refill valve opens and sodium hydroxide is added; when the tower `pH < 8`, the lye pump transports alkali into the denitration system; and when the oxidation-mixing liquid level is low, the solenoid valve replenishes circulating water.
   对应摘录：B
4. 句子 4：In manual mode, the operator watches `NOx`, tower `pH`, and liquid level on the touch screen, manually starts circulation pump 1, enables additive transfer, and opens jet pump 1, while a failed primary jet pump can be replaced by backup jet pump 2.
   对应摘录：D
5. 句子 5：In automatic mode, the PLC monitors the same thresholds by itself: if `NOx` becomes too high it starts jet pump 1, switches to backup pump 2 on failure, closes the jet pump after the flue gas returns to a low value, and emits alarm signals whenever pressure, temperature, communication, or pump states leave the normal range.
   对应摘录：B, D

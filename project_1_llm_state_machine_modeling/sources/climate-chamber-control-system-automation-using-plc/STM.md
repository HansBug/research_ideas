# Climate Chamber Control System Automation Using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把气候舱控制器的 `Off / Automatic / Manual` 模式、温湿度阈值环、CO2 定时投喂、12 段 schedule、dew-point 保护和 Modbus 轮询都写得很细，是过程与环境控制方向很稳的双 A `EFSM + T1` 样本。

## 条目 1: Climate Chamber Schedule-and-Threshold Supervisor

- 控制对象：过程与环境控制领域的气候舱多变量环境控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 Siemens PLC 自动调节温度、湿度、CO2 和照明的气候舱控制器，以 schedule、阈值和安全约束共同决定执行器状态。
- 判断：算。对象是真实环境控制系统，原文明确给出模式编码、执行器开闭规则、阈值带、CO2 定时器、时间槽调度、Modbus 通信周期和异常回退条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 18-19 页，`4.2 Modes / 4.2.1 Off Mode`，`paper_content.txt` 第 472-502 行
> The control system operates in three modes, which are defined by the variable Setpoints.mode ... 0: Off mode ... 1: Automatic mode ... 3: Manual mode.
>
> In Off mode, all actuators are turned off to prevent accidental activation. ... Power off the AC ... Stop dehumidifier ... Stop humidifier ... Power off the left light ... Power off the right light ... Stop feeding the CO2.

#### 摘录 B

- 出处：第 19-24 页，`4.2.2 Automatic Mode / 4.2.3 Manual Mode`，`paper_content.txt` 第 503-610 行、第 622-657 行
> The automatic mode is the primary operational state for the climate chamber ... designed to regulate environmental conditions based on predefined setpoints and schedules.
>
> Humidifier activation: if the current humidity is below the lower threshold, the humidifier is turned on ... Dehumidifier activation: if the current humidity is above the upper threshold ... Neutral zone: if the humidity is within an inner threshold range ... both the humidifier and dehumidifier are turned off.
>
> Heating mode: activated if the temperature drops below the lower threshold. Cooling mode: activated if the temperature rises above the upper threshold. Fan mode: activated if the temperature is within an inner threshold range around the setpoint.
>
> When the internal CO2 is lower than the lower threshold within the chamber, the chamber CO2 valve opens automatically ... two timers are implemented. The first timer known as Open_valve_timer ... The other timer which is referred to as CO2_delay helps in putting a time gap between the two consecutive feedings of CO2.
>
> In the manual mode, the control of the climate chamber's actuators is done directly through user-defined setpoints ... The AC can be turned on or off ... mode of operation ... fan speed ... temperature setpoint.

#### 摘录 C

- 出处：第 24-33 页，`4.3 Schedule / 4.4 Implementing Modbus Communication in PLC / 4.6 Safety Measures`，`paper_content.txt` 第 658-733 行、第 742-846 行、第 883-906 行
> The scheduling mechanism ... Initially, a simple day/night state was requested ... However ... an extended version of the schedule was implemented. In this extended schedule, a full day (24 hours) can be broken down into up to 12 time slots.
>
> The Value_from_schedule function block ... uses the current time to determine the appropriate setpoint ... Interpolation ... provide a smooth transition.
>
> For the Modbus cyclic interrupt with a cycle of 500 ms written in the LAD language was created.
>
> The mode changes to OFF state if the schedule is invalid. ... If the current temperature is closer to the calculated dew point value than the configured dew point threshold ... the humidifier is set off, the dehumidifier is set on, the air conditioner is set to mode “dry”.

### 2. 基于原文整理后的自然语言描述

The climate-chamber controller is an extended-state supervisor with three top-level modes encoded in `Setpoints.mode`: `0` for off, `1` for automatic, and `3` for manual. In off mode the PLC explicitly de-energizes the AC, humidifier fan, dehumidifier relay, humidifier relay, lighting relays, and CO2 valve so the chamber cannot start accidentally. In automatic mode it compares sensor readings against scheduled setpoints and threshold bands to decide when to enable humidification, dehumidification, heating, cooling, fan-only circulation, CO2 valve opening, and timed lighting, while also enforcing dew-point protection and actuator-specific limits. CO2 delivery is timed by `Open_valve_timer` and `CO2_delay`, the daily recipe can expand from a simple day and night pair to up to `12` time slots with interpolation between setpoints, and Modbus read/write cycles run on a `500 ms` interrupt so AC and dehumidifier status are synchronized with the PLC logic. Manual mode exposes direct actuator-level commands for testing and maintenance, but invalid schedules force the controller back to `OFF` and the UI surfaces readiness or error states instead of blindly executing unsafe requests.

### 3. 逐句溯源

1. 句子 1：The climate-chamber controller is an extended-state supervisor with three top-level modes encoded in `Setpoints.mode`: `0` for off, `1` for automatic, and `3` for manual.
   对应摘录：A
2. 句子 2：In off mode the PLC explicitly de-energizes the AC, humidifier fan, dehumidifier relay, humidifier relay, lighting relays, and CO2 valve so the chamber cannot start accidentally.
   对应摘录：A
3. 句子 3：In automatic mode it compares sensor readings against scheduled setpoints and threshold bands to decide when to enable humidification, dehumidification, heating, cooling, fan-only circulation, CO2 valve opening, and timed lighting, while also enforcing dew-point protection and actuator-specific limits.
   对应摘录：B, C
4. 句子 4：CO2 delivery is timed by `Open_valve_timer` and `CO2_delay`, the daily recipe can expand from a simple day and night pair to up to `12` time slots with interpolation between setpoints, and Modbus read/write cycles run on a `500 ms` interrupt so AC and dehumidifier status are synchronized with the PLC logic.
   对应摘录：B, C
5. 句子 5：Manual mode exposes direct actuator-level commands for testing and maintenance, but invalid schedules force the controller back to `OFF` and the UI surfaces readiness or error states instead of blindly executing unsafe requests.
   对应摘录：B, C

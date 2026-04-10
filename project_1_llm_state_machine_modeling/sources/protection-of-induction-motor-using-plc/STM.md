# Protection of Induction Motor Using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `监测电压/电流/温度 -> 与阈值比较 -> 发出保护继电器信号 -> 切断接触器 -> 故障指示` 这一套保护链讲清楚了，可直接入库。

## 条目 1: Voltage-current-temperature trip protection controller

- 控制对象：工业电气领域的三相感应电机 PLC 保护控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向三相感应电机的 PLC 保护系统，用电压、电流和温度传感输入来决定是否维持供电、触发跳闸和点亮故障指示。
- 判断：算。对象是实际工业保护控制器，原文明确写出传感器、保护继电器、接触器和停机指示之间的因果链，而不是只谈电机故障背景。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`Methodology and Implementation`，`paper_content.txt` 第 87-103 行
> The voltages, the current, and the temperature values of the motor, and the problems occurring in the system, are monitored and warning lights are shown on the designated LED Fault Indicators. ... Voltage transformer, current transformer and ntc temperature sensor is used to measure voltage, current and temperature respectively. These sensors provide data to be compared against the initial value set with the PLC. The PLC is connected to a protection Relay ... whenever a voltage, current or temperature is sensed that is not within the limits provided to the PLC, the PLC send a signal through the protective relay to the 3-phase contactor that is connected to the motor to disconnect the motor from the mains power supply.

#### 摘录 B

- 出处：第 3 页，`Fig. 1 Circuit Diagram`，`paper_content.txt` 第 107-110 行
> In the above circuit diagram, the three-phase supply is given to the motor through a trip coil. The phase voltage, phase current, temperature is monitored using PLC. These monitored values are continuously compared with their rated value stored in PLC. If any fault occurs, the program automatically stops the motor immediately. The motor is shut down by the control signal sent from PLC. When the motor is turned off an indication is shown.

### 2. 基于原文整理后的自然语言描述

The protection controller keeps the induction motor in a powered state only while the sensed phase voltage, phase current, and temperature remain within the limits stored in the PLC. Voltage transformers, current transformers, and an NTC temperature sensor continuously feed measurement values into the controller so the ladder logic can compare them against the configured rated values. If any monitored variable moves outside its allowed range, the PLC drives the protection relay and trip path that control the three-phase contactor, disconnecting the motor from the mains immediately. After the trip is issued, the controller places the motor in a shutdown condition and turns on the corresponding warning indication so the fault is visible to the operator.

### 3. 逐句溯源

1. 句子 1：The protection controller keeps the induction motor in a powered state only while the sensed phase voltage, phase current, and temperature remain within the limits stored in the PLC.
   对应摘录：A, B
2. 句子 2：Voltage transformers, current transformers, and an NTC temperature sensor continuously feed measurement values into the controller so the ladder logic can compare them against the configured rated values.
   对应摘录：A
3. 句子 3：If any monitored variable moves outside its allowed range, the PLC drives the protection relay and trip path that control the three-phase contactor, disconnecting the motor from the mains immediately.
   对应摘录：A, B
4. 句子 4：After the trip is issued, the controller places the motor in a shutdown condition and turns on the corresponding warning indication so the fault is visible to the operator.
   对应摘录：A, B

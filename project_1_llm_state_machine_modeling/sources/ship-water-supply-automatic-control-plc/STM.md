# The Design of Water Supply Automatic Control System of Ship Based on PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把船舶集中供水系统的温度调节、冷/热水混合、PLC 输入输出以及 start-work-stop-emergency 分支写成了明确控制链，可作为过程温控方向的双 A 样本。

## 条目 1: Temperature-Regulated Ship Water-Supply Start-Work-Stop Control
- 控制对象：船舶集中供水系统的 PLC 温度调节与启停控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是船舶能源与供水系统里的 PLC 集中控制器，用温度探头、流量开关、阀门、加热器和循环泵协调多级热水箱的供水与温度保持。
- 判断：算。对象是实际船舶过程控制系统，正文明确给出了温度低/高两种调节分支、PLC 输入输出集合以及启动、停机和紧急停机逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，`III. The Heating Circulation System`，`paper_content.txt` 第 111-137 行
> The exhaust energy in the pipes heat the water in the water jacket which has heat losses ... When the water temperature is too low in the buffer electric heating mixed box, the temperature two-way switch will be closed. The heater will be switched on completely. When the water temperature in the mixed box meet the requirements of the temperature the bidirectional switch will be switched off to be in the insulating state.
>
> Because the exhaust heat temperature will be gradually reduced when it be transfered in the exhaust pipes. So the temperature of the first level water tank is 30 ~ 40 ℃ ... used as bathing water. The second tank water temperature is 70 ~ 80 ℃ ... used for heating oil and cylinder liner cooling water. The water temperature of three stage water jacket is about 100 ℃ ... used to be the kitchen water, these three kinds of water temperature is adjusted by the temperature probe, the new gate valve and the heater.

#### 摘录 B
- 出处：第 2 页，`A. Temperature Regulation in the Water Supply System`，`paper_content.txt` 第 138-160 行
> When the water temperature in the supply pipe is lower than the design value, the temperature probe will take temperature signal to the new gate valve. The gate valve will close slightly. At the same time, the temperature package in the buffer electric heating mixed will feel the water temperature reduced, the temperature switch will be closed, the heater heat water until the water temperature get the settings to keep the water temperature constant.
>
> When the temperature of water supply in the pipeline higher than design value, the temperature probe will put the signal to the new gate valve. The gate valve will open slightly and add cold water. At the same time, the temperature sense bag in the mixing water package will send signals to the temperature switch. The temperature switch is disconnected. Then the heater stops working. The temperature will be decreased until the temperature reached the design value of temperature.
>
> This system will keep the temperature of water in a certain temperature range. The buffer heating mixed tank has played the role of a buffer.

#### 摘录 C
- 出处：第 2-3 页，`V. PLC CENTRALIZED CONTROL SYSTEM / A. Start and Work / B. System Stoping`，`paper_content.txt` 第 167-200 行
> The system is controlled by the PLC. The system has 3 input signals and 3 output signals. Input signals include circulating pump control switch, a temperature probe and the flow switch. The output signal include circulating pump motor, the new inlet electromagnetic valve and the pump motor.
>
> When the vessel operation or the occurrence of staff need the System will startup. When the circulating pump total switch and the individual systems be opened, the system will be work in the condition of the normal operation. When the water flow switch is opened, the water pump will be started to work for water supply. A temperature probe is to sense the change of temperature, to control the new water valve, to ensure the temperature, to meet the requirements.
>
> When the staff control switch of the circulating pump off, a single system will be corresponded to stop working. In case of emergency, the staff will control the circulating pump control switch closing. The whole system will cease to work in order to avoid accident intensifies.

### 2. 基于原文整理后的自然语言描述

The ship water-supply controller combines diesel exhaust heat, solar energy, a buffer electric-heating mixed box, a temperature probe, a new gate valve, and a heater to maintain three tank levels at about `30-40 ℃`, `70-80 ℃`, and `100 ℃` for bathing water, oil and cylinder-liner heating water, and kitchen water. When the supply-pipe temperature falls below the design value, the temperature probe sends a signal that slightly closes the new gate valve, the temperature switch closes, and the heater keeps heating until the set temperature is restored. When the pipeline temperature rises above the design value, the probe causes the new gate valve to open slightly to add cold water, the temperature switch disconnects, and the heater stops until the water temperature decreases back to the design value. The PLC centralized control system uses three inputs, namely the circulating-pump control switch, temperature probe, and flow switch, and three outputs, namely the circulating-pump motor, the new inlet electromagnetic valve, and the pump motor; when the vessel needs water and the switches are opened the flow switch starts water supply, turning off the circulating-pump control switch stops a single system, and emergency closing stops the whole system.

### 3. 逐句溯源

1. 句子 1：The ship water-supply controller combines diesel exhaust heat, solar energy, a buffer electric-heating mixed box, a temperature probe, a new gate valve, and a heater to maintain three tank levels at about `30-40 ℃`, `70-80 ℃`, and `100 ℃` for bathing water, oil and cylinder-liner heating water, and kitchen water.
   对应摘录：A
2. 句子 2：When the supply-pipe temperature falls below the design value, the temperature probe sends a signal that slightly closes the new gate valve, the temperature switch closes, and the heater keeps heating until the set temperature is restored.
   对应摘录：B
3. 句子 3：When the pipeline temperature rises above the design value, the probe causes the new gate valve to open slightly to add cold water, the temperature switch disconnects, and the heater stops until the water temperature decreases back to the design value.
   对应摘录：B
4. 句子 4：The PLC centralized control system uses three inputs, namely the circulating-pump control switch, temperature probe, and flow switch, and three outputs, namely the circulating-pump motor, the new inlet electromagnetic valve, and the pump motor; when the vessel needs water and the switches are opened the flow switch starts water supply, turning off the circulating-pump control switch stops a single system, and emergency closing stops the whole system.
   对应摘录：C

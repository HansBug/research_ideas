# Upgrading of Alum Preparation and Dosing Unit for Sharq Dijla Water Treatment Plant by Using Programmable Logic Controller System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三座明矾配制池的优先级切换、配制步骤、泵阀/鼓风机动作、传感器融合加药和自动停机条件写成了可追溯的 `PLC + SCADA` 过程控制链，是质量很高的给水厂加药样本。

## 条目 1: Priority-Basin Alum Preparation and Sensor-Fused Dosing Controller

- 控制对象：过程与环境控制领域的给水厂明矾配制、优先级 basin 切换与投加泵速调节控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 `Sharq Dijla WTP` 化学投加单元的高层监督控制器，围绕三座配制池、卸料阀、供水泵、鼓风机、投加泵以及 `FIT / DIT / ALIT / TIT / LIT` 传感器完成明矾配制和投加调节。
- 判断：算。对象是实际水厂加药控制系统，原文直接说明了自动/手动模式、池优先级、配制步骤、传感器闭环和停机条件，足以组织成完整状态机自然语言描述。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 15-29 行
> This study deals with how to transform the conventional operation to an automatic monitoring and controlling system depending on a Programmable Logic Controller (PLC) and on line sensors for alum preparation and dosing unit in Sharq Dijla WTP. PLC system will receive, analyze transmitting data, compare them with preset points then automatically orders the operational equipment (such as pumps, valves, and mixers) in a way that guarantees the safe and appropriate operation of the unit.

#### 摘录 B

- 出处：第 4-5 页，`4.1 Alum Preparation & Dosing Units Instrumentations`，`paper_content.txt` 第 208-229 行、第 237-248 行
> The following devices can be used to control the alum preparation and dosing manually through the OWS, Local Control Panel (LCP) when the manual mode is selected or automatically through the PLC-CB when the automatic mode is selected.
>
> An ultrasonic LIT would be used on the alum preparation basins ... DIT would be used in the preparation basins to monitor the alum solution concentration ... TIT ... for the automatic control of the dosing operation ... FIT signal of the influent raw water flow should be connected to the PLC-CB ... dosing pump speeds ... replace them by variable speed pumps ...

#### 摘录 C

- 出处：第 5-6 页，`4.2 Automatically Operation`，`paper_content.txt` 第 256-277 行
> Before selecting the auto mode, the three preparation basins must be set with priority within the PLC-CB. Each basin priority is selected depending on the alum solutions preparation age. The basin with longer alum solutions preparation age is set with the first priority for feeding dosing pumps.
>
> After selecting the Auto mode, the PLC-CB detects the alum solution level in the three basins to start the alum preparation within the empty basins.
>
> To start the alum preparation, the PLC-CB sends firstly an order to the silo unloading-valve to unload the pre-set value of the alum powder ... operate the water service pumps to fill the tank with specific water level controlled LIT signals. Then sends orders to operate the air blower and opening the air inlet valves of the basin to start mixing for a preset period.
>
> The PLC-CB will use the FIT, DIT, ALIT and TIT signals to calculate the alum required feeding rate and modify the dosing pumps speed in order to obtain the required alum dosage.

#### 摘录 D

- 出处：第 6 页，`This process proceeds automatically until`，`paper_content.txt` 第 297-303 行
> This process proceeds automatically until:
> a) Manual operation sets on the OWS or LCP,
> b) The PLC-CB receive the signal from LIT in-ground storage tank indicating that is full,
> c) Low turbidity level of raw water indicating by TIT in the low lift pumping wet-well,
> d) No response for low alum powder level alarm on the silo,
> e) Instrumentations damage without alarm response for repair,
> f) Emergency shutdown of WTP.

### 2. 基于原文整理后的自然语言描述

The Sharq Dijla alum unit is supervised by a PLC/SCADA controller that switches between local/manual handling and automatic preparation-dosing operation for three preparation basins. Before automatic mode starts, the controller assigns basin priority according to alum-solution age, selects the highest-priority nonempty basin for feeding, and detects which basins are empty and need a new preparation cycle. To prepare a new batch, the PLC opens the silo unloading valve for a preset powder quantity, runs the service pumps until the `LIT` target level is reached, and then starts the air blower and inlet valves for a preset mixing period. During dosing, the controller fuses `FIT`, `DIT`, `ALIT`, and `TIT` to compute the required alum feed rate and adjust variable-speed dosing pumps so dosage follows raw-water flow, basin concentration, turbidity, and residual-aluminum constraints. The automatic sequence continues until manual takeover, full downstream storage, low raw-water turbidity, unresolved low-powder alarm, instrumentation failure, or plant emergency shutdown.

### 3. 逐句溯源

1. 句子 1：The Sharq Dijla alum unit is supervised by a PLC/SCADA controller that switches between local/manual handling and automatic preparation-dosing operation for three preparation basins.
   对应摘录：A, B
2. 句子 2：Before automatic mode starts, the controller assigns basin priority according to alum-solution age, selects the highest-priority nonempty basin for feeding, and detects which basins are empty and need a new preparation cycle.
   对应摘录：C
3. 句子 3：To prepare a new batch, the PLC opens the silo unloading valve for a preset powder quantity, runs the service pumps until the `LIT` target level is reached, and then starts the air blower and inlet valves for a preset mixing period.
   对应摘录：B, C
4. 句子 4：During dosing, the controller fuses `FIT`, `DIT`, `ALIT`, and `TIT` to compute the required alum feed rate and adjust variable-speed dosing pumps so dosage follows raw-water flow, basin concentration, turbidity, and residual-aluminum constraints.
   对应摘录：B, C
5. 句子 5：The automatic sequence continues until manual takeover, full downstream storage, low raw-water turbidity, unresolved low-powder alarm, instrumentation failure, or plant emergency shutdown.
   对应摘录：D

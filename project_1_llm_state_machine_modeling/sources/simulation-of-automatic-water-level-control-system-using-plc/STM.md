# Simulation of Automatic Water Level Control System by using Programmable Logic Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把八级液位感知、泵启停阈值、S7-1200 输入输出表和 PLC 梯形图组合在一起，足以形成完整的水位顺序控制样本。

## 条目 1: Eight-Step PLC Water Level and Pump Starter Controller

- 控制对象：基于 S7-1200 的八级水位传感与泵启停控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似（PLC 水位顺序控制簇）

### 0. 条目识别与判定

- 一句话说明：这是过程与环境控制领域的水位控制器，利用八级传感器 S1-S8、S7-1200 PLC 和泵启动回路把“缺水补水、满水停泵、跌回阈值再启动”写成了完整控制链。
- 判断：算。对象是实际水箱液位控制系统，不是纯传感器电路说明；正文给出了状态级别、最小/最大阈值动作、PLC 梯形图和 I/O 名单。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，Operation Of Water Level Indicator Control System，`paper_content.txt` 第 303-335 行
> If the level reach the under level limit, the sensor (S1) will actuate ... If the water level reach to the 7th state level, the sensor (S7) will actuate ... relay outputs the contact to send a minimum water level signal to the PLC to run the pump motor ... If the water level reach to the 8th state level, the sensor (S8) will actuate ... send a maximum water level signal to the PLC to stop the pump motor. If the water level refill and under of the 7th state level, the pump motor restarts to run again to maintain the water level between the minimum and maximum level.

#### 摘录 B

- 出处：第 4 页，Manual water level control system，`paper_content.txt` 第 340-354 行
> Manual control is used in water pumping system as an auxiliary control ... One of the power circuits of star-delta control is shown in figure 8 ... Manual control circuit ... consists of 6 magnetic contactors, 2 timer, 4 pilot light and 4 push buttons.

#### 摘录 C

- 出处：第 5-7 页，Automatic water level control system by PLC，`paper_content.txt` 第 365-370 行，396-408 行
> Siemen S7-1200 PLC is used in control circuit associated with programming software. Ladder diagram language is used ... Figure 11 shows the PLC ladder diagram ... Input List I0.0= system stop, I0.1= system start, I0.2= emergency stop, I0.5 = GT min level limit switch, I0.6 = GT max level limit switch, I0.7 = OH min level limit switch, I1.0 = OH max level limit switch ... Output List O0.0= System RUN PL ... O0.5= GT Pump STOP PL ... O1.0= DMC2.

### 2. 基于原文整理后的自然语言描述

The automatic water-level controller represents the tank level as an eight-step sequence sensed by electrodes `S1` to `S8`, and it updates the plant state as the water rises through successive bands. The PLC keeps the pump off while the tank is below the activation condition, then treats `S7` as the minimum refill threshold that generates a PLC signal to run the pump, and `S8` as the maximum threshold that commands the PLC to stop the pump. If the water level later drops below the seventh state again, the controller restarts the pump so that the tank is maintained between the minimum and maximum bands rather than running only once. The implementation is tied to a Siemens `S7-1200` ladder program whose input list includes system start, stop, emergency, fail-safe and ground/overhead tank limit switches, while the output list includes run/stop pilot lights and the starter-control relays. The paper further places this automatic chain alongside a star-delta based pump starter circuit, showing how the sensed water-level states are connected to the actual motor-control hardware.

### 3. 逐句溯源

1. 句子 1：The automatic water-level controller represents the tank level as an eight-step sequence sensed by electrodes `S1` to `S8`, and it updates the plant state as the water rises through successive bands.
   对应摘录：A；`paper_content.txt` 第 303-324 行。
2. 句子 2：The PLC keeps the pump off while the tank is below the activation condition, then treats `S7` as the minimum refill threshold that generates a PLC signal to run the pump, and `S8` as the maximum threshold that commands the PLC to stop the pump.
   对应摘录：A；`paper_content.txt` 第 324-332 行。
3. 句子 3：If the water level later drops below the seventh state again, the controller restarts the pump so that the tank is maintained between the minimum and maximum bands rather than running only once.
   对应摘录：A；`paper_content.txt` 第 332-335 行。
4. 句子 4：The implementation is tied to a Siemens `S7-1200` ladder program whose input list includes system start, stop, emergency, fail-safe and ground/overhead tank limit switches, while the output list includes run/stop pilot lights and the starter-control relays.
   对应摘录：C；`paper_content.txt` 第 365-370 行，396-408 行。
5. 句子 5：The paper further places this automatic chain alongside a star-delta based pump starter circuit, showing how the sensed water-level states are connected to the actual motor-control hardware.
   对应摘录：B, C；`paper_content.txt` 第 340-354 行，365-370 行。

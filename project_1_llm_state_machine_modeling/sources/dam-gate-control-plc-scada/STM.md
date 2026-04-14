# Dams Gate Control Using Programmable Logic Controller and SCADA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了以 `20% / 90%` 液位、模拟浮球量与 `5 s / 10 s` 电机定时驱动为核心的 dam gate 开闭逻辑，可直接作为带工程定时的水工控制样本。

## 条目 1: Reservoir-threshold dual-gate opening and closing controller

- 控制对象：过程与环境控制领域的水坝双闸门液位阈值控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于水位数字传感器、浮球模拟量、PLC、继电器和 SCADA 的 dam gate 控制系统，用分段液位和定时电机动作来决定两扇闸门的开度。
- 判断：算。对象是具体水坝闸门控制器，原文不仅有 flow chart，还有功能块、输入变量、定时器用途和分段开闭策略。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 19-33 行
> This paper is focused on the automation of gates of dam with using the current smart technologies of Programmable Logic Controller (PLC) and SCADA.
>
> The operations of dam gates are based on the feed back signals from the level sensors (Digital Input) and float sensor (Analog Input). The forward and reverse operation of dc motor of gates is achieved with the PLC. Ladder programming is used to implement the whole operations of this system. SCADA is used for remote monitoring.

#### 摘录 B

- 出处：第 4 页，`3.0 Ladder Program Execution`，`paper_content.txt` 第 161-189 行
> Level sensor (20), refers to the water level at 20% of the reservoir.
>
> Level sensor (90), refers to the water level at 90% of the reservoir.
>
> Pulse timer are used for counting the time of the operation of motor for the forward and reverse moment of the gates.
>
> Function block 5 uses a Ladder Logic to take input from the level sensor(90) and uses a timer for gate operation.
>
> Function block 4 uses a Ladder Logic to take input from the level sensor(20) and uses a timer for gate operation.

#### 摘录 C

- 出处：第 4 页，`4.0 Operation`，`paper_content.txt` 第 202-222 行
> When the main switch is turned on, green light is also turned ON to show that the whole system is in operating mode. And hooter is turned ON for 5 sec and after that the sensors give input signal to the PLC.
>
> If the level sensor connected at 90% of the water level gives the input signal to be high than the motor-1 and motor-2 operates in forward direction for 10 sec. Hence, opening the full gates.
>
> If the water level drops to the range of more than 50 but less than 75 than the motor-1 operates for 5 sec in reverse direction. Hence, closing gate-1 to half while gate-2 is completely opened.
>
> If the water level drops to the range of more than 25 but less than 50 than motor-1 operates for 5 sec in reverse direction completely closing gate-1. While motor-2 operates for 5 sec in reverse direction closing gate-2 to half.
>
> If the level sensor connected at 20% of the water level gives the input signal to be high than the motor-2 operates for 5 sec in reverse direction. Hence, closing the gate-2 completely.

#### 摘录 D

- 出处：第 5 页，`4.1 SCADA Display`，`paper_content.txt` 第 224-239 行
> Supervisory control and data acquisition system is used for remote operation of the controlling system of dam gates operations. A Human Machine Interface (HMI) is used to display the status of the water level. The various states of the whole system can be seen in the figure 4.

### 2. 基于原文整理后的自然语言描述

The dam-gate controller combines two digital level sensors, one analog float signal, PLC ladder logic, and SCADA supervision to manage two motorized gates. After the main switch is enabled, the controller enters an operating state, turns the green indicator on, and holds a 5-second hooter delay before accepting sensor-driven gate commands. When the reservoir reaches the 90% threshold, both gate motors run forward for 10 seconds to fully open the two gates; as the level falls, the controller steps through partial-closing regimes, first driving gate 1 backward for 5 seconds to half-close it while gate 2 stays open, then fully closing gate 1 and half-closing gate 2 with another 5-second reverse action. Once the low-level 20% sensor becomes active, the controller drives gate 2 backward for 5 seconds and fully closes the second gate, returning the reservoir to its closed configuration. The logic is therefore an EFSM with explicit timer-controlled actions whose state progression depends jointly on discrete level thresholds and the analog float input.

### 3. 逐句溯源

1. 句子 1：The dam-gate controller combines two digital level sensors, one analog float signal, PLC ladder logic, and SCADA supervision to manage two motorized gates.
   对应摘录：A, B, D
2. 句子 2：After the main switch is enabled, the controller enters an operating state, turns the green indicator on, and holds a 5-second hooter delay before accepting sensor-driven gate commands.
   对应摘录：C
3. 句子 3：When the reservoir reaches the 90% threshold, both gate motors run forward for 10 seconds to fully open the two gates; as the level falls, the controller steps through partial-closing regimes, first driving gate 1 backward for 5 seconds to half-close it while gate 2 stays open, then fully closing gate 1 and half-closing gate 2 with another 5-second reverse action.
   对应摘录：C
4. 句子 4：Once the low-level 20% sensor becomes active, the controller drives gate 2 backward for 5 seconds and fully closes the second gate, returning the reservoir to its closed configuration.
   对应摘录：C
5. 句子 5：The logic is therefore an EFSM with explicit timer-controlled actions whose state progression depends jointly on discrete level thresholds and the analog float input.
   对应摘录：A, B, C

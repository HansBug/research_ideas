# Automatic Car Washing System using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把洗车设备的 `washing -> cleaning -> drying` 顺序、`T1-T4` 计时器、传感器门控和 interlock 全都写成了可直接复用的 PLC 顺序控制链。

## 条目 1: Wash-clean-dry PLC sequence controller

- 控制对象：PLC 自动洗车设备的喷水、刷洗与吹干顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是工业自动化与离散制造领域的 car-wash PLC controller，用于根据 proximity sensor 和定时器顺序驱动 pump、brush、fan 和 main motor 完成洗车流程。
- 判断：算。对象是实际洗车设备顺序控制器，原文明确给出了三阶段流程、进入触发、`T1-T4` 计时器、interlock 和 standby 返回逻辑，不是单纯装置介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`Washing`，`paper_content.txt` 第 84-90 行
> The washing process begins when the Start Proximity Sensor signals the PLC, activating the pump to spray water uniformly over the vehicle ... The process halts automatically once the timer elapses or the Stop Proximity Sensor is triggered.

#### 摘录 B

- 出处：第 4 页，`Cleaning`，`paper_content.txt` 第 98-103 行
> The cleaning process starts immediately after the washing phase. The PLC activates Brush 1 and Brush 2, which rotate in opposite directions ... The cleaning duration is preprogrammed ... Once the cleaning cycle is complete, the brushes automatically stop, transitioning the system to the next phase.

#### 摘录 C

- 出处：第 5-6 页，`Drying / Simulation`，`paper_content.txt` 第 114-116 行、第 120-140 行
> Once the drying timer concludes, the fan and motor shut off automatically, marking the end of the drying phase.
>
> Timer T1 is used to maintain water flow ... Timers T2 and T3 ensure the brushes operate for a specific duration ... Interlocks are implemented to avoid overlapping operations ... Timer T4 controls the fan's operation ... Sensors provide feedback ... before transitioning to standby mode.

### 2. 基于原文整理后的自然语言描述

The car-washing controller executes a fixed three-stage sequence of `Washing -> Cleaning -> Drying` after the start proximity sensor triggers the PLC. In the washing phase, the PLC turns on the pump and keeps spraying until either timer `T1` expires or the stop proximity sensor signals the end of the wetting interval. The cleaning phase starts immediately afterward, energizes `Brush 1` and `Brush 2`, and uses timers `T2` and `T3` together with interlocks to keep the brushing interval bounded and non-overlapping with the previous phase. The drying phase then activates the fan and main motor, runs under timer `T4`, uses sensor feedback to confirm completion, and finally returns the equipment to standby for the next vehicle.

### 3. 逐句溯源

1. 句子 1：The car-washing controller executes a fixed three-stage sequence of `Washing -> Cleaning -> Drying` after the start proximity sensor triggers the PLC.
   对应摘录：A, B
2. 句子 2：In the washing phase, the PLC turns on the pump and keeps spraying until either timer `T1` expires or the stop proximity sensor signals the end of the wetting interval.
   对应摘录：A, C
3. 句子 3：The cleaning phase starts immediately afterward, energizes `Brush 1` and `Brush 2`, and uses timers `T2` and `T3` together with interlocks to keep the brushing interval bounded and non-overlapping with the previous phase.
   对应摘录：B, C
4. 句子 4：The drying phase then activates the fan and main motor, runs under timer `T4`, uses sensor feedback to confirm completion, and finally returns the equipment to standby for the next vehicle.
   对应摘录：C

# Opportunities of Adaptive Control Algorithms Application in Railway Control Systems - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文围绕铁路道口自适应关闭控制给出了传感器、PLC、现有道口设备三部分结构，并明确说明 `D1/D2/D3/D4`、`T1/T2`、速度计算、关闭延迟计算和关闭信号生成，足以形成双 A 级 `EFSM + T1` 样本。

## 条目 1: Speed-Adaptive Railway-Crossing Close-Delay Controller

- 控制对象：轨道交通领域的铁路道口自适应关闭控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用铁路侧传感器测得列车类型与速度，再由 PLC 计算道口关闭延迟并触发现有信号/栏杆设备的自适应道口控制器。
- 判断：算。原文明确给出传感器组合、PLC 程序步骤、定时器、速度与关闭延迟计算，以及最终 `SIGN` 关闭命令，不是泛泛的铁路控制综述。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，`Structure of new system of crossing control and its main blocks`
> The suggested adaptive control system consists of 3 main parts: sensors, a PLC in the crossing relay enclosure, and the existing crossing equipment control system.

#### 摘录 B

- 出处：第 4 页，传感器系统说明
> Sensors D1 and D2 on the railway route obtain a signal from D3 on the train; D4 detects an undefined train, and the crossing is blocked without using the closing time.

#### 摘录 C

- 出处：第 4-5 页，PLC 程序框图与示例运行说明
> The algorithm starts timer T1 at D1, stops T1 at D2, determines train speed, calculates the required closing time, starts timer T2, and generates SIGN to close the crossing.

### 2. 基于原文整理后的自然语言描述

The adaptive railway-crossing controller starts by identifying whether an approaching train should be handled by the adaptive branch. Sensors `D1` and `D2` on the rail receive a signal from train-mounted `D3`, and an auxiliary `D4` branch forces immediate crossing blocking when an undefined train is detected without the expected `D1/D2` evidence. If the adaptive train branch is valid, the PLC starts timer `T1` when `D1` is triggered and stops it when `D2` is triggered, using the known sensor spacing to calculate train speed. The PLC then computes the required movement time to the crossing and derives the close delay `taiztures` from the required warning time. After starting timer `T2`, the controller waits until `T2` reaches the calculated delay and then emits `SIGN` to the existing traffic-light and barrier equipment; after the crossing-passed signal is received, it clears the parameters and returns to the next detection cycle.

### 3. 逐句溯源

1. 句子 1：The adaptive railway-crossing controller starts by identifying whether an approaching train should be handled by the adaptive branch.
   对应摘录：B, C
2. 句子 2：Sensors `D1` and `D2` on the rail receive a signal from train-mounted `D3`, and an auxiliary `D4` branch forces immediate crossing blocking when an undefined train is detected without the expected `D1/D2` evidence.
   对应摘录：B
3. 句子 3：If the adaptive train branch is valid, the PLC starts timer `T1` when `D1` is triggered and stops it when `D2` is triggered, using the known sensor spacing to calculate train speed.
   对应摘录：C
4. 句子 4：The PLC then computes the required movement time to the crossing and derives the close delay `taiztures` from the required warning time.
   对应摘录：C
5. 句子 5：After starting timer `T2`, the controller waits until `T2` reaches the calculated delay and then emits `SIGN` to the existing traffic-light and barrier equipment; after the crossing-passed signal is received, it clears the parameters and returns to the next detection cycle.
   对应摘录：A, C

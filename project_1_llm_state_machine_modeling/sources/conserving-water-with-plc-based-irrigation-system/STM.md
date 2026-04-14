# Conserving Water with A PLC Based Irrigation System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把田间水位传感器、蓄水池传感器、`START/STOP`、`Q1/Q2/Q3/Q5`、水源切换和 `T0` 延迟都写进 PLC 梯形图说明，能形成完整的双水源灌溉 EFSM。

## 条目 1: Dual-Source Irrigation and Reservoir Refill Supervisor

- 控制对象：过程与环境控制领域的 PLC 自动灌溉与双水源切换控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 PLC 按田间水位需求启停灌溉，并在蓄水池低水位时切换到第二水源和补水泵的自动灌溉控制器。
- 判断：算。原文有系统框图、梯形图解释、输入输出线圈、定时器和仿真/原型验证，不是只停留在“智能灌溉”概念层。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`System Block Diagram / Theory of Operation`
> Water level sensors `S1-S4` feed the PLC; under normal conditions the PLC drives water from the overhead reservoir and enables solenoids 1-3.

#### 摘录 B

- 出处：第 2 页，`Theory of Operation`
> If the reservoir goes below the predetermined level, the PLC disables solenoid 3 and switches control to water source 2 by turning on the pump.

#### 摘录 C

- 出处：第 5-6 页，`Ladder diagram implementation`
> With `START` on and any sensor low, latch relay `Q1` is latched; reservoir sensor `I5` controls timer `T0`; reservoir solenoid `Q2` turns on after a specified delay, and pump `Q3` is turned on when reservoir level is low.

### 2. 基于原文整理后的自然语言描述

The PLC irrigation controller is enabled by the `START` switch and disabled by the `STOP` switch, so the controller stays off during maintenance or non-operation. Once enabled, field sensors `S1-S4` are combined through OR-style ladder logic; if any field sensor indicates water demand, latch relay `Q1` is set and the controller proceeds to choose a water source. Under normal reservoir conditions, the controller opens the reservoir path by energizing the relevant solenoid outputs and supplies the fields from water source 1. If the overhead reservoir sensor indicates low level, input `I5` drives timer `T0`, reservoir solenoid `Q2` turns on after the configured delay, pump `Q3` starts, and control transfers to water source 2 to refill or supply the system. Field solenoids are then controlled by field demand sensors and latch coils, while the pump status is exposed through `Q5`; when no water demand remains, the solenoids and pump outputs are turned off to save power.

### 3. 逐句溯源

1. 句子 1：The PLC irrigation controller is enabled by the `START` switch and disabled by the `STOP` switch, so the controller stays off during maintenance or non-operation.
   对应摘录：C
2. 句子 2：Once enabled, field sensors `S1-S4` are combined through OR-style ladder logic; if any field sensor indicates water demand, latch relay `Q1` is set and the controller proceeds to choose a water source.
   对应摘录：A, C
3. 句子 3：Under normal reservoir conditions, the controller opens the reservoir path by energizing the relevant solenoid outputs and supplies the fields from water source 1.
   对应摘录：A
4. 句子 4：If the overhead reservoir sensor indicates low level, input `I5` drives timer `T0`, reservoir solenoid `Q2` turns on after the configured delay, pump `Q3` starts, and control transfers to water source 2 to refill or supply the system.
   对应摘录：B, C
5. 句子 5：Field solenoids are then controlled by field demand sensors and latch coils, while the pump status is exposed through `Q5`; when no water demand remains, the solenoids and pump outputs are turned off to save power.
   对应摘录：C

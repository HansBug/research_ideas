# PLC Based Automated Irrigation System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `moist sensor -> master valve / zonal valve / pump` 的映射表和五种开阀规则，能直接形成分区灌溉状态机样本。

## 条目 1: Moisture-threshold zone-valve irrigation controller

- 控制对象：环境与过程控制领域的分区灌溉阀门与水泵控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `SIEMENS LOGO 230 RC` 的自动灌溉控制器，用四路湿度传感器控制总阀、四个分区阀和水泵的启停。
- 判断：算。对象是实际灌溉控制系统，原文给出了输入输出表、湿度阈值以及每个传感器触发对应阀门动作的规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，`Results and Discussion`，`paper_content.txt` 第 129-145 行
> I have programmed this controller so that it controls the opening and closing of the master valve and zonal valve of the irrigation system. And also controls the ON and OFF position of the water pump automatically. I have set the value of moisture sensor manually as 22 to Turn ON and 55 to Turn OFF. ... The input, output coil descriptions are shown in table 1. I1 Moist sensor 1 ... I4 Moist sensor 4 ... Q1 Motor ... Q2 Master valve ... Q3 Zonal valve 1 ... Q6 Zonal valve 4.

#### 摘录 B

- 出处：第 6-7 页，`Circuit Diagram`，`paper_content.txt` 第 156-176 行
> 1) when moisture sensor 1 is initiated, master valve and zonal valve 1 gets open
>
> 2) When moisture sensor 2 is initiated, master valve and zonal valve 2 gets open
>
> 3) When moisture sensor 3 is initiated, master valve and zonal valve 3 gets open
>
> 4) When moisture sensor 4 is initiated, master valve and zonal valve 4 gets open
>
> 5) When all moisture sensors are initiated all zonal and master valves gets open

### 2. 基于原文整理后的自然语言描述

The irrigation controller monitors four soil-moisture inputs and compares them against fixed thresholds, using 22 as the turn-on point and 55 as the turn-off point for watering decisions. When a zone sensor indicates that watering is required, the PLC opens the shared master valve and the zonal valve that corresponds to that sensor. At the same time, the controller manages the water-pump motor so the hydraulic path is active only when irrigation is being executed. If multiple dry zones are requested together, the PLC keeps the master valve open and can activate all of the relevant zonal valves; in the full-demand case, all four zonal valves are opened together with the master valve.

### 3. 逐句溯源

1. 句子 1：The irrigation controller monitors four soil-moisture inputs and compares them against fixed thresholds, using 22 as the turn-on point and 55 as the turn-off point for watering decisions.
   对应摘录：A
2. 句子 2：When a zone sensor indicates that watering is required, the PLC opens the shared master valve and the zonal valve that corresponds to that sensor.
   对应摘录：A, B
3. 句子 3：At the same time, the controller manages the water-pump motor so the hydraulic path is active only when irrigation is being executed.
   对应摘录：A
4. 句子 4：If multiple dry zones are requested together, the PLC keeps the master valve open and can activate all of the relevant zonal valves; in the full-demand case, all four zonal valves are opened together with the master valve.
   对应摘录：B

# Automatic irrigation system using PLC - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文在摘要里明确写出了湿度阈值、分区阀门和 PLC 反馈控制关系，但正文提取质量一般，适合作为简洁阈值控制样本。

## 条目 1: Humidity-Regulated Irrigation Valve Control
- 控制对象：PLC 滴灌系统的土壤湿度与阀门控制逻辑

### 0. 条目识别与判定
- 一句话说明：这是农业环境控制领域的 PLC 灌溉控制器，用于根据田间湿度的最小/最大阈值控制各分区阀门并维持土壤含水水平。
- 判断：算。对象是实际灌溉控制系统，原文明确给出了 humidity sensing、separate valve、PLC control 和 feedback regulation。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 18-28
> irrigation may be defined as the process of artificially supplying water to soil for raising crops. ... The field humidity is prime parameter considered for plantation of different plants. It is controlled by sensors, for minimum and maximum humidity. The field is irrigated by a separate valve. The valves are controlled by the PLC. Through feedback control mechanism, humidity of the fields is maintained at the certain level. In PLC based drip irrigation system we control the percentage of moisture in the soil. The developed irrigation system removes the need for workmanship for flooding irrigation.

### 2. 基于原文整理后的自然语言描述

The PLC-based drip-irrigation controller uses field-humidity sensing as the primary condition for watering different plants. Separate valves are assigned to the fields, and these valves are controlled by the PLC according to minimum and maximum humidity conditions. Through feedback control, the system maintains the soil-moisture level at the required value instead of relying on manual flooding irrigation.

### 3. 逐句溯源

1. 句子 1：The PLC-based drip-irrigation controller uses field-humidity sensing as the primary condition for watering different plants.
   对应摘录：A
2. 句子 2：Separate valves are assigned to the fields, and these valves are controlled by the PLC according to minimum and maximum humidity conditions.
   对应摘录：A
3. 句子 3：Through feedback control, the system maintains the soil-moisture level at the required value instead of relying on manual flooding irrigation.
   对应摘录：A

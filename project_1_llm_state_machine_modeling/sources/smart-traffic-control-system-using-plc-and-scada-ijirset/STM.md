# SMART TRAFFIC CONTROL SYSTEM USING PLC and SCADA - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文给出了基于重量与拥堵计数的交通放行/限行逻辑，但很多细节依赖流程图，正文可提取度中等。

## 条目 1: Weight-Based Diversion and Congestion Gating
- 控制对象：道路交通分流与拥堵放行控制器

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的 PLC 交通分流控制器，用于按车辆重量和路段拥堵状态决定是否允许车辆进入目标路段。
- 判断：算。对象是实际交通控制系统，原文给出了传感器输入、计数条件和红黄绿放行规则，能够整理成离散控制逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section B/Congestion Control，`paper_content.txt` 第 58-59 行
> Weight sensor is placed at toll booth. It sens es the weight & sends signal to PLC. PLC will generate a slip having the info about the vehicle in the form of barcode. PLC will give the diversion according to the weight of the vehicle.

#### 摘录 B
- 出处：第 2 页，Section B/Congestion Control，`paper_content.txt` 第 64-74 行
> In this there are two counters – UP Counter (at the starting of the road) & DOWN Counter (at the end of the road) whose max value is 100. When a vehicle enters the road, UP Counter is set and vice versa. There are 3 conditions for allowing the vehicle in the area ... If UP Counter==100 & DOWN Counter==0, then red light will be shown i.e. no vehicle will be allowed to enter the area. If 100>UP Counter>80 & 20>Down Counter>0, then yellow light will be shown i.e. vehicles will be told to be ready to enter the area. If UP Counter<60 & DOWN Counter>40, then green light will be shown i.e. vehicles will be allowed to enter the area.

### 2. 基于原文整理后的自然语言描述

The PLC-based traffic diversion controller classifies vehicles at the toll booth by weight and issues diversion information accordingly. For the congestion-controlled road segment, the controller maintains an UP counter at the road entrance and a DOWN counter at the road exit to estimate occupancy. It blocks new entries with a red signal when the segment is full, switches to yellow when vehicles should prepare to enter, and allows entry with a green signal when the downstream side is sufficiently clear.

### 3. 逐句溯源

1. 句子 1：The PLC-based traffic diversion controller classifies vehicles at the toll booth by weight and issues diversion information accordingly.
   对应摘录：A
2. 句子 2：For the congestion-controlled road segment, the controller maintains an UP counter at the road entrance and a DOWN counter at the road exit to estimate occupancy.
   对应摘录：B
3. 句子 3：It blocks new entries with a red signal when the segment is full, switches to yellow when vehicles should prepare to enter, and allows entry with a green signal when the downstream side is sufficiently clear.
   对应摘录：B

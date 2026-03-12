# Automatic Bottle Filling System Using PLC/SCADA - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接给出了 IR 检测、超声液位检测、停带、泵灌装和恢复输送的顺序控制链路。

## 条目 1: IR-and-Ultrasonic Bottle Filling Loop
- 控制对象：PLC/SCADA 自动瓶装灌装产线

### 0. 条目识别与判定
- 一句话说明：这是工业灌装领域的自动瓶装控制器，用于检测瓶子到位、监测液位并控制水泵和输送带完成灌装循环。
- 判断：算。对象是实际瓶装灌装系统，原文明确写出了 IR sensor、ultrasonic sensor、pump 和 conveyor 的动作顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Introduction，行 58-69
> The proposed system uses a Siemens S7-1200 PLC programmed using TIA Portal V16, enabling precise control over the sequence of operations. An IR sensor is used to detect the presence of a bottle on the conveyor, while an ultrasonic sensor monitors the liquid level inside the bottle. Once the bottle is in position, the conveyor halts, and a mini water pump is activated to fill the bottle. After reaching the desired level, the pump stops, and the conveyor resumes, moving the filled bottle forward.

### 2. 基于原文整理后的自然语言描述

The PLC bottle-filling controller uses an IR sensor to detect the presence of a bottle on the conveyor and an ultrasonic sensor to monitor the liquid level during filling. When the bottle reaches the filling position, the conveyor halts and the mini water pump is activated. After the desired liquid level is reached, the pump stops and the conveyor resumes to move the filled bottle forward.

### 3. 逐句溯源

1. 句子 1：The PLC bottle-filling controller uses an IR sensor to detect the presence of a bottle on the conveyor and an ultrasonic sensor to monitor the liquid level during filling.
   对应摘录：A
2. 句子 2：When the bottle reaches the filling position, the conveyor halts and the mini water pump is activated.
   对应摘录：A
3. 句子 3：After the desired liquid level is reached, the pump stops and the conveyor resumes to move the filled bottle forward.
   对应摘录：A

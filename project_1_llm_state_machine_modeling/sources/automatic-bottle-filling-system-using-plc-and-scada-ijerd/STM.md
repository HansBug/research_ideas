# Automatic Bottle Filling System Using PLC and SCADA - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文用一句完整的运行说明串起了输送、瓶检测、停带、开阀、10 秒灌装和恢复输送的全过程，适合作为短流程控制样本。

## 条目 1: Proximity-Triggered Timed Filling Sequence
- 控制对象：带输送带的自动瓶装灌装控制系统

### 0. 条目识别与判定
- 一句话说明：这是工业灌装领域的 PLC 控制器，用于在瓶子到达传感器附近时暂停输送、定时灌装并在定时结束后恢复输送。
- 判断：算。对象是实际瓶装灌装系统，原文直接给出了 proximity switch、motor stop、valve open、10-second pause 和 restart 的顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Methodology，行 148-152
> When motor is started using normally open (NO) push button the conveyor starts. The bottle placed over the conveyor starts to move. When the bottle (metal body) reaches near the vicinity of the proximity switch it detects the metal body and the motor stops and simultaneously the valve opens for water filling. The system pauses for 10 seconds. After 10 seconds the motor again starts to move and the valve closes. The system stops using the normally close (NC) button.

### 2. 基于原文整理后的自然语言描述

When the operator starts the system with the normally open push button, the conveyor begins moving the bottle forward. As soon as the bottle reaches the proximity switch, the PLC stops the motor and opens the filling valve so that water filling can proceed. The system maintains this filling state for ten seconds, and then the motor starts again while the valve closes and the bottle is moved onward.

### 3. 逐句溯源

1. 句子 1：When the operator starts the system with the normally open push button, the conveyor begins moving the bottle forward.
   对应摘录：A
2. 句子 2：As soon as the bottle reaches the proximity switch, the PLC stops the motor and opens the filling valve so that water filling can proceed.
   对应摘录：A
3. 句子 3：The system maintains this filling state for ten seconds, and then the motor starts again while the valve closes and the bottle is moved onward.
   对应摘录：A

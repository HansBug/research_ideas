# Design and Implementation of Automatic Bottle Filling System Using PLC and SCADA - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文对瓶到位检测、停带、开阀灌装、按液位或重量关阀、延时后重新启带的流程描述非常完整。

## 条目 1: Photoelectric Detection and Valve-Controlled Filling Cycle
- 控制对象：瓶装液体灌装站的 PLC 与 SCADA 控制系统

### 0. 条目识别与判定
- 一句话说明：这是工业灌装领域的瓶装灌装控制器，用于检测瓶子到达灌装工位、停止输送带、打开电磁阀灌装并在达到目标后恢复输送。
- 判断：算。对象是实际灌装控制系统，原文给出了 photoelectric sensor、conveyor stop/run、electrovalve open/close 和 filling completion 的明确顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 31 页，Bottle Detection Mechanism / Liquid Flow Control Mechanism，行 743-755
> The task of bottle detection is performed using a photoelectric sensor. A photoelectric sensor is placed on the side of the conveyor belt at the filling station to detect the presence of a bottle. ... when a bottle is brought in front of the sensor by the conveyor belt ... the PLC will give command to the conveyor motor to run or to stop. When the bottle is detected by the photoelectric sensor, the task of filling the bottle with liquid starts. An electro valve is used to control the flow of liquid from overhead tank to the bottle. The electrovalve is positioned at the filling station. When a bottle stops underneath the valve, it gets a command from the PLC to open the valve and liquid flows from the overhead tank to the bottle up to a particular level.

#### 摘录 B
- 出处：第 66-67 页，Flow Chart for Bottle Sensing and Filling System，行 1821-1842
> Figure 4.11 shows the flow chart of the bottle sensing and filling system. When the system is powered on, the conveyor belt starts running. The conveyor belt keeps running if the photoelectric sensor does not detect the presence of any bottle in front of it. If the sensor detects any bottle then the conveyor belt stops, Electro valve opens and bottle filling starts, the amount of liquid filling is controlled using a weighting sensor. ... the opening of the valve is decided. The Electro valve then closes and after some time delay conveyor belt starts again with the filled bottle and carries the bottle to the other end where the bottle is collected.

### 2. 基于原文整理后的自然语言描述

When the bottle-filling system is powered on, the conveyor keeps running until the photoelectric sensor detects a bottle at the filling station. Once a bottle is detected, the PLC stops the conveyor, opens the electrovalve, and starts filling the bottle from the overhead tank. After the target amount is reached, the valve is closed, and after a short delay the conveyor starts again and carries the filled bottle to the collection end.

### 3. 逐句溯源

1. 句子 1：When the bottle-filling system is powered on, the conveyor keeps running until the photoelectric sensor detects a bottle at the filling station.
   对应摘录：A, B
2. 句子 2：Once a bottle is detected, the PLC stops the conveyor, opens the electrovalve, and starts filling the bottle from the overhead tank.
   对应摘录：A, B
3. 句子 3：After the target amount is reached, the valve is closed, and after a short delay the conveyor starts again and carries the filled bottle to the collection end.
   对应摘录：B

# Monitoring and Controlling of Components in a Conveyor using PLC and SCADA - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接描述了三段输送带在对象检测后启动、延时停机以及第三段在累计 5 个对象后启动的顺序控制逻辑。

## 条目 1: Multi-Conveyor Detection and Delayed Transfer Logic
- 控制对象：离散制造场景下的三段输送带 PLC 控制系统

### 0. 条目识别与判定
- 一句话说明：这是工业自动化领域的输送带控制器，用于检测部件到位、控制各段输送带启停，并在累计到一定数量后触发后续输送。
- 判断：算。对象是实际输送控制系统，原文给出了每段输送带的传感检测、延时停机和计数触发规则。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 12-19
> The main objective of the project is to Monitor and Control the Components that is being carried over the Belt Conveyers using PLC, SCADA. The conveyor is operated by DC motor. The components in the conveyor are detected by using sensors. The Conveyer is controlled through the PLC Programming for its Control process, monitoring of how many Completed Components passed through the conveyer at a specified time along with Power reduction using Energy Efficient PLC Programming.

#### 摘录 B
- 出处：第 3 页，Conclusion，行 268-279
> The project is based on the controlling of components by using PLC. In this there are three conveyors which are controlled by dc motor each conveyor has a proximity sensor. So that the object through the conveyor is observed. The conveyor running is started only when the object is detected in the proximity sensor and the conveyor is offed after certain seconds of the object detected. The process is the same for each conveyor and in the third conveyor the running starts after five objects are collected.

### 2. 基于原文整理后的自然语言描述

The conveyor-control system uses PLC logic and sensors to monitor the components transported on DC-motor-driven belts. Each conveyor segment starts running only after its proximity sensor detects an object, and the segment is turned off after a certain number of seconds following detection. The same sequence is applied to all three conveyors, except that the third conveyor starts only after five objects have been collected.

### 3. 逐句溯源

1. 句子 1：The conveyor-control system uses PLC logic and sensors to monitor the components transported on DC-motor-driven belts.
   对应摘录：A, B
2. 句子 2：Each conveyor segment starts running only after its proximity sensor detects an object, and the segment is turned off after a certain number of seconds following detection.
   对应摘录：B
3. 句子 3：The same sequence is applied to all three conveyors, except that the third conveyor starts only after five objects have been collected.
   对应摘录：B

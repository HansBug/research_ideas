# PLC BASED RAILWAY LEVEL CROSSING GATE CONTROL - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（普通离散状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接写出了列车到达检测、PLC 接收传感器信号后驱动步进电机顺逆时针动作的门控序列，可直接转成控制逻辑样本。

## 条目 1: Vibration-Sensed Gate Open-Close Sequence
- 控制对象：铁路平交口的 PLC 道口栏杆控制器
- 状态机类型：FSM（普通离散状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是轨道交通领域的道口门控控制器，用于在列车到达时自动关闭栏杆、在列车离开后重新打开栏杆。
- 判断：算。对象是实际铁路道口控制系统，原文给出了 arrival sensor、departure sensor 与步进电机动作方向之间的明确关系。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Introduction，行 15-22
> By employing the automatic railway gate control at the level crossing the arrival of the train is detected by the sensors placed in the side of the tracks. Hence, the time for which it is closed is less compared to the manually operated gates. The operation is automatic so error due to manual operation is prevented.

#### 摘录 B
- 出处：第 1-3 页，Accident Avoidence Details / Sensor Distance Calculation，行 43-58, 146-157
> controls the operation of the gate. When the wheels of the train moves over the track there will be creation of vibration the sensor-1 senses the vibration and sends the signal to PLC to indicate train arrival. ... PLC produces an output signal to the stepper motor to rotate in clockwise direction. When the output is from sensor-2 is sent to PLC it sends another signal to stepper motor to rotate in anti-clock wise direction. ... Here the distance of sensors from the gate is taken as 2KM ... At maximum speed total time of execution: 1 min 30 sec, at average speed total time of execution: 3 min, at minimum speed total time of execution: 6 min.

### 2. 基于原文整理后的自然语言描述

The PLC railway-gate controller places vibration sensors beside the track, with the design calculation taking the sensing position about 2 km from the gate so that the controller has enough time to react at different train speeds. When the train wheels create vibration at sensor 1, the PLC interprets it as train arrival and drives the stepper motor clockwise to close the crossing gate. When sensor 2 reports the departing train, the PLC sends the reverse command so that the stepper motor rotates anti-clockwise and reopens the gate. The resulting execution window is sized for about 1 min 30 s at maximum speed, 3 min at average speed, and 6 min at minimum speed.

### 3. 逐句溯源

1. 句子 1：The PLC railway-gate controller places vibration sensors beside the track, with the design calculation taking the sensing position about 2 km from the gate so that the controller has enough time to react at different train speeds.
   对应摘录：A, B
2. 句子 2：When the train wheels create vibration at sensor 1, the PLC interprets it as train arrival and drives the stepper motor clockwise to close the crossing gate.
   对应摘录：B
3. 句子 3：When sensor 2 reports the departing train, the PLC sends the reverse command so that the stepper motor rotates anti-clockwise and reopens the gate.
   对应摘录：B
4. 句子 4：The resulting execution window is sized for about 1 min 30 s at maximum speed, 3 min at average speed, and 6 min at minimum speed.
   对应摘录：B

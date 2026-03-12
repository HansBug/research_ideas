# AUTOMATIC RAILWAY GATE CROSSING CONTROL USING PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文对列车接近、报警、落杆、通过后复位的顺序描述非常直接，适合直接作为道口门控样本。

## 条目 1: Sensor-Triggered Gate Closing and Reopening
- 控制对象：铁路平交口自动栏杆门控系统

### 0. 条目识别与判定

- 一句话说明：这是铁路道口控制领域的 PLC 门控系统，用于根据列车接近和离开传感器控制报警、栏杆关闭与复位。
- 判断：算。对象是实际铁路平交口门控系统，原文明确给出了到达侧传感、离开侧传感以及栏杆动作顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Introduction，`paper_content.txt` 第 47-64 行
> In this project detect the train and warn the road users about the arrival of train. ... After they are cleared, the gate is closed and train is passed. We will make sure that the train is passed and reopen the gate. ... In this system whole operation is based on the sensor and their input to the PLC which sends the signal to open or close operation of the railway gate operating DC motor.

#### 摘录 B
- 出处：第 1-2 页，Working，`paper_content.txt` 第 82-95 行
> When any train is coming from any one side than the sensor situated on that track gets high and a high signal is generated from the sensor by which the PLC generate a beep sound for a while and close the barriers for the traffic and the traffic signal gets amber by which the train can cross the gate easily. And when the train passes out from the crossing than the end side sensor which is sensor2 gets high and give a signal to PLC by which the PLC opens the barriers and the signals comes in its normal positions (off position).

### 2. 基于原文整理后的自然语言描述

The railway gate controller detects an approaching train with a track-side sensor and warns road users before closing the barriers. After the arrival-side sensor is triggered, the PLC generates a beep, drives the barriers closed, and changes the indication so the train can pass safely through the crossing. When the train clears the crossing and the exit-side sensor is activated, the PLC reopens the barriers and returns the signals to their normal position.

### 3. 逐句溯源

1. 句子 1：The railway gate controller detects an approaching train with a track-side sensor and warns road users before closing the barriers.
   对应摘录：A, B
2. 句子 2：After the arrival-side sensor is triggered, the PLC generates a beep, drives the barriers closed, and changes the indication so the train can pass safely through the crossing.
   对应摘录：B
3. 句子 3：When the train clears the crossing and the exit-side sensor is activated, the PLC reopens the barriers and returns the signals to their normal position.
   对应摘录：B

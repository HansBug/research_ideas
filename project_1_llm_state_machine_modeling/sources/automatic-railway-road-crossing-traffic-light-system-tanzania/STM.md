# Automatic Railway Road Crossing (RLC) Traffic Light System for Metric Gauge Railway Network in Tanzania - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路道口的 `RFID + ultrasonic` 检测、栏杆闭合、告警维持、障碍监测、按车速确定闭合时间与 `30 seconds` 预警窗口写成完整门控监督链，可稳定形成双 A 样本。

## 条目 1: RFID-Ultrasonic Railway Crossing Supervisor

- 控制对象：轨道交通与铁路控制领域的道口 `RFID / ultrasonic` 栏杆门控与交通灯监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向坦桑尼亚米轨铁路道口的自动门控系统，用 `RFID strike-in / strike-out` 检测列车到离、用超声波检测滞留车辆，并根据车速、ETA、栏杆、闪灯和蜂鸣器联动控制道口状态。
- 判断：算。对象是实际铁路平交道口门控系统，原文明确给出 approaching / activated / obstacle-detection / barrier-close / pass / reopen 的事件链，以及 `30` 秒预警窗口和车速决定闭门时间的条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 20-30 行
> The aim is to develop an automated railway level crossing system that would reduce the likelihood of collisions between trains and road users at intersections. ... Two RFID sensors and Ultrasonic sensors are used located at strike-in and strike-out points at the level crossing. Detection of automobiles stuck on the railroad once the train has activated the automation at the RLC is performed by the Ultrasonic sensor. Other warning measures in the system include an automated barrier, Light Emitting Diode flashing lights, and an audio alarm device. ... Consequently, the next train station from RLC was updated of the incoming train’s Expected Time of Arrival (ETA). The time it takes for the barriers to close will be determined by the train’s speed.

#### 摘录 B

- 出处：第 4-5 页，`3.3.2 Hardware tools used / Figure 5`，`paper_content.txt` 第 156-160、170-178、183-189、229-236 行
> Arduino UNO micro-controller is used to screen the status of all the level crossing related devices such as RFID reader, flashing lights and mechanical barriers triggering, audible alarm activation, and also manual control of gate mechanism in case of emergency.
>
> The RFID system functions by detecting the presence of an approaching train from either direction of the RLC. ... The microcontrollers generate signal controls ...
>
> The ultrasonic sensor has the same task as the RFID technology but as a backup ... the ultrasonic sensors are used for the obstacle detection at the level crossing protection systems and control.
>
> Figure 5: Design of an Automatic RLC
> Figure 6: The flow of events and controls for the RLC system designed

#### 摘录 C

- 出处：第 7 页，`4. Discussion and Results`，`paper_content.txt` 第 255-261 行
> This system will assist automobile drivers and pedestrians in recognizing an oncoming train, and the gate will automatically close or open the road barriers to allow the train to pass without colliding with the vehicles. RFID MFRC522 reader sensor and RFID tags attached to the rail side and the train carriage are used for train detection to activate and deactivate the level-crossing system. The ultrasonic sensors are used for the obstacle detection at the level crossing protection systems and control. Furthermore, regardless of the speed the train is operating on the track, the circuits controlling the automatic warning devices provide a minimum operation of 30 seconds before the train arrive at the level crossing. Basically, this automatic railway level crossing system consists of 4 main parts; sensing, transmitting, processing and controlling.

### 2. 基于原文整理后的自然语言描述

The proposed railway-crossing controller is a supervisory EFSM for a real level crossing, not just a gate motor demo, and it combines train-side `RFID` strike-in/strike-out detection with ultrasonic obstacle sensing at the crossing itself. When an approaching train is detected, the microcontroller activates the warning outputs, computes barrier-closing behavior from the train speed, updates the next station with the expected arrival time, and drives the automated barrier into the protective state. During activation, the ultrasonic subsystem acts as a backup detector and checks whether an automobile is still stuck on the crossing before or while the barrier is closing. The warning circuit is guaranteed to run for at least `30` seconds before the train reaches the crossing, and after the train has passed the level-crossing system is deactivated so the barriers reopen and road traffic resumes.

### 3. 逐句溯源

1. 句子 1：The proposed railway-crossing controller is a supervisory EFSM for a real level crossing, not just a gate motor demo, and it combines train-side `RFID` strike-in/strike-out detection with ultrasonic obstacle sensing at the crossing itself.
   对应摘录：A, B
2. 句子 2：When an approaching train is detected, the microcontroller activates the warning outputs, computes barrier-closing behavior from the train speed, updates the next station with the expected arrival time, and drives the automated barrier into the protective state.
   对应摘录：A, B
3. 句子 3：During activation, the ultrasonic subsystem acts as a backup detector and checks whether an automobile is still stuck on the crossing before or while the barrier is closing.
   对应摘录：A, B, C
4. 句子 4：The warning circuit is guaranteed to run for at least `30` seconds before the train reaches the crossing, and after the train has passed the level-crossing system is deactivated so the barriers reopen and road traffic resumes.
   对应摘录：C

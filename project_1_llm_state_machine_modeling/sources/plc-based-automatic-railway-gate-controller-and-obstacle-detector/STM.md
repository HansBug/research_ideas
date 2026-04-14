# PLC BASED AUTOMATIC RAILWAY GATE CONTROLLER AND OBSTACLE DETECTOR - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把道口门控、障碍停障、位置开闭逻辑和 PLC I/O 都写得较完整，既有主顺序链，也有障碍分支与“after some delay”时间语义，可直接作为铁路门控双 A 样本。

## 条目 1: Sensor-Gated Railway Crossing Closure with Obstacle Stop
- 控制对象：铁路平交口的 PLC 栏杆与障碍停障控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是轨道交通与铁路控制领域的铁路道口门控控制器，利用列车位置开关、障碍检测开关、继电器和电机，完成接近关闸、障碍停障、离开延时开闸的完整安全链。
- 判断：算。对象是实际铁路平交口控制系统，原文直接给出列车接近检测、障碍检测、门机开闭、列车停止/继续运行和具体 I/O 地址，不是泛化的硬件介绍。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，`Introduction / Abstract`，`paper_content.txt` 第 20-24 行、第 41-50 行
> the automatic railway gate control at the railway crossing the arrival of the train is detected by the sensing element placed on the track at a precise distance from the gate. This sensing element detects the approaching train and consequently controls the operation of the gate. When the wheels of the train moving over the track there will be position switch and it will send the signal to PLC to indicate train arrival.
>
> In this work, an automatic railway crossing gate control system has been developed using a Programmable Logic Controller (PLC). ... Signaling light models are implemented using several red, green and yellow Light Emitting Diodes (LEDs); and railway gates are opened using DC motors with gear trains that are connected to the output ports of the PLC.

#### 摘录 B
- 出处：第 3 页，`Figure 2 shows the flowchart ...`，`paper_content.txt` 第 114-123 行
> train position sensors are used on either end of the railway crossing to sense the position of the train and gives appropriate output to PLC. The obstacle detector senses any obstacle present on the level crossing and gives the signal to PLC. If any obstacle is present on the track then PLC will send stop command to geared DC motors which are used as wheels of the train ... Once the obstacle is removed from the track then PLC will send run command to geared DC motors.
>
> If the train is closer to the level crossing, PLC activates its output and sends the close command through a relay to DC motors which are coupled to the railway gate assembly. ... Once the train crosses the leveler, PLC activates its output to open the gate automatically after some delay.

#### 摘录 C
- 出处：第 3-4 页，`Hardware specifications / Table-2 PLC Input and Output Addresses`，`paper_content.txt` 第 153-159 行、第 175-193 行
> Limit switches are used to detect the obstacle and position of the train. ... When there’s an obstacle on track, the limit switch gets pressed and PLC receives the input signal. ... When the train reaches at position switch 5, the switch gets pressed. The signal goes to the PLC and according to the PLC programming gates closed. When the train reaches at position switch 1, the switch gets pressed, in step with the PLC programming gates opened.
>
> Train Motor (Forward) O:0/1 ... Train Motor (Reverse) O:0/2 ... Gate Assembly Motor (Closing) O:0/3 ... Gate Assembly Motor (Opening) O:0/4

### 2. 基于原文整理后的自然语言描述

The railway-crossing controller is a PLC-based EFSM that uses train-position switches at both sides of the crossing together with obstacle-detection switches to supervise gate closure, reopening, and train movement. When an approaching train triggers the arrival-side position switch, the PLC drives the warning lights, energizes the gate-closing motor through relays, and closes the barrier automatically. While the crossing is occupied, the obstacle detector remains active, and if an obstacle is found on the track the PLC sends a stop command to the train motor; once the obstacle is removed, the PLC issues the run command again. The paper also maps this logic to explicit I/O addresses, including gate closing on `O:0/3`, gate opening on `O:0/4`, and train motor control on `O:0/1` and `O:0/2`. After the train reaches the departure-side position switch, the controller reopens the gate after a delay, so the overall cycle is an approach-close-protect-reopen sequence with an explicit safety branch for obstacle handling.

### 3. 逐句溯源

1. 句子 1：The railway-crossing controller is a PLC-based EFSM that uses train-position switches at both sides of the crossing together with obstacle-detection switches to supervise gate closure, reopening, and train movement.
   对应摘录：A, B, C
2. 句子 2：When an approaching train triggers the arrival-side position switch, the PLC drives the warning lights, energizes the gate-closing motor through relays, and closes the barrier automatically.
   对应摘录：A, B
3. 句子 3：While the crossing is occupied, the obstacle detector remains active, and if an obstacle is found on the track the PLC sends a stop command to the train motor; once the obstacle is removed, the PLC issues the run command again.
   对应摘录：B, C
4. 句子 4：The paper also maps this logic to explicit I/O addresses, including gate closing on `O:0/3`, gate opening on `O:0/4`, and train motor control on `O:0/1` and `O:0/2`.
   对应摘录：C
5. 句子 5：After the train reaches the departure-side position switch, the controller reopens the gate after a delay, so the overall cycle is an approach-close-protect-reopen sequence with an explicit safety branch for obstacle handling.
   对应摘录：B, C

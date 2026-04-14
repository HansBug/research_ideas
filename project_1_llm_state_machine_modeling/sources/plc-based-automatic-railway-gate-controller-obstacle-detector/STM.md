# PLC Based Automatic Railway Gate Controller and Obstacle Detector - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把列车接近、障碍检测、停障、落杆、通过后开杆以及 I/O 地址都写得较细，能形成双 A 的铁路道口门控样本。

## 条目 1: Sensor-and-Obstacle Governed Gate Cycle
- 控制对象：轨道交通与铁路控制领域的 PLC 道口栏杆与障碍检测控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个铁路平交口 PLC 控制系统，使用列车位置限位开关和障碍检测开关来同时控制列车运行、道口栏杆关闭/开启以及电机正反转。
- 判断：算。对象是实际铁路道口控制子系统，不是单纯硬件实验流程；原文直接给出了事件链、限位开关位置、延迟开杆和 PLC 输入输出地址。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，`Figure 2 shows the flowchart...`，`paper_content.txt` 第 114-123 行
> train position sensors are used on either end of the railway crossing to sense the position of the train and gives appropriate output to PLC. The obstacle detector senses any obstacle present on the level crossing and gives the signal to PLC. If any obstacle is present on the track then PLC will send stop command to geared DC motors which are used as wheels of the train ... Once the obstacle is removed from the track then PLC will send run command to geared DC motors. If no obstacle is present on the track at level crossing then the train will continue to run. For automatic railway gate opening and closing system, PLC takes the reference of train position sensors ... Once the train crosses the leveler, PLC activates its output to open the gate automatically after some delay.

#### 摘录 B
- 出处：第 3-4 页，`Hardware Specifications / PLC Programming`，`paper_content.txt` 第 147-170 行
> Limit switches are used to detect the obstacle and position of the train. These switches work as the system input to inform the programmable logic controller (PLC) regarding the current situation of the system (train position). When there’s an obstacle on track, the limit switch gets pressed and PLC receives the input signal.
>
> When the train reaches at position switch 5, the switch gets pressed. The signal goes to the PLC and according to the PLC programming gates closed. When the train reaches at position switch 1, the switch gets pressed, in step with the PLC programming gates opened.
>
> The advantages of using the PLC is that if same PLC is employed for many railway crossings ... the signaling system will automatically be synchronized.

#### 摘录 C
- 出处：第 4 页，`Table-2 PLC Input and Output Addresses`，`paper_content.txt` 第 175-193 行
> Limit Switch 1 (Position 1) I:0/1
> Limit Switch 2 (Position 2) I:0/2
> ...
> Limit Switch 5 (Position 5) I:0/8
> ...
> Limit Switch 1 (Obstacle Detector 1) I:0/9
> ...
> Limit Switch 5 (Obstacle Detector 5) I:0/13
> ...
> Train Motor (Forward) O:0/1
> Train Motor (Reverse) O:0/2
> Gate Assembly Motor (Closing) O:0/3
> Gate Assembly Motor (Opening) O:0/4

#### 摘录 D
- 出处：第 7 页，Conclusion，`paper_content.txt` 第 223-232 行
> Here we used DC motors to open and close the gates automatically by its rotation in anticlockwise and clockwise directions respectively. Whenever the train arrives from a specific direction the proximity sensor provides the signal to PLC and it generates an acceptable signal for the operation of DC motor to close/open the gate. PLC sends operating signal to the dc motors according to the output signal of sensors to open/close the railway crossing gate. In our project, we used obstacle detector switch which saves the life of obstacle.

### 2. 基于原文整理后的自然语言描述

The railway-crossing controller uses train-position limit switches at both sides of the crossing together with obstacle-detector switches, and all of these signals are fed into the PLC as the current system situation. When an obstacle is detected on the level crossing, the PLC sends a stop command to the geared DC train motors, and it releases the train to run again only after the obstacle has been removed. For gate operation, reaching `position switch 5` causes the PLC to command the gate-closing motor, while reaching `position switch 1` causes the PLC to command the gate-opening motor after the crossing has been cleared and the programmed delay has elapsed. The implementation ties these events to explicit PLC addresses: position switches occupy `I:0/1` to `I:0/8`, obstacle detectors occupy `I:0/9` to `I:0/13`, and the outputs `O:0/1` to `O:0/4` drive train forward/reverse and gate closing/opening.

### 3. 逐句溯源

1. 句子 1：The railway-crossing controller uses train-position limit switches at both sides of the crossing together with obstacle-detector switches, and all of these signals are fed into the PLC as the current system situation.
   对应摘录：A, B, C
2. 句子 2：When an obstacle is detected on the level crossing, the PLC sends a stop command to the geared DC train motors, and it releases the train to run again only after the obstacle has been removed.
   对应摘录：A, B
3. 句子 3：For gate operation, reaching `position switch 5` causes the PLC to command the gate-closing motor, while reaching `position switch 1` causes the PLC to command the gate-opening motor after the crossing has been cleared and the programmed delay has elapsed.
   对应摘录：A, B
4. 句子 4：The implementation ties these events to explicit PLC addresses: position switches occupy `I:0/1` to `I:0/8`, obstacle detectors occupy `I:0/9` to `I:0/13`, and the outputs `O:0/1` to `O:0/4` drive train forward/reverse and gate closing/opening.
   对应摘录：C, D

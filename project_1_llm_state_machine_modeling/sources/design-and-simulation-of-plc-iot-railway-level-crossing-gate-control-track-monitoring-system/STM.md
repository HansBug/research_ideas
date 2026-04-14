# Design and Simulation of a PLC and IoT-based Railway Level Crossing Gate Control and Track Monitoring System using LOGO - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路平交口控制器的来车检测、蜂鸣预警、栏杆闭合、道路红灯/列车绿灯、列车离开后的复位开门链条写得较完整，还补了轨道故障监测接口，足够形成 `🚆` 方向的双 A 条目。

## 条目 1: Train-Arrival Gate Closure and Road-Signal Recovery Cycle

- 控制对象：轨道交通与铁路控制领域的 PLC 道口门控与轨道监测联动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向铁路平交口的 PLC 控制器，用轨旁传感器、PLC 输出、栏杆电机和道路/列车信号灯来完成列车到达时的闭门保护与列车离开后的恢复。
- 判断：算。对象是真实铁路道口控制系统，原文不仅说明了传感器到 PLC、PLC 到栏杆和信号灯的输入输出链，还明确写出“来车触发蜂鸣并关门、道路转红/列车转绿、列车离开后重新开门并恢复正常信号”的完整控制顺序。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，`Hardware Design using PLC and IoT`，`paper_content.txt` 第 173-181 行
> The sensor node located on the rail track at a specific distance from the level crossing gate senses the arrival of the train. This sensed signal goes to the PLC's input. After processing the input signal, the PLC sends an appropriate output signal to control the operation of the level-crossing gate.
>
> When the train moves on the railway track, the position switch tracks its position and then directs the input to the PLC to point out the arrival of the train.

#### 摘录 B

- 出处：第 4 页，`Hardware Design using PLC and IoT`，`paper_content.txt` 第 196-201 行
> This system provides the control for automatically closing and opening the gate, and ON/OFF traffic lights indication for status of the gate open and close, anti-collision of two trains at the same track, and identifying track faults or any obstacles present on the track by using the ultrasonic sensors.

#### 摘录 C

- 出处：第 6-7 页，`System Operation`，`paper_content.txt` 第 267-289 行
> When any train is coming from anyone's side then the sensor situated on that track gets HIGH and a signal is generated from the first sensor. The output of the sensor is then fed to the input of the PLC that generates a sound signal for a while ... and then sends an appropriate signal to its output ports to close the barriers for the road traffic.
>
> Before that, the traffic signal gets red color, and the signal for the train line gets green color by which the train can cross through the level crossing gate.
>
> When the train passes out from the level crossing gate then the end side's second sensor gets HIGH and gives a signal to the PLC by which the PLC sends the signal to open up the barriers and then the signals come in their normal positions (i.e., OFF position).

#### 摘录 D

- 出处：第 7 页，`System Operation / Figure 4`，`paper_content.txt` 第 298-305 行
> The whole system operation is shown schematically in Fig. 4. The ultrasonic and RF sensors detect the rail track conditions and the arrival of the locomotive on the track. The sensed signals are then sent to the input ports of the PLC and accordingly the PLC processes the signals to produce the appropriate output signals at its output ports for the motor driver circuits to close the gate and traffic signals to turn red via a short yellow on the road.
>
> When the train passes completely the level crossing gate, the IR sensor is activated and then it sends the signals to the input ports of the PLC. Accordingly, the PLC processes the signals to produce the appropriate output signals at its output ports for the motor driver circuits to open the gate and traffic signals to turn green on the road.

### 2. 基于原文整理后的自然语言描述

The railway level-crossing controller is a PLC-based extended state machine whose inputs come from train-arrival and train-exit sensors together with track-condition sensors, and whose outputs drive the gate motor, warning buzzer, and road or train traffic lights. When the first track-side sensor goes high and announces an approaching train, the PLC first raises an audible warning and then commands the road barriers to close while turning the road signal red and the train-line signal green. The controller keeps the crossing in that protected state while the train occupies the crossing area, and it also integrates obstacle or track-fault detection into the same supervisory control frame. Once the exit-side sensor reports that the train has completely passed, the PLC reverses the motor command, opens the barriers, and restores the signals to their normal road-open state. This gives a usable `EFSM + T0` sample because the paper states the sensing chain, the guarded transition between arrival and departure phases, and the concrete actuator outputs explicitly.

### 3. 逐句溯源

1. 句子 1：The railway level-crossing controller is a PLC-based extended state machine whose inputs come from train-arrival and train-exit sensors together with track-condition sensors, and whose outputs drive the gate motor, warning buzzer, and road or train traffic lights.
   对应摘录：A, B, D
2. 句子 2：When the first track-side sensor goes high and announces an approaching train, the PLC first raises an audible warning and then commands the road barriers to close while turning the road signal red and the train-line signal green.
   对应摘录：C
3. 句子 3：The controller keeps the crossing in that protected state while the train occupies the crossing area, and it also integrates obstacle or track-fault detection into the same supervisory control frame.
   对应摘录：B, D
4. 句子 4：Once the exit-side sensor reports that the train has completely passed, the PLC reverses the motor command, opens the barriers, and restores the signals to their normal road-open state.
   对应摘录：C, D
5. 句子 5：This gives a usable `EFSM + T0` sample because the paper states the sensing chain, the guarded transition between arrival and departure phases, and the concrete actuator outputs explicitly.
   对应摘录：A, B, C, D

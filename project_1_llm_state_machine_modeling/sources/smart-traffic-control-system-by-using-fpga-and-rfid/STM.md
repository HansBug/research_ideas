# Smart Traffic Control System by Using FPGA and RFID - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：协议交互, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 RFID 应急车辆优先、IR 车流密度检测、正常 FSM 序列、灯色输出和 5 秒/2 秒延时，可形成双 A 交通信号优先控制样本，但与既有应急车辆优先簇高度相近。

## 条目 1: RFID Emergency-Priority Density-Aware Traffic FSM

- 控制对象：道路交通信号控制领域的 RFID 应急车辆优先与 IR 密度感知交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：协议交互, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G2 应急车辆交通灯优先）

### 0. 条目识别与判定

- 一句话说明：这是一个四向路口交通灯控制器，FPGA 接收 RFID 应急车辆信号和 IR 车流密度信号，在正常 FSM 相位、密度优先相位和应急绿通道之间切换。
- 判断：算。对象是实际交通灯控制系统，原文同时给出通信触发、密度 guard、红黄绿输出、正常序列和显式延时，满足 `EFSM + T1` 的双 A 样本要求。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`Abstract`，`paper_content.txt` 第 20-33 行
> To overcome these problems, Smart Traffic Control System using FPGA (Field Programmable Gate Array) IR sensors and RFID (Radio frequency Identifier) is introduced to sophisticated traffic moves and provide the lane for the ambulances. The RFID uses in this system is determines the emergency vehicles from the long distance and this information passes and controlled by the FPGA and it control the main traffic control lights. ... The controlling and switching of the traffic lights states (Red, Yellow and Green) is found on the FSM (Finite State Machine). ... This implementation shows the results of identifying the emergency vehicles and Green signal is on till that emergency vehicles are passed.

#### 摘录 B

- 出处：第 4 页，`IV. PROPOSED SYSTEM / V. FLOW CHART`，`paper_content.txt` 第 95-119 行
> The FPGA Spartan 6 device is a heart of the control system. Which receives the multiple input signals from the input sensors (IR and RFID) and processes the input signal according to the programming and sends the multiple output signals to the output device i.e. light emitting diode (LED). Mainly these control system is worked based on the Finite State Machine (FSM). The RFID (Radio Frequency Identifier) is mainly employed to detect the emergency vehicles (EV) through the RFID tag and RFID reader. If any emergency vehicle is detected, this data is send to the FPGA it immediately on the "Green Corridor" to clear the traffic lane and provides the easy way for the emergency Automobiles.
>
> The IR input sensors mainly used to the four ways of the junction to detect the density of traffic. ... Depending upon the length of the traffic density, it blink the green LED lights to clear the traffic. If there is no Ambulance are detected and if the traffic jam in all four lanes are equal, the advanced traffic control system works in the regular sequence i.e. finite state machine(FSM).
>
> Once the system is initialize, it start to detect the any emergency vehicles. If any emergency vehicles are detected in out of four road lanes, the "green corridor" will be automatically on for certain amount of period. Once the emergency vehicle is passed, the control system immediately starts to regulate the traffic in normal way. If there is no emergency vehicles are detected, the system is skips to the next condition that is calculation of vehicle density.

#### 摘录 C

- 出处：第 5 页，`VI. FINITE STATE MACHINE`，`paper_content.txt` 第 133-145 行
> The FSM is Structural model with finite of states, finite stimuli and finite outputs. ... Implementation of the state machine in our project employs Moore.
>
> In the above diagram, we can see the pictorial representation of FSM with the controller. It consists of four states for each lane of the junction. They are Reading the previous timing parameter, writing the advanced timing parameter, Running of the normal mode traffic and running the blinking mode traffic. In the idle mode, the LED's are turned off. So that it is referred as rest mode. Where the model will visit to the reset state. For all direction green and red lights, the five seconds delay is given and for yellow two seconds delay is given.

### 2. 基于原文整理后的自然语言描述

The FPGA traffic controller is an extended Moore-style FSM that receives RFID emergency-vehicle detections and IR traffic-density inputs from the four approaches of a junction, then drives red, yellow, and green LED traffic-light outputs. After initialization the controller first checks for an emergency vehicle; if an RFID-tagged ambulance is detected on one lane, it immediately enables the green corridor for that lane and keeps the priority green signal active until the emergency vehicle passes, after which it returns to normal traffic regulation. If no emergency vehicle is present, the controller evaluates IR-based density, assigns green to a congested lane when density exceeds the configured limit, skips empty lanes, and otherwise runs the regular FSM sequence when all lanes have equal traffic. Its controller FSM includes reset/idle behavior plus timing-parameter read/write, normal traffic mode, and blinking mode states, and it applies local light delays of five seconds for green/red directions and two seconds for yellow.

### 3. 逐句溯源

1. 句子 1：The FPGA traffic controller is an extended Moore-style FSM that receives RFID emergency-vehicle detections and IR traffic-density inputs from the four approaches of a junction, then drives red, yellow, and green LED traffic-light outputs.
   对应摘录：A, B, C
2. 句子 2：After initialization the controller first checks for an emergency vehicle; if an RFID-tagged ambulance is detected on one lane, it immediately enables the green corridor for that lane and keeps the priority green signal active until the emergency vehicle passes, after which it returns to normal traffic regulation.
   对应摘录：A, B
3. 句子 3：If no emergency vehicle is present, the controller evaluates IR-based density, assigns green to a congested lane when density exceeds the configured limit, skips empty lanes, and otherwise runs the regular FSM sequence when all lanes have equal traffic.
   对应摘录：B
4. 句子 4：Its controller FSM includes reset/idle behavior plus timing-parameter read/write, normal traffic mode, and blinking mode states, and it applies local light delays of five seconds for green/red directions and two seconds for yellow.
   对应摘录：C

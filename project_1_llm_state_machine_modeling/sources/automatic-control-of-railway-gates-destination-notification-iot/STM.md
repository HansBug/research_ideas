# Automatic Control of Railway Gates and Destination Notification System using Internet of Things (IoT) - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把道口门控写成一条完整的 arrival-close / departure-open 控制链，并明确列出了双传感确认、LED 联动和持续轮询算法。

## 条目 1: Four-IR level-crossing gate controller
- 控制对象：轨道交通领域的铁路平交道口自动门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G3 铁路道口门控）

### 0. 条目识别与判定

- 一句话说明：这是一个用 Raspberry Pi、四个 IR 传感器、伺服电机和红黄 LED 实现的铁路道口门控系统，按列车到达和离开顺序自动关闸和开闸。
- 判断：算。对象是实际 level crossing gate controller，原文给出了传感器布置、双传感判定、开关闸动作、LED 输出以及逐步算法。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4-5 页，`System Design And Analysis / General Architecture of Proposed System`，行 139-180
> the ideal place at which IR sensors could be placed to detect the arrival of the train is 6km and 7kms from the level crossing and ideal distance for IR sensors to detect the departure of the train is 2km and 3km. thus the gate will not be closed for more than 10 minutes.
> ...
> The proposed system uses 4 IR sensors for detecting the train, LEDs for controlling the traffic, RFID reader for sending notification or alert message and Servo motor for opening and closing gate.
> ...
> The proposed system makes use of 4 IR sensors - 2 left and 2 right sensors.
> ...
> When the train arrives red LED will glow and when the train departures yellow LED will glow.
> ...
> Figure 2 shows the Data flow diagram for gate operations ... When the train is detected by the right sensors, the motor closes the gate and red LED will glow. In the same way, the left sensors will senses the departure of the train and motor will opens the gate and yellow LED glows.

#### 摘录 B
- 出处：第 5-6 页，`The Algorithm for opening and closing of the gate`，行 188-199
> Step 1: Start.
> Step 2: Turn on all IR sensors and yellow LEDs.
> Step 3: Continuously check the status of right IR sensors.
> Step 4: If both right IR sensors are active [arrival of train] go to Step 5 otherwise go to Step 3.
> Step 5: Activate the motor, which closes the gate, turn on Red LED [stop indication for vehicles] and turn off yellow LEDs.
> Step 6: Continuously check the status of left IR sensors.
> Step 7: If both left IR sensors are active [departure of train] go to Step 8 otherwise go to Step 6.
> Step 8: Send the signal to motor for opening the gate. Motor opens the gate then Pi turns off Red LED and turn on yellow LEDs [go indication for vehicles]. Go to Step 3.

#### 摘录 C
- 出处：第 8-9 页，`Result and Analysis`，行 237-273
> In normal state [no train], YELLOW LED is blinking, right and left sensors are in inactive state and RED LED is in OFF state.
> ...
> When train is detected by the right sensors [both are active], right sensors will send the active information to pi then pi will send the gate closing information to gate controller, OFF signal to YELLOW LED and ON signal to RED LED.
> ...
> gate controller will close the gate, RED LED is turned ON and YELLOW LED is turned OFF
> ...
> When train is detected by the left sensors [both are active] ... pi will send the gate opening information to gate controller, OFF signal to RED LED and ON signal to YELLOW LED.
> ...
> gate controller will open the gate, YELLOW LED is turned ON and RED LED is turned OFF

### 2. 基于原文整理后的自然语言描述

The railway level-crossing controller uses four IR sensors, two on the approach side and two on the departure side, together with a Raspberry Pi, servo motor, and red/yellow LEDs to manage the gate automatically. It starts in a normal state with blinking yellow indication, inactive sensors, and the gate open, then continuously polls the approach-side sensors until both arrival sensors are active, at which point it closes the gate, turns off yellow, and turns on red for road traffic. After closure, it continuously polls the departure-side sensors until both departure sensors are active, then commands the motor to reopen the gate, turns red off, turns yellow on, and returns to the monitoring loop. The design also constrains the sensor layout so that train arrival is detected kilometers before the crossing and the gate is intended not to remain closed for more than about ten minutes.

### 3. 逐句溯源

1. 句子 1：The railway level-crossing controller uses four IR sensors, two on the approach side and two on the departure side, together with a Raspberry Pi, servo motor, and red/yellow LEDs to manage the gate automatically.
   对应摘录：A
2. 句子 2：It starts in a normal state with blinking yellow indication, inactive sensors, and the gate open, then continuously polls the approach-side sensors until both arrival sensors are active, at which point it closes the gate, turns off yellow, and turns on red for road traffic.
   对应摘录：B, C
3. 句子 3：After closure, it continuously polls the departure-side sensors until both departure sensors are active, then commands the motor to reopen the gate, turns red off, turns yellow on, and returns to the monitoring loop.
   对应摘录：B, C
4. 句子 4：The design also constrains the sensor layout so that train arrival is detected kilometers before the crossing and the gate is intended not to remain closed for more than about ten minutes.
   对应摘录：A

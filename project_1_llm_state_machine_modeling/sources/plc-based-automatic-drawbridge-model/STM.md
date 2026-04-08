# PLC based Automatic Drawbridge Model - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把船舶到达检测、桥面清空、道闸关闭、桥体开启、船舶通行和恢复道路通行写成了一条闭环顺序控制链，是通用控制方向很干净的双 A `EFSM + T0` 样本。

## 条目 1: Ship-Triggered Barrier and Bridge Opening Cycle

- 控制对象：通用控制领域的船舶触发道闸与开桥顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 `IR` 船舶检测、`ultrasonic` 障碍检测、`servo motor` 道闸和 `Johnson motor` 桥体驱动构成的自动开桥控制器。
- 判断：算。对象是实际桥梁交通控制系统，原文明确给出了来船检测、清桥、关道闸、开桥、船过桥、关桥和重新放行道路交通的顺序链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 22-25 行
> a fully automated bridge is proposed by using microcontroller and PLC ... automate the process of ship detection, opening or closing of the bridge, controlling the signals and road barriers.

#### 摘录 B

- 出处：第 1-2 页，`Introduction / System Design`，`paper_content.txt` 第 46-52 行、第 127-134 行
> The sensor detects the presence of ship and vehicles on the bridge. ... Ship is detected by IR sensor ... Ultrasonic sensors are used to check the presence of vehicles on the bridge. Sensors output provides input to the microcontroller and then to PLC and it will drive Johnson motor, Servo motor and Signal Poles according to programming.
>
> The IR sensors are placed on either side of the bridge which detects the ship arrival and departure respectively. The ultrasonic sensors are used to provide an interrupt signal ... when vehicles are detected on the bridge. The servomotors open and close the toll gates ... Johnson motors are used to open and close the bridges.

#### 摘录 C

- 出处：第 3 页，`system outputs`，`paper_content.txt` 第 148-151 行、第 202-205 行
> LEDs are installed in the signal poles on either side of bridge and across the bridge for signaling of ship and vehicles respectively. Buzzer is used for alarming in case of emergency situations ... and to alarm before the bridge opens.
>
> According to the signals given by the microcontroller PLC drives the required motors.

#### 摘录 D

- 出处：第 5 页，`Flowchart of the system`，`paper_content.txt` 第 295-305 行
> When arrival of the ship is detected it sends a signal to microcontroller. The microcontroller turns the buzzer on for clearing the bridge. The ultrasonic sensors detect the presence of any obstacles on the bridge before opening the bridge ... If the bridge is clear, microcontroller sends signal to PLC to drive the servo motors to close the road barriers and signal changes from green to red. Then PLC drives Johnson motors to open the bridge and the signal for ship turns from red to green. ... the PLC drives the Johnson motor in reverse direction until the bridge is totally closed. Then road barrier will be opened and signal changes from red to green for vehicles and green to red for ship.

### 2. 基于原文整理后的自然语言描述

The drawbridge controller begins in a road-open state in which vehicle barriers stay open and the bridge leaf remains closed to road traffic. When an `IR` sensor detects an arriving ship, the microcontroller first starts a buzzer-based clearing phase and checks the bridge deck with `ultrasonic` sensors to ensure no vehicles remain on the span. If the deck is clear, the PLC closes the road barriers with the servo motors, switches the road signal from green to red, and then drives the `Johnson motor` to raise the bridge while the ship-side signal changes from red to green. After the ship reaches the opposite side and the departure sensor fires, the PLC reverses the bridge motor until the span is fully closed, reopens the road barriers, restores road green, and turns the ship signal back to red.

### 3. 逐句溯源

1. 句子 1：The drawbridge controller begins in a road-open state in which vehicle barriers stay open and the bridge leaf remains closed to road traffic.
   对应摘录：A, B, C
2. 句子 2：When an `IR` sensor detects an arriving ship, the microcontroller first starts a buzzer-based clearing phase and checks the bridge deck with `ultrasonic` sensors to ensure no vehicles remain on the span.
   对应摘录：B, C, D
3. 句子 3：If the deck is clear, the PLC closes the road barriers with the servo motors, switches the road signal from green to red, and then drives the `Johnson motor` to raise the bridge while the ship-side signal changes from red to green.
   对应摘录：B, C, D
4. 句子 4：After the ship reaches the opposite side and the departure sensor fires, the PLC reverses the bridge motor until the span is fully closed, reopens the road barriers, restores road green, and turns the ship signal back to red.
   对应摘录：B, D

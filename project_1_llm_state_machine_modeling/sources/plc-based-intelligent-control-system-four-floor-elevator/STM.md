# PLC-Based Intelligent Control System for Four-Floor Elevator - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四层电梯的 collective-call 调度、三态方向机、3 秒门停留和 overload/obstruction 安全联锁完整写成了 PLC 状态链，是稳定的 T1 电梯样本。

## 条目 1: Collective-Call Four-Floor Elevator PLC Controller

- 控制对象：楼宇机电领域的四层电梯呼梯调度、门控与安全联锁控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 Siemens PLC 四层电梯控制器，用 car-call、hall-call、楼层传感器、门阻挡和过载输入来驱动上行、下行、停层和开关门逻辑。
- 判断：算。对象是实际电梯 PLC 控制系统，原文明确给出了状态机、I/O 映射、门控定时和测试序列，不是纯硬件展示。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract / Introduction，`paper_content.txt` 第 10-15, 28-34 行
> This paper presents a PLC-based control system for a four-floor elevator ... to manage car calls, hall calls, motion scheduling, and door operations. The system offers automatic and manual modes with safety interlocks for the overload and door obstruction.
>
> This study applied a PLC to control a four-floor elevator system, achieving intelligent operation by managing car and hall calls, determining motion direction, and controlling doors and safety interlocks. The PLC implements collective call scheduling, which is a standard elevator strategy that groups and sequences requests in the direction of travel.

#### 摘录 B

- 出处：第 2-3 页，Section 2.2 `Control Logic Strategy`，`paper_content.txt` 第 66-80, 89-104 行
> The system is connected to the following components: ... Floor Sensors ... Obstruction Sensor ... Overload Sensor ... Car Call Buttons ... Hall Call Buttons ...
>
> The PLC logic maintains a state machine that processes these inputs and controls the outputs. ... Direction State Machine: The program has three states: Ascending, Descending, and Stopped. ... From Stopped, it chooses a new direction based on pending requests above or below the current position. ... Door Control: When the car arrives at the requested floor ... the PLC opens the doors for a fixed interval. If the obstruction sensor is triggered during closing, the PLC reopens the door and waits until the obstruction is cleared.

#### 摘录 C

- 出处：第 5-7 页，Section 4 `Software Design`，`paper_content.txt` 第 179-203, 209-236 行
> The core control logic is implemented as a state machine with three primary states: Ascending, Descending, and Stopped. ... the elevator serves all calls above it before reversing ... Once no calls remain in the current direction, the logic transitions to stopped and then to the opposite direction, if needed.
>
> When the car arrives at the requested floor ... the PLC triggers Q0.2 to open the doors for a fixed dwell time (e.g., 3 s). After the interval, the PLC signals the door to close. If the obstruction sensor becomes active during closing, the program reopens the doors and restarts the closing timer.
>
> If the overload input is true, the motor outputs are inhibited until the condition clears.

#### 摘录 D

- 出处：第 8 页，Section 5 `Implementation and Testing`，`paper_content.txt` 第 260-265 行
> In one test, the car-call buttons for floors 1, 3, and 4 were pressed. Starting from floor 1, the elevator ascended, stopped at floor 3 to open the doors, and then proceeded to floor 4. In another test, hall-call Up on floor 2 and hall-call Down on floor 4 were entered; the elevator moved up from 1 to 2, then reversed direction and stopped at 4. In all scenarios, the doors opened for the programmed interval at each stop, and the simulated obstruction or overload signals were handled correctly.

### 2. 基于原文整理后的自然语言描述

The four-floor elevator controller uses floor sensors, car-call buttons, hall-call buttons, door-obstruction sensing, and overload detection as its main decision inputs, and it drives `Motor Up`, `Motor Down`, and the door actuator as outputs. Its scheduling policy is collective-call control: while moving in one direction, the PLC keeps serving requests in that direction before it stops and considers reversing. The direction logic is organized as a three-state machine with `Ascending`, `Descending`, and `Stopped` states, and transitions are determined by pending requests above or below the current floor. When the car reaches a requested floor, the PLC opens the door for a fixed dwell time of about `3 s`; if obstruction is detected during closing, the controller reopens the door and restarts the timer. If the overload input is active, motion outputs are inhibited until the unsafe condition is cleared. The implementation section further shows concrete test sequences such as `1 -> 3 -> 4` servicing and `2-up / 4-down` reversal, confirming that the state machine is exercised as a real controller rather than only described abstractly.

### 3. 逐句溯源

1. 句子 1：The four-floor elevator controller uses floor sensors, car-call buttons, hall-call buttons, door-obstruction sensing, and overload detection as its main decision inputs, and it drives `Motor Up`, `Motor Down`, and the door actuator as outputs.
   对应摘录：A, B
2. 句子 2：Its scheduling policy is collective-call control: while moving in one direction, the PLC keeps serving requests in that direction before it stops and considers reversing.
   对应摘录：A, B, C
3. 句子 3：The direction logic is organized as a three-state machine with `Ascending`, `Descending`, and `Stopped` states, and transitions are determined by pending requests above or below the current floor.
   对应摘录：B, C
4. 句子 4：When the car reaches a requested floor, the PLC opens the door for a fixed dwell time of about `3 s`; if obstruction is detected during closing, the controller reopens the door and restarts the timer.
   对应摘录：B, C
5. 句子 5：If the overload input is active, motion outputs are inhibited until the unsafe condition is cleared.
   对应摘录：A, C
6. 句子 6：The implementation section further shows concrete test sequences such as `1 -> 3 -> 4` servicing and `2-up / 4-down` reversal, confirming that the state machine is exercised as a real controller rather than only described abstractly.
   对应摘录：D

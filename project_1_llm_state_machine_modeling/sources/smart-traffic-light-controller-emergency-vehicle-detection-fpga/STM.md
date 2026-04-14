# Design and implementation of smart traffic light controller with emergency vehicle detection on FPGA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四向路口交通灯控制器写成 `clock divider + counter + FSM` 三子模块结构，并给出 `50/30/15/5` 秒定时和 `RFID/IR` 触发规则，足以形成双 A 的应急优先交通灯样本。

## 条目 1: Emergency-Priority Four-Way Traffic-Light EFSM

- 控制对象：四向路口的应急车辆优先交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号领域的四向路口交通灯 controller，用 RFID 检测应急车辆、用 IR 传感器估计密度，并通过显式计时器决定绿黄红相位切换。
- 判断：算。对象是实际交通信号控制器，原文明确给出输入设备、子模块划分、密度到绿灯时长映射，以及 `check RFID / check IR / green / yellow` 的状态切换链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> The controller is designed specifically to detect emergency vehicle at four-way intersections for inputs radio frequency identification (RFID) readers and infrared (IR) sensors. The RFID readers and IR sensors are managed through slide switches on the FPGA board. The smart traffic light controller contains three sub-modules: clock division, counter, and finite state machine (FSM) operation, enabling it to manage traffic in scenarios with emergency vehicles, high traffic density, and low traffic density.

#### 摘录 B

- 出处：第 4 页，Figure 1 / Table 1
> RFID readers can identify the presence of an emergency vehicle within a 100 meter radius, while the number of active IR sensors detects the traffic density. Once the RFID reader detects the emergency vehicle’s unique RFID tag, the green light for the detected lane will be turned on for at least 50 seconds ...
>
> Table 1. Green light timing duration based on the number of activated IR sensors
> 0 -> 0 second -> Zero density
> 1 -> 15 second -> Low density
> 2 -> 30 second -> High density

#### 摘录 C

- 出处：第 5 页，Figure 3 / Figure 4 说明
> The operation starts in the check RFID state. If an emergency vehicle (EV) is detected (RFID≠0000), the lane with the EV is turned green for at least 50 seconds. Once the 50 seconds have elapsed, and if the EV is no longer detected, the light transitions to yellow for 5 seconds before returning to the check RFID state.
>
> If no EV is detected (RFID=0000), the system moves to the check IR state. Here, traffic is evaluated sequentially for the North (N), East (E), South (S), and West (W) lanes.

#### 摘录 D

- 出处：第 5 页，Figure 4 说明续
> Depending on traffic density, the green light is activated for either 30 seconds (for high traffic density) or 15 seconds (for low traffic density). After the designated green light duration, the lane turns yellow for 5 seconds before reverting to the check RFID state. While a lane is green, the RFID status is continuously monitored. If an EV is detected in any lane during this period, the current green lane will switch to yellow for 5 seconds and return to the check RFID state.

### 2. 基于原文整理后的自然语言描述

The proposed four-way traffic-light controller is an FPGA-based EFSM that combines RFID emergency detection, IR-based traffic-density sensing, and explicit phase timers. Its control pipeline is split into `clock division`, `counter`, and `FSM operation` submodules, so each state transition is driven by a visible timing and event layer rather than by implicit combinational behavior. The machine starts in `check RFID`, where any detected emergency vehicle immediately forces the corresponding lane to green for at least `50` seconds; once the emergency tag disappears, the controller inserts a `5`-second yellow interval and returns to emergency monitoring. If no emergency vehicle is present, the controller enters `check IR`, evaluates the `North / East / South / West` lanes sequentially, and assigns `15` seconds of green for low density or `30` seconds for high density according to the number of activated IR sensors. While a normal green phase is active, RFID input continues to be monitored, so an emergency request can preempt the current lane and hand control back to the emergency-priority branch.

### 3. 逐句溯源

1. 句子 1：The proposed four-way traffic-light controller is an FPGA-based EFSM that combines RFID emergency detection, IR-based traffic-density sensing, and explicit phase timers.
   对应摘录：A, B
2. 句子 2：Its control pipeline is split into `clock division`, `counter`, and `FSM operation` submodules, so each state transition is driven by a visible timing and event layer rather than by implicit combinational behavior.
   对应摘录：A
3. 句子 3：The machine starts in `check RFID`, where any detected emergency vehicle immediately forces the corresponding lane to green for at least `50` seconds; once the emergency tag disappears, the controller inserts a `5`-second yellow interval and returns to emergency monitoring.
   对应摘录：B, C
4. 句子 4：If no emergency vehicle is present, the controller enters `check IR`, evaluates the `North / East / South / West` lanes sequentially, and assigns `15` seconds of green for low density or `30` seconds for high density according to the number of activated IR sensors.
   对应摘录：B, C, D
5. 句子 5：While a normal green phase is active, RFID input continues to be monitored, so an emergency request can preempt the current lane and hand control back to the emergency-priority branch.
   对应摘录：D

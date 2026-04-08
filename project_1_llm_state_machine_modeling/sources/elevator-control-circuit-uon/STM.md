# Elevator Control Circuit - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：报告把三层电梯的楼层状态、楼层请求到跃迁的映射，以及门保持开启 `7` 秒的计数链写得很完整，可直接作为楼宇机电顺序控制样本。

## 条目 1: Three-Floor Service and Door-Dwell Controller
- 控制对象：楼宇机电领域的三层电梯顺序控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定
- 一句话说明：这是一个服务三层建筑的电梯控制器，用按钮请求、楼层状态和门开闭计数器来决定轿厢停留、上下行和开门保持时长。
- 判断：算。对象是实际电梯控制系统，原文明确给出了状态名、楼层请求到迁移的对应关系、`OPEN / CLOSE` 对门计时的影响，以及 `7` 秒开门保持。

### 1. 原文摘录

#### 摘录 A
- 出处：第 20-21 页，`3.1 Design specification`，`paper_content.txt` 第 433-450 行
> The Algorithmic State Machine design method is used due to the presence of large number of input signals. The controller responds to call switches on each floor and floor select switches within the elevator. When the elevator lands on a given floor of the building, signals are generated from the sensor switches. The controller should also generate control signals to move the elevator up or down and generate signals to open or close the door.
>
> There is a request push-button on each floor beside the elevator door. When the elevator arrives at a given floor, the door opens for a pre-determined duration to allow passengers on and off and then closes automatically. Inside the elevator there are several push-button switches. These are X0, X1, X2, OPEN and CLOSE push-buttons switches. Pressing the open switch will cause the door to reopen. If none of the switches is activated, then the elevator remains at the last floor serviced. A slow clock signal controls the time that the door remains open when the elevator stops at a floor.

#### 摘录 B
- 出处：第 23 页，`3.3 The Algorithmic State Machine (ASM) Chart for the controller`，`paper_content.txt` 第 514-535 行
> The three states of the system are as follows;
> • GRD: The elevator is waiting on ground floor with the door open or closed.
> • FIR: The elevator is waiting on first floor with the door open or closed.
> • SEC: The elevator is waiting on second floor with the door open or closed.
>
> Each block in the ASM chart describes the state of the system during one clock pulse interval. The operations in the state and conditional boxes within that block are executed with a common clock pulse while the elevator is in that state. The same clock pulse also transfers the system controller to one of the next states – GRD, FIR or SEC as dictated by the binary values.

#### 摘录 C
- 出处：第 21-24 页，`Description of the system requirement / State GRD`，`paper_content.txt` 第 460-471 行、第 538-540 行
> If the elevator is on ground floor and the floor requested is ground floor, then the elevator remains waiting on ground floor. When the elevator is on ground floor and the floor requested is first floor, then the elevator is raised up one floor, then if the elevator is on ground floor and the floor requested is second floor, then the elevator is raised up two floors.
>
> When the elevator is on first floor and the floor requested is first floor, then the elevator remains on first floor. If the elevator is on first floor and the floor requested is second floor, then the elevator is raised up one floor, then if the elevator is on first floor and the floor requested is ground floor, then the elevator goes down one floor.
>
> When the elevator is on second floor and the floor requested is second floor, then the elevator remains on second floor. If the elevator is on second floor and the floor requested is first floor, then the elevator goes down one floor. When the elevator is on second floor and the floor requested is ground floor, then the elevator goes down two floors.
>
> If CLOSE = 1, the counter is cleared to 0 and the door is closed. Then if OPEN = 1, the counter continues to count while the door is open.

#### 摘录 D
- 出处：第 29 页，`3.3.5 Datapath`，`paper_content.txt` 第 617-631 行
> The Datapath for the elevator controller consists of a pulser, three counters and gates. ... counter 1 and counter 2 ... are used to determine the stability of the pulse, to generate a low frequency of about one pulse per second to observe slow changes in the digital signal. The third counter, counter 3 is a down counter with parallel load, this counter determines the open /close door operations, in this counter the binary number decreases by one for each input pulse.
>
> The count starts at Q3Q2Q1Q0 = 0111 and decrements by 1 after every clock pulse. When the count reaches Q3Q2Q1Q0 = 0000, counter 1 and 2 are cleared and counter 3 stops counting (door closes). ... If OPEN = 1 counter3 is set and the count continues, then if CLOSE = 1 count stops. Therefore door opens for seven seconds to allow passengers on or off and then closes automatically. Pressing the open push button inside the elevator will cause the door to reopen or stay open longer than the preset time as long as the elevator is not moving.

### 2. 基于原文整理后的自然语言描述

The controller is an ASM-based three-floor elevator FSM that reads hall and car-call buttons, floor sensors, and `OPEN / CLOSE` door commands, and it drives elevator motion, door actuation, and floor display outputs. It organizes service around the three named states `GRD`, `FIR`, and `SEC`, where each state means the car is waiting at the corresponding floor with the door either open or closed and state changes occur on a common clock pulse. From each floor, a request for the same floor keeps the controller in the current state, a request for the adjacent floor produces an immediate one-floor move, and a request for the far floor produces a two-floor jump up or down. Door dwell is handled by a counter chain that counts one pulse per second from `0111` to `0000`, keeps the door open for seven seconds, closes it automatically at timeout, reopens or extends it when `OPEN` is pressed, and clears the count immediately when `CLOSE` is asserted.

### 3. 逐句溯源

1. 句子 1：The controller is an ASM-based three-floor elevator FSM that reads hall and car-call buttons, floor sensors, and `OPEN / CLOSE` door commands, and it drives elevator motion, door actuation, and floor display outputs.
   对应摘录：A
2. 句子 2：It organizes service around the three named states `GRD`, `FIR`, and `SEC`, where each state means the car is waiting at the corresponding floor with the door either open or closed and state changes occur on a common clock pulse.
   对应摘录：B
3. 句子 3：From each floor, a request for the same floor keeps the controller in the current state, a request for the adjacent floor produces an immediate one-floor move, and a request for the far floor produces a two-floor jump up or down.
   对应摘录：C
4. 句子 4：Door dwell is handled by a counter chain that counts one pulse per second from `0111` to `0000`, keeps the door open for seven seconds, closes it automatically at timeout, reopens or extends it when `OPEN` is pressed, and clears the count immediately when `CLOSE` is asserted.
   对应摘录：C, D

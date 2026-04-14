# FPGA Implementation of Elevator Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确把 FPGA 电梯控制器定义为 Mealy 型 FSM，并给出楼层开门/运行状态、内外呼梯按钮、位置传感器、默认状态、门定时和多请求方向处理，足以形成双 A 电梯控制样本。

## 条目 1: Parameterized Mealy Elevator Request and Door Controller

- 控制对象：楼宇机电与电梯控制领域的参数化 FPGA 电梯请求、运行与门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G4 同向优先电梯调度与门控）

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Verilog 和 FPGA 的电梯控制器，用 Mealy 状态机根据内外呼梯按钮、楼层位置传感器、门定时器和方向请求来控制轿厢移动和开门。
- 判断：算。对象是实际电梯控制器，原文给出了状态集合、输入触发、传感器 guard、输出动作、默认状态、门关闭定时和多请求方向策略，属于我们关注的具有状态机属性的控制系统。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`1. INTRODUCTION / 2. ELEVATOR CONTROLLER AND ITS WORKING`，`paper_content.txt` 第 71-95 行
> The elevator control system is basically a finite state machine (F SM).  FSM is a digital sequential circuit that consists of different defined states that are controlled by inputs. The given elevator control system is based on Mealy machine in which the output values are determined both by its current state and the current inputs.
>
> The complete operation of the elevator system is controlled by the elevator controller. The proximity sensors are located to sense the positions of the cars providing the current state storing it in register. The elevator controller also reads the requests from any of the request positions through the flip-flops. ... When the door of any elevator is open, the timer signals from the elevator inform the controller of being busy. The control state machine (CSM) of the controller receives all these signals. It is programmed according to the algorithm which controls the entire operation of the system. The CSM then generates control signals for movement of the elevators and for its next position.

#### 摘录 B

- 出处：第 1 页，`2. ELEVATOR CONTROLLER AND ITS WORKING`，`paper_content.txt` 第 100-110 行
> A. Elevator Priority: Elevators are prioritized for the requests. The elevator1 has a priority for the request from first floor the elevator2 for the second floor request.
>
> B. Default State: The default states are elevator1 on first floor with closed door and elevator2 at second floor with closed door. These default positions provide faster response to the request coming at any of the two floors.
>
> C. Closing the Elevator Door: Door of the elevator closes after some time as defined by the timer present in the module. By default, the timer should be 0 and after closing it must be 1.

#### 摘录 C

- 出处：第 2-3 页，`4. STATE DIAGRAM`，`paper_content.txt` 第 153-195、203-218 行
> The state diagram of the elevator controller for a building is shown in Fig 2. In this, Mealy model is implemented. A control signal is used to select the number of floors for which the elevator should work.
>
> F1_OPEN, F2_OPEN, F3_OPEN, F4_OPEN: These state variables are used to represent that the elevator door is open at the corresponding floor. ... F1_OPEN is the default state.
>
> F1_MOVING, F2_MOVING, F3_MOVING, F4_MOVING: These variables are used to indicate the floor to which the elevator is moving.
>
> F_1, F_2, F_3, F_4: These are the buttons inside the car ... When F_2 is pressed from a floor, the elevator enters the F2_MOVING state.
>
> AF_1, AF_2, AF_3, AF_4: These are the position sensors which, when high, indicates that the corresponding floor has been reached. ... When AF_2 makes a transition from 0 to 1, the F2_MOVING state will be changed to F2_OPEN state. ... The program is also developed in such a way that it can handle multiple requests at a time and the directions are also taken into consideration.
>
> Once the requested floors position sensor is high, the door of the elevator is opened, that is, the state changes from MOVING to OPEN. The OPEN state of first floor (F1_OPEN) is set as the default state. Upon reset, all the requests and the control signal will be cleared and the elevator will be in the default state.

#### 摘录 D

- 出处：第 3 页，`5. RESULTS AND REPORTS`，`paper_content.txt` 第 236-244 行
> Here, the control signal is 1010 and the system works as a 9 floor elevator controller. Thereafter different conditions for the elevator controller were checked. When F_7 button is pressed by the user, the car moves to the seventh floor and the current state will be F7_MOVING. The state of the door at any instant is indicated by the state variable 'open'; the door remains closed during the moving state. When AF_7 goes high, it indicates that the elevator has now reached the seventh floor and the door will be open.

### 2. 基于原文整理后的自然语言描述

The FPGA elevator controller is a Mealy-style extended state machine whose outputs depend on both the current elevator state and the current button, sensor, timer, and control-signal inputs. It uses floor-open states such as `F1_OPEN` and floor-moving states such as `F2_MOVING`, with internal car buttons `F_1` to `F_4`, external up/down calls `U_1` to `U_3` and `D_2` to `D_4`, and arrival sensors `AF_1` to `AF_4` as transition triggers. After reset, all requests and the control signal are cleared and the controller returns to the default first-floor open state or the configured default car positions; when a request button is pressed, the car enters the requested `MOVING` state, keeps the door closed while moving, and changes to the corresponding `OPEN` state when the target floor sensor rises. The controller also handles multiple requests by respecting direction order, gives configured priority between elevators, and uses a door timer so that an open door closes after the defined delay and the controller can leave the busy condition.

### 3. 逐句溯源

1. 句子 1：The FPGA elevator controller is a Mealy-style extended state machine whose outputs depend on both the current elevator state and the current button, sensor, timer, and control-signal inputs.
   对应摘录：A, C
2. 句子 2：It uses floor-open states such as `F1_OPEN` and floor-moving states such as `F2_MOVING`, with internal car buttons `F_1` to `F_4`, external up/down calls `U_1` to `U_3` and `D_2` to `D_4`, and arrival sensors `AF_1` to `AF_4` as transition triggers.
   对应摘录：C
3. 句子 3：After reset, all requests and the control signal are cleared and the controller returns to the default first-floor open state or the configured default car positions; when a request button is pressed, the car enters the requested `MOVING` state, keeps the door closed while moving, and changes to the corresponding `OPEN` state when the target floor sensor rises.
   对应摘录：B, C, D
4. 句子 4：The controller also handles multiple requests by respecting direction order, gives configured priority between elevators, and uses a door timer so that an open door closes after the defined delay and the controller can leave the busy condition.
   对应摘录：A, B, C

# Modular supervisory control for multi-floor manufacturing processes - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多楼层制造流程中的水平搬运机器人和垂直电梯系统分别建成有限自动机，并明确给出状态、事件、转移和电梯门/急停约束，是一条完整的离散制造监督控制链。

## 条目 1: Modular Floor-and-Elevator Manufacturing Supervisor

- 控制对象：工业自动化与离散制造领域的多楼层制造物料转运监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于多楼层制造流程的模块化监督控制系统，把每层的水平搬运机器人和跨楼层的电梯式垂直物料搬运系统分别写成确定性自动机并组合调度。
- 判断：算。对象是真实制造过程中的物料转运控制系统，而不是纯离散事件系统方法论文；原文直接给出了每层机器人自动机和垂直电梯自动机的状态集合、事件字母表、转移函数以及门控、急停和直达目标层约束。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，Section `3`，行 181-240
> The states of the mobile robot system are four. The states of the platform are two ... the platform is still ... the platform is moving. The states regarding the manipulators are also two ... grippers ... open and ... low position ... grippers ... closed and ... high position. Thus, the set of the states ... are {(iq1,1,iq2,1), (iq1,1,iq2,2), (iq1,2,iq2,1), (iq1,2,iq2,2)}. The alphabet of the automaton is {ie1, ie2, ie3, ie4} ... The event ie1 is the command for the mobile robot system to start moving ... ie2 ... stop ... ie3 ... move the manipulators to the low position and open the grippers ... ie4 ... close the grippers and move the manipulators to the high position. ... The transitions of the automaton are ...

#### 摘录 B

- 出处：第 5 页，Section `3`，行 329-389
> If the car is aligned with the level of the i-th floor, then the state of the car is denoted by ql,i ... The set of the states of the motor is Qr = {qr,1, qr,2, qr,3, qr,4, qr,5}. If the car is stopped, then the motor is at state qr,1. If the car moves up with high speed, then the motor is at state qr,2. If the car moves up with low speed, then the motor is at state qr,3. If the car moves down with high speed, then the motor is at state qr,4. If the motor moves down with low speed, then the motor is at state qr,5. If the doors of all floors are closed, then the state of the doors is denoted by qd,1. If the door of at least one floor is open, then the state of the doors is denoted by qd,2. ... The set of all events of the elevator system is Ee = El ∪ Ea ∪ Eca ∪ Es ∪ {eo, ecl, eg, ee,a, ee,d}. ... Ge = (Qe, Ee, fe, He, xe,0, Qm,e) is the finite deterministic automaton of the elevator system.

#### 摘录 C

- 出处：第 6 页，Section `4.2 Desired behavior of the vertical material handling system`，行 434-447
> The desired behavior of the vertical material handling system, i.e., the elevator system, is analyzed to the following specifications: If at least one door is open, then the motor must stay stopped. ... if one door is open then all button events must be deactivated. If the call button of the ground floor or any send button at the rest floors is pressed, then the car must go to the ground floor without intermediate stations. If the call button from any floor is pressed, then the car must go directly to the requested floor without intermediate stations. ... If the emergency signal is activated while the car moves, then the car must stop immediately and remain stopped until the falling edge of the emergency signal takes place.

### 2. 基于原文整理后的自然语言描述

The multi-floor manufacturing process is controlled through a modular finite-state supervisor that separates horizontal material transfer on each floor from vertical transfer by the elevator system. For each floor, the mobile robot automaton has four explicit states formed by the cross-product of platform motion (`still` or `moving`) and manipulator posture (`open-low` or `closed-high`), and it reacts to start, stop, lower-open, and close-lift commands together with product-availability and terminal-switch events. The vertical handling part is modeled as another finite deterministic automaton whose state combines the car level, motor mode (`stop`, `up-high`, `up-low`, `down-high`, `down-low`), and whether any floor door is open. Its event alphabet includes level sensors, alignment sensors, call buttons, send buttons, door-open/door-closed events, and emergency rising/falling edges. The desired behavior is also explicit: doors open implies motor stop and button deactivation, floor requests must be served directly without intermediate stations, and an active emergency signal forces the car to stop and remain blocked until the emergency edge falls.

### 3. 逐句溯源

1. 句子 1：The multi-floor manufacturing process is controlled through a modular finite-state supervisor that separates horizontal material transfer on each floor from vertical transfer by the elevator system.
   对应摘录：A, B
2. 句子 2：For each floor, the mobile robot automaton has four explicit states formed by the cross-product of platform motion (`still` or `moving`) and manipulator posture (`open-low` or `closed-high`), and it reacts to start, stop, lower-open, and close-lift commands together with product-availability and terminal-switch events.
   对应摘录：A
3. 句子 3：The vertical handling part is modeled as another finite deterministic automaton whose state combines the car level, motor mode (`stop`, `up-high`, `up-low`, `down-high`, `down-low`), and whether any floor door is open.
   对应摘录：B
4. 句子 4：Its event alphabet includes level sensors, alignment sensors, call buttons, send buttons, door-open/door-closed events, and emergency rising/falling edges.
   对应摘录：B
5. 句子 5：The desired behavior is also explicit: doors open implies motor stop and button deactivation, floor requests must be served directly without intermediate stations, and an active emergency signal forces the car to stop and remain blocked until the emergency edge falls.
   对应摘录：C

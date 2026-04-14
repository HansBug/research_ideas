# Application of PLC for Elevator Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出了“呼梯后按方向运动并在限位信号处停靠”的主链，还补出了输入/输出配置、脉冲发生方式以及“已在目标层则不动作”的守卫。

## 条目 1: Level-Call Driven Elevator Motion
- 控制对象：楼宇机电领域的 PLC 电梯控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个单轿厢电梯控制器，用于根据楼层呼叫驱动轿厢上行或下行，并在目标层由限位开关反馈停靠。
- 判断：算。对象是实际电梯控制系统，原文直接描述了呼梯、正反转、位置反馈和停层逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Section 2, 行 98-109
> The working principle of PLC for elevator control system functions in the similar manner as that the elevator we use in our daily life. The motion of the elevator that people normally use is controlled by a stepper motor. It consists of a pulley which helps in upward and downward movement of the lift. The position feedback is provided by the limit switches. The principle of this set up is; whenever the cabinet is called to any level, the motor either runs in forward or reverse direction and then stops at the level indicated. The indication of the level or the position of the cabinet is given by the limit switches which act as a sensor and gives the signal indicating that the cabinet has reached the required position.

#### 摘录 B
- 出处：第 3 页，Section 3.3 `Interfacing of PLC with Elevator`，行 218-226
> PLC used in this set up is GE FANUC with six inputs and four
> outputs. ... The inputs are connected to three
> limit switches and three push buttons and the four outputs are
> connected to the stepper motor to generate a pulse. PLC consists
> of an on delay timer which is used to generate a pulse and also
> resets itself. A bit sequencer is also used in the program to
> generate four pulses continuously in sequence which is also used
> to change the direction of the motor. The program also consists
> of thirteen markers which are used as an internal output because
> of the less number of output ports.

#### 摘录 C
- 出处：第 3 页，`4. Results and Discussion`，行 242-251
> When push button for the first level is pressed then the motor
> runs in reversed condition till the cabinet reaches its required
> position and actuates the limit switch which enables the motor to
> stop and if the cabinet is already in the required position then the
> motor won’t get actuated.
> Again, when push button for the second level is pressed then the
> motor runs either in forward or reversed condition according to
> its position till the cabinet reaches its required position and
> actuates the limit switch which enables the motor to stop and if
> the cabinet is already in the required position then the motor will
> not get actuated and subsequently it worked successfully for
> other levels too.

### 2. 基于原文整理后的自然语言描述

The GE FANUC PLC uses six inputs and four outputs, with three push buttons and three limit switches feeding the controller while the four motor outputs are generated through an on-delay timer, a bit sequencer, and internal marker signals. When the elevator cabinet is called to a target level, the PLC drives the stepper motor in either the forward or reverse direction according to the requested level and the current position of the cabinet. The limit switches provide the position feedback that stops the motor when the required level is reached, and if the cabinet is already at the requested level then the motor is not actuated at all. In the reported trials, a first-floor call always drives the motor in reverse until the target limit switch is hit, while a second-floor call may run either forward or reverse depending on the current position.

### 3. 逐句溯源

1. 句子 1：The GE FANUC PLC uses six inputs and four outputs, with three push buttons and three limit switches feeding the controller while the four motor outputs are generated through an on-delay timer, a bit sequencer, and internal marker signals.
   对应摘录：B
2. 句子 2：When the elevator cabinet is called to a target level, the PLC drives the stepper motor in either the forward or reverse direction according to the requested level and the current position of the cabinet.
   对应摘录：A, C
3. 句子 3：The limit switches provide the position feedback that stops the motor when the required level is reached, and if the cabinet is already at the requested level then the motor is not actuated at all.
   对应摘录：A, C
4. 句子 4：In the reported trials, a first-floor call always drives the motor in reverse until the target limit switch is hit, while a second-floor call may run either forward or reverse depending on the current position.
   对应摘录：C

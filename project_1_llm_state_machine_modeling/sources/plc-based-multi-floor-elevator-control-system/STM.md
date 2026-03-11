# PLC based Multi-Floor Elevator Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文把电梯控制程序明确拆成上行/下行两部分，并给出了根据当前楼层和目标楼层决定电机方向的运行逻辑。

## 条目 1: Upward and downward traversal logic for a four-floor elevator
- 控制对象：四层 PLC 电梯的上行/下行遍历控制

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电与电梯控制领域的多层电梯驱动逻辑，用于根据当前楼层与请求楼层之间的关系决定上行、下行以及跨越一层到三层的遍历过程。
- 判断：算。对象是实际电梯控制器，原文明确给出了上行/下行划分、不同 traversals 和电机方向切换条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，程序逻辑描述，行 96-118
> The program is divided into two parts, upward traversal of the elevator and downward traversal of
> the elevator. Ea ch part is divided into three cases, one floor traversal, two floor traversal and three floor
> traversal. A counter is used to indicate the floor on which the elevator is currently present.
> Table 1 shows the input address and counter value corresponding to floor number.
> The ladder diagram includes the equality block, which will work only when the accumulator value
> of the counter, here represented as C5:0.ACC, equals the user defined integer value.
> Six timers have been used, three in upward motion and three in downward motion of elevator. The Timer
> Timing bit (TT bit) is used to run the motor. Output address O:0/0 and O:0/1 are used for the upward and
> downward m otion of motor respectively.
> 2.1.1.  Upward Motion
> Fig.2, fig.3 and fig.4 describe the logic that has been developed for one floor, two floor and three
> floor traversal respectively, and table 2 represents the operation of the elevator for upward motion.

#### 摘录 B
- 出处：第 6 页，运行结果与整体流程说明，行 381-390
> After interfacing the PLC with the elevator, followed by thorough checking of errors, the trials of
> the setup were done and the setup under consideration successfully worked. Fig.11 shows the flow chart of
> whole operation of PLC based elevator.
> The operation started with turning on of the s upply. When the push button for the desired floor was pressed
> and the elevator was on the same floor, the motor did not run. When the elevator was below the desired floor,
> the motor ran in clockwise direction. Thus, the elevator moved in the upward directi on. When it was above
> the desired floor, the motor ran in anti -clockwise direction. Thus, elevator moved in the downward direction.
> Similarly, when push button was pressed again, then the motor ran either in the forward or reverse
> direction according to it s position, till the elevator reached its required position and subsequently, it worked
> successfully for all possible combinations.

### 2. 基于原文整理后的自然语言描述

The PLC program for the four-floor elevator is organized into two main parts, upward traversal and downward traversal, and each part contains separate cases for moving across one floor, two floors, or three floors. The controller keeps a counter for the current floor and uses dedicated timers and outputs to drive upward and downward motor motion. After power-up, if the requested floor is the same as the current floor the motor does not run; if the car is below the requested floor the motor runs in the upward direction, and if it is above the requested floor the motor runs in the downward direction until the car reaches the required position.

### 3. 逐句溯源

1. 句子 1：The PLC program for the four-floor elevator is organized into two main parts, upward traversal and downward traversal, and each part contains separate cases for moving across one floor, two floors, or three floors.
   对应摘录：A
2. 句子 2：The controller keeps a counter for the current floor and uses dedicated timers and outputs to drive upward and downward motor motion.
   对应摘录：A
3. 句子 3：After power-up, if the requested floor is the same as the current floor the motor does not run; if the car is below the requested floor the motor runs in the upward direction, and if it is above the requested floor the motor runs in the downward direction until the car reaches the required position.
   对应摘录：B

# A Control System of Elevators by Using Programmable Logic Controller (PLC) - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接描述了双梯分区响应、到呼叫层开门、`2 sec` 开门计时、`3 sec` 保持和继续去目标层的顺序，结构很干净。

## 条目 1: Selective Dual-Elevator Dispatch with Timed Door Operation
- 控制对象：双电梯五层选择性调度控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电控制领域的双电梯 PLC 调度系统，用于按楼层分区响应呼叫、到层后开关门，并继续前往乘客目标层。
- 判断：算。对象是实际电梯控制系统，原文明确给出了楼层分配、传感检测、计时开门和继续运行顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Introduction，`paper_content.txt` 第 12-21, 31-37 行
> PLC is used as a controller for an elevator system that has two elevators with five floors. The PLC will control vertical movement of the two elevators either moving up or down simultaneously with only one PLC. The PLC also control opened and closed door process after the elevator had reached each level. The automation of this elevator process consists in providing technological means for its selective operation and control, such that the system as so conceived is enabled to deal with those situations for which a proper command has been implemented.
>
> This paper present work implementation of elevators that designed to perform selective operation to reduce congestion among passengers. The elevator designed for this project is the roped elevator type.

#### 摘录 B
- 出处：第 3-4 页，Flowchart / Sequence of the Flowchart，`paper_content.txt` 第 238-248, 298-309 行
> ELEVATOR CAR STOP AT CALLING LEVEL ... OPEN DOOR FOR 2 SEC TIMER ... HOLD FOR 3 SEC ... DOOR CLOSED ... ELEVATOR A GO TO DESIRED LEVEL ... ELEVATOR B GO TO DESIRED LEVEL.
>
> When the keypad of each level is pressed, one of the elevators responds. Elevator A responds to keypad pressed only at level 1, 2 and 3. Elevator B responds to keypad pressed only at level 4 and 5. Then each elevator will go to the called level and performed opened door operation. After the timer for the passengers to enter the elevator is off, the elevator will closed the door and continue to go to desired level and performed opened and closed door operation again.

### 2. 基于原文整理后的自然语言描述

The PLC controls two elevators serving five floors with a selective dispatch rule intended to reduce passenger congestion, and one PLC manages both cars' vertical motion and door operation. Calls from levels `1-3` are assigned to Elevator A, whereas calls from levels `4-5` are assigned to Elevator B. After the selected elevator reaches the calling level, it opens the door for a `2 sec` timer interval, holds for `3 sec`, closes the door, and then continues to the passenger's desired level. When the desired level is reached, the same open-and-close door sequence is executed again.

### 3. 逐句溯源

1. 句子 1：The PLC controls two elevators serving five floors with a selective dispatch rule intended to reduce passenger congestion, and one PLC manages both cars' vertical motion and door operation.
   对应摘录：A
2. 句子 2：Calls from levels `1-3` are assigned to Elevator A, whereas calls from levels `4-5` are assigned to Elevator B.
   对应摘录：B
3. 句子 3：After the selected elevator reaches the calling level, it opens the door for a `2 sec` timer interval, holds for `3 sec`, closes the door, and then continues to the passenger's desired level.
   对应摘录：B
4. 句子 4：When the desired level is reached, the same open-and-close door sequence is executed again.
   对应摘录：B

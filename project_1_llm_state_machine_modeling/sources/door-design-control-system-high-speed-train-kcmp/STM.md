# Door Design and Control System In High Speed Train - Case Study Kereta Cepat Merah Putih (KCMP) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把高速列车滑动塞拉门的控制边界明确分成 opening、closing 和 fault/trap 三类工况，并给出限位、过流/障碍检测与重开步骤，适合抽成车门控制 EFSM。

## 条目 1: Sliding-plug train door close-and-reopen trap controller

- 控制对象：轨道交通与铁路控制领域的高速列车滑动塞拉门开闭与防夹控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于高速列车乘客门的滑动塞拉门控制器，负责门体打开、关闭以及障碍/夹人故障时的重开保护。
- 判断：算。原文明确给出门控命令源、滑动与 plug 两级执行、限位反馈、障碍检测和 trap 重开逻辑，满足控制系统状态机样本要求。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> The scheme used in door control consists of opening, closing and action when there is fault or trap condition in operation.

#### 摘录 B

- 出处：第 3 页，Introduction / Methodology
> Entrapment accidents, such as fingers hitting doors and passengers accidentally being dragged by trains, are serious problems. ... research was carried out on the design of the door control system by paying attention to the fault condition in the design of the slidding plug door.

#### 摘录 C

- 出处：第 5 页，Safety
> The train door machine control and monitoring system is a system that aims to ensure the safety and comfort of train passengers. This system works by controlling and monitoring the train doors so that they can open and close properly, and ensure that no passengers are pinched or trapped inside the doors.

#### 摘录 D

- 出处：第 6 页，Security system steps
> To close the door Pressed Button Close and opomatis Motor sliding active for close. If not Obstacle occurred Motor sliding active for close and Sliding set parameter 1 (set target position for close 80% set speed normal) and Sliding set parameter 2 (set target position for close 100% set speed slow) until Limit Switch close active.

#### 摘录 E

- 出处：第 6 页，Security system steps
> If Limit Switch close active, Motor plug active for close and Target position plug is acquired. If Target position plug isn’t acquired, Motor plug active for close again until Target position plug is acquired.

#### 摘录 F

- 出处：第 6 页，Security system steps
> If any Obstacle occurred Motor sliding active for open, Sliding set parameter 1 (set target position open 2 set speed slow) and Sliding set parameter 2 (set target position open 1 set speed normal) until Limit Switch open active.

#### 摘录 G

- 出处：第 10 页，Conclusion
> Door control system that has 3 conditions in service to passengers, namely opening, closing and fault operation occurs. In normal operation, door opened and closed for passenger support then trap identification when passenger crashed by the door. The current sensor is used to identify trap condition.

### 2. 基于原文整理后的自然语言描述

The high-speed-train passenger door controller distinguishes three operating conditions: opening, closing, and fault or trap handling. When a close command is issued, the sliding DC motor first executes the sliding-close phase in two stages, moving toward `80%` closure at normal speed and then to `100%` closure at slow speed until the close limit switch becomes active. After the sliding stage is confirmed, the plug actuator executes the plug-close action and repeats until the target plug position is acquired. During closing, the controller monitors obstacle and over-current signals used to identify passenger entrapment. If an obstacle or trap condition is detected, the sliding motor reverses into the reopen sequence, runs through the open parameters, and continues until the open limit switch becomes active, after which the system can wait for a new close command.

### 3. 逐句溯源

1. 句子 1：The high-speed-train passenger door controller distinguishes three operating conditions: opening, closing, and fault or trap handling.
   对应摘录：A, G
2. 句子 2：When a close command is issued, the sliding DC motor first executes the sliding-close phase in two stages, moving toward `80%` closure at normal speed and then to `100%` closure at slow speed until the close limit switch becomes active.
   对应摘录：D
3. 句子 3：After the sliding stage is confirmed, the plug actuator executes the plug-close action and repeats until the target plug position is acquired.
   对应摘录：E
4. 句子 4：During closing, the controller monitors obstacle and over-current signals used to identify passenger entrapment.
   对应摘录：B, C, G
5. 句子 5：If an obstacle or trap condition is detected, the sliding motor reverses into the reopen sequence, runs through the open parameters, and continues until the open limit switch becomes active, after which the system can wait for a new close command.
   对应摘录：F

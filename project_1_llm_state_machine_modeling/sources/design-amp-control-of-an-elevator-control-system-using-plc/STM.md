# Design & Control of an Elevator Control System using PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：电梯门、停层、超载、低载节能与失电应急动作都给出了明确控制描述。

## 条目 1: PLC-based elevator car and door control
- 控制对象：PLC 三层电梯的轿厢与门控子系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电控制领域的 PLC-based elevator controller，用于在楼层之间移动轿厢、控制开关门并处理超载和失电等安全情形。
- 判断：算。对象是实际电梯控制系统，原文给出了门控、停层、超载保持停机和失电就近平层开门等离散行为。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Introduction，对 elevator control functions 的说明，行 33-35
> Elevator control system is needed to control all the functions
> of the elevator. It is the one which guides the elevator car ... between the different
> floors; it also controls the opening and closing of doors at different floor, and the safety switches are also controlled by

#### 摘录 B
- 出处：第 2 页，Sensors，对 doorway obstruction、floor hold 与 overload/low-load 的说明，行 79-83
> IR sensors are used for detecting object. It prevents the door closing when a person or object is present in between. It is
> also used to detect floor. The limit switches are used for holding a car in correct position at each floor. Load cell is used
> to measure weight present in car. Load cell also functions as occupancy sensor. when the weight is at or less than set
> minimum value for sufficient time then it make the fans and extra lights off and when the weight is more than max
> preset value, the control system will stop the motor. motor will not start until the load is dropped below maximum

#### 摘录 C
- 出处：第 2 页，Sensors，对 oxygen/power failure 触发的应急动作说明，行 84-87
> Oxygen sensor is the additional feature used in elevator. Whenever there is any failure in supply system
> and lift is blocked ... when it detects minimum set level it will give a signal to
> PLC so that car will be moved to nearest floor and will open the door.

### 2. 基于原文整理后的自然语言描述

The elevator control system guides the elevator car between floors, controls door opening and closing at each floor, and supervises the associated safety switches. Infrared sensing prevents the door from closing when a person or object is in the doorway, and limit switches hold the car in the correct position at each floor. The load cell introduces two additional guarded behaviors: when the car weight stays at or below the minimum value for sufficient time, the fan and extra lights are turned off, and when the weight exceeds the maximum preset value the motor is stopped and cannot start again until the load drops below that maximum. If the supply system fails and the oxygen level reaches the minimum set level while passengers are blocked inside, the PLC moves the car to the nearest floor and opens the door.

### 3. 逐句溯源

1. 句子 1：The elevator control system guides the elevator car between floors, controls door opening and closing at each floor, and supervises the associated safety switches.
   对应摘录：A
2. 句子 2：Infrared sensing prevents the door from closing when a person or object is in the doorway, and limit switches hold the car in the correct position at each floor.
   对应摘录：B
3. 句子 3：The load cell introduces two additional guarded behaviors: when the car weight stays at or below the minimum value for sufficient time, the fan and extra lights are turned off, and when the weight exceeds the maximum preset value the motor is stopped and cannot start again until the load drops below that maximum.
   对应摘录：B
4. 句子 4：If the supply system fails and the oxygen level reaches the minimum set level while passengers are blocked inside, the PLC moves the car to the nearest floor and opens the door.
   对应摘录：C

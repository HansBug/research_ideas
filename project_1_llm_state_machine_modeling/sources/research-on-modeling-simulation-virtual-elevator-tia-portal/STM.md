# Research on Modeling and Simulation of Virtual Elevator System Based on TIA Portal - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把六层虚拟电梯的呼梯、运行方向、平层、开关门、夹人和超重逻辑都写成可追溯的 PLC 控制链，并明确保留门延时与异常重开门规则，双 A 条件成立。

## 条目 1: Six-Floor Elevator Call-Direction-Door Supervisor

- 控制对象：楼宇机电与电梯控制领域的六层虚拟电梯 PLC 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `TIA Portal` 与虚拟 `HMI` 的六层电梯控制器，统一管理内外呼叫、运行方向、平层停车、开关门、夹人重开门和超重禁行。
- 判断：算。对象是论文的主控制系统，原文以 PLC 输入/输出刷新、流程图和测试表的方式明确写出了感知输入、门控/曳引执行器、方向决策、定时开门和异常联锁。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，`2.1 虚拟控制器结构及设置`，`paper_content.txt` 第 98-102 行
> 虚拟电梯的 PLC 控制系统主要由内外呼信号控制系统和轿厢和门电机牵引系统组成 ... 根据控制程序需要读取并在 CPU 中进行逻辑运算处理，再将结果存入输出映像寄存器，每个周期进行输出刷新 ... 向门机发出开关门控制信号，从而实现电梯运行状态的控制。

#### 摘录 B

- 出处：第 6 页，`3.2 电梯门控制程序` 与 `3.3 轿厢运行方向控制程序`，`paper_content.txt` 第 214-228 行
> 当轿厢到达平层停车后自动开门，开门设有延时，若无人进入则自动关门；若关门过程中，有人按下开门按钮或是电梯门闭合之间有人或者物品遮挡则自动转为开门状态；门全部关闭后，轿厢才可以运行。
>
> 当电梯轿厢到达目标楼层时 ... 平层停车，然后再执行开门程序。
>
> 每一层外呼按钮和轿厢内呼按钮有呼叫时，轿厢当前位置会和目标楼层位置比较来决定运行的方向。到达目标楼层后，之前按下的按钮命令会被消除。

#### 摘录 C

- 出处：第 9-10 页，`3.4 夹人超重报警控制程序`，`paper_content.txt` 第 262-274 行
> 当轿厢门闭合时中间有人或者物体时 ... 会触发夹人警报，轿厢门与层门会转变为打开状态 ... 关门程序才会响应。
>
> 当轿厢超重时，轿厢门与层门将保持打开，轿厢不执行上升与下降操作。

#### 摘录 D

- 出处：第 11-14 页，`4. 系统测试` 与 `5. 结论`，`paper_content.txt` 第 335-357、390-407 行
> 当接受到外呼的命令时，其按键相对应的指示灯会亮起，到达目标楼层后轿厢门会打开，其相应的按键指示灯会灭。
>
> 当出现夹人信号时，关门信号转变为开门信号，门电机处于正转状态，夹人报警指示灯亮。
>
> 包含平层停车、轿厢门与层门开合、轿厢上升下降、内外呼控制、定上、下行控制、楼层显示、夹人超重报警、故障检修。针对这些功能要求，设计的程序能准确地对其进行控制。

### 2. 基于原文整理后的自然语言描述

The virtual elevator controller is a PLC-driven supervisor for a six-floor elevator that cyclically reads hall calls, car calls, floor-position signals, obstruction/overweight inputs, and then refreshes door, traction, and indicator outputs every control cycle. When a destination is requested, the controller compares the current floor with the target floor to choose upward or downward travel, runs until the leveling sensors indicate arrival, clears the served request, and then executes the door-opening routine. The door logic is itself a timed sub-sequence: after leveling, the doors open automatically, remain open for a dwell interval, and then close unless an open-button request or an obstruction signal forces an immediate return to the open state. The same controller also contains safety interlocks for person trapping and overweight conditions, both of which hold the car in a door-open alarm state and inhibit further upward or downward movement until the abnormal condition is cleared. The test section confirms these call, leveling, door, and alarm chains through concrete scenarios such as `1F -> 4F` hall call service, `1F -> 6F` car-call travel, and obstruction-triggered reopen behavior.

### 3. 逐句溯源

1. 句子 1：The virtual elevator controller is a PLC-driven supervisor for a six-floor elevator that cyclically reads hall calls, car calls, floor-position signals, obstruction/overweight inputs, and then refreshes door, traction, and indicator outputs every control cycle.
   对应摘录：A, D
2. 句子 2：When a destination is requested, the controller compares the current floor with the target floor to choose upward or downward travel, runs until the leveling sensors indicate arrival, clears the served request, and then executes the door-opening routine.
   对应摘录：B, D
3. 句子 3：The door logic is itself a timed sub-sequence: after leveling, the doors open automatically, remain open for a dwell interval, and then close unless an open-button request or an obstruction signal forces an immediate return to the open state.
   对应摘录：B
4. 句子 4：The same controller also contains safety interlocks for person trapping and overweight conditions, both of which hold the car in a door-open alarm state and inhibit further upward or downward movement until the abnormal condition is cleared.
   对应摘录：C
5. 句子 5：The test section confirms these call, leveling, door, and alarm chains through concrete scenarios such as `1F -> 4F` hall call service, `1F -> 6F` car-call travel, and obstruction-triggered reopen behavior.
   对应摘录：D

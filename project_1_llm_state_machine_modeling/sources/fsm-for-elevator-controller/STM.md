# FSM for Elevator Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：报告把八层电梯的请求楼层比较、楼层传感、超时开门与超载停机写成同步控制链，虽然是课程项目报告，但原文可追溯细节足以形成楼宇机电方向的双 A 新样本。

## 条目 1: Eight-floor request-floor elevator supervisor

- 控制对象：楼宇机电与电梯控制领域的八层电梯楼层请求与安全门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向八层楼宇电梯的同步控制器，用请求楼层、当前楼层编码、超载输入和开门超时输入来决定上行、下行、到站驻留和安全停机。
- 判断：算。对象是实际 elevator controller，而不是单纯 HDL 语法示例；原文明确写出了楼层比较逻辑、门超时和超载保护、楼层传感器以及双向运行仿真。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-7 页，Abstract / Introduction，`paper_content.txt` 第 161-166、198-207 行
> A four -Phase lift controller modeled on Verilog HDL code using Finite State Machine (FSM) has been presented in this paper. Verilog HDL helps in automated analysis and simulation of lift controller circuit. This design is based on synchronous input that operates on a fixed frequency. The Lift motion is controlled by means of accepting the destination floor level as input and generate control signal as output.
>
> This project is designed for an eight floor elevator controller of an integrated circuit that can be used as part of elevator controller. The elevator decides moving direction by comparing request floor with current floor. In a condition that the weight has to be less than 4500lb and door has to be closed in three minute. If the weight is larger than it, the elevator will alert automatically. The Door Alert signal is normally low but goes high whenever the door has been open for more than three minute. There is a sensor at each floor to sense whether the elevator has passed the current floor.

#### 摘录 B

- 出处：第 9 页，Design Strategy，`paper_content.txt` 第 270-291 行
> First, we defined the input and output current floor as In_Current_Floor and Our_Current_Floor to avoid same variable name as output and input. Second, we add two more input pins - Over_time and Over_Weight in the code. These signals will be output from the mechanical machine to the controller. When the controller receives signal from weight alert or door alert, the complete will become one so that the elevator will stay unmoved at the Out_Current_Floor.
>
> ... when the Request_Floor is on, the variable In_Current_Floor is set to be equal to Out_Current_Floor only once. Then, In_Current_Floor stay the same, Out_Current_Floor keep changing (updating) and compare with request floor, until Out_Current_Floor is at the same level as Request_Floor.
>
> Lastly, define three cases of if statement for the elevator. There are cases for normal running cases - (comparing between Request_Floor and Out_Current_Floor to decide the moving direction), door open for more than three minutes - (turn on the Door_Alert) and overweight cases for elevator - (turn on the Weight_Alert).

#### 摘录 C

- 出处：第 19-20 页，Simulation Results，`paper_content.txt` 第 348、357 行
> The elevator moves up from eighth floor to ground floor.
>
> The elevator moves up from ground floor to eighth floor.

### 2. 基于原文整理后的自然语言描述

The elevator controller is an eight-floor synchronous EFSM whose core variables are the requested floor, the current floor, and two safety inputs for door timeout and overload. In nominal service, the machine compares `Request_Floor` with `Out_Current_Floor` to determine the travel direction, keeps updating floor position according to the per-floor sensors, and stops when the current-floor encoding reaches the requested level. The controller adds two explicit abnormal branches to that nominal travel loop: if the car stays overloaded beyond the allowed bound, `Weight_Alert` is raised and motion is inhibited; if the door remains open for more than `3 min`, `Door_Alert` is raised and the elevator is forced to stay at the current floor. The report also states that the design is an FSM-based four-phase lift controller and includes both `ground -> eighth floor` and `eighth -> ground` simulation paths, so the original text preserves bidirectional movement instead of only one travel branch.

### 3. 逐句溯源

1. 句子 1：The elevator controller is an eight-floor synchronous EFSM whose core variables are the requested floor, the current floor, and two safety inputs for door timeout and overload.
   对应摘录：A, B
2. 句子 2：In nominal service, the machine compares `Request_Floor` with `Out_Current_Floor` to determine the travel direction, keeps updating floor position according to the per-floor sensors, and stops when the current-floor encoding reaches the requested level.
   对应摘录：A, B
3. 句子 3：The controller adds two explicit abnormal branches to that nominal travel loop: if the car stays overloaded beyond the allowed bound, `Weight_Alert` is raised and motion is inhibited; if the door remains open for more than `3 min`, `Door_Alert` is raised and the elevator is forced to stay at the current floor.
   对应摘录：A, B
4. 句子 4：The report also states that the design is an FSM-based four-phase lift controller and includes both `ground -> eighth floor` and `eighth -> ground` simulation paths, so the original text preserves bidirectional movement instead of only one travel branch.
   对应摘录：A, C

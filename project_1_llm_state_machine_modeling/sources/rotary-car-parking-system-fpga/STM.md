# Hardware Design and Implementation of Automated Rotary Car Parking System on FPGA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把旋转立体停车系统的重量校验、车位计数、密码取车、最短路径旋转、消防联锁和停车计时都写成了可追溯的系统级控制链，足以形成双 A 的停车样本。

## 条目 1: Weight-Checked Rotary Parking Admission and Retrieval Supervisor

- 控制对象：智慧停车与车位管理领域的旋转立体车库入场、存取车与安全联锁控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 FPGA 的旋转立体停车监督控制器，用重量传感、车位传感、房间密码、温度传感和计时器来组织车辆入场、分配、取车、消防和计费。
- 判断：算。对象是实际旋转车库控制系统，而不是一般性 `FPGA` 平台说明；原文直接写出了重量门槛、入场/计数/取车条件、左右旋转规则、温度触发消防和停车时间计费逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 14-34 行
> This paper presents the design and implementation of an advanced hardware system for a fully automated rotary car parking solution deployed on a programmable chip ... The research presents an advanced FPGA-based rotary car parking system that automates vehicle management through real-time control and safety protocols ... implements safety measures, including weight compliance monitoring and password protection for vehicle retrieval ... incorporates temperature sensors for fire safety, activating suppression systems in case of high temperatures ... Directional sensors provide precise vehicle location tracking ...

#### 摘录 B

- 出处：第 4-7 页，Section 2 `Methodology`，`paper_content.txt` 第 159-168、180-202、224-248 行
> Initially, the system is implemented to assess each car's weight ... If the vehicle meets the required weight, it is allowed into the receiving bay; otherwise, access is denied ... the system alternates the direction of the rotating mechanism with each vehicle entry, moving either to the right or left.
>
> After a car enters the receiving bay, the system increments the internal car count, decreasing the count of available slots by one. Simultaneously, a time counter initiates ... When a user initiates a departure, the system verifies the legitimacy of the request by requiring a unique room password ... Upon correct password entry, the system locates the car ... activating the motor to rotate left or right as needed for efficient car retrieval.
>
> This algorithm determines the direction in which the motor should rotate left or right to retrieve a car ... If the car is parked in spaces 1 to 8, the motor rotates left; if the car is in spaces 9 to 15, it rotates right ... To process the exit, the user must first enter the correct password ... If the user enters an incorrect password, the timer continues to run, and the exit request is denied.

#### 摘录 C

- 出处：第 5-12 页，Section 2.3 / Results and Discussions，`paper_content.txt` 第 203-220、281-307、326-349 行
> Each parking bay is equipped with a temperature sensor ... If the temperature exceeds a predefined threshold, the alarm activates, and the water pump for the affected room engages ... Both the extinguishing system and the alarm remain active until the temperature returns to a safe level.
>
> Figure 9 shows the fire-extinguishing functionality. When the temperature sensor in a room detects a temperature of 50°C or above, both the alarm bell and water pump activate ... remain active until the temperature falls below 50°C ...
>
> Figure 14 illustrates the time count functionality ... When a user requests an exit, the total time in hours is multiplied by the hourly rate ... However, if the user enters an incorrect password, the counter continues but no payment is calculated ...
>
> Figure 15 displays the system's response in three situations: when the user enters an incorrect room code, when there are no available spaces in the rotary parking system, or when an exit request is made for an already empty room.

### 2. 基于原文整理后的自然语言描述

The FPGA controller organizes the rotary parking equipment as an integrated admission-storage-retrieval supervisor rather than a simple slot counter. It first checks the front and rear wheel loads against the allowed entry limits, admits only compliant vehicles into the receiving bay, increments the car count, starts the parking-time counter, and alternates lift rotation left and right to balance the mechanical load. On a departure request, the user must provide the correct room password, after which the controller locates the vehicle with room sensors and selects the shortest rotation direction, turning left for rooms `1-8` and right for rooms `9-15`, to bring the car back to the pickup area. In parallel, each bay monitors temperature and activates an alarm plus pump above the fire threshold, while incorrect passwords, empty-room requests, or full-capacity conditions block motion and keep the timer or error response active instead of executing retrieval.

### 3. 逐句溯源

1. 句子 1：The FPGA controller organizes the rotary parking equipment as an integrated admission-storage-retrieval supervisor rather than a simple slot counter.
   对应摘录：A, B
2. 句子 2：It first checks the front and rear wheel loads against the allowed entry limits, admits only compliant vehicles into the receiving bay, increments the car count, starts the parking-time counter, and alternates lift rotation left and right to balance the mechanical load.
   对应摘录：A, B
3. 句子 3：On a departure request, the user must provide the correct room password, after which the controller locates the vehicle with room sensors and selects the shortest rotation direction, turning left for rooms `1-8` and right for rooms `9-15`, to bring the car back to the pickup area.
   对应摘录：B
4. 句子 4：In parallel, each bay monitors temperature and activates an alarm plus pump above the fire threshold, while incorrect passwords, empty-room requests, or full-capacity conditions block motion and keep the timer or error response active instead of executing retrieval.
   对应摘录：A, C

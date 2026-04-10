# Development and Implementation of a Smart Parking Spot Allocation System Based on the User's Category and Priority using Verilog HDL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把类别优先停车位分配、同类空位搜索、回退到普通车位，以及成功分配后的道闸开闭链写得足够完整，可直接作为双 A 停车控制样本。

## 条目 1: Priority-aware parking-slot allocation and bar-gate controller

- 控制对象：智慧停车与车位管理领域的类别优先停车位分配与道闸控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个部署在停车场第二道闸入口的 `Verilog HDL + FPGA` 控制器，用用户类别按钮、车位 `IR` 传感器和道闸 `IR` 传感器共同决定分配哪个车位、何时开闸以及何时重新关闸。
- 判断：算。对象是实际停车系统的主控制链，不是单一显示模块或局部门禁逻辑；原文给出了类别优先级、最近空位搜索、同类满位时回退到普通车位，以及成功分配后的道闸控制顺序。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 41-51 行
> In this project, a prototype of a smart parking spot allocation system based on the user’s category and priority was developed. The choice of user categories is people with disabilities (OKU), pregnant women/elderly, women, and normal users. The highest priority is assigned to OKU, followed by pregnant women/elderly, followed by women and the lowest priority is assigned to normal users. ... The controller is programmed to process the user’s category which is selected by the user at the second entrance and assign a specific parking spot number according to the category’s priority.

#### 摘录 B

- 出处：第 3-4 页，`2.1 Design of Smart Parking Spot Allocation System`，`paper_content.txt` 第 185-199、208-214 行
> This “Smart Parking Spot Allocation System” is designed for a single-level parking area with twelve parking spots ... two parking spots were allocated for each pregnant woman/elderly and OKU user. While three parking spots were allocated for women users and the balanced five parking spots were assigned to normal users. Before the car can enter the parking area, there are two automatic bar gates. The first automatic bar gate will close automatically when all the parking spots have been filled ... At the second automatic bar gate, there is a selection panel for users to choose their category and obtain the allocated parking spot based on their category.
>
> The parking spots for OKU, pregnant women/the elderly, and women are all located near the mall entrance based the priority. ... To identify whether a parking spot is empty or not, several IR sensors equivalent to the total number of parking spots were installed at the parking spot connected to the Altera Board DE2-115.

#### 摘录 C

- 出处：第 5-7 页，`2.2 Verilog HDL Design ... / Fig. 5`，`paper_content.txt` 第 268-299 行
> The system begins with a welcome message displayed on the LCD (Example of welcome message: “Welcome to VIXX Mall”). If an IR sensor detects the presence of a car, the system will read the availability of all twelve parking spots using IR sensors. If a free parking spot is unavailable, the LCD will display “Sorry No Parking”. Otherwise, the LCD will display “Choose Type of Parking”. ... The choices of push-button are either button 1 for women or button 2 for pregnant women/the elderly or button 3 for OKU or button 4 for a normal user.
>
> For each category, the system will assign a parking spot based on the nearest parking spot to the mall entrance. ... If all the parking spots for the selected category are unavailable, the system will switch to the normal parking spot option.
>
> If the user successfully obtained their assigned parking spot number, the system would send a signal to the bar control module ... The automatic bar will immediately open using a motor. ... If the IR sensor detects that the car has not moved yet, the system will still open the bar. If the car has moved, the red LED light will illuminate, signaling the automatic bar to close.

#### 摘录 D

- 出处：第 11-12 页，`Fig. 17 / Fig. 18 / Fig. 19`，`paper_content.txt` 第 410-450 行
> The number "006" displayed on the next three seven segments as the assigned parking spot selected from available parking for women detected by IR sensor 6.
>
> the next three seven segments displayed "003" as the assigned parking spot because IR sensor 3 which is located at parking spot number 003 for pregnant women/elderly is available.
>
> Fig. 19(b), button 3 is selected, but parking spots for OKU are fully occupied. Therefore, the system automatically assigned a normal parking spot to the user where at this time normal parking spot number 010 is available ... and thus, seven segments displayed “010” as the assigned parking spot.

### 2. 基于原文整理后的自然语言描述

The parking controller starts at the second entrance gate with an LCD idle state that keeps showing `Welcome to VIXX Mall` until the gate-side `IR` sensor detects an arriving car. Once a car is detected, the controller reads all twelve parking-slot sensors; if every slot is occupied it raises the `Sorry No Parking` branch, and otherwise it switches to `Choose Type of Parking` and waits for one of the four category buttons `women / pregnant-elderly / OKU / normal`. For the selected category, the controller searches slots in priority order from the nearest place to the mall entrance to the farther ones and outputs the assigned slot number on the seven-segment display. If the requested privileged category is full, the machine falls back to the normal-parking branch instead of rejecting the vehicle immediately, as shown by the `OKU -> normal slot 010` example. After a slot number is successfully issued, the controller activates the bar-control module, opens the gate, keeps the barrier open while the gate `IR` sensor still sees the car in place, and closes the barrier once the car has moved through the entrance.

### 3. 逐句溯源

1. 句子 1：The parking controller starts at the second entrance gate with an LCD idle state that keeps showing `Welcome to VIXX Mall` until the gate-side `IR` sensor detects an arriving car.
   对应摘录：B, C
2. 句子 2：Once a car is detected, the controller reads all twelve parking-slot sensors; if every slot is occupied it raises the `Sorry No Parking` branch, and otherwise it switches to `Choose Type of Parking` and waits for one of the four category buttons `women / pregnant-elderly / OKU / normal`.
   对应摘录：A, B, C
3. 句子 3：For the selected category, the controller searches slots in priority order from the nearest place to the mall entrance to the farther ones and outputs the assigned slot number on the seven-segment display.
   对应摘录：A, B, C, D
4. 句子 4：If the requested privileged category is full, the machine falls back to the normal-parking branch instead of rejecting the vehicle immediately, as shown by the `OKU -> normal slot 010` example.
   对应摘录：C, D
5. 句子 5：After a slot number is successfully issued, the controller activates the bar-control module, opens the gate, keeps the barrier open while the gate `IR` sensor still sees the car in place, and closes the barrier once the car has moved through the entrance.
   对应摘录：C

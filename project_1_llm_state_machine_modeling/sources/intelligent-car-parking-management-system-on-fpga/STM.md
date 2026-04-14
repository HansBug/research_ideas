# Intelligent Car Parking Management System On FPGA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车场的引导入场、空位分配、带令牌校验的安全出场和基于停留时长的计费链路都写成了可追溯的 FPGA 控制模块，足以形成双 A 样本。

## 条目 1: Guided-Entry Secure-Exit Parking Controller

- 控制对象：智慧停车与车位管理领域的停车场引导入场、安全出场与车位计数控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 FPGA 的智能停车场管理控制器，使用入口/出口红外检测、空位与已占位计数、显示分配、出场安全码校验和按停留时长生成账单。
- 判断：算。对象是实际停车场运行控制系统，原文明确给出了入场、出场、安全码、账单和空位更新等控制模块及其事件链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`II. ALGORITHM / Car Entering Module`，`paper_content.txt` 第 63-66 行
> In Car Entering Module, as the car enters the lot, it is detected by the IR Sensors. The IR Sensors provide the pulse to the FPGA which assumes that an input is detected and thus the car is entered into the parking lot. Now as the car enters the lot, the car is directed to park in the first empty slot available.

#### 摘录 B

- 出处：第 2-3 页，`II. ALGORITHM / Car Exiting Module, Security Module, Invoice Module`，`paper_content.txt` 第 68-74、89-96 行
> In Car Exiting Module, as the car leaves the lot, it is detected by the IR Sensors ... This slot number should be tracked so that at exit we can display the right invoice and the security code, which the user will provide, is correctly matched.
>
> He will be only allowed to leave the Parking Lot, if the given code is correct.
>
> We have developed a procedure to calculate invoice. This formula keeps track of the time spent by each car in the Parking Lot.

#### 摘录 C

- 出处：第 3-4 页，`III. DESIGN AND IMPLEMENTATION / Flow charts of Entering and Exiting Module`，`paper_content.txt` 第 100-110、131-133 行
> When the car enters the Car park the sensors at the main entrance detects the arrival of the car ... if there is a free slot in the parking lot, the car is allowed to enter the car park and a security token is assigned to it ... the free locations or free slots are decremented by one and the allotted slots values are incremented by one.
>
> Initially the car is in the parked state, when it exits, the sensor in the slot detects it. After detecting the car the security token assigned is checked. If it is found correct the car is allowed to go to the next state which is the invoice payment.
>
> As soon as a car enters the lot, a space is reserved for it and the space number flashed on the Display ... It creates Invoice for each entering car ... For the security purpose, a security code is assigned to the arrived car and it is checked at the exit time.

### 2. 基于原文整理后的自然语言描述

The parking controller uses IR sensing at the lot boundary to detect vehicle entry and immediately directs the arriving car to the first empty slot instead of leaving the driver to search manually. During this entry path the system checks lot capacity, assigns a security token, updates the free-slot and allotted-slot counts, and displays the reserved space to the user. During exit, the slot-side sensor first detects that the parked vehicle is leaving, then the controller validates the previously assigned security code and advances to invoice payment only when the token matches. The same controller also keeps track of each car’s stay time so it can generate the invoice, and it restores the free-slot count after a validated departure.

### 3. 逐句溯源

1. 句子 1：The parking controller uses IR sensing at the lot boundary to detect vehicle entry and immediately directs the arriving car to the first empty slot instead of leaving the driver to search manually.
   对应摘录：A
2. 句子 2：During this entry path the system checks lot capacity, assigns a security token, updates the free-slot and allotted-slot counts, and displays the reserved space to the user.
   对应摘录：C
3. 句子 3：During exit, the slot-side sensor first detects that the parked vehicle is leaving, then the controller validates the previously assigned security code and advances to invoice payment only when the token matches.
   对应摘录：B, C
4. 句子 4：The same controller also keeps track of each car’s stay time so it can generate the invoice, and it restores the free-slot count after a validated departure.
   对应摘录：B, C

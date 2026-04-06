# PLC Based Intelligent Toll Road Traffic Control Using Solar Panel - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把收费道口的测速、超速罚款、车道满载改道、闸门单次/双次放行和路灯感应点亮写成了完整的输入-决策-执行链，是一条较少见的 toll-road 监督控制样本。

## 条目 1: Overspeed-fine and lane-reassignment toll-gate supervisor

- 控制对象：智能收费道口的车道分配与闸门放行控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个收费道口交通控制器，用 LDR 面板、摄像头、收费闸门、车道占满检测和路灯传感器管理超速处罚、车道改派和闸门放行。
- 判断：算。对象是实际收费道路控制系统，原文明确写出测速输入、超速罚款分支、满载换道分支、单次/双次闸门开启条件和沿线路灯跟随逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract / Introduction，`paper_content.txt` 第 4-16 行、第 37-58 行
> The system developed is able to sense the presence or absence of vehicles as the vehicle moves over the LDR panels. These LDR panels give their output to the PLC ... The new timing scheme promises an improvement in the current toll road traffic system.
>
> The Intelligent Toll Road Traffic Control System is an electronic automatism toll collection system ... collecting fine from over speeding vehicles and managing traffic on each toll lane. ... When a vehicle comes towards toll station the LDR panels fitted on the highway calculate its speed and sends the information to PLC. If it exceeds the speed limit value, then a fine is imposed ... The LDR panel also senses the maximum capacity of the toll lane and if the lane is fully occupied, then the vehicle is directed towards another lane.

#### 摘录 B

- 出处：第 1-2 页，`III. Methodology`，`paper_content.txt` 第 67-103 行
> Each panel consists of 8 pairs of LDRs. In each pair the LDR is placed one above the other and the distance between the 2 LDRs is 1 meter. When a car moves over the 1st LDR, and crosses the 2nd LDR, the output is send to PLC. From the output provided to PLC, the speed is calculated.
>
> If the speed of the car exceeds the speed limit then the picture of the number plate is captured and sent to PLC for fining process. Now when the car reaches the toll gate the driver has to pay a toll tax and also a fine for over speeding.
>
> Each toll lane of ITRTC consists of LDR panels. When all the LDRs in a particular toll lane detect the presence of a vehicle over them, then they send this output to the PLC. Then the PLC directs the car to another toll lane which is still vacant.

#### 摘录 C

- 出处：第 2-3 页，`IV. Process Description / Input Module / Output Module`，`paper_content.txt` 第 148-155 行、第 207-223 行
> Cameras are used to capture photos of the vehicle’s number plate. This information is given to PLC for checking the authentication of the vehicle registration. The switch is used to open the toll gate. Gates are controlled by the signal provided by the PLC. If any LDR panel senses an over-speeding vehicle, then the gates are opened by pressing the switch twice, otherwise gates are opened by pressing it only once.
>
> The driver can open the gate by pressing the gate switch once after paying the toll tax. But if a vehicle breaks the speed limit, then the toll gate opens by pressing the switch twice. Street lamps are controlled by the output of the LDRs provided to PLC ... If no vehicle passes the street lamp, then the lamp remains OFF. Camera provides photo image data of vehicle number plate. This is further processed by PLC for authentication of the vehicle.

### 2. 基于原文整理后的自然语言描述

The intelligent toll-road controller uses paired LDR panels as its primary input so the PLC can detect vehicle presence and compute speed from the time required to travel one meter between two sensors. If the measured speed exceeds the configured limit, the system captures the vehicle number plate, adds a fine to the toll transaction, and later requires a double gate-switch action for release instead of the normal single-switch opening. The PLC also watches whether all LDRs in a lane are occupied; if a toll lane is already full, the arriving vehicle is reassigned to another vacant lane rather than admitted into the saturated queue. In parallel, the same controller drives auxiliary behaviors such as vehicle-following street-lamp activation and number-plate authentication, so the overall control chain combines sensing, charging, gating, rerouting, and security checks in one supervised toll-road workflow.

### 3. 逐句溯源

1. 句子 1：The intelligent toll-road controller uses paired LDR panels as its primary input so the PLC can detect vehicle presence and compute speed from the time required to travel one meter between two sensors.
   对应摘录：A, B
2. 句子 2：If the measured speed exceeds the configured limit, the system captures the vehicle number plate, adds a fine to the toll transaction, and later requires a double gate-switch action for release instead of the normal single-switch opening.
   对应摘录：A, B, C
3. 句子 3：The PLC also watches whether all LDRs in a lane are occupied; if a toll lane is already full, the arriving vehicle is reassigned to another vacant lane rather than admitted into the saturated queue.
   对应摘录：A, B
4. 句子 4：In parallel, the same controller drives auxiliary behaviors such as vehicle-following street-lamp activation and number-plate authentication, so the overall control chain combines sensing, charging, gating, rerouting, and security checks in one supervised toll-road workflow.
   对应摘录：B, C

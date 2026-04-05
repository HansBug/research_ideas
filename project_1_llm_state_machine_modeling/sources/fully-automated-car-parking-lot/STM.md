# A Fully Automated Car Parking Lot - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车场入口判空、门禁放行、泊位驻留计时、计费回传和出口放行组织成一条 PLC 控制链，原文与描述都足够支撑双 A 样本。

## 条目 1: Sensor-Gated Slot Search and Parking-Billing Cycle

- 控制对象：全自动停车场的入口门禁、泊位计时与计费控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个停车场运营控制器，用入口/车位/出口传感器、PLC、屏显、栏杆和计时逻辑把“找空位-开闸-泊位驻留-计费-出场”串成离散控制流程。
- 判断：算。对象是真实停车场控制系统，原文不仅给出四阶段运行流程，还明确写出入口判空、栏杆开闸、泊位计时、金额计算、支付反馈与 WinCC 监控。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 24-35 行
> Most car parking lots in the country have not been fully automated and many of them serve temporal, manual parking needs. A fully automated car parking lot assures of flexibility, improved efficiency and minimisation of manual tasks.
>
> In this paper, use was made of Siemens Step 7 PLC and WinCC Flexible Advanced software to design a fully automated car parking lot. The number of parking spaces available, the parking space number and position, arrival and departure times of cars and the time spent at the parking space are provided by the design.

#### 摘录 B

- 出处：第 2-3 页，`Design Concept and Criteria / Mode of Operation of the Proposed Automated Car Parking Lot`，`paper_content.txt` 第 194-220 行
> Schematic diagram of the proposed fully automated car parking lot is as shown in Fig. 1. ... The barrier gate controls the parking lot accessibility. The retro-reflective sensor generates and sends information to the PLC. These sensors are provided at the car parking spaces, the exit and the entrance points.
>
> There are four operative stages of the automated car parking lot.
>
> Car at the parking lot: Position car within the demarcated area. The sensor senses the presence of a car and sends a signal to the PLC. The PLC searches through the program ... searches for empty car parking spaces. For example, three parking spaces are found, that is, parking spaces 1, 3 and 5. Display parking spaces 1, 3, 5 on LED display. ... The entrance barrier gate opens and this stage takes about 5 seconds.

#### 摘录 C

- 出处：第 3 页，`Mode of Operation of the Proposed Automated Car Parking Lot`，`paper_content.txt` 第 248-267 行
> Car at the parking space: There are two sub-stages at the car parking space namely, "car parked" and "car removed". For car parked, the sensor senses the presence of the car and sends information to the PLC. ... The corresponding output under satisfied conditions will start a timer.
>
> For the car removed: The same sensor sends information to the PLC. The timer stops because the car has been removed. Difference in time is calculated and the time spent is converted to corresponding money equivalent. Information is conveyed to the cash counter.
>
> Car at the Exit: Park car near the cash counter. Pay money into cash counter machine; wait for change or top up amount. Feedback is sent to the PLC. The PLC makes decisions based on the program and the barrier gate is opened. Car exits the car parking lot.

### 2. 基于原文整理后的自然语言描述

The fully automated parking-lot controller runs as a PLC workflow with four operative stages that cover entry detection, vacancy search, parking-space dwell tracking, payment handling, and exit release. When a car reaches the entrance, the sensor notifies the PLC, the program searches for empty spaces, the LED display reports candidates such as spaces `1`, `3`, and `5`, and the entrance barrier opens for about `5` seconds. After a car occupies a parking space, the local sensor starts a timer, and the same sensor later stops that timer when the car is removed so the system can compute dwell time and convert it into a monetary amount for the cash counter. At the exit, payment feedback is sent back to the PLC, which decides whether the exit barrier can open and then releases the car from the lot. The same control chain is integrated with WinCC Flexible Advanced so the parking process can also be monitored remotely.

### 3. 逐句溯源

1. 句子 1：The fully automated parking-lot controller runs as a PLC workflow with four operative stages that cover entry detection, vacancy search, parking-space dwell tracking, payment handling, and exit release.
   对应摘录：A, B, C
2. 句子 2：When a car reaches the entrance, the sensor notifies the PLC, the program searches for empty spaces, the LED display reports candidates such as spaces `1`, `3`, and `5`, and the entrance barrier opens for about `5` seconds.
   对应摘录：B
3. 句子 3：After a car occupies a parking space, the local sensor starts a timer, and the same sensor later stops that timer when the car is removed so the system can compute dwell time and convert it into a monetary amount for the cash counter.
   对应摘录：A, C
4. 句子 4：At the exit, payment feedback is sent back to the PLC, which decides whether the exit barrier can open and then releases the car from the lot.
   对应摘录：C
5. 句子 5：The same control chain is integrated with WinCC Flexible Advanced so the parking process can also be monitored remotely.
   对应摘录：A, C

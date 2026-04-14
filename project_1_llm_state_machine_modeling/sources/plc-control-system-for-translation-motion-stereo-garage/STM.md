# PLC Control System for Translation Motion Stereo-garage - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把待机、停车、取车、车位分配、排队执行和电机/传感器映射写成了完整车库存取控制链，足以形成高质量立体车库样本。

## 条目 1: Queued Slot Allocation and Retrieval Controller
- 控制对象：智慧停车领域的平移式立体车库存取控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定
- 一句话说明：这是一个面向平移式立体车库的 PLC 存取控制器，用车位分配、刷卡取车、平移/升降机构和安全检测来组织整套停车与取车流程。
- 判断：算。对象是实际立体车库控制系统，原文直接给出了待机、`parking / taking` 分支、队列式车位分配、执行机构、传感器与 I/O 规模。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 9-17 行
> A PLC (Programmable Logic Controller) control system for a stacker translation stereo-garage is presented in this paper. Firstly, the overall scheme of the stacker translation stereo-garage is proposed according to user requirement, and the structure scheme and automatic parking and taking flow of a vehicle are introduced in detail, especially the Queuing Theory is used to optimize the automatic control process.
>
> And then, based on the analysis on the technological requirements of the stacker translation stereo-garage, its PLC control system scheme is proposed. The proposed control system for stacker translation stereo-garage has simplicity of operator, and can realize full automatic control.

#### 摘录 B
- 出处：第 2-3 页，`Overall Scheme of the Stacker Translation Stereo-garage`，`paper_content.txt` 第 55-68 行
> The selection mechanism, which includes two mechanisms in horizontal and vertical direction, is used to select the parking space, and after selecting a parking space, the vehicle will be parked or took by the access mechanism. In order to automatically select the parking space, there are respectively four inspections in the horizontal and vertical direction. Two position detections are used to park or take a vehicle.
>
> The function of the limit switches SQ1-SQ4 is to ensure security when selecting the parking space. There is a state inspection in every parking space to judge whether a vehicle have already been parked in the parking space.

#### 摘录 C
- 出处：第 3 页，`Automatically parking and taking flow of a vehicle`，`paper_content.txt` 第 69-84 行
> Based on the Queuing Theory, the automatically parking and taking flow of a vehicle shown in Figure 2 is proposed to reduce the waiting time. As shown in Fig. 2, when the system is in standby mode, the vehicle owner could choose “parking” or “taking” according to the prompt. If “parking”, firstly the vehicle owner should park his vehicle in the right position in the floors, flame out and get off. And then he must been press the button “Parking”, the system will automatically arrange for a parking space to park his vehicle and pop up a card which the No. of the parking space has been written in. Finally the system begins to park the vehicles by No. of the parking space in queue until all vehicles are parked in the garage.
>
> If “taking”, firstly the vehicle owner should swipe the card, and then the system will automatically read No. in the card and takes the vehicle from the parking space.

#### 摘录 D
- 出处：第 3-4 页，`Analysis on Input and Output Electrical Appliances / PLC Control System`，`paper_content.txt` 第 79-112 行、第 122-133 行
> according to the structural scheme in Fig. 1 and control flow shown in Fig. 2, four motors and eights relays ... are required to realize automatically parking and taking flow. In order to know the running state of the translation motion stereo-garage, a two 8421 BCD code seven segment digital tube is used to display the parking space which has been selected to park or take a vehicle. Two indicator lights are used to the state of “Parking/Taking” and “Ready”.
>
> Table 1 Drive motor and its control electrical appliances ... selection mechanism translation ... lifting ... access mechanism translation ... lifting ...
>
> As shown in Table 3, the system needs 69 inputs and 19 outputs, and considering 3% -4% Remain, FX3U-80MR/DS base module and FX2NC-32EX extended module are selected. Furthermore, FX3U-232-BD communication module is used to link the card reader.

### 2. 基于原文整理后的自然语言描述

The stereo-garage controller uses a PLC to coordinate a selection mechanism and an access mechanism, with horizontal and vertical inspections, position detections, and limit switches `SQ1-SQ4` ensuring that a parking space is selected and reached safely before a vehicle is stored or retrieved. In standby mode, the operator chooses either `parking` or `taking`; the parking branch requires the vehicle to be positioned correctly, then after the `Parking` button is pressed the controller allocates a slot, issues a card containing the slot number, and executes storage according to that slot number. The taking branch starts from card swiping, reads the stored slot number, and commands the mechanism to fetch the vehicle from the addressed parking space. The realized PLC scheme maps this logic onto four motors, eight relay outputs, `Parking/Taking` and `Ready` indicators, a seven-segment slot display, and a `69`-input / `19`-output I/O configuration linked to the card reader.

### 3. 逐句溯源

1. 句子 1：The stereo-garage controller uses a PLC to coordinate a selection mechanism and an access mechanism, with horizontal and vertical inspections, position detections, and limit switches `SQ1-SQ4` ensuring that a parking space is selected and reached safely before a vehicle is stored or retrieved.
   对应摘录：A, B
2. 句子 2：In standby mode, the operator chooses either `parking` or `taking`; the parking branch requires the vehicle to be positioned correctly, then after the `Parking` button is pressed the controller allocates a slot, issues a card containing the slot number, and executes storage according to that slot number.
   对应摘录：C
3. 句子 3：The taking branch starts from card swiping, reads the stored slot number, and commands the mechanism to fetch the vehicle from the addressed parking space.
   对应摘录：C
4. 句子 4：The realized PLC scheme maps this logic onto four motors, eight relay outputs, `Parking/Taking` and `Ready` indicators, a seven-segment slot display, and a `69`-input / `19`-output I/O configuration linked to the card reader.
   对应摘录：D

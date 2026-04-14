# Analysis of PLC-Based Automated Dock Door Application in Vehicle Queuing System of Cold Chain - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把冷链装卸门的车辆识别、seal 展开、灭菌、开闭门、温度偏差回关与手动开关门都写成了明确 PLC 控制链，可直接形成双 A 样本。

## 条目 1: Sterilizing Dock-Door and Temperature-Hold Cycle
- 控制对象：冷链装卸区的 PLC 自动 dock door 与温控联动控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是冷链仓库装卸区的自动装卸门控制系统，用 proximity sensor、ID 校验、seal、灭菌、门电机和温度传感器协调 reefer pickup 的入位、装货和温度保持。
- 判断：算。对象是实际仓储机电控制系统，原文明确给出了事件顺序、限位条件、手动/自动模式、温度 setpoint 以及温差异常时的回关门逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，`4.2.4 Adjustment for Automated Dock Door Run Time`，`paper_content.txt` 第 350-375 行
> The automated dock door system installed on the loading dock will cause the original operating time data (based on the time of other vehicles) to change. This is because the system has a new procedure for handling reefer pickup when entering the loading dock. The reefer pickup procedure sequence when entering the loading dock to the dock door is: The reefer pickup enters the loading dock → the reefer pickup will be verified by the vehicle ID code by the proximity sensor → When the reefer pickup cabin position is stable on the dock shelter, the seal will expand → The dock shelter will sterilize the room as well as the reefer pickup cabin → after completion, the dock door will open automatically → the product can be loaded safely → the dock door will close again.
>
> 1 The time for the sensor verifying reefer pickup code ... 0.083
> 2 The time for the dock shelter deflating the seal ... 0.3
> 3 The time for the dock shelter doing sterilization ... 0.3
> 4 The time for the automated dock door opens and closes ... 1
> Total 1.683

#### 摘录 B
- 出处：第 5 页，`4.3.1 Automated Dock Door System Simulation`，`paper_content.txt` 第 450-478 行
> The system designed consists of room temperature control and dock door control. The system intended can be simulated with two types of power: automatic mode and manual mode. When the switch selector is ON, the system will be active, indicated by a green indicator light. When the system is active, the temperature sensor will display the current temperature conditions and activate the automated dock door control system. The temperature value read by the sensor (actual condition) will be compared with the system setpoint condition (-15 ℃). When the temperature is below -15 ℃, this condition is called a normal condition indicated by a green temperature indicator light. When the displayed temperature exceeds (above) -15 ℃, the system will turn on the purple temperature indicator light, and an alarm will sound.
>
> When the open sensor detects a recognized reefer pickup in the dock door system, the motor will be active with a yellow indicator light on. The dock door will open upward until the upper limit sensor is HIGH. When the upper limit sensor is HIGH, the motor will stop, which is indicated by the yellow indicator light goes out. When the close sensor detects the reefer pickup engine's condition, the motor will actively move to close down, which is indicated by a blue indicator light. The dock door will continue moving downwards until the lower limit sensor is HIGH. When the lower limit sensor is HIGH, the motor will stop, which is indicated by the blue indicator light goes out. The process of controlling the dock door can be done manually by pressing the START / STOP pushbutton. Pushbutton START functions to open the dock door manually. While the STOP pushbutton functions to close the dock door manually.

#### 摘录 C
- 出处：第 9 页，`4.4.1 Analysis of Automated Dock Door Design`，`paper_content.txt` 第 782-806 行
> Based on the simulation of the dock door system that has been designed in the CX-Designer software, the dock door will work if there is a registered reefer pickup approaching the dock shelter (the dock door system identifies the arrival of the reefer pickup via a proximity sensor embedded around the dock shelter). A registered reefer pickup is a vehicle that is indeed recognized by the automatic dock door system, which is a vehicle that has a unique identification or ID from the Distribution Warehouse. The ID will be verified in advance by the reader sensor embedded together with the proximity sensor. Once verified, the dock door system will activate chamber sterilization mode (as an effort to prevent the spread of Covid-19 by spraying disinfectant on the reefer pickup that enters the dock shelter) together with the seal on the lip of the shelter will actively expand (this expanding seal serves to compress the air so that the temperature between the cold storage and the outside storage area can be maintained during the loading process of the Ice Cream product into the reefer pickup cabin).
>
> Besides, this automatic dock door system also has a temperature sensor that functions to detect changes in temperature extremes, so that the dock door system can provide a marker when the temperature is unstable through the LED monitor information display and an alarm (buzzer) that will light up during the product loading process. So if the temperature in the dock door area and the dock shelter (actual) experiences a difference from the set temperature setpoint (for example: -15 ℃), the dock door will close for a while until the actual temperature returns to the set point.

### 2. 基于原文整理后的自然语言描述

The PLC-controlled dock-door system verifies each reefer pickup by proximity-sensor ID, waits for the vehicle to stabilize at the dock shelter, expands the seal, sterilizes the shelter and cabin, opens the door for loading, and closes the door again after loading. The engineered cycle uses explicit operation times of `0.083 min` for code verification, `0.3 min` for seal action, `0.3 min` for sterilization, and `1 min` for door opening and closing, for a total dock-door run time of `1.683 min`. In automatic mode the controller keeps the dock area around the `-15 ℃` setpoint, opens upward until the upper-limit sensor is HIGH, closes downward until the lower-limit sensor is HIGH, and also allows manual `START/STOP` pushbuttons to open or close the door directly. If the measured temperature rises above the setpoint during loading, the controller raises the purple temperature indicator and alarm and temporarily closes the dock door until the actual temperature returns to the setpoint.

### 3. 逐句溯源

1. 句子 1：The PLC-controlled dock-door system verifies each reefer pickup by proximity-sensor ID, waits for the vehicle to stabilize at the dock shelter, expands the seal, sterilizes the shelter and cabin, opens the door for loading, and closes the door again after loading.
   对应摘录：A, C
2. 句子 2：The engineered cycle uses explicit operation times of `0.083 min` for code verification, `0.3 min` for seal action, `0.3 min` for sterilization, and `1 min` for door opening and closing, for a total dock-door run time of `1.683 min`.
   对应摘录：A
3. 句子 3：In automatic mode the controller keeps the dock area around the `-15 ℃` setpoint, opens upward until the upper-limit sensor is HIGH, closes downward until the lower-limit sensor is HIGH, and also allows manual `START/STOP` pushbuttons to open or close the door directly.
   对应摘录：B
4. 句子 4：If the measured temperature rises above the setpoint during loading, the controller raises the purple temperature indicator and alarm and temporarily closes the dock door until the actual temperature returns to the setpoint.
   对应摘录：B, C

# Design and Implementation of a Reliable and Secure Controller for Smart Home Applications Based on PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接给出智能家居安防控制器的六状态图、传感器触发、`5 s / 10 s` 定时检查、报警输出和锁闭恢复逻辑，能够稳定提取成双 A 的楼宇安防 EFSM 样本。

## 条目 1: Smart-home intrusion alert and lockdown supervisor

- 控制对象：楼宇机电与电梯控制领域的 PLC 智能家居安防告警与安全屋锁闭控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个以 PLC 与 HMI 为核心的家庭安防控制器，围绕门廊运动、门限位、穿透式光电传感器、塔灯、警笛和锁闭安全屋组织六状态告警链。
- 判断：算。对象是真实楼宇安防控制器，原文既给出显式状态图，也给出触发条件、提示信息、报警输出、局部定时和复位动作，满足高质量 EFSM 提取条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> This paper proposes a PLC-based home security controller based on the ladder logic programming model. The design, analysis, and hardware implementation of this controller are presented in this paper. The designed system consists of three basic modules which are a sensing module used for reading the data of the input field devices for the smart home application, a computation-based decisional module used for executing the programming model, and an actuating module used for sending the control commands to the output field devices. The proposed home security system utilized different types of sensors such as a laser photoelectric sensor, a motion or proximity sensor, and a limit switch.

#### 摘录 B

- 出处：第 4 页，Table I / Fig. 4
> OFF When the “SYSTEM OFF” button is pressed on the HMI panel, a message “SYSTEM OFF” will appear
>
> ON Allowing sensors and system functionality to proceed by pressing the “SYSTEM RESET” button
>
> Alert_1 When there is a movement on the porch, system alert the homeowner with a message “PERSON ON PORCH” displayed on HMI panel AND the green light of the tower is turned on
>
> Alert_2 When the limit switch is tripped, a message “DOOR IS BREACHED” is displayed AND the yellow light of the tower is turned on
>
> Alert_3 When the through beam photoelectric sensor is tripped, a flashing message “INTRUDED IN HOUSE” will appear AND a siren will sound
>
> Lockdown if the “LOCKDOWN” button is pressed, this state locks the designated safe room automatically

#### 摘录 C

- 出处：第 4 页，The operation is described according to the following specifications
> When the system is ON and there is movement on the porch, the system will alert the homeowner with a message displayed on the HMI panel stating, “PERSON ON PORCH.” ... the sensor must be active for at least 5 seconds before notifying the homeowner. Additionally, the sensor is checked 10 seconds after engaging the ALERT 1 state. If the sensor is still active after 10 seconds, the ALERT 1 state remains true. If the sensor is inactive after 10 seconds, the state returns to false.
>
> When the limit switch is tripped once, the ALERT 2 state becomes true. The ALERT 2 state consists of displaying the message: “DOOR IS BREACHED” on the HMI panel.
>
> When the through beam photoelectric sensor is tripped, the alert 3 state is engaged causing the highest alert for the homeowner. A flashing message will appear on the HMI panel, which states: “INTRUDED IN HOUSE”. Furthermore, a siren will sound notifying the homeowner in case the control panel is out of sight.
>
> If the ALERT 3 state is active, the lockdown state will also become active. This state locks the master bedroom or designated safe room automatically. Additionally, if the “LOCKDOWN” button is pressed by the user on the HMI panel, the system will enter the lockdown state.

#### 摘录 D

- 出处：第 4-5 页，The operation is described according to the following specifications / Part 1
> When the system is powered on, the system is rendered inactive or in the OFF state. The OFF state can be engaged at any time by pressing the “SYSTEM OFF” button on the HMI panel.
>
> If the “SYSTEM ON” button is pressed, the system is rendered ON thus, allowing sensors and system functionality to proceed.
>
> The only way to reset the system while keeping the system ON is by pressing the “SYSTEM RESET” button.

### 2. 基于原文整理后的自然语言描述

The PLC-based smart-home security controller starts in `OFF` and moves into `ON` when the user enables the system from the HMI, which then activates the sensing chain. While in `ON`, porch motion must remain active for at least `5 s` before the controller raises `Alert_1`, lights the green tower lamp, and shows `PERSON ON PORCH`; the same branch is rechecked after `10 s` and cleared if the sensor goes inactive. A tripped door limit switch forces `Alert_2` with the yellow tower light and `DOOR IS BREACHED` message, while the through-beam photoelectric sensor triggers `Alert_3`, flashes `INTRUDED IN HOUSE`, and activates the siren. Whenever `Alert_3` is active, or whenever the user presses `LOCKDOWN`, the controller enters `Lockdown` and automatically locks the designated safe room. The only in-place recovery is `SYSTEM RESET`, which clears the alert chain while keeping the system powered and ready for renewed monitoring.

### 3. 逐句溯源

1. 句子 1：The PLC-based smart-home security controller starts in `OFF` and moves into `ON` when the user enables the system from the HMI, which then activates the sensing chain.
   对应摘录：A, B, D
2. 句子 2：While in `ON`, porch motion must remain active for at least `5 s` before the controller raises `Alert_1`, lights the green tower lamp, and shows `PERSON ON PORCH`; the same branch is rechecked after `10 s` and cleared if the sensor goes inactive.
   对应摘录：B, C
3. 句子 3：A tripped door limit switch forces `Alert_2` with the yellow tower light and `DOOR IS BREACHED` message, while the through-beam photoelectric sensor triggers `Alert_3`, flashes `INTRUDED IN HOUSE`, and activates the siren.
   对应摘录：B, C
4. 句子 4：Whenever `Alert_3` is active, or whenever the user presses `LOCKDOWN`, the controller enters `Lockdown` and automatically locks the designated safe room.
   对应摘录：B, C
5. 句子 5：The only in-place recovery is `SYSTEM RESET`, which clears the alert chain while keeping the system powered and ready for renewed monitoring.
   对应摘录：D

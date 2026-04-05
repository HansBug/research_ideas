# Modelling of Smart Car Parking System Using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车流程拆成入场引导、优先车位分配、密码解锁出场和报警保护，并明确给出 `10 s / 20 s` 工程定时。

## 条目 1: Priority-Slot Guidance and Passcode-Protected Unparking

- 控制对象：智慧停车领域的 PLC/SCADA 停车场导引与安全控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个停车场控制器，用于处理车辆入场、优先车位导引、车位占用保护、密码校验出场和异常报警。
- 判断：算。对象是实际停车控制系统，原文对入场、车位分配、密码解锁、运动传感器和报警联动给出了连续控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，`2. METHODOLOGY / 2.1 Entry of car / 2.2 Parking assistance / 2.3 Security / 2.4 Unparking of car`
> The parking spaces have been designed at an angle of 45o with the horizontal ... Each parking space has been provided with a motion sensor. The motion sensor remains OFF only for 10 seconds after the customer clicks the 'Park' button ... Once the car enters the area ... the parking assistance will be ON ... it will be guided to the available parking space through arrow shaped LEDs. The green colour LED glows as per the 'Priority method' ... A unique passcode for different parking slots would be generated ... The customer has to click on 'Unpark' ... fill in the correct passcode for unparking the car. If the customer fills the wrong passcode, another chance would be given failing which, security breach alarm would blow.

#### 摘录 B

- 出处：第 5-6 页，`3. SOFTWARE IMPLEMENTATION OF THE DESIGNED SYSTEM`
> It has been shown that the car count increases from 0 to 1 and the green light glows showing the availability of the empty parking spaces. When the car count would be 4, the red light would glow showing the unavailability of the empty parking space inside the area. ... The motion sensor remains OFF for a certain fixed amount of time after the parking of the car. If any external agent tries to enter the motion sensor area, the alarm along with the hooter blows. ... The parking of the car is carried out as per a 'priority method' ... On clicking 'Unpark', a 'Passcode Screen' opens on the 'Panel' ... A total of 2 chances would be given to fill in the right password within 20 seconds.

### 2. 基于原文整理后的自然语言描述

When a vehicle enters the facility and payment is accepted, the parking-assistance routine is enabled and the controller starts guiding the car to an available slot. The PLC/SCADA logic uses a priority method to decide which slot is filled first, shows green guidance toward the selected slot, and switches to red when the capacity count reaches four vehicles. After parking, the slot is protected by a motion sensor, and any unauthorized movement in the protected area triggers an alarm and hooter. To leave, the driver must press `Unpark` and enter the correct slot-specific passcode, which temporarily disables protection for about ten seconds; if the password is entered incorrectly twice within twenty seconds, the system raises a security-breach alarm instead of releasing the car.

### 3. 逐句溯源

1. 句子 1：When a vehicle enters the facility and payment is accepted, the parking-assistance routine is enabled and the controller starts guiding the car to an available slot.
   对应摘录：A
2. 句子 2：The PLC/SCADA logic uses a priority method to decide which slot is filled first, shows green guidance toward the selected slot, and switches to red when the capacity count reaches four vehicles.
   对应摘录：A, B
3. 句子 3：After parking, the slot is protected by a motion sensor, and any unauthorized movement in the protected area triggers an alarm and hooter.
   对应摘录：A, B
4. 句子 4：To leave, the driver must press `Unpark` and enter the correct slot-specific passcode, which temporarily disables protection for about ten seconds; if the password is entered incorrectly twice within twenty seconds, the system raises a security-breach alarm instead of releasing the car.
   对应摘录：A, B

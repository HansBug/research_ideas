# Modelling Of Smart Car Parking System Using Plc - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四车位 smart parking 写成 `entry -> guidance -> secured parking -> unpark/auth` 控制链，并给出 `10 s` 传感器抑制、`20 s` 密码重试窗口和 priority-based slot filling，足以形成停车方向的双 A 样本。

## 条目 1: Priority-guided passcode parking supervisor

- 控制对象：智慧停车与车位管理领域的 PLC/SCADA 车位引导与安全取车控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向四车位 smart parking 的停车监督控制器，用 priority-based slot filling、唯一 passcode、motion sensor 和报警逻辑来组织入场引导、占位保护和出场放行。
- 判断：算。对象是真实停车设施控制链，不是单纯界面展示；原文明确给出了 entry、guidance、security、unparking 和 alarm 条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Introduction，`paper_content.txt` 第 57-64 行
> The smart car parking system ensures a safe, secure and reliable parking facility for the people by providing parking assistance automatically to the drivers at the time of parking the vehicle.
>
> The priority is set for the parking of the cars in the available spaces. The security can be achieved by generating a unique security code for each parking space that is provided to the driver while entering the parking facility and that he/she has to enter before taking the car out of the parking space. This automation process can be easily achieved using a PLC and SCADA based system. The SCADA system can be used for the control and monitoring of the parking slots from a remote location also.

#### 摘录 B

- 出处：第 3-4 页，Methodology，`paper_content.txt` 第 98-125 行
> The parking spaces have been designed at an angle of 45o with the horizontal ... Each parking space has been provided with a motion sensor. The motion sensor remains OFF only for 10 seconds after the customer clicks the ‘Park’ button and the sensor may remain OFF for 5 minutes if the system is implemented in real time.
>
> Once the car enters the area ... the parking assistance will be ON ... Once the car gets into the parking zone, it will be guided to the available parking space through arrow shaped LEDs. The green colour LED glows as per the ‘Priority method’ set to avoid any conflict in the parking order.
>
> A unique passcode for different parking slots would be generated ... The customer has to click on ‘Unpark’ button ... fill in the correct passcode for unparking the car. If the customer fills the wrong passcode, another chance would be given failing which, security breach alarm would blow.

#### 摘录 C

- 出处：第 5-6 页，Results and Discussion，`paper_content.txt` 第 158-180、186-189 行
> It has been shown that the car count increases from 0 to 1 and the green light glows showing the availability of the empty parking spaces. When the car count would be 4, the red light would glow showing the unavailability of the empty parking space inside the area. ... The arrows shaped LEDs guide the car to the next available location which has further indication of green or red color based on the ‘Available’ or ‘Blocked’ slot respectively.
>
> The system has been designed such that the motion sensor turns OFF automatically only after the ‘Unpark’ button is pressed and correct password is entered in the ‘Passcode screen’ ... A total of 2 chances would be given to fill in the right password within 20 seconds.
>
> The first alarm blows when the customer fills the wrong password twice ... The second alarm blows if the motion sensor senses any movement in the parking slot with car already parked.

### 2. 基于原文整理后的自然语言描述

The smart parking controller is an EFSM for a four-car parking facility that combines entry admission, guided slot allocation, occupied-slot protection, and authenticated unparking. Once a car enters the facility, parking assistance is enabled and arrow LEDs guide the driver to the next available slot according to a fixed priority order; the occupancy display changes from green to red as the count moves from available to full. Every slot is protected by a unique passcode and a motion sensor. After a car is parked, the motion sensor remains active and is disabled only for about `10 s` after a valid unparking request, while the real deployment is expected to stretch that masking window to minutes. The exit branch begins with an `Unpark` request and a passcode screen, allows two password attempts within `20 s`, and raises a security-breach alarm if the code is wrong twice. In addition, if motion is detected inside an occupied slot without a valid unpark authorization, a second alarm and hooter branch is triggered. The paper also fixes a `45°` slot arrangement and PLC/SCADA realization, so it preserves both the parking-facility geometry and the full admission-protection-release control loop.

### 3. 逐句溯源

1. 句子 1：The smart parking controller is an EFSM for a four-car parking facility that combines entry admission, guided slot allocation, occupied-slot protection, and authenticated unparking.
   对应摘录：A, B
2. 句子 2：Once a car enters the facility, parking assistance is enabled and arrow LEDs guide the driver to the next available slot according to a fixed priority order; the occupancy display changes from green to red as the count moves from available to full.
   对应摘录：A, B, C
3. 句子 3：Every slot is protected by a unique passcode and a motion sensor.
   对应摘录：A, B
4. 句子 4：After a car is parked, the motion sensor remains active and is disabled only for about `10 s` after a valid unparking request, while the real deployment is expected to stretch that masking window to minutes.
   对应摘录：B
5. 句子 5：The exit branch begins with an `Unpark` request and a passcode screen, allows two password attempts within `20 s`, and raises a security-breach alarm if the code is wrong twice.
   对应摘录：B, C
6. 句子 6：In addition, if motion is detected inside an occupied slot without a valid unpark authorization, a second alarm and hooter branch is triggered.
   对应摘录：C
7. 句子 7：The paper also fixes a `45°` slot arrangement and PLC/SCADA realization, so it preserves both the parking-facility geometry and the full admission-protection-release control loop.
   对应摘录：B

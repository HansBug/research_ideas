# Parking Monitoring System with Security System Features - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把私有停车位的空位检测、密码校验、LCD 提示和闸门驱动写成了一条完整的门禁-监测控制链，原文细节足够支撑双 A。

## 条目 1: Password-Gated Parking Gate and Slot Monitor

- 控制对象：私有停车位的空位检测、密码门禁与闸门开闭控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是智慧停车与车位管理领域的私有停车位门禁控制器，用磁场/红外检测空位，用密码判断放行，并用步进电机驱动闸门。
- 判断：算。对象是实际停车控制系统，原文给出了空位检测、密码正确/错误分支、LCD 提示、闸门开门动作和步进电机驱动顺序。

### 1. 原文摘录

#### 摘录 A

- 出处：第 20 页，Background，对传感器与密码门禁主链的说明，`paper_content.txt` 第 688-705 行
> Magnetic field sensors will use in this project and it is a main part of the parking monitoring system.
>
> The sensor is design to detect the car at the car park and sent the data to the microcontroller.
>
> All the flow of the system will be completely control by microcontroller ... before someone is given to enter the car park.
>
> the user only have to put or key in their password and the gate will open. If the password is wrong, then the gate will remain close.

#### 摘录 B

- 出处：第 65-66 页，`Sytems flowchart the whole systems`，`paper_content.txt` 第 1849-1865 行
> “ACCESS GRANTED”
>
> LCD display “WELCOME”
>
> Password Insert. Correct?
>
> Sensor Detect Car
>
> LCD display “Free parking space Example = ‘C2’ ”
>
> LCD display “INSERT PASSWORD”
>
> LCD display “ACCESS DENIED”
>
> STEPPER MOTOR Open gate

#### 摘录 C

- 出处：第 68-70 页，`Flow Chart for Stepper Motor / KEYPAD`，`paper_content.txt` 第 1930-1954 行
> Start
>
> Data “CW” load to ACCA ... Stepper Motor Move Step by Step ... Data “CW+1” load to ACCA
>
> Keypad is used as the security for the system itself. The system will only functioning if the correct password is press.
>
> Otherwise LCD will display “ACCESS DENIED” and all the systems is malfunction.
>
> Each time when any key is press, DA will indicate a data is available. The 68HC11 will receive the data and display a character at the LCD.

### 2. 基于原文整理后的自然语言描述

The parking monitor starts from a guarded idle condition in which the microcontroller watches magnetic or infrared sensing points and reports an available parking slot on the LCD. When a car is detected and a free slot such as `C1` or `C2` is available, the controller prompts the user to insert a password before entry is granted. A correct password triggers the gate-opening branch, drives the stepper motor through its clockwise sequence, and opens the barrier so the vehicle can enter the private parking area. A wrong password instead drives the controller to an access-denied branch in which the gate remains closed and the system does not continue to the parking routine. The resulting controller is therefore an EFSM whose key guards are slot availability, car detection, and password correctness, and whose main outputs are LCD prompts and gate-motor commands.

### 3. 逐句溯源

1. 句子 1：The parking monitor starts from a guarded idle condition in which the microcontroller watches magnetic or infrared sensing points and reports an available parking slot on the LCD.
   对应摘录：A, B
2. 句子 2：When a car is detected and a free slot such as `C1` or `C2` is available, the controller prompts the user to insert a password before entry is granted.
   对应摘录：A, B
3. 句子 3：A correct password triggers the gate-opening branch, drives the stepper motor through its clockwise sequence, and opens the barrier so the vehicle can enter the private parking area.
   对应摘录：B, C
4. 句子 4：A wrong password instead drives the controller to an access-denied branch in which the gate remains closed and the system does not continue to the parking routine.
   对应摘录：A, B, C
5. 句子 5：The resulting controller is therefore an EFSM whose key guards are slot availability, car detection, and password correctness, and whose main outputs are LCD prompts and gate-motor commands.
   对应摘录：A, B, C

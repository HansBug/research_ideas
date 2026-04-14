# Automatic Railway Gate Control System Using Arduino Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路道口的预警、关闸、障碍阻止和开闸恢复写成了清晰的传感器驱动控制链，原文细节足以支持双 A 样本。

## 条目 1: IR-Countdown Railway Gate and Obstacle-Stop Controller

- 控制对象：轨道交通与铁路控制领域的铁路平交口门控与障碍保护控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Arduino 的铁路道口控制器，用红外传感器、计数器、蜂鸣器、道闸电机和激光-LDR 障碍检测链路来管理来车预警、关闸、开闸与障碍阻止。
- 判断：算。对象是真实道口门控控制系统，原文明确给出了传感器布置、触发顺序、灯光输出、倒计时预警和障碍阻止关闸的 guard。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Abstract，`paper_content.txt` 第 21-28 行
> The proposed system uses infrared sensors to detect the arrival and departure of trains at the railway level crossing and Arduino to control the opening/closing of gates. The system uses two IR sensors to detect the arrival of the train and a third IR sensor to detect the departure of the train. When the arrival of the train is sensed, signals are provided to the trac indicating the arrival of the train on the track. When the second sensor detects the train then the signal turns red and the motor operates to close the gate. The gate remains closed until the train completely moves away from the level cross. When the departure of the train is detected by the third sensor, the trac signal turns green and the motor operates to open the gate.

#### 摘录 B

- 出处：第 3 页，`3. System Overview`，`paper_content.txt` 第 73-78 行
> Sensor based railway gate automation system is developed to automate the process of opening and closing of gate at the railway level crosses. The system detects the arrival and the departure of  train for the gate operation using different types of sensors. The proposed system uses three infrared sensors to identify the arrival and departure of trains. The system also implements obstacle sensor which detects any obstacle on the track and controls the operation of the train. Sensors and servo motors are programmed using Arduino micro-controller.

#### 摘录 C

- 出处：第 4 页，`4. System Architecture`，`paper_content.txt` 第 95-118 行
> In India the maximum speed at which a train moves is 91.82km/hr and the minimum speed of a passenger/goods train is 59km/hr. Hence the ideal distance at which the sensors could be placed to detect the arrival of the train is 5km from the level cross and the departure of the train is 1km and thus the gate will not be closed for more than 8 minutes [1]. Our paper proposes a system which uses ve sensors, four IR Sensors (IR1, IR2, IR3 and IR4), a Light Dependent Resistor (LDR), a laser source (L), counter and one buzzer (B1).  In real time, the IR Sensors are placed on the track at a distance of 5km and 1km on both sides of the level crossing. The LDR and laser source is used to detect the presence of an obstacle between the railway gates. The system also uses DC motors to control the operation of the gates. The buzzer is used to indicate the arrival of the train within a stipulated time [6].
>
> IR1 detects the arrival of a train. Once it detects a train, it sends a signal to B1 and C1, and B1 is triggered and C1 starts count down, and yellow LEDs are switched on for the trac to know the arrival of the train. The train then travels to IR2. When the train nears IR2, DC motors are powered on. The DC motors starts and the gates begin to close. Parallel red LEDs are switched on. After the train passes the gates and nears IR3, a signal is again sent to the DC motors and the gates open and green LEDs are switched on for the road trac to pass. The laser source and LDR work simultaneously to detect obstacles in the path. The laser source continuously emits laser rays which reach the LDR. When the rays do not reach the LDR it means that there is some obstacle in the path and the gates do not close. A signal is also sent to the LEDs to signal the trains to stop as an obstacle is present.

### 2. 基于原文整理后的自然语言描述

The railway level-crossing controller uses an Arduino, four trackside IR sensors, a buzzer, a counter, DC gate motors, and a laser-LDR obstacle detector to automate warning, gate closing, reopening, and obstacle protection. The paper places arrival sensors and departure sensors at `5 km` and `1 km` on both sides of the crossing so the gate will not remain closed for more than about `8` minutes under the stated speed assumptions. When `IR1` detects an approaching train, the controller triggers the buzzer, starts the countdown `C1`, and turns on yellow warning LEDs for road traffic; when the train reaches `IR2`, the DC motors close the gates and the parallel road signals turn red. After the train clears the crossing and reaches `IR3`, the controller reopens the gates and switches the road signals to green, while the laser-LDR pair blocks gate closing and sends a stop indication instead whenever an obstacle interrupts the beam between the gates.

### 3. 逐句溯源

1. 句子 1：The railway level-crossing controller uses an Arduino, four trackside IR sensors, a buzzer, a counter, DC gate motors, and a laser-LDR obstacle detector to automate warning, gate closing, reopening, and obstacle protection.
   对应摘录：B, C
2. 句子 2：The paper places arrival sensors and departure sensors at `5 km` and `1 km` on both sides of the crossing so the gate will not remain closed for more than about `8` minutes under the stated speed assumptions.
   对应摘录：C
3. 句子 3：When `IR1` detects an approaching train, the controller triggers the buzzer, starts the countdown `C1`, and turns on yellow warning LEDs for road traffic; when the train reaches `IR2`, the DC motors close the gates and the parallel road signals turn red.
   对应摘录：A, C
4. 句子 4：After the train clears the crossing and reaches `IR3`, the controller reopens the gates and switches the road signals to green, while the laser-LDR pair blocks gate closing and sends a stop indication instead whenever an obstacle interrupts the beam between the gates.
   对应摘录：A, C

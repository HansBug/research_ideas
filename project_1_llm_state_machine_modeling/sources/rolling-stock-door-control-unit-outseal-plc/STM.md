# Development of a Rolling Stock Door Control Unit (DCU) using Outseal Programmable Logic Controller (PLC) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把列车滑门 DCU 的命令接收、门位反馈、编码器测速、超声防夹、`> 5 s` 回退判据和双设定值闭环关门过程写成了完整控制链，可直接作为铁路门控双 A 样本。

## 条目 1: Modbus-Connected Train Door Close-Loop and Anti-Trap Controller

- 控制对象：轨道交通与铁路控制领域的电动列车滑门 Door Control Unit
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向电动列车滑门的 PLC 门控单元，用 Modbus RTU 接收开关门命令，并结合磁性开闭传感器、旋转编码器、超声防夹和 PID 速度控制来完成关门过程。
- 判断：算。对象是实际列车门控制器，原文不仅说明了执行器和传感器集合，还给出了 `> 5 s` 防夹超时、双设定值速度控制、主从 Modbus 通信和门位闭环。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract 与 Introduction，`paper_content.txt` 第 9-29 行、第 67-86 行
> this research focuses on developing a Door Control Unit (DCU) to regulate the train doors' condition and manage the opening and closing speed. The DCU system relies on a Programmable Logic Controller (PLC) as its foundation, enabling seamless communication with other PLCs through the RS485 communication line using the Modbus RTU protocol in a master-slave configuration. ... The DCU employs a Proportional-Integral-Derivative (PID) control method with a closed-loop system, coupled with PWM Duty Cycle output adjustments.
>
> The train door control is a primary safety system. If the train door is not fully closed, the train cannot be operated by the driver. Additionally, the train door is designed not to open while the train is running at a specific speed. ... certain train doors do not utilize a closed-loop controller for each door, leading to time discrepancies between different doors during opening and closing operations.

#### 摘录 B

- 出处：第 2-3 页，`III. PROPOSED METHODS / A. Proposed System`，`paper_content.txt` 第 190-202 行、第 215-235 行
> The primary role of the Programmable Logic Controller (PLC) on the DCU panel is to act as the main controller, receiving commands from either the PLC Master or the Human Machine Interface through the Modbus RTU RS485 protocol. Additionally, the PLC on the DCU panel functions as a control system responsible for regulating the motor's rotation speed through the motor driver and reading the door sensors.
>
> The Brushless Direct Current Motor (BLDC Motor) operates as the actuator responsible for moving the door, rotating either clockwise or counterclockwise. The Magnetic Opened/Closed Sensor is utilized to detect the door's condition, whether it is opened or closed ... Additionally, a rotary encoder is mounted on the BLDC motor to track the number of rotations made by the BLDC motor during the door's opening or closing process.
>
> The Ultrasonic Sensor serves the purpose of detecting objects on the doors using ultrasonic waves, helping to identify any obstructions when the door is closing. The ESP32 acts as a controller for reading values from the ultrasonic sensor and the number of pulses from the Rotary Encoder. The collected data is processed on the ESP32 and then transmitted to the PLC via Modbus RTU communication.

#### 摘录 C

- 出处：第 4-6 页，`IV. EXPERIMENTAL RESULTS`，`paper_content.txt` 第 399-412 行、第 533-566 行
> The Anti Trap system that has been designed in the DCU uses 2 systems, namely based on readings from the calibration results on the ultrasonic sensor and the time on the timer that has been determined according to the standard. ... the Ultrasonic sensor can only read the condition if the detected object is < 100 cm, if the object is in a position > 100 cm from the top of the door then the anti trap system remains active using a time reading where the door does not close successfully > 5 seconds.
>
> The implementation of the trials carried out on the Sliding Door Electric PID speed control was carried out using 2 set points ... The speed set point value of 85 RPM will be set if the door movement distance is < 800 mm and the speed set point value of 35 RPM will be set if the door movement distance is > 800 mm. ... The results of closing the door lasted 4.2 s ... the door moves with a set point of 85 RPM for 2.2 s and a change in set point to 35 RPM occurs in 2.3 s.

#### 摘录 D

- 出处：第 6-7 页，`D. Testing the Modbus RTU... / V. CONCLUSIONS`，`paper_content.txt` 第 580-609 行、第 649-667 行
> The communication protocol design for the DCU employs the Modbus RTU communication protocol. ... By using the Outseal PLC as the master, the DCU can seamlessly integrate with sensors having individual reading modules through the Modbus RTU protocol.
>
> By receiving commands from the TCMS via the Modbus RTU RS485 protocol, the DCU can effectively control the opening and closing of doors, enhancing train operation and safety.
>
> functioning as a slave, the Modbus RTU DCU can be effectively controlled by the primary control device within a train, receiving commands such as open, close, and anti-trap detection.

### 2. 基于原文整理后的自然语言描述

The train-door DCU is an Outseal PLC-based controller that receives open and close commands from a PLC master, HMI, or TCMS over Modbus RTU RS485 and then regulates a BLDC door motor through a motor driver and PWM/PID speed control. Its state estimation depends on several feedback channels at once: magnetic opened/closed sensors report end conditions, a rotary encoder measures door travel, and an ultrasonic sensor connected through ESP32 provides obstacle information during closing. For safety, the anti-trap logic has two parallel guards: it reacts to ultrasonic detection when an object is within `100 cm` from the top of the door, and it also treats a door-closing attempt that remains unsuccessful for more than `5 s` as an anti-trap condition. During closing, the controller uses a two-set-point profile, switching between `85 RPM` and `35 RPM` according to the measured door-travel distance around the `800 mm` threshold, and the reported closed-loop process reaches the required `4.2 s` standard closing time. Because the train cannot safely depart with an incompletely closed door, the resulting sample is a railway EFSM with command states, sensor-confirmed end states, timed anti-trap recovery, and distance-based speed adjustment.

### 3. 逐句溯源

1. 句子 1：The train-door DCU is an Outseal PLC-based controller that receives open and close commands from a PLC master, HMI, or TCMS over Modbus RTU RS485 and then regulates a BLDC door motor through a motor driver and PWM/PID speed control.
   对应摘录：A, B, D
2. 句子 2：Its state estimation depends on several feedback channels at once: magnetic opened/closed sensors report end conditions, a rotary encoder measures door travel, and an ultrasonic sensor connected through ESP32 provides obstacle information during closing.
   对应摘录：B
3. 句子 3：For safety, the anti-trap logic has two parallel guards: it reacts to ultrasonic detection when an object is within `100 cm` from the top of the door, and it also treats a door-closing attempt that remains unsuccessful for more than `5 s` as an anti-trap condition.
   对应摘录：C
4. 句子 4：During closing, the controller uses a two-set-point profile, switching between `85 RPM` and `35 RPM` according to the measured door-travel distance around the `800 mm` threshold, and the reported closed-loop process reaches the required `4.2 s` standard closing time.
   对应摘录：C
5. 句子 5：Because the train cannot safely depart with an incompletely closed door, the resulting sample is a railway EFSM with command states, sensor-confirmed end states, timed anti-trap recovery, and distance-based speed adjustment.
   对应摘录：A, D

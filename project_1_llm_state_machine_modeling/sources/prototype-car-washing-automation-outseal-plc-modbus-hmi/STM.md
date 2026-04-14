# Prototype of Car Washing Automation and Monitoring System Using Outseal PLC and Modbus HMI - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把洗车线的车辆检测、顺序执行、远程监控和阶段响应写成了完整 PLC 工艺链，虽然与现有洗车样本邻近，但仍满足双 A 收录条件。

## 条目 1: Sensor-Triggered Conveyor Car-Wash Sequence with Modbus Monitoring

- 控制对象：工业自动化与离散制造领域的 Outseal PLC 洗车线顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🧰 清洗后保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向小型洗车线的 PLC 自动控制系统，用红外接近传感器检测车辆，并按既定逻辑驱动输送带、喷皂泵、刷洗机构、清水泵和风机，同时通过 Modbus HMI 远程监控。
- 判断：算。对象是实际服务业自动化控制系统，原文直接给出了执行链、输入输出部件、手动按钮、远程监控接口和各阶段响应结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract 与 Introduction，`paper_content.txt` 第 21-42 行、第 74-83 行
> This research aims to design and develop a prototype of an automatic car washing system using Outseal PLC and Modbus HMI ... The prototype integrates infrared proximity sensors, DC gearbox motors, DC pumps, DC fans, and a conveyor system controlled by a ladder diagram programmed through Outseal Studio.
>
> The system successfully automated all stages of the car washing process, including soap spraying, brushing, rinsing with clean water, and drying ...
>
> The system is designed to automate the entire car washing process, including soap spraying, brushing, rinsing with clean water, and drying using a conveyor system for vehicle movement. Infrared proximity sensors are utilized to detect vehicle presence and trigger the washing stages automatically.

#### 摘录 B

- 出处：第 2-3 页，`METHOD`，`paper_content.txt` 第 123-153 行、第 166-176 行
> The system integrates an infrared proximity sensor for vehicle detection, push buttons for manual control, DC pumps for soap spraying and water rinsing, a DC gearbox motor for conveyor movement, a DC fan for the drying process, relays for actuator switching, a PWM module for speed regulation, and the DT-06 WiFi module for wireless communication. The Outseal PLC functions as the main controller programmed using Outseal Studio software, while the Modbus HMI allows users to monitor and control the system remotely through an Android device.
>
> 1 Outseal PLC 12 input / 8 output Main controller for automation ... 3 IR Proximity Sensor ... Vehicle presence detection ... 4 DC Gearbox Motor ... Drives the conveyor ... 5 DC Pump ... Soap spraying and water rinsing ... 6 DC Fan ... Drying stage ...
>
> The proximity sensor detects the presence of the vehicle on the conveyor and sends signals to the PLC, which then activates relays to control the soap pump, brush, clean water pump, dryer, and conveyor sequentially according to the programmed logic. The HMI monitors the system status, sensor conditions, and actuator states while enabling users to control the system remotely via WiFi connectivity.

#### 摘录 C

- 出处：第 4-5 页，`RESULT / DISCUSSION / CONCLUSION`，`paper_content.txt` 第 235-250 行、第 266-279 行、第 311-319 行
> The system responded promptly to input signals, with response times ranging from 0.14 to 0.3 seconds, ensuring synchronous and efficient operation throughout the washing process.
>
> The sensors demonstrated a high level of accuracy with an error margin between 2% and 3.2% ... ensuring reliable detection necessary for triggering the automated washing stages.
>
> The prototype was tested under real conditions, and the system was able to operate automatically in executing all washing stages with the vehicle moving through each stage on the conveyor. The integration of the Modbus HMI allowed the operator to monitor the status of each stage, observe actuator conditions, and control the process remotely using a mobile device.
>
> The system was able to automate the entire washing process, including soap spraying, brushing, rinsing, and drying, with responsive control and high detection accuracy using infrared proximity sensors.

### 2. 基于原文整理后的自然语言描述

The car-wash controller uses an Outseal PLC as the main decision unit and combines an infrared proximity sensor, manual push buttons, a conveyor motor, soap and clean-water pumps, a brush stage, a dryer fan, relays, PWM speed regulation, and a WiFi-connected Modbus HMI. Once a vehicle is detected on the conveyor, the PLC executes a programmed stage sequence in which the conveyor and actuators are driven in order to perform soap spraying, brushing, rinsing, and drying. The HMI is not a passive display only: it reports sensor and actuator states and allows remote supervision and control over the process through WiFi communication. The reported implementation reacts to stage inputs within roughly `0.14-0.31 s`, and the proximity sensor accuracy remains within `2-3.2%`, which the paper explicitly ties to reliable triggering of the washing stages. The resulting sample is therefore a service-industry EFSM whose state progression is organized around vehicle detection, sequential stage activation, and stage-status monitoring rather than around a single motor-control loop.

### 3. 逐句溯源

1. 句子 1：The car-wash controller uses an Outseal PLC as the main decision unit and combines an infrared proximity sensor, manual push buttons, a conveyor motor, soap and clean-water pumps, a brush stage, a dryer fan, relays, PWM speed regulation, and a WiFi-connected Modbus HMI.
   对应摘录：A, B
2. 句子 2：Once a vehicle is detected on the conveyor, the PLC executes a programmed stage sequence in which the conveyor and actuators are driven in order to perform soap spraying, brushing, rinsing, and drying.
   对应摘录：A, B
3. 句子 3：The HMI is not a passive display only: it reports sensor and actuator states and allows remote supervision and control over the process through WiFi communication.
   对应摘录：B, C
4. 句子 4：The reported implementation reacts to stage inputs within roughly `0.14-0.31 s`, and the proximity sensor accuracy remains within `2-3.2%`, which the paper explicitly ties to reliable triggering of the washing stages.
   对应摘录：C
5. 句子 5：The resulting sample is therefore a service-industry EFSM whose state progression is organized around vehicle detection, sequential stage activation, and stage-status monitoring rather than around a single motor-control loop.
   对应摘录：A, B, C

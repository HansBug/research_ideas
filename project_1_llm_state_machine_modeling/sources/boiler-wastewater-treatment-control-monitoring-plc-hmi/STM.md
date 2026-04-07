# Design Control and Monitoring System for Boiler Wastewater Treatment Process Using Programmable Logic Controller and HMI (Human Machine Interface) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把锅炉废水处理的单元流程、`Auto / Manual` 模式、PLC I/O、回流闭环和 HMI 监控链写得很细，是过程控制方向可靠的双 A 样本。

## 条目 1: Auto-Manual WWTP Supervisor with Conductivity-Feedback Return Loop

- 控制对象：过程与环境控制领域的锅炉废水处理与监控控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于锅炉废水处理厂的 PLC 监督控制器，负责在自动/手动模式下协调泵、阀、搅拌器、传感器和回流旁路，以保证出水质量达标。
- 判断：算。对象是真实过程控制系统，原文明确给出了处理单元、输入输出设备、闭环回流 guard、自动/手动模式职责和 HMI 面板中的操控边界。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，Abstract 与 `Work Process Flow chart`，`paper_content.txt` 第 18-33 行、第 166-172 行
> we conducted research that is designing a system to control and monitor the process at the wastewater treatment plant automatically. The design of this control system is done by adding sensors and actuators that are connected to the modular PLC that is the control system. This system is also designed to be connected to a PC as a monitoring system so that the process can be monitored continuously.
>
> The boiler wastewater treatment plant consists of treatment units and a tool for treating wastewater. Wastewater treatment units consist of equalization units, coagulation units, flocculation units, clarifier units, and final tank units.

#### 摘录 B

- 出处：第 4-5 页，`Control System Design / Design of Control Devices and their Specifications`，`paper_content.txt` 第 243-286 行、第 295-334 行
> The design of the control system includes the design of control devices, input, and output devices on the PLC ... Figure 4 shows the number of inputs and outputs used in the design of this control system. The system uses 16 inputs and 18 outputs with details of 12 digital input devices, two analog input devices, 16 digital output devices, and two analog output devices.
>
> Input
> Motorized Valve PAC
> Motorized Valve Polymer
> pH Sensor
> Conductivity Sensor
> ...
> High Equalization Water Level Sensor
> Low Equalization Water Level Sensor
> High Final Tank Water Level Sensor
> Low Final Tank Water Level Sensor
> ...
> Output
> Intake Pump Relay
> Agitator Relay
> PAC Pump Relay
> Polymer Pump Relay
> Flocculation Unit Mixer Relay
> Coagulation Unit Mixer Relay
> ...
> Solenoid Valve Blow down
> Solenoid Valve Out

#### 摘录 C

- 出处：第 5 页，`The control system becomes the closed-loop system`，`paper_content.txt` 第 336-364 行
> The process control system of the wastewater treatment plant is designed by adding a conductivity sensor to the final tank unit, adding a new pipeline to the equalization unit, and adding a solenoid valve in the pipeline. So that the control system becomes a closed control system, where the incoming wastewater will be processed and reviewed by a conductivity sensor. The value of the conductivity sensor reading will be processed by the PLC and given feedback to the system whether the processed water is disposed of or not. If the reading value is in the safe number, the water will be discharged into the water channel. However, if the reading value is at a high rate, the water will flow back to the equalization unit so that the process water that is discharged into the water channel is water that meets the standards and is free of hazardous and toxic material content.

#### 摘录 D

- 出处：第 5-7 页，`Flow chart / Interface Design / Quality of water`，`paper_content.txt` 第 378-406 行、第 443-452 行、第 511-537 行
> There are two methods in the process of treating waste in the system ... The first method is to use an auto mode which parameter settings and activation of the supporting system of the system is carried out in full by the program sequence by utilizing the input values of the input devices (sensors, selector switches, pushbuttons) connected to the PLC so that the system can run without manual input performed by the operator. While the operation of the plant with the second method is manual mode, the operator must activate the system supporting devices manually and set its parameters so that the system can treat waste properly.
>
> In the main panel window, there is a main control tab that functions to activate and stop the system and choose the system mode, the actuator tab to display the actuator (pump, solenoid valve) which is active, the analog value tab to display the analog value, the manual activation tab to activate the pump in manual mode ...
>
> The design of the process control system for wastewater treatment uses a pH sensor as a detector for the pH value of the flocculation unit. Whereas the conductivity sensor ... will be a parameter to determine the size of the motorized control valve opening and whether the solenoid valve bypass is used as a programmatic opening and closing device ... If water is > 1500 ppm, it will flow back to the equalization unit.

### 2. 基于原文整理后的自然语言描述

The boiler-wastewater controller supervises a full treatment chain that spans `equalization`, `coagulation`, `flocculation`, `clarifier`, and `final tank` units rather than only one isolated pump or valve module. Its PLC design explicitly binds together `16` inputs and `18` outputs, including `pH`, conductivity, and water-level sensors together with motorized valves, intake and transfer pumps, mixers, and blowdown or outlet solenoid valves. The controller exposes two main operating modes: in `auto mode` the PLC runs the whole supporting sequence from sensor, selector, and pushbutton inputs without further operator intervention, while in `manual mode` the operator directly activates pumps and adjusts parameters through the HMI main panel. A conductivity sensor in the final tank closes the loop by deciding whether processed water is released to the water channel or routed back through a new pipeline to the equalization unit, and the same HMI also surfaces analog values, active actuators, and manual override tabs so the operator can monitor or intervene when the plant is not following the normal automatic path. The paper further ties this supervisory logic to quality constraints by using pH and conductivity readings to parameterize control-valve opening and bypass decisions, ensuring that outflow water stays within the required `pH 6-9` and `<1500 ppm` limits.

### 3. 逐句溯源

1. 句子 1：The boiler-wastewater controller supervises a full treatment chain that spans `equalization`, `coagulation`, `flocculation`, `clarifier`, and `final tank` units rather than only one isolated pump or valve module.
   对应摘录：A
2. 句子 2：Its PLC design explicitly binds together `16` inputs and `18` outputs, including `pH`, conductivity, and water-level sensors together with motorized valves, intake and transfer pumps, mixers, and blowdown or outlet solenoid valves.
   对应摘录：B
3. 句子 3：The controller exposes two main operating modes: in `auto mode` the PLC runs the whole supporting sequence from sensor, selector, and pushbutton inputs without further operator intervention, while in `manual mode` the operator directly activates pumps and adjusts parameters through the HMI main panel.
   对应摘录：D
4. 句子 4：A conductivity sensor in the final tank closes the loop by deciding whether processed water is released to the water channel or routed back through a new pipeline to the equalization unit, and the same HMI also surfaces analog values, active actuators, and manual override tabs so the operator can monitor or intervene when the plant is not following the normal automatic path.
   对应摘录：C, D
5. 句子 5：The paper further ties this supervisory logic to quality constraints by using pH and conductivity readings to parameterize control-valve opening and bypass decisions, ensuring that outflow water stays within the required `pH 6-9` and `<1500 ppm` limits.
   对应摘录：A, D

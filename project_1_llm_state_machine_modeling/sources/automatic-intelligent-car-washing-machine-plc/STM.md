# Control Design of Automatic Intelligent Car Washing Machine Based on PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把洗车机的双 PLC 分布式结构、输入/输出信号、自动/手动模式、洗车工艺链以及异常 pause/cancel 与污水回收收尾写得足够完整，可直接作为双 A 样本。

## 条目 1: Distributed PLC Car-Wash Sequence with Pause/Cancel and Water Reuse
- 控制对象：基于双 PLC 与三维喷头机构的智能洗车机控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是车辆服务设备领域的智能洗车机控制系统，用双 `S7-200 SMART` PLC、三维喷头运动机构、故障检测输入、阀门/电机输出和污水回收模块组织自动洗车全过程。
- 判断：算。对象是实际洗车设备控制系统，正文明确给出模式划分、输入输出集合、执行机构布局以及自动工作链与异常分支。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，`Control system structure`，`paper_content.txt` 第 91-111 行
> The operation panel has function buttons of the washing machine, and the detection signals include position detection of various nozzles, position detection of the blowing device, position detection of the body of the washing machine, detection of the defect position of each motor, position detection of the body of the washing machine, and each motor defect and overload detection.
>
> This detection signal is connected to the input of the S7-200 SMART as the opening point of the detection device. If there is a problem in the working part, the fault point can be found according to the status of the various indicators on the input of the S7-200 SMART, which is very beneficial for the later maintenance and repair work. The output load of the PLC includes a motor-controlled AC contactor, a DC solenoid valve that controls the vehicle and the water supply, a light-emitting diode that is indicated by the panel, and a buzzer alarm for the fault reminder.

#### 摘录 B
- 出处：第 2-3 页，`3.1 PLC selection / 3.2 Control system hardware wiring`，`paper_content.txt` 第 118-180 行
> the system uses two S7-200PLC networked distributed control system solutions, one of which is a PLC host. It is located in the control room ... Another PLC is placed in the washing shop as a slave station to control the input and output of the equipment in the washing workshop. The two PLCs use the switch connection to realize information interaction and coordination control.
>
> In order to ensure the accuracy and stability of the sliding guide, two sets of sliding guides and stepping motors are adopted to form the X-axis. The Y-axis and the Z-axis each have a set of sliding guides and a stepping motor. The nozzle bracket is mounted on the sliding guide of the Z-axis ... The system uses the SMART 700I IE touch screen as a human-machine interface to adjust the parameters of the car wash process, and controls the movement of the stepper motor by controlling the drive of the stepper motor.

#### 摘录 C
- 出处：第 3 页，`4. SOFTWARE DESIGN OF CONTROL SYSTEM`，`paper_content.txt` 第 228-257 行
> The car wash mode of this intelligent car wash system is divided into automatic mode and manual mode. The automatic mode is the main working mode, and the manual mode is mainly used for debugging and maintenance of equipment.
>
> The control requirements are: opening the entrance machine at the beginning to slow the vehicle into the washing shop. Open the bottom spray system to clean the wheel and the bottom of the vehicle during the vehicle's entry, and close the bottom spray system after the vehicle has completely crossed the bottom spray system. At the same time, the sensor is used to collect the vehicle parameters and the vehicle abnormality detection. After the detection is correct, the user is prompted to select the automatic car wash mode.
>
> During the car wash, the user can observe whether the washing, foam, water wax and air drying are completed through the touch screen ... the user can also pause or cancel the process under abnormal conditions. When the car wash is finished, the system will remind the user to complete the car wash through the display and voice. After the vehicle leaves the washing workshop, the car wash sewage recovery and purification system will be started to realize the reuse of water resources, and finally the system will be shut down.

### 2. 基于原文整理后的自然语言描述

The intelligent car-wash controller uses two networked `S7-200 SMART` PLCs, one host in the control room and one slave in the washing shop, to coordinate detection inputs, stepper-motor motion, valves, indicators, and alarms through a distributed control structure. Its detection inputs cover nozzle position, blowing-device position, car-body position, and each motor's defect or overload state, while outputs drive AC contactors, vehicle and water-supply solenoid valves, panel indicators, and a buzzer for fault reminders. The controller also operates a three-dimensional nozzle motion system built from X/Y/Z sliding guides and stepper motors and exposes process adjustment through a touch-screen HMI. In software it separates automatic and manual modes, where automatic mode opens the entrance machine, runs the bottom spray while the vehicle enters, checks vehicle parameters and abnormalities, guides the user through washing, foam, water-wax, and air-drying stages, allows pause or cancel under abnormal conditions, and then starts sewage recovery and purification after the vehicle leaves before shutting the system down.

### 3. 逐句溯源

1. 句子 1：The intelligent car-wash controller uses two networked `S7-200 SMART` PLCs, one host in the control room and one slave in the washing shop, to coordinate detection inputs, stepper-motor motion, valves, indicators, and alarms through a distributed control structure.
   对应摘录：A, B
2. 句子 2：Its detection inputs cover nozzle position, blowing-device position, car-body position, and each motor's defect or overload state, while outputs drive AC contactors, vehicle and water-supply solenoid valves, panel indicators, and a buzzer for fault reminders.
   对应摘录：A
3. 句子 3：The controller also operates a three-dimensional nozzle motion system built from X/Y/Z sliding guides and stepper motors and exposes process adjustment through a touch-screen HMI.
   对应摘录：B
4. 句子 4：In software it separates automatic and manual modes, where automatic mode opens the entrance machine, runs the bottom spray while the vehicle enters, checks vehicle parameters and abnormalities, guides the user through washing, foam, water-wax, and air-drying stages, allows pause or cancel under abnormal conditions, and then starts sewage recovery and purification after the vehicle leaves before shutting the system down.
   对应摘录：C

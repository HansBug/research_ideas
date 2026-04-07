# Automated Carwash Using Programmable Logic Control (PLC) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把六个传感器、三段喷淋/刷洗/吹干工位、进出场 `5 second delay` 和停机回初态链条都写成了可直接复用的 `PLC` 顺序控制器。

## 条目 1: Six-Sensor Carwash PLC Cycle

- 控制对象：自动洗车设备的输送、喷淋、刷洗、漂洗、吹干与停机顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是工业自动化与离散制造领域的 carwash `PLC` controller，用 `Sensor 1` 到 `Sensor 6` 和两个 `5 second delay` 定义车辆进入、喷淋、洗涤、刷洗、漂洗、吹干和停机回初态的整条控制链。
- 判断：算。对象是实际自动洗车设备的主控制器，原文给出了顺序阶段、传感器触发、输出执行件和局部定时，不是单纯流程展示。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，`Methodology`，`paper_content.txt` 第 71-80 行
> Figure 1 represent the operation of the Automated Car wash system using PLC Controller. The operation will begin after Switch Button has been triggered or Sensor 1 detect the car entering the car wash by activating the conveyor and water spray delay in 5 second. ... Then Sensor 2 will detect the car and will activate the detergent spray. ... Sensor 3 will detect the car and activate the brushless in the brushing section. Then in, Sensor 4 when detecting car, it will activate the spray water in rinse section. Sensor 5 on detecting a car, will operate the fan in the drying section. Lastly, Sensor 6 will detect the car and start to stop the overall system in 5 second delay.

#### 摘录 B

- 出处：第 5-6 页，`Simulation of the System`，`paper_content.txt` 第 108-127 行、第 143-147 行
> when the power supply is on, the output Greenlight is activate and triggered the TIM000 (Timer_0). After TIM_0 on state it will turn the Green Light in off state and Red Light in on state.
>
> In Figure 4, the triggered Timer 000 (TIM_0) will activate the conveyor to start its operation. ... 0.02 (Sensor_1) ... will trigger the 10.03 (Water Pump_1) operation. ... when the 0.03 (Sensor 2) is on state it will activate the 10.05 (Pump_2) which represent detergent spray. ... When 0.04 (Sensor 3) turn to the on state it will activate 10.02 (Motor_2).
>
> The 10.06 (Pump_3) is in the on state when 0.05 (Sensor 4) is detecting signal. ... The 10.07 (Fan) will operate when 0.06 (Sensor_5) is in the on state. Finally, TIM003 will end all the program's 5-second delay after 0.07 (Sensor_7) has been triggered.

#### 摘录 C

- 出处：第 8-10 页，`Results and Discussion`，`paper_content.txt` 第 184-188 行、第 206-218 行、第 238-241 行
> When the switch of PLC is ON, Start Push Button will be triggered to start the system so that green light start light up to triggered Timer 1. After that, Timer 1 will activate the Conveyor motor and turn off greenlight because red light is turn to the on state.
>
> Figure 14 shows conveyor starting to move after 5 second when the Push Button had been triggered. ... When car reaches section 2, Sensor 2 detects the car and the water pump_1 will stop because it passes through the Sensor_1. Detergent pump_2 will only operate if Sensor_2 is detecting the car and the Sensor_3 will activate brush motor in the next section 3. ... Figure 18 shows car washing with water again in section 4, after car reaches Sensor 4 and the operation of brush will stop after Sensor_3 did not detect the car.
>
> In Figure 19, the operation of the water pump_2 will stop because the car already passed through Sensor_4 and dry fan will be activated to dry the car when the car reaches Sensor_5. When car reaches exit gate and Sensor 6 detect the car it will start to activate the Timer_2 before shutting down all the process to the initial state after 5 second delay.

### 2. 基于原文整理后的自然语言描述

The carwash controller begins when the start button or `Sensor 1` detects a vehicle, then uses an entry `5 second delay` to switch from green-ready indication to red-running indication and start the conveyor plus the first water spray. As the vehicle progresses through the tunnel, `Sensor 2` enables detergent spray, `Sensor 3` starts the brush motor, `Sensor 4` switches the process to the rinse pump, and `Sensor 5` starts the drying fan, so the control flow is a sensor-driven sequence rather than a free-running loop. Each transition also shuts off the previous actuator once the car passes the corresponding sensor, which means pump, brush, and fan outputs are guarded by both section occupancy and timer-controlled start/stop logic. After the vehicle reaches the exit, `Sensor 6` starts another `5 second delay`, and once that delay elapses the controller stops the whole process and returns the equipment to its initial ready state for the next car.

### 3. 逐句溯源

1. 句子 1：The carwash controller begins when the start button or `Sensor 1` detects a vehicle, then uses an entry `5 second delay` to switch from green-ready indication to red-running indication and start the conveyor plus the first water spray.
   对应摘录：A, B, C
2. 句子 2：As the vehicle progresses through the tunnel, `Sensor 2` enables detergent spray, `Sensor 3` starts the brush motor, `Sensor 4` switches the process to the rinse pump, and `Sensor 5` starts the drying fan, so the control flow is a sensor-driven sequence rather than a free-running loop.
   对应摘录：A, B, C
3. 句子 3：Each transition also shuts off the previous actuator once the car passes the corresponding sensor, which means pump, brush, and fan outputs are guarded by both section occupancy and timer-controlled start/stop logic.
   对应摘录：B, C
4. 句子 4：After the vehicle reaches the exit, `Sensor 6` starts another `5 second delay`, and once that delay elapses the controller stops the whole process and returns the equipment to its initial ready state for the next car.
   对应摘录：A, B, C

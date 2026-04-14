# A Control System of PLC's Stereo Garage Based on Photoelectric Sensor - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把立体车库的复位、零层进车、尺寸/位置检查、升降横移、互锁和传感器故障防护都写进了 PLC 程序与流程图，能形成较完整的多阶段停车控制样本。

## 条目 1: Photoelectric-Guided Lift-and-Traverse Parking Controller
- 控制对象：智慧停车领域的光电传感立体车库存车控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个垂直升降式立体车库存车控制器，用光电/压力传感器、升降与横移机构、故障自诊断和速度闭环来组织入库流程。
- 判断：算。对象是实际立体车库控制系统，原文明确给出了停车主流程、复位和互锁规则、速度/爬行控制、故障诊断以及时间保护。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 13-20 行
> In order to design a vertical lifting three-dimensional garage control system, and to achieve the mechanical three-dimensional garage of the university automatic operation, the photoelectric sensors, hall pressure sensors and programmable logic controller (PLC) are used. The results show that the three-dimensional garage control system can run safely and reliably, and each sensor can perform fault self-diagnosis and carry out certain treatment on the fault. In conclusion, the three-dimensional garage control system designed is feasible, and it can get wide extension and application.

#### 摘录 B
- 出处：第 3-4 页，`Methods`，`paper_content.txt` 第 81-90 行
> When the user saves the car, the system first determines whether there is a car board on the platform. If there is a car carrying board, the elevator platform will directly drop to the zero floor. If there is no car carrying board, the elevator platform will select a parking space and remove the corresponding car board.
>
> When the elevator is landing to the zero floor, the user can get the car into the space. The zero floor photoelectric switch sensor and the pressure sensor cannot only detect whether the vehicle meets the parking standards, but also can detect whether the vehicle is parked in place. After the vehicle stops, the user presses the "Confirm Stop" button, and the lift starts to rise. When the vehicle stops at the target level, the traversing motor will drive the carriage along the rail into the parking space. When the vehicle is parked in place, the traverse motor moves back, and the lift platform is to carry out leveling treatment.

#### 摘录 C
- 出处：第 3-4 页，`Methods`，`paper_content.txt` 第 95-113 行
> In operation, the PLC dynamically generates the speed reference value according to the current running distance, and introduces the speed PI link to form the speed closed-loop control system, which effectively improves the system's response capability.
>
> As can be seen from Figure 1, the speed curve includes the acceleration section, uniform speed section, deceleration section and crawling section ... in order to improve the positioning accuracy, the study should set a crawl distance (fixed value) before reaching the target position, and given a very low creep speed to ensure reliable stop in place.
>
> The positioning of the lifting platform and the traverse mechanism adopts reflection type photoelectric switch sensor ... A car in the lifting platform moves one location every time unit, PLC detects the input signal changes, thereby updating the current floor value. If the target level has been reached, the supply is stopped and the brake is closed.

#### 摘录 D
- 出处：第 6-7 页，`Software design of the control system`，`paper_content.txt` 第 224-241 行、第 342-343 行
> When the garage starts running, the initial state is unknown, it must call the reset subroutine to establish a new initial state ... Parking and vehicle operation cannot be carried out at the same time, the lifting mechanism and the sliding mechanism is also not allowed to run at the same time.
>
> Sensor fault diagnosis and alarm subroutine by scanning all parking spaces on the photoelectric sensors and Hall sensors can detect the initial state of the garage, and provide alarms and fault indications in case of failure. ... In the motion control, this study uses photoelectric sensors and rotary encoder mutual checking method to prevent errors ... In addition, the system is also equipped with time protection, a variety of calibration and other measures.
>
> The S7-200 PLC reads the high-speed counter value every 5 ms and the S7-300 PLC computes the PI every 50 ms.

### 2. 基于原文整理后的自然语言描述

The garage controller is a photoelectric-sensor-driven EFSM that begins by calling a reset subroutine to establish a known initial state and then enforces mutual exclusion so parking/retrieval and lifting/sliding cannot execute at the same time. During parking, it checks whether a carrier board is already on the platform, moves or fetches the board as needed, brings the elevator platform to the zero floor, validates vehicle size and parking position with the zero-floor photoelectric and pressure sensors, waits for the user to confirm parking, then lifts to the target level and traverses the carriage into the selected berth before leveling and returning. Motion control is not just on/off: the PLC generates speed references from travel distance, runs a speed PI loop, uses acceleration, uniform-speed, deceleration, and crawl sections, and stops the mechanism only when the reflection photoelectric sensors indicate the target level has been reached and the brake can close. Safety supervision is integrated into the same controller through full-space sensor fault diagnosis, photoelectric-plus-encoder mutual checking, explicit time protection, and scan periods of `5 ms` for the high-speed counter and `50 ms` for the PI computation.

### 3. 逐句溯源

1. 句子 1：The garage controller is a photoelectric-sensor-driven EFSM that begins by calling a reset subroutine to establish a known initial state and then enforces mutual exclusion so parking/retrieval and lifting/sliding cannot execute at the same time.
   对应摘录：A, D
2. 句子 2：During parking, it checks whether a carrier board is already on the platform, moves or fetches the board as needed, brings the elevator platform to the zero floor, validates vehicle size and parking position with the zero-floor photoelectric and pressure sensors, waits for the user to confirm parking, then lifts to the target level and traverses the carriage into the selected berth before leveling and returning.
   对应摘录：B
3. 句子 3：Motion control is not just on/off: the PLC generates speed references from travel distance, runs a speed PI loop, uses acceleration, uniform-speed, deceleration, and crawl sections, and stops the mechanism only when the reflection photoelectric sensors indicate the target level has been reached and the brake can close.
   对应摘录：C
4. 句子 4：Safety supervision is integrated into the same controller through full-space sensor fault diagnosis, photoelectric-plus-encoder mutual checking, explicit time protection, and scan periods of `5 ms` for the high-speed counter and `50 ms` for the PI computation.
   对应摘录：A, D

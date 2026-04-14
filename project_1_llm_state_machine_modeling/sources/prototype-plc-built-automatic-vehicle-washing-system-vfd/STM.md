# A Prototype PLC Built Automatic Vehicle Washing System Using VFD - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把输送带、起泡、刷洗、漂洗、吹干和回初态写成带 `15 / 10 / 10 / 20 sec` 局部定时的完整洗车顺序控制链，原文和提取文本都达到双 A。

## 条目 1: Conveyor-Foaming-Brushing-Rinsing-Drying Wash Supervisor

- 控制对象：工业自动化与离散制造领域的自动车辆清洗输送、喷淋、刷洗、漂洗与吹干顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `PLC + VFD` 的外部洗车隧道主控制器，用入口传感器、各工位 proximity sensor 和多段 off-delay timer 管理输送、起泡、刷洗、漂洗、吹干与停机复位。
- 判断：算。对象是实际自动洗车设备的主控制逻辑，原文直接写出了阶段顺序、传感器触发、各工位执行器以及明确秒数定时，不是单纯机械设计或系统概述。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 21-30 行
> The system is built around a Logo Zelio (SR3B261BD) PLC for inputs and output components control. VFD moderates the conveyor belt motor speed as required for it smooth operation. Water recirculation system is incorporated for water and detergent economy. The status lamp on the control panel informs the user of the instantaneous stages of operation and control of the entire system.

#### 摘录 B

- 出处：第 5-6 页，`2.3. System operation`，`paper_content.txt` 第 160-176 行
> With the vehicle parked on the transport conveyor, a capacitive proximity sensor at this entry point detects the presence of the vehicle. This gives an output that energize the AC motor to drive the conveyor leading the vehicle into the washing tunnel. Vehicle reaches the showery down/foaming stage. A proximity sensor at this stage detects the vehicle, energizes a solenoid pump to discharge water and foaming water over the vehicle. This stage spans for 15 sec. The off-delay timer arrangement stops the solenoid pump.
>
> A proximity sensor at the washing stage detects the vehicle, energize the twin cotton brush ... This continues for a period of 10 sec. Then the off-delay timer deactivates the cotton brushes. ... another proximity sensor detects the vehicle and energizes the solenoid pump to discharge water on the vehicle for rinsing for 10 sec ... This detection activates the twin fans on the side of the tunnel for 20 sec.

#### 摘录 C

- 出处：第 6-7 页，`2.3. System operation / 2.4. Water recirculation system` 与第 7 页 `2.5. PLC ladder logic`，`paper_content.txt` 第 177-178、218-223、230-251 行
> The conveyor moves the vehicle to the terminal of the tunnel for finish operation and the cycle is repeated for the succeeding vehicle.
>
> ladder diagram of the Logo Zelio (SR3B261BD) PLC is presented in the subsequent figures.
>
> The second rung in figure 6 shows input I0.1 and Q4.0 as NOC, timer T0 as NCC ... The third rung in figure 7 presents inputs Q4.0 and I0.3 (proximity sensor) ... Figure 8 ... I0.4 (proximity sensor) ... Figure 9 ... I0.5 (proximity sensor) are NOC inputs and the timer reset register with Q4.6 as outputs.

### 2. 基于原文整理后的自然语言描述

The washing controller is organized as a staged tunnel sequence rather than a single on-off cleaning loop, and it uses the PLC plus a VFD-regulated conveyor as the backbone of the whole process. Once the entry proximity sensor detects a vehicle, the conveyor starts and the controller advances the car through foaming, brushing, rinsing, and drying workstations, where the foam stage lasts `15` seconds, brushing lasts `10` seconds, rinsing lasts `10` seconds, and drying lasts `20` seconds. Each stage is guarded by its own proximity sensor and is stopped by an off-delay timer, so actuator transitions happen only when both vehicle position and local timer conditions are satisfied. After the vehicle reaches the terminal of the tunnel, the controller ends the current cycle and returns the equipment to a ready state for the succeeding vehicle.

### 3. 逐句溯源

1. 句子 1：The washing controller is organized as a staged tunnel sequence rather than a single on-off cleaning loop, and it uses the PLC plus a VFD-regulated conveyor as the backbone of the whole process.
   对应摘录：A, B
2. 句子 2：Once the entry proximity sensor detects a vehicle, the conveyor starts and the controller advances the car through foaming, brushing, rinsing, and drying workstations, where the foam stage lasts `15` seconds, brushing lasts `10` seconds, rinsing lasts `10` seconds, and drying lasts `20` seconds.
   对应摘录：B
3. 句子 3：Each stage is guarded by its own proximity sensor and is stopped by an off-delay timer, so actuator transitions happen only when both vehicle position and local timer conditions are satisfied.
   对应摘录：B, C
4. 句子 4：After the vehicle reaches the terminal of the tunnel, the controller ends the current cycle and returns the equipment to a ready state for the succeeding vehicle.
   对应摘录：C

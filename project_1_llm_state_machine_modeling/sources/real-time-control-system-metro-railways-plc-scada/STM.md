# Real Time Control System for Metro Railways Using PLC & SCADA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次、显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 OCC 主控和站台、牵引供电两个子应用写成分层 PLC/SCADA 监督链，同时给出门控、发车和变压器故障切换的定时条件，能够稳定支撑双 A 铁路监督控制样本。

## 条目 1: OCC-Supervised Metro Platform and Power-Control Hierarchy

- 控制对象：地铁自动运行系统中的 OCC 监督式站台与牵引供电控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是轨道交通场景里的地铁运行监督器，用 OCC 作为主控制层，下挂站台发车、车站牵引和电力故障切换子应用，把门状态、信号灯、列车运行、报警和辅助供电切换组织成分层时序控制。
- 判断：算。对象是真实地铁运行控制系统，原文明确给出 `main application / sub-application` 结构、门控与发车定时、故障站告警以及 `T1/T2/T3` 变压器故障切换分支。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，`Abstract / Prototype of Metro Railways System`，`paper_content.txt` 第 7-16、62-79 行
> This work presents a simulated prototype of an automated metro train system operator that uses PLC and SCADA for the real time monitoring and control of the metro railway systems.
>
> The metro railways system has deployed infrastructure based on SCADA from the power supply system, and each station's traction power control is connected to the OCC remotely which commands all of the stations and has the highest command priority. An alarm is triggered in the event of an emergency or system congestion.
>
> PLC receives data/signals from input devices such as sensors, push button switches, contact limit switches ... stations, and emergencies feed into the PLC, which generates six output signals such as signal/alarm, train running or halting, and door open or close.

#### 摘录 B

- 出处：第 4 页，`Functioning of main application / Metro platforms / Metro stations`，`paper_content.txt` 第 84-109 行
> The prototype of the automated metro railways system operator has four main applications. OCC is the main application of this automated metro train system operator prototype. ... CCTV function, Metro stations view, Metro platform view, and Electrical control are other sub-applications of the system.
>
> The driver of the trains controls the metro platforms ... This flowchart in Fig. 5 and Tab. 1 shows the working of Metro platforms view sub-application.
>
> Metro train starts moving when the switch is turned ON. ... The emergency light will turn ON in case of any fault station and an alert message is displayed by the OCC in the relevant metro station on the HMI or operation display.

#### 摘录 C

- 出处：第 5 页，`Table 1: Metro platform view description`，`paper_content.txt` 第 125-132 行
> 1. t = 0 The traffic light is red, the trains are stopped and the passengers move out/in of the train and pantograph is not collect the power yet.
>
> 2. 20 > t >= 15 The doors are closed.
>
> 3. For t >= 20 The doors are closed and pantograph collects the power and electrical signal on overhead system is ON. Train starts running.
>
> 4. 100 >= t >= 20 Traffic light is green. The train starts moving forward.

#### 摘录 D

- 出处：第 7、12 页，`Electrical control view description / Electrical Control view`，`paper_content.txt` 第 140-158、208-217 行
> 1. S0 is ON Power supply is ON.
>
> 2. T1 and S1 are ON Power supply (132 kV/33 kV) is fed to the stepdown transformer (T1), then fed to the step-up transformer (T3), and then fed to metro stations and utility load.
>
> 3. For 50 <= t1 < 100 Transformer (T1) is damaged.
>
> 4. S2 is ON When transformer1 (T1) is damaged, the Auxiliary transformer1 (Aux-T1) is operated ...
>
> (3) For 50 <= t2 < 100: Stepdown transformer2 (T2, 132 kV/25 kV) is ON ... If transformer2 (T2) gets damaged, then Auxiliary transformer2 (Aux-T2) provides the power ...
>
> (4) When Stepdown transformer3 (T3) gets damaged, then Auxiliary transformer3 (Aux-T3) provide the power in case of T3.

### 2. 基于原文整理后的自然语言描述

The proposed metro operator is organized hierarchically, with the OCC as the main supervisory application and metro-platform, traction-SCADA, CCTV, and electrical-control branches as subordinate controllers. In the platform branch, the sequence begins with a red signal and open-door boarding state at `t = 0`, closes the doors during the `15-20` second interval, and after `t >= 20` energizes the pantograph and releases train movement while the traffic light turns green for the departure window. In the station branch, the PLC/SCADA system tracks train location and raises emergency lights plus OCC alerts when a fault station is detected. In the electrical-control branch, `S0` powers the system, `T1/T3` feed station loads in the nominal case, and timed fault windows such as `50 <= t1 < 100` and `50 <= t2 < 100` switch the supply path over to `Aux-T1`, `Aux-T2`, or `Aux-T3` so traction and utility loads can continue running after transformer damage. Together these nested branches form a supervisory HSM in which OCC oversees timed station and power-control subchains rather than a single flat signal cycle.

### 3. 逐句溯源

1. 句子 1：The proposed metro operator is organized hierarchically, with the OCC as the main supervisory application and metro-platform, traction-SCADA, CCTV, and electrical-control branches as subordinate controllers.
   对应摘录：A, B
2. 句子 2：In the platform branch, the sequence begins with a red signal and open-door boarding state at `t = 0`, closes the doors during the `15-20` second interval, and after `t >= 20` energizes the pantograph and releases train movement while the traffic light turns green for the departure window.
   对应摘录：C
3. 句子 3：In the station branch, the PLC/SCADA system tracks train location and raises emergency lights plus OCC alerts when a fault station is detected.
   对应摘录：A, B
4. 句子 4：In the electrical-control branch, `S0` powers the system, `T1/T3` feed station loads in the nominal case, and timed fault windows such as `50 <= t1 < 100` and `50 <= t2 < 100` switch the supply path over to `Aux-T1`, `Aux-T2`, or `Aux-T3` so traction and utility loads can continue running after transformer damage.
   对应摘录：D
5. 句子 5：Together these nested branches form a supervisory HSM in which OCC oversees timed station and power-control subchains rather than a single flat signal cycle.
   对应摘录：A, B, C, D

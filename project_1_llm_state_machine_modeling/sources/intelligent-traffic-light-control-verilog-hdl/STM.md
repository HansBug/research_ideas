# Design and Implementation of an Intelligent Traffic Light Control System Based on Verilog HDL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把日常循环、行人请求、紧急车辆优先和夜间模式统一写成一个八状态交通灯控制器，并给出优先级与秒级定时参数，足以支撑双 A 交通信号样本。

## 条目 1: Eight-state multi-mode traffic-signal supervisor

- 控制对象：道路交通信号控制领域的八状态多模式交通灯监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `Verilog HDL` 的四向路口交通灯控制器，用日常循环、行人相位、紧急车辆抢占和夜间闪黄模式共同管理路口通行。
- 判断：算。对象是实际交通灯控制系统，不是单纯 RTL 演示；原文不仅枚举了八个核心状态，还明确给出了优先级、状态跳转条件和各相位的 `30/60/5/20` 秒级定时。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 30-43 行
> This paper presents the design of an intelligent traffic light control system based on the Verilog hardware description language (HDL), achieving dynamic traffic flow optimization through a multi-mode switching mechanism. The system incorporates four core operational modes: Firstly, the Daily Mode (Default) ... Secondly, the Pedestrian Mode ... Thirdly, the Emergency Mode ... Finally, the Night Mode ... A Finite State Machine (FSM) architecture facilitates seamless transitions between these modes.

#### 摘录 B

- 出处：第 2-3 页，`2.2.1 State Machine Design`，`paper_content.txt` 第 96-127 行
> eight core states are defined:
> S_IDLE ... S_EW_GREEN ... S_EW_YELLOW ... S_NS_GREEN ... S_NS_YELLOW ... S_PED ... S_EMERGENCY ... S_NIGHT ...
>
> S_PED: Pedestrian crossing state. All vehicular are lights red; pedestrian signals are green ...
>
> S_EMERGENCY: Emergency mode state. Forces green light for a specific direction (EW in this design) and red for others ...
>
> S_NIGHT: Night mode state. All directions display flashing yellow lights ...

#### 摘录 C

- 出处：第 3-4 页，`2.2.2 State Transition Logic and Priority / 2.2.3 State Machine Code Implementation`，`paper_content.txt` 第 128-145、191-202 行
> This design establishes clear priority rules ... Reset Signal (Highest Priority) ... Emergency Vehicle Signal (Second Priority) ... Mode Setting Signals (Third Priority) ... Pedestrian Request (Fourth Priority).
>
> During S_EW_GREEN/S_NS_GREEN, latches request if ped_req is high. After the current green timer expires and the yellow transition completes: Diverts to S_PED instead of the next vehicular green state.
>
> Emergency : Enter from any state; exit to S_EW_GREEN when signal deasserts.

#### 摘录 D

- 出处：第 7-9 页，`Output Logic / Waveform Diagram Simulation Verification`，`paper_content.txt` 第 345-384、438-458 行
> EW_GREEN ... timer = (time_set == 2'b01) ? 60 : 30; // Peak 60s, Normal 30s
> EW_YELLOW ... timer = 5;
> NS_GREEN ... timer = (time_set == 2'b01) ? 60 : 30;
> NS_YELLOW ... timer = 5;
> PEDESTRIAN ... timer = 20;
>
> The system operates normally in the order of S_EW_GREEN -> S_EW_YELLOW -> S_NS_GREEN. ... When the timer is over, the system correctly responds to the latched pedestrian request ... to the S_PED pedestrian state.
>
> Since it has the highest priority, the system immediately interrupts the pedestrian access state and forces the jump to S_EMERGENCY state. ... When the emergency_vehicle signal is revoked ... the system ... first enters S_IDLE state for safe recovery ... then enters S_EW_GREEN state again.

### 2. 基于原文整理后的自然语言描述

The controller is an eight-state traffic-signal machine with `S_IDLE`, east-west green/yellow, north-south green/yellow, pedestrian, emergency, and night states, so normal circulation and special modes are handled within one explicit supervisory loop. Its transition policy is priority-driven: reset is highest, emergency preempts every active traffic state, night-mode commands are evaluated next, and pedestrian requests are latched below those higher-priority events. During normal operation, `EW_GREEN` and `NS_GREEN` each hold for `30 s` in regular mode or `60 s` in peak mode, the yellow transitions last `5 s`, and the pedestrian branch keeps all vehicle lights red while granting a `20 s` pedestrian crossing interval. A pedestrian request raised during a green vehicular phase does not interrupt immediately; instead, the controller waits for the current green timer and the yellow transition to finish before diverting to `S_PED`. By contrast, an emergency request forces an immediate jump to `S_EMERGENCY`, gives east-west traffic a green signal, and the simulation narrative shows that after the request is released the controller re-enters the normal cycle through a safe recovery path.

### 3. 逐句溯源

1. 句子 1：The controller is an eight-state traffic-signal machine with `S_IDLE`, east-west green/yellow, north-south green/yellow, pedestrian, emergency, and night states, so normal circulation and special modes are handled within one explicit supervisory loop.
   对应摘录：A, B
2. 句子 2：Its transition policy is priority-driven: reset is highest, emergency preempts every active traffic state, night-mode commands are evaluated next, and pedestrian requests are latched below those higher-priority events.
   对应摘录：C
3. 句子 3：During normal operation, `EW_GREEN` and `NS_GREEN` each hold for `30 s` in regular mode or `60 s` in peak mode, the yellow transitions last `5 s`, and the pedestrian branch keeps all vehicle lights red while granting a `20 s` pedestrian crossing interval.
   对应摘录：A, D
4. 句子 4：A pedestrian request raised during a green vehicular phase does not interrupt immediately; instead, the controller waits for the current green timer and the yellow transition to finish before diverting to `S_PED`.
   对应摘录：C, D
5. 句子 5：By contrast, an emergency request forces an immediate jump to `S_EMERGENCY`, gives east-west traffic a green signal, and the simulation narrative shows that after the request is released the controller re-enters the normal cycle through a safe recovery path.
   对应摘录：B, C, D

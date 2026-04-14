# Control of Hydraulic Pulse System Based on the PLC and State Machine Programming - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟、层次、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把液压脉冲系统的低成本 PLC 控制拆成 physical/application 两层线程，并明确给出了 WAIT/MANUAL/AUTO/PULSE/ERROR 主状态及 `N / p / T1 / T0` 脉冲参数。

## 条目 1: Two-Layer Pulse-Train Master State Machine
- 控制对象：工业气动液压脉冲系统的 PLC 主控程序
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟、层次、并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业液压脉冲设备的 PLC 控制器，用于在 WAIT、MANUAL、AUTO、PULSE 与 ERROR 等主状态之间切换，并按 `N / p / T1 / T0` 参数生成液压脉冲列车。
- 判断：算。对象是实际液压脉冲系统，不是方法流程；原文既给出可调脉冲参数，也给出两层线程组织、主状态集合、子状态调用和基于 program flags 的状态转移方式。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，Abstract / Section 2，行 75-120, 242-247
> In this paper, we deal with a simple embedded electronic system for an industrial pneumatic-hydraulic system, based on a low-cost programmable logic controller (PLC) ... The developed system is a hydraulic pulse system and generates a series of high-pressure hydraulic pulses with up to a max. 200 bar output pressure level and with up to a max. 2 Hz output hydraulic pulses frequency ... the threads create the main control state machine.
>
> The system controls up to four independent series, each of them defined by four adjustable parameters; the number of pulses (N), the maximum hydraulic pressure (p), the hydraulic pulse duration (T1) and the duration of the pause between pulses (T0).

#### 摘录 B
- 出处：第 7-8 页，Table 3 `List of application layer threads`，行 1261-1352
> some threads in application layer create individual states in the master control state diagram ... thread 2_State_Func can call of sub state 6_State_Func ...
>
> WAIT STATE, Initialization of calibration constants, zeroing of the ATE pressure sensor
>
> MANUAL STATE, manual control of output hydraulic pressure via manual potentiometer
>
> AUTO STATE, setting of parameters for hydraulic pulse train: WAGON parameters numbers of TRAIN WAGON and number of TRAIN SEASSON, manual calibration constants inputs (sub state: 22_State_Func)
>
> PULSE STATE, performing of hydraulic pulsation according of parameter settings, after finish of pulsing goes automatic to AUTO MODE (FLAGS_2_AUTO = ON, FLAGS_3_PULSE = OFF)
>
> ERROR STATE, Safety relay determined, determination of the error source

#### 摘录 C
- 出处：第 8 页，Section 4.5 `Description of the Master Control State Machine` / Section 4.7 `Auxiliary Functions`，行 1436-1486
> The main control state machine (Figure 4) for hydraulic pulse system consists of 7 separate threads running in the application layer ... Transitions between states in the application layer is controlled by the program flags and they are isolated from the hardware input signals ... This solution allows for the reliable function of high-pressure hydraulic pulse system, with reliable answers to user inputs or to the error status.
>
> The control of pulses sequences according to saved parameters in the hydraulic pulse train ensures thread 7_State_Func ... called from the state PULSE (3_State_Func). The thread 6_State_Func ensures the users inputs for controlling of the actual content of the hydraulic pulse train and is called from AUTO STATE (2_State_Func).

### 2. 基于原文整理后的自然语言描述

The hydraulic pulse controller is implemented on a low-cost PLC as a two-layer state-machine architecture in which physical-layer threads process hardware inputs and application-layer threads realize the master control logic. The application layer contains the main states `WAIT`, `MANUAL`, `AUTO`, `PULSE`, and `ERROR`, where `WAIT` initializes calibration constants and zeros the pressure sensor, `MANUAL` drives output pressure through a manual potentiometer, `AUTO` edits the pulse-train configuration, `PULSE` executes the hydraulic pulsation sequence, and `ERROR` identifies the error source reported by the safety relay. Each pulse train can contain up to four wagons, and every wagon is parameterized by pulse count `N`, maximum pressure `p`, pulse duration `T1`, and pause duration `T0`, so the controller explicitly stores both output magnitude and local timing. The `AUTO` state invokes a parameter-entry substate for train content and calibration constants, while `PULSE` invokes auxiliary substates for peak measurement and session-wise parameter modification. State transitions are not driven directly by raw hardware lines but by program flags derived from the physical layer, and once a pulsation cycle finishes the controller automatically clears `PULSE` and returns to `AUTO`.

### 3. 逐句溯源

1. 句子 1：The hydraulic pulse controller is implemented on a low-cost PLC as a two-layer state-machine architecture in which physical-layer threads process hardware inputs and application-layer threads realize the master control logic.
   对应摘录：A, B, C
2. 句子 2：The application layer contains the main states `WAIT`, `MANUAL`, `AUTO`, `PULSE`, and `ERROR`, where `WAIT` initializes calibration constants and zeros the pressure sensor, `MANUAL` drives output pressure through a manual potentiometer, `AUTO` edits the pulse-train configuration, `PULSE` executes the hydraulic pulsation sequence, and `ERROR` identifies the error source reported by the safety relay.
   对应摘录：B
3. 句子 3：Each pulse train can contain up to four wagons, and every wagon is parameterized by pulse count `N`, maximum pressure `p`, pulse duration `T1`, and pause duration `T0`, so the controller explicitly stores both output magnitude and local timing.
   对应摘录：A
4. 句子 4：The `AUTO` state invokes a parameter-entry substate for train content and calibration constants, while `PULSE` invokes auxiliary substates for peak measurement and session-wise parameter modification.
   对应摘录：B, C
5. 句子 5：State transitions are not driven directly by raw hardware lines but by program flags derived from the physical layer, and once a pulsation cycle finishes the controller automatically clears `PULSE` and returns to `AUTO`.
   对应摘录：B, C

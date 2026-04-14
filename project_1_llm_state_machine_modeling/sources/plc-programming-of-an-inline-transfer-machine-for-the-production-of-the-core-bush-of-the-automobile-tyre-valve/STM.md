# PLC Programming of an Inline Transfer Machine for the Production of the Core Bush of the Automobile Tyre Valve - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 inline transfer 机的 `auto / single cycle / jog` 顶层模式、门联锁、故障优先级、回零和带 `ON Timer` 的启动顺序写成了明确的工业控制链。

## 条目 1: Mode-Governed Inline Transfer Machine Supervisor
- 控制对象：工业自动化与离散制造领域的 inline transfer 机模式监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是汽车轮胎气门芯套筒生产线上的 PLC 模式控制器，负责管理生产机在 auto、single cycle、jog、门联锁和 fault 处理之间的运行条件与切换。
- 判断：算。对象是实际自动化生产线控制器，原文明确写出了顶层模式、进入条件、回零要求、门/故障联锁、编码器反馈和定时启动顺序，足以整理成 `HSM + T1` 样本。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract
> The process of manufacturing the bush is carried out by PLC programming. An attempt has been made in this work to control the operations performed by this automated production line for the machining of the bush. The PLC programming is carried out in order to achieve control over every function of the machine, the workstations, poka yoke system and to enable easy fault traceability through the Human Machine Interface (HMI). Safety of the machine and the operator is realised through programming.

#### 摘录 B
- 出处：第 2 页，Methodology
> The machine is then run in the auto mode, jog mode and single cycle mode as per the conditions of the program, to test whether the program is in agreement with the requirements.

#### 摘录 C
- 出处：第 2 页，The Functions Programmed in PLC / Auto Mode
> Auto Mode: This is the mode in which there is mass production of the valve core bush. The mode is programmed such that it is executed only if,
>
> • The Emergency Push Button is released.
> • The switch used for selecting different modes, is positioned in the auto mode.
> • All doors are closed.
> • No emergency faults or poka yoke faults are activated.
> • The machine has completed a single cycle, once.
>
> If the above conditions are satisfied the machine can be run in the auto mode. The mode is started by switching on the oil pump. The machine is programmed such that the motors of the workstations switch on only after the oil pumps are turned on. A short time delay is achieved between these two operations using the ON Timer function.

#### 摘录 D
- 出处：第 2 页，The Functions Programmed in PLC / Single Cycle Mode / Jog Mode / Door / Faults / Encoder
> Single Cycle Mode: In this mode, the cam shaft is required to complete one full rotation so that all the workstations are in the home position before beginning the auto mode.
>
> Jog Mode: This is a mode used to run the machine in small steps, only as long as the pushbutton is pressed. This mode helps to observe the movements of the workstations to find out if there is any mechanical fault.
>
> Door: The programming ensures operator safety by enabling the machine to run only when all the doors are closed.
>
> Faults: The faults that would cause damages to the machine or would result in hazard to the operator are treated on first priority by making the machine stop immediately if those faults occur. On the other hand, error signals from sensors, poka yoke systems etc. are faults that would only require the machine to stop after homing.
>
> Encoder: An absolute encoder is used to get the position feedback of the cam shaft.

### 2. 基于原文整理后的自然语言描述

The inline transfer machine is organized around several top-level operating modes rather than a single flat production loop. Before the machine can enter auto production, it must satisfy a guarded entry condition set: the emergency push button must be released, the selector must be in auto, all doors must be closed, no emergency or poka-yoke fault may be active, and one single-cycle homing run must already have been completed. Once auto mode starts, the oil pump is switched on first and the workstation motors are enabled only after a short delay produced by an `ON Timer`, which makes the startup sequence explicitly timer-governed. Outside mass-production mode, the controller also supports a single-cycle homing mode, a pushbutton-held jog mode for stepwise inspection, and safety branches in which critical faults stop the machine immediately while lower-priority sensor or poka-yoke faults stop it after homing. Encoder feedback and HMI fault display complete the supervisor, making the paper a clear mode-oriented production-machine control sample.

### 3. 逐句溯源

1. 句子 1：The inline transfer machine is organized around several top-level operating modes rather than a single flat production loop.
   对应摘录：A, B, D
2. 句子 2：Before the machine can enter auto production, it must satisfy a guarded entry condition set: the emergency push button must be released, the selector must be in auto, all doors must be closed, no emergency or poka-yoke fault may be active, and one single-cycle homing run must already have been completed.
   对应摘录：C, D
3. 句子 3：Once auto mode starts, the oil pump is switched on first and the workstation motors are enabled only after a short delay produced by an `ON Timer`, which makes the startup sequence explicitly timer-governed.
   对应摘录：C
4. 句子 4：Outside mass-production mode, the controller also supports a single-cycle homing mode, a pushbutton-held jog mode for stepwise inspection, and safety branches in which critical faults stop the machine immediately while lower-priority sensor or poka-yoke faults stop it after homing.
   对应摘录：B, D
5. 句子 5：Encoder feedback and HMI fault display complete the supervisor, making the paper a clear mode-oriented production-machine control sample.
   对应摘录：A, D

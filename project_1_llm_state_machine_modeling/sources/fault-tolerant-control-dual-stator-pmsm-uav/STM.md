# Fault-Tolerant Control of a Dual-Stator PMSM for the Full-Electric Propulsion of a Lightweight Fixed-Wing UAV - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双定子推进系统在不同飞行阶段下的模式切换、故障补偿与终止着陆回退链写得比较明确，可直接整理为 UAV 推进模式管理样本。

## 条目 1: Mission-phase and fault-driven FEPS mode switching
- 控制对象：轻型固定翼 UAV 双定子全电推进系统（FEPS）的模式切换控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是固定翼无人机电推进领域的 FEPS supervisory controller，用于根据任务阶段和监测故障标志在 `FMM / FTM / HSB / CSB` 四种推进模式间切换，并在故障后保持飞行或完成安全终止着陆。
- 判断：算。对象是实际 UAV 推进控制子系统，原文明确给出了模式集合、任务阶段到模式的映射、故障触发的模式切换和终止着陆时的附加切换条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4-5 页，`operation modes / Table 1`
> As a consequence, four operation modes have been defined to control each stator of the AFPMSM:
>
> (1) Flight Mission Mode (FMM) ... a speed-tracking closed-loop system ...
>
> (2) Flight Termination Mode (FTM) ... the two ones of the FMM plus an outer loop on motor shaft rotation, with a predefined setpoint for the propeller alignment;
>
> (3) Hot Stand-By (HSB) ... stand-by status;
>
> (4) Cold Stand-By (CSB) ... passive.
>
> depending on the MON fault flags ... and on the mission phase ... the CON modules can be switched to FMM, FTM, HSB or CSB modes.

#### 摘录 B
- 出处：第 5 页，`Table 1. FEPS operation modes as functions of mission phases and detected faults`
> Climb ... `FMM/FMM` ... Normal operation (active/active)
>
> Cruise, Loiter, Descent ... `HSB/FMM` ... Normal operation (stand-by/active)
>
> Flight termination/Landing ... `HSB/FTM` ... Normal operation (stand-by/active)
>
> With detected faults, the combinations become `FMM/CSB`, `CSB/FMM`, or `FTM/CSB`.

#### 摘录 C
- 出处：第 9, 12, 15 页，`Fault-Tolerant Control System Design / failure transient events`
> The multi-mode closed-loop system of the FEPS ... has been entirely developed as a finite-state machine, by using the Matlab-Simulink-Stateflow tools.
>
> During cruise and flight termination/landing, the healthy stator is activated (250 ms delay is assumed to achieve the full electric supply) and controlled.
>
> Event 4 (E4, only for flight termination/landing): the active stator is switched to operate from FMM to FTM.
>
> when the speed is adequately small (<1 rad/s), the CON modules switch from HSB/FMM to FTM/CSB.

### 2. 基于原文整理后的自然语言描述

The FEPS controller treats each stator of the dual-stator propulsion machine as a finite-state mode actuator with four modes, `FMM`, `FTM`, `HSB`, and `CSB`, selected from the current mission phase and the monitor fault flags. During climb both stators operate in `FMM/FMM` active-active mode, during cruise/loiter/descent the normal configuration is `HSB/FMM` stand-by-active, and during flight termination or landing the normal configuration is `HSB/FTM` so that the active stator can align the propeller with the wing before parachute deployment. When a fault is detected on one stator, the faulty side is driven to `CSB` and the healthy side is activated to `FMM` or kept in `FTM` according to the current phase, yielding fail-operative combinations such as `FMM/CSB`, `CSB/FMM`, or `FTM/CSB`. For cruise and landing recovery, the controller assumes a 250 ms delay to fully energize the previously stand-by stator before it takes over torque production. During flight termination and landing, once the propeller speed becomes sufficiently small, the controller performs an additional transition from `FMM` to `FTM` so the blades can be stopped and aligned safely, and the whole switching logic is implemented as a Stateflow finite-state machine.

### 3. 逐句溯源

1. 句子 1：The FEPS controller treats each stator of the dual-stator propulsion machine as a finite-state mode actuator with four modes, `FMM`, `FTM`, `HSB`, and `CSB`, selected from the current mission phase and the monitor fault flags.
   对应摘录：A
2. 句子 2：During climb both stators operate in `FMM/FMM` active-active mode, during cruise/loiter/descent the normal configuration is `HSB/FMM` stand-by-active, and during flight termination or landing the normal configuration is `HSB/FTM` so that the active stator can align the propeller with the wing before parachute deployment.
   对应摘录：A, B
3. 句子 3：When a fault is detected on one stator, the faulty side is driven to `CSB` and the healthy side is activated to `FMM` or kept in `FTM` according to the current phase, yielding fail-operative combinations such as `FMM/CSB`, `CSB/FMM`, or `FTM/CSB`.
   对应摘录：B
4. 句子 4：For cruise and landing recovery, the controller assumes a 250 ms delay to fully energize the previously stand-by stator before it takes over torque production.
   对应摘录：C
5. 句子 5：During flight termination and landing, once the propeller speed becomes sufficiently small, the controller performs an additional transition from `FMM` to `FTM` so the blades can be stopped and aligned safely, and the whole switching logic is implemented as a Stateflow finite-state machine.
   对应摘录：C

# Developing a Prototype of a Mechanical Ventilator Controller from Requirements to Code with ASMETA - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机） / HSM（层次状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟、层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：论文不仅明确给出通气控制器的主运行阶段，还细化了 `state/phase` 两层结构、PCV/PSV 下的时间窗、阀门动作、暂停/复张和 apnea 回退，是高质量控制样本。

## 条目 1: Main Ventilation Modes and Start-Up Phases
- 控制对象：机械呼吸机 MVM 控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：层次、显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是医疗设备控制领域的机械通气控制器，用于在启动、自检、待机和两种通气模式之间切换并处理无呼吸回退。
- 判断：算。对象是实际医疗控制系统，原文明确给出了主运行阶段和模式切换条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section 3 / Section 4，`paper_content.txt` 第 184-216, 224-240 行
> MVM has two operative modes: Pressure Controlled Ventilation (PCV) and Pressure Support Ventilation (PSV). In the PCV mode, the respiratory cycle is kept constant and the pressure level changes between the target inspiratory pressure and the positive end-expiratory pressure. New inspiration is initiated either after a breathing cycle is over, or when the patient spontaneously initiates a breath. ... The PSV mode is not suitable for patients that are not able to start breathing on their own ... If a new inspiratory phase is not detected within a certain amount of time (apnea lag), MVM will automatically switch to the PCV mode because it is assumed that the patient is not able to breathe alone.
>
> Before starting the ventilation the MVM controller passed through three phases. The start-up in which the controller is initialized with default parameters, self-test which ensures that the hardware is fully functional, and ventilation off in which the controller is ready for ventilation when requested.
>
> The first model introduces the operation phases of the MVM controller. At the end of startup and self-test, the ventilator goes in the ventilation off state. Afterward, on the basis of the user request, it can go to one of the two operation modes: PCV or PSV.

#### 摘录 B
- 出处：第 5-10 页，Section 4.2 / 4.3 / 4.4，`paper_content.txt` 第 268-286, 436-505, 521-540 行
> The second model refines the inspiration and expiration phases in PCV and PSV mode. ... In PCV mode, the transition between inspiration and expiration is determined by the duration of each phase decided by the physician ... In PSV mode ... the transition from inspiration to expiration happens when the airflow drops a defined threshold after a minimum inspiration time, or when the maximum inspiration time set by the doctor is expired. ... the physician can change from PSV to PCV and without interrupting the ventilation when in expiration phase.
>
> The third model adds the expiratory/inspiratory pauses, the recruitment manoeuvrer, and the apnea. ... if `cmdInPause` then `rInPause[]` ... if `cmdRm` then `rrm[]` ... if `cmdExPause` then `rExPause[]` ... when PSV is running and the ventilator does not detect a new breath within apnea lag ... the ventilator automatically changes to PCV mode starting from the inspiration phase.
>
> In the last model ... the transition between expiration and inspiration in case of pressure drop, and the transition between inspiration and expiration in case the pressure exceeds a threshold.

### 2. 基于原文整理后的自然语言描述

The controller uses a top-level state machine with `STARTUP`, `SELFTEST`, `VENTILATIONOFF`, `PCV_STATE`, and `PSV_STATE`, and before ventilation starts it always passes through startup, self-test, and ventilation-off before entering PCV or PSV on user request. Inside the ventilation modes, the refinement hierarchy introduces a second level of phase states, first `INSPIRATION` and `EXPIRATION`, and then `INPAUSE`, `EXPAUSE`, and `RM` for inspiratory pause, expiratory pause, and recruitment manoeuvre. In PCV, the respiratory cycle is kept constant and can also be triggered by a spontaneous pressure drop within the trigger window, whereas in PSV the patient initiates inspiration and the mode can later fall back to PCV if apnea lag expires without a new breath. The last refinement also adds threshold-based phase switching, so the controller can move from expiration to inspiration on pressure drop and from inspiration to expiration when the pressure exceeds the configured maximum.

### 3. 逐句溯源

1. 句子 1：The controller uses a top-level state machine with `STARTUP`, `SELFTEST`, `VENTILATIONOFF`, `PCV_STATE`, and `PSV_STATE`, and before ventilation starts it always passes through startup, self-test, and ventilation-off before entering PCV or PSV on user request.
   对应摘录：A
2. 句子 2：Inside the ventilation modes, the refinement hierarchy introduces a second level of phase states, first `INSPIRATION` and `EXPIRATION`, and then `INPAUSE`, `EXPAUSE`, and `RM` for inspiratory pause, expiratory pause, and recruitment manoeuvre.
   对应摘录：B
3. 句子 3：In PCV, the respiratory cycle is kept constant and can also be triggered by a spontaneous pressure drop within the trigger window, whereas in PSV the patient initiates inspiration and the mode can later fall back to PCV if apnea lag expires without a new breath.
   对应摘录：A, B
4. 句子 4：The last refinement also adds threshold-based phase switching, so the controller can move from expiration to inspiration on pressure drop and from inspiration to expiration when the pressure exceeds the configured maximum.
   对应摘录：B

## 条目 2: Inspiration/Expiration and Valve Switching Logic
- 控制对象：机械呼吸机 MVM 的吸气-呼气相位控制
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是医疗设备控制领域的机械呼吸机子控制逻辑，用于按相位和模式切换输入/输出阀并决定吸气、呼气的转换条件。
- 判断：算。对象是实际呼吸机控制子系统，原文给出了 PCV/PSV 吸呼相位的切换条件和阀门开闭配置。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section 3/Case Study，`paper_content.txt` 第 202-213 行
> The ventilator allows the air to enter/exit through two valves, i.e., an input valve and an output valve. When the ventilator is not running, the valves are set to safe mode: input valve closed and output valve opened. When the inspiration starts, the input valve is opened and the output valve is closed, while during the expiration the input valve is closed and the output valve is opened. Both in PCV and PSV mode inspiratory pause, expiratory pause, and recruitment manoeuvrer are allowed by user request.
>
> Inspiratory/Expiratory pause consists in closing the input and output valves of the ventilator respectively after the inspiration and expiration phase. ... Recruitment manoeuvrer is an emergency procedure ... during this manoeuvrer, the input valve is opened and the output valve is closed.

#### 摘录 B
- 出处：第 6-10 页，Section 4.2 / 4.3 / 4.4，`paper_content.txt` 第 271-289, 441-517, 521-540 行
> In PCV mode, the transition between inspiration and expiration is determined by the duration of each phase decided by the physician ... When the inspiration time is passed, the controller goes to the PCV expiration phase. ... If a stop request ... is received during the inspiration phase, it is stored in `stopVentilation` and will be executed in the expiration phase. When in expiration ... the ventilator moves to PCV inspiration when expiration duration expires.
>
> In PSV mode ... the transition from inspiration to expiration happens when the airflow drops a defined threshold after a minimum inspiration time, or when the maximum inspiration time set by the doctor is expired. The opposite transition occurs after a minimum expiration time. ... the physician can change from PSV to PCV and without interrupting the ventilation when in expiration phase.
>
> In the third model ... if `cmdInPause` then `rInPause[]` ... if `cmdRm` then `rrm[]` ... if `cmdExPause` then `rExPause[]` ... when PSV is running and the ventilator does not detect a new breath within apnea lag ... the ventilator automatically changes to PCV mode starting from the inspiration phase.
>
> In the last model ... when the ventilator is in expiration ... and it detects ... a sudden drop in pressure below the inhale trigger sensitivity threshold ... the ventilator directly moves to the inspiration phase. The transition from inspiration to expiration is automatically performed when the pressure goes beyond the maximum threshold set by the doctor.

### 2. 基于原文整理后的自然语言描述

When the ventilator is not running, it stays in a safe valve configuration with the input valve closed and the output valve open; inspiration opens the input valve and closes the output valve, while expiration closes the input valve and opens the output valve. In PCV mode, inspiration ends when `timerInspirationDurPCV` expires or when pressure exceeds the configured maximum, expiration ends when `timerExpirationDurPCV` expires or, after the trigger-window delay, when a spontaneous pressure drop is detected, and a stop request received during inspiration is latched and executed in expiration. In PSV mode, inspiration ends after the minimum inspiration time when the inspiratory flow drops below the threshold or when the maximum inspiration time expires, expiration ends after the minimum expiration time and a spontaneous pressure drop can start the next inspiration, while apnea-lag expiration forces a backup switch to PCV. User-requested `INPAUSE` and `EXPAUSE` close both valves after inspiration or expiration respectively, and recruitment manoeuvre keeps the input valve open with the output valve closed.

### 3. 逐句溯源

1. 句子 1：When the ventilator is not running, it stays in a safe valve configuration with the input valve closed and the output valve open; inspiration opens the input valve and closes the output valve, while expiration closes the input valve and opens the output valve.
   对应摘录：A
2. 句子 2：In PCV mode, inspiration ends when `timerInspirationDurPCV` expires or when pressure exceeds the configured maximum, expiration ends when `timerExpirationDurPCV` expires or, after the trigger-window delay, when a spontaneous pressure drop is detected, and a stop request received during inspiration is latched and executed in expiration.
   对应摘录：B
3. 句子 3：In PSV mode, inspiration ends after the minimum inspiration time when the inspiratory flow drops below the threshold or when the maximum inspiration time expires, expiration ends after the minimum expiration time and a spontaneous pressure drop can start the next inspiration, while apnea-lag expiration forces a backup switch to PCV.
   对应摘录：B
4. 句子 4：User-requested `INPAUSE` and `EXPAUSE` close both valves after inspiration or expiration respectively, and recruitment manoeuvre keeps the input valve open with the output valve closed.
   对应摘录：A, B

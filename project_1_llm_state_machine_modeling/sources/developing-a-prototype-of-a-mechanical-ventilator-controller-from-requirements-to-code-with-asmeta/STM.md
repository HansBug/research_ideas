# Developing a Prototype of a Mechanical Ventilator Controller from Requirements to Code with ASMETA - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：论文不仅明确给出通气控制器的主运行阶段，还细化了 PCV/PSV 下的吸气-呼气切换和阀门动作，是高质量控制样本。

## 条目 1: Main Ventilation Modes and Start-Up Phases
- 控制对象：机械呼吸机 MVM 控制器

### 0. 条目识别与判定

- 一句话说明：这是医疗设备控制领域的机械通气控制器，用于在启动、自检、待机和两种通气模式之间切换并处理无呼吸回退。
- 判断：算。对象是实际医疗控制系统，原文明确给出了主运行阶段和模式切换条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section 3/Case Study，`paper_content.txt` 第 184-200 行
> MVM has two operative modes: Pressure Controlled Ventilation (PCV) and Pressure Support Ventilation (PSV). In the PCV mode, the respiratory cycle is kept constant ... New inspiration is initiated either after a breathing cycle is over, or when the patient spontaneously initiates a breath. ... The PSV mode is not suitable for patients that are not able to start breathing on their own ... If a new inspiratory phase is not detected within a certain amount of time (apnea lag), MVM will automatically switch to the PCV mode because it is assumed that the patient is not able to breathe alone.

#### 摘录 B
- 出处：第 5 页，Section 3 / Section 4.1，`paper_content.txt` 第 214-216, 225-239 行
> Before starting the ventilation the MVM controller passed through three phases. The start-up in which the controller is initialized with default parameters, self-test which ensures that the hardware is fully functional, and ventilation off in which the controller is ready for ventilation when requested.
>
> The first model introduces the operation phases of the MVM controller. At the end of startup and self-test, the ventilator goes in the ventilation off state. Afterward, on the basis of the user request, it can go to one of the two operation modes: PCV or PSV.

### 2. 基于原文整理后的自然语言描述

The MVM ventilator controller operates in two main ventilation modes, PCV and PSV. Before ventilation starts, the controller progresses through startup, self-test, and ventilation-off phases, and then enters PCV or PSV according to the user request. In PSV, if a new inspiratory phase is not detected within the apnea lag, the controller automatically switches back to PCV because the patient is assumed to be unable to breathe alone.

### 3. 逐句溯源

1. 句子 1：The MVM ventilator controller operates in two main ventilation modes, PCV and PSV.
   对应摘录：A
2. 句子 2：Before ventilation starts, the controller progresses through startup, self-test, and ventilation-off phases, and then enters PCV or PSV according to the user request.
   对应摘录：B
3. 句子 3：In PSV, if a new inspiratory phase is not detected within the apnea lag, the controller automatically switches back to PCV because the patient is assumed to be unable to breathe alone.
   对应摘录：A

## 条目 2: Inspiration/Expiration and Valve Switching Logic
- 控制对象：机械呼吸机 MVM 的吸气-呼气相位控制

### 0. 条目识别与判定

- 一句话说明：这是医疗设备控制领域的机械呼吸机子控制逻辑，用于按相位和模式切换输入/输出阀并决定吸气、呼气的转换条件。
- 判断：算。对象是实际呼吸机控制子系统，原文给出了 PCV/PSV 吸呼相位的切换条件和阀门开闭配置。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section 3/Case Study，`paper_content.txt` 第 202-213 行
> The ventilator allows the air to enter/exit through two valves, i.e., an input valve and an output valve. When the ventilator is not running, the valves are set to safe mode: input valve closed and output valve opened. When the inspiration starts, the input valve is opened and the output valve is closed, while during the expiration the input valve is closed and the output valve is opened. Both in PCV and PSV mode inspiratory pause, expiratory pause, and recruitment manoeuvrer are allowed by user request.

#### 摘录 B
- 出处：第 6-7 页，Section 4.2 Second model，`paper_content.txt` 第 271-287 行
> In PCV mode, the transition between inspiration and expiration is determined by the duration of each phase decided by the physician ... When the inspiration time is passed, the controller goes to the PCV expiration phase. ... When in expiration ... the ventilator moves to PCV inspiration when expiration duration expires.
>
> In PSV mode ... the transition from inspiration to expiration happens when the airflow drops a defined threshold ... after a minimum inspiration time, or when the maximum inspiration time set by the doctor is expired. The opposite transition occurs after a minimum expiration time. ... Depending on the ventilator state, the input and output valves are in the following position ...

### 2. 基于原文整理后的自然语言描述

When the ventilator is not running, it keeps a safe valve configuration with the input valve closed and the output valve open. During inspiration the controller opens the input valve and closes the output valve, and during expiration it closes the input valve and opens the output valve. In PCV mode, inspiration and expiration alternate on physician-configured timers, whereas in PSV mode inspiration ends when the airflow drops below the threshold after the minimum inspiration time or when the maximum inspiration time expires, and expiration ends after the minimum expiration time.

### 3. 逐句溯源

1. 句子 1：When the ventilator is not running, it keeps a safe valve configuration with the input valve closed and the output valve open.
   对应摘录：A
2. 句子 2：During inspiration the controller opens the input valve and closes the output valve, and during expiration it closes the input valve and opens the output valve.
   对应摘录：A
3. 句子 3：In PCV mode, inspiration and expiration alternate on physician-configured timers, whereas in PSV mode inspiration ends when the airflow drops below the threshold after the minimum inspiration time or when the maximum inspiration time expires, and expiration ends after the minimum expiration time.
   对应摘录：B

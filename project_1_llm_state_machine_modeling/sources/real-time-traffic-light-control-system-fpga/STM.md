# Design and Implementation of a Real-time Traffic Light Control System Based on FPGA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把相位轮转、倒计时显示和人工接管一起组织进一个 FPGA 交通灯控制器里，时间参数、自动/手动切换和 LED 倒计时链都比较直白，可作为交通信号 HSM/T1 样本。

## 条目 1: Countdown-and-manual-override traffic supervisor

- 控制对象：道路交通信号控制领域的倒计时与人工接管交通灯监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 FPGA 的十字路口交通灯控制器，在自动相位轮转之外还保留了倒计时显示和由警员触发的 manual override。
- 判断：算。对象是实际交通灯控制器，原文把状态机、各方向相位、`15 / 5 / 25 s` 时长、倒计时显示和自动/手动切换都写成了明确的控制逻辑，而不是单纯实验板展示。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Introduction，`paper_content.txt` 第 64-70 行
> The states machine is good way to separate the system to different function model.
>
> An advanced system should include traffic lights controller, countdown controller and LED display controller. LED display showing the countdown time ...

#### 摘录 B

- 出处：第 2-3 页，`Second number counter selection / Signal_Light_vector3 countdown control circuit`，`paper_content.txt` 第 140-177 行
> the maintain time of red light vector, yellow light vector and the green light vector are 15s, 5s and 25s on both meridional and transmeridional direction.
>
> ... the countdown display ... telling the vehicles and pedestrians how much time they have by the traffic signal changing ...
>
> when the internal counter start counting, the green lamp light, load minus 1 and put it into COUNT_ff ... drives the LED displaying the remaining time.

#### 摘录 C

- 出处：第 3 页，`Traffic signal control circuit`，`paper_content.txt` 第 189-220 行
> during the rush hour sometimes the manual control is required ...
>
> main function is to switch manual and automatic mode.
>
> According to the chart: when a_m=1 (the automatic mode) the next_state can be triggered.
>
> ... when rewg sn=1 ... red ones for east-west direction and the green ones for north-south direction ...
>
> When next_state_butt = 1, the state automatic switches to manual (auto_manual=0) ... reset = 1 ... the initial state.

### 2. 基于原文整理后的自然语言描述

The controller is organized as a traffic-signal state machine whose automatic phase cycle is surrounded by two additional supervisory layers: a countdown subsystem and a manual-override mode. In its automatic cycle, the paper assigns explicit engineering times of `15 s` red, `5 s` yellow, and `25 s` green for the two orthogonal traffic directions, so the phase persistence is not implicit. The same timing chain is exposed to road users through an LED countdown subsystem, where the internal counter decrements the remaining phase time and drives the display. Around this timed cycle, the controller supports a manual takeover path for rush-hour or police-directed operation: when `a_m=1`, the automatic `next_state` transitions are enabled, but when `next_state_butt=1`, the system switches from automatic to manual mode and resets to the initial signal configuration. This makes the sample more than a flat traffic FSM, because it retains an outer mode layer that supervises the inner timed phase transitions and the countdown-display behavior.

### 3. 逐句溯源

1. 句子 1：The controller is organized as a traffic-signal state machine whose automatic phase cycle is surrounded by two additional supervisory layers: a countdown subsystem and a manual-override mode.
   对应摘录：A, C
2. 句子 2：In its automatic cycle, the paper assigns explicit engineering times of `15 s` red, `5 s` yellow, and `25 s` green for the two orthogonal traffic directions, so the phase persistence is not implicit.
   对应摘录：B
3. 句子 3：The same timing chain is exposed to road users through an LED countdown subsystem, where the internal counter decrements the remaining phase time and drives the display.
   对应摘录：A, B
4. 句子 4：Around this timed cycle, the controller supports a manual takeover path for rush-hour or police-directed operation: when `a_m=1`, the automatic `next_state` transitions are enabled, but when `next_state_butt=1`, the system switches from automatic to manual mode and resets to the initial signal configuration.
   对应摘录：C
5. 句子 5：This makes the sample more than a flat traffic FSM, because it retains an outer mode layer that supervises the inner timed phase transitions and the countdown-display behavior.
   对应摘录：A, B, C

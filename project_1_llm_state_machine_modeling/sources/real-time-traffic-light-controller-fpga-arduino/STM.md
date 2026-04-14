# Real-Time Traffic Light Controller System based on FPGA and Arduino - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次、显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出 `read / write / normal / blinking` 外层模式、九态交通灯循环、`TBASE / TEXT / TYEL / TBLINK` 四类时序参数和传感器/行人请求逻辑，足以形成双 A 的层次交通灯样本。

## 条目 1: Mode-Structured Nine-State Traffic-Light Controller

- 控制对象：带侧路传感器与行人请求的实时交通灯控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号领域的实时交通灯控制器，在 `read / write / normal / blinking` 模式选择之下，驱动一个带定时器、侧路拥堵扩展和行人按钮的九状态灯色循环。
- 判断：算。对象是明确的交通灯 controller，原文不仅给出 FPGA/Arduino 实现，还明确给出模式表、定时参数、九个交通灯状态以及传感器和行人请求的处理规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> The system is designed to manage street traffic control and assist walkers to move freely to prevent automobile crashes.
>
> To solve congestion problems at intersection roads, it is necessary to create a simple and reliable traffic control system.

#### 摘录 B

- 出处：第 5 页，Table 1 / Table 2 与正文
> L1 L0 Time Type
> 0 0 TBASE
> 0 1 TEXT
> 1 0 TYEL
> 1 1 TBLINK
>
> In normal mode or blinking mode, the system just cycles through the various traffic light states. As shown in Table 2, the designed controller has been modelled with nine states without taking the traffic sensors and pedestrian request into account.

#### 摘录 C

- 出处：第 5 页，Normal / Blinking mode 说明
> In normal mode, the main road has a longer green interval than the side road, but if there is congestion on the side road when the controller is about to switch the green light off, it will extend the green light by the shorter side street green interval.
>
> After finishing the main street yellow interval, and then only if the pedestrian request button is pressed, the walk light will turn on.
>
> Late at night or when something in the system is not working, the blinking mode will activate which means the lights will blink on and off, alternating between side red, main yellow and side yellow, main red.

#### 摘录 D

- 出处：第 6 页，Section 4.1.1
> The design system is composed of a finite state machine (FSM), data storage (D_RAM), timer, divider, and various synchronizers ...
>
> A divider is used to generate the clock (1 MHz) for an overall system from 50 MHz of the chip FPGA Spartan 3E.
>
> Sec_pulse is used to generate a one-second clock, which is used in the timing of the traffic lights.
>
> A timer is implemented as a counter.

### 2. 基于原文整理后的自然语言描述

The proposed traffic-light controller is best understood as a layered timed controller rather than a flat lamp sequencer. At the outer level, it distinguishes at least four operating modes: `read`, `write`, `normal`, and `blinking`, where `read` and `write` are used to inspect or update timing parameters and `normal`/`blinking` drive the actual signal behavior. Inside the operational branch, the paper models the traffic-light cycle with nine states and four timing parameters, `TBASE`, `TEXT`, `TYEL`, and `TBLINK`, implemented through an `FSM + D_RAM + timer + divider` architecture. The FPGA path derives a `1 MHz` internal clock from the `50 MHz` board clock and then produces a one-second pulse for traffic-light timing, so green, yellow, walk, and blink intervals are all explicit counter-driven dwell states. In normal operation, side-road congestion can extend the side-street green interval, and a latched pedestrian request activates the walk light after the main-street yellow interval. When late-night or fault conditions occur, the controller switches to blinking mode and alternates the two yellow/red lamp patterns instead of running the full junction sequence.

### 3. 逐句溯源

1. 句子 1：The proposed traffic-light controller is best understood as a layered timed controller rather than a flat lamp sequencer.
   对应摘录：A, B, D
2. 句子 2：At the outer level, it distinguishes at least four operating modes: `read`, `write`, `normal`, and `blinking`, where `read` and `write` are used to inspect or update timing parameters and `normal`/`blinking` drive the actual signal behavior.
   对应摘录：B
3. 句子 3：Inside the operational branch, the paper models the traffic-light cycle with nine states and four timing parameters, `TBASE`, `TEXT`, `TYEL`, and `TBLINK`, implemented through an `FSM + D_RAM + timer + divider` architecture.
   对应摘录：B, D
4. 句子 4：The FPGA path derives a `1 MHz` internal clock from the `50 MHz` board clock and then produces a one-second pulse for traffic-light timing, so green, yellow, walk, and blink intervals are all explicit counter-driven dwell states.
   对应摘录：D
5. 句子 5：In normal operation, side-road congestion can extend the side-street green interval, and a latched pedestrian request activates the walk light after the main-street yellow interval.
   对应摘录：C
6. 句子 6：When late-night or fault conditions occur, the controller switches to blinking mode and alternates the two yellow/red lamp patterns instead of running the full junction sequence.
   对应摘录：C

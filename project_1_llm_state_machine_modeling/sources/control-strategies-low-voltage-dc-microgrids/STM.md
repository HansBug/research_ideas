# Control Strategies for Low Voltage DC Microgrids - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：原文在第 6 章把低压直流微电网接口变换器写成两级状态机，第一层负责信号发送/接收，第二层负责 `sleep / droop / power` 模式切换，细节足以形成双 A 的过程控制样本。

## 条目 1: Two-Level Converter Signalling and Mode-Switch Controller
- 控制对象：过程与环境控制领域的低压直流微电网接口变换器协调控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向低压直流微电网接口变换器的两级层次状态机，上层协调信号发送/接收，下层协调 `sleep / droop / power` 三种工作模式。
- 判断：算。对象是实际微电网接口变换器控制逻辑，原文明确给出两级状态机、各状态职责、模式切换条件和负载/信号驱动的源切换过程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 126 页，`6.4.2 System State Machine`，`paper_content.txt` 第 3510-3538 行
> The system state machine contains two levels. The first level is for signal series sending and receiving.
> State I: this state mainly includes the initializations. The functions of the converter need to be determined by the users. If this
> converter is operated as a grid-connected converter, then it will not need to send signals and will directly step into state III. If the
> converter is operated as a normal converter, it will step into state II for signal series sending.
> State II: this state is responsible for the signal sending. After finishing sending the signal series, it will step into state III.
> State III: this state is the centre of the state machine. In this state, the controller always monitors the common DC bus voltage ...
> State IV: this state is responsible for signal receiving. After the signal series is received, it will step into state III.

#### 摘录 B
- 出处：第 126-127 页，第一层状态机中的中心状态说明，`paper_content.txt` 第 3532-3542 行
> State III: this state is the centre of the state machine. In this state, the controller always monitors the common DC bus voltage,
> and determines if any signal voltage comes through. This state also contains the second level state machines for the transfer
> between sleep mode, droop mode and power mode. When the signal voltage arrives, it will trigger the receiving algorithm in
> state IV. In addition, it will react to the load situations and automatically or manually trigger the sending algorithm in state II
> to switch on other sources in DC microgrids for charging/discharging operations.

#### 摘录 C
- 出处：第 127 页，`Figure 6.15 State machine switches of different working modes`，`paper_content.txt` 第 3546-3569 行
> The second level state machine is included in state III in the first level. At this level, it mainly deals with the mode switch
> between sleep mode, droop mode and power mode according to the signal series attained at the first level.
> State I: in this state, the interface converter works under sleep mode, monitoring the DC bus voltage and waiting for the
> potential signal series from other interface converters.
> State II: in this state, the interface converter works under droop control mode. The grid converter will firstly step into this mode.
> State III: in this state, the interface converter will work under power control mode. The reference current in the control loop is
> determined by the signal series and it interacts with battery’s SoC. When the battery is fully charged, it will go to sleep in state I.

### 2. 基于原文整理后的自然语言描述

The thesis models the low-voltage DC microgrid interface-converter logic as a two-level hierarchical state machine rather than as a flat list of operating modes. At the first level, the converter moves among initialization `State I`, signal sending `State II`, central monitoring `State III`, and signal receiving `State IV`, using converter role, sending completion, signal arrival, and load-driven source requests to decide whether to bypass communication, send a signal series, or switch into reception. `State III` is the hub of that upper machine because it continuously monitors the common DC bus voltage, detects arriving signal voltages, and triggers charging or discharging coordination by invoking either the receiving path or a new sending cycle. Inside `State III`, a second-level machine switches the interface converter among `sleep mode`, `droop mode`, and `power mode` according to the signal series obtained from the first level. Non-grid converters start in sleep mode, the grid converter starts in droop mode, and a converter in power mode can return to sleep once the battery reaches full charge, so the whole design forms a concrete hierarchical controller for plug-and-play source coordination in a DC microgrid.

### 3. 逐句溯源

1. 句子 1：The thesis models the low-voltage DC microgrid interface-converter logic as a two-level hierarchical state machine rather than as a flat list of operating modes.
   对应摘录：A, C
2. 句子 2：At the first level, the converter moves among initialization `State I`, signal sending `State II`, central monitoring `State III`, and signal receiving `State IV`, using converter role, sending completion, signal arrival, and load-driven source requests to decide whether to bypass communication, send a signal series, or switch into reception.
   对应摘录：A
3. 句子 3：`State III` is the hub of that upper machine because it continuously monitors the common DC bus voltage, detects arriving signal voltages, and triggers charging or discharging coordination by invoking either the receiving path or a new sending cycle.
   对应摘录：B
4. 句子 4：Inside `State III`, a second-level machine switches the interface converter among `sleep mode`, `droop mode`, and `power mode` according to the signal series obtained from the first level.
   对应摘录：B, C
5. 句子 5：Non-grid converters start in sleep mode, the grid converter starts in droop mode, and a converter in power mode can return to sleep once the battery reaches full charge, so the whole design forms a concrete hierarchical controller for plug-and-play source coordination in a DC microgrid.
   对应摘录：C

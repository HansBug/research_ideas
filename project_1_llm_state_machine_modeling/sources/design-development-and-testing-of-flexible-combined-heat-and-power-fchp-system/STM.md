# Design, Development, and Testing of a Flexible Combined Heat and Power (F-CHP) System With 10-kV SiC MOSFET-Based Power Conditioning System (PCS) Converter - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然整体还覆盖 PCS 硬件设计，但中央控制器的 `off / ready-to-run / grid-connected / islanded / fault` 模式机写得足够具体，包含 grid availability、BESS 电压阈值、islanding 和故障恢复逻辑，可以直接形成 `🌡️` 方向的高质量能源管理模式样本。

## 条目 1: F-CHP central controller mode manager

- 控制对象：过程与环境控制领域的 F-CHP 能源系统中央控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个协调 CHP 源、BESS、PCS 变换器、本地负载与并网/孤岛模式切换的系统级中央控制器。
- 判断：算。对象是实际 F-CHP 能源系统里的模式管理控制器，原文直接给出状态机结构、各模式职责、grid loss / reconnection / fault 触发和 BESS 接管逻辑，不是泛泛的能源管理框架说明。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Introduction
> The F-CHP central controller is similar to the central controller in a microgrid with similar control functions, including energy management, state machine, economic operation based on source and load forecasting, power balancing, protection coordination, model transitions, and data logging.

#### 摘录 B

- 出处：第 4-5 页，`The F-CHP System With Power Electronic Converters`
> The two main operation modes of the F-CHP system are the grid-connected mode and the islanded mode. The F-CHP system operates in the grid-connected mode when the MV ac grid is available. ... In the islanded mode ... the PCS converter will operate in grid forming mode.

#### 摘录 C

- 出处：第 6-7 页，`F. The State Machine`
> The state machine of the F-CHP central controller is shown in Fig. 6. It starts with the off state and goes to the ready-to-run state when the system is enabled. When starting up the system, if the ac grid is available, the system will start to the grid-connected mode. ... When the ac grid is unavailable, the system starts to the islanded mode.

#### 摘录 D

- 出处：第 6-7 页，`F. The State Machine`
> Because of its fast response, the BESS is designed to operate as a voltage source when the LV dc bus voltage is below a threshold value Vth1 or higher than the other threshold value Vth2. ... When the ac grid is suddenly lost, once the PCS converter identifies the islanding it stops operating and gives up the role of LV dc bus voltage control. ... In the islanded mode, the BESS controls the LV dc bus voltage. ... All the active states (excluding the off state) can go to the fault state if any fault in the system happens, and the fault state can only go to the ready-to-run state.

### 2. 基于原文整理后的自然语言描述

The F-CHP central controller is organized as a mode-management state machine that begins in `off`, moves to `ready-to-run`, and then chooses either `grid-connected` or `islanded` operation depending on whether the MV ac grid is available at startup. In the grid-connected state, the PCS converter regulates the LV dc bus and the local sources follow central power commands, while the BESS only takes an active voltage-source role when the bus voltage crosses threshold values `Vth1` or `Vth2`. If the grid is suddenly lost, the controller receives islanding information, stops PCS bus-voltage control, and transfers LV dc bus regulation to the BESS so that the system can continue in islanded operation. When the grid returns, the BESS switches back to droop-based support and the PCS resumes dc-bus regulation, so reconnection is treated as a mode handover rather than a fresh start. Any active operating mode can jump to `fault`, and recovery is constrained to pass through `ready-to-run`, which makes fault clearance and restart an explicit branch of the supervisory logic.

### 3. 逐句溯源

1. 句子 1：The F-CHP central controller is organized as a mode-management state machine that begins in `off`, moves to `ready-to-run`, and then chooses either `grid-connected` or `islanded` operation depending on whether the MV ac grid is available at startup.
   对应摘录：B, C
2. 句子 2：In the grid-connected state, the PCS converter regulates the LV dc bus and the local sources follow central power commands, while the BESS only takes an active voltage-source role when the bus voltage crosses threshold values `Vth1` or `Vth2`.
   对应摘录：C, D
3. 句子 3：If the grid is suddenly lost, the controller receives islanding information, stops PCS bus-voltage control, and transfers LV dc bus regulation to the BESS so that the system can continue in islanded operation.
   对应摘录：C, D
4. 句子 4：When the grid returns, the BESS switches back to droop-based support and the PCS resumes dc-bus regulation, so reconnection is treated as a mode handover rather than a fresh start.
   对应摘录：D
5. 句子 5：Any active operating mode can jump to `fault`, and recovery is constrained to pass through `ready-to-run`, which makes fault clearance and restart an explicit branch of the supervisory logic.
   对应摘录：D

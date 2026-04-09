# Accelerating Urban Traffic Management via FPGA-Based FSM Architecture - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四向路口控制器明确写成六状态 Moore FSM，并给出 `30/5/2 s` 配时、`1 Hz` 定时逻辑和板级测试行为，足以形成 `FSM + T1` 双 A 样本。

## 条目 1: Six-State Four-Way Traffic Light Moore Controller
- 控制对象：道路交通信号控制领域的四向路口定时交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个部署在 `Basys 3` 板上的四向路口交通灯控制器，用六个离散相位状态和固定秒级定时控制南北、东西两个方向的红黄绿灯切换。
- 判断：算。对象是明确的 four-way traffic controller，不是单纯 FPGA 指标展示；原文给出了状态名、相位顺序、每相位时长、时钟分频与按钮传感输入。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 15-30 行
> This paper presents the design and implementation of a traffic controller system on a Digilent Basys 3 FPGA board using Verilog Hardware Description Language (HDL). The system manages traffic light sequences at a four-way intersection, employing a Moore finite state machine to ensure deterministic transitions between green, yellow, and red states for North-South and East-West roads. Pushbuttons simulate car detection sensors, while timers control light durations (30 s green, 5 s yellow, 2 s red).

#### 摘录 B
- 出处：第 4-5 页，`Moore Finite State Machine / Control Logic`，`paper_content.txt` 第 153-178 行
> The Moore FSM has six states, ensuring stable light sequences: • NS Green: North-South green, East-West red (30 s). • NS Yellow: North-South yellow, East-West red (5 s). • NS Red: North-South red, East-West red (2 s). • EW Green: East-West green, North-South red (30 s). • EW Yellow: East-West yellow, North-South red (5 s). • EW Red: East-West red, North-South red (2 s). ... The control logic integrates: • Clock Divider: Converts 100 MHz clock to 1 Hz for timer operation. • Timer: Counts seconds for state transitions. • State Machine: Processes button inputs to trigger transitions. • Output Logic: Maps FSM states to LED outputs.

#### 摘录 C
- 出处：第 8 页，`Simulation Testing / Hardware Testing`，`paper_content.txt` 第 250-269 行
> Simulation was conducted using Vivado’s testbench ... The simulation confirmed: • Correct cycling through NS Green, NS Yellow, NS Red, EW Green, EW Yellow, EW Red. • Accurate timing (30 s green, 5 s yellow, 2 s red). • Proper response to button presses for sensor simulation. ... Functional Testing: Observed LED sequences over multiple cycles, confirming alignment with FSM states ... Sensor Simulation: Pressed buttons to emulate vehicles, verifying state transitions.

### 2. 基于原文整理后的自然语言描述

The traffic controller models a four-way intersection as a six-state Moore machine whose states are `NS Green`, `NS Yellow`, `NS Red`, `EW Green`, `EW Yellow`, and `EW Red`. Each state corresponds to a complete lamp configuration and is paired with explicit engineering durations: `30 s` for green, `5 s` for yellow, and `2 s` for all-red changeover. The control logic derives a `1 Hz` timer from the `100 MHz` FPGA clock, counts seconds for state transitions, and accepts pushbutton inputs as vehicle-detection surrogates during simulation and board testing. The reported tests confirm both the normal phase order and the button-driven transition behavior, so the paper exposes a complete `FSM + T1` traffic-light sample with explicit states, outputs, and timing semantics.

### 3. 逐句溯源

1. 句子 1：The traffic controller models a four-way intersection as a six-state Moore machine whose states are `NS Green`, `NS Yellow`, `NS Red`, `EW Green`, `EW Yellow`, and `EW Red`.
   对应摘录：A, B
2. 句子 2：Each state corresponds to a complete lamp configuration and is paired with explicit engineering durations: `30 s` for green, `5 s` for yellow, and `2 s` for all-red changeover.
   对应摘录：A, B, C
3. 句子 3：The control logic derives a `1 Hz` timer from the `100 MHz` FPGA clock, counts seconds for state transitions, and accepts pushbutton inputs as vehicle-detection surrogates during simulation and board testing.
   对应摘录：A, B, C
4. 句子 4：The reported tests confirm both the normal phase order and the button-driven transition behavior, so the paper exposes a complete `FSM + T1` traffic-light sample with explicit states, outputs, and timing semantics.
   对应摘录：C

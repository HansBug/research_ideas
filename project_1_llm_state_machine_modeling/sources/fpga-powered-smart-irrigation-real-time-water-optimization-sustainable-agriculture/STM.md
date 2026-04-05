# FPGA-Powered Smart Irrigation: Real-Time Water Optimization for Sustainable Agriculture - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把灌溉控制器直接写成同步有限状态机，明确给出三路传感输入、`111/101` 两个关键状态、继电器/蜂鸣器/LED 输出以及时钟驱动循环，足以形成 `🌡️` 方向的双 A 样本。

## 条目 1: Sensor-Vector Irrigation Pump and Alarm FSM

- 控制对象：过程与环境控制领域的 FPGA 智能灌溉监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个运行在 Artix-7 FPGA 上的灌溉控制器，用土壤湿度、水位和降雨三个二值传感输入，按同步状态机逻辑决定水泵继电器、低水位蜂鸣器和状态 LED 的动作。
- 判断：算。对象是真实灌溉控制系统，原文不仅说明了控制目标和硬件链路，还把输入向量、关键状态、输出映射和时钟循环都写成了可追溯的状态机式控制逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，Abstract，`paper_content.txt` 第 23-40 行
> This paper presents a highly innovative, FPGA-based smart irrigation system ... The control logic, developed in Verilog, employs a synchronous finite state machine to process sensor inputs and actuate a relay-controlled submerged pump, ensuring water delivery only when soil is dry, water is available, and no rainfall is detected. A buzzer alerts users to low water levels ... Simulation using Vivado validates the design’s robustness, with the relay activated solely in the 111 state ... and the buzzer in the 101 state ...

#### 摘录 B

- 出处：第 4 页，`I.2 System Overview / I.3 Technical Contributions`，`paper_content.txt` 第 79-94 行
> The proposed system integrates three sensors: a soil moisture sensor to detect soil dryness, a water level sensor to monitor tank/borewell availability, and a rain sensor to detect precipitation. These sensors feed into an EDGE Artix-7 FPGA, which processes inputs using a synchronous finite state machine implemented in Verilog ... The use of a 50 MHz clock ensures rapid response to environmental changes ...

#### 摘录 C

- 出处：第 7 页，`III.2 Control Logic Design`，`paper_content.txt` 第 169-176 行
> The control logic is implemented as a synchronous finite state machine (FSM) in Verilog, operating at 50 MHz. The FSM evaluates three binary inputs (moisture, water, rain) to produce three outputs: relay (pump control), buzzer (alert), and a 3-bit LED vector (status). The logic ensures the pump activates only when moisture=1, water=1, and rain=1 ... The buzzer is triggered when moisture=1, water=0, and rain=1 ...

#### 摘录 D

- 出处：第 8-9 页，`III.3 System Flow Chart / IV.1 Simulation`，`paper_content.txt` 第 184-190、226-238 行
> The process begins with sensor data acquisition ... Evaluate the 3-bit input vector (moisture, water, rain): If =111, activate the relay (=1) to start the pump and set LEDs to 101. If =101 ... trigger the buzzer (=1) and set LEDs to 111 ... Return to step 1, repeating every clock cycle (20 ns at 50 MHz).
>
> The simulation environment tested all eight possible combinations of the three binary sensor inputs ... For the input state moisture=1, water=1, rain=1 (binary 111), the relay output was activated ... For moisture=1, water=0, rain=1 (101), the buzzer was activated ...

### 2. 基于原文整理后的自然语言描述

The smart irrigation controller is implemented as a synchronous finite state machine on an Artix-7 FPGA, and it continuously evaluates a three-bit sensor vector made of soil moisture, water level, and rain status. The controller turns the submerged pump on only in the `111` state, which means dry soil, sufficient water, and no rain, while the `101` state triggers the buzzer to warn that irrigation is needed but the water source is insufficient. Outside those key conditions, the relay remains off and the LED outputs are updated to mirror the sensed environmental condition. The whole decision loop repeats every clock cycle under a `50 MHz` clock, so the paper treats irrigation as a real-time monitoring-and-actuation supervisor rather than a slow manual batch task. The hardware mapping is also explicit: the FPGA reads three binary sensors and directly drives the relay, buzzer, and three LED indicators through dedicated GPIO lines.

### 3. 逐句溯源

1. 句子 1：The smart irrigation controller is implemented as a synchronous finite state machine on an Artix-7 FPGA, and it continuously evaluates a three-bit sensor vector made of soil moisture, water level, and rain status.
   对应摘录：A, B, C
2. 句子 2：The controller turns the submerged pump on only in the `111` state, which means dry soil, sufficient water, and no rain, while the `101` state triggers the buzzer to warn that irrigation is needed but the water source is insufficient.
   对应摘录：A, C, D
3. 句子 3：Outside those key conditions, the relay remains off and the LED outputs are updated to mirror the sensed environmental condition.
   对应摘录：C, D
4. 句子 4：The whole decision loop repeats every clock cycle under a `50 MHz` clock, so the paper treats irrigation as a real-time monitoring-and-actuation supervisor rather than a slow manual batch task.
   对应摘录：B, D
5. 句子 5：The hardware mapping is also explicit: the FPGA reads three binary sensors and directly drives the relay, buzzer, and three LED indicators through dedicated GPIO lines.
   对应摘录：B, C, D

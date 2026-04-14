# FSM-Based Digital Design and RTL Synthesis of a Traffic Light Controller Using Verilog HDL and Cadence EDA Tools - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四向路口控制器写成八态 Moore FSM，并给出了固定周期、复位、安全性验证和综合结果。

## 条目 1: Eight-state Moore traffic-light controller
- 控制对象：道路交通信号领域的四向路口交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G1 固定相位交通灯）

### 0. 条目识别与判定

- 一句话说明：这是一个采用 Verilog 与 Cadence 工具实现的 Moore FSM 交通灯控制器，用八个状态轮转管理四个方向的绿灯与黄灯相位。
- 判断：算。对象是实际 traffic light controller，原文明确列出了状态集合、相位持续周期、时钟驱动转移和安全复位要求。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，`IV. FSM DESIGN METHODOLOGY`，行 155-170
> The controller of a traffic light is implemented as a Moore-type FSM: its output signals depend only on the current state.
> ...
> In this FSM there are eight states, including four green and four corresponding yellow states, one pair in each direction
> ...
> The state transitions in it are synchronized with the rising edge of the clock.
> ...
> It follows a timing mechanism with a counter that decides on the transitions.
> ...
> The FSM is initialized asynchronously to an active-high reset into a safe default state to ensure that the startup behavior will be predictable.

#### 摘录 B
- 出处：第 3 页，状态表与其说明，行 183-197
> Current State / Duration / Next State / Active Direction
> North Green / 8 cycles / North Yellow / North
> North Yellow / 4 cycles / South Green / North
> South Green / 8 cycles / South Yellow / South
> South Yellow / 4 cycles / East Green / South
> East Green / 8 cycles / East Yellow / East
> East Yellow / 4 cycles / West Green / East
> West Green / 8 cycles / West Yellow / West
> West Yellow / 4 cycles / North Green / West
> ...
> The state transition should be cyclic, which will grant every direction a fair and orderly flow of traffic.

#### 摘录 C
- 出处：第 3-4 页，`FUNCTIONAL VERIFICATION / RESULTS AND PERFORMANCE ANALYSIS / DISCUSSION`，行 202-214, 239-244, 278-281
> there is a dedicated testbench that generates a periodic clock and applies an asynchronous reset during the first few hundred nanoseconds into the simulation.
> ...
> mutual exclusivity of traffic signals verifies that there are no illegal states or green signal overlaps in extended simulation runs
> ...
> The post-synthesis timing analysis reveals a critical path delay of 1.294 ns
> ...
> the simulation results from the waveform diagrams show the proper phase transition of the traffic signal and validate the Moore FSM design style in which the outputs do not depend on the inputs directly but depend on the current state only.

### 2. 基于原文整理后的自然语言描述

The traffic-light controller is implemented as a Moore FSM with eight cyclic states: four green phases and four corresponding yellow phases, one pair for each direction. State transitions occur on the rising clock edge and are driven by a counter-based timing mechanism, with green phases lasting `8` cycles and yellow phases lasting `4` cycles before handing control to the next direction in the fixed order North, South, East, and West. The controller is also equipped with an asynchronous active-high reset that forces a safe default startup state, and simulation explicitly checks that no illegal overlap of green signals occurs during repeated cycles. Functional verification and synthesis then confirm the timed phase sequence under a `10 ns` clock constraint, with a reported critical-path delay of about `1.294 ns`.

### 3. 逐句溯源

1. 句子 1：The traffic-light controller is implemented as a Moore FSM with eight cyclic states: four green phases and four corresponding yellow phases, one pair for each direction.
   对应摘录：A, B
2. 句子 2：State transitions occur on the rising clock edge and are driven by a counter-based timing mechanism, with green phases lasting `8` cycles and yellow phases lasting `4` cycles before handing control to the next direction in the fixed order North, South, East, and West.
   对应摘录：A, B
3. 句子 3：The controller is also equipped with an asynchronous active-high reset that forces a safe default startup state, and simulation explicitly checks that no illegal overlap of green signals occurs during repeated cycles.
   对应摘录：A, C
4. 句子 4：Functional verification and synthesis then confirm the timed phase sequence under a `10 ns` clock constraint, with a reported critical-path delay of about `1.294 ns`.
   对应摘录：C

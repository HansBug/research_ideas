# Implementation of a Fully Automatic Four-way Traffic Light Controller Using Verilog - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四向路口写成 `S0-S7` 八态 Verilog/Mealy FSM，并明确给出 `16 / 8 / 4 seconds` 驻留时间和 `64 seconds` 全周期，属于典型的双 A 交通灯样本。

## 条目 1: Eight-State Four-Way Traffic-Light Mealy Controller

- 控制对象：道路交通信号控制领域的四向路口 Verilog 配时与安全黄灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向四向交叉路口的 Verilog 交通灯控制器，用 `S0-S7` 八态链、红黄绿输出和显式秒级配时来组织车辆放行与安全黄灯过渡。
- 判断：算。对象是实际交通灯控制器，而不是通用 FPGA 平台说明；原文直接写出了 FSM 类型、状态数、每态驻留时间和红黄绿输出表。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract / Introduction，`paper_content.txt` 第 21-31、67-83 行
> In this project, the Fully Automatic Four-way Traffic light controller is implemented by using Verilog and we have overcome some drawbacks i.e., we included the area detection parameter that improves the detection of vehicles compared to the design part in the base paper.
>
> Melay model of Finite State Machine (FSM) is used to design the traffic light controller system ... The traffic controller system also makes use of the maximum possible number of safe states. Before the stoppage of traffic across each direction, the yellow signal is displayed ... The states containing yellow signals act as safe states and prevent the possibility of accidents.

#### 摘录 B

- 出处：第 2 页，`IV. State Diagram`，`paper_content.txt` 第 121-137 行
> The vehicle movement during the S0 and S4 states ... are comparatively higher than that during the other states ... The signal timing for two states is set to 16 seconds and for S2 and S6 states, the signal timing is set to 8 seconds, and for S1, S3, S5, and S7, the signal timing is set to 4 seconds. ... After the S7 state, the system again enters into the S0 state and this cycle continues. The time taken for the system to complete one full cycle is 64 seconds.

#### 摘录 C

- 出处：第 2-3 页，`V. State Table / VI. Results and Discussion`，`paper_content.txt` 第 141-175 行
> In each of the states, if the bit is 3, it indicates that the light display is showing a red signal ... if the bit is 2, it corresponds to a yellow signal ... if the bit is 1, it corresponds to a green signal ... The S1, S3, S5, and S7 states act as ‘safe’ states ...
>
> State North East South West No. of Clock cycles
> S0 1 3 3 3 16
> S1 2 2 3 3 4
> S2 3 1 3 3 8
> S3 3 2 2 3 4
> S4 3 3 1 3 16
> S5 3 3 2 2 4
> S6 3 3 3 1 8
> S7 2 3 3 2 4

### 2. 基于原文整理后的自然语言描述

The controller is an explicitly named Mealy FSM for a four-way road intersection rather than a fixed-delay lamp driver. It cycles through eight states `S0` to `S7`, where `S0` and `S4` are the long green phases for the heavier-movement directions, `S2` and `S6` are intermediate green phases, and `S1 / S3 / S5 / S7` are yellow safe states inserted before traffic is stopped in the corresponding directions. The dwell times are also explicit: `S0` and `S4` last `16` seconds, `S2` and `S6` last `8` seconds, and the yellow safety states last `4` seconds, producing a `64` second full cycle before the machine returns from `S7` to `S0`. Because both the output colors and the transition schedule are fully enumerated in the state table, this paper is a clean FSM/T1 traffic-light sample rather than a generic HDL implementation note.

### 3. 逐句溯源

1. 句子 1：The controller is an explicitly named Mealy FSM for a four-way road intersection rather than a fixed-delay lamp driver.
   对应摘录：A
2. 句子 2：It cycles through eight states `S0` to `S7`, where `S0` and `S4` are the long green phases for the heavier-movement directions, `S2` and `S6` are intermediate green phases, and `S1 / S3 / S5 / S7` are yellow safe states inserted before traffic is stopped in the corresponding directions.
   对应摘录：A, B, C
3. 句子 3：The dwell times are also explicit: `S0` and `S4` last `16` seconds, `S2` and `S6` last `8` seconds, and the yellow safety states last `4` seconds, producing a `64` second full cycle before the machine returns from `S7` to `S0`.
   对应摘录：B, C
4. 句子 4：Because both the output colors and the transition schedule are fully enumerated in the state table, this paper is a clean FSM/T1 traffic-light sample rather than a generic HDL implementation note.
   对应摘录：A, B, C

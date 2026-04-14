# VHDL Based FPGA Implemented Advanced Traffic Light Controller System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文有明确 `TLC state diagram`，用 `cnt` 和 `dir` 表达四向绿灯/黄灯/行人相位轮转，并说明传感器和计数器如何调整绿灯时长，可形成 `FSM + T1` 交通灯样本。

## 条目 1: Four-Direction Congestion-Aware Traffic-Light Phase FSM

- 控制对象：道路交通信号领域的 FPGA/VHDL 四向路口交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 VHDL 在 FPGA 上实现的四向交通灯相位状态机，同时用道路传感器和车辆计数影响绿灯延时。
- 判断：算。论文直接给出 state diagram 解释，列出 `cnt/dir` 的相位切换和 reset 行为，且包含传感器对延时的影响。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`System Implementation / Roads Structure`
> Four sensors `SW1-SW4` are placed on lanes and linked with signals `L1-L8`; when a sensor output is enabled, the appropriate traffic continues on the road.

#### 摘录 B

- 出处：第 3 页，`State Diagram`
> When `cnt=00` and `dir=00`, the north green light is on and the other directions are red; `cnt=01` activates yellow and pedestrian north, then `dir` increments.

#### 摘录 C

- 出处：第 3-4 页，`State Diagram / Hardware Implementation`
> The sequence repeats for east, south, and west; reset sets `cnt` and `dir` to `00`, and sensors can change the delay from one state to another when congestion is detected.

### 2. 基于原文整理后的自然语言描述

The FPGA traffic-light controller is a VHDL-coded phase FSM driven by a clock and reset input. When reset enables the controller, `cnt` and `dir` are initialized to `00`, which selects the north-direction green phase while west, south, and east remain red. The next `cnt` phase turns on the yellow and pedestrian signal for the current direction, then increments `dir` and resets `cnt` so that the same green-yellow/pedestrian pattern is applied to east, south, and west in sequence. After the west yellow/pedestrian phase, `dir` returns to `00` and the phase cycle repeats. Road sensors and up/down counters observe vehicle presence, vehicle count, and weight, and the controller uses this information to lengthen or shorten the delay between states, for example extending a congested lane's green time.

### 3. 逐句溯源

1. 句子 1：The FPGA traffic-light controller is a VHDL-coded phase FSM driven by a clock and reset input.
   对应摘录：C
2. 句子 2：When reset enables the controller, `cnt` and `dir` are initialized to `00`, which selects the north-direction green phase while west, south, and east remain red.
   对应摘录：B, C
3. 句子 3：The next `cnt` phase turns on the yellow and pedestrian signal for the current direction, then increments `dir` and resets `cnt` so that the same green-yellow/pedestrian pattern is applied to east, south, and west in sequence.
   对应摘录：B, C
4. 句子 4：After the west yellow/pedestrian phase, `dir` returns to `00` and the phase cycle repeats.
   对应摘录：C
5. 句子 5：Road sensors and up/down counters observe vehicle presence, vehicle count, and weight, and the controller uses this information to lengthen or shorten the delay between states, for example extending a congested lane's green time.
   对应摘录：A, C

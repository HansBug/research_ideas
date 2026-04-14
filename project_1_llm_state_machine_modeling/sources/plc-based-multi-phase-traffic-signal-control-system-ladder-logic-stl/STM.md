# DESIGN AND IMPLEMENTATION OF A PLC-BASED MULTI-PHASE TRAFFIC SIGNAL CONTROL SYSTEM USING LADDER LOGIC & STL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把多相位交通灯写成有限状态与定时表，并给出 `Q0.0 / Q0.1 / Q0.3` 输出映射、状态图和 `10/5/10/5/10` 秒相位序列，是非常标准的双 A 交通信号样本。

## 备注

- `paper_content.txt` 存在少量连字和空格缺失，但状态图、时序表、输出映射和状态方程在文本中仍可稳定定位，不影响案例抽取。

## 条目 1: Multi-phase timed traffic signal FSM

- 控制对象：多相位 PLC 交通信号控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个多相位 PLC 交通信号状态机，用定时状态和固定输出映射驱动红灯、黄灯、绿灯，并显式保证相位互斥。
- 判断：算。对象是实际交通信号控制器，原文明确给出状态图、状态方程、相位时长和 `Q0.0 / Q0.1 / Q0.3` 输出映射。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / Introduction，`paper_content.txt` 第 20-31 行、第 120-126 行
> this work presents the design and implementation of a multi-phase traffic signal control system based on a Programmable Logic Controller (PLC) ... The proposed system employs a deterministic, timer-driven sequencing strategy to precisely regulate red, yellow, and green signal phases, ensuring conflict-free operation and predictable traffic flow.
>
> The system uses the red signal, yellow signal, and green signal phases, which are managed in a safe and conflict-free way using timer-based sequencing.

#### 摘录 B

- 出处：第 3-4 页，`III. System Design / A. Conceptual System Architecture`，`paper_content.txt` 第 197-223 行
> The system is of a fixed-time control strategy whereby red, yellow, and green traffic lights are turned on in order through timer controlled logic. The design has the benefit of ensuring that there are no traffic conflicts as only one signal will be active at any given time.
>
> Output Q0.0 controls the red lamp, Q0.1 controls the yellow lamp, and Q0.3 controls the green lamp. A timer module inside the PLC governs the duration of each signal phase. The PLC executes the programmed logic cyclically. Based on the timer value, the PLC switches the active output and resets the previous output.

#### 摘录 C

- 出处：第 7-9 页，`E. State Analysis / Table I / B. Ladder Logic Program Verification`，`paper_content.txt` 第 315-349 行、第 419-429 行
> the traffic signal sequence is represented using finite states. Each state corresponds to a unique combination of signal outputs ... The system starts from state S1 and progresses sequentially through all states before returning to S1.
>
> Table I: Traffic Signal Timing Sequence ... 1 ON OFF OFF T32 10 ... 2 OFF ON OFF T32 5 ... 3 OFF OFF ON T32 10 ... 4 OFF ON OFF T32 5 ... 5 ON OFF OFF T32 10.
>
> The ladder program verifies that: Red signal activates for the first time interval. Yellow signal activates during transition. Green signal activates after yellow phase. Outputs are mutually exclusive.

### 2. 基于原文整理后的自然语言描述

The controller is organized as a timed finite-state machine in which each state corresponds to a unique red-yellow-green output combination. The PLC maps `Q0.0` to red, `Q0.1` to yellow, and `Q0.3` to green, and a timer module drives phase advancement so the logic cycles automatically from one state to the next. The paper states that the machine starts from `S1`, progresses sequentially through the remaining states, and then returns to `S1`, while Table I fixes the phase schedule as `10 s` red, `5 s` yellow, `10 s` green, `5 s` yellow, and `10 s` red before reset. Because the ladder logic keeps the outputs mutually exclusive, the design enforces a conflict-free multi-phase traffic signal cycle with explicit state, output, and timing semantics.

### 3. 逐句溯源

1. 句子 1：The controller is organized as a timed finite-state machine in which each state corresponds to a unique red-yellow-green output combination.
   对应摘录：A, C
2. 句子 2：The PLC maps `Q0.0` to red, `Q0.1` to yellow, and `Q0.3` to green, and a timer module drives phase advancement so the logic cycles automatically from one state to the next.
   对应摘录：B
3. 句子 3：The paper states that the machine starts from `S1`, progresses sequentially through the remaining states, and then returns to `S1`, while Table I fixes the phase schedule as `10 s` red, `5 s` yellow, `10 s` green, `5 s` yellow, and `10 s` red before reset.
   对应摘录：C
4. 句子 4：Because the ladder logic keeps the outputs mutually exclusive, the design enforces a conflict-free multi-phase traffic signal cycle with explicit state, output, and timing semantics.
   对应摘录：A, B, C

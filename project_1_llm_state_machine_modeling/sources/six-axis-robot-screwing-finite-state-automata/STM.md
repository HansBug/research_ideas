# Implementation of Finite State Automata for 6-Axis Robot in the Screwing Process - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把六轴机器人螺接工位的状态集、输入输出集合、转移表和输出表全部列出，是一条很完整的离散机器人作业顺序链。

## 条目 1: Six-state robot screwing Mealy controller

- 控制对象：工业自动化与离散制造领域的六轴机器人取刀、取螺钉与拧紧作业顺序控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业机器人螺接工位的作业顺序控制器，用于驱动六轴机器人在安全点、取刀位、螺钉供给位和拧紧位之间切换，并根据传感器反馈触发夹持、锁刀和拧紧动作。
- 判断：算。对象是实际 workcell controller，原文明确给出了状态集合、输入集合、输出集合、转移函数和输出函数，而不是只给一张示意图。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，`Table 1 / state sets`，`paper_content.txt` 第 157-175 行
> a tuple consisting of five elements, namely with the formula M = (Q, Σ, δ, S, F). The description of each element is as follows: state sets (Q), input symbol sets (Σ), transition function (δ), initial state (S), final state sets (F). So it can be defined as follows:
> Q: {S0, S1, S2, S3, S4, S5}
> Σ: {A, B, C, D, E, F, G, H, I, J}
> δ: transition function
> S: {S0}
> F: {S5}
> ... The initial state S0 serves as the system's starting point, where the robot remains idle, awaiting a signal to commence operations. Upon receiving the input, the robot proceeds to S1 to access the safe point tool ... The robot proceeds to S2 to retrieve the screwdriver tool ... the robot proceeds to S3 to the screw feeder location to get the screw ... the robot retreats to S4, designated as the secure position for screwing ... Ultimately, the robot transitions to state S5, designated as the Screwing Station, where the screwing operation is executed.

#### 摘录 B

- 出处：第 5-7 页，`Table 2 / Figure 4 / Table 3 / Table 4`，`paper_content.txt` 第 185-264 行
> Inputs are derived from several control signals, including the start push button and various sensors ... The outputs represent system responses ... tool locking and unlocking, activation of the vacuum mechanism, vertical motion of the screwdriver (up/down), object gripping, and initiation of the screwing process itself.
> In state S0, the robot awaits input from the push button labeled A. Upon receiving this input, the robot transitions to state S1, resulting in an output of off (0). In state S1, if the photoelectric sensor (B) identifies an object, the robot transitions to state S2. The generated output consists of tool unlock (b) and grip (f). ... Upon arriving at state S3, if the robot accesses the screw feeder (H), it transitions to state S4 with the output designated as vacuum (e). Upon attaining state S4, the robot proceeds to the screwing station (S5) to execute the screwing operation. The generated output activates the screwdriver (g) and the screwdriver down (c). The final state is S5 ...
> Table 3 illustrates the transition function δ ...
> Table 4 ... In state S5, the output from input J indicates the screwdriving operation with outputs g and c (screwdriver and screwdriver down) ...

### 2. 基于原文整理后的自然语言描述

The screwing controller is defined as a Mealy-style FSA `M = (Q, Σ, δ, S, F)` with `Q = {S0, S1, S2, S3, S4, S5}`, start state `S0`, and final state `S5`. The state set encodes a concrete robotic work sequence from idle to `Safe Point Tool`, `Screwdriver Tool`, `Screw Feeder`, `Safe Point Screwing`, and finally `Screwing Station`. The transition and output tables bind sensor and button inputs `A-J` to actions such as tool unlock, tool lock, vacuum gripping, screwdriver up/down, and screwing, so each movement stage is guarded by real-time feedback from photoelectric sensors, reed switches, and station-arrival signals. After the screwing step is completed, the table returns the controller toward the tool-handling state for the next cycle, giving a full `T0` finite-state workcell controller rather than a loose process narrative.

### 3. 逐句溯源

1. 句子 1：The screwing controller is defined as a Mealy-style FSA `M = (Q, Σ, δ, S, F)` with `Q = {S0, S1, S2, S3, S4, S5}`, start state `S0`, and final state `S5`.
   对应摘录：A
2. 句子 2：The state set encodes a concrete robotic work sequence from idle to `Safe Point Tool`, `Screwdriver Tool`, `Screw Feeder`, `Safe Point Screwing`, and finally `Screwing Station`.
   对应摘录：A
3. 句子 3：The transition and output tables bind sensor and button inputs `A-J` to actions such as tool unlock, tool lock, vacuum gripping, screwdriver up/down, and screwing, so each movement stage is guarded by real-time feedback from photoelectric sensors, reed switches, and station-arrival signals.
   对应摘录：B
4. 句子 4：After the screwing step is completed, the table returns the controller toward the tool-handling state for the next cycle, giving a full `T0` finite-state workcell controller rather than a loose process narrative.
   对应摘录：B

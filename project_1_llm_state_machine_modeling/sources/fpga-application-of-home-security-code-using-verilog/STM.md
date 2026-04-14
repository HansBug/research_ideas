# An FPGA application of home security code using verilog - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把门锁密码序列清楚写成 `IDLE -> S1 -> S2 -> S3` 四状态 FSM，并用按键模式与板级验证结果补齐了解锁链路，足以形成 `FSM + T0` 双 A 样本。

## 条目 1: Four-State Keypad Home Entry Code Lock
- 控制对象：楼宇机电与智能家居领域的四状态门禁密码锁控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个在 `DE2-115` 板上实现的家庭门禁密码锁控制器，支持按键按钮和矩阵键盘两种解锁模式，其中键盘模式被明确写成四状态状态机。
- 判断：算。对象是实际 home security code lock，而不是泛泛 FPGA 教学流程；原文给出了状态名、正确密码序列、错误回退语义以及板级验证输出。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 20-35 行
> Traditional entrance keys performed a number of drawbacks ... This project proposed a home security code lock using verilog hardware descriptive language (HDL) with two unlocking modes, using a button or a keypad which can be changed using a switch. ... The result of simulation on the keypad using finite state machine (FSM) technique was fulfill the theoretical concept in which it will go to the next state each time the correct input or passcode was entered. When the wrong input or passcode was entered, it will be entered to reset mode.

#### 摘录 B
- 出处：第 5 页，`Finite state machine`，`paper_content.txt` 第 183-188 行
> Figure 6 shows the state diagram for home security code lock using verilog HDL. It had 4 states which were IDLE, S1, S2 and S3. IDLE state represents when home entrance was lock while S3 when home entrance was unlocking. Transition from IDLE to S1 was 2, from S1 to S2 was 6 and from S2 to S3 was C. To return default state was by using the reset button.

#### 摘录 C
- 出处：第 6-8 页，`Switch on and keypad correctly pressed / Summary on verification`，`paper_content.txt` 第 246-306 行
> Figure 10 shows the output for the ModelSim simulation when the sequence of the keypad had been correctly pressed using the sequence of “2”, “6” and “c”. ... Figure 11 reflects the outcome of “L2” ... Figure 12 demonstrates the outcome of “L6” ... Figure 13 shows the outcome of “UC” stands for “Unlocked C” ... The “U” will notify that all the previously entered combination was correct and the system will be in “unlocked” or reset state. ... Table 3 ... 1 1 / / / U U

### 2. 基于原文整理后的自然语言描述

The keypad-controlled door lock is modeled as a four-state FSM with `IDLE`, `S1`, `S2`, and `S3` representing the progression from locked state to unlocked state. In keypad mode, the controller only advances when the correct symbol sequence `2 -> 6 -> C` is entered, so the transition chain is `IDLE -> S1 -> S2 -> S3`, while wrong input returns the machine to reset mode and the reset button also restores the default state. The verification results expose the same progression on hardware by showing `L2` after the first correct symbol, `L6` after the second, and `UC` only when the final symbol is accepted, at which point the system reports the unlocked condition. This gives a clean `FSM + T0` access-control sample with explicit states, input symbols, reset behavior, and observable outputs.

### 3. 逐句溯源

1. 句子 1：The keypad-controlled door lock is modeled as a four-state FSM with `IDLE`, `S1`, `S2`, and `S3` representing the progression from locked state to unlocked state.
   对应摘录：A, B
2. 句子 2：In keypad mode, the controller only advances when the correct symbol sequence `2 -> 6 -> C` is entered, so the transition chain is `IDLE -> S1 -> S2 -> S3`, while wrong input returns the machine to reset mode and the reset button also restores the default state.
   对应摘录：A, B
3. 句子 3：The verification results expose the same progression on hardware by showing `L2` after the first correct symbol, `L6` after the second, and `UC` only when the final symbol is accepted, at which point the system reports the unlocked condition.
   对应摘录：C
4. 句子 4：This gives a clean `FSM + T0` access-control sample with explicit states, input symbols, reset behavior, and observable outputs.
   对应摘录：A, B, C

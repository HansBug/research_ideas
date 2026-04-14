# PM-FSM: Policies Modulating Finite State Machine for Robust Quadrupedal Locomotion - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四足机器人步态控制器写成“每条腿子自动机 + 全局 FSM + 接触反射”的分层结构，并给出了状态语义、转移条件和上下楼反射触发条件。

## 条目 1: Contact-Aware Gait-and-Reflex Quadruped Controller
- 控制对象：四足机器人在平地、扰动和上下楼场景下的接触感知步态与反射控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是四足机器人 locomotion controller，把每条腿的子自动机、全局步态状态和基于接触事件的反射机制组合成一个接触感知状态机。
- 判断：算。对象是实际四足机器人步态控制主链，原文明确给出了接触标志与关节角作为上下文、`s1 / s2 / s3` 子状态语义、全局状态转移条件，以及上下楼反射的触发条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 16-23
> contact-aware finite state machines

#### 摘录 B
- 出处：第 3 页，Figure 3 / Section III-D，行 184-240
> "leg extension (s1)" ... "leg retraction (s2)" ... "support phase (s3)"

#### 摘录 C
- 出处：第 3-4 页，Section III-D / III-E，行 236-258
> "all swing legs make contacts"

### 2. 基于原文整理后的自然语言描述

The PM-FSM controller organizes quadruped locomotion as a contact-aware hierarchical FSM whose inputs include current foot-contact flags and joint angles. Each leg is modeled with a three-state sub-automaton composed of `s1` leg extension, `s2` leg retraction, and `s3` support/angle-adjustment, and the rows of the expanded gait matrix form the global FSM states that coordinate all four legs. The controller advances between global gait states when swing legs make contact or when joints reach their target angles, while policy-generated frequency, amplitude, and height continuously modulate the target leg motion inside those states. On top of the nominal gait chain, the FSM adds an upstairs reflex for unexpected early contact during `s1` and a downstairs reflex for dangling legs at the end of `s2`, so the same controller can recover from terrain-induced perturbations without leaving the state-machine framework. This combination of leg-level sub-automata, contact-triggered state transitions, and reflex branches makes the controller a strong `HSM + T0` locomotion sample.

### 3. 逐句溯源

1. 句子 1：The PM-FSM controller organizes quadruped locomotion as a contact-aware hierarchical FSM whose inputs include current foot-contact flags and joint angles.
   对应摘录：A, B
2. 句子 2：Each leg is modeled with a three-state sub-automaton composed of `s1` leg extension, `s2` leg retraction, and `s3` support/angle-adjustment, and the rows of the expanded gait matrix form the global FSM states that coordinate all four legs.
   对应摘录：B
3. 句子 3：The controller advances between global gait states when swing legs make contact or when joints reach their target angles, while policy-generated frequency, amplitude, and height continuously modulate the target leg motion inside those states.
   对应摘录：B, C
4. 句子 4：On top of the nominal gait chain, the FSM adds an upstairs reflex for unexpected early contact during `s1` and a downstairs reflex for dangling legs at the end of `s2`, so the same controller can recover from terrain-induced perturbations without leaving the state-machine framework.
   对应摘录：B, C
5. 句子 5：This combination of leg-level sub-automata, contact-triggered state transitions, and reflex branches makes the controller a strong `HSM + T0` locomotion sample.
   对应摘录：A, B, C

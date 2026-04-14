# A Simple Controller for Omnidirectional Trotting of Quadrupedal Robots: Command Following and Waypoint Tracking - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四足机器人 trot gait 的对角腿组切换写成了带固定步时 `ts` 的有限状态机，并明确给出了 swing/stance 切换、对角配对以及两类腿使用的控制律。

## 条目 1: Timed Diagonal-Pair Trotting Scheduler
- 控制对象：四足机器人在命令跟踪和航点跟踪中的对角步态调度控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是四足机器人 trot gait 的低层调度器，用固定步时 `ts` 协调 `FR-RL` 与 `FL-RR` 两组对角腿在 swing/stance 间切换，并为两类腿分配不同控制律。
- 判断：算。对象是实际四足机器人低层步态控制链，原文明确给出了有限状态机角色、对角腿配对关系、固定步时触发的状态切换，以及 stance/swing 腿分别采用的扭矩生成方式。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 36-39
> leg scheduler ... fixed step time

#### 摘录 B
- 出处：第 3 页，Section 3.2，行 173-180
> FR–RL and FL–RR

#### 摘录 C
- 出处：第 4 页，Section 3.10，行 318-324
> stance and swing legs

### 2. 基于原文整理后的自然语言描述

The quadruped low-level controller is driven by a finite state machine that schedules the trot gait with an explicit fixed step time `ts`. The FSM groups the legs into the diagonal pairs `FR-RL` and `FL-RR`, and these pairs alternate together between `swing` and `stance` as time-triggered states. The current FSM state is fed to the Cartesian trajectory generator so the controller can choose the proper leg trajectory profile and decide which torque law to apply. For stance legs, the torque command combines ground-reaction-force torque with feedback torque, while for swing legs it combines gravity torque with feedback torque. Because the high-level controller updates once per step and the state switch itself is tied to `ts`, the paper provides a clean `FSM + T1` sample for timed gait scheduling.

### 3. 逐句溯源

1. 句子 1：The quadruped low-level controller is driven by a finite state machine that schedules the trot gait with an explicit fixed step time `ts`.
   对应摘录：A, B
2. 句子 2：The FSM groups the legs into the diagonal pairs `FR-RL` and `FL-RR`, and these pairs alternate together between `swing` and `stance` as time-triggered states.
   对应摘录：B, C
3. 句子 3：The current FSM state is fed to the Cartesian trajectory generator so the controller can choose the proper leg trajectory profile and decide which torque law to apply.
   对应摘录：B, C
4. 句子 4：For stance legs, the torque command combines ground-reaction-force torque with feedback torque, while for swing legs it combines gravity torque with feedback torque.
   对应摘录：C
5. 句子 5：Because the high-level controller updates once per step and the state switch itself is tied to `ts`, the paper provides a clean `FSM + T1` sample for timed gait scheduling.
   对应摘录：A, B, C

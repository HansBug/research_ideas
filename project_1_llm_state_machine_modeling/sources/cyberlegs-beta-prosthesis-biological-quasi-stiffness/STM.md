# The Challenges and Achievements of Experimental Implementation of an Active Transfemoral Prosthesis Based on Biological Quasi-Stiffness: The CYBERLEGs Beta-Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出 `Early Stance / Late Stance / Swing / Late Swing` walking submachine，还保留 quiet standing / gait initiation / gait termination 的上层状态、`WSA` 触发链，以及 `Δt1 / Δt2` 两个绝对时间延迟，可直接作为 `HSM + T1` 样本。

## 条目 1: Hierarchical WSA-driven walking state machine for the CYBERLEGs Beta-Prosthesis
- 控制对象：`CYBERLEGs Beta-Prosthesis` 的 top-level walking supervisor
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 `CYBERLEGs Beta-Prosthesis` 的分层 walking supervisor，它在顶层处理 `quiet standing / gait initiation / gait termination`，在 walking 层再切分 `Early Stance / Late Stance / Swing / Late Swing`，并用 `WSA` 角速度、pressure insole 与两个绝对时间延迟去调度 knee、ankle 与 `WA` 位置。
- 判断：算。对象是真实主动股骨假肢控制器；原文明确写出了多层状态机、步态子状态、触发传感器、setpoint family 和 time-based transition delay。

### 1. 原文摘录

#### 摘录 A
- 出处：第 9 页，Section `2.3.2. Top Level Control`
> Control methods for the Beta-Prosthesis utilized a modified Intention Detection system and Wearable Sensory Apparatus controller with a finite state machine ... The state machine of the WSA contained a number of levels, the first including a quiet standing, gait initiation, and gait termination phases.

#### 摘录 B
- 出处：第 9 页，Section `2.3.2. Top Level Control`
> From the gait initiation phase the main walking state machine was entered. The walking state was broken into four different sub-states ... Early Stance (State 1), Late Stance (State 2), Swing (State 3), and Late Swing (State 4) ... triggered by a combination of the WSA angular velocity sensors as well as signals from pressure insoles.

#### 摘录 C
- 出处：第 10 页，Figure `10` caption
> The CYBERLEGs WSA was used to create the triggers for state transitions, using the angular velocity ... of the different limb sectors. The pressure insoles were used to determine if the feet were on the ground ... positions of each of the knee, ankle, and WA are shown.

#### 摘录 D
- 出处：第 11-12 页，Section `4.3. Preliminary Walking Experiments`
> Figure 14 shows ... the timing of the state machine transitions during the gait cycle. Also shown here are the two absolute time based transitions `Δt1` and `Δt2` ... between the beginning of State 2 and the unlocking of the WA and between State 4 and the locking of the WA.

### 2. 基于原文整理后的自然语言描述

The `CYBERLEGs Beta-Prosthesis` is governed by a hierarchical `WSA`-driven supervisor rather than by a single flat gait-state machine. At the top level, the controller distinguishes `quiet standing`, `gait initiation`, and `gait termination`, and only after initiation does it enter the main walking submachine. That walking submachine contains four explicit gait states, `Early Stance`, `Late Stance`, `Swing`, and `Late Swing`, which are triggered from wearable angular-velocity sensing and pressure-insole contact signals so that heel-strike, heel-off, toe-off, and terminal-swing events can be recognized on-line. The same walking-state machine simultaneously routes discrete setpoints for the knee, ankle, and `WA` mechanism, so state recognition and actuator-position selection are coupled in the supervisor itself. In addition to sensor-triggered transitions, the controller includes two absolute time-based delays, `Δt1` and `Δt2`, which schedule `WA` unlocking after the beginning of `State 2` and `WA` locking during `State 4`, making the sample a clear hierarchical gait controller with explicit local timing semantics.

### 3. 逐句溯源

1. 句子 1：The `CYBERLEGs Beta-Prosthesis` is governed by a hierarchical `WSA`-driven supervisor rather than by a single flat gait-state machine.
   对应摘录：A, B
2. 句子 2：At the top level, the controller distinguishes `quiet standing`, `gait initiation`, and `gait termination`, and only after initiation does it enter the main walking submachine.
   对应摘录：A, B
3. 句子 3：That walking submachine contains four explicit gait states, `Early Stance`, `Late Stance`, `Swing`, and `Late Swing`, which are triggered from wearable angular-velocity sensing and pressure-insole contact signals so that heel-strike, heel-off, toe-off, and terminal-swing events can be recognized on-line.
   对应摘录：B, C
4. 句子 4：The same walking-state machine simultaneously routes discrete setpoints for the knee, ankle, and `WA` mechanism, so state recognition and actuator-position selection are coupled in the supervisor itself.
   对应摘录：C
5. 句子 5：In addition to sensor-triggered transitions, the controller includes two absolute time-based delays, `Δt1` and `Δt2`, which schedule `WA` unlocking after the beginning of `State 2` and `WA` locking during `State 4`, making the sample a clear hierarchical gait controller with explicit local timing semantics.
   对应摘录：D

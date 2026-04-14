# A Muscle-First, Electromechanical Hybrid Gait Restoration System in People With Spinal Cord Injury - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `MAHNP` 的 muscle-first hybrid gait control 写成“定时 stimulation pattern + gait-event detector FSM + walk/stand/sit transition states”的层次控制结构，并明确给出 gait states、按钮/FSR 触发与 `250 µs / 60-30 ms` 时间参数，可直接入账为高质量 `HSM + T1` 样本。

## 条目 1: Hierarchical gait-event supervisor for the MAHNP hybrid restoration system
- 控制对象：`MAHNP` 混合神经刺激/外骨骼 gait restoration system 的 gait event detector 与 mode supervisor
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向截瘫患者 hybrid gait restoration system 的层次监督控制器，用定时刺激模式驱动肌肉，再由 gait-event `FSM` 叠加关节锁止/解锁和行走、站立、坐下转换逻辑。
- 判断：算。对象是真实混合步态恢复系统，不是纯康复实验流程；原文明确给出 gait states、state progression、触发条件和定时 stimulation 参数。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `2.2.1. Gait Event Detection`，行 301-317
> The stimulation pattern is open loop—a pre-programmed pattern of stimulation commands as a function of time is deployed to facilitate stepping.
>
> During gait with the MAHNP, this feedforward operation was kept, with exoskeleton control built on top of this. By treating the exoskeleton actions as an extension of the stimulation, this approach utilized full advantage of institutional knowledge of testing and tuning stimulation patterns and parameters for maximal effectiveness.

#### 摘录 B
- 出处：第 4 页，Section `2.2.1. Gait Event Detection`，行 318-332
> We implemented a GaitEventDetector (GED) as a finite state machine to determine the phase of gait from on board sensors and trigger the correct joint power commands.
>
> The MAHNP recognized the same gait states the stimulation used; `left swing`, `left double stance`, `right swing`, and `right double stance`.
>
> Progression through the state machine is achieved through a combination of user button presses via a wireless switch to initiate steps, and force sensitive resistors in the soles of the shoes to detect heel strike.
>
> During a step, the stance knee remains locked, while the swing leg joints unlock to facilitate motion.

#### 摘录 C
- 出处：第 4 页，Section `2.2.1. Gait Event Detection`，行 333-338
> In addition to the gait cycle, there are transition states into and out of gait, quiet standing and sitting. All state transitions are triggered by a set of transition criteria, based on hip and knee positions and velocities, as well as the force sensitive resistors at the heels. In addition, these states can be manually commanded with a wireless tactile button interface or a smartphone interface.

#### 摘录 D
- 出处：第 5-6 页，Human Testing / stimulation description，行 354-365
> At the conclusion of the timed pattern, final stimulation values are held until the next step is initiated.
>
> The stimulation consisted of biphasic, charge balanced pulse trains. Pulse widths were tuned for each muscle to elicit the maximum strength while tuning out unwanted movements, with a hardware safety limit of `250 µs`.
>
> Current amplitudes were set to a constant `20 mA` and stimulation inter-pulse intervals of `60` and `30 ms` were used depending on the muscle.

### 2. 基于原文整理后的自然语言描述

The MAHNP hybrid restoration system is organized as a hierarchical gait supervisor in which a timed stimulation program provides the base muscle drive and a GaitEventDetector finite-state machine layers electromechanical joint commands on top of it. At the gait-submachine level, the controller recognizes `left swing`, `left double stance`, `right swing`, and `right double stance`, and it advances one-way through these states from button-triggered step initiation and heel-strike detections from force-sensitive resistors in the shoes. When a step begins, the exoskeleton joints unlock, but during the step the stance knee remains locked while the swing-leg joints unlock to facilitate motion. Above the cyclic gait machine, the system also includes transition states into and out of gait, quiet standing, and sitting, driven by hip and knee positions, velocities, heel FSRs, and optional manual commands from a tactile button or smartphone interface. The sample is timed rather than purely untimed, because the baseline stimulation is an explicit time pattern with hold behavior, `250 µs` pulse-width safety limits, and `60/30 ms` inter-pulse intervals.

### 3. 逐句溯源

1. 句子 1：The MAHNP hybrid restoration system is organized as a hierarchical gait supervisor in which a timed stimulation program provides the base muscle drive and a GaitEventDetector finite-state machine layers electromechanical joint commands on top of it.
   对应摘录：A, B
2. 句子 2：At the gait-submachine level, the controller recognizes `left swing`, `left double stance`, `right swing`, and `right double stance`, and it advances one-way through these states from button-triggered step initiation and heel-strike detections from force-sensitive resistors in the shoes.
   对应摘录：B
3. 句子 3：When a step begins, the exoskeleton joints unlock, but during the step the stance knee remains locked while the swing-leg joints unlock to facilitate motion.
   对应摘录：B
4. 句子 4：Above the cyclic gait machine, the system also includes transition states into and out of gait, quiet standing, and sitting, driven by hip and knee positions, velocities, heel FSRs, and optional manual commands from a tactile button or smartphone interface.
   对应摘录：C
5. 句子 5：The sample is timed rather than purely untimed, because the baseline stimulation is an explicit time pattern with hold behavior, `250 µs` pulse-width safety limits, and `60/30 ms` inter-pulse intervals.
   对应摘录：A, D

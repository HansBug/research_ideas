# EMG-Based Shared Control Framework for Human-Robot Co-Manipulation Tasks - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `Low-Damping / High-Damping` 两个 operational modes 的切换条件、`1.5 s / 3 s` 触发时长和实验执行链都写得很清楚，是高质量的人机共操作 mode manager 样本。

## 条目 1: Low-/High-damping co-manipulation mode manager

- 控制对象：工业自动化与离散制造领域的人机共操作机械臂共享控制监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个通过 EMG 分类结果在 `Low-Damping` 与 `High-Damping` 两种协作模式之间切换的机械臂共享控制监督器。
- 判断：算。对象是实际 co-manipulation 控制器的高层 FSM，不是单纯 EMG 分类器；原文写出了状态名、模式对应的 admittance gains、最小时长 guard，以及重复执行路径跟踪任务时的完整切换过程。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract 与 Section `2`，`paper_content.txt` 第 12-17、141-155 行
> ... identify two classes of contractions that are fed into a finite state machine algorithm to trigger the activation of different sets of admittance control parameters corresponding to the envisaged operational modes.
>
> The proposed architecture includes two possible operational modes:
> • Low-Damping mode ...
> • High-Damping mode ...
> ... A finite state machine algorithm handles the switching between these sets based on the movements or contractions of the operator’s arm ...

#### 摘录 B

- 出处：第 5 页，Section `4.2 Finite State Machine`，`paper_content.txt` 第 445-463 行
> The two classes in output from the SVM classifier are fed into a finite state machine algorithm to automatically switch between the operational modes ...
>
> In detail, the system starts in Low-Damping mode; when the operator executes the contraction class for at least 1.5 s, the state switches to High-Damping mode ...
>
> By generating the contraction class for at least 3 s, the state returns to the Low-Damping mode ...

#### 摘录 C

- 出处：第 6-7 页，Section `5.3 Experimental Results`，`paper_content.txt` 第 622-648、677-683 行
> ... green and blue paths correspond to Low-Damping and High-Damping modes, respectively.
>
> ... the user ... generates the contraction class for 1.5 s to switch to High-Damping mode ... By generating contraction for at least 3 s, the user switches the FSM back to Low-Damping mode ...
>
> ... after the first 6 s (or after 83 s) ... she generates contraction for 1.5 s and the FSM switches to High-Damping mode ... then, the operator generates a 3 s contraction (after 72 or 146 s) and the FSM returns to Low-Damping mode.

### 2. 基于原文整理后的自然语言描述

The shared-control architecture is supervised by a two-state FSM that switches the manipulator between `Low-Damping` and `High-Damping` co-manipulation modes. The input to this supervisor is not raw force but the output of an EMG classifier that distinguishes `free` motion from `contraction`, and the state machine uses that classification to select one of two predefined admittance-gain sets. The controller starts in `Low-Damping`, where the operator can move the end-effector quickly and with low resistance in free space, and it transitions to `High-Damping` only when the `contraction` class is sustained for at least `1.5 s`. In `High-Damping`, the robot becomes slower and more precise for near-surface path following, and a sustained `3 s` contraction sends the FSM back to `Low-Damping` so the user can rapidly reposition the end-effector toward the start point. The experiments reproduce this timed switching several times while tracing a square-wave filament, so the paper provides both the timed guards and the task-level semantics of each mode.

### 3. 逐句溯源

1. 句子 1：The shared-control architecture is supervised by a two-state FSM that switches the manipulator between `Low-Damping` and `High-Damping` co-manipulation modes.
   对应摘录：A, B
2. 句子 2：The input to this supervisor is not raw force but the output of an EMG classifier that distinguishes `free` motion from `contraction`, and the state machine uses that classification to select one of two predefined admittance-gain sets.
   对应摘录：A, B
3. 句子 3：The controller starts in `Low-Damping`, where the operator can move the end-effector quickly and with low resistance in free space, and it transitions to `High-Damping` only when the `contraction` class is sustained for at least `1.5 s`.
   对应摘录：A, B
4. 句子 4：In `High-Damping`, the robot becomes slower and more precise for near-surface path following, and a sustained `3 s` contraction sends the FSM back to `Low-Damping` so the user can rapidly reposition the end-effector toward the start point.
   对应摘录：B, C
5. 句子 5：The experiments reproduce this timed switching several times while tracing a square-wave filament, so the paper provides both the timed guards and the task-level semantics of each mode.
   对应摘录：C

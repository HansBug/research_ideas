# Investigation of Timing to Switch Control Mode in Powered Knee Prostheses during Task Transitions - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出“高层 locomotion mode 选择 + 低层五态 gait-phase FSM”的双层控制结构，并把 mode switch timing 展开成跨两个 gait cycle 的 `10` 个触发点，是强度很高的分层 prosthesis 控制样本。

## 条目 1: Two-hierarchy gait-phase prosthesis mode-switch supervisor

- 控制对象：医疗设备与生命支持控制领域的主动膝假肢任务切换与步态相位分层控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个主动膝假肢的双层监督控制器，高层负责识别 locomotion task 并切换 control mode，低层用五态 gait-phase FSM 与 impedance control 调节膝关节阻抗，而模式切换时机在地形过渡前后两个 gait cycle 中被显式设计和评估。
- 判断：算。对象是真实 powered knee prosthesis 控制器，不是单纯实验评估流程；原文明确写出双层结构、五个低层状态、十个 mode switch timing、state/mode 对应阻抗参数和安全切换窗口。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，`Methods / Design and Control of a Powered Knee Prosthesis`，`paper_content.txt` 第 98-107 行
> The control structure of the powered prosthesis contained two hierarchies as demonstrated in Fig 1. The function of the high-level controller was to recognize the prosthesis user’s intended tasks and determine the control mode in the low-level intrinsic controller accordingly. In the low-level controller, a finite-state machine (FSM) and impedance control were designed to modulate the knee joint impedances based on the user’s task (output of high-level control) and current state (gait phase). Five states were defined, each of which corresponded to one of the five defined gait phases: initial double support (IDS), single support (SS), terminal double support (TDS), swing flexion (SWF), and swing extension (SWE). The ground reaction force, measured by the load cell, and knee kinematics (i.e. knee angle and angular velocity) were used to trigger the state transitions.

#### 摘录 B

- 出处：第 4 页，`Investigated Task Transitions and Mode Switch Timing`，`paper_content.txt` 第 124-129 行
> To investigate the effects of control mode switch timing during task transitions, the time duration between one full gait cycle before and after the prosthetic foot stepped on the upcoming terrain was studied.
>
> The locomotion mode simulator triggered the prosthesis control mode change at the beginning of a randomly selected gait phase within these two gait cycles. As a result, 10 transition timings (i.e. IDS_1, SS_1, TDS_1, SWF_1, SWE_1, IDS_2, SS_2, TDS_2, SWF_2, and SWE_2) were investigated.

#### 摘录 C

- 出处：第 5 页，`Experimental Protocol`，`paper_content.txt` 第 152-157 行
> In the training procedure, the intrinsic controller impedance parameters for each control mode and each state (gait phase) were obtained for each individual subject.
>
> The prosthesis control mode was switched by the locomotion mode simulator at a randomly selected timing during the transition period.

#### 摘录 D

- 出处：第 7 页，`Results`，`paper_content.txt` 第 215-224、230-232 行
> Fig 4 showed the effects of mode switch timing on the subjects’ gait stability in task transitions.
>
> Clearly, for each individual type of task transition there was a time window (about 3–4 gait phases) within which switching the control mode permitted smooth and safe task transitions in all the test subjects.
>
> For AB subjects, the time windows that were observed to allow safe and smooth transitions between tasks included TDS_1, SWF_1, SWE_1, and IDS_2.

### 2. 基于原文整理后的自然语言描述

The powered knee prosthesis uses a hierarchical controller in which the high-level layer selects the locomotion task mode while the low-level intrinsic controller executes a five-state gait-phase FSM with impedance control. The lower layer explicitly contains the gait states `IDS`, `SS`, `TDS`, `SWF`, and `SWE`, and their transitions are triggered by load-cell ground-reaction force together with knee angle and angular velocity. Mode switching is not treated as an informal operator choice: the paper defines a two-gait-cycle transition interval around terrain change and places the control-mode switch at one of ten explicit timing points from `IDS_1` through `SWE_2`. The mode/state combination is operational rather than decorative, because impedance parameters are specified for each control mode and each gait-phase state before the experiments are run. Results then show that smooth task transitions require switching within a safe timing window of about `3–4` gait phases, with stable examples including `TDS_1`, `SWF_1`, `SWE_1`, and `IDS_2`, so local switch timing is part of the controller semantics rather than an external evaluation detail.

### 3. 逐句溯源

1. 句子 1：The powered knee prosthesis uses a hierarchical controller in which the high-level layer selects the locomotion task mode while the low-level intrinsic controller executes a five-state gait-phase FSM with impedance control.
   对应摘录：A
2. 句子 2：The lower layer explicitly contains the gait states `IDS`, `SS`, `TDS`, `SWF`, and `SWE`, and their transitions are triggered by load-cell ground-reaction force together with knee angle and angular velocity.
   对应摘录：A
3. 句子 3：Mode switching is not treated as an informal operator choice: the paper defines a two-gait-cycle transition interval around terrain change and places the control-mode switch at one of ten explicit timing points from `IDS_1` through `SWE_2`.
   对应摘录：B
4. 句子 4：The mode/state combination is operational rather than decorative, because impedance parameters are specified for each control mode and each gait-phase state before the experiments are run.
   对应摘录：C
5. 句子 5：Results then show that smooth task transitions require switching within a safe timing window of about `3–4` gait phases, with stable examples including `TDS_1`, `SWF_1`, `SWE_1`, and `IDS_2`, so local switch timing is part of the controller semantics rather than an external evaluation detail.
   对应摘录：D

# A Pediatric Knee Exoskeleton With Real-Time Adaptive Control for Overground Walking in Ambulatory Individuals With Cerebral Palsy - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `P.REX` 膝外骨骼的多粒度 gait-phase `FSM`、`FSR` 与速度阈值转移、`Constant / Zero / Adaptive` 模式和相位定向扭矩输出，可直接作为高质量步态监督控制样本。

## 条目 1: Gait-phase supervisory controller for the P.REX pediatric knee exoskeleton
- 控制对象：`P.REX` 儿童膝关节外骨骼的高层 gait-phase 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个利用 `FSR` 足底接触与膝关节编码器信号将步态切分为 `2/3/4/5` 个离散相位，并在不同相位下切换恒定扭矩、阻抗辅助或自适应扭矩的儿童膝外骨骼监督控制器。
- 判断：算。对象是真实外骨骼控制器，不是临床流程；原文明确给出状态划分、转移阈值、模式输出和相位级辅助策略，能够恢复完整的步态控制主链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `Control`
> The highest or supervisory level consists of the finite state machine (FSM) ... The FSM is flexible in that it can split the gait cycle in four different ways: 1) 2 states: stance/swing ... 4) 5 states: early stance/mid-stance/late stance/early swing/late swing.

#### 摘录 B
- 出处：第 4 页，Section `Control`
> Within each state, the controller can activate three different operational modes ... Constant mode ... Zero mode ... The third mode is an adaptive control mode which provides assistive or resistive torque proportional to the estimated internal knee moment ... The adaptive mode was only utilized with a 2-state FSM ... only active during stance phase.

#### 摘录 C
- 出处：第 8-9 页，Section `Exoskeleton Validation in Participant With Typical Development`
> assistive torque was maintained at the target level during stance and late swing in the 3-state condition ... in the 5-state mode assistive torques were confined to mid-stance and late swing phases during which the knee was extending.

#### 摘录 D
- 出处：第 9 页，Section `Exoskeleton Validation in Participant With Typical Development`
> A FSR threshold was used to separate stance phase of gait cycle from swing phase ... A negative velocity threshold was used to identify the transition from early stance to middle stance and from early swing to late swing. A positive velocity threshold was used to identify the transition from mid-stance to late stance. All the transitions proceeded according to design.

### 2. 基于原文整理后的自然语言描述

The `P.REX` pediatric knee exoskeleton uses a supervisory FSM that parses the gait cycle into discrete phases, with the richest configuration dividing walking into `early stance`, `mid-stance`, `late stance`, `early swing`, and `late swing`. Inside each phase, the controller can switch among `Constant`, `Zero`, and `Adaptive` assistance modes, so the same state partition can either apply fixed extension torque, cancel drivetrain friction, or generate torque proportional to the estimated biological knee moment. In the reported constant-assistance configurations, the `3-state` machine keeps assistance on during `stance` and `late swing`, while the `5-state` machine confines extension assistance to `mid-stance` and `late swing` where knee extension is most useful. Phase transitions are guarded by measured variables rather than a simple fixed schedule: an `FSR` threshold separates `stance` from `swing`, a negative knee-velocity threshold triggers `early stance -> mid-stance` and `early swing -> late swing`, and a positive velocity threshold triggers `mid-stance -> late stance`. The paper reports that these threshold-based transitions and phase-specific torque outputs all behaved according to design during overground walking tests.

### 3. 逐句溯源

1. 句子 1：The `P.REX` pediatric knee exoskeleton uses a supervisory FSM that parses the gait cycle into discrete phases, with the richest configuration dividing walking into `early stance`, `mid-stance`, `late stance`, `early swing`, and `late swing`.
   对应摘录：A
2. 句子 2：Inside each phase, the controller can switch among `Constant`, `Zero`, and `Adaptive` assistance modes, so the same state partition can either apply fixed extension torque, cancel drivetrain friction, or generate torque proportional to the estimated biological knee moment.
   对应摘录：B
3. 句子 3：In the reported constant-assistance configurations, the `3-state` machine keeps assistance on during `stance` and `late swing`, while the `5-state` machine confines extension assistance to `mid-stance` and `late swing` where knee extension is most useful.
   对应摘录：C
4. 句子 4：Phase transitions are guarded by measured variables rather than a simple fixed schedule: an `FSR` threshold separates `stance` from `swing`, a negative knee-velocity threshold triggers `early stance -> mid-stance` and `early swing -> late swing`, and a positive velocity threshold triggers `mid-stance -> late stance`.
   对应摘录：D
5. 句子 5：The paper reports that these threshold-based transitions and phase-specific torque outputs all behaved according to design during overground walking tests.
   对应摘录：C, D

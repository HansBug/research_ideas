# A Functional Electrical Stimulation System for Human Walking Inspired by Reflexive Control Principles - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 gait-phase detector、事件脉冲生成和上层/下层 FES controller 串成了完整的分层控制架构，细到每个相位、触发条件和肌群开关规则。

## 条目 1: Hierarchical gait-phase FES supervisor inspired by reflexive control
- 控制对象：多通道步行辅助 FES 系统的 gait-phase 检测与肌群刺激监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 FES gait-assist controller，用 `FSR + hip angle` 信号驱动五相步态状态机，再通过上层肌群开关和下层传递函数生成分肌群刺激序列。
- 判断：算。对象是真实步行辅助控制系统，原文明确给出了 gait states、事件脉冲、状态触发规则和层次化 stimulation outputs。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section `Gait phase detection`
> One gait cycle is divided into five gait phases, namely, the loading response, stance, pre-swing, swing and terminal swing. An IF-THEN type finite state machine is employed in this system ... the sensor signals to the finite state machine include FSR signals ... and the hip angle in the sagittal plane.

#### 摘录 B
- 出处：第 4 页，Section `Event impulses are generated during transitions between states`
> Four types of impulses are required for the FES control, IHS, IHO, ISW and ITSW ... IHS ... if any part of foot touches the ground after the swing phase ... IHO ... heel is not pressed and the forefoot is still in contact ... ISW ... the foot is lifted entirely off the ground ... ITSW ... transition from the swing phase to terminal swing phase when the hip flexes forward and the measured fH reaches its threshold.

#### 摘录 C
- 出处：第 4 页，Section `Stimulation strategy`
> A hierarchical controller was created ... The top level implements an FSC model where the state function S switches on and off electrical stimulations of muscles ... STA = 1 state = swing = terminal swing ... SLG,HS = 1 state = loading response ... SRF,TSW = 1 state = terminal swing ... The stimulation amplitude is adjusted by convolving an event impulse with a transfer function H in the lower level part of controller.

### 2. 基于原文整理后的自然语言描述

The FES walking-assistance controller detects five gait phases, `loading response`, `stance`, `pre-swing`, `swing`, and `terminal swing`, using heel contact, forefoot contact, and sagittal hip-angle signals rather than a fixed periodic schedule. Phase transitions generate explicit event impulses such as `IHS`, `IHO`, `ISW`, and `ITSW`, so the controller can distinguish initial contact, heel-off, complete foot lift-off, and forward hip-flexion entry into terminal swing. On top of this detector, the system implements a hierarchical controller in which the upper finite-state control layer decides which muscles should be active in each gait phase, while the lower layer shapes the stimulation amplitude through transfer functions driven by those event impulses. In the published rules, tibialis anterior and biceps femoris are activated through swing and terminal swing, lateral gastrocnemius is turned on in loading response and again around pre-swing, and rectus femoris is enabled in loading response and terminal swing. The resulting control chain is therefore a state-driven multi-muscle stimulation supervisor that couples discrete gait events to phase-specific FES output patterns.

### 3. 逐句溯源

1. 句子 1：The FES walking-assistance controller detects five gait phases, `loading response`, `stance`, `pre-swing`, `swing`, and `terminal swing`, using heel contact, forefoot contact, and sagittal hip-angle signals rather than a fixed periodic schedule.
   对应摘录：A
2. 句子 2：Phase transitions generate explicit event impulses such as `IHS`, `IHO`, `ISW`, and `ITSW`, so the controller can distinguish initial contact, heel-off, complete foot lift-off, and forward hip-flexion entry into terminal swing.
   对应摘录：B
3. 句子 3：On top of this detector, the system implements a hierarchical controller in which the upper finite-state control layer decides which muscles should be active in each gait phase, while the lower layer shapes the stimulation amplitude through transfer functions driven by those event impulses.
   对应摘录：C
4. 句子 4：In the published rules, tibialis anterior and biceps femoris are activated through swing and terminal swing, lateral gastrocnemius is turned on in loading response and again around pre-swing, and rectus femoris is enabled in loading response and terminal swing.
   对应摘录：C
5. 句子 5：The resulting control chain is therefore a state-driven multi-muscle stimulation supervisor that couples discrete gait events to phase-specific FES output patterns.
   对应摘录：A, B, C

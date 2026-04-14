# Assessment of an Assistive Control Approach Applied in an Active Knee Orthosis Plus Walker for Post-Stroke Gait Rehabilitation - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `HMIR -> FSM -> admittance/PI` 三层控制架构、`SU/SD/F/E/W/RSU/RSD` motion classes，以及 stance/swing 子阶段阻抗调节都写得很完整，可直接作为康复正交辅助控制样本入账。

## 条目 1: Hierarchical gait-assistance supervisor for the ALLOR knee orthosis
- 控制对象：`ALLOR` 主动膝关节矫形器加助行器的步态康复监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向卒中后步态训练的主动膝关节矫形器控制器，用 trunk `sEMG` 识别动作意图，再由中层 `FSM` 选择 gait class 和 stance-control 逻辑。
- 判断：算。对象是真实康复矫形器控制系统，不是实验流程；原文明确给出控制层级、离散 motion classes、允许的动作序列、gait sub-phases 以及各阶段的阻抗调节目标。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5-6 页，Section `2.1` / Table `1`
> The ALLOR’s control system is based on a hierarchical structure made up of a high-level Human Movement Intention Recognition (HMIR) system ... the controller includes, at the middle level, a Finite State Machine (FSM), which establishes the control strategy corresponding to the suitable gait movement. Finally, the admittance controller, speed controller, and Proportional Integral (PI) controller take care of performing the desired low-level motion ...
>
> The FSM is in charge of leading with the following motion classes: (1) Stand-Up (SU); (2) Sit-Down (SD); (3) Knee Flexion-Extension (F/E); (4) Walking (W); (5) Rest in Stand-Up Position (RSU); (6) Rest in Sit-Down Position (RSD). Then, for gait movements, the FSM is used to carry out the following transition sequence: RSU-SD-SU-W-RSU-SD-F/E-SU.

#### 摘录 B
- 出处：第 6 页，Section `2.2. Controller`
> The stance control strategy proposed here consists of the following features: (1) suitable free knee motion in the swing phase to allow free joint rotation in flexion and extension; (2) suitable lock of the knee joint to resist knee flexion while allowing free knee extension.
>
> Here, a modulation through variable gain is used to increase or decrease the impedance components (damping and inertia), according to the gait sub-phases, in order to adapt the knee joint impedance during walking ... The objective of this modulation is to allow the precise adjustment of knee impedance during gait cycle to obtain a smooth and quick switching between gait phases ...
>
> An algorithm is also used to recognize the other gait sub-phases: initial contact (defined by the heel contact); mid stance (defined by a flat foot contact); terminal stance (defined by the heel off); and swing (defined by the foot off based on ground reaction forces during gait) ...

#### 摘录 C
- 出处：第 1 页，Abstract
> Signals from plantar pressure, gait phase, and knee angle and torque were acquired during gait, which allowed us to verify that the stance control strategy proposed here was efficient at improving the patients’ gaits ... without the necessity of imposing a fixed knee trajectory.

### 2. 基于原文整理后的自然语言描述

The ALLOR rehabilitation orthosis uses a three-layer hierarchical controller in which a trunk-sEMG Human Movement Intention Recognition module feeds a middle-layer FSM and the selected motion class is executed by admittance, speed, and PI controllers. The FSM manages six motion classes, `SU`, `SD`, `F/E`, `W`, `RSU`, and `RSD`, and constrains their evolution through the sequence `RSU-SD-SU-W-RSU-SD-F/E-SU` rather than allowing arbitrary jumps between behaviors. During walking, the controller applies a stance-control policy that locks the knee against flexion collapse while still permitting free extension in stance and releases the joint in swing for free flexion and extension. The low-level impedance is modulated by a variable gain over footswitch-derived subphases `initial contact`, `mid stance`, `terminal stance`, and `swing`, so damping and inertia change with gait context instead of following a fixed position trajectory. This makes the orthosis a mode-structured gait supervisor driven by detected user intention, plantar pressure, gait phase, knee angle, and knee torque.

### 3. 逐句溯源

1. 句子 1：The ALLOR rehabilitation orthosis uses a three-layer hierarchical controller in which a trunk-sEMG Human Movement Intention Recognition module feeds a middle-layer FSM and the selected motion class is executed by admittance, speed, and PI controllers.
   对应摘录：A
2. 句子 2：The FSM manages six motion classes, `SU`, `SD`, `F/E`, `W`, `RSU`, and `RSD`, and constrains their evolution through the sequence `RSU-SD-SU-W-RSU-SD-F/E-SU` rather than allowing arbitrary jumps between behaviors.
   对应摘录：A
3. 句子 3：During walking, the controller applies a stance-control policy that locks the knee against flexion collapse while still permitting free extension in stance and releases the joint in swing for free flexion and extension.
   对应摘录：B
4. 句子 4：The low-level impedance is modulated by a variable gain over footswitch-derived subphases `initial contact`, `mid stance`, `terminal stance`, and `swing`, so damping and inertia change with gait context instead of following a fixed position trajectory.
   对应摘录：B, C
5. 句子 5：This makes the orthosis a mode-structured gait supervisor driven by detected user intention, plantar pressure, gait phase, knee angle, and knee torque.
   对应摘录：A, B, C

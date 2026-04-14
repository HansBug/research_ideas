# Preliminary Evaluations of a Self-Contained Anthropomorphic Transfemoral Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自供能膝踝假肢的 `intent recognizer -> activity-mode controller -> joint torque controller` 三层结构和 walking/standing 子状态机写得很清楚，可直接作为层次化 prosthesis supervisor 样本。

## 条目 1: Hierarchical walking-standing supervisor for the self-contained anthropomorphic transfemoral prosthesis
- 控制对象：自供能膝踝一体主动股骨假肢的高层活动模式与相位监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个主动股骨假肢的分层监督器，最上层识别用户活动意图，中层为 walking/standing 等 activity mode 选择有限状态机，底层再执行相位相关的 knee/ankle torque tracking。
- 判断：算。对象是真实膝踝假肢控制系统，原文明确给出三层控制结构、walking/standing 状态机以及状态相关阻抗输出。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，Section `II. Control`
> The general control architecture of the prosthesis consists of three levels ... The high-level supervisory controller, which is the intent recognizer, infers the user’s intent ... and switches the middle-level controllers appropriately ... A middle-level controller is developed for each activity mode, such as walking, standing, sitting, and stair ascent/descent. The middle-level controllers generate torque references for the joints using a finite-state machine ... The low-level controllers are the closed-loop joint torque controllers.

#### 摘录 B
- 出处：第 5-6 页，Section `II. Control`
> The joint torques for each activity mode ... are governed by separate finite-state machines ... The finite-state machines for walking and standing are diagrammed in Fig. 9 and Fig. 10, respectively. The state model for walking is described by five phases, three of which are stance phases (early stance, middle stance, and late stance) and two of which are swing phases (swing knee flexion and swing knee extension). The standing state model is described by two phases, which are a weight-bearing phase and a nonweight-bearing phase.

#### 摘录 C
- 出处：第 6 页，Section `II. Control`
> In each phase, the knee and ankle torques ... are each described by a passive spring and damper with a fixed equilibrium point ... Energy is delivered to the user by switching between appropriate equilibrium points ... the prosthesis is guaranteed to be passive within each phase, and thus, generates power simply by switching between phases.

### 2. 基于原文整理后的自然语言描述

The self-contained anthropomorphic transfemoral prosthesis uses a three-level controller in which a high-level intent recognizer first selects the current activity mode, a middle layer then runs a mode-specific finite-state machine, and low-level joint controllers track the resulting knee and ankle torque references. For locomotion, the walking controller decomposes gait into five phases: `early stance`, `middle stance`, `late stance`, `swing knee flexion`, and `swing knee extension`, while the standing controller uses a separate two-state machine with `weight-bearing` and `nonweight-bearing` phases. This gives the prosthesis a hierarchical supervisory structure rather than a single flat gait automaton, because activity selection and phase progression are separated across controller levels. Inside each phase, the knee and ankle are governed by passive spring-damper impedances with fixed equilibrium points, and the device produces useful positive work by switching those equilibrium points between phases instead of by enforcing a stiff position trajectory. The resulting controller therefore combines activity-mode routing, gait-phase switching, and state-specific impedance output into one traceable powered-prosthesis control chain.

### 3. 逐句溯源

1. 句子 1：The self-contained anthropomorphic transfemoral prosthesis uses a three-level controller in which a high-level intent recognizer first selects the current activity mode, a middle layer then runs a mode-specific finite-state machine, and low-level joint controllers track the resulting knee and ankle torque references.
   对应摘录：A
2. 句子 2：For locomotion, the walking controller decomposes gait into five phases: `early stance`, `middle stance`, `late stance`, `swing knee flexion`, and `swing knee extension`, while the standing controller uses a separate two-state machine with `weight-bearing` and `nonweight-bearing` phases.
   对应摘录：B
3. 句子 3：This gives the prosthesis a hierarchical supervisory structure rather than a single flat gait automaton, because activity selection and phase progression are separated across controller levels.
   对应摘录：A, B
4. 句子 4：Inside each phase, the knee and ankle are governed by passive spring-damper impedances with fixed equilibrium points, and the device produces useful positive work by switching those equilibrium points between phases instead of by enforcing a stiff position trajectory.
   对应摘录：C
5. 句子 5：The resulting controller therefore combines activity-mode routing, gait-phase switching, and state-specific impedance output into one traceable powered-prosthesis control chain.
   对应摘录：A, B, C

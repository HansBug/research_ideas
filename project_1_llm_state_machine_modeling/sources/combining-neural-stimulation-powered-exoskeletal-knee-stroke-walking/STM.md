# Combining neural stimulation and a powered exoskeletal knee to enhance walking after stroke - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把卒中步行辅助混合外骨骼明确定义为四相位 `FSM`，并把 `IMU + FSR` 相位检测、相位内电机弹簧/阻尼参数和神经刺激通道绑定到同一监督链上，可直接形成双 A 正例。

## 条目 1: Four-phase hybrid gait-assistance supervisor for post-stroke exoskeletal knee

- 控制对象：卒中步行辅助混合外骨骼四相位控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（步态相位外骨骼）

### 0. 条目识别与判定

- 一句话说明：这是一个面向卒中患者步行辅助的混合外骨骼监督控制器，用四个 gait phase 状态统一调度 `IMU/FSR` 触发、膝关节电机助力和神经刺激输出。
- 判断：算。对象是真实下肢外骨骼控制器，不是临床流程或单纯效果评估；原文直接给出四相位 `FSM`、状态转换信号和各相位的 motor/stimulation actions。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6 页，Section `Controller`，`paper_content.txt` 第 252-260 行
> For proof of concept, the exoskeleton was controlled by a feedforward finite state machine (FSM) divided into four states based on the gait cycle: early swing, late swing, early stance, and push off ... State transitions were determined from the thigh and shank orientations and velocities as measured from the IMUs, as well as initial contact and foot off events from the FSRs. NS was applied to muscles known to elicit desired motions in each given state.

#### 摘录 B

- 出处：第 7 页，Section `Controller`，`paper_content.txt` 第 264-273 行
> Spring stiffness during each state was scaled by an estimated percent assistance needed ... A derivative term was also added to provide damping for the joint. ... Each state included a torque-limiter that constrained the jerk ... The torque rate thresholds were determined by identifying maximum jerk values found in neurotypical data for each phase of gait.

#### 摘录 C

- 出处：第 8 页，Section `Participant`，`paper_content.txt` 第 286-289 行
> Stimulation was applied to tibialis anterior for dorsiflexion during swing, gastrocnemius for plantar flexion for push off into the swing phase, and quadriceps for knee extension to prepare the leg for weight acceptance at initial contact.

### 2. 基于原文整理后的自然语言描述

The hybrid post-stroke exoskeleton uses a feedforward finite-state machine with four gait states: `early swing`, `late swing`, `early stance`, and `push off`. State transitions are derived from thigh and shank orientations and angular velocities measured by IMUs, together with initial-contact and foot-off events from FSRs, so the phase logic reacts directly to the user’s gait rather than following a fixed timer. Within each state, the knee motor is parameterized as a phase-specific torsional spring with state-dependent stiffness and damping, and every state also includes a torque limiter that bounds jerk for smoother assistance. Neural stimulation is coordinated with the same phase machine, activating tibialis anterior during swing, gastrocnemius during push-off, and quadriceps to prepare knee extension for weight acceptance. The controller is therefore an extended gait-phase supervisor whose discrete states select both stimulation channels and motor-assistance laws.

### 3. 逐句溯源

1. 句子 1：The hybrid post-stroke exoskeleton uses a feedforward finite-state machine with four gait states: `early swing`, `late swing`, `early stance`, and `push off`.
   对应摘录：A
2. 句子 2：State transitions are derived from thigh and shank orientations and angular velocities measured by IMUs, together with initial-contact and foot-off events from FSRs, so the phase logic reacts directly to the user’s gait rather than following a fixed timer.
   对应摘录：A
3. 句子 3：Within each state, the knee motor is parameterized as a phase-specific torsional spring with state-dependent stiffness and damping, and every state also includes a torque limiter that bounds jerk for smoother assistance.
   对应摘录：B
4. 句子 4：Neural stimulation is coordinated with the same phase machine, activating tibialis anterior during swing, gastrocnemius during push-off, and quadriceps to prepare knee extension for weight acceptance.
   对应摘录：A, C
5. 句子 5：The controller is therefore an extended gait-phase supervisor whose discrete states select both stimulation channels and motor-assistance laws.
   对应摘录：A, B, C

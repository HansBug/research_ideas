# Design and Control of a Powered Transfemoral Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文清楚给出了动力股骨假肢的四模态 gait controller、状态切换传感条件和各模态的 knee/ankle impedance 角色，是 powered prosthesis 主链的强样本。

## 条目 1: Four-mode gait controller for the powered transfemoral prosthesis
- 控制对象：动力股骨假肢膝踝一体 gait-phase 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个主动膝踝股骨假肢的四态 gait-mode controller，用不同的 impedance segment 和传感器触发条件来协调 load acceptance、push-off、swing flexion 与 swing extension。
- 判断：算。对象是真实 powered prosthesis controller，原文明确写出模态划分、转换守卫和状态相关的 joint behavior。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6-7 页，Section `3.2 Gait Modes`
> The decomposition of joint behavior into passive segments requires the division of the gait cycle into modes or “finite states” ... such fits were improved significantly by further dividing swing and stance into two sub-modes ... Mode 1 begins with a heel strike ... Mode 2 is the push-off phase and begins as the ankle dorsiflexes beyond a given angle ... Mode 3 begins as the foot leaves the ground as indicated by the ankle torque load cell ... Mode 4 is active during the extension of the knee joint ... and ends at heel strike as determined by the three-axis socket load cell.

#### 摘录 B
- 出处：第 6 页，Section `3.2 Gait Modes`
> Both knee and ankle joints have relatively high stiffness during this mode to prevent buckling ... The knee stiffness decreases in this mode to allow knee flexion while the ankle provides a plantarflexive torque for push-off ... In both of the swing modes, the ankle torque is small and is represented in the controller as a relatively weak spring regulated to a neutral position. The knee is primarily treated as a damper in both swing modes.

#### 摘录 C
- 出处：第 19-20 页，Fig. 9 and Fig. 10 captions
> A finite-state model of normal gait. Each box represents a state and the transition conditions between states are specified ... Piecewise fitting of knee and ankle torques ... to a non-linear spring-damper impedance model ... the gait stride [is segmented] into four distinct modes.

### 2. 基于原文整理后的自然语言描述

The powered transfemoral prosthesis controller represents level walking as a four-mode finite-state machine rather than a single continuous trajectory tracker. `Mode 1` starts at heel strike and provides high knee and ankle stiffness for impact absorption, loading, and flat-foot attainment; `Mode 2` begins when ankle dorsiflexion passes a guard angle and shifts the prosthesis into push-off with reduced knee stiffness and plantarflexive ankle torque. `Mode 3` starts when the foot leaves the ground according to the ankle torque load cell and governs swing knee flexion, while `Mode 4` starts when knee velocity becomes negative and carries the leg through swing extension until the next heel strike detected by the three-axis socket load cell. Across all four modes, the knee and ankle torques are produced by piecewise spring-damper impedance functions, so the same state machine simultaneously determines both the active gait phase and the corresponding impedance regime for each joint. The result is a sensor-driven powered-prosthesis supervisor in which gait progression is encoded by measurable guards and state-specific joint behavior rather than by replaying a fixed reference trajectory.

### 3. 逐句溯源

1. 句子 1：The powered transfemoral prosthesis controller represents level walking as a four-mode finite-state machine rather than a single continuous trajectory tracker.
   对应摘录：A, C
2. 句子 2：`Mode 1` starts at heel strike and provides high knee and ankle stiffness for impact absorption, loading, and flat-foot attainment; `Mode 2` begins when ankle dorsiflexion passes a guard angle and shifts the prosthesis into push-off with reduced knee stiffness and plantarflexive ankle torque.
   对应摘录：A, B
3. 句子 3：`Mode 3` starts when the foot leaves the ground according to the ankle torque load cell and governs swing knee flexion, while `Mode 4` starts when knee velocity becomes negative and carries the leg through swing extension until the next heel strike detected by the three-axis socket load cell.
   对应摘录：A
4. 句子 4：Across all four modes, the knee and ankle torques are produced by piecewise spring-damper impedance functions, so the same state machine simultaneously determines both the active gait phase and the corresponding impedance regime for each joint.
   对应摘录：B, C
5. 句子 5：The result is a sensor-driven powered-prosthesis supervisor in which gait progression is encoded by measurable guards and state-specific joint behavior rather than by replaying a fixed reference trajectory.
   对应摘录：A, B, C

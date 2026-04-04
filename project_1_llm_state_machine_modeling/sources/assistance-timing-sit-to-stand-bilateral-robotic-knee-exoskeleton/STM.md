# Effect of Assistance Timing in Knee Extensor Muscle Activation During Sit-to-Stand Using a Bilateral Robotic Knee Exoskeleton - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 bilateral robotic knee exoskeleton 的 `sit / sit-to-stand / stand / stand-to-sit` 四态 FSM、`FSR + knee angle` 守卫、`800 ms` assistance 窗口与 `10/25/40/55%` phase-timed torque schedule，可直接作为 `FSM + T1` 双 A 样本。

## 条目 1: Four-state sit-to-stand assistance controller for the bilateral robotic knee exoskeleton
- 控制对象：bilateral robotic knee exoskeleton 的 sit-to-stand assistance controller
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 bilateral robotic knee exoskeleton 的 sit-to-stand controller，它用 heel `FSR` 和 knee-angle threshold 识别四个姿态状态，并在 `sit-to-stand` 段施加显式时长和相位峰值可配置的 torque assistance。
- 判断：算。对象是真实膝外骨骼控制器，不是单纯实验协议；原文明确给出了四个离散状态、进入 guard、`800 ms` assistance 时间窗以及 phase-based torque schedule。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，Section `II. Methods`
> We developed a heuristic-based controller using a finite state machine (`FSM`) to determine the state of the user's movement in real-time ... The `FSM` divides the user's movement into four main states: `sit`, `sit-to-stand`, `stand`, and `stand-to-sit`.

#### 摘录 B
- 出处：第 3 页，Section `II. Methods`
> During this state, a force-sensitive resistor (`FSR`) attached at the user's heel is unloaded, and the knee angle is above the threshold sit angle ... As the subject initiates an instant seat-off ... the `FSR` becomes loaded and the knee angle goes below the threshold sit angle which initiates the `sit-to-stand state`.

#### 摘录 C
- 出处：第 3 页，Section `II. Methods`
> The duration after detecting the start of the phase is `800 ms` for the assistance ... During this state, the controller assists at the knee joints from `0%` to `65%` of the sit-to-stand movement. Assistance torque linearly increases ... to the specified peak timing (`10%`, `25%`, `40%`, and `55%`) ... and linearly decreases back to `0 Nm` until `65%` of the sit-to-stand movement.

#### 摘录 D
- 出处：第 4 页，Section `III. Analysis`
> The initiation of the sit-to-stand was defined as the knee angle passes the threshold sit angle, `95°`, and the completion was defined as the knee angle converges to the standing angle for each subject.

#### 摘录 E
- 出处：第 4 页，Section `III. Results`
> The assistance with a peak torque timed at `25%` of the sit-to-stand phase was the most effective assistance condition ... Among the four assistance conditions, two conditions with each peak occurring at `25%` and `40%` significantly reduced the muscle activation relative to the no assistance condition.

### 2. 基于原文整理后的自然语言描述

The bilateral robotic knee exoskeleton uses a heuristic four-state controller with `sit`, `sit-to-stand`, `stand`, and `stand-to-sit` as its discrete movement states. Entry into `sit-to-stand` is detected when the heel-mounted `FSR` becomes loaded and the knee angle falls below the threshold sit angle, while the stable `sit` state requires an unloaded heel and a knee angle above that same boundary. After the phase start is detected, the assistance window lasts `800 ms`, and within that window the knee torque is scheduled as a triangular profile from `0%` to `65%` of the sit-to-stand movement with alternative peak timings at `10%`, `25%`, `40%`, or `55%`. Phase normalization is tied to explicit kinematic thresholds as well, because the analysis defines sit-to-stand initiation at a knee angle of `95°` and completion when the knee converges to the standing angle. The controller therefore combines state recognition from contact and joint-angle guards with an explicit assistance duration and phase-timed torque profile, which makes it a direct `FSM + T1` sit-to-stand assistance sample.

### 3. 逐句溯源

1. 句子 1：The bilateral robotic knee exoskeleton uses a heuristic four-state controller with `sit`, `sit-to-stand`, `stand`, and `stand-to-sit` as its discrete movement states.
   对应摘录：A
2. 句子 2：Entry into `sit-to-stand` is detected when the heel-mounted `FSR` becomes loaded and the knee angle falls below the threshold sit angle, while the stable `sit` state requires an unloaded heel and a knee angle above that same boundary.
   对应摘录：B
3. 句子 3：After the phase start is detected, the assistance window lasts `800 ms`, and within that window the knee torque is scheduled as a triangular profile from `0%` to `65%` of the sit-to-stand movement with alternative peak timings at `10%`, `25%`, `40%`, or `55%`.
   对应摘录：C
4. 句子 4：Phase normalization is tied to explicit kinematic thresholds as well, because the analysis defines sit-to-stand initiation at a knee angle of `95°` and completion when the knee converges to the standing angle.
   对应摘录：D
5. 句子 5：The controller therefore combines state recognition from contact and joint-angle guards with an explicit assistance duration and phase-timed torque profile, which makes it a direct `FSM + T1` sit-to-stand assistance sample.
   对应摘录：A, B, C, D, E

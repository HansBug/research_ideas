# Whole Body Awareness for Controlling a Robotic Transfemoral Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `WBAC` 的双层意图识别架构、`8` 个 maneuvre 状态、walking/stair 子相位与带 timeout 的安全回退环，可直接作为高质量主动股骨假肢监督控制样本。

## 条目 1: Double-layer intention-aware supervisor for the CYBERLEGs transfemoral prosthesis
- 控制对象：`CYBERLEGs` 主动股骨假肢的 `WBAC` 全身感知监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用可穿戴 `IMU + instrumented shoes` 做意图识别的双层主动股骨假肢控制器，用高层状态机识别 maneuver 与 subphase，再驱动膝踝执行机构和 `WA/ET` 机制。
- 判断：算。对象是真实主动股骨假肢控制器，不是离线识别流程；原文明确给出状态集合、子相位、阈值规则、低层动作和 timeout 安全逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `The controller`
> The signals acquired through the WSA are fed to a finite-state machine implementing subject-independent real-time intention detection and consequently driving the actuators.
>
> The controller distinguishes up to eight different maneuvres, among which four are steady state activities, while the other ones are transient actions. In particular, the controller recognizes (i) quiet standing, (ii) quiet sitting, (iii) step-by-step stair ascent, and (iv) walking, as steady state maneuvres, while the actions of (v) sitting down, (vi) standing up, (vii) initiating, and (viii) terminating locomotion are detected as transient states.
>
> Within each steady activity, the controller further recognizes the occurrence of subsequent subphases ... walking and stair ascent can only be entered upon recognition of specific subphases ...

#### 摘录 B
- 出处：第 4-5 页，Section `The controller` / Table `1`
> For either the detection of a new phase or activity, the transition rules consist of combinations of heuristic rules evaluating the exceedance of pre-set thresholds ...
>
> additional rules guarantee safety in case of missed transitions’ detections by timing out the current phase and triggering the next one or setting the prosthesis in the extended stiff configuration ...
>
> Walking ... DS-PTS ... SS-S ... DS-STS ... SS-P ...
>
> Stair Ascent ... SL ... SP ... PL ... PP ...

#### 摘录 C
- 出处：第 5 页，Section `The controller`
> Once a specific maneuvre and phase are detected, the controller sets the commands that drive the actuation stage at the low level of control.
>
> During stair ascent and walking, the commands consist of cyclically locking/unlocking the Weight Acceptance and Energy Transfer mechanisms and setting the positions of the knee and ankle actuators ...
>
> during the stand-to-sit and sit-to-stand tasks, the control action is designed to assist the maneuvre by providing an extensor torque at knee level ...
>
> The variation of their setpoint can be triggered not only by the transition from “Single Support—Sound” state to the “Double Support—Sound to Swing” state, but also by a threshold mechanism on the Centre of Pressure of the sound limb ... enabling knee extension and Weight Acceptance blocking to accomplish a safe initial foot contact with a rigid knee joint.

### 2. 基于原文整理后的自然语言描述

The Whole Body Awareness Controller is a hierarchical intention-aware supervisor that uses wearable IMUs, instrumented shoes, and heuristic threshold rules to drive the CYBERLEGs active transfemoral prosthesis. At the maneuver level, it recognizes eight states: steady `quiet standing`, `quiet sitting`, `stair ascent`, and `walking`, plus transient `sitting down`, `standing up`, `initiation`, and `termination`; within the steady maneuvers it also recognizes task-specific subphases. Walking and stair ascent are constrained to enter only through specific subphases, and the transition logic is explicit over sensor-derived conditions such as `DS-PTS`, `SS-S`, `DS-STS`, `SS-P`, `SL`, `SP`, `PL`, and `PP`. Once a maneuver-phase pair is recognized, the low-level controller cyclically locks or unlocks the Weight Acceptance and Energy Transfer mechanisms and sets knee and ankle positions for locomotion, while sit-to-stand and stand-to-sit inject knee extensor torque for push-off or braking. Safety is reinforced by timeout rules that force progression or an extended stiff configuration when transitions are missed, and by a center-of-pressure guard that can trigger knee extension and weight-acceptance blocking before foot contact.

### 3. 逐句溯源

1. 句子 1：The Whole Body Awareness Controller is a hierarchical intention-aware supervisor that uses wearable IMUs, instrumented shoes, and heuristic threshold rules to drive the CYBERLEGs active transfemoral prosthesis.
   对应摘录：A, B
2. 句子 2：At the maneuver level, it recognizes eight states: steady `quiet standing`, `quiet sitting`, `stair ascent`, and `walking`, plus transient `sitting down`, `standing up`, `initiation`, and `termination`; within the steady maneuvers it also recognizes task-specific subphases.
   对应摘录：A
3. 句子 3：Walking and stair ascent are constrained to enter only through specific subphases, and the transition logic is explicit over sensor-derived conditions such as `DS-PTS`, `SS-S`, `DS-STS`, `SS-P`, `SL`, `SP`, `PL`, and `PP`.
   对应摘录：A, B
4. 句子 4：Once a maneuver-phase pair is recognized, the low-level controller cyclically locks or unlocks the Weight Acceptance and Energy Transfer mechanisms and sets knee and ankle positions for locomotion, while sit-to-stand and stand-to-sit inject knee extensor torque for push-off or braking.
   对应摘录：C
5. 句子 5：Safety is reinforced by timeout rules that force progression or an extended stiff configuration when transitions are missed, and by a center-of-pressure guard that can trigger knee extension and weight-acceptance blocking before foot contact.
   对应摘录：B, C

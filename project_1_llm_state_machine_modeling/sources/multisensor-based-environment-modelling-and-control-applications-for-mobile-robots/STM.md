# Multisensor Based Environment Modelling and Control Applications for Mobile Robots - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：整篇 thesis 主要讲 SLAM 与 moving-object detection，但 Chapter 5 单独给出了一个用于移动机器人停车的 `St / F / R / Sp` 四态 FSM，状态、事件和切换条件都很明确，可作为 `🅿️` 方向离散停车控制样本。

## 条目 1: Four-State Vision-Based Parking FSM

- 控制对象：智慧停车领域的视觉引导移动机器人停车控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 thesis 第 5 章里一个基于视觉停车站特征的移动机器人停车控制器，用四态 FSM 在对齐、前进、后退和停车之间切换。
- 判断：算。虽然 thesis 大部分内容是 SLAM 和动态目标检测，但停车章节里的控制对象是实际移动机器人停车控制器，原文明确给出 FSM 元组、四个状态、事件和各状态中的控制动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 108 页，Section 5.3 `Control Strategy`
> Specifically, a finite state machine (FSM) is used at the heart of the parking control system to provide the context (state) of operation ... based on the current sensory information and the progress of the parking process. Thus, a state in the discrete part of the hybrid system encapsulates a particular continuous control scenario.

#### 摘录 B

- 出处：第 109-110 页，Section 5.3.1 `Finite State Machine`
> The FSM has four states and five transitions. Three states represent active controllers, while the other state represents the termination state. The FSM can be mathematically represented as: FSM = (X, E, a, x0, Xm) ... X = {St, F, R, Sp} ... a = {(St, e1) -> F, (St, e2) -> R, (F, e4) -> St, (R, e5) -> F, (R, e3) -> Sp}.

#### 摘录 C

- 出处：第 110-114 页，Section 5.3.2 `Details of the States`
> In the start state, the robot will be oriented so that the feature in the center (P2) of the parking station aligns with the center feature in the reference image (P2r). Then it will switch the control of the robot to either F or R state depending on the relative size of the parking station in the current image.
>
> When the controller is in [forward] state ... it will align a side feature a distance of c pixels from the edge of the image while moving towards the parking station ... The robot will exit this state when the uncontrolled side feature is less than c pixels away from the other edge.

#### 摘录 D

- 出处：第 114-116 页，Section 5.3.2 `Reverse (R) State` / Section 5.4.1
> During the reverse state the robot will move away from the parking station while aligning the center feature ... The robot will exit the reverse state when the robot is parked or when the overall size of the parking configuration is less than a predefined value, Amin.
>
> During the reverse motion the controller will attempt to keep the center feature of the parking station properly aligned ... When the parking station appears to be sufficiently small the robot will switch to the forward state. ... This cycle would continue until the robot converges to the defined position.

### 2. 基于原文整理后的自然语言描述

The parking controller is organized as a four-state FSM `St / F / R / Sp` whose purpose is to park a mobile robot against a visual parking station using repeated forward-reverse maneuvers. In `St`, the robot aligns the center feature of the observed parking station with the center feature of the reference image and then decides whether the next active state should be `F` or `R` based on the current apparent size of the station. In `F`, the robot drives toward the station while keeping a side feature at a virtual image-edge offset `c`, so the station remains inside the camera field of view and the controller can steer without losing visual context. In `R`, the robot backs away while re-aligning the center feature, and it leaves this state either when the station becomes small enough for another forward pass or when the parking condition is already satisfied. The machine repeats the `St -> F -> St -> R -> F ...` cycle until `Sp` is reached, where the vehicle stops after successful parking.

### 3. 逐句溯源

1. 句子 1：The parking controller is organized as a four-state FSM `St / F / R / Sp` whose purpose is to park a mobile robot against a visual parking station using repeated forward-reverse maneuvers.
   对应摘录：A, B
2. 句子 2：In `St`, the robot aligns the center feature of the observed parking station with the center feature of the reference image and then decides whether the next active state should be `F` or `R` based on the current apparent size of the station.
   对应摘录：C
3. 句子 3：In `F`, the robot drives toward the station while keeping a side feature at a virtual image-edge offset `c`, so the station remains inside the camera field of view and the controller can steer without losing visual context.
   对应摘录：C
4. 句子 4：In `R`, the robot backs away while re-aligning the center feature, and it leaves this state either when the station becomes small enough for another forward pass or when the parking condition is already satisfied.
   对应摘录：D
5. 句子 5：The machine repeats the `St -> F -> St -> R -> F ...` cycle until `Sp` is reached, where the vehicle stops after successful parking.
   对应摘录：B, D

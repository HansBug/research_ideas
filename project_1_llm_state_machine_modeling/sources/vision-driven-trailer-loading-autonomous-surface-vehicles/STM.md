# Vision driven trailer loading for autonomous surface vehicles in dynamic environments - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `ASV` 拖车装载的 `6` 状态 `FSM`、四个误差状态变量、`PI / time-based` 子控制器和 `replan` 回退链，可直接作为高质量移动平台对接控制样本。

## 条目 1: Trailer-docking supervisor for an autonomous surface vehicle
- 控制对象：自主水面艇 `ASV` 的拖车装载高层监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个围绕 `LED` 面板检测、航向纠正、横向纠正、纵向接近和回退重规划来组织 `ASV` 拖车对接的高层 docking supervisor。
- 判断：算。对象是真实自主船艇对接控制器，不是纯仿真流程；原文明确给出状态集合、误差变量、阈值 guard、每态低层控制器和失视/碰撞风险回退链，能恢复完整控制主链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section `3.2 Control strategy`
> The hierarchical control structure includes a finite state machine (FSM) ... and low-level controllers for each state.

#### 摘录 B
- 出处：第 6-7 页，Section `3.2 Control strategy` / Figure 5
> The FSM defines six high-level states ... Detect LED Panel (initial state), Correct Heading Error, Correct Lateral Error, Correct Longitudinal Error, Replan, and Mission Complete.
>
> The four state variables are: (1) LED panel detected, (2) lateral error below threshold elat, (3) heading error below threshold eang, and (4) longitudinal error below threshold Ex.

#### 摘录 C
- 出处：第 7 页，Section `3.2 Control strategy`
> In the starting state, it will rotate itself until it detects the LED panel. Once the LED panel is detected, it will enter the Correct Heading Error state. A PI controller is utilized to minimize the heading error eang ... After the eang is smaller than the threshold ϵang=0.05rad, the system will first try to minimize the lateral error elat.

#### 摘录 D
- 出处：第 7 页，Section `3.2 Control strategy`
> In the Correct Lateral Error state, a time-based controller is used to decrease elat ... if elat is larger than the threshold ... and the boat is closer than 0.5m to the bunk boards, the system will enter the Replan state ... If the ASV briefly loses visual contact with the LED panel, it stops its motion and transitions to the Detect LED Panel state.

#### 摘录 E
- 出处：第 7 页，Section `3.2 Control strategy`
> If both the elat and eang are smaller than the thresholds, the boat will enter the moving forward state ... If elong is smaller than the threshold ϵlong=0.1m, we consider the loading to be successful and stop the motors.

### 2. 基于原文整理后的自然语言描述

The trailer-loading controller organizes the `ASV` docking mission as a six-state FSM with `Detect LED Panel`, `Correct Heading Error`, `Correct Lateral Error`, `Correct Longitudinal Error`, `Replan`, and `Mission Complete`, and each state owns its own low-level controller. State evolution depends on four explicit variables: whether the `LED` panel is detected, whether `eang` is below threshold, whether `elat` is below threshold, and whether `elong` is below threshold. From the initial search state, the boat rotates until the panel is detected, then a `PI` heading controller drives `eang` below `0.05 rad` before the machine proceeds to lateral correction. In `Correct Lateral Error`, a time-based maneuver turns clockwise or counterclockwise according to the sign of `elat`, but if the lateral error is still too large when the hull is within `0.5 m` of the bunk boards, the FSM enters `Replan`, backs away, and later re-enters heading correction; temporary loss of the panel also forces a return to `Detect LED Panel`. Once both heading and lateral errors are small enough, the supervisor enters longitudinal approach, applies a second `PI` controller to reduce `elong`, and stops the motors when `elong < 0.1 m`.

### 3. 逐句溯源

1. 句子 1：The trailer-loading controller organizes the `ASV` docking mission as a six-state FSM with `Detect LED Panel`, `Correct Heading Error`, `Correct Lateral Error`, `Correct Longitudinal Error`, `Replan`, and `Mission Complete`, and each state owns its own low-level controller.
   对应摘录：A, B
2. 句子 2：State evolution depends on four explicit variables: whether the `LED` panel is detected, whether `eang` is below threshold, whether `elat` is below threshold, and whether `elong` is below threshold.
   对应摘录：B
3. 句子 3：From the initial search state, the boat rotates until the panel is detected, then a `PI` heading controller drives `eang` below `0.05 rad` before the machine proceeds to lateral correction.
   对应摘录：C
4. 句子 4：In `Correct Lateral Error`, a time-based maneuver turns clockwise or counterclockwise according to the sign of `elat`, but if the lateral error is still too large when the hull is within `0.5 m` of the bunk boards, the FSM enters `Replan`, backs away, and later re-enters heading correction; temporary loss of the panel also forces a return to `Detect LED Panel`.
   对应摘录：D
5. 句子 5：Once both heading and lateral errors are small enough, the supervisor enters longitudinal approach, applies a second `PI` controller to reduce `elong`, and stops the motors when `elong < 0.1 m`.
   对应摘录：E

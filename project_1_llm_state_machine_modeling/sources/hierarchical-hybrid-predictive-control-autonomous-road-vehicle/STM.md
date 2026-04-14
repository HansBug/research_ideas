# Hierarchical Hybrid Predictive Control of an Autonomous Road Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动驾驶高速工况的高层 maneuver assigner 明确写成 FSM，并把连续速度边界、前后车速度和换道许可条件直接写进切换规则，是高质量的 hybrid-EFSM 样本。

## 条目 1: Highway Maneuver Assigner for Hybrid Predictive Guidance

- 控制对象：高速公路场景下自动驾驶车辆的高层 maneuver assigner 与轨迹引导切换控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把离散 maneuver selection 与连续 MPC 轨迹引导耦合起来的自动驾驶高层控制器。
- 判断：算。对象是自动驾驶车辆的高层决策控制器本身，原文明确给出了 FSM assigner、切换规则、离散 maneuver state 集合和与 MPC 的接口关系。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 27-42 行
> This paper presents a hierarchical hybrid predictive control framework for an autonomously controlled road vehicle. At the top, an assigner module is designed as a finite state machine for decision-making. ... the assigner selects discrete maneuver states through pre-defined switching rules. The several maneuver states are related to different setups for the underlying model predictive trajectory guidance module.

#### 摘录 B

- 出处：第 2 页，Section 2 `Control Framework`，`paper_content.txt` 第 182-195 行
> The higher-level discrete state module is responsible for the discrete situations or several maneuver states designed in the assigner and executed by MPC-based PTG system. ... The assigner is designed as a (set of) finite state machine(s) for decision-making. Therein, which state the vehicle is to be in is determined by switching rules acting according to the current state of the vehicle and its environment.

#### 摘录 C

- 出处：第 3 页，Section 3 `Assigner Maneuver States`，`paper_content.txt` 第 208-230, 237-242 行
> The assigner module could consist of several finite state machines (FSMs) ... In each FSM, the ACV can switch its target state among different maneuvers each of which have associated setups of the MPC in the PTG. ... The transitions between different maneuvers are determined by the switching rules shown in Table 1.
>
> vf and vr represent the speeds of the front vehicle (FV) and rear vehicle (RV) ... vt is the speed of the ACV. vlcl and vlch are customizable lower and higher bounds of satisfactory speeds ... If these speed ranges are violated, i.e. vt > vlch or vt < vlcl, a lane change will be triggered.

#### 摘录 D

- 出处：第 3-4 页，Section 3 `Assigner Maneuver States`，`paper_content.txt` 第 268-302 行
> When the FV and RV are too far away ... the ACV is in the state designated S1: Normal Tracking. ... If FV is approaching the ACV (vf < vt), ... the ACV will switch from state S1 to state S2: Following. When the RV is approaching (vr > vt), the ACV will switch to state S3: Leading. ... Once vt violates [vlcl, vlch], the ACV will switch to state S4: Lane Change, if it’s allowed to make a lane change based on the lane marks and the availability of the adjacent lanes. After the lane change, the state will automatically switch back to state S1. ... the ACV could also switch to state S4 if it needs to merge in or leave the highway.

### 2. 基于原文整理后的自然语言描述

The proposed autonomous-road-vehicle controller is a hierarchical hybrid framework in which a high-level assigner chooses discrete maneuver states and a lower MPC layer executes the corresponding trajectory-guidance setup. The assigner itself is modeled as one or more finite state machines whose target state depends on switching rules over the current vehicle state and environmental observations. Those rules explicitly use front-vehicle speed `vf`, rear-vehicle speed `vr`, ego speed `vt`, and the satisfactory-speed interval `[vlcl, vlch]`, so the maneuver selector is an extended state machine driven by continuous-valued guards. In the highway case study, the main maneuver states are `S1: Normal Tracking`, `S2: Following`, `S3: Leading`, and `S4: Lane Change`. The controller keeps the lane in `S1`, switches to `S2` when the front vehicle approaches, switches to `S3` when the rear vehicle approaches, and enters `S4` when the ego speed violates the satisfactory-speed bounds or when the route requires merge-in or exit. After a valid lane change is completed, the FSM returns automatically to `S1`, completing the discrete-to-continuous supervisory loop.

### 3. 逐句溯源

1. 句子 1：The proposed autonomous-road-vehicle controller is a hierarchical hybrid framework in which a high-level assigner chooses discrete maneuver states and a lower MPC layer executes the corresponding trajectory-guidance setup.
   对应摘录：A, B
2. 句子 2：The assigner itself is modeled as one or more finite state machines whose target state depends on switching rules over the current vehicle state and environmental observations.
   对应摘录：B, C
3. 句子 3：Those rules explicitly use front-vehicle speed `vf`, rear-vehicle speed `vr`, ego speed `vt`, and the satisfactory-speed interval `[vlcl, vlch]`, so the maneuver selector is an extended state machine driven by continuous-valued guards.
   对应摘录：C
4. 句子 4：In the highway case study, the main maneuver states are `S1: Normal Tracking`, `S2: Following`, `S3: Leading`, and `S4: Lane Change`.
   对应摘录：D
5. 句子 5：The controller keeps the lane in `S1`, switches to `S2` when the front vehicle approaches, switches to `S3` when the rear vehicle approaches, and enters `S4` when the ego speed violates the satisfactory-speed bounds or when the route requires merge-in or exit.
   对应摘录：D
6. 句子 6：After a valid lane change is completed, the FSM returns automatically to `S1`, completing the discrete-to-continuous supervisory loop.
   对应摘录：D

# Design and Control of a Size-Adjustable Pediatric Lower-Limb Exoskeleton Based on Weight Shift - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了儿童下肢外骨骼的 `6` 状态 `FSM`、`8` 个动作、基于 `COM` 的 minimum-jerk 轨迹规划和 `GRF` 触发 guard，可直接提取为高质量 gait assistance 样本。

## 条目 1: Weight-shift walking supervisor for the pediatric lower-limb exoskeleton
- 控制对象：儿童下肢外骨骼的 gait assistance 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个通过 `COM` 转移和 `GRF` 降幅判断来组织站立、重心平移和左右摆腿的儿童外骨骼步态监督控制器。
- 判断：算。对象是真实儿童外骨骼控制器，不是康复流程；原文明确给出状态定义、过渡动作、轨迹生成和步触发 guard，能恢复成完整高层控制链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section `A. FINITE STATE MACHINE`
> The general scheme of the proposed FSM model can be seen in Figure 8, where the exoskeleton’s gait is separated into 6 different states.
>
> State 1 (S1): The exoskeleton is in stand-up position and the feet are parallel.
>
> State 2 (S2): Both feet are still parallel, however, the joint configuration of the exoskeleton is changed to let the COM approach the left foot.
>
> State 3 (S3) ... right foot is at the front and the left foot is at the rear.
>
> State 4 (S4) ... the COM is moved from the center of the support polygon to the right foot.
>
> State 5 (S5) ... left foot at the front ...
>
> State 6 (S6) ... the COM will be located on the left foot.

#### 摘录 B
- 出处：第 6 页，Section `A. FINITE STATE MACHINE`
> Transitions between different states need to go through some well-designed actions.
>
> Action 1 (A1) ... shift the COM ... to the left foot while holding both feet on the ground.
>
> Action 4 (A4) ... The left leg starts to swing and move the left foot forward to make an entire step.
>
> Action 7 (A7) ... brings the exoskeleton back to a previous state (S3) so that a closed loop for continuous walking can be formed: S6⇒S3⇒S4⇒S5⇒S6.
>
> Action 8 (A8) ... let the exoskeleton return to its initial state (S1).

#### 摘录 C
- 出处：第 7 页，Section `B. GAIT PLANNING CONSIDERING COM SHIFT`
> During the rehabilitation training with an exoskeleton, one of the most challenging parts for the patient is the shifting of their COM to a suitable position so that they can easily lift up the swing leg and move forward.
>
> We can first plan the trajectory of the COM and then calculate the joint configuration by using the inverse kinematic model ...
>
> The minimum jerk trajectory function is a commonly used method in the robotic field for generating both smooth and energy-efficient movement.

#### 摘录 D
- 出处：第 7 页，Section `C. AUTOMATIC STEP TRIGGERING`
> An automatic step-triggering strategy based on the ground reaction force on the swing leg is proposed.
>
> The main idea of this strategy is to monitor the change of ground reaction force of the swing leg during the COM shift actions (A1, A3, and A6), if the force is sufficiently decreased compared to the start of the action, we can assume that the COM transition is done and the step can be triggered.
>
> After the COM shift action is finished, the controller will keep monitoring the γtGRF,i and if it is larger than a preset threshold, the step will be triggered.

#### 摘录 E
- 出处：第 7 页，Section `D. IMPLEMENTATION USING SIMULINK REAL-TIME`
> This model consists of three main parts ... and PDO communication which contains the core of the control algorithm and runs in real-time with a frequency of 1kHz.

### 2. 基于原文整理后的自然语言描述

The pediatric lower-limb exoskeleton is supervised by a six-state walking FSM that alternates between parallel standing, left or right weight-shift states, and asymmetric double-support configurations with one foot leading. State transitions are not direct jumps but are realized by eight explicit actions, where `A1 / A3 / A6` shift the `COM` over the future stance leg, `A2 / A4 / A7` execute full-step swings, and `A5 / A8` execute half-step returns to `S1`, thereby supporting both continuous walking and controlled stop. For each action, the controller plans a specific `COM` path using minimum-jerk trajectories and then derives the joint configuration through inverse kinematics so that the exoskeleton performs a smooth transfer-and-swing motion. After every `COM`-shift action, the supervisor monitors the swing-leg ground reaction force and triggers the next step only when the normalized decrease `γGRF` exceeds a preset threshold, which means the body mass has actually shifted to the support leg. The resulting FSM, trajectory planner, and `GRF`-based trigger run together in the real-time control core at `1 kHz`, forming a complete pediatric gait-assistance supervisor.

### 3. 逐句溯源

1. 句子 1：The pediatric lower-limb exoskeleton is supervised by a six-state walking FSM that alternates between parallel standing, left or right weight-shift states, and asymmetric double-support configurations with one foot leading.
   对应摘录：A
2. 句子 2：State transitions are not direct jumps but are realized by eight explicit actions, where `A1 / A3 / A6` shift the `COM` over the future stance leg, `A2 / A4 / A7` execute full-step swings, and `A5 / A8` execute half-step returns to `S1`, thereby supporting both continuous walking and controlled stop.
   对应摘录：B
3. 句子 3：For each action, the controller plans a specific `COM` path using minimum-jerk trajectories and then derives the joint configuration through inverse kinematics so that the exoskeleton performs a smooth transfer-and-swing motion.
   对应摘录：C
4. 句子 4：After every `COM`-shift action, the supervisor monitors the swing-leg ground reaction force and triggers the next step only when the normalized decrease `γGRF` exceeds a preset threshold, which means the body mass has actually shifted to the support leg.
   对应摘录：D
5. 句子 5：The resulting FSM, trajectory planner, and `GRF`-based trigger run together in the real-time control core at `1 kHz`, forming a complete pediatric gait-assistance supervisor.
   对应摘录：E

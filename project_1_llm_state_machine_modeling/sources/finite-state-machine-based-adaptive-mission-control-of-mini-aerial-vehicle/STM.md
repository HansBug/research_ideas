# A Finite State Machine Based Adaptive Mission Control of Mini Aerial Vehicle - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把高压线路绝缘子巡检任务写成了带顶层 `Flight / Inspection` 父状态、九个子状态和显式输入真值表的任务控制器，是一个很完整的 `HSM + T1` 无人机样本。

## 备注

- 文中形式化元组一处写成 `$Q = \{S1,\dots,S7\}$`，但后续状态枚举、层次说明和真值表明确包含 `S8 = Land`、`S9 = Emergency`；本条目按图 2、状态列表与表 5 联合解释控制链。

## 条目 1: Adaptive Inspection Mission HSM for Mini Aerial Vehicle
- 控制对象：航空航天与飞行控制领域的微型飞行器巡检任务控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向输电线路绝缘子巡检任务的 MAV 自适应任务控制器，用分层任务状态和显式事件输入调度起飞、搜目标、悬停、变位、着陆与应急接管。
- 判断：算。对象是实际巡检飞行任务控制器而不是单纯视觉算法，原文给出了任务状态集合、层次父状态、输入变量、参数表和完整转移真值表。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，`II. ADAPTIVE MISSION CONTROL FOR MAV`（对应 `paper_content.txt` 第 210-260 行）
> Each step becomes a state of FSM for the MAV mission control. There are several main tasks/actions (states) to fulfill the inspection completely: Initial, Take off, Hold Position, Change Position, Search Object, Landing, Inspection, Emergency.
>
> Take Off ... The MAV will continue the taking off procedure until it reaches the given target height.
>
> Hold Position ... there could be pre-defined time for this procedure.
>
> Change Position ... it is guided by certain height or horizontal position parameters ... During the inspection process, the flight is guided by visual navigation and the inspection object has to be continuously detected.

#### 摘录 B
- 出处：第 4 页，`Search Object / Inspection / Emergency`（对应 `paper_content.txt` 第 281-316 行）
> Search Object ... MAV rotates in one position until it finds the inspection object. This is an initial action of the inspection process and crucial task of self-navigation. On the other hand, this is a transition face from GPS navigation to visual navigation.
>
> Inspection state is a hierarchal state, which includes Hold Position, Change Position and History states.
>
> In Emergency state, MAV flight control switches to Position Hold Mode, so the operator can control the MAV manually. After the dangerous condition has been eliminated, the mission control arrives in the previous state.

#### 摘录 C
- 出处：第 4-5 页，`III. STATE MACHINE FOR MISSION CONTROL / Table 5`（对应 `paper_content.txt` 第 324-366 行、第 374-397 行）
> Mission control FSM is a hierarchical state machine and has total nine states. It starts from Initial state. The next main state is Flight state ... Inspection state is also super state, which has hierarchical Hold Position, Change Position and History states.
>
> For the state transition, there are six different inputs defined initially: `I1` start button, `I2` target position reached, `I3` target time reached, `I4` inspection object detected, `I5` inspection done, `I6` emergency condition occurred.
>
> Table 5 ... `S1 -> S2`, `S2 -> S3`, `S3 -> S4`, `S4 -> S7 / S5`, `S5 -> S5 / S6 / S8`, `S6 -> S6 / S5`, `S7 -> S7 / S4(H)`, `S8 -> S8 / S1`, `S2-S9 -> S9`.

### 2. 基于原文整理后的自然语言描述

The adaptive mission controller models mini-aerial-vehicle insulator inspection as a hierarchical mission state machine that begins in `Initial`, enters top-level `Flight` after a manual start command, and refines flight into `Take Off`, `Inspection`, `Land`, `Search Object`, and history states. Within `Inspection`, a nested controller alternates between `Hold Position` and `Change Position`, where `Hold Position` captures timed stabilization and `Change Position` moves the MAV according to mission height or distance parameters or visual-navigation guidance. `Search Object` rotates the MAV in place until the insulator is detected, thereby bridging GPS-based navigation and visual navigation, while `Emergency` is triggered by restricted-zone entry, low voltage, or other unsafe situations and forces `Position Hold Mode` for manual operator takeover. The paper also defines event inputs `I1-I6` for start, target-position reached, target-time reached, object detected, inspection done, and emergency occurred, and Table 5 maps these inputs to concrete transitions such as `S1 -> S2`, `S3 -> S4`, `S4 -> S7 / S5`, `S5 -> S6 / S8`, and `S7 -> S4(H)`. This makes the controller a reusable `HSM + T1` mission skeleton in which nested inspection behavior is driven by position, time, detection, completion, and emergency events.

### 3. 逐句溯源

1. 句子 1：The adaptive mission controller models mini-aerial-vehicle insulator inspection as a hierarchical mission state machine that begins in `Initial`, enters top-level `Flight` after a manual start command, and refines flight into `Take Off`, `Inspection`, `Land`, `Search Object`, and history states.
   对应摘录：A, C
2. 句子 2：Within `Inspection`, a nested controller alternates between `Hold Position` and `Change Position`, where `Hold Position` captures timed stabilization and `Change Position` moves the MAV according to mission height or distance parameters or visual-navigation guidance.
   对应摘录：A, B
3. 句子 3：`Search Object` rotates the MAV in place until the insulator is detected, thereby bridging GPS-based navigation and visual navigation, while `Emergency` is triggered by restricted-zone entry, low voltage, or other unsafe situations and forces `Position Hold Mode` for manual operator takeover.
   对应摘录：B
4. 句子 4：The paper also defines event inputs `I1-I6` for start, target-position reached, target-time reached, object detected, inspection done, and emergency occurred, and Table 5 maps these inputs to concrete transitions such as `S1 -> S2`, `S3 -> S4`, `S4 -> S7 / S5`, `S5 -> S6 / S8`, and `S7 -> S4(H)`.
   对应摘录：C
5. 句子 5：This makes the controller a reusable `HSM + T1` mission skeleton in which nested inspection behavior is driven by position, time, detection, completion, and emergency events.
   对应摘录：A, B, C

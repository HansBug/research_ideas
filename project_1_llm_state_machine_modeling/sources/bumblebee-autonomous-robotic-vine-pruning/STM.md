# Bumblebee: A Path Towards Fully Autonomous Robotic Vine Pruning - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把葡萄藤修剪机器人明确写成 `navigation / perception / manipulation / error` 四态高层 FSM，并给出每个宏状态下的子模块与 `success / failure / done` 驱动的切换链。

## 条目 1: Hierarchical vine-pruning autonomy supervisor

- 控制对象：工业自动化与农业机器人领域的葡萄藤自主修剪高层监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于葡萄藤自主修剪机器人的高层分层监督器，外层在导航、感知、操作和错误恢复之间推进，内层由各状态的任务子模块与内部错误子状态实现。
- 判断：算。对象是真实农业机器人控制系统而不是纯视觉/规划方法；原文明确给出四个主状态、状态内子模块、`success / failure / done` 结果驱动的切换逻辑，以及完整的 field pruning cycle。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 22-30 行
> In this paper, we present the design and field evaluation of a rugged, and fully autonomous robot for end-to-end pruning of dormant season grapevines. The proposed design incorporates novel camera systems, a kinematically redundant manipulator, and a mobile robot platform for autonomous navigation and pruning.

#### 摘录 B

- 出处：第 18 页，Figure 13 / Section `4.5.2 Full autonomy`
> Figure 13 shows outer states `navigation`, `perception`, `manipulation`, and `error`. The `navigation` sub-module contains `GPS Waypoint Follow`, `RTK Set`, and `Internal Error State`; the `perception` sub-module contains `3D Modeling`, `Cut-point Localization`, and `Internal Error State`; and the `manipulation` sub-module contains `Approach Target`, `Homing`, and `Internal Error State`, with `success`, `failure`, and `done` transitions connecting the macro states.

#### 摘录 C

- 出处：第 18 页，`paper_content.txt` 第 726-736 行
> Figure 13: Finite state machine. Depending on the state of the sub-modules, the state machine transitions between navigation, manipulation, perception, and error states for autonomous high-level control of the robot. ... The states in the FSM were navigation, perception, manipulation, and error. Depending on the status of the sub-modules within each state, the FSM transitions between different states following a pre-defined sequence ... Additionally, for robustness, each of the sub-processes of the states were equipped with internal error sub-states ...

#### 摘录 D

- 出处：第 19 页与结论，`paper_content.txt` 第 1016-1024、1157-1160 行
> the robot drove to each pruning location, remain stopped while pruning and start moving again to the next vine location. ... the pruning task was accomplished successfully in all 20 vines. ... The integrated system robustly identified pruning location and pruned 87% of the canes successfully, with an average cycle time of 213 sec /vine from two sides and 137 sec/vine from one side.

### 2. 基于原文整理后的自然语言描述

The Bumblebee pruning robot is supervised by a hierarchical FSM whose outer states are `navigation`, `perception`, `manipulation`, and `error`, so one complete pruning cycle is executed as a controlled sequence rather than as a loose collection of perception and motion modules. Each macro state owns its own sub-module: navigation handles waypoint following and RTK positioning, perception performs `3D Modeling` and `Cut-point Localization`, and manipulation performs `Approach Target` and `Homing`, with internal error states embedded in these sub-processes. The outer supervisor advances or rolls back according to `success`, `failure`, and `done` results returned by the sub-modules, and unknown hardware or software issues force the system into the error path for manual intervention. In field operation, this supervisory layer makes the robot drive to each vine, stop while pruning, move to the next vine, and repeat the cycle until all vines are processed. The reported integrated system robustly identified pruning locations and successfully pruned `87%` of canes, showing that the FSM is tied to a real autonomous work cycle rather than to a toy lab workflow.

### 3. 逐句溯源

1. 句子 1：The Bumblebee pruning robot is supervised by a hierarchical FSM whose outer states are `navigation`, `perception`, `manipulation`, and `error`, so one complete pruning cycle is executed as a controlled sequence rather than as a loose collection of perception and motion modules.
   对应摘录：A, C
2. 句子 2：Each macro state owns its own sub-module: navigation handles waypoint following and RTK positioning, perception performs `3D Modeling` and `Cut-point Localization`, and manipulation performs `Approach Target` and `Homing`, with internal error states embedded in these sub-processes.
   对应摘录：B, C
3. 句子 3：The outer supervisor advances or rolls back according to `success`, `failure`, and `done` results returned by the sub-modules, and unknown hardware or software issues force the system into the error path for manual intervention.
   对应摘录：B, C
4. 句子 4：In field operation, this supervisory layer makes the robot drive to each vine, stop while pruning, move to the next vine, and repeat the cycle until all vines are processed.
   对应摘录：C, D
5. 句子 5：The reported integrated system robustly identified pruning locations and successfully pruned `87%` of canes, showing that the FSM is tied to a real autonomous work cycle rather than to a toy lab workflow.
   对应摘录：A, D

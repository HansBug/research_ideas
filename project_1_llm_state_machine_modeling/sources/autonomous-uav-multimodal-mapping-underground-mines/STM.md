# Development of an Autonomous UAV for Multi-Modal Mapping of Underground Mines - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了地下矿井 UAV 的三类 mission mode 及其子阶段，包括手动记录、反应式探索和支柱扫描，状态图与正文都能直接支撑高质量任务级建模。

## 条目 1: Mission supervisor for mine exploration and pillar inspection
- 控制对象：地下矿井测绘无人机的任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个地下矿井 UAV 的多任务监督状态机，用于在手动记录、走廊探索和支柱自动扫描三种模式之间切换，并管理起飞、定高、自由空间搜索、角点检测和落地。
- 判断：算。对象是真实地下矿井测绘无人机的平台任务控制器，不是单纯 SLAM 或点云处理流程；原文给出了 mission mode、子阶段和 back-and-forth 扫描逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 12 页，Section 3.5 `Onboard Computing and Control`
> Three distinct control modes were developed: manual data collection, reactive exploration, and supervised autonomous pillar inspection.
>
> This package centralizes the required communication bridges, camera and LiDAR drivers, and the core finite-state machine.
>
> Each mode is governed by its own FSM, which manages transitions between flight phases, ensuring safety and data integrity.

#### 摘录 B
- 出处：第 13 页，Figure 6
> The robot state machine has the initial state to record data, and three different options: manual flight (mission 1), reactive exploration (mission 2), and supervised autonomous inspection (mission 3).
>
> In mission 2, the drone takes off to a safe altitude, finds the most open space, adjusts its attitude towards it and move with the commanded velocity toward it.
>
> In mission 3, a back-and-forth strategy is utilized to cover the face of a pillar.

#### 摘录 C
- 出处：第 13 页，Section 3.5.1 `Manual Flight and Data Logging`
> The state machine for this mission decouples flight control from data acquisition.
>
> A dedicated "Data recording" mission can be started independently of the flight status, allowing the operator to fly to a region of interest and engage the high-bandwidth recording (LiDAR and cameras) only when necessary.

#### 摘录 D
- 出处：第 13-14 页，Section 3.5.2-3.5.3
> The second mode is designed to navigate unknown corridors autonomously, using a lightweight, reactive planner.
>
> The third mission focuses on high-resolution 3D reconstruction of specific mine pillars.
>
> The algorithm adjusts the current distance to the wall and maintains it constant, ensuring complete coverage of the pillar face.
>
> To execute the sequence of horizontal passes at incremental altitudes, we use a single-point array of four LiDARs, with three pointing forward to identify corners and one pointing up to measure the distance to the ceiling.

### 2. 基于原文整理后的自然语言描述

The underground-mine UAV is governed by a hierarchical mission supervisor whose initial state can start standalone data recording or branch into one of three mission modes: manual flight, reactive exploration, and supervised autonomous pillar inspection. In the manual branch, flight control remains with the operator while the FSM decouples data acquisition so that high-bandwidth LiDAR and camera recording can be turned on only when required at a region of interest. In `Mission 2`, the controller takes off to a safe altitude, evaluates the surrounding LiDAR returns to find the most open direction, adjusts the vehicle attitude toward that free-space vector, and then moves with the commanded velocity while still allowing supervised intervention or landing. In `Mission 3`, the UAV first adjusts its distance and relative pose with respect to a target pillar, then uses forward corner detection and upward ceiling distance sensing to maintain the geometry needed for scanning. The inspection routine executes a back-and-forth sweeping pattern over the pillar face through repeated horizontal passes at incremental altitudes until full coverage is achieved or the landing path is triggered.

### 3. 逐句溯源

1. 句子 1：The underground-mine UAV is governed by a hierarchical mission supervisor whose initial state can start standalone data recording or branch into one of three mission modes: manual flight, reactive exploration, and supervised autonomous pillar inspection.
   对应摘录：A, B, C
2. 句子 2：In the manual branch, flight control remains with the operator while the FSM decouples data acquisition so that high-bandwidth LiDAR and camera recording can be turned on only when required at a region of interest.
   对应摘录：C
3. 句子 3：In `Mission 2`, the controller takes off to a safe altitude, evaluates the surrounding LiDAR returns to find the most open direction, adjusts the vehicle attitude toward that free-space vector, and then moves with the commanded velocity while still allowing supervised intervention or landing.
   对应摘录：B, D
4. 句子 4：In `Mission 3`, the UAV first adjusts its distance and relative pose with respect to a target pillar, then uses forward corner detection and upward ceiling distance sensing to maintain the geometry needed for scanning.
   对应摘录：B, D
5. 句子 5：The inspection routine executes a back-and-forth sweeping pattern over the pillar face through repeated horizontal passes at incremental altitudes until full coverage is achieved or the landing path is triggered.
   对应摘录：B, D

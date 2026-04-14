# PIRATE-Precision Imaging Real-Time Autonomous Tracker & Explorer - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把海上自主追踪平台的 mission execution 明确写成层次化 `FSM`，包含 `idle / navigation / tracking / visual processing / RTH / fault handling`、全局 failsafe 中断和声学-视觉闭环追踪链，是质量很高的自主平台任务监督样本。

## 条目 1: Hierarchical mission-execution FSM for an autonomous marine tracker

- 控制对象：通用控制与自主水面观测平台领域的任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个部署在 `PIRATE` 自主水面平台上的任务执行状态机，用层次化 mission supervisor 协调航迹导航、声学定位、视觉处理、追踪追击和故障回家。
- 判断：算。对象是真实自主平台控制器，原文不仅明确给出高层模式集合和全局中断逻辑，还说明追踪任务如何在 triangulation、pursuit、loiter 和视觉采样之间切换。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 24-37 行
> PIRATE enables adaptive, target-driven operation, in which navigation, acoustic monitoring, and visual processing are coordinated within a mission-level control loop. The system integrates real-time AI-based visual detection and tracking with automatic mission planning ...

#### 摘录 B

- 出处：第 9-10 页，`Mission execution` 与 Figure 3，`paper_content.txt` 第 407-418 行
> Mission execution is structured as a finite state machine (FSM) governing distinct operational modes, including idle, navigation, tracking, visual processing, return-to-home (RTH), and fault handling. This FSM-based design enforces deterministic state transitions ... high-level operational states are organized hierarchically, with composite modes encapsulating navigation and perception substates. Transition triggers are event-driven, and a global interrupt mechanism allows immediate transition to the RTH state from any active mode.

#### 摘录 C

- 出处：第 10、18 页，`Single-Receiver Acoustic Localization` 与 tracking experiment，`paper_content.txt` 第 443-453、771-779 行
> During tracking missions, the platform autonomously executes predefined polygonal listening trajectories to generate sufficient spatial diversity for localization. Target position estimates are updated incrementally onboard ...
>
> The experiment consisted of three consecutive tracking-pursuit cycles executed within a single continuous deployment. In each cycle, PIRATE first performed an acoustic triangulation phase ... Following target estimation, PIRATE transitioned into a pursuit phase ... Upon completion of the first pursuit phase, PIRATE entered a loiter mode in the vicinity of the estimated target position.

### 2. 基于原文整理后的自然语言描述

The PIRATE platform organizes mission execution as a hierarchical FSM whose top-level modes are `Idle`, `Navigation`, `Tracking`, `Visual Processing`, `Return-to-Home`, and `Fault Handling`. This supervisor is not only a label set: the paper states that composite modes contain navigation and perception substates, that transitions are event-driven, and that a global interrupt can force immediate `RTH` from any active mode. In normal tracking missions, the platform first runs polygonal listening trajectories to gather acoustic measurements, incrementally estimates target position onboard, and then transitions into a pursuit phase toward the estimated location. After each pursuit cycle, the controller can enter a loiter phase near the target while continuing to receive acoustic transmissions and collect underwater visual data. The same mission-level loop coordinates acoustic localization, visual sensing, and vehicle motion so that perception outputs actively change navigation behavior rather than being logged passively. This makes PIRATE a clean `HSM + T0` sample for autonomous marine mission supervision.

### 3. 逐句溯源

1. 句子 1：The PIRATE platform organizes mission execution as a hierarchical FSM whose top-level modes are `Idle`, `Navigation`, `Tracking`, `Visual Processing`, `Return-to-Home`, and `Fault Handling`.
   对应摘录：A, B
2. 句子 2：This supervisor is not only a label set: the paper states that composite modes contain navigation and perception substates, that transitions are event-driven, and that a global interrupt can force immediate `RTH` from any active mode.
   对应摘录：B
3. 句子 3：In normal tracking missions, the platform first runs polygonal listening trajectories to gather acoustic measurements, incrementally estimates target position onboard, and then transitions into a pursuit phase toward the estimated location.
   对应摘录：C
4. 句子 4：After each pursuit cycle, the controller can enter a loiter phase near the target while continuing to receive acoustic transmissions and collect underwater visual data.
   对应摘录：C
5. 句子 5：The same mission-level loop coordinates acoustic localization, visual sensing, and vehicle motion so that perception outputs actively change navigation behavior rather than being logged passively.
   对应摘录：A, C
6. 句子 6：This makes PIRATE a clean `HSM + T0` sample for autonomous marine mission supervision.
   对应摘录：A, B, C

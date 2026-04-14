# Safety-critical Autonomous Inspection of Distillation Columns using Quadrupedal Robots Equipped with Roller Arms - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把蒸馏塔托盘巡检任务明确组织成七任务状态机，给出了搜索、巡检、移向 manway、过渡准备、上下层转移、后处理与安全撤离的主链，并说明了失败时的停机处理。

## 条目 1: Seven-Task Distillation-Column Inspection Supervisor
- 控制对象：在蒸馏塔多层托盘环境中执行自主巡检的四足机器人任务监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是化工装置巡检场景中的四足机器人任务监督器，用来把托盘内巡检、manway 搜索、层间过渡和安全撤离组织成一条完整的自主任务链。
- 判断：算。对象是实际四足巡检机器人在工业蒸馏塔中的任务控制链，原文明确给出了状态机在系统中的角色、七个任务状态、任务重复条件以及转移失败时的停止处理。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Introduction，行 17-20、43-57
> integrates ... into a state machine

#### 摘录 B
- 出处：第 5 页，Section V-E，行 495-518
> "Searching" ... "Transition (Up/Down)" ... "safe location"

#### 摘录 C
- 出处：第 5-6 页，Section V-E / Figure 6-7，行 519-539
> "failed transitions" ... "halts"

### 2. 基于原文整理后的自然语言描述

The inspection controller is a seven-task FSM that coordinates a quadruped robot as it autonomously inspects multi-layer distillation-column trays. The task chain starts with `Searching` to obtain the manway vertices, proceeds to `Locomotion (Inspection)` inside one tray, then sends the robot to the manway, applies a pre-motion to prepare the required contact sequence, executes an `Up/Down` transition between columns, performs a post-motion to restore locomotion readiness, and finally drives the robot to a predefined safe location. The same state machine can repeat the inspection phase when new goals are added or modified, so it supports incremental mission execution rather than a single one-shot pass. If a stable layer transition is not achieved, the transition is terminated, and failed transitions halt the robot’s actions instead of letting it continue in an unsafe state. This gives the paper a clear system-level `FSM + T0` supervisory chain for industrial inspection robotics.

### 3. 逐句溯源

1. 句子 1：The inspection controller is a seven-task FSM that coordinates a quadruped robot as it autonomously inspects multi-layer distillation-column trays.
   对应摘录：A, B
2. 句子 2：The task chain starts with `Searching` to obtain the manway vertices, proceeds to `Locomotion (Inspection)` inside one tray, then sends the robot to the manway, applies a pre-motion to prepare the required contact sequence, executes an `Up/Down` transition between columns, performs a post-motion to restore locomotion readiness, and finally drives the robot to a predefined safe location.
   对应摘录：B
3. 句子 3：The same state machine can repeat the inspection phase when new goals are added or modified, so it supports incremental mission execution rather than a single one-shot pass.
   对应摘录：C
4. 句子 4：If a stable layer transition is not achieved, the transition is terminated, and failed transitions halt the robot’s actions instead of letting it continue in an unsafe state.
   对应摘录：C
5. 句子 5：This gives the paper a clear system-level `FSM + T0` supervisory chain for industrial inspection robotics.
   对应摘录：A, B, C

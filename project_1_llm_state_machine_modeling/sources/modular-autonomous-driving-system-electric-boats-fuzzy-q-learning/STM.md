# A Modular Autonomous Driving System for Electric Boats based on Fuzzy Controllers and Q-Learning - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把电动船自主驾驶系统明确写成一个监督层 `FSM`，用 `Virtual Anchor / Manual Drive / Exiting / Navigation / Avoid / Enter` 六态选择不同控制流水线，系统级结构和状态语义都很完整。

## 条目 1: Six-State Supervisor for Autonomous Electric-Boat Operations

- 控制对象：通用控制与水面载具任务领域的电动船自主驾驶监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向内河电动船自主驾驶的高层监督器，用监督层 `FSM` 在手动、出港、导航、避障、入港和虚拟锚泊之间切换不同运动控制流水线。
- 判断：算。对象是实际自主船控制系统的监督层，不是单纯模块框架；原文直接给出六个状态、状态切换条件和每个状态对应的处理流水线。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 15-23 行
> The boat will be in charge to exit and enter from harbors, plan and follow a route, avoid obstacles such as other boats, correct its motion, perform a virtual anchor and switch between these operations autonomously ... We propose an architecture integrating several Fuzzy Controller-based modular pipelines.

#### 摘录 B

- 出处：第 3-4 页，Section 2 `Proposed Autonomous Driving System Architecture`，`paper_content.txt` 第 229-247 行
> The supervision level consists of a Supervisor, a HMI and a FSM ... The driving level consists of manual controls and four modular pipelines ... navigation ... obstacle avoidance ... harbor exiting ... harbor entering ... The four modular pipelines and manual controls provide motion control signals which converge into a multiplexer. Each input of the multiplexer corresponds to a FSM's state.

#### 摘录 C

- 出处：第 3-4 页，状态说明，`paper_content.txt` 第 248-278 行
> The FSM has six states ... The initial state is the Virtual Anchor state ... any state of the FSM can change to the Manual Drive state ... The FSM jumps from the initial state to the Exiting state ... switch to the Navigation state if the sonar no longer detects the presence of docks. From the Navigation state, the FSM switches to the Avoid state if an obstacle is detected or to the Enter state if any dockside is detected and the destination is near ... from the Entry state the FSM returns to the initial state.

### 2. 基于原文整理后的自然语言描述

The proposed electric-boat ADS is organized around a supervisory FSM that sits above multiple motion-control pipelines rather than around a single monolithic controller. At the supervision level, the `FSM` receives processed perception signals and HMI commands, then selects through a multiplexer which of the manual, exiting, navigation, obstacle-avoidance or entering pipelines will drive the propulsion controller. The machine has six explicit states: `Virtual Anchor`, `Manual Drive`, `Exiting`, `Navigation`, `Avoid` and `Enter`. Its transition logic forms a mission-level operation chain in which destination entry launches harbor exit, sonar release enables normal navigation, obstacle detection triggers avoidance, dockside detection near the destination triggers entry, and successful completion returns the boat to the virtual-anchor baseline state.

### 3. 逐句溯源

1. 句子 1：The proposed electric-boat ADS is organized around a supervisory FSM that sits above multiple motion-control pipelines rather than around a single monolithic controller.
   对应摘录：A, B
2. 句子 2：At the supervision level, the `FSM` receives processed perception signals and HMI commands, then selects through a multiplexer which of the manual, exiting, navigation, obstacle-avoidance or entering pipelines will drive the propulsion controller.
   对应摘录：B
3. 句子 3：The machine has six explicit states: `Virtual Anchor`, `Manual Drive`, `Exiting`, `Navigation`, `Avoid` and `Enter`.
   对应摘录：C
4. 句子 4：Its transition logic forms a mission-level operation chain in which destination entry launches harbor exit, sonar release enables normal navigation, obstacle detection triggers avoidance, dockside detection near the destination triggers entry, and successful completion returns the boat to the virtual-anchor baseline state.
   对应摘录：A, C

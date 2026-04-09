# A method for autonomous robotic manipulation through exploratory interactions with uncertain environments - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了机器人材料操作任务的 `4` 态主状态机，并在 `Exploration` 与 `Task` 中嵌入 `Fault Detection` 子单元和任务子状态，结构完整且工程语义明确。

## 条目 1: Four-State Exploratory Manipulation Supervisor with Fault-Detection Substates

- 控制对象：自主机器人材料探索与舀取操作的任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个机器人操作任务监督器，按 `Workspace definition -> Exploration -> Materials distribution -> Task` 的顺序组织感知、探索、参数学习和实际舀取任务，并在关键阶段嵌入故障检测子单元。
- 判断：算。对象是真实机器人操作系统，原文给出了状态数、状态名、进入后的动作、任务子状态和故障回退逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-7 页，Section 2.5 `Finite state machine`，`paper_content.txt` 第 419-446 行
> The FSM is formed by four states.
>
> The “Workspace definition” state is responsible of acquiring the knowledge regarding the environment ...
>
> the FSM switches to the “Exploration” state.

#### 摘录 B

- 出处：第 7 页，`Exploration` 与故障检测，`paper_content.txt` 第 457-483 行
> we designed a “Fault Detection” sub-unit, within the “Exploration” state
>
> if the sensed external forces ... experience an abrupt increase, the robot ends its motion and goes back to its homing position.
>
> During the final state, named “Task”, the robot needs to scoop some material and pour it in a pot held by another robot.

#### 摘录 C

- 出处：第 8 页，`Task` 状态与阈值，`paper_content.txt` 第 495-503 行
> kst_max,m = kst_exploration,m * (1 + p)
>
> If, in the “Task” state, this value is exceeded, the “Fault Detection” sub-unit is triggered, and the robot goes back to its homing position.

### 2. 基于原文整理后的自然语言描述

The manipulation framework is governed by a hierarchical task supervisor whose main flow contains four states: `Workspace definition`, `Exploration`, `Materials distribution`, and `Task`. In `Workspace definition`, the robot receives polygon vertices from the visual-perception module and builds the structured representation of the materials present in the workspace. It then enters `Exploration`, where the end-effector probes each material in turn, activates the self-tuning impedance logic when contact is expected, and stores the learned stiffness parameter `kst` for later use. `Materials distribution` assigns peak points to each material, after which the `Task` state executes the actual scooping-and-pouring sequence using the previously learned stiffness values as priors. The controller is hierarchical rather than flat because both `Exploration` and `Task` contain a `Fault Detection` sub-unit that can interrupt execution and send the robot back to its homing position when force trends or the bounded task stiffness `kst_max` indicate a collision or abnormal material change.

### 3. 逐句溯源

1. 句子 1：The manipulation framework is governed by a hierarchical task supervisor whose main flow contains four states: `Workspace definition`, `Exploration`, `Materials distribution`, and `Task`.
   对应摘录：A, B
2. 句子 2：In `Workspace definition`, the robot receives polygon vertices from the visual-perception module and builds the structured representation of the materials present in the workspace.
   对应摘录：A
3. 句子 3：It then enters `Exploration`, where the end-effector probes each material in turn, activates the self-tuning impedance logic when contact is expected, and stores the learned stiffness parameter `kst` for later use.
   对应摘录：A
4. 句子 4：`Materials distribution` assigns peak points to each material, after which the `Task` state executes the actual scooping-and-pouring sequence using the previously learned stiffness values as priors.
   对应摘录：B
5. 句子 5：The controller is hierarchical rather than flat because both `Exploration` and `Task` contain a `Fault Detection` sub-unit that can interrupt execution and send the robot back to its homing position when force trends or the bounded task stiffness `kst_max` indicate a collision or abnormal material change.
   对应摘录：B, C

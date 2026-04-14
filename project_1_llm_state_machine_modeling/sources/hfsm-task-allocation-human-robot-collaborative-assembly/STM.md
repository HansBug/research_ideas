# A Hierarchical Finite-State Machine-Based Task Allocation Framework for Human-Robot Collaborative Assembly Tasks - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把人机协作装配中的任务选择、分配、指令发布和执行组织成 HFSM，并在 crusher-unit 装配案例中给出 28 个任务与并行执行逻辑，是非常扎实的工业 HSM 样本。

## 条目 1: Crusher-unit assembly task-allocation HFSM

- 控制对象：工业自动化与离散制造领域的人机协作装配任务分配监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个 HRC assembly supervisor，用 HFSM 管理 task selection、agent allocation、human instruction 和 robot execution，并在 smoothie machine 的 crusher-unit 装配中决定哪些子任务交给人、哪些交给机器人。
- 判断：算。对象是明确的协作装配控制逻辑而不是单纯优化框架；原文给出了顶层状态、触发信号、子任务状态机、并行关系以及真实装配案例中的任务序列与并行执行效果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> This paper proposes a novel generic task allocation approach based on hierarchical finite-state machines for human-robot assembly tasks. The developed framework decomposes first the main task into sub-tasks modelled as state machines. Based on capabilities considerations, workload, and performance estimations, the task allocator assigns the sub-task to human or robot agent. The algorithm was validated on the assembly of a crusher unit of a smoothie machine using the collaborative Franka Emika Panda robot.

#### 摘录 B

- 出处：第 2-3 页，Section `II` 与 Figure 1/Figure 2 说明
> The states of the higher level of the HFSM, namely the task selector, the task allocator, the communication instructor, and the task executor.
>
> When started the HFSM, the start signal triggers the launching of the assembly task ... Once a new task is found (newtask), the task allocator module is enabled ... If the sub-task is assigned to the human, instructions are provided in textual form in the communication instructor. Otherwise, the task executor controls the robot to perform the required operations. Once the task is performed, task finished is sent back to the task selector ... The assembly finishes when no more tasks (nomore task) are found.
>
> Every task is composed of state machines that represent the sub-tasks ... Each state can be connected to other states in series or in parallel. The states of parallel tasks are combined using vertical forks.

#### 摘录 C

- 出处：第 6-7 页，Section `III` 与 `IV Experimental Validation`
> The assembly task consists in assembling the crusher unit of a smoothie machine by both the human and the robot.
>
> The crusher unit assembly consists of 28 tasks ... it is possible to devise the task selector structure ... Thanks to the hierarchical state machine, it is possible to run parallel tasks where both the robot and the human perform the required operations. Thanks to the performance module, the total assembly time is improved by 31% ... and 34% ...

### 2. 基于原文整理后的自然语言描述

The proposed controller is a hierarchical task-allocation supervisor for human-robot collaborative assembly rather than a flat one-step allocator. Its top level cycles through `task selector`, `task allocator`, `communication instructor`, and `task executor`: `start` activates task selection, `newtask` invokes allocation, human-assigned tasks are forwarded as textual instructions, robot-assigned tasks are executed by the robot module, and `task finished` returns control to the selector until `nomore task` terminates the job. Beneath this upper loop, each assembly task is itself represented as a finite-state machine of sub-tasks, and those sub-task states can be arranged in series or in parallel through vertical forks. The framework is not only schematic, because it is instantiated on a crusher-unit assembly of a smoothie machine where the task selector is derived from a 28-task sequence and the human and robot can execute parallel branches. This yields a concrete industrial HSM in which layered task decomposition and concurrent branch execution are first-class control semantics.

### 3. 逐句溯源

1. 句子 1：The proposed controller is a hierarchical task-allocation supervisor for human-robot collaborative assembly rather than a flat one-step allocator.
   对应摘录：A, B
2. 句子 2：Its top level cycles through `task selector`, `task allocator`, `communication instructor`, and `task executor`: `start` activates task selection, `newtask` invokes allocation, human-assigned tasks are forwarded as textual instructions, robot-assigned tasks are executed by the robot module, and `task finished` returns control to the selector until `nomore task` terminates the job.
   对应摘录：B
3. 句子 3：Beneath this upper loop, each assembly task is itself represented as a finite-state machine of sub-tasks, and those sub-task states can be arranged in series or in parallel through vertical forks.
   对应摘录：A, B
4. 句子 4：The framework is not only schematic, because it is instantiated on a crusher-unit assembly of a smoothie machine where the task selector is derived from a 28-task sequence and the human and robot can execute parallel branches.
   对应摘录：A, C
5. 句子 5：This yields a concrete industrial HSM in which layered task decomposition and concurrent branch execution are first-class control semantics.
   对应摘录：A, B, C

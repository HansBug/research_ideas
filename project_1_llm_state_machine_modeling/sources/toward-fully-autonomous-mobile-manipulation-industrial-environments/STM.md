# Toward fully autonomous mobile manipulation for industrial environments - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把工业 fetch-and-carry mobile manipulation 的 flow control 明确写成 hierarchical state machine，并给出 `goToWorkstation / pickObjectFrom / placeObjectOn` 三个高层任务状态机。

## 条目 1: Hierarchical fetch-and-carry mobile-manipulation flow controller

- 控制对象：工业自动化与移动操作领域的取放-搬运层次流控控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向工业 fetch-and-carry 任务的 mobile manipulator flow control system，用分层 state machine 和 `SMACH` 组织导航、抓取和放置流程。
- 判断：算。对象是实际工业移动操作系统控制链，不是纯方法讨论；原文明确说明为何采用 hierarchical flow control，以及高层任务状态机 `goToWorkstation / pickObjectFrom / placeObjectOn` 如何串成实际任务。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，行 1-14
> This work presents a concept for autonomous mobile manipulation in industrial environments.
> ... a modular software concept which is handled and organized by a hierarchical flow control depending on the given task and environmental requirements.
> The presented concept ... is implemented exemplary for industrial manipulation tasks and proven by real-world application in a water pump production site.

#### 摘录 B

- 出处：第 7-8 页，Section `Flow control`，行 544-556
> Therefore, a concept similar to a state machine is applied in this layer.
> Each call of a module functionality can be abstracted as state of the flow.
> ... a hierarchical structure is used. This means every state of the state machine can be a state machine itself ...
> ... also a data flow between the different states is possible. For some tasks also, parallel execution of states is necessary.
> For the implementation of this flow control state machine, the SMACH tool available in the ROS framework is used.

#### 摘录 C

- 出处：第 12 页，Section `Task control`，行 922-937
> knowledge is encapsulated into state machines ...
> For pick and place operations, the following high-level state machines are used:
> goToWorkstation(workstation),
> pickObjectFrom(object_to_pick, object_to_pick_from), and
> placeObjectOn(object_to_place, object_to_place_on).
> By sequencing these high-level modules, an unskilled worker could program new tasks for the robot within the fetch and carry domain.

#### 摘录 D

- 出处：第 18 页，Section `Conclusions`，行 1393-1396
> ... modules with a hierarchical flow control system leads to a system which can be set up by a worker and is able to act comparably to a human worker in the fetch and carry domain.

### 2. 基于原文整理后的自然语言描述

The industrial mobile manipulator is controlled by a hierarchical flow-control layer that explicitly treats module invocations as states and uses nested state machines to orchestrate complex fetch-and-carry tasks. In that layer, a state can itself be another state machine, data can flow between states, and some subtasks are allowed to execute in parallel, which is why the implementation uses ROS `SMACH` rather than a flat sequential controller. For task execution, the paper identifies three top-level reusable state machines: `goToWorkstation`, `pickObjectFrom`, and `placeObjectOn`, and larger industrial jobs are formed simply by sequencing those modules. This arrangement shifts robot-specific complexity into the lower hierarchy while allowing an unskilled worker to configure new fetch-and-carry tasks during setup. The resulting controller is therefore a genuine HSM-style industrial supervisor that coordinates navigation, perception, grasping, and placement as reusable task states rather than as one-off scripts.

### 3. 逐句溯源

1. 句子 1：The industrial mobile manipulator is controlled by a hierarchical flow-control layer that explicitly treats module invocations as states and uses nested state machines to orchestrate complex fetch-and-carry tasks.
   对应摘录：A, B
2. 句子 2：In that layer, a state can itself be another state machine, data can flow between states, and some subtasks are allowed to execute in parallel, which is why the implementation uses ROS `SMACH` rather than a flat sequential controller.
   对应摘录：B
3. 句子 3：For task execution, the paper identifies three top-level reusable state machines: `goToWorkstation`, `pickObjectFrom`, and `placeObjectOn`, and larger industrial jobs are formed simply by sequencing those modules.
   对应摘录：C
4. 句子 4：This arrangement shifts robot-specific complexity into the lower hierarchy while allowing an unskilled worker to configure new fetch-and-carry tasks during setup.
   对应摘录：A, C, D
5. 句子 5：The resulting controller is therefore a genuine HSM-style industrial supervisor that coordinates navigation, perception, grasping, and placement as reusable task states rather than as one-off scripts.
   对应摘录：A, B, C, D

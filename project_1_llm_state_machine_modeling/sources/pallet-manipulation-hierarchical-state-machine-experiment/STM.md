# Robust Behavior and Perception Using Hierarchical State Machines: A Pallet Manipulation Experiment - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把移动机器人托盘搬运任务组织成带宏状态、内层子状态和失败回退箭头的层次状态机，并明确写出识别、姿态精化与取货链。

## 条目 1: Pallet Delivery Hierarchical Perception-Manipulation Supervisor

- 控制对象：通用控制与机器人任务领域的托盘搬运移动机器人分层监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于移动机器人托盘定位、接近、姿态精化和叉取搬运的高层行为控制器，外层按任务阶段推进，失败时可回退到前序阶段重试。
- 判断：算。对象是真实移动机器人控制系统，而不是单独的视觉算法；原文明确给出顺序子任务、失败回退原则、六个宏状态及其内层子状态，以及 `recognize/reject -> refine pose -> final approach/pick` 的连续控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Section `III. Sequential Task Design`，行 145-200
> Robust manipulation by mobile robots requires a careful design of a sequence of states and transitions ... Safe error recovery is a very desirable feature ... In case of errors, a good option is to start over from a previous stage, even going back to the main plan if it is necessary. ... The task of pallet delivering is decomposed in a list of subtasks: (1) Gather context information. (2) Search for a target object candidate. (3) Approach to gain a favourable point of view. (4) Verify the target and gather initial information. (5) Refine object information. (6) Approach and pick/grasp the object. (7) Manipulate the object. ... these error conditions have to be managed by transitions to former or halt exception states.

#### 摘录 B

- 出处：第 4-5 页，Section `VI. A State Machine for Pallet Manipulation` 与 Figure 4，行 363-394
> The remaining of this section chronologically describes the states that the component (the state machine describing its behavior) would go through ... Error-triggered transitions are specified within each state description. ... Fig. 4: Hierarchical state machine used in the experiment. There are six macro states and the Standby and Final destination. Each macro state includes inner states representing with finer detail the structure of each stage. Note the arrows pointing back to former states, signalling failure situations that prevent the normal working of the plan.

#### 摘录 C

- 出处：第 7 页，Section `D-F`，行 531-587
> When the robot enters the “recognize or reject” state, a rapid test to accept or discard the candidate object is run. ... if the classifier returns a positive answer, the object is recognized as a pallet and the subtask proceeds. ... When entering this state, the robot believes that it is taking a close look at a pallet. However, its pose estimation being still imprecise, he decides to refine the estimated pose of the pallet. ... If this test succeeds the procedure is iterated varying the position and orientation of the pallet in a small range ... Once a good estimate of the pose is obtained, this last state moves the robot towards the pallet ... Four infrared sensors placed in the forklift arms ... send a signal to the component when they are occluded by the pallet. This information triggers the lifting behavior ...

### 2. 基于原文整理后的自然语言描述

The pallet manipulation robot is supervised by a hierarchical state machine that decomposes the delivery task into ordered behavioral stages rather than treating perception and manipulation as a single monolithic routine. At the top level, the plan progresses through context gathering, target search, viewpoint approach, target verification, pose refinement, grasp approach, and pallet manipulation, and the design explicitly allows failures to send execution back to previous stages or halt states. The paper also states that the implementation is not a flat FSM: Figure 4 contains six macro states plus `Standby` and `Final destination`, and each macro state contains inner states that refine the behavior of that stage. Inside the mid-to-late pipeline, the `recognize or reject` state first classifies the visual candidate and estimates pallet orientation, the `refine pose` state performs iterative model-based pose optimization with a rendered pallet model, and the final approach state drives the robot into the pallet. Pickup completion is guarded by fork-mounted infrared sensors, whose occlusion event triggers the lifting behavior once the forks have entered the pallet openings.

### 3. 逐句溯源

1. 句子 1：The pallet manipulation robot is supervised by a hierarchical state machine that decomposes the delivery task into ordered behavioral stages rather than treating perception and manipulation as a single monolithic routine.
   对应摘录：A, B
2. 句子 2：At the top level, the plan progresses through context gathering, target search, viewpoint approach, target verification, pose refinement, grasp approach, and pallet manipulation, and the design explicitly allows failures to send execution back to previous stages or halt states.
   对应摘录：A
3. 句子 3：The paper also states that the implementation is not a flat FSM: Figure 4 contains six macro states plus `Standby` and `Final destination`, and each macro state contains inner states that refine the behavior of that stage.
   对应摘录：B
4. 句子 4：Inside the mid-to-late pipeline, the `recognize or reject` state first classifies the visual candidate and estimates pallet orientation, the `refine pose` state performs iterative model-based pose optimization with a rendered pallet model, and the final approach state drives the robot into the pallet.
   对应摘录：C
5. 句子 5：Pickup completion is guarded by fork-mounted infrared sensors, whose occlusion event triggers the lifting behavior once the forks have entered the pallet openings.
   对应摘录：C

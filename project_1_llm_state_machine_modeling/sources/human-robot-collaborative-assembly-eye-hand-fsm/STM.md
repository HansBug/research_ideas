# Human-Robot Collaborative Assembly Based on Eye-Hand and a Finite State Machine in a Virtual Environment - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把眼手协同装配的交互控制拆成 `instruction / mapping` 两层模式和 `Recognize / Indication / Capture / Mapping` 运行链，并补出 `G1-G4` 手势触发与 PRM 自动抓取-人工精调的分工，可作为完整的 HRC supervisor 样本入账。

## 条目 1: Eye-Hand Instruction-and-Mapping Assembly Supervisor

- 控制对象：工业自动化与离散制造领域的眼手协同装配人机协作监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个虚拟装配环境中的 human-robot collaboration controller，用眼动和手势在自动抓取模式与人工映射装配模式之间切换。
- 判断：算。对象是明确的协作装配控制器，而不是单纯手势识别算法；原文给出了 FSM 的模式划分、阶段划分、`G1-G4` 触发关系、PRM 负责的自动段和 mapping 负责的人工精调段。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> Based on eye-hand and finite state machines, a collaborative assembly method is proposed. The method determines the human’s intention by collecting posture and eye data, which can control a robot to grasp an object, move it, and perform co-assembly. The robot’s automatic path planning is based on a probabilistic roadmap planner.

#### 摘录 B

- 出处：第 2-3 页，Highlights / Section `2 Experimental Setup`
> A model based on eye-hand cooperation with an FSM to change the robot’s state is proposed. Based on the classification of previous gestures, the interaction mode is roughly divided into “instruction” and “mapping” modes. The robot deals with the fixed part based on PRM, while the human deals with the flexible part.
>
> Commands are divided into instructions and mapping. The instruction combined with the PRM algorithm makes the robot run automatically. The mapping enables the robot to follow the users. HRC is divided into three stages: indication, capture, and mapping.

#### 摘录 C

- 出处：第 9 页，Section `2.4 Finite State Machine for Human-Robot Collaboration`
> Gesture G1 was used to indicate an object by calculating the index finger’s ray position and orientation. The indication state is that the robot needs to grasp the object and put it at the target position according to G1 + E1 (gesture and eye commands). Gesture G2 was used to switch the robot mode from the indication state to the mapping state. The mapping state maps the hand space state to the end of the robot and directly commands the robot to move. Gesture G3 was used to end the mapping state. Gesture G4 was used to change the gripper to relax.

#### 摘录 D

- 出处：第 13-14 页，Section `4.1 Experimental State Change`
> According to the experimental process, there were ... four states in Group B (eye-hand states 1-4 = Recognize, Indication, Capture, and Mapping).
>
> In Group B, the stage of selecting the object and indicating the target position took t0. In the grabbing stage, the robot took t1 to capture the object and move it. Mapping assembly took t2.

### 2. 基于原文整理后的自然语言描述

The collaborative-assembly controller is organized as a hierarchical eye-hand supervisor whose upper mode split is `instruction` versus `mapping`. In `instruction`, the user provides coarse intent by the eye-hand combination and the robot uses PRM-based automatic planning to grasp the selected object and move it toward the designated position; in `mapping`, the hand-space state is directly mapped to the robot end effector for local assembly adjustment. Operationally, the interaction sequence runs through `Recognize`, `Indication`, `Capture`, and `Mapping`, so the system first recognizes the user and gesture, then accepts an object-and-target indication, then performs automatic capture and transfer, and finally lets the human finish the assembly with direct mapped motion. The transition logic is explicit: `G1 + E1` issues the indication command, `G2` switches from indication to mapping after the robot reaches the placement area, `G3` ends mapping, and `G4` relaxes the gripper. This makes the FSM a layered HRC supervisor in which the robot handles the repeatable coarse transport subtask while the human only takes over the flexible fine-placement subtask.

### 3. 逐句溯源

1. 句子 1：The collaborative-assembly controller is organized as a hierarchical eye-hand supervisor whose upper mode split is `instruction` versus `mapping`.
   对应摘录：A, B
2. 句子 2：In `instruction`, the user provides coarse intent by the eye-hand combination and the robot uses PRM-based automatic planning to grasp the selected object and move it toward the designated position; in `mapping`, the hand-space state is directly mapped to the robot end effector for local assembly adjustment.
   对应摘录：A, B, C
3. 句子 3：Operationally, the interaction sequence runs through `Recognize`, `Indication`, `Capture`, and `Mapping`, so the system first recognizes the user and gesture, then accepts an object-and-target indication, then performs automatic capture and transfer, and finally lets the human finish the assembly with direct mapped motion.
   对应摘录：B, D
4. 句子 4：The transition logic is explicit: `G1 + E1` issues the indication command, `G2` switches from indication to mapping after the robot reaches the placement area, `G3` ends mapping, and `G4` relaxes the gripper.
   对应摘录：C
5. 句子 5：This makes the FSM a layered HRC supervisor in which the robot handles the repeatable coarse transport subtask while the human only takes over the flexible fine-placement subtask.
   对应摘录：A, B, D

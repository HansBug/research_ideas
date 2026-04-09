# A Floor Tiling Robotic System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把建筑施工场景中的铺砖机械臂控制流程拆成 `Initialization / Idle / Tile Pickup / Tile Placement / Error Handling` 五态 FSM，并给出图像驱动触发、执行动作与错误停机逻辑。

## 条目 1: Tile-Pickup and Placement Arm FSM

- 控制对象：地砖铺设机器人中负责抓取、对位、放置与异常停机的机械臂控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向建筑地砖铺设任务的机器人机械臂高层控制器，用 FSM 管理系统初始化、待命、取砖、放砖与异常处理。
- 判断：算。对象是实际施工机器人控制算法，原文明确给出状态集合、图像处理结果到用户命令的触发关系、各状态内的执行动作，以及传感器/通信异常时的安全停机与等待链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，Section 3.4 Floor Tiling Robot Control Algorithm Design，行 242-282
> In conjunction with the control algorithm, a finite state machine (FSM) regulates the motion of the robotic arm. The FSM establishes a number of states that correspond to different phases of the tile installation procedure, such as idle, initialization, tile collection, and tile placement. Transitions between states are initiated in response to user commands, while user commands will be determined based on the image processing result. The FSM can be sectioned into several states: `Initialization State`, during which the system calibrates servo motors, initializes sensor readings, and makes operational preparations; `Idle State`, in which the robotic arm awaits control system instructions; `Tile Pickup State`, in which the arm approaches the specified tile, activates the suction cup mechanism, and firmly grasps the tile; `Tile Placement State`, in which the arm locates the desired position on the floor, aligns it with adjacent tiles, and releases it with deliberate and controlled motions; and `Error Handling State`, which accommodates unforeseen issues such as sensor failures and communication errors, ceases operations in a secure manner, informs the control system, and waits for additional instructions.

#### 摘录 B

- 出处：第 4-5 页，Section 3.4 / Section 4.1 Quantitative Metrics，行 288-297, 366-400
> The control algorithm has been intentionally developed to be versatile and adjustable. To allow for the inclusion of uncertainties introduced during calibration and variations in tile positions, tolerance thresholds are incorporated. Furthermore, the implementation of adaptive strategies, including dynamic path planning and obstacle avoidance, serves to augment the system's capacity to adjust to environmental fluctuations and unanticipated impediments. Every tile's paving time is recorded during the experiment, beginning when the Floor Tiling Robot is in the finite state machine's `IDLE` state. The experiment was repeated 20 times. The average installation time per tile is approximately 38.87 seconds, 70% of tiles were accurately placed in their correct position, and six tiles exhibited defective angles ranging from -5° to 7°.

### 2. 基于原文整理后的自然语言描述

The floor-tiling robot controls its arm through a five-state FSM composed of `Initialization`, `Idle`, `Tile Pickup`, `Tile Placement`, and `Error Handling`, and the state transitions are triggered by user commands derived from the image-processing pipeline. At startup, the arm calibrates servos and sensors in `Initialization`, waits for the next assignment in `Idle`, moves to the specified tile and activates the vacuum suction cup in `Tile Pickup`, and then aligns the tile with adjacent tiles and releases it in `Tile Placement`. Sensor failures and communication faults send the controller into `Error Handling`, where the system stops safely, reports the issue, and waits for further instructions instead of continuing placement blindly. The same FSM is evaluated from the `Idle` state in 20 tiling trials, and the paper reports tolerance thresholds, adaptive path planning and obstacle avoidance, an average placement time of about 38.87 seconds per tile, and a 70% correct-placement rate.

### 3. 逐句溯源

1. 句子 1：The floor-tiling robot controls its arm through a five-state FSM composed of `Initialization`, `Idle`, `Tile Pickup`, `Tile Placement`, and `Error Handling`, and the state transitions are triggered by user commands derived from the image-processing pipeline.
   对应摘录：A
2. 句子 2：At startup, the arm calibrates servos and sensors in `Initialization`, waits for the next assignment in `Idle`, moves to the specified tile and activates the vacuum suction cup in `Tile Pickup`, and then aligns the tile with adjacent tiles and releases it in `Tile Placement`.
   对应摘录：A
3. 句子 3：Sensor failures and communication faults send the controller into `Error Handling`, where the system stops safely, reports the issue, and waits for further instructions instead of continuing placement blindly.
   对应摘录：A
4. 句子 4：The same FSM is evaluated from the `Idle` state in 20 tiling trials, and the paper reports tolerance thresholds, adaptive path planning and obstacle avoidance, an average placement time of about 38.87 seconds per tile, and a 70% correct-placement rate.
   对应摘录：B

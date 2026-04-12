# Research on 3*3 Stereo Garage Control System Based on PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文围绕 `3*3` 七车位升降横移车库，给出 S7-200 PLC、光电传感器、上位机按钮、升降时间 `17` 秒和目标车位调度过程，能整理为资源受限的车位存取 EFSM。

## 条目 1: 3x3 stereo-garage lift-traverse access controller

- 控制对象：智慧停车与车位管理领域的 `3x3` 立体车库升降横移存取控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🧰 清洗后保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用于三层七车位升降横移式立体车库的 PLC 控制器，通过上位机按钮、光电传感器和升降横移动作完成车辆存取。
- 判断：算。虽然论文没有直接画传统状态图，但它给出了车库结构、传感器输入、PLC 控制边界、车辆位置调度和 `17` 秒升降时间，足以支撑资源状态与动作阶段的 EFSM 描述。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> In this paper, the storage and access of 7 parking Spaces in 3*3 stereo garages are designed. This paper introduces the structure and working principle of the garage, expounds the structure and components of the garage control system, and designs and analyzes the control circuit of the garage motor.

#### 摘录 B

- 出处：第 3 页，Overall design scheme of three-dimensional garage
> In the three-dimensional garage, the lifting and moving control system is designed. Siemens S7-200 PLC is used as the three-dimensional garage control system, and its programming software is used for lifting and moving, debugging and running.

#### 摘录 C

- 出处：第 3 页，Lifting mechanism and selection
> According to the actual requirements of garage application, the vehicle lifting time should not be too slow, and it needs to meet the requirements that the vehicle lifting time is less than seconds. The lifting time t of the designed vehicle in this garage is 17 seconds.

#### 摘录 D

- 出处：第 6 页，Hardware design of stereo garage
> The system is divided into two levels. One is the human-computer interaction control subsystem with single-chip microcomputer as the control core. It is responsible for the data acquisition and processing of single chip microcomputer. The system is also responsible for garage control, monitoring the real-time status of the garage at any time, including recording vehicle information, etc; the other is the field implementation system to control vehicle access, mainly including detection, drive equipment and PLC control subsystem.

#### 摘录 E

- 出处：第 6 页，Hardware design of stereo garage
> The detection equipment adopts high-performance photoelectric sensor, which can accurately detect the moving position and parking status of the vehicle. The sensor sends the detected data to PLC as the control input.

#### 摘录 F

- 出处：第 6-7 页，Specific algorithm application scheduling vehicle
> In the 3 * 3three-dimensional garage, the initial state of vehicles in the garage is as shown in the figure. The garage is fully loaded with 7 vehicles. Among them, vehicle 5 is the target vehicle for pick-up, which is located on the left most side of the third floor. Pick up vehicle 5. According to the specific parking space scheduling algorithm, the optimal path scheduling is carried out, and the mobile route is shown in Figure 4-6.

### 2. 基于原文整理后的自然语言描述

The `3x3` stereo-garage controller manages seven occupied parking spaces in a lift-and-traverse layout. A user or administrator issues a storage or retrieval command from the human-machine side, and the control system records the vehicle information while the field PLC subsystem controls detection, drive equipment, lifting, and traverse actions. Photoelectric sensors report each carrier plate's moving position and vehicle parking status to the PLC, so a movement is only continued when the expected position or occupancy condition is confirmed. For retrieval, such as the paper's example of picking up vehicle 5 from the left side of the third floor in a fully loaded garage, the scheduling algorithm computes an optimal path, then the PLC executes a sequence of lift or traverse moves under the slot-occupancy constraints. The lift stage uses the designed `17` second lifting time as a local engineering timing constraint, and the retrieval cycle completes when the target vehicle reaches the exit safely and stably.

### 3. 逐句溯源

1. 句子 1：The `3x3` stereo-garage controller manages seven occupied parking spaces in a lift-and-traverse layout.
   对应摘录：A, F
2. 句子 2：A user or administrator issues a storage or retrieval command from the human-machine side, and the control system records the vehicle information while the field PLC subsystem controls detection, drive equipment, lifting, and traverse actions.
   对应摘录：B, D
3. 句子 3：Photoelectric sensors report each carrier plate's moving position and vehicle parking status to the PLC, so a movement is only continued when the expected position or occupancy condition is confirmed.
   对应摘录：E
4. 句子 4：For retrieval, such as the paper's example of picking up vehicle 5 from the left side of the third floor in a fully loaded garage, the scheduling algorithm computes an optimal path, then the PLC executes a sequence of lift or traverse moves under the slot-occupancy constraints.
   对应摘录：F
5. 句子 5：The lift stage uses the designed `17` second lifting time as a local engineering timing constraint, and the retrieval cycle completes when the target vehicle reaches the exit safely and stably.
   对应摘录：C, F

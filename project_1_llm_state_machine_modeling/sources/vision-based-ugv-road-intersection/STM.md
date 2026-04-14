# A Vision-Based System for a UGV to Handle a Road Intersection - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口车辆优先权判断写成 `No Vehicle Waiting / Arriving / Waiting / Passing` 四态 FSM，并给出 15 帧静止判定和 2 s 清空等待，足以形成紧凑但完整的道路交通监督样本。

## 条目 1: Four-State Right-of-Way Supervisor for UGV Intersection Crossing

- 控制对象：UGV 在四向 stop-sign 路口的道路优先权判断与通过监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是自动驾驶 UGV 在四向路口的交通过车监督 FSM，用来根据三路来车的视觉跟踪结果判定谁有优先权、何时允许 autopilot 通过。
- 判断：算。对象是实际 UGV 的路口监督控制逻辑，不是单纯检测算法；原文明确给出 4 个状态、进入/退出条件、阈值和通过等待时间。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> "four possible states"

#### 摘录 B

- 出处：第 5 页，`Finite-State-Machine Intersection Model`
> "about 15 frames"

#### 摘录 C

- 出处：第 5 页，`Finite-State-Machine Intersection Model`
> "waits for two seconds"

### 2. 基于原文整理后的自然语言描述

The intersection supervisor models the traffic seen in each camera view with four discrete states: `No Vehicle Waiting`, `Arriving`, `Waiting`, and `Passing`. When a new vehicle is detected, the model moves from `No Vehicle Waiting` to `Arriving`; from there, the vehicle can become `Waiting` if its velocity, acceleration, and scale change all drop below thresholds, or become `Passing` if it crosses a spatial threshold in the image. To prevent spurious transitions, the vehicle must remain still for about 15 frames, or roughly half a second, before the controller accepts the `Waiting` state. A vehicle in `Passing` can still transition back to `Waiting` if it is disturbed while crossing, and once it reaches the edge of the frame the machine returns to `No Vehicle`. At the multi-view decision layer, the UGV yields if another vehicle is already `Waiting` when it arrives or if any vehicle is `Passing`; after the finite-state machine stops indicating `Passing`, the autopilot still waits for two seconds before crossing, which adds a simple but explicit temporal safety margin.

### 3. 逐句溯源

1. 句子 1：The intersection supervisor models the traffic seen in each camera view with four discrete states: `No Vehicle Waiting`, `Arriving`, `Waiting`, and `Passing`.
   对应摘录：A；`paper_content.txt` 第 160-167 行。
2. 句子 2：When a new vehicle is detected, the model moves from `No Vehicle Waiting` to `Arriving`; from there, the vehicle can become `Waiting` if its velocity, acceleration, and scale change all drop below thresholds, or become `Passing` if it crosses a spatial threshold in the image.
   对应摘录：A；`paper_content.txt` 第 170-189 行。
3. 句子 3：To prevent spurious transitions, the vehicle must remain still for about 15 frames, or roughly half a second, before the controller accepts the `Waiting` state.
   对应摘录：B；`paper_content.txt` 第 173-177 行。
4. 句子 4：A vehicle in `Passing` can still transition back to `Waiting` if it is disturbed while crossing, and once it reaches the edge of the frame the machine returns to `No Vehicle`.
   对应摘录：A；`paper_content.txt` 第 188-192 行。
5. 句子 5：At the multi-view decision layer, the UGV yields if another vehicle is already `Waiting` when it arrives or if any vehicle is `Passing`; after the finite-state machine stops indicating `Passing`, the autopilot still waits for two seconds before crossing, which adds a simple but explicit temporal safety margin.
   对应摘录：C；`paper_content.txt` 第 197-201 行。

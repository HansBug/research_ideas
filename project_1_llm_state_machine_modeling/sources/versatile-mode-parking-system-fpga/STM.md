# A Real Time Algorithm for Versatile Mode Parking System and Its Implementation on FPGA Board - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四种停车模式的识别条件、传感器距离比较、模式选择 guard 和执行条件写成了明确的 flowchart，可直接作为停车控制领域的 `EFSM + T0` 双 A 样本。

## 条目 1: Four-mode parking-mode selector and path-generation controller

- 控制对象：智慧停车与车位管理领域的四模式停车位识别与路径生成控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个在 FPGA 上实现的 Autonomous and Versatile mode Parking System (AVPS)，它依据距离量 `D1-D5`、角度 `α`、坡度存在性和角点检测结果，在 parallel、perpendicular、head-in angled、head-out angled 四种停车模式之间切换。
- 判断：算。对象是实际停车控制器而不是纯路径优化背景；原文明确给出了模式集合、输入观测、判断顺序、阈值比较和最终执行动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 35-48 行
> This paper presents the design and development of a technique for an Autonomous and Versatile mode Parking System (AVPS) that combines a various number of parking modes. ... This research aims at developing a parking system that automatically chooses a parking lot starting from four parking modes. ... A variety of candidate modes could be generated using one developed real time VHDL ... algorithm ... The AVPS is able to find and recognize in advance which parking mode to select.

#### 摘录 B

- 出处：第 7-8 页，`2.2. Proposed Algorithm` 与 Figure 6 说明，`paper_content.txt` 第 247-295 行
> Figure 6 shows the generic scheme (parking algorithm flowchart) of functional building blocks of the proposed Autonomous and Versatile mode Parking System (AVPS).
>
> (a) Detection of free parking space.
> (b) Measurement of distance D1 corresponding to the free parking place.
> ...
> (f) Testing if there is an existing slope? If yes, the proposed AVPS recognizes that the mode is head-in angled mode parking or head-out angled mode. If there is no slope, the same proposed AVPS recognizes intelligently that the configuration ... is a parallel parking mode or perpendicular parking mode.
> ...
> (h) If D2 = K * cos α, the mode is the head-out angled parking mode ... the algorithm tests if D1 ≥ D5 ... If D2 ≠ K * cos α, the appropriate mode is the head-in angled parking mode ...
> ...
> (i) If there is no slope ... If D2 = K ... If D1 ≥ D3, the appropriate mode is “parallel parking” ... If D2 ≠ K ... If D1 ≥ D4, the appropriate mode is “perpendicular parking” ...
> ...
> (k) Finally, the mobile robot executes the selected parking mode.

#### 摘录 C

- 出处：第 8 页，`3.1. With Description in Simplorer Environment`，`paper_content.txt` 第 303-307 行
> Sensor 2 and sensor 3 provide information to determinate the parking mode.
>
> Corner 1 and corner 2 detection depends on the selected mode.
>
> The possible existence of a slope is important to calculate the value of the angle α.
>
> Finally, the reaction of DC motors and the stepper motor.

### 2. 基于原文整理后的自然语言描述

The retained controller is an FPGA-implemented AVPS that first detects a free parking space, measures the free-slot distance `D1`, and then keeps updating geometric observations such as corner detections, travelled distance `D2`, and slope angle `α` before committing to a parking maneuver. Its core decision logic branches on whether a slope exists: if a slope is present, the controller compares `D2` against `K * cos α` to distinguish `head-out angled` from `head-in angled` parking and then checks whether `D1 ≥ D5` before allowing execution. If no slope is present, the controller instead uses `D2 = K` and the capacity tests `D1 ≥ D3` or `D1 ≥ D4` to distinguish `parallel parking` from `perpendicular parking`, otherwise it keeps moving forward until enough space is found. In all four branches, the selected mode is guarded by a minimum-space check on `D1`, so mode selection and motion execution are both driven by the same extended geometric state. After the mode has been selected, the controller generates the corresponding geometric path and drives the DC motors and stepper motor to execute the chosen maneuver.

### 3. 逐句溯源

1. 句子 1：The retained controller is an FPGA-implemented AVPS that first detects a free parking space, measures the free-slot distance `D1`, and then keeps updating geometric observations such as corner detections, travelled distance `D2`, and slope angle `α` before committing to a parking maneuver.
   对应摘录：A, B, C
2. 句子 2：Its core decision logic branches on whether a slope exists: if a slope is present, the controller compares `D2` against `K * cos α` to distinguish `head-out angled` from `head-in angled` parking and then checks whether `D1 ≥ D5` before allowing execution.
   对应摘录：B
3. 句子 3：If no slope is present, the controller instead uses `D2 = K` and the capacity tests `D1 ≥ D3` or `D1 ≥ D4` to distinguish `parallel parking` from `perpendicular parking`, otherwise it keeps moving forward until enough space is found.
   对应摘录：B
4. 句子 4：In all four branches, the selected mode is guarded by a minimum-space check on `D1`, so mode selection and motion execution are both driven by the same extended geometric state.
   对应摘录：B
5. 句子 5：After the mode has been selected, the controller generates the corresponding geometric path and drives the DC motors and stepper motor to execute the chosen maneuver.
   对应摘录：B, C

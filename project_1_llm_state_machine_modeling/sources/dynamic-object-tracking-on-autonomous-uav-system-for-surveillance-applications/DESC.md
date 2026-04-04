# 面向监视应用的自主无人机动态目标跟踪系统 / Dynamic Object Tracking on Autonomous UAV System for Surveillance Applications

## 基本信息

- **标题**：Dynamic Object Tracking on Autonomous UAV System for Surveillance Applications
- **中文标题**：面向监视应用的自主无人机动态目标跟踪系统
- **作者**：Li-Yu Lo，Chi Hao Yiu，Yu Tang，An-Shik Yang，Boyang Li，Chih-Yung Wen
- **单位**：
  - The Hong Kong Polytechnic University
  - National Taipei University of Technology
- **发表**：Sensors，2021
- **DOI**：10.3390/s21237888
- **链接**：https://doi.org/10.3390/s21237888

### 代码/仓库获取方式

- 原文摘要明确写到 *The source code is released to the research community*。
- 但当前 PDF 正文前部未给出稳定仓库 URL，因此这里只能确认“原文声明已公开代码”，不能给出仓库入口。

### 数据集/案例获取方式

- 原文未提供单独数据集下载条目。
- 论文基于自研 surveillance UAV 系统给出了 finite-state maneuver logic、relative-position based reactions 和 fail-safe lost-target chain，可直接作为单案例 source paper 使用。

## 简报

这篇论文解决的是**无人机在监视任务中如何根据目标相对位置执行搜索、悬停、横摆、升降、前后跟随以及失目标后的安全降落**的问题。输入是 RGB 图像、深度、相对目标运动趋势、安全距离与失目标帧数，方法是设计两个并行状态机来分别处理 camera FoV 姿态/高度和 UAV 与目标的相对距离，输出是离散 waypoint/maneuver 序列。

- **输入**：camera image、depth estimate、relative target motion、`Rsafe / Rsur`、lost-target duration。
- **方法**：目标检测与跟踪之上的 parallel finite-state maneuver controller。
- **输出**：`search / hover / sway / climb / descend / forward / backward / lost-and-await / land` 控制链。
- **一句话评价**：这是很强的 `EFSM + T1` 监视任务样本，parallel FSM、safe-radius guard 和 lost-target fail-safe 都写得很清楚。

## 控制系统与状态机证据

### 控制对象

论文对象是一个自主 surveillance UAV 系统。控制器根据目标在相机坐标系中的相对位置与动态趋势，决定无人机该搜索、悬停、横摆、升降、前后调整，还是进入失目标等待与降落模式。

### 状态机组织方式

原文明确说明系统有**两个并行状态机**：

1. 一个处理 camera FoV 的姿态与高度
2. 一个处理 UAV 与目标之间的相对距离

并列出的核心状态包括：

1. `Initialization`
2. `Sway and Search`
3. `Track and Hover`
4. `Track and Sway`
5. `Track and Climb or Descend`
6. `Track and Forward or Backward`
7. `Lost and Await`
8. `Land`

### 关键控制链

论文把主链写得很完整：

- 初始化后无人机起飞到固定高度，再进入 `Sway and Search` 做 360 度搜索。
- 锁定目标后进入 `Track and Hover`，先判断目标是否静止。
- 如果目标在画面中横向移动，则进入 `Track and Sway`；如果目标高低变化，则进入 `Track and Climb or Descend`。
- 如果目标距离超出 `Rsafe` 与 `Rsur` 约束，则进入 `Track and Forward or Backward` 调整距离。
- 如果目标连续丢失，则进入 `Lost and Await`，等待时间超过阈值后再 `Land` 并返航降落。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它是**真实 UAV 监视任务的高层 maneuver controller**，不是只做感知性能比较。
- 论文已经把 parallel FSM、relative-position guards 和 lost-target fail-safe 讲清楚，适合直接转写为自然语言状态机样本。
- 该类“目标跟踪监督器”在当前文库里仍不多，能补充视觉驱动任务控制案例。

### 可直接借鉴之处

- 可以直接借鉴“两个并行状态机分别处理姿态/高度与相对距离”的结构表达。
- 可以直接借鉴 `Rsafe / Rsur` 约束、`Vqmax / Vzmax / Vxmax` 动态约束与离散 maneuver 状态的结合方式。
- 可以直接借鉴 `Lost and Await -> Land` 的 fail-safe 任务回退链。

### 局限性

- 论文仍包含较多视觉检测、Kalman 预测和感知评估内容，需要和高层状态机事实分开看。
- 一部分 transition 条件通过相对运动趋势和帧级判断给出，没有像 PLC 论文那样给出更低层的离散 I/O 表。
- 时间语义主要体现在 lost-target waiting threshold，不是复杂实时调度。

## 文献分类总结

- **文献类型**：真实无人机任务控制案例论文
- **控制对象**：自主监视无人机的动态目标跟踪控制器
- **状态机画像**：`EFSM + T1`
- **证据强度**：parallel FSM、状态定义、relative-position guard 和 fail-safe chain 都比较完整，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充视觉目标跟踪与失目标回退类无人机控制样本

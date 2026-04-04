# 面向地下矿井多模态测绘的自主无人机 / Development of an Autonomous UAV for Multi-Modal Mapping of Underground Mines

## 基本信息

- **标题**：Development of an Autonomous UAV for Multi-Modal Mapping of Underground Mines
- **中文标题**：面向地下矿井多模态测绘的自主无人机
- **作者**：Luis Escobar，David Akhihiero，Jason N. Gross，Guilherme A. S. Pereira
- **单位**：
  - Department of Mechanical, Materials and Aerospace Engineering, West Virginia University
- **发表**：Robotics，2026
- **DOI**：10.3390/robotics15030063
- **链接**：https://doi.org/10.3390/robotics15030063

### 代码/仓库获取方式

- 原文说明软件实现基于自定义 `ROS 2 Humble` package，并集中管理通信桥、传感器驱动和 core finite-state machine。
- 论文未提供公开仓库，但 mission profile、控制模式和 Figure 6 的状态机已经足够详细，可直接作为 source paper 使用。

### 数据集/案例获取方式

- 原文没有单独开放数据集入口。
- 论文提供了地下矿井 corridor exploration 与 pillar inspection 的真实任务案例，以及多模态点云重建流程，可直接作为单案例控制论文收纳。

## 简报

这篇论文解决的是**无人机如何在 GNSS 缺失、低光和狭窄地下矿井中切换手动记录、反应式探索与自主支柱扫描三种任务模式**的问题。输入是 RC 指令、LiDAR 空旷方向、天花板距离、支柱角点和目标支柱位置，方法是用一个包含三个 mission block 的层次状态机来调度起飞、找自由空间、扫掠支柱和落地流程，输出是 `manual data collection / reactive exploration / supervised autonomous pillar inspection` 的统一任务监督控制链。

- **输入**：manual RC commands、LiDAR free-space vectors、ceiling distance、pillar corners、mission profile、payload selection。
- **方法**：自定义 `ROS 2` 包中的 core FSM，按 mission block 切换手动记录、反应式探索与 back-and-forth pillar inspection。
- **输出**：独立数据记录、起飞到安全高度后的 corridor exploration、沿支柱表面的往返扫描与落地流程。
- **一句话评价**：这是高质量的 `HSM + T0` 地下矿井 UAV 监督控制样本，顶层 mission 和子任务阶段都足够清晰。

## 控制系统与状态机证据

### 控制对象

论文对象是地下矿井测绘无人机上的任务监督控制器。它负责决定无人机何时仅做手动遥控与数据记录、何时进入自主 corridor exploration，以及何时切换到受监督的 pillar inspection 扫描任务。

### 状态机组织方式

原文把控制软件明确写成一个 `core finite-state machine`，并给出三种 mission mode：

1. `Mission 1`：manual flight / data logging
2. `Mission 2`：reactive exploration
3. `Mission 3`：supervised autonomous inspection

其中 `Mission 2` 和 `Mission 3` 又分别展开为 `Take off / Reach altitude / Free Space / Set direction / Move Robot` 与 `Adjust altitude / Adjust parallel pos / Corner Detection / Move robot / Land` 等子阶段。

### 关键控制链

论文给出的任务控制链包括：

- 初始 `Wait` 状态既可以进入独立的 `PayloadRecord` 数据记录模式，也可以根据用户选择切换到三类 mission 中的一类。
- `reactive exploration` 模式下，无人机先起飞到安全高度，再寻找最大空旷方向、调整姿态并沿 `V_cmd` 前进，直到到达结束条件或收到落地命令。
- `supervised autonomous pillar inspection` 模式下，系统先调节与支柱和天花板的相对距离，再通过 corner detection 与 parallel position adjustment 维持扫描几何关系。
- 在扫描阶段，任务控制器执行 back-and-forth 覆盖策略，逐层推进支柱面扫描，直到完成任务或转入落地流程。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实地下矿井 UAV 任务监督器**，不是单纯 SLAM 或点云重建论文。
- 原文已经把三类 mission、起飞/探索/扫描子阶段以及落地入口明确组织成 state machine，适合直接转写成自然语言状态机样本。
- 对“同一平台上多 mission profile 切换”的层次监督控制很有参考价值。

### 可直接借鉴之处

- 可以直接借鉴 `manual / exploration / inspection` 三 mission 模式共存的顶层组织。
- 可以直接借鉴 `Take off -> Reach altitude -> Free Space -> Move Robot` 的轻量探索控制链。
- 可以直接借鉴 pillar inspection 中 `Adjust altitude / Adjust parallel pos / Corner Detection / Move robot` 的扫描监督逻辑。

### 局限性

- 论文的大量篇幅仍然用于多模态点云重建与传感器方案，不应把这些内容误当作状态机主链。
- 时间语义主要是阶段顺序和任务完成条件，不是显式计时约束。
- 原文把状态图放在 Figure 6 中，部分子状态名仍需结合正文说明一起解读。

## 文献分类总结

- **文献类型**：真实地下矿井 UAV 任务控制案例论文
- **控制对象**：地下矿井测绘无人机 mission supervisor
- **状态机画像**：`HSM + T0`
- **证据强度**：三类 mission、起飞/探索/扫描子阶段和落地流程均明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充地下空间 UAV 自主巡检、任务模式切换与扫描覆盖控制样本

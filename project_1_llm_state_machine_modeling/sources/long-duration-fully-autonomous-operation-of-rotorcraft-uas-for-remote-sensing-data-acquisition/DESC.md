# 长时全自主旋翼无人机遥感数据采集运行 / Long-Duration Fully Autonomous Operation of Rotorcraft UAS for Remote-Sensing Data Acquisition

## 基本信息

- **标题**：Long-Duration Fully Autonomous Operation of Rotorcraft UAS for Remote-Sensing Data Acquisition
- **中文标题**：长时全自主旋翼无人机遥感数据采集运行
- **作者**：Danylo Malyuta，Christian Brommer，Daniel Hentzen，Thomas Stastny，Roland Siegwart，Roland Brockers
- **单位**：
  - University of Washington
  - Alpen-Adria-Universität Klagenfurt
  - Jet Propulsion Laboratory, California Institute of Technology
  - ETH Zürich
- **发表**：Journal of Field Robotics, 2020, 37(1): 137-157
- **DOI**：10.1002/rob.21898
- **链接**：https://doi.org/10.1002/rob.21898

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文正文给出了 autonomy engine、master/slave state machine、vision-based landing 和 charging station 的完整软件架构与关键控制逻辑，可据此重建高层控制器。

### 数据集/案例获取方式

- 原文未提供单独下载的 benchmark 数据集。
- 论文包含真实无人机、充电站、任务循环、室内外长时试验和状态转换曲线，可直接作为单案例 source paper 使用。

## 简报

这篇论文解决的是**长时户外自主旋翼无人机如何反复执行“起飞-采集-返航-着陆-充电”任务循环**的问题。输入是电池状态、起飞前健康检查、航点任务、着陆点视觉可见性和紧急事件，方法是把 autonomy engine 组织成 `master + phase-specific autopilot` 的层次状态机，输出是可在真实充电站上连续自主运行数小时的任务控制系统。

- **输入**：battery status、motor nominal performance、mission waypoint/hover plan、landing pad visibility、touchdown detection。
- **方法**：master state machine 调度 `takeoff / mission / landing / emergency landing` 四个 autopilot。
- **输出**：可长时运行的自主飞行任务控制逻辑、视觉回充落点对准流程和应急降落回退链。
- **一句话评价**：这是很强的 `HSM + T0` 航空航天控制样本，因为层次结构、状态名和异常回退路径都非常具体，而且对象是真实平台而不是仿真示意。

## 控制系统与状态机证据

### 控制对象

论文对象是一个真实的 rotorcraft UAS 与地面 landing station 联合系统，不是泛化的无人机框架。系统能在用户只给出一次任务后反复执行自主飞行、着陆、充电和再次起飞，并已在室内外实验中完成多次无人值守飞行循环。

### 状态机组织方式

原文明确说明高层自主决策采用 `hierarchy of master and slave state machines`。其中：

1. **master state machine** 负责选择当前任务阶段。
2. **slave / autopilot state machines** 分别实现 `takeoff`、`mission`、`landing` 和 `emergency landing` 的具体逻辑。

这意味着该系统不是单条简单顺序链，而是一个典型的“顶层模式切换 + 阶段内专属控制器”的层次式任务管理结构。

### 关键控制细节

这篇论文对 `project_1` 很有价值的一点，是它把每个阶段的控制动作写得相当具体：

- 起飞前要检查 battery voltage 和 motor nominal performance。
- `takeoff` 中要重新初始化状态估计器并记住返航位置。
- `landing` 中先检查 AprilTag 着陆标记是否可见；不可见时进入 spiral grid search。
- 对准后执行 constant-velocity descent，并用高度/垂向速度阈值判定 touchdown。
- 电池危急时切到 `emergency landing`，在当前位置原地软着陆。

因此它虽然不以显式 timer 为主，但高层状态和事件驱动的控制链非常完整。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它补充了 `sources` 中高质量的**真实 UAV 任务管理**样本。
- 它不是连续控制律论文，而是把高层 mission control 的状态骨架直接写清楚。
- 它能提供“正常任务链 + 异常回退链 + 真实实验验证”三者同时具备的 source 证据。

### 可直接借鉴之处

- 可以直接借鉴 `master state + phase autopilot` 的层次化写法。
- 可以直接借鉴从健康检查、返航、视觉搜索到 touchdown 判定的自然语言组织方式。
- 可以直接借鉴把 low battery、motor fault、pad invisible 这些异常条件写成高层模式切换触发器。

### 局限性

- 论文的低层控制与感知仍包含较多导航/视觉实现细节，不应整段混入状态机文本。
- 真正的 autopilot 内部图主要依赖文中流程图，抽取时需要结合相关图示理解。
- 时间语义主要体现在任务事件与阈值，而不是显式时钟逻辑。

## 文献分类总结

- **文献类型**：真实无人机控制案例论文
- **控制对象**：带充电站的长时自主旋翼无人机任务控制器
- **状态机画像**：`HSM + T0 + 层次`
- **证据强度**：主状态、子控制器和异常回退链都很清晰，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，用于补齐真实任务调度型无人机控制样本

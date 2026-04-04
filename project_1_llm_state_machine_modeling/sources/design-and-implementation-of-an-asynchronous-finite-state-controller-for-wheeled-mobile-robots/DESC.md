# 轮式移动机器人异步有限状态控制器的设计与实现 / Design and Implementation of an Asynchronous Finite State Controller for Wheeled Mobile Robots

## 基本信息

- **标题**：Design and Implementation of an Asynchronous Finite State Controller for Wheeled Mobile Robots
- **中文标题**：轮式移动机器人异步有限状态控制器的设计与实现
- **作者**：Alessandro Bozzi，Simone Graffione，Roberto Sacile，Enrico Zero
- **单位**：University of Genoa
- **发表**：Actuators，2022
- **DOI**：10.3390/act11110330
- **链接**：https://doi.org/10.3390/act11110330

### 代码/仓库获取方式

- 原文未提供独立公开仓库。
- 论文说明控制算法在 `Simulink/Stateflow` 中设计，并部署到 `STM Nucleo` 板卡上，可作为异步 FSM 控制器工程实现案例阅读。

### 数据集/案例获取方式

- 原文未提供外部数据集。
- 论文给出了三车道避障 case study、状态流图、guard conditions、传感器输入和电机 PWM 输出，适合作为单案例 source paper。

## 简报

这篇论文解决的是**一个轮式移动机器人如何在三车道环境中跟踪车道并在前方出现障碍物时异步切换车道**的问题。输入是超声波传感器、循迹传感器、轮编码器和舵机角度，方法是用 `Stateflow` 实现异步有限状态控制器，输出是 `follow / check lane / lane change / stop` 控制链及相应 PWM 控制信号。

- **输入**：obstacle distance、line-tracking signals、wheel encoder feedback、servo heading。
- **方法**：异步有限状态机加 `PID` 车道跟踪与比例式换道控制。
- **输出**：三车道环境中的跟随、检测、变道和停止控制逻辑。
- **一句话评价**：这是清晰的 `EFSM + T0` 离散控制样本，状态图、guard 条件和输出接口都比较完整。

## 控制系统与状态机证据

### 控制对象

论文对象是一个非转向式四轮移动机器人。控制器需要在车道跟随与变道之间切换，并根据前方障碍距离和相邻车道是否空闲决定下一状态。

### 状态机组织方式

原文的 flowchart / FSM 包含如下显式状态：

1. `START`
2. `Follow right lane`
3. `Check middle lane`
4. `Follow middle lane`
5. `Check left lane`
6. `Follow left lane`
7. `STOP`

这些状态围绕 obstacle detection、lane availability 和 orientation guard 进行切换。

### 关键控制链

论文把主控制链写得比较具体：

- 机器人初始在最右侧车道跟线行驶。
- 当前方 `0.5 m` 内检测到障碍物时，状态机触发车道检查。
- 若相邻车道可用，则进入变道状态并用高增益比例控制完成转向。
- 变道结束后重新回到对应车道的 `Follow` 状态。
- 若已无可用车道，则进入 `STOP`。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 这是一个**真实轮式移动机器人控制器**，不是仅做路径规划评估。
- 原文把输入、状态、guard 和输出都连在一起，适合直接转为自然语言状态机样本。
- 它补充了当前文库中相对稀缺的“小型移动机器人避障换道”离散控制案例。

### 可直接借鉴之处

- 可以直接借鉴 `Follow -> Check -> Follow/Stop` 的多车道避障控制模板。
- 可以直接借鉴 measured distance 和 orientation 作为转移 guard 的写法。
- 可以直接借鉴把 line-tracking PID 与 lane-change proportional controller 作为状态内动作分开的组织方式。

### 局限性

- 论文面向教学和实验平台，系统规模比工业移动机器人更小。
- 时间语义主要靠 obstacle threshold 与动作顺序，不是显式定时器。
- 车道状态名主要通过 flowchart 给出，低层执行代码没有全文展开。

## 文献分类总结

- **文献类型**：真实轮式移动机器人控制案例论文
- **控制对象**：三车道避障换道 WMR 控制器
- **状态机画像**：`EFSM + T0`
- **证据强度**：state flow、guard conditions、case study 与输出接口都明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充移动机器人换道与避障类控制样本

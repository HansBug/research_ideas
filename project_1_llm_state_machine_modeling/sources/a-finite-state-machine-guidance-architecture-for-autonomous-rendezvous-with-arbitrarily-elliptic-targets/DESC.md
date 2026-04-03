# 面向任意椭圆目标轨道的自主交会有限状态机引导架构 / A Finite State Machine Guidance Architecture for Autonomous Rendezvous with Arbitrarily Elliptic Targets

## 基本信息

- **标题**：A Finite State Machine Guidance Architecture for Autonomous Rendezvous with Arbitrarily Elliptic Targets
- **中文标题**：面向任意椭圆目标轨道的自主交会有限状态机引导架构
- **作者**：Diego Buratti，Gabriella Gaias，Stefano Torresan，Thomas Vincent Peters，Pedro Roque
- **单位**：
  - OHB System AG
  - Politecnico di Milano
  - KTH Royal Institute of Technology
- **发表**：Aerospace, 2026, 13(3): 230
- **DOI**：10.3390/aerospace13030230
- **链接**：https://doi.org/10.3390/aerospace13030230

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文给出了 guidance layer 的分层 FSM 结构、控制子模块、漂移阈值和场景参数，可复现其状态机逻辑。

### 数据集/案例获取方式

- 原文未提供外部 benchmark 包下载链接。
- 论文正文提供了 rendezvous 场景、FSM 参数表、轨道参数和数值仿真配置，可直接作为单案例来源。

## 简报

这篇论文解决的是**航天器在任意椭圆目标轨道附近的自主交会引导问题**。输入是相对漂移、hold point、relative orbit 状态和任务时间线，方法是构造 `WSE / SSE` 双主状态的分层 FSM，并在下层挂接 drift、safe sizing 和 station keeping 等控制模块，输出是可安全执行的交会 guidance logic。

- **输入**：relative drift、hold point、keep-out-zone margin、mission timeline、relative orbital elements。
- **方法**：layered FSM + truth tables + maneuver library。
- **输出**：自主交会 guidance layer 与仿真验证结果。
- **一句话评价**：这是一条很强的 `HSM + T1` 航天控制样本，因为主状态、子模块和时间阈值都写得非常具体。

## 控制系统与状态机证据

### 主状态与层次结构

论文把 guidance layer 明确组织为两大主状态：

1. `WSE`：Walking Safe Ellipse
2. `SSE`：Stationary Safe Ellipse

在其上方还有 `Timeline Manager` 与 `WSE/SSE status` 这类高层判定逻辑，在其下方还有 `stand-by / safe sizing / station keeping / shape control / compute drift` 等控制子模块，因此这是非常标准的层次式控制结构。

### 时间语义

这篇论文不是单纯 `T0` 的模式管理，因为它给了：

- hold duration
- drifting period
- `TTL` 触发的重新计算
- `aδa_thr / aδa_min / aδa_max`

这让它成为一个非常典型的工程 `T1` 航天控制样本。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它补充了当前 `sources` 中较少见的**交会/近距离操作**方向 HSM 样本。
- 它的状态名字、判定条件和时间阈值非常适合直接转写成状态机自然语言描述。
- 与一般只讲轨道控制方程的论文不同，它把高层 mission guidance 的状态骨架讲清楚了。

### 可借鉴之处

- 可以直接借鉴 `main state + manager truth table + control submodule` 的层次化写法。
- 可以直接借鉴 `hold point / TTL / drift threshold` 这套时间和空间条件表达。
- 可以直接借鉴在一个状态机中融合 `move/stop + sizing + waiting + correction` 的复合控制叙事。

### 局限性

- 低层机动求解仍然带有较多轨道动力学公式，不适合全部直接当作状态机文本。
- 结构图重要性很高，抽取时必须结合 Figure 4/5 与 Table 9。
- 这是 guidance layer 样本，不是完整飞控闭环实现。

## 文献分类总结

- **文献类型**：真实航天控制案例论文
- **控制对象**：自主交会任务的机载 guidance layer
- **状态机画像**：`HSM + T1 + 显式时钟/层次`
- **证据强度**：状态、子模块与时间阈值均清晰，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，用于补齐航天任务管理与时间阈值控制样本

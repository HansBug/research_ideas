# 面向 LNG 船混合供能的状态转移逻辑设计 / State Transitions Logical Design for Hybrid Energy Generation with Renewable Energy Sources in LNG Ship

## 基本信息

- **标题**：State Transitions Logical Design for Hybrid Energy Generation with Renewable Energy Sources in LNG Ship
- **中文标题**：面向 LNG 船混合供能的状态转移逻辑设计
- **作者**：Michael E. Stamatakis，Maria G. Ioannides
- **单位**：School of Electrical and Computer Engineering, National Technical University of Athens, Greece
- **发表**：Energies, 2021, 14(22): 7803
- **DOI**：10.3390/en14227803
- **链接**：https://doi.org/10.3390/en14227803

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文给出了输入变量、输出变量、数学模型、状态表和 Matlab 流程图，足以复现其 EMS 逻辑。

### 数据集/案例获取方式

- 原文未提供单独下载的数据集包。
- LNG 船供能系统配置、负荷模型、状态条件和流程图均在正文与表格中给出，可直接作为 source case 使用。

## 简报

这篇论文解决的是**LNG 船在可再生能源与热机并存条件下的供能调度问题**。输入是负荷需求、光伏/风能出力、各热机最大功率和电池 SoC，方法是把 EMS 写成 12 状态有限状态机，输出是针对 LNG、DG1、DG2、电池与剩余功率的调度决策。

- **输入**：`PL / Ppv / Pw / SoC / eng1_Pmax / eng2_Pmax / eng3_Pmax`
- **方法**：有限状态机 + 逻辑状态转移表 + Matlab 流程图实现
- **输出**：对 LNG 发电机、柴油机、电池充放电与 spare power 的请求量
- **一句话评价**：这是一篇非常适合 `project_1` 的 `EFSM + T0` 高质量 source 论文，因为它把变量、守卫和状态行为都写得很明确。

## 控制系统与状态机证据

### 为什么它是 EFSM

论文不是只列出模式名，而是把状态切换明确依赖到一组变量守卫上：

- `Ppv + Pw ≥ PL`
- `Ppv + Pw < PL`
- `eng3_Pmax > PL - Ppv - Pw`
- `SoC > 0.5` / `SoC < 0.5`

这类“状态 + 变量 + 守卫”的写法非常标准地对应 `EFSM`，并且每个状态还给出了进入后的动作描述。

### 状态主链

状态表至少覆盖了三类情况：

1. **可再生能源足够供电**：`State 1_1 / 1_2`
2. **负荷超过 RES，需要逐步启用 LNG / DG1 / DG2**：`State 2_1 ... 2_6`
3. **零负荷或极端非法工况**：`State 3_1 ... 3_3` 与 `State 2_7`

因此它既有 nominal dispatch，也有边界状态与非法状态，不只是单一顺序流程。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它提供了真实的船舶能量管理控制对象。
- 它把状态和变量守卫写得足够完整，适合直接抽成自然语言到状态机样本。
- 它补充了当前 `sources` 中较少见的**船舶能源管理 EFSM** 样本。

### 可借鉴之处

- 可以直接借鉴“输入变量表 + 输出变量表 + 状态表”这种强结构化写法。
- 可以直接借鉴按资源优先级递增启用执行单元的控制叙事。
- 可以直接借鉴非法状态 `State 2_7` 这种边界场景表达方式。

### 局限性

- 时间语义更多体现在“随负荷变化的状态转移”，而不是显式局部计时器，所以更适合作为 `T0` 样本。
- 大量篇幅在做功率方程与稳定性分析，抽取时需要主动聚焦 EMS 状态表。
- 状态数较多，命名偏工程编号，需要在后续数据整理时补自然语言别名。

## 文献分类总结

- **文献类型**：真实控制案例论文
- **控制对象**：LNG 船混合供能 EMS
- **状态机画像**：`EFSM + T0`
- **证据强度**：状态表、守卫条件与动作描述都足够强，可直接支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，不是方法 baseline

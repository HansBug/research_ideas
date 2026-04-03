# 智能系统决策制定的设计、形式化与验证 / Design, Formalization, and Verification of Decision Making for Intelligent Systems

## 基本信息

- **标题**：Design, Formalization, and Verification of Decision Making for Intelligent Systems
- **中文标题**：智能系统决策制定的设计、形式化与验证
- **作者**：Mohammad Hejase，Andreas Katis，Anastasia Mavridou
- **单位**：
  - NASA Ames Research Center
  - KBR Inc. / NASA Ames Research Center
- **发表**：AIAA SCITECH 2024 Forum, 2024
- **DOI**：10.2514/6.2024-2409
- **链接**：https://doi.org/10.2514/6.2024-2409

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文明确给出了 `FRET -> CoCoSim -> Simulink` 的工具链，以及 `DZR` 案例的 H-FSM、需求模板和验证入口。

### 数据集/案例获取方式

- 原文未提供外部 benchmark 打包下载链接。
- 论文正文提供了 NASA `Troupe` 系统 `Dynamic Zonal Relay (DZR)` 阶段的功能分解、层次状态机、事件定义和参数输出，可直接作为单案例来源。

## 简报

这篇论文解决的是**自主系统高层决策模块如何系统设计、形式化并验证**的问题。虽然论文有明显的方法论文属性，但它并不是空泛示例，而是把 NASA 漫游车协同任务中的 `DZR` 决策层完整地实例化成一个可追溯的 `H-FSM`，并给出状态、事件、局部时间窗口和输出参数。

- **输入**：任务分解结果、事件向量 `EA / EB / EC / ED / EE`、相关 flag 和 rover 任务阶段。
- **方法**：functional decomposition + `H-FSM` + FRET structured NL + CoCoSim verification。
- **输出**：`DZR` 决策层状态机、形式化需求和针对 Simulink 实现的验证结果。
- **一句话评价**：如果只看论文主题，它偏方法；但如果聚焦 `DZR` case，本质上是一个状态、事件、参数输出都很明确的 `HSM + T1` source 样本。

## 控制系统与状态机证据

### 控制对象

原文 case study 针对的是 NASA 自主 rover 系统中的 `Dynamic Zonal Relay` 阶段决策模块。该模块不负责连续控制本身，而是位于高层，向低层控制器下发 controller mode、activity 和 velocity 等参数，并根据任务事件切换状态。

### 状态机组织方式

作者把 `DZR_1` 拆成三个 meta-state：

1. `DriveToZone_11`
2. `CharacterizeZone_12`
3. `Relay_13`

每个 meta-state 内部又有叶状态，例如：

- `Drive_111` / `Transmit_112`
- `Drive_121` / `Acquire_122` / `Transmit_123`
- `ApproachRelayLoc_131` / `TransferData_132` / `Idle_133`

因此它是标准的层次状态机，而不是一条单层流程链。

### 时间与事件语义

这篇论文对 `project_1` 特别有用的一点，是它不仅写了状态，还把事件条件写成了可直接落形式化模型的规则。例如：

- `ED_2 <=> persisted(3, F_segmentCharacterizationComplete)`
- `Upon(FSM_State_3 = DZR_CharacterizeZone_Acquire & ED_2) ... FSM_State_3 = DZR_CharacterizeZone_Transmit`

这说明状态转移不是单纯布尔切换，而带有“连续保持 3 个决策步”的局部时间语义，因此更适合归入 `T1`。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它补充了 `sources` 中较少见的**自治任务决策层**样本。
- 它同时具备层次状态、事件向量、局部时间窗口和参数输出映射。
- 即使论文整体偏验证方法，`DZR` 部分仍然具备足够强的原文证据，可直接入库。

### 可直接借鉴之处

- 可以直接借鉴 `meta-state / sub-state / leaf-state` 的组织方式。
- 可以直接借鉴把状态机事件定义写成 `persisted(n, flag)` 这种局部时间条件。
- 可以直接借鉴在叶状态上附着 `controllerType / activity / velocity` 这样的接口参数。

### 局限性

- 论文重点仍包含方法论与工具链介绍，抽取时必须明确只保留 `DZR` 案例的控制对象部分。
- 具体 rover 硬件与环境约束写得不如纯控制案例论文细。
- 若后续做纯自然语言需求建模，还需要把部分 FRET 句式转写成更自然的工程表述。

## 文献分类总结

- **文献类型**：方法论文中的高质量控制案例子部分
- **控制对象**：NASA 自主 rover `DZR` 决策层
- **状态机画像**：`HSM + T1 + 层次`
- **证据强度**：状态、事件、时间窗口和输出参数都清晰，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，用于补齐自治任务管理与可验证决策层样本

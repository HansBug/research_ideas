# Orion 交会、近距离操作与对接的 GN&C 序列设计 / GN&C Sequencing for Orion Rendezvous, Proximity Operations, and Docking

## 基本信息

- **标题**：GN&C Sequencing for Orion Rendezvous, Proximity Operations, and Docking
- **中文标题**：Orion 交会、近距离操作与对接的 GN&C 序列设计
- **作者**：Peter Z. Schulte，Peter T. Spehar，David C. Woffinden
- **单位**：
  - The Charles Stark Draper Laboratory
  - NASA Johnson Space Center
- **发表**：Annual AAS Guidance, Navigation and Control Conference, 2020
- **报告号**：JSC-E-DAA-TN77227
- **链接**：https://ntrs.nasa.gov/citations/20200001393

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文明确说明 `PSAM` 信息在 prototype flight software、Timeline Management 和 GN&C Executive 中实现，并给出了实现与测试流程。

### 数据集/案例获取方式

- 原文未提供外部 benchmark 包下载链接。
- 论文正文给出了 Orion `RPOD` 的 nominal/off-nominal ConOps、PSAM 层次结构、状态机转移图和关键时序条件，可直接作为单案例来源。

## 简报

这篇论文解决的是**Orion 航天器在 Gateway / EUS 附近执行交会、近距离操作与对接时，高层 GN&C sequencing 如何设计与实现**的问题。输入是 relative range、`NRI`/`RB3`/`RB5`/`RB6` 等关键任务事件、`ATP` 授权和 docking 状态，方法是以 `PSAM` 形式构建 `Phase -> Segment -> Activity -> Mode` 的层次序列控制，输出是可以嵌入 prototype flight software 的任务序列逻辑。

- **输入**：range to Gateway、planned `TIG`、`ATP`、hard capture、undock 和 off-nominal 指令。
- **方法**：层次 `PSAM` + nominal/off-nominal state machine design。
- **输出**：Orion `RPODOperations` 阶段的 GN&C sequencing 定义与仿真实现。
- **一句话评价**：这是很强的 `HSM + T1` 航天任务管理样本，因为层次结构、时间窗口、阶段切换和异常分支都被明确写成状态机设计对象。

## 控制系统与状态机证据

### 控制对象

论文对象是 Artemis 任务中 Orion 航天器的 `RPOD` 高层序列控制，而不是轨道动力学求解器本身。它负责在不同接近距离和任务阶段下切换 GN&C software configuration，并决定何时进入 burn configuration、close range、docked、departure 等任务状态。

### 状态机组织方式

作者使用 `PSAM` 层次：

1. `Phase`
2. `Segment`
3. `Activity`
4. `Mode`

其中新增了专门的 `RPODOperations` Phase，并在其内部定义：

- `RPOD_Coast`
- `RPOD_Burn_Config`
- `RPOD_Burn`
- `RPOD_Mid_Range`
- `RPOD_Close_Range`
- `Docked`
- `RPOD_Departure`

这已经是非常标准的层次任务控制结构。

### 时间与任务语义

论文最有价值的地方在于把关键任务时间点写得很具体：

- `RangeToTarget < [TBD] km` 或 `NRI - 1 hr` 进入 `RPODOperations`
- Far Range burn 前 `20 min` 切到 `RPOD_Burn_Config`
- `5 min before TIG` 切到 `RPOD_Burn`
- `RB3` 完成后进入 `RPOD_Mid_Range`
- `RB5` 完成后进入 `RPOD_Close_Range`
- hard capture 后进入 `Docked`

同时又补充了 off-nominal 分支：

- `RPOD_Passive_Flyby`
- `RPOD_*_Hold_Retreat`
- `RPOD_*_Abort`

因此这是一个典型的 mission sequencing `HSM + T1` 样本。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它补充了 `sources` 中高质量的**航天任务序列控制**样本。
- 它非常适合训练“长链任务阶段 + 层次状态 + 工程时序触发”的建模能力。
- 它不仅有 nominal path，还有明确的 contingency branches。

### 可直接借鉴之处

- 可以直接借鉴 `Phase / Segment / Activity / Mode` 的层次组织模式。
- 可以直接借鉴把 `NRI-1h`、`20 min before TIG`、`5 min before TIG` 这类工程时间点写成状态转移条件。
- 可以直接借鉴将 `Hold_Retreat` 与 `Abort` 作为独立 off-nominal segment 的设计方式。

### 局限性

- 论文重点是 sequencing 设计，不是完整 GN&C 低层算法细节。
- `Activity` 级完整图太大，文中只给了局部示例，抽取时要以 phase/segment 主链为主。
- 一些 off-nominal 细节仍在 development 中，部分逻辑保留了 TBD 空间。

## 文献分类总结

- **文献类型**：真实航天任务序列控制案例论文
- **控制对象**：Orion `RPOD` 高层 GN&C sequencing
- **状态机画像**：`HSM + T1 + 显式时钟/层次`
- **证据强度**：阶段、时间窗口和 contingency branches 都清晰，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，用于补齐航天交会任务的层次时序控制样本

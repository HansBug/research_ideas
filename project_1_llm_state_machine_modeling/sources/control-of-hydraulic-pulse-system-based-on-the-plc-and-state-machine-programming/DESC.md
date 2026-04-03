# 基于 PLC 和状态机编程的液压脉冲系统控制 / Control of Hydraulic Pulse System Based on the PLC and State Machine Programming

## 基本信息

- **标题**：Control of Hydraulic Pulse System Based on the PLC and State Machine Programming
- **中文标题**：基于 PLC 和状态机编程的液压脉冲系统控制
- **作者**：Juraj Pančík，Pavel Maxera
- **单位**：Institute of Forensic Engineering, Brno University of Technology, Czech Republic
- **发表**：Designs, 2018, 2(4): 48
- **DOI**：10.3390/designs2040048
- **链接**：https://doi.org/10.3390/designs2040048

### 代码/仓库获取方式

- 原文未提供独立的公开代码仓库链接。
- 论文摘要明确说明“for further study we offer readers the full programming code written in sequential function charts”，因此当前可获取的实现入口主要是论文正文中的顺序功能图、线程表与主控状态机说明。

### 数据集/案例获取方式

- 原文未提供独立数据集下载链接。
- 液压脉冲系统的需求、I/O 信号、应用层线程、脉冲列车参数和校准方式均在正文中给出，可直接作为单案例 source paper 使用。

## 简报

这篇论文解决的是一个**工业液压脉冲设备的低成本 PLC 控制落地问题**：输入是实际设备的硬件信号、用户模式切换以及脉冲列车参数，方法是把控制程序拆成 physical layer 与 application layer 两层线程，并在 application layer 上构造主控状态机，输出是可执行的 PLC 控制逻辑与主控状态机设计。

- **输入**：`ERROR / MANUAL / AUTO / PULSE / RESET` 等硬件信号，以及 `N / p / T1 / T0` 脉冲列车参数与校准常数。
- **方法**：physical-layer 线程先把原始硬件信号变成 program flags；application-layer 再用 `WAIT / MANUAL / AUTO / PULSE / ERROR` 主状态和若干子状态管理系统行为。
- **输出**：液压脉冲系统的 PLC 控制程序、主控状态机、参数输入与脉冲执行逻辑。
- **一句话评价**：这是非常典型的“真实工业对象 + 明确状态名 + 显式局部定时参数 + 可靠回退逻辑”的高质量 source 样本。

## 控制系统与状态机证据

### 控制对象

论文对象不是抽象软件流程，而是一个实际的工业气动液压脉冲系统。原文明确写出该系统可输出最高 `200 bar`、最高 `2 Hz` 的液压脉冲，并且控制程序运行在低成本 PLC 上。

### 状态机组织方式

作者采用了双层结构：

1. **physical layer** 负责处理硬件输入信号。
2. **application layer** 负责实现主控状态机。

在 application layer 中，论文明确给出了 `WAIT / MANUAL / AUTO / PULSE / ERROR` 五个主状态，以及 `6_State_Func / 7_State_Func` 等从属子状态。`AUTO` 负责参数编辑，`PULSE` 负责按配置执行脉冲列车，并在完成后自动返回 `AUTO`。

### 时间与参数语义

这篇论文对 `project_1` 特别有价值的一点，是它不是泛泛地说“有状态切换”，而是把每个脉冲 wagon 的四个关键参数直接写了出来：

- `N`：脉冲数量
- `p`：最大压力
- `T1`：脉冲持续时间
- `T0`：脉冲间暂停时间

因此它天然属于 `HSM + T1` 风格样本，既有层次结构，也有可以直接落到状态机边或状态驻留条件上的工程定时语义。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它是**真实控制对象**，不是工具论文或综述。
- 它的原文证据足以支撑 `STM.md` 写到 `🟢 A`。
- 它给出的不是单一主链，而是“模式切换 + 子状态调用 + 局部定时参数 + 故障状态”组合，适合做高质量 source 样本。

### 可直接借鉴之处

- 可以直接借鉴“两层线程 -> 主控状态机”的文字组织方式。
- 可以直接借鉴 `WAIT / MANUAL / AUTO / PULSE / ERROR` 这种工程控制中常见的 mode vocabulary。
- 可以直接借鉴 `N / p / T1 / T0` 这种参数化脉冲模板，作为后续自然语言到状态机建模的目标表达形式。

### 局限性

- 论文更偏工程实现，数学化验证较弱。
- 某些转移细节更多通过图和线程调用关系体现，而不是像形式化论文那样用统一 transition table 写全。
- 子状态 `6_State_Func / 7_State_Func` 的业务语义需要结合上下文整理，不是现成的自然语言需求文本。

## 文献分类总结

- **文献类型**：真实工业控制案例论文
- **控制对象**：工业气动液压脉冲系统
- **状态机画像**：`HSM + T1 + 显式时钟/层次/并行`
- **证据强度**：原文可追溯性强，适合直接进入 `sources` 主数据集候选池
- **与本研究关系**：不是 baseline，而是高价值 source sample

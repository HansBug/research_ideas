# 面向负荷削减的混合能源系统 Stateflow 能量管理策略 / Stateflow-Based Energy Management Strategy for Hybrid Energy System to Mitigate Load Shedding

## 基本信息

- **标题**：Stateflow-Based Energy Management Strategy for Hybrid Energy System to Mitigate Load Shedding
- **中文标题**：面向负荷削减的混合能源系统 Stateflow 能量管理策略
- **作者**：Muhammad Paend Bakht，Zainal Salam，Abdul Rauf Bhatti，Waqas Anjum，Saifulnizam A. Khalid，Nuzhat Khan
- **单位**：
  - Universiti Teknologi Malaysia
  - Balochistan University of Information Technology, Engineering and Management Sciences
  - Government College University Faisalabad
  - The Islamia University of Bahawalpur
  - Universiti Sains Malaysia
- **发表**：Applied Sciences, 2021, 11(10): 4601
- **DOI**：10.3390/app11104601
- **链接**：https://doi.org/10.3390/app11104601

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库链接。
- 论文给出了完整的 Stateflow 分层图、状态关系和关键守卫条件，可直接据此复现实验级控制逻辑。

### 数据集/案例获取方式

- 原文未提供独立 benchmark 下载链接。
- 论文正文提供了 Quetta 地区的辐照度、温度、负荷削减时段与 HES 参数设置，并用这些数据驱动仿真。

## 简报

这篇论文关注的是**在频繁 load shedding 条件下维持混合能源系统连续供电**。输入是 `P_Grid / P_PV / P_Load / SOC` 等运行量与负荷削减事件，方法是用 Stateflow 把 EMS 组织成带 `Grid_Connected_Mode` 与 `Islanded_Mode` 的分层状态机，输出是可执行的 HES 调度逻辑和按场景仿真的运行结果。

- **输入**：电网可用性、光伏功率、负荷需求、储能 SOC、发电机可用功率。
- **方法**：Stateflow 扩展有限状态机，根状态 `HES_Operation` 下再分 `Grid_Connected_Mode / Islanded_Mode` 与对应子状态。
- **输出**：模式切换逻辑、能源分配策略、按季节和负荷削减场景的仿真结果。
- **一句话评价**：这是典型的 `HSM + T1` 工程控制论文，原文对状态层次、并行关系和时间迭代都写得很清楚。

## 控制系统与状态机证据

### 状态机骨架

论文最重要的价值，在于它不是只说“有 energy management”，而是把控制骨架直接建成 Stateflow chart：

1. 根状态 `HES_Operation`
2. 两个主模式 `Grid_Connected_Mode` 与 `Islanded_Mode`
3. `Grid_Connected_Mode` 下的并行子状态 `PV_Mode` 与 `Grid_Mode`
4. `Islanded_Mode` 下围绕 `RES_Mode` 与 `Gen_Mode` 的切换

这已经足以支持单条高质量 `STM`。

### 关键守卫与时间语义

论文明确给出了：

- `P_Grid = 0` 触发 `Grid_Connected_Mode -> Islanded_Mode`
- `P_PV + P_ESU > P_Load` 时进入 `RES_Mode`
- `P_PV + P_ESU < P_Load` 时进入 `Gen_Mode`

同时它还明确说明 chart 通过 `timer` 实现 for-loop 构造，并且以**每小时**为时间步执行，因此这是很标准的工程 `T1` 样本，而不是纯 `T0` 模式切换。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它提供了真实控制对象而不是方法论文。
- 它用非常清晰的自然语言解释了状态层次和条件守卫，适合作为 `NL -> state machine` 建模输入。
- 它扩充了当前 `sources` 里较稀缺的**能源/负荷管理 HSM** 样本。

### 可借鉴之处

- 可直接借鉴 `root mode -> child mode -> guard` 的层次写法。
- 可直接借鉴 `inter-state / intra-state` 的分层转移语义。
- 可直接借鉴“电网模式 / 孤岛模式 / 储能优先 / 发电机兜底”的控制叙事模板。

### 局限性

- 系统主要通过仿真验证，没有落到实机部署。
- 低层 PV/电池模型篇幅较大，会稀释状态机主链，需要抽取时聚焦 `EMS` 部分。
- 一部分模式细节依赖图示和表格，不是完全文本化需求书风格。

## 文献分类总结

- **文献类型**：真实控制案例论文
- **控制对象**：负荷削减场景下的混合能源系统 EMS
- **状态机画像**：`HSM + T1 + 显式时钟/层次/并行`
- **证据强度**：可直接支撑 `🟢 A` 级 `STM`
- **与本研究关系**：高质量 source sample，不属于 baseline 论文

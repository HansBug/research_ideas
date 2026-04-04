# 自动腹膜透析机的状态机设计 / State Machine Design for an Automated Peritoneal Dialysis Machine

## 基本信息

- **标题**：State Machine Design for an Automated Peritoneal Dialysis Machine
- **中文标题**：自动腹膜透析机的状态机设计
- **作者**：Wafa A. Baroudi，Fatimah B. Alnahdi，Raghad S. Aljohani，Maryam A. Alzuabi，Nora K. Alsaqoub，Ibrahim A. Aljamaan，Naif A. Alrubai，Sajid Ali
- **单位**：
  - Biomedical Engineering Department, College of Engineering, Imam Abdulrahman Bin Faisal University
  - Department of Mechanical and Energy Engineering, College of Engineering, Imam Abdulrahman Bin Faisal University
- **发表**：Frontiers in Medical Technology，2025
- **DOI**：10.3389/fmedt.2025.1630829
- **链接**：https://doi.org/10.3389/fmedt.2025.1630829

### 代码/仓库获取方式

- 原文未提供公开代码仓库。
- 论文说明有限状态机设计与界面仿真基于 `LabVIEW` 实现，但未开放工程文件。
- 原文给出了 I/O 表、状态图、状态转移表、定时与错误状态说明，足以作为 source paper 直接使用。

### 数据集/案例获取方式

- 原文未提供独立数据集。
- 论文给出了自动腹膜透析机的完整过程设计与状态机实现，可直接作为医疗设备控制案例收纳。

## 简报

这篇论文解决的是**自动腹膜透析机如何在准备液体、注液、驻留、排液、冲洗和异常告警之间进行安全切换，并根据浊度尽早终止透析**的问题。输入是模式选择、温度、流量、液位、压力、浊度、危险值和故障信号，方法是把整个 APD 流程编码成 5-bit 有限状态机和对应 I/O/转移表，输出是 `standby -> instruction -> heating -> filling -> dwelling -> draining -> loop/flush -> error` 的完整设备控制链。

- **输入**：`S`, `DM`, `FM`, `AI`, `P`, `T`, `SD`, `F1-F4`, `L`, `PR`, `TU`, `DV`, `F`。
- **方法**：FSM-based APD process design + LabVIEW interface + turbidity-triggered early termination。
- **输出**：准备液体、注液、驻留计时、排液、循环判断、冲洗结束和 `11111` 错误告警的完整过程控制逻辑。
- **一句话评价**：这是高质量的 `EFSM + T1` 医疗设备控制样本，状态编码、I/O、驻留定时和错误状态都很完整。

## 控制系统与状态机证据

### 控制对象

论文对象是自动腹膜透析机的过程控制器。它负责在不同模式和传感器条件下调度加热、注液、驻留、排液、冲洗和异常停机，并通过浊度与计时逻辑优化 session 长度。

### 状态机组织方式

原文把该控制器明确写成 `finite state machine`，并给出 5-bit 状态编码。关键状态包括：

1. `S0` standby
2. `S1` written instructions
3. `S2` audible instructions
4. `S3` heater on
5. `S5` filling start
6. `S6` filling end
7. `S7` downward movement
8. `S8` draining start
9. `S10` draining end
10. `S11` loop stage
11. `S13` flush stage
12. `S17` error alarm (`11111`)

### 关键控制链

论文把 APD 主流程和异常处理写得较清晰：

- 用户完成安全问答后进入透析模式，系统先执行 `Preparing the Solution` 与温度控制。
- 进入 filling stage 后，持续监控液位、流量与压力；随后进入 dwelling phase，并显式启动 dwell timer。
- 排液阶段结合 turbidity sensor 判断浊度，若液体已足够清澈则提前结束 session，否则继续 loop 或后续流程。
- session 结束后进入 cleansing / flush stage，完成管路冲洗。
- 任一故障或危险值会触发 `state 11111` 错误告警，立即停机并向用户发出视觉与声音警报。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实医疗设备过程控制器**，不是单纯界面设计或综述。
- 原文保留了状态图、I/O 表、状态编码、浊度终止与错误态说明，适合直接提取成高质量自然语言状态机描述。
- 对“设备过程控制 + 计时 + 传感器驱动提前终止 + error state”这一类样本非常有价值。

### 可直接借鉴之处

- 可以直接借鉴 5-bit 状态编码与 I/O/transition table 并列呈现的方式。
- 可以直接借鉴 dwell timer 和 turbidity-triggered termination 的控制逻辑。
- 可以直接借鉴 `11111` 统一错误态与 watchdog/报警处理口径。

### 局限性

- 论文包含较多背景介绍与界面设计，需要聚焦第 4 节 FSM 主体。
- 部分状态采用编码名而非自然语言状态名，整理时需补足语义映射。
- 低层执行机构电路与结构细节不是核心，需要避免过度展开。

## 文献分类总结

- **文献类型**：真实医疗设备过程控制案例论文
- **控制对象**：自动腹膜透析机的过程监督控制器
- **状态机画像**：`EFSM + T1`
- **证据强度**：状态图、I/O、dwell timer、浊度触发和统一错误态明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充医疗设备阶段流程、传感器驱动终止和错误态样本

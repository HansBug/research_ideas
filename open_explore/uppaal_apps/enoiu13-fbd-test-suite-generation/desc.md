问题一句话：本文验证的是铁路 `TCMS` 中基于 `IEC 61131-3` 的 `FBD` 控制程序，核心问题是能否把工业 `PLC` 图形程序自动转成 `UPPAAL` 模型，并从中生成可执行的测试套件。
方法一句话：作者设计了 `FBD -> timed automata` 的结构化转换，用 `UPPAAL` 通过 reachability 诊断轨迹生成面向测试性质和 `FC/DC/CC` 覆盖准则的离线测试序列。
验证收获一句话：在 Bombardier `TCMS` 的 battery control system 上，测试性质和结构覆盖用例都能在 `0.03-0.53 s`、`4-6 MB` 的代价下生成，说明 `UPPAAL` 足以支撑工业 `FBD` 单元级测试生成。

## 基本信息

- 标题：Model-Based Test Suite Generation for Function Block Diagrams using the UPPAAL Model Checker
- 中文标题：使用 `UPPAAL` 模型检查器对功能块图生成测试套件
- 作者：Eduard Paul Enoiu、Daniel Sundmark、Paul Pettersson
- 单位：Mälardalen University
- 发表：2013 IEEE Sixth International Conference on Software Testing, Verification and Validation Workshops
- DOI：`10.1109/ICSTW.2013.27`
- 链接：[DOI](https://doi.org/10.1109/ICSTW.2013.27)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🚦 交通、车载与铁路
- 被验证系统：Bombardier `TCMS` 中的 battery control system 及其 `FBD` 控制程序
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文未提供独立 `UPPAAL` 模型仓库或转换工具下载；文中仅说明基于自建 reader/parser 和 `UPPAAL` 工具链。
- 案例/数据获取方式：案例来自 Bombardier `TCMS` 工业项目，正文给出 `BCS` 架构、测试性质和覆盖准则，但原始 `FBD` 工程不公开。

## 简报

这篇论文的核心不在“证明 `FBD` 可以验证”，而在“如何直接从工业 `PLC` 程序生成测试套件”。它把 `UPPAAL` 从性质检查器进一步变成测试用例生产器。

- 系统：高铁 `TCMS` 中的 battery control system。
- 特点：程序写在 `IEC 61131-3 FBD` 中，带 PLC scan-cycle 语义和定时功能块。
- 规模：完整 `TCMS` 超过 `800` 个 FBD 程序、约 `122,000` 行生成 `C` 代码；实验聚焦 `BCS` 子系统，包含 `30+` 个 FBD 程序和约 `5,000` 行生成 `C`。
- 模型：把每个 `FE` 转成一个 timed automaton，并补上 PLC 扫描周期、端口赋值和 timing annotation。
- 性质：既有人工定义的测试性质 `TP1-TP6`，也有 `FC/DC/CC` 三类结构覆盖要求。
- 方法：从 `FBD XML` 自动构建 `UPPAAL` 模型，再让模型检查器输出 witness trace 作为测试套件。
- 结果：工业 `BCS` 的性质测试和覆盖测试都能快速生成，并可在 `softTCMS` 模拟平台上执行。

`FBD 程序/XML -> timed automata 网络 -> reachability/test property -> diagnostic trace -> 离线测试套件`

## 论文定位

这是一篇边界非常清楚的 `🎛️ + 🚦` 条目。它主贡献是测试生成方法，但对象不是玩具例子，而是铁路 `TCMS` 的真实控制软件，因此仍然属于值得正式入账的工业应用论文。

## 验证对象与问题背景

### 系统与场景

被验证对象是 Bombardier `TCMS` 的 battery control system。它负责在辅助电源缺失时由电池给列车单元供电，在辅助电源存在时进行充电与监视。

### 系统组成与运行机制

`BCS` 至少包含以下关键部件：

1. 两条冗余 battery buses。
2. 两组冗余 batteries 与 chargers。
3. main battery contactor。
4. load shed contactors。
5. 通过 IP 网络向 `TCMS` 报告状态的 charger/supervision 逻辑。

### 验证边界

论文验证的是 `FBD` 控制程序及其 scan-cycle 语义，不涉及真实电池电化学、整车网络延迟细节或整车系统级集成测试。

### 核心问题

铁路 `PLC` 程序通常依赖人工功能测试、仿真和覆盖测试，但：

1. 手工测试成本高。
2. 时序逻辑不容易靠人工覆盖。
3. `FBD` 图形结构需要一种贴近语义的自动模型化方式。

## 模型与形式化建模

### 抽象对象

作者把 `FBD` 程序表示为：

1. `FE` 集合，包括 `FUNC` 与 `FB`
2. 输入/输出变量
3. 参数
4. 连线 `Con`

随后将每个 `FE` 映射成 timed automaton 片段。

### 建模形式

1. 每个 `FE` 生成一个 TA。
2. 额外加入环境、扫描周期和端口赋值逻辑。
3. 通过 timed automata network 保持 `read-execute-write` 语义。

### 关键抽象与取舍

1. 假设 `FBD` 程序符合 `IEC 61131-3` 标准。
2. 执行顺序采用预定 control-flow dependency。
3. 定时功能块按标准语义建模，而不是只保留布尔功能。

## 验证目标与性质

### 待验证问题

1. 是否能为 `BCS` 的实际测试需求自动生成测试套件。
2. 是否能为 `FC/DC/CC` 覆盖准则生成测试套件。
3. 工业规模子系统下的生成时间、内存和 trace 长度是否可接受。

### 性质类型

- reachability 型测试性质
- 结构覆盖
- 时序相关功能要求

### 性质分组与实际含义

论文展示的测试性质包括：

1. `TP1`
   - battery contactor 因低电压跳开。
2. `TP2`
   - battery contactor 在低电压条件下断开。
3. `TP3-TP6`
   - contactor 状态、charger charging/faulty/working 等业务语义。

### 查询表达

作者将测试需求统一改写为简单的 CTL reachability 性质，让 `UPPAAL` 输出 witness trace 作为测试序列。

## 核心方法与验证流程

1. 从 `FBD XML` 读取程序结构。
2. 自动生成 `UPPAAL` timed automata 模型。
3. 输入测试性质或覆盖准则。
4. 利用 `UPPAAL` 导出 witness trace。
5. 将 trace 转成 ready-to-use test suite。
6. 在 `softTCMS` 模拟平台执行。

## 案例与结果

### 工业规模

1. 完整 `TCMS` 超过 `800` 个 FBD programs、约 `122,000` 行生成 `C`。
2. 本文实验子系统 `BCS` 包含 `30+` 个 FBD programs、约 `5,000` 行生成 `C`。
3. 作者手工建模了 `35+` 个符合 `IEC` 标准和 MITRAC 库的功能块模型。

### 测试性质生成

表 `II` 显示 `TP1-TP6` 的测试套件生成结果：

1. 时间 `0.03-0.09 s`
2. 套件长度 `38-50`
3. 内存 `4-6 MB`

### 覆盖准则生成

表 `IV` 显示：

1. `FC`：`0.15 s`，长度 `49`
2. `DC`：`0.53 s`，长度 `102`
3. `CC`：`0.47 s`，长度 `100`

### 结果解释

作者强调，coverage-driven test generation 明显比 test-property generation 更贵，但在工业 `BCS` 子系统上仍然完全可接受。

## 与本研究的关系

### 相关性分析

这篇论文和博士研究的相关性在于：它展示了如何把工业图形控制程序稳定翻译成形式模型，并进一步从模型产出可执行工件。

### 可借鉴之处

1. `FBD -> TA` 的结构化映射。
2. 用 witness trace 直接生成测试序列。
3. 把 coverage criterion 也转成形式化目标，而不是只做需求性质。

### 存在的不足与改进空间

1. 更偏测试生成，不直接证明系统级安全。
2. 真实 `TCMS` 工程和模型不公开。
3. 结果主要停留在单元级和子系统级。

### 对本研究的启发

如果后续要让 `LLM` 自动从需求生成状态机，再自动产出验证场景或测试场景，这篇论文提供了很现实的桥接路径：先统一把结构和语义模式抽清楚，再把后续验证/测试目标自动投影到形式模型上。

## 重要的相关工作

### 1. `IEC 61131-3`

- 论文的全部建模前提都基于 `IEC 61131-3` 的 `FBD` 组件语义。

### 2. `UPPAAL`

- `UPPAAL` 在本文中不只是验证器，更直接承担 test suite generation 的 witness engine 角色。

### 3. `softTCMS`

- 生成出的测试最终落在 `softTCMS` 平台执行，说明该方法并非只停留在纸面模型。

## 案例、模型与数据公开情况

- 可获取性判断：🔒 难以取得
- 判断依据：论文公开，但核心 `TCMS/BCS` 工程来自 Bombardier 工业项目，原始程序、模型和平台工件未公开。
- 获取方式/链接：[DOI](https://doi.org/10.1109/ICSTW.2013.27)
- 对后续复用的现实影响：适合作为 `FBD -> TA -> 测试生成` 工作流样本，但若要复现实验，需要自建等价 `FBD` 子系统。

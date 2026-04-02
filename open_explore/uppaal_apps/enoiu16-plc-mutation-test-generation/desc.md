问题一句话：本文验证的是铁路 `TCMS` 中 `IEC 61131-3 FBD` 控制程序的测试生成流程，核心问题是 mutation-adequate 自动测试是否真能在工业 `PLC` 软件上替代或逼近人工测试。
方法一句话：作者把原程序与所有 mutants 聚合进一个统一的 `UPPAAL` 模型，用 monitor 动态观察变异是否被区分，再基于模型检查生成 weak/strong mutation 测试套件。
验证收获一句话：在 Bombardier `TCMS` 的 `61` 个程序和 `77` 个人工植入故障上，mutation 测试的 fault detection 仍弱于人工测试，但明显优于 decision coverage，且平均成本比人工测试低约 `110-115` 分钟。

## 基本信息

- 标题：Mutation-Based Test Generation for PLC Embedded Software Using Model Checking
- 中文标题：基于模型检查的 `PLC` 嵌入式软件变异测试生成
- 作者：Eduard P. Enoiu、Daniel Sundmark、Adnan Čaušević、Robert Feldt、Paul Pettersson
- 单位：Mälardalen University；Blekinge Institute of Technology
- 发表：Testing Software and Systems，2016
- DOI：`10.1007/978-3-319-47443-4_10`
- 链接：[DOI](https://doi.org/10.1007/978-3-319-47443-4_10)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🚦 交通、车载与铁路
- 被验证系统：Bombardier `TCMS` 中的一组 `IEC 61131-3 FBD` 控制程序及其测试流程
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文未提供独立工具或模型仓库；仅说明构建在已有 `CompleteTest` 与 `UPPAAL` 工作流之上。
- 案例/数据获取方式：案例源自 Bombardier `TCMS` 工业项目；论文公开给出程序规模、故障植入方式、成本口径和实验结果，但原始程序与人工测试资产不公开。

## 简报

这篇论文延续了前一篇 `FBD -> UPPAAL` 测试工作，但把关注点从“能否生成测试”推进到“生成出来的测试到底值不值得用”。因此它是一个非常实在的工业评测案例。

- 系统：Bombardier `TCMS` 的 `IEC 61131-3 FBD` 程序集合。
- 特点：比较人工测试、decision coverage 和 weak/strong mutation 三类方案，并以人工植入真实风格故障做评测。
- 规模：`61` 个程序，平均每个程序约 `828` 行 `FBD`、`22` 个 decisions、`11` 个输入、`5` 个输出；`33` 个程序被植入 `77` 个 faults。
- 模型：原程序与所有 mutants 聚合成一个 combined timed automata model，并由 mutation detection monitor 观察差异。
- 性质：谁能杀死更多现实风格 faults，谁的总成本更低。
- 方法：每个 faulty program 上重复运行 mutation/decision-coverage test generation，各 `10` 次、每次上限 `10` 分钟，再与工业人工测试对比。
- 结果：mutation-adequate test suites 比 coverage-based 更能发现 fault，但仍不如人工测试；成本却显著更低。

`工业 FBD 程序 -> mutant generation -> combined UPPAAL model -> mutation monitor -> 自动生成测试 -> 与人工测试对照`

## 论文定位

这篇论文虽以 testing 为主，但验证对象、工业场景、错误模式和评估口径都很具体，因此仍属于 `🎛️ + 🚦` 的高价值应用条目。它更像“工业测试与形式化验证结合”的案例，而不是纯算法论文。

## 验证对象与问题背景

### 系统与场景

对象是铁路 `TCMS` 项目中的 `IEC 61131-3 FBD` 程序。程序已部署在运营列车上，人工测试在开发流程中已经长期使用。

### 系统组成与运行机制

论文不是聚焦某一个单一子系统，而是把一组真实控制程序作为被测对象。每个程序都运行在典型 PLC scan-cycle 语义下，并依赖逻辑块、比较块、计时块和连接关系完成控制功能。

### 验证边界

论文验证的是单元级测试生成与 fault detection 能力，不验证整车系统级运行安全，也不直接分析物理过程。

### 核心问题

1. 高 code coverage 并不自动等于高 fault detection。
2. `IEC 61131-3` 这类领域特定语言缺乏成熟 mutation testing 工具。
3. 人工测试可能更强，但成本高且难规模化。

## 模型与形式化建模

### 抽象对象

作者延续已有 `FBD -> TA` 翻译框架，再在其上增加变异测试层：

1. 原程序模型
2. 多个 mutant 模型
3. mutation detection monitor
4. 目标 reachability 性质

### 建模形式

核心创新是 combined model：把原程序与全部 mutants 聚到同一个 `UPPAAL` 模型中，而不是为每个 mutant 单独跑一遍模型检查。

### 关键抽象与取舍

1. 采用 mutation operators 模拟工业常见错误。
2. 用 single combined model 减少重复模型检查代价。
3. weak/strong mutation 都做，便于和人工测试、decision coverage 比较。

## 验证目标与性质

### 待验证问题

1. mutation-adequate test suites 是否比 decision-coverage suites 更能发现人工植入 faults。
2. mutation-adequate suites 是否比人工测试更便宜。
3. 哪些类型的 faults 仍然只有人工测试能稳定抓到。

### 性质类型

- 变异可区分性
- fault detection score
- 测试成本

### 性质分组与实际含义

1. `WM/SM`
   - 用 mutants 作为 fault proxy 生成测试。
2. `DC`
   - 基于 decision coverage 的自动测试。
3. `MAN`
   - 工程师按自然语言规格编写的人工测试。

## 核心方法与验证流程

1. 对每个原始 `FBD` 程序生成 mutants。
2. 将原程序与 mutants 聚合成 combined timed automata model。
3. 用 monitor 为每个 mutant 生成可达性性质。
4. 调用 `UPPAAL` 输出 weak/strong mutation test suites。
5. 对同一批 faulty programs 再生成 decision-coverage suites，并收集人工测试。
6. 在 `77` 个人工植入 faults 上执行所有测试并统计 fault detection 与成本。

## 案例与结果

### 工业数据集

1. `61` 个来自 Bombardier 的 `TCMS` 程序。
2. 平均每个程序约 `828` 行 `FBD`、`22` 个 decisions、`11` 个 inputs、`5` 个 outputs。
3. `4` 位工程师在 `33` 个程序上人工植入 `77` 个 faults。

### fault detection

图 `4` 给出的平均结果为：

1. `MAN`：`89.6%`
2. `SM`：`83.4%`
3. `WM`：`80.1%`
4. `DC`：`71.5%`

作者进一步指出，有 `8` 个 faults 能被人工测试稳定发现，但 strong mutation 测试无法覆盖。这些缺口主要来自：

1. 多重改动的 higher-order faults。
2. feedback loop insertion。
3. extra logical block insertion。
4. non-boundary constant replacement。

### 成本

作者访谈了 `3` 位工程师，估算：

1. 每个 test case 创建 `6.6` 分钟。
2. 执行 `3.3` 分钟。
3. 结果检查 `2.5` 分钟。

综合结果显示：

1. `WM` 平均比人工测试少约 `110` 分钟。
2. `SM` 平均比人工测试少约 `115` 分钟。
3. 自动测试整体成本显著低于人工测试。

### 结果解释

mutation testing 并没有全面击败人工测试，但它显著降低了成本，并在 fault detection 上明确优于单纯 decision coverage，这正是它在工业流程里的现实意义。

## 与本研究的关系

### 相关性分析

这篇论文对博士研究有两点直接价值：一是说明工业控制程序可以稳定地进入形式模型；二是说明“验证场景/测试场景生成”完全可以成为闭环的一部分。

### 可借鉴之处

1. 用 combined model 而不是逐 mutant 重跑。
2. 将人工植入现实风格 faults 作为评价基准，而不是只看 mutation score。
3. 从实验结果反推需要补充哪些 mutation operators。

### 存在的不足与改进空间

1. 仍然偏单元级。
2. 工业程序与测试资产不公开。
3. 作者自己也承认需要引入更好的 mutation operators 与 higher-order mutation。

### 对本研究的启发

如果后续要研究“LLM 生成模型后，如何自动生成更有效的验证场景”，这篇论文提醒一个关键点：不能只看结构覆盖，必须让场景尽量贴近真实缺陷模式。

## 重要的相关工作

### 1. `CompleteTest`

- 本文沿用作者此前的 `CompleteTest` 自动测试生成工具链。

### 2. mutation operators for IEC 61131-3

- 论文最后专门新增了 `FIO/LIO/LDO` 等更贴近 PLC 现实缺陷的 operator 建议。

### 3. 工业人工测试

- 人工测试在本文不是背景板，而是核心对照基线，直接决定结论的现实意义。

## 案例、模型与数据公开情况

- 可获取性判断：🔒 难以取得
- 判断依据：论文公开，但数据集、faulty programs、人工测试集和 Bombardier 工程环境均未公开。
- 获取方式/链接：[DOI](https://doi.org/10.1007/978-3-319-47443-4_10)
- 对后续复用的现实影响：非常适合借鉴其评测设计和 combined-model 思路，但若要完全复现，必须自行准备 PLC 程序集和现实风格 fault set。

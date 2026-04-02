问题一句话：本文验证的是 `EAST-ADL2` 描述的 Brake-by-Wire 架构，核心问题是如何在架构层就把功能块内部行为形式化出来，并据此验证安全、时序和 bounded response 需求。
方法一句话：作者把 `EAST-ADL2` 的 analysis functions 映射到 `SAVE-CCM` 组件，再为每个功能块分配 `UPPAAL-PORT` timed automata，通过组合模型检查验证功能和质量属性。
验证收获一句话：结果表明该方法可以在架构早期对 Brake-by-Wire 系统的 `28` 条性质做自动验证，包括 deadlock freedom、数据流 leads-to、局部执行时间与 bounded response 约束。

## 基本信息

- 标题：Verifying functional behaviors of automotive products in EAST-ADL2 using UPPAAL-PORT
- 中文标题：使用 `UPPAAL-PORT` 验证 `EAST-ADL2` 汽车产品的功能行为
- 作者：Eun-Young Kang、Pierre-Yves Schobbens、Paul Pettersson
- 单位：University of Namur；MDH PROGRESS Research Centre, Mälardalen University
- 发表：`SAFECOMP 2011`
- DOI：`10.1007/978-3-642-24270-0_18`
- 链接：[DOI](https://doi.org/10.1007/978-3-642-24270-0_18)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🚦 交通、车载与铁路
- 被验证系统：`EAST-ADL2` analysis level 下的 Brake-by-Wire System (`BWS`) 架构模型
- UPPAAL线：`UPPAAL PORT`
- 代码/模型/仓库获取方式：论文未给出完整 `Papyrus`/`SAVE-CCM`/`UPPAAL-PORT` 工程下载入口。
- 案例/数据获取方式：案例来自 `ATESST2` 项目的 Brake-by-Wire system design；正文给出功能块、端口、假设和代表性性质。

## 简报

这篇论文解决的是 `EAST-ADL2` 架构语言“只描述结构、不描述功能块内部行为”这一缺口。作者的做法是把 analysis function 的内部执行语义补成 timed automata，然后再把整个架构做成可验证网络。

- 系统：Brake-by-Wire 架构级模型。
- 特点：从汽车架构语言出发、关注 analysis level、强调早期设计阶段的形式验证。
- 规模：核心部件包括 environment、device sensor、brake calculator/controller、wheel speed、vehicle speed、`ABS` 和 actuator，共验证 `28` 条性质。
- 模型：`EAST-ADL2 -> SAVE-CCM -> UPPAAL-PORT` 组件化 timed automata 网络。
- 性质：deadlock freedom、数据流 leads-to、状态互斥、局部执行时间和 bounded response。
- 方法：给每个 `AnalysisFunction` 指定行为自动机，再把连线与端口映射为组件交互。
- 结果：选取的全部性质均验证成功，文中报告平均每条性质约 `2 s` 即可得到结果。

`EAST-ADL2 架构 -> SAVE-CCM 组件 -> UPPAAL-PORT 行为自动机 -> 功能/质量属性形式化 -> 架构级模型检查`

## 论文定位

这是一篇很明显偏“架构建模方法”的应用论文，但它用的不是抽象 benchmark，而是真实的 Brake-by-Wire 设计。因此它在 `uppaal_apps/` 中更适合被视为“应用驱动的架构验证案例”。

## 验证对象与问题背景

### 系统与场景

对象是汽车 Brake-by-Wire System。在该系统中，制动功能由多个 analysis functions 通过端口和触发关系协作实现，早期设计阶段就需要保证这些功能块之间的行为约束不会冲突。

### 系统组成与运行机制

论文列出的关键组件包括：

1. `Environment`
2. `DeviceSensor`
3. `BCC` (`Brake calculator and controller`)
4. `WheelSpeed`
5. `VehicleSpeed`
6. `ABS`
7. `Actuator`

功能块采用 run-to-completion 假设：读取输入端口、执行本地计算、写回输出端口。

### 验证边界

论文验证的是 analysis level 架构及其功能行为，不涉及后续更具体的软件实现、硬件部署或完整车辆动力学。

### 核心问题

1. `EAST-ADL2` 原生不提供足够细的块内部行为定义；
2. 缺少块内部行为时，很难对整个系统执行统一模型检查；
3. 需要同时验证功能属性和 timing / response 这类 quality 属性。

## 模型与形式化建模

### 抽象对象

作者把每个 `AnalysisFunction` 定义为带输入端口、输出端口、触发端口、内部变量和本地时钟的行为元组，再把它映射成 `UPPAAL-PORT` timed automaton。

### 建模形式

模型链条分成三层：

1. `EAST-ADL2`
   - 表示结构、端口和需求；
2. `SAVE-CCM`
   - 表示组件与连线框架；
3. `UPPAAL-PORT`
   - 表示每个功能块的内部 timed automaton 和整个系统组合行为。

### 关键抽象与取舍

1. 采用 run-to-completion 语义；
2. 假设函数周期触发且相互不同步；
3. 以 observer automaton 的方式补充 bounded response 验证。

## 验证目标与性质

### 待验证问题

论文展示的代表性性质包括：

1. `A[] not deadlock`
2. 环境触发后最终执行 `ABS` 并根据各速度与踏板信息计算制动力；
3. `BrakePedal` 的端口值最终传到 `BrakeController`；
4. `BCC`、`WheelSensor`、`VehicleSensor` 的若干执行状态应互斥；
5. 每个功能块执行时间需满足本地上界，例如 `clock <= 2`。

### 性质类型

这些性质覆盖：

1. 安全；
2. 活性；
3. deadlock freedom；
4. bounded response；
5. 局部执行时间。

### 查询表达

文中给出的查询包括：

1. `A[] not deadlock`
2. `(C1.BrakePedal and C1.EBPP==1) -> (C3.BrakeCtr and C3.BCCin==1)`
3. `A[] C7.exec ==> (C7.clock <= 2 and C7.clock >= 0)`

这些都很明确地对应了系统中的数据传播和 timing 约束。

## 核心方法与验证流程

1. 将 `BWS` 的 `EAST-ADL2` analysis model 翻译为 `SAVE-CCM` 组件图；
2. 为各 `AnalysisFunction` 手工指定 `UPPAAL-PORT` 行为自动机；
3. 把需求文本和 timing constraints 形式化成 `UPPAAL` 逻辑；
4. 对普通安全/活性性质直接做模型检查；
5. 对 bounded response 性质引入 observer automata 辅助验证。

## 案例与结果

### 代表性结果

论文报告到当时已验证 `28` 条性质，并列出若干选例均为 `valid`。这些性质覆盖 deadlock freedom、数据流传播、状态对应关系和执行时间。

### 性能

作者给出的实验环境是一台 Intel `T9600 2.80 GHz` 机器，平均每条性质约 `2 s` 就能完成验证。对架构级分析而言，这个速度足以支持交互式设计迭代。

### 方法意义

这项工作的价值在于：它让 `EAST-ADL2` 不再只是结构建模工具，而能够在早期阶段就承载正式行为验证。

## 与本研究的关系

### 相关性分析

这篇论文与博士研究第一部分“从需求/架构到状态机建模”直接相关，因为它处理的正是“如何给架构元素补上形式行为”。

### 可借鉴之处

1. 用统一的函数块行为模板消除架构语言中的语义空洞。
2. 将功能需求和质量需求统一映射到同一模型检查流程。
3. 对 bounded response 用 observer 补强，而不是把所有约束都硬塞进主模型。

### 存在的不足与改进空间

1. 更偏手工定义行为模板，自动化还有限。
2. 主要停留在 analysis level，没有走到实现部署层。
3. 原始工程和模型未公开，复现成本较高。

### 对本研究的启发

对博士研究而言，这篇论文说明：如果原始语言或需求只给了结构骨架，后续自动建模的关键不是“全文重写”，而是先为最基本的功能块定义可组合的行为语义模板。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文公开，但未见 `Papyrus` 模型、`SAVE-CCM` 工程或 `UPPAAL-PORT` 自动机仓库。
- 获取方式/链接：[DOI](https://doi.org/10.1007/978-3-642-24270-0_18)
- 对后续复用的现实影响：很适合复用其架构到自动机的映射思路和 observer 验证方式，但具体案例需要按正文重建。

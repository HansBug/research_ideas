问题一句话：本文验证的是一个真实感较强的航电任务系统的组合式可调度性，核心问题是当多个航电组件共享 CPU 与通信资源时，单核平台是否还能保证全部任务不丢 deadline。
方法一句话：作者使用参数化 stopwatch automata、非确定性 supplier 与 `SIRAP` 资源共享协议，在 `UPPAAL` 中把可调度性转写为 `error` 状态不可达的 reachability/safety 问题。
验证收获一句话：论文在 `15` 任务、`4` 组件的航电 mission control computer 案例上证明 `Fire and Stores` 组件本身就不可在单核上调度，从而推得整机也不可调度。

## 基本信息

- 标题：Compositional Schedulability Analysis of An Avionics System Using UPPAAL
- 中文标题：使用 `UPPAAL` 的航电系统组合式可调度性分析
- 作者：Abdeldjalil Boudjadar、Jin Hyun Kim、Kim G. Larsen、Ulrik Nyman
- 单位：Aalborg University，Institute of Computer Science
- 发表：ICAASE 2014 / CEUR Workshop Proceedings Vol. 1294
- DOI：原文未提供
- 链接：[CEUR PDF](https://ceur-ws.org/Vol-1294/paper16.pdf)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🚀 航天
- 被验证系统：航电 mission control computer 的层次化实时任务系统
- UPPAAL线：`UPPAAL` + `UPPAAL SMC`
- 代码/模型/仓库获取方式：论文公开，但未给出当前可直接获取的完整 `UPPAAL` 模型与查询文件。
- 案例/数据获取方式：任务与组件定义来自文中 avionics case study，需要按表格和架构图重建。

## 简报

本文是一个很“应用化”的 schedulability 案例：作者拿一个假想但结构具体的航电 mission control computer，按功能拆成多个组件，再用组合式供应合同分析每个组件和整机是否还能在单核 CPU 上运行。

- 系统：`15` 个航电任务组成的 mission control computer。
- 特点：层次化组件、具体 timed actions、共享输入/输出资源、`SIRAP` 资源共享协议。
- 规模：`4` 个组件，分别含 `4 + 6 + 3 + 2` 个任务；任务时间参数按毫秒给出，分析时转换到微秒。
- 模型：任务模板、supplier 模板、CPU 模板和 `SIRAP` 资源协议模板。
- 性质：任何任务都不应进入 deadline miss；组件预算必须足够；顶层组合仍应可调度。
- 方法：先用 `SMC` 猜测 supplier 预算，再用符号模型检查确认 `A[] error!=1`。
- 结果：`Fire and Stores` 组件在单核上不可调度，整机 CPU 利用率超过 `100%`，因此顶层也不可能可调度。

`航电任务表/组件架构 -> supplier + task/resource PSA -> 组件级 schedulability -> 顶层接口合成 -> 不可调度反例`

## 论文定位

这篇论文虽然建立在框架工作之上，但真正落脚点是一个具体航电案例，因此比纯框架论文更像正式应用条目。它很好地展示了 `UPPAAL` 在“任务系统级验证”上的工程解释能力。

## 验证对象与问题背景

### 系统与场景

对象是一个面向 combat/attack aircraft 的 mission control computer。系统包含武器释放、雷达跟踪、导航、显示和内建测试等任务。

### 系统组成与运行机制

文中把 `15` 个任务分成 `4` 个组件：

1. `Control and Display`：`4` 个图形/显示相关任务。
2. `Sensor and Navigation`：`6` 个导航与外部传感任务。
3. `Fire and Stores`：`3` 个武器与火控任务。
4. `Background`：`2` 个后台检查与轨迹更新任务。

任务之间还会竞争输入/输出通信资源，资源分配通过 `SIRAP` 协议管理。

### 验证边界

论文只验证任务级可调度性与共享资源争用，不覆盖更上层战术逻辑或物理飞行动力学。

### 核心问题

作者要回答：

1. 每个组件在给定 supplier 预算下是否可调度。
2. 即便组件独立看起来合理，整机在单核上是否仍可能超载。

## 模型与形式化建模

### 抽象对象

任务行为由 timed actions 列表给出，可包含 `COMPUTE`、`LOCK SIRAP`、`UNLOCK SIRAP` 等指令。组件则由预算、周期、本地调度策略和子实体构成。

### 建模形式

作者使用 `Parameterized Stopwatch Automata`。任务在 `Executing` 位置运行时 stopwatch 递增；supplier 在周期内非确定性分块提供 CPU；资源共享则由 `SIRAP` 自动机负责。

### 关键抽象与取舍

1. 顶层不直接细化别的组件内部行为，只消费其接口预算。
2. 非确定性 supplier 用来保守模拟“其它组件何时占用 CPU”的影响。
3. deadline miss 被统一规约为进入 `MissDeadline/Error` 位置。

## 验证目标与性质

### 待验证问题

1. 各组件是否在其预算合同下可调度。
2. 顶层系统是否在单核 CPU 上可调度。
3. 共享资源协议是否会导致预算不足或 deadline miss。

### 查询表达

论文核心查询是：

`A[] error != 1`

为了寻找预算候选，还会先借助 `UPPAAL SMC` 试探 supplier 配置，再用符号模型检查确认。

### 性质分组与实际含义

1. deadline 满足：没有任务 miss deadline。
2. 预算可接受性：supplier 至少要给够多少资源。
3. 资源共享正确性：`SIRAP` 不应把任务拖到预算外。

## 核心方法与验证流程

1. 从任务表提取周期、执行时间、优先级、输入/输出消息。
2. 将任务按功能聚成四个组件，并给每个组件配置本地 `FPS`。
3. 为每个组件引入非确定性 supplier。
4. 用 `SMC` 找 supplier budget candidate。
5. 用 `UPPAAL` 确认 `A[] error!=1` 是否成立，并分析反例。

## 案例与结果

### 案例规模

1. `15` 个任务。
2. `4` 个组件。
3. 共享输入与输出通信资源。

### 关键结果

1. 组合式分析表明：各组件中只有 `Fire and Stores` 在单核平台上不可调度。
2. 顶层航电系统在任何调度策略 `S` 下都不可能在单 CPU 上可调度。
3. 原因是整体 CPU 利用率已超过 `100%`，论文给出的是 `75% + 69% + 4.4%` 级别的累加压力。
4. `UPPAAL` 反例能进一步指出 `Fire and Stores` 中哪类任务在何种情景下 miss deadline。

## 与本研究的关系

### 相关性分析

这篇论文对博士研究很重要，因为它展示了如何从结构化系统描述一路走到“哪个组件/哪类任务出了问题”的反例级解释。

### 可借鉴之处

1. 用组件接口和反例把全局问题定位回局部组件。
2. 把 deadline 违例统一转成 reachability。
3. 资源共享协议也可以直接作为状态机模块纳入验证，而非前置假设。

### 存在的不足与改进空间

论文没有公开完整模型，且结论主要停留在“不可调度”层面，没有进一步给出修复后新配置。

### 对本研究的启发

它提醒我们：面向控制系统状态机的验证不应只停留在“通过/不通过”，最好还能把违例直接投影回局部组件或参数配置。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文公开，但未见稳定的 `UPPAAL` 模型、任务配置文件或 `SIRAP` 查询包下载入口。
- 获取方式/链接：[CEUR PDF](https://ceur-ws.org/Vol-1294/paper16.pdf)
- 对后续复用的现实影响：案例非常适合做层次化调度样本，但复跑需要手工重建组件与任务表。

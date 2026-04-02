问题一句话：本文验证的是多核平台上受限抢占并行实时应用的可调度性，核心问题是怎样对周期性 `DAG` 任务给出精确而非保守的 schedulability 与 response-time 分析。
方法一句话：作者将 limited-preemptive parallel applications 建成 `UPPAAL` timed automata，包括任务模板和全局固定优先级调度器，并直接用可达性与上确界查询求不可调度反例和响应时间界。
验证收获一句话：论文给出了一条可作为 ground truth 的精确分析链，说明单核实例在严格 `250 s` 超时下大多可处理，多核与更高并行度则显著推高分析成本，但仍足以用作现有充分性分析的对照基准。

## 基本信息

- 标题：Exact Schedulability Analysis for Limited-Preemptive Parallel Applications Using Timed Automata in UPPAAL
- 中文标题：基于 `UPPAAL` timed automata 的受限抢占并行应用精确可调度性分析
- 作者：Jonas Hansen、Srinidhi Srinivasan、Geoffrey Nelissen、Kim G. Larsen
- 单位：Aalborg Universitet；Eindhoven University of Technology
- 发表：2025 Design, Automation and Test in Europe Conference (DATE)，2025
- DOI：`10.23919/DATE64628.2025.10992936`
- 链接：[DOI](https://doi.org/10.23919/DATE64628.2025.10992936)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🏭 工业与基础设施
- 被验证系统：多核平台上采用全局固定优先级调度的受限抢占并行 `DAG` 任务系统
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文未给出独立仓库；论文主要公开建模思想、查询和随机任务集生成设置。
- 案例/数据获取方式：案例为论文生成的 periodic limited-preemptive parallel task sets，需按正文参数重建。

## 简报

这篇论文的应用对象不是一个具体工业设备，而是一类非常典型的实时软件系统：在多核平台上运行、支持并行段、但只允许在段边界抢占的实时任务集。作者的重点是建立一条“精确分析”基线，用它去判断已有充分性分析到底保守到什么程度。

- 系统：受限抢占的周期性并行 `DAG` 任务集。
- 特点：段内非抢占、段间可抢占、全局固定优先级、存在 best/worst-case execution time 与 release offset。
- 规模：实验中随机生成 `4/8/12` 个任务，单任务最多 `20` 个 segments；核心数取 `1` 或 `2`。
- 模型：任务自动机 + 调度器自动机 + ready-set / active-core 联合状态。
- 性质：deadline miss 可达性、最坏/最好响应时间界。
- 方法：把 schedulability 判断变成 `UPPAAL` 查询，再以 depth-first / breadth-first 配置区分“找反例”和“证可调度”。
- 结果：单核大多数实例可在严格超时内完成；多核和更频繁 blocking 会显著增大运行时间，但方法足以做 benchmark。

`并行 DAG 任务集 -> 任务/调度器 timed automata -> 不可调度可达性查询 + 响应时间上确界查询 -> 为充分性分析提供精确对照`

## 论文定位

它是很典型的 `⏱️` 主轴论文。正文真正验证的不是应用业务逻辑，而是“并行任务在给定调度策略下是否赶得上 deadline”。由于论文更像分析框架和 benchmark，而不是单个工程系统案例，所以必须明确标成 `🟡`：它属于应用类，但应用对象是“实时并行任务系统”这一类软件执行对象，而不是具体装置。

## 验证对象与问题背景

### 系统与场景

系统由一组周期性 limited-preemptive parallel `DAG` tasks 构成，运行在多核平台上，采用 work-conserving global fixed-priority scheduling。

### 系统组成与运行机制

1. 每个任务由多个 execution segments 组成。
2. 段间的先后关系由 `DAG` 表示。
3. 每段执行时不可被更高优先级任务打断。
4. 只有在段结束、即 preemption point 处才能切换任务。

### 验证边界

论文验证的是**调度与响应时间层**，不涉及具体应用代码语义，也不分析更高层功能正确性。其价值在于给 schedulability 工具提供精确 ground truth。

### 核心问题

1. 现有充分性分析可能把可调度系统误判为不可调度。
2. 多核并行 `DAG` 加上 limited-preemption 后，精确分析很难做且容易爆炸。
3. 若没有精确基准，就很难衡量其他分析到底保守多少。

## 模型与形式化建模

### 抽象对象

作者分别为任务与调度器建模，再通过同步把运行、完成和 ready 状态连接起来。

### 关键模型组件

1. **Task automata**
   - 表达 release、waiting、active、segment completion。
2. **Scheduler automaton**
   - 维护空闲核心、ready 任务和段完成后的重新分配。
3. **局部时钟**
   - `tp` 用于相对 deadline 检查，`response` 用于响应时间界。

### 关键抽象

论文保留了：

1. 最好/最坏执行时间；
2. 优先级；
3. release offset；
4. 段级 non-preemption；
5. 多核资源分配。

## 验证目标与性质

### 待验证问题

1. 是否存在任务在 active 状态时超过相对 deadline。
2. 各任务最坏响应时间和最好响应时间是多少。

### 性质类型

1. 调度安全性质。
2. 可达性反例性质。
3. 响应时间上界/下界分析。

### 查询表达

论文给出三类关键查询：

1. 不可调度反例：
   `E<> exists (i : id_t) Task(i).Active && tp > Task(i).deadline()`
2. 最坏响应时间：
   `sup{Task(i).Active}: Task(i).response`
3. 最好响应时间：
   `inf{Task(i).Waiting}: Task(i).response`

### 判定边界与前提

结论建立在 periodic tasks、constrained deadlines、global fixed-priority 和有限核心数等前提下。

## 核心方法与验证流程

1. 用 timed automata 形式化任务和调度器。
2. 先用 deadline miss 可达性查询检验是否不可调度。
3. 若不存在反例，再进一步计算响应时间界。
4. 将该精确分析与 `SAG` 等充分性分析结合，用来确认“潜在不可调度”是否真实存在。

作者特别指出：

1. 要找反例时，`depth-first search` 更适合；
2. 要证明可调度时，`breadth-first search` 更高效。

## 案例与结果

### 案例规模

论文的可扩展性实验使用随机任务集：

1. 任务数 `N ∈ {4, 8, 12}`；
2. 核心数 `M ∈ {1, 2}`；
3. 每任务最多 `20` 个 segments；
4. 总利用率约 `30%`；
5. 单组实验 timeout 设为 `250 s`。

### 主要结果

1. 单核分析在严格 `250 s` 限制内处理了几乎所有问题实例。
2. 增加任务数会明显拉高分析时间。
3. 单核情形中，segment 数增加的影响相对有限。
4. 双核情形下，任务数和 segment 数都会更显著地推高运行时间。
5. 不可调度实例往往比可调度实例更快结束，因为找到一个 counter-example 即可停止。

### 结果解释

这说明该方法未必适合大规模日常调度分析，但非常适合作为“精确 benchmark”去校准其他更快但更保守的分析器。

## 与本研究的关系

### 相关性分析

这篇论文与博士研究的关系在于：它把“任务调度系统”也视为一种可形式化的状态机对象，并用查询直接表达 deadline 和 response-time 性质。

### 可借鉴之处

1. 把工程需求直接写成 `UPPAAL` 查询。
2. 区分“找反例”和“证正确”的求解策略。
3. 用精确模型给其他快速分析提供对照基线。

### 存在的不足与改进空间

1. 更偏框架/benchmark，具体应用业务语义较弱。
2. 多核与高并行度下的状态空间仍然很重。
3. 原文未公开可直接运行的模型仓库。

### 对本研究的启发

对博士研究而言，这篇论文提示：当状态机验证对象是调度系统时，可以把 deadline miss、响应时间界和反例轨迹组织成一组稳定的验证剖面，而不仅是写成“可调度/不可调度”标签。

## 重要的相关工作

### 1. 受限抢占并行任务分析

- 论文把自己的 `UPPAAL` 精确分析定位为现有充分性分析方法的 benchmark。

### 2. `SAG` 分析工具

- 作者使用 `Schedule Abstraction Graph` 作为对照对象，检验其“潜在不可调度”判断是否真的能由精确模型复现。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：可稳定获取论文 PDF，但正文未提供独立 `UPPAAL` 模型、查询文件或任务集仓库。
- 获取方式/链接：[DOI](https://doi.org/10.23919/DATE64628.2025.10992936)
- 对后续复用的现实影响：适合作为并行实时任务 schedulability 建模模板复现，但需按论文自行重建任务生成器和模型。

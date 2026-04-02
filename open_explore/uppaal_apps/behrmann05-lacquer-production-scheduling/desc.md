问题一句话：本文验证的是工业漆料生产调度问题，核心问题是在并行资源、工序间时距约束和工作时段限制同时存在时，能否用 `UPPAAL` 的可达性分析直接合成可行 schedule。
方法一句话：作者把 Axxom 提供的 lacquer production case 建成 timed automata 网络，用 reachability analysis 搜索可行排程，再用 `UPPAAL CORA` 把 storage / delay / setup cost 一并纳入成本最优分析。
验证收获一句话：论文表明在合适启发式下，`29`、`73`、`219` 个订单的基础实例都能快速求得可行调度，其中 `219` 单场景在 `4` 秒内完成；扩展到成本和精确 working-hours 后，模型仍能给出与工业方竞争力相当的排程。

## 基本信息

- 标题：Production Scheduling by Reachability Analysis - A Case Study
- 中文标题：通过可达性分析进行生产调度：一个案例研究
- 作者：Gerd Behrmann、Ed Brinksma、Martijn Hendriks、Angelika H. Mader
- 单位：Aalborg University；University of Twente；Radboud University Nijmegen
- 发表：`Workshop on Parallel and Distributed Real-Time Systems (WPDRTS 2005)`，2005
- DOI：`10.1109/IPDPS.2005.363`
- 链接：[DOI](https://doi.org/10.1109/IPDPS.2005.363)
- 主轴分类：⏱️ 调度、资源与性能分析
- 次轴场景：🏭 工业与基础设施
- 被验证系统：Axxom 提供的 lacquer production job-shop 风格生产调度问题
- UPPAAL线：`UPPAAL` + `UPPAAL CORA`
- 代码/模型/仓库获取方式：论文 PDF 可公开获取；原文提到 `AMETIST` 项目站收录了相关技术材料，但当前未确认有稳定可访问的独立 `UPPAAL` 模型包。
- 案例/数据获取方式：论文直接给出了 `uni/metallic/bronce` 三类 recipe、资源类型、实例规模、启发式和实验结果，可按正文重建基础案例。

## 简报

这篇论文验证的是一个很典型但又不容易直接套经典调度公式的工业案例。对象是 Axxom 提供的漆料生产场景，既像 job-shop scheduling，又带有额外的工序间最大间隔、并行资源占用、人员工作时段、清洗切换和提前/延迟成本，因此作者选择把它直接映射为 timed automata 网络来做可达性分析和成本优化。

- 系统：Axxom 提供的 lacquer production scheduling case。
- 特点：三类配方、并行资源使用、工序间最大等待时间、availability/performance factor、后续还加入 setup/storage/delay cost。
- 规模：基础实例包含 `29`、`73`、`219` 个订单；订单使用 `uni`、`metallic`、`bronce` 三类 recipe；其中 `5` 类资源用计数器建模，其余资源用小型 automata 建模。
- 模型：每个订单一个 recipe automaton，外加资源 automata，共同形成 unscheduled system；扩展模型再加入 working-hours、清洗切换和 `cost` 导数。
- 性质：订单能否在 due date 前全部完成、成本是否最优、working-hours 与资源竞争下是否仍存在可行调度。
- 方法：`unscheduled timed automata network -> reachability property -> heuristics 削减搜索空间 -> feasible schedule`；扩展版再转到 `UPPAAL CORA` 做 cost-optimal reachability。
- 结果：基础实例在合适启发式下可快速求解，`29`/`73` 单案例可在 `1` 秒内完成，`219` 单案例约 `3.46s`；扩展版即便引入精确 working-hours 和 cost，仍能找到与工业方相当甚至更低成本的调度。

`工业排程描述 -> recipe / resource timed automata -> reachability 查询 -> 启发式裁剪搜索空间 -> 可行或低成本 schedule`

## 论文定位

这是一个强 `⏱️ + 🏭` 条目。论文的中心不是 `UPPAAL` 算法本体，而是一个真实工业排程对象如何被形式化并求解。它同时跨越了经典 `UPPAAL` 的 feasibility checking 和 `UPPAAL CORA` 的 cost-optimal reachability，是文库里较早、较完整的“排程对象直接入模”案例。

## 验证对象与问题背景

### 系统与场景

对象是工业漆料生产调度问题。Axxom 作为工业合作方提供了来自 value chain management 背景的案例描述，目标是在多订单并发时为三类漆料 recipe 生成满足时限的生产 schedule。

### 系统组成与运行机制

每个订单对应一条 recipe，recipe 规定：

1. 需要经过哪些 processing steps。
2. 每一步需要哪些资源。
3. 处理时间是多少。
4. 相邻步骤间允许的最大等待时间是多少。

系统中的典型资源包括 mixing vessels、dose spinners、filling lines 等。与普通 job-shop 不同，这个案例还有两个额外难点：

1. 某些步骤之间有显式时间约束。
2. 一个订单在执行时可能需要并行占用多个资源，例如 mixing vessel 会和其他资源一起长期占用。

### 验证边界

论文验证的是生产调度抽象模型，而不是车间控制软件或连续物理化学过程本身。它关注的是“有没有可行排程”和“排程代价是否可优化”，而不是设备底层实现。

### 核心问题

1. 工业方给出的案例并不是标准 job-shop，需要先把 recipe、资源和时间约束整理成可形式化表达的结构。
2. 直接做 reachability analysis 容易遭遇状态空间爆炸。
3. 当加入 setup time、storage cost、delay cost 和精确 working-hours 后，普通 feasibility 已经不足以表达实际优化目标。

### 研究动机

作者想证明 timed automata 不只是验证协议和控制器，也可以直接承载复杂调度问题；同时相比传统专用排程算法，模型在参数和需求变化下更稳健、更容易重构。

## 模型与形式化建模

### 抽象对象

模型把每个订单抽象为一个 recipe automaton，把共享设备抽象为资源计数器或小型资源 automata，并通过并行组合保留订单间的资源竞争与时间推进。

### 建模形式

基础版本使用普通 `UPPAAL` timed automata network：

1. 每个 recipe 被拆成一串 processing-step fragments。
2. 每个 step 进入时抢占资源，执行期间让时钟推进，完成后释放资源。
3. 订单 automata 与资源 automata 共同组成 unscheduled model。

扩展版本使用 `UPPAAL CORA`：

1. 把 delay/storage cost 表示为 `cost` 的导数。
2. 把 filling line 的清洗切换时间与成本显式建模。
3. 进一步用单独 automaton 处理 exact working-hours constraint。

### 关键抽象与取舍

1. 基础版先用 availability factor 近似表示工作时段限制，适合 long-term scheduling。
2. performance factor 不是主线分析重点，而是留给后续 stochastic analysis。
3. 为控制状态空间，论文显式加入 non-overtaking、non-laziness、greediness、限制 active jobs 数量等启发式。

## 验证目标与性质

### 待验证问题

论文分两层处理：

1. **基础可行性问题**
   - 是否存在一个 schedule，使全部订单在 due date 前完成。
2. **扩展成本问题**
   - 在考虑 setup / storage / delay / working-hours 后，是否能找到成本更低的可行 schedule。

### 性质类型

这些性质主要属于：

1. 可达性与 deadline 满足。
2. 资源竞争下的排程可行性。
3. 成本最优性与性能优化。

### 查询表达

基础版本的核心是 reachability property：

1. 所有表示订单的 automata 都能到达 final state。
2. 进入 final state 时 due date 尚未过去。

扩展版本则把 delay/storage cost 写成线性 priced timed automata 上的优化目标，由 `UPPAAL CORA` 搜索 cost-optimal reachable state。

## 核心方法与验证流程

1. 从工业方给出的非标准 recipe/资源描述中整理出统一表示法。
2. 为三类 recipe 建立 timed automata 模板。
3. 将资源表示为计数器或资源 automata，并与订单 automata 并行组合。
4. 先用 `UPPAAL` 做 feasibility reachability 分析。
5. 再逐步加入启发式，压缩搜索空间。
6. 对扩展案例加入 setup/storage/delay cost 与 exact working-hours。
7. 用 `UPPAAL CORA` 搜索低成本 schedule，并与工业方结果对比。

## 案例与结果

论文给出了很具体的实验结果：

1. 基础案例覆盖 `29`、`73`、`219` 个订单三种规模。
2. 在合适启发式下，`29` 和 `73` 订单场景可在 `1` 秒内完成，`219` 订单场景约 `3.46s`。
3. 限制 active jobs 数量和 non-overtaking 对大实例的效果尤其明显，可把时钟数降到 `3·A+3`。
4. 加入 storage / delay / setup cost 后，问题被转成 `UPPAAL CORA` 成本优化问题。
5. 加入 exact working-hours 后模型显著变大，但仍能找到与工业方竞争力相当的 schedule；部分实验中甚至得到约一半成本的解。
6. 论文还指出 availability/performance factor 更适合粗粒度长期规划，不适合直接生成精细短期排程。

## 与本研究的关系

### 相关性分析

它和博士研究中的“形式模型不仅用于验错，也可直接承载场景求解与需求回推”高度相关，尤其适合作为“状态机/时间自动机模型支撑生产调度与约束满足”的应用样本。

### 可借鉴之处

1. 先把工业 partner 的非标准业务描述整理成结构化 recipe，再进入形式化建模。
2. 将资源竞争、时间约束和成本目标统一放进同一个自动机框架。
3. 用启发式和建模模式共同控制状态空间，而不是只依赖工具本身。

### 存在的不足与改进空间

1. 模型强依赖人工加入启发式，尚不是推钮即用。
2. 工业方原始案例和模型包没有稳定公开，复现门槛较高。
3. availability/performance factor 的近似语义会影响调度解释。

### 对本研究的启发

这篇论文说明，对复杂工业案例来说，“先把业务对象压成统一的状态机骨架，再围绕可达性和代价逐层加细约束”是一条现实可行的路线；同时，启发式本身也应被看成验证流程中的一等对象。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文 PDF 可直接获取，但未见稳定公开的 `UPPAAL`/`UPPAAL CORA` 模型、查询文件或工业实例包；原文提到 `AMETIST` 项目站有相关技术材料，但当前公开工件入口不明确。
- 获取方式/链接：[DOI](https://doi.org/10.1109/IPDPS.2005.363)；[公开 PDF](https://sws.cs.ru.nl/publications/papers/martijnh/AXXOM/WPDRTS05.pdf)
- 对后续复用的现实影响：适合复用其 recipe-to-automata 建模和启发式裁剪思路，但要复跑工业案例仍需按正文自行重建模型与实例数据。

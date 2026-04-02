问题一句话：本文验证的是 NASA `Deep Space 1` Remote Agent 中 `HSTS` 规划/调度器的计划模型，核心问题是这些计划模型能否被翻译成 `UPPAAL` 并用于检查目标可达性与模型缺陷。
方法一句话：作者提出把 `HSTS DDL` 计划模型映射为 timed automata 的 `ddl2uppaal` 算法，并用 `UPPAAL` 查询和诊断轨迹来对照 `HSTS` 计划结果。
验证收获一句话：论文证明计划目标可以被转成 `UPPAAL` 性质、诊断轨迹可以对应 `HSTS` 计划，但也明确指出完整规划模型过大，现实上需要代表性抽象模型才能继续扩大应用。

## 基本信息

- 标题：Verification of Plan Models Using UPPAAL
- 中文标题：使用 `UPPAAL` 验证计划模型
- 作者：Lina Khatib、Nicola Muscettola、Klaus Havelund
- 单位：NASA Ames Research Center；QSS Group, Inc.；RECOM Technologies
- 发表：NASA Preprint / NTRS，2001
- DOI：原文未提供 DOI
- 链接：[NASA NTRS](https://ntrs.nasa.gov/citations/20010081322)
- 主轴分类：🧩 软件服务与业务流程
- 次轴场景：🚀 航空航天与国防
- 被验证系统：`Deep Space 1` Remote Agent 中 `HSTS` 规划/调度器的计划模型
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：原文未提供公开模型仓库，仅给出 NASA 预印本。
- 案例/数据获取方式：工业背景来自 `Deep Space 1` Remote Agent；正文展示的可复核示例为 `Rover/Rock` 计划模型。

## 简报

这篇论文的对象不是常见的协议或控制器，而是自治航天系统中的计划模型。作者想验证的不是某一条执行代码，而是 `HSTS` 规划器描述出来的高层计划约束能否被 `UPPAAL` 接管并检查，从而作为规划器自身的独立验证通道。

- 系统：`Deep Space 1` Remote Agent 的 `HSTS` 计划/调度模型。
- 特点：约束规划、连续时间、token/timeline 语义、目标可达性与计划轨迹对应。
- 规模：工业目标是 `DS1` 自治规划系统；文中核心演示案例是 `Rover/Rock` 两对象计划模型，其中 rover 状态域大小为 `4`，rock 状态域大小为 `2`。
- 模型：将 `DDL` 计划模型翻译为 `UPPAAL` timed automata，duration 变成 invariant/guard，时序关系变成同步信道。
- 性质：目标可达性、互斥谓词违规与模型不一致性检测。
- 方法：以 `ddl2uppaal` 为桥接，把 `HSTS` goal 映射为 `UPPAAL` 查询，把 `UPPAAL` 诊断轨迹映回 `HSTS` plan。
- 结果：方法在有限复杂度模型上可行，并能用 `UPPAAL` 检查计划目标与诊断轨迹；但作者承认完整真实规划模型仍需抽象。

`HSTS/DDL 计划模型 -> ddl2uppaal -> timed automata -> goal/property checking -> 计划轨迹对照`

## 论文定位

本文是一个明显带边界的 `🧩 + 🚀` 条目。它服务于真实航天自治系统，但正文更多是在展示“如何把计划模型映射到 `UPPAAL`”而不是完整工业级验证，因此应视为方法驱动但有明确应用背景的 `🟡 可整理` 案例。

## 验证对象与问题背景

### 系统与场景

被验证对象是 `HSTS`（Heuristic Scheduling Testbed System）计划模型。`HSTS` 是 Remote Agent 自治系统中的规划/调度器，曾用于 `Deep Space 1` 的自主控制实验。

### 系统组成与运行机制

在 `HSTS` 中：

1. 对象由若干 state variables / timelines 组成。
2. token 表示某状态持续的时间区间。
3. compatibilities 表示 token 间的持续时间与时序关系。
4. 给定 goal 后，规划器生成满足约束的 complete plan。

### 验证边界

本文验证的是**计划模型与目标在形式化模型中的一致性与可达性**，不是飞行控制器底层执行逻辑，也不是完整 `DS1` 自治系统的所有连续参数。

### 核心问题

`HSTS` 模型非常适合规划，但其连续时间和丰富时序约束不易直接套入传统模型检查工具；需要找到能保留关键约束的映射方案。

### 研究动机

作者希望用 `UPPAAL` 作为一个独立于规划器本身的验证引擎，检查计划模型是否存在缺陷，以及规划结果是否可由另一套推理机制复核。

## 模型与形式化建模

### 建模对象

1. `HSTS` 的 state variable / predicate
2. token duration 约束
3. token 之间的 meets / before 等时序关系
4. 目标谓词与诊断轨迹

### 模型形式

`ddl2uppaal` 算法的核心思想是：

1. 每个 `state variable` 映射为一个 `UPPAAL` automaton。
2. 每个 predicate 映射为 automaton 中的一个 location。
3. duration 约束映射为 local clock invariant / guard。
4. token 间的时序关系映射为同步信道或条件迁移。

### 关键抽象

1. 论文明确承认完整 `HSTS` 规划模型过于复杂，当前只适用于有限规模与复杂度。
2. `Rover/Rock` 示例用于解释映射细节，而非代表完整 `DS1` 工业模型。
3. 目标在 `UPPAAL` 中表达为 reachability 性质，诊断轨迹对应 `HSTS` 计划。

## 验证目标与性质

### 待验证问题

1. 给定 goal 是否存在满足约束的 complete plan。
2. 计划模型是否存在互斥谓词、不可达谓词或不完整约束。
3. `UPPAAL` 的诊断轨迹是否能作为 `HSTS` 计划的独立佐证。

### 性质类型

1. Reachability
2. 一致性 / 完整性检查
3. 计划目标可满足性

### 性质分组与实际含义

1. Goal satisfaction
   对应“规划目标在形式化模型中是否可达”。
2. Model sanity
   对应“模型中是否存在互斥冲突或约束缺口”。
3. Plan-to-trace consistency
   对应“`UPPAAL` 轨迹能否映回 `HSTS` 计划”。

### 查询表达

论文在 `Rover/Rock` 示例中把目标写成：

`E<> Rock.withRover`

其输出诊断轨迹为：

`(Rover.atS, Rock.atL) -> (Rover.gotoRock, Rock.atL) -> (Rover.getRock, Rock.atL) -> (Rover.gotoS, Rock.withRover)`

## 核心方法与验证流程

1. 选取 `HSTS DDL` 计划模型。
2. 通过 `ddl2uppaal` 构建 timed automata。
3. 把计划目标映射为 `UPPAAL` 查询。
4. 运行模型检查并读取诊断轨迹。
5. 将 `UPPAAL` 轨迹与 `HSTS` 计划进行对照。

## 案例与结果

### 案例规模

1. 真实应用背景为 `Deep Space 1` Remote Agent。
2. 演示案例 `Rover/Rock` 含 `2` 个对象、`2` 个 state variables。
3. Rover 的状态域大小为 `4`，Rock 的状态域大小为 `2`。

### 主要结果

1. 论文成功把 `HSTS` goal 映射成 `UPPAAL` 的 reachability 性质。
2. `UPPAAL` 生成的诊断轨迹与 `HSTS` 计划可对应。
3. 方法能用于检测计划模型中的不一致与不完备。
4. 作者同时明确指出：完整规划模型过于复杂，需要代表性抽象模型才能继续推进。

### 结果解释

这说明 `UPPAAL` 在这里扮演的是“规划模型审查器”而非原生规划器。它能独立复核计划模型与目标，但尚不足以直接吃下完整工业级规划描述。

## 与本研究的关系

### 相关性分析

本文与博士研究有两个直接交点：一是“如何把高层非传统状态机模型映射为 timed automata”，二是“如何用另一套推理引擎独立复核模型”。

### 可借鉴之处

1. 将目标映射为 reachability 性质，把计划轨迹映回诊断路径。
2. 把 duration / temporal relation 逐项翻译成 invariant、guard 与同步。
3. 坦诚承认完整模型过大，并把抽象作为正式下一步而非临时 workaround。

### 存在的不足与改进空间

1. 应用背景很强，但正文演示主要落在小型 `Rover/Rock` 例子。
2. 没有公开 `UPPAAL` 模型文件。
3. 连续参数和完整工业规模尚未真正落到 `UPPAAL`。

### 对本研究的启发

对博士研究而言，本文提醒我们：即使对象不是传统控制器或协议，只要能把对象的约束结构映射为状态机与时序关系，就仍然可以纳入 `UPPAAL` 式验证闭环；但与此同时，抽象策略必须从一开始就被正视。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：NASA 预印本可直接获取，但未提供映射工具或 `UPPAAL` 模型文件。
- 获取方式/链接：[NASA NTRS](https://ntrs.nasa.gov/citations/20010081322)；[PDF](https://ntrs.nasa.gov/api/citations/20010081322/downloads/20010081322.pdf)
- 对后续复用的现实影响：适合作为“计划模型如何转 timed automata”的早期样本，但若要复用到完整自治航天计划场景，仍需重新实现映射与抽象。

问题一句话：本文验证的是 ASML `EUV` wafer scanner 中 vacuum system 与 source component 的协同控制，核心问题是两者在 nominal/interrupt/error 场景下能否维持安全时序与正确交互。
方法一句话：作者先用 `χ` 建模真空系统、光源与环境，再通过 `χ -> UPPAAL` 翻译做 deadlock、safety 和 temporal property 验证，并把已验证模型用于早期集成测试。
验证收获一句话：验证与测试共找出 `5` 个错误，其中 `3` 个是设计错误；修复后模型满足全部性质，并把测试窗口从预计 `4` 天压到半天，提前约 `20` 周暴露集成问题。

## 基本信息

- 标题：Model-based system analysis using Chi and Uppaal: An industrial case study
- 中文标题：使用 `Chi` 与 `Uppaal` 做模型驱动系统分析的工业案例研究
- 作者：N. C. W. M. Braspenning、Elena M. Bortnik、J. M. van de Mortel-Fronczak、J. E. Rooda
- 单位：Eindhoven University of Technology
- 发表：Computers in Industry, 2008
- DOI：`10.1016/j.compind.2007.06.002`
- 链接：[DOI](https://doi.org/10.1016/j.compind.2007.06.002)
- 主轴分类：🎛️ 控制器与设备控制
- 次轴场景：🏭 工业与基础设施
- 被验证系统：ASML `EUV` wafer scanner 中 vacuum system 与 source component 的协同控制子系统
- UPPAAL线：`UPPAAL`
- 代码/模型/仓库获取方式：论文公开，但原文未给独立 `χ`/`UPPAAL` 模型仓库。
- 案例/数据获取方式：案例来自 ASML 工业设计文档与真实 source realization；无公开数据包。

## 简报

本文的价值不只是“验证了一个工业模型”，而是把建模、翻译、验证和早期系统测试串成一个闭环。被验证对象是 `EUV` 光源与真空控制的协同逻辑，这类对象恰好体现了工业设备中“状态互锁 + 时序约束 + 中断处理”的复杂性。

- 系统：ASML `EUV` wafer scanner 的 source-vacuum 协同控制。
- 特点：`vented / pre-vacuum / exposure / active` 等 latch 状态互锁，并支持请求中断与错误恢复。
- 规模：环境 `Me`、真空系统 `Mv`、光源 `Ms` 组成集成模型；修复后最大验证状态数约 `9961`，原始模型约 `20510`。
- 模型：`χ` 进程代数模型自动翻译为 `UPPAAL` timed automata。
- 性质：deadlock freedom、请求完成性、无未定义行为、无错误、真空/光源互斥安全、真空/venting 时长上界。
- 方法：建模、仿真、`UPPAAL` 验证，再把模型接到真实 source realization 做早期测试。
- 结果：总计发现 `5` 个错误；经修复后全部性质成立，测试时间显著下降。

`工业设计文档 -> χ 组件模型 -> χ→UPPAAL -> 性质验证 -> 与真实 source 集成测试 -> 设计/实现缺陷回修`

## 论文定位

这是一篇很典型的工业控制应用论文。它的对象不是协议或软件流程，而是明确的设备控制协同逻辑，因此归入 `🎛️ + 🏭` 最合适。

## 验证对象与问题背景

### 系统与场景

ASML 的 `EUV` wafer scanner 需要在严格真空条件下工作，因为 `EUV` 光源的运行依赖真空环境。论文聚焦的正是 vacuum system 与 source component 之间的交互控制。

### 系统组成与运行机制

核心部件包括：

1. 真空系统 `Cv`
2. 光源组件 `Cs`
3. 环境/上层控制 `Ce`
4. 四个关键 latch：`vented`、`pre-vacuum`、`exposure`、`active`

运行机制上，环境可以请求系统进入 vacuum 或 vented 状态；真空系统逐步改变真空条件，并通过 latch 与 source 协调。source 只有在满足相应真空条件时才能进入 active/exposure 等状态。

### 验证边界

论文验证的是 vacuum-source 协同控制子系统，而不是整个 wafer scanner 的完整物理过程。

### 核心问题

1. nominal vacuum / venting sequence 是否正确；
2. 中断时 sequence 能否安全切换；
3. source 与 vacuum 的状态互锁是否始终安全；
4. 真空与 venting 时长是否满足上界。

## 模型与形式化建模

论文先用 `χ` 对组件建模，再翻译到 `UPPAAL`。

### 组件建模

1. 环境模型 `Me`
2. 真空系统模型 `Mv`
3. 光源模型 `Ms`

其中真空系统和光源内部都由多个并行 process 组成，显式保留 latch、请求/回复接口和错误状态。

### 抽象边界

模型保留了：

1. supervisory machine control in software；
2. interrupt behavior；
3. electronic communication；
4. sequence timing。

物理连续过程本身没有被细粒度建模。

## 验证目标与性质

论文给出的性质非常清楚：

1. Deadlock freeness：
   `A[] deadlock imply env.end`
2. 请求完成与顺序正确性；
3. No undefined behavior：
   `A[] undefined == 0`
4. No errors：
   `A[] error == 0`
5. 光源 active 时真空系统不能处于 vented；
6. 时长约束：
   `A[] vacuum imply clk <= 21600`
   `A[] venting imply clk <= 3600`

这些性质分别对应死锁安全、设计一致性、设备互锁安全和时序需求。

## 核心方法与验证流程

1. 根据 ASML 设计文档建立 `χ` 组件模型。
2. 通过增量建模和仿真先暴露一部分交互问题。
3. 用 `χ -> UPPAAL` 翻译得到 timed automata。
4. 在 `UPPAAL` 中验证上述性质。
5. 修复设计与模型后再次验证。
6. 将 vacuum 模型与真实 source realization 集成，做早期 model-based system testing。

## 案例与结果

### 验证结果

1. 总共发现 `5` 个错误。
2. 其中 `3` 个是设计错误。
3. 只有 `1` 个设计错误是仿真发现的，其余 `2` 个设计错误只能靠验证发现。
4. 修复后全部性质成立。

### 状态空间与工具代价

1. 原始模型最大状态空间约 `20510`。
2. 修复后验证 property 1 时探索约 `9961` 个状态。
3. 原始模型使用 `UPPAAL 3.6 beta`，修复模型使用 `UPPAAL 4.0.2`。

### 集成测试收益

1. 早期系统测试比真实集成测试提前约 `20` 周。
2. 论文估计测试用时从真实集成阶段的约 `4` 天降为半天。
3. 模型帮助定位了 source realization 的集成问题，避免 clean room 阶段高代价停机。

## 与本研究的关系

### 相关性分析

这篇论文和博士研究的贴合度非常高，因为它完整展示了“文档 -> 模型 -> 性质 -> 反例 -> 修复 -> 测试”的闭环。

### 可借鉴之处

1. 将复杂工业设计文档拆成 latch、请求、回复和 sequence。
2. 把中断行为与 nominal 行为并列处理。
3. 用单一模型同时服务验证与早期测试。

### 存在的不足与改进空间

1. 案例资产依赖工业文档，公开性有限。
2. 连续物理层未纳入形式模型。
3. 当前公开版本不附完整模型仓库。

### 对本研究的启发

它说明高价值应用案例不一定来自“完整公开系统”，很多时候关键是能把控制交互、互锁关系和时间要求抽成可验证状态机。

## 重要的相关工作

### 1. `χ` 到 `UPPAAL` 的翻译链

- 本文把 `χ` 作为上游模型语言，展示了多表示之间的桥接价值。

### 2. 工业 `UPPAAL` 案例

- 它是文库里很强的工业控制代表案例，和 `PLC`、`COMDES-II`、batch plant 一起构成工业控制主线。

## 案例、模型与数据公开情况

- 可获取性判断：🟠 信息不清
- 判断依据：论文与预印本可获得，但未提供独立 `χ`/`UPPAAL` 模型包、设计文档或真实 source realization。
- 获取方式/链接：[DOI](https://doi.org/10.1016/j.compind.2007.06.002)；[TU/e PDF](https://pure.tue.nl/ws/files/3336674/642387.pdf)
- 对后续复用的现实影响：适合作为“工业控制 sequence + 中断 + 测试闭环”的强参考，但复跑必须按论文重建模型。

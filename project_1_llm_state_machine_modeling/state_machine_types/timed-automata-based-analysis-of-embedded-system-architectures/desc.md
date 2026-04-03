# 基于定时自动机的嵌入式系统架构分析 / Timed Automata Based Analysis of Embedded System Architectures

## 基本信息

- 标题：Timed Automata Based Analysis of Embedded System Architectures
- 中文标题：基于定时自动机的嵌入式系统架构分析
- 作者：Martijn Hendriks，Marcel Verhoef
- 发表：*Proceedings of the 20th IEEE International Parallel & Distributed Processing Symposium (IPDPS 2006)*，2006
- DOI：`10.1109/IPDPS.2006.1639422`
- 链接：https://doi.org/10.1109/IPDPS.2006.1639422
- 形式主义：`Timed Automata / Embedded-Architecture Resource Model`
- 主类：⏱️
- 描述客体：🏭
- 所属领域：⏱️
- 论文角色：架构级时序分析 / 定时自动机应用建模
- 工具/实现获取方式：原文明确使用 `UPPAAL` 对 deployment-specific timed automata 模型做分析；未提供独立公开模型仓库。
- 标准/格式获取方式：承载方式是 computation/communication resource `TA`、event generator templates、measuring event generator 与 `UPPAAL` 查询；无统一交换标准。

## 简报

这篇论文的重点不是提出新的 `Timed Automata` 子类，而是把嵌入式系统架构层的分析对象系统化地翻成一组 timed automata。作者关心的是早期 architecture exploration：在不同部署方案下，多个应用任务共享处理器和通信资源时，某个关键端到端反应时间上界是多少。为此，论文分别为 computation resource、communication resource 和 environment events 建模，再用一个 measuring event generator 和 hurry automaton 组合成完整系统。

- 形式主义定位：这是经典 `Timed Automata` 主干上的架构级分析条目，重点是“deployment-specific resource automata + end-to-end latency query”。
- 构造方式简述：先枚举每个资源可能执行的 operation / message，再分别生成 computation/communication `TA`；环境输入用 periodic、sporadic、jitter、bursty generator 模板描述，最后组合后对 bound `C` 做二分搜索。
- 基础设施与场景简述：依托 `UPPAAL`、event models、hurry automaton 和手动 binary search，服务车载导航/音频系统这类多任务嵌入式架构对比分析。

```text
部署架构 + 资源容量 + 输入事件模型 -> resource / environment timed automata -> latency query -> 架构比较
```

## 形式主义定义与核心对象

### 定义对象

论文的核心对象包括：

1. computation resource automata。
2. communication resource automata。
3. periodic、sporadic、jitter、bursty 等 event generator automata。
4. 用于端到端测量的 measuring event generator。
5. 让系统尽快推进的 hurry automaton。

### 核心抽象

原文没有把模型本体写成一个标准元组，而是强调一套模板化 automata 组合。结合正文，可保守整理为：

$$
\mathcal{M}_{arch} = \Big(\bigparallel_i A^{comp}_i\Big) \parallel \Big(\bigparallel_j A^{comm}_j\Big) \parallel \Big(\bigparallel_k E_k\Big) \parallel E_{meas} \parallel H
$$

上式中的符号逐项解释如下：

1. `A^{comp}_i` 是第 `i` 个 computation resource automaton。
2. `A^{comm}_j` 是第 `j` 个 communication resource automaton。
3. `E_k` 是普通 event generator automata。
4. `E_{meas}` 是带测量功能的 event generator。
5. `H` 是 hurry automaton，用来避免资源无意义空转。
6. `\parallel` 表示各 automata 并行同步组成系统模型。

对单个 computation resource，论文给出的抽象非常直接：资源只有 idle 或执行某个 operation 两类位置；每个位置的驻留时间由

$$
\text{time(op)} = \frac{\#instructions(op)}{\text{capacity}}
$$

决定。上式中的符号逐项解释如下：

1. `\#instructions(op)` 是操作 `op` 的指令数。
2. `capacity` 是处理器算力。
3. `time(op)` 是该 operation 在该资源上的执行时间。

对 communication resource，原理完全平行：

$$
\text{time(msg)} = \frac{\#size(msg)}{\text{bandwidth}}
$$

上式中的符号逐项解释如下：

1. `\#size(msg)` 是消息大小。
2. `bandwidth` 是链路带宽。
3. `time(msg)` 是消息传输时长。

### 一个最小例子与通俗解释

论文的 in-car radio navigation 例子很适合做直觉说明：

1. 一个 `Handle TMC` 应用由多个 task 和 message 组成。
2. 每个 task 被放到某个 computation resource 上执行，每个 message 被放到某个 communication resource 上传输。
3. 外部输入事件由 periodic 或 jitter generator 触发。
4. 测量 automaton 从某个输入被观察到开始计时，到输出事件发生时停止，用查询判断是否满足 `ReceiveTMC \le 1000ms`。

通俗地说，这篇论文做的是“把架构图中的 CPU、总线和输入流都先写成状态机，再问这套部署到底快不快”。

### 运行 / 接受 / 转移语义

论文给出的关键查询是：

$$
AG\ (aut.seen \Rightarrow aut.y < C)
$$

上式中的符号逐项解释如下：

1. `AG` 表示所有路径上的全局不变式。
2. `aut.seen` 表示 measuring automaton 已经观察到目标事件。
3. `aut.y` 是 measuring automaton 的测量时钟。
4. `C` 是待验证的候选上界。
5. 该式表示：一旦测量 automaton 见到终止事件，测量值必须小于候选 bound `C`。

作者进一步用手动 binary search 查找最小可行 `C`。因此这里的“接受语义”本质上是 bound-search，而不是语言接受。

### 语义边界

这篇论文的边界也非常清楚：

1. 重点是 best/worst-case execution / response time，不做利用率理论。
2. 系统抽象偏资源层，而不是复杂功能状态机。
3. 论文假设某些 overhead 为零，适合早期 design exploration，不是 cycle-accurate 仿真。
4. 数据依赖、缓存效应和复杂调度策略只被保守压缩进 resource behavior。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 全局架构模型 | `$\mathcal{M}_{arch} = (\bigparallel_i A^{comp}_i) \parallel (\bigparallel_j A^{comm}_j) \parallel (\bigparallel_k E_k) \parallel E_{meas} \parallel H$` | 把资源、环境和测量器组合成统一 `TA` 网络。 |
| 计算资源时间 | `$\text{time(op)} = \#instructions(op) / \text{capacity}$` | operation 驻留时间由指令数和算力决定。 |
| 通信资源时间 | `$\text{time(msg)} = \#size(msg) / \text{bandwidth}$` | message 驻留时间由消息大小和带宽决定。 |
| 端到端时延查询 | `$AG\ (aut.seen \Rightarrow aut.y < C)$` | 检查候选上界 `C` 是否足够。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 资源通常在 idle / busy 或特定 operation 位置之间切换。 |
| 事件 / 触发 | 强支持 | 环境到达、资源请求、消息传输和观测事件是主体。 |
| 守卫 / 数据 | 中等支持 | 主要使用时间与请求计数，不依赖复杂数据结构。 |
| 层次 | 不支持 | 不是层次状态机，核心是模板化平铺网络。 |
| 并发 / 同步 | 很强 | 多资源、多应用、多输入流并行组合是模型主体。 |
| 时间约束 | 很强 | 执行时间、传输时间、输入到达模型和端到端 bound 都显式建模。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散实时架构模型。 |
| 可执行 / 可验证性 | 强验证 | 可直接在 `UPPAAL` 中做 bound analysis。 |

### 形式化问题与性质

1. 论文表明，architecture exploration 也可以直接落到 `TA`，而不只靠 analytic queueing 或 response-time calculus。
2. hurry automaton 是一个很有价值的工程技巧，它让模型更接近“资源只要可工作就立刻工作”的最坏/最好界分析语义。
3. 对本文库而言，它补强了 `Timed Automata` 主干在“部署架构比较”上的代表应用带。

## 构造方式与承载格式

### 建模入口

建模步骤可概括为：

1. 枚举部署方案中的 computation / communication resources。
2. 为每个资源收集其可能执行的 operation 或可传输的 message。
3. 依据周期、抖动、突发等输入模式选择 event generator 模板。
4. 叠加 measuring event generator 和 hurry automaton。
5. 对目标 end-to-end requirement 做 `UPPAAL` 查询与 binary search。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. deployment-specific timed automata templates。
2. event generator templates。
3. measuring event generator。
4. `UPPAAL` 查询公式。

### 交换与互操作

论文的互操作重点是：

1. 从架构部署信息生成 resource automata；
2. 从输入事件模型生成 generator automata；
3. 把分析结果回写到 architecture alternative 的优劣比较中。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：无统一元模型；模型是部署特定的 `TA` 网络。
- 仿真/执行支持：以仿真和验证为主，不强调运行时代码部署。
- 验证/分析支持：`UPPAAL` reachability / invariant checking + manual binary search。
- 代码生成/转换支持：支持从 architecture description 到 resource automata 的系统化建模，但原文未提供自动生成器。
- 标准化或社区生态：属于 `Timed Automata` 在 embedded performance analysis 上的经典工具线应用。

## 适用场景与需求前提

### 适用场景

适合车载电子、嵌入式平台和分布式资源部署的早期架构探索，尤其适合比较不同 CPU / bus / deployment 组合对响应时间的影响。

### 需求前提

1. 操作集合、消息集合和资源容量必须可枚举。
2. 输入到达模式需要能抽成 periodic / sporadic / jitter / bursty 等有限模板。
3. 关键目标是端到端时间 bound，而不是复杂功能正确性。

### 不适用或高成本场景

若系统的关键差异来自缓存、流水线、复杂抢占代价、数据相关执行时间或连续物理过程，这种 architecture-level `TA` 抽象会偏粗。

## 与相邻形式主义的关系

相对 [resource-optimal-scheduling-using-priced-timed-automata/desc.md](../resource-optimal-scheduling-using-priced-timed-automata/desc.md)，本文不追求代价最优，而是比较不同部署架构的时间 bound；相对 [a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md](../a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md)，这里仍停留在经典 clocks，而没有 stopwatches；相对 [timed-automata-based-schedulability-analysis-for-distributed-firm-real-time-systems-a-case-study/desc.md](../timed-automata-based-schedulability-analysis-for-distributed-firm-real-time-systems-a-case-study/desc.md)，这篇更偏 architecture alternative exploration，而不是给定通信系统的详细 schedulability map。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求描述已经包含任务、消息、周期和部署资源时，LLM 生成模型时不一定非得先长成控制器逻辑，也可以直接长成资源级 timed automata 网络。

### 作为目标形式主义还是中间表示

对架构分析和时延估计，它可以直接作为目标形式主义；对更大的控制系统开发流程，它更像一层架构分析中间表示。

### 对需求到模型生成的启发

1. 需求抽取应显式区分 task、message、resource 和 input stream 四类对象。
2. 输入事件模型本身值得模板化，而不是藏在自然语言里。
3. 若目标是最坏响应时间估计，生成 measuring automaton 往往和生成业务 automata 同样重要。

### 现实限制

这类模型最容易失真在于“资源时延公式很容易给，真实调度成本很难给”，因此需求抽取阶段必须明确哪些 overhead 已被忽略。

## 重要的相关工作

- [resource-optimal-scheduling-using-priced-timed-automata/desc.md](../resource-optimal-scheduling-using-priced-timed-automata/desc.md)：同样面向资源/部署问题，但把 reachability 提升成了 minimum-cost reachability。
- [a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md](../a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md)：同样做嵌入式架构可调度性分析，但需要 `Stopwatch Automata` 保留抢占语义。
- [timed-automata-based-schedulability-analysis-for-distributed-firm-real-time-systems-a-case-study/desc.md](../timed-automata-based-schedulability-analysis-for-distributed-firm-real-time-systems-a-case-study/desc.md)：另一篇典型的 distributed embedded `TA` 应用，可对照其更通信密集的建模对象。

## 文献分类总结

- 主类：⏱️
- 描述客体：🏭
- 所属领域：⏱️
- 形式主义：`Timed Automata / Embedded-Architecture Resource Model`
- 论文角色：架构级时序分析 / 定时自动机应用建模
- 核心功能：用 resource/event generator automata 评估部署架构的端到端时间界
- 关键特性：deployment-specific resource models、event generators、measuring automaton、hurry automaton、binary search
- 构造方式：computation/communication resources + environment generators + `UPPAAL` queries
- 基础设施：`UPPAAL`
- 适用场景：嵌入式架构比较、早期设计探索和端到端时延估计
- 需求前提：任务/消息/容量/带宽和事件模型需可显式结构化
- 状态：🟢

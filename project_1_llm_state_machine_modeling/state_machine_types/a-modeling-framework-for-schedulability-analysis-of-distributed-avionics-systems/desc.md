# 分布式航电系统可调度性分析的建模框架 / A Modeling Framework for Schedulability Analysis of Distributed Avionics Systems

## 基本信息

- 标题：A Modeling Framework for Schedulability Analysis of Distributed Avionics Systems
- 中文标题：分布式航电系统可调度性分析的建模框架
- 作者：Pujie Han，Zhengjun Zhai，Brian Nielsen，Ulrik Nyman
- 发表：*Electronic Proceedings in Theoretical Computer Science*，Volume 268，2018
- DOI：`10.4204/EPTCS.268.5`
- 链接：https://doi.org/10.4204/EPTCS.268.5
- 形式主义：`Stopwatch Automata / DIMA Schedulability Framework`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：分布式航电可调度性分析 / `Stopwatch Automata` 应用条目
- 工具/实现获取方式：原文明确使用 `UPPAAL` classic 与 `UPPAAL SMC`，并给出 classical MC、global SMC 与 compositional MC 三条分析路径；未提供独立代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` 模板、ARINC-653 / AFDX 结构化模型和 safety / hypothesis-testing 查询；无统一交换标准。

## 简报

这篇论文把 `Stopwatch Automata` 真正拉进了复杂工程系统：不是一个单一控制器，而是一个由 `ARINC-653` 分区调度、周期/偶发任务和 `AFDX` 网络共同构成的 distributed integrated modular avionics (`DIMA`) 系统。作者的核心判断是：如果还想在 `UPPAAL` 里既保留任务可抢占执行时间，又保留分区/网络时序，就必须用 stopwatches 而不是普通 clocks。于是整篇论文围绕一组 `UPPAAL SWA` 模板展开，并把 classical MC、SMC 和 compositional MC 组合起来做分层分析。

- 形式主义定位：这是 `Timed Automata -> Stopwatch Automata` 的工程化应用条目，重点是“可抢占执行时间 + 航电分区调度 + 网络时延联合验证”。
- 构造方式简述：通过 `PartitionScheduler`、`TaskScheduler`、`PeriodicTask / SporadicTask`、`IPTx / IPRx / VLinkTx / VLinkRx` 等模板，把 DIMA 架构压成一组 `UPPAAL SWA/TA` 网络。
- 基础设施与场景简述：依托 `UPPAAL` classic、`UPPAAL SMC`、ARINC-653 分区调度和 AFDX 网络模型，服务分布式航电系统的 schedulability verification。

```text
ARINC-653 分区 + 周期/偶发任务 + AFDX 通信 -> layered SWA/TA templates -> SMC falsification / MC proof -> schedulability conclusion
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. `PartitionScheduler` 与 `TaskScheduler` 两层调度模板。
2. `PeriodicTask` / `SporadicTask` 两类 `SWA` 任务模板。
3. `IPTx / IPRx / VLinkTx / VLinkRx` 通信层模板。
4. `error` 变量表达的 safety property。
5. classical MC 与 SMC 的组合分析流程。

### 核心抽象

论文没有单独给出一个全局系统元组，但结合文中模板组织，可以保守整理为：

$$
\mathcal{M}_{DIMA} = \bigparallel_i PartitionScheduler_i \parallel TaskScheduler_i \parallel \bigparallel_j Task_j \parallel \bigparallel_k Comm_k
$$

上式中的符号逐项解释如下：

1. `PartitionScheduler_i` 表示第 `i` 个分区的 TDM 调度器。
2. `TaskScheduler_i` 表示该分区内部的 preemptive fixed-priority 调度器。
3. `Task_j` 代表 `PeriodicTask` 或 `SporadicTask` 模板实例。
4. `Comm_k` 代表 `IPTx / IPRx / VLinkTx / VLinkRx` 等通信层模板。

上式不是论文直接写出的公式，而是根据其模板分层结构做的保守整理；论文的正式分析对象仍是 `UPPAAL` 中的模板网络。

### 一个最小例子与通俗解释

论文最直观的例子，是一个周期任务在分区内被可抢占执行：

1. 任务有普通时钟 `x`、`curTime`，以及一个 stopwatch `exeTime`。
2. `x` 和 `curTime` 负责测 release point、period 和 deadline。
3. `exeTime` 只在任务真正占用处理器时前进；一旦被高优先级任务抢占，它就会暂停。
4. 这正是 stopwatch 相比普通 `TA` 的关键区别：任务的“已执行量”被暂停而不是重算。

通俗地说，普通 `TA` 的时钟像“无论 CPU 有没有分给你都在走”；这里的 `exeTime` 像“只有真的拿到 CPU 才计时的秒表”，这更像真实的航电调度。

### 运行 / 接受 / 转移语义

论文用一个布尔变量 `error` 来统一表达 schedulability violation，并把 classical MC 的 safety property 写成：

$$
A[]\ \mathrm{not}\ error
$$

上式中的符号逐项解释如下：

1. `A[]` 是 `UPPAAL` 的全路径全局算子。
2. `error` 在任何 deadline miss、sampling-port refresh violation 或 queue overflow 发生时被置为 `True`。
3. 因而只要能证明 `A[] not error`，就说明该配置满足论文定义的 schedulability。

对应的 SMC 假设检验查询则是：

$$
Pr[\le M](\Diamond error) \le \theta
$$

上式中的符号逐项解释如下：

1. `M` 是仿真时间上界。
2. `\Diamond error` 表示在时界内最终触发违反。
3. `\theta` 是一个很小的概率阈值。
4. 这个查询用于快速 falsification，而不是给出严格证明。

### 语义边界

这篇论文的边界也很明确：

1. classical MC 用于 strict proof，但受 state-space explosion 限制。
2. SMC 适合快速 falsification，却不能单独作为严格可调度证明。
3. 论文的网络和调度模型已经很工程化，但仍是离散/stopwatch 抽象，不是全连续物理模型。
4. 由于 `UPPAAL` 对 `SWA` 的 symbolic MC 带有轻微 over-approximation，`No / May not` 不能直接等价为真实不可调度。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 分层系统模型 | `$\mathcal{M}_{DIMA} = \bigparallel_i PartitionScheduler_i \parallel TaskScheduler_i \parallel \bigparallel_j Task_j \parallel \bigparallel_k Comm_k$` | 保守整理出的模板网络骨架，体现分区、任务和网络三层结构。 |
| classical MC 安全性质 | `$A[]\ \mathrm{not}\ error$` | 把所有违反统一压成 safety property。 |
| SMC 假设检验 | `$Pr[\le M](\Diamond error) \le \theta$` | 用仿真快速筛掉非可调度配置。 |
| 关键 stopwatch 用法 | `exeTime` 仅在任务实际执行时流逝 | 用 stopwatches 表达 preemption/resume。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 分区、任务、通信层都有显式模式。 |
| 事件 / 触发 | 强支持 | `enter_partition`、`exit_partition`、`ready`、`sched`、`stop` 等通道很完整。 |
| 守卫 / 数据 | 强支持 | guards、任务优先级、ready queue 与消息端口属性都进入模型。 |
| 层次 | 强支持 | 模型按 scheduling / task / communication 三层组织。 |
| 并发 / 同步 | 强支持 | 分区调度、任务调度和网络通信通过 channel 同步。 |
| 时间约束 | 强支持 | partition windows、task deadlines、refresh period、network latency 全部显式建模。 |
| 连续动态 / 随机性 | 部分支持 | SMC 版本允许 stochastic delay interpretation，但主体仍是 timed/stopwatch 抽象。 |
| 可执行 / 可验证性 | 强支持 | `UPPAAL` classic 与 `UPPAAL SMC` 双路线联用。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先按 `scheduling / task / communication` 三层拆系统。
2. 用 `PartitionScheduler` 和 `TaskScheduler` 描述 ARINC-653 两层调度。
3. 用 `PeriodicTask / SporadicTask` 中的 `exeTime` stopwatch 表达抢占执行。
4. 再把 sampling / queuing ports、UDP/IP 和 VL 延时接到任务层上。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `UPPAAL` classic 模板网络。
2. `UPPAAL SMC` 对应的 stochastic template 变体。
3. `error` 布尔变量与查询模板。
4. compositional partition + environment interface 建模。

### 交换与互操作

论文没有统一交换格式；它的工程价值主要体现在：

1. 用模板网络稳定承载 ARINC-653 / AFDX 关键结构；
2. 在同一模型骨架上兼容 MC 与 SMC；
3. 支持 partition-level compositional reasoning。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` classic、`UPPAAL SMC`。
- 解析/交换/元模型支持：原文未给 XML/JSON 标准。
- 仿真/执行支持：`UPPAAL SMC` 用于 simulation-based falsification。
- 验证/分析支持：global SMC、global MC、compositional MC。
- 代码生成/转换支持：论文重点在分析而非代码生成，但模板组织已经足够接近可复用建模骨架。
- 标准化或社区生态：与 `ARINC-653`、`AFDX` 航电标准直接挂接，但形式化承载仍主要绑定 `UPPAAL`。

## 适用场景与需求前提

### 适用场景

适合具有分区调度、优先级调度、网络通信和端口刷新约束的复杂实时嵌入式系统，尤其是分布式航电系统。

### 需求前提

1. 分区窗口、任务周期/截止期和通信时延必须可显式结构化。
2. 执行进度需要保留 preemption/resume 语义。
3. 系统可接受 layered template 建模，而不是完整源码级精确仿真。
4. 若要做 strict proof，需要接受 compositional 分析。

### 不适用或高成本场景

若系统具有很强的数据依赖、巨大的并行度或需要连续物理闭环精度，单靠这套 `SWA` 框架仍会很吃力。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文最关键的增量不是普通 clocks，而是能在任务被抢占时冻结的 `exeTime` stopwatch；相对 [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)，两者都依赖 stopwatches 表达“进度暂停”，但本文把它工程化到 ARINC-653 + AFDX 航电框架；相对 [Parametric Schedulability Analysis of a Launcher Flight Control System under Reactivity Constraints](../parametric-schedulability-analysis-of-a-launcher-flight-control-system-under-reactivity-constraints/desc.md)，本文保留普通 `SWA`，而那篇进一步把 stopwatches 参数化成 `PSA`。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文是非常强的“状态机类型落地证据”：它说明 `Stopwatch Automata` 不是抽象概念，而是能直接承载分区调度、可抢占任务和网络时延联合分析的工程形式主义。

### 作为目标形式主义还是中间表示

对复杂实时软件架构分析，它可以直接作为目标形式主义；对需求自动建模，它更像一个高保真验证后端或结构化中间表示。

### 对需求到模型生成的启发

1. 文本里的“可抢占执行”“分区窗口”“端口刷新周期”是明显的 stopwatch / timed 建模信号。
2. LLM 生成的模型若要进入真实验证，应尽量先分层，再实例化模板。
3. Safety property 与 hypothesis testing 可以在同一建模骨架上共用。

### 现实限制

最大瓶颈仍是 state-space explosion，因此自动化生成时必须控制模板粒度并尽量支持 compositional verification。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文建立在经典 `TA` 主干上。
- [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)：说明 stopwatch 对抢占建模的基础价值。
- [Parametric Schedulability Analysis of a Launcher Flight Control System under Reactivity Constraints](../parametric-schedulability-analysis-of-a-launcher-flight-control-system-under-reactivity-constraints/desc.md)：沿着同一 schedulability 路线，把 `SWA` 进一步推到参数综合。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Stopwatch Automata / DIMA Schedulability Framework`
- 论文角色：分布式航电可调度性分析 / `Stopwatch Automata` 应用条目
- 核心功能：用 `UPPAAL SWA` 建模分区调度、可抢占任务与 AFDX 通信，并联用 `MC/SMC` 做可调度性分析
- 关键特性：`exeTime` stopwatch、layered templates、ARINC-653 / AFDX、global / compositional analysis
- 构造方式：调度层 + 任务层 + 通信层模板网络
- 基础设施：`UPPAAL` classic、`UPPAAL SMC`
- 适用场景：分布式航电和其他复杂实时嵌入式架构
- 需求前提：分区窗口、任务时序和网络延时需可显式建模，并保留抢占语义
- 状态：🟢

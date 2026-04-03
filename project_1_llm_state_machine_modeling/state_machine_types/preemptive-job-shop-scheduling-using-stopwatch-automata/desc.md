# 抢占式 Job-Shop 调度中的秒表自动机 / Preemptive Job-Shop Scheduling Using Stopwatch Automata

## 基本信息

- 标题：Preemptive Job-Shop Scheduling Using Stopwatch Automata
- 中文标题：抢占式 Job-Shop 调度中的秒表自动机
- 作者：Yasmina Abdeddaim，Oded Maler
- 发表：*Proceedings of the AIPS-02 Workshop on Planning via Model-Checking*，Toulouse，France，2002
- DOI：当前目录保存的是 workshop proceedings 裁出的单篇 PDF；同名正式 chapter 可见 `10.1007/3-540-46002-0_9`
- 链接：https://doi.org/10.1007/3-540-46002-0_9
- 形式主义：`Stopwatch Automata / Preemptive Job-Shop Model`
- 主类：⏱️
- 描述客体：🏭
- 所属领域：🏭
- 论文角色：调度建模 / `Stopwatch Automata` 分支代表应用条目
- 工具/实现获取方式：原文报告了若干 shortest-path 算法和启发式的原型实现，但未提供独立公开仓库。
- 标准/格式获取方式：承载方式是数学定义、job-to-automaton 构造和最短路问题；原文未提供行业标准或交换格式。

## 简报

这篇论文的重要性不在“又找了一个调度案例”，而在于它把 `Timed Automata` 明确推进到了一个可稳定命名的新分支：`Stopwatch Automata`。作者指出，普通时间自动机只能让时钟始终以单位速率前进，无法自然表达“任务被抢占后进度暂停、恢复后继续累积”的行为；而在可抢占 job-shop 中，这个能力是核心。因此论文引入 slope 取 `0/1` 的时钟，把调度问题压成秒表自动机上的最短路。

- 形式主义定位：这是 `Timed Automata -> Stopwatch Automata` 的典型应用型代表条目，重点是“冻结时钟 + preempt/resume + 最优调度”。
- 构造方式简述：先为每个 job 构造一个带 waiting/executing/preempted 状态的一时钟秒表自动机，再通过 machine-level mutual exclusion 做并行组合，最后求最短路径。
- 基础设施与场景简述：依托秒表自动机语义、调度优先关系和 prototype shortest-path heuristics，服务可抢占 job-shop 与共享机器资源调度。

```text
作业步骤与机器占用约束 -> 每个 job 的 stopwatch automaton -> 资源互斥组合 -> shortest path -> 最优可抢占调度
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. 机器集合 `M` 与作业步骤序列 `J = (m_1, d_1), \ldots, (m_k, d_k)`。
2. 每个作业对应的 waiting / executing / preempted 三类位置。
3. 在执行态以速率 `1` 增长、在被抢占态以速率 `0` 冻结的时钟。
4. 用于强制同一机器互斥占用的组合构造。
5. 以 elapsed time 为代价的 shortest-path 优化目标。

### 核心抽象

原文给出的秒表自动机定义是：

$$
A = (Q, C, s, f, u, \Delta)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集合。
2. `C` 是时钟集合。
3. `s` 与 `f` 分别是初始状态和终止状态。
4. `u : Q \to \{0,1\}^n` 是 slope 映射，决定每个状态下各时钟以 `0` 还是 `1` 的速率演化。
5. `\Delta` 是离散迁移集合，边上带 guard 和 reset。

论文进一步给出两类基本步：

$$
(q, v) \xrightarrow{0} (q', \mathrm{Reset}_{\rho}(v))
$$

$$
(q, v) \xrightarrow{t} (q, v + t u_q)
$$

上式中的符号逐项解释如下：

1. `v` 是当前时钟赋值。
2. `\rho \subseteq C` 是本次离散迁移需要复位的时钟集合。
3. `u_q` 是状态 `q` 上的时钟导数向量。
4. 当 `u_q = 0` 时，对应时钟会被冻结；这正是 stopwatch 相比经典 `TA` 的关键增量。

对单个作业 `J = (k, \mu, d)`，原文构造的 job automaton 可以保守概括为：

$$
Q = P \cup \bar{P} \cup \tilde{P} \cup \{f\}
$$

其中 `P` 表示 waiting 位置，`\bar{P}` 表示正在执行该步骤的位置，`\tilde{P}` 表示步骤已开始但当前被抢占的位置。执行态上 `u_q = 1`，被抢占态上 `u_q = 0`。

### 一个最小例子与通俗解释

一个最小例子是作业 `J = (m_1, 3), (m_2, 2)`：

1. 作业先在 `m_1` 的 waiting 状态等待机器可用。
2. 一旦开始执行，时钟 `c` 从 `0` 开始累计，直到 `c \ge 3` 才能结束第一步。
3. 如果中途被别的作业抢走机器，系统转到 `\tilde{m}_1`，这时 `c` 冻结而不是清零。
4. 机器重新可用时再恢复执行，从之前累计值继续跑到 `3`。

通俗地说，普通时间自动机里的时钟像“永远在走的秒表”；秒表自动机里的时钟像“能按暂停键的秒表”，这正好对应可抢占任务的剩余加工时间。

### 运行 / 接受 / 转移语义

论文把完整 job-shop 建模成各 job automata 的互斥组合。若 `A_i` 是第 `i` 个 job 的秒表自动机，则整体系统可保守写成：

$$
A_J = A_1 \parallel \cdots \parallel A_n
$$

但这里只保留 non-conflicting 的全局状态，也就是任意时刻同一机器不能同时被两个作业占用。原文的关键结论是：

$$
\mathrm{OptSchedule}(J) = \mathrm{ShortestPath}(A_J)
$$

其含义是：每一条 complete run 对应一份可行调度，运行的 metric length 就是调度总时长，因此最优调度问题可以还原成秒表自动机上的最短路问题。

### 语义边界

这篇论文也明确给出边界：

1. 一般 `Stopwatch Automata` 的 reachability 是不可判定的。
2. 本文可解，并不是因为 stopwatch 本身突然变简单，而是因为 preemptive job-shop 诱导出的路径具有额外结构。
3. 论文依赖“高效调度存在”这一 folktheorem，把候选调度收束到有限 priority relation。
4. 因而它是一个“可抢占调度子类上的可解分支”，不是任意 stopwatch 都能直接套用。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 秒表自动机元组 | `$A = (Q, C, s, f, u, \Delta)$` | 在 `TA` 基础上加入可冻结时钟。 |
| 时间步 | `$(q, v) \xrightarrow{t} (q, v + t u_q)$` | 时钟导数由状态 `q` 决定，可为 `0`。 |
| 离散步 | `$(q, v) \xrightarrow{0} (q', \mathrm{Reset}_{\rho}(v))$` | 离散跳转不耗时，但可复位时钟。 |
| 作业组合 | `$A_J = A_1 \parallel \cdots \parallel A_n$` | 多作业通过 machine-level 互斥并发。 |
| 调度求解 | `$\mathrm{OptSchedule}(J) = \mathrm{ShortestPath}(A_J)$` | 最优可抢占调度归约为最短路。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | waiting / executing / preempted 三类模式是核心。 |
| 事件 / 触发 | 支持 | begin、pause、resume、end 等离散迁移明确定义。 |
| 守卫 / 数据 | 部分支持 | 重点是 clock guard，不依赖复杂数据变量。 |
| 层次 | 不支持 | 仍是平面自动机组合。 |
| 并发 / 同步 | 强支持 | 多作业通过互斥组合并发运行。 |
| 时间约束 | 强支持 | 时钟冻结、恢复与累计时间是主体。 |
| 连续动态 / 随机性 | 不支持 | 只有 piecewise-constant 时钟导数。 |
| 可执行 / 可验证性 | 条件强支持 | 一般 stopwatch 不可判定，但本文调度子类可做最短路求解。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先列出每个 job 的步骤序列和每步所需机器/时长。
2. 为每个步骤创建 waiting、executing、preempted 三类位置。
3. 用一块时钟记录已执行进度，并在 preempted 状态冻结。
4. 最后通过 machine 冲突约束组合成全局自动机。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. job-shop 规格 `(k, \mu, d)`。
2. 单 job 秒表自动机。
3. mutual exclusion composition。
4. shortest-path 搜索状态空间。

### 交换与互操作

这篇论文没有给 XML/DSL 交换标准；它的贡献重点是：

1. job-shop 到 stopwatch automata 的结构映射；
2. 调度 run 与 automaton run 的双向对应；
3. 从模型到 shortest-path 求解问题的归约。

## 配套基础设施

- 建模/编辑工具：原文未给专用建模器；主要依赖数学构造与原型实现。
- 解析/交换/元模型支持：原文未给通用元模型或交换格式。
- 仿真/执行支持：原文实现了若干 shortest-path 算法与启发式，并在 benchmark 上测试。
- 验证/分析支持：核心分析任务是最优路径搜索，而不是一般 reachability model checking。
- 代码生成/转换支持：支持从 job-shop 规格构造成 stopwatch automaton。
- 标准化或社区生态：属于 `Timed Automata` 研究分支，工程生态远弱于 `UPPAAL` 主线。

## 适用场景与需求前提

### 适用场景

适合可抢占作业车间、共享机器资源调度、任务执行进度需要暂停/恢复而不能简单 reset 的离散实时系统。

### 需求前提

1. 每个 job 的步骤顺序必须明确。
2. 每步所需机器和加工时长必须可离散列出。
3. 系统允许抢占且抢占后保留已完成进度。
4. 优化目标可以写成总 elapsed time 最小。

### 不适用或高成本场景

若系统包含复杂数据依赖、概率持续时间、连续物理动力学或抢占代价不可忽略，本文这条 stopwatch 最短路建模就会失真。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文把“时钟始终按单位速率前进”的限制放宽为“某些状态下可冻结”，因此稳定补出了 `Timed Automata` 下的 `Stopwatch Automata` 分支；相对 [Timed Verification of the Generic Architecture of a Memory Circuit Using Parametric Timed Automata](../timed-verification-of-the-generic-architecture-of-a-memory-circuit-using-parametric-timed-automata/desc.md)，这里增加的是时钟导数分支而不是参数化时延；相对 [Adaptive Scheduling of Data Paths using Uppaal Tiga](../adaptive-scheduling-of-data-paths-using-uppaal-tiga/desc.md)，这里没有 controller/environment 二人博弈结构，而是纯优化型调度搜索。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果需求里明确出现“任务可暂停、恢复后继续累计执行进度”，那么直接落到经典 `TA` 会丢信息，而 `Stopwatch Automata` 是更贴切的目标或中间表示。

### 作为目标形式主义还是中间表示

对资源调度和执行优化问题，它可以直接作为目标形式主义；对一般控制系统需求到模型生成，它更适合作为带执行进度语义的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时要显式识别 preemption/resume。
2. “暂停后保留剩余加工量”应映射成冻结时钟，不应误写成 reset。
3. 资源互斥关系天然适合转成全局组合时的冲突状态剪枝。

### 现实限制

一般 stopwatch 分支判定性较弱，若后续验证链条需要主流工具和稳定可判定性，就必须控制在类似本文这种结构化子类里。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文明确以经典 `TA` 为出发点，只是把时钟导数扩展到 `0/1`。
- `On the Impressive Power of Stopwatches`：原文用它说明一般 stopwatch reachability 的困难性。
- `Job-Shop Scheduling using Timed Automata`：本文直接承接作者团队在 non-preemptive 情况下的前一阶段工作。

## 文献分类总结

- 主类：⏱️
- 描述客体：🏭
- 所属领域：🏭
- 形式主义：`Stopwatch Automata / Preemptive Job-Shop Model`
- 论文角色：调度建模 / `Stopwatch Automata` 分支代表应用条目
- 核心功能：把可抢占 job-shop 调度归约为秒表自动机最短路
- 关键特性：冻结时钟、preempt/resume、machine mutual exclusion、efficient schedule theorem
- 构造方式：单作业秒表自动机 + 资源互斥组合 + shortest-path 搜索
- 基础设施：论文原型算法与 benchmark 实验，未提供独立公开仓库
- 适用场景：可抢占作业车间与共享机器资源调度
- 需求前提：步骤顺序、机器占用、持续时间和抢占语义需明确
- 状态：🟢

# Distributed Parametric and Statistical Model Checking

- 问题一句话：`UPPAAL-SMC` 虽然比穷举更可扩展，但大量仿真、顺序假设检验和大规模参数扫面仍然会被单机时间拖住。
- 方法一句话：把 `SMC` 放到 master/slave 架构上，对 sequential testing 采用 batch+buffer 的无偏分布式收集策略，对 estimation 与参数扫面采用独立任务并行。
- 解决点一句话：把 `UPPAAL-SMC` 从“单机统计验证”推进到“可分布式做阈值检验、概率估计和参数探索”的实用平台。

## 论文定位

这篇论文属于 `⚡ 改进与扩展`，位于 `UPPAAL-SMC` 主线的早期性能扩展阶段。它不是重新定义 `SMC` 语义，而是回答一个更工程化、但同样核心的问题：**当随机仿真本身已经成为瓶颈时，怎样把 `SMC` 正确而高效地分布出去**。

它在线路上的位置很适合放在：

1. [david11-statistical-model-checking-real-time](./../david11-statistical-model-checking-real-time/) 之后；
2. [bulychev12-distributed-statistical-model-checking](./../bulychev12-distributed-statistical-model-checking/) 之前或同一小支线；
3. [muniz24-gpu-accelerating-smc-extended-timed-automata](./../muniz24-gpu-accelerating-smc-extended-timed-automata/) 之前，作为 CPU/cluster 时代的并行化前驱。

它的独特之处在于，同时覆盖了两种看似相近、其实并行难点不同的任务：

1. distributed statistical model checking
2. distributed parametric model checking

前者要解决顺序检验的偏差问题，后者要解决大量独立参数任务的调度与扫面问题。

## 立足问题

`SMC` 的核心优点是规避穷举，但它并不意味着“总是很快”。作者指出，两类场景会让 `SMC` 也变得吃力：

1. **单个统计结论就需要很多 runs**
   - 比如要做高置信度概率估计，或 rare event 检验。
2. **同一个模型要对很多参数组合重复跑**
   - 比如扫 arrival rate、节点数、网络拓扑、策略参数。

在这种情况下，单机虽然不必存完整状态空间，但仍然可能耗在大量独立仿真上。

作者还特别指出，分布式并不只是“把 runs 扔给多台机器”这么简单。对 fixed-sample estimation 来说，任务天然独立，的确很好并行；但对 sequential hypothesis testing 来说，**若更快返回的 worker 恰好更常生成某类结果，就可能引入统计偏差**。也就是说，分布式 `SMC` 的真正难点不只是调度，而是既要并行、又不能破坏原算法的统计正确性。

此外，参数化分析还有另一层需求：不仅要算一个结论，还要大规模地画出“性能随参数怎么变”“哪个参数是最优”“哪组参数满足 Nash equilibrium”。这要求工具不仅会并行仿真，还要会并行组织大量独立作业。

## 核心方法

论文的方法分成三层：`NPTA` 概率语义、distributed SMC 架构、distributed parametric sweep 框架。

### 1. 用 `PTA/NPTA` 和 `PWCTL` 作为统计模型检查底座

本文的基础模型是 priced timed automata 及其 network 组合。多个 PTA 通过消息传递同步后，借助 stochastic semantics 形成随机运行分布。作者强调，这里的随机性不是额外手工贴在全系统上的，而是由各组件延时分布与同步竞争自然诱导出来。

对应的性质语言使用 `PWCTL`。典型形式是：

$$
\Pr_A[\Diamond_{c \le C}\ \varphi]
$$

也就是观察 clock `c` 在界 `C` 内是否能达到状态谓词 `\varphi`。于是 `SMC` 需要回答两类问题：

1. testing：某个概率是否至少达到阈值 `\theta`
2. estimation：这个概率大约是多少

这里 testing 采用 Wald sequential hypothesis testing，estimation 则采用 Chernoff-Hoeffding bound 下的 Monte Carlo 风格采样。

### 2. 对 distributed statistical testing，关键不是并行本身，而是无偏并行

论文最重要的方法点在第三节。作者先明确指出：若简单让多个 slave 独立跑仿真，然后 master 按“谁先返回谁先记”的顺序把结果喂给 sequential test，就可能偏向那些生成更快的 run。这样得到的顺序和单机算法看到的观测序列不等价，结论就可能被污染。

为此，作者沿着 Younes 的 round-robin 思想继续推进，但做了两个关键工程改造：

1. **batch**
   - slave 不按单个 run 回传，而是把一批样本聚合后再发给 master。
   - 作用是减少通信频率。
2. **buffer**
   - master 对到来的结果不立刻强同步消耗，而是设置缓冲。
   - 作用是降低 worker 之间的同步耦合，提高并发度。

这两个设计的目标很明确：在保持统计判断不失真的前提下，把网络通信和节点同步带来的开销降下来。论文里反复强调，Younes 原始方案相当于 `batch = 1, buffer = 1` 的特例，而这个特例在真实 cluster 上不够 scalable。

### 3. 对 estimation，直接做 embarrassingly parallel 划分

和 sequential testing 不同，估计概率时需要的样本数由 Chernoff bound 预先给定，因此可以直接把总样本数均匀分给各个 worker，再把结果汇总回来。

这里的关键点是：

1. 每个 run 相互独立；
2. 每个 worker 的工作量可静态划分；
3. 总和后直接得到总体估计值。

论文也提到，理论上可以再加 work-stealing 去抵消机器波动，但在他们的实验里，简单均分就已经接近线性扩展，所以没必要额外复杂化。

### 4. 在参数维度上，引入 parameterized `UPPAAL-SMC`

这篇论文和单纯 distributed SMC 不同，它还把“多参数重复调用 `UPPAAL-SMC`”也系统化了。

作者在 `UPPAAL` 输入语言上加入：

1. `#range(a, b)`
2. `#booleanmatrix(N)`

前者表示一维离散参数域，后者直接表示网络拓扑矩阵的参数空间。这样就能把“同一个模型在不同参数下的很多次调用”当成一批相互独立作业统一管理。

在执行层面，这些作业被当成彼此独立的 `UPPAAL-SMC` 调用，可以通过：

1. `SLURM` 批处理系统
2. 或 SSH 分发

扔到异构 cluster 上执行。于是这个框架不仅能给出一两个概率结果，还能系统做：

1. parameter sweep
2. worst-case / optimization
3. Nash equilibrium 计算

### 5. 用 train-gate、Firewire、LMAC、Aloha 展示两类并行收益

论文实验并不是只给一个小 benchmark。

1. 对 distributed statistical testing，作者用 train-gate、Firewire、LMAC 展示 batch / buffer 调参后接近线性的速度提升。
2. 对 distributed parametric analysis，作者用 railway bridge 与 Aloha 协议展示：
   - 参数扫面曲线如何被批量生成；
   - 不同节点数下如何找 Nash equilibrium；
   - 带 `#booleanmatrix` 的网络拓扑如何被系统检索。

这说明本文的方法并不局限于“加速同一个统计检验”，还把 `SMC` 变成了一个更通用的 exploration platform。

## 解决了什么问题

这篇论文解决了 `UPPAAL-SMC` 走向实际大规模使用时的两个核心瓶颈。

第一，它解决了 distributed sequential testing 的偏差问题。作者没有停在“可以并行”这种口号上，而是明确区分：

1. fixed-sample estimation 的天然并行；
2. sequential testing 的有偏风险；

并给出 batch + buffer 的实作化方案。

第二，它把参数化分析作为一等任务纳入 `UPPAAL-SMC` 工作流。这样 `SMC` 不只是“估一个概率”，还可以系统地做参数寻优、参数敏感性分析和策略稳定性分析。

第三，它展示了 `UPPAAL-SMC` 的一个重要扩张方向：当单次模型检查已不再是主瓶颈时，调度、通信和任务组织本身也成为形式化工具链的一部分。这条线后来继续延伸到更现代的 distributed SMC、rare-event 技术和 GPU-SMC。

## 与 UPPAAL 技术线的关系

本文与 `UPPAAL` 技术线的关系非常直接：

1. 它建立在 `UPPAAL-SMC` 已有的 stochastic timed automata / priced timed automata 支线上。
2. 它把这条支线从单机统计验证推进到了 cluster 级并行。
3. 它为后续 `distributed SMC`、`importance splitting`、`GPU-SMC` 等性能增强工作打开了路径。

如果从文库主线看，它最靠近：

1. `SMC`
2. `distributed SMC`
3. `parametric exploration`

也可以把它看成 `UPPAAL` 在“性能工程 + 实验工作流”方向上的重要一步。

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟩 较完整`。它把：

1. NPTA/PWCTL 背景；
2. sequential testing 与 estimation 的统计需求；
3. distributed master/slave 方案；
4. parameterized extensions 与 cluster 调度；
5. 多个案例；

都交代得比较清楚。真正没完全展开的是内部实现代码结构和更细的通信协议实现。

从实现可获取程度看，更适合标 `🟧 仅可执行/可使用版本可得`。原因是：

1. 论文明确说结果已经实现到 `UPPAAL-SMC`；
2. 还给了模型与性质的网页入口；
3. 但目前看不到对应 distributed SMC 核心实现的公开源码仓库。

因此，这篇条目的源码线索主要是：

1. `UPPAAL-SMC` 工具线；
2. 作者主页上的模型资源；
3. `SLURM/SSH` 调度思路与语言扩展定义。

## 对本研究的启发

对当前博士研究，这篇论文的启发主要在于：当验证流程进入大规模自动化阶段，**调度与任务组织本身也是研究对象**。

具体有三点值得迁移：

1. 如果未来你的验证场景生成器一次吐出大量候选模型/性质组合，后端验证不应只看单条查询，而应像本文一样把“批量调度”纳入设计。
2. 统计或启发式验证若进入闭环，不仅要保证正确性，还要防止由于异步执行顺序不同而引入偏差。
3. 参数扫面思路很适合迁移到“验证 profile”或“修复参数”搜索上，把单次验证扩展成系统性实验。

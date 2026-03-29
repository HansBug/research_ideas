# GPU Accelerating Statistical Model Checking for Extended Timed Automata

- 问题一句话：`UPPAAL-SMC` 的瓶颈已不只是算法复杂度，而是大规模仿真在 CPU/cluster 上的时间与能耗成本。
- 方法一句话：为 `NSXTA` 构建 CUDA 版 `SMAcc`，把定量 `SMC` 的独立采样分配到 GPU threads，并通过 JIT、Polish notation、weakest preconditions 与 shared memory 降低 thread divergence。
- 解决点一句话：把 `UPPAAL` 风格扩展随机 timed automata 的 `SMC` 推到 GPU 平台，获得显著的时间与能耗改进。

## 论文定位

这篇论文属于 `⚡ 改进与扩展`，是 `UPPAAL-SMC` 性能演进线在 2020s 的一个很新节点。若说 [bulychev11-distributed-parametric-statistical-model-checking](./../bulychev11-distributed-parametric-statistical-model-checking/) 和 [bulychev12-distributed-statistical-model-checking](./../bulychev12-distributed-statistical-model-checking/) 解决的是 cluster/CPU 并行问题，那么本文解决的是：**当采样规模继续增大时，能否把 `SMC` 的核心仿真工作迁到 GPU**。

它之所以重要，不只是因为“GPU 更快”，而是因为 `UPPAAL` 这里的对象已经不是简单 Markov chain，而是 `Networks of Stochastic Extended Timed Automata (NSXTA)`：

1. 有 clock；
2. 有整数与表达式；
3. 有同步与竞速；
4. 有复杂 branching。

这类模型比传统线性代数型 GPU 任务更容易出现 thread divergence，因此本文本质上是在解决“`UPPAAL` 这类复杂语言怎样适配 GPU 架构”。

## 立足问题

`SMC` 的核心代价是重复采样。理论上，每条 run 独立，天然适合并行；但现实中的 `UPPAAL-SMC` 模型存在几个阻碍。

第一，`NSXTA` 模型往往含有复杂表达式、guards、updates 与随机延时竞赛。不同 run 很容易走到不同控制流路径，从而让 GPU 的 SIMD/SIMT 优势被 thread divergence 吃掉。

第二，不像流体力学或矩阵运算那样的 GPU 友好任务，`NSXTA` 的单次仿真里：

1. 每一步都要先为每个组件采样 delay；
2. 再解决 race；
3. 再选 winning transition；
4. 再更新复杂表达式与离散数据。

这导致“把 CPU 代码直接搬到 GPU”几乎不可能高效。

第三，定量 `SMC` 为了达到给定置信度，本来就需要很多条 independent runs。若继续完全靠 CPU cluster：

1. 时间开销高；
2. 能耗也高；
3. 一些原本要上 cluster 的模型，不适合日常工作站环境。

因此，本文真正盯住的问题是：如何把 `UPPAAL` 风格 `NSXTA` 的 SMC engine 重新设计成 GPU 友好的执行模式，同时尽可能减少 divergence。

## 核心方法

论文的方法有三层：把定量 `SMC` 重新表达到 GPU 可执行框架里、设计 `SMAcc` 内部表示、再用一系列针对 divergence 的优化把性能拉起来。

### 1. 从 `NSXTA` 的随机运行语义出发，固定每个线程承担的样本数

论文延续 `UPPAAL-SMC` 的基本随机运行语义：每个组件按其 stochastic semantics 采样 delay，最小 delay 的组件赢得 race，然后触发对应动作。对定量问题，仍然是估计：

$$
P(N \models \varphi)
$$

而估计所需的样本数来自 Chernoff-Hoeffding bound。作者把这一点改写成 GPU-friendly 版本时，最关键的决定是：**每个线程分配固定数目的 simulations**。

原因在于，如果让线程“谁先做完谁多跑几个样本”，就会引入对短 trace 的过采样偏差。固定样本数虽然可能产生 straggler，但统计上是安全的。

### 2. 设计 `SMAcc`：把 `NSXTA` 解析成适合 host/device 迁移的树结构

论文中的工具 `SMAcc` 先在 CPU 端解析 `Uppaal` 风格输入，再转成内部表示：

1. abstract syntax trees
2. expression trees

之所以使用树，是因为 guards、updates、rates、weights 等值在 `NSXTA` 里都可能是复杂表达式。作者又必须考虑 CUDA 不支持普通递归调用栈，因此专门使用**非递归后序遍历**与显式 stack 来求值表达式树。

这一步已经显出本文的难点：并不是“采样逻辑难”，而是表达式求值本身就会造成严重 divergence。

### 3. GPU 上的 `SMC` 算法：并行跑 trajectory，而不是并行一条 trajectory 内部

作者明确选择的并行粒度是：

1. 一个 thread 负责若干完整 random runs；
2. 而不是让多个 thread 合作求一条 run。

这很合理，因为 `SMC` 的天然并行性来自样本独立，而单条 run 内部由于竞速和分支太复杂，进一步拆细反而很难控制。

对应的 CUDA 版算法里：

1. 总样本数先按置信度与误差界算出；
2. 再均匀分配给所有 threads；
3. 每个 thread 重复调用 trajectory simulation；
4. 最后汇总所有 thread 的计数结果。

### 4. 识别并攻击两类 thread divergence

论文把 divergence 来源总结得很清楚。

#### 4.1 表达式复杂度导致的 divergence

不同 automaton 位置上的 guards / invariants / updates 复杂度可能完全不同。若直接解释执行 expression tree，同一 warp 中不同线程常会走不同求值路径。

#### 4.2 delay re-sampling 导致的 divergence

某些线程一次就能采到合法 delay，另一些线程则要反复重采。这会让同一 warp 里成功线程长时间空等。

作者承认第二类 divergence 目前没有彻底解决，因此本文主要攻的是第一类，也就是表达式与控制流层面的 divergence。

### 5. 四种关键优化

#### 5.1 JIT compilation

作者把模型表达式即时翻译成 CUDA C 代码，用 NVRTC 在运行时编译。这样做的好处不是消灭 divergence，而是让分支更短、更规则，也给编译器更多优化空间。

#### 5.2 Polish notation

另一种路线是不做 JIT，而是把表达式树转成 Polish notation，再以更线性的方式解释执行。这样能明显减少由树形结构差异带来的 branch divergence。

#### 5.3 Weakest preconditions 与表达式简化

作者观察到，传统 `Uppaal` successor 计算会在 guard、update、invariant 三处都可能分支。于是他们把 destination invariant 往前推到 edge guard 上，做 weakest precondition，再配合恒等式简化，把多个分支点压缩成更少的分支。

#### 5.4 Shared memory

若模型尺寸允许，就把模型放到 GPU 的 shared memory 而不是 global memory，以降低读取延迟。这个优化的限制在于：模型过大或 block/thread 配置不合适时，shared memory 容量不够。

### 6. 与 CPU、`Uppaal` baseline、不同优化版本系统对比

实验部分不是只做一个“GPU 对 CPU”的粗比。作者系统比较：

1. `Uppaal` baseline
2. `SMAcc` 单核 baseline
3. 多核 CPU 版
4. GPU 版的 post-order expression traversal
5. GPU 版的 Polish notation
6. GPU 版的 JIT
7. shared-memory 优化版本

并在 ALOHA、CSMA、Fischer、Covid、Bluetooth、Firewire 等多类模型上比较运行时间与表现。结果显示：

1. GPU 在很多模型上能显著加速；
2. 在某些场景还有明显能耗优势；
3. 但表达式形态、模型结构和 kernel 配置对性能影响很大。

也就是说，本文不是证明“GPU 一定更好”，而是把 `NSXTA` 的 GPU-SMC 做成一条有清楚收益边界的可行路线。

## 解决了什么问题

这篇论文解决了 `UPPAAL-SMC` 继续扩展时的一个新瓶颈：当分布式 CPU 并行已不再足够便宜时，怎样把大量 statistical simulations 放到 GPU 上。

第一，它给出了首个面向 `NSXTA` 这类混合线性/非线性、带复杂离散表达式的 GPU-SMC 原型之一，而不是只处理简单概率图模型。

第二，它明确提出并实践了一套 divergence-aware 实现策略，使 GPU 化不只是“并行跑得快一点”，而是针对 `UPPAAL` 模型语言结构做了专门改造。

第三，它把性能目标从纯时间进一步扩展到能耗，这很符合近年形式化工具也要考虑实际计算成本的趋势。

第四，它让一些原本需要 CPU cluster 的估计任务，向“工作站 + 合适 GPU”迁移成为可能，降低了大规模 `SMC` 的使用门槛。

## 与 UPPAAL 技术线的关系

这篇论文在 `UPPAAL` 技术线里，是 `SMC` 分支的一次现代性能升级：

1. 前面有 `SMC` 语义与工具化；
2. 中间有 distributed SMC、importance splitting、rare-event 技术；
3. 本文则把采样执行层推到 GPU。

因此，它最适合和以下几篇连起来看：

1. `david11-smc`：统计模型检查进入 `UPPAAL`
2. `bulychev11/12`：分布式 cluster 并行
3. `muniz24`：GPU 并行与 divergence-aware engine

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟩 较完整`。它不仅讲了高层算法，还讲了：

1. internal representation
2. CUDA execution model
3. divergence 来源
4. 四类优化
5. 多组实验

从实现可获取程度看，更适合标 `🟨 部分实现源码可得`。论文明确有 `SMAcc` prototype，但当前文本里没有像 `lu22` 那样直接给出明确公开仓库链接；更像是原型实现存在、工具线索清楚，但完整公开源码入口未在文中稳定给出。

因此，这篇条目的实现线索更接近：

1. `SMAcc` 原型；
2. `UPPAAL-SMC` 既有模型语法；
3. GPU/CUDA 相关实现思路。

## 对本研究的启发

对当前博士研究，这篇论文最值得迁移的是两个观念。

第一，**大规模自动化验证的瓶颈可能落在执行层，而不是判定逻辑本身**。如果你的闭环未来要并行评估大量场景、性质或修复候选，那么如何映射到 CPU/GPU 架构会成为实际问题。

第二，**表达式形态本身会决定并行效率**。这对 LLM 生成模型很重要，因为若模型表达式过于复杂、分支过深，即使语义正确，也可能让后端执行效率崩掉。换句话说，生成阶段就该考虑“是否便于验证执行”。

第三，本文把 weakest precondition、JIT、表达式线性化这些编译/程序分析思路拉进了 `SMC` 引擎，说明形式化工具和程序优化之间的边界其实非常薄，这对你的工具链设计也很有借鉴意义。

# 道口恒定预警时间计数逻辑 / Standardization of Logic for a Constant Warning Time Control at Automatic Level Crossings

## 论文在讲什么

这篇论文讨论的是日本自动道口中“恒定预警时间控制”逻辑的标准化问题。作者关心的不是抽象 signalling theory，而是一个很现实的工程痛点：如果道口始终按最快列车设计 warning time，那么低速进站列车会导致道口长时间关闭，给道路交通带来很大负担。传统方案虽然已经能用 `ATS-P` 和多组 track circuits 缩短 warning time，但每个道口的 relay logic 都需要单独设计和测试，维护成本很高。

作者提出的新方案把重点放在 software logic 上，而不是继续堆轨道电路和继电器。他们把 passing train、stopping train 和 leaving point 分别压缩到 `A / E / B` 三个探测点，再用 `AB / EB` 两个列车计数器加 first-train 判定逻辑，统一处理 warning 开始、持续和 barrier reopening。论文因此不是简单讲“道口系统概述”，而是在正文里给出一套可复用的控制器逻辑。

## 控制系统在文中的位置

这套控制系统描述就是文中的核心对象。论文的主要目标是证明：原来依赖大量 track circuits 的 constant-warning logic，可以被一个更标准化的软件控制器替代，而且这个控制器足够具体，能够直接解释 passing train 和 stopping train 怎样触发 warning、following train 怎样被追踪、barrier 在什么条件下才允许重新打开。

对 `sources/` 来说，这一点尤其有用，因为作者没有停留在“铁路系统需要更智能的控制”这种高层口号，而是把控制器拆成 `train count logic / warning control logic / diagnostic logic` 三部分，再说明两个 counter、first-train judgement、warning continuation 和 barrier opening 的关系。这些内容已经足够支撑一个完整 EFSM 条目，而不只是铁路方法论文里的附带示例。

## 对我们为什么有用

这篇论文补的是铁路方向里一种相对稀缺的样本类型：不是联锁表、route reservation 或 protocol-style interlocking，而是面向道口 warning controller 的工程逻辑。它既有明确的输入事件与探测点，也有内部扩展变量形式的计数器和 first-train 标记，还把输出效果直接落实到 warning 持续与 barrier 开闭上，因此特别适合归入 `EFSM + T0` 的高质量样本。

此外，它还能帮助样本库覆盖“计数器驱动的离散控制逻辑”这一类结构。很多铁路论文更偏资源互斥或 route locking，而这篇更像是一个带内部状态变量的现场控制器：同样有很强的离散控制语义，但控制核心来自 detector event、counter update 和 first/following train 的差异化处理。这种类型对后续状态机自动建模的泛化能力是有补益的。

## 如果需要人工细读，建议怎么读

如果后续要人工细读，建议先看第 2-3 页理解旧系统里的 `A / E / B` 三个探测点和 passing/stopping train 的基本 warning 规则，再直接跳到第 8-10 页的 `3.2 Standardization of logic`。重读时第一优先级是把 `AB / EB` 两个 counter 的含义、first-train judgement、warning 什么时候开始、什么时候允许结束这四件事读稳，因为它们构成了主控制链。

第 4-7 页关于不同 track-circuit position patterns 的分析可以放在第二轮再看，它们更像是作者论证“为什么旧方案难以标准化”的背景材料，而不是状态机条目的主干。如果只是为了重写 `STM.md`，最值得优先保住的仍然是 detector 角色、双计数器更新逻辑、first-train / following-train 区分，以及 barrier 只在 `AB = 0` 且 `EB = 0` 时才允许打开这一关键 guard。

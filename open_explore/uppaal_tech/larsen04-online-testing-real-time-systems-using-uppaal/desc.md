# Online Testing of Real-time Systems Using Uppaal

- 问题一句话：要把 `UPPAAL` 从“只验证模型”推进到“在线测试真实实现”，必须同时解决实时 conformance 定义、环境建模、在线状态估计以及算法正确性证明。
- 方法一句话：论文引入 `TIOTS` 与 relativized timed input/output conformance，在显式环境假设下给出随机化在线测试算法，并用 zones 进行 symbolic state-set tracking。
- 解决点一句话：它把 2003 年的 testing 原型推进成一篇带完整语义框架、soundness / probabilistic completeness 说明和实验验证的正式论文。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `🛠️ 工程/工具链` 与 `🧪 扩展方向`，但比 [mikucionis03-online-on-the-fly-testing-real-time-systems](../mikucionis03-online-on-the-fly-testing-real-time-systems/) 更成熟、更完整。若说 `2003` 那篇是 testing 分支的起步原型，那么这篇就是 testing 分支的**第一篇正式成形论文**。

它的新增价值主要体现在三点：

1. 语义基础不再只讲 timed trace inclusion，而是引入更正式的 `TIOTS` 框架；
2. 把 environment assumptions 显式做成 relativized conformance；
3. 对在线算法给出 soundness 与 probabilistic completeness 口径，并补上更完整实验。

因此，这篇论文不是简单重复 `2003` 版，而是把 testing 线从 prototype 推到可正式讨论的理论-工程结合状态。

## 立足问题

这篇论文立足的问题，是如何让实时在线测试真正成为一件“理论上站得住、工具上跑得动”的事情。

与 `2003` 版相比，作者这里更加明确地指出几个关键难点：

1. **实时系统测试不能只关心动作序列**
   - timing 本身就是待检对象。
2. **不同环境下的正确性不能混在一起**
   - 某实现可能在一个环境下完全没问题，在另一个更激进环境下不对。
3. **非确定规格与 dense-time 让离线 determinization 很不现实**
   - 所以 online 是自然选择。
4. **若算法要被信任，就必须说明何时 sound、何时 complete**
   - 不能停留在“实验看起来不错”。

因此论文真正面对的是一个四合一问题：

> 什么叫“相对某环境的实时实现正确”；怎样在线测试；怎样在连续时间上维护可能状态集；以及这样的算法到底有没有理论保证。

## 核心方法

这篇论文的方法比 `2003` 版更系统，可以拆成六步。

### 1. 用 `TIOTS` 统一描述实现、规格与环境

论文先引入 `Timed I/O Transition Systems`，简称 `TIOTS`。其核心对象是：

1. 输入动作集合；
2. 输出动作集合；
3. `τ` 内部动作；
4. 时间延迟；
5. 满足 time determinism 和 time additivity 的转移系统。

这一步的意义很大，因为 testing 现在不再只是对某个 timed automata 直接做 ad hoc 解释，而是先有一个统一的 I/O 语义对象。

作者还特别要求某些系统满足：

1. strongly input enabled；
2. non-blocking；
3. 对潜在实现还讨论 isolated outputs 与 determinism。

这些假设正是后面 soundness / completeness 证明所依赖的“测试假设”。

### 2. 定义 relativized timed input/output conformance

这是全文最关键的理论点之一。作者不是只写：

$$
\text{Traces}(IUT) \subseteq \text{Traces}(Spec)
$$

而是把环境 `E` 显式带进关系里，定义相对某环境状态 `e` 的 conformance：

$$
s\; rtioco_e\; t
$$

其直觉是：

1. 只有那些环境 `E` 真会产生的测试场景才需要被纳入判断；
2. 在这些场景下，`IUT` 的可观察输出和可允许 delay 必须被规格 `S` 允许。

这一步比单纯 timed trace inclusion 多走了一步，因为它把环境约束和实现规范分离了：

1. `E` 决定测试生成与输入激励；
2. `S` 决定输出是否合法；
3. 同一实现在更弱或更强环境下，conformance 结论可能不同。

作者还讨论了环境之间的 preorder，即哪个环境更“有辨别力”。这说明他们不是简单加了个环境对象，而是真的把“相对环境”做成了 testing 理论的一部分。

### 3. 在线算法维护联合状态集 `Z`

测试算法的基本状态不再只是规格状态，而是实现模型与环境模型并行后的可能联合状态集：

$$
Z \subseteq S \times E
$$

算法循环大意是：

1. 根据环境模型选择一个输入，或者选择等待一段时间；
2. 执行后观察 IUT 是否输出；
3. 用观察到的动作/延迟更新 `Z`；
4. 若更新结果为空，或输出不在允许集合中，则给 `fail`；
5. 若当前 run 正常结束，则给 `pass`。

和 `2003` 原型相比，这里的一个关键提升是：作者清楚地区分了

1. 环境允许给什么输入；
2. 实现允许给出什么输出；
3. delay 什么时候是合法的；

因此 verdict 的依据更细、更干净。

### 4. 用 symbolic zones 实现 `After` 运算

虽然理论层换成了 `TIOTS`，但真正让工具跑起来的，仍然是 `UPPAAL` 的 symbolic engine。论文继续采用：

$$
Z \; After \; a
$$

和

$$
Z \; After \; d
$$

这两个基本算子。

底层对象仍是 zone。作者定义：

1. `Closure_tau`
2. `Closure_tau^d`

并通过 auxiliary clock `t` 来裁剪 delay closure。这与 `2003` 版相同，但这里讲得更系统，也更明确地嵌入到完整算法和证明框架中。

换句话说，这篇论文的结构很漂亮：

1. 顶层是 `TIOTS`；
2. 中层是 `rtioco_e`；
3. 算法层是 online randomized testing；
4. 实现层仍回到 zones / `UPPAAL` reachability engine。

### 5. 给出 soundness 与 probabilistic completeness 口径

这是这篇论文相较 `2003` 条目的最大进步之一。作者在特定测试假设下证明：

1. 若 `IUT` 不满足 relativized conformance，则算法最终以概率 1 给出 `fail`；
2. 若 `IUT` 满足 conformance，则算法不会给出错误 `fail`，并能在适当条件下给出 `pass`。

这里的“complete”不是绝对穷尽式 completeness，而是与 randomized choices 相关的 probabilistic completeness。作者并没有回避这一点，而是明确写出前提：

1. `IUT` 需可由 input-enabled、non-blocking、deterministic、isolated-output 的 `TIOTS` 建模；
2. 环境与规格满足相应 closure 条件；
3. 随机化策略满足一定“最终会探索到区分性行为”的要求。

这种写法很扎实，因为它准确区分了工具原理与使用前提。

### 6. 用 train controller case 做中等规模实验

论文最后仍用 train controller 及 mutants 做实验，但描述比 `2003` 版更完整。

实验重点包括：

1. error detection capability；
2. state-set size；
3. `After(delay)` / `After(action)` computation time。

几个核心观察是：

1. 平均 state-set 很小，很多情况下只有 `2-3` 个 symbolic states；
2. `After(delay)` 平均代价大约毫秒量级；
3. 工具对多类 mutant 有不错检测能力；
4. 对更大或更复杂系统，仍需进一步测试与优化。

这说明 testing 线已经不只是概念验证，而是进入了可认真衡量工程表现的阶段。

## 解决了什么问题

这篇论文解决的是 testing 分支的“正式化”问题。

### 1. 它把环境显式带入 conformance 定义

这是一个很关键的升级。现实测试从来不是在“任意环境”里做的；relativized conformance 让这件事被正式化了。

### 2. 它把在线测试算法从原型提升到有证明保证的算法

有了 soundness 与 probabilistic completeness 口径，这条 testing 线才真正进入可累积的学术技术轨道。

### 3. 它证明 `UPPAAL` 的 symbolic reachability 引擎可以稳定复用到 testing

换言之，`UPPAAL` 不只是 verifier 的底盘，也可以是 online tester 的底盘。

## 与 UPPAAL 技术线的关系

这篇论文是 testing 分支的真正立柱之一。

### 它接在谁之后

它直接接在：

1. [mikucionis03-online-on-the-fly-testing-real-time-systems](../mikucionis03-online-on-the-fly-testing-real-time-systems/)
   - 提出原型框架与 `After` 路线。
2. 核心 symbolic engine 的早期实现论文
   - 因为 testing 线本质上复用 `UPPAAL` reachability。

### 它往后影响了谁

它往后明显影响：

1. [larsen04-online-testing-status-future-work](../larsen04-online-testing-status-future-work/)
   - 对工具拆分、coverage、诊断等方向做路线图总结。
2. [hessel08-testing-real-time-systems-using-uppaal](../hessel08-testing-real-time-systems-using-uppaal/)
3. [mikucionis10-online-testing-real-time-systems](../mikucionis10-online-testing-real-time-systems/)

### 它更靠近哪条主线

它最靠近：

1. relativized conformance；
2. online testing；
3. timed I/O semantics；
4. symbolic state-set based test execution。

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - 原因是它把语义对象、实现关系、在线算法、证明口径和实验都讲全了，已经明显超过早期短报告。
2. **实现可获取程度**
   - 适合评为 `🟥 源码未见明确公开`。
   - 论文明确依托 `T-UPPAAL`，但从当前条目材料看，没有看到一个稳定、仍可直接获取的正式源码入口；不能把“有工具原型”误写成“实现源码可得”。
3. **材料质量**
   - `paper_content.txt` 足够支撑这条 testing 理论线的主条目写作，是 testing 分支非常值得反复回读的一篇。

## 对本研究的启发

这篇论文对当前博士研究尤其重要，因为它展示了一个很接近你现在关心的“模型生成后如何与真实系统交互验证”的范式。

具体可借鉴的点有：

1. 若未来要把 `LLM` 生成的模型接到真实控制系统上，环境假设必须独立建模，而不是隐含在主规格里。
2. online 状态估计是连接形式模型与黑盒实现的关键机制。
3. 闭环系统里的 verdict 不应只靠一次运行结果解释，而应建立在明确的实现关系上。
4. 证明口径可以不是绝对 completeness，但必须把概率性、输入假设和适用边界写清楚。

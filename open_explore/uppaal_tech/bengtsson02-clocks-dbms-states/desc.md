# Clocks, DBMs and States in Timed Systems

- 问题一句话：`UPPAAL` 若想从“理论上可判定”走到“工程上真能跑大模型”，就必须同时解决 `DBM` 实现、difference constraints 正规化、内存压缩和并发交错爆炸这几类底层问题。
- 方法一句话：论文以 5 篇子论文为主线，系统展开 `DBM` 包实现、面向时钟差分约束的新 normalisation、状态存储压缩、`supertrace/hash-compaction` 近似存储，以及 committed locations 与 local-time semantics 的 partial-order reduction。
- 解决点一句话：它把 `UPPAAL` 在 Uppsala 侧最关键的一批底层实现工作做成了一篇 thesis 级总入口，明确说明引擎为什么能变快、为什么能省内存、为什么能少探索无谓交错。

## 论文定位

这篇论文在 `uppaal_tech/` 中应归到 `🧱 核心算法/数据结构` 与 `🛠️ 工程/工具链` 的交界位置。它不是单点算法论文，而是一篇**围绕 `UPPAAL` 底层实现问题展开的博士论文**，重点落在三个层面：

1. `DBM` 与 zone 操作如何做成真正可复用的软件包。
2. 状态空间搜索过程中怎样压缩时间和内存成本。
3. 怎样通过 committed locations 与 local-time semantics 减少 timed concurrency 的无谓交错。

论文开头摘要其实已经把主线说得非常清楚：这篇 thesis 的主要贡献就是 `UPPAAL` 的发展与实现。也就是说，它不是“借用 `UPPAAL` 做几个案例”，而是直接围绕 `UPPAAL` 内核问题展开。

从技术线位置看，它连接了早期 [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/) 与 [llpy97-compact-data-structure](../llpy97-compact-data-structure/) 的 symbolic verification 路线，也连接了后续 [behrmann02-new-uppaal-architecture](../behrmann02-new-uppaal-architecture/) 与 [david03-unification-sharing-timed-automata-verification](../david03-unification-sharing-timed-automata-verification/) 的新架构和共享存储路线。

## 立足问题

这篇 thesis 面对的问题很集中：**timed automata verification 真正难的，不只是语义或可判定性，而是引擎底层有没有一整套能够支撑长期扩展的实现技术。**

作者给出的三个核心瓶颈分别是：

1. **时钟约束表示与操作瓶颈**
   - `DBM` 是事实标准，但若没有成熟的数据结构、闭包、最小化、重置、延时、判空、正规化操作，就很难把它做成实际工具核心。
2. **空间与时间成本瓶颈**
   - 即便 symbolic state 已经比显式状态强，真实模型上还是会被 `PASSED`、`WAIT`、zone 存储、包含判定这些成本拖垮。
3. **并发交错爆炸瓶颈**
   - timed systems 的 interleavings 很多是建模引入的伪差异，不是语义上真的有意义；若全都探索，工具会很快失去可扩展性。

这篇 thesis 的价值，就在于它不把这些问题分裂看待，而是承认：它们共同构成了 `UPPAAL` 变成成熟工具前必须跨过的工程门槛。

## 核心方法

这篇论文以 5 篇子论文为主体，因此它的核心方法也最好按这 5 条线来理解。

### 1. Paper A: 把 `DBM` 做成完整可实现的软件包

第一条线是 `DBM: Structures, Operations and Implementation`。其核心目标不是重新证明 `DBM` 的理论性质，而是把 `UPPAAL` 需要的 `DBM` 操作做成完整工程基座。

其核心对象仍是差分约束：

$$
x - y \le c
$$

作者把一个 zone 看成这类约束的合取，再把它转成有向带权图与矩阵表示。方法上有几个关键点：

1. **Canonical closure**
   - 通过 shortest-path closure 让约束系统进入 canonical form。
   - 这让相同 zone 有统一表示，也让 inclusion、emptiness 等操作变得稳定。
2. **Minimal constraint systems**
   - 在保留语义的前提下去掉冗余边，减少存储与比较成本。
3. **基本操作全集**
   - 包括判空、包含、交、reset、delay、规范化等。
4. **内存表示**
   - 不只是抽象矩阵，还讨论了 `DBM` 元素在内存里的布局和稀疏存储。

这一条线的意义在于：它把“`DBM` 是可用数据结构”从文献级共识推进成了工具级实现细节。

### 2. Paper B: 为含 clock-difference guards 的模型设计新正规化算法

第二条线是这篇 thesis 里很关键、也很容易在二手介绍中被低估的一条：**当 timed automata 里出现 clock-difference guards 时，传统只看单时钟最大常数的正规化方式不够了。**

作者指出，已有文献中的 normalisation 主要依据每个 clock 的 maximal constants，但如果 automata 里存在：

$$
x - y \le c
$$

这类差分守卫，那么 termination 所需的等价抽象边界就不仅由单时钟上界决定，还受 difference constraints 影响。

因此论文提出两种新的 normalisation 算法：

1. **without zone splitting**
2. **with zone splitting**

它们共同的思想是：

1. 不只看每个时钟的最大常数；
2. 还把 automata 中真实出现的 difference constraints 纳入正规化依据；
3. 以此保证 reachability analysis 在更一般模型上的终止性。

这条线的技术意义非常大，因为它告诉我们：`UPPAAL` 的 canonical symbolic semantics 并不是一劳永逸的；一旦语言表达力扩大，正规化边界也必须重新设计。

### 3. Paper C: 从“单状态表示”与“全局状态空间表示”两边同时省内存

第三条线聚焦 memory reduction。论文把问题拆成两部分：

1. **单个 symbolic state 如何存得更紧凑**
2. **整张 `WAIT / PASSED` 结构如何少占内存**

在单状态层，作者讨论：

1. packed states
2. packed zones with cheap inclusion check

也就是说，目标不是单纯压缩字节数，而是要保证压缩后 inclusion check 仍便宜，因为 `UPPAAL` 搜索中覆盖判定是高频操作。

在全局状态空间层，作者讨论：

1. `WAIT` 的组织方式；
2. `PASSED` 的组织方式；
3. `supertrace`；
4. `hash compaction`。

这里很重要的一点是，作者并不只依赖精确存储，也研究当内存实在不够时，怎样用近似结构继续做大规模探索。`supertrace` 和 `hash compaction` 本质上都是牺牲部分完备性的近似状态存储策略，用来让原本根本放不下的模型仍有被探索的机会。

论文实验表明，这些技术显著降低了空间占用，并改善了 `UPPAAL` 的整体性能。

### 4. Paper D: 用 local-time semantics 把 partial-order reduction 真正带进 timed systems

第四条线处理并发交错爆炸。传统 partial-order reduction 在线程/进程系统里很成熟，但 timed systems 更麻烦，因为全球时钟让组件之间天然耦合。

作者在这篇 thesis 中的关键思路是：

1. 引入 **committed locations** 作为建模与验证层共同可见的标注；
2. 再把它推广到 **local-time semantics**。

committed locations 的第一层作用，是表达原子过渡中的中间状态：一旦进入 committed location，就禁止 delay，并限制允许与之交错的其他动作。

更进一步，作者提出 local-time semantics，把每个自动机的时间推进尽量留在本地尺度上，只在必要同步处重新对齐。其直觉是：

1. 某个 automaton 的局部时间推进，不应无谓地影响其他 automata；
2. 这样可以削弱很多仅由全局时标引入的伪相关性；
3. 从而让 partial-order reduction 可以真正发挥作用。

这条线是 thesis 里很有方法味的一块：它不是单纯做一个“优化启发式”，而是重新设计了 timed concurrency 的语义观察角度。

### 5. Paper E: 用 committed locations 把真实协议案例做下来

第五条线用 audio-control protocol case study 说明 committed locations 的现实价值。论文很直白地指出：

1. 某些协议若不使用 committed locations，`UPPAAL` 在当时根本跑不下来；
2. 引入 committed locations 后，状态数和时间开销大幅下降；
3. audio protocol 就是一个明确例子。

因此，Paper E 的意义不是“又做了一个案例”，而是给前面的语义与 reduction 机制提供现实验证：这不是纸上技巧，而是实际决定工具能否拿下复杂模型。

## 解决了什么问题

这篇 thesis 解决的问题非常实在，可以概括成三层。

### 1. 它让 `DBM` 从“文献中的标准表示”变成了“工具里的标准组件”

没有 Paper A/B 这条线，`UPPAAL` 很难拥有稳定而可复用的时钟约束内核，尤其很难优雅处理 difference constraints 带来的正规化问题。

### 2. 它显著缓解了 `UPPAAL` 的内存瓶颈

通过 packed state、cheap inclusion、`supertrace`、`hash compaction` 等方法，论文为大状态空间提供了从“精确压缩”到“近似存储”的一整套层次化手段。

### 3. 它把 timed partial-order reduction 做成了可落地的技术路线

通过 committed locations 与 local-time semantics，论文说明了：

1. 交错爆炸不一定只能硬算；
2. timed systems 也可以借助合适语义重写来减少伪交错；
3. 这条线在实际协议案例中确实有效。

## 与 UPPAAL 技术线的关系

这篇 thesis 是 `UPPAAL` 早期内核技术线里非常核心的一块，而且它明显带有 **Uppsala 分支** 的风格：实现细、数据结构实、对内存与并发交错问题非常敏感。

### 它接在谁之后

它接在：

1. [ad90-timed-automata](../ad90-timed-automata/)
   - 提供 timed automata 理论底座。
2. [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/)
   - 给出早期 symbolic reachability 主骨架。
3. [llpy97-compact-data-structure](../llpy97-compact-data-structure/)
   - 开始认真讨论 `DBM` 压缩与状态存储问题。

### 它往后影响了谁

它往后直接影响：

1. [behrmann02-new-uppaal-architecture](../behrmann02-new-uppaal-architecture/)
   - 对状态表示和探索架构的系统重构。
2. [behrmann02-uppaal-implementation-secrets](../behrmann02-uppaal-implementation-secrets/)
   - 把这条 thesis 里的多项工作汇入总览。
3. [david03-unification-sharing-timed-automata-verification](../david03-unification-sharing-timed-automata-verification/)
   - 在 `PWList` 与 sharing 路线上继续深化。
4. 测试线与 TIOA 线中的 symbolic state-set tracking
   - 因为这些分支也都复用 `UPPAAL` 核心 symbolic engine。

### 它更靠近哪条主线

它最靠近的是：

1. `DBM` 与 zone 操作；
2. 内存优化与状态表示；
3. partial-order reduction；
4. `UPPAAL` 引擎的可扩展实现。

## 实现与材料

1. **内容详细程度**
   - 这篇 thesis 可评为 `🟩 较完整`。
   - 原因是它不仅给出总体摘要，还把 5 篇子论文和大量实现细节放进同一份材料里，已经接近“知道该怎么复做各条技术线”的程度。
2. **实现可获取程度**
   - 可评为 `🟨 部分实现源码可得`。
   - 这篇 thesis 所述内容中的不少实现后来都以 `UPPAAL`、`UDBM` 或相关公开实现的形态继续存在，但难以得到一份与 thesis 每个子章节严格一一对应的完整历史源码快照。
3. **材料质量**
   - 根目录 `paper_content.txt` 足够支撑 thesis 级重建。
   - 另外本目录已经把 `paper-a` 到 `paper-e` 做成子阅读入口，后续若需要更深度整理某条线，直接从这些子目录继续向下切是合理的。

## 对本研究的启发

这篇 thesis 对当前博士研究的启发很强，因为它告诉我们：如果一个形式化平台要长成真正可用的研究基础设施，单靠一个漂亮的主算法远远不够。

可直接借鉴的点有：

1. 底层表示必须被当作一等研究对象，尤其是约束系统、状态对象和全局状态空间的存储方式。
2. termination 与可扩展性往往藏在“语言稍微变强之后该怎样重做正规化”这种细节里。
3. 真实工程问题里，精确算法、近似算法、语义重写和建模标注机制往往需要一起配套。
4. thesis 级父路径非常适合当“技术汇聚入口”，后续扩文库时应继续保持对子论文与总论之间关系的明确引导。

# Randomized Reachability Analysis in Uppaal: Fast Error Detection in Timed Systems

- 问题一句话：对 timed / stopwatch automata 来说，开发者经常只想赶紧知道“错误状态到底能不能到”，而完整符号搜索或 `SMC` 往往太慢、太重，甚至给不出精确反例。
- 方法一句话：把前一年的 randomized falsification 思路推广到一般 reachability，设计多种 random walk 启发式、动态 delay 分布、可调 walk 深度与“最短/最快”反例搜索，并直接做进 `Uppaal`。
- 解决点一句话：为 `UPPAAL` 增加了一种真正面向开发过程的“快速找错”工作模式，尤其对 stopwatch 场景和 rare-event detection 很有价值。

## 论文定位

这篇论文是 [kiviriga20-randomized-refinement-checking-tioa](../kiviriga20-randomized-refinement-checking-tioa/) 的自然推广，但影响面更广。前一篇还局限在 `TIOA refinement` falsification；这篇则直接面向 `UPPAAL` 用户最常做的 reachability 问题：

1. 某个 error location 能不能到。
2. deadline miss 能不能发生。
3. 复杂 stopwatch model 里某个看起来可疑的状态到底是不是可达。

更重要的是，这篇论文不再只是 Java prototype，而是明确把 randomized reachability analysis 实现并开放到 `Uppaal` 里。因此它在技术线里的地位，不只是“提出思路”，而是“让这种思路真正进入主工具工作流”。

## 立足问题

论文立足的问题，可以概括成一句话：**开发过程中，错误检测和最终证明需要不同工具**。

### 1. 符号 reachability 对大型 timed system 仍然太贵

作者开篇强调，timed automata 建模时，开发者会频繁写一些 sanity queries，就像软件开发里的单元测试一样。如果每次模型多改一点，都必须重新做一轮重型符号分析，反馈会很慢。

尤其在大型系统上：

1. 状态空间爆炸让 BFS/DFS 类方法很快吃满内存或时间。
2. 即便是 `Uppaal` 这样的成熟工具，也不能改变这一基本困难。

### 2. `SMC` 在 rare-event falsification 上并不总合适

论文明确区分了 `SMC` 和 randomized reachability 的目标。

`SMC` 的设计目标是：

1. 按 stochastic semantics 采样。
2. 估计性质满足概率。
3. 给出统计置信度。

但如果目标是找 reachability counterexample，特别是“极窄 guard”“极少发生的 deadline miss”“必须踩中特定边界时机”的情况，那么 `SMC` 可能极其低效。论文用 timed automata 例子说明：在宽区间上均匀选 delay 时，少数关键窗口几乎永远碰不到。

### 3. Stopwatch automata 还多了一层“精确反例”需求

论文特别重视 stopwatch model，因为这类模型在 `Uppaal` 里的符号分析常常是 over-approximate 的：

1. 它可以证明某些安全性。
2. 但当它给出可达 trace 时，那个 trace 可能是 spurious。

这意味着在 stopwatch 系统上，哪怕符号分析发现“也许能到错误状态”，开发者仍然需要一条 concrete trace 来确认。随机化具体运行正好填上这个缺口。

所以这篇论文瞄准的并不是“替代所有符号分析”，而是提供一种：

1. 更轻量；
2. 更快；
3. 更适合找到 concrete error trace；

的补充分析模式。

## 核心方法

这篇论文的技术核心，是把 random walk falsification 从 refinement 推广到一般 reachability，并围绕 timed systems 的特殊难点做了多层启发式设计。

### 1. 用 repeated concrete random walks 做 under-approximate reachability

和前一篇一样，方法依然工作在 concrete states 上，而非符号 zones 上。每条 random walk 都很轻：

1. 不保留 explored graph。
2. 不维护大型 passed/waiting 结构。
3. 只记录当前具体状态和当前最优反例。

这种做法天生 under-approximate：

1. 找到目标状态，就说明确实可达。
2. 找不到，不说明不可达。

它的价值就在于：如果目标是 rare event，许多实例里 under-approximate concrete search 反而能比重型完整搜索快几个数量级。

### 2. 提出四类随机化启发式

论文系统比较了四类 reachability 启发式：

1. `SEM`
   - semantic exploration
   - 先在可能 delay 上采样，再选动作
   - 最接近“朴素随机跑”
2. `RET`
   - Random Enabled Transition
   - 先选 eventually enabled transition，再为它选 delay
3. `RLC`
   - Random Least Coverage
   - 优先选择覆盖次数最少的 transition
4. `RLC-A`
   - Random Least Coverage Accumulative
   - 类似 `RLC`，但 coverage 在多次 walk 间累计，而不是每轮重置

这四类启发式的区别，不只是“速度快慢”，而是对应四种不同偏好：

1. 朴素语义式探索。
2. 公平地优先遍历边。
3. 刻意拉高未覆盖边的探索频率。
4. 在全局上持续偏好低覆盖区域。

### 3. 继续采用边界偏置的 delay 选择，并允许中间值

延续前作思想，论文继续强调：delay 选择不能是简单均匀随机，否则 timed rare event 往往永远碰不到。于是作者使用一组 delay probability distributions，在 lower bound、upper bound 和中间值之间切换。

与前一篇相比，这里一个重要改进是：

1. 不是只在 `LB`/`UB` 间轮换；
2. 还加入 `40% LB / 40% UB / 20% 中间值` 这种分布；

这样可以避免某些需要“中间延迟”才能到达的目标被系统性漏掉。也就是说，论文试图在“边界优先”和“完整覆盖可能性”之间取得更稳妥的平衡。

### 4. 动态增长 random walk 深度

如果每条 walk 都只有很浅的 step bound，就很难穿透长执行链；但一开始就给特别深的 walk，又会让每轮试探很慢。论文因此采用动态 walk depth：

1. 初始一批 walk 的深度较浅。
2. 当完整跑过一轮 delay distributions 后，再把最大深度翻倍。
3. 直到达到预设上限。

这体现出一种很典型的 falsification 思维：

1. 先尝试快速抓浅层错误。
2. 再逐步把搜索半径扩出去。

### 5. 支持“更短”或“更快”反例搜索

论文非常重视一个实际开发问题：找到任何一条错误 trace 只是开始，开发者通常更希望拿到：

1. 更短的 trace
2. 或更快达到错误的 trace

因为更短/更快的反例更容易分析和调试。

因此作者在 randomized reachability 里又加入了两个优化模式：

1. `-S`
   - 搜索更少步数的 trace。
2. `-F`
   - 搜索总延迟更小的 trace。

它们的做法都不是 exhaustive optimal search，而是：

1. 先找到一条错误 trace。
2. 然后把后续 walk 的约束收紧，只接受比当前最优更短/更快的候选。

这和符号最优反例搜索的思想不同，但对 under-approximate 方法非常实用，因为它几乎不额外增加内存负担。

### 6. 把方法落实到 `Uppaal` 里，而不只是独立原型

这篇论文和前作相比的一个最大差别，在于它明确是主工具集成工作。也就是说：

1. 用户可以在 `Uppaal` 内直接使用 randomized reachability。
2. 它能处理 `Uppaal` 已支持的 timed automata 和 stopwatch automata 模型特性。
3. 开发者无需切去单独原型工具做这类分析。

这一步让 randomized falsification 不再是实验性技巧，而变成真正可进入日常建模流程的能力。

### 7. 用 Herschel-Planck 说明方法在 stopwatch / schedulability 上的价值

论文里最亮眼的案例，是重新分析 ESA Herschel-Planck 卫星系统的 schedulability。

这里的问题特别适合这篇论文：

1. 系统大。
2. 有 preemption，要用 stopwatch automata 编码。
3. 符号分析可能给出 spurious traces。
4. `SMC` 在某些执行时间区间设置上很慢。

论文结果非常强：

1. 某些设置下，`SMC` 需要大约 `23` 小时才能找到 unschedulability witness。
2. randomized reachability 只需大约 `23` 秒。
3. 还把原来只能证 `f <= 71%` 左右的区域，推进到更高的 execution-time ratio 区间。

更重要的是，这里找到的是 concrete trace，不是 stopwatch over-approximation 里的伪迹。

### 8. 在其他 benchmark 上验证可扩展性

除了 Herschel-Planck，论文还做了：

1. 更多 schedulability benchmark。
2. 学生编写的 Gossiping Girls 模型。
3. 一系列经典 `Uppaal` benchmark 的放大版本。

从结果看：

1. 随机化方法在很多模型上比 BFS/DFS/RDFS/SMC 快几个数量级。
2. 内存占用几乎与模型大小无关，通常只需几十 MB。
3. 不同启发式在不同模型上的优劣差异很大，说明“快速找错”本身也需要 heuristic tuning。

## 解决了什么问题

这篇论文解决的是“如何把 `UPPAAL` 用成一个适合持续开发的快速找错平台”。

### 1. 它让 reachability checking 有了轻量级早期阶段

在这篇工作之前，`UPPAAL` 用户更容易陷入“要么完整符号验证，要么 SMC”两种模式。随机化 reachability 加入后，出现了第三种模式：

1. 先用 randomized walk 疯狂找错。
2. 再决定是否需要完整证明。

这非常符合真实开发节奏。

### 2. 它为 stopwatch systems 提供了获取 exact error trace 的新手段

这一点尤其重要。对于会产生 spurious symbolic trace 的模型，随机化 concrete search 实际上是非常珍贵的补强。

### 3. 它把“短反例/快反例”正式纳入工作流

不只是“错误能不能到”，还考虑“给开发者看的 trace 是否足够好分析”。这说明论文始终把调试场景放在眼前，而不是只盯着理论 reachability 定义。

## 与 UPPAAL 技术线的关系

这篇论文的位置非常清晰：

1. 它向前继承了 `TIOA refinement falsification` 的 randomized 思路。
2. 它向外把这套思路推到整个 `Uppaal` reachability 分析。
3. 它向后预示了 `UPPAAL` 不再只有 symbolic / statistical 两种验证范式，而是多出了一条 dedicated falsification 路线。

所以它代表的是 `UPPAAL` 技术线在 2020 年代的一个很明显转向：越来越重视“开发中快速反馈”而不仅是“最终严格证明”。

## 实现与材料

- 内容详细程度：`🟩 较完整`。启发式、参数、案例和结果都交代得很细，足够理解与复现方法主线。
- 实现可获取程度：`🟧 仅可执行/可使用版本可得`。论文明确说该能力已集成进 `Uppaal`，但未提供完整公开源码仓库快照。
- 关键材料线索：
  - `UPPAAL` 下载版与文档
  - 论文附带 benchmark 数据与模型链接
  - 前序 [kiviriga20-randomized-refinement-checking-tioa](../kiviriga20-randomized-refinement-checking-tioa/)

## 对本研究的启发

对当前博士研究，这篇论文最重要的启发有四点。

1. **开发期与收尾期可以用不同验证器**
   - LLM 生成模型的早期迭代，非常适合先用 cheap randomized falsification 清理大错。
2. **错误反例的“可读性”也应该是目标**
   - 短反例、快反例对人工修复更有价值。
3. **under-approximate concrete search 对复杂执行语义很有价值**
   - 特别是 stopwatch、复杂调度、非线性 timing 误差这类符号法容易给出伪迹的场景。
4. **启发式不必统一一刀切**
   - 论文同时保留多种启发式，这种“方法组合”思路对后续做 LLM+formal 的快速回路也很重要。

总之，这篇论文把随机化 falsification 从一个局部技巧扩成了 `UPPAAL` 主工具中的正式分析模式，这对理解 `UPPAAL` 后期工作流的变化非常关键。

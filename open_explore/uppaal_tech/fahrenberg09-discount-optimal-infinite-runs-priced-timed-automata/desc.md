# Discount-Optimal Infinite Runs in Priced Timed Automata

- 问题一句话：priced timed automata 的最优性分析长期偏向有限执行，而 infinite schedule 的最优语义和可计算性仍然不清楚。
- 方法一句话：论文为 PTA 引入 exponential discounting 语义，把 infinite-run cost 定义成折扣和，并通过 corner-point abstraction 把问题归约到有限 weighted graph，再证明该归约对 discounted price 是 sound / complete 的。
- 解决点一句话：它把 `UPPAAL` 的 priced timed automata 优化线从“有限 reachability 最优”推进到了“无限运行最优”的可计算层面。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `⚡ 改进与扩展`，而且是 priced timed automata 分支里非常重要的一篇理论补链条目。它不是去改 `DBM` 或工具架构，而是在追问更深一层的问题：若系统并不以 reachability 终止，而是必须长期运行，那么“最优”应该怎么定义。

因此，它与 [behrmann01-cost-optimality-uppaal](../behrmann01-cost-optimality-uppaal/) 和 [behrmann05-optimal-scheduling-priced-timed-automata](../behrmann05-optimal-scheduling-priced-timed-automata/) 的关系很直接：

1. 前两者主要关注有限路径上的 cost-optimal reachability；
2. 本文则把优化对象改成 infinite runs；
3. 目标不再是“最便宜到达某个终点”，而是“长期运行下怎样定义并计算最优 schedule”。

这使它在 `UPPAAL` 优化路线里占了一个很特别的位置。

## 立足问题

很多 real-time scheduling / control 系统其实不会自然终止。例如：

1. 周期性调度；
2. 长期运行的控制器；
3. 永续服务系统。

在这些场景里，只讨论 reachability 或 finite horizon optimality 往往不够。因为系统真正关心的是：

1. 长期运行时是否还能保持低代价；
2. 若运行无限久，总代价到底该如何定义；
3. 这种定义是否还能被算法处理。

如果直接把无限运行的总代价写成普通求和，几乎总会发散；若改看平均代价或 limit ratio，又会突出长期稳态，削弱“越近的未来越重要”这一调度直觉。

于是论文选择了一条不同于 limit-ratio / mean-payoff 的道路：**discounting**。也就是认为越远的未来对当前决策越不重要，应该指数式折减其贡献。

这里真正的技术缺口有两个：

1. 如何为 priced timed automata 定义一个适用于 infinite runs 的 discounted cost 语义；
2. 定义出来之后，这个问题是否仍然可计算，而不是一头栽回无限维实数状态空间。

## 核心方法

本文的方法非常工整：先在 priced timed transition systems 上定义 discounted price，再证明 infinite optimality 问题可通过 corner-point abstraction 归约到有限 weighted graph。

### 1. 固定折扣因子 `\lambda`，把“越远的未来越不重要”写进语义

论文先固定一个 discount factor：

$$ 0 < \lambda < 1 $$

然后要求发生在未来 `t` 个时间单位之后的成本，按 `\lambda^t` 折扣。

对 delay transition，作者先把位置 cost rate 按时间积分并乘上折扣。也就是说，一段纯等待的代价不是简单 `r \cdot t`，而是要把连续时间中的每一小段都折扣后再求和。

因此，discounting 不是简单加在离散边上，而是同时作用于：

1. delay cost
2. discrete transition cost
3. 整条 alternating path 的累计 cost

### 2. 定义 infinite path 的 discounted price，而不是只看 finite prefix

在这套语义下，一条 alternating path `\pi` 的 discounted price 可以写成对每个离散步之前累计时间 `T_i` 的折扣求和。论文正文给出的有限路径形式大致是：

$$ P(\pi) = \sum_{i=0}^{n-1} \lambda^{T_i - 1} ( p(\text{delay}_i) + \lambda^{t_i} p(\text{edge}_i) ) $$

而 infinite path 的 discounted price 则是有限前缀代价的极限。随后定义从状态 `s` 出发的最优值：

$$ P_{\min}(s) = \inf \{ P(\pi) \mid \pi \text{ is an infinite path from } s \} $$

这一步非常重要，因为它把 infinite optimality 问题真正形式化了。后面所有“是否可算”的讨论，都是围绕这个对象展开的。

### 3. 允许“最优路径不存在，但最优路径族存在”

论文并没有偷懒地默认最优 infinite path 一定存在。它明确指出：

1. 某些状态下，最优值是某个 infimum；
2. 但未必存在单条 path 恰好达到该 infimum；
3. 因此需要允许 `\varepsilon`-optimal family of paths。

这说明作者非常清楚 infinite optimization 的微妙性：即便代价语义定义好了，最优值也不必自动对应到某一条“最优 run”。这对后续算法设计很关键，因为求解器可能输出的是一族逐渐逼近最优值的 schedule，而不是单条精确轨迹。

### 4. 用 corner-point abstraction 把 PTA 压缩成有限 weighted graph

真正让问题可算的关键技术，是 corner-point abstraction。直观上，它是 region abstraction 的一种强化版：

1. 先按时钟常数把 valuation 空间切成 finitely many regions；
2. 再不只记 region，还记其 corner points；
3. 用这些 corner points 构成一个有限的 weighted graph。

这样做的直觉是：虽然 zone / region 内仍有无限多 valuation，但在 discount-price 这种目标下，极值往往会在角点处达到。只要这一点能被严格证明，就可以把 infinite-dimensional optimization 拉回有限图上。

论文也确实把 PTA 问题约化到了 corner-point graph `cp(A)` 上，然后在这个有限图里求 discount-optimal infinite path。

### 5. 证明“无限维区域上的最小值落在 corner”

这是整篇文章最关键也最技术性的地方。为了证明 corner-point abstraction 不是拍脑袋近似，作者需要一个数学结果：某类定义在 infinite-dimensional zone 上的单调函数，其最小值可以在 corner 上取得。

这一步不是一般 textbook 里能直接拿来的。作者专门给出一组关于闭有界集合与函数极小值的论证，最终得到“最优值可在 corner 点上找到”的结论。

也正因为有了这个定理，后面才能说：

1. 从原 PTA 的 infinite run，可以映射到 corner-point graph 上代价不更坏的 run；
2. 反过来，从 corner-point graph 上的最优 run，也能还原回 PTA 中相应的 infinite run 或其近似族。

### 6. Soundness / completeness 使 corner-point abstraction 成为真正的求解基础

论文随后证明了两件事：

1. **soundness**
   - 原 PTA 中任意路径都能在 corner-point abstraction 中找到不更差的代表。
2. **completeness**
   - corner-point abstraction 中的最优值并不会虚假变优，能被还原回原 PTA。

有了这两点，算法就非常明确了：

1. 构造 `cp(A)`；
2. 在有限 weighted graph 上求 discount-optimal infinite path；
3. 再把结果映回原 PTA。

这里的意义在于：本文不是只定义了一种漂亮语义，而是确实把它变成了**可计算问题**。

## 解决了什么问题

这篇论文解决的是 PTA 优化线里“无限运行最优性没有清晰可计算语义”的问题。

第一，它给 infinite schedules 引入了一种非常自然的 discounted optimality 语义。相比单纯看 limit ratio，它更符合“近未来更重要”的 planning / control 直觉。

第二，它证明这件事不只是概念上好看，而是真的可算。corner-point abstraction 把无限维问题重新压回了有限图问题。

第三，它清楚承认并处理了“最优 run 可能不存在，只能有最优路径族”这一细节，没有把 infinite optimization 过分简化。

第四，它把 `UPPAAL` priced 线从 finite reachability 继续向 long-run optimization 推进，这为后续各种 planning / strategy / scheduling 扩展提供了一个更宽的语义地盘。

## 与 `UPPAAL` 技术线的关系

### 它接在谁之后

它直接接在：

1. [behrmann01-cost-optimality-uppaal](../behrmann01-cost-optimality-uppaal/)
2. [behrmann05-optimal-scheduling-priced-timed-automata](../behrmann05-optimal-scheduling-priced-timed-automata/)
3. priced timed automata 与 corner-point abstraction 的前置工作

这些工作解决的是 finite optimality；本文则把问题推进到 infinite horizon。

### 它往后影响了谁

它对后续影响主要体现在：

1. planning / strategy optimization 的理论视角
2. 更晚的 [jensen22-monte-carlo-tree-search-priced-timed-automata](../jensen22-monte-carlo-tree-search-priced-timed-automata/)
3. 更一般的“代价 + 长期运行”研究

虽然这些后继不一定都直接用 discounting，但本文把“PTA 优化不必只看 reachability”的边界打开了。

### 它更靠近哪条主线

它最靠近：

1. priced timed automata
2. infinite-horizon optimization
3. abstraction-based optimality computation

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - 定义、discount 语义、corner-point abstraction 与 soundness / completeness 都写得比较扎实，但实现层面并没有落成完整工具说明。
2. **实现可获取程度**
   - 更适合评为 `🟥 暂未获取实现源码`。
   - 论文给出的是理论算法路径，当前没有找到直接对应“discount-optimal infinite PTA”求解器的公开源码仓库。
3. **材料价值**
   - 它非常适合当作 PTA 长期最优性问题的理论入口，尤其适合补齐 finite optimality 之外的那一截语义链条。

## 对本研究的启发

对当前博士研究，这篇论文最有价值的地方在于它处理“长期运行目标”的方式。

第一，你的很多控制系统模型其实也不是一次性 reachability 问题，而是要长期维持某种行为。本文说明这类目标不能简单拿 finite-horizon 语义代替。

第二，它展示了一条很典型的形式化方法思路：先换语义，再证明恰当 abstraction 仍然保真。对后续若要给“迭代修复过程”引入长期代价函数，这条路很值得参考。

第三，它提醒我们：一旦目标变成 infinite-horizon，结果对象未必还是单条最优轨迹，可能只能得到一族逐步逼近的最优行为。这对后续自动策略生成和修复建议表示方式都很重要。

# Optimal Scheduling Using Priced Timed Automata

- 问题一句话：`UPPAAL` 已经能做 cost-optimal reachability，但还缺一套把真实 scheduling / planning 问题稳定映射进该框架的方法与工具链。
- 方法一句话：论文用 priced timed automata 给任务、资源、持续时间与代价统一建模，再在 `UPPAAL CORA` 里用 priced zones、guided search 与 branch-and-bound 做 cost-optimal reachability。
- 解决点一句话：它把 `UPPAAL` 从“验证 timed automata”推进成“求最优调度”的工程化平台，并给出了通用 resource/task 模板。

## 论文定位

这篇论文放在 `uppaal_tech/` 中，虽然带有明显的 scheduling 应用味道，但其主贡献仍然属于 `⚡ 改进与扩展`，因为它推进的是 `UPPAAL` 本体技术的使用边界：如何把 priced timed automata 真的变成一个可复用的 optimal scheduling / planning engine。

它的作用不是验证某一个具体系统，而是回答：

1. 任务与资源怎样编码成 PTA；
2. 代价如何和 timing 一起进入语义；
3. `UPPAAL CORA` 怎样做最优可达性搜索；
4. 哪些经典调度问题能被统一放进这套模板里。

所以它更像是 `UPPAAL` cost-optimal 路线的一个工程转折点，而不是一篇普通案例论文。

## 立足问题

到这篇论文出现时，`UPPAAL` 社区已经知道 timed automata 不只可以做 yes/no verification，也可以开始谈最优性。但真正把这条线推向 scheduling / planning 仍然卡着几个问题。

第一，传统 scheduling 社区常见的建模方式很多：

1. 数学规划；
2. 各类启发式 search；
3. 定制的 resource-allocation formalism。

这些方法各有优点，但若研究者已经在 `UPPAAL` 生态里工作，就会很自然地问：**为什么不能直接用 timed automata 的语义对象表达资源、持续时间和互斥约束，同时把最优调度也放进同一符号引擎里。**

第二，普通 timed automata reachability 只关心“是否能到目标”，而 scheduling 真正关心的是：

1. 什么时候能完成；
2. 花费多少；
3. 在多个可行计划里哪一个最便宜。

因此，光有 reachability 还不够，必须把累计代价与时间推进一起纳入状态语义。

第三，即便 priced timed automata 在理论上已经出现，真正面向 scheduling 时仍然缺：

1. 通用建模模板；
2. 能在无限状态语义上运行的符号代价表示；
3. 大实例下不至于直接炸掉的剪枝与搜索策略。

所以本文的核心问题并不是“某个飞机着陆例子怎么验证”，而是：**怎样把 PTA 做成一个通用的 optimal scheduling 计算载体。**

## 核心方法

论文的方法可以拆成三层：先定义 priced timed automata 的代价语义，再用 priced symbolic states 做符号化搜索，最后给出 resource / task 建模模板，把一批典型调度问题统一塞进 `UPPAAL CORA`。

### 1. 用 `P : L \cup E \to \mathbb{N}_0` 给位置与边统一加价

文章从标准 timed automata 起步，然后给位置和边都标上 price：

$$ P : L \cup E \to \mathbb{N}_0 $$

其中：

1. 位置的 price rate 表示单位时间停留成本；
2. 边的 price 表示离散动作本身的成本。

于是语义中的两类迁移都带 cost：

1. edge transition
   - 若 `(l,v)` 经边 `e` 到 `(l', v')`，则其 cost 是 `P(e)`；
2. delay transition
   - 若在位置 `l` 停留 `\delta` 时间，则其 cost 是：

$$ p = \delta \cdot P(l) $$

这一步很重要，因为它把 scheduling 里最常见的两类成本一起纳入了 timed model：

1. “执行某动作本身要花多少钱”；
2. “占着某资源或让某机器空转会持续烧多少钱”。

对于网络化 PTA，论文还直接规定向量位置的 cost rate 是各分量位置 cost rate 之和，这就让多资源系统的总成本能自然累加。

### 2. 把最优调度问题压成 cost-optimal reachability

有了 priced semantics 后，最优调度就被压成一个非常统一的问题：找一条到达目标位置的执行 `α`，让总代价最小。

若执行写成：

$$ \alpha = s_0 \xrightarrow{p_1} s_1 \xrightarrow{p_2} \cdots \xrightarrow{p_n} s_n $$

则其总代价是：

$$ \mathrm{cost}(\alpha) = \sum_{i=1}^{n} p_i $$

而最优可达性则是：

$$ \mathrm{mincost}(s) = \inf \{ \mathrm{cost}(\alpha) \mid \alpha : s_0 \to^* s \} $$

这一步的价值在于统一性。无论是 job shop、task graph 还是 aircraft landing，最终都被压成“到达某个完成状态的最小 cost”。

### 3. 用 priced symbolic states / priced zones 避开无限状态枚举

真正的技术核心在于：时钟是实数，直接枚举状态不可能。因此作者继续沿 `UPPAAL` 的符号化传统，用 priced symbolic states 来表示无限多 concrete states。

普通 zone 只保存 clock valuation 的约束集合；这里则进一步让 symbolic state 还携带一层 cost 信息。论文把它描述成：

1. 一个 zone 表示一批可能的 clock valuations；
2. 一个 affine cost plane 表示在这批 valuations 上，当前已知的最小 cost 上界。

也就是说，算法探索的不是单个状态，而是“`zone + cost function`”。

这一步是把 `UPPAAL` 的强项直接延续到 optimization 上：

1. timing 仍用 zone / DBM 表示；
2. 代价则跟着 symbolic path 累积进 symbolic state；
3. 当同一 symbolic state 被不同路径以不同 cost 抵达时，可以比较、支配并剪枝。

### 4. 在 `UPPAAL CORA` 中用 branch-and-bound 做 cost-optimal search

论文明确给出 `UPPAAL CORA` 的搜索主干是标准 branch-and-bound。算法维护：

1. `WAITING`
2. `PASSED`
3. 当前最佳上界 `COST`

其核心逻辑是：

1. 从 `WAITING` 里按某种 branching strategy 取一个 priced symbolic state `S`；
2. 若 `S` 已被更优 symbolic state 支配，或者 `S` 的当前 cost 加上剩余代价下界都不可能优于当前 `COST`，则剪掉；
3. 若 `S` 命中目标，则更新 `COST`；
4. 否则展开后继继续搜索。

这其实把 scheduling 里的“可行方案搜索 + 下界剪枝”与 `UPPAAL` 的 symbolic successor generation 完整接上了。

### 5. 搜索策略不只 BFS，还允许 lower-bound guided search

论文还明确提到 `UPPAAL CORA` 不只支持普通 breadth-first / depth-first 风格，还支持用户提供剩余代价下界估计，从而得到更像 best-first / A* 的 guided search。

这件事在 scheduling 里非常关键。因为若没有 heuristic，下界再弱一点，大模型会很快爆掉；而一旦能告诉工具“从这个 location 到 goal 至少还要花多少钱”，剪枝效率会明显上升。

这说明 `UPPAAL CORA` 并不只是把一个理论算法塞进工具，而是开始认真处理 optimization workload 所需的工程问题。

### 6. 给出通用 resource / task 模板，而不是只写单个 benchmark

我认为本文最有工程价值的地方，是它没有只展示“若干个例子能编码”，而是明确提出 generic templates。

资源模板的基本结构是：

1. `Idle`
2. `InUse`

任务模板则负责：

1. 请求资源；
2. 占用资源；
3. 满足持续时间；
4. 释放资源并转向下一阶段。

在这一层上，作者把 scheduling 的结构抽象成：

1. passive resources
2. active tasks

然后再把不同问题实例化为不同 cost、不同持续时间、不同资源约束。

### 7. 用多个经典调度问题验证“同一建模套路可复用”

文章展示的实例并不少，包括：

1. task graph scheduling
2. job shop scheduling
3. aircraft landing
4. 更工业化的资源调度问题

这些例子的真正意义不在于“谁跑得更快”，而在于说明：

1. 一套 priced timed automata 语义；
2. 一套 symbolic branch-and-bound 引擎；
3. 一组 resource/task 模板；

已经足以覆盖一批原本分散的 scheduling 问题。

## 解决了什么问题

这篇论文把 `UPPAAL` 的 cost-optimal 分支从“理论上能谈 cost”推进成“可以真的拿来做最优调度”。

第一，它给出了统一建模法。资源、任务、互斥、持续时间和代价不再需要分散在不同 formalism 里，而是能被 PTA 统一表达。

第二，它把无限状态优化问题真正做成了符号搜索问题。priced zones / symbolic states 是让 `UPPAAL` 不至于退化成普通枚举器的关键。

第三，它形成了 `UPPAAL CORA` 这条明确的工具分支。也就是说，`UPPAAL` 从此不只是 verifier，也开始成为 planner / scheduler。

第四，它把后续 priced PTA、expected cost、planning-guided search 这条线都接通了。很多更晚的工作本质上都在继续回答这里已经提出的两个问题：

1. 如何更好表示 symbolic costs；
2. 如何更快搜索到真正优的计划。

## 与 `UPPAAL` 技术线的关系

### 它接在谁之后

它直接接在：

1. [behrmann01-cost-optimality-uppaal](../behrmann01-cost-optimality-uppaal/)
   - 打开了 cost-guided reachability。
2. [behrmann03-real-time-data-structures](../behrmann03-real-time-data-structures/)
   - 整理了 priced symbolic structures 的基础。
3. 更一般的 `DBM / zone` 底盘工作。

### 它往后影响了谁

它往后影响：

1. priced timed games / optimal strategies
2. [david14-minimal-expected-cost](../david14-minimal-expected-cost/)
3. [david15-uppaal-stratego](../david15-uppaal-stratego/)
4. [jensen22-monte-carlo-tree-search-priced-timed-automata](../jensen22-monte-carlo-tree-search-priced-timed-automata/)

因为这些路线都可以被看成“如何把 `UPPAAL CORA` 式最优 reachability 继续推进”。

### 它更靠近哪条主线

它最靠近：

1. priced timed automata
2. optimal scheduling / planning
3. symbolic cost search

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - PTA 代价语义、cost-optimal reachability、branch-and-bound 和模板建模都讲得比较清楚，但它毕竟是短文，对 priced symbolic state / affine plane 的内部算法没有完全展开。
2. **实现可获取程度**
   - 更适合评为 `🟧 仅可执行/可使用版本可得`。
   - 论文明确依托 `UPPAAL CORA`，说明了工具分支真实存在，但当前没有找到与当年 `CORA` 版本直接对应的公开源码仓库。
3. **材料价值**
   - 这篇条目非常适合当作 `UPPAAL` 优化/调度方向的工程入口，尤其适合用来理解“怎样把问题建模成 PTA 并交给 symbolic optimizer”。

## 对本研究的启发

对当前博士研究，这篇论文最值得借鉴的是“把高层工程问题压成统一形式化核心”的做法。

第一，作者不是为每个调度问题重新造轮子，而是坚持用同一套 `timed automata + price + symbolic search` 框架复用。这对未来把不同控制系统验证任务压成统一 verification profile 很有启发。

第二，branch-and-bound + remain lower bound 的思想，对后续做“候选模型修复的排序”也非常有价值。很多修复不该只判断是否可行，还该判断代价是否最小。

第三，resource / task 模板的写法说明：一旦问题抽象得足够稳，工程案例其实可以批量投影到同一个形式化骨架里。这与后续 LLM 辅助建模很契合，因为模板化结构正是最容易被自动化学习和生成的部分。

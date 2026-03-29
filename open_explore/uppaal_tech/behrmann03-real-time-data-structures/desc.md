# Data Structures and Algorithms for the Analysis of Real Time Systems

- 问题一句话：`UPPAAL` 一侧的 timed reachability 已经站稳后，接下来要回答的是能否用更强的 symbolic 数据结构与代价语义，把分析能力从普通 reachability 推进到非凸表示、最优代价与调度优化。
- 方法一句话：论文以 thesis 形式串起 `CDD`、priced timed automata、priced zones、cost-optimal reachability、`guiding heuristics` 以及 `The Making of Uppaal` 中的工具架构与发展经验。
- 解决点一句话：它把 `UPPAAL` 技术线从“只会做经典 timed reachability”推进到“能讨论非凸 symbolic set、代价最优路径和调度问题”的更宽框架中。

## 论文定位

这篇论文是 Gerd Behrmann 的博士论文，也是当前文库里一个非常典型的 **thesis 级父入口**。它收了 6 篇文章，其中前两篇偏 `visualSTATE` 与 state/event systems，后四篇才逐步进入和 `UPPAAL` 最直接相关的路线：

1. `Paper C`
   - `CDD`
2. `Paper D`
   - minimum-cost reachability for priced timed automata
3. `Paper E`
   - cost-optimal guiding in `UPPAAL`
4. `Paper F`
   - priced zones / facets / efficient optimal-cost reachability

再加上 thesis 中专门有一节 `The Making of Uppaal`，这篇论文因此并不是单个结果的长版，而是一个把**数据结构、算法扩展与工具成长史**串起来的总论。

如果说 [bengtsson02-clocks-dbms-states](../bengtsson02-clocks-dbms-states/) 更像 Uppsala 侧围绕 `DBM`、状态存储与 reduction 的 thesis，那么这篇更像 Aalborg 侧向外扩展的一篇 thesis：它一方面继续追 symbolic data structure，另一方面明显把视野推进到 cost、optimality、scheduling 与工具平台化。

## 立足问题

这篇 thesis 面对的问题，比早期 `UPPAAL` 论文更“第二阶段”一些。它默认你已经接受 timed automata + symbolic reachability 这条主线成立，然后进一步追问：

1. **如果 symbolic state 不是凸的，`DBM` 还够用吗？**
2. **如果问题不再是 reachability，而是“最省代价地到达目标”或“找到最优调度”，原来的 symbolic 框架还能不能扩？**
3. **一个研究工具在不断加入新能力时，内部架构和研发方式应该怎样演进？**

这几个问题共同指向一个判断：`UPPAAL` 若只停留在“普通 reachability checker”，技术线很快会封顶。要继续生长，就必须同时改进：

1. 数据结构表达力；
2. 分析目标；
3. 工具组织方式。

因此，这篇 thesis 的问题意识并不局限于某个算法，而是非常明显地带着“如何把 `UPPAAL` 做成更广意义上的 real-time analysis platform”的味道。

## 核心方法

这篇 thesis 的方法主线可以概括为：**先扩 symbolic 表示，再扩分析语义，再扩工具能力。**

### 1. 用 `CDD` 处理 `DBM` 不擅长的非凸 symbolic 集合

论文中与 `UPPAAL` 直接相关的第一条重要路线是 `Paper C`，也就是 `Clock Difference Diagrams`。

作者非常清楚地指出，`DBM` 的标准优势在于：

1. 适合表示 convex zones；
2. 基本操作成熟；
3. 已经是 timed automata 工具事实标准。

但它也有结构性短板：union 不闭包。如果 symbolic computation 中某批状态天然应当被当成一个整体，但它们的 union 不是凸的，那么只靠 `DBM` 就不得不拆成一堆 zone 来回处理。

`CDD` 的核心思路因此是借鉴 `BDD` 风格，把 symbolic set 改写成一棵关于 clock differences 的决策图：

1. 每个内部节点代表某个 clock difference；
2. 每条边标记一个整数区间；
3. 一条到 `true` 终端的路径表示一组差分约束的合取；
4. 整棵图表示这些约束组合形成的并集。

也就是说，`CDD` 试图把：

$$
\text{union of zones}
$$

作为一等对象处理，而不是总在 `DBM federation` 层面被动维护。作者也很诚实地指出，`CDD` 不像 `ROBDD` 那样天然有漂亮的 canonical normal form，某些操作也更复杂，例如 existential quantification 可能代价很高。因此 thesis 并不是把 `CDD` 说成“全面替代 `DBM`”，而是把它作为处理非凸 symbolic 集合的一条新方向。

### 2. 用 priced timed automata 把问题从 reachability 推到 optimality

第二条关键路线是 `Paper D/E/F` 共享的那条：**把 timed automata 扩展成带代价信息的模型，并让 symbolic analysis 不只回答“能否到达”，还回答“最小代价是多少”。**

作者引入的是 linearly priced timed automata。直觉上就是：

1. location 停留会持续累积 cost rate；
2. 某些 discrete transitions 也可能带离散代价；
3. 因而路径代价不再只是“经过几步”，而是“时间与离散动作共同累积的代价函数”。

这样一来，问题从普通 reachability 变成：

$$
\min \{ \text{Cost}(\pi) \mid \pi \text{ reaches goal} \}
$$

它的意义很大，因为很多 scheduling 问题天然就是“满足可达性约束下最小化某代价”。

### 3. 用 priced zones 与 facets 支撑代价最优的 symbolic 搜索

一旦把 cost 引进来，普通 zone 已经不够，因为每个 valuation 除了是否属于该集合，还要带一个代价函数。论文因此提出 priced zones。

priced zone 的核心不只是一个普通 zone，而是：

1. 一个 zone 几何区域；
2. 一个定义在该区域上的线性代价面。

也就是说，同一个符号状态不再只是“这些 clock valuations 都可能在这里”，还包含“这些 valuations 从起点到这里的当前最优代价如何随 valuation 变化”。

这就逼出几个关键新问题：

1. intersection 怎样 lift 到 priced zones；
2. reset 与 delay 怎样更新 cost；
3. difference / subtraction 之类操作怎样处理；
4. 什么时候一个 priced zone 可被另一个安全覆盖。

论文中 `facets` 的引入正是为了解决 priced zone 运算会裂成多块的问题。其核心思想可以理解为：当代价面与约束边界交互后，单个 priced zone 可能需要沿某些边界切分成多个面片，再分别维护线性代价。

因此，作者真正做的不是“把普通 zone 上面再随便贴个数”，而是建立了一套 priced symbolic state calculus。

### 4. 用 guiding heuristics 提高 cost-optimal search 的实际效率

仅有 priced semantics 还不够，因为最优代价搜索非常容易陷入：

1. 找到一个可行但很差的解；
2. 然后长时间在巨大空间里慢慢逼近最优。

`Paper E` 于是专门处理 guiding toward cost-optimality。作者的核心判断是：如果仅凭朴素搜索顺序，即便 symbolic algorithm 理论上正确，实践上也可能很难尽快遇到好解。

因此方法上又加了一层：

1. 通过启发式 search order 让更有希望的状态更早被探索；
2. 尽早得到更低 cost 的 candidate；
3. 再利用这些 candidate 去剪掉明显不可能更优的分支。

这条线很像把经典 `UPPAAL` 的模型检查器往“带 branch-and-bound 味道的最优搜索器”方向推。

### 5. 把调度问题重写成模型检查问题

论文 repeatedly 强调：很多 scheduling 问题可以被编码为模型检查问题。核心套路是：

1. 把被调度对象、资源、顺序限制建成 timed automata / priced timed automata；
2. 把目标状态建成 reachability goal；
3. 把完成时间、资源占用或其他优化目标编码进 cost；
4. 然后用 symbolic optimal reachability 去求最优调度。

这条方法线对 `UPPAAL` 来说意义极大，因为它把工具的用途从“证明协议对不对”拓宽到了“构造或比较最优调度”。这已经不是传统 model checking 的窄定义了，而是把形式化验证技术迁移到 optimization / synthesis 邻域。

### 6. 在 `The Making of Uppaal` 里总结工具架构与研发方式

这篇 thesis 很难得的一点，是它专门有一节 `The Making of Uppaal`。这部分非常重要，因为它把 `UPPAAL` 不断成长的原因讲得很直接。

作者强调了几件事：

1. `UPPAAL` 从一开始就非常 case-study-driven。
2. 很多功能不是先拍脑袋加的，而是被实际案例“逼出来”的。
3. 工具采用 client-server 架构，GUI 与 engine 分离。
4. 引擎内部逐步走向 layered architecture，便于替换数据结构与算法模块。

这说明 thesis 的方法视角并不只停留在数学对象上，也很重视“工具为什么能不断吸收新技术并保持可用”。

## 解决了什么问题

这篇 thesis 解决的，是 `UPPAAL` 技术线第二阶段的三个核心扩展问题。

### 1. 它为非凸 symbolic 表示提供了明确路线

通过 `CDD`，作者说明 `UPPAAL` 技术线不必被 `DBM = convex zone` 的框架永久锁死。即便 `CDD` 未必成为唯一标准，它也打开了“更强 symbolic 集合表示”这扇门。

### 2. 它把最优代价与调度问题正式带入 `UPPAAL` 语境

priced timed automata、priced zones、optimal reachability 这条线，让 `UPPAAL` 不再只是做 yes/no reachability，而可以回答“多快、多省、多优”。

### 3. 它把工具成长经验也沉淀成了研究内容

很多 thesis 只写结果，不写工具是怎么长出来的；这篇不一样。`The Making of Uppaal` 明确说明平台化、架构化和案例驱动在 `UPPAAL` 成长中的作用，这对理解后续 `UPPAAL 4`、`SMC`、`Stratego` 都非常关键。

## 与 UPPAAL 技术线的关系

这篇 thesis 在 `UPPAAL` 技术线中的位置，可以概括为：**从经典 timed reachability 向更丰富 symbolic 表示与 optimality 分析扩张的桥梁。**

### 它接在谁之后

它接在：

1. [behrmann02-uppaal-implementation-secrets](../behrmann02-uppaal-implementation-secrets/)
   - 对早期实现线做过一次系统总结。
2. [behrmann01-cost-optimality-uppaal](../behrmann01-cost-optimality-uppaal/)
   - 已经把 optimality 问题带进 `UPPAAL`。
3. [hune01-guided-synthesis-control-programs-uppaal](../hune01-guided-synthesis-control-programs-uppaal/)
   - 说明 `UPPAAL` 可以不只做验证，也能往控制/合成问题走。

### 它往后影响了谁

它往后明显影响：

1. [david14-minimal-expected-cost](../david14-minimal-expected-cost/)
   - 继续把 cost/optimality 推向更复杂模型。
2. [david15-uppaal-stratego](../david15-uppaal-stratego/)
   - 从 optimality 走向策略综合与学习式控制。
3. 近年的 `MCTS`、stochastic / hybrid optimal control 分支
   - 因为它们都继承了“把调度/控制问题编进 symbolic model-checking 平台”的思路。

### 它更靠近哪条主线

它最靠近的是：

1. `CDD` 与更强 symbolic set；
2. priced timed automata；
3. cost-optimal reachability；
4. `UPPAAL` 工具成长史与架构演进。

## 实现与材料

1. **内容详细程度**
   - 这篇 thesis 可评为 `🟩 较完整`。
   - 尤其对 `CDD`、priced zones、最优代价路线和工具架构背景都给了 thesis 级描述，已经明显超出普通 conference paper 的细节量。
2. **实现可获取程度**
   - 适合评为 `🟨 部分实现源码可得`。
   - 其中不少思想后来进入 `UPPAAL` 公开工具与相关扩展中，但 thesis 各个 paper 的历史实现不一定都能以独立源码包精确回收。
3. **材料质量**
   - 根目录 `paper_content.txt` 加上当前已拆出的 `paper-intro/`、`paper-c/` 到 `paper-f/`，很适合作为后续扩展 `UPPAAL` cost / optimality 技术线的母条目。

## 对本研究的启发

这篇 thesis 对当前博士研究有两层启发。

第一层是方法论上的：一个验证平台成熟以后，下一步很自然不是只把原算法做得更快，而是问“能否支持更强表示、更多目标、更多问题类型”。  
第二层是工程上的：若希望后续把 `LLM` 与形式化方法做成长期平台，也应像 `UPPAAL` 一样，把 case-study-driven 演进、架构重构和新数据结构引入看成研究工作的组成部分，而不是附属劳动。

从文库建设角度看，这篇 thesis 也非常适合作为后续把 `CDD`、priced analysis、`Stratego` 前史和调度路线串起来的中枢节点。

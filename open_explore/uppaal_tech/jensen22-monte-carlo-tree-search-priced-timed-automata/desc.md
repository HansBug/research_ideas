# Monte Carlo Tree Search for Priced Timed Automata

- 问题一句话：`PTA` 上的最优可达/调度问题虽然可判定，`UPPAAL CORA` 等符号方法也很强，但在大规模 planning/scheduling benchmark 上仍会遇到搜索空间过大、完整方法难落地的问题。
- 方法一句话：把 `Monte Carlo Tree Search` 系统性改造到 `PTA` 上，设计适合 timed/planning 场景的树策略、delay policy 与剪枝增强。
- 解决点一句话：让 `UPPAAL` 的 `PTA` 线从纯符号 cost-optimal reachability，进一步吸收 planning 社区的 anytime / heuristic search 能力。

## 论文定位

这篇论文在 `uppaal_tech/` 技术线上属于 `⚡ 改进与扩展`，但它和常见的“验证”论文很不一样。它的关注点不是 safety/liveness model checking，而是把 `PTA` 当成一种**带时间约束的 planning formalism**，用来解决：

1. job-shop scheduling
2. task graph scheduling
3. 卫星任务规划

等典型优化问题。

因此，这篇论文的位置更接近：

1. 向前承接 `CORA` 这条 `PTA` optimal reachability 线。
2. 向外吸收 planning 社区的 `MCTS/UCT` 思想。
3. 向后预示 `UPPAAL` 在优化与控制方向上继续与 heuristic search / learning 融合。

如果说 [david15-uppaal-stratego](../david15-uppaal-stratego/) 是把“策略对象 + 优化查询”带进 `UPPAAL`，那这篇论文则是在 `PTA` 规划问题上把“启发式树搜索”明确接入 `UPPAAL` 生态。

## 立足问题

论文立足的问题非常具体：虽然 `PTA` 的最优可达问题早已可判定，也已有 `priced zones`、`corner-point` 等成熟符号方法，但真实调度问题里，完整符号搜索依然常常不够快。

作者给出的观察很准确：

1. `PTA` 形式化非常通用，足以编码大量资源分配与调度问题。
2. `UPPAAL CORA` 已成功应用于多种调度/规划案例。
3. 但规划社区的很多大型问题早已依赖启发式搜索，而 `PTA` 线还主要停留在符号法。

因此论文想问的是：

$$
\text{既然 PTA 已经能表达这些规划问题，能否也把 MCTS 这种 planning 搜索方法带进来？}
$$

这不是简单“换个求解器”，而是要解决 `MCTS` 与 `PTA` 语义之间的几处结构冲突：

1. `PTA` 允许时间延迟，理论搜索树可能无限。
2. `PTA` 的动作既包括离散 action，也包括 delay。
3. 规划目标是代价最小，而 MCTS 传统上更常用于有限游戏或离散规划。

## 核心方法

这篇论文的方法可以概括成三层：`把 PTA 变成 MCTS 可搜索的对象 -> 为 timed search 设计合适 policy -> 用若干增强让搜索更实用`。

### 1. 先把 `PTA` 写成 priced transition system，并离散化可搜索动作

论文从 `PTA` 的标准定义出发：

1. location 有 cost rate。
2. edge 有固定 cost increment。
3. 一个 run 的总代价由 delay 累计代价与 transition 代价共同构成。

为了让 `MCTS` 真能工作，作者利用 `PTA` 在 non-strict guards 下的一个经典性质：如果最大常数为 `k`，则很多 reachability/optimality 问题只需要考虑有界自然数延迟即可。

于是可搜索标签被限制到一个有限集合：

$$
\Sigma = Act \cup \mathbb{N}_{\le k+1}
$$

这一步极关键。没有它，`MCTS` 面对的是连续无限 delay 分支，树根本没法展开；有了它之后，`PTA` 才能被嵌进有限搜索树框架。

### 2. 用 timed word 构造 search tree

论文把 search tree 的节点定义成从初始状态出发的有效 timed word。也就是说：

1. 根节点是空字 `\epsilon`。
2. 每个后继节点是在当前 word 后面再接一个动作或 delay。
3. 只有对应真实 `PTA` 运行的 word 才存在于树中。

这种做法的好处是：

1. `MCTS` 能沿标准树结构工作。
2. 每个节点都天然对应一个具体 `PTA` 配置与累计代价。
3. 回报函数可以直接基于当前路径总代价定义。

这相当于把 `PTA` 优化问题重新包装成“在有限搜索树里找最优 reaching trace”。

### 3. 改写 UCT：奖励以当前 best-known cost 归一化

论文没有直接套用教科书版 UCT，而是针对 cost-minimization 做了适配。选择最优子节点时，使用 exploitation + exploration 的组合，但 exploitation 不是最大化赢率，而是偏好更小总代价。

伪代码里最佳孩子的大致评分可概括成：

$$
\frac{Q_B}{Q(n')} + C_p \sqrt{\frac{\ln V(n)}{V(n')}}
$$

其中：

1. `Q_B`
   - 当前已知最好解的代价。
2. `Q(n')`
   - 该节点累计代价/估计。
3. `V(n)`
   - 访问次数。

这种归一化设计的优点是：

1. 不依赖预先知道代价尺度。
2. 能把“越便宜越好”的优化目标自然嵌进 UCT。

### 4. 解决 `PTA` 场景下的三个非标准难点

作者专门抽出一节谈 `PTA` 对 `MCTS` 的挑战，这很值得注意。

#### 4.1 无限 transition sequence

`PTA` 里可能有 loop，因此 rollout 可能永远不终止。论文用 rollout budget 解决：simulation 到一定步数强制截断。

#### 4.2 非终止状态也要能给 reward

既然 rollout 可能被截断在非目标状态，那就不能只给 terminal reward。论文直接用当前 accumulated cost 评估非终止状态，并照样回传。

#### 4.3 dead states

`PTA` 里可能出现没有后继但也不是目标的 dead state。标准 UCT 对这类状态不够友好。论文的处理是：

1. rollout 遇到 dead state 就结束。
2. 如果 expansion 进入 dead state，则把该节点及必要祖先剪掉，避免无效反复探索。

这三点看似细节，实际上决定了 `MCTS` 能不能在 `PTA` 上真的跑起来。

### 5. 设计四类 policy，核心差别在如何处理 delay

论文最核心的方法贡献之一，是系统比较了四种 tree/default policy。

#### 5.1 `UDP`：Unit Delay Policy

只允许单位时间 delay。它最简单，也最完整，但有一个严重偏差：长延迟必须通过多次单位 delay 才能实现，因此其概率会指数下降。论文明确给出这种偏置：

$$
\Pr(s,d) = (\frac{1}{|Act_s| + 1})^d
$$

所以 `UDP` 天然偏好短延迟，对某些必须等待较久的优化问题非常不利。

#### 5.2 `DSP`：Delay Sampling Policy

作者接着提出 `DSP`，允许从 lower bound、upper bound 与中间采样值中选若干 delay，而不是只用单位 delay。这样改善了长延迟被严重低估的问题，但分支数可能变大。

#### 5.3 `NLP`：Non-Lazy Policy

受 non-lazy schedules 启发，`NLP` 只考虑：

1. `0` delay
2. 最小的 non-zero delay，使得某个动作刚好 become enabled

这显著降低了 branching factor，尤其适合许多 job-shop / scheduling 问题，因为它逼近“资源一可用就尽快用”的规划风格。

#### 5.4 `ETP`：Enabled Transition Policy

这是论文很有意思的另一条路线，明显受到 randomized reachability 思想启发。它先关注 eventually enabled actions，再用其最早 enabling delay 去组织搜索，相当于“动作优先、延迟随后”。

这说明不同 `UPPAAL` 支线之间已经开始相互借力：前面的 randomized falsification 思路，被挪到了 `PTA + MCTS` 优化搜索里。

### 6. 再加两类增强：Building Rollouts 与 Stepping

除了 policy，论文还引入了两个关键增强。

#### 6.1 `BR`：Building Rollouts

如果 rollout 中找到了当前最优 terminal solution，就把这条 rollout 真正并入树，而不是简单丢掉。这能让有价值的经验更快反馈到主树。

#### 6.2 `SP/RP`：Tree pruning with steps

论文比较了两类推进根节点的方法：

1. `RP`：relative pruning
2. `SP`：stepping pruning

其中 `SP` 用一个固定样本数阈值，当根积累足够多访问后就向前推进一步。实验发现它比 `RP` 更稳，更实用。

### 7. 用 benchmark 说明 `NLP + BR + SP` 的效果最好

论文在 job-shop、task graph 和卫星规划 benchmark 上做了大规模实验，并与：

1. `UPPAAL CORA`
2. `TiaMo`
3. 若干 randomized reachability 风格搜索

进行比较。

结果有几个核心结论：

1. `UDP` 表现最差，说明“朴素 delay 离散化”不可取。
2. `NLP` 是整体最稳的 policy。
3. `BR + SP` 对效果提升很大。
4. 在很多 benchmark 上，`MCTS` 能给出接近最优的计划。
5. 对一些符号方法很难在给定时间内解出的实例，`MCTS` 依然能给出可用方案。

这说明论文不是单纯做“另一种求解器”，而是在 `PTA` 线上真正引入了 anytime heuristic planner。

## 解决了什么问题

这篇论文主要解决了两个问题。

### 1. 它让 `PTA` 问题第一次系统性地进入 `MCTS` 工作流

此前 `PTA` 优化更多依赖完整符号法；这篇论文证明，`MCTS` 也能在这个领域有意义，而且不是玩具实现，而是能跑大规模调度 benchmark。

### 2. 它给出了一套 timed/planning 兼容的 MCTS 设计经验

也就是：

1. 必须控制 delay 分支。
2. 需要专门的 timed policy。
3. rollout、dead state、stepping 等细节都要重新设计。

这些经验本身就很有价值，因为它们说明“planning 搜索接入 formal timed model”并不是平移，而是深度改造。

## 与 UPPAAL 技术线的关系

这篇论文把 `UPPAAL` 的 `PTA` 线往 planning 方向推进了一步。它和其他路线的关系大致是：

1. 与 `CORA/TiaMo` 一样，都在处理 `PTA` 优化。
2. 与 `Stratego` 一样，都在让 `UPPAAL` 不只做验证，还做求解与规划。
3. 与 randomized analysis 线一样，都越来越接受 anytime / heuristic / under-complete 的搜索方式。

因此它代表的是 `UPPAAL` 技术线的另一个明显变化：对优化问题，不再默认只有完整符号法一种主路。

## 实现与材料

- 内容详细程度：`🟩 较完整`。形式化定义、policy、增强、实验都交代得很细，足以把主方法完全读清。
- 实现可获取程度：`🟧 仅可执行/可使用版本可得`。论文描述了实现与 benchmark，但没有在正文给出完整公开源码仓库。
- 关键材料线索：
  - `UPPAAL CORA`
  - `TiaMo`
  - 论文 benchmark 链接
  - 与 randomized reachability 的交叉引用

## 对本研究的启发

这篇论文对当前博士研究最重要的启发，不在于 `PTA` 本身，而在于**如何把 formal model 变成搜索问题**。

1. **一旦目标是优化，验证器就不该只返回布尔值**
   - 需要显式的 search tree、reward、candidate action。
2. **时间动作的搜索组织是关键**
   - 很多 formal model 的难点，不在离散动作，而在 delay 如何进入搜索。
3. **完整性与 anytime 能力可以分开看**
   - 对大模型来说，先拿到高质量候选解，再决定是否继续追最优，往往更实用。

如果以后你希望把“模型修复建议”做成带目标函数的搜索过程，这篇 `PTA + MCTS` 论文给了非常直接的设计参考。

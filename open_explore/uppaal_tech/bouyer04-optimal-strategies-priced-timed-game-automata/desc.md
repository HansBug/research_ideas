# Optimal Strategies in Priced Timed Game Automata

- 问题一句话：timed games 的可赢性已经有了成熟算法，但一旦再加入 prices，怎样计算真正的最优策略仍然远未解决。
- 方法一句话：论文先把 reachability timed game 的 winning 策略合成梳理清楚，再为 priced timed game 定义 optimal-cost 语义，并通过向游戏状态加入累计代价的归约，把最优策略问题转到可计算的线性混成博弈框架上。
- 解决点一句话：它为 `UPPAAL` 生态里的 priced timed games / optimal-control 路线给出了第一套较完整的最优性计算框架与边界条件。

## 论文定位

这篇论文在 `uppaal_tech/` 里应归到 `⚡ 改进与扩展`。它不是一般 timed automata 背景论文，而是 `timed games -> priced timed games -> optimal strategy synthesis` 这条分支上的核心理论节点。

若把 `UPPAAL` 的 games / planning 技术线粗略拆开，这篇论文的位置很清楚：

1. [cassez05-analysis-of-timed-games](../cassez05-analysis-of-timed-games/) 更偏 timed games 的 on-the-fly 求解；
2. [behrmann07-uppaal-tiga](../behrmann07-uppaal-tiga/) 是 timed games 工具化；
3. 本文则补上了“如果游戏里不仅要赢，还要以**最小代价**赢，应该怎么定义、什么时候可算、策略还是否只依赖当前状态”。

因此，这篇工作不是简单把 cost 往 timed game 上一贴，而是在问一个更深的问题：**引入代价以后，原来 timed game 的状态式策略观点还能保住多少。**

## 立足问题

reachability timed games 研究到 2004 年时，已经能回答很多经典问题：

1. 从哪些状态出发，控制方一定能赢；
2. 怎样用 controllable predecessor 迭代求 winning region；
3. 如何在 timed-game 框架里合成 controller。

但这些答案大多停在“能赢 / 不能赢”的层面。现实里的很多控制问题其实还会继续追问：

1. 赢是能赢，但**最便宜**怎么赢；
2. 若可选策略很多，哪条策略总代价最低；
3. 策略是否只需要看当前 location 与 clock valuation；
4. 还是说还必须记住“之前已经花了多少钱”。

这并不是一个把 cost-optimal reachability 直接从普通 priced timed automata 生搬到 timed games 上的问题。原因在于：

1. timed automata 里只有单方优化；
2. timed games 里有 controllable / uncontrollable 两方；
3. 一旦对手能逼你绕路、耗时或进入高 cost 区域，最优代价就不再只是单纯 shortest path。

更麻烦的是，priced timed game 里的最优值不一定天然就是“只依赖当前状态”的。也就是说，某个时刻的最优选择可能不仅取决于当前 zone，还取决于历史累计 cost。这会直接威胁 `UPPAAL` 一贯依赖的 symbolic state-based reasoning。

所以本文真正盯住的缺口是：**在带代价的 timed games 里，如何定义 optimal strategy，何时存在 state-based optimal strategy，何时必须把累计代价也纳入状态。**

## 核心方法

论文的方法不是一条单算法，而是一条从 timed game 可赢性到 priced optimality 的逐层搭建过程。

### 1. 先把 reachability timed game 的 winning 语义与策略合成重述清楚

作者先回顾 reachability timed games (`RTG`)。这一步的作用不是铺垫背景而已，而是为了把后面的 priced 版本建立在一个已经稳定的 controllable / uncontrollable predecessor 框架上。

在这类游戏里，控制方关心的是某个目标集合 `Goal` 是否最终可达。相应地，winning region 可以写成 predecessor 闭包的最小不动点：

$$ W = \mu Y . ( Goal \cup \mathrm{CPre}(Y) ) $$

这里的核心仍然是：控制方能否选择延时与 controllable action，使得无论对手怎样响应，系统都能回到 `Y` 并最终进 `Goal`。

这一步的重要性在于，论文明确保留了 timed-game 里最关键的结构：

1. 连续时间推进；
2. controllable / uncontrollable action 竞争；
3. zone-based symbolic reasoning。

后面 priced 版本不是推倒重来，而是在这套结构上继续叠加代价。

### 2. 为 priced timed game 定义 cost、strategy cost 与 optimal cost

接下来作者把 game 扩成 `priced timed game automata`。直觉上很简单：位置和边都可以带 price，时间流逝时按 rate 积累 cost，离散跳转时再叠加 edge cost。

于是对一条 run `ρ`，其总代价可以理解为“各段停留成本 + 各条离散边成本”的总和：

$$ \mathrm{Cost}(\rho) = \sum_i \mathrm{rate}(\ell_i) \cdot \delta_i + \sum_i \mathrm{price}(e_i) $$

真正棘手的是 optimality 定义。因为这是 game：

1. 控制方想最小化；
2. 环境方想让它变差。

因此某个策略 `f` 的代价，不能只看一条 run，而要看在该策略下所有对手响应里最坏的一条。再往上，optimal cost 则是控制方在所有可用策略里，把这个“最坏情形代价”压到最低：

$$ \mathrm{OptCost}(q) = \inf_f \sup_{\rho \in \mathrm{Out}(q,f)} \mathrm{Cost}(\rho) $$

这一点非常关键。因为它把“最优”明确放在博弈语义里，而不是 ordinary PTA 里的单方最短路语义里。

### 3. 定义状态式 optimal-cost 函数 `O`，并追问它是否真能代表 run-based 最优值

论文里最核心的理论动作，是引入一个 state-based optimal-cost function `O`。直观上，它试图给每个状态 `q` 直接分配一个“从这里出发，控制方能保证的最小最坏代价”。

如果这个对象成立，事情就会很美：

1. 最优控制不必记历史；
2. symbolic state 仍然足够；
3. 可以继续按状态递推策略。

但作者没有直接假设它当然存在，而是认真地区分两层：

1. `run-based` 的 optimal cost，本质上定义在策略与 outcome 上；
2. `state-based` 的 `O(q)`，则试图把它压缩回状态函数。

论文的关键工作之一，就是证明在合适条件下，这两种观点是一致的；但在更一般情况下，最优策略可能必须记住累计 cost，而不能只看当前 timed state。

这其实是在给 `UPPAAL` 路线划边界：什么时候还能延续 state-based symbolic game solving，什么时候必须把“已付代价”也一并进状态。

### 4. 用累计代价变量把 `RPTGA` 归约到更标准的混成博弈问题

为了真正做可计算性证明，作者没有直接在原 priced timed game 上硬算，而是引入了一个非常关键的 reduction：给系统增加一个累计代价变量，把 `RPTGA` 的 optimality 问题转成一个带显式 cost variable 的控制问题。

直观上，这一步做了两件事：

1. 让“已经花了多少”成为系统显式状态的一部分；
2. 把原本 awkward 的最优性问题转成更标准的 reachability/control 形式。

也就是说，论文不是试图否认历史代价的重要性，而是把它正面纳入语义对象。这样一来，即便某些场景里最优策略并不纯 state-based，它也仍然有机会在“扩展状态空间”上被计算。

这一步和普通 `UPPAAL` 风格非常一致：当某个性质不能直接在原状态上保持闭合时，就把缺失的信息升格为显式状态成分。

### 5. 在有界、严格非 Zeno 等条件下证明终止与最优策略存在

论文没有给一个“任意 PTGA 都可算”的过度乐观结论，而是仔细说明了可计算性需要哪些假设。最重要的条件包括：

1. 游戏是有界的；
2. 价格积累满足严格非 Zeno 一类条件；
3. 某些 strictness / regularity 假设保证不会在边界处出现病态行为。

这些假设的作用很明确：

1. 防止通过无限多次极短切换把 cost 逼向奇怪极限；
2. 保证 value iteration / recursive optimality 论证能停下来；
3. 让“最优值函数”与“可实现策略”之间有稳定对应。

所以本文的方法不是一个可直接落地的单求解器，而是先给出**何时这件事在理论上可做**的清晰框架。

### 6. 区分“只依赖状态的最优策略”和“依赖累计代价的最优策略”

我认为这篇论文最重要的洞见之一就在这里。许多二手概述会把它说成“priced timed game 最优策略可算”，但原文其实更细：

1. 某些场景下，可以得到 state-based optimal strategy；
2. 另一些场景下，只能得到依赖额外 cost information 的策略。

这意味着论文并不只是给出一个 yes/no 可判定性结果，而是在解释：

1. 为什么 priced information 会改变策略表示方式；
2. 为什么有时必须把“历史已花费”升格为正式状态；
3. 为什么 ordinary timed-game solver 不能无修改地直接拿来做 optimal PTG。

## 解决了什么问题

这篇论文解决的是 priced timed games 长期缺少严谨最优性语义与可计算框架的问题。

第一，它把“能赢”与“最优地赢”明确区分开。以前 timed games 的结果更多是 winning / losing；本文把 optimal cost 作为一等公民引入。

第二，它给出了从 run-based optimality 到 state-based value function 的桥梁，同时也说明了这座桥何时会断。对后续工具路线来说，这一点非常重要，因为它决定 symbolic engine 到底还能保留多少原有结构。

第三，它把 priced timed games 的理论边界画清楚了：不是所有情况下都能无代价地得到纯状态策略，但在有界且满足若干正则条件时，optimal synthesis 是可以系统开展的。

第四，它为后来的 priced scheduling、expected cost、planning 与 strategy optimization 分支提供了非常扎实的理论底座。

## 与 `UPPAAL` 技术线的关系

### 它接在谁之后

它紧接：

1. [behrmann01-cost-optimality-uppaal](../behrmann01-cost-optimality-uppaal/)
   - 打开了 cost-optimal reachability 的单方优化主线。
2. [cassez05-analysis-of-timed-games](../cassez05-analysis-of-timed-games/)
   - 给出了 timed games 的高效求解基础。

本文本质上把这两条线交叉起来：既要 timed game 的对抗结构，又要 priced optimization 的代价目标。

### 它往后影响了谁

它明显影响：

1. [behrmann05-optimal-scheduling-priced-timed-automata](../behrmann05-optimal-scheduling-priced-timed-automata/)
2. [david14-minimal-expected-cost](../david14-minimal-expected-cost/)
3. [david15-uppaal-stratego](../david15-uppaal-stratego/)
4. 更现代的 planning / MCTS / strategy optimization 路线

因为这些方向都需要把“可赢性”进一步推进成“最优性”。

### 它更靠近哪条主线

它最靠近：

1. priced timed games
2. optimal strategy synthesis
3. game-theoretic control with costs

而不是 `DBM` 内核或纯工具架构。

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - 作为 BRICS technical report，它比一般会议短文展开得更充分；定义、策略语义和 reduction 思路都比较清楚，但它仍然更偏可计算性框架，不是直接可复刻的 solver manual。
2. **实现可获取程度**
   - 更适合评为 `🟥 暂未获取实现源码`。
   - 本文是理论主线条目，当前没有找到与文中 optimal PTG 求解直接对应的公开源码仓库；后续只能沿 `UPPAAL-Tiga`、`CORA` 与更晚的 optimization 工具线间接追踪。
3. **材料价值**
   - 它非常适合用来理解 priced strategy synthesis 的语义与边界，不适合直接当作工程实现说明书。

## 对本研究的启发

对当前博士研究，这篇论文有两点尤其重要。

第一，**一旦目标从“满足性质”升级为“最优地满足性质”，状态表示就往往必须显式携带更多历史信息**。这对后续做“最小代价修复”“最小扰动修改”非常有启发。

第二，论文对“state-based enough?” 这件事的谨慎处理很值得借鉴。很多自动化研究容易一上来默认“当前状态足够决定下一步”，而本文恰恰说明：当优化目标改变时，这个假设可能失效。

第三，它为把 verification、control、optimization 三者放进同一个 timed symbolic framework 提供了非常好的思想模板。对于你后续可能做的“验证失败后如何选择更优修复动作”，这种 game + cost 的视角是可以直接迁移的。

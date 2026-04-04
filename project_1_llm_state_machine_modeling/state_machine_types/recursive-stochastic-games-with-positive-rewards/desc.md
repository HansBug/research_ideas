# 带正奖励的递归随机博弈 / Recursive Stochastic Games with Positive Rewards

## 基本信息

- 标题：Recursive Stochastic Games with Positive Rewards
- 中文标题：带正奖励的递归随机博弈
- 作者：Kousha Etessami, Dominik Wojtczak, Mihalis Yannakakis
- 发表：*Automata, Languages and Programming*, `LNCS 5125`, pp. 711-723, 2008
- DOI：`10.1007/978-3-540-70575-8_58`
- 链接：https://homepages.inf.ed.ac.uk/kousha/icalp08_final_proceedings_version.pdf
- 形式主义：`1-exit Recursive Markov Decision Processes / 1-exit Recursive Simple Stochastic Games (1-RMDP / 1-RSSG)` 的 positive-reward 扩展
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：positive-reward 子枝 conference origin
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 positive-reward `1-RMDP / 1-RSSG` tuple、线性 `min/max` 方程、`SM` 策略和 strategy improvement。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是递归随机博弈组件、正奖励边、call cost 与 total expected reward 语义。

## 简报

这篇 `ICALP 2008` 条目把 `1-RMDP / 1-RSSG` 从“只看 termination 概率”的 family，推进到了“看 total expected reward”的新子枝，而且强调奖励必须严格为正。对演化树来说，它最重要的地方不是复杂度数字，而是把 `positive-reward 1-RMDP / 1-RSSG` 稳定成了一个值得单独命名的经典变体。

- 形式主义定位：`RMDP/RSSG` 下 `1-exit` 子类的 reward 扩展，也是 probabilistic recursive branch 中与 termination 口径平行的一条新子枝。
- 构造方式简述：保留 component、box、entry / exit、chance / max / min 的骨架，再给每条转移和每个 call port 赋正奖励。
- 基础设施与场景简述：原文虽讨论算法，但真正对文库有长期价值的是“正奖励”这个模型条件本身，它改变了值域、策略结构和多种 pathological case。

```text
1-RMDP / 1-RSSG -> attach strictly positive rewards -> total expected reward objective -> SM strategies + linear min/max equations
```

## 形式主义定义与核心对象

### 定义对象

原文研究的是 `1-exit` recursive stochastic games with strictly positive rewards。与 2005/2006 年那批 termination 论文相比，它把目标从“终止概率”切换为“总期望奖励”，从而得到一个新的经典子类。

### 核心抽象

按照原文的正奖励版本，组件系统可以保守写成：

$$
A=(A_1,\ldots,A_k)
$$

其中每个组件满足：

$$
A_i=(N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i,\xi_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是节点集合。
2. `B_i` 是 boxes 集合。
3. `Y_i` 指出每个 box 调用的 component。
4. `En_i` 与 `Ex_i` 是 entry / exit 接口。
5. `pl_i` 把顶点分成 chance、max、min。
6. `\delta_i` 是带正奖励的边关系。
7. `\xi_i` 把 call port 映射到正的 call cost。

### 一个最小例子与通俗解释

一个最小例子可以是：

1. 玩家在某个 max 顶点可以选择“立即结束并拿到奖励 `2`”。
2. 也可以选择“递归调用一次子过程，先付出 call reward `1`，回来后再继续”。
3. 只要系统不终止，就会一直累积正奖励。

通俗地说，这个模型像“每走一步都要花钱或拿钱，而且只要永远不结束，总收益就会一直涨”的递归随机状态机。正奖励约束让很多原本棘手的 0-reward 病态现象消失了。

### 运行 / 接受 / 转移语义

原文把 total expected reward 作为目标。若 `u` 是普通顶点，`v` 是后继，`c_{u,v}` 是边奖励，`c_u` 是 call reward，则可保守整理成如下线性 `min/max` 语义：

$$
x_u =
\begin{cases}
\sum_v p_{u,v}(c_{u,v}+x_v), & u \text{ is chance}\\
\max_v (c_{u,v}+x_v), & u \text{ is max}\\
\min_v (c_{u,v}+x_v), & u \text{ is min}
\end{cases}
$$

对 call port，则额外包含“进入子过程 + 返回后继续”的分解：

$$
x_{(b,en)} = c_u + x_{en} + x_{(b,ex)}
$$

这里的式子是对原文 reward 语义的保守整理，用来表达“奖励在调用前后分段累积”的核心结构。

### 语义边界

这个 family 的边界很明确：

1. 仍然只处理 `1-exit` 子类。
2. 关键新增不是玩家类型，而是 strictly positive rewards。
3. 模型仍是 turn-based，不是 simultaneous concurrent game。
4. 一旦转向 multi-exit，很多基本问题会变得不可判定。

### 关键性质与判定边界

原文最重要的家族级结论是：

$$
\text{exact value for maximizing / minimizing 1-RMDP with positive rewards} \in P
$$

并且：

$$
\text{quantitative decision for positive-reward 1-RSSG} \in NP \cap coNP
$$

策略方面，原文给出强 determinacy 结果：

$$
\text{both players have optimal stackless and memoryless strategies}
$$

这说明 positive-reward 不是单纯“换个目标函数”，而是足以把 `1-RMDP / 1-RSSG` 切成一个独立 family 变体。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍是递归 components + boxes + entry / exit。 |
| 事件 / 触发 | 强支持 | 概率 / 玩家选择与奖励边共同驱动演化。 |
| 守卫 / 数据 | 不支持 | 原文核心不在变量。 |
| 层次 | 强支持 | call / return 递归骨架完整保留。 |
| 并发 / 同步 | 不支持 | 这里仍是 turn-based。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率、博弈与奖励并存。 |
| 可执行 / 可验证性 | 强理论支持 | exact reward、`SM` 策略、strategy improvement。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| reward family tuple | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i,\xi_i)$` | positive-reward 版 recursive game component。 |
| call-return reward | `$x_{(b,en)}=c_u+x_{en}+x_{(b,ex)}$` | 递归调用的奖励分解。 |
| exact `1-RMDP` value | `P-time` | 单玩家 reward 子类可精确求值。 |
| positive-reward `1-RSSG` decision | `NP \cap coNP` | 双玩家版本的定量决策边界。 |

## 构造方式与承载格式

### 建模入口

1. 先构造 `1-exit` recursive stochastic game。
2. 给每条边赋严格正的 transition reward。
3. 给每个 call port 赋 call cost。
4. 把目标定义成 total expected reward，而不是 termination probability。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. positive-reward recursive game tuple；
2. linear `min/max` equation system；
3. `SM` strategy semantics；
4. simultaneous strategy improvement。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [efficient-qualitative-analysis-of-classes-of-recursive-markov-decision-processes-and-simple-stochastic-games/desc.md](../efficient-qualitative-analysis-of-classes-of-recursive-markov-decision-processes-and-simple-stochastic-games/desc.md) 的 `1-exit / linearly-recursive` termination family。
2. 向后由 [recursive-stochastic-games-with-positive-rewards-tcs/desc.md](../recursive-stochastic-games-with-positive-rewards-tcs/desc.md) 提供 journal full version。
3. 与 [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md) 平行，前者引入 reward，后者引入 simultaneous moves。

## 配套基础设施

- 建模/编辑工具：原文未提供公开工具。
- 解析/交换/元模型支持：核心是 positive-reward tuple 与线性 `min/max` 方程。
- 仿真/执行支持：可按递归随机博弈加 reward 语义直接执行。
- 验证/分析支持：exact reward computation、strategy improvement、定量决策。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，但与 `SCFG / branching process / probabilistic procedural program` 对应非常稳固。

## 适用场景与需求前提

### 适用场景

适合：

1. 要分析递归概率程序的 expected running time / expected accumulated reward。
2. 需要 system-environment 对抗，但又是 turn-based。
3. 想把 termination family 继续扩成 reward family。

### 需求前提

1. 每个组件只有一个 exit。
2. 奖励必须严格为正。
3. 系统复杂度主要来自递归与概率 / 对抗，而不是时间或数据。

### 不适用或高成本场景

如果奖励允许为 `0`，或者需要 simultaneous moves / multi-exit / dense time，这篇条目的 family 就不再足够。

## 与相邻形式主义的关系

相对 2005/2006 的 `RMDP/RSSG` termination family，它引入了 positive rewards；相对 `RCSG`，它没有并发 simultaneous moves；相对 2019 `TCS` full version，它是 conference origin，不够系统但足以稳定 positive-reward 分支名义。

## 与本研究的关系

### 对 Project 1 的价值

它直接把 `RMDP/RSSG` 再切出一条可挂树的新子枝：`positive-reward 1-RMDP / 1-RSSG`。这对于完善层次状态机理论树的随机递归一支很有用。

### 作为目标形式主义还是中间表示

更适合作为高表达力理论中间表示与 family 分支，而不是工程交付语言。

### 对需求到模型生成的启发

如果需求文本显式包含“递归子过程 + 概率分支 + 总成本 / 总收益 / 期望运行时间”，那目标 family 不应只停在 termination-oriented `RMDP`，而应直接考虑 positive-reward 变体。

## 重要的相关工作

1. [recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md)
2. [efficient-qualitative-analysis-of-classes-of-recursive-markov-decision-processes-and-simple-stochastic-games/desc.md](../efficient-qualitative-analysis-of-classes-of-recursive-markov-decision-processes-and-simple-stochastic-games/desc.md)
3. [recursive-stochastic-games-with-positive-rewards-tcs/desc.md](../recursive-stochastic-games-with-positive-rewards-tcs/desc.md)

## 文献分类总结

- 这篇论文属于 `🌊 混成 / 随机扩展`。
- 这篇论文的对象类型是 `🧱 模型本体`。
- 这篇论文描述的客体是 `🤝 接口 / 交互契约`。
- 这篇论文所属领域是 `🧮 形式语言与自动机理论`。

它应挂到当前演化树的 `RMDP/RSSG` 之下，作为 `positive-reward 1-RMDP / 1-RSSG` 子枝的 conference origin；在树上最合适的写法是把该子枝标成 `2008 / 2019`，同时用本条目承担 conference 起点。

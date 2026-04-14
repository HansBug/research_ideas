# 递归马尔可夫决策过程与递归随机博弈 / Recursive Markov Decision Processes and Recursive Stochastic Games

## 基本信息

- 标题：Recursive Markov Decision Processes and Recursive Stochastic Games
- 中文标题：递归马尔可夫决策过程与递归随机博弈
- 作者：Kousha Etessami, Mihalis Yannakakis
- 发表：*Automata, Languages and Programming*, `LNCS 3580`, pp. 891-903, 2005
- DOI：`10.1007/11523468_72`
- 链接：https://www.pure.ed.ac.uk/ws/files/14029819/final_icalp05.pdf
- 形式主义：`Recursive Markov Decision Processes (RMDP)` 与 `Recursive Simple Stochastic Games (RSSG)`
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / `RMC` 上的 controlled-game conference origin
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 `RMDP/RSSG` tuple、全局递归随机博弈语义以及 `1-exit` 情况下的非线性 min/max 方程组。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 component、box、entry/exit、player partition 与概率/控制转移。

## 简报

这篇 `ICALP 2005` 论文把 `RMC` 从“只有随机性”的 closed model，继续推进到“控制器 / 对手可参与决策”的 open recursive model。它的重要性不在于某个算法技巧，而在于首次把 `RSM` 概率支线补成 `RMC -> RMDP/RSSG`：前者是单控制器递归 `MDP`，后者是 turn-based 递归随机博弈，并且 `1-exit` 子类又恰好对应 branching processes 与 `SCFG` 的 controlled / game 版本。

- 形式主义定位：`RMC` 的控制与博弈扩展，也是递归状态机支线进入 probabilistic game / environment interaction 的第一层。
- 构造方式简述：模型仍由 components、boxes 和 call-return 语义组成，但顶点再按 `chance / max / min` 三类划分。
- 基础设施与场景简述：纯理论条目，但已经给出 `1-exit` 情况的单调 nonlinear min/max equations，并系统区分 `1-exit` 可判定与 multi-exit 不可判定边界。

```text
RMC -> player partition on recursive components -> max/min/chance recursive game -> nonlinear min/max equations -> controlled / adversarial termination analysis
```

## 形式主义定义与核心对象

### 定义对象

原文把 `RSSG` 定义成 turn-based 递归随机博弈，并把 `RMDP` 当作其单控制器特例。相对于 `RMC`，新增点不是新的栈语义，而是“谁来选下一步”。

### 核心抽象

原文把一个 `RSSG` 写成：

$$
A=(A_1,\ldots,A_k)
$$

其中每个 component 为：

$$
A_i=(N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是节点集合。
2. `B_i` 是 boxes 集合。
3. `Y_i` 指出 box 调用的 component。
4. `En_i` 与 `Ex_i` 是 entry / exit 接口。
5. `pl_i:Q_i\to\{0,1,2\}` 把顶点划分为 chance、max、min 三类。
6. `\delta_i` 是转移关系；chance 顶点用概率边，玩家顶点用控制边。

### 一个最小例子与通俗解释

一个最小例子可以是“递归任务处理中的系统-环境博弈”：

1. 系统处在 component `A_1` 的某个 max 顶点，可选择“继续处理”或“调用子过程”。
2. 环境在某个 min 顶点可选择“制造失败分支”或“允许返回”。
3. 某些中间顶点则仍是概率顶点，表示随机结果。

通俗地说，`RMDP/RSSG` 是“会压栈递归的随机决策状态机 / 随机博弈状态机”。它比 `RMC` 多了显式交互方，因此更适合表示 system-environment 或 controller-adversary 场景。

### 运行 / 接受 / 转移语义

全局状态仍然是递归上下文上的顶点：

$$
\langle \beta,u\rangle \in B^*\times Q
$$

上式中的符号逐项解释如下：

1. `\beta` 是当前调用栈。
2. `u` 是当前活动顶点。
3. `Q` 是所有 component 顶点、调用端口和返回端口的并集。

在 `1-exit` 情形下，termination value 满足单调 min/max 方程。若 `u` 是 chance、call、max、min 顶点，则分别有：

$$
x_u=\sum_{(u,p_{u,v},v)\in\delta} p_{u,v}x_v,\quad
x_{(b,en)}=x_{en}\cdot x_{(b,ex)},\quad
x_u=\max_v x_v,\quad
x_u=\min_v x_v
$$

上式中的符号逐项解释如下：

1. 第一式对应概率转移。
2. 第二式对应调用后再返回的乘法结构。
3. 第三式对应最大化玩家的选择。
4. 第四式对应最小化玩家的选择。

### 语义边界

这个 family 的边界如下：

1. 它是 turn-based recursive stochastic game，不是 simultaneous-move game。
2. 它保留递归与概率，但不引入时间或连续变量。
3. `RMDP` 是 `RSSG` 的单控制器特例。
4. 论文明确表明 multi-exit 情形会比 `1-exit` 难得多。

### 关键性质与判定边界

论文最关键的 family 结论是：`1-exit` 情形仍可收束到最小不动点系统，因此定量 termination 可判定，而 multi-exit 情形则迅速走向不可判定。可压成：

$$
\text{quantitative termination for 1-RMDPs / 1-RSSGs} \in \mathrm{PSPACE}
$$

同时，论文还指出：

$$
\text{multi-exit RMDPs} \Rightarrow \text{qualitative termination undecidable}
$$

这意味着 `RMDP/RSSG` 不是把 `RMC` 简单加个玩家标签，而是真正形成了新的递归随机博弈 family 边界。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | components、boxes、entry/exit、player partition。 |
| 事件 / 触发 | 强支持 | 概率边与玩家控制边共同决定演化。 |
| 守卫 / 数据 | 不支持 | 原文核心不在变量。 |
| 层次 | 强支持 | recursive components + call/return。 |
| 并发 / 同步 | 不支持 | 这里仍是 turn-based，不是并发 simultaneous moves。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率和玩家选择并存。 |
| 可执行 / 可验证性 | 强理论支持 | `1-exit` LFP、质性/定量 termination、multi-exit boundary。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 家族总元组 | `$A=(A_1,\ldots,A_k)$` | 递归随机决策 / 博弈总骨架。 |
| component 元组 | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i)$` | 单个递归随机博弈组件。 |
| 顶点玩家划分 | `$pl_i:Q_i\to\{0,1,2\}$` | chance / max / min 三类顶点。 |
| 全局状态 | `$\langle \beta,u\rangle \in B^*\times Q$` | 调用栈 + 当前顶点。 |
| `1-exit` 方程 | `sum / product / max / min` | termination value 的递归定义。 |

## 构造方式与承载格式

### 建模入口

1. 先定义递归 components 与 entry / exit。
2. 用 boxes 表达过程调用。
3. 把顶点划分为 chance、max、min。
4. 在 chance 顶点上放概率边，在玩家顶点上放可选边。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `RSSG/RMDP` tuple；
2. 全局递归随机博弈语义；
3. `1-exit` 情况下的 nonlinear min/max equations；
4. 质性 / 定量 termination 判定问题。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations/desc.md) 的 `RMC`。
2. 向下为 [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md) 的 simultaneous-move `RCSG` 提供 turn-based 母线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 recursive game tuple 与 `1-exit` 方程系统。
- 仿真/执行支持：可按全局递归随机博弈语义执行。
- 验证/分析支持：定量 / 质性 termination、`PSPACE` 判定、`1-exit` 与 multi-exit 边界。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，同时连接 branching process、`SCFG` 与 stochastic-game 社区。

## 适用场景与需求前提

### 适用场景

适合：

1. 概率递归系统里的 controller choice。
2. 递归 system-environment 对抗或最优控制。
3. 想把 branching process / `SCFG` 的 controlled / game 扩展拉回状态机谱系。

### 需求前提

1. 系统核心是递归调用。
2. 决策者是 turn-based，而不是并发 simultaneous move。
3. 接口可抽成有限 entry / exit。

### 不适用或高成本场景

如果双方需要同时独立出手，应转向 `RCSG`；如果没有决策者，只需 `RMC`；如果系统要求 dense time 或数据变量，则这篇条目本身不够。

## 与相邻形式主义的关系

相对 `RMC`，它加入了 max / min 玩家；相对 `RGG`，它这里的重点是概率 termination value 而不是 `omega`-regular modular strategy；相对 `RCSG`，这里仍是 turn-based 而非并发 simultaneous moves。

## 与本研究的关系

### 对 Project 1 的价值

它把 `RSM` 之后的 probabilistic recursive branch 从“随机过程”进一步推进到“带控制与环境交互的递归状态机”，使演化树不只停在 `RMC`。

### 对状态机自动建模的启发

如果需求文本里同时出现“递归子过程 + 随机结果 + 控制器或环境决策”，把它压回 plain `RMC` 会损失交互结构；`RMDP/RSSG` 更合适。

### 现实限制

它没有工业标准或 DSL，主要承担理论谱系和 formal intermediate representation 角色。

## 重要的相关工作

1. [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md)：`RMDP/RSSG` 的随机递归母线 `RMC`。
2. [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md)：本条目的 journal full version。
3. [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md)：把 turn-based 支线继续推进到并发 simultaneous-move。

## 文献分类总结

- 这篇文献在 `state_machine_types` 中属于：`🌊 混成 / 随机扩展`
- 这篇文献在 `state_machine_types` 中的对象类型是：`🧱 模型本体`
- 这篇文献在 `state_machine_types` 中描述的客体是：`🤝 接口 / 交互契约`
- 这篇文献在 `state_machine_types` 中所属的领域是：`🧮 形式语言与自动机理论`

它应挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> Probabilistic Recursive State-Machine 支线 -> RMC/HMC -> RMDP/RSSG` 位置，并作为这条 controlled / game recursive stochastic branch 的 conference 起点。

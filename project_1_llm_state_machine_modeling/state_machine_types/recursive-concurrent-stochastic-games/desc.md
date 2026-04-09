# 递归并发随机博弈 / Recursive Concurrent Stochastic Games

## 基本信息

- 标题：Recursive Concurrent Stochastic Games
- 中文标题：递归并发随机博弈
- 作者：Kousha Etessami, Mihalis Yannakakis
- 发表：*Automata, Languages and Programming*, `LNCS 4052`, pp. 324-335, 2006
- DOI：`10.1007/11787006_28`
- 链接：https://homepages.inf.ed.ac.uk/kousha/final_icalp06.pdf
- 形式主义：`Recursive Concurrent Stochastic Games (RCSG)`，重点讨论 `1-RCSG`
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / concurrent recursive stochastic-game extension
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 `RCSG` tuple、`1-RCSG` 的 nonlinear minimax system 与 randomized stackless-memoryless strategy 语义。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 recursive components、joint-action labeled transitions 与零和矩阵博弈值算子 `\mathrm{Val}`。

## 简报

这篇 `ICALP 2006` 论文把 `RMDP/RSSG` 再往前推了一步：不再是 turn-based 轮流出手，而是两个玩家在递归组件里同时、独立地出手，得到真正的 concurrent recursive stochastic game。对当前状态机族演化树来说，这意味着 `RSM` 的概率递归支线已经不是“随机过程”或“轮流博弈”就结束，而是可以稳定长到 `RMC/HMC -> RMDP/RSSG -> RCSG`。

- 形式主义定位：`RMDP/RSSG` 的 concurrent 扩展，也是 recursive stochastic-game 支线接入 simultaneous-move semantics 的首个稳定节点。
- 构造方式简述：component、box、entry / exit 与调用栈骨架仍保留，但 player vertex 不再直接指向某个后继，而是由双方动作对 `(γ_1,γ_2)` 共同决定。
- 基础设施与场景简述：纯理论条目，但已经给出 `1-RCSG` termination value 的 nonlinear minimax equations、`r-SM` 策略改进以及 `SQRT-SUM` 级困难性。

```text
RMDP/RSSG -> simultaneous independent moves on recursive components -> local matrix games -> nonlinear minimax equations -> randomized recursive game values
```

## 形式主义定义与核心对象

### 定义对象

原文把 `RCSG` 定义成递归 concurrent stochastic game。它的关键变化在于：在某些顶点上，双方不是轮流选边，而是同时独立选择动作，再由动作对决定后继。

### 核心抽象

给定玩家动作字母表 `\Gamma_1,\Gamma_2`，原文把一个 `RCSG` 写成：

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
3. `Y_i` 把 box 映射到被调 component。
4. `En_i` 与 `Ex_i` 是 entry / exit 接口。
5. `pl_i:Q_i\to\{0,\mathrm{play}\}` 区分概率顶点和并发博弈顶点。
6. `\delta_i` 在 `play` 顶点上用动作对 `(γ_1,γ_2)` 标注转移。

### 一个最小例子与通俗解释

一个最小例子可以是“递归服务中的系统-环境并发出招”：

1. 当前处于某个 `play` 顶点。
2. 系统同时选择动作 `γ_1`，环境同时选择动作 `γ_2`。
3. 这对动作联合决定是留在本 component、递归调用子 component，还是走向失败分支。

通俗地说，`RCSG` 就是“会压栈调用、而且双方同步出招的递归随机博弈状态机”。它比 `RSSG` 多的是 simultaneous concurrency，不是新的递归骨架。

### 运行 / 接受 / 转移语义

全局状态仍是：

$$
\langle \beta,u\rangle \in B^*\times Q
$$

上式中的符号逐项解释如下：

1. `\beta` 是调用栈。
2. `u` 是当前活动顶点。
3. `Q` 是顶点与端口的并集。

在 `1-RCSG` termination game 中，最关键的方程系统写成：

$$
x=P(x)
$$

其中若 `u` 是四类顶点之一，则：

$$
x_u=1,\ x_u=\sum_{(u,p_{u,v},v)\in\delta} p_{u,v}x_v,\ x_{(b,en)}=x_{en}\cdot x_{(b,ex')},\ x_u=\mathrm{Val}(A_u(x))
$$

这里 `A_u(x)` 是局部零和矩阵博弈，其矩阵元满足：

$$
(A_u(x))_{\gamma_1,\gamma_2}=x_v\quad \text{if }(u,(\gamma_1,\gamma_2),v)\in\delta
$$

上式中的符号逐项解释如下：

1. `\gamma_1,\gamma_2` 分别是玩家 1 和玩家 2 的动作。
2. `v` 是动作对触发的后继顶点。
3. `\mathrm{Val}(A_u(x))` 是该零和矩阵博弈的值。
4. 因此 `RCSG` 的核心算子不再是 `max/min`，而是 `minimax`。

### 语义边界

这个 family 的边界如下：

1. 它是 concurrent、simultaneous、零和随机博弈。
2. 它仍是递归顺序组件骨架，不含时间或连续变量。
3. 论文重点放在 `1-RCSG`，因为 multi-exit 情形此前已知会失控。
4. 玩家通常需要 randomized memoryless，而不是确定性策略。

### 关键性质与判定边界

原文的核心结果是：

$$
q^*=\mathrm{LFP}(P)
$$

同时：

$$
\text{quantitative termination for 1-RCSGs} \in \mathrm{PSPACE}
$$

策略层面，论文证明：

$$
\text{player 2 has optimal r-SM strategies,\quad player 1 has }\epsilon\text{-optimal r-SM strategies}
$$

这里 `r-SM` 指 randomized stackless-memoryless。也就是说，`RCSG` 与 `RSSG` 的关键差别之一正是：并发 simultaneous moves 迫使随机化进入最优策略定义。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 递归 components、boxes、entry/exit、joint-action vertices。 |
| 事件 / 触发 | 强支持 | 动作对 `(γ_1,γ_2)` 共同决定后继。 |
| 守卫 / 数据 | 不支持 | 原文核心不在变量。 |
| 层次 | 强支持 | 递归调用骨架完整保留。 |
| 并发 / 同步 | 强支持 | simultaneous independent moves 是核心新增点。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率与 concurrent game 并存。 |
| 可执行 / 可验证性 | 强理论支持 | nonlinear minimax system、`r-SM` determinacy、`PSPACE` quantitative termination。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 家族总元组 | `$A=(A_1,\ldots,A_k)$` | 递归并发随机博弈总骨架。 |
| component 元组 | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i)$` | 单个 concurrent recursive component。 |
| 顶点类型 | `$pl_i:Q_i\to\{0,\mathrm{play}\}$` | 概率顶点与并发博弈顶点。 |
| 局部矩阵值 | `$x_u=\mathrm{Val}(A_u(x))$` | simultaneous moves 的核心语义。 |
| 策略口径 | `r-SM`, `\epsilon`-optimal | `RCSG` 与 turn-based `RSSG` 的关键差异。 |

## 构造方式与承载格式

### 建模入口

1. 先定义递归 components、entry / exit 与 boxes。
2. 在 `play` 顶点上列出双方动作集合。
3. 用动作对 `(γ_1,γ_2)` 标注联合转移。
4. 在 `1-exit` 情形下构造对应 minimax 方程系统。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `RCSG` tuple；
2. joint-action labeled transitions；
3. `1-RCSG` nonlinear minimax equations；
4. randomized stackless-memoryless strategy semantics。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md) 的 turn-based `RMDP/RSSG`。
2. 向更早的母线承接 [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md) 的 `RMC`。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 recursive concurrent-game tuple 与 `\mathrm{Val}` 算子。
- 仿真/执行支持：可按全局 concurrent stochastic game 语义执行。
- 验证/分析支持：`1-RCSG` termination value、`PSPACE` 定量判定、strategy improvement。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，连接 finite concurrent stochastic games、recursive games 与 branching-process game 扩展。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归系统中的 simultaneous system-environment interaction。
2. 需要随机化策略的递归零和博弈。
3. 想把递归状态机支线继续推进到 concurrent stochastic-game 层。

### 需求前提

1. 双方动作是同时且独立选择的。
2. 系统核心复杂度来自递归与并发出招。
3. 接口仍可抽成有限 entry / exit。

### 不适用或高成本场景

如果交互是 turn-based，则 `RMDP/RSSG` 更自然；如果只是 closed stochastic recursion，则 `RMC` 即可；如果需要时间、数据或连续变量，这个条目仍不覆盖。

## 与相邻形式主义的关系

相对 `RMDP/RSSG`，它把 `max/min` 单步选择提升为 simultaneous-move matrix game；相对 finite concurrent stochastic games，它又额外叠加了递归 component / call-return 栈结构；相对 `RGG`，它关注的是概率 termination value 而不是 `omega`-regular modular strategy。

## 与本研究的关系

### 对 Project 1 的价值

它让 `RSM` 的概率递归支线在 `RMC/HMC -> RMDP/RSSG` 之后还能继续稳定地下长出 concurrent game 分支，直接丰富层次状态机族演化树。

### 对状态机自动建模的启发

如果需求文本中同时出现“递归子过程、随机结果、系统与环境同时决策”，那么 turn-based `RMDP/RSSG` 已不够，需要 `RCSG` 这类 family。

### 现实限制

它纯属理论条目，没有工程语言和工业建模生态，更适合当高表达力 formal node。

## 重要的相关工作

1. [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md)：直接母线。
2. [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md)：更上游的 `RMC` 随机递归骨架。
3. 有限 concurrent stochastic games：本文显式把它们当作 `RCSG` 的无递归特例来比较。

## 文献分类总结

- 这篇文献在 `state_machine_types` 中属于：`🌊 混成 / 随机扩展`
- 这篇文献在 `state_machine_types` 中的对象类型是：`🧱 模型本体`
- 这篇文献在 `state_machine_types` 中描述的客体是：`🤝 接口 / 交互契约`
- 这篇文献在 `state_machine_types` 中所属的领域是：`🧮 形式语言与自动机理论`

它应挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> Probabilistic Recursive State-Machine 支线 -> RMC/HMC -> RMDP/RSSG -> RCSG` 位置，并作为 concurrent recursive stochastic-game 节点的代表条目。

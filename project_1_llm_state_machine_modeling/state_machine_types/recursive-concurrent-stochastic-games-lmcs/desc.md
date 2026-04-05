# 递归并发随机博弈（LMCS 全文版） / Recursive Concurrent Stochastic Games

## 基本信息

- 标题：Recursive Concurrent Stochastic Games
- 中文标题：递归并发随机博弈（LMCS 全文版）
- 作者：Kousha Etessami, Mihalis Yannakakis
- 发表：*Logical Methods in Computer Science*, 4(4:7), 2008
- DOI：`10.2168/LMCS-4(4:7)2008`
- 链接：https://lmcs.episciences.org/1196/pdf
- 形式主义：`Recursive Concurrent Stochastic Games (RCSG)`，重点讨论 `1-RCSG`
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / concurrent recursive stochastic-game family
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 `RCSG` tuple、全局 denumerable stochastic game `M_A`、`1-RCSG` nonlinear minimax equations 与 randomized stackless-memoryless (`r-SM`) strategy semantics。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 recursive components、joint-action labeled transitions、matrix-game value operator `\mathrm{Val}` 与 least fixed-point equations。

## 简报

这篇 `LMCS 2008` 全文版把 `ICALP 2006` 的 `RCSG` 会议条目彻底稳定下来：它不仅保留“simultaneous moves + recursive components”这个模型定义，还系统补全了 `1-RCSG` termination value 的 `LFP` 方程、`PSPACE` quantitative decision、`r-SM` 策略改进与 `SQRT-SUM` 级下界。对当前演化树来说，这使 `RCSG` 不再只是 `RMDP/RSSG` 之后的一个单点 conference 节点，而是有了 journal-level family 锚点。

- 形式主义定位：`RMDP/RSSG` 的 concurrent 扩展，也是 probabilistic recursive branch 接入 simultaneous-move semantics 的 journal full version。
- 构造方式简述：保留 recursive components、boxes、entry / exit 与调用栈骨架，但在 `play` 顶点上由双方动作对 `(γ_1,γ_2)` 共同决定后继。
- 基础设施与场景简述：全文版最重要的新增不是别的应用，而是 `r-SM` determinacy、strategy improvement 和 `1-RCSG` minimax fixed-point 语义被完整收束。

```text
RMDP / RSSG -> simultaneous independent moves in recursive components -> matrix-game value operator -> nonlinear minimax fixed point -> r-SM-determined 1-RCSG
```

## 形式主义定义与核心对象

### 定义对象

`RCSG` 研究的是递归 concurrent stochastic games。它的关键新增点是：在某些顶点上，玩家 1 和玩家 2 不是轮流出手，而是**同时且独立**地选择动作，再由动作对决定后继。

### 核心抽象

原文把一个 `RCSG` 写成：

$$
A = (A_1,\ldots,A_k)
$$

其中每个 component 为：

$$
A_i = (N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是节点集合，`En_i` 与 `Ex_i` 分别是 entry / exit 节点集合。
2. `B_i` 是 boxes 集合，`Y_i` 指定每个 box 调用哪个 component。
3. `Call_b` 与 `Return_b` 分别是某个 box 的 call / return ports。
4. `Q_i = N_i \cup Call_i \cup Return_i` 是 component 的全部 vertices。
5. `pl_i : Q_i \to \{0,\mathrm{play}\}` 指出顶点是概率顶点还是并发博弈顶点。
6. `\delta_i \subseteq Q_i \times ( \mathbb{R} \cup (\Gamma_1 \times \Gamma_2)) \times Q_i` 是转移关系；在 `play` 顶点上，标号是玩家动作对 `(γ_1,γ_2)`。

### 一个最小例子与通俗解释

论文给出的最小例子可以理解成“递归服务里的双方同步出招”：

1. 当前位于某个 `play` 顶点。
2. 系统同时选择 `γ_1`，环境同时选择 `γ_2`。
3. 这对动作共同决定是进入普通后继、调用 box 还是走向失败分支。

通俗地说，`RCSG` 是“会压栈递归、同时又要在每步解一个局部矩阵博弈的状态机 family”。它比 `RSSG` 多的不是 recursion，而是 simultaneous concurrency。

### 运行 / 接受 / 转移语义

`RCSG` 诱导出的全局 denumerable stochastic game 的状态形如：

$$
\langle \beta, u \rangle \in B^* \times Q
$$

上式中的符号逐项解释如下：

1. `\beta` 是调用栈上的 box 串。
2. `u` 是当前活动顶点。
3. `Q` 是所有 component vertices 的并集。

在 `1-RCSG` termination game 中，全文版把值函数系统写成：

$$
x = P(x)
$$

并在 `play` 顶点上满足：

$$
x_u = \mathrm{Val}(A_u(x))
$$

其中局部矩阵博弈的每个元素为：

$$
(A_u(x))_{\gamma_1,\gamma_2} = x_v
$$

若 `(u,(\gamma_1,\gamma_2),v) \in \delta`，则 `v` 是该动作对触发的后继。也就是说，`RCSG` 的核心算子是 `minimax` 值，而不是 `max/min` 或单纯概率求和。

### 语义边界

这个 family 的边界如下：

1. 它是 zero-sum、simultaneous、recursive stochastic game。
2. 它仍是 sequential recursive component skeleton，不含时间与连续变量。
3. multi-exit `RCSG` 的基本问题已知会失控，因此原文重点放在 `1-RCSG`。
4. 玩家策略一般需要 randomized stackless-memoryless，而不是纯确定性记忆无关策略。

### 关键性质与判定边界

全文版最核心的结论包括：

$$
q^* = \mathrm{LFP}(P)
$$

以及：

$$
\text{quantitative termination for 1-RCSGs} \in \mathrm{PSPACE}
$$

策略层面，原文证明：

$$
\text{player 2 has optimal r-SM strategies}
$$

并且：

$$
\text{player 1 has } \epsilon\text{-optimal r-SM strategies for all } \epsilon > 0
$$

于是 `1-RCSG` termination games 满足：

$$
\text{1-RCSGs are r-SM-determined}
$$

这正是 journal full version 比 conference 起点更值得作为长期锚点的地方。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | recursive components、boxes、entry/exit、joint-action vertices。 |
| 事件 / 触发 | 强支持 | 动作对 `(γ_1,γ_2)` 共同决定后继。 |
| 守卫 / 数据 | 不支持 | 原文核心不在变量。 |
| 层次 | 强支持 | recursive component / call-return 骨架完整保留。 |
| 并发 / 同步 | 强支持 | simultaneous independent moves 是核心新增点。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率与并发博弈并存。 |
| 可执行 / 可验证性 | 强理论支持 | `LFP`、`PSPACE` termination、`r-SM` determinacy 与 strategy improvement。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总元组 | `$A = (A_1,\ldots,A_k)$` | recursive concurrent stochastic game 总骨架。 |
| component 元组 | `$A_i = (N_i,B_i,Y_i,En_i,Ex_i,pl_i,\delta_i)$` | 单个 recursive concurrent component。 |
| 全局状态 | `$\langle \beta, u \rangle \in B^* \times Q$` | 调用栈 + 当前顶点。 |
| 局部博弈值 | `$x_u = \mathrm{Val}(A_u(x))$` | simultaneous moves 的核心语义。 |
| 策略口径 | `r-SM`, `\epsilon`-optimal, `r-SM-determined` | journal full version 的关键 family boundary。 |

## 构造方式与承载格式

### 建模入口

1. 先按 `RSM` 一样定义 recursive components、boxes、entry / exit。
2. 在 `play` 顶点上为双方列出合法动作集 `\Gamma_u^1,\Gamma_u^2`。
3. 用动作对 `(γ_1,γ_2)` 标记联合转移。
4. 在 `1-exit` 情形下构造对应 minimax fixed-point system 与策略改进过程。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `RCSG` tuple；
2. global denumerable stochastic game `M_A`；
3. `1-RCSG` nonlinear minimax equations；
4. `r-SM` strategy semantics；
5. strategy-improvement process。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md) 的 `ICALP 2006` conference origin。
2. 直接母线是 [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md) 的 turn-based `RMDP / RSSG`。
3. 更上游承接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 与 [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md)。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 recursive concurrent-game tuple 与 `\mathrm{Val}` operator。
- 仿真/执行支持：可按全局 denumerable stochastic game 语义执行。
- 验证/分析支持：`1-RCSG` termination、`PSPACE` quantitative decision、`r-SM` strategy improvement。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，连接 finite concurrent stochastic games、recursive games 与 probabilistic recursive systems。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归系统中的 simultaneous system-environment interaction。
2. 需要随机化策略的 recursive zero-sum stochastic games。
3. 想把 `RSM` 的 probabilistic branch 继续推进到 concurrent game 设定。

### 需求前提

1. 双方动作必须是同时且独立选择的。
2. 系统复杂度主要来自递归与并发出招。
3. 接口仍可抽成有限 entry / exit。

### 不适用或高成本场景

如果交互是 turn-based，则 `RMDP / RSSG` 更自然；如果只是 closed stochastic recursion，则 `RMC` 即可；如果还要时间或连续变量，这个条目不覆盖。

## 与相邻形式主义的关系

相对 conference 版，这篇全文版把 `RCSG` 的 `r-SM` determinacy 与 strategy-improvement 语义彻底稳定下来；相对 `RMDP / RSSG`，它把单步 `max/min` 选择替换为 simultaneous-move matrix game；相对 finite concurrent stochastic games，它又叠加了 recursive call-return skeleton。

## 与本研究的关系

### 对 Project 1 的价值

它让层次状态机理论线里的 probabilistic recursive branch 在 `RMDP / RSSG` 之后有了一个 journal-level 的 concurrent 节点，从而让 `RSM` 的高表达力尾部分支更完整。

### 作为目标形式主义还是中间表示

更适合作为高表达力 formal node 或验证中间表示，而不是工程前端建模语言。

### 对需求到模型生成的启发

当需求同时包含“递归子过程、随机结果、系统与环境同步出招”时，turn-based `RMDP / RSSG` 已经不够，需要提升到 `RCSG` family。

### 现实限制

它是高度理论化条目，没有工程 DSL 与工业工具生态。

## 重要的相关工作

### 奠基或前身工作

- [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md)
- [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md)

### 同类型或同家族工作

- [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md)
- finite concurrent stochastic games

## 文献分类总结

- 这篇全文版把 `RCSG` 从 2006 conference 节点稳定成了 journal-level family。
- 它严格属于 `🌊 + 🧱 + 🧮` 的模型本体条目，不是 DSL、工具实现或应用案例。
- 在当前演化树里，它最适合挂到 `Statecharts -> HSM -> uHSM -> RSM -> Probabilistic Recursive State-Machine 支线 -> RMC/HMC -> RMDP/RSSG -> RCSG`，并作为该节点的 2008 full-version 锚点。

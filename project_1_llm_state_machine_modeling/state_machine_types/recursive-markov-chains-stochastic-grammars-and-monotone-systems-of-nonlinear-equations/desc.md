# 递归马尔可夫链、随机文法与非线性单调方程组 / Recursive Markov Chains, Stochastic Grammars, and Monotone Systems of Nonlinear Equations

## 基本信息

- 标题：Recursive Markov Chains, Stochastic Grammars, and Monotone Systems of Nonlinear Equations
- 中文标题：递归马尔可夫链、随机文法与非线性单调方程组
- 作者：Kousha Etessami, Mihalis Yannakakis
- 发表：*STACS 2005*, `LNCS 3404`, pp. 340-352, 2005
- DOI：`10.1007/978-3-540-31856-9_28`
- 链接：https://homepages.inf.ed.ac.uk/kousha/stacs05_rmc.pdf
- 形式主义：`Recursive Markov Chains (RMC)`，并在同文定义其无环特例 `Hierarchical Markov Chains (HMC)`
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / `RSM` 的概率化 conference origin
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 `RMC` component tuple、全局 Markov chain `M_A` 语义以及单调多项式方程组 `$x=P(x)$`。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 components、boxes、entry/exit、call/return ports 与概率标注边。

## 简报

这篇 `STACS 2005` 论文是当前层次状态机理论树上“递归状态机概率化”支线的真正起点。它不是泛泛讨论概率 pushdown，也不是只谈随机文法算法，而是明确把 `RSM` 概率化成 `RMC`，并顺手把 `HMC`、`1-exit RMC` 与 `SCFG/MT-BP` 的关系一起固定下来，因此可以直接挂到 `Statecharts -> HSM -> uHSM -> RSM` 之后。

- 形式主义定位：`RSM` 的概率版本，也是递归状态机支线向 `SCFG`、branching process 与 probabilistic pushdown 过渡的核心桥。
- 构造方式简述：系统由若干有限状态 component Markov chains 组成，component 内既有普通节点，也有调用其他 component 的 boxes。
- 基础设施与场景简述：纯理论模型，但已经给出 termination / reachability 概率对应的最小不动点方程组，以及 `1-exit`、`HMC`、bounded 等子类的复杂度边界。

```text
recursive state machine -> probability-labeled components -> call/return stack semantics -> monotone polynomial equations -> termination / reachability analysis
```

## 形式主义定义与核心对象

### 定义对象

原文把 `RMC` 定义为“允许递归调用的有限状态马尔可夫链集合”。和普通有限 `MC` 相比，新增的不是一般数据或时间，而是 `RSM` 风格的 box 调用结构，再加上概率边。

### 核心抽象

原文把一个 `RMC` 写成：

$$
A=(A_1,\ldots,A_k)
$$

其中每个 component graph 为：

$$
A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是普通节点集合。
2. `B_i` 是 boxes 集合。
3. `Y_i:B_i\to\{1,\ldots,k\}` 指定 box 调用哪个 component。
4. `En_i` 与 `Ex_i` 分别是 entry / exit 节点集合。
5. `\delta_i` 是带概率的局部转移关系。

对每个 box `b`，原文还定义：

$$
\mathrm{Call}_b=\{(b,en)\mid en\in En_{Y(b)}\},\quad \mathrm{Return}_b=\{(b,ex)\mid ex\in Ex_{Y(b)}\}
$$

上式中的符号逐项解释如下：

1. `\mathrm{Call}_b` 是调用端口集合。
2. `\mathrm{Return}_b` 是返回端口集合。
3. `Y(b)` 指向被调 component。
4. 每个调用端口和返回端口都与被调 component 的 entry / exit 一一对应。

### 一个最小例子与通俗解释

一个最小例子可以是“带随机递归重试的过程控制”：

1. component `A_1` 的节点 `u` 以概率 `1/2` 直接走向成功 exit。
2. 以概率 `1/2` 经 box `b` 调用另一个 component `A_2`。
3. `A_2` 完成后，通过 `Return_b` 回到 `A_1` 继续。

通俗地说，`RMC` 就是“会递归调用、而且每一步还带概率的状态机”。它比 `RSM` 多的是随机性，比普通 `MC` 多的是可压栈的调用上下文。

### 运行 / 接受 / 转移语义

原文把 `RMC` 展开成一个全局可数马尔可夫链 `M_A=(V,\Delta)`，其全局状态写成：

$$
\langle \beta,u\rangle \in B^*\times Q
$$

上式中的符号逐项解释如下：

1. `\beta` 是由 boxes 组成的调用栈。
2. `u` 是当前活动顶点。
3. `B^*` 表示任意长度 box 序列。
4. `Q` 是所有普通节点、调用端口和返回端口的并集。

终止概率由同一 component 内的顶点-出口对来描述：

$$
q^*_{(u,ex)}=\Pr[\langle \epsilon,u\rangle \leadsto \langle \epsilon,ex\rangle]
$$

上式中的符号逐项解释如下：

1. `u` 与 `ex` 位于同一 component。
2. `\epsilon` 是空调用上下文。
3. `\leadsto` 表示最终达到目标终止状态。
4. `q^*_{(u,ex)}` 是我们真正要计算的 termination / reachability 概率。

论文进一步把这些概率收束成单调多项式系统：

$$
x=P(x)
$$

并指出其最小不动点给出所求概率。

### 语义边界

这个 family 的边界非常明确：

1. 它是递归顺序模型，不含并发。
2. 它是概率模型，不含对手或控制器动作。
3. 它没有显式变量、时钟或连续动态。
4. 若调用图无环，则退化到 `HMC`。

### 关键性质与判定边界

论文给出的关键结构结论是：

$$
q^*=\mathrm{LFP}(P)
$$

也就是说 termination / reachability 概率是单调多项式系统的最小不动点。对一般 `RMC`，定量判定可放在：

$$
\mathrm{PSPACE}
$$

而 `1-exit RMC` 与 `SCFG/MT\text{-}BP` 精确对应，`HMC` 则是调用图无环的有限层次子类。论文还明确说明这些概率即使在 `SCFG` 情形下也可能是无理数，因此不能把它当作普通线性方程组来解。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | components、nodes、boxes、call/return ports。 |
| 事件 / 触发 | 中等支持 | 通过概率标注边驱动。 |
| 守卫 / 数据 | 不支持 | 原文不引入变量或守卫。 |
| 层次 | 强支持 | component + box 形成层次调用结构。 |
| 并发 / 同步 | 不支持 | 纯顺序递归。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率边是模型核心。 |
| 可执行 / 可验证性 | 强理论支持 | termination / reachability 概率、`SCFG` 对应、LFP 语义。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 家族总元组 | `$A=(A_1,\ldots,A_k)$` | 整体递归概率状态机。 |
| component 元组 | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)$` | 单个 component 的结构骨架。 |
| 全局状态 | `$\langle \beta,u\rangle \in B^*\times Q$` | 调用栈 + 当前顶点。 |
| 调用端口 | `$\mathrm{Call}_b,\mathrm{Return}_b$` | box 的 entry / exit 接口。 |
| 概率方程 | `$x=P(x)$` | termination / reachability 的 LFP 描述。 |

## 构造方式与承载格式

### 建模入口

1. 先按递归过程边界切出 components。
2. 给每个 component 标出 entry / exit。
3. 用 boxes 表达递归或过程调用。
4. 最后在局部边上附概率。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `RMC` tuple；
2. `Call/Return` 端口；
3. 全局 Markov chain `M_A`；
4. termination 概率方程组 `$x=P(x)$`。

### 交换与互操作

它和当前文库中的关系很直接：

1. 向上承接 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 与 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM`。
2. 向下引出 `1-exit RMC <-> SCFG/MT-BP` 以及后续 `RMDP/RSSG/RCSG` 支线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 component / box / port / probability tuple。
- 仿真/执行支持：可直接展开为全局可数马尔可夫链执行。
- 验证/分析支持：termination / reachability、LFP 方程系统、`PSPACE` 定量判定。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，和 `SCFG`、branching process、probabilistic pushdown 社区交叉明显。

## 适用场景与需求前提

### 适用场景

适合：

1. 概率化递归过程控制流。
2. 想把层次状态机理论线延伸到 stochastic recursion。
3. 需要把 `SCFG/MT-BP` 重新表述为状态机 family。

### 需求前提

1. 系统核心是递归调用而不是并发。
2. 概率分支是模型本体的一部分，而不是后验统计附注。
3. 过程接口可抽成有限 entry / exit。

### 不适用或高成本场景

如果系统还需要显式控制器 / 对手决策，应转向 `RMDP/RSSG`；如果需要并发随机博弈，应转向 `RCSG`；如果根本没有递归，只需 ordinary `MC` 或 `HMC` 即可。

## 与相邻形式主义的关系

相对 `RSM`，`RMC` 的新增点是概率边；相对 `SCFG/MT-BP`，它保留了更直观的 component / box / call-return 状态机骨架；相对后续 `RMDP/RSSG`，它还没有把控制器或对手放入模型。

## 与本研究的关系

### 对 Project 1 的价值

它直接证明 `Statecharts -> HSM -> uHSM -> RSM` 这条线并不会止于非概率递归，而是自然长出一个稳定的 probabilistic recursive branch。

### 对状态机自动建模的启发

如果需求文本里已经出现“递归子过程 + 概率转移 / 随机调用结果”，那目标 family 不应继续停在 `RSM`，而应考虑 `RMC`。

### 现实限制

它没有工业建模标准，也不直接给工程工具，更多适合作为理论谱系节点与中间表示。

## 重要的相关工作

1. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：`RMC` 的非概率蓝本 `RSM`。
2. [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md)：本条目的 journal full version。
3. [recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md)：在 `RMC` 上继续加入控制器和对手。

## 文献分类总结

- 这篇文献在 `state_machine_types` 中属于：`🌊 混成 / 随机扩展`
- 这篇文献在 `state_machine_types` 中的对象类型是：`🧱 模型本体`
- 这篇文献在 `state_machine_types` 中描述的客体是：`🎛️ 控制 / 反应式逻辑`
- 这篇文献在 `state_machine_types` 中所属的领域是：`🧮 形式语言与自动机理论`

它应挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> Probabilistic Recursive State-Machine 支线 -> RMC/HMC` 位置，并作为这条随机递归状态机支线的 conference 起点。

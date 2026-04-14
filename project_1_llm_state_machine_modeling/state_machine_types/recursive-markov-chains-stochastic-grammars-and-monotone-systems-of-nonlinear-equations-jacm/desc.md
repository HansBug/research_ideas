# 递归马尔可夫链、随机文法与非线性单调方程组 / Recursive Markov Chains, Stochastic Grammars, and Monotone Systems of Nonlinear Equations

## 基本信息

- 标题：Recursive Markov Chains, Stochastic Grammars, and Monotone Systems of Nonlinear Equations
- 中文标题：递归马尔可夫链、随机文法与非线性单调方程组
- 作者：Kousha Etessami, Mihalis Yannakakis
- 发表：*Journal of the ACM*, 56(1):1-66, 2009
- DOI：`10.1145/1462153.1462154`
- 链接：https://homepages.inf.ed.ac.uk/kousha/final_rmc_jacm_version.pdf
- 形式主义：`Recursive Markov Chains (RMC)`，并系统整理 `HMC`、`1-exit`、linear、bounded 等关键子类
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / 随机递归状态机 family 整理
- 工具/实现获取方式：原文没有附带公共实现；机器可处理入口是 `RMC` tuple、termination 方程系统 `$x=P(x)$` 以及分解式 Newton 迭代。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 components、boxes、entry/exit、call/return 接口与多项式不动点语义。

## 简报

这篇 `JACM` 版本不是简单重印 `STACS 2005`。它把 `RMC` 从“概率化的 `RSM` 想法”进一步稳定成完整 family：一方面把 `HMC`、`1-exit RMC`、linear、bounded 等子类系统列清；另一方面把 termination / reachability 概率统一到最小不动点和分解式 Newton 方法上。因此如果说 conference 版负责开枝，这篇 full version 负责把整条 `RSM -> RMC/HMC` 概率支线固定成可长期引用的母节点。

- 形式主义定位：`RSM` 的概率化 journal 级整理条目，也是 `RMC/HMC` 支线当前最稳的 family 边界说明。
- 构造方式简述：`RMC` 仍由 components、boxes、entries、exits 和概率边构成，但该版本额外把 `HMC`、`1-exit`、linear、bounded 的内部结构与判定性差异明确写全。
- 基础设施与场景简述：纯理论条目，但已给出 `LFP(P)`、`Pk(0)` 迭代、分解式多元 Newton 方法，以及与 `SCFG/MT-BP` 的双向线性变换。

```text
RSM-style recursion + probabilities -> RMC/HMC family -> monotone polynomial system -> LFP / Newton approximation -> subclass taxonomy and complexity
```

## 形式主义定义与核心对象

### 定义对象

原文把 `RMC` 定义成“有限表示的可数马尔可夫链”，并强调它既是 probabilistic procedural program 的抽象模型，也是 `SCFG`、multi-type branching process、probabilistic pushdown 之间的统一状态机桥。

### 核心抽象

原文仍将一个 `RMC` 写成：

$$
A=(A_1,\ldots,A_k)
$$

其中每个 component 为：

$$
A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是普通节点集合。
2. `B_i` 是 boxes 集合。
3. `Y_i` 指定每个 box 调用的 component。
4. `En_i` 与 `Ex_i` 分别是 entry / exit 接口。
5. `\delta_i` 是带概率的局部转移关系。

与 conference 版相比，这个版本把几个关键子类直接固定下来：

$$
\mathrm{HMC}\subseteq \mathrm{RMC},\quad \mathrm{1\text{-}exit\ RMC}\subseteq \mathrm{RMC}
$$

上式中的符号逐项解释如下：

1. `HMC` 指调用图无环的层次马尔可夫链。
2. `1-exit RMC` 指每个 component 只有一个 exit。
3. 论文还进一步讨论 `linear RMC` 与 `bounded RMC`。

### 一个最小例子与通俗解释

可以把它想成“带随机调用结果的递归程序框图”：

1. 在 component `A_1` 中，某节点以概率 `p` 进入 box `b` 调用 `A_2`。
2. `A_2` 从 entry 开始运行，最终可能从某个 exit 返回。
3. 返回到 `A_1` 后继续下一步，整个系统的 termination 概率由全局调用栈累积而来。

通俗地说，`RMC` 不是“随机文法的另一种写法”，而是“把概率递归过程直接画成状态机组件图”。`SCFG/MT-BP` 只是它的 `1-exit` 特例投影。

### 运行 / 接受 / 转移语义

原文把全局状态仍定义为：

$$
\langle \beta,u\rangle \in B^*\times Q
$$

上式中的符号逐项解释如下：

1. `\beta` 是待返回的 boxes 序列。
2. `u` 是当前活动顶点。
3. `Q` 是所有 component 顶点、调用端口和返回端口的并集。

termination / reachability 概率统一由单调多项式系统刻画：

$$
x=P(x)
$$

其目标解满足：

$$
q^*=\mathrm{LFP}(P)=\lim_{k\to\infty} P^k(0)
$$

上式中的符号逐项解释如下：

1. `P` 是由 `RMC` 自动构造出的单调多项式映射。
2. `0` 是全零初值。
3. `q^*` 是各 termination / reachability 概率构成的向量。
4. `\mathrm{LFP}` 表示最小不动点。

### 语义边界

这个 family 的边界与 conference 版一致，但 journal 版把子类更清楚地区分为：

1. `HMC`：调用图无环。
2. `1-exit RMC`：与 `SCFG/MT-BP` 精确对应。
3. `linear RMC`：return port 到 call port 不再形成递归反馈。
4. `bounded RMC`：component 数和 entry/exit 宽度受常数限制。

### 关键性质与判定边界

本版本最重要的新增之一是数值方法与子类复杂度整理。核心结论可压成：

$$
q^*=\mathrm{LFP}(P)
$$

以及分解式 Newton 方法对 `q^*` 单调收敛。复杂度上：

$$
\text{general RMC quantitative problems} \in \mathrm{PSPACE}
$$

同时：

$$
\text{qualitative termination for 1-exit RMCs} \in \mathrm{P}
$$

而线性递归情形下，概率还是有理数并可精确多项式时间求解。这个版本还把 `SQRT\text{-}SUM`、`PosSLP` 等下界和 `HMC`、piecewise-linear 子类的边界一起整理出来，所以它比 conference 版更适合做 family 总结锚点。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | components、boxes、entry/exit、return ports。 |
| 事件 / 触发 | 中等支持 | 概率标注边驱动。 |
| 守卫 / 数据 | 不支持 | 原文核心不在变量。 |
| 层次 | 强支持 | `HMC` 与一般 `RMC` 都保留显式层次 / 调用结构。 |
| 并发 / 同步 | 不支持 | 纯顺序递归。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率和 termination 值是中心。 |
| 可执行 / 可验证性 | 强理论支持 | `LFP`、Newton、`1-exit/linear/bounded/HMC` 子类算法。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 家族总元组 | `$A=(A_1,\ldots,A_k)$` | `RMC` 总骨架。 |
| 全局状态 | `$\langle \beta,u\rangle \in B^*\times Q$` | 调用栈 + 当前顶点。 |
| 方程系统 | `$x=P(x)$` | termination / reachability 多项式系统。 |
| 最小不动点 | `$q^*=\mathrm{LFP}(P)$` | 所求概率向量。 |
| 子类整理 | `HMC`, `1-exit`, `linear`, `bounded` | 概率递归支线内部的稳定分层。 |

## 构造方式与承载格式

### 建模入口

1. 用 components 表达过程或子系统。
2. 用 boxes 表达过程调用。
3. 用 entry / exit 表达参数化调用接口。
4. 用概率边表达局部随机行为。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `RMC` tuple；
2. 全局 Markov chain 语义；
3. 单调多项式系统 `$x=P(x)$`；
4. 分解式 Newton 迭代与 SCC 分解。

### 交换与互操作

它与当前文库中的几条线直接相关：

1. 向上承接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM`。
2. 向旁边把 `SCFG/MT-BP` 拉回到状态机家族。
3. 向下为 [recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md) 和 [recursive-concurrent-stochastic-games/desc.md](../recursive-concurrent-stochastic-games/desc.md) 提供随机递归母线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 tuple 与 `LFP` 方程系统。
- 仿真/执行支持：可按全局 Markov chain 语义运行。
- 验证/分析支持：`PSPACE` 定量判定、`1-exit` 质性判定、分解式 Newton 近似。
- 代码生成/转换支持：原文给出与 `SCFG/MT-BP` 的双向变换，但不是工程代码生成。
- 标准化或社区生态：研究型 family，跨 program analysis、stochastic grammar、branching process。

## 适用场景与需求前提

### 适用场景

适合：

1. 概率递归控制流与概率过程调用。
2. 需要系统整理 `RMC/HMC/1-exit/linear/bounded` 内部边界。
3. 想把 `SCFG/MT-BP` 纳入状态机族演化树。

### 需求前提

1. 系统以顺序递归为主。
2. 概率是本体结构的一部分。
3. 接口宽度可抽象成有限 entry / exit。

### 不适用或高成本场景

如果还需要决策者或对手，应改用 `RMDP/RSSG/RCSG`；如果只有有限层次、没有递归，则普通 `HSM/HMC` 即可。

## 与相邻形式主义的关系

相对 conference 版，这篇条目更多承担 family consolidation 角色；相对 `RSM`，它把随机性纳入本体；相对 `RMDP/RSSG`，它仍是无控制器、无对手的 closed stochastic recursive model。

## 与本研究的关系

### 对 Project 1 的价值

它让 `RSM` 后的 probabilistic recursive branch 不再只是一个孤立节点，而是拥有清楚的子类结构和数值语义支撑。

### 对状态机自动建模的启发

若需求同时包含递归调用与已知概率分支，这篇论文给出的不是某个应用套路，而是直接可落树的 formal family。

### 现实限制

它更适合作为理论中间表示和谱系节点，而不是工业前端 DSL。

## 重要的相关工作

1. [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations/desc.md)：conference 起点。
2. [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md)：在 `RMC` 上加入 controller / adversary。
3. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：`RMC` 的非概率母线 `RSM`。

## 文献分类总结

- 这篇文献在 `state_machine_types` 中属于：`🌊 混成 / 随机扩展`
- 这篇文献在 `state_machine_types` 中的对象类型是：`🧱 模型本体`
- 这篇文献在 `state_machine_types` 中描述的客体是：`🎛️ 控制 / 反应式逻辑`
- 这篇文献在 `state_machine_types` 中所属的领域是：`🧮 形式语言与自动机理论`

它应挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> Probabilistic Recursive State-Machine 支线 -> RMC/HMC` 位置，并作为该节点的 journal full version 依据。

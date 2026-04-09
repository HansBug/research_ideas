# 递归概率状态机的算法验证 / Algorithmic Verification of Recursive Probabilistic State Machines

## 基本信息

- 标题：Algorithmic Verification of Recursive Probabilistic State Machines
- 中文标题：递归概率状态机的算法验证
- 作者：Kousha Etessami、Mihalis Yannakakis
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems* (`TACAS 2005`, `LNCS 3440`), pp. 253-270, 2005
- DOI：`10.1007/978-3-540-31980-1_17`
- 链接：https://homepages.inf.ed.ac.uk/kousha/tacas05_rmc.pdf
- 形式主义：`Recursive Probabilistic State Machines / Recursive Markov Chains (RPSM / RMC)`
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：conference origin / 概率递归状态机验证 family 锚点
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 `RMC` tuple、全局 denumerable Markov chain、entry-exit probability 方程与 `Buchi` automaton product。
- 标准/格式获取方式：原文没有 DSL 或交换标准；核心承载方式是 `RMC` 组件元组、全局链语义、`1-exit` / `Bd-RMC` 子类与 least-fixed-point 方程。

## 简报

这篇论文的标题写的是 `Recursive Probabilistic State Machines`，但正文正式定义的其实是 `Recursive Markov Chains (RMCs)`。因此这里把 `RPSM` 视为标题层口径、把 `RMC` 视为文中真正落到 tuple 与语义上的 formal family，这是基于原文定义部分的保守归纳。对当前文库来说，这篇条目的价值不只是“做了验证算法”，而是把 `RSM` 的概率版本再次清晰写成一个可长期引用的模型本体入口，并顺带稳定了 `1-exit RMC` 与 `Bd-RMC` 这两个 subtype 口径。

- 形式主义定位：`RSM` 的概率扩展，也是 `Statecharts -> HSM -> uHSM -> RSM` 之后随机递归支线的 conference-level 锚点。
- 构造方式简述：系统由多个 finite-state components 组成，每个 component 具有 nodes、boxes、entry/exit，内部转移按概率选择，box 调用被调 component 后在 exit 处返回。
- 基础设施与场景简述：原文虽以 `Buchi` model checking 为主，但同时把 `1-exit RMC`、bounded total entry-exit `RMC` 和 `q^*` fixed-point semantics 放在一处，适合作为 `RMC` 子类命名依据。

```text
RSM skeleton + probabilistic transitions -> global denumerable Markov chain -> entry-exit probabilities / omega-regular model checking
```

## 形式主义定义与核心对象

### 定义对象

原文研究的是带 recursion 的 probabilistic procedural programs。它把 ordinary `RSM` 的 component / box / call-return 骨架保留下来，只把“普通转移”改成“概率转移”，从而得到 `RMC`。

### 核心抽象

原文给出的 `RMC` 写法是：

$$
A=(A_1,\ldots,A_k)
$$

其中每个组件

$$
A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是 ordinary nodes。
2. `B_i` 是 boxes，也就是递归调用点。
3. `Y_i:B_i\to\{1,\ldots,k\}` 指明 box 调用哪个组件。
4. `En_i` 与 `Ex_i` 分别是 entry / exit 节点集合。
5. `\delta_i` 是带概率的转移关系。

原文还把 call / return ports 显式引入，使 box 不只是一个“跳转标签”，而是一个拥有被调组件接口的结构节点。

### 一个最小例子与通俗解释

最小直觉例子是一个 probabilistic procedure `P`：

1. `P` 以 `1/2` 的概率直接结束。
2. 以 `1/2` 的概率调用自己一次。
3. 调用返回后再决定是否继续。

这在 `RMC` 里就会变成：

1. 一个 component；
2. 一个 box，映射到自身；
3. 若干 entry / exit；
4. 带概率的 local transitions。

通俗地说，`RMC` 就是“给 `RSM` 的 call/return 结构装上概率边”。普通 `Markov chain` 只能在一张平面图里随机游走；`RMC` 则允许随机过程进入子过程、递归返回，再继续随机演化。

### 运行 / 接受 / 转移语义

原文把 `RMC` 的运行语义显式落成一个全局可数马尔可夫链：

$$
M_A=(V,\Delta)
$$

上式中的符号逐项解释如下：

1. `V` 是全局状态集合，状态形如 `\langle \beta,u\rangle`。
2. `\beta` 是当前调用栈上的 box 序列。
3. `u` 是当前活动节点。
4. `\Delta` 是全局概率转移关系。

entry-exit reachability 的核心量写成：

$$
q^*_{(u,ex)}=\Pr(\text{starting at } \langle\epsilon,u\rangle \text{ eventually reaches } \langle\epsilon,ex\rangle)
$$

上式中的符号逐项解释如下：

1. `u` 是某个 component 内的顶点。
2. `ex` 是同一 component 的一个 exit。
3. `\langle\epsilon,u\rangle` 表示空栈启动。
4. `q^*_{(u,ex)}` 是从 `u` 最终以空栈从 `ex` 退出该 component 的概率。

### 语义边界

原文在模型层面把几个重要子类写得很清楚：

1. `1-exit RMC`：每个 component 最多一个 exit。
2. `Bd-RMC`：总 entry / exit 数有常数上界。
3. 一般 `RMC`：允许多 exit，接口宽度不受常数约束。

其中 `1-exit RMC` 对应 `SCFG/MT-BP` 这条经典等价线，是当前树里最值得保留的 subtype。

### 关键性质与判定边界

原文最关键的 formal object 是 least-fixed-point 方程组：

$$
x=P(x)
$$

上式中的符号逐项解释如下：

1. `x` 收集所有 `x(u,ex)` 变量。
2. `x(u,ex)` 对应上面的 entry-exit probability。
3. `P` 是由 ordinary transition、call port 与 return port 诱导的多项式算子。

原文明确指出：

$$
q^*=\mathrm{LFP}(P)
$$

这意味着 `RMC` 的概率语义不是靠 ad hoc simulation 给出的，而是被压成单调多项式系统的最小不动点。

在 `omega`-regular model checking 方面，原文考虑：

$$
P_A(L(B))
$$

上式中的符号逐项解释如下：

1. `A` 是给定 `RMC`。
2. `B` 是 `Buchi automaton` 规格。
3. `L(B)` 是 `B` 接受的 `omega`-语言。
4. `P_A(L(B))` 是 `A` 的运行被 `B` 接受的概率。

对 family 边界而言，最重要的不是具体复杂度常数，而是：

1. 一般 `RMC` 已形成稳定的 `omega`-regular model-checking 对象。
2. `1-exit RMC` 与 `Bd-RMC` 在 `|A|` 维度上更可控。
3. 这些子类因此值得直接进演化树，而不是只留在复杂度证明里。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | component、box、entry/exit 与 global stack state 都保留。 |
| 事件 / 触发 | 弱支持 | 原文主要是概率转移，不强调独立事件接口。 |
| 守卫 / 数据 | 不支持 | 无显式变量或守卫。 |
| 层次 | 强支持 | 递归 component hierarchy 是模型本体。 |
| 并发 / 同步 | 不支持 | 讨论的是 sequential recursive stochastic systems。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率转移是核心扩展。 |
| 可执行 / 可验证性 | 强理论支持 | `q^*` fixed-point、`Buchi` model checking、`1-exit/Bd-RMC` 子类边界都很清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `RMC` 骨架 | `$A=(A_1,\ldots,A_k)$` | 概率递归状态机的组件集合。 |
| component tuple | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)$` | 说明 `RSM` 骨架如何被概率化。 |
| 全局链语义 | `$M_A=(V,\Delta)$` | 把递归系统落成可数 Markov chain。 |
| entry-exit probability | `$q^*_{(u,ex)}$` | `RMC` 最核心的数值语义。 |
| least fixed point | `$q^*=\mathrm{LFP}(P)$` | 说明概率语义的正式求值方式。 |

## 构造方式与承载格式

### 建模入口

1. 先按递归 procedures 拆成 components。
2. 每个 component 明确 entry / exit。
3. 用 boxes 表达过程调用。
4. 给 ordinary transitions 指定概率。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `RMC` component tuple；
2. call / return ports；
3. 全局 Markov chain `M_A`；
4. 多项式 fixed-point system `x=P(x)`。

### 交换与互操作

它与当前文库中的几条线关系很直接：

1. 向上承接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM`。
2. 向下引出 [recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md) 的 controlled/game branch。
3. 向旁边连接 `SCFG`、`MT-BP` 与 probabilistic pushdown systems。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `RMC` tuple、全局链语义与 fixed-point 方程。
- 仿真/执行支持：可按全局 Markov chain `M_A` 运行。
- 验证/分析支持：entry-exit probabilities、`Buchi` model checking、qualitative / quantitative analysis。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 probabilistic pushdown / recursive stochastic systems / formal-language theory 的经典交叉点。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归概率程序。
2. 随机过程调用 / 返回系统。
3. 需要把 `SCFG/branching process` 重新接回 state-machine tree 的场景。

### 需求前提

1. 系统核心必须是 sequential recursion。
2. 概率选择属于模型本体，而不是外部噪声注释。
3. 过程接口必须可抽成有限 entry / exit。

### 不适用或高成本场景

若系统是 turn-based 或 concurrent game，应转向 `RMDP/RSSG/RCSG`；若需求只需平面概率有限状态机，普通 `Markov chain` 即可；若含时间或连续变量，则需另接 `RTA/RHA`。

## 与相邻形式主义的关系

相对 ordinary `RSM`，`RMC` 的新增点是概率转移；相对 `RMDP/RSSG`，它还没有玩家分区；相对 probabilistic pushdown systems，它更保留 component/box/entry/exit 的层次接口结构。

## 与本研究的关系

### 对 Project 1 的价值

它把层次状态机主线从 deterministic call/return 推向概率递归控制流，是 `RSM` 之后最自然的一条随机扩展线。

### 作为目标形式主义还是中间表示

对随机递归控制逻辑，它可以直接作为目标形式主义；对一般需求到模型生成，它更像高表达力理论落点。

### 对需求到模型生成的启发

如果需求里出现“子过程调用 + 随机结果 + 终止概率 / 满足概率”这样的描述，LLM 生成 `RMC` 往往比生成 flat `DTMC/MDP` 更自然。

## 重要的相关工作

1. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：`RSM` 母线。
2. [checking-ltl-properties-of-recursive-markov-chains/desc.md](../checking-ltl-properties-of-recursive-markov-chains/desc.md)：把 `RMC` 继续推进到 direct `LTL` 入口。
3. [model-checking-of-recursive-probabilistic-systems/desc.md](../model-checking-of-recursive-probabilistic-systems/desc.md)：同一 family 的 journal full version。

## 文献分类总结

- 这篇论文属于 `🌊 混成 / 随机扩展`。
- 这篇论文的对象类型是 `🧱 模型本体`。
- 这篇论文描述的客体是 `🎛️ 控制 / 反应式逻辑`。
- 这篇论文所属领域是 `🧮 形式语言与自动机理论`。

它最适合挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> Probabilistic Recursive State-Machine 支线 -> RMC` 之下，并为 `1-exit RMC` 与 `Bd-RMC` 这些 subtype 提供 conference-level 命名依据。

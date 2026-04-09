# 递归马尔可夫决策过程中的可达性 / Reachability in Recursive Markov Decision Processes

## 基本信息

- 标题：Reachability in Recursive Markov Decision Processes
- 中文标题：递归马尔可夫决策过程中的可达性
- 作者：Tomas Brazdil, Vaclav Brozek, Vojtech Forejt, Antonin Kucera
- 发表：*Concurrency Theory*, `LNCS 4137`, pp. 358-374, 2006
- DOI：`10.1007/11817949_24`
- 链接：https://www.fi.muni.cz/usr/kucera/papers/concur06.pdf
- 形式主义：`1-exit Recursive Markov Decision Processes (1-RMDP)` 的 `BPA / stateless PDA` 正规化视角
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：`1-exit RMDP` 子类 / `BPA` 等价口径稳定条目
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 `1-exit RMDP ↔ BPA` 对应、扩展可达性目标 `S U T`、规则诱导的 `1 1/2-player` Markov 链及 `SMD` 策略语义。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 `BPA` 规则系统、top-of-stack 配置语义与扩展可达性目标。

## 简报

这篇论文表面上讨论的是 reachability，但它对当前文库真正重要的地方在于：它把 `RMDP/RSSG` 家族里最关键、也最容易挂树的一条 subtype 口径彻底写实了，即 `1-exit RMDP` 与 stateless `PDA/BPA` 的等价表示。对层次状态机演化树来说，它不是另起一条方法线，而是把 `RMDP/RSSG` 节点下的 `1-exit / BPA-equivalent` 子类稳定成一个可以长期引用的经典分支说明。

- 形式主义定位：`RMDP/RSSG` 下最典型的 `1-exit` 子类条目，用 `BPA` 口径把递归随机状态机压成更简洁的正规化表示。
- 构造方式简述：把 `1-exit RSM/RMDP` 视为栈顶符号驱动的 stateless pushdown / `BPA` 游戏；配置只看栈串，控制选择也只作用于 top-of-stack symbol。
- 基础设施与场景简述：原文重点是扩展可达性与 `PCTL`，但更长期的文库价值在于它把 `1-exit`、`BPA`、top-of-stack regular winning region 与 `SMD` 策略这些 family 关键词固定到了同一处。

```text
RMDP / RSSG -> 1-exit restriction -> BPA / stateless PDA presentation -> top-of-stack objective -> regular winning set
```

## 形式主义定义与核心对象

### 定义对象

原文研究的是由 stateless pushdown automata 生成的 `1 1/2-player` 游戏 / 决策过程，并明确指出它们“恰好对应” `1-exit recursive state machines`。因此，这篇论文最适合作为 `RMDP/RSSG` 下面 `1-exit` 正规化子类的代表条目。

### 核心抽象

按原文的 `BPA` 视角，可以把这一 family 保守写成：

$$
\mathcal B = (\Gamma,\Delta,\Gamma_\circ,\Gamma_2)
$$

上式中的符号逐项解释如下：

1. `\Gamma` 是栈字母表，也就是所有 top-of-stack symbols。
2. `\Delta` 是重写 / 转移规则集合，用于把当前栈顶符号改写成新的栈串。
3. `\Gamma_\circ` 是概率符号集合，其后继按固定分布选择。
4. `\Gamma_2` 是控制者可决策的符号集合。

这里的 tuple 写法是对论文 `BPA` 叙述的保守整理；原文强调的是“`1-exit RSM` 可以等价表示成 stateless `PDA/BPA`”，而不是再发明一个新 DSL。

### 一个最小例子与通俗解释

一个最小例子可以是这样的 top-of-stack 递归过程：

1. 栈顶符号 `X` 表示“当前还没完成一个子过程”。
2. 控制者可以把 `X` 改写成 `YX`，表示先递归展开一个子过程 `Y` 再回来继续。
3. 也可以把 `X` 直接改写成 `\epsilon`，表示当前过程正常结束。

通俗地说，这类模型像“只看栈顶符号就做决策的递归随机状态机”。相比普通 `RMDP` 的 component / box 图形直觉，这里把模型压成了更接近形式语言理论的 `BPA` 记法，因此特别适合拿来稳定 `1-exit` 子类。

### 运行 / 接受 / 转移语义

原文把扩展可达性目标定义成“在始终留在 safe 集合里时到达 terminal 集合”。如果 `M` 是策略固定后的 Markov 链，`s` 是起始配置，则：

$$
\mathrm{Run}(M,s,S \mathbin{U} T)=\{w\in \mathrm{Run}(M,s)\mid \exists j\ge 0:\ w(j)\in T\land \forall i<j:\ w(i)\in S\}
$$

上式中的符号逐项解释如下：

1. `S` 是 safe configurations 集合。
2. `T` 是 terminal configurations 集合。
3. `w(j)\in T` 表示第一个成功命中终止目标。
4. `\forall i<j: w(i)\in S` 表示在命中之前始终保持安全。

原文特别强调，这里的 `S` 和 `T` 都只依赖 top-of-stack symbol，这使得 winning region 可以回落到 regular language / finite automaton 口径。

### 语义边界

这篇条目的模型边界如下：

1. 它只处理 `1-exit` 子类，而不是一般 multi-exit `RMDP`。
2. 它关注的是 top-of-stack 目标，因此特别适合 `BPA` 正规化。
3. 它仍是 turn-based / controller-vs-probability 模型，不是 concurrent game。
4. 它没有引入 reward、time 或连续变量。

### 关键性质与判定边界

原文的关键结论不是新建一个大类，而是说明 `1-exit` 子类在 `BPA` 表达下能保住强结构性：

$$
\text{qualitative extended reachability for 1-exit RMDP / BPA games} \in P
$$

并且 winning set 仍然是 regular 的，可由一个有限自动机表示。策略方面，原文把 termination 口径下的强结果显式回顾为：

$$
\text{optimal strategies for 1-exit BPA termination are SMD}
$$

这里 `SMD` 指 stackless-memoryless-deterministic。对当前文库而言，这说明 `1-exit` 子类不是“只是算法更容易”，而是模型本体已经收缩到一个高度正规、适合独立命名的 family。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 配置是栈串，核心对象是 top-of-stack symbol。 |
| 事件 / 触发 | 强支持 | 重写规则 / 转移规则直接驱动配置演化。 |
| 守卫 / 数据 | 不支持 | 无显式变量。 |
| 层次 | 强支持 | 本质仍是递归 call-return 结构，只是正规化成 `BPA`。 |
| 并发 / 同步 | 不支持 | 不是 concurrent game。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率与控制选择共同存在。 |
| 可执行 / 可验证性 | 强理论支持 | `S U T` 目标、regular winning set、`PCTL` model checking。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `1-exit` 正规化 | `1-exit RSM \equiv` stateless `PDA/BPA` | 这是全文最关键的 family 对应。 |
| 扩展可达性目标 | `$\mathrm{Run}(M,s,S \mathbin{U} T)$` | safe-until-terminal 的规范目标。 |
| winning-set regularity | regular language / DFA representation | `1-exit` 子类可有效落回有限自动机口径。 |
| termination 策略性质 | `SMD` | top-of-stack 子类的强结构性。 |

## 构造方式与承载格式

### 建模入口

1. 先把递归过程压成有限个栈符号类型。
2. 再按 top-of-stack symbol 给出概率 / 控制规则。
3. 把目标写成只依赖栈顶的 safe / terminal 条件。
4. 需要时再从 `BPA` 口径反向解释回 `1-exit RSM/RMDP`。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. `BPA` 规则系统；
2. top-of-stack objective；
3. finite automaton representation of winning sets；
4. `PCTL` model-checking reduction。

### 交换与互操作

它与当前文库中的关系非常明确：

1. 向上承接 [recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md) 的 `RMDP/RSSG` 母节点。
2. 向旁边连接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM` / `1-exit RSM` 语义。
3. 向下与 [efficient-qualitative-analysis-of-classes-of-recursive-markov-decision-processes-and-simple-stochastic-games/desc.md](../efficient-qualitative-analysis-of-classes-of-recursive-markov-decision-processes-and-simple-stochastic-games/desc.md) 的 linearly-recursive `1-RMDP / 1-RSSG` 子类自然接续。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `BPA` 规则、top-of-stack 目标与 DFA 表示。
- 仿真/执行支持：可按规则诱导的 Markov 决策过程直接运行。
- 验证/分析支持：qualitative extended reachability、qualitative `PCTL`。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，但在 `BPA / pushdown / recursive-state-machine` 三个社区之间互操作性很强。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要把 `RMDP` 明确收缩到 `1-exit` 子类。
2. 目标只依赖栈顶 / 过程接口，而不是全局复杂数据。
3. 想把层次状态机支线和 `BPA` / formal-language 理论直接挂接起来。

### 需求前提

1. 每个递归组件只有一个 exit。
2. 关心的性质可以写成 top-of-stack safe / terminal 目标。
3. 系统复杂度主要来自递归，而不是并发、时间或 reward。

### 不适用或高成本场景

如果系统需要 multi-exit 递归接口、并发博弈、reward 或时间语义，这个子类就太窄，应回到一般 `RMDP/RSSG` 或其后继扩展。

## 与相邻形式主义的关系

相对一般 `RMDP/RSSG`，这篇条目专门把 family 收缩到 `1-exit`；相对 `RSM`，它这里引入了概率 / 控制语义；相对 `linearly-recursive 1-RSSG`，它还没有进一步限制 return-to-call 依赖图；相对 positive-reward `1-RSSG`，它还没有把 termination / reachability 推到 total expected reward。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合作为演化树里 `RMDP/RSSG` 下 `1-exit / BPA-equivalent` 挂接说明，因为它把一个原本容易写得很泛的 family 收成了可直接命名的经典子类。

### 作为目标形式主义还是中间表示

更适合作为高表达力理论中间表示，而不是工程交付语言。

### 对需求到模型生成的启发

如果需求里的递归调用根本不返回多路值，只需要“调用完继续往下走”的 `1-exit` 语义，那么生成一般 `RMDP` 往往过重，直接识别为 `1-exit / BPA-equivalent` 子类更合适。

## 重要的相关工作

1. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：递归状态机母线。
2. [recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md)：把 `RMC` 推到 controlled / game recursive stochastic family。
3. [efficient-qualitative-analysis-of-classes-of-recursive-markov-decision-processes-and-simple-stochastic-games/desc.md](../efficient-qualitative-analysis-of-classes-of-recursive-markov-decision-processes-and-simple-stochastic-games/desc.md)：继续把 `1-exit` 子类细分到 linearly-recursive family。

## 文献分类总结

- 这篇论文属于 `🌊 混成 / 随机扩展`。
- 这篇论文的对象类型是 `🧱 模型本体`。
- 这篇论文描述的客体是 `🤝 接口 / 交互契约`。
- 这篇论文所属领域是 `🧮 形式语言与自动机理论`。

它最适合挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM -> Probabilistic Recursive State-Machine 支线 -> RMDP/RSSG` 之下，作为 `1-exit / BPA-equivalent` 子类的代表条目，而不是单独另起一条与层次状态机无关的新主线。

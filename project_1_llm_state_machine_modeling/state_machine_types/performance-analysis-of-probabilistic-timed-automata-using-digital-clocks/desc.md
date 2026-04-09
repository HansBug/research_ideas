# 用数字时钟分析概率定时自动机性能 / Performance Analysis of Probabilistic Timed Automata using Digital Clocks

## 基本信息

- 标题：Performance Analysis of Probabilistic Timed Automata using Digital Clocks
- 中文标题：用数字时钟分析概率定时自动机性能
- 作者：Marta Kwiatkowska，Gethin Norman，David Parker，Jeremy Sproston
- 发表：*Formal Methods in System Design*，29(1):33-78，2006
- DOI：`10.1007/s10703-006-0005-2`
- 链接：https://doi.org/10.1007/s10703-006-0005-2
- 形式主义：`Probabilistic Timed Automata / digital clocks / PRISM-style quantitative verification`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：digital-clocks verification route for closed diagonal-free `PTA`
- 工具/实现获取方式：论文明确说明其方法已用 `PRISM` 实现 integral-semantics / `MTBDD` verification，并在多个概率实时协议上做实验；正文未把该方法单独发布成独立工具。
- 标准/格式获取方式：承载对象是 `PTA`、dense/integral semantics、`PRISM` guarded-command encoding 与 cost/reward queries；它不是新的交换标准。

## 简报

这篇论文解决的是一个很核心的问题：经典 timed automata 里常见的 digital-clocks 技巧，什么时候也足以支撑 probabilistic timed automata 的性能分析。作者给出的答案是：对 closed、diagonal-free 的 `PTA`，不仅 probabilistic reachability，连 expected reachability 也能在 integral semantics 下保持正确，从而可以把连续时间模型压成有限、可由 `PRISM` 直接求解的对象。

- 形式主义定位：`PTA` 的定量验证方法，不是新的自动机母型。
- 构造方式简述：先给 `PTA` 定义 dense-time semantics 与 integral semantics，再证明两者在特定片段上对概率/期望可达分析等价，最后映射到 `PRISM`。
- 基础设施与场景简述：依托 digital clocks、`MTBDD`、`PRISM`、closed diagonal-free 约束与 cost/reward encoding，服务概率实时协议和嵌入式控制分析。

```text
closed diagonal-free PTA -> integral semantics / digital clocks -> finite MDP-like model -> PRISM quantitative checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. probabilistic timed automata (`PTA`)。
2. dense-time semantics 与 integral semantics。
3. probabilistic reachability 与 expected reachability。
4. digital-clocks reduction。
5. `PRISM` 上的实现化验证流程。

### 核心抽象

论文给出的 `PTA` 骨架可直接整理为：

$$
PTA = (L, \bar{l}, X, \Sigma, inv, prob)
$$

上式中的符号逐项解释如下：

1. `L` 是离散 location 集合。
2. `\bar{l}` 是初始 location。
3. `X` 是时钟集合。
4. `\Sigma` 是动作集合。
5. `inv` 给每个 location 一个 invariant。
6. `prob` 给出带 guard 和离散概率分布的边。

对概率边，论文明确采用：

$$
prob \subseteq L \times CC(X) \times \Sigma \times Dist(2^X \times L)
$$

上式中的符号逐项解释如下：

1. `CC(X)` 是时钟约束集合。
2. `Dist(2^X \times L)` 是“重置时钟集合 + 目标 location”上的离散概率分布。
3. 这说明一次跳转不仅会选目标位置，还会概率性地选 reset 集。

数字时钟语义的关键在于把每个时钟截断到 `k_x + 1`，可写成：

$$
(v \oplus_N t)(x) = \min\{v(x) + t,\ k_x + 1\}
$$

上式中的符号逐项解释如下：

1. `v` 是当前整数时钟赋值。
2. `t` 是离散时间延迟。
3. `k_x` 是时钟 `x` 在模型中被比较到的最大常数。
4. `k_x + 1` 代表“超过最大相关常数”的饱和值。

论文最重要的等价结果之一可保守写成：

$$
p^{\max}_{[[PTA]]_R}(F_R) = p^{\max}_{[[PTA]]_N}(F_N), \qquad
p^{\min}_{[[PTA]]_R}(F_R) = p^{\min}_{[[PTA]]_N}(F_N)
$$

上式中的符号逐项解释如下：

1. `[[PTA]]_R` 是 dense-time semantics。
2. `[[PTA]]_N` 是 integral semantics。
3. `F_R`、`F_N` 是对应语义下的目标状态集。
4. 该等式仅在论文给定的 closed diagonal-free 条件下成立。

### 一个最小例子与通俗解释

论文首页给了一个很直观的 retransmission 例子：

1. 系统发送一条消息后进入 `WAIT`。
2. 时钟 `c` 记录等待时间，必须在给定窗口内决定成功、重传或失败。
3. 某条发送边以 `99/100` 概率成功，以 `1/100` 概率丢失。
4. 问题不再只是“能不能到达成功状态”，而是“多大概率成功、期望多久或花多少代价成功”。

通俗地说，普通 `TA` 关心“什么时候能跳”；`PTA` 还关心“跳过去时各结果出现的概率是多少”。这篇论文证明：在不少重要场景里，你不必真的保留连续时钟，也能算对这些概率和期望。

### 运行 / 接受 / 转移语义

论文把 `PTA` 的语义定义成 timed probabilistic system。一步离散概率跳转的直觉可写成：

$$
(l,v) \xrightarrow{a,\mu} (l', v[X:=0])
$$

上式中的符号逐项解释如下：

1. `(l,v)` 是当前 location 与时钟赋值。
2. `a` 是动作标签。
3. `\mu` 是对 `(X,l')` 的离散概率分布。
4. `v[X:=0]` 表示对被选中的重置集做时钟清零。

论文关心的两类定量查询分别是：

$$
\min/\max\ \Pr(\Diamond F), \qquad \min/\max\ \mathbb{E}[Cost\ \mathrm{Until}\ F]
$$

其中：

1. `\Pr(\Diamond F)` 是到达目标集 `F` 的概率。
2. `\mathbb{E}[Cost\ \mathrm{Until}\ F]` 是到达 `F` 前的期望累计代价。
3. `\min/\max` 对应 nondeterminism 下的最小/最大值。

### 语义边界

1. digital-clocks 等价只覆盖 closed、diagonal-free `PTA` 片段。
2. 论文明确指出一般 stopwatch 性质和更强 `PTCTL` 性质不能简单由 integral semantics 保证。
3. 方法依赖 rational probabilities 与时钟上界截断。
4. 它是方法论文，不是 `PRISM 4.0` 那种工具平台总览。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PTA` 元组 | `$PTA = (L, \bar{l}, X, \Sigma, inv, prob)$` | 分析对象是概率定时自动机。 |
| 概率边 | `$prob \subseteq L \times CC(X) \times \Sigma \times Dist(2^X \times L)$` | 每条边同时包含 guard、action、reset 与概率目标。 |
| 数字时钟更新 | `$(v \oplus_N t)(x) = \min\{v(x)+t,\ k_x+1\}$` | integral semantics 的核心截断规则。 |
| 概率等价 | `$p^{\max/\min}_{[[PTA]]_R}(F_R) = p^{\max/\min}_{[[PTA]]_N}(F_N)$` | 在特定片段上，dense/integral 语义对 reachability 概率等价。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 以 location-based `PTA` 为核心。 |
| 事件 / 触发 | 中等支持 | 动作与 guard 都是显式对象。 |
| 守卫 / 数据 | 强支持 | 时钟约束、概率分布与 reward/cost 同时进入分析。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 中等支持 | 论文也定义了 `PTA` 的并行组合。 |
| 时间约束 | 很强 | 主体就是 dense/integral timed semantics。 |
| 连续动态 / 随机性 | 随机性强，连续动态不支持 | 概率是核心，但没有混成连续动力学。 |
| 可执行 / 可验证性 | 很强 | 直接落到 `PRISM` 上做 quantitative checking。 |

### 形式化问题与性质

1. 论文的核心命题是“哪些 `PTA` 查询在 digital clocks 下仍然是正确的”。
2. 它把 timed/probabilistic 理论与实际 `PRISM` 验证桥接起来，是很典型的方法母线。
3. 相对平台论文，它更强调语义保持条件与限制边界。

## 构造方式与承载格式

### 建模入口

论文中的主要建模入口是：

1. `PTA` locations、时钟与概率边。
2. target locations / reward functions。
3. digital-clocks 语义离散化。
4. `PRISM` guarded-command encoding。

### 机器可处理承载方式

机器可处理承载方式包括：

1. dense-time `PTA`。
2. integral-semantics finite model。
3. `PRISM` modules 与 integer clocks。
4. reward/cost query。

### 交换与互操作

互操作重点在于：

1. `PTA` 到 `PRISM` 的 integral-semantics 映射。
2. `MTBDD` backend 对 finite integral model 的利用。
3. 与后续 `mcpta/PRISM 4.0` 的概率实时平台路线直接相连。

## 配套基础设施

- 建模/编辑工具：主体不是 GUI，而是 `PTA` 建模与 `PRISM` 编码。
- 解析/交换/元模型支持：digital-clocks reduction、target sets 与 reward structure encoding。
- 仿真/执行支持：论文重点在概率/期望验证，不在运行时仿真。
- 验证/分析支持：probabilistic reachability、expected reachability、dense/integral 等价分析。
- 代码生成/转换支持：主要是 `PTA -> PRISM` 的分析性转换。
- 标准化或社区生态：后续 `PRISM`、`mcpta` 与概率实时验证线都明显受益于这条方法。

## 适用场景与需求前提

### 适用场景

适合带概率超时、重传、争用和代价分析的实时协议与嵌入式控制系统，尤其适合希望从连续时间模型退化到有限可解模型的场景。

### 需求前提

1. 模型应落在 closed、diagonal-free `PTA` 片段。
2. 目标性质主要是 probabilistic reachability 或 expected reachability。
3. 系统时间语义能接受 digital-clocks 的离散化。

### 不适用或高成本场景

若需求涉及一般 stopwatch 性质、复杂 `PTCTL` clock formulae 或更强的实时逻辑表达，这篇方法不能直接保证正确。

## 与相邻形式主义的关系

相对 [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)，本文更偏语义保持与方法基础，而不是高层语言到后端的自动翻译；相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，它是更早的 digital-clocks 方法锚点；相对 [fortuna-model-checking-priced-probabilistic-timed-automata/desc.md](../fortuna-model-checking-priced-probabilistic-timed-automata/desc.md)，这里的重点是等价约化与 reachability/expected reachability，而不是 multi-priced zones。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明若未来模型里引入概率与时间，不一定必须直接走复杂 dense-time symbolic engine，也可以先判断是否满足 digital-clocks 片段。
2. 对“生成-验证-修复”闭环而言，这种“先检测适用片段，再选择验证后端”的思路很有工程价值。
3. 它也提示需求建模阶段应尽量避免不必要的 diagonal/strict clock constraints。

### 作为目标形式主义还是中间表示

更像 quantitative verification 方法与后端约化路线，而不是直接面向最终用户的前端状态机语言。

### 对需求到模型生成的启发

1. 若需求里同时有概率和时间，最好尽早标明是否允许 diagonal constraints。
2. 生成模型时主动保持在可 digital-clocks 的片段内，能显著降低后续验证成本。

### 现实限制

文章的很多结果是“在特定片段上成立”的；若模型超出片段，不能机械套用其等价结论。

## 重要的相关工作

1. [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)：高层 `Modest` 到 `PTA/PRISM` 的方法路线。
2. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：`PTA/PPTA` 平台化工具版本。
3. [fortuna-model-checking-priced-probabilistic-timed-automata/desc.md](../fortuna-model-checking-priced-probabilistic-timed-automata/desc.md)：priced probabilistic timed reachability 工具条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统

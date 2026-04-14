# 递归马尔可夫链的 LTL 性质检验 / Checking LTL Properties of Recursive Markov Chains

## 基本信息

- 标题：Checking LTL Properties of Recursive Markov Chains
- 中文标题：递归马尔可夫链的 LTL 性质检验
- 作者：Mihalis Yannakakis、Kousha Etessami
- 发表：*Second International Conference on the Quantitative Evaluation of Systems* (`QEST 2005`), pp. 155-164, 2005
- DOI：`10.1109/QEST.2005.8`
- 链接：https://doi.org/10.1109/QEST.2005.8
- 形式主义：`Recursive Markov Chains (RMC) / linearly-recursive RMC family`
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：`LTL`-specific family stabilization / `linearly-recursive RMC` 锚点
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 `RMC` tuple、`LTL` satisfaction probability、`1-exit / Bd-RMC / lr-RMC` 子类与直接 `LTL` 算法。
- 标准/格式获取方式：原文无 DSL 或标准格式；核心承载方式是 `RMC` 组件定义、`LTL` 公式语义与 direct `LTL` model-checking construction。

## 简报

这篇论文表面上是“`RMC` 上做 `LTL` 模型检验”，但对演化树更重要的价值在于：它把 `1-exit RMC`、bounded total entry-exit `RMC` 以及 `linearly-recursive RMC (lr-RMC)` 三个结构子类放到了同一处，而且给了 `lr-RMC` 一个非常清晰的 family 口径。对当前文库来说，这正好可以把 `RMC` 节点继续细化出一个稳妥的 subtype，而不必再发明不稳的伪节点。

- 形式主义定位：`RMC` 家族里的 direct `LTL` 入口，也是 `lr-RMC` 命名最清楚的 early paper。
- 构造方式简述：仍以 components、boxes、entry/exit 和概率转移建模，只是把规格从 `Buchi automaton` 直接换成 `LTL` 公式。
- 基础设施与场景简述：原文最大的长期价值在于直接固定 `lr-RMC` 的结构限制，而不是只留下“先转 `Buchi` 再检验”的间接说法。

```text
RMC -> LTL property -> direct LTL model checking -> one-exit / bounded-interface / linearly-recursive subfamilies
```

## 形式主义定义与核心对象

### 定义对象

原文继续使用 `RMC` 作为概率递归控制流模型，并把 `LTL` 规格直接施加在 `RMC` 顶点标签生成的无限执行上。模型本体并没有变化，变化的是：它开始把哪些 `RMC` 结构子类更适合 direct temporal-property reasoning 说清楚。

### 核心抽象

`RMC` 的基本写法沿用：

$$
A=(A_1,\ldots,A_k),\qquad A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `A_1,\ldots,A_k` 是递归组件集合。
2. `N_i` 是 ordinary nodes。
3. `B_i` 是 boxes。
4. `Y_i` 指定 box 调用的组件。
5. `En_i` 与 `Ex_i` 是组件接口。
6. `\delta_i` 是概率转移。

原文随后显式点出三个结构子类：

1. `1-exit RMC`；
2. `Bd-RMC`；
3. `linearly-recursive RMC (lr-RMC)`。

其中 `lr-RMC` 的口径最值得保留。

### 一个最小例子与通俗解释

一个直觉例子是：

1. 组件 `A_1` 在每次执行时都可能调用 `A_2`。
2. `A_2` 结束后返回 `A_1`。
3. 如果组件内部不存在“从某个 return port 再走到另一个 call entry”的路径，那么它就落入 `lr-RMC` 这类更受限的 family。

通俗地说，`lr-RMC` 像是“同一组件里不允许把返回之后又立刻接进新的递归调用链”，于是递归依赖图更像一条线性展开链，而不是密集嵌套网。

### 运行 / 接受 / 转移语义

原文把 `LTL` satisfaction probability 写成：

$$
P_A(\varphi)
$$

上式中的符号逐项解释如下：

1. `A` 是给定 `RMC`。
2. `\varphi` 是 `LTL` 公式。
3. `P_A(\varphi)` 表示 `A` 的随机运行满足 `\varphi` 的概率。

和一般 `RMC` 一样，执行仍对应一个全局可数 Markov chain，差别在于性质不再先显式给成 `Buchi automaton`，而是直接从 `LTL` 出发。

### 语义边界

原文对 `lr-RMC` 的说明可以保守压成：

$$
\text{lr-RMC}: \text{ no component contains a path from a return port of a box to an entry of a box}
$$

上式中的符号逐项解释如下：

1. “return port of a box” 表示某次递归返回后的继续点。
2. “entry of a box” 表示同一组件里新的调用入口。
3. 若两者之间不存在同组件内部路径，就属于 linearly-recursive 子类。

这不是简单的算法假设，而是一个清楚的结构 family 条件。

### 关键性质与判定边界

对当前文库最值得保留的不是全部复杂度细节，而是三类 boundary：

1. 一般 `RMC` 的 direct `LTL` model checking 已是稳定问题。
2. `1-exit RMC` 与 `Bd-RMC` 在 `|A|` 维度上更容易处理。
3. `lr-RMC` 更进一步，能支持 exact probability 计算。

可压成如下代表性表述：

$$
\text{For lr-RMCs, exact } P_A(\varphi) \text{ is computable in time polynomial in } |A| \text{ and exponential in } |\varphi|
$$

这说明 `lr-RMC` 不是“只在证明里顺手提一下”的 complexity fragment，而是值得挂树的稳定 subtype。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | components、boxes、entry/exit 与栈语义完整保留。 |
| 事件 / 触发 | 弱支持 | 仍以概率递归控制流为主，不强调独立事件接口。 |
| 守卫 / 数据 | 不支持 | 无显式变量。 |
| 层次 | 强支持 | 递归 component hierarchy 仍是模型本体。 |
| 并发 / 同步 | 不支持 | 讨论的是 sequential `RMC`。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率转移是核心。 |
| 可执行 / 可验证性 | 强理论支持 | 原文把 `LTL`、`1-exit`、`Bd-RMC` 与 `lr-RMC` 边界清楚并列。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `RMC` 骨架 | `$A=(A_1,\ldots,A_k)$` | family 的统一母线。 |
| component tuple | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)$` | call/return + probability 的最小结构。 |
| `LTL` 满足概率 | `$P_A(\varphi)$` | direct `LTL` model-checking 的目标量。 |
| `lr-RMC` 结构限制 | return-port 到 box-entry 无路径 | linearly-recursive family 的核心定义。 |
| exactness boundary | polynomial in `|A|` for `lr-RMC` | 说明该子类有独立保留价值。 |

## 构造方式与承载格式

### 建模入口

1. 先按递归 procedures 建 `RMC`。
2. 再给顶点附上 atomic propositions。
3. 把需求写成 `LTL` 公式。
4. 若系统恰好满足 `1-exit` 或 `lr-RMC` 结构，再利用对应 family 口径。

### 机器可处理承载方式

主要包括：

1. `RMC` tuple；
2. 全局执行概率语义；
3. `LTL` formula；
4. `1-exit / Bd-RMC / lr-RMC` 子类判断。

### 交换与互操作

1. 向上接 [algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md](../algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md) 的 `RMC` / `RPSM` conference anchor。
2. 向后接 [model-checking-of-recursive-probabilistic-systems/desc.md](../model-checking-of-recursive-probabilistic-systems/desc.md) 的 journal full version。
3. 向旁边与 [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md) 的 `1-exit / linear / bounded` family 说明呼应。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `RMC` tuple 与 `LTL`-to-automata reasoning。
- 仿真/执行支持：可按全局 Markov chain 执行。
- 验证/分析支持：direct `LTL` model checking、qualitative / quantitative probability analysis。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 `RMC` family 与 temporal-logic verification 的经典理论交汇点。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归概率控制流上的长期时序性质分析。
2. 需要保留 `LTL` 而不想只停留在 `Buchi` 中间表示的场景。
3. 希望进一步识别 `lr-RMC` 子类的需求。

### 需求前提

1. 系统仍然是 sequential recursive stochastic family。
2. 需求主要是 `LTL`-style linear-time property。
3. 若想利用 strongest results，结构最好落在 `1-exit` 或 `lr-RMC`。

### 不适用或高成本场景

如果规格天然更像 branching-time 或开放系统性质，应转回 `Buchi/CTL` 或 `OPD`；如果系统已经引入玩家分区，则应转向 `RMDP/RSSG/RCSG`。

## 与相邻形式主义的关系

相对 [algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md](../algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md)，这篇条目没有换模型骨架，而是把 `LTL` 与 `lr-RMC` 子类讲清楚；相对 `RMDP/RSSG`，它仍是无玩家分区的纯 `RMC` family。

## 与本研究的关系

### 对 Project 1 的价值

它让 `RMC` 这条树枝不只停在“有概率”这一层，而是继续长出 `linearly-recursive` 这种足够稳定的 subtype。

### 作为目标形式主义还是中间表示

更像 `RMC` family 的理论细化节点，而不是独立工程交付语言。

### 对需求到模型生成的启发

如果需求里的时序性质本来就是线性时间叙述，而且递归调用图相对稀疏，那么让 LLM 进一步判断是否属于 `lr-RMC`，会比一律输出一般 `RMC` 更有价值。

## 重要的相关工作

1. [algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md](../algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md)：`RMC` conference anchor。
2. [model-checking-of-recursive-probabilistic-systems/desc.md](../model-checking-of-recursive-probabilistic-systems/desc.md)：同一 family 的 journal full version。
3. [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md)：随机递归 family 往 control/game 方向的扩展。

## 文献分类总结

- 这篇论文属于 `🌊 混成 / 随机扩展`。
- 这篇论文的对象类型是 `🧱 模型本体`。
- 这篇论文描述的客体是 `🎛️ 控制 / 反应式逻辑`。
- 这篇论文所属领域是 `🧮 形式语言与自动机理论`。

它最适合挂到当前演化树的 `RMC/HMC` 之下，作为 `linearly-recursive RMC` 这个 subtype 的代表条目，而不是单独另起新的主线。

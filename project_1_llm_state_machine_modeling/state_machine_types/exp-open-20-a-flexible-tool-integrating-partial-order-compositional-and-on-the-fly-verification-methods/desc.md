# Exp.Open 2.0：整合偏序、组合式与按需验证的并发验证工具 / Exp.Open 2.0: A Flexible Tool Integrating Partial Order, Compositional, and On-the-fly Verification Methods

## 基本信息

- 标题：Exp.Open 2.0: A Flexible Tool Integrating Partial Order, Compositional, and On-the-fly Verification Methods
- 中文标题：Exp.Open 2.0：整合偏序、组合式与按需验证的并发验证工具
- 作者：Frédéric Lang
- 发表：*Integrated Formal Methods (IFM 2005)*，pp. 70-88，2005
- DOI：`10.1007/11589976_6`
- 链接：https://doi.org/10.1007/11589976_6
- 形式主义：`LTS composition expressions / flat networks / synchronization vectors / Exp.Open 2.0`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：`CADP` concurrency front-end / `Open/Caesar`-based partial-order and compositional verification infrastructure
- 工具/实现获取方式：原文明确说明 `Exp.Open 2.0` 是 `CADP` 工具箱的组成部分，并给出 `CADP` 入口；论文未给独立于 `CADP` 的单独仓库。
- 标准/格式获取方式：主承载对象是 composition expressions、flat networks、synchronization vectors、`BCG`、`Open/Caesar`、`Fc2` 和 low-level `Pep` Petri nets；它是工具链与输入语言，不是中立标准。

## 简报

这篇论文补的是 `CADP` 生态里非常关键的一层前端基础设施。`Exp.Open 2.0` 的真正价值，不只是“再支持几种并发组合算子”，而是把 process algebra 风格的并发组合、on-the-fly exploration、partial-order reduction 和 compositional verification 放进同一个语言无关框架里，并直接复用 `Open/Caesar` back-end。它让很多不同前端形式最终都能先降成 flat network，再统一吃到 `CADP` 的验证后端。

- 形式主义定位：并发 `LTS` 组合与验证基础设施，而不是新的状态机本体。
- 构造方式简述：先把 composition expression 翻译成 flat network，再通过 `Open/Caesar` 的 `init/post` 风格接口做按需探索、偏序约减、组合式约束和外部后端分析。
- 基础设施与场景简述：依托 `CADP`、`Open/Caesar`、synchronization vectors、`BCG`、automata networks 与 Petri-net export，服务协议、通信并发系统与 process-algebra 规格验证。

```text
composition expression -> flat network -> Open/Caesar API -> on-the-fly exploration / partial-order reduction / CADP back-ends
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. labelled transition systems；
2. composition expressions；
3. synchronization vectors；
4. flat networks；
5. `Open/Caesar` 语言无关探索接口与 partial-order reduction。

### 核心抽象

论文把 flat network 定义为由若干个局部 `LTS` 与同步向量集合组成。可直接整理为：

$$
N = ((S_1,\ldots,S_n), Sync)
$$

上式中的符号逐项解释如下：

1. `S_1,\ldots,S_n` 是参与组合的局部 `LTS`。
2. `Sync` 是同步向量集合。
3. 每个同步向量左侧长度都是 `n`，与局部组件个数一致。
4. 论文明确说 Exp.Open 2.0 先把任意 composition expression 统一翻成这种 flat network。

全局状态则是各局部状态的元组：

$$
s = (s_1,\ldots,s_n)
$$

上式中的符号逐项解释如下：

1. `s_i` 是第 `i` 个局部 `LTS` 的当前状态。
2. 一个全局迁移要么来自若干局部迁移同步执行，要么来自单个局部迁移的异步执行。
3. 这正对应论文对 global state / global transition 的解释。

同步向量的骨架可写成：

$$
(L_1 \mid *) * \cdots * (L_n \mid *) \to L_0
$$

上式中的符号逐项解释如下：

1. `L_i` 表示第 `i` 个分量需要匹配的 gate 或 full label。
2. `*` 表示该位置不参与此次同步。
3. `L_0` 是同步后的结果标签。
4. 在 gate matching 模式下，同步后的标签还可附带同步分量共享的 offer 参数。

### 一个最小例子与通俗解释

论文里最直观的例子，是几个局部组件通过门 `G` 两两或多方同步：

1. 一个组件发 `Snd`，另一个组件发 `Rcv`。
2. synchronization vector 把它们同步成结果标签 `Com`。
3. 若某个局部动作不需要同步，它就可以独立异步执行。
4. 工具最终不直接保留复杂嵌套表达式，而是把它们先变成统一的 flat network。

通俗地说，`Exp.Open 2.0` 像一个“并发组合编译器”。前端可以保留不同 process algebra 的写法，但后端真正要验证时，都会被整理成同一张同步网络。

### 运行 / 接受 / 转移语义

局部到全局的同步一步可保守写成：

$$
(s_1,\ldots,s_n) \xrightarrow{L_0} (t_1,\ldots,t_n)
$$

上式中的符号逐项解释如下：

1. 对所有参与当前同步向量的位置，局部状态 `s_i` 会沿匹配 `L_i` 的转移走到 `t_i`。
2. 不参与同步的位置保持原状态。
3. 全局标签由同步向量右侧 `L_0` 决定。
4. 这对应论文对 Rule 6 语义的解释。

composition expression 的统一翻译工作流可写成：

$$
B \mapsto (s(B), v(B))
$$

上式中的符号逐项解释如下：

1. `B` 是原始 composition expression。
2. `s(B)` 是其中所有局部 `LTS` 的向量。
3. `v(B)` 是递归构造出的同步向量集合。
4. 论文明确说该翻译只依赖标签集合，不依赖状态空间大小，因此本身不触发 state explosion。

偏序约减的核心不是任意删边，而是在状态 `s` 上寻找 persistent set。可保守写成：

$$
P(s) \subseteq Enabled(s)
$$

上式中的符号逐项解释如下：

1. `Enabled(s)` 是在状态 `s` 上使能的 synchronization vectors 集合。
2. `P(s)` 是其中满足 persistent 条件的子集。
3. 对 branching-bisimulation preserving 情况，论文进一步收紧到“只含一个 deterministic `\tau` synchronization vector”的特殊 persistent set。

### 语义边界

1. `Exp.Open 2.0` 的主对象是并发组合与探索基础设施，不是新的控制建模语言。
2. 它主要处理有限状态并发系统；虽然 front-end 很灵活，但验证核心仍是 explicit-state 路线。
3. 工具擅长处理 action-based `LTS` 和 process algebra 组合，而不是富数据控制器或连续动力学。
4. flat network 是工具内部统一层，不是面向领域工程师的最终语义对象。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| flat network | `$N=((S_1,\ldots,S_n),Sync)$` | `Exp.Open 2.0` 的统一内部模型。 |
| global state | `$s=(s_1,\ldots,s_n)$` | 全局状态是局部状态的元组。 |
| synchronization vector | `$(L_1 \mid *) * \cdots * (L_n \mid *) \to L_0$` | 定义哪些局部动作需要同步及其结果标签。 |
| 统一翻译 | `$B \mapsto (s(B),v(B))$` | 任意 composition expression 都先被规整成 flat network。 |
| partial-order core | `$P(s) \subseteq Enabled(s)$` | persistent-set reduction 是按状态计算的。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕 `LTS` 组合展开。 |
| 事件 / 触发 | 很强 | 标签匹配、同步向量和结果标签是核心。 |
| 守卫 / 数据 | 弱支持 | 主要操作标签，不强调富数据守卫。 |
| 层次 | 不支持 | 不是层次状态图工具。 |
| 并发 / 同步 | 很强 | parallel composition、synchronization vectors 和 partial-order reduction 都是主线。 |
| 时间约束 | 不支持 | 本文不处理 timed semantics。 |
| 连续动态 / 随机性 | 部分支持 | 论文提到 stochastic branching-bisimulation preserving reduction，但不讨论连续动力学。 |
| 可执行 / 可验证性 | 很强 | on-the-fly exploration、compositional verification、partial-order reduction 和 `CADP` back-end 全部可用。 |

### 形式化问题与性质

1. 这篇论文真正补的是“把多种并发组合写法规整到同一探索接口”的工程方法。
2. flat network 与 `Open/Caesar` 的解耦，使验证后端几乎不需要关心前端语言差异。
3. persistent-set reduction 被做进 front-end，而不是强迫每个 back-end 单独实现一遍。

## 构造方式与承载格式

### 建模入口

原文中的建模入口有：

1. `CCS / CSP / LOTOS / E-LOTOS / muCRL` 风格标签和组合表达式；
2. renaming / hiding / cut operator；
3. 多种 binary 或 n-ary parallel composition；
4. synchronization vectors。

### 机器可处理承载方式

机器可处理承载方式包括：

1. composition expressions；
2. flat networks；
3. `BCG`、Aldebaran、`Fc2`、`Seq` 格式的局部 `LTS`；
4. `Open/Caesar` API 对应的 `init` 与 `IterateState()` 接口实现。

### 交换与互操作

互操作是本文核心价值之一：

1. flat networks 可导出为 low-level `Pep` Petri nets；
2. 也可导出为 `Fc2` automata networks；
3. 通过 `Open/Caesar`，`Exp.Open 2.0` 可以直接复用 `CADP` 的大量 back-end。

## 配套基础设施

- 建模/编辑工具：`Exp.Open 2.0` 输入语言与 `CADP` 命令行工具链。
- 解析/交换/元模型支持：composition expressions、flat networks、`BCG`、Aldebaran、`Fc2`、`Seq`。
- 仿真/执行支持：`Open/Caesar` 交互仿真、random execution 与 distributed state-space generation。
- 验证/分析支持：on-the-fly model checking、equivalence checking、reachability、deadlock detection、partial-order reduction、interface constraints。
- 代码生成/转换支持：支持导出 automata networks 和 low-level Petri nets。
- 标准化或社区生态：依托 `CADP`、`Open/Caesar` 与 `BCG` 生态；原文未给独立标准化组织。

## 适用场景与需求前提

### 适用场景

适合协议、并发组件、process algebra 规格和任何需要在多前端并发表达之间共享验证后端的场景。

### 需求前提

1. 系统行为最好能压成有限 `LTS` 组合。
2. 并发复杂度主要体现在同步组合与交错爆炸，而不是复杂数据域。
3. 团队需要 partial-order、compositional 和 on-the-fly 三条路线的组合收益。
4. 前端标签设计需要足够稳定，便于做 gate/full-label matching。

### 不适用或高成本场景

若系统核心难点是实数时钟、连续变量、富数据求解或图形层次状态机语义，`Exp.Open 2.0` 不是最自然入口。

## 与相邻形式主义的关系

相对 [cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md](../cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md)，本文更前置，重点是把多种并发组合写法和偏序约减接到 `CADP` 主平台上；相对 [context-constraints-for-compositional-reachability-analysis/desc.md](../context-constraints-for-compositional-reachability-analysis/desc.md)，二者都关心 compositional reachability，但本文更强调工具化的 front-end 与 persistent-set reduction；相对 [testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md](../testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md)，`TESTOR` 复用了 `CADP/Open-Caesar` 生态，而本文解释的是其中更基础的组合与探索层。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提示我们，未来如果 `project_1` 需要支持多种状态机/交互模型前端，先统一到中间组合表示再接验证后端会更稳。
2. synchronization vectors 对“多状态机协同”建模非常有启发，尤其适合表达需求里的交互同步约束。
3. partial-order reduction 做在前端，也说明“建模入口层”就能承担一部分可验证性优化职责。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`Exp.Open 2.0` 更像并发模型组合与探索基础设施，而不是最终输出给需求工程师的目标形式主义。

### 对需求到模型生成的启发

1. 不同语法的状态机/进程模型可以共享统一的组合语义层。
2. 先规整标签和同步关系，再做后端分析，比为每种语法分别实现验证更可维护。
3. 若后续生成的是多组件协作模型，synchronization-vector 风格中间层很值得参考。

## 重要的相关工作

- [cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md](../cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md)：`Exp.Open 2.0` 所依附的主工具箱平台。
- [context-constraints-for-compositional-reachability-analysis/desc.md](../context-constraints-for-compositional-reachability-analysis/desc.md)：更偏方法论的 compositional reachability 基线。
- [testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md](../testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md)：建立在 `CADP/Open-Caesar` 之上的后续测试工具线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 结论：这是一篇典型的并发组合与验证基础设施条目，适合作为 `CADP/Open-Caesar` 生态中 synchronization vectors、flat networks、partial-order reduction 与 compositional exploration 路线的核心证据入账。

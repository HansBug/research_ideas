# 可扩展的基于树的寄存器自动机学习 / Scalable Tree-based Register Automata Learning

## 基本信息

- 标题：Scalable Tree-based Register Automata Learning
- 中文标题：可扩展的基于树的寄存器自动机学习
- 作者：Simon Dierl，Paul Fiterau-Brostean，Falk Howar，Bengt Jonsson，Konstantinos Sagonas，Fredrik Tåkvist
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 14571`，pp. 87-108，2024
- DOI：`10.1007/978-3-031-57249-4_5`
- 链接：https://doi.org/10.1007/978-3-031-57249-4_5
- 形式主义：`register automata learning / SLλ / classification-tree and restricted-suffix route`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：tree-based register-automata learning method / scalable active-learning route for data languages
- 工具/实现获取方式：原文明确说明 `SLλ` 已作为新算法实现进公开的 `RALib`，并给出实验工件的 `Zenodo` 与 GitHub 更新入口；评测还直接对比 `SL*` 与 `SLCT`。
- 标准/格式获取方式：原文不主打交换标准；主要承载方式是 data words、`RA` 元组、classification tree、symbolic suffixes 与 `membership/equivalence queries`。

## 简报

这篇论文的关键价值，不是再定义一种新的寄存器自动机，而是把 `RA` 主动学习从 observation-table 路线推进到 classification-tree 路线，并系统压缩 suffix 的数量、长度与数据依赖范围。`SLλ` 的中心判断很明确：`RA` 学习真正的瓶颈不是“有没有 counterexample”，而是“tree query 为了区分 registers 和 guards 要做多少 membership queries”。因此论文把短 suffix、restricted suffix、counterexample 分析和 classification tree 放到同一条可扩展方法链里。

- 形式主义定位：围绕 `register automata` 的学习方法路线，而不是新的 `RA` 本体。
- 构造方式简述：用 classification tree 维护短前缀、symbolic suffix 与等价类，再由 tree queries 抽 guards、registers 与 target locations。
- 基础设施与场景简述：依托 `membership/equivalence queries`、`RALib`、restricted symbolic suffixes 与 counterexample analysis，服务带数据参数的 API、协议与 `EFSM/RA` 风格黑盒模型恢复。

```text
SUL + membership/equivalence queries -> classification tree + symbolic suffixes -> canonical RA hypothesis -> counterexample analysis -> refined RA
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. data languages 与 theory `⟨D,R⟩`；
2. register automata (`RA`)；
3. symbolic suffixes 与 tree queries；
4. classification tree；
5. `SLλ / SL* / SLCT` 三条学习路线对比。

### 核心抽象

论文首先把数据语言放在理论参数化框架中：

$$
\langle D, R \rangle
$$

上式中的符号逐项解释如下：

1. `$D$` 是通常无限的数据域。
2. `$R$` 是定义在 `$D$` 上的一组关系，可包含等号、不等号或更丰富关系。
3. 整个学习任务围绕“仅依赖这些关系可区分的数据语言”展开。

论文采用的 `RA` 定义是：

$$
A = (L, l_0, X, \Gamma, \lambda)
$$

上式中的符号逐项解释如下：

1. `$L$` 是有限的 location 集合。
2. `$l_0$` 是初始 location。
3. `$X$` 为每个 location 指派一组 registers。
4. `$\Gamma$` 是形如 `$\langle l, \alpha(p), g, \pi, l' \rangle$` 的转移集合。
5. `$\lambda$` 把 location 标成接受或拒绝。

对某个前缀 `$u$` 与 symbolic suffix `$v$`，论文把 tree query 的结果写成：

$$
L[u,v](d,p)=+ \iff u\alpha_1'(p_1)\cdots\alpha_m'(p_m)\in L
$$

上式中的符号逐项解释如下：

1. `$u$` 是已有数据前缀。
2. `$v=\alpha_1'(p_1)\cdots\alpha_m'(p_m)$` 是带参数的 symbolic suffix。
3. `$d$` 是前缀中的数据值，`$p$` 是 suffix 参数取值。
4. `L[u,v]` 不直接是 automaton，而是一个描述“继续接这个 suffix 时语言如何响应”的 decision tree。

classification tree 中最关键的等价关系是：

$$
u \equiv_V u' \iff \forall v \in V,\; L[u,v] \equiv L[u',v]
$$

上式中的符号逐项解释如下：

1. `$V$` 是当前维护的 symbolic suffix 集合。
2. 若两个前缀对所有 suffix 都等价，就可把它们放进同一 location 候选类。
3. `SLλ` 的 classification tree 正是用这些等价类来组织 hypothesis。

论文还把学习所需的数据结构压成三组集合：

$$
(Sp, U, V)
$$

上式中的符号逐项解释如下：

1. `$Sp$` 是 short prefixes，对应候选 locations。
2. `$U$` 是 `$Sp$` 及其一符号扩展，对应候选 transitions。
3. `$V$` 是 suffix-closed symbolic suffix 集合。
4. classification tree 则负责把 `$U$` 按 `$V$` 给出的区分能力分成等价类。

### 一个最小例子与通俗解释

论文用 `stack` 风格语言做示例。最典型的片段是：

1. 先执行 `push(0)`。
2. 再执行 `push(1)`。
3. 若后面接 `pop(1)`，该词属于语言。
4. 若后面接 `pop(2)`，则不属于语言。

这说明学习器不能只区分“现在在第几个离散状态”，还必须知道“当前是否记住了之前的某个数据值，以及 suffix 参数是否与它相等”。`SLλ` 的 tree query 就是在用少量但足够区分的 suffix，把这些依赖关系显式挖出来。

### 运行 / 接受 / 转移语义

论文给出的 `RA` 一步运行语义是：

$$
\langle l,\mu \rangle \xrightarrow{\alpha(d)} \langle l',\mu' \rangle
$$

上式中的符号逐项解释如下：

1. `$\langle l,\mu \rangle$` 是当前 location 与 register valuation。
2. `$\alpha(d)$` 是带数据值的输入符号。
3. 若存在转移 `$\langle l,\alpha(p),g,\pi,l' \rangle$` 且 guard 被满足，则该步可执行。
4. 新 valuation `$\mu'$` 按 assignment `$\pi$` 由旧 registers 或新参数 `$d$` 更新。

论文强调 `SLλ` 会生成 `determinate` 但未必完全 deterministic 的 `RA`。与 `SL*` 相比，它把主要改进放在：

1. 用 classification tree 代替 observation table；
2. 用 incrementally constructed short suffixes 代替大量长 suffix；
3. 用 restricted suffixes 降低一次 tree query 需要实际触发的 membership queries 数量；
4. 用更细的 counterexample analysis 决定是扩 short prefix 还是补新 suffix。

### 语义边界

这篇论文的边界比较清楚：

1. 主体是 `RA` 学习方法，不是 richer `EFSM` 全谱系统一框架。
2. 论文核心依赖可查询 `SUL`，不是从自然语言需求正向生成模型。
3. restricted suffix 的具体构造依赖 theory，本论文实现重点是 `⟨N,\{=\}\rangle`。
4. 更一般的数据理论和更复杂输入输出对象仍需额外工程化工作。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 理论参数化 | `$\langle D, R \rangle$` | 学习对象是受关系 `$R$` 约束的数据语言。 |
| `RA` 元组 | `$A = (L, l_0, X, \Gamma, \lambda)$` | 论文明确采用的目标模型族。 |
| tree query 语义 | `$L[u,v](d,p)=+ \iff u\alpha_1'(p_1)\cdots\alpha_m'(p_m)\in L$` | 说明 suffix 测试如何承载学习信息。 |
| 前缀等价 | `$u \equiv_V u' \iff \forall v \in V,\; L[u,v] \equiv L[u',v]$` | classification tree 的分裂依据。 |
| 复杂度主结论 | `$O(t)$` equivalence queries | 论文明确给出 `SLλ` 在 equivalence-query 数量上优于 `SL*` 的理论界。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 目标就是恢复 canonical `RA` locations。 |
| 事件 / 触发 | 很强 | 输入由 action + data symbol 构成。 |
| 守卫 / 数据 | 很强 | guards、registers、suffix 参数依赖是主轴。 |
| 层次 | 不支持 | 不面向 hierarchical state machines。 |
| 并发 / 同步 | 弱支持 | 论文主线是单组件黑盒学习。 |
| 时间约束 | 不支持 | 不是 timed-learning 路线。 |
| 连续动态 / 随机性 | 不支持 | 纯离散数据语言学习。 |
| 可执行 / 可验证性 | 很强 | 已在 `RALib` 实现并有公开 benchmark / artifact。 |

### 形式化问题与性质

1. 论文真正解决的是“如何让 `RA` 学习少做无效 suffix 测试”。
2. classification tree 让 location 区分不再强依赖宽 observation table。
3. restricted symbolic suffixes 是最关键的工程化提速点之一。
4. `SLλ` 对 `SL*` 的改进，不只是实现优化，而是数据结构和反例处理策略的整体替换。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 可执行 `membership/equivalence query` 的 `SUL`；
2. data words；
3. theory `⟨D,R⟩`；
4. `RALib` 中的学习与测试基础设施。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `RA` tuples；
2. symbolic suffixes；
3. `(u,v)`-trees；
4. classification tree；
5. short-prefix / one-symbol-extension / suffix-closed 三组集合。

### 交换与互操作

这篇论文的互操作重点不在文件格式，而在学习流程接口：

1. 黑盒部分通过 `MQ/EQ` 与 `SUL` 交互。
2. `RALib` 提供实验基座与对比实现。
3. benchmark 与 artifact 让不同 learning route 可以在同一实验管线里比较。

## 配套基础设施

- 建模/编辑工具：不是图形编辑器，主线是 `RALib` 学习框架与 benchmark 管线。
- 解析/交换/元模型支持：data words、`RA` 元组、symbolic suffixes 与 classification tree。
- 仿真/执行支持：通过 `membership/equivalence queries` 与 `SUL` 交互，并在 white-box setup 中借助 model checker 找短 counterexample。
- 验证/分析支持：counterexample analysis、restricted suffix construction、`SL* / SLCT / SLλ` 对比评测。
- 代码生成/转换支持：不以部署代码生成见长，重点是从交互行为恢复结构化 `RA` 模型。
- 标准化或社区生态：`RALib`、`LearnLib` 相关生态、Zenodo artifact 与 GitHub benchmarking。

## 适用场景与需求前提

### 适用场景

适合带数据参数的协议、API、库接口和实现行为恢复，尤其适合希望把黑盒系统抽成 `RA/EFSM` 风格模型再做验证、对照或回归分析的场景。

### 需求前提

1. 目标系统必须可执行 `membership/equivalence` 风格查询。
2. 关键行为需能压成 data words。
3. 若要获得文中最强评测效果，最好能接入 `RALib` 和较强的 counterexample 发现器。
4. 数据理论最好能落在论文支持或易扩展的关系框架里。

### 不适用或高成本场景

若系统数据理论过于复杂、不可复位、无法稳定查询，或者目标是 timed / hybrid / stochastic 模型学习，`SLλ` 不是直接解法。

## 与相邻形式主义的关系

相对 [combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md](../combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md)，本文更聚焦纯 learning pipeline 的可扩展化，而不是把 white-box 信息并入学习；相对 [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)，`LearnLib` 更像通用 learning 基础设施，而本文是 `RA` 场景下的具体高性能方法；相对 [libalf-the-automata-learning-framework/desc.md](../libalf-the-automata-learning-framework/desc.md)，`libalf` 提供较早的学习框架底座，本文则展示 dataful `RA` 学习如何在现代 benchmark 上进一步扩展。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明需求生成之外，仍可通过主动学习从实现或原型恢复状态机，用来交叉校验 LLM 生成模型。
2. 对带变量、带参数守卫的控制逻辑，这条路线比纯 `DFA/Mealy` 学习更接近真实工程对象。
3. classification tree、短 suffix 与反例分析的分层设计，也很适合迁移到“生成 - 验证 - 修复”闭环中的修复侧证据收集。

### 作为目标形式主义还是中间表示

更适合作为行为恢复、对照验证和模型修复的中间表示，而不是控制工程师直接手写的前端语言。

### 对需求到模型生成的启发

1. 若正向生成的状态机含数据守卫，后续修正不能只看离散结构，还要考虑寄存器与 guard 的可学习性。
2. 结构化反例分析比单纯追加更多测试更有效。
3. 数据型状态机的闭环构建，很适合把 query-based evidence 当成独立证据层。

## 重要的相关工作

1. [combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md](../combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md)：`RA` 学习中引入 white-box 辅助的路线。
2. [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)：更通用的主动自动机学习基础设施。
3. [libalf-the-automata-learning-framework/desc.md](../libalf-the-automata-learning-framework/desc.md)：更早的 online/offline 自动机学习框架底座。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`register automata learning / SLλ / classification-tree and restricted-suffix route`
- 论文角色：tree-based register-automata learning method / scalable active-learning route for data languages
- 归类理由：论文主体是 `RA` 学习算法、suffix 选择策略与 counterexample 分析方法，核心贡献属于方法路线而不是新的标准或工具平台本体。

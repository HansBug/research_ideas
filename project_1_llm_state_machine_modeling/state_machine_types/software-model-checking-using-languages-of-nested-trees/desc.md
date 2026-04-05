# 使用嵌套树语言的软件模型检验 / Software Model Checking Using Languages of Nested Trees

## 基本信息

- 标题：Software Model Checking Using Languages of Nested Trees
- 中文标题：使用嵌套树语言的软件模型检验
- 作者：Rajeev Alur、Swarat Chaudhuri、P. Madhusudan
- 发表：*ACM Transactions on Programming Languages and Systems*, 33(5), Article 15, 2011
- DOI：`10.1145/2039346.2039347`
- 链接：https://www.cs.utexas.edu/~swarat/pubs/toplas11.pdf
- 形式主义：`Nested State Machines (NSM)`，以及其 branching-time semantics `Nested Trees`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / `NSM` family 稳定锚点
- 工具/实现获取方式：原文未提供独立工程实现；机器可处理入口是 `NSM` 的 `V_{loc}/V_{call}/V_{ret}` tuple、nested-tree unfolding、bounded summaries、`AP-NTA` 与 `NT-μ`。
- 标准/格式获取方式：原文没有 DSL、XML 或交换标准；核心承载方式是 `NSM` tuple、execution tree / unfolding 与 automata / fixpoint semantics。

## 简报

这篇 `TOPLAS` 论文是当前这一轮最关键的 `NSM` 主锚点。相较于前面的 conference / lecture-note 条目，它把 `Nested State Machine` 明确细分成 `V_{loc}`、`V_{call}`、`V_{ret}` 三类状态，并把 branching semantics、bounded summaries、`NT-μ` 与 nested-tree automata 全部系统化，因此足以作为 `RSM -> NSM` 侧枝的正式 journal-level family definition。

- 形式主义定位：`RSM` 的 nested-structure semantic sibling，用 `NSM` 统一递归控制流与 stack-sensitive branching semantics。
- 构造方式简述：把程序控制点分类成 local / call / return states，用三类迁移组成 `NSM`，再把 unfolding 定义成 nested tree。
- 基础设施与场景简述：原文没有工程标准，但它把 `NSM`、nested trees、`NT-μ` 与 `AP-NTA` 放在一个闭环里，说明这不是零散的辅助概念，而是一个完整 family。

```text
recursive program -> NSM(Vloc/Vcall/Vret) -> nested-tree unfolding -> bounded summaries -> NT-μ / AP-NTA model checking
```

## 形式主义定义与核心对象

### 定义对象

原文把 `NSM` 定义成“用于递归程序的状态机抽象”，并强调其 branching semantics 直接是 nested tree，而不是 stack configuration graph。

### 核心抽象

论文给出的正式定义是：

$$
M = \langle V_{loc}, V_{call}, V_{ret}, v_{in}, \kappa, \Delta_{loc}, \Delta_{call}, \Delta_{ret} \rangle
$$

上式中的符号逐项解释如下：

1. `V_{loc}` 是 local states 集合。
2. `V_{call}` 是 call states 集合。
3. `V_{ret}` 是 return states 集合。
4. `v_{in}` 是初始状态。
5. `\kappa : V \to 2^{AP}` 给状态赋可观察原子命题。
6. `\Delta_{loc} \subseteq (V_{loc}\cup V_{ret}) \times (V_{loc}\cup V_{call})` 是局部迁移。
7. `\Delta_{call} \subseteq V_{call} \times (V_{loc}\cup V_{call})` 是调用迁移。
8. `\Delta_{ret} \subseteq (V_{loc}\cup V_{ret}) \times V_{call} \times V_{ret}` 是返回迁移。

与 earlier `RSM` 定义相比，这里最关键的变化是：

1. 状态先按 control-flow role 被分型；
2. 返回迁移显式依赖上一次未匹配调用的 call state；
3. family 的自然语义对象是 unfolding `T(M)`。

### 一个最小例子与通俗解释

论文用 `foo()` 递归过程给出一个很典型的 `NSM`：

1. `v_2` 是唯一的 call state。
2. `v_2'` 是唯一的 return state。
3. `\Delta_{call} = \{(v_2,v_1)\}` 表示从 `v_2` 调入下层过程。
4. `\Delta_{ret} = \{(v_5,v_2,v_2')\}` 表示过程结束时依据最近未匹配调用 `v_2` 返回到 `v_2'`。

通俗地说，`NSM` 像“给递归程序画一张状态机图，但每个状态先声明自己到底是普通控制点、调用点还是返回点”。然后程序的分支执行树不再只是普通树，而是会自动长出 call-to-return 的 jump-edges。

### 运行 / 接受 / 转移语义

论文把 branching-time semantics 定义为 execution tree：

$$
T_V(M) = (T,\rightsquigarrow,\lambda)
$$

上式中的符号逐项解释如下：

1. `T` 是 `NSM` 展开的树形控制骨架。
2. `\rightsquigarrow` 把 call 节点与其 matching return 节点连接起来。
3. `\lambda` 给每个节点标一个 `NSM` 状态。

再经观测映射得到最终 unfolding：

$$
T(M) = (T,\rightsquigarrow,\lambda')
$$

其中 `\lambda'(s)=\kappa(\lambda(s))`，也就是把状态投影到原子命题。

论文后续模型检验所依赖的 bounded summary 则可整理成：

$$
\langle u,u',V_1,\ldots,V_k \rangle
$$

这里：

1. `u` 是当前根节点对应的 `NSM` 状态。
2. `u'` 是 unmatched call ancestor 对应的状态，若不存在则为空标记。
3. `V_1,\ldots,V_k` 是与公式自由变量相关的节点集合摘要。

### 语义边界

这篇论文对 `NSM` 的边界比早期条目更清楚：

1. 目标是 recursive sequential programs，不考虑并发模块。
2. 模型重点在 call / return 结构，不处理时间、概率或连续动态。
3. `NSM` 与 pushdown / `RSM` 同属同一家族，但语义入口不同。
4. 一旦需要 finite-data variables，应再往 `ERSM` 方向扩展，而不是继续留在这里。

### 关键性质与判定边界

论文给出的核心结论是：

$$
\mathrm{MC}_{NT\text{-}\mu}(M,\varphi)\ \text{is EXPTIME-complete}
$$

以及：

$$
\mathrm{MC}_{AP\text{-}NTA}(M,A)\ \text{is EXPTIME-complete}
$$

上式中的符号逐项解释如下：

1. `M` 是一个 `NSM`。
2. `\varphi` 是 nested-tree 上的 `NT-μ` 公式。
3. `A` 是 alternating parity nested tree automaton。
4. 两个结论都说明 `NSM` family 的核心规范体系仍保持经典的 `EXPTIME` 可判定性。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 明确区分 `V_{loc}`、`V_{call}`、`V_{ret}`。 |
| 事件 / 触发 | 中等支持 | 更强调 control-flow role 和边类型。 |
| 守卫 / 数据 | 不支持 | 不处理有限变量赋值。 |
| 层次 | 强支持 | call / return 嵌套直接进入语义。 |
| 并发 / 同步 | 不支持 | 目标是 sequential recursion。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | bounded summaries、`NT-μ`、`AP-NTA` 一套齐全。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `NSM` 元组 | `$M = \langle V_{loc}, V_{call}, V_{ret}, v_{in}, \kappa, \Delta_{loc}, \Delta_{call}, \Delta_{ret} \rangle$` | family 的正式 journal 定义。 |
| execution tree | `$T_V(M)=(T,\rightsquigarrow,\lambda)$` | branching semantics。 |
| unfolding | `$T(M)=(T,\rightsquigarrow,\lambda')$` | 观测投影后的最终语义对象。 |
| bounded summary | `$\langle u,u',V_1,\ldots,V_k\rangle$` | syntax-directed symbolic algorithm 的核心摘要对象。 |
| 复杂度 | `$\mathrm{EXPTIME}$-complete` | `NSM` 上主要规范体系的统一边界。 |

## 构造方式与承载格式

### 建模入口

1. 先把程序控制点分成 local / call / return 三类。
2. 用三类迁移关系连接这些控制点。
3. 再自动生成 nested-tree unfolding。
4. 在 unfolding 上运行 `NT-μ` 或 `AP-NTA`。

### 机器可处理承载方式

机器可处理承载方式主要是：

1. `NSM` tuple；
2. execution tree / unfolding；
3. bounded summaries；
4. `NT-μ` 与 `AP-NTA`。

### 交换与互操作

它与当前文库的互操作关系如下：

1. 上游是 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM`。
2. sibling 是 [languages-of-nested-trees/desc.md](../languages-of-nested-trees/desc.md) 的 conference-origin nested-tree family。
3. 若进一步加入 finite-data 程序抽象，则自然接到 [model-checking-procedural-programs/desc.md](../model-checking-procedural-programs/desc.md) 的 `ERSM`。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `NSM` tuple 与 nested-tree summaries。
- 仿真/执行支持：execution tree / unfolding 给出精确 branching semantics。
- 验证/分析支持：`NT-μ`、`AP-NTA`、bisimulation、bounded-summary symbolic algorithm。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：理论 family，适合做验证中间表示，不是工程标准语言。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归过程控制流的 branching-time 语义建模。
2. 需要 stack-sensitive temporal specifications 的程序分析。
3. 需要给 `RSM` 主线补一个更偏语义对象的 sibling 节点。

### 需求前提

1. 系统本质是顺序递归控制流。
2. 需求想直接指向 matching returns、current context、caller-sensitive properties。
3. 不需要并发、时间或概率扩展。

### 不适用或高成本场景

若系统主要难点在并发递归交互，应转到 `CRSM` 或 `RGG`；若重点在有限数据赋值，应考虑 `ERSM`；若只是普通 `RSM` reachability，则没必要额外转成 `NSM`。

## 与相邻形式主义的关系

相对 `RSM`，`NSM` 把 call / return stack semantics 重新表述成 nested-tree semantics；相对 `HSM / uHSM`，它更靠近真实递归程序控制流；相对 `nested tree automata`，它是生成这些 semantic objects 的程序模型本体。

## 与本研究的关系

### 对 Project 1 的价值

它使当前 `Statecharts -> HSM -> uHSM -> RSM` 理论线能继续自然长出一条新的 semantic side-branch：`NSM`。这为后续“生成状态机后如何做上下文相关验证”提供了更合适的语义容器。

### 作为目标形式主义还是中间表示

显然更适合作为验证 / 分析阶段的中间表示，而不是需求建模前端。

### 对需求到模型生成的启发

如果需求里反复出现“在当前过程上下文中终将满足”“调用前条件在返回后必须兑现”这类 stack-sensitive 约束，LLM 生成的控制流模型后续可自动规范化到 `NSM`，再进入 nested-tree verification 流程。

## 重要的相关工作

1. [logics-and-automata-for-software-model-checking/desc.md](../logics-and-automata-for-software-model-checking/desc.md)：更早的讲义型语义入口。
2. [languages-of-nested-trees/desc.md](../languages-of-nested-trees/desc.md)：给出该 family 的 conference-origin nested-tree language / automaton 结果。
3. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：作为 `NSM` 最近的上游递归状态机主干。

## 文献分类总结

- 这篇文献应作为当前文库里 `NSM` 节点的首选主锚点。
- 它最大的增量，不是又加了一个逻辑，而是把 `NSM` 作为独立程序抽象写稳了。
- 后续若在演化树中只保留一个 `NSM` 年份标记，优先应取本文的 `2011` journal full version，并把 `2006` conference / notes 作为旁证。
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论

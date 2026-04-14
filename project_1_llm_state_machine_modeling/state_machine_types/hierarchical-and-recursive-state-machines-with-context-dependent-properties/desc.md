# 带上下文相关性质的层次与递归状态机 / Hierarchical and Recursive State Machines with Context-Dependent Properties

## 基本信息

- 标题：Hierarchical and Recursive State Machines with Context-Dependent Properties
- 中文标题：带上下文相关性质的层次与递归状态机
- 作者：Salvatore La Torre, Margherita Napoli, Mimmo Parente, Gennaro Parlato
- 发表：*Automata, Languages and Programming*, pp. 776-789, 2003
- DOI：`10.1007/3-540-45061-0_61`
- 链接：https://www.southampton.ac.uk/~gp1y10/papers/crsm-icalp03.pdf
- 形式主义：`Context-Dependent Hierarchical / Recursive State Machines (CDHSM / CDRSM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `CRSM` 元组、`expand` / `expand^+`、`true` 标注函数、flat state tuple `[u_1,\ldots,u_m]` 与 `LTL` model-checking reduction。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 graph collection、supernode expansion、context-dependent labeling 与 flat semantics。

## 简报

这篇论文做的增强非常具体，但对谱系很重要：它不改变 `HSM/RSM` 的基本控制骨架，而是允许 atomic propositions 贴在 supernodes 上，从而让“在不同上下文里看到的性质”直接进入模型本体，而不必先完全 flatten 再打标签。作者因此得到两类模型：非递归的 context-dependent hierarchical state machines，以及递归的 context-dependent recursive state machines。它们不是另一个 DSL，而是对 `HSM/RSM` 的语义压缩增强。

- 形式主义定位：`HSM` 与 `RSM` 的 context-dependent labeling 扩展，用更紧凑的层次标注来表达 flat state 上的组合性质。
- 构造方式简述：组件图仍由 nodes / supernodes 组成，但增加 `true` 标签函数，并要求祖先上下文标签满足不冲突约束。
- 基础设施与场景简述：原文纯理论，但同时覆盖 reachability、cycle detection 与 `LTL` model checking，并给出 `CHSM` 与 `CRSM` 两个子族。

```text
层次 / 递归控制图 -> supernode labels + context-sensitive truth assignment -> flat tuple states -> reachability / LTL checking
```

## 形式主义定义与核心对象

### 定义对象

原文从 Kripke-style graph collection 出发，扩展点不是新的控制结构，而是“性质标签不再只能贴在 basic nodes 上”。为了避免和 [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md) 的 `CHSM` 缩写冲突，本文库用 `CDHSM` 指代 context-dependent hierarchical state machines，用 `CDRSM` 指代 context-dependent recursive state machines。

### 核心抽象

原文把 context-dependent recursive state machine 写成：

$$
M = (M_1,\ldots,M_k)
$$

并给出如下组成部分：

$$
\bigl(N,\ IN,\ OUT,\ expand,\ E_i,\ true\bigr)
$$

上式中的符号逐项解释如下：

1. `N = N_1 \cup \cdots \cup N_k` 是所有顶点集合。
2. `IN = \{in_1,\ldots,in_k\}` 是各组件初始顶点。
3. `OUT = OUT_1 \cup \cdots \cup OUT_k` 是输出顶点集合。
4. `expand : N \to \{0,1,\ldots,k\}` 指定某个顶点是否展开成另一个组件；`expand(u)=0` 表示 basic node。
5. `E_i` 是第 `i` 个组件的边集。
6. `true : N \to 2^{AP}` 给每个节点或 supernode 贴上 atomic propositions。

原文还要求一个上下文一致性条件：

$$
true(u) \cap true(v) = \varnothing
$$

当 `v \in N_h`、`u \notin N_h` 且 `h \in expand^+(u)` 时成立。直观上，这表示祖先上下文与内部组件的标签不会在同一个 proposition 上冲突。

### 一个最小例子与通俗解释

论文直接用 digital clock 举例。若只用传统 `HSM`，最底层状态可能只能知道“现在是第几秒”；但若想让 flat state 同时带上“当前小时 / 当前分钟 / 当前秒”，普通层次结构往往要靠展开后再打标签。`CDHSM` 则允许：

1. 小时 supernode 自己带有“当前小时”标签；
2. 分钟 supernode 自己带有“当前分钟”标签；
3. 最底层秒节点带有“当前秒”标签；
4. flat state 的命题集合就是这些上下文标签的并集。

通俗地说，`CDHSM/CDRSM` 像“允许大状态把自己的语义标签一并带进展开后状态里”的层次状态机。

### 运行 / 接受 / 转移语义

原文的 flat machine `M^F` 的状态写成：

$$
X = [u_1,\ldots,u_m]
$$

上式中的符号逐项解释如下：

1. `u_1` 是顶层组件中的节点。
2. 若 `u_j` 是 supernode，则 `u_{j+1}` 必须属于 `expand(u_j)` 指向的组件。
3. `u_m` 必须是 basic node，也就是 `expand(u_m)=0`。

flat state 的标签定义为：

$$
true(X) = \bigcup_{j=1}^{m} true(u_j)
$$

这正是 context-dependent property 的核心。相应地，整机语言可写成：

$$
L(M) = \mathrm{Traces}(M^F)
$$

对非递归子类，原文定义 `CDHSM` 只需额外要求：

$$
expand(u) < i \quad \text{for every } u \in N_i
$$

也就是展开必须朝更低层走，不能回到自己或更高层；而 `CDRSM` 则允许递归展开。

### 语义边界

这个 family 的边界很明确：

1. 它没有增加并发、时间或数据变量。
2. 它保留 `HSM/RSM` 的控制骨架，只增强 labeling semantics。
3. `CDHSM` 是非递归子类，`CDRSM` 是递归全类。
4. 它的价值主要是“用更短的模型表达本来要 flatten 后才能写清的性质”。

### 关键性质与判定边界

原文给出的代表性结论包括：

$$
\mathrm{Reachability}(\mathrm{CDRSM}),\ \mathrm{CycleDetection}(\mathrm{CDRSM})
$$

都是 `NP`-complete，而对 `CDHSM` 也已具有 `NP`-hardness。

对 `LTL`，论文给出：

$$
\mathrm{MC}_{LTL}(\mathrm{CDRSM},\varphi) = O(|M| \cdot 16^{|\varphi|})
$$

若 `M` 是 `CDHSM`，则可进一步降到：

$$
\mathrm{MC}_{LTL}(\mathrm{CDHSM},\varphi) = O(|M| \cdot 8^{|\varphi|})
$$

这说明 context-dependent labeling 虽然让 reachability / cycle detection 变难，但对 `LTL` 仍然可以保持标准 automata-theoretic 路线。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | nodes + supernodes。 |
| 事件 / 触发 | 弱支持 | 以 graph transitions 为主。 |
| 守卫 / 数据 | 不支持 | 原文重点不是变量。 |
| 层次 | 强支持 | `CDHSM` 是非递归层次子类。 |
| 并发 / 同步 | 不支持 | 明确是 sequential。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | reachability / cycle detection / `LTL` 全覆盖。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 家族总元组 | `$M=(M_1,\ldots,M_k)$` | context-dependent family 的组件集合。 |
| expand 映射 | `$expand:N\to\{0,\ldots,k\}$` | 指定 supernode 展开结构。 |
| 上下文标签 | `$true:N\to 2^{AP}$` | 允许 supernode 携带性质标签。 |
| flat state | `$X=[u_1,\ldots,u_m]$` | 上下文链 + basic node。 |
| flat label | `$true(X)=\bigcup_{j=1}^m true(u_j)$` | context-dependent property 的核心。 |

## 构造方式与承载格式

### 建模入口

1. 先按 `HSM/RSM` 方式定义 graph collection 和 `expand` 关系。
2. 再决定哪些命题适合贴在 supernodes 上，而不是 basic nodes 上。
3. 最后检查上下文标签冲突条件是否满足。

### 机器可处理承载方式

机器可处理承载方式主要是：

1. graph collection；
2. `expand / expand^+`；
3. `true` labeling；
4. flat-state tuple `[u_1,\ldots,u_m]`。

### 交换与互操作

它与现有谱系的关系非常直接：

1. 非递归版本承接 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)。
2. 递归版本承接 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `expand` 与 `true` 的上下文语义。
- 仿真/执行支持：可通过 `M^F` 直接解释。
- 验证/分析支持：reachability、cycle detection、`LTL` model checking。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要价值在谱系和复杂度边界。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要在层次上下文上直接携带语义标签的控制模型。
2. 需要比较“flatten 后打标签”和“层次中直接打标签”的 succinctness。
3. 需要在 `HSM/RSM` 支线上继续精细化语义。

### 需求前提

1. 系统仍是 sequential hierarchy / recursion。
2. 关心的性质可以写成原子命题标签，而不是复杂变量公式。
3. 允许上下文标签按祖先链并集传播。

### 不适用或高成本场景

如果需求需要并发同步 product，就不是这条 context-dependent line 的目标；如果只是 plain hierarchy 且不需要 supernode labeling，则普通 `HSM/RSM` 更简单。

## 与相邻形式主义的关系

相对 `HSM`，`CDHSM` 允许 supernode 标签直接参与 flat-state 语义；相对 `RSM`，`CDRSM` 允许同样的上下文标签机制进入递归 call stack；相对 `CHSM`，这里的 `CDHSM` 不是 communicating hierarchical machines，而是 context-dependent hierarchical machines。

## 与本研究的关系

### 对 Project 1 的价值

它让层次状态机支线不只是一棵“控制结构树”，还开始显式吸收“性质标签如何沿层次传播”的语义问题，这对后续从需求生成形式模型很有启发。

### 作为目标形式主义还是中间表示

更适合作为理论中间表示和演化树节点，不适合作为工程团队直接维护的主语言。

### 对需求到模型生成的启发

如果需求文本里反复出现“只要系统处在某个大模式下，就整体满足某类性质”的描述，LLM 可以考虑是否该生成带 context-dependent labeling 的层次模型，而不是把这些性质全部推到最叶子节点。

### 现实限制

它的工程落地生态很弱，而且 reachability / cycle detection 已经上升到 `NP`-complete，不适合直接当工程工具语言。

## 重要的相关工作

### 奠基或前身工作

- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)
- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)

### 同类型或同家族工作

- `Verification of scope-dependent hierarchical state machines`：后续更成熟的 journal 版本。
- [communicating-hierarchical-state-machines/desc.md](../communicating-hierarchical-state-machines/desc.md)：另一条“并发扩展”而非“标签扩展”路线。

## 文献分类总结

- 这篇论文对应层次状态机支线里的 context-dependent semantic extension。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL 或应用。
- 在演化树里，它同时为 `HSM` 和 `RSM` 两条线提供了 2003 年的上下文语义后继。

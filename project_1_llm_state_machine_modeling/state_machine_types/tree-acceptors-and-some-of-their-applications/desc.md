# 树接受器及其若干应用 / Tree Acceptors and Some of Their Applications

## 基本信息

- 标题：Tree Acceptors and Some of Their Applications
- 中文标题：树接受器及其若干应用
- 作者：John Doner
- 发表：*Journal of Computer and System Sciences*, 4(5):406-451, 1970
- DOI：`10.1016/S0022-0000(70)80041-1`
- 链接：https://doi.org/10.1016/S0022-0000(70)80041-1
- 形式主义：`Tree Acceptors`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 deterministic / nondeterministic tree acceptor、state tree 和 recognizable sets。
- 标准/格式获取方式：原文没有工程交换标准，核心承载方式是树递归、转移函数 `t`、designated states 和 frontier / yield 操作。

## 简报

这篇论文把 ordinary finite automata 正式推广成“输入对象是树”的 `tree acceptors`，并围绕 `recognizable sets` 给出布尔闭包、确定化、空性判定、regular sets 与 context-free languages 的新刻画，以及 monadic second-order logic 上的应用。对当前演化树而言，它正好把 `Tree Automata` 母节点向前补回 1970 年代的更早 `Tree Acceptors` 锚点。

- 形式主义定位：`Finite Automata` 向有限树识别推广后的早期经典母型。
- 构造方式简述：用二叉树递归自底向上计算每个子树状态，根状态落入 `D` 时接受。
- 基础设施与场景简述：原文是纯理论工作，但 recognizable sets、subset construction、emptiness 和 frontier/yield 刻画都非常适合做树自动机谱系的上游节点。

```text
有限树 / 项结构 -> tree acceptor 自底向上求状态 -> recognizable set -> regular / context-free / logic characterization
```

## 形式主义定义与核心对象

### 定义对象

输入对象是 `\Sigma`-trees，而不是线性词。论文先定义树域和 `\Sigma`-tree，再定义 deterministic 与 nondeterministic tree acceptors 及其接受语言 `T(\mathcal A)`。

### 核心抽象

对二叉情形，原文 Definition 1.2 给出的 deterministic tree acceptor 是：

$$
\mathcal A = (S,t,s_0,D)
$$

上式中的符号逐项解释如下：

1. `S` 是非空有限状态集。
2. `t : S \times S \times \Sigma \to S` 是转移函数，把左右子树状态和当前节点标签规约成父节点状态。
3. `s_0 \in S` 是初始状态，负责空树 / 叶边界处的初值。
4. `D \subseteq S` 是 designated states。

与 `\mathcal A` 关联的树求值函数 `f : \Sigma^\# \to S` 满足：

$$
f(\Lambda)=s_0
$$

$$
f(\sigma[\tau,\tau']) = t(f(\tau),f(\tau'),\sigma)
$$

接受语言定义为：

$$
T(\mathcal A)=\{\tau\in \Sigma^\# \mid f(\tau)\in D\}
$$

这里 `\Lambda` 表示空树/边界对象，`\sigma[\tau,\tau']` 表示以 `\sigma` 为根、左右子树分别为 `\tau,\tau'` 的树。

### 一个最小例子与通俗解释

一个最小例子是“只接受所有叶边界都正常、且内部节点都标成 `a` 的二叉树”。可取 `S=\{ok,bad\}`，令 `s_0=ok`，并定义：

$$
t(ok,ok,a)=ok,\quad t(s,s',\sigma)=bad\ \text{otherwise}
$$

再取 `D=\{ok\}`。这样自底向上看，只要某个子树已经 `bad`，或者当前节点不是允许的 `a` 结构，父节点就变成 `bad`，最终根状态是 `ok` 才接受。

通俗地说，tree acceptor 就像“把普通自动机从沿字符串向右走，改成沿树从叶子往根折叠”。每棵子树先被压成一个状态，父节点再根据两个子状态和自己的标签算出新状态。

### 运行 / 接受 / 转移语义

原文还定义了与输入树兼容的 state tree。若 `\tau` 是输入树，`\pi` 是状态树，则对每个节点 `w` 有：

$$
\pi(w)=f(\tau\mid w)
$$

其中 `\tau\mid w` 是 `w` 处子树。Lemma 1.4 说明：

$$
\tau \in T(\mathcal A) \iff \pi(\Lambda)\in D
$$

这表示接受只看根节点最终算出的状态是否落在 `D`。

### 语义边界

当树的 order 退化为 1 时，tree acceptor 就可与 ordinary finite automaton 对齐，因此普通自动机理论是 tree acceptor 理论的特例。相反，它仍只处理有限树，不处理 Rabin 式 infinite-tree acceptance。

### 关键性质与判定边界

论文给出几条非常适合挂树的核心结论：

$$
\mathrm{Rec}_\Sigma \text{ is closed under } \cup,\ \cap,\ \setminus
$$

$$
\forall \mathcal A_{\mathrm{nd}},\ \exists \mathcal A_{\mathrm{det}},\ T(\mathcal A_{\mathrm{nd}})=T(\mathcal A_{\mathrm{det}})
$$

$$
\text{Emptiness}(T(\mathcal A)) \text{ is decidable}
$$

此外，论文还通过 frontier/yield 和 `Q(A)` 操作，把 recognizable tree sets 与 regular sets、context-free languages 建立联系。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态是每棵子树的归约类型。 |
| 事件 / 触发 | 不适用 | 输入是树节点结构而非事件流。 |
| 守卫 / 数据 | 不支持 | 原始模型没有一般变量守卫。 |
| 层次 | 强支持 | 层次直接来自树对象本体。 |
| 并发 / 同步 | 不支持 | 左右分支是结构递归，不是并发同步语义。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散有限树识别。 |
| 可执行 / 可验证性 | 强支持 | 确定化、布尔闭包、空性判定和逻辑应用都很清楚。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| tree acceptor 骨架 | `$\mathcal A=(S,t,s_0,D)$` | 早期树自动机母体定义。 |
| 自底向上求值 | `$f(\sigma[\tau,\tau'])=t(f(\tau),f(\tau'),\sigma)$` | 父状态由两个子状态和节点标签决定。 |
| 接受语言 | `$T(\mathcal A)=\{\tau\mid f(\tau)\in D\}$` | 根状态落入 designated set 时接受。 |
| 确定化 | `$T(\mathcal A_{\mathrm{nd}})=T(\mathcal A_{\mathrm{det}})$` | 子集构造在 tree acceptor 中仍成立。 |
| 空性判定 | `$\text{Emptiness}(T(\mathcal A))$ decidable` | recognizable tree sets 可有效分析。 |

## 构造方式与承载格式

### 建模入口

1. 明确输入对象是有限有序树，而不是线性 trace。
2. 设计有限状态集 `S` 和根接受集合 `D`。
3. 为每个节点标签和左右子状态组合定义转移函数 `t`。
4. 如需证明闭包或投影性质，可转到 nondeterministic tree acceptor 再做 subset construction。

### 机器可处理承载方式

机器可处理承载方式是树递归、状态转移表、state tree compatibility 和 recognizable-set 操作；没有 DSL、XML 或 JSON 标准。

### 交换与互操作

它和 [tree-automata/desc.md](../tree-automata/desc.md) 的后续 tree automata 母线、[decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md) 的树逻辑线，以及 context-free / regular characterization 直接相连。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是树递归定义与 recognizable-set 闭包构造。
- 仿真/执行支持：可按子树递归直接执行求值。
- 验证/分析支持：布尔闭包、确定化、空性判定和逻辑可判定性应用是原文重点。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是早期 tree automata / recognizable tree sets 理论的关键母体之一。

## 适用场景与需求前提

### 适用场景

适合有限树语言识别、语法树/项结构检查、regular tree sets、context-free yield characterization，以及把逻辑公式集合转成可识别树集合的理论任务。

### 需求前提

1. 对象必须显式是树。
2. 节点语义主要由有限个子树状态组合决定。
3. 不需要时间、数据守卫或连续动态。

### 不适用或高成本场景

若对象是 infinite trees、XML hedges、线性词流或含时钟/物理变量的控制模型，就应转向后续 infinite-tree / unranked / timed / hybrid 分支。

## 与相邻形式主义的关系

相对 [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)，它把线性词接受推广到有限树；相对 [tree-automata/desc.md](../tree-automata/desc.md)，本文更早、更接近 `Tree Acceptors` 原始命名；相对 [finite-tree-automata-on-infinite-trees/desc.md](../finite-tree-automata-on-infinite-trees/desc.md)，它仍停留在有限树与 recognizable sets。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata` 母支线向前补回到 1970 年的 `Tree Acceptors`，让演化树不再只从后期 monograph 起步。

### 作为目标形式主义还是中间表示

在“需求对象天然是树结构”的场景可以作为目标形式主义；对控制系统主线更常作为谱系母节点和中间抽象。

### 对需求到模型生成的启发

如果需求结构已经是“节点 + 子节点组合”，就不应先压平成字符串 `FSM`，而可以直接生成自底向上的 tree acceptor / tree automaton。

### 现实限制

原文没有现代工具链或交换格式，工程上更多需要后接 XML/tree grammar/term-processing 生态。

## 重要的相关工作

### 奠基或前身工作

- [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)
- `Mezei-Wright recognizable sets`

### 同类型或同家族工作

- [tree-automata/desc.md](../tree-automata/desc.md)
- [finite-tree-automata-on-infinite-trees/desc.md](../finite-tree-automata-on-infinite-trees/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线。

### 与本研究关系最紧的工作

- 它最适合挂成 `Tree Acceptors -> Tree Automata` 的早期母节点，并为后续 infinite-tree / unranked 树枝提供历史起点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Tree Acceptors`
- 论文角色：模型提出
- 核心功能：把 finite automata 推广到有限树接受器，并围绕 recognizable sets 建立闭包、确定化、空性判定和语言刻画。
- 关键特性：自底向上树求值、state tree compatibility、Boolean closure、subset construction、regular/CFL characterization。
- 构造方式：`(S,t,s_0,D)` + 递归求值函数 `f` + 根状态接受。
- 基础设施：纯理论模型，无工程标准/工具。
- 适用场景：有限树语言、语法树/项结构识别、recognizable tree sets 与逻辑应用。
- 需求前提：对象必须是树，且父节点语义由有限子树状态组合决定。
- 状态：🟢

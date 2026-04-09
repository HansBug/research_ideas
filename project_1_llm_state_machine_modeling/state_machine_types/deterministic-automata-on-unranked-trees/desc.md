# 非定秩树上的确定性自动机 / Deterministic Automata on Unranked Trees

## 基本信息

- 标题：Deterministic Automata on Unranked Trees
- 中文标题：非定秩树上的确定性自动机
- 作者：Julien Cristau, Christof Löding, Wolfgang Thomas
- 发表：Dagstuhl Seminar Proceedings 05061, 2005
- DOI：`10.4230/DagSemProc.05061.3`
- 链接：https://drops.dagstuhl.de/entities/document/10.4230/DagSemProc.05061.3
- 形式主义：Deterministic Unranked Tree Automata
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：分支整理
- 工具/实现获取方式：原文没有公开实现；机器可处理入口是 bottom-up deterministic automata `A=(Q,\Sigma,(D_a)_{a\in\Sigma},F)`、top-down `#DTA` 和最小化构造。
- 标准/格式获取方式：没有工程标准，核心承载方式是 vertical states `Q` 与 per-label horizontal DFA `D_a` 的二层 automaton 表示。

## 简报

这篇论文不是在 unranked tree automata 上再讲一遍“存在确定化”，而是认真定义了 **什么样的 deterministic bottom-up model 才适合最小化**，并给出 canonical minimal automaton；同时又把 deterministic top-down 路线分离出来，证明何时一个 regular unranked tree language 可以被 top-down deterministic 模型识别。对演化树而言，它正是 `unranked tree automata` 下最稳定的 deterministic 子枝。

- 形式主义定位：unranked tree automata 主干上的 deterministic refinement。
- 构造方式简述：用 vertical states 处理树根归约，用每个标签对应的 horizontal DFA 处理孩子状态串。
- 基础设施与场景简述：原文完全是理论工作，但 minimization、canonical representation 与 top-down decidability 都是非常稳的“可挂树”证据。

```text
unranked tree -> horizontal DFA 读孩子状态串 -> vertical state at node -> deterministic tree-language acceptance
```

## 形式主义定义与核心对象

### 定义对象

作者先回顾 nondeterministic bottom-up automata，再明确指出：若想让 deterministic model 在 unranked setting 中可最小化、可 canonical，就不能只靠“transition languages 两两不交”这种语义定义，而要改成“每个标签配一个 deterministic horizontal automaton”的显式结构。

### 核心抽象

论文给出的 bottom-up deterministic unranked tree automaton 可写成：

$$
A=(Q,\Sigma,(D_a)_{a\in\Sigma},F)
$$

其中每个 `D_a` 都是一个带输出的 deterministic finite automaton：

$$
D_a=(S_a,Q,s_a^{in},\delta_a,\lambda_a)
$$

上式中的符号逐项解释如下：

1. `Q` 是 vertical states，也就是树节点归约后的状态。
2. `\Sigma` 是输入树标签字母表。
3. `F\subseteq Q` 是 final states。
4. `S_a` 是处理标签 `a` 的 horizontal DFA 状态集。
5. `s_a^{in}` 是其初始状态。
6. `\delta_a : S_a \times Q \to S_a` 是读取孩子状态串的转移函数。
7. `\lambda_a : S_a \to Q` 是 horizontal computation 的输出函数。

由此导出的 transition language 是：

$$
L_{a,q}=\{\, w\in Q^* \mid \lambda_a(\delta_a^*(s_a^{in},w))=q \,\}
$$

这表示：若一个 `a`-labelled 节点的孩子状态串为 `w`，则经过 `D_a` 处理后输出 `q`，该节点就归约到 vertical state `q`。

### 一个最小例子与通俗解释

论文自己的例子是布尔表达式树：叶子标记为 `0/1`，内部节点标记为 `\land / \lor`。每个标签各自带一个 horizontal DFA，读取孩子子树已经归约好的真假状态串，然后输出该节点的真假状态。若根节点输出 `q_1`，整棵树就被接受。

通俗地说，这个模型像“两层自动机叠在一起”：

1. 第一层横向扫描兄弟状态串；
2. 第二层把扫描结果提升为当前节点状态。

因此它特别适合 unranked trees，因为一个节点可以有任意多个孩子。

### 运行 / 接受 / 转移语义

若 `t=a(t_1\cdots t_k)`，并且子树 `t_i` 已分别归约到状态 `q_i`，则节点 `a` 的状态由对应 horizontal automaton 决定：

$$
q=\lambda_a(\delta_a^*(s_a^{in}, q_1\cdots q_k))
$$

整棵树接受当且仅当根状态在 `F` 中：

$$
t\in T(A)\iff q_{root}\in F
$$

在此基础上，论文又定义了 top-down deterministic 模型 `#DTA`，并研究其表达能力与判定问题。最关键的两个结论是：

$$
\forall T\subseteq T_\Sigma,\ \exists!\ A_T
$$

即每个 regular unranked tree language 都存在唯一的 minimal bottom-up deterministic automaton；以及：

$$
T \text{ is } \#DTA\text{-recognizable } \iff \text{a corresponding path-language condition holds}
$$

### 语义边界

相对 [regular-tree-languages-over-non-ranked-alphabets/desc.md](../regular-tree-languages-over-non-ranked-alphabets/desc.md)，它不再停留在“一般 unranked tree automata 都能做什么”，而是专门固定 deterministic 子类和最小化结构；相对 `Hedge Automata`，它仍以单树为对象，而不是 hedge / forest。

### 关键性质与判定边界

论文的核心结构定理是：

$$
\text{For every regular } T\subseteq T_\Sigma,\ \text{there is a unique minimal } "DTA\ A_T
$$

并且原文通过 top congruence 与 horizontal congruence 定义 canonical automaton。对应的最小化路线是：

1. 定义树级等价 `\equiv_T`；
2. 定义水平方向等价 `\equiv_T^h`；
3. 由这些等价类构造 `A_T`。

对 top-down 路线，论文证明：

$$
\text{Given regular }T\subseteq T_\Sigma,\ \text{it is decidable whether }T\text{ is } \#DTA\text{-recognizable}
$$

这让 deterministic unranked tree automata 既有 canonical bottom-up 主线，也有可判定的 top-down 子线。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | vertical/horizontal 双层状态结构很清晰。 |
| 事件 / 触发 | 不适用 | 输入对象是 unranked tree。 |
| 守卫 / 数据 | 不支持 | 原始模型无一般数据变量。 |
| 层次 | 强支持 | 层次来自树结构；横向关系由 horizontal DFA 处理。 |
| 并发 / 同步 | 不支持 | 不是并发交互模型。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散树语言识别。 |
| 可执行 / 可验证性 | 强支持 | 最小化、canonical form 和 top-down decidability 都很成熟。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| bottom-up deterministic 骨架 | `$A=(Q,\Sigma,(D_a)_{a\in\Sigma},F)$` | 论文主定义。 |
| horizontal DFA | `$D_a=(S_a,Q,s_a^{in},\delta_a,\lambda_a)$` | 每个标签各自处理孩子状态串。 |
| transition language | `$L_{a,q}=\{w\in Q^* \mid \lambda_a(\delta_a^*(s_a^{in},w))=q\}$` | 节点归约规则。 |
| 唯一最小自动机 | `$\exists!\ A_T$` | Theorem 1。 |
| top-down 可判定性 | `$\text{decidable whether }T\text{ is }\#DTA\text{-recognizable}$` | Theorem 6。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先给定 unranked tree language；
2. 区分 vertical states 与每个标签的 horizontal DFA；
3. 通过孩子状态串的 deterministic 扫描定义节点状态；
4. 若关心 top-down processing，再检查是否满足 `#DTA` 可识别条件。

### 机器可处理承载方式

机器可处理承载方式是：

1. vertical state set `Q`；
2. per-label horizontal DFA family `(D_a)`；
3. path-language characterization。

### 交换与互操作

它直接连到：

1. general unranked tree automata；
2. XML query / validation 场景；
3. canonical minimization 与 deterministic top-down processing。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：无工程标准。
- 仿真/执行支持：可直接按 horizontal DFA + vertical state 递归执行。
- 验证/分析支持：equivalent states、minimal automaton、path-language characterization 很强。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：为 deterministic unranked / XML processing 路线提供了很稳的理论骨架。

## 适用场景与需求前提

### 适用场景

适用于 XML-like trees 的 deterministic recognition、canonical validator construction、top-down query processing 以及需要最小 deterministic recognizer 的场景。

### 需求前提

1. 对象必须是 regular unranked trees。
2. 需要 deterministic 识别而不是仅仅可识别。
3. 节点局部约束能写成孩子状态串上的 deterministic horizontal processing。

### 不适用或高成本场景

若对象本质上是 hedge / forest 或需要 XML schema 工程语法层，`Hedge Automata` 或具体 schema 语言更直接。

## 与相邻形式主义的关系

相对 [regular-tree-languages-over-non-ranked-alphabets/desc.md](../regular-tree-languages-over-non-ranked-alphabets/desc.md)，它专注 deterministic 子线；相对 [hedge-automata-a-formal-model-for-xml-schemata/desc.md](../hedge-automata-a-formal-model-for-xml-schemata/desc.md)，它仍然处理单树而非 hedge；相对 ranked deterministic top-down tree automata，它多了处理有限但无上界分支数的 horizontal DFA 层。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata -> unranked` 支线继续长成了一个清晰的 deterministic 子枝，使演化树不再只停在一般 unranked/hedge 概念层。

### 作为目标形式主义还是中间表示

在 XML-like tree recognition 或 canonical validation 场景下可以作为目标形式主义；对控制系统主线则更多是树对象谱系中的理论节点。

### 对需求到模型生成的启发

它提示我们：当需求希望得到 deterministic、可最小化、可 canonical 的 unranked-tree recognizer 时，必须显式区分 vertical semantics 和 horizontal sibling processing。

### 现实限制

原文没有 DSL、schema 标准或工具实现，主要价值仍是理论骨架。

## 重要的相关工作

### 奠基或前身工作

- [regular-tree-languages-over-non-ranked-alphabets/desc.md](../regular-tree-languages-over-non-ranked-alphabets/desc.md)

### 同类型或同家族工作

- deterministic top-down tree automata
- XML query / path-language 路线

### 标准 / 格式 / 工具链工作

- 原文无工程标准，但显式面向 XML/document processing 语境。

### 与本研究关系最紧的工作

- 它为 `unranked` 支线补出了一个比 survey 更稳的 deterministic 子节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Deterministic Unranked Tree Automata
- 论文角色：分支整理
- 核心功能：为 unranked trees 给出可最小化、可 canonical 的 deterministic bottom-up automata，并判定何时可 top-down deterministic。
- 关键特性：vertical/horizontal 双层 automaton、唯一最小模型、path-language characterization。
- 构造方式：`A=(Q,\Sigma,(D_a),F)`，其中每个标签都配一个 horizontal DFA。
- 基础设施：无工程标准，但理论可执行性和最小化分析很成熟。
- 适用场景：deterministic unranked tree recognition、canonical validator、XML-like top-down processing。
- 需求前提：对象是 regular unranked tree，且希望得到 deterministic、最小化的 recognizer。
- 状态：🟢

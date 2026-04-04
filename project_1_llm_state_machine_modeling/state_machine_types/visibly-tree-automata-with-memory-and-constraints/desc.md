# 带记忆与约束的可见树自动机 / Visibly Tree Automata with Memory and Constraints

## 基本信息

- 标题：Visibly Tree Automata with Memory and Constraints
- 中文标题：带记忆与约束的可见树自动机
- 作者：Hubert Comon-Lundh, Florent Jacquemard, Nicolas Perrin
- 发表：*Logical Methods in Computer Science* 4(2:8):1-36, 2008
- DOI：`10.2168/LMCS-4(2:8)2008`
- 链接：https://doi.org/10.2168/LMCS-4(2:8)2008
- 形式主义：`Visibly Tree Automata with Memory (VTAM) / constrained VTAM`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 闭包与判定性整理
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `TAM/VTAM` 元组、底向上 rewrite semantics、visibility partition、determinization construction 与 constrained variants。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 tree automaton with memory 的 rewrite rules、`PUSH/POP/INT` 分类及结构约束。

## 简报

这篇论文的关键点不是单纯把 stack 换成 tree memory，而是证明：只要 memory 操作对输入符号“可见”，tree automata with memory 这条通常很难处理的家族也能重新获得 determinization、Boolean closure 和低复杂度 emptiness / membership。题目里的 “with constraints” 也不是装饰，而是进一步说明哪些 memory-test 扩展还能保持这些好性质，哪些会直接把 emptiness 推到不可判定。

- 形式主义定位：`Tree Automata` 下 memory-tree 支线上的经典母节点，可视为 tree-side 的 visibly pushdown 思想推广。
- 构造方式简述：先从一般 `TAM` 出发，再把输入符号分到 `PUSH / POP / INT` 各子类，使每个符号预先决定 memory 操作种类。
- 基础设施与场景简述：纯理论模型，但 determinization、Boolean closure、`PTIME` emptiness / membership，以及 structural-equality constraint 的可保留性都非常适合作为演化树中的稳定家族节点。

```text
输入树 -> bottom-up tree automaton + tree memory -> visible memory action -> determinizable tree-language family
```

## 形式主义定义与核心对象

### 定义对象

原文先定义一般的 tree automaton with memory (`TAM`)，再在其上施加 visibility restriction 得到 `VTAM`。计算方向是 bottom-up：每个子树先算出状态和 memory，父节点再根据当前符号和孩子 memory 更新自己的状态与 memory。

### 核心抽象

一般 `TAM` 被定义为：

$$
A = (\Gamma,Q,Q_f,\Delta)
$$

上式中的符号逐项解释如下：

1. `\Gamma` 是 memory signature，也就是 memory term 的字母表。
2. `Q` 是有限状态集。
3. `Q_f \subseteq Q` 是终结状态集。
4. `\Delta` 是 rewrite-style transition rules。

其基本 rule 形如：

$$
f(q_1(m_1),\ldots,q_n(m_n)) \to q(m)
$$

上式中的符号逐项解释如下：

1. `f` 是当前输入树节点符号。
2. `m_1,\ldots,m_n` 是子树已算出的 memory contents。
3. `q_1,\ldots,q_n` 是对应子树状态。
4. `m` 是父节点要构造出的新 memory。

接受与 memory language 定义为：

$$
L(A,q) = \{ t \mid \exists m \in T(\Gamma),\ t \to_\Delta^* q(m) \}
$$

$$
M(A,q) = \{ m \mid \exists t \in T(\Sigma),\ t \to_\Delta^* q(m) \}
$$

`VTAM` 则要求输入字母表被分成固定的可见类别：

$$
\Sigma = \Sigma_{\mathrm{PUSH}} \uplus \Sigma_{\mathrm{POP11}} \uplus \Sigma_{\mathrm{POP12}} \uplus \Sigma_{\mathrm{POP21}} \uplus \Sigma_{\mathrm{POP22}} \uplus \Sigma_{\mathrm{INT0}} \uplus \Sigma_{\mathrm{INT1}} \uplus \Sigma_{\mathrm{INT2}}
$$

其中的代表性规则分别是：

$$
f(q_1(y_1),q_2(y_2)) \to q(h(y_1,y_2))
$$

这对应 `PUSH`；

$$
f(q_1(h(y_{11},y_{12})),q_2(y_2)) \to q(y_{11})
$$

这对应 `POP11`；

$$
f(q_1(y_1),q_2(y_2)) \to q(y_1)
$$

这对应 `INT1`。

### 一个最小例子与通俗解释

一个很直观的最小例子是：把某类二叉控制树中的某些节点看成 `PUSH` 符号，另一些节点看成 `POP11`。当自动机在某个 `PUSH` 节点合成出 `h(m_1,m_2)` 时，它相当于把两份待恢复的 continuation 打包进一棵 memory tree；之后若读到 `POP11`，就只能取回这棵 memory 的左子部分 `m_1`。

通俗地说，`VTAM` 像“bottom-up tree automaton 外接一棵受输入符号显式控制的记忆树”。因为每个输入符号的 memory 行为是预先固定的，所以 determinization 又重新变得可能。

### 运行 / 接受 / 转移语义

`VTAM` 的运行语义仍是 rewrite semantics：

$$
t \to_\Delta^* q(m)
$$

这表示输入树 `t` 经过若干步底向上规约后，在根处得到状态 `q` 和 memory `m`。

接受条件可写成：

$$
t \in L(A) \iff \exists q \in Q_f,\ \exists m \in T(\Gamma),\ t \to_\Delta^* q(m)
$$

visibility restriction 的核心，不是限制状态，而是限制“当前读到什么符号时允许做什么 memory operation”。因此 determinization 时可以像 visibly pushdown automata 一样，把某些 memory 更新延迟到 matching pop 阶段统一处理。

### 语义边界

相对一般 `TAM`，`VTAM` 通过 visibility 换回了 determinization 和 Boolean closure；相对 [pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md)，它是 bottom-up tree memory 而不是 top-down tree pushdown；相对 [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md)，它强调的是 visible memory discipline 与 closure，而不是 matching-pop branching power。

### 关键性质与判定边界

原文给出的核心正结果包括：

$$
\forall A \in \mathrm{VTAM},\ \exists A_{\mathrm{det}} \in \mathrm{VTAM}\text{ such that }L(A_{\mathrm{det}})=L(A)
$$

以及 closure：

$$
\mathrm{VTAM}\text{ is closed under union, intersection, complement}
$$

判定性方面：

$$
\mathrm{emptiness}(\mathrm{VTAM})\ \text{is PTIME-complete}
$$

$$
\mathrm{membership}(\mathrm{VTAM})\ \text{is decidable in PTIME}
$$

$$
\mathrm{universality}(\mathrm{VTAM}),\ \mathrm{inclusion}(\mathrm{VTAM})\ \text{are EXPTIME-complete}
$$

对 title 中的 constrained extension，论文还说明：

1. 某些 structural equality / disequality constraints 仍可保持 determinization 与 decidable emptiness。
2. 但若把 constraints 放宽到一般 regular binary relations，则 emptiness 会变成 undecidable。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 底向上有限状态识别。 |
| 事件 / 触发 | 不适用 | 输入是树。 |
| 守卫 / 数据 | 中等支持 | 通过 memory equality / structure constraints 做有限测试。 |
| 层次 | 强支持 | 输入与 memory 都是树。 |
| 并发 / 同步 | 中等支持 | tree memory 能自然容纳多 continuation / 线程式结构。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | determinization、Boolean closure、PTIME emptiness / membership 都很清楚。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| TAM 元组 | `$A=(\Gamma,Q,Q_f,\Delta)$` | tree automaton with memory 的母体定义。 |
| 语言定义 | `$L(A,q)=\{t\mid \exists m,\ t\to_\Delta^* q(m)\}$` | bottom-up 接受语义。 |
| visibility partition | `$\Sigma=\Sigma_{\mathrm{PUSH}}\uplus\cdots\uplus\Sigma_{\mathrm{INT2}}$` | 每个符号预先决定 memory action。 |
| determinization | `$L(A_{\mathrm{det}})=L(A)$` | VTAM 可确定化。 |
| 判定边界 | `emptiness/membership PTIME`, `universality/inclusion EXPTIME` | 说明 visible restriction 的收益。 |

## 构造方式与承载格式

### 建模入口

1. 先判断 memory 操作能否由输入符号静态决定。
2. 若可以，再把符号划到 `PUSH / POP / INT` 各类别。
3. 若还需要比较 memory 结构，再谨慎引入 structural constraints，而不是一般 regular relation constraints。

### 机器可处理承载方式

机器可处理承载方式包括：

1. bottom-up rewrite rules；
2. tree memory signature `\Gamma`；
3. visibility partition；
4. determinization construction 与 constrained variants。

### 交换与互操作

它与 visibly pushdown automata、tree automata with one memory 和结构约束树自动机之间互操作很强，但没有工程 DSL / schema。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 rewrite-style rule system 与 memory signature。
- 仿真/执行支持：可按 bottom-up reduction 直接解释。
- 验证/分析支持：determinization、Boolean closure、emptiness / inclusion / universality / membership 结果完整。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 tree-memory family 中少数兼具表达力与良好 closure / decidability 的稳定节点。

## 适用场景与需求前提

### 适用场景

适合：

1. tree-structured control flow / continuation / concurrent return structure 的理论建模。
2. 需要 tree memory，但又希望保 determinization 与 Boolean closure 的场景。
3. 作为 tree automata family 中 memory-based 分支的代表条目。

### 需求前提

1. 输入对象必须是树。
2. memory 操作最好能由符号类别静态决定。
3. 若引入 constraints，最好限制在 structural equality / disequality 这类可控家族。

### 不适用或高成本场景

若需求需要一般正则二元关系约束、复杂顺序数据或高自由度 memory test，则可判定性很快失去；若只是普通 pushdown tree parsing，[pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md) 更直接。

## 与相邻形式主义的关系

相对 [pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md)，它把线性 / 树形 stack 提升为 bottom-up tree memory，并强调 visible operation；相对 [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md)，它追求的是 closure 与 decidability，而不是 matching-pop branching expressiveness；相对 [tree-automata/desc.md](../tree-automata/desc.md)，它是在 regular tree automata 之后沿 memory 方向展开的一条独立支线。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata` 下面的 memory-tree / visible-memory 分支正式立名，使这条线不再只有零散的 data-tree 或 constraint 论文，而有一个清晰母节点。

### 作为目标形式主义还是中间表示

更适合作为谱系节点和中间表示，不适合作为控制系统最终交付语言。

### 对需求到模型生成的启发

如果需求中出现“树状控制流 + continuation 结构 + 返回操作类别可由语法决定”的特征，LLM 可以优先考虑 visible memory family，而不是直接跳到更一般、也更不可控的 constrained tree automata。

### 现实限制

没有工程生态，constraints 一放宽就可能越界，因此它在本研究中的核心价值仍是扩树和表达力 / 判定性边界整理。

## 重要的相关工作

### 奠基或前身工作

- [tree-automata/desc.md](../tree-automata/desc.md)
- [pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md)

### 同类型或同家族工作

- [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合作为 `Tree Automata` 下 `Memory / Visibly Tree` 支线的经典代表条目，与 [pushdown-tree-automata/desc.md](../pushdown-tree-automata/desc.md) 一起把 tree-side memory/pushdown 演化树补得更完整。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Visibly Tree Automata with Memory (VTAM) / constrained VTAM`
- 论文角色：模型提出 / 闭包与判定性整理
- 核心功能：把 tree automata with memory 加上 visible operation discipline，并整理哪些约束扩展仍保 determinization 与 decidability。
- 关键特性：bottom-up tree memory、visible `PUSH/POP/INT` partition、determinization、Boolean closure、PTIME emptiness / membership、constrained extension boundary。
- 构造方式：`TAM` 元组 `(\Gamma,Q,Q_f,\Delta)` 加 visibility partition 与 rewrite semantics。
- 基础设施：纯理论模型，无工程标准或工具；核心基础设施是 determinization construction 与 constrained-family analysis。
- 适用场景：tree-memory family、continuation / thread-like tree control flow、演化树中的 memory-tree 支线。
- 需求前提：输入必须是树，memory 操作最好对符号可见，约束最好限制在 structural family。
- 状态：🟢

# 下推树自动机 / Pushdown Tree Automata

## 基本信息

- 标题：Pushdown Tree Automata
- 中文标题：下推树自动机
- 作者：Irène Guessarian
- 发表：*Mathematical Systems Theory* 16(1):237-263, 1983
- DOI：`10.1007/BF01744582`
- 链接：https://doi.org/10.1007/BF01744582
- 形式主义：`Pushdown Tree Automata (PDTA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `M=(Q,F,\Pi,q_0,Z_0,R)` 元组、read / `\varepsilon` rules、instantaneous description 与 configuration rewrite semantics。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 ranked trees、tree-shaped pushdown、grammar correspondence 与 restricted linear-stack variant。

## 简报

这篇论文把 `Pushdown Automata` 从线性词真正推进到了树对象，同时连输入和栈都允许是树，而不是简单把树扫描再压回字符串。它最关键的贡献不是某个技巧性判定，而是把“context-free tree languages 的 automaton-theoretic 面貌”正式立成了 `PDTA` 这条支线。之后的 `BPTA`、线性 `L-PDTA` 和一些 tree-pushdown machine 都是在这条母线上继续分化。

- 形式主义定位：`Tree Automata` 下的 pushdown / context-free tree 母节点，也是 tree-side pushdown branch 的经典起点。
- 构造方式简述：输入是 ranked tree，pushdown store 也是树；自动机自顶向下读输入，同时只访问当前树栈的根。
- 基础设施与场景简述：原文纯理论，但完整给出 `PDTA` 与 context-free tree grammar、Greibach tree language、deterministic tree language 以及 linear-stack restricted variant 之间的对应。

```text
输入树 -> 顶层读入 + 树形 pushdown -> read / epsilon rewrite -> context-free tree language
```

## 形式主义定义与核心对象

### 定义对象

原文的对象是 ranked input trees，而不是 words。与普通 `PDA` 的差别在于：

1. 输入是树。
2. pushdown store 也是树，而不是线性栈串。
3. 机器一次只读当前输入节点和当前栈树的根。

### 核心抽象

原文把 pushdown tree automaton 写成：

$$
M = (Q, F, \Pi, q_0, Z_0, R)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `F` 是输入 ranked alphabet。
3. `\Pi` 是 pushdown alphabet，也是 ranked alphabet。
4. `q_0 \in Q` 是初始状态。
5. `Z_0 \in \Pi_0` 是初始树栈符号。
6. `R` 是有限规则集。

最核心的两类规则分别是 read rule 与 `\varepsilon`-rule。原文的 read rule 形如：

$$
q(f(v_1,\ldots,v_r), E(x_1,\ldots,x_s)) \to f(q_1(v_1,\pi_1),\ldots,q_r(v_r,\pi_r))
$$

` \varepsilon`-rule 形如：

$$
q(v, E(x_1,\ldots,x_s)) \to q'(v,\pi')
$$

上式中的符号逐项解释如下：

1. `f \in F_r` 是当前输入树节点符号。
2. `E \in \Pi_s` 是当前 pushdown 根符号。
3. `v_i` 表示输入子树位置。
4. `x_i` 表示 pushdown 子树位置。
5. `\pi_i,\pi'` 是由 pushdown 符号和变量组成的树项，用来重写后继 pushdown。
6. read rule 在读取一个输入节点后，把若干子任务分发到各子树。
7. `\varepsilon`-rule 不读输入，只改写当前树栈。

### 一个最小例子与通俗解释

原文的 Example 2 很能说明 `PDTA` 的直觉。该自动机在读到二叉符号 `f(u,v)` 时，不只是像普通 tree automaton 那样把两个状态发给左右子树，而是会在 pushdown 中压入像 `K(H(B))` 这样的 continuation 树，先处理一侧子树，再用树栈中保存的上下文去恢复另一侧子树的待处理义务。

通俗地说，`PDTA` 像“在树上做递归下降分析的 pushdown parser”。普通 `Tree Automata` 只会给每棵子树贴有限状态标签，而 `PDTA` 还会把未完成的树形上下文压到一个树栈里，之后再取回来。

### 运行 / 接受 / 转移语义

原文把 instantaneous description 写成：

$$
q(t,\pi) \in Q \times A(F) \times A(\Pi)
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `t` 是当前待处理输入子树。
3. `\pi` 是当前树形 pushdown 内容。

configuration 则是由若干 ID 组成的树形 sentential form。move relation 通过对某个 ID 应用一条 read / `\varepsilon` rule 来定义，记为：

$$
c \vdash_M c'
$$

接受语言定义为：

$$
T(M) = \{ t \in A(F) \mid q_0(t,Z_0) \vdash_M^* t \}
$$

也就是说，从初始 ID `q_0(t,Z_0)` 出发，若能把整棵树规约到只剩输入树本身，就说明所有挂起的控制与 pushdown 义务都已经被正确消费。

### 语义边界

与 [tree-automata/desc.md](../tree-automata/desc.md) 相比，`PDTA` 的增强点是无界树形记忆，因此能覆盖 context-free tree languages；与 [on-context-free-languages-and-push-down-automata/desc.md](../on-context-free-languages-and-push-down-automata/desc.md) 相比，它把 pushdown 从 word-side 扩展到 tree-side；与 [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md) 相比，它还不能在一次 push 的所有 matching pops 上同时表达 existential / universal branching 要求。

### 关键性质与判定边界

原文最重要的结论是：

$$
\mathrm{Lang}(\mathrm{PDTA}) = \mathrm{CFTL}
$$

其中 `\mathrm{CFTL}` 表示 context-free tree languages。

对受限子类，论文进一步给出：

$$
\mathrm{Lang}(\mathrm{real\mbox{-}time\ PDTA}) = \mathrm{Greibach\ tree\ languages}
$$

$$
\mathrm{Lang}(\mathrm{deterministic\ PDTA}) = \mathrm{deterministic\ tree\ languages}
$$

并证明任何 context-free tree language 都可由 restricted PDTA 接受：

$$
\forall L \in \mathrm{CFTL},\ \exists M_{\mathrm{RPDTA}} \text{ such that } T(M_{\mathrm{RPDTA}})=L
$$

这意味着 tree-side pushdown family 不只是理论存在，而且可以进一步压成更 operational 的线性栈变体。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 保留有限控制骨架。 |
| 事件 / 触发 | 不适用 | 输入是 ranked tree。 |
| 守卫 / 数据 | 不支持 | 原始模型不含变量守卫。 |
| 层次 | 强支持 | 输入与 pushdown 都是树。 |
| 并发 / 同步 | 弱支持 | read rule 会把子任务分发到多个子树，但不是并发网语义。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | grammar correspondence、deterministic / Greibach characterization 与 restricted variant 都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| PDTA 元组 | `$M=(Q,F,\Pi,q_0,Z_0,R)$` | tree-side pushdown automaton 的标准定义。 |
| ID | `$q(t,\pi)$` | 当前状态、输入子树与树形 pushdown。 |
| move relation | `$c \vdash_M c'$` | 配置重写语义。 |
| 接受语言 | `$T(M)=\{t\mid q_0(t,Z_0)\vdash_M^* t\}$` | final-state acceptance 定义。 |
| 家族对应 | `$\mathrm{Lang}(\mathrm{PDTA})=\mathrm{CFTL}$` | context-free tree language 的 automaton characterization。 |

## 构造方式与承载格式

### 建模入口

1. 先给定输入树字母表 `F` 和 pushdown 字母表 `\Pi`。
2. 再决定每个输入符号在当前 pushdown 根下应如何分发子任务。
3. 若需要纯控制改写，则使用 `\varepsilon`-rules。
4. 若要更 operational 的实现，可继续把树栈限制成 linear stack，转向 restricted `PDTA` / `L-PDTA` 路线。

### 机器可处理承载方式

机器可处理承载方式主要就是：

1. ranked-tree 输入；
2. tree-shaped pushdown；
3. read / `\varepsilon` rewrite rules；
4. context-free tree grammar 与 restricted parser 之间的转换。

### 交换与互操作

它与 context-free tree grammar、indexed language yield 和 semi-Thue-style rewriting 之间互操作很强，但原文没有工程化交换格式。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 ranked alphabet、tree rewrite rule 与 grammar correspondence。
- 仿真/执行支持：可直接按 ID / configuration semantics 解释运行。
- 验证/分析支持：有 deterministic、real-time、Greibach 和 restricted-stack 对应结果。
- 代码生成/转换支持：原文未讨论工程代码生成，但与 grammar / parser 之间转换清楚。
- 标准化或社区生态：是后续 tree-pushdown family 的经典起点。

## 适用场景与需求前提

### 适用场景

适合：

1. 树对象上的 context-free 结构识别。
2. 需要比 ordinary tree automata 更强的无界层次记忆。
3. 讨论 indexed-language yield 与 tree-language 关系的理论场景。

### 需求前提

1. 输入对象必须是树而不是词。
2. 需求中的非正则性主要来自递归上下文和挂起义务，而不是时间或数值数据。
3. 可以接受 top-down parsing 风格的 tree-side pushdown 视角。

### 不适用或高成本场景

如果需求重点是 bottom-up memory、visible stack discipline 或 matching-pop 上的 branching 约束，那么后续 [visibly-tree-automata-with-memory-and-constraints/desc.md](../visibly-tree-automata-with-memory-and-constraints/desc.md)、[branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md) 和 [deterministic-linear-pushdown-tree-automata/desc.md](../deterministic-linear-pushdown-tree-automata/desc.md) 会更贴切。

## 与相邻形式主义的关系

相对 [tree-automata/desc.md](../tree-automata/desc.md)，它从 regular tree language 推到了 context-free tree language；相对 [on-context-free-languages-and-push-down-automata/desc.md](../on-context-free-languages-and-push-down-automata/desc.md)，它是 tree-side 的 pushdown 对应物；相对 [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md)，它还没有 count-constraint 级的 branching matching；相对 [deterministic-linear-pushdown-tree-automata/desc.md](../deterministic-linear-pushdown-tree-automata/desc.md)，它是更一般、也更重的母节点。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Tree Automata` 下的 pushdown 主枝正式立了起来，使后续 `BPTA`、`L-PDTA` 等节点都能有稳定父边，而不是散落成“树上某种复杂 machine”。

### 作为目标形式主义还是中间表示

更适合作为谱系母节点和高表达力中间表示，不适合作为控制系统的直接交付语言。

### 对需求到模型生成的启发

如果需求文本里已经出现“树状对象 + 递归展开 + 待处理上下文”的特征，LLM 不应只考虑 ordinary tree automata，而应判断是否需要 pushdown tree family。

### 现实限制

原文没有工程工具，且树形 pushdown 对实际控制系统建模来说偏重，因此其价值主要在演化树骨架和表达力边界。

## 重要的相关工作

### 奠基或前身工作

- [on-context-free-languages-and-push-down-automata/desc.md](../on-context-free-languages-and-push-down-automata/desc.md)
- [tree-automata/desc.md](../tree-automata/desc.md)

### 同类型或同家族工作

- [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md)
- [deterministic-linear-pushdown-tree-automata/desc.md](../deterministic-linear-pushdown-tree-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合作为 `Tree Automata` 下 `Pushdown Tree` 母枝的经典代表条目，并为 [branching-pushdown-tree-automata/desc.md](../branching-pushdown-tree-automata/desc.md) 与 [deterministic-linear-pushdown-tree-automata/desc.md](../deterministic-linear-pushdown-tree-automata/desc.md) 提供父节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Pushdown Tree Automata (PDTA)`
- 论文角色：模型提出
- 核心功能：把 pushdown 记忆从词推广到树输入与树栈，并给出 context-free tree language 的 automaton characterization。
- 关键特性：tree input、tree-shaped pushdown、read / `\varepsilon` rewrite、context-free tree language 对应、Greibach / deterministic 子类、restricted linear-stack variant。
- 构造方式：`M=(Q,F,\Pi,q_0,Z_0,R)` 元组加 instantaneous description / configuration semantics。
- 基础设施：纯理论模型，无工程标准或工具；核心在 grammar correspondence 与 restricted operational variant。
- 适用场景：context-free tree language、tree-side pushdown parsing、indexed-language yield 理论。
- 需求前提：对象必须是树，且核心复杂度来自递归上下文与无界挂起义务。
- 状态：🟢

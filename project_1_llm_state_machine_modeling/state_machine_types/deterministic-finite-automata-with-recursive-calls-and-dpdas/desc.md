# 带递归调用的确定性有限自动机与 DPDA / Deterministic finite automata with recursive calls and DPDAs

## 基本信息

- 标题：Deterministic finite automata with recursive calls and DPDAs
- 中文标题：带递归调用的确定性有限自动机与 DPDA
- 作者：Jean H. Gallier、Salvatore La Torre、Supratik Mukhopadhyay
- 发表：*Information Processing Letters*, 87(4):187-193, 2003
- DOI：`10.1016/S0020-0190(03)00281-3`
- 链接：https://doi.org/10.1016/S0020-0190(03)00281-3
- 形式主义：`Recursive-Call DFA / Deterministic Finite Automata with Recursive Calls`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / automata-theoretic recursive-call branch
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 component DFA definition、call / return edges、graph-substitution semantics 与与 `DPDA` 的构造性互译。
- 标准/格式获取方式：原文没有 DSL 或交换标准；核心承载方式是 `D=\langle F_1 \Leftarrow D_1,\ldots,F_N \Leftarrow D_N \rangle` 这类递归调用 DFA 定义、即时描述 `\langle R,p,u \rangle` 与 graph rewriting semantics。

## 简报

这篇论文的价值不在“又给 `DPDA` 做了一个等价变体”，而在于它把 recursive call 这件事压回了最朴素的 `DFA` 骨架里。作者明确把模型描述成“若干 component DFAs 可以递归调用彼此”，并直接指出它与 `recursive state machines`、`unrestricted hierarchical state machines` 同宗。对当前演化树来说，这使 `uHSM/RSM` 旁边多出一个更偏 formal-language 口径、但仍然清楚属于递归层次支线的 automata 节点。

- 形式主义定位：`uHSM/RSM` 的 automata-theoretic sibling，用纯语言识别视角表达 call-return hierarchy。
- 构造方式简述：若干 component DFA 之间通过不读输入的 call / return 边相互嵌套；每次调用把被调 component 的 entry 与调用点、各 exits 与返回点做图替换。
- 基础设施与场景简述：纯理论条目，但它把 recursive-call automaton 明确接到了 `DPDA` 与 deterministic context-free languages，适合作为 `RSM` 支线的语言论锚点。

```text
component DFA family -> recursive calls / returns -> graph substitution semantics -> deterministic CFL -> DPDA equivalence
```

## 形式主义定义与核心对象

### 定义对象

原文研究的是“带递归调用的确定性有限自动机”，也就是若干 component DFA 可通过特殊调用边互相进入。与普通 `DFA` 相比，变化点只有一个：迁移里除了 ordinary symbol transitions，还允许不读输入的 call / return discipline。

### 核心抽象

原文把整体机器写成：

$$
D = \langle F_1 \Leftarrow D_1,\ldots,F_N \Leftarrow D_N \rangle
$$

上式中的符号逐项解释如下：

1. `F_i` 是非终结符风格的过程名，也就是 component name。
2. `D_i` 是与 `F_i` 对应的 component DFA。
3. `F_1 \Leftarrow D_1` 是主定义，也就是顶层入口。

每个 component definition `F_i \Leftarrow D_i` 的正式骨架为：

$$
D_i = \langle Q,\Sigma \cup \Phi \cup [1,M],\delta,in,OUT,FINAL \rangle
$$

上式中的符号逐项解释如下：

1. `Q` 是局部状态集合。
2. `\Sigma` 是输入字母表。
3. `\Phi` 是可调用的 component 名集合。
4. `[1,M]` 是返回出口编号。
5. `\delta` 是迁移函数，既可处理普通输入，也可处理 call / return 标签。
6. `in` 是 entry state。
7. `OUT` 把某些状态标成 exit states，并给出出口编号。
8. `FINAL` 是接受状态集合。

### 一个最小例子与通俗解释

原文 Figure 1 的三组件例子最能说明它怎么工作：

1. 主组件 `D_1` 在某个状态上读到调用符号后进入 `D_2`。
2. `D_2` 继续在自己的局部状态里消费输入。
3. 一旦 `D_2` 到达某个编号出口，就沿对应 return 边回到调用者给这个出口预留的位置。

通俗地说，这个模型像“每个状态机都能像函数一样调用别的状态机”，而且调用时不会读输入，只是把控制权切给子机。比普通 `DFA` 多出来的，不是变量或时间，而是一条真正的调用栈语义。

### 运行 / 接受 / 转移语义

原文把一条运行写成即时描述序列：

$$
\langle R,p,u \rangle
$$

上式中的符号逐项解释如下：

1. `R` 是当前已展开出的递归图。
2. `p` 是当前控制点。
3. `u` 是尚未读完的输入后缀。

普通读符号步可以写成：

$$
\langle R,p,au \rangle \to \langle R,\delta(p,a),u \rangle
$$

若当前位置是一次对 `F_i` 的调用，则语义上是把 `D_i` 的 entry / exits 接到当前图中：

$$
\langle R,p,u \rangle \to \langle R[q \leftarrow D_i],in_i,u \rangle
$$

这说明它的 call 语义不是“显式栈字母推入”，而是“递归图替换后把控制权送进被调 component 的入口”。语言定义则是：

$$
L(D)=\{u \mid \langle D_1,in_1,u \rangle \to^* \langle R,f,\epsilon \rangle,\ f \in FINAL\}
$$

### 语义边界

这篇论文把边界划得很明确：

1. 模型仍是 deterministic 的；如果某个状态有 call 边，那它不能再有别的 outgoing transitions。
2. 允许 multiple exits，因此返回位置可以不止一个。
3. 如果再允许 ordinary transitions 上的 nondeterminism，就会滑向一般 `CFL`，不再是本文关注的 deterministic family。

### 关键性质与判定边界

原文最关键的结论可以压成：

$$
\text{DFA with recursive calls} \equiv \text{DPDA}
$$

更精确地说，它刻画的正是 deterministic context-free languages：

$$
L(D) \text{ is exactly a deterministic context-free language}
$$

因此，这个 family 在演化树里的意义不是“替代 `RSM`”，而是提供一个更偏自动机理论、直接通向 `DPDA` 的递归层次节点。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 由 component DFA 与局部状态构成。 |
| 事件 / 触发 | 支持 | 普通输入符号驱动 ordinary transitions。 |
| 守卫 / 数据 | 不支持 | 没有变量。 |
| 层次 | 强支持 | component 间递归调用形成 hierarchy。 |
| 并发 / 同步 | 不支持 | 纯 sequential。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 与 `DPDA` 等价，语言与等价性分析可继承。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总体定义 | `$D=\langle F_1 \Leftarrow D_1,\ldots,F_N \Leftarrow D_N \rangle$` | recursive-call DFA 的总骨架。 |
| component tuple | `$D_i=\langle Q,\Sigma \cup \Phi \cup [1,M],\delta,in,OUT,FINAL \rangle$` | 单个 component DFA 的正式定义。 |
| 即时描述 | `$\langle R,p,u \rangle$` | 当前展开图、控制点与剩余输入。 |
| call step | `$\langle R,p,u \rangle \to \langle R[q \leftarrow D_i],in_i,u \rangle$` | 图替换式调用语义。 |
| 表达力 | `$\text{recursive-call DFA} \equiv \text{DPDA}$` | 直接锁定 deterministic CFL family。 |

## 构造方式与承载格式

### 建模入口

1. 先定义若干 component DFA。
2. 给 component 指定 entry 与若干编号 exits。
3. 用 `F_i` 调用符号把某些状态变成调用点。
4. 为每个调用点的每个出口固定返回位置。

### 机器可处理承载方式

原文真正可供机器处理的承载方式是：

1. recursive component tuple；
2. graph substitution semantics；
3. 即时描述与输入消费规则；
4. 到 atomic normal-form `DPDA` 的互译。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [model-checking-of-unrestricted-hierarchical-state-machines/desc.md](../model-checking-of-unrestricted-hierarchical-state-machines/desc.md) 的递归 hierarchy 思想。
2. 与 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md) 构成 automata-language 视角与程序分析视角的两条平行表达。
3. 向另一侧直接连到 [two-way-deterministic-pushdown-automaton-languages-and-some-open-problems-in-the-theory-of-computation/desc.md](../two-way-deterministic-pushdown-automaton-languages-and-some-open-problems-in-the-theory-of-computation/desc.md) 所在的 `DPDA` 主线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 recursive-call DFA tuple 与 graph rewriting semantics。
- 仿真/执行支持：可通过即时描述 `\langle R,p,u \rangle` 直接定义运行。
- 验证/分析支持：语言等价到 `DPDA`，因此可借用 deterministic CFL / `DPDA` 决策结论。
- 代码生成/转换支持：原文给出到 atomic normal-form `DPDA` 的构造性对应。
- 标准化或社区生态：研究型 automata family，主要价值在把递归 hierarchy 明确压回 formal-language 口径。

## 适用场景与需求前提

### 适用场景

适合：

1. 想用纯自动机语言来表达递归调用控制流，而不引入额外程序语义时。
2. 需要把 `RSM/uHSM` 这条支线直接接到 deterministic context-free languages 时。
3. 关心 call-return hierarchy 的语言识别，而不是开放系统、博弈或概率扩展时。

### 需求前提

1. 系统核心是顺序递归控制流。
2. 交互对象仍是线性输入词。
3. 若坚持 deterministic family，则调用状态不能再带其他竞争性迁移。

### 不适用或高成本场景

如果问题重点是变量、开放环境、时间或概率，这个 family 就太弱；那时更合适的是 `RSM`、open modules、timed recursive models 或 stochastic recursive branch。

## 与相邻形式主义的关系

相对普通 `DFA`，它多了 call / return hierarchy；相对 `DPDA`，它把栈语义重新包装成 component-recursion；相对 `RSM`，它更偏语言识别而不是程序分析，但两者都共享 entry / exit / recursive-call 的核心骨架。

## 与本研究的关系

对 `project_1` 来说，这篇文献的直接价值在于：它证明“层次状态机递归化”不只是一条 program-analysis 线，也是一条干净的 automata-theory 线。后续若要把需求里的 procedure-like control logic 映到形式化对象，这个 family 可以作为 `uHSM/RSM` 的语言论参照系。

## 重要的相关工作

1. [model-checking-of-unrestricted-hierarchical-state-machines/desc.md](../model-checking-of-unrestricted-hierarchical-state-machines/desc.md)：给出 `uHSM` 的递归层次 Kripke 语义。
2. [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)：把同类 call-return 骨架推进成 `RSM`。
3. [two-way-deterministic-pushdown-automaton-languages-and-some-open-problems-in-the-theory-of-computation/desc.md](../two-way-deterministic-pushdown-automaton-languages-and-some-open-problems-in-the-theory-of-computation/desc.md)：对应的 `DPDA` 主线。

## 文献分类总结

- 这是一篇 `🧩 经典离散状态机` 文献，因为主体是有限状态与递归调用构成的 automata family。
- 这是一篇 `🧱 模型本体` 文献，因为核心贡献是定义 recursive-call DFA 并证明其表达边界。
- 它主要描述 `📝 序列 / 语言对象`，因为接受对象是 deterministic context-free languages。
- 它属于 `🧮 形式语言与自动机理论`，因为全文都在做 automata / language equivalence，而不是 DSL、运行时或应用实现。

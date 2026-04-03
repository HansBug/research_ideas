# 树自动机 / Tree Automata

## 基本信息

- 标题：Tree Automata
- 中文标题：树自动机
- 作者：Ferenc G{\'e}cseg, Magnus Steinby
- 发表：Akad{\'e}miai Kiad{\'o} monograph, 1984；当前 PDF 为 2015 年重排版 arXiv 再版
- DOI：原书未提供 DOI
- 链接：https://arxiv.org/pdf/1509.06233.pdf
- 形式主义：Tree Automata
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：教程专著
- 工具/实现获取方式：原书不绑定单一实现；机器可处理入口是有限 `\Sigma`-algebra、initial assignment 与 final states。
- 标准/格式获取方式：原书没有统一 XML/JSON 标准，核心承载方式是 tree recognizer、recognizable forest 和 tree grammar 的形式定义。

## 简报

这本经典专著是 tree automata 最标准的母体之一。它把 frontier-to-root、root-to-frontier、deterministic / nondeterministic recognizer、recognizable forests、最小化和 decidability 全部系统化地放到 universal algebra 语言里。和后来的 `TATA` 相比，它更像“树自动机谱系的原始蓝本”，非常适合拿来给演化树上的 `Tree Automata` 节点补早期代表条目。

- 形式主义定位：普通 finite automata 向树和项结构推广后的经典母体。
- 构造方式简述：用有限 `\Sigma`-algebra、叶子初值赋值和 final states 描述树识别器。
- 基础设施与场景简述：原书是纯理论专著，没有工程标准，但 recognizer / forest / grammar / transducer 的骨架极稳。

```text
树 / 项结构 -> tree recognizer -> recognizable forest -> 判定 / 最小化 / 变换
```

## 形式主义定义与核心对象

### 定义对象

书中把 tree automata 表述为 tree recognizers。输入不是线性词，而是 ranked alphabet 上生成的树与 forest；识别对象不是 string language，而是 recognizable forests。

### 核心抽象

书中第 2 章给出的 frontier-to-root recognizer 可写成：

$$
A = (\mathcal A, \alpha, A')
$$

其中：

$$
\mathcal A = (A, \Sigma)
$$

并且其识别森林定义为：

$$
T(A) = \{ t \in F_{\Sigma}(X) \mid t^{\mathcal A}(\alpha) \in A' \}
$$

上式中的符号逐项解释如下：

1. `\mathcal A = (A,\Sigma)` 是有限 `\Sigma`-algebra。
2. `A` 是有限状态集。
3. `X` 是 frontier alphabet，也就是叶子符号集。
4. `\alpha : X \to A` 是初始赋值，把叶子映射到状态。
5. `A' \subseteq A` 是 final-state set。
6. `F_{\Sigma}(X)` 是由 ranked alphabet `\Sigma` 和 frontier alphabet `X` 生成的全部树。
7. `t^{\mathcal A}(\alpha)` 表示在代数 `\mathcal A` 中对树 `t` 进行自叶到根求值后的状态。

书中还等价地写成：

$$
T(A) = A' \hat{\alpha}^{-1}
$$

其中 `\hat{\alpha}` 是把 `\alpha` 扩展为从自由树代数到状态代数的同态。

### 一个最小例子与通俗解释

书里给出的经典最小例子是布尔表达式求值。令 `\Sigma` 包含 `\neg,\land,\lor`，状态集取 `{0,1}`，叶子 `x,y` 通过 `\alpha` 分别映射到真假值。这样一棵布尔表达式树从叶子开始向上规约，最后根节点落到 `1` 就接受。

通俗地说，`Tree Automata` 像“自底向上的语法检查器”。普通 `FA` 是沿字符串一格一格走，这里则是先判断每棵子树是什么类型，再把整棵树逐层折叠成一个最终状态。

### 运行 / 接受 / 转移语义

书中对 frontier-to-root recognizer 的运行可以理解为：

1. 叶子节点先由 `\alpha` 或常元在状态代数中取值。
2. 内部节点依据其符号和子树状态被规约成新状态。
3. 根节点最终落入 `A'` 时接受。

可把它写成：

$$
t \in T(A) \iff t^{\mathcal A}(\alpha) \in A'
$$

书中进一步比较了四类 recognizer：

1. deterministic frontier-to-root
2. nondeterministic frontier-to-root
3. nondeterministic root-to-frontier
4. deterministic root-to-frontier

其中前三类识别能力相同，而 deterministic root-to-frontier 明显更弱。

### 语义边界

与普通 `Finite Automata` 相比，增强点在于对象从串变成树；与 `Pushdown Automata` 相比，它描述的是显式树对象而不是线性输入上的栈行为；与 infinite-tree automata 相比，它仍然只处理有限树 / forest。

### 关键性质与判定边界

书中系统整理了 recognizable forests 的核心问题：

$$
\text{Emptiness}(A):\ T(A)=\emptyset\ ?
$$

$$
\text{Finiteness}(A):\ |T(A)|<\infty\ ?
$$

$$
\text{Equiv}(A,B):\ T(A)=T(B)\ ?
$$

并证明最小 recognizer 存在且在同构意义下唯一，可压缩成：

$$
\forall T,\ \exists A_{\min}\ \text{such that } T(A_{\min}) = T
$$

这些结论说明 tree automata 不只是定义干净，而且最小化和判定问题也有成熟理论。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 支持 | 用有限状态给子树分类。 |
| 事件 / 触发 | 不适用 | 核心输入是树节点而非事件流。 |
| 守卫 / 数据 | 不支持 | 原始模型不强调变量守卫。 |
| 层次 | 强支持 | 层次来自树对象本身。 |
| 并发 / 同步 | 不支持 | 不是并发网模型。 |
| 时间约束 | 不支持 | 无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 纯离散有限树识别。 |
| 可执行 / 可验证性 | 强支持 | emptiness、finiteness、equivalence、最小化体系完整。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原书意义 |
|---|---|---|
| recognizer 骨架 | `$A=(\mathcal A,\alpha,A')$` | 用有限代数和叶子赋值定义树识别器。 |
| 识别森林 | `$T(A)=\{t\in F_{\Sigma}(X)\mid t^{\mathcal A}(\alpha)\in A'\}$` | tree language 的核心定义。 |
| recognizer 比较 | `F-det \equiv F-nondet \equiv R-nondet` | 三类 recognizer 识别能力相同。 |
| 弱分支 | `R-det \subsetneq Rec` | deterministic root-to-frontier 更弱。 |
| 最小化 | `$\exists A_{\min}$` | 最小 recognizer 存在且唯一到同构。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 选定 ranked alphabet `\Sigma` 与 frontier alphabet `X`。
2. 定义有限状态代数 `\mathcal A`。
3. 给出初始赋值 `\alpha` 和 final states `A'`。

### 机器可处理承载方式

其机器可处理承载方式是代数运算、tree recognizer 和 grammar，而不是工程化交换格式。

### 交换与互操作

它和 context-free languages、tree grammars、tree transducers、logic、term rewriting 都有强互操作。

## 配套基础设施

- 建模/编辑工具：原书不绑定具体编辑器。
- 解析/交换/元模型支持：以自由树代数、recognizer 和 grammar 为主。
- 仿真/执行支持：本质是自底向上的树求值与识别。
- 验证/分析支持：emptiness、finiteness、equivalence、最小化和 recognizability 判定很成熟。
- 代码生成/转换支持：后续可连到 tree transducers，但原书重点是理论骨架。
- 标准化或社区生态：是后续 `TATA`、XML/tree language 与 tree-transducer 线的经典母体。

## 适用场景与需求前提

### 适用场景

适用于抽象语法树、项结构、层次文档、树形约束和任何“对象天然是树而不是串”的语言识别问题。

### 需求前提

1. 输入对象需要显式树结构。
2. 关键语义来自子树组合，而不是线性次序。
3. 不需要时间、并发或连续动态。

### 不适用或高成本场景

若需求对象是协议事件流、资源并发或实时控制器，tree automata 不是直接主线。

## 与相邻形式主义的关系

相对 `Finite Automata`，它把对象从词推广到树；相对 [tree-automata-techniques-and-applications/desc.md](../tree-automata-techniques-and-applications/desc.md)，这本书更早、更基础，是经典母体条目；相对 [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)，它处理的是有限树而非 infinite-tree 接受。

## 与本研究的关系

### 对 Project 1 的价值

它把演化树里的 `Tree Automata` 节点从 2008 的后期教程条目往前推回到了经典母体时期，更符合“先扩充演化树，再围绕分支补代表条目”的目标。

### 作为目标形式主义还是中间表示

当需求天然是层次结构对象时可以作为目标形式主义；在控制系统主线中更常作为旁支理论节点或中间抽象。

### 对需求到模型生成的启发

它提示我们：如果需求对象是语法树、配置树或层次文档，就不该硬压成线性事件流，而应直接选择 tree-language 家族。

### 现实限制

工程标准和直接可执行工具不如 `UML/SCXML` 这类 DSL 明显，但理论表达力和判定性非常成熟。

## 重要的相关工作

### 奠基或前身工作

- [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)

### 同类型或同家族工作

- [tree-automata-techniques-and-applications/desc.md](../tree-automata-techniques-and-applications/desc.md)
- [decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md](../decidability-of-second-order-theories-and-automata-on-infinite-trees/desc.md)

### 标准 / 格式 / 工具链工作

- 原书没有工程标准，但为后续 tree grammar / tree transducer / XML 线提供了母体定义。

### 与本研究关系最紧的工作

- 它是状态机族演化树里 `Tree Automata` 节点更合适的经典代表条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Tree Automata
- 论文角色：教程专著
- 核心功能：用 tree recognizer 识别 finite trees / recognizable forests，并系统整理其最小化与判定理论。
- 关键特性：frontier-to-root / root-to-frontier、recognizable forests、最小化、等价与判定问题。
- 构造方式：有限 `\Sigma`-algebra + frontier assignment + final states。
- 基础设施：理论骨架成熟，但无工程化标准/工具。
- 适用场景：树结构语言、语法树、项结构和层次文档约束分析。
- 需求前提：对象必须天然是树，且核心语义来自子树组合而不是线性扫描。
- 状态：🟢

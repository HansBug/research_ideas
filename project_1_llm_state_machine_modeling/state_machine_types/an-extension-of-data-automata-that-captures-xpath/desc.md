# 能够刻画 XPath 的数据自动机扩展 / An extension of data automata that captures XPath

## 基本信息

- 标题：An extension of data automata that captures XPath
- 中文标题：能够刻画 XPath 的数据自动机扩展
- 作者：Mikołaj Bojańczyk，Sławomir Lasota
- 发表：*Logical Methods in Computer Science*, 8(1:5):1-28, 2012
- DOI：`10.2168/LMCS-8(1:5)2012`
- 链接：https://doi.org/10.2168/LMCS-8(1:5)2012
- 形式主义：`Class Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / XPath 捕获
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是输入树字母表 `\Sigma`、工作字母表 `\Gamma`、letter-to-letter tree transducer `f`、以及定义在 `\Gamma \times \{0,1\}` 上的 regular tree language class condition。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 data tree、first-child / next-sibling 语义稳定性、transducer 输出树 `s` 与按 class 打标签后的 `s \otimes X`。

## 简报

这篇论文提出了 `Class Automata`，它的核心跳跃不是再把 data-word 自动机往前推一点，而是把“对每个数据类单独检查”的思想从字线性对象推广到数据树，并且让 class condition 能看到整棵输出树加一层 `0/1` class mask。这样一来，`Class Automata` 不再只是 `Data Automata` 的小修小补，而是一个足以捕获 unary `XPath` 查询的更强树模型。代价也很直接：它比 `Data Automata` 强得多，以至于一般空性已经不可判定。

- 形式主义定位：`Finite Automata -> Tree Automata -> Data / Infinite-Alphabet Tree` 附近的一条 class-based 树模型分支，同时也是 `Data Automata` 的严格扩展。
- 构造方式简述：先用 nondeterministic letter-to-letter tree transducer 把输入 data tree 转写到工作字母表，再对每个数据类 `X` 检查标注树 `s \otimes X` 是否属于 class condition。
- 基础设施与场景简述：原文纯理论，但它给出了“捕获 XPath”这条非常强的表达力界线，也明确说明了一般空性为何不可判定。

```text
data tree -> tree transducer output -> mark one data class by 0/1 mask -> regular tree language check -> class-quantified acceptance
```

## 形式主义定义与核心对象

### 定义对象

`Class Automata` 处理的是 data trees。每个节点都有一个有限字母表标签以及一个来自无限域的数据值，数据值只允许做相等性测试。论文的主战场是 unranked ordered trees，但明确指出经 first-child / next-sibling 编码后，模型在 binary trees 上同样稳定，因此 words 也只是它的一个特例。

### 核心抽象

原文没有直接给出一个紧凑元组；按照其定义，可保守整理为：

$$
\mathcal C = (\Sigma,\Gamma,f,K)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是输入字母表。
2. `\Gamma` 是工作字母表。
3. `f` 是从 `\Sigma` 到 `\Gamma` 的 nondeterministic letter-to-letter tree transducer。
4. `K` 是定义在 `\Gamma \times \{0,1\}` 上的 regular tree language，作为 class condition。

给定输出树 `s` 和某个数据类 `X`，论文的关键构造是：

$$
s \otimes X \in T_{\Gamma \times \{0,1\}}
$$

上式中的符号逐项解释如下：

1. `s` 是 transducer 在输入树上的某个输出。
2. `X` 是一个数据类，也就是具有相同数据值的节点集合。
3. `s \otimes X` 表示：保留树结构和工作字母 `\Gamma`，并给节点额外打上 `1` 或 `0`，分别表示节点是否属于 `X`。

### 一个最小例子与通俗解释

论文自己的例子之一是“某个数据类中至少有三个 `a` 节点”。`Class Automata` 的做法是：

1. transducer 先在输入树里猜出三个候选 `a` 节点，并把它们标成特殊工作字母。
2. 对每个数据类 `X`，把输出树改写成 `s \otimes X`。
3. class condition 检查：`X` 要么包含全部三个候选点，要么一个也不包含。

通俗地说，`Class Automata` 像“对每个数据值类，把整棵树重新看一遍，只是额外告诉你哪些节点属于当前这个类”。因此它比 `Data Automata` 强得多，因为 class condition 不再只能看 class 内的线性投影，而是能看整棵结构化上下文。

### 运行 / 接受 / 转移语义

设输入 data tree 为 `(t,\sim)`，其中 `\sim` 给出节点上的 data-equality 类。原文的接受语义可以压成：

$$
(t,\sim) \in L(\mathcal C)
\iff
\exists s \in f(t)\ \forall X \in \mathrm{Class}(t,\sim),\ s \otimes X \in K
$$

上式中的符号逐项解释如下：

1. `f(t)` 是 transducer 对输入树 `t` 产生的所有工作树输出。
2. `\mathrm{Class}(t,\sim)` 是输入树中全部数据类的集合。
3. `s \otimes X \in K` 表示当前数据类 `X` 在该输出树上的 class test 通过。

### 语义边界

`Class Automata` 的增强点在于：

1. 它允许 class condition 看整棵输出树外加 class mask；
2. 因而严格强于仅看 class 子串的 `Data Automata`；
3. 但它也因此不再保留一般空性可判定性。

换句话说，它不是为了“继续保持 decidable emptiness”而设计的，而是为了给 XPath 一类真实树查询语言找到一个自动机对应物。

### 关键性质与判定边界

原文最关键的结论可压成：

$$
\text{Every unary XPath query over data trees can be recognized by a class automaton}
$$

$$
\mathcal L(\mathrm{DA}) \subsetneq \mathcal L(\mathrm{Class\ Automata})
$$

$$
\mathrm{emptiness}(\mathrm{Class\ Automata})\ \text{undecidable}
$$

$$
\mathcal L(\mathrm{Class\ Automata})\ \text{is closed under } \cup,\ \cap,\ \text{relabelings and inverse relabelings}
$$

上面几式中的符号逐项解释如下：

1. 第一式是本文的主结果，也解释了为什么模型一定会很强。
2. 第二式来自它对 `Data Automata` 的严格推广。
3. 第三式说明它更适合表达力与不可表达性分析，而不是直接做一般空性分析。
4. 第四式说明作为“表达力载体”它仍有不错的代数稳定性。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 通过 tree transducer 与 regular tree language 提供有限控制。 |
| 事件 / 触发 | 中等支持 | 主要对象是树节点与 class mask，而不是事件流。 |
| 守卫 / 数据 | 强支持 | 核心是按数据类逐个检查 `s \otimes X`。 |
| 层次 | 强支持 | 主对象就是 unranked / ordered data trees。 |
| 并发 / 同步 | 不支持 | 无显式并发组合算子。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散树模型。 |
| 可执行 / 可验证性 | 强表达力但空性受限 | evaluation 可做，闭包好，但一般 emptiness 不可判定。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 保守元组 | `$\mathcal C=(\Sigma,\Gamma,f,K)$` | 由输入字母表、工作字母表、tree transducer 与 class condition 组成。 |
| class-marked tree | `$s \otimes X$` | 这是区别于 `DA` 的关键对象。 |
| 接受语义 | `$\exists s\in f(t)\ \forall X,\ s\otimes X\in K$` | 对每个数据类逐个检查。 |
| XPath 捕获 | `$\text{XPath} \le \text{Class Automata}$` | 主结果。 |
| 空性边界 | `$\mathrm{emptiness}$ undecidable` | 表达力上升的直接代价。 |

## 构造方式与承载格式

### 建模入口

1. 先确定目标对象是 data tree，而不是纯 data word。
2. 再选择 tree transducer 要在输出树上暴露哪些结构特征。
3. 最后把“对每个数据类要检查什么”写成 regular tree language `K` 对 `s \otimes X` 的要求。

### 机器可处理承载方式

机器可处理承载方式是：

1. data tree；
2. letter-to-letter tree transducer `f`；
3. 工作树 `s`；
4. class-masked 树 `s \otimes X`；
5. regular tree language `K`。

原文没有 XML Schema、JSON 或工程 DSL。

### 交换与互操作

它与 [tree-automata/desc.md](../tree-automata/desc.md) 的 regular tree language 主线直接相接，但多了一层 data-class 量化；与 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 的 `Data Automata` 相比，差别就落在 class condition 是否能看到整棵树；而 [a-decidable-extension-of-data-automata/desc.md](../a-decidable-extension-of-data-automata/desc.md) 又可以看作对这条 class-automata 线路做可判定收束。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 tree transducer、regular tree languages、以及 class mask 语义。
- 仿真/执行支持：evaluation 问题可做，原文指出 even 对固定 automaton 也是 NP-complete。
- 验证/分析支持：适合做 XPath 表达力、不可表达性与受限输入下的可判定性分析。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 data-tree / XPath 静态分析与 class-based automata 之间的经典桥梁。

## 适用场景与需求前提

### 适用场景

适合 XML / data-tree 上那类“对每个数据值类都要满足一个结构化树模式”的需求，例如 XPath 数据相等查询、文档静态分析、class-sensitive tree property 检查。

### 需求前提

1. 对象必须天然是树或可稳定编码成树。
2. 数据关系以 equality class 为核心。
3. 需求需要同时看树结构与 class 外围上下文，而不是只看 class 内线性投影。

### 不适用或高成本场景

若实际目标是一般可判定验证，而不是表达力分析，那么 `Class Automata` 往往太强；此时更适合退回 `Data Automata`、`WDA`、`PCA` 或其他 decidable 子类。

## 与相邻形式主义的关系

相对 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 中的 `Data Automata`，`Class Automata` 让 class condition 从“只看 class 子串”升级到“看整棵带 mask 的树”；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，它不是一寄存器线程模型，而是 transducer + regular tree condition 路线；相对 [a-decidable-extension-of-data-automata/desc.md](../a-decidable-extension-of-data-automata/desc.md)，后者是在这条 class-based 线路上重新施加限制以恢复 decidability。

## 与本研究的关系

### 对 Project 1 的价值

它让当前演化树的 data-tree 一侧第一次有了一个明确命名、且能直接挂接 XPath 的 class-based 模型节点，而不是只停在 `BUDA / ODTA` 这类更专门的树自动机上。

### 作为目标形式主义还是中间表示

更适合作为理论分析节点和表达力参照物，而不是控制系统自动建模的最终交付形式。

### 对需求到模型生成的启发

如果需求里充满“某类对象的所有节点都必须满足结构模式”这类叙述，LLM 可以先判断是否实际上需要 class-quantified tree semantics；若需要，这一支能帮助判定该需求是否已超出一般 decidable data-tree 模型。

## 重要的相关工作

1. [tree-automata/desc.md](../tree-automata/desc.md)：regular tree language 母线。
2. [a-decidable-extension-of-data-automata/desc.md](../a-decidable-extension-of-data-automata/desc.md)：对 `Class Automata` 加优先级限制以恢复 emptiness decidability。
3. [bottom-up-automata-on-data-trees-and-vertical-xpath/desc.md](../bottom-up-automata-on-data-trees-and-vertical-xpath/desc.md)：另一条 data-tree 自动机路线。

## 文献分类总结

- 形式主义：`Class Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / XPath 捕获

# 关于无限字母表上双卵石自动机的说明 / A Note on Two-pebble Automata Over Infinite Alphabets

## 基本信息

- 标题：A Note on Two-pebble Automata Over Infinite Alphabets
- 中文标题：关于无限字母表上双卵石自动机的说明
- 作者：Michael Kaminski, Tony Tan
- 发表：*Fundamenta Informaticae*, 98(4):379-390, 2010
- DOI：`10.3233/FI-2010-234`
- 链接：https://doi.org/10.3233/FI-2010-234
- 形式主义：`Two-Pebble Automata over Infinite Alphabets (2-PA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：子类边界 / 判定性分化
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `k`-PA 的 transition set `\mu`、configuration `[i,q,\mu]`、以及把整数等式编码成 permutation language 的构造。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是带端标记与分隔符 `$` 的无限字母表词、pebble assignment、以及 `2-PA/3-PA` 的对比分界。

## 简报

这篇论文的价值，在于把 infinite-alphabet pebble family 从“有一条总母线”推进到“至少有一个严格可命名的子类节点”。它并不重新发明 pebble automata，而是把 `2-PA` 单独拎出来，证明这个看似更弱的小分支已经足够强到让空性不可判定，同时又严格弱于 `3-PA`。因此它非常适合作为当前演化树里 `Pebble Automata over Infinite Alphabets -> Two-Pebble Automata` 这条支线的代表条目。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet -> Pebble Automata over Infinite Alphabets` 下的明确子类节点。
- 构造方式简述：在输入词上始终只允许两枚 pebbles 按栈纪律工作，通过 equality / co-location 检测与 delimiter `$` 组织复杂的 permutation-style 编码。
- 基础设施与场景简述：原文纯理论，但给出了 `2-PA` 的 arithmetic encoding、不可判定空性和 `2-PA < 3-PA` 的严格分层。

```text
无限字母表词 -> 两枚栈式 pebbles -> permutation / equality encoding -> 判定边界与层级分化
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是来自无限字母表 `\Sigma` 的有限字符串，并在输入左右添加端标记，同时使用 `$` 作为内部段落分隔符。模型关心的不是数值计算，而是“某个符号在不同区段是否是同一名字”“若干区段是否互为排列”这类 equality-only 结构。

### 核心抽象

论文先回顾一般 `k`-pebble automaton，然后把结果聚焦到 `k=2`。一般 `k`-PA 写成：

$$
A = \langle Q, q_0, F, \mu \rangle
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `q_0 \in Q` 是初始状态。
3. `F \subseteq Q` 是接受状态集。
4. `\mu` 是有限转移集。

转移的源侧有两种形状：

$$
(i,a,P,V,q) \to (q',\mathrm{action}), \qquad
(i,P,V,q) \to (q',\mathrm{action})
$$

上式中的符号逐项解释如下：

1. `i \in \{1,\ldots,k\}` 是当前活跃 pebble 的编号。
2. `a` 是当前读到的字母，允许取输入符号或左右端标记。
3. `P` 记录有哪些更外层 pebbles 与当前 pebble 位于同一输入位置。
4. `V` 记录有哪些更外层 pebbles 看到与当前 pebble 相同的数据值。
5. `q,q'` 是源状态与目标状态。
6. `\mathrm{action}` 属于 `\{\mathrm{left},\mathrm{right},\mathrm{place\text{-}pebble},\mathrm{lift\text{-}pebble}\}`。

在 `2-PA` 情形里，当前 configuration 写成：

$$
[i,q,\mu]
$$

其中 `i \in \{1,2\}`，而 pebble assignment `\mu : \{1,\ldots,i\}\to\{0,1,\ldots,n,n+1\}` 记录每枚已放下 pebble 在输入 `/w.` 上的位置。

### 一个最小例子与通俗解释

原文的第一个直观例子是语言

$$
L_{\mathrm{diff}} = \{ a_1\cdots a_n \mid a_i \neq a_j \text{ for all } i\neq j \}
$$

也就是“所有符号都互不相同”的词。`2-PA` 的做法是：

1. pebble `1` 从左到右走过每个位置。
2. 每到一个位置，就放下 pebble `2` 扫描整条词。
3. 若 pebble `2` 在其他位置又看到了同一个符号，则拒绝。

通俗地说，`2-PA` 像“一个检查员带一根当前指针和一个回看探针”。第一枚 pebble 固定当前比较基准，第二枚 pebble 负责把整条输入再扫一遍做对照。虽然只有两枚 pebbles，但已经足以做很多超出半线性语言直觉的事情。

### 运行 / 接受 / 转移语义

原文把一步转移写成：

$$
[i,q,\mu] \vdash [i',q',\mu']
$$

其语义来自某条可用转移 `\alpha \to (q',\mathrm{action})`。其中：

1. `\mathrm{left}` 让当前 pebble 左移一格。
2. `\mathrm{right}` 让当前 pebble 右移一格。
3. `\mathrm{place\text{-}pebble}` 让深度从 `i` 变成 `i+1`，新 pebble 放在当前 pebble 所在位置附近的标准起点。
4. `\mathrm{lift\text{-}pebble}` 让深度回退到 `i-1`。

接受语义是：从初始 configuration

$$
[1,q_0,\mu_0(1)=0]
$$

出发，经过若干步达到某个 `q \in F` 的 configuration 即接受。

### 语义边界

这篇论文给 `2-PA` 划出的边界非常鲜明：

1. 它仍然只是两枚栈式 pebbles，不是任意多 pebbles。
2. 它已经能编码整数相等、加法、乘法等 Diophantine-style 结构。
3. 它仍然做不到某些需要第三枚 pebble 才能稳定表达的有序配对语言。
4. 因此它既不是“太弱的小玩具”，也还不是一般 `k`-PA 的全部能力。

### 关键性质与判定边界

原文最重要的主结论可以直接写成：

$$
\mathrm{emptiness}(2\text{-}\mathrm{PA}) \text{ undecidable}
$$

论文的证明路线，是把 Hilbert 第十问题约化到 `2-PA` 空性。支撑这个结论的关键中间事实，是 `2-PA` 能接受若干基于排列编码的整数语言，例如加法与乘法约束。

第二个关键结论是严格层级：

$$
2\text{-}\mathrm{PA} \subsetneq 3\text{-}\mathrm{PA}
$$

原文用语言 `L_{\mathrm{ord}}` 给出分离，其中：

$$
L_{\mathrm{ord}} = \{ a_1\cdots a_n\$a_1\cdots a_n \mid n\ge 1,\ a_i\neq a_j\ (i\neq j),\ a_i\neq \$ \}
$$

它可被 `3-PA` 接受，但不能被 `2-PA` 接受。

此外，论文沿用前作结果指出，对固定 `k`：

$$
\text{two-way nondeterministic } k\text{-PA} \equiv \text{one-way deterministic } k\text{-PA}
$$

这说明 `2-PA` 的关键强度并不来自双向性本身，而来自 pebble 机制和 equality 编码。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍保留有限控制骨架。 |
| 事件 / 触发 | 强支持 | 输入是线性词，逐位置扫描。 |
| 守卫 / 数据 | 强支持 | 通过两枚 pebbles 做 equality / position 对照。 |
| 层次 | 不支持 | 对象不是树。 |
| 并发 / 同步 | 不支持 | 单串上的顺序模型。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 分层严格、空性不可判定、编码能力清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=\langle Q,q_0,F,\mu\rangle$` | `k`-PA 的标准骨架。 |
| 配置 | `$[i,q,\mu]$` | 当前活跃 pebble、状态和 pebble assignment。 |
| 空性边界 | `$\mathrm{emptiness}(2\text{-}\mathrm{PA})$ undecidable` | 两枚 pebbles 已足够强到不可判定。 |
| 严格层级 | `$2\text{-}\mathrm{PA}\subsetneq 3\text{-}\mathrm{PA}$` | `2-PA` 是稳定子类而非一般 `PA` 的同义写法。 |
| 分离语言 | `$L_{\mathrm{ord}}\in 3\text{-}\mathrm{PA}\setminus 2\text{-}\mathrm{PA}$` | 用具体 family node 证明 strictness。 |

## 构造方式与承载格式

### 建模入口

1. 先确认需求是否真是 two-pebble 级别的回看与排列比较，而不是任意深度的 pebble 栈。
2. 用 pebble `1` 表示“当前主位置”，用 pebble `2` 表示“回看扫描器”。
3. 若需要三层以上的嵌套书签，再转向一般 `k`-PA` 或其他更强模型。

### 机器可处理承载方式

机器可处理承载方式是：

1. `2-PA` 转移表 `\mu`；
2. configuration 语义 `[i,q,\mu]`；
3. 基于 delimiter `$` 的区段编码；
4. permutation-style word encodings。

原文没有 XML、JSON、DSL 或标准文件格式。

### 交换与互操作

它与更一般的 infinite-alphabet pebble 母线直接相连，而与后续可判定子类的关系同样重要：前者告诉我们 family 的基准强度，后者告诉我们如何把模型重新压回可判定区间。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 transition relation、pebble assignment 和 permutation encoding。
- 仿真/执行支持：可按 configuration 语义直接运行。
- 验证/分析支持：Hilbert 第十问题约化、strict hierarchy 证明与半线性边界分析是主线。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：属于 infinite-alphabet pebble automata 的经典理论分支节点。

## 适用场景与需求前提

### 适用场景

适合以下理论场景：

1. 线性 data-word 上的回看 / 排列 / equality pattern 分析。
2. 需要明确区分 `2-PA` 与更一般 `k`-PA` 的谱系建设。
3. 需要一个已证明“仍不可判定，但又严格低于 `3-PA`”的中间节点。

### 需求前提

1. 输入必须是线性词。
2. 数据关系最好只依赖 equality 与区段排列。
3. 需求确实能用两层位置书签表达，而不是依赖无界数量的同时活跃回看点。

### 不适用或高成本场景

若需求只关心固定少量名字记忆，`RA/FMA` 更轻；若需求要可判定空性，`Top-View Weak PA` 更合适；若需求需要树结构或时间信息，`2-PA` 也不是终点。

## 与相邻形式主义的关系

相对 [towards-regular-languages-over-infinite-alphabets/desc.md](../towards-regular-languages-over-infinite-alphabets/desc.md)，这篇论文把 `PA` 总母线收紧成明确的 `2-PA` 子节点；相对 [on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md](../on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md)，这里还是 full `2-PA`，尚未施加 top-view 限制，因此空性仍不可判定；相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md) 与 [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)，它依赖位置 pebbles 而非寄存器式名字存储。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Pebble Automata over Infinite Alphabets` 这条支线从“只有总母线和后续可判定弱化版”推进到“有一个严格命名的中间子类节点”，便于后续继续补 `3-PA`、top-view 弱化线和其他分层结果。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点和表达力边界参照，而不是控制系统主线的最终建模语言。

### 对需求到模型生成的启发

如果需求里出现“固定一个位置，再整段扫另一段做排列或 equality 检查”的模式，LLM 可以考虑这是 `2-PA` 级别的结构；若需求只需要有限名字缓存，则不必上 pebble family。

### 现实限制

原文没有工程生态，且空性已不可判定，因此它在本研究中的价值主要是谱系与能力边界，而不是直接可执行性。

## 重要的相关工作

### 奠基或前身工作

- [towards-regular-languages-over-infinite-alphabets/desc.md](../towards-regular-languages-over-infinite-alphabets/desc.md)

### 同类型或同家族工作

- [on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md](../on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合在主蓝本树中作为 `Pebble Automata over Infinite Alphabets` 之下 `Two-Pebble Automata` 子节点的代表条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Two-Pebble Automata over Infinite Alphabets (2-PA)`
- 论文角色：子类边界 / 判定性分化
- 核心功能：把 infinite-alphabet pebble family 细化成严格可命名的 `2-PA` 子类，并给出其不可判定空性与 `2-PA < 3-PA` 分层。
- 关键特性：双 pebble 回看、排列编码、Hilbert 第十问题约化、严格层级。
- 构造方式：`\langle Q,q_0,F,\mu\rangle` 元组加 configuration `[i,q,\mu]` 与 `place/lift/move` 规则。
- 基础设施：纯理论模型，无工程标准或工具；核心在于 permutation encoding 与判定问题分析。
- 适用场景：data-word equality / permutation 理论分析、pebble family 分层建设。
- 需求前提：输入是线性词，核心关系主要是 equality 与区段排列，且两层位置书签足够表达目标约束。
- 状态：🟢

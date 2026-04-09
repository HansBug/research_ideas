# Owl：用于 $\omega$-词、自动机与 LTL 的库 / Owl: A Library for $\omega$-Words, Automata, and LTL

## 基本信息

- 标题：Owl: A Library for $\omega$-Words, Automata, and LTL
- 中文标题：Owl：用于 $\omega$-词、自动机与 LTL 的库
- 作者：Jan Křetínský，Tobias Meggendorfer，Salomon Sickert
- 发表：*Automated Technology for Verification and Analysis*，`LNCS 11138`，pp. 543-550，2018
- DOI：`10.1007/978-3-030-01090-4_34`
- 链接：https://doi.org/10.1007/978-3-030-01090-4_34
- 形式主义：`omega-automata / LTL / Owl / HOA/TLSF infrastructure`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：`omega` 自动机与 `LTL` 统一库 / `CLI + Java/C++ API` 工具基础设施
- 工具/实现获取方式：原文明确给出 `Owl` 的 command-line interface、Java API、specialized `C++` API、server mode、testing infrastructure 与 `JBDD` 支撑；同时说明它已作为 `Rabinizer 4`、`Strix`、`MoChiBa` 等工具的底座使用。
- 标准/格式获取方式：原文明确支持 Spot 风格 `LTL`、`TLSF` 与 `HOA`，并强调 transition-based acceptance、pipe-style CLI 与 automata serialization；不是新的行业标准，而是标准格式与转换算法的承载层。

## 简报

这篇论文的核心价值，不是提出新的 $\omega$-automata 本体，而是把 `LTL` 解析、重写、`omega` 自动机表示、acceptance 改写、格式互操作和工具级测试，压成一套真正适合反复复用的库。`Owl` 的定位很明确：让“从 `LTL` 到不同 `omega` 自动机”的研究工具不必每次从 parser、BDD、CLI、HOA serializer 和 on-the-fly traversal 重新造轮子。

- 形式主义定位：`LTL` 与 `omega` 自动机算法/工具的底层基础设施，而不是新的状态机族主蓝本。
- 构造方式简述：以 Java 库为核心，同时暴露 pipe-style CLI、server mode 和 specialized `C++` API；内部统一处理 `LTL`、`TLSF`、多类 acceptance 与 explicit / implicit automata。
- 基础设施与场景简述：依托 `HOA`、`TLSF`、`JBDD`、`ltlcross` 和 on-the-fly traversal，服务 `LTL` 翻译、概率模型检查、合成和 automata-theoretic verification。

```text
LTL / TLSF -> Owl parser + simplifier -> omega-automata constructions -> HOA / API output -> model checking / synthesis / benchmarking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `LTL` parser、simplifier 与 normal-form processing；
2. deterministic / nondeterministic `omega` automata；
3. transition-based acceptance；
4. explicit 与 implicit automaton representations；
5. `HOA` / `TLSF` / CLI / API / testing infrastructure。

### 核心抽象

对 `Owl` 而言，最核心的工作对象可以保守整理为：

$$
A = (Q, q_0, \Sigma, \delta, \mathrm{Acc})
$$

上式中的符号逐项解释如下：

1. `$Q$` 是自动机状态集合。
2. `$q_0$` 是初始状态。
3. `$\Sigma$` 是字母表；在 `LTL` 翻译场景里通常来自 atomic propositions 的 valuation。
4. `$\delta$` 是转移关系；`Owl` 同时支持 explicit 存储和 implicit successor computation。
5. `$\mathrm{Acc}$` 是接受条件，原文强调支持 Büchi、co-Büchi、Rabin、parity、generalized Rabin、Emerson-Lei 等多种形式。

论文也把 `LTL` 到自动机的翻译看成统一接口：

$$
\tau : \mathrm{LTL} \to \mathrm{Aut}_\omega
$$

上式中的符号逐项解释如下：

1. `$\mathrm{LTL}$` 是线性时序逻辑公式集合。
2. `$\mathrm{Aut}_\omega$` 是一族以无限词为对象的自动机。
3. `$\tau$` 不是单一算法，而是 `Owl` 用统一基础设施承载的多条翻译链。

论文还直接强调 `LTL` expansion laws，例如：

$$
a \mathbin{U} b \equiv b \lor (a \land X(a \mathbin{U} b))
$$

上式中的符号逐项解释如下：

1. `$a$` 与 `$b$` 是命题公式。
2. `$U$` 是 until 算子。
3. `$X$` 是 next 算子。
4. 这类重写是 `Owl` parser / simplifier / semantic translation 的基础。

对接受语义，可保守写成：

$$
L(A) = \{\, w \in \Sigma^\omega \mid \mathrm{run}_A(w) \models \mathrm{Acc} \,\}
$$

上式中的符号逐项解释如下：

1. `$\Sigma^\omega$` 是无限词集合。
2. `$\mathrm{run}_A(w)$` 是自动机在词 `$w$` 上的运行。
3. `$\models \mathrm{Acc}$` 表示该运行满足给定接受条件。
4. 这说明 `Owl` 面向的是 infinite-word automata，而不是普通有限词自动机。

### 一个最小例子与通俗解释

论文给出的典型使用方式是：

1. 从 stdin 或文件读入一条 `LTL` 公式。
2. 先做 simplification。
3. 再调用如 `ltl2dpa`、`ltl2dgra` 之类的翻译器。
4. 最后把结果写成 `HOA`。

最小例子可以写成：

```text
owl ltl --- simplify-ltl --- ltl2dpa --- hoa
```

通俗地说，`Owl` 像“`omega` 自动机世界的通用底盘”。如果你要做 `LTL -> DPA`、`LTL -> DGRA`、`LTL -> Emerson-Lei automata`、甚至把结果继续送到合成或概率模型检查后端，`Owl` 帮你把 parser、格式、acceptance、遍历和测试都先搭好。

### 运行 / 接受 / 转移语义

论文特别强调 implicit automata 的 on-the-fly 语义。对某个状态 `$q$` 和输入 valuation `$a$`，可以把后继抽象为：

$$
\delta(q, a) \subseteq Q
$$

上式中的符号逐项解释如下：

1. `$q$` 是当前状态。
2. `$a$` 是当前字母或命题 valuation。
3. `$\delta(q,a)$` 是可能的后继集合。
4. 当自动机以 implicit 方式表示时，`Owl` 并不要求预先把整个状态空间全部显式展开。

这带来一个关键工程性质：

$$
\mathrm{Reach}(A, w[0..i]) \text{ 可以按需增量计算}
$$

上式中的符号逐项解释如下：

1. `$w[0..i]$` 是输入前缀。
2. `$\mathrm{Reach}(A,\cdot)$` 表示可达状态集合。
3. “按需增量计算”对应论文反复强调的 on-the-fly traversal 和 incremental exploration。

### 语义边界

这篇论文的边界很清楚：

1. 它处理的是 `LTL` 与 `omega` 自动机工具基础设施，不是前端控制建模语言。
2. 它擅长翻译、重写、acceptance 操作与互操作，不解决工业控制器图形建模问题。
3. 它更多服务 verification / synthesis back-end，而不是直接面向状态机建模者的最终交付格式。
4. 它处理的是 infinite-word object；若问题是 timed / hybrid / hierarchical control semantics，本体仍在别处。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `omega` 自动机骨架 | `$A = (Q, q_0, \Sigma, \delta, \mathrm{Acc})$` | 统一了承载多类 acceptance 的基础对象。 |
| `LTL` 翻译接口 | `$\tau : \mathrm{LTL} \to \mathrm{Aut}_\omega$` | 说明 `Owl` 的中心任务是承载多条翻译链。 |
| expansion law | `$a U b \equiv b \lor (a \land X(a U b))$` | 支撑 parser/simplifier 与 semantic constructions。 |
| 无限词接受语义 | `$L(A)=\{w\in\Sigma^\omega \mid \mathrm{run}_A(w)\models \mathrm{Acc}\}$` | 说明对象是 infinite-word automata。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 面向 deterministic / nondeterministic `omega` automata。 |
| 事件 / 触发 | 中等支持 | 核心是词上的 valuation，不是 richer controller event calculus。 |
| 守卫 / 数据 | 弱支持 | 不面向 data guards，本体仍是 word/logical valuation。 |
| 层次 | 不支持 | 不是 hierarchical state-machine tool。 |
| 并发 / 同步 | 间接支持 | 主要通过 product/translation 支持，而非显式并发语言。 |
| 时间约束 | 不支持 | 不属于 timed automata family。 |
| 连续动态 / 随机性 | 不支持 | 不处理 hybrid/CPS 动力学。 |
| 可执行 / 可验证性 | 很强 | `CLI`、`Java/C++ API`、`HOA`、测试框架和 `BDD` 支撑都到位。 |

### 形式化问题与性质

1. `Owl` 真正补的是“翻译链公共底层”，而不是单个新 automaton family。
2. transition-based acceptance、implicit successor computation 和 `HOA/TLSF` 互操作，是它对工具生态最核心的贡献。
3. 它让 `Rabinizer`、`Strix`、`MoChiBa` 这类工具能够共用一套稳定基础设施，而不是各自重复实现 parser/BDD/serializer。

## 构造方式与承载格式

### 建模入口

`Owl` 的典型入口有：

1. Spot 风格 `LTL` 文本；
2. `TLSF` synthesis specification；
3. `HOA` automata text format；
4. Java / `C++` API 调用。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `LTL` AST、normal forms 与 rewrite results；
2. explicit / implicit `omega` automata structures；
3. transition-based acceptance representation；
4. `HOA` serialization；
5. `JBDD`-based symbolic support。

### 交换与互操作

互操作是这篇论文的重点之一：

1. `HOA` 是 automata 交换主格式。
2. `TLSF` 用于 synthesis-side specification ingestion。
3. `CLI` 管线和 server mode 让外部工具能以 shell/socket 方式调用。
4. specialized `C++` API 则让其他高性能工具按状态增量探索 automata。

## 配套基础设施

- 建模/编辑工具：不是图形编辑器，主线是 `CLI`、Java API、specialized `C++` API 与 server mode。
- 解析/交换/元模型支持：`LTL` parser、`TLSF` parser、`HOA` reader/writer、acceptance conversion。
- 仿真/执行支持：不面向控制执行 runtime，但支持 automata traversal、translation pipeline 与工具互调。
- 验证/分析支持：SCC decomposition、lasso emptiness、union/intersection、degeneralization、acceptance simplification。
- 代码生成/转换支持：核心是 logic-to-automata 与 automata-to-automata translations，不是嵌入式代码生成。
- 标准化或社区生态：`HOA`、`TLSF`、`ltlcross`、`JBDD`，以及 `Rabinizer / Strix / MoChiBa` 等基于它的工具生态。

## 适用场景与需求前提

### 适用场景

适合 `LTL` 翻译、`omega` 自动机实验、概率模型检查前端、LTL synthesis 和需要快速原型化 automata-theoretic back-end 的研究工具开发。

### 需求前提

1. 需求已经是 `LTL`、`TLSF` 或可落成 `omega` automata 的逻辑/语言对象。
2. 团队需要的是算法底座与互操作层，而不是图形状态机前端。
3. 使用者愿意接受 `HOA`、`CLI`、API 和 automata library 风格工作流。

### 不适用或高成本场景

如果任务核心是 timed / hybrid controller modeling、工业状态图前端建模或含复杂数据守卫的交互协议本体，`Owl` 不是直接落地的目标语言。

## 与相邻形式主义的关系

相对 [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)，`HOA` 解决的是交换格式，而 `Owl` 解决的是围绕该格式的完整算法与工具底盘；相对 [spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md](../spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md)，两者都做 `LTL/omega` 工具基础设施，但 `Owl` 更强调 Java 生态、semantic constructions 与多工具复用底盘；相对 [rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md](../rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md)，后者是具体翻译器套件，而 `Owl` 是其底层共用库。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提醒我们：很多状态机后端不必自己实现，可以复用成熟 automata-theoretic infrastructure。
2. 如果后续要把 `LTL` 性质、对比自动机、acceptance 转换和模型检查前端串起来，`Owl` 这类库是天然桥梁。
3. 它也说明“统一 CLI/API/format/test infrastructure”本身就是研究工具长期可维护的关键。

### 作为目标形式主义还是中间表示

更适合作为后端中间表示与验证/综合基础设施，而不是控制系统工程师直接编写的前端形式主义。

### 对需求到模型生成的启发

1. 若需求输出最终还要接 `LTL` 性质验证或合成，保留对 `HOA` / `omega` automata 的稳定导出很重要。
2. 单个模型族之外，格式和 acceptance 的统一抽象同样值得提前设计。
3. 前端建模语言与后端 automata 库分层，是后续闭环工具的重要架构模式。

## 重要的相关工作

1. [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)：`omega` 自动机交换格式标准。
2. [spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md](../spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md)：`LTL / omega` 自动机操作框架。
3. [rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md](../rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md)：建立在相同工具底盘上的 deterministic-automata translation suite。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`omega-automata / LTL / Owl / HOA/TLSF infrastructure`
- 论文角色：`omega` 自动机与 `LTL` 统一库 / `CLI + Java/C++ API` 工具基础设施
- 归类理由：论文主体是 `LTL` 与 `omega` 自动机的解析、翻译、格式互操作与 API/CLI 底盘建设，典型属于 automata tooling / infrastructure 条目。

# SMPT：广义 Petri 网可达性方法试验台 / SMPT: A Testbed for Reachability Methods in Generalized Petri Nets

## 基本信息

- 标题：SMPT: A Testbed for Reachability Methods in Generalized Petri Nets
- 中文标题：SMPT：广义 Petri 网可达性方法试验台
- 作者：Nicolas Amat，Silvano Dal Zilio
- 发表：*Formal Methods*，pp. 445-453，2023
- DOI：`10.1007/978-3-031-27481-7_25`
- 链接：https://doi.org/10.1007/978-3-031-27481-7_25
- 形式主义：`generalized Petri nets / reachability formulas / SMPT`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 论文角色：广义 `Petri Net` 可达性验证 portfolio、polyhedral-reduction backend 与 verdict-certificate 基础设施
- 工具/实现获取方式：原文明确给出开源仓库 `https://github.com/nicolasAmat/SMPT`，并说明项目使用 `Python` 实现、采用 `GNU GPL v3.0` 许可。
- 标准/格式获取方式：输入侧支持 `PNML`、colored-net unfolding 与 `MCC` reachability-property XML；内部约束统一转成 `SMT-LIB` 的 `QF-LIA`，不是独立行业标准。

## 简报

这篇论文补的是 `Petri Net` reachability 工具链里一类很实用但经常分散实现的基础设施层。`SMPT` 不主张重新定义新的网语义，而是把 generalized `Petri Net` 的可达性、不可达性、归纳不变式、polyhedral reduction、`SMT` 求解和 verdict certificate 串成统一试验台，使不同方法能在相同输入、相同 reduction、相同调度框架下并行比较。

- 形式主义定位：广义 `Petri Net` reachability 的工具与求解基础设施，而不是新的 `Petri Net` 母型。
- 构造方式简述：`PNML / MCC property -> optional Reduce polyhedral reduction -> QF-LIA encoding -> portfolio checkers -> verdict / counterexample / certificate`。
- 基础设施与场景简述：依托 `Python`、`z3`、`MiniZinc`、`Tina` 的 `Reduce/walk`、以及并行 jobs scheduler，服务 generalized `Petri Net` reachability、`MCC` 风格 benchmark 与方法对比实验。

```text
generalized Petri net + reachability formula -> reduction / SMT encoding -> parallel checkers -> invariant proof or witness
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 广义 `Petri Net` 及其 marking。
2. 以线性约束组合表示的 reachability / invariant 公式。
3. 结构约简与 polyhedral reduction。
4. 归纳不变式与 verdict certificate。
5. `BMC / k-induction / PDR / state equation / random walk / enumeration` 组成的 portfolio。

### 核心抽象

论文默认继承标准 `Petri Net` 记号；结合文中“marked net `(N;m_0)`”的写法，可把工具处理对象保守整理为：

$$
(N;m_0),\quad N = (P,T,\mathrm{Pre},\mathrm{Post})
$$

上式中的符号逐项解释如下：

1. `$P$` 是 places 集合。
2. `$T$` 是 transitions 集合。
3. `$\mathrm{Pre}$` 与 `$\mathrm{Post}$` 分别给出弧权重。
4. `$m_0 : P \to \mathbb{N}$` 是初始 marking。
5. 论文强调的是 generalized `Petri Net`，即 place 上 token 数与弧权重不额外受安全网或有界网限制。

论文直接给出性质语言的核心形态：`F` 是由线性约束字面量做布尔组合得到的公式。可写成：

$$
F ::= \alpha \bowtie \beta \mid \neg F \mid F \land F \mid F \lor F
$$

上式中的符号逐项解释如下：

1. `$\alpha,\beta$` 是由 places 和常数构成的线性表达式。
2. `$\bowtie$` 是比较算子。
3. 文中示例 `$(p+q>r)\lor(p\le 5)$` 就属于这一类性质。
4. 这使 `SMPT` 不只检查“某个精确 marking 是否可达”，还可以检查线性不变量、deadlock、quasi-liveness 等更一般的 reachability 条件。

论文显式给出两类查询：

$$
EF\,F
$$

以及

$$
AG\,F \equiv \neg(EF\,\neg F)
$$

上式中的符号逐项解释如下：

1. `$EF\,F$` 表示存在某个可达 marking 满足性质 `$F$`。
2. `$AG\,F$` 表示所有可达 markings 都满足 `$F$`，也就是 `$F$` 是不变式。
3. 第二个公式是论文直接写出的经典对偶关系。

### 一个最小例子与通俗解释

论文正文直接给出一个很好的最小例子：性质

$$
(p+q>r)\lor(p\le 5)
$$

表示“要么 `p` 和 `q` 上的 token 总数大于 `r`，要么 `p` 上 token 不超过 5”。在 `SMPT` 里，可以问两类问题：

1. `EF` 版本：是否存在某个可达 marking 让这个公式为真。
2. `AG` 版本：是否所有可达 markings 都让这个公式为真。
3. 若问 deadlock、quasi-liveness，本质上也会被翻成同类的线性约束 reachability 公式。

通俗地说，`SMPT` 不是只会问“能不能到某个具体状态”，而是把 `Petri Net` 的很多验证问题统一翻译成“有没有某种满足线性条件的 token 分布”。

### 运行 / 接受 / 转移语义

论文把 reachability 语义写得很直接。可达性查询可整理为：

$$
(N;m_0) \models EF\,F \iff \exists m \in \mathrm{Reach}(N,m_0): m \models F
$$

上式中的符号逐项解释如下：

1. `$\mathrm{Reach}(N,m_0)$` 是从初始 marking 可达的 markings 集合。
2. `$m \models F$` 表示把每个 place `p` 替换成 `m(p)` 后，公式 `$F$` 为真。
3. 这正是论文对 `EF` 查询的语义解释。

对应地，不变式查询可写成：

$$
(N;m_0) \models AG\,F \iff \forall m \in \mathrm{Reach}(N,m_0): m \models F
$$

上式中的符号逐项解释如下：

1. `$AG\,F$` 要求所有可达 markings 都满足 `$F$`。
2. 这也是 `SMPT` 生成 verdict certificate 的主要场景。

论文对结构约简的核心表达是“用 reduced net 和线性方程组恢复原网 reachability 信息”。可保守整理为：

$$
(N_1;m_1) \rightsquigarrow_E (N_2;m_2)
$$

上式中的符号逐项解释如下：

1. `$(N_1;m_1)$` 是原始网。
2. `$(N_2;m_2)$` 是约简后的网。
3. `$E$` 是把原网 places 与约简后网 places 联系起来的线性方程组。
4. 这条记号是根据论文对 polyhedral reduction 的描述做的保守整理，核心意思是“约简后仍保留足够信息以重建原问题的 reachability 结论”。

论文还明确给出归纳不变式的三个条件。可压成：

$$
m_0 \models R,\quad (m \to m' \land m \models R) \Rightarrow m' \models R,\quad R \Rightarrow F
$$

上式中的符号逐项解释如下：

1. `$R$` 是候选归纳不变式。
2. 第一项要求初始状态满足 `$R$`。
3. 第二项要求 `$R$` 对所有一步迁移都封闭。
4. 第三项要求 `$R$` 蕴含待证明性质 `$F$`。
5. 若三项都成立，就能把 `$R$` 作为 `AG F` 的独立证书输出。

### 语义边界

1. 论文目标是 generalized `Petri Net` reachability infrastructure，不讨论更广的连续、随机或 timed-net 语义。
2. 尽管支持 colored-net unfolding，但核心求解对象仍会回落到普通 `Petri Net` + 线性整数约束。
3. `SMPT` 通过 portfolio 汇聚多类方法，但并不声称所有方法对所有实例都同样高效。
4. polyhedral reduction 很强，但前提是可由 `Reduce` 找到足够有效的结构约简。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| marked generalized `Petri Net` | `$(N;m_0),\ N=(P,T,\mathrm{Pre},\mathrm{Post})$` | `SMPT` 的核心输入对象。 |
| reachability formula | `$F ::= \alpha \bowtie \beta \mid \neg F \mid F \land F \mid F \lor F$` | 统一 deadlock、liveness、线性不变量等问题。 |
| existential reachability | `$(N;m_0) \models EF\,F \iff \exists m \in \mathrm{Reach}(N,m_0): m \models F$` | 论文中的 `EF` 查询语义。 |
| invariant query | `$AG\,F \equiv \neg(EF\,\neg F)$` | 论文显式给出的 `AG` 与 `EF` 对偶。 |
| inductive certificate | `$m_0 \models R,\ (m \to m' \land m \models R)\Rightarrow m' \models R,\ R \Rightarrow F$` | `SMPT` 可输出并独立检查的 verdict certificate。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | marking 是一等对象，支持无界网。 |
| 事件 / 触发 | 很强 | transitions firing 构成主语义。 |
| 守卫 / 数据 | 中等支持 | 核心不是 rich data，而是 places 上的线性整数约束。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 很强 | `Petri Net` 并发语义是母线。 |
| 时间约束 | 不支持 | 论文主体不是 timed `Petri Net`。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic `Petri` 工具线。 |
| 可执行 / 可验证性 | 很强 | `SMT`、portfolio、proof export、enumeration 和 reduction 全部到位。 |

### 形式化问题与性质

1. `SMPT` 的关键价值是把 reachability 研究方法做成同一工作台，而不是只交付一个单算法原型。
2. polyhedral reduction 让它能把 `Tina` 的结构性优势和 `SMT` 求解优势接起来。
3. verdict certificate 很重要，因为它把“不变式成立”从工具结论变成可独立重放的证明工件。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `PNML` 网模型。
2. colored-net 输入与外部 unfolding。
3. `MCC` property XML。
4. `--deadlock`、`--quasi-liveness`、`--reachability` 等命令行快捷查询。

### 机器可处理承载方式

机器可处理承载方式包括：

1. generalized `Petri Net` 内部数据结构。
2. reduction equations。
3. `QF-LIA` 的 `SMT-LIB` 约束。
4. 反例 marking、inductive invariant 与 verdict certificate。

### 交换与互操作

1. `SMPT` 直接吃 `PNML` 与 `MCC` 公式，天然贴近 `Petri Net` 比赛生态。
2. `Reduce` 和 `walk` 来自 `Tina` 工具箱，是它的重要外部后端。
3. `z3` 与 `MiniZinc` 让它能把 `Petri Net` 问题压到通用求解器接口上。

## 配套基础设施

- 建模/编辑工具：命令行驱动，输入可来自 `PNML`、colored nets 和 `MCC` 公式。
- 解析/交换/元模型支持：`ptio` 库负责 `Petri Net`、公式和 reduction-equation 数据结构与解析。
- 仿真/执行支持：`Random Walk` 与 `Enumeration` 提供探索式或穷举式执行路径。
- 验证/分析支持：`Induction`、`BMC`、`k-induction`、`PDR`、`State Equation`、`Constraint Programming`、`Enumeration` 组成 portfolio。
- 代码生成/转换支持：核心不是代码生成，而是向 `SMT-LIB`、proof export 和 reduced-net artifact 转换。
- 标准化或社区生态：`GitHub`、`GPL v3`、`MCC`、`PNML`、`Tina` 和 `z3` 共同构成可复现实验生态。

## 适用场景与需求前提

### 适用场景

适合 generalized `Petri Net` reachability、`MCC` 基准实验、结构约简与 `SMT` 方法对比、以及需要可独立检查证书的 invariant verification。

### 需求前提

1. 系统需要能落成普通或经 unfolding 后的 `Petri Net`。
2. 目标性质最好能写成 places 上的线性约束组合。
3. 若希望充分利用 `SMPT` 优势，模型结构最好允许 reduction、trap constraints 或状态方程近似发挥作用。
4. 使用者接受“同一问题多方法并行试探”的 portfolio 工作方式。

### 不适用或高成本场景

如果需求核心在 dense-time、连续动力学或 rich symbolic data structure，而不是 marking reachability，本工具就不是最自然的后端。

## 与相邻形式主义的关系

相对 [quickly-prototyping-petri-nets-tools-with-snakes/desc.md](../quickly-prototyping-petri-nets-tools-with-snakes/desc.md)，`SNAKES` 更偏 Petri 工具原型框架，`SMPT` 更偏 reachability portfolio；相对 [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)，`Tina` 更像完整 timed-net 工具箱，而 `SMPT` 重点吸收其 `Reduce/walk` 能力来服务 generalized reachability；相对 [symbolic-model-checking-using-its-tools/desc.md](../symbolic-model-checking-using-its-tools/desc.md)，`ITS-tools` 提供更通用的 symbolic state-space engine，而 `SMPT` 更聚焦 `Petri Net` reachability 与证书；相对 [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)，`TAPAAL` 面向 timed-arc `Petri Net`，`SMPT` 则面向 generalized untimed `Petri Net` reachability。

## 与本研究的关系

### 对 Project 1 的价值

`SMPT` 说明“状态机族基础设施”不只包括建模前端，也包括把性质语言、约简、中间约束和证书统一起来的验证后端。在后续生成-验证-修复闭环里，这类统一后端特别适合承接 LLM 生成的资源流或并发过程模型。

### 可复用启发

1. 性质语言最好尽早结构化为线性约束组合，而不是停留在口语描述。
2. verification profile 不应只决定调用哪个 solver，还应决定是否先做 reduction、是否导出证书。
3. “工具返回结论”与“工具返回可独立检查证据”是两层能力，后者更适合高可信研究路线。

## 重要的相关工作

1. [quickly-prototyping-petri-nets-tools-with-snakes/desc.md](../quickly-prototyping-petri-nets-tools-with-snakes/desc.md)：研究型 `Petri Net` 工具原型基础库。
2. [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)：`Reduce` 与 `walk` 所属的 `Petri` 工具箱母线。
3. [symbolic-model-checking-using-its-tools/desc.md](../symbolic-model-checking-using-its-tools/desc.md)：更通用的 symbolic verification backend 对照线。
4. [tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md](../tapaal-20-integrated-development-environment-for-timed-arc-petri-nets/desc.md)：时间化 `Petri Net` 工具生态对照。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 关键特性：generalized `Petri Net`、linear-constraint reachability、polyhedral reduction、portfolio checking、verdict certificate。
- 构造方式：`PNML / MCC property -> reduction / SMT encoding -> parallel methods -> witness or proof`。
- 基础设施：`Python`、`z3`、`MiniZinc`、`Tina Reduce/walk`、`PNML`、`MCC`。
- 对状态机族演化树而言，它是 generalized `Petri Net` reachability backend 的静态挂接口径，不形成新的主树节点。

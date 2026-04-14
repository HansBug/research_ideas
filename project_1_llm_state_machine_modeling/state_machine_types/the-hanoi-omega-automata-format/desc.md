# HOA：河内 Omega 自动机格式 / The Hanoi Omega-Automata Format

## 基本信息

- 标题：The Hanoi Omega-Automata Format
- 中文标题：HOA：河内 Omega 自动机格式
- 作者：Tomáš Babiak，František Blahoudek，Alexandre Duret-Lutz，Joachim Klein，Jan Křetínský，David Müller，David Parker，Jan Strejček
- 发表：*Computer Aided Verification*，pp. 479-486，2015
- DOI：`10.1007/978-3-319-21690-4_31`
- 链接：https://doi.org/10.1007/978-3-319-21690-4_31
- 形式主义：`HOA / omega-automata exchange format`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：`omega` 自动机交换格式 / 工具互操作标准
- 工具/实现获取方式：论文明确给出 `http://adl.github.io/hoaf/support.html` 作为工具支持总入口，并说明 `Spot`、`jhoafparser`、`PRISM`、`ltl2dstar`、`ltl3ba`、`ltl3dra`、`Rabinizer3` 等已实现支持。
- 标准/格式获取方式：论文明确给出 `http://adl.github.io/hoaf/` 作为 `HOA` 完整规范和示例入口。

## 简报

这篇论文的贡献，不是再提出一种新的 `omega` 自动机，而是把原本各自为政的 `Büchi / generalized Büchi / Rabin / Streett / alternating` 工具输入输出，收束到同一个统一、可扩展、 acceptance-agnostic 的交换格式里。`HOA` 的关键动作，是把 acceptance condition 从“若干硬编码特例”升级成“对 `Inf/Fin` 原语做布尔组合”的通用语法。

- 形式主义定位：`omega` 自动机交换标准，而不是新的状态机母型。
- 构造方式简述：用 header 描述 automaton 的语义属性，用 body 描述状态、标签、转移和 acceptance sets；核心是 `Acceptance:` 行上的通用接受条件语法。
- 基础设施与场景简述：依托 `HOA` 规范、`Spot` 解析/转换链、`jhoafparser` 与 `PRISM` 接口，服务 `LTL/PSL -> omega automata -> verification backend` 的工具流水线。

```text
LTL/PSL/verification tool -> HOA header/body + generic acceptance -> parser / translator / model checker -> acceptance-agnostic automata workflow
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `omega` 自动机的统一文件表示；
2. `Acceptance:` 行上的通用接受条件语法；
3. state-based / transition-based acceptance；
4. deterministic / nondeterministic / alternating 自动机支持；
5. 多工具互操作生态。

### 核心抽象

从格式结构看，可以把 `HOA` 保守整理为：

$$
\mathrm{HOA} = (\mathrm{Header}, \mathrm{Body}, AP, Acc, Q, Start)
$$

上式中的符号逐项解释如下：

1. `Header` 给出 automaton 的元信息和语义属性。
2. `Body` 给出状态、转移、标签与 acceptance-set 标记。
3. `AP` 是原子命题列表。
4. `Acc` 是接受条件公式。
5. `Q` 是状态集合。
6. `Start` 是初始状态或初始状态组合。

论文最关键的形式化贡献是接受条件语法：

$$
acc ::= f \mid t \mid Inf(s) \mid Inf(!s) \mid Fin(s) \mid Fin(!s) \mid acc \land acc \mid acc \lor acc \mid (acc)
$$

上式中的符号逐项解释如下：

1. `f` 与 `t` 分别表示恒假与恒真接受条件。
2. `s` 是某个 acceptance set 的编号。
3. `Inf(s)` 表示运行在集合 `s` 中被访问无穷多次。
4. `Fin(s)` 表示运行在集合 `s` 中只被访问有限次。
5. `!s` 表示 acceptance set `s` 的补集。
6. `\&` 与 `|` 分别是布尔合取与析取。

运行满足接受条件可保守写成：

$$
\mathrm{Run} \models Acc
$$

上式中的符号逐项解释如下：

1. `Run` 是 automaton 的运行；对 alternating automata，它会是一棵运行树。
2. `Acc` 是 `Acceptance:` 行给出的布尔公式。
3. 只要 `Run` 满足 `Acc`，该运行就是接受运行。

### 一个最小例子与通俗解释

论文用 `p_0 U p_1` 这个 `LTL` 公式举了一个最小例子，其 `HOA` 表示大致是：

$$
\mathrm{Acceptance}: 1\ Inf(0)
$$

对应的 body 中，状态 `1` 标记了 `{0}`，表示它属于 acceptance set `0`。这等价于说：

1. 自动机总共有一个接受集合。
2. 一条运行只要无穷多次访问这个集合，就被接受。

通俗地说，`HOA` 做的事情像“给各种 omega 自动机找了一个大家都能说的共同语”。以前一个工具输出 never claim，另一个输出 XML，第三个输出只支持 Rabin；现在它们至少可以先交换成 `HOA`，再各做各的算法。

### 运行 / 接受 / 转移语义

论文明确区分了：

1. state-labelled 与 transition-labelled 自动机；
2. state-based 与 transition-based acceptance；
3. deterministic、nondeterministic 与 alternating 结构。

`HOA` 中标签的基本语义可保守写成：

$$
\ell : Q \cup \delta \to \mathrm{Bool}(AP)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `\delta` 是转移集合。
3. `AP` 是原子命题表。
4. `\mathrm{Bool}(AP)` 表示关于原子命题的布尔公式。
5. 这说明标签既可以挂在状态上，也可以挂在转移上。

### 语义边界

这篇论文的边界同样很清楚：

1. 它只规范交换格式，不替代模型检查器或转换算法本身。
2. 它覆盖的是 `omega` 自动机，而不是 timed / hybrid / probabilistic model 本体格式。
3. 它支持 generic acceptance，但最终消费工具是否能直接处理，仍取决于后端算法能力。
4. 它不要求所有工具都支持所有 acceptance，只要求能在统一语法下交换。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 格式骨架 | `$\mathrm{HOA} = (\mathrm{Header}, \mathrm{Body}, AP, Acc, Q, Start)$` | 说明 `HOA` 以 header/body 双段组织 automaton。 |
| 通用接受条件 | `$acc ::= f \mid t \mid Inf(s) \mid Inf(!s) \mid Fin(s) \mid Fin(!s) \mid \cdots$` | 这是 `HOA` 最核心的语法创新。 |
| 接受判定 | `$\mathrm{Run} \models Acc$` | 运行是否接受由 `Acceptance:` 公式统一决定。 |
| Rabin 示例 | `$\mathrm{Acceptance}: 6\ (Fin(0)\&Inf(1)) | (Fin(2)\&Inf(3)) | (Fin(4)\&Inf(5))$` | 说明 `HOA` 可把传统命名接受条件降成统一布尔语法。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 `omega` 自动机状态图。 |
| 事件 / 触发 | 中等支持 | 通过原子命题布尔标签承载，而不是事件驱动控制语义。 |
| 守卫 / 数据 | 弱支持 | 仅支持命题标签层，不是富数据守卫语言。 |
| 层次 | 不支持 | 不是层次状态机格式。 |
| 并发 / 同步 | 不适用 | 不以并发控制建模为目标。 |
| 时间约束 | 不支持 | 不表示 clocks 或 deadlines。 |
| 连续动态 / 随机性 | 不支持 | 不表达混成/随机动力学本体。 |
| 可执行 / 可验证性 | 很强 | 作为交换层可直接服务大量验证工具链。 |

### 形式化问题与性质

1. `HOA` 的核心不是压缩某个单一 acceptance，而是统一多种 acceptance family。
2. 它把工具互操作的瓶颈从“格式不兼容”转成“后端算法支不支持某类接受条件”。
3. 对 acceptance-agnostic toolchain 来说，这比继续堆自定义 XML 或专用文本格式更稳。

## 构造方式与承载格式

### 建模入口

`HOA` 的建模入口主要来自其他工具：

1. `ltl2dstar`、`ltl3ba`、`ltl3dra`、`Rabinizer3` 等自动机生成器；
2. `Spot` 的 `ltl2tgba`、`randaut`、`autfilt`、`ltldo`；
3. `PRISM` 等消费端验证器。

### 机器可处理承载方式

机器可处理承载方式包括：

1. header/body 文本格式；
2. `AP:`、`Acceptance:`、`State:` 等关键字段；
3. acceptance sets 的花括号标记；
4. `jhoafparser` 与 `Spot` parser。

### 交换与互操作

这篇论文的重点几乎全部落在互操作：

1. `HOA` 统一了 `never claim`、LBT、GFF 等碎片化格式之上的交换层。
2. `Spot` 与 `jhoafparser` 分别提供 `C++` 与 `Java` 解析入口。
3. `PRISM` 已能通过 `HOA` 与外部 deterministic-automata translators 对接。

## 配套基础设施

- 建模/编辑工具：`Spot` 及一系列 `LTL -> omega automata` 生成器。
- 解析/交换/元模型支持：`HOA` 规范本体、`Spot` parser、`jhoafparser`。
- 仿真/执行支持：`HOA` 自身不执行模型，执行依赖消费端工具。
- 验证/分析支持：`PRISM` 等工具已利用 `HOA` 对接 generic acceptance 工作流。
- 代码生成/转换支持：支持格式转换、过滤、包装与 acceptance-preserving pipelines。
- 标准化或社区生态：`adl.github.io/hoaf/` 维护规范，GitHub 上公开讨论问题与改进。

## 适用场景与需求前提

### 适用场景

适合任何需要在 `LTL/PSL` 翻译器、`omega` 自动机构造器、解析器和模型检查器之间稳定交换自动机的场景，尤其适合 acceptance conditions 不再局限于 `Büchi` 的工作流。

### 需求前提

1. 目标对象本质上是 `omega` 自动机。
2. 团队关心工具互操作而不是单一工具闭环。
3. 后续工具至少愿意解析 `HOA` 或通过 parser 接口接入。
4. 接受条件最好能保留在统一布尔语法中，而不是过早硬编码为某单一 family。

### 不适用或高成本场景

如果目标对象本身是 timed automata、hybrid automata、quantitative model 或控制状态机 DSL，本格式就只是局部桥梁，而非最终承载体。

## 与相邻形式主义的关系

相对 [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)，两者都在做“工具互操作层”，但 `JANI` 面向 quantitative models，`HOA` 面向 `omega` 自动机；相对 [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)，`Momba` 更像以 `JANI` 为中心的工作流平台，而 `HOA` 是更底层的 automata interchange format；相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，`PRISM` 是消费端模型检查器，而 `HOA` 是把自动机安全送进这些后端的共同载体。

## 与本研究的关系

### 对 Project 1 的价值

1. 如果未来要把需求性质翻成 `LTL`、再走 automata-theoretic verification，`HOA` 是现成且稳定的交换层。
2. 它说明“标准/格式”本身就是一个独立且高价值的研究资产，不必总把关注点放在模型本体上。
3. 对 `project_1` 而言，这类标准层条目能帮助判断某个形式主义是否真的具备成熟工具生态。

### 局限

1. 它不直接帮助从需求生成状态机。
2. 它的价值主要体现在与验证工具链的衔接上，而不是建模前端。

## 重要的相关工作

- [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)：对照另一条“交换格式先行”的基础设施路线。
- [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)：展示交换格式如何进一步演化成工作流平台。
- [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：说明 `HOA` 一类交换格式最终如何被验证后端消费。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 结论：这是一篇非常典型的 `omega` 自动机标准层条目，适合补入文库的“标准/基础设施”主线。

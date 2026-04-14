# ROLL 1.0：ω-正则语言学习库 / ROLL 1.0: ω-Regular Language Learning Library

## 基本信息

- 标题：ROLL 1.0: ω-Regular Language Learning Library
- 中文标题：ROLL 1.0：ω-正则语言学习库
- 作者：Yong Li，Xuechao Sun，Andrea Turrini，Yu-Fang Chen，Junnan Xu
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 11427`，pp. 365-371，2019
- DOI：`10.1007/978-3-030-17462-0_23`
- 链接：https://doi.org/10.1007/978-3-030-17462-0_23
- 形式主义：`omega-regular language learning / Buchi automata / FDFA / ROLL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：`omega`-regular language learning library with learning, complementation and inclusion tooling
- 工具/实现获取方式：原文明确给出 `ROLL` 在线主页 `https://iscasmc.ios.ac.cn/roll/`、GitHub 仓库 `https://github.com/ISCAS-PMC/roll-library` 与 Jupyter notebook 入口。
- 标准/格式获取方式：原文明确支持 `RABIT` 的 `.ba` 格式与 `HOA` `.hoa` 格式，命令行接口统一为 `java -jar ROLL.jar ...`。

## 简报

这篇论文补的是 `omega-automata` 工具链里非常关键但长期空缺的一块：不是继续讲 `L*` 如何学习有限词语言，而是把完整 `omega-regular language` 学习、`Buchi` 自动机补余和 inclusion testing 真正做成一套可复用库。`ROLL 1.0` 的价值主要在三点：它把已知的 `BA` 学习算法统一进一个 Java 框架；它把 `Teacher/Learner` 接口做成可扩展抽象；它同时把 `.ba/.hoa` 格式、`RABIT` 等价检查、命令行与 Jupyter 教学入口串成了完整基础设施。

- 形式主义定位：围绕 `Buchi automata / omega-regular language` 的学习与操作基础设施，而不是新的自动机子类。
- 构造方式简述：`Learning Library` 提供 `L$`、`Lω` 与 `FDFA` 相关学习算法，`Control Center` 负责任务分发、格式处理和命令行执行。
- 基础设施与场景简述：依托 `Java`、`Teacher/Learner` 接口、`RABIT`、`ASCC`、`.ba/.hoa`、Graphviz dot 与 Jupyter notebook，服务 `omega`-language learning、教学、补余和包含检查实验。

```text
omega-language target -> Teacher / Learner loop -> BA / FDFA hypothesis -> RABIT / ASCC query support -> learned BA / complementation / inclusion result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Buchi automata` 与 `omega`-regular languages。
2. active automata learning 的 `Teacher / Learner` 交互。
3. `L$` learner 与基于 `FDFA` 的 `Lω` learner。
4. learning-based complementation 与 inclusion checking。
5. `.ba / .hoa` 格式和命令行 / Jupyter 承载。

### 核心抽象

论文依赖的核心自动机对象可保守写成：

$$
B = (Q, \Sigma, \delta, q_0, F)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是 `Buchi automaton` 的有限状态集合。
2. `$\Sigma$` 是输入字母表。
3. `$\delta \subseteq Q \times \Sigma \times Q$` 是迁移关系。
4. `$q_0$` 是初始状态。
5. `$F \subseteq Q$` 是接受状态集合。

论文里的学习工作流可保守整理为：

$$
\mathcal{R} = (\Sigma, \mathrm{Teacher}, \mathrm{Learner}, H, \mathrm{EQ})
$$

上式中的符号逐项解释如下：

1. `$\Sigma$` 是字母表。
2. `$\mathrm{Teacher}$` 回答 membership 与 equivalence queries。
3. `$\mathrm{Learner}$` 是具体学习算法，如 `L$` 或 `Lω`。
4. `$H$` 是当前 hypothesized `Buchi` 自动机或其相关中间对象。
5. `$\mathrm{EQ}$` 是等价查询过程，论文实现里主要借助 `RABIT`。

`ROLL` 明确处理无限词，因此 membership query 的对象可直接写成 ultimately periodic word：

$$
w = u v^\omega
$$

$$
MQ(u, v) =
\begin{cases}
1, & uv^\omega \in L(B) \\
0, & uv^\omega \notin L(B)
\end{cases}
$$

上式中的符号逐项解释如下：

1. `$u$` 是 stem。
2. `$v$` 是 loop。
3. `$uv^\omega$` 是无限词。
4. `$L(B)$` 是目标 `Buchi automaton` 接受的语言。

### 一个最小例子与通俗解释

论文在 Jupyter 示例里直接用了语言 `\Sigma^* \cdot b^\omega`：

1. 字母表是 `\Sigma = \{a,b\}`。
2. 允许前面出现有限个 `a/b` 混合前缀。
3. 一旦进入最终稳定段，之后必须一直是 `b`。
4. `ROLL` 用 membership query 问类似 `ba \cdot (ba)^\omega` 这类无限词是否属于目标语言，再用 counterexample 修正假设机。

通俗地说，`ROLL` 像“无限词世界里的 LearnLib”。它不是从文本直接生成状态机，而是拿一个可查询的目标语言当老师，不断提出“这条无限行为属于你吗”“我现在猜的自动机对不对”，最后学出一个 `Buchi` 自动机。

### 运行 / 接受 / 转移语义

论文依赖的 `Buchi` 接受语义可保守写成：

$$
\rho \in L(B) \iff \mathrm{Inf}(\rho) \cap F \neq \emptyset
$$

上式中的符号逐项解释如下：

1. `$\rho$` 是 `B` 在某个无限词上的运行。
2. `$\mathrm{Inf}(\rho)$` 是运行中被无限次访问的状态集合。
3. `$F$` 是接受状态集合。
4. 这也是 `omega-regular language` 与 `Buchi automata` 对接的基本语义。

学习迭代可压成：

$$
H_{i+1} = \mathrm{Refine}(H_i, ce_i)
$$

上式中的符号逐项解释如下：

1. `$H_i$` 是第 `$i$` 轮假设机。
2. `$ce_i$` 是本轮等价查询返回的反例。
3. `$\mathrm{Refine}$` 表示 observation table 或 classification tree 的更新。

补余功能的目标则可直接写成：

$$
L(B^c) = \Sigma^\omega \setminus L(B)
$$

上式中的符号逐项解释如下：

1. `$B$` 是输入 `Buchi automaton`。
2. `$B^c$` 是学习式补余得到的自动机。
3. `$\Sigma^\omega$` 是所有无限词。
4. 论文强调这条 learning-based complementation 路线可作为结构化补余算法的 baseline。

### 语义边界

1. `ROLL 1.0` 聚焦 `omega-regular language learning`，不是通用系统建模前端。
2. 主对象是 `Buchi automata` 及其学习相关中间结构，不覆盖 rich data、时间或混成语义。
3. 它更像算法工程平台，而不是工业 GUI 建模器。
4. 论文尤其强调的是“完整 `omega`-regular class 的 learning support”，不是仅做一个 `BA` translator。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `Buchi` 自动机骨架 | `$B = (Q, \Sigma, \delta, q_0, F)$` | `ROLL` 处理的核心对象。 |
| 学习框架 | `$\mathcal{R} = (\Sigma, \mathrm{Teacher}, \mathrm{Learner}, H, \mathrm{EQ})$` | `Teacher/Learner` 组件化接口。 |
| 无限词 membership query | `$MQ(u,v)=1 \Leftrightarrow uv^\omega \in L(B)$` | Jupyter 交互与 oracle 语义基础。 |
| `Buchi` 接受 | `$\rho \in L(B) \Leftrightarrow \mathrm{Inf}(\rho)\cap F \neq \emptyset$` | `omega`-语言语义底座。 |
| 补余目标 | `$L(B^c)=\Sigma^\omega \setminus L(B)$` | learning-based complementation 的直接目标。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接操作 `Buchi automata` 与 `FDFA` 相关结构。 |
| 事件 / 触发 | 中等支持 | 以字母表输入和 ultimately periodic words 为主。 |
| 守卫 / 数据 | 不支持 | 不讨论富数据 guards。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 不支持 | 不负责并发系统前端建模。 |
| 时间约束 | 不支持 | 对象是 `omega-regular languages`，不是 timed automata。 |
| 连续动态 / 随机性 | 不支持 | 不在本文对象范围内。 |
| 可执行 / 可验证性 | 很强 | 学习、补余、包含检查、命令行和 Jupyter 均已工程化。 |

### 形式化问题与性质

1. `ROLL` 的核心不是单一算法实现，而是把完整 `omega` 学习工作流库化。
2. `Learner / Teacher` 抽象让后续算法和功能更容易复用。
3. `.hoa` 支持很关键，因为它把 `ROLL` 接进了更现代的 `omega-automata interchange` 生态。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `.ba` 或 `.hoa` 输入自动机。
2. `learn / play / complement / include` 命令行模式。
3. `Teacher / Learner` Java 接口扩展。
4. Jupyter notebook 交互式教学入口。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `RABIT` 的 `.ba` 格式。
2. `HOA` `.hoa` 格式。
3. `Graphviz` dot 输出。
4. Java library API 与命令行 options。

### 交换与互操作

互操作重点在现有 `omega` 工具链衔接：

1. `ROLL` 直接支持 `RABIT` 输入格式。
2. `ROLL` 同时支持 `HOA`，可接更通用的 `omega-automata` 工作流。
3. 等价查询实现借助 `RABIT`，membership query 则使用 `ASCC`。

## 配套基础设施

- 建模/编辑工具：主体不是图形 editor，而是 Java library、命令行和 notebook 入口。
- 解析/交换/元模型支持：`.ba`、`.hoa`、Graphviz dot、Java interfaces。
- 仿真/执行支持：interactive `play` mode 可让用户扮演 teacher。
- 验证/分析支持：`BA` 学习、complementation、inclusion testing、Monte Carlo `omega`-word sampling。
- 代码生成/转换支持：可保存 learned automaton，输出格式与输入格式一致。
- 标准化或社区生态：`RABIT`、`HOA`、JupyterHub 与 `omega-automata` 学习社区共同构成生态。

## 适用场景与需求前提

### 适用场景

适合 `omega-regular language learning`、`Buchi` 补余 baseline、语言包含实验、`LTL/omega` 工具教学，以及需要把无限词语言恢复为自动机的研究场景。

### 需求前提

1. 目标对象需能表示成 `omega-regular language`。
2. 系统或 oracle 需支持 membership / equivalence 风格交互。
3. 团队接受 `Buchi automata`、`FDFA` 等自动机中间表示。
4. 若做包含检查或补余，最好已有 `BA` 输入模型。

### 不适用或高成本场景

如果目标系统核心依赖数据参数、时钟、概率或混成动力学，`ROLL` 就更像旁路研究工具，而不是直接主战场。

## 与相邻形式主义的关系

相对 [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)，`LearnLib` 主战场是有限词自动机学习，而 `ROLL` 直接补到 `omega-regular language`；相对 [tool-support-for-learning-buchi-automata-and-linear-temporal-logic/desc.md](../tool-support-for-learning-buchi-automata-and-linear-temporal-logic/desc.md)，后者更偏 `GOAL` 式图形交互和公式-自动机演示，`ROLL` 更偏算法库与学习实验；相对 [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)，`HOA` 是交换格式，`ROLL` 则是直接消费该格式的学习库。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“状态机不只可由需求正向生成，也可由行为 / oracle 反向学习”。
2. `omega-language` 这条线对性质自动机、活性约束和长期行为分析很有参考价值。
3. `Teacher / Learner` 抽象也可借鉴到后续“生成 - 验证 - 修复”闭环中。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`Buchi automata` 与 `omega` 学习更适合作为验证侧中间表示和工具后端，而不是控制工程师最终交付的前端模型。

### 对需求到模型生成的启发

1. 活性需求若能落成 `omega-language` 或性质自动机，会更容易和成熟工具链对接。
2. 生成模型和学习模型可以互相做 consistency check。
3. 交换格式兼容性很重要，`HOA` 支持让工具接入成本明显下降。

## 重要的相关工作

1. [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)：有限词主动学习基础设施。
2. [tool-support-for-learning-buchi-automata-and-linear-temporal-logic/desc.md](../tool-support-for-learning-buchi-automata-and-linear-temporal-logic/desc.md)：`Buchi` / `LTL` 图形交互工具。
3. [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)：`omega`-automata 交换格式。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`omega-regular language learning / Buchi automata / FDFA / ROLL`
- 论文角色：`omega`-regular language learning library with learning, complementation and inclusion tooling
- 核心功能：把 `Buchi` 学习、补余、包含检查和 `.ba/.hoa` 承载统一进可复用 Java 库
- 关键特性：`Teacher/Learner` 接口、`L$ / Lω`、`RABIT` 等价查询、`ASCC` membership、Jupyter notebook
- 构造方式：`oracle / BA input -> learner loop -> learned BA / complementation / inclusion result`
- 基础设施：`ROLL`、`.ba/.hoa`、`RABIT`、`ASCC`、Graphviz、JupyterHub
- 适用场景：`omega`-language learning、`Buchi` 补余 baseline、教学和包含检查实验
- 需求前提：目标对象需能落成 `omega-regular language`，并具备可查询 teacher 或现成 `BA`
- 状态：🟢

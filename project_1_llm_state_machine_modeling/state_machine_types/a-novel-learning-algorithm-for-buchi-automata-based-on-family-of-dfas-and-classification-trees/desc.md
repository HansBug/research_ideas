# 基于 DFA 族与分类树的 Büchi 自动机新学习算法 / A Novel Learning Algorithm for Büchi Automata Based on Family of DFAs and Classification Trees

## 基本信息

- 标题：A Novel Learning Algorithm for Büchi Automata Based on Family of DFAs and Classification Trees
- 中文标题：基于 DFA 族与分类树的 Büchi 自动机新学习算法
- 作者：Yong Li，Yu-Fang Chen，Lijun Zhang，Depeng Liu
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 10206`，pp. 208-226，2017
- DOI：`10.1007/978-3-662-54577-5_12`
- 链接：https://doi.org/10.1007/978-3-662-54577-5_12
- 形式主义：`Büchi automata learning / FDFA / classification tree / ROLL`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：tree-based Büchi-automata learning method with FDFA teachers and the first public ROLL library
- 工具/实现获取方式：原文明确给出 `ROLL` 入口 `http://iscasmc.ios.ac.cn/roll`，并说明该库以 Java 实现，收录了文献中的 Büchi 自动机学习算法。
- 标准/格式获取方式：主承载是 `FDFA`、classification tree、`membership/equivalence queries`、under/over-approximation `BA` 构造与 `ROLL` 实现；它不是交换标准。

## 简报

这篇论文补的是 `omega`-automata learning 里的方法路线。它并不是重新定义 `Büchi automata`，而是把“学习未知 `\omega`-regular language”拆成 `FDFA learner + FDFA teacher + FDFA-to-BA approximation + counterexample analysis` 四段，并用 classification tree 替换 observation table，最终落成第一套公开 `ROLL` 学习库。

- 形式主义定位：围绕 `Büchi automata` 的主动学习方法路线，而不是新的 `BA` 本体。
- 构造方式简述：先学习 canonical `FDFA`，再通过 under/over-approximation 构造 `Büchi automata`，再用 counterexample analysis 回馈 refinement。
- 基础设施与场景简述：依托 `membership/equivalence queries`、periodic / syntactic / recurrent `FDFA`、classification trees 与 `ROLL`，服务 `\omega`-regular language learning、`LTL` 生成的 benchmark 学习和 automata-theoretic reverse engineering。

```text
BA teacher -> FDFA learner -> classification-tree FDFA hypothesis -> under/over-approximation BA -> counterexample analysis -> refined BA
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. ultimately periodic words 与 `\omega`-regular languages。
2. family of DFAs (`FDFA`)。
3. periodic / syntactic / recurrent canonical `FDFA`。
4. classification-tree based `FDFA` learner。
5. under-approximation / over-approximation 从 `FDFA` 到 `Büchi automata` 的转换。

### 核心抽象

论文直接定义 ultimately periodic words 集合：

$$
UP(L)=\{uv^\omega \mid u\in\Sigma^*,\ v\in\Sigma^+,\ uv^\omega\in L\}
$$

上式中的符号逐项解释如下：

1. `$L \subseteq \Sigma^\omega$` 是某个 `\omega`-language。
2. `$u$` 是有限前缀。
3. `$v$` 是非空有限循环片段。
4. `$uv^\omega$` 表示前缀后无限重复 `$v$` 的 `\omega`-word。

`FDFA` 的定义直接写成：

$$
F=(M,\{A_q\}_{q\in Q})
$$

上式中的符号逐项解释如下：

1. `$M=(\Sigma,Q,q_0,\delta)$` 是 leading automaton。
2. `$\{A_q\}_{q\in Q}$` 是为每个 leading state 配备的 progress DFA family。
3. `FDFA` 的目标不是直接接受所有 `\omega`-words，而是刻画其 ultimately periodic fragments。

论文给出的接受条件是：

$$
(u,v)\ \text{is accepted by }F \iff M(uv)=M(u)\ \land\ v\in L(A_{M(u)})
$$

上式中的符号逐项解释如下：

1. `$(u,v)$` 是某个 `uv^\omega` 的 decomposition。
2. `$M(uv)=M(u)$` 要求循环片段 `$v$` 把 leading automaton 带回同一状态。
3. `$A_{M(u)}$` 是对应 leading state 的 progress DFA。
4. `$v\in L(A_{M(u)})$` 表示循环片段被该 progress DFA 接受。

### 一个最小例子与通俗解释

论文里的直觉例子可以压成：

1. leading automaton 只有一个状态 `\varepsilon`。
2. progress DFA `A_\varepsilon` 接受有限词 `ba`。
3. 那么 `(ba,ba)` 是合法 decomposition。
4. 因而 `(ba)^\omega` 被当前 `FDFA` 所刻画。

通俗地说，`FDFA` 不是直接“看一条无限长输入”。它做的是先找一个前缀，再看后面的循环块会不会不断把系统带回同一类状态；如果会，而且这个循环块被对应 progress DFA 接受，就把整条无限行为认作合法。

### 运行 / 接受 / 转移语义

从 `FDFA` 到 `Büchi automata` 的核心近似关系可写成：

$$
UP(L(\underline{B})) \subseteq UP(F), \qquad UP(F) \subseteq UP(L(\overline{B}))
$$

上式中的符号逐项解释如下：

1. `$\underline{B}$` 是 under-approximation 构造得到的 `Büchi automaton`。
2. `$\overline{B}$` 是 over-approximation 构造得到的 `Büchi automaton`。
3. under-approximation 保证构造出的 `BA` 不会接受超出 `FDFA` 的 ultimately periodic words。
4. over-approximation 保证 `FDFA` 刻画的 ultimately periodic words 至少都被构造的 `BA` 覆盖。

论文还给出 tree-based periodic `FDFA` 的查询复杂度：

$$
EQ = O(n+nk), \qquad MQ = O((n+nk)\cdot(|u|+|v|+(n+k)\cdot|\Sigma|))
$$

上式中的符号逐项解释如下：

1. `$n$` 是 leading automaton 的状态数。
2. `$k$` 是最大 progress automaton 的状态数。
3. `$|u|+|v|$` 是最长 counterexample decomposition 的长度。
4. `$EQ$`、`$MQ$` 分别表示 equivalence queries 和 membership queries 的数量级。

### 语义边界

1. 论文重点是 `\omega`-regular language learning，不是 general software learning framework。
2. `FDFA` 是学习中间对象，不是最终交付对象；最终目标仍是 `Büchi automata`。
3. over-approximation route 可能不完整，论文也明确说明只有 under-approximation 路线保证总能终止并返回正确 `BA`。
4. 工程实现 `ROLL` 很重要，但论文主要创新仍然是 learning framework 与 classification-tree method。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| ultimately periodic words | `$UP(L)=\{uv^\omega \mid u\in\Sigma^*,v\in\Sigma^+,uv^\omega\in L\}$` | 论文把 `\omega`-regular language learning 收束到该对象上。 |
| `FDFA` 骨架 | `$F=(M,\{A_q\}_{q\in Q})$` | learning 的中间目标模型。 |
| `FDFA` 接受条件 | `$(u,v)$ accepted iff $M(uv)=M(u)\land v\in L(A_{M(u)})$` | decomposition 如何对应无限词接受。 |
| `FDFA -> BA` 近似 | `$UP(L(\underline{B}))\subseteq UP(F)\subseteq UP(L(\overline{B}))$` | under / over approximation 的语义位置。 |
| 查询复杂度 | `$EQ=O(n+nk)$` | classification-tree periodic `FDFA` 学习的主复杂度结论。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 `FDFA` 与 `Büchi automata`。 |
| 事件 / 触发 | 很强 | 输入对象是线性字母串及其无限重复。 |
| 守卫 / 数据 | 不支持 | 不是 dataful `RA/EFSM` learning。 |
| 层次 | 不支持 | 不是 hierarchical state machines。 |
| 并发 / 同步 | 不适用 | 论文主线是 `\omega`-language learning。 |
| 时间约束 | 不支持 | 不是 timed automata learning。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 `\omega`-automata learning。 |
| 可执行 / 可验证性 | 很强 | `ROLL` 提供公开实现，含 under/over-approximation 与 benchmark 实验。 |

### 形式化问题与性质

1. 论文把 `Büchi` 学习的难点明确放在“如何通过 `FDFA` 更稳定地承载 ultimately periodic information”。
2. classification tree 替代 table 后，query efficiency 成为方法的主要工程优势。
3. `ROLL` 使这条路线不再只是理论方案，而是可复用学习基础设施。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `BA` teacher 提供 `MemBA` 与 `EquBA`。
2. `FDFA` learner 构造 classification trees。
3. under / over-approximation `FDFA -> BA` translator。
4. `ROLL` library 的 Java implementation。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `FDFA` tuples。
2. decomposition pairs `$(u,v)$`。
3. classification trees。
4. under / over-approximation `BA` constructions。
5. benchmark `LTL` specifications 和对应最小 `BA`。

### 交换与互操作

互操作重点不在中立交换标准，而在 learning pipeline：

1. `FDFA learner` 与 `FDFA teacher` 通过 `MQ/EQ` 交互。
2. `BA teacher` 通过 counterexample `uv^\omega` 与 learner 交换证据。
3. `ROLL` 把不同 `Büchi` learning algorithms 放进同一库中，便于横向对比。

## 配套基础设施

- 建模/编辑工具：主体不是图形建模器，而是 Java `ROLL` library。
- 解析/交换/元模型支持：`FDFA`、`BA`、decomposition pair、classification tree 和 query interfaces。
- 仿真/执行支持：通过 teacher answering 与 benchmark tasks 运行 learning loop。
- 验证/分析支持：under/over-approximation、counterexample analysis、periodic / syntactic / recurrent `FDFA` learning、复杂度对比实验。
- 代码生成/转换支持：重点在 `FDFA -> BA` 构造，而非部署代码生成。
- 标准化或社区生态：`ROLL`、`dk.brics.automaton`、`LTL` benchmark 与 `omega`-automata learning 研究线。

## 适用场景与需求前提

### 适用场景

适合学习未知 `\omega`-regular language、自动机构造实验、`LTL` 到 automata 研究 benchmark，以及需要从无限行为样本或 oracle 反推出 `Büchi automata` 的场景。

### 需求前提

1. 需要存在 `membership/equivalence query` 风格 teacher。
2. 目标语言应是 `\omega`-regular 或可保守近似为 `\omega`-regular。
3. 团队接受通过 `FDFA` 作为中间对象来学习最终 `Büchi automata`。
4. 若追求完整性，应优先采用 under-approximation 路线。

### 不适用或高成本场景

如果目标是带数据参数、时间约束或连续变量的状态机学习，这篇方法不能直接覆盖；它更适合纯符号 `\omega`-language 场景。

## 与相邻形式主义的关系

相对 [ltl-to-buchi-automata-translation-fast-and-more-deterministic/desc.md](../ltl-to-buchi-automata-translation-fast-and-more-deterministic/desc.md)，`LTL3BA` 是 translation tool，而本文是 learning route；相对 [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)，`LearnLib` 更偏一般主动自动机学习框架，本文专注 `\omega`-automata；相对 [owl-a-library-for-omega-words-automata-and-ltl/desc.md](../owl-a-library-for-omega-words-automata-and-ltl/desc.md)，`Owl` 提供 `omega`-automata / `LTL` infrastructure，而 `ROLL` 提供 `Büchi` learning route。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机闭环不只有“从需求生成模型”，还可以从行为或 oracle 反向学习 `\omega`-automata 作为校验工件。
2. `FDFA` 作为中间表示的思路，对需要在生成与验证之间插入结构化过渡层的系统很有借鉴价值。
3. counterexample analysis 这条线也可迁移到 LLM 生成模型的修复环节。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`Büchi automata` 可以是性质侧或长期行为侧的目标形式主义，而 `FDFA` 更像学习与修复阶段的中间表示。

### 对需求到模型生成的启发

1. 若需求包含长期循环、无限执行或活性模式，最好保留 ultimately periodic view，而不是只看 finite traces。
2. 生成与学习之间可以共享一个更易处理的中间对象，而不必直接在最终自动机上迭代。
3. 结构化反例比纯“否定样本列表”更适合作为修复输入。

## 重要的相关工作

1. [ltl-to-buchi-automata-translation-fast-and-more-deterministic/desc.md](../ltl-to-buchi-automata-translation-fast-and-more-deterministic/desc.md)：`LTL -> Büchi automata` translator 路线。
2. [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)：主动自动机学习基础设施。
3. [owl-a-library-for-omega-words-automata-and-ltl/desc.md](../owl-a-library-for-omega-words-automata-and-ltl/desc.md)：`omega`-automata tooling 与 `LTL` infrastructure。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Büchi automata learning / FDFA / classification tree / ROLL`
- 论文角色：tree-based Büchi-automata learning method with FDFA teachers and the first public ROLL library
- 核心功能：通过 classification-tree `FDFA` 学习和 under/over-approximation 构造学习 `Büchi automata`
- 关键特性：`FDFA`、decomposition `$(u,v)$`、under/over-approximation、counterexample analysis、`ROLL`
- 构造方式：`BA teacher -> FDFA learner -> approximation BA -> counterexample refinement`
- 基础设施：`ROLL` Java library、query interfaces、`dk.brics.automaton`、benchmark tasks
- 适用场景：`\omega`-regular language learning、`LTL` benchmark 学习和 automata-theoretic reverse engineering
- 需求前提：需要 `MQ/EQ` teacher，目标语言应可落成 `\omega`-regular family
- 状态：🟢

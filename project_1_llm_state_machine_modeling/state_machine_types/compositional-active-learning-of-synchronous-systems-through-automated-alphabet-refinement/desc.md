# 通过自动字母表细化进行同步系统的组合式主动学习 / Compositional Active Learning of Synchronous Systems through Automated Alphabet Refinement

## 基本信息

- 标题：Compositional Active Learning of Synchronous Systems through Automated Alphabet Refinement
- 中文标题：通过自动字母表细化进行同步系统的组合式主动学习
- 作者：Léo Henry，Mohammad Reza Mousavi，Thomas Neele，Matteo Sammartino
- 发表：*CoRR / arXiv preprint*，`2504.16624v1`，2025
- DOI：`10.48550/arXiv.2504.16624`
- 链接：https://arxiv.org/abs/2504.16624
- 形式主义：`synchronizing LTS / CoalA / alphabet-distribution refinement`
- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：compositional active-learning route for synchronous `LTS` systems
- 工具/实现获取方式：原文明确说明作者实现了 `CoalA` 原型，并基于 `LearnLib` 完成实验；正文还提到附有 replication package，但当前提取文本未保留稳定下载链接。
- 标准/格式获取方式：核心承载对象是 `LTS`、alphabet distributions、local observations、membership/equivalence queries 和 `LearnLib` learner 组合；它不是交换标准。

## 简报

这篇论文补的是主动自动机学习里一条很重要的“从单体学习走向组合学习”的路线。现有 compositional learning 通常假设组件划分已知，或者只支持很受限的同步方式。本文的关键推进是：在不知道组件 alphabet 分解的情况下，边学习边自动 refinement alphabet distribution，把全局同步系统拆成若干本地 `LTS` 去学，并在 global counterexample 出现时系统地修正分解。

- 形式主义定位：围绕同步 `LTS` 组合的主动学习方法路线，而不是新的 automaton 母型。
- 构造方式简述：从 singleton alphabets 起步，收集全局 observation，对 distribution consistency 做检查；一旦出现 counterexample，就按 discrepancy 扩充 alphabet distribution，并为新组件启动 local learners。
- 基础设施与场景简述：依托 `CoalA`、`LearnLib`、distribution theory、counterexample-guided refinement 和 630+ benchmarks，服务并发系统逆向建模与组合式 automata learning。

```text
global teacher queries -> local observations -> alphabet-distribution refinement -> component learners -> composed hypothesis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. labelled transition systems；
2. parallel composition；
3. alphabet distributions；
4. distribution counterexamples；
5. `CoalA` 组合式学习算法。

### 核心抽象

论文首先固定 `LTS` 母型：

$$
T = (S, \Sigma, \rightarrow, \hat{s})
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `\Sigma` 是动作字母表。
3. `\rightarrow \subseteq S \times \Sigma \times S` 是转移关系。
4. `\hat{s}` 是初始状态。
5. 论文所有 compositional learning 都建立在同步 `LTS` 语义上。

未知系统的 alphabet decomposition 被写成：

$$
\Omega = \{\Sigma_1,\ldots,\Sigma_n\}, \quad \bigcup_{i=1}^n \Sigma_i = \Sigma
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是全局 alphabet。
2. `\Sigma_i` 是第 `i` 个组件的 local alphabet。
3. 这些 local alphabets 可以重叠。
4. 论文把这种集合称为 distribution。

### 一个最小例子与通俗解释

论文里的经典例子是两个组件共享动作 `b`：

1. 第一个组件 alphabet 类似 `{a,b,c}`。
2. 第二个组件 alphabet 类似 `{b,d}`。
3. 其中 `a,c,d` 是本地动作，`b` 是同步动作。
4. 如果一开始把每个字母都拆成 singleton alphabet，学习器会发现某些全局 observation 与当前分解不一致，于是把 `{a,b}` 或 `{b,c}` 之类 discrepancy 加回 distribution，逐步学到更合理的组件划分。

通俗地说，`CoalA` 不是先知道“系统由哪几个组件组成”，而是通过 counterexample 反过来把“组件应该怎么切”学出来。

### 运行 / 接受 / 转移语义

组件同步的平行组合可保守写成：

$$
\parallel_{i=1}^n T_i
$$

上式中的符号逐项解释如下：

1. `T_i` 是第 `i` 个局部 `LTS`。
2. 共享动作必须由所有拥有该动作的组件同时执行。
3. 不共享的本地动作可独立执行。
4. 论文的目标正是从全局查询结果中恢复这些局部 `T_i`。

对 observation 和 distribution 的一致性，论文写成：

$$
\Omega \models Obs
$$

上式中的符号逐项解释如下：

1. `\Omega` 是当前 alphabet distribution。
2. `Obs` 是目前累积到的全局 observation。
3. 当 `\Omega \models Obs` 时，当前分解与已知观测兼容。
4. 若不成立，就说明需要 refinement。

典型的 refinement 一步可以保守写成：

$$
\Omega' = \Omega \cup \{\delta\}
$$

上式中的符号逐项解释如下：

1. `\delta` 是从 distribution counterexample 中提取出的 discrepancy。
2. `\Omega'` 是更新后的 distribution。
3. 增加连接关系后，原先的 counterexample 会被消除或收缩。
4. 论文证明这种 refinement 过程会收敛到某个满足 `\Omega' \models Obs` 的分解。

### 语义边界

1. 该方法针对同步 `LTS` 组合，不是一般富数据 `EFSM` 学习。
2. 它依赖全局 alphabet 已知，且系统可通过 queries 访问。
3. 最终学到的组件划分不一定唯一，也不保证与真实实现的内部架构逐字对应。
4. 它主要处理离散同步行为，不包含时间或连续动力学。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `LTS` 母型 | `$T = (S, \Sigma, \rightarrow, \hat{s})$` | 目标学习对象是同步组合的 `LTS`。 |
| alphabet distribution | `$\Omega = \{\Sigma_1,\ldots,\Sigma_n\}$` | 组件划分由一组可能重叠的 local alphabets 给出。 |
| 一致性判定 | `$\Omega \models Obs$` | 当前分解是否与已知观测兼容。 |
| refinement | `$\Omega' = \Omega \cup \{\delta\}$` | 用 discrepancy 修正 alphabet 分解。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 目标就是恢复多个 `LTS` 组件。 |
| 事件 / 触发 | 很强 | alphabet 和同步动作是整个方法的核心。 |
| 守卫 / 数据 | 不支持 | 不处理富数据守卫。 |
| 层次 | 不支持 | 不是层次状态机学习。 |
| 并发 / 同步 | 很强 | 解决的正是同步并行系统的组合学习问题。 |
| 时间约束 | 不支持 | 不是 timed-learning 路线。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散并发行为学习。 |
| 可执行 / 可验证性 | 很强 | 已有 `CoalA + LearnLib` 原型与大规模 benchmark。 |

### 形式化问题与性质

1. 论文真正解决的是“组件划分未知时还能不能做 compositional learning”。
2. distribution consistency 把“架构发现”与“主动学习”统一到了同一循环里。
3. 与单体学习相比，`CoalA` 在大量 benchmark 上显著减少 membership queries。

## 构造方式与承载格式

### 建模入口

原文中的建模入口有：

1. 全局 `LTS` 的 alphabet；
2. membership / equivalence queries；
3. observation functions；
4. initial singleton distribution。

### 机器可处理承载方式

机器可处理承载方式包括：

1. global observations；
2. local alphabet distributions；
3. local learners 及其 hypotheses；
4. composed hypothesis；
5. counterexamples 与 discrepancies。

### 交换与互操作

这篇论文的互操作重点在：

1. `CoalA` 建立在 `LearnLib` 之上，而不是重做底层 learner；
2. 全局 teacher 与本地 learners 之间通过 observations 和 distribution refinement 协调；
3. local learning 与 global equivalence checking 形成闭环。

## 配套基础设施

- 建模/编辑工具：不主打图形建模，核心是 `CoalA`、`LearnLib` 和 query-based learning setup。
- 解析/交换/元模型支持：alphabets、observations、distributions、counterexamples。
- 仿真/执行支持：通过 teacher 对 black-box system 发起 membership / equivalence queries。
- 验证/分析支持：distribution consistency checking、discrepancy extraction、composed equivalence checking。
- 代码生成/转换支持：重点是从观测恢复组件模型，而不是部署代码生成。
- 标准化或社区生态：依附主动自动机学习与 `LearnLib` 社区。

## 适用场景与需求前提

### 适用场景

适合黑盒同步系统的逆向建模、组件发现、并发接口学习，以及想用组合方式缓解字母表爆炸的 automata learning 场景。

### 需求前提

1. 目标系统必须可 query。
2. 全局 alphabet 需要可获得或可枚举。
3. 行为应当主要服从同步 `LTS` 组合语义。
4. 组件划分未知，但希望由 counterexample 驱动自动发现。

### 不适用或高成本场景

如果系统含大量数据参数、复杂时钟或真正异步缓冲语义，`CoalA` 这套同步 `LTS` 分解假设就会变弱。

## 与相邻形式主义的关系

相对 [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)，本文不是通用学习平台，而是建立在 `LearnLib` 上的 compositional route；相对 [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)，本文更聚焦同步并发组件发现；相对 [grey-box-learning-of-register-automata/desc.md](../grey-box-learning-of-register-automata/desc.md)，后者补的是 data-aware `RA` 学习，本文补的是同步 `LTS` 组合学习。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机建模不只可以“从需求生成”，也可以“从系统交互行为恢复并分解”。
2. 对 `project_1` 而言，这为后续验证现有系统或做 baseline recovery 提供了很好的横向补充。
3. alphabet-refinement 的思想也适合迁移到“需求元素 -> 状态机组件划分”的自动建模问题。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像同步 `LTS` / automata learning 的方法路线，而不是最终输出形式主义。

### 对需求到模型生成的启发

1. 自动组件划分可以通过 counterexample 驱动，而不必全靠先验架构知识。
2. 对复杂系统，先恢复组件 alphabet，再恢复组件状态机，可能比直接学全局机更稳。
3. 学习框架与验证后端解耦，能让生成、验证、修复更容易串联。

## 重要的相关工作

- [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)：`CoalA` 所依附的主动学习基础设施。
- [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)：更晚的 `LearnLib` 生态总览。
- [grey-box-learning-of-register-automata/desc.md](../grey-box-learning-of-register-automata/desc.md)：数据化 `RA` 学习路线的代表条目。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 结论：这是一篇典型的组合式主动学习方法条目，适合作为同步 `LTS` 组件发现、alphabet-refinement 与 `LearnLib` 组合学习路线的关键证据入账。

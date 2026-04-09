# 开源 LearnLib：主动自动机学习框架 / The Open-Source LearnLib: A Framework for Active Automata Learning

## 基本信息

- 标题：The Open-Source LearnLib: A Framework for Active Automata Learning
- 中文标题：开源 LearnLib：主动自动机学习框架
- 作者：Malte Isberner，Falk Howar，Bernhard Steffen
- 发表：*Computer Aided Verification*，`LNCS 9206`，pp. 487-495，2015
- DOI：`10.1007/978-3-319-21690-4_32`
- 链接：https://doi.org/10.1007/978-3-319-21690-4_32
- 形式主义：`active automata learning / LearnLib / AutomataLib`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 论文角色：open-source active automata learning framework with reusable algorithms, oracles, filters and adapters
- 工具/实现获取方式：原文明确把新版 `LearnLib` 作为开源发布的 Java 框架，并强调 `AutomataLib`、学习算法、equivalence tests、SUL adapters、统计与可视化组件共同构成完整工具链。
- 标准/格式获取方式：核心承载不是统一交换标准，而是 `AutomataLib` abstraction layer、`LearnLib` components、Java API、GraphViz visualization、logging/import-export 与面向 SUL 的 adapter interfaces。

## 简报

这篇论文的重点，不是再讲一遍 `L*`，而是把主动自动机学习从“几个算法实现”升级成一套真正可复用的工程框架。新版 `LearnLib` 把 automata representation 拆到 `AutomataLib`，把学习器、counterexample handling、equivalence tests、filters、adapters 和 stats 分模块组织，再用开源发布和高性能实现把它变成研究与工业都能复用的基础设施。

- 形式主义定位：主动自动机学习基础设施，而不是新的被学习 automaton 本体。
- 构造方式简述：下层 `AutomataLib` 统一 automata abstraction、实现与算法；上层 `LearnLib` 组合 learning algorithms、equivalence-query approximations、infrastructure filters 和 SUL adapters。
- 基础设施与场景简述：依托 Java、模块化 learners/oracles/filters、可视化与统计组件，服务协议建模、接口逆向、GUI testing、smart card / bank card analysis 与 typestate inference。

```text
SUL + alphabet -> membership / equivalence infrastructure -> learning algorithm -> hypothesis automaton -> counterexample refinement loop
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. active automata learning；
2. `AutomataLib` abstraction / implementation / algorithm 三层结构；
3. learning algorithms；
4. equivalence-query approximation / conformance testing；
5. filters、caches、parallelization 与 SUL adapters。

### 核心抽象

可把 `LearnLib` 的学习工作流保守整理为：

$$
\mathcal{L} = (\Sigma, SUL, \mathrm{Learner}, \mathrm{EQ}, H)
$$

上式中的符号逐项解释如下：

1. `$\Sigma$` 是输入字母表。
2. `$SUL$` 是 system under learning。
3. `$\mathrm{Learner}$` 是具体学习算法，如 `L^\ast`、Observation Pack、TTT 等。
4. `$\mathrm{EQ}$` 是 equivalence-query 或其近似实现。
5. `$H$` 是当前 hypothesis automaton。
6. 这是对论文框架图与组件划分的保守抽象。

论文同时把 `AutomataLib` 架构拆成三层：

$$
\mathcal{A} = (\mathcal{I}, \mathcal{M}, \mathcal{G})
$$

上式中的符号逐项解释如下：

1. `$\mathcal{I}$` 是 abstraction layer，由细粒度 Java interfaces 组成。
2. `$\mathcal{M}$` 是 automata implementations 与 adapters。
3. `$\mathcal{G}$` 是 algorithms，如 minimization、equivalence testing、visualization。
4. 这层独立出来后，`LearnLib` 不再把 automata storage 和 learning logic 混在一起。

### 一个最小例子与通俗解释

一个最小例子可以这样理解：

1. 目标系统是一个可复位、可查询的接口程序。
2. 学习器不断发 membership queries，得到系统对输入串的响应。
3. 当当前 hypothesis 稳定后，用 conformance test 或随机方法找 counterexample。
4. 一旦找到反例，就用 counterexample analysis 更新 hypothesis，再重复。

通俗地说，`LearnLib` 像“自动机学习的积木盒”。你不用只会调一个固定算法，而是可以把 learner、cache、equivalence oracle、并行化和适配器拼成适合 конкрете SUL 的学习流程。

### 运行 / 接受 / 转移语义

其最核心的迭代可保守写成：

$$
H_{k+1} = \mathrm{Refine}(H_k, ce_k)
$$

上式中的符号逐项解释如下：

1. `$H_k$` 是第 `$k$` 次迭代得到的 hypothesis automaton。
2. `$ce_k$` 是本轮由 equivalence query 或其近似找到的 counterexample。
3. `$\mathrm{Refine}$` 表示学习算法根据反例更新 observation table、discrimination tree 或其他内部结构。

若把 equivalence step 抽成接口，则有：

$$
\mathrm{EQ}(H) \in \{\mathrm{OK}, ce\}
$$

上式中的符号逐项解释如下：

1. `$H$` 是当前 hypothesized model。
2. 若返回 `$\mathrm{OK}$`，表示在当前近似下没找到反例。
3. 若返回 `$ce$`，则学习继续。
4. 论文重点正是在于把这一步做成可替换的 tests / random walks / exhaustive checks。

### 语义边界

边界同样明确：

1. `LearnLib` 解决的是主动学习基础设施，不是直接从文本需求合成状态机。
2. 它默认存在可交互的 `SUL` 与稳定字母表。
3. 2015 版重点是 classical active learning 与 engineering framework，尚未把更丰富的数据型学习完整开源移植进来。
4. 学到的模型类型取决于具体 learner 与 automaton abstraction，不是无限泛化的。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 学习工作流 | `$\mathcal{L} = (\Sigma, SUL, \mathrm{Learner}, \mathrm{EQ}, H)$` | 概括 LearnLib 运行一个主动学习实验所需的核心接口。 |
| AutomataLib 架构 | `$\mathcal{A} = (\mathcal{I}, \mathcal{M}, \mathcal{G})$` | 把 automata storage / interfaces / algorithms 独立成可复用基础层。 |
| hypothesis refinement | `$H_{k+1} = \mathrm{Refine}(H_k, ce_k)$` | 学习循环的核心。 |
| equivalence step | `$\mathrm{EQ}(H) \in \{\mathrm{OK}, ce\}$` | conformance testing、random walk 等组件就是对这一步的工程化实现。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接支持 DFA、Mealy，以及若干 NFA / deterministic automata abstractions。 |
| 事件 / 触发 | 很强 | 学习流程围绕字母表输入和系统响应组织。 |
| 守卫 / 数据 | 条件支持 | 2015 论文主体仍偏经典学习；更丰富的 register automata 扩展被列为后续移植方向。 |
| 层次 | 不支持 | 不是 hierarchical-state learning framework。 |
| 并发 / 同步 | 条件支持 | 可学习交互系统接口，但不是显式并发语义平台。 |
| 时间约束 | 不支持 | 不是 timed automata learning 工具。 |
| 连续动态 / 随机性 | 不支持 | 主线是离散自动机学习。 |
| 可执行 / 可验证性 | 很强 | 算法、equivalence tests、filters、visualization、stats、SUL adapters 都已工程化。 |

### 形式化问题与性质

1. 论文真正补的是“如何把主动学习的所有零件标准化”，而不是单独某个 learner。
2. `AutomataLib` 独立化是结构性改进，使 automata manipulation 成为 LearnLib 之外也可复用的底层库。
3. cache、parallelization、state reuse 与 adapters 这些工程组件，是它和纯算法论文的核心区别。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `AutomataLib` interfaces 与 generic implementations；
2. learner 配置；
3. equivalence test / random test / exhaustive input generation；
4. SUL adapters，例如 Java classes、web services、stdio processes。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `AutomataLib` abstraction layer；
2. `LearnLib` algorithms / oracles / infrastructure components；
3. import/export 与 logging；
4. GraphViz-based visualization；
5. statistics 与 experiment components。

### 交换与互操作

互操作重点在接口抽象：

1. 算法只依赖 abstraction layer，而不绑定单一 automaton implementation。
2. wrapped third-party automata libraries 也能接到 `AutomataLib` 接口中。
3. SUL adapters 让真实程序、协议实现和服务都能接到同一学习工作流。

## 配套基础设施

- 建模/编辑工具：主体不是图形建模器，而是 Java framework、API、visualization 与 statistics tooling。
- 解析/交换/元模型支持：`AutomataLib` 提供 abstraction layer 和 import/export mechanism。
- 仿真/执行支持：通过 SUL adapters、query filters、state reuse 和 workers 与真实系统交互。
- 验证/分析支持：perfect equivalence、W-method、Wp-method、random walk、random tests、exhaustive tests。
- 代码生成/转换支持：不以部署代码生成见长，但支持 hypothesis import/export 与 GraphViz visualization。
- 标准化或社区生态：开源发布、Java 生态、`AutomataLib` / `LearnLib` 双层社区，以及后续 LearnLib 系列演化。

## 适用场景与需求前提

### 适用场景

适合协议接口逆向、黑盒组件建模、GUI / web / service regression checking，以及任何可以通过 queries 与系统交互的 learning-based modeling 场景。

### 需求前提

1. 存在可交互的 `SUL`。
2. 输入字母表可被稳定定义。
3. 能够实现 membership queries 与某种形式的 equivalence approximation。
4. 团队更关心“从现有系统恢复模型”，而不是“从需求直接合成模型”。

### 不适用或高成本场景

若系统根本不可查询、不可复位、输入字母表难以抽象，或目标是 rich timed / hybrid semantics，`LearnLib` 就不是主战场。

## 与相邻形式主义的关系

相对 [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)，这篇 2015 论文是开源 LearnLib 的早期母线，重点在 open-source rewrite 与框架重构；相对 [aalpy-an-active-automata-learning-library/desc.md](../aalpy-an-active-automata-learning-library/desc.md)，`AALpy` 更偏 Pythonic 轻量工作流，而本文更强调 Java 模块化工程框架；相对 [combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md](../combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md)，后者关注 dataful `RA/EFSM` 学习方法，本篇关注通用主动学习基础设施。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“从系统行为反推状态机”已经有成熟工具框架，不必所有状态机都从需求文本正向生成。
2. 若未来要把 LLM 生成的模型与真实实现做黑盒对照，`LearnLib` 这类工具是很现实的 baseline / side channel。
3. `AutomataLib` 与 `LearnLib` 的分层也很适合作为研究工具架构参考。

### 作为目标形式主义还是中间表示

更像状态机恢复与验证的基础设施，而不是最终交付给工程师的前端状态机语言。

### 对需求到模型生成的启发

1. 前端生成与黑盒学习不是互斥路线，可以互相做 consistency check。
2. 算法、oracle、adapter 与 cache 的模块化边界值得复用到 LLM 驱动的闭环工具里。
3. 一套可组合框架比“只实现一个论文算法”更适合长期研究演化。

### 现实限制

论文强调的是从交互系统恢复模型；如果研究对象没有可交互实现或测试接口，这条路就难以落地。

## 重要的相关工作

1. [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)：LearnLib 十年后版本的现代化总结。
2. [aalpy-an-active-automata-learning-library/desc.md](../aalpy-an-active-automata-learning-library/desc.md)：更轻量的 Python active learning 基础设施。
3. [combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md](../combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md)：`RA/EFSM` 学习方法扩展路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 形式主义：`active automata learning / LearnLib / AutomataLib`
- 论文角色：open-source active automata learning framework with reusable algorithms, oracles, filters and adapters
- 归类理由：论文主体是主动自动机学习框架、底层 automata 库与 query/oracle/adapter 组件化基础设施，而不是某个单独学习算法。

# AALpy：主动自动机学习库 / AALpy: an active automata learning library

## 基本信息

- 标题：AALpy: an active automata learning library
- 中文标题：AALpy：主动自动机学习库
- 作者：Edi Muškardin，Bernhard K. Aichernig，Ingo Pill，Andrea Pferscher，Martin Tappler
- 发表：*Innovations in Systems and Software Engineering*，18(3):417-426，2022
- DOI：`10.1007/s11334-022-00449-3`
- 链接：https://doi.org/10.1007/s11334-022-00449-3
- 形式主义：`Active Automata Learning / AALpy`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 论文角色：Python active automata learning library / modular learning infrastructure
- 工具/实现获取方式：原文明确给出 GitHub 入口 `https://github.com/DES-Lab/AALpy` 与 wiki 文档，并强调工具以 `Python` 实现。
- 标准/格式获取方式：原文未主打中立交换标准；主要承载方式是 `Python` API、`SUL` 接口、equivalence oracles、可视化导出和将 `MDP` 导出到 `PRISM` 格式。

## 简报

这篇论文的关键价值，在于把主动自动机学习从“若干算法实现”落成一个轻量、可组合、可快速试验的 `Python` 基础设施。`AALpy` 不只支持确定型 `DFA / Mealy / Moore`，还支持 `ONFSM`、`MDP`、`SMM`，并把 `membership query`、`equivalence oracle`、cache、visualization 和 `PRISM` 导出等能力收进同一库里。

- 形式主义定位：主动自动机学习基础设施，而不是新的状态机本体。
- 构造方式简述：围绕 minimally adequate teacher 框架，把 `SUL`、membership/equivalence query、learner 与反例 refinement 组合成可复用 learning loop。
- 基础设施与场景简述：依托 `Python`、GitHub、wiki、缓存、oracle 组合与 stochastic-model export，服务黑盒系统建模、测试、调试和 verification handoff。

```text
SUL + alphabet -> MQ / EQ oracles -> learner -> hypothesis automaton -> counterexample refinement -> reusable learning workflow
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `AALpy`：

1. system under learning (`SUL`)；
2. membership queries 与 equivalence queries；
3. learner 与 hypothesis model；
4. `DFA / Mealy / Moore / ONFSM / MDP / SMM`；
5. cache、visualization 与 `PRISM` export。

### 核心抽象

结合论文对 learning workflow 的表述，可把一次学习过程保守整理为：

$$
\mathcal{L} = (\Sigma, SUL, MQO, EQO, Learner, H)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是交互字母表。
2. `SUL` 是被学习系统。
3. `MQO` 是 membership-query oracle。
4. `EQO` 是 equivalence oracle。
5. `Learner` 是所选学习算法。
6. `H` 是当前 hypothesis automaton。

membership query 和 equivalence query 的职责可压成：

$$
MQO : \Sigma^* \to O, \qquad EQO(H) \in \{\bot\} \cup CEX
$$

上式中的符号逐项解释如下：

1. `O` 是观测输出域。
2. `MQO` 对输入串执行查询并返回系统行为。
3. `EQO(H)` 若返回 `\bot`，表示暂未找到反例。
4. 若返回 `CEX`，则说明假设模型 `H` 被反例推翻。

论文还明确给出库覆盖的主要模型族。可写成：

$$
\mathcal{M} = \{ DFA, Mealy, Moore, ONFSM, MDP, SMM \}
$$

上式中的符号逐项解释如下：

1. `DFA / Mealy / Moore` 是确定型常见模型。
2. `ONFSM` 是 observable nondeterministic finite-state machine。
3. `MDP` 是 Markov decision process。
4. `SMM` 是 stochastic Mealy machine。
5. 这说明 `AALpy` 不只是一个 DFA learner。

### 一个最小例子与通俗解释

论文给出的最小入口非常清楚：

1. 用户先定义一个 `SUL` 类。
2. 这个类至少实现 `pre()`、`step(letter)`、`post()`。
3. 再选择一个 equivalence oracle 和 learner。
4. 运行后得到 learned automaton。

通俗地说，`AALpy` 像“自动机学习的 Python 积木盒”。你不必从头写查询循环，只要告诉它如何和真实系统交互，它就能一轮轮地“问行为 -> 猜模型 -> 找反例 -> 修正模型”。

### 运行 / 接受 / 转移语义

论文中的 learning loop 可保守写成：

$$
H_{i+1} =
\begin{cases}
\mathrm{refine}(H_i, cex_i), & EQO(H_i) = cex_i \neq \bot \\
H_i, & EQO(H_i) = \bot
\end{cases}
$$

上式中的符号逐项解释如下：

1. `H_i` 是第 `i` 轮 hypothesis。
2. `cex_i` 是 equivalence oracle 返回的 counterexample。
3. `\mathrm{refine}` 表示 learner 用反例更新假设。
4. 若找不到反例，当前模型就是当前轮的稳定结果。

对 stochastic learning，论文还强调 `AALpy` 支持树查询和 `MDP/SMM` 学习。可保守写成：

$$
\mathrm{Learn}_{stoch} : (SUL, \Sigma, EQO) \to \{ MDP, SMM \}
$$

上式中的符号逐项解释如下：

1. `SUL` 和 `\Sigma` 仍是黑盒系统及其交互字母表。
2. `EQO` 在 stochastic setting 下采用相应的随机测试 oracle。
3. 输出是 learned `MDP` 或 `SMM` 模型。
4. 这说明 `AALpy` 已把 active learning 推向概率行为对象。

### 语义边界

这篇论文的边界主要有：

1. 主动学习要求系统可复位、可查询或至少可稳定采样。
2. 它解决的是“从行为学习模型”，不是“从自然语言直接生成模型”。
3. 学习效果高度依赖字母表设计、oracle 质量和抽象粒度。
4. 对富连续系统，往往还需要额外 abstraction 才能落到可学习对象。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 学习流程骨架 | `$\mathcal{L} = (\Sigma, SUL, MQO, EQO, Learner, H)$` | `AALpy` 围绕哪些核心对象组织学习。 |
| 查询接口 | `$MQO : \Sigma^* \to O,\ EQO(H) \in \{\bot\} \cup CEX$` | membership/equivalence query 的最小职责。 |
| 反例驱动 refinement | `$H_{i+1} = \mathrm{refine}(H_i, cex_i)$` | 学习如何逐步逼近真实系统。 |
| 覆盖模型族 | `$\mathcal{M} = \{ DFA, Mealy, Moore, ONFSM, MDP, SMM \}$` | 工具覆盖面已扩到非确定和随机系统。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向多类自动机模型。 |
| 事件 / 触发 | 很强 | 学习流程由输入字母和输出观察驱动。 |
| 守卫 / 数据 | 条件支持 | 原生不是富数据 DSL，但可通过 abstraction / mapper 扩展。 |
| 层次 | 弱支持 | 主线不在层次状态机。 |
| 并发 / 同步 | 间接支持 | 通过黑盒接口学习系统交互，而非直接建模并发语义。 |
| 时间约束 | 弱支持 | 论文主线不在 timed learning。 |
| 连续动态 / 随机性 | 支持随机性，不支持连续动态 | `MDP/SMM` 已支持；连续 ODE 不在主线。 |
| 可执行 / 可验证性 | 很强 | cache、oracle、visualization 和 `PRISM` export 已具工程成熟度。 |

### 形式化问题与性质

1. `AALpy` 的价值在于“学习算法 + 查询基础设施 + 输出互操作”被做成同一库。
2. 与只实现单算法的原型不同，它已经覆盖 deterministic、non-deterministic 和 stochastic 三条线。
3. 对本文库而言，它补的是自动机学习这条工具基础设施主干。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 定义字母表；
2. 实现 `SUL` 的 `pre/post/step` 接口；
3. 选择 equivalence oracle；
4. 选择 learner 并执行 learning loop。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Python` API；
2. `SUL` 抽象接口；
3. cache 和 oracle 组件；
4. 可视化输出；
5. learned `MDP` 到 `PRISM` 的导出格式。

### 交换与互操作

这篇论文的互操作重点在组件接口和后端导出：

1. 用户可以快速替换 learner、oracle 和 query cache。
2. learned stochastic models 可导出到 `PRISM` 格式。
3. GitHub wiki 和可视化功能让研究复现与教学更方便。

## 配套基础设施

- 建模/编辑工具：不是图形编辑器，而是 `Python` 库与示例脚本。
- 解析/交换/元模型支持：`SUL` 接口、query cache、oracle 组合和 `PRISM` export。
- 仿真/执行支持：直接对真实或仿真的 `SUL` 发起查询。
- 验证/分析支持：conformance testing-based equivalence oracles、counterexample processing、visualization。
- 代码生成/转换支持：支持 learned stochastic model 到 `PRISM` 的导出。
- 标准化或社区生态：GitHub、wiki、case studies 和 `Python` 生态共同构成可复用社区入口。

## 适用场景与需求前提

### 适用场景

适合黑盒系统建模、接口协议推断、测试基线构造、调试、学习驱动验证以及需要快速尝试主动自动机学习流程的研究和工程场景。

### 需求前提

1. 系统可被复位并接受可控查询。
2. 交互字母表能被稳定定义。
3. 用户接受“先学模型，再做验证/测试/比较”的工作流。
4. 若要学随机模型，系统应支持稳定的 stochastic sampling。

### 不适用或高成本场景

如果目标根本不可查询，或者需求一开始就需要从自然语言直接得到正式模型，`AALpy` 就不在主战场。

## 与相邻形式主义的关系

相对 [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)，二者都属于主动自动机学习基础设施，但 `AALpy` 更强调 `Python` 轻量性和 stochastic learning；相对 [a-robust-class-of-data-languages-and-an-application-to-learning/desc.md](../a-robust-class-of-data-languages-and-an-application-to-learning/desc.md)，后者更偏学习对象本体与理论，本文更偏工程化工具；相对 [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)，`PRISM` 是验证后端，而 `AALpy` 可以把 learned `MDP` 交给这类后端继续分析。

## 与本研究的关系

### 对 Project 1 的价值

1. 它为“从既有系统行为反推状态机”提供了成熟工具锚点，可补足纯生成路线之外的学习/修正闭环。
2. 如果未来要用黑盒行为来校验或修复 LLM 生成的状态机，`AALpy` 这类框架很有现实价值。
3. 它也提示 `project_1`：状态机自动化不仅是生成与验证，还包括从运行行为中学习和对齐模型。

### 作为目标形式主义还是中间表示

它是基础设施和工作流平台，而不是最终状态机本体。

## 重要的相关工作

- [learnlib-10-years-later/desc.md](../learnlib-10-years-later/desc.md)：同类主动自动机学习框架的另一条主线。
- [a-robust-class-of-data-languages-and-an-application-to-learning/desc.md](../a-robust-class-of-data-languages-and-an-application-to-learning/desc.md)：学习对象本体扩展的理论条目。
- [prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md](../prism-a-tool-for-automatic-verification-of-probabilistic-systems/desc.md)：`AALpy` learned stochastic model 的典型下游验证后端。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Active Automata Learning / AALpy`
- 论文角色：Python active automata learning library / modular learning infrastructure
- 核心功能：把主动自动机学习流程做成可复用的 `Python` 基础设施
- 关键特性：`DFA/Mealy/Moore/ONFSM/MDP/SMM`、oracles、cache、visualization、`PRISM` export
- 构造方式：`SUL + alphabet + MQ/EQ + learner` 组合成 learning loop
- 基础设施：GitHub、wiki、`Python` API、oracle 组件、stochastic model export
- 适用场景：黑盒系统建模、测试、调试与学习驱动验证
- 需求前提：系统需可查询/复位，且交互字母表可定义

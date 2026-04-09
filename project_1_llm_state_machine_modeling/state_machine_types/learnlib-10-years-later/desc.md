# LearnLib：十年后的主动自动机学习框架 / LearnLib: 10 years later

## 基本信息

- 标题：LearnLib: 10 years later
- 中文标题：LearnLib：十年后的主动自动机学习框架
- 作者：Markus Frohme，Falk Howar，Bernhard Steffen
- 发表：*Computer Aided Verification*，pp. 141-160，2025
- DOI：`10.1007/978-3-031-98685-7_7`
- 链接：https://doi.org/10.1007/978-3-031-98685-7_7
- 形式主义：`Active Automata Learning / LearnLib`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 论文角色：主动自动机学习框架 / 模块化黑盒学习工具链
- 工具/实现获取方式：论文明确给出 `https://github.com/LearnLib/learnlib` 作为开源入口，说明其基于 `Java`、以 `Apache 2.0` 许可证发布，并已部署到 `Maven Central`。
- 标准/格式获取方式：原文未主打某个中立交换格式，而是强调 `LearnLib` 的 `Java` API、模块化组件、`JPMS` / Maven 工件与 GitHub 文档站点。

## 简报

这篇论文的重点，不是提出新的自动机家族，而是把主动自动机学习从“若干算法实现”提升为一个可组合的工程框架。`LearnLib` 把 learner、membership oracle、equivalence oracle、cache、parallel oracle、counterexample analyzer、driver 和 SUL 访问层拆成可替换构件，让用户可以快速拼出贴合具体系统的学习流程。

- 形式主义定位：主动自动机学习基础设施，而不是新的状态机本体。
- 构造方式简述：围绕 minimally adequate teacher 框架，把 `SUL`、membership/equivalence oracles 和 learner 组合成循环式学习流程。
- 基础设施与场景简述：依托 `Java`、`GitHub`、`Maven Central`、parallel oracles、caches、`LTSmin` 接口和 procedural learners，服务黑盒模型推断、monitoring 和 model-based QA。

```text
SUL + symbolic alphabet -> membership/equivalence oracles -> learner -> hypothesis automaton -> counterexample refinement -> reusable learning workflow
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `system under learning (SUL)`；
2. membership oracle 与 equivalence oracle；
3. learner / hypothesis model；
4. `DFA / Mealy / Moore / VPA / SPA / SBA / SPMM` 等被学习模型族；
5. caches、parallel oracles、counterexample analyzers 与 drivers。

### 核心抽象

结合论文对 minimally adequate teacher 框架的表述，可把一次学习过程保守整理为：

$$
\mathcal{L} = (\Sigma, SUL, MQO, EQO, Learner, H)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是系统交互字母表。
2. `SUL` 是被学习系统。
3. `MQO` 是 membership oracle，用于回答行为查询。
4. `EQO` 是 equivalence oracle，用于寻找反例。
5. `Learner` 是具体学习算法。
6. `H` 是当前假设模型。

membership oracle 与 equivalence oracle 的职责可压成：

$$
MQO : \Sigma^* \to O, \quad EQO(H) \in \{\bot\} \cup CEX
$$

上式中的符号逐项解释如下：

1. `O` 是系统输出域；对接受器模型它可能是 `Boolean`，对 `Mealy`/`SPMM` 则通常是输出字或输出序列。
2. `MQO` 输入一个查询串，返回 `SUL` 的观测行为。
3. `EQO(H)` 要么返回 `\bot` 表示未找到反例，要么返回 counterexample `CEX`。
4. 这正对应论文对 exploration/verification 两相过程的描述。

学习主循环可保守写成：

$$
H_{i+1} = \mathrm{refine}(H_i, cex_i) \text{ if } EQO(H_i)=cex_i \neq \bot,\quad H_{i+1} = H_i \text{ if } EQO(H_i)=\bot
$$

上式中的符号逐项解释如下：

1. `H_i` 是第 `i` 轮的假设模型。
2. `cex_i` 是第 `i` 轮等价测试发现的反例。
3. `\mathrm{refine}` 表示 learner 用反例修正假设模型。
4. 如果 `EQO` 找不到反例，当前模型就被视为本轮稳定结果。

论文的框架图还说明 `LearnLib` 覆盖的模型不止 DFA/Mealy，而是扩展到：

$$
\mathcal{M} = \{ DFA, Mealy, Moore, VPA, SPA, SBA, SPMM \}
$$

上式中的符号逐项解释如下：

1. `DFA / Mealy / Moore` 是规则型有限状态模型。
2. `VPA` 是 visibly pushdown automata。
3. `SPA / SBA / SPMM` 是 procedural / context-free 方向的系统模型。
4. 这解释了为什么 `LearnLib` 不只是“某个 DFA learner”，而是更广的 learning framework。

### 一个最小例子与通俗解释

论文给了一个很清晰的 `SPMM` 学习例子：

1. 先准备 `alphabet` 和两个本地系统实例。
2. 用 `ParallelOracleBuilders` 建并行 membership oracle。
3. 用 `MealyCaches.createCache` 给查询链加缓存。
4. 用 `SampleSetEQOracle + WMethodEQOracle` 组成 equivalence oracle chain。
5. 再用 `SPMMLearner(..., TTTAdapterMealy::new)` 启动学习。

通俗地说，`LearnLib` 像“自动机学习里的积木盒”。你不再是直接调用一个单独算法，而是把查询层、验证层、缓存层、并行层和 learner 像积木一样拼起来，然后不停地“猜模型 -> 找反例 -> 改模型”。

### 运行 / 接受 / 转移语义

论文中的实际运行逻辑就是经典 learning loop：

$$
\mathrm{while}\ ((cex = EQO(H,\Sigma)) \neq \bot)\ :\ H := Learner.\mathrm{refine}(cex)
$$

上式中的符号逐项解释如下：

1. `EQO(H,\Sigma)` 用当前假设模型和字母表找反例。
2. `cex` 是找到的反例。
3. `Learner.refine` 负责把反例反向灌回 learner。
4. 这条循环同时适用于离线学习与论文强调的 monitoring-based life-long learning。

### 语义边界

这篇论文也清楚给出了边界：

1. 主动学习要求 `SUL` 可被查询，且外部能控制或观测输入/输出。
2. `LearnLib` 解决的是黑盒模型推断，不是从自然语言需求直接生成状态机。
3. 框架很强，但具体能否学到有用模型，仍取决于字母表设计、oracle 质量和 formalism 选择。
4. 论文强调的是工程成熟度与组合性，不是单一算法复杂度新结果。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 学习流程骨架 | `$\mathcal{L} = (\Sigma, SUL, MQO, EQO, Learner, H)$` | 说明 `LearnLib` 围绕哪些核心接口组织。 |
| 查询接口 | `$MQO : \Sigma^* \to O,\ EQO(H) \in \{\bot\} \cup CEX$` | 对应 membership/equivalence oracles 的最小职责。 |
| 反例驱动 refinement | `$H_{i+1} = \mathrm{refine}(H_i, cex_i)$` | 说明学习过程如何递进。 |
| 覆盖模型族 | `$\mathcal{M} = \{ DFA, Mealy, Moore, VPA, SPA, SBA, SPMM \}$` | 说明框架不是单一 `DFA` learner。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向多类 automata-based models。 |
| 事件 / 触发 | 很强 | 通过字母表与输入/输出查询驱动学习。 |
| 守卫 / 数据 | 条件支持 | 可通过更 expressive formalisms 或外部 abstraction 扩展，但不是原生富数据 DSL。 |
| 层次 | 弱支持 | 主线不在层次状态机，而在 regular / procedural models。 |
| 并发 / 同步 | 间接支持 | 通过学习系统接口行为处理，不直接建模并发语义。 |
| 时间约束 | 弱支持 | 论文主线不在 timed learning。 |
| 连续动态 / 随机性 | 有扩展潜力 | 可学习的 formalism 在扩张，但本文核心仍是离散 black-box 行为。 |
| 可执行 / 可验证性 | 很强 | 组件化学习链、并行查询、缓存、`LTSmin` 集成都已落地。 |

### 形式化问题与性质

1. `LearnLib` 最大的价值在于“组件可替换而工作流不散”。
2. 从 regular learners 到 procedural learners、从 classic oracles 到 adaptive/parallel/cached oracles，这篇论文展示的是基础设施宽度。
3. 这种组合能力对研究和工程都重要，因为它显著降低了比较算法、构建专用流程和做长期维护的成本。

## 构造方式与承载格式

### 建模入口

`LearnLib` 的建模入口不是图形状态机，而是：

1. 定义交互字母表；
2. 封装 `SUL` 访问接口；
3. 选择或组合 oracle；
4. 选择 learner 与 counterexample analysis；
5. 运行 learning loop。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Java` API；
2. Maven 工件；
3. learners / oracles / caches / drivers 这组模块化组件；
4. GitHub 仓库和文档站点。

### 交换与互操作

其互操作重点在组件级接口而非文件标准：

1. membership oracles 与 equivalence oracles 共享统一抽象接口。
2. procedural learner 可以参数化 regular learner。
3. 外部模型检查器 `LTSmin` 可作为 black-box checking equivalence oracle 接入。

## 配套基础设施

- 建模/编辑工具：不是图形编辑器路线，核心是 `Java` 框架与库组件。
- 解析/交换/元模型支持：通过模块化 API、`JPMS`、Maven Central 与 GitHub 工程实践提供复用入口。
- 仿真/执行支持：可以直接把学习流程跑在真实或复制的 `SUL` 实例上。
- 验证/分析支持：支持 `W-method`、random walk、sampling、`LTSmin` black-box checking 等等价测试路线。
- 代码生成/转换支持：不以代码生成为主，而是面向行为模型推断与后续监控/验证衔接。
- 标准化或社区生态：`Apache 2.0`、GitHub discussions、文档站点、持续集成和开放贡献流程都较成熟。

## 适用场景与需求前提

### 适用场景

适合黑盒接口学习、协议/组件行为建模、monitoring-based learning、model-based quality assurance，以及需要快速比较不同 automata learning setups 的研究与工程场景。

### 需求前提

1. 目标系统可被查询和复位，或至少可通过 monitor 持续采样。
2. 交互字母表能被稳定定义。
3. 任务愿意接受“先学模型再做验证/监控”的两阶段路线。
4. 团队能处理学习 formalism、反例质量和缓存/并行策略这些工程参数。

### 不适用或高成本场景

如果需求一开始就是从文本需求直接合成正式状态机，而没有可查询系统对象，`LearnLib` 就不在主战场；它更适合“系统已存在，但模型未知”的场景。

## 与相邻形式主义的关系

相对 [a-robust-class-of-data-languages-and-an-application-to-learning/desc.md](../a-robust-class-of-data-languages-and-an-application-to-learning/desc.md)，那篇强调学习对象本身的理论扩展，这篇强调把学习流程做成成熟框架；相对 [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)，`LearnLib` 不是 automata 本体奠基，而是黑盒反推 automata 模型的基础设施；相对 [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)，`LearnLib` 关注如何学习 `VPA` 一类模型，而不是定义 `VPL/VPA` 本身。

## 与本研究的关系

### 对 Project 1 的价值

1. 它为“从已有系统反推状态机”提供了成熟工具锚点，可作为生成路线之外的重要旁证。
2. 若后续需要对 LLM 生成的状态机做黑盒一致性检查，`LearnLib` 这类框架能提供现实的对照基线。
3. 它也提示 `project_1`：状态机研究不只包括生成和验证，也包括从系统行为中学习和修正模型的闭环。

### 局限

1. 它不直接解决自然语言需求建模。
2. 对富数据、时间和混成控制系统，仍需更多 abstraction 或更强 formalism 支撑。

## 重要的相关工作

- [a-robust-class-of-data-languages-and-an-application-to-learning/desc.md](../a-robust-class-of-data-languages-and-an-application-to-learning/desc.md)：展示学习对象从 regular 扩展到数据语言时的另一条线。
- [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)：提供被学习自动机家族的经典理论基线。
- [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)：对应 `LearnLib` 已覆盖的 `VPA` 方向。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 结论：这是一篇很适合补入“主动学习/黑盒建模”广度的基础设施条目，能把文库的状态机工具链视角从“建模/验证”进一步扩到“学习/修正”。

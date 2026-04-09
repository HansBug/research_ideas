# 使用 Petri 网对多机器人任务进行建模、分析与执行 / Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets

## 基本信息

- 标题：Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets
- 中文标题：使用 Petri 网对多机器人任务进行建模、分析与执行
- 作者：Hugo Costelha, Pedro Lima
- 发表：*Proceedings of the 7th International Joint Conference on Autonomous Agents and Multiagent Systems (AAMAS 2008)*, pp. 1187-1190, 2008
- DOI：`10.65109/vkfc7194`
- 链接：https://doi.org/10.65109/vkfc7194
- 形式主义：`MOPN / GSPN for Multi-Robot Tasks`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：多机器人任务建模 / Petri 网分析执行框架
- 工具/实现获取方式：原文把任务模型组织为可展开的 `PN` 模块与分析版本通信动作，强调 qualitative analysis 与 Markov-chain based quantitative analysis；具体分析工具未固定到某一软件。
- 标准/格式获取方式：承载方式是 `Marked Ordinary Petri Nets (MOPNs)`、`Generalised Stochastic Petri Nets (GSPNs)`、macro places 和 predicate places；原文未提供统一交换标准。

## 简报

这篇论文的价值在于，它没有把 Petri 网只当“能表达并发”的理论模型，而是把多机器人任务拆成一组可复用、可组合、可分析、还能落到执行层的 `PN` building blocks。特别是它把机器人间同步消息、环境谓词、动作原语和任务层次都塞进同一套 `MOPN/GSPN` 框架里，并明确区分了用于执行的任务网和用于分析的闭环环境网。

- 形式主义定位：面向多机器人协作任务的 `Petri Net` 应用框架，而不是纯工作流或纯制造系统建模。
- 构造方式简述：以 macro places、predicate places 和 action/environment layers 组织任务，再用 `MOPN` 做结构正确性分析，用 `GSPN` 做成功概率与性能分析。
- 基础设施与场景简述：依托 PN 组合、marking graph 与 Markov-chain analysis，服务多机器人同步、显式/隐式通信和任务执行分析。

```text
多机器人任务需求 -> action / environment Petri net blocks -> macro-place 组合 -> MOPN / GSPN 分析 -> 任务执行与性能评估
```

## 形式主义定义与核心对象

### 定义对象

论文的核心对象包括：

1. individual robot task plans。
2. multi-robot synchronisation 与 communication actions。
3. environment models。
4. `MOPN` 与 `GSPN` 两类 Petri 网视图。
5. macro places、predicate places 和 layered task models。

### 核心抽象

论文没有单独重新定义 Petri 网元组，而是直接说明采用 `MOPN` 与 `GSPN`。据其建模方式，可把基础任务网保守整理为：

$$
PN = (P, T, Pre, Post, M_0)
$$

上式中的符号逐项解释如下：

1. `P` 是 place 集合，对应 primitive actions、subtasks、predicates 或 communication conditions。
2. `T` 是 transition 集合，对应事件发生或任务控制逻辑推进。
3. `Pre` 是输入弧关系。
4. `Post` 是输出弧关系。
5. `M_0` 是初始 marking。

论文还显式区分 `MOPN` 与 `GSPN`。据其描述，可把性能分析用网保守整理为：

$$
GSPN = (P, T_{imm}, T_{exp}, Pre, Post, \lambda, \pi, M_0)
$$

上式中的符号逐项解释如下：

1. `T_{imm}` 是立即变迁集合。
2. `T_{exp}` 是指数定时变迁集合。
3. `\lambda` 为定时变迁的 firing rate。
4. `\pi` 为随机分支或 switch 的概率参数。
5. 其他符号与普通 Petri 网定义一致。

论文最有特色的不是上述标准元组本身，而是 macro place：

$$
\mathit{MP} = (N_{sub}, P_{in}, P_{out})
$$

上式中的符号逐项解释如下：

1. `N_{sub}` 是被封装的子网。
2. `P_{in}` 是输入 connection places。
3. `P_{out}` 是输出 connection places。

这使得一个复杂任务网可以像单个 place 一样被展开或折叠。

### 一个最小例子与通俗解释

论文的直观例子来自 robotic soccer / multi-robot passing：

1. 一台机器人先执行某个 primitive action。
2. 另一台机器人必须在收到显式消息，或通过视觉观察到队友动作后，才能进入下一子任务。
3. place 可以表示“球已传出”“队友已就位”“通信已收到”。
4. transition 表示“开始跑位”“执行传球”“确认接球”等离散事件。

通俗地说，这里的 Petri 网像一块“多机器人协作布线板”：token 在不同的条件节点流动，一旦某些资源、消息和动作条件都到位，相应 transition 就能触发，整个团队任务才会往前推进。

### 运行 / 接受 / 转移语义

Petri 网 firing 语义可保守写成：

$$
M \xrightarrow{t} M'
$$

当且仅当变迁 `t` 在 marking `M` 下使能，并在 firing 后得到新 marking `M'`。

若采用普通单位权值弧，其使能条件可写为：

$$
\forall p \in {}^\bullet t,\quad M(p) \ge 1
$$

上式中的符号逐项解释如下：

1. `${}^\bullet t` 是变迁 `t` 的输入 places。
2. `M(p)` 是 place `p` 中 token 的数量。
3. 每个输入 place 至少有一个 token，表示执行该事件的先决条件都已满足。

触发后的 marking 更新可保守写成：

$$
M' = M - {}^\bullet t + t^\bullet
$$

上式中的符号逐项解释如下：

1. `{}^\bullet t` 表示输入弧消耗的 token。
2. `t^\bullet` 表示输出弧产生的 token。
3. 整体含义是：任务条件被消费、后继条件被激活。

论文对 `GSPN` 还强调：其 marking process 构成 semi-Markov process，并可进一步导出 Markov chain 用于性能分析。可保守写成：

$$
\mathcal{M}(GSPN) \Rightarrow MC(GSPN)
$$

这里的符号逐项解释如下：

1. `\mathcal{M}(GSPN)` 表示由 `GSPN` marking 诱导的半马尔可夫过程。
2. `MC(GSPN)` 表示进一步得到的 Markov chain。
3. 论文借此分析成功概率、达到某状态的期望时间等指标。

### 语义边界

这篇论文的 Petri 网语义边界同样明确：

1. 它主要处理离散任务与同步，不直接建模连续控制律。
2. 重点是“任务执行 + 闭环环境分析”，而不是一般高层规划算法。
3. 通信被抽象成 place / transition / predicate，而不是复杂协议栈。
4. 结果更偏设计与分析框架，而不是统一标准文件格式。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基础任务网 | `$PN = (P, T, Pre, Post, M_0)$` | place 表示动作/谓词/子任务，transition 表示事件。 |
| 性能分析网 | `$GSPN = (P, T_{imm}, T_{exp}, Pre, Post, \lambda, \pi, M_0)$` | 把执行时序与随机成功率也压进同一模型。 |
| 宏节点 | `$\mathit{MP} = (N_{sub}, P_{in}, P_{out})$` | 允许把子任务网折叠成可复用 building block。 |
| 执行语义 | `$M \xrightarrow{t} M'$` | 表示多机器人任务从一组条件推进到下一组条件。 |
| 使能条件 | `$\forall p \in {}^\bullet t,\ M(p) \ge 1$` | 所有同步前提、资源和通信条件必须到位。 |
| 分析路径 | `$\mathcal{M}(GSPN) \Rightarrow MC(GSPN)$` | 结构网还能导出概率/性能分析模型。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 部分支持 | place/marking 表达任务状态，但不是传统单控制状态机。 |
| 事件 / 触发 | 强支持 | 事件直接由 transition 建模。 |
| 守卫 / 数据 | 支持 | 通过 predicate places、环境谓词和 stochastic parameters 间接表达。 |
| 层次 | 强支持 | macro places 支持层次建模与展开。 |
| 并发 / 同步 | 强支持 | 这是论文的核心优势。 |
| 时间约束 | 部分支持 | 通过 `GSPN` 的定时变迁和性能分析表达。 |
| 连续动态 / 随机性 | 支持随机、无连续 | `GSPN` 支持随机性能分析；连续动力学不在主体。 |
| 可执行 / 可验证性 | 强分析 | 支持 boundedness、liveness、deadlock 与成功概率分析。 |

### 形式化问题与性质

1. 相比很多把 `FSM` 用作机器人行为图的工作，这篇论文把 concurrency 当成一等公民。
2. 它强调“任务执行网”和“闭环环境网”的组合，这对真实多机器人协作尤其关键。
3. `MOPN` / `GSPN` 双视图让结构正确性和概率性能分析可以复用同一任务骨架。
4. macro place / predicate place 的引入，使多机器人任务规格化和复用成为可能。

## 构造方式与承载格式

### 建模入口

建模入口遵循明显的积木式流程：

1. 为 primitive action、subtask、environment condition 建立小规模 `PN` 模块。
2. 用 predicate places 表示传感器读数、通信消息或环境条件。
3. 用 macro places 折叠子网，形成更高层任务计划。
4. 对执行网展开后，再和 environment models 组合做分析。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `MOPN` 用于 qualitative analysis。
2. `GSPN` 用于 stochastic / performance analysis。
3. macro places 与 connection places。
4. predicate places 与 communication actions 的 analysis 版本。

### 交换与互操作

互操作主要体现在模型组合上：

1. task plan 展开后可与 environment layer 自动组合。
2. 通信动作在执行版与分析版之间可以替换。
3. 多机器人共享的 predicate places 在组合时合并为同一环境条件。

## 配套基础设施

- 建模/编辑工具：原文强调 PN-based framework，本身未绑定单一编辑器。
- 解析/交换/元模型支持：通过 macro place、predicate place 和 layer 组织模型，但无统一交换标准。
- 仿真/执行支持：任务网可直接服务执行层，尤其是多机器人同步任务。
- 验证/分析支持：boundedness、liveness、deadlocks、conservation，以及 Markov-chain based performance analysis。
- 代码生成/转换支持：原文重点不在代码生成，而在 plan execution 与 analysis。
- 标准化或社区生态：依托一般 Petri net / stochastic Petri net 生态，具体机器人框架耦合较弱。

## 适用场景与需求前提

### 适用场景

适合多机器人协作任务、机器人足球、显式/隐式通信协同、任务同步和资源约束明显的系统。

### 需求前提

1. 任务可以分解成离散动作、子任务与同步条件。
2. 机器人之间的通信或观察关系可以写成显式 predicate / transition。
3. 重点是并发、同步和成功概率，而不是复杂连续控制。
4. 团队愿意采用模块化子网而非单一大状态机。

### 不适用或高成本场景

如果系统核心困难在连续动力学、复杂优化规划或高维数据守卫，那么仅靠这类 Petri 网框架不足以覆盖，需要与 hybrid / optimization 模型结合。

## 与相邻形式主义的关系

相对传统 `FSM` 机器人任务图，它更擅长表达并发与同步；相对 [The Application of Petri Nets to Workflow Management](../application-of-petri-nets-to-workflow-management/desc.md) 的 `WF-net`，它不是单 case 工作流，而是多机器人协作与环境闭环；相对 [Coloured Petri Nets](../coloured-petri-nets/desc.md)，本文更偏任务框架和执行分析，而不是数据类型化本体。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提供了一个很有代表性的事实：一旦需求里“并发、同步、资源流和通信协作”成为主导，Petri 网往往比普通状态机更贴近问题结构。

### 作为目标形式主义还是中间表示

对多机器人协作、流程调度和资源约束任务，它可以直接作为目标形式主义；对一般控制系统，也很适合作为“并发子系统”的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应把动作、环境谓词、同步消息和资源条件分离。
2. 宏节点式组合比一次性生成一张巨网更适合 LLM 分步建模。
3. 若后续要做验证或性能分析，最好一开始就区分 qualitative net 与 stochastic extension。

## 重要的相关工作

- [The Application of Petri Nets to Workflow Management](../application-of-petri-nets-to-workflow-management/desc.md)：展示 `WF-net` 如何把流程正确性落到 Petri 网。
- [Coloured Petri Nets](../coloured-petri-nets/desc.md)：提供 typed token 与 richer data handling 的主线。
- [Time Petri Nets](../time-petri-nets/desc.md)：补出实时并发场景下的时间扩展。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值应用条目，重点在多机器人任务的并发、同步与分析，而不是 Petri 网本体教程。
- 其描述客体是并发过程与资源/消息流，因此记为 `🏭`；论文语境落在机器人/CPS 协作任务，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它很好地说明了 Petri 网为什么在“多主体协作 + 同步通信”场景下值得作为主干备选形式主义。

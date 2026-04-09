# UPPAAL Stratego：策略综合与统计评估 / Uppaal Stratego

## 基本信息

- 标题：Uppaal Stratego
- 中文标题：UPPAAL Stratego：策略综合与统计评估
- 作者：Alexandre David，Peter Gjøl Jensen，Kim Guldstrand Larsen，Marius Mikučionis，Jakob Haahr Taankvist
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 9035`，pp. 206-211，2015
- DOI：`10.1007/978-3-662-46681-0_16`
- 链接：https://doi.org/10.1007/978-3-662-46681-0_16
- 形式主义：`Stochastic Priced Timed Games / Timed Game Automata / Uppaal Stratego`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：strategy-synthesis and statistical-evaluation workbench on top of `UPPAAL` game and `SMC` lines
- 工具/实现获取方式：原文明确给出 `Uppaal Stratego` 可用入口，并说明其整合了 `Uppaal Tiga` 的符号策略综合、`UPPAAL SMC` 的统计模型检查以及基于学习的近优策略优化。
- 标准/格式获取方式：承载方式沿用 `UPPAAL` 模板/查询语言，并新增 `strategy ... = control: ...`、`under NS/SS` 等 query 语法；不是独立中立交换标准。

## 简报

这篇论文的核心贡献，是把 `UPPAAL` 生态里原本分散的三条线重新接起来：`Tiga` 负责**符号策略综合**，`SMC` 负责**统计评估**，再加上一条**学习近优策略**的路线。于是它处理的就不再只是“这个 timed game 是否可赢”，而是“先综合一个保证目标的策略，再在随机环境下评估它、优化它”。

- 形式主义定位：stochastic priced timed game 基础设施，而不是新的 timed-game 母模型。
- 构造方式简述：先把 `SPTG` 抽象成 `TGA` 做符号综合得到策略 `\sigma`，再把 `\sigma` 放回 stochastic/priced 模型里做 statistical model checking 与 learning-based optimization。
- 基础设施与场景简述：依托 `UPPAAL Tiga`、`UPPAAL SMC`、strategy query language、memoryless strategies 与 `SPTG/TGA` abstraction，服务实时调度、资源竞争与带不确定时长的控制优化。

```text
stochastic priced timed game -> abstraction to timed game -> symbolic strategy synthesis -> strategy-constrained statistical model checking -> optional near-optimal refinement
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. stochastic priced timed games (`SPTG`)；
2. timed games (`TGA`)；
3. non-deterministic / deterministic / stochastic strategies；
4. statistical model checking under strategies；
5. learning-based strategy optimization。

### 核心抽象

原文最关键的模型关系可以直接保守写成：

$$
\mathrm{Abs}(P) = G
$$

上式中的符号逐项解释如下：

1. `P` 是 `SPTG`。
2. `G` 是通过忽略 prices 与 stochasticity 得到的 timed game。
3. 这个抽象不会改变可能行为，只是忘掉代价与概率信息。
4. 论文的综合步骤正是先在 `G` 上求策略。

得到策略后，系统会构造：

$$
G \mid \sigma
$$

以及

$$
P \mid \sigma
$$

上式中的符号逐项解释如下：

1. `\sigma` 是在 timed-game 上综合出来的策略。
2. `G \mid \sigma` 用于符号模型检查。
3. `P \mid \sigma` 用于统计模型检查与代价评估。
4. 这正是本文把 game solving 和 `SMC` 接起来的关键。

论文还把策略限定为 memoryless，并给出三类：

$$
\sigma : State \to 2^{Act \cup Delay}
$$

上式中的符号逐项解释如下：

1. 对 non-deterministic strategy，返回的是一组允许动作。
2. 对 deterministic strategy，可把返回集收缩成单个动作。
3. 对 stochastic strategy，则把动作集合再赋上概率分布。
4. `State` 是当前符号状态，`Act \cup Delay` 表示控制动作或时间推进。

### 一个最小例子与通俗解释

论文的 newspaper jobshop 例子很适合解释：

1. 多个人要共享报纸不同版面。
2. 谁下一步读什么版、等多久，并不全由控制器决定，因为阅读时长由随机环境决定。
3. `Uppaal Stratego` 先综合一个“保证一小时内看完”的策略。
4. 再在随机时长下统计评估哪个人平均等待时间更小，并进一步学出更优策略。

通俗地说，它不像传统模型检查那样只回答“能不能”；它更像先找一个保底可行策略，再问“这个保底策略在真实随机环境里表现到底好不好”。

### 运行 / 接受 / 转移语义

论文引入的策略查询语法可直接保守写成：

$$
\texttt{strategy NS = control: A<> prop}
$$

上式中的符号逐项解释如下：

1. `NS` 是策略标识符。
2. `control:` 表示调用 `Tiga` 风格的控制综合。
3. `A<> prop` 表示必须在所有环境行为下最终到达 `prop`。
4. 这是保证性策略的直接语法入口。

策略求出后，统计评估可写成：

$$
\Pr[bound](<> prop)\ \texttt{under}\ SS
$$

以及

$$
E[bound;int](min: expr)\ \texttt{under}\ SS
$$

上式中的符号逐项解释如下：

1. `SS` 是 stochastic strategy。
2. 第一类查询估计某个目标在给定边界内满足的概率。
3. 第二类查询估计代价 / 时间类表达式的期望。
4. 这正是 `UPPAAL SMC` 路线在策略约束下的延伸。

若学习过程在 permissive strategy 内优化得到更优策略，则论文记为：

$$
\sigma^\circ
$$

并进一步分析：

$$
P \mid \sigma^\circ
$$

这里的含义是：先保留原先 guarantee，再在随机代价意义下把策略继续推向 near-optimal。

### 语义边界

1. 论文只处理 memoryless strategies。
2. 主线是 perfect-information timed/stochastic-priced game，不是部分可观测博弈。
3. 代价与概率主要通过 `SMC` 和 learning 优化处理，而不是一次性完整符号求精。
4. 这是工具框架论文，不是 `SPTG` 的最原始理论定义论文。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型抽象 | `$\mathrm{Abs}(P) = G$` | 先忘掉 stochasticity / price，在 `TGA` 上做综合。 |
| 策略约束模型 | `$G \mid \sigma,\ P \mid \sigma$` | 同一策略可分别用于符号验证和统计评估。 |
| 策略接口 | `$\sigma : State \to 2^{Act \cup Delay}$` | 统一概括 nondeterministic / deterministic / stochastic strategies。 |
| 保证查询 | `$\texttt{strategy NS = control: A<> prop}$` | `Tiga` 风格 synthesis 入口。 |
| 统计评估 | `$\Pr[bound](<> prop)\ \texttt{under}\ SS$` | 在策略约束下评估随机环境表现。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 仍以 `UPPAAL` timed-game / priced-game 骨架为核心。 |
| 事件 / 触发 | 很强 | controllable actions、environment choices 与 delays 都是一等对象。 |
| 守卫 / 数据 | 中等支持 | 继承 `UPPAAL` 风格 guards、variables 与 templates。 |
| 层次 | 不支持 | 不是层次状态机平台。 |
| 并发 / 同步 | 很强 | 多 template 组合与资源竞争是主场景。 |
| 时间约束 | 很强 | 这是 timed-game 工具线。 |
| 连续动态 / 随机性 | 条件支持 | 支持 stochasticity 与 prices，但不处理连续动力学。 |
| 可执行 / 可验证性 | 很强 | synthesis、SMC、learning-based optimization 已被统一进同一工具链。 |

### 形式化问题与性质

1. 这篇论文最重要的不是某个单独算法，而是把 synthesis、evaluation 和 optimization 接成闭环。
2. 它把 `UPPAAL` 从“证明存在策略”推进到“评估策略实际表现”。
3. 这非常适合那些目标既有 hard guarantee，又有 soft cost metric 的实时控制问题。

## 构造方式与承载格式

### 建模入口

原文给出的主要入口有：

1. `SPTG`/timed-game templates；
2. strategy synthesis queries；
3. `under NS/SS` 风格的 strategy-aware evaluation queries；
4. learning-based near-optimal strategy refinement。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UPPAAL` templates 与 declarations；
2. strategy objects；
3. `G \mid \sigma`、`P \mid \sigma` 这类受策略约束模型；
4. statistical evaluation / simulation traces。

### 交换与互操作

互操作重点非常明确：

1. `UPPAAL Tiga` 负责符号策略综合。
2. `UPPAAL SMC` 负责统计评估。
3. learning optimization 再在 permissive strategy 里做细化。

## 配套基础设施

- 建模/编辑工具：沿用 `UPPAAL` 图形/模板化建模入口。
- 解析/交换/元模型支持：strategy declarations、`under NS/SS` 查询语法与策略对象。
- 仿真/执行支持：支持在策略约束下做统计仿真与 performance observation。
- 验证/分析支持：symbolic synthesis、symbolic model checking、statistical model checking、learning-based optimization。
- 代码生成/转换支持：论文不主打代码生成；重点是策略生成与评估。
- 标准化或社区生态：这是 `UPPAAL 4.0 -> Tiga -> SMC` 三线汇合后的平台型条目。

## 适用场景与需求前提

### 适用场景

适合带 hard timing guarantees 和 soft expected-cost objective 的实时控制、资源调度和竞争式嵌入式系统。

### 需求前提

1. 系统要能压成 `SPTG/TGA` 风格模型。
2. 环境不确定性主要体现为 stochastic delays 或 environment choices。
3. 目标至少包含一部分可以先做 guarantee synthesis。
4. 之后才值得在该安全壳内继续做期望代价优化。

### 不适用或高成本场景

如果系统核心是部分可观测、连续动力学、富数据博弈或非 memoryless 策略，本文这套工具线就不够直接。

## 与相邻形式主义的关系

相对 [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)，本文不是单纯回答“能否综合 winning strategy”，而是继续把该策略拿去做统计评估与优化；相对 [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)，`UPPAAL-SMC` 更偏无控制器的概率/期望分析，而本文强调 strategy-aware analysis；相对 [uppaal-40/desc.md](../uppaal-40/desc.md)，`UPPAAL 4.0` 是底层 timed-automata 平台升级，而本文是更上层的 game + `SMC` 融合工作台。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机目标语言的价值不只在“能验证”，还在“能不能对生成出来的策略继续做统计评估和优化”。
2. 对控制系统需求建模来说，很多需求天然包含 hard constraints 与 soft objectives 两层，这篇论文提供了很直接的工具链例证。
3. 若未来 `project_1` 需要把模型生成和策略评估接成闭环，`Uppaal Stratego` 这类条目比单纯 model checker 更贴近终局工具形态。

### 局限

1. 论文站在 timed game / `SMC` 平台层，不直接解决如何从非形式化需求生成这些模型。
2. 其策略假设和模型假设都比一般工业控制软件更理想化。

## 重要的相关工作

1. [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)：timed-game synthesis 的直接前置平台。
2. [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)：priced timed automata 统计验证路线。
3. [uppaal-40/desc.md](../uppaal-40/desc.md)：`UPPAAL` 主平台升级锚点。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇典型的 `🏗️` 条目，适合作为 `UPPAAL` 生态从“timed-game 可赢性”继续扩展到“策略约束下的统计评估与近优优化”的关键基础设施锚点。

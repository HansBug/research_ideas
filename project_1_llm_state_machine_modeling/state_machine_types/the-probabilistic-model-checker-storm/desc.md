# Storm 概率模型检查器 / The Probabilistic Model Checker Storm

## 基本信息

- 标题：The probabilistic model checker Storm
- 中文标题：Storm 概率模型检查器
- 作者：Christian Hensel，Sebastian Junges，Joost-Pieter Katoen，Tim Quatmann，Matthias Volk
- 发表：*International Journal on Software Tools for Technology Transfer*，24(4):589-610，2022
- DOI：`10.1007/s10009-021-00633-z`
- 链接：https://doi.org/10.1007/s10009-021-00633-z
- 形式主义：`probabilistic model checking / DTMC / CTMC / MDP / MA / POMDP / Storm`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：full journal tool paper for modular probabilistic model checking, extending the earlier `Storm` abstract with richer engines, solvers, APIs and advanced analysis routes
- 工具/实现获取方式：原文明确给出 `Storm` 作为开源 probabilistic model checker，并强调 command-line、C++ interface 与 Python API。
- 标准/格式获取方式：核心承载是 `Prism/JANI`、explicit formats、`GSPN`、`DFT`、`pGCL` 前端，以及 sparse / `dd` / hybrid / abstraction-refinement engines 和 solver interfaces；它不是单一建模语言标准。

## 简报

如果说 2017 年那篇 [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md) 是 `Storm` 的平台宣言，那么这篇 2022 journal paper 才是完整的工具说明书。它不再只是说“我们有一个现代概率模型检查器”，而是系统展开：支持哪些模型、哪些输入语言、哪些 property、哪些 engines、哪些 solvers、哪些高级功能，以及这些模块是怎样拼到一起的。

- 形式主义定位：概率模型检查平台与工具基础设施，不是新的单体状态机语言。
- 构造方式简述：从 `Prism/JANI/GSPN/DFT/pGCL` 等输入构建 Markov models，再根据任务选择 sparse / `dd` / hybrid / abstraction-refinement engine 与合适 solver，最后通过 CLI 或 Python API 返回概率、奖励、反例、策略或参数分析结果。
- 基础设施与场景简述：依托多输入语言、可插拔 engines / solvers、exact rational arithmetic、high-level counterexamples、parameter synthesis、POMDP analysis 与 automatic engine selection，服务 quantitative verification research 与工程 workflow。

```text
Prism / JANI / GSPN / DFT / pGCL -> model builder -> chosen engine + chosen solver -> probabilities / rewards / strategies / counterexamples / parameter results
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 支持的概率模型族；
2. 输入语言与格式；
3. properties 与 advanced analyses；
4. model-checking engines；
5. solver architecture 与 user-facing APIs。

### 核心抽象

为压缩论文架构，可把 `Storm` 保守写成：

$$
\mathrm{Storm} = (\mathcal M, \mathcal L, \mathcal P, \mathcal E, \mathcal S, \mathcal I)
$$

上式中的符号逐项解释如下：

1. `\mathcal M` 是支持的模型族。
2. `\mathcal L` 是输入语言与格式集合。
3. `\mathcal P` 是支持的性质与高级分析任务。
4. `\mathcal E` 是 model-checking engines。
5. `\mathcal S` 是可插拔 solver interfaces / implementations。
6. `\mathcal I` 是 command-line、C++ 与 Python 等接口层。

论文明确覆盖的模型家族可写成：

$$
\mathcal M = \{\mathrm{DTMC}, \mathrm{CTMC}, \mathrm{MDP}, \mathrm{MA}, \mathrm{POMDP}\}
$$

上式中的符号逐项解释如下：

1. `DTMC` 是离散时间马尔可夫链。
2. `CTMC` 是连续时间马尔可夫链。
3. `MDP` 是马尔可夫决策过程。
4. `MA` 是 Markov automata。
5. `POMDP` 是部分可观测 `MDP`，是本文相对早期工具说明的重要扩展点。

输入层可压成：

$$
\mathcal L = \{\mathrm{Prism}, \mathrm{JANI}, \mathrm{Explicit}, \mathrm{GSPN}, \mathrm{DFT}, \mathrm{pGCL}\}
$$

上式中的符号逐项解释如下：

1. `Prism` 与 `JANI` 是最核心的通用输入。
2. `Explicit` 指显式状态转移格式。
3. `GSPN`、`DFT`、`pGCL` 则反映 `Storm` 对特定建模 formalism 的前端吸纳。

论文给出的主要 engine family 可写成：

$$
\mathcal E = \{\mathrm{sparse}, \mathrm{dd}, \mathrm{hybrid}, \mathrm{dd\mbox{-}to\mbox{-}sparse}, \mathrm{exploration}, \mathrm{abstraction\mbox{-}refinement}, \mathrm{automatic}\}
$$

上式中的符号逐项解释如下：

1. `sparse` 走稀疏矩阵路线。
2. `dd` 走 decision-diagram 路线。
3. `hybrid` 混合 MTBDD 和 sparse representation。
4. `dd-to-sparse` 适合先做符号构造或最小化，再转 sparse analysis。
5. `automatic` 由决策树自动挑选较合适的配置。

### 一个最小例子与通俗解释

一个最小直觉例子是：

1. 用户给出一个 `Prism` 模型和一条 reachability property。
2. `Storm` 先把输入模型翻成内部 Markov representation。
3. 再根据模型结构与任务，选择 sparse / hybrid 等 engine 和对应 solver。
4. 最后返回的是概率、奖励、最小反例、策略甚至参数区域，而不只是一个 yes / no。

通俗地说，`Storm` 更像“概率验证操作系统”而不是“单一求解器”。你给它的是模型和任务，它再决定该走哪条内部路线。

### 运行 / 接受 / 转移语义

在性质层，论文 repeatedly 围绕 reachability / reward 这类 quantitative queries。最基础的 reachability 语义可保守写成：

$$
\Pr^\sigma_s(\Diamond B)
$$

上式中的符号逐项解释如下：

1. `s` 是初始状态。
2. `\sigma` 是在含 nondeterminism 模型上的策略或 scheduler。
3. `B` 是目标坏状态或好状态集合。
4. `\Diamond B` 表示最终到达 `B`。
5. `Storm` 的很多 engine / solver 最终都在求这一类数量。

对工具架构而言，关键不是重定义模型语义，而是把不同数值子问题抽象到 solver 层，包括线性方程、Bellman equations、MILP、SMT 等等。这使得 advanced features 如 high-level counterexamples、parameter synthesis、POMDP analysis 都能在统一平台内落地。

### 语义边界

1. `Storm` 是平台，不是一个统一 DSL。
2. 虽然覆盖的概率模型非常广，但并不等于“所有 quantitative formal methods 都支持”。
3. 论文明确指出某些方向如 statistical model checking、probabilistic timed automata、stochastic games 仍不在其核心覆盖范围内。
4. 平台强项是模块化和 breadth，不是某单一路线的一统天下。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 平台骨架 | `$\mathrm{Storm} = (\mathcal M, \mathcal L, \mathcal P, \mathcal E, \mathcal S, \mathcal I)$` | 概括其“模型-语言-性质-引擎-求解器-接口”六层结构。 |
| 模型族 | `$\mathcal M = \{\mathrm{DTMC}, \mathrm{CTMC}, \mathrm{MDP}, \mathrm{MA}, \mathrm{POMDP}\}$` | 相比早期摘要版，模型覆盖进一步展开。 |
| 输入族 | `$\mathcal L = \{\mathrm{Prism}, \mathrm{JANI}, \mathrm{Explicit}, \mathrm{GSPN}, \mathrm{DFT}, \mathrm{pGCL}\}$` | 说明它不是单前端工具。 |
| 引擎族 | `$\mathcal E = \{\mathrm{sparse}, \mathrm{dd}, \mathrm{hybrid}, \mathrm{dd\mbox{-}to\mbox{-}sparse}, \mathrm{exploration}, \mathrm{abstraction\mbox{-}refinement}, \mathrm{automatic}\}$` | 平台内部路线可按任务切换。 |
| reachability quantity | `$\Pr^\sigma_s(\Diamond B)$` | 概率性质求解的典型对象。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 覆盖 `DTMC/CTMC/MDP/MA/POMDP` 等多种概率状态模型。 |
| 事件 / 触发 | 中等支持 | 由具体前端语言决定，如 `Prism/JANI/pGCL`。 |
| 守卫 / 数据 | 很强 | `Prism`、`JANI`、`pGCL` 等前端保留变量、更新和结构信息。 |
| 层次 | 弱支持 | 平台主体不是层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 可由 `Prism/JANI` 自动机网络或 `GSPN/DFT` 前端提供。 |
| 时间约束 | 中等支持 | 支持 `CTMC/MA` 一类定量时间模型，但不主打 `PTA`。 |
| 连续动态 / 随机性 | 很强 | 核心就是概率 / 随机模型检查。 |
| 可执行 / 可验证性 | 很强 | engines、solvers、API、counterexamples、parameter synthesis 都已工程化。 |

## 构造方式与承载格式

### 建模入口

原文给出的建模入口包括：

1. `Prism`；
2. `JANI`；
3. explicit transition formats；
4. `GSPN`、`DFT`、`pGCL`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. sparse matrices；
2. decision diagrams / MTBDDs；
3. solver-level equation / optimization problems；
4. API-level model objects and results。

### 交换与互操作

本文的互操作重点非常强：

1. `JANI` 作为跨工具建模语言被直接支持。
2. 同一模型可切换 engines 与 solvers。
3. CLI、C++ 与 Python API 把平台暴露给外部 workflow。

## 配套基础设施

- 建模/编辑工具：原文重点在 parser / builder，而不是图形建模器。
- 解析/交换/元模型支持：`Prism`、`JANI`、`GSPN`、`DFT`、`pGCL`、explicit formats。
- 仿真/执行支持：不主打 statistical simulation；主体是数值和符号化分析。
- 验证/分析支持：reachability、rewards、conditional properties、exact arithmetic、high-level counterexamples、parameter synthesis、POMDP analysis。
- 代码生成/转换支持：重点在 model translation 与 internal representation，不在 deployment code generation。
- 标准化或社区生态：与 `JANI`、`Prism`、`PROPhESY` 等 quantitative ecosystem 深度连接。

## 适用场景与需求前提

### 适用场景

适合概率模型检查、奖励分析、策略与 scheduler 合成、参数分析、POMDP 近似分析，以及需要在不同内部求解路线之间灵活切换的 quantitative verification workflow。

### 需求前提

1. 模型需能落成 `DTMC/CTMC/MDP/MA/POMDP` 或它们的主流前端表述。
2. 用户关心的是概率、奖励、策略或参数结果，而不只是布尔可达性。
3. 工作流允许把平台作为 back end，而非单一专用工具。

### 不适用或高成本场景

若目标是 probabilistic timed automata、statistical model checking 或 stochastic games，本文指出这些方向仍不属于其完整主线。

## 与相邻形式主义的关系

相对 [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)，本文是更完整的 journal tool paper，覆盖了 `POMDP`、high-level counterexamples、parameter synthesis、automatic engine 与 solver architecture；相对 [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)，`JANI` 是交换层，而本文展示 `Storm` 如何消费 `JANI` 并完成真正分析；相对 [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)，`Momba` 更像 Python workflow bridge，而 `Storm` 是底层求解平台。

## 与本研究的关系

### 对 Project 1 的价值

它说明一旦状态机谱系扩展到概率或随机方向，真正可用的不只是语言定义，而是成套的输入、求解器、API、反例与参数分析基础设施。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`Storm` 不是目标形式主义，而是概率扩展状态机及其性质验证的成熟后端。

### 对需求到模型生成的启发

1. 若后续要支持概率状态机或概率需求，应优先考虑能直接落到 `JANI/Prism` 的中间表示。
2. “模型语言”与“求解路线”最好解耦，这正是 `Storm` 模块化架构最值得借鉴的地方。
3. high-level counterexamples 和 parameter synthesis 非常适合接入“生成-验证-修复”闭环。

### 现实限制

本文覆盖面很广，但也意味着它更像平台总装论文，不会替代每条子路线上的专门理论论文。

## 重要的相关工作

### 奠基或前身工作

1. [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)：`Storm` 的早期平台摘要。
2. `PRISM` 主线：本文多次以 `Prism` 为重要对照。

### 同类型或同家族工作

1. [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)：`JANI` + Python workflow。
2. [epmc-gets-knowledge-in-multi-agent-systems/desc.md](../epmc-gets-knowledge-in-multi-agent-systems/desc.md)：同样强调 plugin / architecture 的 quantitative platform。

### 标准 / 格式 / 工具链工作

1. [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)：本文最关键的交换层伙伴。

### 与本研究关系最紧的工作

1. 概率模型检查、策略综合与参数分析统一平台路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`probabilistic model checking / DTMC / CTMC / MDP / MA / POMDP / Storm`
- 论文角色：full journal tool paper for modular probabilistic model checking, extending the earlier `Storm` abstract with richer engines, solvers, APIs and advanced analysis routes
- 核心功能：把多类 Markov models、多种输入语言、engines、solvers 与 advanced quantitative analyses 统一进同一平台
- 关键特性：`Prism/JANI`、multiple engines、solver abstraction、Python API、high-level counterexamples、parameter synthesis、POMDP support
- 构造方式：front-end model -> internal Markov representation -> engine + solver selection -> quantitative verification result
- 基础设施：`Storm` CLI / C++ / Python API、sparse / `dd` / hybrid engines、solver interfaces、`JANI` ecosystem
- 适用场景：概率验证、奖励分析、策略合成、参数分析、POMDP 近似分析
- 需求前提：模型需能落到主流 Markov formalism 和 `Prism/JANI` 一类输入，且关注 quantity-bearing verification
- 状态：🟢 直接可用

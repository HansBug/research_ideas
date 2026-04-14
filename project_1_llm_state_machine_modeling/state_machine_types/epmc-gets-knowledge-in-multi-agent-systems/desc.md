# EPMC 在多智能体系统中支持知识推理 / EPMC Gets Knowledge in Multi-agent Systems

## 基本信息

- 标题：EPMC Gets Knowledge in Multi-agent Systems
- 中文标题：EPMC 在多智能体系统中支持知识推理
- 作者：Chen Fu，Ernst Moritz Hahn，Yong Li，Sven Schewe，Meng Sun，Andrea Turrini，Lijun Zhang
- 发表：*Verification, Model Checking, and Abstract Interpretation*，`LNCS 13182`，pp. 93-107，2022
- DOI：`10.1007/978-3-030-94583-1_5`
- 链接：https://doi.org/10.1007/978-3-030-94583-1_5
- 形式主义：`EPMC / plugin-based probabilistic model checking / PETL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：extendible probabilistic model checker with minimal kernel and plugin architecture
- 工具/实现获取方式：原文明确说明 `ePMC` 以 Git 仓库形式提供以便 fork 和修改；当前公开实现入口为 `https://github.com/ISCAS-PMC/ePMC`。
- 标准/格式获取方式：主承载是 minimal kernel、plugins、`PRISM` / `JANI` parsers、property solvers 与命令行装配；它不是中立交换标准，而是 plugin-based quantitative model-checking platform。

## 简报

这篇论文补的是概率模型检查里的平台架构线。`EPMC` 的关键设计不是“再做一个只支持某一逻辑的 model checker”，而是把 model checking 平台压成一个极小 kernel，再把算法、automata、`BDD`、graph solver、`JANI`、`PRISM` format、property solver 等功能都拆成可装配 plugins。论文用 `EPMC-petl` 作为案例，展示这套平台如何较低成本扩到多智能体系统中的知识推理。

- 形式主义定位：概率模型检查平台基础设施，而不是新的概率状态机族。
- 构造方式简述：kernel 只负责 bootstrap、plugin loading 与启动 model-checking procedure；具体模型、逻辑、求解器和格式支持由 plugins 注册并组合。
- 基础设施与场景简述：依托 Java、`JNA`、Maven、`BDD` wrappers、`PRISM/JANI` parsers 与 property-solver plugins，服务 `MC/MDP/Markov games`、`PCTL/PLTL/PCTL*` 以及 `PETL` 这类扩展逻辑。

```text
model + property -> minimal kernel -> selected plugins -> parser / graph / automata / solver pipeline -> quantitative verification result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `EPMC` minimal kernel。
2. native plugin groups 与 plugin manager。
3. probabilistic model families，例如 `Markov chains`、`MDP`、`Markov games`。
4. logics，例如 `PCTL`、`PLTL`、`PCTL*` 与扩展的 `PETL`。
5. `PRISM` / `JANI` 输入、`BDD` / graph encodings 与 property solvers。

### 核心抽象

根据论文架构图，可把 `EPMC` 保守整理为：

$$
EPMC = (K, \Pi, \mathcal{M}, \mathcal{L})
$$

上式中的符号逐项解释如下：

1. `$K$` 是 minimal kernel，负责 bootstrap、plugin loading 与启动检查流程。
2. `$\Pi$` 是已装载并注册的 plugins 集合。
3. `$\mathcal{M}$` 是可处理的模型家族。
4. `$\mathcal{L}$` 是可处理的逻辑家族。
5. 这是依据论文架构描述做的保守平台抽象，而不是原文直接给出的单一数学元组。

论文在引言中明确给出基线支持范围，可写成：

$$
\mathcal{M} = \{MC, MDP, MarkovGames\}, \qquad \mathcal{L} = \{PCTL, PLTL, PCTL^*\}
$$

上式中的符号逐项解释如下：

1. `$MC$` 是 Markov chains。
2. `$MDP$` 是 Markov decision processes。
3. `$MarkovGames$` 是随机博弈模型。
4. `$PCTL$`、`$PLTL$`、`$PCTL^*$` 是论文明确列出的基线逻辑能力。

native plugin groups 可保守列为：

$$
\Pi_{native} = \{algorithm, automata, command, dd, bisimulation, expression, graph, graphsolver, jani, prism, propertysolver, util, value\}
$$

上式中的符号逐项解释如下：

1. 每个元素都是论文明确介绍的 plugin group。
2. `algorithm` 负责经典概率模型检查算法。
3. `automata` 负责 `\omega`-automata 表示与确定化。
4. `dd`、`graph`、`graphsolver`、`propertysolver` 负责符号表示、图求解和性质求解。
5. `jani` 与 `prism` groups 负责输入输出与互操作。

### 一个最小例子与通俗解释

一个最小 `EPMC` 例子可以是：

1. 用户给出一个 `PRISM` 风格 `MDP` 模型和一个 `PCTL` 公式。
2. kernel 根据命令行或嵌入式配置装入 `prism-format`、`graphsolver-iterative`、`propertysolver-pctl` 等 plugins。
3. parser 把模型转成 graph 或 `MTBDD`，property solver 再调用相应 graph solver 求概率结果。
4. 若换成 `PCTL^*` 或 `PETL`，只需再装入相应 automata / property-solver / extension plugins。

通俗地说，`EPMC` 像“把概率模型检查器拆成了乐高积木”。kernel 不预先假定你一定要做哪类模型和哪类逻辑，功能都靠 plugins 在启动时自己注册进来。

### 运行 / 接受 / 转移语义

plugin 装配流程可保守写成：

$$
Load(K, \Pi_{emb}, \Pi_{cli}) \to \Pi
$$

上式中的符号逐项解释如下：

1. `$K$` 是 kernel。
2. `$\Pi_{emb}$` 是 `embeddedplugins.txt` 中列出的内嵌 plugins。
3. `$\Pi_{cli}$` 是命令行 `plugin` 选项指定的 plugins。
4. `$\Pi$` 是最终按顺序装载并可彼此覆盖注册结果的 plugin 集合。

论文在 `PETL` 扩展中明确使用知识算子，可写成：

$$
K_i \varphi,\qquad E_G \varphi,\qquad C_G \varphi,\qquad D_G \varphi
$$

上式中的符号逐项解释如下：

1. `$K_i \varphi$` 表示 agent `$i$` 知道 `$\varphi$`。
2. `$E_G \varphi$` 表示群组 `$G$` 中每个 agent 都知道 `$\varphi$`。
3. `$C_G \varphi$` 表示群组 `$G$` 的 common knowledge。
4. `$D_G \varphi$` 表示 distributed knowledge。

对应的不可区分关系写成：

$$
\sim_i \subseteq S \times S
$$

上式中的符号逐项解释如下：

1. `$S$` 是全局状态集合。
2. `$\sim_i$` 是 agent `$i$` 的 equivalence relation。
3. 若两个状态在 `$\sim_i$` 下相关，则对 agent `$i$` 不可区分。
4. `EPMC-petl` 就是在现有平台上新增模型、关系和求解器 plugins 来支持这部分语义。

### 语义边界

1. `EPMC` 是平台架构论文，不重新定义 `MC/MDP/Markov games` 的母理论。
2. kernel 本身极小，真正能力取决于装载的 plugins。
3. `PETL` 这类多智能体知识逻辑扩展只是平台可扩展性的案例之一，不等于平台只服务多智能体场景。
4. 连续动力学与一般 hybrid systems 不在本文主线中。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 平台骨架 | `$EPMC=(K,\Pi,\mathcal{M},\mathcal{L})$` | minimal kernel 与 plugin ecosystem 的保守抽象。 |
| 基线模型族 | `$\mathcal{M}=\{MC,MDP,MarkovGames\}$` | 论文显式列出的主要模型对象。 |
| 基线逻辑族 | `$\mathcal{L}=\{PCTL,PLTL,PCTL^*\}$` | 论文引言明确强调的逻辑支持面。 |
| native plugin groups | `$\Pi_{native}=\{\cdots\}$` | 平台的主要功能切片。 |
| 知识算子 | `$K_i\varphi,E_G\varphi,C_G\varphi,D_G\varphi$` | `EPMC-petl` 对多智能体知识推理的扩展入口。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 平台覆盖 `MC/MDP/Markov games` 等多类概率状态模型。 |
| 事件 / 触发 | 中等支持 | 由具体输入模型语言决定。 |
| 守卫 / 数据 | 条件支持 | 通过 `PRISM/JANI` 等格式与 solver plugins 提供。 |
| 层次 | 弱支持 | 平台主轴不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 可通过 `PRISM`-style modules 与多智能体扩展建模。 |
| 时间约束 | 条件支持 | 可通过 quantitative models 与逻辑扩展间接进入，但本文主线不是 timed automata。 |
| 连续动态 / 随机性 | 支持随机性，不支持连续动态 | 概率模型检查是平台核心。 |
| 可执行 / 可验证性 | 很强 | kernel、plugins、`BDD`、property solvers 与输入格式都已平台化。 |

### 形式化问题与性质

1. `EPMC` 的价值在于“最小内核 + 插件组装”，而不是某个单独求解算法。
2. `PRISM` 与 `JANI` parser 同时存在，说明它同时重视现有事实标准与新互操作格式。
3. `EPMC-petl` 证明新逻辑和新模型扩展可以复用既有平台，而不必重写整个 model checker。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `PRISM` 模型与性质。
2. `JANI` 模型和公式。
3. 插件式命令行装配。
4. 扩展插件，例如 `PETL` 相关模型、关系和求解器。

### 机器可处理承载方式

机器可处理承载方式包括：

1. Java kernel 与 plugin manager。
2. `MANIFEST.MF` 依赖声明。
3. `embeddedplugins.txt` 和命令行 `plugin` 选项。
4. graph / `MTBDD` encodings。
5. `BDD` libraries、iterative graph solvers、property solvers。

### 交换与互操作

互操作是本文核心之一：

1. `prism-format` plugin 解析 `PRISM` 输入。
2. `jani-model` 与 `jani-exporter` 处理 `JANI` model / property interchange。
3. property solvers 与 automata plugins 可重组，形成不同逻辑能力的 `EPMC` flavour。

## 配套基础设施

- 建模/编辑工具：主入口是 `PRISM/JANI` 文本模型与命令行装配，而不是图形建模器。
- 解析/交换/元模型支持：`PRISM` parser、`JANI` parser/exporter、JSON utilities、value/type interfaces。
- 仿真/执行支持：论文重点在 model checking，不以 runtime execution 为核心。
- 验证/分析支持：`PCTL`、`PLTL`、`PCTL^*`、概率 reachability、reward、bisimulation lumping、`BDD` symbolic solving、`PETL` 知识推理扩展。
- 代码生成/转换支持：主要是模型与性质的解析、导出与 graph/`MTBDD` 转换，不主打部署代码生成。
- 标准化或社区生态：依托 Git 仓库、Maven、`JNA`、`CUDD/BuDDy/Sylvan`、`PRISM/JANI` quantitative verification 生态。

## 适用场景与需求前提

### 适用场景

适合概率模型检查平台研究、多输入格式 quantitative verification、教学型 / 研究型 solver experimentation，以及需要较低成本扩展新逻辑或新模型族的场景。

### 需求前提

1. 模型需能落成 `PRISM`、`JANI` 或平台支持的 graph/`MTBDD` 结构。
2. 团队接受 plugin-based architecture，而不是只接受单体工具。
3. 目标逻辑最好能映射到现有 property-solver / automata / graphsolver pipeline。
4. 若扩展新逻辑，需要同步提供 parser、data structure 与 solver plugins。

### 不适用或高成本场景

如果目标只是做单一固定工作流，`EPMC` 的平台化设计可能偏重；如果系统依赖连续动力学或非概率大规模数值仿真，也不在本文主战场。

## 与相邻形式主义的关系

相对 [pat-3-an-extensible-architecture-for-building-multi-domain-model-checkers/desc.md](../pat-3-an-extensible-architecture-for-building-multi-domain-model-checkers/desc.md)，两者都强调 plugin architecture，但 `PAT 3` 面向多语义域 DSL 平台，`EPMC` 更聚焦 quantitative / probabilistic model checking；相对 [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)，`JANI` 是 interchange format，而 `EPMC` 是消费该格式的平台；相对 [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)，`Storm` 强在现代多引擎 solver platform，`EPMC` 的特色则是更细粒度的 plugin 自注册架构。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“生成多类状态机后统一送入验证平台”的关键不只是模型格式，还要有可扩展的 solver architecture。
2. 若 `project_1` 后续要支持不同性质语言、不同验证后端或不同抽象层，`minimal kernel + plugins` 的组织方式很值得借鉴。
3. `EPMC-petl` 这类扩展示例也说明，平台设计得好时，新性质族可以增量接入，而不必推倒重来。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`EPMC` 更像验证平台和后端基础设施，而不是最终目标状态机语言。

### 对需求到模型生成的启发

1. 工具平台应把 parser、interchange、solver、logic support 明确解耦。
2. 如果模型要长期扩展，先定义 plugin boundaries 比先堆单体功能更重要。
3. 知识、概率和时序这类性质族最好从架构层就预留扩展点。

## 重要的相关工作

1. [pat-3-an-extensible-architecture-for-building-multi-domain-model-checkers/desc.md](../pat-3-an-extensible-architecture-for-building-multi-domain-model-checkers/desc.md)：多领域 model-checking platform architecture。
2. [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)：quantitative model interchange layer。
3. [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)：现代概率模型检查平台对照项。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`EPMC / plugin-based probabilistic model checking / PETL`
- 论文角色：extendible probabilistic model checker with minimal kernel and plugin architecture
- 核心功能：把概率模型检查器拆成 minimal kernel 与可组合 plugins，并可增量扩展到 `PETL` 等新逻辑
- 关键特性：plugin manager、`PRISM/JANI` parsers、`BDD` wrappers、graphsolver、property solvers、`PETL` extension
- 构造方式：model + property -> kernel -> selected plugins -> parser / graph / solver pipeline
- 基础设施：`ePMC` Git repo、Java、Maven、`JNA`、`BDD` libraries、`PRISM/JANI`
- 适用场景：quantitative verification platform、逻辑扩展实验与多输入格式 model checking
- 需求前提：模型与性质需能落到平台支持的 parser / solver boundary 上
- 状态：🟢

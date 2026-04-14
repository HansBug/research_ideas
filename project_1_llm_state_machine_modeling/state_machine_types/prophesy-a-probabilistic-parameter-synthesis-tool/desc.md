# PROPhESY：概率参数综合工具 / PROPhESY: A PRObabilistic ParamEter SYnthesis Tool

## 基本信息

- 标题：PROPhESY: A PRObabilistic ParamEter SYnthesis Tool
- 中文标题：PROPhESY：概率参数综合工具
- 作者：Christian Dehnert，Sebastian Junges，Nils Jansen，Florian Corzilius，Matthias Volk，Harold Bruintjes，Joost-Pieter Katoen，Erika Abraham
- 发表：*Computer Aided Verification*，pp. 214-231，2015
- DOI：`10.1007/978-3-319-21690-4_13`
- 链接：https://doi.org/10.1007/978-3-319-21690-4_13
- 形式主义：`parametric Markov chains / rational functions / PROPhESY`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：parametric-probabilistic model checking and parameter-synthesis workbench
- 工具/实现获取方式：原文明确说明工具包含 web front-end、可视化与用户引导式 synthesis；当前提取文本未保留稳定公开仓库链接。
- 标准/格式获取方式：输入是 `PRISM` 风格的 `pMC` 模型与性质约束，核心机读对象是 rational functions、sample points、safe/unsafe regions 与 `SMT` checks；它不是交换标准。

## 简报

`PROPhESY` 补的是概率模型检查里一条很实用的“参数不确定但仍要做定量验证”路线。它不要求所有概率在建模阶段就完全定死，而是允许把转移概率写成参数上的有理函数，然后围绕 reachability probability、conditional probability 和 expected reward 计算 rational function，并进一步把参数空间分成 safe / unsafe regions。

- 形式主义定位：面向 parametric `MC` 的分析与参数综合工具链，而不是新的随机自动机母型。
- 构造方式简述：从 `PRISM` 输入生成 `pMC`，先做 symbolic model checking 求 measure-of-interest 的 rational function，再通过 sampling + `SMT` 做区域验证与 refinement。
- 基础设施与场景简述：依托 `PRISM` 输入、state elimination、`SMT`-guided region synthesis、web front-end 和 visualization，服务参数化可靠性分析、资源约束分析与概率模型修复前置工作。

```text
parametric PRISM model -> rational-function model checking -> sampling / SMT region checks -> safe / unsafe parameter regions
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. parametric discrete-time Markov chains；
2. 参数上的有理函数；
3. reachability / conditional probability / expected reward objectives；
4. safe / unsafe parameter regions；
5. `PROPhESY` 的可视化与 `SMT`-guided synthesis workflow。

### 核心抽象

论文直接给出 `pMC` 元组：

$$
M = (S, V, s_I, P)
$$

上式中的符号逐项解释如下：

1. `S` 是有限状态集合。
2. `V = \{x_1,\ldots,x_n\}` 是实值参数集合。
3. `s_I` 是初始状态。
4. `P : S \times S \to Q_V` 是到有理函数集合 `Q_V` 的参数化转移概率矩阵。
5. 当 `P` 退化为实值矩阵时，模型就回到普通 `MC`。

论文同时定义参数上的有理函数：

$$
f = g_1 / g_2 \in Q_V
$$

上式中的符号逐项解释如下：

1. `g_1` 与 `g_2` 是以参数 `V` 为变量、系数为有理数的多项式。
2. `Q_V` 是所有此类有理函数的集合。
3. `f(u)` 表示把 valuation `u : V \to \mathbb{R}` 代入后的实值。
4. `PROPhESY` 的核心引擎正是围绕这种 symbolic rational function 运算展开。

对参数实例化，论文给出：

$$
M[u] = (S, s_I, P_u)
$$

上式中的符号逐项解释如下：

1. `u` 是对参数集 `V` 的具体赋值。
2. `P_u(s,s') = P(s,s')(u)` 是把每个参数化概率替换为实数后的概率矩阵。
3. 若 `u` 使所有概率合法且每行和为 `1`，就得到一个 well-defined `MC`。
4. 后续概率或期望性质都是在 `M[u]` 上判定。

论文没有把 safe region 单独写成一个总公式，但按其 synthesis 目标可保守整理为：

$$
R_{\mathrm{safe}} = \{u \mid \mu_{M[u]} \triangleleft \lambda\}
$$

上式中的符号逐项解释如下：

1. `u` 是一个参数 valuation。
2. `\mu_{M[u]}` 是在实例化模型 `M[u]` 上求得的 measure-of-interest，例如 reachability probability 或 expected reward。
3. `\triangleleft \lambda` 表示用户给定的阈值关系与界值。
4. 这是根据原文“safe / unsafe regions”工作目标做的保守整理，不是原文逐字元组。

### 一个最小例子与通俗解释

一个最小直觉例子可以是：

1. 某协议里把“转发给好节点”的概率写成参数 `p`，把“丢包概率”写成参数 `q`。
2. 我们关心“最终泄漏发送者身份的概率是否不超过 `5%`”。
3. `PROPhESY` 先把这个性质算成关于 `p,q` 的有理函数，再找出哪些 `(p,q)` 区域一定满足阈值、哪些一定违反阈值。
4. 用户不必逐点枚举所有参数组合，而是直接拿到大块 safe / unsafe polygonal regions。

通俗地说，`PROPhESY` 像是在“参数空间上做模型检查”。普通概率模型检查只回答“这个具体模型是否满足性质”，而它回答的是“哪些参数范围会让模型满足性质”。

### 运行 / 接受 / 转移语义

语义主线是：

1. `pMC` 的转移概率先保持为参数上的有理函数。
2. 一旦给定 `u`，就实例化为普通 `MC`。
3. 对实例化模型可以计算 reachability probability、conditional probability 和 expected reward。
4. 参数综合再把整个参数空间按这些量的阈值关系切分成 safe / unsafe regions。

论文强调 measure-of-interest 至少包括：

$$
\Pr(\Diamond T), \quad \Pr(\Diamond G \mid \Diamond Term), \quad \mathbb{E}[cost \text{ until } T]
$$

上式中的符号逐项解释如下：

1. `\Pr(\Diamond T)` 表示到达目标状态集合 `T` 的概率。
2. `\Pr(\Diamond G \mid \Diamond Term)` 表示条件到达概率。
3. `\mathbb{E}[cost \text{ until } T]` 表示到达目标前累计 reward / cost 的期望。
4. 这些正是工具支持的典型分析对象。

### 语义边界

1. 论文主体聚焦 parametric discrete-time `MC`，不是一般 `MDP` 或任意 stochastic game。
2. 工具强项在参数化概率与 reward 分析，不在通用程序语义建模。
3. 它依赖参数空间可由采样、`SMT` 与 region refinement 有效切分；参数维度非常高时成本会上升。
4. 其 `GUI` 很重要，但不是开放中立交换层。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `pMC` 元组 | `$M = (S, V, s_I, P)$` | 参数化概率模型的基本骨架。 |
| 参数函数 | `$f = g_1 / g_2 \in Q_V$` | reachability / reward 目标被化为有理函数。 |
| 实例化 | `$M[u] = (S, s_I, P_u)$` | 参数赋值后回到普通 `MC`。 |
| 区域综合目标 | `$R_{\mathrm{safe}} = \{u \mid \mu_{M[u]} \triangleleft \lambda\}$` | `SMT` 与 sampling 要证实哪些参数区域满足性质。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 目标模型是有限状态 `pMC`。 |
| 事件 / 触发 | 中等支持 | 依赖 `PRISM` 建模后的转移结构。 |
| 守卫 / 数据 | 弱支持 | 参数主要体现在概率表达式，不是富数据 guard 语言。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 间接支持 | 若 `PRISM` 模型本身含并发模块，可经展开后分析。 |
| 时间约束 | 间接支持 | 论文提到概率 timed families，但核心实现聚焦 `pMC`。 |
| 连续动态 / 随机性 | 很强 | 随机性是模型本体，参数不确定性是核心主题。 |
| 可执行 / 可验证性 | 很强 | 已含 symbolic engine、`SMT` synthesis 和 `GUI`。 |

### 形式化问题与性质

1. 它把“symbolic probability computation”与“region synthesis”串成闭环，而不是只给一条数值分析路线。
2. 对 `project_1` 而言，`PROPhESY` 很适合作为“模型已生成后，如何在参数不完全确定时继续验证”的方法侧证。
3. 其 `safe / unsafe` 区域概念，也很适合迁移到后续 repair 或 profile-based verification 任务。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `PRISM` 风格的参数化 `MC` 模型；
2. 上界或下界形式的概率 / reward 要求；
3. 待分析的参数域；
4. 用户在 `GUI` 中手动指定或调整的候选 region。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 参数化转移矩阵；
2. 有理函数表示；
3. sample points；
4. convex polygons 或自动生成的 region candidates；
5. `SMT` queries。

### 交换与互操作

这篇论文的互操作重点在：

1. 直接接受 `PRISM` 输入模型；
2. symbolic engine 与 `SMT` solver 串联；
3. `GUI` 同时展示 sampling 结果与 synthesis 中间结果。

## 配套基础设施

- 建模/编辑工具：主要依赖 `PRISM` 输入语言和 web front-end，不主打独立图形建模器。
- 解析/交换/元模型支持：核心是 `PRISM` 模型、parametric `MC`、rational-function backend 与 region objects。
- 仿真/执行支持：重点不是 simulation，而是 symbolic quantitative analysis。
- 验证/分析支持：reachability、conditional probability、expected reward、sensitivity analysis、safe/unsafe partitioning。
- 代码生成/转换支持：没有面向部署的代码生成；重点是 parameter-space analysis。
- 标准化或社区生态：与 `PRISM`、`PARAM`、`SMT` 求解器和 parametric-probabilistic verification 社区紧密相连。

## 适用场景与需求前提

### 适用场景

适合早期设计阶段概率参数尚未完全确定、但已经希望分析可达概率、期望代价、鲁棒性或模型修复候选空间的场景。

### 需求前提

1. 模型应能整理为 finite-state parametric `MC`。
2. 关键不确定性主要体现为转移概率或 reward 参数，而不是结构本体不断变化。
3. 性质最好是 reachability、conditional probability 或 expected reward 这类定量目标。
4. 若要高效切分参数空间，参数维度和区域复杂度需仍处于可控范围。

### 不适用或高成本场景

如果问题的主要难点是组件拓扑未定、控制器结构尚未选定或存在强对抗博弈语义，`PROPhESY` 并不是最自然入口。

## 与相邻形式主义的关系

相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，`PRISM` 更像通用概率模型检查平台，而 `PROPhESY` 聚焦参数综合；相对 [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md) 和 [the-probabilistic-model-checker-storm/desc.md](../the-probabilistic-model-checker-storm/desc.md)，`Storm` 侧更强调多模型平台化，`PROPhESY` 更强调 rational-function 与 region synthesis；相对 [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)，后者是 `PTA` 检查桥接，本文是参数空间切分工具链。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“状态机已经建好但参数还不确定”时，仍然可以继续形式化分析，而不必等参数完全定值。
2. 对后续验证 profile 或 repair 闭环，它提供了很合适的 safe / unsafe region 视角。
3. 若 `project_1` 将来把需求中的不确定概率、故障率、超时率抽进模型，`PROPhESY` 是很好的下游验证锚点。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像验证与综合后端，而不是前端目标状态机语言。

### 对需求到模型生成的启发

1. 需求建模时可主动保留概率参数，而不是过早硬编码。
2. 可把“参数范围是否安全”纳入生成后验证环节。
3. 以后做 repair 时也可把参数调优看成区域搜索问题。

## 重要的相关工作

- [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：经典概率模型检查平台。
- [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)：模块化概率模型检查平台的较早工具锚点。
- [the-probabilistic-model-checker-storm/desc.md](../the-probabilistic-model-checker-storm/desc.md)：`Storm` 的完整期刊版平台条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 结论：这是一篇典型的 parametric-probabilistic verification 方法条目，适合作为 `pMC` 参数综合、safe/unsafe region 分析与基于 `SMT` 的概率模型验证路线证据入账。

# 带可变性的服务契约控制器综合 / Controller Synthesis of Service Contracts with Variability

## 基本信息

- 标题：Controller Synthesis of Service Contracts with Variability
- 中文标题：带可变性的服务契约控制器综合
- 作者：Davide Basile, Maurice H. ter Beek, Pierpaolo Degano, Axel Legay, Gian-Luigi Ferrari, Stefania Gnesi, Felicita Di Giandomenico
- 发表：*Science of Computer Programming*, 187:102344, 2020
- DOI：`10.1016/j.scico.2019.102344`
- 链接：https://doi.org/10.1016/j.scico.2019.102344
- 形式主义：`Featured Modal Contract Automata (FMCA)`
- 主类：🔌
- 描述客体：🤝
- 所属领域：🌐
- 论文角色：服务契约组合 / 可变性约束下的 orchestration 综合
- 工具/实现获取方式：原文明确给出 `FMCAT` 原型工具，并说明其建立在 `CAT`/`CATLib` 与 `FeatureIDE` 之上。
- 标准/格式获取方式：承载方式是 contract automata、feature constraint、product line orchestration 与 `FMCAT` 输入模型；原文未给独立行业标准格式。

## 简报

这篇论文的核心贡献，是把原本已经能做 agreement-based orchestration 的 contract automata，推进成一个同时处理“结构可变性”和“行为可变性”的组合模型。结构层用 feature constraint 限定哪些服务动作必须出现或必须禁用；行为层把必要请求再分成 `urgent` 和 `lazy`，前者要求始终满足，后者允许延后满足。结果不是简单多了几个标签，而是把服务组合、产品线和 supervisory control synthesis 真正压进了一套统一自动机里。

- 形式主义定位：面向 service contracts、组合和产品线 orchestrations 的接口/契约自动机，而不是一般组件 DSL。
- 构造方式简述：把单服务或服务组合表示成 `FMCA`，通过 feature constraints 选定合法产品，再综合 most permissive controller 形式的 orchestration。
- 基础设施与场景简述：依托 `FMCAT`、`CAT`/`CATLib`、`FeatureIDE`，服务带 `SLA`、服务优先级和产品线变体的组合式服务系统。

```text
服务契约 + feature constraint -> FMCA composition -> valid product selection -> mpc synthesis -> compliant orchestration / product-line orchestration
```

## 形式主义定义与核心对象

### 定义对象

论文的直接对象包括：

1. principal contract automata，即单个服务契约。
2. service composition，即多方服务组合。
3. feature constraint，即约束合法 product 的布尔公式。
4. urgent / lazy request modalities。
5. orchestration synthesis，即 most permissive controller。

### 核心抽象

论文给出的核心模型是 `Featured Modal Contract Automata`。为了便于阅读，可将原文记号保守整理为：

$$
A = \langle Q, \vec{q}_0, A^\diamond, A^u, A^\ell, A^o, T, \varphi, F \rangle
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `\vec{q}_0` 是初始状态。
3. `A^\diamond` 是 permitted requests 集合。
4. `A^u` 是 urgent requests 集合。
5. `A^\ell` 是 lazy requests 集合。
6. `A^o` 是 offers 集合。
7. `T` 是转移集合，并分成 permitted transitions 与 necessary transitions。
8. `\varphi` 是 feature constraint，用来刻画合法产品。
9. `F` 是终态集合。

若把标签字母表写出来，可保守写成：

$$
\Sigma_A \subseteq (A^r \cup A^o \cup \{\bullet\})^n,\quad A^r = A^\diamond \cup A^u \cup A^\ell
$$

上式中的符号逐项解释如下：

1. `n` 是 automaton 的 rank，也就是参与方数量。
2. `A^r` 是全部 request 集合。
3. `\bullet` 表示该参与方在某次转移中 idle。
4. 一个标签向量上要么出现 request、要么出现 offer、要么出现 match。

论文把语言定义为：

$$
L(A) = \{\, w \mid (w,\vec{q}_0) \xrightarrow{*} (\epsilon,\vec{q}),\ \vec{q} \in F \,\}
$$

上式中的符号逐项解释如下：

1. `w` 是 action trace。
2. `\vec{q}_0` 是初始状态。
3. `\xrightarrow{*}` 是零步或多步执行。
4. `\epsilon` 是空后缀，表示 trace 被完整消费。
5. `\vec{q}` 是到达的终态。

### 一个最小例子与通俗解释

论文最直观的例子是 hotel service product line：

1. `BusinessClient` 和 `EconomyClient` 都会向 `Hotel` 请求房间。
2. feature constraints 决定诸如 `card`、`cash`、`sharedBathroom` 是否被选中。
3. `singleRoom` 可被标成 urgent request，表示必须优先满足。
4. `invoice` 可被标成 lazy request，表示最终得被满足，但可以延后。

通俗地说，`FMCA` 就像“带配置开关的契约状态机”：不仅要问“服务之间能否配起来”，还要问“当前启用了哪些产品特征”“哪些请求必须立刻响应”“哪些请求可以稍后补上”。

### 运行 / 接受 / 转移语义

论文的 product composition 运算是 `\bigotimes`。可保守理解为：当两个参与方一个发 offer、一个发 matching request 时，组合后优先生成 match transition，而不是任由二者无约束交错。

论文对安全性给出 agreement 视角。可把 agreement language 写成：

$$
\mathcal{A} = \{\, w \in \Sigma_A^* \mid \text{每一步都是 match 或 offer，没有裸 request} \,\}
$$

于是安全性可写成：

$$
L(A) \subseteq \mathcal{A}
$$

上式中的符号逐项解释如下：

1. `\mathcal{A}` 是 agreement traces 的集合。
2. `L(A)` 是 automaton 的全部接受语言。
3. 若 `L(A) \subseteq \mathcal{A}`，则表示 automaton 的所有执行都满足 agreement。

对单一有效产品 `p`，综合目标是求其 mpc。论文把 controller 的核心约束归结为：

$$
K_p = \mathrm{mpc}(A,p)
$$

其中：

1. `K_p` 是产品 `p` 的 orchestration。
2. 它必须安全、无 dangling states，并尊重 `Mandatory(p)` 与 `Forbidden(p)`。
3. 在所有满足这些条件的 controllers 中，它还要语言最大，即“最宽松但仍正确”。

### 语义边界

这篇论文的语义边界很明确：

1. 它建模的是服务契约与组合，不是任意软件组件内部算法。
2. 其 variability 主要作用在 actions 和 products 上，而非一般数据变量空间。
3. `urgent/lazy` 是对 request criticality 的建模，不是 timed automata 那种时钟时间。
4. orchestration 是集中式控制语义，不是 runtime implementation 本身。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| FMCA 骨架 | `$A = \langle Q, \vec{q}_0, A^\diamond, A^u, A^\ell, A^o, T, \varphi, F \rangle$` | 同时建模服务动作、criticality 和产品线约束。 |
| 标签字母表 | `$\Sigma_A \subseteq (A^r \cup A^o \cup \{\bullet\})^n$` | 多方服务通过向量标签同步或空转。 |
| 接受语言 | `$L(A) = \{\, w \mid (w,\vec{q}_0)\xrightarrow{*}(\epsilon,\vec{q}), \vec{q}\in F \,\}$` | 服务组合的完整行为 traces。 |
| agreement | `$L(A) \subseteq \mathcal{A}$` | 所有请求都必须被相应 offer 匹配。 |
| 产品约束 | `$p \in J\varphi K$` | 只有满足 feature constraint 的配置才是合法产品。 |
| orchestration 综合 | `$K_p = \mathrm{mpc}(A,p)$` | 综合得到该产品的最宽松合规 orchestrator。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个 principal / composite contract 都是自动机。 |
| 事件 / 触发 | 强支持 | request、offer、match 是核心执行单位。 |
| 守卫 / 数据 | 弱支持 | 重点在动作和配置约束，不在复杂数据守卫。 |
| 层次 | 部分支持 | 通过 product line / composition 层次组织，而非层次状态机。 |
| 并发 / 同步 | 强支持 | 多方契约组合和 match 是主体。 |
| 时间约束 | 不支持 | `urgent/lazy` 是 criticality，不是 clock semantics。 |
| 连续动态 / 随机性 | 不支持 | 纯离散契约自动机。 |
| 可执行 / 可验证性 | 强综合 | 可直接求 product-level 与 family-level orchestration。 |

### 形式化问题与性质

1. 论文最大的增量不是“contract automata 再加一个 feature model”，而是把 structural variability 和 behavioural variability 真正结合起来。
2. `urgent` 与 `lazy` 让“必须匹配”这件事从单值约束变成了有优先级和延迟语义的约束。
3. partial order 与 canonical products 让 product-line orchestration 不必对所有产品逐个全算。
4. 这使它非常适合作为接口/契约类主干文献，而不是边缘应用状态机。

## 构造方式与承载格式

### 建模入口

建模入口通常是：

1. 先为每个服务写 principal contract automaton。
2. 再为产品线写 feature constraint。
3. 根据业务要求把请求标成 permitted / urgent / lazy。
4. 最后做 composition、product validity 判断与 orchestration synthesis。

### 机器可处理承载方式

原文体现出的机器可处理承载方式包括：

1. `FMCAT` 中的 `FMCA` 模型。
2. `FeatureIDE` 中的 feature model / propositional constraint。
3. `CAT` / `CATLib` 的 contract automata operations。
4. canonical products 与 family-level orchestration。

### 交换与互操作

互操作重点是：

1. feature-level 约束与 automata-level 语义分离再结合。
2. 单个服务契约可被组合、重用、替换。
3. family-level orchestration 可复用于多个有效产品。

## 配套基础设施

- 建模/编辑工具：`FMCAT` 与 `FeatureIDE`。
- 解析/交换/元模型支持：`CAT` / `CATLib` 提供 contract automata 操作；feature model 用布尔约束表达。
- 仿真/执行支持：论文主体是综合与分析，不是运行时执行。
- 验证/分析支持：agreement analysis、product validity、mpc synthesis、family-level orchestration。
- 代码生成/转换支持：原文未提供直接代码生成。
- 标准化或社区生态：研究型 contract automata 工具链，生态集中在作者工具线。

## 适用场景与需求前提

### 适用场景

适合服务计算、接口契约组合、带 `SLA` 差异和产品线变体的服务编排系统。

### 需求前提

1. 服务可用 offer / request 的交互契约表达。
2. 需求关心“哪些请求必须被满足”以及满足优先级。
3. 系统存在稳定的 feature-level 配置空间。
4. 可以接受集中式 orchestration 作为实现蓝本。

### 不适用或高成本场景

如果系统核心难点在复杂数据流、低层并发实现、时间与资源定量优化，而不是契约满足和组合一致性，那么 `FMCA` 会显得偏高层、偏行为契约。

## 与相邻形式主义的关系

相对 [Contract Automata](../contract-automata/desc.md)，本文引入了 feature constraints 与 urgent/lazy variability；相对 [Interface Automata](../interface-automata/desc.md)，它更强调 request-offer agreement 与 orchestration synthesis，而不是输入输出兼容性；相对 [Reactive Modules](../reactive-modules/desc.md)，它不以 guarded variables 为中心，而以契约交互为中心。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文表明，接口/契约型自动机并不只是“接口是否兼容”的静态检查工具，也可以承载需求优先级、产品配置与自动综合。

### 作为目标形式主义还是中间表示

在服务组合、协议交互和多组件协同场景中，它可以直接作为目标形式主义；在更一般控制系统里，它更适合作为接口层中间表示。

### 对需求到模型生成的启发

1. 需求生成时可以把“必须 / 可选 / 延迟满足”直接编码到动作层，而不必埋到说明文字里。
2. 配置空间和行为语义最好分开抽取，再在自动机层组合。
3. 面向多变体系统时，优先生成 canonical products 比穷举所有产品更现实。

## 重要的相关工作

- [Contract Automata](../contract-automata/desc.md)：本文直接建立其上。
- [Interface Automata](../interface-automata/desc.md)：同属接口/组合路线，但兼容性口径不同。
- `Timed service contract automata`：原文提到的后续时间扩展路线，说明 contract automata 还能继续接时序语义。

## 文献分类总结

- 这是一篇 `🔌` 类高价值主干条目，核心是服务契约与产品线组合，而不是 DSL 或标准载体。
- 其描述客体是接口/交互契约，因此记为 `🤝`；论文语境面向服务组合与分布式交互，因此记为 `🌐`。
- 对 `project_1` 来说，它非常适合补“接口/组合/契约模型”这条主干，并为后续组合验证与自动修复提供更细颗粒度的约束对象。

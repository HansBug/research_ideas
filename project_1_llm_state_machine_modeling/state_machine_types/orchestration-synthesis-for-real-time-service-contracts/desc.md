# 面向实时服务契约的编排综合 / Orchestration Synthesis for Real-Time Service Contracts

## 基本信息

- 标题：Orchestration Synthesis for Real-Time Service Contracts
- 中文标题：面向实时服务契约的编排综合
- 作者：Davide Basile，Maurice H. ter Beek，Axel Legay，Louis-Marie Traonouez
- 发表：收录于 *Verification and Evaluation of Computer and Communication Systems*，pp. 31-47，2018
- DOI：`10.1007/978-3-030-00359-3_3`
- 链接：https://doi.org/10.1007/978-3-030-00359-3_3
- 形式主义：`Timed Service Contract Automata (TSCA)`
- 主类：🔌
- 描述客体：🤝
- 所属领域：🌐
- 论文角色：实时服务契约编排 / `Contract Automata` 的时间与关键性扩展
- 工具/实现获取方式：原文给出基于 timed games 与 zones 的 symbolic synthesis 过程，并说明可用 timed games library 实现；原文未提供独立公开代码仓库。
- 标准/格式获取方式：承载方式是 `TSCA` 元组、zones、winning strategy 与 safe orchestration；原文未给统一交换标准。

## 简报

这篇论文处理的是服务契约组合里最难自动化的一步：多个服务都带有 request/offer 约束时，不光要判断“能不能配”，还要算出一条在时间上安全、在关键请求上不失守的 orchestration。作者在 `Contract Automata` 路线上加入 clocks，并把必要请求细分成 `urgent / greedy / lazy` 三个 criticality 等级，然后用 zones 和 supervisory control 里的 most-permissive controller 思想综合 safe orchestration。

- 形式主义定位：这是接口/组合/契约主干上的应用型条目，核心价值是给服务契约组合补上“时间 + 请求关键性 + 可综合控制器”三层能力。
- 构造方式简述：先用 `TSCA` 建模单个 principal 的 request/offer/match 与 clocks，再做 compositional product，最后在 symbolic configuration graph 上计算 safe orchestration。
- 基础设施与场景简述：依托 timed games、zones 和 supervisory control，服务于实时预订、服务协商、多方业务组合与不同关键等级请求并发竞争场景。

```text
real-time service contracts -> TSCA composition -> uncontrollable-disagreement analysis -> maximal winning strategy -> safe orchestration
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 带时间约束的服务契约自动机 `TSCA`。
2. 四类请求/动作模态：permitted、urgent、greedy、lazy。
3. 记录时间窗口的时钟集合 `X` 与 rectangular constraints。
4. 在组合后空间上运行的 configurations `(q, v)` 与 zones。
5. 作为综合结果的 safe orchestration strategy。

### 核心抽象

论文对 `TSCA` 的定义是：

$$
A = \langle Q, q_0, A_3, A_{2u}, A_{2g}, A_{2\ell}, A_o, X, T, F \rangle
$$

上式中的符号逐项解释如下：

1. `Q = Q_1 \times \cdots \times Q_n` 是局部状态集合的积，表示 rank 为 `n` 的组合状态空间。
2. `q_0 \in Q` 是初始状态。
3. `A_3` 是 permitted requests 集合。
4. `A_{2u}`、`A_{2g}`、`A_{2\ell}` 分别是 urgent、greedy、lazy 必要请求集合。
5. `A_o` 是 offers 集合。
6. `X` 是实值 clocks 集合。
7. `T` 是带 guards、actions、reset 集合的迁移。
8. `F` 是接受状态集合。

论文把请求集记为：

$$
A_r = A_3 \cup A_2,\quad A_2 = A_{2u} \cup A_{2g} \cup A_{2\ell}
$$

上式中的符号逐项解释如下：

1. `A_r` 是所有 requests 的总集合。
2. `A_3` 表示 permitted requests，可在不破坏安全的前提下被丢弃。
3. `A_{2u}` 表示最严格的 urgent requests。
4. `A_{2g}` 表示 greedy requests，一旦能匹配就不能再被禁用。
5. `A_{2\ell}` 表示 lazy requests，只要后续还能保证 agreement，可以暂缓。

对可组合 `TSCA` 的组合，论文给出：

$$
A = \bigotimes_{i=1}^{n} A_i
$$

上式中的符号逐项解释如下：

1. `A_i` 是各个 composable `TSCA`。
2. 组合通过 interleaving 与 complementary request-offer matching 共同构造。
3. 如果两个分量上存在互补动作，则优先形成 match，而不是任意自由交错。
4. 组合结果仍是一个 `TSCA`，供后续 orchestration synthesis 使用。

论文最关键的综合对象是 safe orchestration 对应的 winning strategy。其 fixed-point 核心写成：

$$
C_0 = \{ c \mid c \xrightarrow{a},\ a \text{ 是 } \hat{A} \text{ 上的 uncontrollable request} \}
$$

$$
f^\ast =
\begin{cases}
\bot & \text{若 } (q_0,0) \in C^\ast \\
f_{C^\ast} & \text{否则}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `\hat{A}` 是把 permitted requests 剪掉后的 `TSCA`。
2. `C_0` 是最初的不安全配置集合。
3. `C^\ast` 是反复应用 predecessor、dangling 与 uncontrollable-disagreement 运算后的最小不动点。
4. 若初始配置落入 `C^\ast`，则不存在安全编排。
5. 否则 `f^\ast` 就是可实施的 safe orchestration strategy。

### 一个最小例子与通俗解释

论文用酒店订房场景说明 `TSCA`：

1. `Hotel` 提供普通房和折扣房，并要求支付方式和收据流程按时完成。
2. `DiscountClient` 会先请求 discount room，再提供 `card`，最后请求 `receipt`。
3. 若某个请求是 `urgent`，系统就不能无限拖延等待；若是 `lazy`，则可以在还有后续 match 机会时暂缓。
4. 综合器会删掉那些会把系统带向 disagreement 的动作，只保留仍能到达 final agreement 的那部分行为。

通俗地说，这像“给服务合同加上红黄绿优先级，再让控制器自动决定哪些请求现在必须满足、哪些可以先压住，否则整个协作就会超时或违约”。

### 运行 / 接受 / 转移语义

`TSCA` 的运行状态是 configuration `(q, v)`，其中 `q` 是离散组合状态，`v` 是时钟赋值。论文把 agreement 语言写成：

$$
\mathcal{A} = \{ w \in (\Sigma_n^\#)^\ast \mid \forall i,\ w(i)=a^\# \Rightarrow a \text{ 是 match 或 offer} \}
$$

上式中的符号逐项解释如下：

1. `\Sigma_n^\#` 是带模态标签的组合动作字母表。
2. `w` 是某条接受 trace。
3. 若 trace 中出现的必要动作都表现为 match 或 offer，则该 trace 属于 agreement 语言。
4. 这意味着单边未满足的 request 不应出现在最终安全语言中。

论文进一步把“不受控分歧”定义成综合必须避免的坏配置。若某配置只能继续经过 timed/forced transitions，且最终无法在不经过坏集合 `C` 的前提下到达 final agreement，那么该配置就属于 uncontrollable disagreement。安全编排就是永远不触达这类配置的 maximal winning strategy。

### 语义边界

这篇论文的边界主要在于：

1. 主体是服务契约组合，不处理复杂内部数据语义。
2. 时间约束采用 rectangular clocks，适合 timed games / zones。
3. 关键性区分只作用于 requests / matches 的可控性，不是一般 QoS 优化。
4. 连续动力学和概率不是主体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TSCA` 定义 | `$A = \langle Q, q_0, A_3, A_{2u}, A_{2g}, A_{2\ell}, A_o, X, T, F \rangle$` | 给服务契约同时编码时间和请求关键性。 |
| 请求分层 | `$A_r = A_3 \cup A_2,\ A_2 = A_{2u} \cup A_{2g} \cup A_{2\ell}$` | 把请求分成 permitted / urgent / greedy / lazy 四类。 |
| 组合 | `$A = \bigotimes_{i=1}^{n} A_i$` | 构造多方服务契约的 product。 |
| agreement 语言 | `$\mathcal{A} = \{w \mid w(i)=a^\# \Rightarrow a \text{ 是 match 或 offer}\}$` | 判定一条 trace 是否真正达成 agreement。 |
| 初始坏集 | `$C_0 = \{ c \mid c \xrightarrow{a},\ a \text{ 是 uncontrollable request}\}$` | 标出综合起点上的危险配置。 |
| 安全编排策略 | `$f^\ast = \bot$ 或 `$f_{C^\ast}$` | 给出“无解”或“最大安全编排”两种输出。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 多 principal 的局部状态通过 product 构成组合状态。 |
| 事件 / 触发 | 强支持 | request / offer / match 是一等动作。 |
| 守卫 / 数据 | 部分支持 | 重点是 clocks 和 rectangular guards，而非复杂数据变量。 |
| 层次 | 不支持 | 主体是组合自动机，不是层次状态机。 |
| 并发 / 同步 | 强支持 | composition 明确处理 interleaving 与 complementary matching。 |
| 时间约束 | 强支持 | clocks、zones、timed games 是核心。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散实时契约。 |
| 可执行 / 可验证性 | 强验证 | 可综合 maximal winning strategy。 |

### 形式化问题与性质

1. 论文真正补出的不是“实时服务契约能不能写”，而是“写完后怎样自动删掉危险行为、保住 agreement”。
2. `urgent / greedy / lazy` 把 request 的控制优先级显式化，这比普通 request/offer 二元分类更细。
3. 由于综合基于 zones，`TSCA` 不只是描述语言，还是可操作的 synthesis 对象。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 为每个 principal 写局部契约状态机。
2. 标记每个 request 是 permitted、urgent、greedy 还是 lazy。
3. 在迁移上加入 clocks 和 rectangular guards。
4. 对多个 principal 做 compositional product。
5. 在 configuration/zone 层运行 orchestration synthesis，求最大安全策略。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `TSCA` 图模型与 tuple。
2. symbolic configurations `(q, v)`。
3. zones 与 predecessor 运算。
4. safe orchestration strategy。

### 交换与互操作

互操作重点在：

1. 各 principal 的 clocks 必须彼此不相交，才能做 composable product。
2. complementary request / offer 会被自动提升成 match。
3. synthesis 输出的是策略级编排，而不是单纯语言判定。

## 配套基础设施

- 建模/编辑工具：原文主要给出形式化定义和 symbolic synthesis 过程，没有配套图形建模器。
- 解析/交换/元模型支持：支持 zone-based symbolic configuration 运算，但无统一交换格式。
- 仿真/执行支持：主体不强调运行时执行器，而强调 orchestration synthesis。
- 验证/分析支持：可计算 agreement、安全性、dangling configurations 与 uncontrollable predecessors。
- 代码生成/转换支持：原文未给代码生成链。
- 标准化或社区生态：依托 timed games、zone 库和 `Contract Automata` 研究线。

## 适用场景与需求前提

### 适用场景

适合实时服务组合、预订/支付/票务/资源协商等需要同时处理时限和契约优先级的多方交互系统。

### 需求前提

1. 服务交互能抽成有限 request / offer / match 集合。
2. 时间约束能写成 clocks 上的矩形约束。
3. 设计目标是 agreement 与安全编排，而非性能最优调度。
4. 需要区分哪些请求绝不能失配、哪些请求允许延后或丢弃。

### 不适用或高成本场景

如果系统关键难点在复杂数据操作、概率服务质量或连续物理过程，仅靠 `TSCA` 综合会过于抽象。

## 与相邻形式主义的关系

相对 [Contract Automata](../contract-automata/desc.md)，本文是在 contract automata 主线上补入时间和 criticality；相对 [Controller Synthesis of Service Contracts with Variability](../controller-synthesis-of-service-contracts-with-variability/desc.md)，这里关注 real-time constraints 和 orchestration，而不是产品线 variability；相对 [Towards Verifying Contract Regulated Service Composition](../towards-verifying-contract-regulated-service-composition/desc.md)，这里输出的是 safe orchestration strategy，而不是把契约约束转译到外部模型检查器。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果需求里除了“谁和谁交互”，还有“这个请求必须尽快满足”“那个请求可以延后但不能永远丢”，那么模型里最好直接把请求分级，而不是都塞进同一种 transition guard。

### 作为目标形式主义还是中间表示

对服务契约与交互规约，它可以直接作为目标形式主义；对更大的控制系统需求，它更适合作为交互契约层和资源协商层的中间表示。

### 对需求到模型生成的启发

1. 需求中的必须/可选/可延后可以直接映射到 `urgent / greedy / lazy / permitted`。
2. “无论怎样调度都不能违约”对应的是 winning strategy，而不仅仅是 reachability。
3. 组合模型一开始就应考虑 controllability，否则后面只能做被动检查。

## 重要的相关工作

- [Contract Automata](../contract-automata/desc.md)：服务 request/offer agreement 的基础家族。
- [Controller Synthesis of Service Contracts with Variability](../controller-synthesis-of-service-contracts-with-variability/desc.md)：在 contract automata 上补 variability 与 controller synthesis。
- [Specification and Verification of Context-dependent Services](../specification-and-verification-of-context-dependent-services/desc.md)：更偏服务配置与上下文约束。
- [Towards Verifying Contract Regulated Service Composition](../towards-verifying-contract-regulated-service-composition/desc.md)：更偏把 contract-regulated composition 送进外部验证链。

## 文献分类总结

- 这是一篇 `🔌` 类应用型条目，核心价值是把 `Contract Automata` 推进到“带 clocks 和请求关键等级的可综合编排”。
- 它描述的是服务请求/提供方之间的契约交互，因此记为 `🤝`；研究语境是多方服务组合与协商，因此记为 `🌐`。
- 对 `project_1` 来说，它最重要的启发是：需求生成状态机时，不仅要产出状态和转移，还可以同时生成“可控性分层”和“策略综合目标”。

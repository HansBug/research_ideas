# 为什么时间自动机上的活性验证更难，以及我们能做什么 / Why Liveness for Timed Automata Is Hard, and What We Can Do About It

## 基本信息

- 标题：Why Liveness for Timed Automata Is Hard, and What We Can Do About It
- 中文标题：为什么时间自动机上的活性验证更难，以及我们能做什么
- 作者：Frédéric Herbreteau，B. Srivathsan，Thanh-Tung Tran，Igor Walukiewicz
- 发表：*ACM Transactions on Computational Logic*，Vol. 21, No. 3，pp. 1-28，2020
- DOI：`10.1145/3372310`
- 链接：https://doi.org/10.1145/3372310
- 形式主义：`Timed Büchi Automata / abstract zone graph / a≼LU / liveness-compatible subsumption graph`
- 主类：⏱️ 时间 / 时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed-automata Büchi/liveness verification 的复杂度分析与 witness-computation 路线
- 工具/实现获取方式：原文明确实现了基于 `SCC` 的迭代算法，并在 `UPPAAL` benchmark 上对比了已有方案；正文未给独立开源仓库入口。
- 标准/格式获取方式：核心承载不是交换标准，而是 `Timed Büchi Automata`、`abstract zone graph`、`a≼LU` 抽象与 subsumption graph 见证结构。

## 简报

这篇论文补的是 timed automata 验证里一个经常被低估的空白：reachability 很成熟，不代表 liveness 也能靠同一套 subsumption 技巧轻松解决。作者证明了 Büchi/liveness 在算法层面确实更难，然后给出一种“活性兼容的 subsumption witness”与迭代 `SCC` 精化算法，让实践上仍能接近 reachability invariant 的大小。

- 形式主义定位：围绕 `Timed Büchi Automata` 的活性验证方法路线，而不是新的时间自动机本体。
- 构造方式简述：`TBA -> abstract zone graph with a≼LU -> subsumption graph -> safe/unsafe SCC refinement -> liveness-compatible witness`。
- 基础设施与场景简述：依托 `zone graph`、`a≼LU`、subsumption edges 与 `SCC` 分析，服务 timed model checking 中的 Büchi non-emptiness 与活性调试。

```text
Timed Büchi Automaton -> 抽象 zone graph -> subsumption graph -> unsafe SCC 精化 -> liveness witness 或 accepting cycle
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Timed Büchi Automaton (TBA)`。
2. `zone` 与 `abstract zone graph`。
3. `a≼LU` 抽象及其 induced subsumption。
4. `subsumption graph` 与 liveness-compatible criterion。
5. 基于 `SCC` 的 iterative witness-finding algorithm。

### 核心抽象

论文直接采用 timed Büchi automaton：

$$
A = (Q, q_0, X, T, F)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是有限状态集合。
2. `$q_0$` 是初始状态。
3. `$X$` 是时钟集合。
4. `$T \subseteq Q \times \Phi(X) \times 2^X \times Q$` 是带 guard 与 reset 的转移集合。
5. `$F \subseteq Q$` 是接受状态集合。

论文要解决的问题不是普通 reachability，而是非 Zeno 的 Büchi 非空性。可保守整理为：

$$
\exists \rho \text{ infinite}, \quad \rho \text{ visits } F \text{ infinitely often and is non-Zeno}
$$

上式中的符号逐项解释如下：

1. `$\rho$` 是从初始配置出发的无限运行。
2. “visits `$F$` infinitely often” 是 Büchi 接受条件。
3. “non-Zeno” 要求总耗时发散，而不是在有限时间内完成无限步。

为了做抽象验证，论文使用 `a≼LU` 抽象上的 zone graph。对两个节点 `$t,s$`，其 subsumption 关系可写成：

$$
t \sqsubseteq s \iff t.q = s.q \land a_{\preceq LU}(t.Z) \subseteq a_{\preceq LU}(s.Z)
$$

上式中的符号逐项解释如下：

1. `$t.q$` 与 `$s.q$` 是两个节点的离散控制位置。
2. `$t.Z$` 与 `$s.Z$` 是对应的 zones。
3. `$a_{\preceq LU}$` 是只依赖 `LU` bounds 的抽象。
4. 若成立，则 `$s$` 可以覆盖 `$t$` 的抽象行为。

论文进一步给出 liveness-compatible subsumption graph。其最关键的兼容条件可压成：

$$
G \text{ is liveness-compatible } \iff \text{no cycle in } G \text{ contains both an accepting node and a subsumption edge}
$$

上式中的符号逐项解释如下：

1. `$G$` 是带普通边与 subsumption edges 的图。
2. accepting node 指其离散状态属于 `$F$`。
3. 若一个环同时包含接受点和 subsumption edge，则可能把真正的 accepting run“折没掉”。
4. 因此该条件是从 reachability invariant 升级到 liveness witness 的关键。

### 一个最小例子与通俗解释

论文里的一个直观例子是：自动机不断回到某个接受状态 `1`，但每次回去时都要求额外时钟条件，例如某个不被重置的时钟 `$y$` 还必须满足 `$y \le 100$`。表面上看：

1. reachability 图很快就能看出“接受状态可达”；
2. 用 subsumption 压缩后，图甚至会显得很小；
3. 但实际上每次回到接受状态都会让 `$y$` 增长；
4. 增长到一定程度后就再也无法回来，因此根本不存在无限次访问接受状态的 run。

通俗地说，reachability 只问“能不能到一次”，而 liveness 要问“能不能一直回来”。对 timed automata 来说，这两个问题共享一些底层结构，但绝不等价。

### 运行 / 接受 / 转移语义

论文给出两类语义转移：

$$
(q,v) \xrightarrow{\delta} (q,v+\delta), \qquad (q,v) \xrightarrow{t} (q',[R]v)
$$

上式中的符号逐项解释如下：

1. 第一类是时间延迟步，`$\delta \in \mathbb{R}_{\ge 0}$`。
2. 第二类是离散动作步，其中 `$t=(q,g,R,q')$`。
3. `$v \models g$` 时 guard 才允许离散转移发生。
4. `[R]v` 表示把 `$R$` 中出现的时钟重置为 `0` 后得到的新 valuation。

论文的主定理把活性验证压成 witness 图问题。可保守写成：

$$
A \text{ has an accepting run } \iff G \text{ has an infinite accepting path of ordinary edges}
$$

上式中的符号逐项解释如下：

1. `$A$` 是原始 `TBA`。
2. `$G$` 是满足 liveness-compatible 条件的 subsumption graph。
3. “ordinary edges” 指真正来自 zone graph 的普通后继边，而不是 subsumption edges。
4. 这说明只要 witness 图构造得对，活性问题仍可落成图上的接受环搜索。

### 语义边界

1. 论文关注的是 `Timed Büchi Automata` 上的活性，不是一般 `LTL` 全流程实现细节。
2. 作者明确假设 strongly non-Zeno 输入，避免额外展开 Zeno 处理主线。
3. 方法的关键收益在“比完全展开无 subsumption 的 zone graph 小很多”，而不是保证和 reachability 一样简单。
4. 核心抽象依赖 `LU` bounds 与 zone-graph verification 生态，不是任意 timed formalism 都可直接套用。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TBA` 骨架 | `$A=(Q,q_0,X,T,F)$` | 活性验证的基本对象。 |
| Büchi 非空性 | `$\exists \rho$ infinite, accepting, non-Zeno` | 与普通 reachability 不同的目标。 |
| subsumption | `$t \sqsubseteq s \iff a_{\preceq LU}(t.Z)\subseteq a_{\preceq LU}(s.Z)$` | reachability 压缩的基础。 |
| 活性兼容条件 | `no accepting-cycle-with-subsumption-edge` | 防止 accepting run 被错误折叠。 |
| 主结论 | `$A$ accepting iff $G$ has accepting path of ordinary edges` | 把活性问题重新固定成 witness 图问题。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | timed location 加 zone 是主对象。 |
| 事件 / 触发 | 中等支持 | 主要关心 guards / resets 与 Büchi 接受，不强调 I/O 接口。 |
| 守卫 / 数据 | 中等支持 | 守卫核心是时钟约束，而非一般数据变量。 |
| 层次 | 不支持 | 主体是扁平 timed automata。 |
| 并发 / 同步 | 中等支持 | 可作用于 network 乘积后得到的 `TBA`，但算法主体不讨论组合语义设计。 |
| 时间约束 | 很强 | clocks、zones、`LU` abstraction 都是中心内容。 |
| 连续动态 / 随机性 | 不支持 | 纯 timed discrete semantics。 |
| 可执行 / 可验证性 | 很强 | 直接指向 Büchi emptiness、witness construction 与 benchmark evaluation。 |

### 形式化问题与性质

1. 这篇论文最核心的洞见是：时间自动机里，liveness 不能被“reachability + 一点点改动”代替。
2. `a≼LU` 仍然是关键抽象，但对 liveness 必须重新定义什么叫“安全的覆盖”。
3. 迭代 `SCC` 精化把理论上的更难，转成实践上经常只需少量 refinement 的工程策略。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Timed Büchi Automata`。
2. 由 timed model 与性质自动机乘积得到的 `TBA`。
3. `LU` bounds 决定的抽象 zone graph。
4. `SCC` 精化过程中形成的 subsumption graph。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `(state, zone)` 节点。
2. 普通后继边与 subsumption edge。
3. `SCC` 标记的安全 / 不安全区域。
4. 最终 liveness witness 或 accepting cycle。

### 交换与互操作

1. 论文主线不是文件格式互操作，而是 timed-verification backend 的算法层互操作。
2. 它天然适合接在 `UPPAAL` 一类 zone-based verifier 的后端。
3. 若上游是 `LTL` 或监视器自动机，则可先做产品构造，再交给本路线处理 Büchi 非空性。

## 配套基础设施

- 建模/编辑工具：原文未引入新建模语言，默认承接现有 timed automata 模型。
- 解析/交换/元模型支持：`zone`、`DBM` 风格抽象、`a≼LU` 抽象与 subsumption graph。
- 仿真/执行支持：主体不是仿真器，而是活性 witness 计算。
- 验证/分析支持：Büchi non-emptiness、zone graph with subsumption、unsafe `SCC` refinement、accepting-cycle detection。
- 代码生成/转换支持：无部署代码生成；转换重点是从 abstract zone graph 迭代构造 liveness-compatible witness。
- 标准化或社区生态：实验基于 `UPPAAL` benchmarks，说明它与主流 timed-verification 生态兼容。

## 适用场景与需求前提

### 适用场景

适合需要验证实时系统活性、重复可达性、持续响应性，或需要检查 timed model 是否实际上“还能一直运行下去”的场景。

### 需求前提

1. 模型需能落成 `Timed Büchi Automata` 或其产品。
2. 性质核心应能表达为“接受状态被无限次访问”。
3. 验证后端需要是 zone-based，而不是纯 region-based 或 SAT-only 路线。
4. 团队接受 reachability invariant 对 liveness 不再足够这一现实。

### 不适用或高成本场景

1. 若只关心一次性 reachability / safety，本路线通常不是首选。
2. 若 timed model 已极大，最坏情况下算法仍可能退化到接近无 subsumption 的 zone graph。
3. 若对象是 hybrid、stochastic 或 priced extensions，需另行扩展语义与抽象。

## 与相邻形式主义的关系

相对 [improving-search-order-for-reachability-testing-in-timed-automata/desc.md](../improving-search-order-for-reachability-testing-in-timed-automata/desc.md)，后者优化的是 reachability 搜索顺序，而这里证明了 reachability 与 liveness 在难度上有本质差距；相对 [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md)，那篇更偏 verified reference checker，这篇更偏 witness graph 与活性算法学；相对 [testing-real-time-systems-using-uppaal/desc.md](../testing-real-time-systems-using-uppaal/desc.md)，`UPPAAL-TRON` 路线把 timed automata 用于测试，而本文则直接重审 timed Büchi verification 的后端难点。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 和后续验证主题都很重要，因为博士主线不只会碰到 safety，还会碰到“模型是否持续响应”“系统是否可能长期停滞”这类活性问题。它提供三点直接价值：

1. 提醒我们不能把活性验证简单降格为 reachability 验证。
2. 给出了一种可解释的 witness 结构，适合后续由 LLM 生成验证剖面时做反馈。
3. 为 timed state machine 的验证后端提供了更接近工程可落地的算法模板。

### 可借鉴点

1. 在“生成-验证-修复”闭环中，可把 unsafe `SCC` 精化视为一种结构化诊断信号。
2. 若 LLM 先生成 timed model，再由 verifier 给出 liveness-compatible witness，修复阶段就有更明确的定位对象。
3. 这条路线也说明 verification profile 不应只记录 reachability queries，还应记录接受条件和活性判据。

### 局限与注意事项

1. 原文主要处理 timed Büchi 后端，不涵盖高层需求编写语言。
2. 对极端困难模型，算法仍可能需要深度 refinement。
3. 若性质不是 Büchi 风格，仍需前置变换或另外的逻辑编译链。

## 重要的相关工作

1. [improving-search-order-for-reachability-testing-in-timed-automata/desc.md](../improving-search-order-for-reachability-testing-in-timed-automata/desc.md)：补 reachability 侧的 zone 搜索优化，与本文形成鲜明对照。
2. [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md)：补 timed-automata verifier 的可信实现路线。
3. [testing-real-time-systems-using-uppaal/desc.md](../testing-real-time-systems-using-uppaal/desc.md)：补 timed automata 在测试侧的工具化路线，说明同一形式主义在验证目标上的差异。

## 文献分类总结

- 这是一篇 `⏱️ 时间 / 时钟自动机` 条目，因为对象始终是 `Timed Büchi Automata` 与 zone 抽象。
- 这是一篇 `🛠️ 方法路线` 条目，因为核心贡献是 liveness witness 与迭代 `SCC` 算法，而不是新的标准格式或工作台。
- 它描述的核心对象是 `🎛️ 控制 / 反应式逻辑`，因为目标是实时控制行为的持续可响应性。
- 它应挂在 `timed-automata symbolic checking / liveness-witness route` 的静态方法口径下，补强 timed verification 不应只看 reachability 的这一条线。

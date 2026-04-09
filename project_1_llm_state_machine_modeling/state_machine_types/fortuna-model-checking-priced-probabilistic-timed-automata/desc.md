# FORTUNA：有代价概率定时自动机模型检查器 / Fortuna: Model Checking Priced Probabilistic Timed Automata

## 基本信息

- 标题：Fortuna: Model Checking Priced Probabilistic Timed Automata
- 中文标题：FORTUNA：有代价概率定时自动机模型检查器
- 作者：Jasper Berendsen，David N. Jansen，Frits W. Vaandrager
- 发表：*2010 Seventh International Conference on the Quantitative Evaluation of Systems*，pp. 273-281，2010
- DOI：`10.1109/QEST.2010.41`
- 链接：https://doi.org/10.1109/QEST.2010.41
- 形式主义：`Priced Probabilistic Timed Automata / PPTA / FORTUNA`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：首个同时覆盖时间、概率与代价的 `PPTA` 模型检查工具
- 工具/实现获取方式：论文把 `FORTUNA` 作为工具发布，但正文未给出稳定公开仓库或长期下载地址。
- 标准/格式获取方式：输入对象是 `PPTA`，内部承载是 multi-priced zones、backward reachability graph 与后续 `MDP` 分析；它不是行业交换标准。

## 简报

`FORTUNA` 补的是概率实时平台线里一个非常关键但又很容易缺口的点：把 `real-time + probability + cost` 三种量化语义放进同一个可算工具里。对 `PTA` 来说，`PRISM` 和 `mcpta` 已经说明了“时间 + 概率”怎么做；对 priced timed models 来说，`UPPAAL CORA` 类路线说明了“时间 + 代价”怎么做；而 `FORTUNA` 解决的是三者同时出现时的 `CBMR` 问题。

- 形式主义定位：`PPTA` 模型检查平台，不是新的状态机母型。
- 构造方式简述：用 backward reachability 生成 symbolic reachability graph，再转成 `MDP` 求最大 cost-bounded reachability。
- 基础设施与场景简述：依托 multi-priced zones、`dpre/tpre`、reachability graph 和 `MDP` 分析，服务带概率失效、代价预算和时间窗口的协议与调度模型。

```text
PPTA model -> multi-priced zones -> backward reachability graph -> induced MDP -> CBMR upper bound / exact probability
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. priced probabilistic timed automata；
2. accumulated-cost semantics；
3. cost-bounded maximal reachability (`CBMR`)；
4. `dpre / tpre` predecessor operations；
5. backward symbolic exploration with multi-priced zones。

### 核心抽象

论文直接给出 `PPTA` 元组：

$$
A = (L, l_{init}, X, inv, edges, \$)
$$

上式中的符号逐项解释如下：

1. `$L$` 是 location 集合。
2. `$l_{init}$` 是初始 location。
3. `$X$` 是有限时钟集合。
4. `$inv : L \to Guards(X)$` 为每个 location 指定不变式。
5. `$edges \subseteq L \times Guards(X) \times Dist(2^X \times \mathbb N \times L)$` 是边集合。
6. `$\$ : L \to \mathbb N$` 给每个 location 指定单位时间 cost-rate。

其中边上的概率分布是 `PPTA` 的关键扩展：

$$
edges \subseteq L \times Guards(X) \times Dist(2^X \times \mathbb N \times L)
$$

上式中的符号逐项解释如下：

1. `$2^X$` 是 reset 时钟集合。
2. `$\mathbb N$` 这一项表示瞬时 cost increment。
3. `$L$` 中的目标 location 表示离散跳转去向。
4. 因此一次 probabilistic effect 同时决定 reset、离散代价和目标位置。

论文给出 `PPTA` 语义：

$$
[A] = (S, s_{init}, T)
$$

其中状态写成：

$$
S = \{(l,v,c) \mid l \in L \land v \models inv(l) \land c \in \mathbb R\}
$$

上式中的符号逐项解释如下：

1. `$l$` 是当前位置。
2. `$v$` 是时钟赋值。
3. `$c$` 是到当前为止累计的 cost。
4. 状态因此同时记住“在哪、时钟到哪、花了多少”。

### 一个最小例子与通俗解释

论文中的 production-plant 例子很直观：

1. 工厂一开始在 `startup/idle`。
2. 调度器可决定何时启动生产。
3. 生产持续 `1` 天，成功概率 `0.7`，失败概率 `0.3`。
4. 成功后进入存储，失败则需要清洗后重试。
5. 同时要满足客户在 `4` 天后取货、总 cost 不超过预算。

通俗地说，普通 `Timed Automata` 只能回答“赶不赶得上”，`PTA` 再往前一步能回答“赶上的概率有多大”，而 `PPTA` 还进一步问“在预算不超支的前提下，最大成功概率是多少”。`FORTUNA` 的任务就是把这个三目标 trade-off 算出来。

### 运行 / 接受 / 转移语义

论文给出的 `CBMR` 定义可整理为：

$$
\mathrm{CBMR} = \sup \mathrm{ProbReach}_{[A]}(\zeta_{goal})
$$

其中目标集可写成：

$$
\zeta_{goal} = \{l_{goal}\} \times \mathbb R^{|X|}_{\ge 0} \times [0, cbound]
$$

上式中的符号逐项解释如下：

1. `$l_{goal}$` 是目标 location。
2. `$\mathbb R^{|X|}_{\ge 0}$` 表示任意非负时钟赋值。
3. `$[0,cbound]$` 限定累计代价不能超过给定上界。
4. `$\sup \mathrm{ProbReach}$` 表示在所有 policy 下的最大可达概率。

论文还直接给出了 predecessor 操作：

$$
dpre_e^f(Z) = \{(l,v,c)\in S \mid v \models g \land (l', v[R:=0], c+h)\in Z\}
$$

$$
tpre(Z) = \{s\in S \mid \exists d>0,\ \exists r\in Z.\ s \xrightarrow{d} r\}
$$

上式中的符号逐项解释如下：

1. `$e=(l,g,p)$` 是一条边。
2. `$f=(R,h,l')$` 是该边上某个 instantaneous effect。
3. `$R$` 是 reset 时钟集合。
4. `$h$` 是离散 cost increment。
5. `$l'$` 是目标 location。
6. `$dpre$` 找的是“离散跳转前”的前驱状态，`$tpre$` 找的是“时间流逝前”的前驱状态。

### 语义边界

1. 论文明确说明一般 `PPTA` 上的 `CBMR` 不可判定。
2. `FORTUNA` 给出的是 semi-algorithm；随着 `maxlength` 增加，结果形成单调不减并收敛到上界的概率序列。
3. 其 symbolic backbone 是 multi-priced zones，因此依赖 convex-polyhedral 风格的代价与时钟表示。
4. 重点性质是 cost-bounded maximal reachability，而不是完整时序逻辑宇宙。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PPTA` 元组 | `$A=(L,l_{init},X,inv,edges,\$)$` | 同时含时间、概率与 cost-rate 的核心对象。 |
| 语义状态 | `$(l,v,c)$` | location、时钟赋值和累计代价三元组。 |
| `CBMR` | `$\sup \mathrm{ProbReach}_{[A]}(\zeta_{goal})$` | 预算约束下的最大可达概率。 |
| 离散前驱 | `$dpre_e^f(Z)$` | backward reachability 的离散步。 |
| 时间前驱 | `$tpre(Z)$` | backward reachability 的延时步。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `PPTA` 以 location-based timed-state 为核心。 |
| 事件 / 触发 | 中等支持 | 通过 guards 与边触发体现。 |
| 守卫 / 数据 | 强支持 | clock guards、resets 与 cost increments 都是一等对象。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 中等到强 | 论文案例支持并行 `PPTA`。 |
| 时间约束 | 很强 | 实时时钟与 invariants 是本体核心。 |
| 连续动态 / 随机性 | 随机性强，连续动态不支持 | 支持离散概率，不是混成连续动力学。 |
| 可执行 / 可验证性 | 很强 | 目标就是对 `CBMR` 做模型检查。 |

### 形式化问题与性质

1. `FORTUNA` 的核心问题是“代价受限下最大可达概率”，不是普通 reachability。
2. 其价值在于把 `PTA` 与 priced timed models 这两条线真正合并。
3. 它也说明 `PPTA` 后端往往不得不依赖近似收敛式算法，而不总是一次性精确求解。

## 构造方式与承载格式

### 建模入口

典型建模入口是：

1. location、clock、invariant；
2. 带 guard 的 edges；
3. 每条边上对 `reset-set / cost increment / destination` 的概率分布；
4. 目标 location 与 cost-bound。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `PPTA` graph；
2. multi-priced zones；
3. backward reachability graph；
4. 由 reachability graph 诱导的 `MDP`。

### 交换与互操作

这篇论文没有统一外部 interchange standard，互操作重点在分析链路：

1. `PPTA` 先被压成 multi-priced zones；
2. reachability graph 再转成 `MDP`；
3. 最终用现成 `MDP` techniques 求最大 reachability probability。

## 配套基础设施

- 建模/编辑工具：原文核心是 `FORTUNA` 检查器，本身未详细展开独立图形前端。
- 解析/交换/元模型支持：输入对象是 `PPTA`；内部用 multi-priced zones 和 reachability graph。
- 仿真/执行支持：重点是 symbolic backward exploration，不是 runtime simulation。
- 验证/分析支持：`CBMR`、predecessor operations、intersection optimization、reachability-graph-to-`MDP` analysis。
- 代码生成/转换支持：原文未涉及。
- 标准化或社区生态：它更像一条研究型 quantitative backend 路线，而不是通用标准。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 带失败概率和资源预算的协议分析；
2. 带成本与超时权衡的嵌入式调度；
3. 需要同时考虑时间、成功率和代价的设计空间比较。

### 需求前提

1. 系统需自然落成 `PPTA`。
2. 代价语义最好可写成 location cost-rate 与离散 cost increment。
3. 目标性质主要是 reachability，而不是高度复杂的嵌套时序逻辑。

### 不适用或高成本场景

如果系统需要一般连续概率分布、复杂混成动力学或超出 `CBMR` 范式的 rich properties，这条路线就不是最自然的首选。

## 与相邻形式主义的关系

相对 [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)，`mcpta` 处理的是 `PTA` 且重点在 `Modest -> PRISM` 桥；`FORTUNA` 则显式补上了 cost 维度。相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，`PRISM 4.0` 把 `PTA/PPTA` 整合成综合平台，而 `FORTUNA` 是更早、更聚焦 `CBMR` 的专用 `PPTA` 工具线。相对 [difference-decision-diagrams/desc.md](../difference-decision-diagrams/desc.md)，`DDD` 是差分约束表示层，而 `FORTUNA` 是完整概率实时验证后端。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明如果未来 `project_1` 需要把控制状态机接入“时间 + 概率 + 代价”的验证闭环，单纯 `TA` 已不够。
2. 对需求建模来说，`cost-bound` 这种资源约束很接近工业控制中的能耗、预算、重试成本和 QoS 上限。
3. 也提醒我们 quantitative backends 的目标对象往往不是前端状态图，而是更细化的 timed-probabilistic intermediate model。

### 作为目标形式主义还是中间表示

更像验证侧目标形式主义和 backend platform，不是业务建模前端。

### 对需求到模型生成的启发

1. 非形式化需求里的“概率成功率”“超时时间”“资源成本”应尽量分离成独立字段，再组合进 `PPTA`。
2. 若要让 LLM 自动建模进入 quantitative verification，生成层最好显式区分 guard、reset、cost-rate 和 probabilistic effects。
3. `CBMR` 这种目标也很适合作为后续 `project_2 / project_3` 的性质模板。

### 现实限制

`FORTUNA` 的核心优势是三因素联合，但这也带来一般不可判定性；因此它更适合研究型验证与有明确 reachability 目标的分析，不应被误解为“万能概率实时平台”。

## 重要的相关工作

1. [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)：`PTA` 的 `Modest -> PRISM` bridge。
2. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：后续更综合的概率实时平台。
3. [uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md](../uppaal-smc-statistical-model-checking-for-priced-timed-automata/desc.md)：另一条 priced timed quantitative analysis 路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Priced Probabilistic Timed Automata / PPTA / FORTUNA`
- 归类理由：论文主贡献是 `PPTA` 模型检查平台与 `CBMR` 分析基础设施，不是新的状态机本体。

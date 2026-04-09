# 用非凸近似高效分析时间自动机 / Using non-convex approximations for efficient analysis of timed automata

## 基本信息

- 标题：Using non-convex approximations for efficient analysis of timed automata
- 中文标题：用非凸近似高效分析时间自动机
- 作者：Frédéric Herbreteau，Dileep Kini，B. Srivathsan，Igor Walukiewicz
- 发表：*Foundations of Software Technology and Theoretical Computer Science (FSTTCS 2011)*，`LIPIcs 13`，pp. 78-89，2011
- DOI：`10.4230/LIPIcs.FSTTCS.2011.78`
- 链接：https://doi.org/10.4230/LIPIcs.FSTTCS.2011.78
- 形式主义：`Timed Automata / zone graph / non-convex closure abstraction`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：non-convex closure-based timed-automata reachability backend with on-the-fly thresholds
- 工具/实现获取方式：原文以原型实现与 benchmark 为主，没有给独立 GUI 工具入口；但明确面向 `UPPAAL/RED` 风格的 zone-based backend，且实验可与这些工具线对照。
- 标准/格式获取方式：承载对象是 `Timed Automata`、zones、distance graphs、`DBM`、region closure 与 `LU` approximation；不是新的交换标准。

## 简报

这篇论文解决的是 timed-automata backend 里一个很“底层但关键”的问题：我们都知道区域闭包 `closure` 比很多常见 convex extrapolation 更精确，但它往往是非凸的，工程上不好直接存。本文的思路不是继续把抽象强行压回单个 convex zone，而是直接问“能不能在不显式存 closure 的情况下，高效判断一个 zone 是否已经包含在另一个 zone 的 closure 里”。

- 形式主义定位：`Timed Automata` reachability 的验证后端方法，不是新的时间自动机母型。
- 构造方式简述：保持标准 zone graph 前向搜索，但把“节点里存的是近似 zone”改成“节点里存原始 zone，只在覆盖测试时判断是否被另一节点的 non-convex closure 吸收”。
- 基础设施与场景简述：依托 zones、distance graphs、`DBM`、`region closure`、`LU` bounds 与 on-the-fly threshold computation，服务 `TA` reachability search 的剪枝和加速。

```text
timed automaton -> unapproximated zone graph exploration -> inclusion test Z ⊆ Closure(Z') -> on-the-fly thresholds -> smaller reachable graph
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Timed Automata`；
2. zones 与 zone graph；
3. region closure abstraction；
4. zone-in-closure inclusion test；
5. `LU`-style thresholds 的按需计算。

### 核心抽象

论文依赖的 `Timed Automata` 骨架可保守写成：

$$
A = (Q, q_0, X, T, Acc)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限离散状态集合。
2. `q_0` 是初始状态。
3. `X` 是时钟集合。
4. `T` 是形如 `(q,g,R,q')` 的迁移集合，其中 `g` 是时钟约束、`R` 是 reset 集。
5. `Acc` 是目标或接受状态集合。

zone graph 的后继关系可写成：

$$
(q, Z) \xrightarrow{t} (q', Z') \quad \text{with} \quad Z' = [R](\overrightarrow{Z \cap g})
$$

上式中的符号逐项解释如下：

1. `Z` 是当前 zone。
2. `t=(q,g,R,q')` 是一条 automaton transition。
3. `Z \cap g` 表示当前 valuations 满足 guard 的部分。
4. `\overrightarrow{(\cdot)}` 表示时间流逝闭包。
5. `[R](\cdot)` 表示对 reset 集 `R` 中的时钟赋值为 `0`。

论文真正要启用的非凸对象是 region closure：

$$
\mathrm{Closure}_\alpha(S) = \bigcup \{\, R \in \mathcal{R}_\alpha \mid R \cap S \neq \emptyset \,\}
$$

上式中的符号逐项解释如下：

1. `S` 是 valuation 集或 zone。
2. `\mathcal{R}_\alpha` 是由阈值参数 `\alpha` 诱导出的 region family。
3. 若某个 region 与 `S` 有交，就整块并入 closure。
4. 这一步解释了为什么结果通常是 non-convex。

因此搜索时真正关键的覆盖判定变成：

$$
Z \subseteq \mathrm{Closure}_\alpha(Z')
$$

上式中的符号逐项解释如下：

1. `Z` 是当前待探索 zone。
2. `Z'` 是某个已访问节点上的 zone。
3. 若包含成立，则当前节点可被已有节点覆盖，无需继续展开。

### 一个最小例子与通俗解释

可以把论文的思想想成二维平面上的时钟区域：

1. 一个 zone 也许只覆盖平面上的一小块凸区域。
2. 但从 region 等价角度看，和它相交的若干小 region 合起来可能形成一个非凸集合。
3. 传统做法常把这件事重新压成更粗的 convex zone。
4. 本文改成“我不显式存这个非凸集合，但我能快速判断另一个 zone 是否已经被它吸收”。

通俗地说，作者不是在发明更复杂的图形对象，而是在发明“如何不把对象真正画出来，也知道它已经够用了”的检测方法。

### 运行 / 接受 / 转移语义

论文关注的是 reachability，因此运行语义重点就是 abstract search 的 soundness：

$$
A \text{ has an accepting run } \iff \text{ some accepting node is reachable in } SG_\alpha(A)
$$

上式中的符号逐项解释如下：

1. `SG_\alpha(A)` 是在 region closure 抽象下得到的 symbolic graph。
2. 只要抽象图里到达接受节点，原 automaton 就存在接受运行。
3. 论文的改进在于让这个抽象图不必显式存储非凸 closure。

工程上最重要的结论之一，是可把 inclusion test 保持在和普通 zone comparison 接近的复杂度级别，依然依托 distance graphs / `DBM` 做高效判定。

### 语义边界

1. 论文主线是 reachability，不是更一般的 `TCTL` 或 timed-liveness。
2. 对象是标准 `Timed Automata` backend，而不是带数据、博弈或概率扩展的 richer model。
3. 关键收益在 non-convex abstraction 和 threshold handling，不在前端建模语言。
4. 本文是 prototype / backend route，不是统一 timed-verification 平台介绍。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TA` 骨架 | `$A = (Q, q_0, X, T, Acc)$` | 讨论始终建立在标准时间自动机上。 |
| zone 后继 | `$Z' = [R](\overrightarrow{Z \cap g})$` | 仍以标准 zone graph 为基础。 |
| closure 抽象 | `$\mathrm{Closure}_\alpha(S)=\bigcup\{R \in \mathcal R_\alpha \mid R \cap S \neq \emptyset\}$` | region closure 是非凸近似的来源。 |
| 覆盖判定 | `$Z \subseteq \mathrm{Closure}_\alpha(Z')$` | 搜索树剪枝的核心测试。 |
| on-the-fly 阈值 | `$\alpha$` not fixed globally | 允许只根据当前可达部分动态收紧 thresholds。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接处理 `Timed Automata` 控制状态与 zone 节点。 |
| 事件 / 触发 | 中等支持 | 迁移标签不关键，重点在 guard / reset 语义。 |
| 守卫 / 数据 | 中等支持 | 以 clocks 与 guards 为主，不涉及富离散数据。 |
| 层次 | 不支持 | 不处理 hierarchy。 |
| 并发 / 同步 | 条件支持 | 可用于 automata network，但本文不是并发建模论文。 |
| 时间约束 | 很强 | 全文核心就是时钟、zones 与 region closure。 |
| 连续动态 / 随机性 | 不支持 | 不涉及 hybrid / probabilistic semantics。 |
| 可执行 / 可验证性 | 很强 | inclusion test、threshold 计算与 benchmark 都面向实际实现。 |

## 构造方式与承载格式

### 建模入口

原文的典型入口包括：

1. 标准 `Timed Automata`；
2. zone graph exploration；
3. `LU`-style threshold information；
4. closure-based inclusion checking。

### 机器可处理承载方式

机器可处理承载方式包括：

1. zones；
2. distance graphs；
3. `DBM`；
4. region-closure induced inclusion tests。

### 交换与互操作

本文的互操作重点很明确：

1. 前端仍然是普通 `TA`。
2. 后端可嵌入 `UPPAAL/RED` 风格的 zone-based workflow。
3. 相比显式存非凸集合，它选择只在覆盖测试时按需计算逻辑条件。

## 配套基础设施

- 建模/编辑工具：原文不提供新的建模器，默认前端 `TA` 已由外部工具给出。
- 解析/交换/元模型支持：核心承载是 zones、distance graphs 与 `DBM`，不是新的 exchange format。
- 仿真/执行支持：主线不是 simulation，而是 symbolic reachability。
- 验证/分析支持：zone graph、closure-based pruning、on-the-fly thresholds、prototype benchmarks。
- 代码生成/转换支持：不主打代码生成；唯一重要“转换”是从显式近似节点转成 closure-based inclusion workflow。
- 标准化或社区生态：方法直接对接 `UPPAAL/RED` 一类 timed-verification backend。

## 适用场景与需求前提

### 适用场景

适合已把系统建成 `Timed Automata`，并希望在 zone-based reachability 里减少节点数、同时避免把更精细的抽象重新压回粗凸近似的场景。

### 需求前提

1. 系统必须能落成标准 `Timed Automata`。
2. 关注点主要是 reachability backend 的效率与剪枝质量。
3. 工具链愿意接受 non-convex abstraction 只在逻辑层显式存在。

### 不适用或高成本场景

如果目标是 richer timed-data models、timed-liveness、或跨多个理论域的一体化验证平台，这篇论文补的只是 backend 一层，不足以单独支撑全部工作流。

## 与相邻形式主义的关系

相对 [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)，本文更强调直接使用 non-convex closure 与动态 thresholds，而后者更系统地整理了 `a4LU` 一类最粗 `LU` 抽象；相对 [fast-algorithms-for-handling-diagonal-constraints-in-timed-automata/desc.md](../fast-algorithms-for-handling-diagonal-constraints-in-timed-automata/desc.md)，那里补的是 diagonal constraints backend，这里补的是 closure / non-convex approximation backend；相对 [tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md](../tarzan-a-region-based-library-for-forward-and-backward-reachability-of-timed-automata/desc.md)，`Tarzan` 强调 region-based library，而本文仍立足 zone workflow。

## 与本研究的关系

### 对 Project 1 的价值

它直接告诉我们：一旦 `project_1` 未来输出到 `Timed Automata`，验证闭环的工程瓶颈常常不在语言定义，而在 backend abstraction 怎样既 sound 又不至于爆炸。

### 作为目标形式主义还是中间表示

它不是目标形式主义，而是目标形式主义落地后的验证后端优化路线。

### 对需求到模型生成的启发

1. 前端建模时是否能减少无关 clocks / constants，会直接影响 closure 质量。
2. 如果需求最终会进入 timed verification，最好尽早考虑阈值与 guard 分布。
3. “模型能表示”与“模型能高效验证”之间并不等价，backend 证据需要单独收集。

### 现实限制

本文没有处理离散数据、博弈、概率或 richer timed updates。

## 重要的相关工作

### 奠基或前身工作

1. [uppaal-in-a-nutshell/desc.md](../uppaal-in-a-nutshell/desc.md)：经典 zone-based `Timed Automata` 平台入口。
2. region / zone abstraction 主线：本文明确站在这条 timed backend 传统上继续推进。

### 同类型或同家族工作

1. [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)：`LU` abstraction 主线。
2. [fast-algorithms-for-handling-diagonal-constraints-in-timed-automata/desc.md](../fast-algorithms-for-handling-diagonal-constraints-in-timed-automata/desc.md)：timed backend 的另一条细化路线。

### 标准 / 格式 / 工具链工作

1. `UPPAAL`、`RED`：本文明确把自己的方法与这些主流工具线对照。

### 与本研究关系最紧的工作

1. [configurable-verification-of-timed-automata-with-discrete-variables/desc.md](../configurable-verification-of-timed-automata-with-discrete-variables/desc.md)：继续把 timed backend 扩展到 discrete variables 和 configurable abstraction。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / zone graph / non-convex closure abstraction`
- 论文角色：non-convex closure-based timed-automata reachability backend with on-the-fly thresholds
- 核心功能：在不显式存储 non-convex closure 的前提下，对 zone graph 做更强覆盖检测与 reachability 剪枝
- 关键特性：region closure、zone-in-closure inclusion、`DBM` / distance graphs、on-the-fly thresholds、prototype benchmarks
- 构造方式：`TA -> unapproximated zones -> inclusion test Z ⊆ Closure(Z') -> threshold refinement`
- 基础设施：zones、distance graphs、`DBM`、`UPPAAL/RED` 风格 timed backend
- 适用场景：`TA` reachability、需要减少 symbolic node 数量的实时验证后端
- 需求前提：系统已建成标准 `Timed Automata`，且团队关注的是 backend 剪枝效率
- 状态：🟢 直接可用

# 带不完美信息的下推模块检验 / Pushdown Module Checking with Imperfect Information

## 基本信息

- 标题：Pushdown Module Checking with Imperfect Information
- 中文标题：带不完美信息的下推模块检验
- 作者：Benjamin Aminof, Aniello Murano, Moshe Y. Vardi
- 发表：*Concurrency Theory*, `LNCS 4703`, pp. 460-475, 2007
- DOI：`10.1007/978-3-540-74407-8_31`
- 链接：https://people.na.infn.it/~murano/pubblicazioni/Revisited-PD-MC-full.pdf
- 形式主义：`Open Pushdown Systems (OPD)` 上的 imperfect-information 扩展
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / conference origin
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 visibility-aware `OPD` tuple、visible part `vis`、induced module `M_S`、`CTL` imperfect-information pruning semantics 与 semi-alternating pushdown tree automata reduction。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 visible/invisible control variables、visible/invisible stack variables、`vis((q,\alpha))` 以及基于可见信息的 environment pruning。

## 简报

这篇 `CONCUR 2007` 论文真正补到树上的，不只是“partial observation 下会更难”这条复杂度结论，而是把 `OPD` 本体继续推进成了**带可见性分层的 open recursive state machine**。环境不再知道完整 configuration，而只能看到控制状态和栈内容的可见部分；同时，论文明确指出：一旦把 stack 也部分隐藏，`CTL` module checking 会立刻掉进不可判定边界。对当前演化树来说，这正是 `Open Pushdown Systems` 下面最自然、也最经典的 imperfect-information 子枝。

- 形式主义定位：`OPD` 的 imperfect-information 扩展，也是 open recursive hierarchy 首次引入 partial observation 的经典条目。
- 构造方式简述：在 `OPD` 的 control states 与 stack symbols 上分别切分 visible / invisible 变量，环境只能基于 `vis((q,\alpha))` 观察 configuration 并进行 pruning。
- 基础设施与场景简述：会议版聚焦 `CTL`；它已经给出 general undecidability、visible-store decidability 与 automata-theoretic proof skeleton，因此足够作为新子节点 conference origin。

```text
open pushdown system -> visible / invisible control + stack variables -> partial-observation pruning -> CTL module checking with imperfect information
```

## 形式主义定义与核心对象

### 定义对象

论文处理的不是一般 finite-state imperfect-information modules，而是**带无界栈的开放式 partial-observation 系统**。它要求环境既能在 environment configurations 上删分支，又只能根据 configuration 的可见部分做决定。

### 核心抽象

原文把一个 visibility-aware `OPD` 写成：

$$
S = \langle AP, Q, q_0, \Gamma, \gamma_b, \delta, \mu, Env \rangle
$$

上式中的符号逐项解释如下：

1. `AP` 是原子命题集合。
2. `Q` 是控制状态集合，`q_0 \in Q` 是初始控制状态。
3. `Q \subseteq 2^{I \cup H}`，其中 `I` 与 `H` 分别是 visible / invisible control variables。
4. `\Gamma` 是栈字母表，另有底符号 `\gamma_b \notin \Gamma`。
5. `\Gamma \subseteq 2^{I_\Gamma \cup H_\Gamma}`，其中 `I_\Gamma` 与 `H_\Gamma` 分别是 visible / invisible stack variables。
6. `\delta` 是 pushdown transition relation。
7. `\mu` 是 labeling function。
8. `Env` 指出 environment configurations。

论文把 configuration 的可见部分定义成：

$$
vis((q,\alpha)) = (vis(q), vis(\alpha))
$$

其中 `vis(q)` 只保留控制状态中的可见变量，`vis(\alpha)` 只保留栈串中的可见部分；若某个 pushed symbol 只含 invisible 变量，则环境甚至看不到这次 push，只能感知到“无可见新增信息”。

### 一个最小例子与通俗解释

论文导言给出的直觉例子是自动取款机：

1. 当前 ATM 允许插卡、取现、退卡，并可能在每次操作后压入若干“待展示广告”。
2. 用户能观察到界面和部分 control state，但看不到机器内部是否缺纸，也看不到内部广告栈里究竟压了哪些 invisible symbol。
3. 环境因此只能依据可见部分判断下一步是否继续剪枝，而无法获知完整 stack content。

通俗地说，这个 family 像“环境戴着部分遮挡眼镜在观察 `OPD`”。如果把遮挡扩展到 stack content，很多原本可判定的性质会直接失控。

### 运行 / 接受 / 转移语义

一个 configuration 仍形如：

$$
(q,\alpha)
$$

论文要求 environment configurations 的指定必须与可见性一致：若两个 configurations 的可见部分相同，则它们要么都属于 `Env`，要么都不属于 `Env`。诱导 module 仍记作：

$$
M_S = \langle AP, W_s, W_e, w_0, R, L, \approx \rangle
$$

其中环境的 observation equivalence 满足：

$$
w \approx w' \iff vis(w) = vis(w')
$$

于是 module checking 关注的不再是任意 pruning，而是**只允许根据可见等价类做一致 pruning** 的执行树族。

### 语义边界

这个子类的边界如下：

1. 它保留 `OPD` 的 open recursive skeleton。
2. 新增点在于 visibility partition，而不是新的 stack 操作。
3. 只要 stack 也可部分隐藏，`CTL` 已经不可判定。
4. 若 stack 完全可见、只隐藏 control states，则又回到可判定边界。

### 关键性质与判定边界

会议版最重要的结论是：

$$
\mathrm{PMC}_{\mathrm{II}}(OPD, CTL) \text{ is undecidable}
$$

并且即使控制状态完全可见，只要 stack 仍能隐藏，原文也证明：

$$
\mathrm{PMC}_{\mathrm{stack\text{-}hidden}}(OPD, CTL) \text{ is undecidable}
$$

另一方面，若 stack 完全可见、只隐藏 control states，则复杂度回落到：

$$
\mathrm{PMC}_{\mathrm{ctrl\text{-}hidden,\ stack\text{-}visible}}(OPD, CTL)
\text{ is } 2\mathrm{EXPTIME}\text{-complete}
$$

这正是当前树上值得单独命名一个子节点的原因：不是一般的“open pushdown + more theorems”，而是 visibility pattern 本身已经切开了 decidable / undecidable family boundary。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | control state、stack content、environment partition 仍然完整保留。 |
| 事件 / 触发 | 强支持 | push/pop/rewrite 规则继续决定配置演化。 |
| 守卫 / 数据 | 弱支持 | 核心不在复杂数据更新，而在可见性切分。 |
| 层次 | 强支持 | pushdown recursion 仍是模型骨架。 |
| 并发 / 同步 | 不支持 | sequential open recursion。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可观测性 / 信息模式 | 强支持 | visible / invisible control 和 stack variables 是本条目的核心新增点。 |
| 可执行 / 可验证性 | 强理论支持 | undecidability boundary 与 visible-store decidability 都直接建立在模型本体上。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| visibility-aware `OPD` | `$S = \langle AP, Q, q_0, \Gamma, \gamma_b, \delta, \mu, Env \rangle$` | open pushdown skeleton 上加入 visibility partition。 |
| 可见部分 | `$vis((q,\alpha)) = (vis(q), vis(\alpha))$` | environment observation 的定义核心。 |
| 观测等价 | `$w \approx w' \iff vis(w) = vis(w')$` | pruning 必须与 observation 一致。 |
| general case | `$\mathrm{PMC}_{\mathrm{II}}(OPD, CTL)$ undecidable` | stack-hidden imperfect information 的主边界。 |
| visible-store case | `$\mathrm{PMC}_{\mathrm{ctrl\text{-}hidden,\ stack\text{-}visible}}(OPD, CTL)$ is $2\mathrm{EXPTIME}$-complete` | 可判定子类。 |

## 构造方式与承载格式

### 建模入口

1. 先按 `OPD` 一样定义 control states、stack alphabet 与 pushdown 规则。
2. 再把 control variables 与 stack variables 切成 visible / invisible 两组。
3. 用 `vis` 函数定义环境能看见什么。
4. 最后要求 environment pruning 只能依据 observation equivalence 执行。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. visibility-aware `OPD` tuple；
2. `vis` observation function；
3. induced module `M_S` 与 observation equivalence；
4. semi-alternating pushdown tree automata；
5. `CTL` imperfect-information module-checking reductions。

### 交换与互操作

它与当前文库中的关系如下：

1. 向上承接 [pushdown-module-checking-lpar/desc.md](../pushdown-module-checking-lpar/desc.md) 与 [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md) 的 `OPD` 母线。
2. 向后续 journal full version 推进到 [pushdown-module-checking-with-imperfect-information-iandc/desc.md](../pushdown-module-checking-with-imperfect-information-iandc/desc.md)。
3. 在 tree 上，它把 open recursive hierarchy 明确切成 perfect-information 与 imperfect-information 两条子线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 visibility-aware `OPD` tuple 与 `vis`。
- 仿真/执行支持：可按 partial-observation induced module 解释执行树。
- 验证/分析支持：`CTL` imperfect-information module checking、semi-alternating pushdown tree automata reduction。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，连接 partial-observation verification、pushdown systems 与 module checking。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归 open systems 中环境只能看到 configuration 一部分的场景。
2. 需要研究“隐藏 stack information 是否会打破可判定性”的 family boundary。
3. 想把 `OPD` 支线继续扩成 partial-observation recursive hierarchy。

### 需求前提

1. 系统复杂度来自递归与开放环境，而不是并发或时间。
2. 观察受限可以自然表示成 visible / invisible variable partition。
3. 关注的是 branching-time open semantics 与环境观测能力。

### 不适用或高成本场景

如果环境具有完全信息，则 plain `OPD` 即可；如果需要 `CTL^*` 或 `$\mu$-calculus` 的完整口径，应看后续 full version；如果系统没有 recursion，则 finite imperfect-information module 更轻。

## 与相邻形式主义的关系

相对 `OPD` 母模型，它加入了 observation equivalence；相对 finite-state imperfect-information module，它又叠加了 pushdown recursion；相对后续 journal full version，这篇会议版主要固定 `CTL` 下的 family boundary，而未把 `CTL^* / $\mu$-calculus` 全部收束进去。

## 与本研究的关系

### 对 Project 1 的价值

它让演化树中的 open recursive branch 不再只有“是否开放”这一维，而是继续长出了“环境看得见多少”的可观测性维度。

### 对状态机自动建模的启发

如果需求里出现“环境只能看到部分模式 / 部分栈上下文”的设定，那么自动建模不能只停在 `OPD`，必须进一步判断是否需要 partial-observation open pushdown family。

### 现实限制

它是高理论密度 family，没有工程建模语言与工业工具承载。

## 重要的相关工作

### 奠基或前身工作

- [pushdown-module-checking-lpar/desc.md](../pushdown-module-checking-lpar/desc.md)
- [pushdown-module-checking/desc.md](../pushdown-module-checking/desc.md)

### 同类型或同家族工作

- [program-complexity-in-hierarchical-module-checking/desc.md](../program-complexity-in-hierarchical-module-checking/desc.md)
- [pushdown-module-checking-with-imperfect-information-iandc/desc.md](../pushdown-module-checking-with-imperfect-information-iandc/desc.md)：统一 `CTL / CTL^* / $\mu$-calculus` 的 journal full version。

## 文献分类总结

- 这篇论文在 `OPD` 下面首次稳定补出了 imperfect-information 子枝。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL、应用案例或单纯复杂度证明。
- 在当前演化树里，它最适合挂到 `Statecharts -> HSM -> Open Hierarchical Modules -> Open Pushdown Systems / Pushdown Module Checking -> Imperfect-Information OPD`，并作为该子节点的 2007 conference origin。

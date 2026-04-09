# 下推定时自动机可达性的快速区域算法 / Fast Zone-Based Algorithms for Reachability in Pushdown Timed Automata

## 基本信息

- 标题：Fast zone-based algorithms for reachability in pushdown timed automata
- 中文标题：下推定时自动机可达性的快速区域算法
- 作者：S. Akshay，Paul Gastin，Karthik R. Prakash
- 发表：*Computer Aided Verification*，LNCS 12759，pp. 619-642，2021
- DOI：`10.1007/978-3-030-81685-8_30`
- 链接：https://doi.org/10.1007/978-3-030-81685-8_30
- 形式主义：`Pushdown Timed Automata / zone-based reachability / TChecker`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：first terminating, sound and complete zone-based reachability algorithm for `PDTA`
- 工具/实现获取方式：原文明确说明算法已在 `TChecker` 上实现，并给出 prototype 仓库与 benchmark 数据入口。
- 标准/格式获取方式：主承载对象是 `PDTA`、zones、simulation / equivalence 关系以及基于归纳规则的 fixed-point algorithm；它不是通用交换标准。

## 简报

这篇论文补的是 `Timed Automata + stack` 这条线里非常关键的一步。过去 `PDTA` 的可达性虽然可判定，但实现多半停留在 region 或更重的理论构造上，难以做出真正好用的工具。本文的贡献在于证明“把普通定时自动机的 zone 算法直接搬到 `PDTA` 上会出错”，然后重新设计一套带栈规则、终止、健全、完备的 zone-based fixed-point 算法，并落地到 `TChecker`。

- 形式主义定位：围绕 `PDTA` 可达性的 zone-based 方法路线，而不是新的 `PDTA` 变体定义。
- 构造方式简述：把 timed-automata zone reachability 重写为归纳规则，再增加 push/pop 专用规则，并用 simulation 与 equivalence 的组合保证终止和正确性。
- 基础设施与场景简述：依托 `PDTA`、zones、subsumption、equivalence、least fixed point 与 `TChecker`，服务递归实时系统的控制状态可达性验证。

```text
pushdown timed model -> inductive zone rules -> saturated finite abstraction -> TChecker implementation -> well-nested reachability result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. timed automata。
2. pushdown timed automata (`PDTA`)。
3. zones 与 zone graph。
4. simulation / subsumption 与 equivalence 关系。
5. 基于归纳规则的 fixed-point computation。

### 核心抽象

论文先回顾 timed automaton：

$$
A = (Q,X,q_0,\Delta,F)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `X` 是 clocks 集合。
3. `q_0` 是初始状态。
4. `\Delta` 是带 guard 与 reset 的转移集合。
5. `F` 是目标或接受状态集合。

本文所处理的 `PDTA` 可保守整理为：

$$
P = (Q,X,\Gamma,q_0,\Delta_{int},\Delta_{push},\Delta_{pop},F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限控制状态集合。
2. `X` 是 clocks 集合。
3. `\Gamma` 是 stack alphabet。
4. `q_0` 是初始状态。
5. `\Delta_{int}` 是内部离散迁移。
6. `\Delta_{push}` 是 push transitions。
7. `\Delta_{pop}` 是 pop transitions。
8. `F` 是目标状态集合。

zone 抽象本身可写成：

$$
Z \subseteq \mathbb R_{\ge 0}^{X}
$$

上式中的符号逐项解释如下：

1. `Z` 是由时钟约束合取定义出的估值集合。
2. `\mathbb R_{\ge 0}^{X}` 表示所有 clocks 的非负实值赋值空间。

论文的关键算法对象是有限抽象固定点，可压成：

$$
\mathcal F(I) = I \cup \mathrm{Post}_{int}(I) \cup \mathrm{Post}_{push}(I) \cup \mathrm{Post}_{pop}(I)
$$

上式中的符号逐项解释如下：

1. `I` 是当前已发现的符号状态集合。
2. `\mathrm{Post}_{int}`、`\mathrm{Post}_{push}`、`\mathrm{Post}_{pop}` 分别对应三类规则的后继扩张。
3. 算法通过反复饱和 `\mathcal F` 直到固定点，得到有限抽象。

### 一个最小例子与通俗解释

一个最小例子是“实时递归调用”：

1. 主过程在时钟满足条件时调用子过程，对应一次 push。
2. 子过程内部继续经历若干 timed transitions，zone 会随 guard 和 reset 演化。
3. 返回时执行 pop，但这一步不能像普通 timed automata 那样只看当前 zone，因为还要和栈上的调用信息配对。
4. 本文的算法正是为了解决“zone 与 stack 混在一起时怎样既不丢精度、又能终止”这个问题。

通俗地说，普通 timed automata 的 zone 算法像“在一个平面图里压缩时间状态”；`PDTA` 多了栈以后，这个平面图变成了“带括号结构的时间状态图”。直接照搬会把不该合并的路径合并掉，于是本文重新设计了带 push/pop 规则的压缩方式。

### 运行 / 接受 / 转移语义

timed automata 的基础语义是：

$$
(q,v) \xrightarrow{t} (q',v')
$$

上式中的符号逐项解释如下：

1. `q`、`q'` 是源和目标状态。
2. `v`、`v'` 是 clock valuations。
3. `t` 可以表示 delay 或 guarded discrete transition。

`PDTA` 的 well-nested control-state reachability 可保守写成：

$$
(q_0,v_0,\epsilon) \Rightarrow^\ast (q_f,v,\epsilon)
$$

上式中的符号逐项解释如下：

1. `v_0` 是把所有 clocks 置零的初始赋值。
2. `\epsilon` 表示空栈。
3. `q_f \in F` 是目标控制状态。
4. `\Rightarrow^\ast` 表示由 delay、internal、push、pop 组成的有限运行。
5. 论文关注的是起点与终点都为空栈的 well-nested reachability。

在 zone 层，算法维护的抽象后继可写成：

$$
(q,Z) \leadsto (q',Z')
$$

上式中的符号逐项解释如下：

1. `q`、`q'` 是控制状态。
2. `Z`、`Z'` 是 zones。
3. `\leadsto` 表示经过规范化后的符号后继关系，而不是原始 concrete run。

### 语义边界

1. 本文处理的是一种“栈本身不计时”的 `PDTA` 口径。
2. 目标问题是 well-nested control-state reachability，不是通用二元关系查询或游戏问题。
3. 算法的重点是 zone-based practicality，而不是更强表达力的新模型。
4. 文中也明确区分了 naive simulation 方案为何不健全。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed automaton 骨架 | `$A=(Q,X,q_0,\Delta,F)$` | `PDTA` 的时间语义基础。 |
| `PDTA` 骨架 | `$P=(Q,X,\Gamma,q_0,\Delta_{int},\Delta_{push},\Delta_{pop},F)$` | 论文方法处理的核心对象。 |
| zone | `$Z\subseteq \mathbb R_{\ge 0}^{X}$` | 符号时钟估值集合。 |
| fixed-point 扩张 | `$\mathcal F(I)=I\cup \mathrm{Post}_{int}(I)\cup \mathrm{Post}_{push}(I)\cup \mathrm{Post}_{pop}(I)$` | 归纳规则饱和的总体框架。 |
| well-nested reachability | `$(q_0,v_0,\epsilon)\Rightarrow^\ast(q_f,v,\epsilon)$` | 目标判定问题。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 结合有限控制、时钟估值与栈结构。 |
| 事件 / 触发 | 中等支持 | 主要体现为 internal / push / pop 三类迁移。 |
| 守卫 / 数据 | 强支持 | zones 直接承载 timed guards 与 resets。 |
| 层次 | 很强 | 栈表达调用返回层次。 |
| 并发 / 同步 | 弱支持 | 本文主线是顺序递归实时系统。 |
| 时间约束 | 很强 | 全文核心就是 timed reachability。 |
| 连续动态 / 随机性 | 不支持 | 不处理连续或概率扩展。 |
| 可执行 / 可验证性 | 很强 | 给出 terminating / sound / complete zone algorithm，并在 `TChecker` 实现。 |

### 形式化问题与性质

1. 论文首先证明 naive zone+simulation 方案在 `PDTA` 上不健全，这是整篇文章的理论起点。
2. 新算法的价值不只是“可判定”，而是第一次把 `PDTA` 真正带进可用的 zone-based 工具世界。
3. 通过 `TChecker` 实验，本文把 `PDTA` 从偏理论的模型往工程验证前端推进了一步。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `PDTA` 模型。
2. zones 与 clock constraints。
3. push / pop / internal transition rules。
4. fixed-point saturation 所需的 subsumption 与 equivalence 关系。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `PDTA` transition system。
2. zones。
3. rule-based symbolic states。
4. `TChecker` 内部数据结构与 benchmark 套件。

### 交换与互操作

互操作重点在于：

1. 算法直接建立在 `TChecker` 现有 timed-automata 基础设施之上。
2. 上游模型若能落成 `PDTA`，就可复用 zone engine 的既有优化。
3. 这不是独立标准格式，而是验证后端能力的扩展。

## 配套基础设施

- 建模/编辑工具：主入口是 `PDTA`/timed-automata 建模前端，正文实现依托 `TChecker`。
- 解析/交换/元模型支持：zones、simulation relation、equivalence relation 与 fixed-point data structures。
- 仿真/执行支持：主体不是执行器，而是 symbolic reachability engine。
- 验证/分析支持：well-nested control-state reachability、zone saturation、soundness / completeness proofs。
- 代码生成/转换支持：正文不主打代码生成，重点是把 `PDTA` 带入可扩展 verifier。
- 标准化或社区生态：`TChecker`、benchmark 集与 `PDTA`/timed-verification 社区构成其生态位置。

## 适用场景与需求前提

### 适用场景

适合递归实时程序、具有过程调用栈的 timed controller、实时协议处理栈以及其他需要同时保留 clocks 与 call-return 结构的验证任务。

### 需求前提

1. 系统必须存在显式递归或栈式控制流。
2. 时间约束需要以 clocks/guards/reset 形式表达。
3. 目标问题主要是 well-nested reachability，而非更复杂的开放系统语义。
4. 团队愿意把模型接到 `TChecker` 风格的 symbolic backend。

### 不适用或高成本场景

如果递归结构并不重要，普通 timed automata 就足够；如果需要 richer stack timing、博弈或参数综合，本文路线仍只是起点。

## 与相邻形式主义的关系

相对 [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)，两者都把时间和递归结合，但那篇更偏模型家族定义与复杂度边界，本文更偏 zone-based 求解方法；相对 [why-liveness-for-timed-automata-is-hard-and-what-we-can-do-about-it/desc.md](../why-liveness-for-timed-automata-is-hard-and-what-we-can-do-about-it/desc.md)，两者都说明 naive zone + subsumption 会在更复杂语义下失效，但一个面对 liveness，一个面对 stack；相对 [certifying-emptiness-of-timed-buchi-automata/desc.md](../certifying-emptiness-of-timed-buchi-automata/desc.md)，后者处理 timed-liveness 证书化，本文处理递归实时 reachability 的可实现算法。

## 与本研究的关系

### 对 Project 1 的价值

它说明若未来 `project_1` 需要支持“带过程调用或嵌套子任务的实时状态机”，后端不必退回完全扁平化；`PDTA` 路线已经开始具备可实现的 zone-based 验证基础。

### 作为目标形式主义还是中间表示

更适合作为高可信验证中间表示，而不是用户直接编辑的前端 DSL。

### 对需求到模型生成的启发

1. 对实时递归需求，生成器应尽量保留调用边界和时钟约束，而不是只产出普通状态机。
2. 若目标是可验证性，必须提前考虑 zone-level 抽象是否还能工作。
3. 时间和栈叠加后，很多“在普通 timed automata 上自然成立的优化”会失效，这对自动建模后的验证闭环很重要。

### 现实限制

本文聚焦可达性而非完整验证生态；若后续要支持 liveness、参数综合或 richer stack timing，还需要接续更多理论与工具工作。

## 重要的相关工作

### 奠基或前身工作

1. [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：定时自动机母线。
2. [recursive-timed-automata/desc.md](../recursive-timed-automata/desc.md)：时间与递归结合的模型主线。

### 同类型或同家族工作

1. `TChecker`：本文实现承载平台。
2. 论文中讨论的 region-based `PDTA` 路线。

### 标准 / 格式 / 工具链工作

1. `TChecker` 上的 zone infrastructure。
2. prototype implementation 与 benchmark 数据集。

### 与本研究关系最紧的工作

1. [why-liveness-for-timed-automata-is-hard-and-what-we-can-do-about-it/desc.md](../why-liveness-for-timed-automata-is-hard-and-what-we-can-do-about-it/desc.md)：复杂 timed semantics 下的 zone/subsumption 边界。
2. [certifying-emptiness-of-timed-buchi-automata/desc.md](../certifying-emptiness-of-timed-buchi-automata/desc.md)：timed backend 路线中的另一条结果可信化分支。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Pushdown Timed Automata / zone-based reachability / TChecker`
- 论文角色：first terminating, sound and complete zone-based reachability algorithm for `PDTA`
- 核心功能：为 `PDTA` 提供首个可终止、健全、完备的 zone-based reachability 算法并落地到 `TChecker`。
- 关键特性：inductive rules、push/pop-specific saturation、simulation+equivalence pruning、`TChecker` implementation。
- 构造方式：`PDTA` -> rule-based zone fixed point -> finite abstraction -> reachability result。
- 基础设施：zones、subsumption/equivalence、`TChecker`、prototype repo、benchmark 套件。
- 适用场景：递归实时程序、调用返回式定时控制逻辑与 stack-sensitive timed verification。
- 需求前提：系统必须同时具有 clocks 与显式栈结构，且核心问题是 well-nested reachability。
- 状态：🟢

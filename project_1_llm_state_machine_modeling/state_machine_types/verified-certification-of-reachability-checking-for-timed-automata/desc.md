# 时间自动机可达性检查的已验证认证 / Verified Certification of Reachability Checking for Timed Automata

## 基本信息

- 标题：Verified Certification of Reachability Checking for Timed Automata
- 中文标题：时间自动机可达性检查的已验证认证
- 作者：Simon Wimmer, Joshua von Mutius
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*, `LNCS 12078`, pp. 425-443, 2020
- DOI：`10.1007/978-3-030-45190-5_24`
- 链接：https://doi.org/10.1007/978-3-030-45190-5_24
- 形式主义：`Timed Automata / unreachability certificate / Isabelle-HOL certifier`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：时间自动机不可达性证书生成与已验证检查方法
- 工具/实现获取方式：论文说明使用新的未验证 `Standard ML` model checker `Mlunta` 生成证书，再由 `Isabelle/HOL` 中机械验证过的 certifier 检查；同时讨论了并行检查和证书压缩。
- 标准/格式获取方式：主承载是 timed automata、symbolic states、zones/`DBM`、覆盖关系与 explored-state certificate；它是工具间共享的证书工件，而不是行业标准交换格式。

## 简报

这篇论文的关键判断是：与其把整个时间自动机 model checker 都做成已验证实现，不如把“不可达”结论输出成一个有限证书，再用一个小得多、已验证的 certifier 去检查它。这样既能继续使用高性能的未验证搜索器和近似策略，也能把最关键的“坏状态确实不可达”结论变成可追溯、可审计的证明对象。

- 形式主义定位：`Timed Automata` reachability 的证书化验证路线，而不是新的时间自动机家族。
- 构造方式简述：`timed automaton -> symbolic zone exploration -> explored-state certificate -> verified certifier`。
- 基础设施与场景简述：依托 `Isabelle/HOL`、`Standard ML`、zones/`DBM`、近似覆盖和并行检查，适合需要提升实时系统验证结果可信度的场景。

```text
timed automaton -> zone-based search -> explored symbolic states -> certificate checking -> trustworthy unreachable result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. timed automata、clock valuations、guards、resets 和 invariants。
2. symbolic states `(location, zone)` 与 `DBM` 表示。
3. 未验证 model checker 生成的 explored-state certificate。
4. 已验证 certifier 对初始性、闭包性、非终态性和覆盖关系的检查。

### 核心抽象

论文直接把时间自动机写成“转移集合 + 不变式”的形式；可保守整理为：

$$
A = (T, I)
$$

上式中的符号逐项解释如下：

1. `$T$` 是离散转移集合，每条转移带起点、终点、guard、action 和 reset 集。
2. `$I$` 是 location 到 invariant 的映射。
3. 状态是 `(l,u)` 这样的二元组，其中 `$l$` 是 location，`$u$` 是 clock valuation。

论文给出的两类基本步语义可整理为：

$$
(l,u) \xrightarrow{d} (l, u \oplus d), \qquad (l,u) \xrightarrow{a} (l', [r:=0]u)
$$

上式中的符号逐项解释如下：

1. `$d \ge 0$` 是时间推进量。
2. `$u \oplus d$` 表示所有 clocks 同步增加 `$d$`。
3. `$a$` 是离散动作标签。
4. `$r$` 是被 reset 为 `0` 的 clocks 集合。
5. guard 和 invariant 在 delay / action 两步中都必须满足。

论文的关键工件不是反例，而是不可达性证书。可保守写成：

$$
\mathcal{C} \subseteq SymState
$$

上式中的符号逐项解释如下：

1. `$SymState$` 是 symbolic states 集合，通常是 `(l,Z)` 形式。
2. `$Z$` 是由 `DBM` 表示的 zone。
3. `$\mathcal{C}$` 是搜索器最终保留下来的 explored symbolic states 集合。

证书有效性的核心条件可压成：

$$
init \in \mathcal{C} \land \forall s \in \mathcal{C}.\ s \notin Final \land Succ(s) \subseteq \downarrow \mathcal{C}
$$

上式中的符号逐项解释如下：

1. `$init$` 是初始 symbolic state。
2. `$Final$` 是违反 safety property 的目标坏状态集合。
3. `$Succ(s)$` 是从 `$s$` 一步可达的所有 symbolic successors。
4. `$\downarrow \mathcal{C}$` 表示被证书中某个状态覆盖的状态集合。
5. 如果初始状态在证书内、证书中没有终态、且所有后继都被证书覆盖，那么坏状态不可达。

### 一个最小例子与通俗解释

论文的直觉非常直接：

1. model checker 先按常规方式搜索 zone graph。
2. 当它判断“找不到更多新状态”时，把已探索的 symbolic states 当作证书输出。
3. certifier 不重跑整个搜索，而只检查三件事：初始状态是否在证书里、证书里有没有坏状态、每个证书状态的后继是否都被证书覆盖。
4. 若这三件事成立，则“不可达”结论可信。

通俗地说，这像是把“搜索过程”换成“可审核的台账”。你不必完全信任搜索器怎么剪枝和并行，只要最终台账在已验证 certifier 看来是闭合且无坏状态，结论就成立。

### 运行 / 接受 / 转移语义

论文的方法链可保守写成：

$$
A \xrightarrow{\mathrm{search}} \mathcal{C} \xrightarrow{\mathrm{verified\ check}} \mathrm{Unreachable}
$$

上式中的符号逐项解释如下：

1. `$A$` 是输入的 timed automaton。
2. `$\mathcal{C}$` 是未验证搜索器产出的 explored-state certificate。
3. `$\mathrm{verified\ check}$` 是经 `Isabelle/HOL` 机械证明正确的 certifier。
4. `$\mathrm{Unreachable}$` 是最终可信的不可达结论。

论文强调 certification 的一个现实优点是：近似算子只需保证“覆盖更大”，而不必把整个近似算法本身完全形式化；这显著降低了可信实现成本。

### 语义边界

1. 论文只处理 reachability / unreachability，而不是一般时序逻辑全覆盖。
2. 它更关心“true result auditing”，而不是反例 replay。
3. 其 symbolic 基础仍是 zones/`DBM`，因此适用面与经典 timed-automata backend 相同。
4. 证书压缩和并行检查提升了实用性，但前提是覆盖关系本身仍能被 certifier 检查。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed automaton 骨架 | `$A=(T,I)$` | 论文直接处理的对象。 |
| delay / action 语义 | `$(l,u)\xrightarrow{d}(l,u\oplus d)$` 与 `$(l,u)\xrightarrow{a}(l',[r:=0]u)$` | 时间推进与离散跳转的基本规则。 |
| 证书对象 | `$\mathcal{C} \subseteq SymState$` | 不可达性结论的有限工件。 |
| 有效性条件 | `$init \in \mathcal{C} \land \forall s \in \mathcal{C}. s \notin Final \land Succ(s)\subseteq\downarrow\mathcal{C}$` | certifier 真正检查的核心性质。 |
| 工程基础 | `DBM`、覆盖关系、证书压缩、并行检查 | 说明该路线兼具可信性与实用性。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 timed automata symbolic states。 |
| 事件 / 触发 | 很强 | guard、action、reset 是离散步核心。 |
| 守卫 / 数据 | 中等支持 | 强在 clocks 和 guards，弱在富数据程序结构。 |
| 层次 | 不支持 | 不是层次状态机前端。 |
| 并发 / 同步 | 中等支持 | 可处理 networked timed automata 的 zone search 背景，但本文不主打组合语义。 |
| 时间约束 | 很强 | 全文围绕 timed reachability。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic 路线。 |
| 可执行 / 可验证性 | 很强 | `Mlunta` 生成证书，`Isabelle/HOL` certifier 检查证书，并支持并行与压缩。 |

### 形式化问题与性质

1. 这篇论文把“不可达”结论从黑盒算法输出变成了可审计工件。
2. 它的实用关键不是重新证明所有搜索优化，而是把优化后结果压回可检查的覆盖台账。
3. 对 `project_1` 来说，这为“验证 profile 也要输出证据”提供了非常直接的工程模板。

## 构造方式与承载格式

### 建模入口

建模入口是标准 timed automata 及其 zone-based symbolic search 场景。

### 机器可处理承载方式

机器可处理承载方式包括：

1. timed automata locations、guards、resets 和 invariants。
2. `(l,Z)` 形式的 symbolic states。
3. `DBM` 表示的 zones。
4. explored-state certificates 与 certificate compression 结果。

### 交换与互操作

这篇论文的互操作重点不在前端建模语言，而在“未验证搜索器与已验证 certifier”之间共享的证书对象。它让高性能 checker 可以保留自己的搜索和剪枝策略，但最终必须输出 certifier 可读的工件。

## 配套基础设施

- 建模/编辑工具：任意能产生 timed-automata symbolic search 输入的前端。
- 解析/交换/元模型支持：symbolic states、zones/`DBM`、覆盖关系和证书压缩工件。
- 仿真/执行支持：主线不是运行时执行，而是 verification-result auditing。
- 验证/分析支持：reachability / unreachability、zone exploration、parallel certificate checking。
- 代码生成/转换支持：搜索器生成证书，certifier 检查证书；重点不是控制代码生成。
- 标准化或社区生态：`Isabelle/HOL`、`Standard ML`、timed-automata benchmark 和 `DBM` 工具传统共同构成其生态。

## 适用场景与需求前提

### 适用场景

适合安全关键实时系统、需要审计第三方 timed model checker 结果、或希望把高性能搜索与高可信结论分离的验证流程。

### 需求前提

1. 系统已经能落成 timed automata。
2. 关键性质主要是 safety / bad-state unreachability。
3. 搜索器能够输出 symbolic-state certificate。
4. 团队愿意接受“先搜索、后认证”的两阶段工作流。

### 不适用或高成本场景

如果团队主要关心 counterexample 重放、一般富数据程序逻辑，或并不需要审计级可信性，那么引入证书化流程的收益会下降。

## 与相邻形式主义的关系

相对 [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md)，那篇走“完整 verified reference checker”路线，而本文走“未验证搜索器 + 已验证 certifier”路线；相对 [certifying-emptiness-of-timed-buchi-automata/desc.md](../certifying-emptiness-of-timed-buchi-automata/desc.md)，两者都是 certificate route，但那篇处理 timed liveness emptiness，这篇处理 reachability / unreachability；相对 [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)，后者关注更好的抽象后端，本文关注怎样在保留近似和优化的同时让结果可审计。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提示我们：自动生成状态机模型之后，验证结果本身也应该被证据化，而不是只保存 yes/no。
2. 对 `project_3` 的 verification profile 设计很有价值，因为 profile 可以定义“该导出什么证书”。
3. 对 `project_4` 的修复闭环也有启发，因为修复时不只要看反例，也要看当前不可达结论依赖的覆盖结构。

### 作为目标形式主义还是中间表示

它是 timed-verification 的证据层方法，而不是建模目标语言。

### 对需求到模型生成的启发

1. 若未来 LLM 生成 timed automata，最好同步生成能支持证书导出的验证配置。
2. 对 safety 问题，证书化不可达性比单纯“验证通过”更适合纳入自动化闭环。
3. 在高风险系统中，轻量 certifier 往往比完全 verified end-to-end tool 更现实。

### 现实限制

它主要覆盖 timed reachability 的认证，不会自动推广成任意时序逻辑或任意混成系统的一般证据框架。

## 重要的相关工作

### 奠基或前身工作

- [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md)：已验证 timed checker 母线。
- 经典 timed-automata zone / `DBM` 后端。

### 同类型或同家族工作

- [certifying-emptiness-of-timed-buchi-automata/desc.md](../certifying-emptiness-of-timed-buchi-automata/desc.md)：timed liveness 证书化路线。
- [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)：抽象后端优化路线。

### 标准 / 格式 / 工具链工作

- `Mlunta` `Standard ML` 搜索器。
- `Isabelle/HOL` certifier 与 timed-automata benchmark 工作流。

### 与本研究关系最紧的工作

- 自动建模之后如何把“验证通过”升级为“可审计通过”，这篇给出了一条非常清晰的实现模板。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / unreachability certificate / Isabelle-HOL certifier`
- 论文角色：时间自动机不可达性证书生成与已验证检查方法
- 核心功能：把 timed-automata reachability 的“不可达”结论转成可被已验证 certifier 检查的有限证书。
- 关键特性：symbolic states、zones/`DBM`、覆盖关系、证书压缩、并行检查、`Mlunta + Isabelle/HOL`。
- 构造方式：`timed automaton -> zone-based search -> explored-state certificate -> verified checking`。
- 基础设施：`Standard ML` 搜索器、`Isabelle/HOL` certifier、`DBM` 和 timed benchmark 生态。
- 适用场景：安全关键实时系统的不可达性审计、第三方 checker 结果复核和高可信验证闭环。
- 需求前提：系统需能落成 timed automata，性质以 safety / unreachability 为主，且搜索器可输出证书。
- 状态：🟢 直接可用

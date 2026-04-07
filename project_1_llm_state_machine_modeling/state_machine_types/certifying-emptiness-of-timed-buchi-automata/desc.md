# 定时 Büchi 自动机空性认证 / Certifying Emptiness of Timed Büchi Automata

## 基本信息

- 标题：Certifying Emptiness of Timed Büchi Automata
- 中文标题：定时 Büchi 自动机空性认证
- 作者：Simon Wimmer，Frédéric Herbreteau，Jaco van de Pol
- 发表：*Formal Modeling and Analysis of Timed Systems*，pp. 58-75，2020
- DOI：`10.1007/978-3-030-57628-8_4`
- 链接：https://doi.org/10.1007/978-3-030-57628-8_4
- 形式主义：`Timed Büchi Automata / certificate checking / Isabelle-HOL certifier`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed-liveness certificate extraction and mechanically verified certificate checking method
- 工具/实现获取方式：原文明确说明证书由 `TChecker` 与 `Imitator` 的 model-checking runs 导出，再交由 `Isabelle/HOL` 中机械验证的 certifier 检查；正文给出 artifact 入口说明。
- 标准/格式获取方式：主承载是 zone graph、subsumption graph、restricted reachability invariant 与 topological numbering 组成的证书对象；它不是通用行业交换标准，但目标就是成为多工具共享的 certifier format。

## 简报

这篇论文补的是 timed-automata 工具线里很关键、也很容易被忽视的一条方法路线：不是再做一个更快的 liveness checker，而是让已有 checker 把“空性为真”的结果输出成可被独立验证的证书。论文最核心的价值在于把 timed Büchi emptiness 的正确性证据压成有限对象，然后用 `Isabelle/HOL` 机械验证过的 certifier 做二次检查。这样一来，像 `TChecker`、`Imitator` 这种高性能工具就不必逐个完全形式化验证，也能把最难信任的“true result”变得可追溯。

- 形式主义定位：`Timed Büchi Automata` 的 liveness-certificate 方法路线，而不是新的 timed-automata 子类。
- 构造方式简述：`TBA -> zone graph / subsumption graph -> restricted reachability invariant + topological numbering -> verified certifier`。
- 基础设施与场景简述：依托 `TChecker`、`Imitator`、`Isabelle/HOL`、certificate extraction 与 common checker，服务安全关键实时系统中的 timed-liveness 验证结果增信。

```text
timed Buchi model-checking run -> finite certificate -> verified certifier -> trustworthy emptiness result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. timed automata 与 timed Büchi automata。
2. zone graph、abstraction 与 subsumption。
3. self-simulating transition system (`SSTS`)。
4. restricted reachability invariant。
5. restricted topological numbering 与 verified certifier。

### 核心抽象

论文给出的 timed automaton 骨架可写成：

$$
A = (Q, q_0, F, I, T, X)
$$

上式中的符号逐项解释如下：

1. `Q` 是 locations 集合。
2. `q_0` 是初始状态。
3. `F` 是 accepting states 集合。
4. `I` 给每个状态分配 invariant。
5. `T` 是带 guards 与 resets 的转移集合。
6. `X` 是 clocks 集合。

论文把带 subsumption 的抽象图提升为自模拟迁移系统：

$$
\mathcal S = (S, \to, \mu)
$$

上式中的符号逐项解释如下：

1. `S` 是图节点集合，例如 `(q,Z)` 形式的 zone states。
2. `\to` 是实际 transition relation。
3. `\mu` 是自模拟关系，在 timed-automata 语境下对应 subsumption。
4. 这正是论文 `SSTS` 的基本对象。

reachability invariant 可压成：

$$
I \subseteq S,\quad s_0 \in I,\quad s \in I \land s \to s' \Rightarrow \exists t \in I,\ s' \mu t
$$

上式中的符号逐项解释如下：

1. `I` 是证书里保留的有限节点集。
2. 初始状态必须在 `I` 内。
3. 每个真实后继都必须能被 `I` 中某个节点通过 `\mu` 覆盖。
4. 这就是“有限 invariant 足以模拟原系统”的核心条件。

为避免 spurious accepting cycles，论文还需要 restricted reachability invariant 与 restricted topological numbering。其代表性约束可写成：

$$
s E t \land \varphi(s) \Rightarrow f(s) > f(t),\qquad s E t \Rightarrow f(s) \ge f(t)
$$

上式中的符号逐项解释如下：

1. `E` 是允许计入证书的 restricted subsumption relation。
2. `\varphi` 是 accepting-state predicate。
3. `f` 是 restricted topological numbering。
4. 第一条保证与 accepting states 相关的边严格下降，第二条保证其他边不升高。
5. 这正是论文用来排除 accepting cycles 的有限证据。

### 一个最小例子与通俗解释

论文反复强调的难点是：对 reachability 来说，多用一点 subsumption 往往没问题；但对 liveness 来说，错误的 subsumption 很容易凭空造出 accepting cycle。

1. 原始 timed Büchi automaton 先展开成 zone graph。
2. 工具会尽量用 subsumption 压缩图。
3. 但若压得过头，某些“看起来能绕回 accepting state”的路径其实只是抽象造成的假圈。
4. 论文的做法不是直接相信压缩图，而是让工具额外给出 restricted invariant 和 numbering，证明这些 accepting cycles 实际不存在。

通俗地说，这像是在告诉 certifier：“我不是只给你一个压缩后的图，还额外给你一份可机器检查的证据，说明图里不会存在真正的活性反例环。”

### 运行 / 接受 / 转移语义

论文的方法链可以保守写成：

$$
\mathrm{TBA} \to \mathrm{zone\ graph} \to (I, E, f) \to \mathrm{check}
$$

上式中的符号逐项解释如下：

1. `TBA` 是待检查的 timed Büchi automaton。
2. `zone graph` 是标准 symbolic semantics。
3. `(I,E,f)` 是有限证书对象：节点集、受限覆盖边与编号函数。
4. `check` 是由 `Isabelle/HOL` 验证过的 certifier。

### 语义边界

1. 论文主线是 emptiness certification，不是通用 timed proof-carrying code。
2. 它处理的是“真结果”的外部认证，而不是 counterexample replay。
3. 效果依赖上游 model checker 能导出合适的 zone/subsumption 信息。
4. 证书格式虽力图通用于多工具，但目前仍紧贴 timed-automata liveness 场景。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TA/TBA` 骨架 | `$A = (Q,q_0,F,I,T,X)$` | 论文处理的基础对象。 |
| `SSTS` 骨架 | `$\mathcal S = (S,\to,\mu)$` | 用来统一 zone graph 与 subsumption 证书的抽象层。 |
| invariant 条件 | `$s \in I \land s \to s' \Rightarrow \exists t \in I,\ s' \mu t$` | 有限证书必须覆盖真实后继。 |
| restricted numbering | `$sEt \land \varphi(s) \Rightarrow f(s) > f(t)$` | 排除 accepting cycles 的核心证据。 |
| 证书对象 | `$(I,E,f)$` | certifier 直接检查的有限工件。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心就是 timed automata 的 symbolic states。 |
| 事件 / 触发 | 中等支持 | 通过 transitions 与 Büchi acceptance 间接体现。 |
| 守卫 / 数据 | 中等支持 | 强在 clock guards/invariants，弱在富数据。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 中等支持 | 可处理同步组合后的 timed models，但本文不主打组合语义。 |
| 时间约束 | 很强 | 整个问题就是 timed liveness。 |
| 连续动态 / 随机性 | 不支持 | 不在范围内。 |
| 可执行 / 可验证性 | 很强 | 上游 checker + certificate extraction + verified certifier 构成完整闭环。 |

### 形式化问题与性质

1. 论文真正解决的是“如何让 timed-liveness 的真结果也能像 SAT 一样被独立认证”。
2. 难点不在生成一个图，而在控制 subsumption，不让其引入伪 accepting cycles。
3. 这条路线对安全关键实时系统非常重要，因为 liveness true-result 往往比 counterexample 更难复核。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Timed Büchi Automata` 模型。
2. 上游 model checker 生成的 zone / subsumption 信息。
3. 从 run 中抽取出的有限 invariant 与 numbering。
4. verified certifier 的输入文件。

### 机器可处理承载方式

机器可处理承载方式包括：

1. zone graph 节点 `(q,Z)`。
2. subsumption relation。
3. restricted reachability invariant `(I,E)`。
4. restricted topological numbering `f`。

### 交换与互操作

互操作重点在于：

1. 证书格式有意设计成不同 timed-checking algorithms 都可产出。
2. 论文展示了与 `TChecker` 和 `Imitator` 的对接。
3. certifier 则独立于具体搜索算法和实现细节。

## 配套基础设施

- 建模/编辑工具：上游可来自 `TChecker`、`Imitator` 等 timed-automata 工具。
- 解析/交换/元模型支持：zone / subsumption / certificate 格式。
- 仿真/执行支持：主线不是执行器，而是 verification result checking。
- 验证/分析支持：Büchi emptiness、certificate extraction、verified certificate checking。
- 代码生成/转换支持：重点是 checker run 到 certificate 的提取转换。
- 标准化或社区生态：依托 `TChecker`、`Imitator`、`Isabelle/HOL` 与 timed-verification 社区。

## 适用场景与需求前提

### 适用场景

适合安全关键实时系统、协议活性验证、需要把“模型为空”这类结论做外部可信复核的 timed-automata 工作流。

### 需求前提

1. 模型需能落成 `Timed Büchi Automata` 或等价 emptiness 问题。
2. 上游工具应能导出 zone/subsumption 级证书信息。
3. 关注点是提高结果可信度，而不是替代高性能 model checker。
4. 性质最好真的是 liveness/accepting-cycle 问题，而不是一般富数据程序逻辑。

### 不适用或高成本场景

若系统不属于 timed-automata 语境，或团队只关心反例 replay 而不关心 true-result certification，这条路线的收益就没那么直接。

## 与相邻形式主义的关系

相对 [why-liveness-for-timed-automata-is-hard-and-what-we-can-do-about-it/desc.md](../why-liveness-for-timed-automata-is-hard-and-what-we-can-do-about-it/desc.md)，后者研究 timed liveness 算法为何困难以及如何构造 witness 图，而本文更进一步把“结果正确”做成可独立认证的工件；相对 [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md)，`Munta` 路线偏完整验证器的形式化实现，而本文偏“高性能工具 + 轻量 verified certifier”的双工具分工；相对 [imitator-ii-a-tool-for-solving-the-good-parameters-problem-in-timed-automata/desc.md](../imitator-ii-a-tool-for-solving-the-good-parameters-problem-in-timed-automata/desc.md)，两者都在 timed-automata 工具生态中，但一个解决参数综合，一个解决 liveness true-result certification。

## 与本研究的关系

### 对 Project 1 的价值

1. 它对“生成-验证-修复”闭环很重要，因为验证结论本身也需要可追溯证据。
2. 后续如果 LLM 生成 timed/state-machine 模型并交给外部 checker，像这种 certificate route 可以显著降低对单一工具黑盒信任的依赖。
3. 对 `project_3` 的 verification profile 也有启发：profile 不只要定义怎么验证，还可以定义该导出什么验证证据。

### 作为目标形式主义还是中间表示

更像 timed-verification 流水线里的证据层方法，而不是目标建模语言。

### 对需求到模型生成的启发

1. 活性性质往往比 reachability 更难验证，也更需要证据化输出。
2. 如果未来要让 AI 自动修模型，最好不仅保存 counterexample，也保存“为什么当前模型已被证明安全/空”的证书。
3. 在自动化研究流程里，轻量 certifier 往往比完全 verified checker 更现实。

### 现实限制

它主要覆盖 timed Büchi emptiness，不会自动扩展成所有时序逻辑或所有连续系统的通用证据框架。

## 重要的相关工作

1. [why-liveness-for-timed-automata-is-hard-and-what-we-can-do-about-it/desc.md](../why-liveness-for-timed-automata-is-hard-and-what-we-can-do-about-it/desc.md)：timed liveness witness 与 `SCC` 细化路线。
2. [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md)：`Isabelle/HOL` 上的 verified timed model checker 路线。
3. [imitator-ii-a-tool-for-solving-the-good-parameters-problem-in-timed-automata/desc.md](../imitator-ii-a-tool-for-solving-the-good-parameters-problem-in-timed-automata/desc.md)：timed-automata 工具生态中的相邻基础设施节点。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Büchi Automata / certificate checking / Isabelle-HOL certifier`
- 归类理由：论文核心贡献是 timed-liveness 结果的证书提取与机械检查方法，而不是新的 automata family 或统一工具平台，因此按 `⏱️/🛠️` 处理最稳。

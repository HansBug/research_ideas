# UPPAAL-SMC：面向 Priced Timed Automata 的统计模型检查 / UPPAAL-SMC: Statistical Model Checking for Priced Timed Automata

## 基本信息

- 标题：UPPAAL-SMC: Statistical Model Checking for Priced Timed Automata
- 中文标题：UPPAAL-SMC：面向 Priced Timed Automata 的统计模型检查
- 作者：Peter Bulychev，Alexandre David，Kim Guldstrand Larsen，Marius Mikučionis，Danny Bøgsted Poulsen，Axel Legay，Zheng Wang
- 发表：*Electronic Proceedings in Theoretical Computer Science*，Vol. 85，pp. 1-16，2012
- DOI：`10.4204/EPTCS.85.1`
- 链接：https://doi.org/10.4204/EPTCS.85.1
- 形式主义：`Networks of Priced Timed Automata / UPPAAL-SMC`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：基于 `NPTA` 的 statistical model checking 与性能分析工具扩展
- 工具/实现获取方式：原文明确把 `UPPAAL-SMC` 作为 `UPPAAL` 的 major extension，提供 query language、GUI、plot composer 和 engine 优化；文中未给独立仓库链接。
- 标准/格式获取方式：承载方式沿用 `UPPAAL` 的 automata network、broadcast channels、shared variables 与 query syntax，如 `Pr[bound](phi)`、`E[bound;N](min:expr)`。

## 简报

这篇论文的核心价值，不是提出新的 timed automata 本体，而是把 `UPPAAL` 从经典穷举式 real-time verification 扩展到面向 `Priced Timed Automata` 网络的统计模型检查与性能分析。`UPPAAL-SMC` 用自然随机语义给 `NPTA` 加上概率测度，再用 hypothesis testing、probability estimation、probability comparison 和 expected-value 查询去逼近原本不可判定或代价太高的问题。

- 形式主义定位：`UPPAAL` 生态中的 stochastic/statistical verification engine，不是新的状态机族主蓝本。
- 构造方式简述：建模仍是 `UPPAAL` 风格的 priced timed automata network，但查询从传统 reachability/temporal checking 扩展到 `Pr[...]`、`E[...]`、probability comparison 和 `WMTL<=` 监视器。
- 基础设施与场景简述：依托 `UPPAAL` GUI、plot composer、distributed SMC engine、monitor PTA 构造与多核优化，服务实时性能、概率时间界限和复杂 CPS 近似验证。

```text
priced timed automata network -> natural stochastic semantics -> Pr/E/WMTL<= queries -> simulation runs + statistical tests -> plots / distributions / performance estimates
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Priced Timed Automata (PTA)` 与 `Networks of PTA (NPTA)`。
2. `UPPAAL-SMC` 的自然随机语义。
3. `WMTL<=` 性质语言与 cost/time-bounded 查询。
4. hypothesis testing、probability estimation、probability comparison。
5. GUI、plot composer、distributed engine 与 choice reuse 优化。

### 核心抽象

论文把系统主对象收束为 `NPTA` 网络；按文中结构可保守整理为：

$$
M = A_1 \parallel A_2 \parallel \cdots \parallel A_n
$$

上式中的符号逐项解释如下：

1. `A_i` 是单个 priced timed automaton component。
2. `\parallel` 表示通过 broadcast channels 与 shared variables 的网络化组合。
3. `M` 是整个 `NPTA` 模型。
4. 这是基于原文“PTAs communicate via broadcast channels and shared variables to generate Networks of Price Timed Automata”做的保守整理。

论文对性质语言直接给出：

$$
\varphi ::= ap \mid \neg \varphi \mid \varphi_1 \land \varphi_2 \mid O\varphi \mid \varphi_1 U_{x \le d} \varphi_2
$$

上式中的符号逐项解释如下：

1. `ap` 是 atomic proposition。
2. `O` 是 next-state operator。
3. `U_{x \le d}` 是带 clock bound 的 until。
4. `x` 是 clock，`d` 是自然数时间或代价界。
5. 这是论文对 `WMTL<=` 的直接定义。

论文还定义了随机运行满足性质的概率：

$$
P_M(\psi)
$$

上式中的符号逐项解释如下：

1. `M` 是给定 `NPTA` 模型。
2. `\psi` 是运行性质。
3. `P_M(\psi)` 表示随机运行满足 `\psi` 的概率。
4. 这是论文在 `WMTL<=` 与统计查询之间的核心桥梁。

对 cost-bounded reachability，论文重点关注的问题可写成：

$$
P_M(\Diamond_{x \le C}\phi) \ge p
$$

上式中的符号逐项解释如下：

1. `\Diamond_{x \le C}\phi` 表示在 clock `x` 不超过 `C` 之前到达满足 `\phi` 的状态。
2. `p` 是比较阈值。
3. 这正是论文三类统计问题里的基础模板。

工具查询语法则直接给成：

$$
\mathrm{Pr}[bound](\phi) \ge p_0
$$

和

$$
\mathrm{E}[bound;N](\min:\mathrm{expr})
$$

上式中的符号逐项解释如下：

1. `bound` 指定按时间、代价或离散步数截断运行。
2. `p_0` 是概率阈值。
3. `N` 是显式运行次数。
4. `expr` 是要统计的 clock 或整数表达式。
5. 这是 `UPPAAL-SMC` 暴露给用户的核心查询接口。

### 一个最小例子与通俗解释

论文第一个小例子是三个组件 `A | B | T` 组成的 `NPTA`：

1. `A` 和 `B` 各自随机决定多久后发出 `a!` 与 `b!`。
2. `T` 通过 `a?`、`b?` 观察这两个事件。
3. 因为每个组件的延时都来自概率分布，系统在什么时候到达 `T3` 就不再是单值，而变成一个 time/cost 分布。

通俗地说，经典 `UPPAAL` 问的是“会不会到”；`UPPAAL-SMC` 问的是“多大概率会在多快、花多少代价的前提下到”。它像是在 timed automata 上加了一层 Monte Carlo 和假设检验。

### 运行 / 接受 / 转移语义

原文的语义要点是：

1. 单个 `PTA` 的停留时间由分布决定。
2. 有界延时用 uniform distribution，无界停留用 exponential distribution。
3. 网络中各组件独立 race，最小 delay 的输出方获胜。
4. 组合后会自动诱导出整个 `NPTA` 的概率测度。

### 语义边界

边界同样清楚：

1. 论文主体是 `UPPAAL` 的统计扩展，不是新 timed automata 理论母线。
2. 许多问题在一般 `NPTA` 上仍不可判定，因此工具默认给统计保证而不是完备证明。
3. 表达能力已经接近一般 `LHA`，因此强表达力与 undecidability 同时出现。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型组合 | `$M = A_1 \parallel \cdots \parallel A_n$` | `UPPAAL-SMC` 分析的是 `PTA` 网络而非单机。 |
| 性质语言 | `$\varphi ::= ap \mid \neg \varphi \mid \varphi_1 \land \varphi_2 \mid O\varphi \mid \varphi_1 U_{x \le d} \varphi_2$` | 采用带代价/时间界的 `WMTL<=`。 |
| 满足概率 | `$P_M(\psi)$` | 概率测度直接建立在随机运行之上。 |
| 概率判定模板 | `$P_M(\Diamond_{x \le C}\phi) \ge p$` | 对 cost/time-bounded reachability 做统计判断。 |
| 工具查询 | `$\mathrm{Pr}[bound](\phi)$`，`$\mathrm{E}[bound;N](\min:\mathrm{expr})$` | 直接暴露概率与期望估计接口。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 仍以 timed automata network 为建模骨架。 |
| 事件 / 触发 | 很强 | 通过 broadcast channels 与 guards 触发转换。 |
| 守卫 / 数据 | 中等支持 | 支持 shared variables 和 clock/cost guards。 |
| 层次 | 不支持 | 主体不是层次状态机。 |
| 并发 / 同步 | 很强 | 多组件 race 与 broadcast 同步是核心。 |
| 时间约束 | 很强 | `PTA/NPTA` 本身就是带 clock/cost 的实时模型。 |
| 连续动态 / 随机性 | 中等支持 | 随机性很强，连续动力学只是后续扩展方向。 |
| 可执行 / 可验证性 | 很强 | 可做 hypothesis testing、probability estimation、comparison 和 expected value。 |

### 形式化问题与性质

1. 工具最突出的不是单个算法，而是把若干 SMC 模式统一到了同一 query 语言里。
2. 它支持对传统 model checking 难以覆盖的性能问题给出有置信度的近似答案。
3. `distributed SMC`、state detection、early termination 和 choice reuse 是性能关键。

## 构造方式与承载格式

### 建模入口

建模入口仍然是典型 `UPPAAL` 模式：

1. 用 automata templates 建 `PTA` 组件。
2. 通过 broadcast channels 与 shared variables 组合成 `NPTA`。
3. 用 `Pr[...]`、`E[...]` 和 `WMTL<=` 监视器查询性质。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UPPAAL` 模板化 automata network。
2. priced clocks / rates / shared variables。
3. `Pr[...]`、`E[...]` 与 comparison queries。
4. 统计输出的 histogram、density 与 cumulative distributions。

### 交换与互操作

这条路线的互操作重点在于：

1. 沿用 `UPPAAL` 前端模型。
2. 在后端追加 statistical engine 与 monitors。
3. 用 GUI 和 plot composer 把数值结果可视化，而不是只给 yes/no。

## 配套基础设施

- 建模/编辑工具：沿用 `UPPAAL` GUI。
- 解析/交换/元模型支持：沿用 `UPPAAL` 模型输入语言，扩展 statistical query syntax。
- 仿真/执行支持：基于随机运行生成样本轨迹，并支持 trajectory clouds、表达式监视与分布图。
- 验证/分析支持：hypothesis testing、probability estimation、probability comparison、expected values、full `WMTL<=` monitoring。
- 代码生成/转换支持：本文重点不是部署代码生成，原文未说明。
- 标准化或社区生态：直接依附 `UPPAAL` 工具体系，是其 stochastic/statistical extension。

## 适用场景与需求前提

### 适用场景

适合实时嵌入式系统、性能分析、概率时间界限验证、控制器性能比较，以及原本不可判定但可接受统计保证的 timed/hybrid-like CPS 场景。

### 需求前提

1. 系统能落成 `PTA/NPTA` 网络。
2. 关注点是概率、代价、性能或近似验证，而不只是布尔正确性。
3. 用户接受统计置信区间，而非完备穷举证明。

### 不适用或高成本场景

如果问题要求完全精确的全状态结论，或者系统行为不适合定时自动机网络表达，`UPPAAL-SMC` 的收益会下降。

## 与相邻形式主义的关系

相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，它更靠近 `UPPAAL` timed-automata 生态和 statistical checking，而不是 symbolic probabilistic model checking 主线；相对 [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)，它覆盖的模型族更聚焦 `PTA/NPTA`，但在实时统计查询与 GUI 可视化上更直接；相对 [an-introduction-to-cora-2015/desc.md](../an-introduction-to-cora-2015/desc.md)，它不是 reachability over-approximation toolbox，而是基于随机运行的近似验证工具。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果后续 LLM 生成的状态机包含显式时序与代价维度，不必只盯着穷举 model checking，也可以接到统计型验证后端。

### 作为目标形式主义还是中间表示

更适合作为验证后端和性能分析载体，而不是最终的人类建模交付语言。

### 对需求到模型生成的启发

1. 如果需求里有“概率多大”“平均多久”“代价分布怎样”这类问题，生成目标应保留 cost/time 变量。
2. `Pr[...]` 与 `E[...]` 这种 query-facing 语义，对需求转验证问题很重要。
3. 统计验证特别适合补足那些精确求解过重或不可判定的 timed/hybrid 扩展问题。

### 现实限制

它依赖用户已经把系统压成 `UPPAAL` 风格 `NPTA`，并且接受统计误差与样本驱动结果。

## 重要的相关工作

1. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：概率实时系统的 symbolic model checker。
2. [the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md](../the-modest-toolset-an-integrated-environment-for-quantitative-modelling-and-verification/desc.md)：更广的 quantitative verification 平台。
3. [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)：定量模型与工具互操作层。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Networks of Priced Timed Automata / UPPAAL-SMC`
- 归类理由：论文主体是建立在 `UPPAAL` 上的 statistical model checking 方法与执行基础设施，而不是新的 timed automata 本体。

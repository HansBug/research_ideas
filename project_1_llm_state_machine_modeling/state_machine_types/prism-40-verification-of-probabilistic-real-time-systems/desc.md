# PRISM 4.0：概率实时系统验证 / PRISM 4.0: Verification of Probabilistic Real-Time Systems

## 基本信息

- 标题：PRISM 4.0: Verification of Probabilistic Real-Time Systems
- 中文标题：PRISM 4.0：概率实时系统验证
- 作者：Marta Kwiatkowska，Gethin Norman，David Parker
- 发表：*Computer Aided Verification*，pp. 585-591，2011
- DOI：`10.1007/978-3-642-22110-1_47`
- 链接：https://doi.org/10.1007/978-3-642-22110-1_47
- 形式主义：`Probabilistic Timed Automata / Priced Probabilistic Timed Automata / PRISM`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：probabilistic real-time model checker / PTA-PPTA tool release
- 工具/实现获取方式：原文明确说明 `PRISM` 是 free and open source (`GPL`)，可从 `http://www.prismmodelchecker.org/` 下载，支持主流操作系统。
- 标准/格式获取方式：承载方式是 `PRISM` 文本建模语言（guarded commands、clock declarations、invariants、reward structures），并配套 benchmark suite 与多种 verification engines；无独立中立交换标准。

## 简报

这篇论文的关键增量，是把 `PRISM` 从一般概率模型检查器推进到能处理 `(priced) probabilistic timed automata` 的概率实时分析平台。它不仅补了 `PTA/PPTA` 本身，还同时补了 quantitative abstraction refinement、digital clocks、explicit-state library、statistical model checking、optimal adversary generation 与 benchmark suite。

- 形式主义定位：概率实时自动机的验证基础设施，而不是新的 timed/probabilistic automaton 本体论文。
- 构造方式简述：用 `PRISM` guarded-command language 描述 `PTA/PPTA`，再选 abstraction-refinement、digital clocks 或其他 engines 做概率实时分析。
- 基础设施与场景简述：依托 `PRISM` language、model checking engines、simulation engine、strategy generation 与 benchmark suite，服务 embedded controllers、wireless protocols、security protocols 等概率实时系统。

```text
probabilistic real-time model -> PRISM language -> PTA/PPTA engine -> probability / reward analysis -> strategy / benchmark / simulation support
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `PRISM 4.0`：

1. probabilistic timed automata (`PTA`)。
2. priced probabilistic timed automata (`PPTA`)。
3. `PRISM` 文本建模语言。
4. quantitative abstraction refinement 与 digital clocks engines。
5. explicit-state library、simulation engine、optimal adversaries 与 benchmark suite。

### 核心抽象

结合论文对 `PTA` 的说明，可把其模型保守写成：

$$
\mathcal{A} = (L, \ell_0, X, V, Inv, E)
$$

上式中的符号逐项解释如下：

1. `L` 是离散 locations 集合。
2. `\ell_0` 是初始 location。
3. `X` 是 clocks 集合。
4. `V` 是 finite-range data variables。
5. `Inv` 是 state invariants。
6. `E` 是带 guards、probabilistic updates 与 resets 的 transitions。
7. 这组符号是依据论文“finite-state automata + clocks + discrete probabilistic choice”做的保守归纳。

对 `PRISM 4.0` 而言，`PTA` 最关键的是 transition 带概率分布，可保守写成：

$$
e = (\ell, g, \mu)
$$

其中：

1. `\ell` 是源 location。
2. `g` 是 clock/data guard。
3. `\mu` 是离散概率分布，目标是若干 `(update, \ell')` 对。

论文进一步说明 `PTA` 可加 reward/cost，得到 `PPTA`。可把 reward 结构保守写成：

$$
\mathcal{R} : L \cup E \to \mathbb{R}_{\ge 0}
$$

上式中的符号逐项解释如下：

1. `\mathcal{R}` 给 states 与 transitions 赋 cost/reward。
2. 从而可分析 reachability probability 之外的 expected accumulated reward。

### 一个最小例子与通俗解释

论文用一个 transmitter 例子解释 `PTA`：

1. location `s=0` 表示准备发送。
2. clock `x` 控制“多久后可以重试/超时”。
3. integer variable `tries` 统计发送次数。
4. `send` 以 `0.9/0.1` 概率分别走成功或失败分支。
5. reward structure `energy` 记录能量开销。

通俗地说，这类模型像“给 timed automaton 再塞进概率选择和代价账本”。`PRISM 4.0` 的价值是让这些对象不只停留在论文里，而能直接被建模、求概率、算最优策略。

### 运行 / 接受 / 转移语义

论文强调 `PRISM` 为 `PTA` 提供两类主分析对象：

$$
\min/\max\ \Pr(\Diamond_{\le T}\ target)
$$

$$
\min/\max\ \mathbb{E}[Reward\ \mathrm{Until}\ target]
$$

上式中的符号逐项解释如下：

1. `\Pr(\Diamond_{\le T}\ target)` 表示时间有界到达目标的概率。
2. `\mathbb{E}[Reward\ \mathrm{Until}\ target]` 表示到达目标前累计 reward/cost 的期望。
3. `\min/\max` 反映 nondeterminism 下的最小/最大值。

原文还给出两条关键求解路线：

$$
\mathrm{PTA\ Check} = \mathrm{QAR} \;\lor\; \mathrm{DigitalClocks}
$$

其中：

1. `\mathrm{QAR}` 是 quantitative abstraction refinement。
2. `\mathrm{DigitalClocks}` 是把实时时钟离散化到等价 finite-state model 的路线。
3. 前者是默认 PTA engine，后者覆盖面更宽，也能处理 linearly priced PTA 的 reward analysis。

### 语义边界

这篇论文的边界主要有：

1. 它是 `PRISM 4.0` release/tool paper，不是 `PTA/PPTA` 的奠基定义论文。
2. digital clocks 方法有若干适用限制，例如 strict clock comparisons 受限。
3. 工具支持的模型类很广，但不同 engine 的可处理能力并不完全相同。
4. 更丰富的 probabilistic/stochastic hybrid systems 仍是未来扩展方向。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PTA` 骨架 | `$\mathcal{A} = (L, \ell_0, X, V, Inv, E)$` | `PRISM 4.0` 支持的概率实时自动机基本对象。 |
| 概率转移 | `$e = (\ell, g, \mu)$` | transition 同时带 guard 和离散概率选择。 |
| reward 结构 | `$\mathcal{R} : L \cup E \to \mathbb{R}_{\ge 0}$` | 支撑 `PPTA` 的 cost/reward 分析。 |
| 概率查询 | `$\min/\max\ \Pr(\Diamond_{\le T}\ target)$` | 原文强调的 reachability probability。 |
| 代价查询 | `$\min/\max\ \mathbb{E}[Reward\ \mathrm{Until}\ target]$` | 原文强调的 expected reward 分析。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | location-based probabilistic real-time models 是核心。 |
| 事件 / 触发 | 中等支持 | 主要通过 guarded commands 与 action labels 表达。 |
| 守卫 / 数据 | 很强 | clocks、finite-range variables、guards、updates 都支持。 |
| 层次 | 弱支持 | 主体是 flat PTA/PPTA 与 modules。 |
| 并发 / 同步 | 强支持 | 多个 PTAs 可并行组合并同步。 |
| 时间约束 | 很强 | `PTA/PPTA` 与 timed reachability 是核心。 |
| 连续动态 / 随机性 | 强随机 / 弱连续 | 概率是核心；连续动力学不在主线。 |
| 可执行 / 可验证性 | 很强 | model checking、simulation、strategy generation、benchmark 全具备。 |

### 形式化问题与性质

1. `PRISM 4.0` 把 `PTA/PPTA` 从“可被讨论的模型”推进成“有成熟引擎、有语言、有 benchmark 的工具支线”。
2. abstraction refinement 与 digital clocks 两条路线共同构成其概率实时分析基底。
3. 这条线对 `project_1` 的意义在于：如果未来出现概率/代价/可靠性需求，不必只停留在 plain timed automata。

## 构造方式与承载格式

### 建模入口

论文中的典型入口是：

1. 用 `PRISM` guarded-command language 写 modules、clock declarations、invariants。
2. 需要代价时再写 reward structures。
3. 选择 PTA engine、simulation 或 strategy generation。
4. 用 benchmark suite 与 case studies 做评测或复现。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `PRISM` 文本模型。
2. clock declarations 与 invariants。
3. reward structures。
4. benchmark suite。

### 交换与互操作

这篇论文的互操作重点在于：

1. 单一语言覆盖 `DTMC/CTMC/MDP/PTA/PPTA`。
2. 通过 digital clocks 等路线与离散 finite-state analysis 接轨。
3. 工具内置 benchmark 与 library，方便新算法在其上复用。

## 配套基础设施

- 建模/编辑工具：`PRISM` GUI 与命令行工具。
- 解析/交换/元模型支持：统一文本语言、多类概率模型前端。
- 仿真/执行支持：discrete-event simulation engine 与 statistical model checking。
- 验证/分析支持：symbolic engines、explicit-state library、abstraction refinement、digital clocks、optimal adversary generation。
- 代码生成/转换支持：主体不是代码生成；重点在 analysis/verification infrastructure。
- 标准化或社区生态：`GPL` 开源发布、官方 benchmark suite、长期维护的概率模型检查生态。

## 适用场景与需求前提

### 适用场景

适合带概率、实时和 nondeterminism 混合特征的 embedded controllers、通信协议、随机化安全协议与资源代价分析场景。

### 需求前提

1. 模型能被表达成 `PRISM` 支持的 probabilistic modules / `PTA/PPTA`。
2. 需求关心概率、期望代价或最优策略，而不只是布尔可达性。
3. 系统时间特征适合 timed automata 风格表示。
4. 团队愿意使用概率模型检查器，而不是只做 deterministic verification。

### 不适用或高成本场景

如果系统主要是连续物理动力学或重度 hybrid ODE，`PRISM 4.0` 这条 PTA 路线并不是最佳入口。

## 与相邻形式主义的关系

相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，`UPPAAL` 强在经典 timed automata，而 `PRISM 4.0` 强在概率实时扩展；相对 [probabilistic-automata/desc.md](../probabilistic-automata/desc.md)，本文不是概率自动机本体定义，而是成熟工具化节点；相对 [the-greatspn-tool-recent-enhancements/desc.md](../the-greatspn-tool-recent-enhancements/desc.md)，两者都支持代价/概率分析，但 `PRISM` 面向 probabilistic automata family，而 `GreatSPN` 面向 stochastic Petri nets。

## 与本研究的关系

### 对 Project 1 的价值

它说明若 `project_1` 后续面对可靠性、成功率、能耗期望等非纯布尔需求，状态机输出可以进一步桥接到 probabilistic real-time backend，而不必停在 deterministic timed automata。

### 作为目标形式主义还是中间表示

对大多数控制需求，它更像验证后端或分析后端；对概率实时系统研究，它也可能成为直接建模目标。

### 对需求到模型生成的启发

1. 需求中若出现概率、代价、资源消耗，就需要比 plain TA 更丰富的中间表示。
2. guarded-command language 很适合把 automaton + data + reward 统一到一个文本承载里。
3. benchmark suite 和 strategy generation 对闭环调试尤其重要。

### 现实限制

它非常强，但也明显提高了建模和验证门槛，不适合作为所有普通控制问题的默认前端。

## 重要的相关工作

- [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：经典 timed automata 工具母线。
- [survey-of-timed-automata-for-real-time-systems/survey.md](../survey-of-timed-automata-for-real-time-systems/survey.md)：时间自动机变体与工具生态总览。
- [the-greatspn-tool-recent-enhancements/desc.md](../the-greatspn-tool-recent-enhancements/desc.md)：另一条定量/概率分析工具线。
- [recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games/desc.md)：概率/随机自动机主线上的理论背景。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Probabilistic Timed Automata / Priced Probabilistic Timed Automata / PRISM`
- 论文角色：probabilistic real-time model checker / PTA-PPTA tool release

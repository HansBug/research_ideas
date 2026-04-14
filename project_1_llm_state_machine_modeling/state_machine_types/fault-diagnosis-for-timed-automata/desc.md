# 时间自动机的故障诊断 / Fault Diagnosis for Timed Automata

## 基本信息

- 标题：Fault Diagnosis for Timed Automata
- 中文标题：时间自动机的故障诊断
- 作者：Stavros Tripakis
- 发表：*Formal Techniques in Real-Time and Fault-Tolerant Systems*，pp. 205-221，2002
- DOI：`10.1007/3-540-45739-9_14`
- 链接：https://doi.org/10.1007/3-540-45739-9_14
- 形式主义：`Timed Automata / diagnosability / diagnoser`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed diagnosability mother paper / diagnoser construction route
- 工具/实现获取方式：原文未给独立发布软件，但明确指出算法可用与 `Kronos`、`Uppaal` 同类 timed-automata 工具相近的数据结构与算法实现。
- 标准/格式获取方式：主承载是 timed automaton、observable / unobservable events、fault event、product automaton、region / simulation graph 与 diagnoser tuple；不是交换标准。

## 简报

这篇论文补的是 `Timed Automata` 支线里非常经典的一条“诊断”路线：系统里 fault 事件本身往往不可直接观测，诊断器只能看到可观测事件和它们之间的时间间隔，因此问题不再只是 reachability，而是“故障发生后，最迟多久能仅凭可观测行为把它判出来”。作者把这一点系统化成 `\Delta`-diagnosability，并给出 diagnosability 检查、最小延迟搜索以及 diagnoser 构造。

- 形式主义定位：这是围绕 `Timed Automata` 的 fault-diagnosis 方法母论文，不是新的时间自动机变体。
- 构造方式简述：`timed automaton with observable/unobservable events -> diagnosability check on self-product -> binary search for minimal Δ -> diagnoser as state estimator`。
- 基础设施与场景简述：依托 region graph、simulation graph、`Kronos` 风格 `DBM/polyhedra` 数据结构，适合安全关键实时系统中的 fault detection。

```text
timed automaton -> diagnosability check -> Δ bound -> diagnoser state estimator -> runtime fault announcement
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 带可观测 / 不可观测事件与 fault event 的 timed automaton。
2. 以时间延迟为界的 `\Delta`-diagnosability。
3. 用自乘积自动机做 diagnosability 判定。
4. 以状态估计器为核心的 diagnoser 构造。

### 核心抽象

论文直接定义 timed automaton：

$$
A = (Q, X, \Sigma, E, I)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是离散状态集合。
2. `$X$` 是 clocks 集合。
3. `$\Sigma = \Sigma_o \cup \Sigma_u$` 是事件集合，其中 `$\Sigma_o$` 为 observable events，`$\Sigma_u$` 为 unobservable events。
4. `$f \in \Sigma_u$` 是 distinguished fault event。
5. `$E$` 是带 guard 与 reset 的 transitions。
6. `$I$` 是 invariant function。

单个运行状态是：

$$
s = (q, v)
$$

上式中的符号逐项解释如下：

1. `$q \in Q$` 是离散位置。
2. `$v$` 是 clock valuation。
3. 整个 timed run 就是在离散状态和时钟赋值上的交替 delay / action 迁移。

论文给出的 `\Delta`-diagnosability 定义是全文核心：

$$
A \text{ is } \Delta\text{-diagnosable}
$$

当且仅当对任意两个有限运行 `$\rho_1,\rho_2$`，若 `$\rho_1$` 是 `$\Delta`-faulty`，则

$$
\rho_2 \text{ is faulty } \lor P(\rho_1,\Sigma_u) \neq P(\rho_2,\Sigma_u)
$$

上式中的符号逐项解释如下：

1. `$\rho_1$` 是在某次 fault 发生后至少又经过 `$\Delta$` 时间单位的运行。
2. `$P(\rho,\Sigma_u)$` 表示把不可观测事件投影掉之后的可观测 timed sequence。
3. 定义要求：一旦 fault 发生并再过 `$\Delta$` 时间，任何非故障运行都不能与它保持同样观测。
4. 这正是“最迟 `\Delta` 时间内必须可诊断”的正式表达。

diagnoser 本身被定义为：

$$
(W, W_0, f_e, f_t, f_d)
$$

上式中的符号逐项解释如下：

1. `$W$` 是 diagnoser 的状态集合。
2. `$W_0$` 是初始状态。
3. `$f_e : W \times \Sigma_o \to W$` 是对 observable event 的状态更新。
4. `$f_t : W \times \mathbb{R} \to W$` 是对时间延迟的状态更新。
5. `$f_d : W \to \{\text{not-yet}, \text{yes}\}$` 是故障判断输出。

论文进一步给出 diagnoser 作为 state estimator 的核心定义：

$$
W = 2^{R_A}
$$

以及

$$
f_d(W) =
\begin{cases}
\text{yes}, & \text{if } \forall s \in W,\ discrete(s)\in Q_f \\
\text{not-yet}, & \text{otherwise}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `$R_A$` 是 timed automaton 的可达状态集合。
2. diagnoser 的一个状态是“当前所有仍然可能的 plant states”的集合。
3. 若该集合里所有可能状态都已经在 fault region `$Q_f$` 内，则 diagnoser 输出 `yes`。
4. 这使得故障检测问题被化成了集合状态估计问题。

### 一个最小例子与通俗解释

论文中最直观的例子是：

1. 系统总会先看到事件 `a`，再看到 `b`。
2. 如果中间发生过 fault，则 `a` 到 `b` 的时间间隔一定大于 `3`。
3. 如果没发生 fault，则这个时间间隔最多为 `3`。
4. 因此 diagnoser 只需要观测到 `a`、`b` 以及两者之间的延迟，就能判断 fault 是否已经发生。

通俗地说，这类 diagnoser 不是在看“有没有收到 fault 事件”，而是在看“现在所有还解释得通的内部状态里，是否已经只剩下故障解释了”。

### 运行 / 接受 / 转移语义

论文沿用 timed automata 的标准两步语义：

$$
(l,u) \xrightarrow{d} (l, u \oplus d), \qquad (l,u) \xrightarrow{a} (l', [r:=0]u)
$$

上式中的符号逐项解释如下：

1. `$d \ge 0$` 是时间推进量。
2. `$u \oplus d$` 表示所有 clocks 同时增加 `$d$`。
3. `$a$` 是离散动作标签。
4. `$r$` 是被 reset 的 clocks 集。
5. guard 与 invariant 必须在对应 delay / action 步中满足。

diagnosability 检查的关键构造则是自乘积：

$$
(A \bar{\times}_{\Sigma_o} A) - f_2
$$

上式中的符号逐项解释如下：

1. 该乘积把 `$A$` 复制成两个版本。
2. 两个副本在 observable events 上同步，在 unobservable events 上各自前进。
3. 第二个副本去掉 fault event，因此表示“无故障解释”。
4. 若这个乘积里还存在 non-zeno faulty run，就说明 fault 与 non-fault 在观测上仍无法区分，系统不可诊断。

### 语义边界

1. 论文讨论 dense-time timed automata，不是一般 hybrid diagnosability。
2. 诊断器只能看到 observable events 和时间延迟，不能直接读取 clocks。
3. 一次分析默认针对一种 fault event，可扩展到多 fault，但需要分别检查。
4. 目标是 detection，不涉及在线 fault repair。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed automaton | `$A = (Q, X, \Sigma, E, I)$` | 诊断问题的 plant 模型。 |
| 运行状态 | `$s = (q, v)$` | 诊断器估计的对象是离散状态与时钟赋值。 |
| `\Delta`-diagnosability | `$\rho_2 \text{ faulty } \lor P(\rho_1,\Sigma_u) \neq P(\rho_2,\Sigma_u)$` | 故障后最迟 `\Delta` 时间必须和无故障行为可区分。 |
| diagnoser | `$(W, W_0, f_e, f_t, f_d)$` | 事件、延迟、决策三部分组成的确定性诊断机。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 timed automaton 状态估计。 |
| 事件 / 触发 | 很强 | observable / unobservable / fault 事件划分是问题核心。 |
| 守卫 / 数据 | 中等支持 | 强在 clocks 与 guard，弱在复杂离散数据。 |
| 层次 | 不支持 | 不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 可组合 timed automata，但主体不是并发语义。 |
| 时间约束 | 很强 | `\Delta`-bounded diagnosis 完全依赖 dense-time 观测。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic diagnosis。 |
| 可执行 / 可验证性 | 很强 | diagnosability 检查与 diagnoser 构造都给了可实现算法。 |

### 形式化问题与性质

1. 论文把故障诊断从 DES 推广到了 dense-time automata。
2. 诊断条件不仅看事件序列，还看时间间隔。
3. diagnoser 的实质是“对所有可能内部状态的集合估计”。
4. 对本论文集而言，这篇是 timed diagnosability 支线的核心挂点。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. timed automaton。
2. observable / unobservable event 划分。
3. distinguished fault event。
4. 诊断延迟目标 `\Delta`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. region graph / simulation graph。
2. self-product automaton。
3. diagnoser state-estimator sets。
4. `DBM/polyhedra` 风格状态表示。

### 交换与互操作

论文本身没有定义中立交换标准；互操作重点在于 timed-automata model-checking backend 与 diagnoser runtime 共享同一套 symbolic state representation。

## 配套基础设施

- 建模/编辑工具：任意 timed-automata 建模入口。
- 解析/交换/元模型支持：region graph、simulation graph、自乘积和 state estimator 表示。
- 仿真/执行支持：diagnoser 可在 runtime 读取 observable events 与 delay 运行。
- 验证/分析支持：diagnosability 检查、最小 `\Delta` 搜索、fault-delay 二分搜索。
- 代码生成/转换支持：论文主体不是代码生成，但给出了 diagnoser 的实现骨架和伪代码。
- 标准化或社区生态：与 `Kronos`、`Uppaal` 同类的 timed-automata backend 紧密相关。

## 适用场景与需求前提

### 适用场景

适合以下问题：

1. 安全关键实时系统的故障检测。
2. 协议、嵌入式控制器、诊断监控器中“时间模式本身能暴露 fault”的场景。
3. 需要同时基于事件与延迟做在线诊断的 timed system。

### 需求前提

1. plant 必须能落成 timed automaton。
2. observable / unobservable events 必须划分清楚。
3. 关键 fault 的判定确实依赖时间信息，而非纯离散序列。
4. 团队能接受 diagnoser 维护一组可能内部状态。

### 不适用或高成本场景

若系统含丰富连续动力学、概率扰动，或 fault 无法通过事件序列与时间间隔区分，这条 timed-automata diagnosis 路线就不够。

## 与相邻形式主义的关系

相对 [verified-certification-of-reachability-checking-for-timed-automata/desc.md](../verified-certification-of-reachability-checking-for-timed-automata/desc.md)，那篇关注 reachability result certification，这篇关注 partial observation 下的 fault diagnosis；相对 [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md)，那篇更偏可信验证后端，这篇强调 diagnoser 构造；相对 [certifying-emptiness-of-timed-buchi-automata/desc.md](../certifying-emptiness-of-timed-buchi-automata/desc.md)，后者处理 liveness-style emptiness，这里处理 bounded-delay fault detection。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 `Timed Automata` 家族不仅适合 reachability / scheduling，也适合 fault diagnosis 这类运行期监控问题。
2. 如果未来自动生成出的时间状态机要直接服务工业诊断，这篇提供了非常清楚的目标能力画像。
3. 它还能帮助区分“适合作为控制模型”和“适合作为监控 / 诊断后端”的 timed family 角色。

### 作为目标形式主义还是中间表示

更适合作为需要时间故障诊断能力时的目标验证 / 监控形式主义，也可作为从需求级 fault pattern 到 diagnosis backend 的中间表示。

### 对需求到模型生成的启发

1. 需求中若出现“故障发生后多少时间内必须发现”，就应该优先考虑 timed family。
2. 诊断需求需要显式写出哪些事件可观测、哪些不可观测。
3. 仅有安全性质还不够，故障诊断还要求模型保留足够精确的时间区分能力。

### 现实限制

它对 timed diagnosis 非常经典，但模型抽象要求较高，且对观测建模不当时容易得到不可诊断结论。

## 重要的相关工作

### 奠基或前身工作

- 离散事件系统中的 fault diagnosis 母线。
- 经典 timed automata、region graph 与 symbolic reachability。

### 同类型或同家族工作

- [verified-certification-of-reachability-checking-for-timed-automata/desc.md](../verified-certification-of-reachability-checking-for-timed-automata/desc.md)
- [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md)

### 标准 / 格式 / 工具链工作

- `Kronos`、region graph、simulation graph、`DBM` 数据结构。

### 与本研究关系最紧的工作

- [survey-of-timed-automata-for-real-time-systems/survey.md](../survey-of-timed-automata-for-real-time-systems/survey.md)
- [certifying-emptiness-of-timed-buchi-automata/desc.md](../certifying-emptiness-of-timed-buchi-automata/desc.md)

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata / diagnosability / diagnoser`
- 论文角色：timed diagnosability mother paper / diagnoser construction route
- 核心功能：把故障诊断推广到 dense-time automata，并给出 diagnosability 检查与 diagnoser 构造。
- 关键特性：observable / unobservable events、fault event、`\Delta`-diagnosability、自乘积检查、state-estimator diagnoser。
- 构造方式：`timed automaton -> diagnosability check -> diagnoser tuple -> runtime diagnosis`。
- 基础设施：region graph、simulation graph、`Kronos` 风格 symbolic backend、`DBM/polyhedra` 实现。
- 适用场景：安全关键实时控制、协议和嵌入式系统的 fault detection 与在线诊断。

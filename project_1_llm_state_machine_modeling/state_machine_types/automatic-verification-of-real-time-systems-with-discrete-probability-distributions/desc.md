# 带离散概率分布的实时系统自动验证 / Automatic Verification of Real-time Systems with Discrete Probability Distributions

## 基本信息

- 标题：Automatic Verification of Real-time Systems with Discrete Probability Distributions
- 中文标题：带离散概率分布的实时系统自动验证
- 作者：Marta Kwiatkowska, Gethin Norman, Roberto Segala, Jeremy Sproston
- 发表：*Theoretical Computer Science*, 282(1):101-150, 2002
- DOI：`10.1016/S0304-3975(01)00046-9`
- 链接：https://doi.org/10.1016/S0304-3975(01)00046-9
- 形式主义：`Probabilistic Timed Automata (PTA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供独立实现；机器可处理入口是 `PTA` 元组、region graph、zone graph、`PTCTL` 与 reachability analysis。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是位置图、clock invariants、enabling zones 与对 `(next state, reset set)` 的离散概率分布。

## 简报

这篇论文把经典 `Timed Automata` 明确扩成 `Probabilistic Timed Automata`：系统先在当前 enabled distributions 之间做 nondeterministic 选择，再按所选分布对目标位置和 reset 集合做 probabilistic 选择。这样得到的模型仍然是 dense-time、clock-based 的 timed automaton，但它不再只表达“可能发生什么”，而能表达“多大概率发生什么”。对当前演化树而言，它非常适合补成 `Timed Automata` 下的 `Probabilistic Timed Automata` 经典节点。

- 形式主义定位：`Timed Automata` 的概率扩展分支，用离散概率分布替代纯非确定边选择。
- 构造方式简述：每个 location 携带 invariant；每个 enabled distribution 给出一组 `(target, reset-set)` 结果及其概率。
- 基础设施与场景简述：原文给出 `PTCTL` 模型检查、region graph 和 zone-based reachability，因此它不仅提出模型，还把分析入口一起固定下来。

```text
timed automaton -> enabled distributions over edges -> probabilistic timed automaton -> PTCTL / reachability verification
```

## 形式主义定义与核心对象

### 定义对象

模型对象仍是“带时钟的实时反应系统”，但边选择不再是单纯 nondeterministic。作者要表达的是：在实时系统里，某些跳转既受时间约束，也有离散概率。

### 核心抽象

论文 Definition 2 给出的 `Probabilistic Timed Automaton` 可写成：

$$
G = (S,L,\bar{s},X,\mathrm{inv},\mathrm{prob},\langle \tau_s \rangle_{s\in S})
$$

上式中的符号逐项解释如下：

1. `S` 是有限节点集。
2. `L : S \to 2^{AP}` 给每个节点标注原子命题。
3. `\bar{s} \in S` 是起始节点。
4. `X` 是有限时钟集。
5. `\mathrm{inv}` 给每个节点赋一个 invariant zone。
6. `\mathrm{prob}(s)` 给每个节点一个有限非空的离散概率分布集合；每个分布定义在 `S \times 2^X` 上。
7. `\tau_s` 给出每个分布何时 enabled 的 clock condition。

换句话说，系统不是直接从边跳到边，而是先选一个 probability distribution `p`，再按 `p(s',R)` 的概率跳到 `s'` 并把 `R \subseteq X` 中的时钟重置为 `0`。

### 一个最小例子与通俗解释

最小例子可以取一个“重试发送”实时协议：位置 `WaitAck` 中时钟 `x` 表示等待确认的时间，只要 `x \le 2` 都可以继续等；当 `x \ge 2` 时必须做一次离散选择，其中某个 distribution 以概率 `0.9` 进入 `Acked`，以概率 `0.1` 进入 `Lost` 并重置 `x` 开始下一轮。

通俗地说，`PTA` 就像“给 timed automata 的边外面再包一层骰子盒子”。普通 `TA` 只说“满足 guard 的边可以走”；`PTA` 则说“先选一个可用的概率盒子，再按盒子里写好的概率决定具体跳哪条边并 reset 哪些 clocks”。

### 运行 / 接受 / 转移语义

系统状态可以看成 location 与 clock valuation 的二元组：

$$
(s,\nu)
$$

时间推进遵循 invariant：

$$
(s,\nu) \xrightarrow{t} (s,\nu+t)
$$

并要求在延时过程中始终满足 `\mathrm{inv}(s)`。离散跳转则先要求某个分布 `p \in \mathrm{prob}(s)` 被当前 valuation 使能，即 `\nu \models \tau_s(p)`，随后以概率 `p(s',R)` 进入：

$$
(s,\nu) \xrightarrow{p} (s',\nu[R:=0])
$$

上式中的符号逐项解释如下：

1. `t \ge 0` 是延时。
2. `\nu+t` 表示所有 clocks 同速增长 `t`。
3. `p` 是在当前 location 可选的离散概率分布。
4. `R` 是这一步要 reset 的时钟集合。
5. `\nu[R:=0]` 表示把 `R` 中时钟置零，其余时钟保持原值。

### 语义边界

它仍然保持 `Timed Automata` 的 dense-time clock 语义，并没有进入连续动力学世界，所以不属于 `Hybrid Automata`。但它也不再是纯 timed-language 识别器，因为模型的核心对象是“带概率的 timed transition system”。

### 关键性质与判定边界

论文最关键的模型级收获不是一个简单复杂度定理，而是把分析链路固定下来：

$$
\text{PTA} \xrightarrow{\text{region construction}} \text{finite probabilistic region graph}
$$

并进一步引入：

$$
\text{PTCTL}
$$

作为同时表达时间与概率约束的逻辑。例如，“以至少 `0.7` 的概率，在 `5` 到 `7` 个时间单位内收到响应”这类性质可以直接写进 `PTCTL`。

论文还给出 zone-based probabilistic reachability 分析，用更粗的抽象替代精细 region graph，在实践上通常更小。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | location 仍是离散控制骨架。 |
| 事件 / 触发 | 支持 | 离散跳转取决于 enabled distributions。 |
| 守卫 / 数据 | 支持时钟守卫 | guard 体现在 invariant 和 enabling zones。 |
| 层次 | 不支持 | 原始模型不是层次状态机。 |
| 并发 / 同步 | 间接支持 | 论文重点是单体模型；并发通常通过网络组合到更大模型。 |
| 时间约束 | 强支持 | dense-time clocks 与 invariants 是核心。 |
| 连续动态 / 随机性 | 支持随机、不支持连续动力学 | 随机性来自离散概率分布。 |
| 可执行 / 可验证性 | 强理论支持 | `PTCTL`、region graph 和 probabilistic reachability 都给出。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$G=(S,L,\bar{s},X,\mathrm{inv},\mathrm{prob},\langle\tau_s\rangle)$` | `PTA` 的标准元组。 |
| 概率目标 | `$p : S\times 2^X \to [0,1]$` | 同时决定目标节点和 reset 集。 |
| 离散语义 | `$(s,\nu)\xrightarrow{p}(s',\nu[R:=0])$` | 先选 distribution，再按概率落到具体后继。 |
| 逻辑接口 | `$\mathrm{PTCTL}$` | 同时表达时间与概率的状态逻辑。 |
| 有限抽象 | `$\text{PTA} \to \text{finite region graph}$` | 使自动验证成为可能。 |

## 构造方式与承载格式

### 建模入口

1. 先确定 timed automata 的位置、时钟和 invariant。
2. 再把“原本一组可能的边”组织成若干 enabled probability distributions。
3. 为每个 distribution 指定其 enabling zone。
4. 最后决定分析目标是 `PTCTL` 还是 reachability。

### 机器可处理承载方式

机器可处理承载方式是 location graph、zones、reset 集与概率分布，而不是 XML / JSON / DSL。

### 交换与互操作

它与 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的经典 `Timed Automata` 母线、[event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md) 的可确定化规格分支，以及 [alternating-timed-automata/desc.md](../alternating-timed-automata/desc.md) 的布尔闭包分支都属于 `Timed Automata` 的理论扩展谱系。

## 配套基础设施

- 建模/编辑工具：原文未提供独立实现。
- 解析/交换/元模型支持：核心是 region graph、augmented regions 和 zone graph。
- 仿真/执行支持：可按概率分布和时钟演化解释运行。
- 验证/分析支持：`PTCTL` model checking、PBTL translation、probabilistic reachability upper-bound analysis。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于概率实时模型检查的经典理论入口。

## 适用场景与需求前提

### 适用场景

适合丢包协议、故障容错实时系统、带概率超时或成功率约束的通信/调度问题，以及需要同时问“多久”和“多大概率”的实时规格。

### 需求前提

1. 连续行为必须仍能用 clocks 表达，而不是一般微分方程。
2. 随机性应主要表现为离散跳转概率，而不是连续噪声。
3. 分析目标通常是 reachability、deadline satisfaction 或概率逻辑性质。

### 不适用或高成本场景

若系统含强连续动力学耦合，应转向 `Hybrid Automata` / stochastic hybrid 分支；若只需纯 deterministic / nondeterministic 时序约束，普通 `TA` 更简单。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，`PTA` 把“enabled edges”升级为“enabled probability distributions”；相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，它关心概率而不是确定化；相对 [o-minimal-hybrid-systems/desc.md](../o-minimal-hybrid-systems/desc.md)，它仍然停留在 clocks + zones 的离散时间抽象，不涉及连续流。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Timed Automata` 主干再补出一个经典的概率子枝，方便后续区分“纯时序控制逻辑”和“带概率可靠性约束的时序控制逻辑”。

### 作为目标形式主义还是中间表示

既可以作为目标验证模型，也可以作为从自然语言需求抽到 `TA` 之后的“概率化增强层”。

### 对需求到模型生成的启发

如果需求中反复出现“以多大概率在多久内完成”“丢包/重传/故障恢复概率”，LLM 不应只生成普通 `TA`；更自然的目标是 `PTA + PTCTL`。

### 现实限制

region graph 可能非常大；而且这类模型主要适合离散概率，不适合复杂连续随机过程。

## 重要的相关工作

### 奠基或前身工作

- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)

### 同类型或同家族工作

- [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)
- [alternating-timed-automata/desc.md](../alternating-timed-automata/desc.md)
- [timed-automata-with-urgent-transitions/desc.md](../timed-automata-with-urgent-transitions/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线，但 region/zone analysis 路线为后续 probabilistic real-time model checking 奠定了结构。

### 与本研究关系最紧的工作

- 它最适合作为 `Timed Automata -> Probabilistic Timed Automata` 的经典代表条目，并为后续在需求里抽取可靠性 / 成功率约束提供目标模型。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Probabilistic Timed Automata (PTA)`
- 论文角色：模型提出
- 核心功能：把 timed automata 扩成带离散概率分布的实时模型，并给出 `PTCTL` 与 probabilistic reachability 验证入口。
- 关键特性：enabled distributions、clock invariants、reset sets、region/zone abstractions、概率逻辑。
- 构造方式：`(S,L,\bar{s},X,\mathrm{inv},\mathrm{prob},\langle\tau_s\rangle)` + delay/discrete semantics。
- 基础设施：region graph、zone graph、`PTCTL/PBTL`，无工程标准/工具。
- 适用场景：带成功率/丢包率/故障概率约束的实时协议和控制逻辑。
- 需求前提：随机性主要体现在离散跳转概率，连续行为仍可由时钟建模。
- 状态：🟢

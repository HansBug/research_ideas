# 将医疗最佳实践指南转成可执行且可验证的状态图模型 / Transforming Medical Best Practice Guidelines to Executable and Verifiable Statechart Models

## 基本信息

- 标题：Transforming Medical Best Practice Guidelines to Executable and Verifiable Statechart Models
- 中文标题：将医疗最佳实践指南转成可执行且可验证的状态图模型
- 作者：Chunhui Guo，Shangping Ren，Yu Jiang，Po-Liang Wu，Lui Sha，Richard B. Berlin Jr.
- 发表：*ICCPS 2016*，pp.1-10，2016
- DOI：`10.1109/ICCPS.2016.7479121`
- 链接：http://dx.doi.org/10.1109/ICCPS.2016.7479121
- 形式主义：`Yakindu Statecharts / Y2U / UPPAAL Timed Automata bridge`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：Yakindu-to-UPPAAL translation / trace-back bridge for medical guidelines
- 工具/实现获取方式：论文明确给出 `Y2U` 网站入口 `www.cs.iit.edu/.../software/Y2U`，并说明使用 `Yakindu` 和 `UPPAAL` 完成建模、验证与 trace-back。
- 标准/格式获取方式：输入承载是 `Yakindu` statechart XML，输出承载是 `UPPAAL` XML timed automata 模型，以及从 `UPPAAL` counterexample 回映到 `Yakindu` 的状态/迁移对应关系。

## 简报

这篇论文不是单纯地把指南编码成状态图，而是把“临床可理解的可执行 `Yakindu` 状态图”与“形式验证可接受的 `UPPAAL` timed automata”中间打了一座桥。它最重要的地方有两层：一层是把 `Yakindu` 的 cycle-driven、同步、支持 simultaneous events 的语义尽可能保真地翻到 `UPPAAL`；另一层是验证失败后还能把 counterexample 路径 trace back 回原始 statechart。对文库来说，这正是一条典型的 `Statecharts -> TA backend` 方法路线。

- 形式主义定位：`Yakindu` 可执行状态图到 `UPPAAL` timed automata 的语义保持翻译与 trace-back 方法。
- 构造方式简述：定义 9 条 transformation rules，把 states、transitions、data types、events、timers、state actions、composite states、priority、synchrony 全部系统映射到 `UPPAAL`。
- 基础设施与场景简述：依托 `Yakindu`、`Y2U`、`UPPAAL` 和 trace-back procedure，适合既要和领域专家交互验证、又要做形式化安全验证的医疗工作流。

```text
medical guideline -> Yakindu statechart -> Y2U transformation -> UPPAAL timed automata -> property verification / counterexample -> trace back to Yakindu
```

## 形式主义定义与核心对象

### 定义对象

论文围绕三层对象组织方法：

1. `Yakindu` statechart 模型。
2. 经 `Y2U` 生成的 `UPPAAL` timed automata。
3. 失败性质对应的 trace-back 映射。

### 核心抽象

原文没有把 `Yakindu` 或 `Y2U` 总结成单一数学元组，但 transformation 关系可以保守写为：

$$
\mathcal{Y2U}: Y \mapsto U
$$

上式中的符号逐项解释如下：

1. `Y` 是输入 `Yakindu` statechart。
2. `U` 是输出 `UPPAAL` timed automata。
3. `\mathcal{Y2U}` 由 Rule 1 到 Rule 9 构成。

论文明确提出三条变换原则：

$$
\mathrm{P1}:\ \mathrm{Sem}(U)\equiv \mathrm{Sem}(Y),\qquad
\mathrm{P2}:\ U \text{ 尽量保持 } Y \text{ 的语法元素},\qquad
\mathrm{P3}:\ U \text{ 只引入最少附加元素}
$$

上式中的符号逐项解释如下：

1. `\mathrm{P1}` 追求执行语义等价。
2. `\mathrm{P2}` 追求语法元素可追踪。
3. `\mathrm{P3}` 追求 trace-back 复杂度最小。

为了在 `UPPAAL` 中模拟 `Yakindu` 的 simultaneous events，论文引入 event stack，可保守写成：

$$
\mathcal{E} = (n,\ e_1,\ldots,e_n,\ \mathrm{push},\ \mathrm{isEventValid},\ \mathrm{empty})
$$

上式中的符号逐项解释如下：

1. `n` 是当前 valid event 数量。
2. `e_i` 是当前 time cycle 内有效事件。
3. `\mathrm{push}` 用于压入新事件。
4. `\mathrm{isEventValid}` 用于在 guard 中判断事件是否有效。
5. `\mathrm{empty}` 在一个 cycle 结束时清空事件栈。

论文的 transition priority 规则也可压成形式化条件。若某状态有按优先级排序的 guard `G_1,\ldots,G_n`，则第 `i` 条转移的新 guard 为：

$$
G_i' = G_i \land \neg G_1 \land \neg G_2 \land \cdots \land \neg G_{i-1}
$$

上式中的符号逐项解释如下：

1. `G_i` 是原始 guard。
2. `G_i'` 是写回 `UPPAAL` 后的 guard。
3. 它保证高优先级转移先于低优先级转移发生。

### 一个最小例子与通俗解释

论文用多个小规则图说明转换，最直观的最小例子是 `every 5s` timer：

1. 在 `Yakindu` 中，某状态带 `every 5s` timing trigger。
2. `Y2U` 为它新建一个 `clock t` 和同步 channel `every5s`。
3. 再增加一个辅助 timer automaton，要求 `t <= 5`，当 `t == 5` 时执行 `every5s!` 并 reset `t := 0`。
4. 主 automaton 则通过 `every5s?` 接收该定时触发。

通俗地说，`Y2U` 像“把 `Yakindu` 里很多 `UPPAAL` 没有的一等语法，比如 event、timer、entry/exit、复合状态、同步执行顺序，都拆成一组显式的 `UPPAAL` automata、channels、guards 和 helper functions”。这样既能验证，又能把失败路径映回原图。

### 运行 / 接受 / 转移语义

论文对正确性的核心说法是“observable executions 等价”。可保守写成：

$$
\mathrm{ObsExec}(Y) = \mathrm{ObsExec}(U)
$$

上式中的符号逐项解释如下：

1. `\mathrm{ObsExec}` 表示对外可观察执行。
2. 论文把它具体化为：相同输入下，两边有相同的执行路径，且每步变量值一致。

同步执行部分通过 lockstep indicators 建模。若自动机按优先级排序为 `A_1,\ldots,A_n`，其同步指示器可概括为：

$$
I_j < I_{j-1}\quad (j>1),\qquad
I_1 = I_2 = \cdots = I_n
$$

上式中的符号逐项解释如下：

1. `I_j` 是 automaton `A_j` 当前 cycle 内已执行步数的指示器。
2. 高优先级 automata 必须先推进。
3. 一个 cycle 结束时，各 automata 执行步数被对齐。

论文随后给出：

$$
\text{Theorem 1: } U \text{ maintains the execution behaviors of } Y
$$

以及 trace-back 关系：

$$
S_U \to S_Y \text{ is bijective},\qquad T_U \to T_Y \text{ is surjective but not injective}
$$

上式中的符号逐项解释如下：

1. `S_U,S_Y` 是 `UPPAAL/Yakindu` 状态集合。
2. `T_U,T_Y` 是两边迁移集合。
3. 状态一一对应，而某些 `UPPAAL` 辅助迁移仅用于模拟语义，不能一一映回 `Yakindu` 原始迁移。

### 语义边界

1. 论文关注 `Yakindu` 到 `UPPAAL` 的 bridge，不是一般 `UML Statecharts` 母语义。
2. 其 transformation rules 只覆盖基本元素，choice / junction / history 这类 syntactic sugar 本文不处理。
3. 正确性论证采取 observable execution equivalence，而不是更强的形式双模拟框架。
4. 场景强绑定医疗最佳实践指南，但方法本体可外溢到其他 `Yakindu` 状态图。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 变换映射 | `$\mathcal{Y2U}: Y \mapsto U$` | `Y2U` 把 `Yakindu` 模型系统翻译为 `UPPAAL`。 |
| 三原则 | `$\mathrm{P1},\mathrm{P2},\mathrm{P3}$` | 语义保持、语法保留、附加元素最少。 |
| 事件栈 | `$\mathcal{E}=(n,e_1,\ldots,e_n,\mathrm{push},\mathrm{isEventValid},\mathrm{empty})$` | 用于模拟 simultaneous events。 |
| 优先级 guard | `$G_i' = G_i \land \neg G_1 \land \cdots \land \neg G_{i-1}$` | 在 `UPPAAL` 中重建 `Yakindu` 转移优先级。 |
| 执行等价 | `$\mathrm{ObsExec}(Y)=\mathrm{ObsExec}(U)$` | 正确性主张的核心。 |
| trace-back 关系 | `$S_U \to S_Y$ bijective, `$T_U \to T_Y$ surjective not injective` | 解释为什么能回溯状态而迁移需过滤辅助边。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `Yakindu` statechart 是输入主语义。 |
| 事件 / 触发 | 很强 | 论文专门为 events 和 simultaneous events 设计 event stack。 |
| 守卫 / 数据 | 很强 | guards、更新、实数/字符串近似编码都覆盖。 |
| 层次 | 很强 | composite states flattening 是核心规则之一。 |
| 并发 / 同步 | 很强 | synchronous execution 和 automaton priority 都被显式编码。 |
| 时间约束 | 很强 | timers 和 `UPPAAL` timed automata 是后端核心。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | `Yakindu` 负责可执行和临床验证，`UPPAAL` 负责形式验证。 |

### 形式化问题与性质

1. 这篇论文最重要的不是“能翻译”，而是“翻译后还能 trace back”。
2. `Yakindu` 的 cycle-driven、deterministic、simultaneous-events 语义是桥接难点，也是本文真正补上的方法价值。
3. 对文库来说，它和 `UPP2SF` 一样，都是“把一个较易执行/易理解载体接到验证后端”的关键桥梁。

## 构造方式与承载格式

### 建模入口

原文中的建模顺序非常清楚：

1. 先用 `Yakindu` 建 best-practice guideline statechart。
2. 让医生通过 `Yakindu` 模拟先做临床验证。
3. 用 `Y2U` 自动翻成 `UPPAAL` timed automata。
4. 再在 `UPPAAL` 上验证 safety properties。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Yakindu` XML。
2. `UPPAAL` XML。
3. timer automata、event automata 和 lockstep-related 辅助结构。
4. state / transition mapping information。
5. counterexample trace-back path。

### 交换与互操作

1. 这篇论文本质上就是互操作 bridge。
2. 输入侧是 `Yakindu` statechart。
3. 输出侧是 `UPPAAL` timed automata。
4. 失败路径还能再从 `UPPAAL` 回到 `Yakindu`。

## 配套基础设施

- 建模/编辑工具：`Yakindu` statechart tool 用于建模与和医生交互验证。
- 解析/交换/元模型支持：`Y2U` 解析 `Yakindu` XML，生成 `UPPAAL` XML，并维护 state/transition mapping。
- 仿真/执行支持：`Yakindu` 提供 simulation 和可执行原型；`UPPAAL` 提供 formal verification。
- 验证/分析支持：安全性质验证、counterexample 生成、trace-back 过程。
- 代码生成/转换支持：`Yakindu` 本身具代码生成功能，论文强调之所以选它就是因为它既能执行又能作为后续实现载体。
- 标准化或社区生态：依赖 `Yakindu` 与 `UPPAAL` 两大成熟生态，`Y2U` 负责桥接。

## 适用场景与需求前提

### 适用场景

适合那些既需要领域专家先看得懂、跑得动，又必须进一步做形式化验证的医疗流程、临床指南和人机协同决策流程。

### 需求前提

1. 需求可先整理成 `Yakindu` statechart。
2. 系统关键问题仍然是离散流程和时间触发，而不是连续动力学。
3. 团队希望保留医生/领域专家可理解的可执行模型，而不是一开始就直接写 `UPPAAL`。

### 不适用或高成本场景

1. 若需求天然就应直接写成 timed automata，`Yakindu -> UPPAAL` 这层桥可能多余。
2. 若模型依赖大量 `Yakindu` syntactic sugar，本文规则未必直接覆盖。
3. 若最终完全不需要 trace-back，仅需简单翻译，方法中的一些保守约束会显得偏重。

## 与相邻形式主义的关系

1. 相比直接把指南写成 `UPPAAL`，这条路线保留了更强的可解释性和可执行性。
2. 相比 `UML Statecharts -> UPPAAL` 旧桥接工作，它专门处理 `Yakindu` 的 cycle-driven 语义差异。
3. 与 `UPP2SF` 一样，它属于“验证桥”，但方向相反：本文是 `Statechart -> Timed Automata`，`UPP2SF` 是 `Timed Automata -> Stateflow`。
4. 与普通 `Yakindu` 工具链相比，本文最关键的新增能力是 formal verification 和 trace-back。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 的直接价值很高，因为它提供了“状态机自动建模之后，如何接到正式验证后端并保持可追溯”的完整范式，尤其适合医疗和安全关键需求。

### 作为目标形式主义还是中间表示

`Yakindu` 可以作为较友好的中间表示，`UPPAAL` 则是强验证后端。两者之间的桥说明文库不一定只能追求单一终态形式主义。

### 对需求到模型生成的启发

1. 对于文本需求，先生成可读、可执行的 `Statechart`，再翻到验证后端，往往比直接生成底层形式模型更现实。
2. 若希望后续 trace-back，生成时就要保留状态和迁移的稳定映射。
3. 事件、定时器、priority 和 hierarchy 等高层语义必须在翻译前先被规范化。

### 现实限制

1. 论文针对 `Yakindu`，不是任意 statechart 方言都能直接套用。
2. 规则集合较多，维护成本不低。
3. correctness 论证偏工程化和构造式，而不是全形式证明。

## 重要的相关工作

### 奠基或前身工作

1. `Yakindu` 是原始可执行状态图前端。
2. `UPPAAL` 是验证后端。

### 同类型或同家族工作

1. 论文明确提到 `UML statecharts`、`HTA`、`RT-DEVS`、`POOSL` 到 `UPPAAL` 的已有翻译工作。
2. 这些工作大多不能直接用于 `Yakindu`，因为其执行语义不同。

### 标准 / 格式 / 工具链工作

1. `Y2U` 是本文的核心桥接工具。
2. event stack、timer automata、lockstep 同步都是工具链级工程构件。

### 与本研究关系最紧的工作

1. 与 `UPP2SF`、`Sismic`、`ArmarX`、`Gamma`、`USM2C` 等文库条目一起构成 statechart execution / verification bridge 线。
2. 对医疗方向，它还是“临床验证 + 形式验证双通道”路线的重要实例。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Yakindu Statecharts / Y2U / UPPAAL Timed Automata bridge`
- 论文角色：Yakindu-to-UPPAAL translation / trace-back bridge for medical guidelines
- 核心功能：把可执行 `Yakindu` 状态图自动翻成可验证 `UPPAAL` timed automata，并支持失败路径回溯。
- 关键特性：9 条 transformation rules、event stack、timer automata、priority/synchrony encoding、trace-back mapping。
- 构造方式：`Yakindu` XML -> `Y2U` rules -> `UPPAAL` XML -> verification / counterexample -> trace-back。
- 基础设施：`Yakindu`、`Y2U`、`UPPAAL`、state/transition mapping、counterexample trace-back。
- 适用场景：医疗指南、临床流程与其他需同时面向领域专家解释和形式化验证的 statechart-driven systems。
- 需求前提：流程可先表达为 `Yakindu` statechart，且关键复杂度主要来自离散流程、事件和 timers。
- 状态：🟢 直接可用

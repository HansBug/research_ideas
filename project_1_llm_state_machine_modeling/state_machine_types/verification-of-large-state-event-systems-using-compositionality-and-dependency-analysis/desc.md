# 大规模 State/Event 系统的组合性与依赖分析验证 / Verification of Large State/Event Systems Using Compositionality and Dependency Analysis

## 基本信息

- 标题：Verification of Large State/Event Systems Using Compositionality and Dependency Analysis
- 中文标题：大规模 State/Event 系统的组合性与依赖分析验证
- 作者：Jørn Lind-Nielsen, Henrik Reif Andersen, Henrik Hulgaard, Gerd Behrmann, Kåre Kristoffersen, Kim G. Larsen
- 发表：*Formal Methods in System Design*, 18(1):5-23, 2001
- DOI：`10.1023/A:1008736219484`
- 链接：https://doi.org/10.1023/A:1008736219484
- 形式主义：`State/Event Machines / Systems (SEM / S/E systems)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / `SEM` family stabilization
- 工具/实现获取方式：原文明确以 `visualSTATE` 为实现载体；机器可处理入口是并发 `SEM` 集合、局部机三元组、同步输入事件、guarded transitions 与 dependency analysis。
- 标准/格式获取方式：原文没有独立 DSL 标准或交换格式；核心承载方式是 `SEM` 机三元组、guard 表达式与 `visualSTATE` 中的同步状态机模型。

## 简报

这篇论文的重要性不在“又做了一次验证优化”，而在于它把 `State/Event model` 明确钉成了一类独立的状态机 family：它是 `Mealy machine` 的并发同步扩展，可被看成 `StateCharts / RSML` 的收束化、工程可落地但又保持 automata 骨架的版本。对当前演化树而言，这篇论文给了 `SEM` 一个足够稳定的 journal 级锚点，使后面的 `HSEM` 不再像凭空长出来，而是明确从“并发 `SEM` + guards + synchronous reaction”这条父线上演化出来。

- 形式主义定位：`Statecharts` 工程直觉和 `Mealy machine` 自动机骨架之间的一条简化母线，核心是同步事件驱动的并发有限状态机。
- 构造方式简述：系统由若干局部 `SEM` 并发组成；每台机器在输入事件上同步反应，迁移由外部事件和对其他机器局部状态的 guard 共同触发。
- 基础设施与场景简述：原文直接绑定 `visualSTATE`，既用于 consistency / reachability checking，也用于从模型生成嵌入式控制代码。

```text
控制逻辑分解 -> 多个局部 SEM -> 同步输入事件 + 跨机 guard -> 全局并发状态机 -> 验证 / 代码生成
```

## 形式主义定义与核心对象

### 定义对象

`SEM` 的基本对象不是单个 flat `FSM`，而是一组同步运行的局部状态机。每台机器都像一台带输入事件、guard 和输出动作的 `Mealy` 机，但系统语义不是异步 product，而是“同一输入事件到来时全部相关机器一起迈一步”的 lock-step 反应。

### 核心抽象

原文先把单台 `SEM` 机器写成三元组：

$$
M_i = (S_i, s_i^0, T_i)
$$

上式中的符号逐项解释如下：

1. `S_i` 是第 `i` 台局部机器的状态集合。
2. `s_i^0` 是该局部机器的初始状态。
3. `T_i` 是该局部机器的迁移关系。

对应的迁移关系满足：

$$
T_i \subseteq S_i \times E \times G_i \times M(O) \times S_i
$$

上式中的符号逐项解释如下：

1. `E` 是输入事件字母表。
2. `G_i` 是不引用机器 `i` 自身位置变量的 guard 集合。
3. `M(O)` 是输出动作的多重集。
4. 一条迁移同时给出“当前局部状态、输入事件、guard、输出动作、后继局部状态”。

原文把整个 `SEM` 系统理解为 `n` 台机器的并发组合。可保守整理成：

$$
\mathcal M = (E, O, M_1, \ldots, M_n)
$$

这不是论文显式给出的 canonical tuple，而是根据原文 “a state/event system consists of `n` machines over input alphabet `E` and output alphabet `O`” 的保守整理。

### 一个最小例子与通俗解释

一个最小例子可以是“列车移动 + 道口关闭”双机控制器：

1. 机器 `M_1` 管列车，状态为 `Stop / Move`。
2. 机器 `M_2` 管道口，状态为 `Open / Closed`。
3. 在输入事件 `Go` 到来时，`M_1` 只有在 guard `M_2 = Closed` 成立时才能从 `Stop` 迁到 `Move`。
4. 若 `Go` 到来而某台机器没有可用迁移，它就保持原地不动。

通俗地说，`SEM` 像“几台会同时听口令的 `Mealy` 机”。普通 `FSM` 只管自己的输入输出；`SEM` 额外允许“我能不能动，要看别人现在停在哪个局部状态”。

### 运行 / 接受 / 转移语义

原文把全局状态空间定义为局部状态空间的直积：

$$
S = S_1 \times S_2 \times \cdots \times S_n
$$

上式中的符号逐项解释如下：

1. `S_i` 是第 `i` 台局部机器的状态集合。
2. `S` 是整个 `SEM` 系统的全局状态集合。
3. 一个全局状态 `s \in S` 记录了每台局部机器当前所在的位置。

在全局状态 `s` 上，所有 guard 都可先被求值，再决定哪些局部迁移在输入事件 `e` 上被触发。可把同步反应压成：

$$
s \xrightarrow{e,\,o} s'
$$

其中 `s'` 由各局部机器在同一输入 `e` 上的下一状态拼成，而总输出满足

$$
o = o_1 \uplus o_2 \uplus \cdots \uplus o_n
$$

这里的符号逐项解释如下：

1. `o_i` 是第 `i` 台机器在该步产生的局部输出多重集。
2. `\uplus` 表示多重集并。
3. 若某台机器在事件 `e` 上无 enabled transition，它保持原状态，相当于贡献空输出。

### 语义边界

`SEM` 的边界很清楚：

1. 它仍是纯离散、有限控制模型。
2. 它有并发和跨机 guard，但没有 hierarchy、call-return、clocks 或连续变量。
3. 它强调同步反应和局部状态依赖，不是共享变量程序语义。
4. 它比普通 `Mealy machine` 强在并发与 guard；比后续 `HSEM` 弱在没有嵌套状态。

### 关键性质与判定边界

这篇论文主要关心的判定问题是 reachability / deadlock / consistency。可保守写成：

$$
\text{Given } g \subseteq S,\ \text{decide whether } \exists s \in \mathrm{Reach}(\mathcal M): s \in g
$$

上式中的符号逐项解释如下：

1. `S` 是全局状态集合。
2. `g` 是目标 guard 或目标全局状态集合。
3. `\mathrm{Reach}(\mathcal M)` 是从初始全局状态出发可达的全局状态集合。

原文的核心不是给出新的复杂度等级，而是说明：通过 compositionality 与 dependency analysis，可以只逐步纳入和目标 guard 真正相关的局部机器，而不必一次性展开全部并发组合。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 以多个局部有限状态机组成。 |
| 事件 / 触发 | 强支持 | 输入事件是同步反应的主触发器。 |
| 守卫 / 数据 | 部分支持 | guard 允许引用其他机器的局部状态，但不引入一般变量数据域。 |
| 层次 | 不支持 | 本文还是 flat `SEM`，层次在后续 `HSEM` 才出现。 |
| 并发 / 同步 | 强支持 | 多台机器对同一输入事件 lock-step 反应。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强支持 | 原文直接落到 `visualSTATE` 的 symbolic verification 与 code generation。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单机骨架 | `$M_i=(S_i,s_i^0,T_i)$` | `SEM` 的最小局部单元。 |
| 迁移关系 | `$T_i \subseteq S_i \times E \times G_i \times M(O) \times S_i$` | 输入事件、guard、输出动作一体化。 |
| 全局状态 | `$S=S_1 \times \cdots \times S_n$` | 并发系统的语义空间。 |
| 同步反应 | `$s \xrightarrow{e,o} s'$` | 所有局部机在同一输入事件上联合迈步。 |
| 输出聚合 | `$o=o_1 \uplus \cdots \uplus o_n$` | 系统输出是局部输出的多重集并。 |

## 构造方式与承载格式

### 建模入口

1. 先把控制逻辑拆成若干局部有限状态机。
2. 为每条局部迁移指定输入事件、guard 和输出动作。
3. 再用局部状态依赖把跨机约束压进 guard。
4. 最后把所有局部机器放到同步反应语义下组成一个并发 `SEM`。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. 局部机三元组 `(S_i,s_i^0,T_i)`。
2. guard 布尔表达式与对应的全局状态集合解释。
3. 全局状态直积与局部迁移的同步合成。
4. `visualSTATE` 中的状态机图与后端符号编码。

### 交换与互操作

原文没有独立交换格式，但谱系意义很强：

1. 它把 `Mealy` 式边输出自动机推进成并发同步控制 family。
2. 它为后续 [verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md](../verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md) 提供了直接父线。
3. 它把 `StateCharts / RSML` 的工程直觉收束成更轻量的 automata-theoretic 骨架。

## 配套基础设施

- 建模/编辑工具：原文明确依托 `visualSTATE`。
- 解析/交换/元模型支持：核心是局部机、guard 与同步合成的内部符号表示；无独立公开交换标准。
- 仿真/执行支持：`visualSTATE` 支持模型操纵、模拟与代码生成。
- 验证/分析支持：symbolic model checking、backward reachability、dependency-guided compositional checking。
- 代码生成/转换支持：原文明确指出可从模型自动生成嵌入式软件代码。
- 标准化或社区生态：研究与商业工具结合的 family，但没有像 `SCXML` 那样的独立标准文本载体。

## 适用场景与需求前提

### 适用场景

适合：

1. 事件驱动的嵌入式控制逻辑。
2. 可以自然拆成多个局部控制器、又需要同步反应的系统。
3. 需要把验证和代码生成接在同一控制模型上的场景。

### 需求前提

1. 系统主复杂度来自离散控制，而不是连续动态。
2. 局部组件之间的耦合可用“其他机器当前局部状态”形式表达。
3. 全局行为仍可由有限个局部状态机及其同步组合覆盖。

### 不适用或高成本场景

如果需求核心是嵌套 superstate、history 或 parallel state inside state，应转向 [verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md](../verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md)；如果核心是 call-return 递归结构，则更接近 [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)。

## 与相邻形式主义的关系

相对普通 `Mealy machine`，`SEM` 加入了并发局部机、同步输入反应和跨机 guard；相对 `StateCharts / RSML`，它更克制，没有把 hierarchy、history、broadcast 内部事件等全部装进来；相对 `HSM`，它不是通过 boxes / entry-exit 做 hierarchy，而是通过并发机 + guard 做同步控制。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文给 `project_1` 提供了一条非常有用的中间母线：在 `FSM/Mealy` 与更复杂的 `Statecharts/HSM/HSEM` 之间，先有一个“同步并发但仍保持 automata 骨架”的 `SEM`。

### 作为目标形式主义还是中间表示

更适合作为中间表示或谱系父节点。它比 plain `FSM` 强，但还不够表达层次控制。

### 对需求到模型生成的启发

当需求文本明显包含“多个局部控制单元同时听同一事件、并根据彼此当前位置协同反应”时，目标输出不应停留在单机 `FSM`，而应提升到 `SEM` 这类同步并发 family。

### 现实限制

它的外部开放生态明显不如后来的标准 DSL；同时，模型主要面向控制部分，不适合承载复杂数据流或时钟约束。

## 重要的相关工作

### 奠基或前身工作

- [a-method-for-synthesizing-sequential-circuits/desc.md](../a-method-for-synthesizing-sequential-circuits/desc.md)
- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)

### 直接后继

- [verification-of-state-event-systems-by-quotienting/desc.md](../verification-of-state-event-systems-by-quotienting/desc.md)
- [verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md](../verification-of-hierarchical-state-event-systems-using-reusability-and-compositionality/desc.md)

## 文献分类总结

- 这是一篇 `🧩 经典离散状态机` 文献，因为主体仍是有限离散控制与自动机式迁移，而不是时间、混成或接口契约模型。
- 这是一篇 `🧱 模型本体` 文献，因为虽然题目带 verification，但正文实际稳定定义了 `SEM` 的对象、同步语义、guard 机制和机器组合骨架。
- 这篇论文的描述客体是 `🎛️ 控制 / 反应式逻辑`，因为其原生对象是嵌入式反应式控制器，而不是字符串、树或接口协议。
- 这篇论文属于 `🧮 形式语言与自动机理论`，因为其核心贡献是把一类并发状态机 family 的结构和语义收束清楚，并直接服务后续谱系扩树。

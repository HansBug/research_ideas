# 带输入决定守卫的时间自动机 / On timed automata with input-determined guards

## 基本信息

- 标题：On timed automata with input-determined guards
- 中文标题：带输入决定守卫的时间自动机
- 作者：Deepak D'Souza、Nicolas Tabareau
- 发表：*arXiv preprint* `cs/0601096`, 2006；相关会议版本发表于 *Formal Techniques, Modelling and Analysis of Timed and Fault-Tolerant Systems* (FORMATS/FTRTFT 2004), pp. 68-83
- DOI：`10.48550/arXiv.cs/0601096`
- 链接：https://arxiv.org/pdf/cs/0601096
- 形式主义：`Input-Determined Timed Automata (IDA)`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 timed words、input-determined operators、symbolic alphabets 与基于这些守卫的 Büchi automata。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 timed word、operator 语义函数、guard 语法和 symbolic / proper symbolic alphabet。

## 简报

这篇论文的关键，不是再给普通 `Timed Automata` 加一个新 clock 语法，而是把“时钟或守卫的真假由输入 timed word 本身唯一决定”抽象成统一 operator 机制。这样一来，`Event-Clock Automata` 之类早先的可确定化 timed-specification family，就被提升成一个更一般的 `Input-Determined Timed Automata` 母类。对当前文库来说，这个节点能把 `Timed Automata` 的 event-clock 支线和后来的 counter-free / logic-characterization 支线连成一条完整分支。

- 形式主义定位：`Timed Automata` 主干上的“由输入 timed word 决定守卫真值”的规格自动机母节点。
- 构造方式简述：先定义 input-determined operator，再用 `I \in \Delta` 这类 guard 组装 symbolic alphabet，最后把普通 `Büchi` 自动机放到该字母表上运行。
- 基础设施与场景简述：原文是纯理论工作，但 determinization、boolean closure、`TMSO` 对应与 timed temporal logic 对应都非常完整。

```text
timed word -> input-determined operators -> guards over intervals -> symbolic alphabet -> Büchi-style timed specification automaton
```

## 形式主义定义与核心对象

### 定义对象

论文工作的对象是 infinite timed words 上的 pointwise semantics。与普通 `Timed Automata` 不同，这里不把 clock value 看成“automaton 沿某条路径如何 reset 的结果”，而把 guard 真值直接看成 timed word 在某个位置上的可观测属性。

### 核心抽象

一个 input-determined operator 的语义函数写成：

$$
\llbracket \Delta \rrbracket : (T\Sigma^\omega \times \mathbb N) \to 2^{I_{\mathbb Q}}
$$

上式中的符号逐项解释如下：

1. `T\Sigma^\omega` 是字母表 `\Sigma` 上的 infinite timed words 集合。
2. `\mathbb N` 表示 timed word 的离散动作位置，而不是任意实数时刻。
3. `I_{\mathbb Q}` 是以有理端点表示的时间区间集合。
4. `\llbracket \Delta \rrbracket(\sigma,i)` 返回在 timed word `\sigma` 的第 `i` 个动作点上，由 operator `\Delta` 识别到的一组区间。

基于 operator 的 guard 语法写成：

$$
g ::= \top \mid I \in \Delta \mid \neg g \mid g \lor g \mid g \land g
$$

上式中的符号逐项解释如下：

1. `I \in \Delta` 表示当前位置上，operator `\Delta` 所识别的区间集合包含区间 `I`。
2. 其余连接词都是普通布尔组合。

在此基础上，论文把 `IDA` 定义成基于 symbolic alphabet 的 `Büchi` 自动机。可保守写成：

$$
A = (Q, s, \rightarrow, F)
$$

其中：

1. `Q` 是有限状态集。
2. `s` 是初始状态。
3. `\rightarrow \subseteq Q \times \Gamma \times Q` 是基于 symbolic alphabet `\Gamma` 的转移关系。
4. `F` 是 `Büchi` 接受状态集。

其 timed language 写成：

$$
L(A) = tw(L_{\mathrm{sym}}(A))
$$

这里的 `L_{\mathrm{sym}}(A)` 是 symbolic language，而 `tw` 把 symbolic word 集翻译回 timed-word language。

### 一个最小例子与通俗解释

论文给出的直观 operator 之一，是“未来某个 `a` 会在多远之后出现”的 eventual operator。若把它记成 `\Diamond_a`，那么“从当前位置起 3 个时间单位内存在一个 `b`”可写成：

$$
[0,3] \in \Diamond_b
$$

于是“每个 `a` 之后 3 个时间单位内必须有一个 `b`”就可以由自动机在读到 `a` 后进入一个要求该 guard 成立的状态来表达。

通俗地说，`IDA` 像是“不给自动机自由 reset clock，而是直接让 timed word 自己决定哪些时间距离关系成立”的 timed automaton。它牺牲了普通 `TA` 的一部分编程自由，换来更好的 determinization 和逻辑刻画。

### 运行 / 接受 / 转移语义

对 timed word `\sigma = (a_0,t_0)(a_1,t_1)\cdots`，自动机在位置 `i` 看到的不是一般时钟 valuation，而是由 `\sigma` 自己决定的 operator 语义。因此一条接受运行仍是普通 `Büchi` 形式：

$$
q_0 \xrightarrow{\gamma_0} q_1 \xrightarrow{\gamma_1} q_2 \xrightarrow{\gamma_2} \cdots
$$

并要求：

$$
q_0 = s,\quad q_i \in F \text{ infinitely often}
$$

关键差别在于每个 `\gamma_i` 的 guard 真值不是由 automaton 自己的 reset 历史决定，而是由输入 timed word 在第 `i` 个动作点唯一决定。

### 语义边界

论文明确强调了两条边界：

1. 结果成立于 pointwise semantics，而不是任意实数时间点都可评估的 continuous semantics。
2. 作者不主张对所有 operator 都能保住 decidability；某些更强 operator 会把 emptiness 推到不可判。

因此 `IDA` 的价值首先是“逻辑框架和 family 抽象”，其次才是具体 decision procedure。

### 关键性质与判定边界

论文的第一个核心结论，是该 family 对布尔运算有效封闭：

$$
\mathrm{IDA}(\Sigma,\mathrm{Op}) \text{ is effectively closed under union, intersection, and complement}
$$

第二个关键结论，是它与 timed monadic second-order logic 对齐：

$$
L \text{ definable by an IDA } \iff L \text{ definable in } \mathrm{TMSO}(\Sigma,\mathrm{Op})
$$

第三个结论，是存在与之 expressively complete 的 timed temporal logic：

$$
\mathrm{IDA}(\Sigma,\mathrm{Op}) \equiv \mathrm{TMSO}(\Sigma,\mathrm{Op}) \equiv \mathrm{TLTL}(\Sigma,\mathrm{Op})
$$

其中 `TLTL` 是论文给出的 timed temporal logic 口径。这三个等价关系一起说明：`IDA` 不是一篇 ad hoc 小变体，而是一个足够稳的 timed-specification 母节点。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍有普通 Büchi 自动机的有限控制骨架。 |
| 事件 / 触发 | 强支持 | 按 timed word 上的离散动作点推进。 |
| 守卫 / 数据 | 支持时间守卫、不支持一般数据 | guard 围绕 `I \in \Delta` 这样的 operator-interval 谓词。 |
| 层次 | 不支持 | 原始模型不是层次自动机。 |
| 并发 / 同步 | 不支持 | 论文关注的是 timed-word language，而非组件并发组合。 |
| 时间约束 | 强支持 | 时间关系通过 operator 直接成为一等对象。 |
| 连续动态 / 随机性 | 不支持 | 没有连续流或概率机制。 |
| 可执行 / 可验证性 | 强理论支持 | determinization、boolean closure、逻辑刻画都很强，但一般 emptiness 不保证可判。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| operator 语义 | `$\llbracket \Delta \rrbracket : (T\Sigma^\omega \times \mathbb N) \to 2^{I_{\mathbb Q}}$` | 把“由输入决定的时间观察”正式函数化。 |
| guard 语法 | `$g ::= \top \mid I \in \Delta \mid \neg g \mid g \lor g \mid g \land g$` | timed guard 只依赖 operator 结果。 |
| automaton 骨架 | `$A=(Q,s,\rightarrow,F)$` | `IDA` 本体仍是 symbolic alphabet 上的 `Büchi` 自动机。 |
| timed language | `$L(A)=tw(L_{\mathrm{sym}}(A))$` | 明确 symbolic language 与 timed language 的接口。 |
| 逻辑刻画 | `$\mathrm{IDA} \equiv \mathrm{TMSO} \equiv \mathrm{TLTL}$` | 说明该 family 是完整的 timed-specification 层。 |

## 构造方式与承载格式

### 建模入口

建模时通常按以下顺序进行：

1. 先确定需求依赖哪些“由 timed word 决定的时间距离”。
2. 再为这些时间观察定义 input-determined operators。
3. 用 `I \in \Delta` 形式写 guard。
4. 最后在 symbolic alphabet 上组装 `Büchi` 自动机。

### 机器可处理承载方式

原文的机器可处理承载方式是 timed words、guards、symbolic alphabets 和 proper symbolic alphabets，而不是 XML / DSL 文件。

### 交换与互操作

它和以下条目关系最紧：

1. [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：普通 `Timed Automata` 母线。
2. [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)：`IDA` 显式吸收并推广了该 family。
3. [counter-free-input-determined-timed-automata/desc.md](../counter-free-input-determined-timed-automata/desc.md)：在当前母线下继续加上 counter-free 约束与 `TFOc` 刻画。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 symbolic alphabet、proper symbolic alphabet 和 operator semantics。
- 仿真/执行支持：可按 timed word 逐位置扫描 symbolic word。
- 验证/分析支持：determinization、boolean closure、`TMSO` 和 `TLTL` 对应。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：属于 timed automata 理论里连接 event-clock family 与 timed logics 的经典抽象节点。

## 适用场景与需求前提

### 适用场景

适合那些把需求天然写成 timed words 上的过去/未来时间距离约束，并希望保留 determinizable specification view 的场景。

### 需求前提

1. 需求对象应能自然表示成 timed event stream。
2. 时间约束最好能直接由输入序列上的事件时距决定。
3. 若目标是 logic characterization 或 specification closure，这个 family 特别合适。

### 不适用或高成本场景

若需求依赖 automaton 自己主动 reset clocks、复杂并发网络或连续变量流，普通 `Timed Automata`、timed game / hybrid families 更自然。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，`IDA` 最大变化是 guard 真值由输入 timed word 决定，而不是由 automaton 自己的 reset 历史决定；相对 [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)，它把 event clocks 上升成更一般的 input-determined operator；相对 [counter-free-input-determined-timed-automata/desc.md](../counter-free-input-determined-timed-automata/desc.md)，后者是在这条母线上进一步切出逻辑对应的 counter-free 子类。

## 与本研究的关系

### 对 Project 1 的价值

它能把现有 `Timed Automata -> Event-Clock Automata` 的零散节点，重整成一条更清晰的 `Input-Determined` 分支，再向下接 `Counter-Free` 子类。

### 作为目标形式主义还是中间表示

它更适合作为 timed specification / logic 中间表示，而不是工业控制器的最终执行模型。

### 对需求到模型生成的启发

如果自然语言需求反复出现“某事件之后多久必须发生另一事件”“未来某个窗口内是否会出现某类事件”这类表达，LLM 先生成 input-determined operators 往往比直接拼 reset-heavy `TA` 更稳定。

## 重要的相关工作

1. [event-clock-automata-a-determinizable-class-of-timed-automata/desc.md](../event-clock-automata-a-determinizable-class-of-timed-automata/desc.md)：`IDA` 的最直接前身和特例。
2. [counter-free-input-determined-timed-automata/desc.md](../counter-free-input-determined-timed-automata/desc.md)：同一条母线上的 counter-free 逻辑刻画。
3. [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)：普通 `Timed Automata` 母线。

## 文献分类总结

- 这是一篇 `🧱 模型本体` 条目，因为它提出并稳定命名了 `Input-Determined Timed Automata` 这一族，而不是只做某个 logic 的 case study。
- 它应挂在 `Timed Automata` 主干下，并作为 `Event-Clock` 与 `Counter-Free Input-Determined` 之间的母节点。
- 它不是 DSL、工具或应用论文；其核心价值在 family abstraction 与 logic characterization。

# 数据词上的类计数自动机 / Class Counting Automata on Datawords

## 基本信息

- 标题：Class Counting Automata on Datawords
- 中文标题：数据词上的类计数自动机
- 作者：Amaldev Manuel, R. Ramanujam
- 发表：*International Journal of Foundations of Computer Science*, 22(4):863-882, 2011
- DOI：`10.1142/S0129054111008465`
- 链接：https://doi.org/10.1142/S0129054111008465
- 形式主义：`Class Counting Automata (CCA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / `CMA` 限制化分支
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `CCA=(Q,\Delta,I,F)`、bag `h:D\to\mathbb N`、约束 `(op,e)`、指令 `+/#` 与到 Petri-net coverability / `\omega`-counter machine 的化简。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 data word、per-data-value bag 计数语义与单步更新规则。

## 简报

这篇论文的价值，不在于再给 data-word family 增加一个应用特例，而在于把“按 data class 计数”的自动机正式稳定命名成 `CCA`。它的核心想法是：对每个 data value 都维护一个单调计数器，但转移只允许做“与常数比较”“加常数”“重置到常数”这类很克制的更新。这样它比纯 register 视角更适合表达“至少多少个 ID”“某个 ID 最多出现几次”这类 multiplicity summary，又比完整 `CMA` 更容易换回 elementary decidability。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 主枝上的 counting / class-summary 分支，可看作 `Class-Memory Automata` 的一个受限、强调 multiplicity 的近邻家族。
- 构造方式简述：读入每个 `(a,d)` 时，只检查当前 datum `d` 对应计数器的当前值是否满足某个约束，然后执行加法或重置，并切换有限状态。
- 基础设施与场景简述：原文纯理论，但给出到 Petri-net coverability 和 `\omega`-counter machine 的空性化简，也明确比较了 `CCA` 与 `CMA` 的表达力边界。

```text
data word -> per-datum counters -> threshold / reset updates -> Petri-net style coverability / CMA comparison
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是 data word，也就是每个位置都带一个有限标签和一个无限域数据值的线性串：

$$
w=(a_1,d_1)(a_2,d_2)\cdots(a_n,d_n)\in (\Sigma\times D)^*
$$

这里 `\Sigma` 是有限字母表，`D` 是可数无限数据域。模型的重点不在“记住某个 datum 的最后状态”，而在“统计每个 datum 目前出现了多少次”。

### 核心抽象

原文把类计数自动机定义为：

$$
\mathrm{CCA}=(Q,\Delta,I,F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `I\subseteq Q` 是初始状态集。
3. `F\subseteq Q` 是接受状态集。
4. `\Delta` 是转移关系。

其中转移关系满足：

$$
\Delta \subseteq Q\times\Sigma\times C\times Inst\times U\times Q
$$

上式中的符号逐项解释如下：

1. `C` 是有限约束集合，单个约束写成 `c=(op,e)`，其中 `op\in\{<,=,\neq,>\}`，`e\in\mathbb N`。
2. `Inst=\{+,\#\}` 表示两类更新指令。
3. `U\subseteq \mathbb N` 是更新中会用到的常数集合。
4. 一个转移 `(q,a,c,\pi,m,q')` 的意思是：在状态 `q` 读到标签 `a` 时，若当前 datum 的计数满足约束 `c`，则按指令 `\pi` 和常数 `m` 更新该 datum 的计数，并转到 `q'`。

模型的配置写成：

$$
(q,h)
$$

上式中的符号逐项解释如下：

1. `q\in Q` 是当前有限状态。
2. `h:D\to\mathbb N` 是 bag，也就是“每个 data value 对应一个计数器值”的总映射。
3. 尽管 `D` 无限，只有有限多个 datum 会在运行中被显式更新；其余 datum 默认计数为 `0`。

### 一个最小例子与通俗解释

一个直观例子是“所有带标签 `a` 的 data value 都不能重复出现”。`CCA` 的做法很直接：

1. 读到 `(a,d)` 时，先检查 `h(d)=0`。
2. 若成立，则把这个 datum 的计数更新为 `1`。
3. 若之后又读到第二个 `(a,d)`，约束就不再成立，自动机转入拒绝分支。

通俗地说，`CCA` 像“给每个 datum 悄悄挂了一个只增不减的小计数器的有限自动机”。普通 `FSM` 只能记全局有限状态；`CCA` 则额外能对“每个名字已经出现了几次”做低精度但可判定的摘要统计。

### 运行 / 接受 / 转移语义

设输入字为

$$
w=(a_1,d_1)(a_2,d_2)\cdots(a_n,d_n)
$$

若第 `i` 步选用转移

$$
t_i=(q,a,c,\pi,m,q')\in\Delta
$$

则它必须满足：

$$
h_i(d_{i+1}) \models c
$$

上式中的符号逐项解释如下：

1. `h_i(d_{i+1})` 是当前 datum `d_{i+1}` 的旧计数。
2. `\models c` 表示这个旧计数满足约束 `c=(op,e)`。

更新后的 bag 满足：

$$
h_{i+1}=
\begin{cases}
h_i[d_{i+1}\mapsto h_i(d_{i+1})+m], & \pi=+ \\
h_i[d_{i+1}\mapsto m], & \pi=\#
\end{cases}
$$

上式中的符号逐项解释如下：

1. `+` 指令把当前 datum 的计数加上常数 `m`。
2. `\#` 指令把当前 datum 的计数直接改成常数 `m`。
3. 只有当前读到的 datum 的计数会被改动，其余 datum 的计数保持不变。

整个语言定义为：

$$
L(A)=\{w\in(\Sigma\times D)^* \mid A\ \text{has an accepting run on}\ w\}
$$

其中接受条件就是运行结束时落在某个 `F` 中的状态。

### 语义边界

`CCA` 强于普通有限自动机，因为它能对每个 datum 做局部计数；但它又明显弱于可以随时记“最后状态”的 `CMA`，因为它只保留非常有限的数值摘要，而不是精确的 per-datum control history。它的设计重点是“计数摘要可判定”，不是“一切 data-language 功能都要装进去”。

### 关键性质与判定边界

原文最关键的结论可以压成：

$$
\mathrm{emptiness}(\mathrm{CCA})\ \text{is Expspace-complete}
$$

$$
\mathrm{membership}(\mathrm{CCA})\ \text{is NP-complete}
$$

$$
\mathrm{universality}(\mathrm{CCA})\ \text{and}\ \mathrm{inclusion}(\mathrm{CCA})\ \text{are undecidable}
$$

$$
\mathrm{emptiness}(\mathrm{two\text{-}way\ CCA})\ \text{and}\ \mathrm{emptiness}(\mathrm{alternating\ CCA})\ \text{are undecidable}
$$

同时，原文还明确指出：

$$
\mathrm{CCA}\ \text{is a natural restriction of}\ \mathrm{CMA}
$$

上面几式中的符号逐项解释如下：

1. 第一式说明 `CCA` 的空性虽然不便宜，但仍停留在 elementary 范围内。
2. 第二式说明即使只是 membership，也已经不再是轻量级问题。
3. 第三和第四式说明这个 family 的可判定边界相当脆弱，双向读头和 alternation 都会把它推回不可判定区。
4. 最后一式表示它在谱系上最适合看作 `Class-Memory` 路线的一个受限分支，而不是完全独立于该主线的陌生模型。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 保留有限状态主骨架。 |
| 事件 / 触发 | 强支持 | 按线性 data word 单向扫描。 |
| 守卫 / 数据 | 强支持 | 通过 per-datum 计数与常数约束进行判断。 |
| 层次 | 不支持 | 对象是线性词，不是树。 |
| 并发 / 同步 | 不支持 | 无交替或并发组合语义。 |
| 时间约束 | 不支持 | 无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散计数。 |
| 可执行 / 可验证性 | 强理论支持 | 空性可判定，但包含/全称类问题很快失守。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$\mathrm{CCA}=(Q,\Delta,I,F)$` | family 的标准骨架。 |
| 配置 | `$(q,h)$` | 每个 datum 都有一个当前计数。 |
| 单步前提 | `$h_i(d_{i+1})\models c$` | 只检查当前 datum 的计数是否落在阈值条件内。 |
| 单步更新 | `$h_i[d\mapsto h_i(d)+m]$` 或 `$h_i[d\mapsto m]$` | 支持常数增量与常数重置。 |
| 复杂度边界 | `$\mathrm{emptiness}$ Expspace-complete` | counting summary 仍在 elementary decidability 内。 |

## 构造方式与承载格式

### 建模入口

1. 先把对象压成 data word。
2. 再确定需求是否真的是“每个 datum 出现多少次”的问题，而不是“某个 datum 上次处于哪个状态”的问题。
3. 对每类事件写出“当前 datum 的计数要满足什么阈值”和“随后怎样更新计数”。

### 机器可处理承载方式

机器可处理承载方式就是：

1. data word；
2. `\mathrm{CCA}=(Q,\Delta,I,F)`；
3. bag `h:D\to\mathbb N`；
4. 到 coverability / `\omega`-counter machine 的分析化简。

原文没有 XML、JSON、DSL 或工程化交换格式。

### 交换与互操作

它和 `Petri Nets` / coverability 的互操作最强，因为空性正是经由这条路线获得；与 `CMA` 的互操作则体现在“加入 reset 与 counter acceptance 后能逼近 `CMA` 表达力”，说明它不是孤立模型，而是 class-based data-automata 主线中的可判定切片。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心就是 data word、bag、constraints 与 instructions。
- 仿真/执行支持：可以直接按 `(q,h)` 语义解释。
- 验证/分析支持：到 Petri-net coverability、`\omega`-counter machine 与 `CMA` 比较。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 data-language landscape 中的经典 counting family。

## 适用场景与需求前提

### 适用场景

适合“无界多进程 / 多会话系统”的计数摘要语言，例如：

1. 每个 process ID 最多做 `k` 次动作 `a`。
2. 至少有 `m` 个 data values 满足某类局部模式。
3. 系统状态只需要保留 multiplicity summary，而不需要精确历史。

### 需求前提

1. 输入对象需可压成 finite data word。
2. 数据关系主要是 datum equality 加计数阈值，而不是 datum order 或算术关系。
3. 需求更像“每个 datum 出现几次”，而不是“这个 datum 最近一次到过哪个控制状态”。

### 不适用或高成本场景

若需求依赖 complement、任意 inclusion、双向扫描、alternation 或复杂算术比较，这个 family 很快就不够，必须转向别的 data-automata 路线。

## 与相邻形式主义的关系

相对 [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md)，它不是 base/class 双层自动机，而是显式的 per-datum counting 机器；相对 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md)，它不记“最后状态”，而记“当前 multiplicity”，因此更像 `CMA` 的受限 counting sibling；相对 [an-automaton-over-data-words-that-captures-emso-logic/desc.md](../an-automaton-over-data-words-that-captures-emso-logic/desc.md)，它也不追求逻辑完备性，而是保守交换出 elementary decidability。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Data / Infinite-Alphabet` 主枝补出了一条此前没有正式入账的 counting-summary 子线，使演化树不再只剩 register / class-memory / freshness 三种解释路径。

### 作为目标形式主义还是中间表示

更适合作为理论谱系节点或中间抽象，而不是控制系统最终交付的建模语言。

### 对需求到模型生成的启发

当需求文本里出现“每个 ID 最多/至少出现多少次”“统计满足某条件的不同实体个数”时，LLM 不应只想到 register 或 `CMA`，还应识别“这可能是更偏 counting summary 的 `CCA` family”。

### 现实限制

没有工程标准、编辑器或成熟运行时；其价值主要在可判定边界、谱系定位与 counting abstraction。

## 重要的相关工作

### 奠基或前身工作

- [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md)
- [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md)

### 同类型或同家族工作

- [an-automaton-over-data-words-that-captures-emso-logic/desc.md](../an-automaton-over-data-words-that-captures-emso-logic/desc.md)
- [a-robust-class-of-data-languages-and-an-application-to-learning/desc.md](../a-robust-class-of-data-languages-and-an-application-to-learning/desc.md)
- [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具。

### 与本研究关系最紧的工作

- 它最适合补到 `Finite Automata -> Data / Infinite-Alphabet` 主枝中 `Class-Memory` 附近的 counting 分支。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Class Counting Automata (CCA)`
- 论文角色：模型提出 / `CMA` 限制化分支
- 核心功能：在 data words 上用 per-datum multiplicity summary 表达 counting-style language constraints，并保持空性可判定。
- 关键特性：bag semantics、threshold constraints、constant increment/reset、Petri-net reduction、`CMA` 近邻关系。
- 构造方式：`\mathrm{CCA}=(Q,\Delta,I,F)` + bag `h:D\to\mathbb N` + per-datum guarded update semantics。
- 基础设施：纯理论模型，无工程标准/工具；核心分析设施是 coverability 与 `\omega`-counter-machine reduction。
- 适用场景：无界 process/session ID 的 multiplicity summary、counting-style data languages。
- 需求前提：输入需可压成 data word，且关键约束主要是 per-datum counting 而不是 order 或复杂历史。
- 状态：🟢

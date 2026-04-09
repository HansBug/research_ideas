# 有限数据词与树上的交替寄存器自动机 / Alternating register automata on finite data words and trees

## 基本信息

- 标题：Alternating register automata on finite data words and trees
- 中文标题：有限数据词与树上的交替寄存器自动机
- 作者：Diego Figueira
- 发表：*Logical Methods in Computer Science*, 8(1:22):1-43, 2012
- DOI：`10.2168/LMCS-8(1:22)2012`
- 链接：https://lmcs.episciences.org/907
- 形式主义：`Alternating Register Automata / Alternating Tree Register Automata (ARA / ATRA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 `ARA(spread;guess)` / `ATRA(spread;guess)` 的 transition grammar、thread configurations 和 data-equality semantics。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 data word / data tree、finite-state thread sets 和一寄存器相等性测试。

## 简报

这篇论文把 register automata 在无限数据域上的“一寄存器 + 交替控制”路线系统推进到 data words 和 data trees 两类对象上，并给出 `guess` / `spread` 两个可判定扩展。它的核心价值，在于为当前演化树补出一条明确的 `data / infinite-alphabet automata` 分支：有限状态骨架不再只看有限字母，还能把一个数据值存进寄存器并做后续相等/不等比较。

- 形式主义定位：`Finite Automata` 主干下的 infinite-alphabet / data automata 子枝，以一寄存器与 alternation 扩展普通有限自动机。
- 构造方式简述：在线性 data word 上用 one-way threads 同步推进；在 unranked data tree 上用 first-child / next-sibling 导航，并通过 `store / eq / guess / spread` 操作管理数据值。
- 基础设施与场景简述：原文是纯理论工作，但直接给出 `ARA(guess;spread)` 空性可判定性，并把 forward `XPath` 可满足性约化到 `ATRA(guess;spread)`。

```text
有限标签 + 无限数据值 -> one-register alternating automata -> 数据相等/不等与线程分裂 -> data-word / data-tree language analysis
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是 data words 和 data trees。每个位置或节点都带一个有限字母表标签和一个来自无限域 `D` 的数据值。对 tree case，论文使用 unranked ordered trees，并通过 first-child / next-sibling 视角组织树导航。

### 核心抽象

对 data words，原文把扩展后的 `ARA(spread;guess)` 定义为：

$$
A = \langle A,Q,q_I,\delta \rangle
$$

上式中的符号逐项解释如下：

1. `A` 是有限输入字母表。
2. `Q` 是有限状态集。
3. `q_I \in Q` 是初始状态。
4. `\delta:Q \to \Phi` 是转移函数。

其中 `\Phi` 由如下语法生成：

$$
a \mid \bar a \mid \beta? \mid \mathrm{store}(q) \mid \mathrm{eq} \mid \overline{\mathrm{eq}} \mid q \land q' \mid q \lor q' \mid Bq \mid \mathrm{guess}(q) \mid \mathrm{spread}(q;q')
$$

上式中的符号逐项解释如下：

1. `a/\bar a` 测试当前标签是否等于/不等于 `a`。
2. `\beta?` 测试当前位置类型，其中 `\beta \in \{B,\bar B\}`。
3. `\mathrm{store}(q)` 把当前数据值写入寄存器并转到状态 `q`。
4. `\mathrm{eq}/\overline{\mathrm{eq}}` 测试当前数据值是否等于寄存器中存储的数据。
5. `q \land q'` 与 `q \lor q'` 分别表示 universal / existential branching。
6. `Bq` 表示移动到右侧下一位置并进入状态 `q`。
7. `\mathrm{guess}(q)` 允许非确定性猜一个任意数据值存入寄存器。
8. `\mathrm{spread}(q;q')` 根据当前所有带状态 `q` 的线程数据，批量生成状态 `q'` 的新线程。

论文的 `ATRA(spread;guess)` 是把同一套一寄存器 + alternation 思路提升到 data trees 上，并允许沿 leftmost-child 与 next-sibling 方向移动。

### 一个最小例子与通俗解释

一个最小例子是“检查未来是否再次出现与当前位置同一 ID 的事件”。在 data word 上，机器先执行 `store(q)` 把当前 datum 存进寄存器，再不断右移；一旦某个后继位置执行 `\mathrm{eq}` 成功，就说明找到相同数据值。若要表达“对目前已见过的所有数据值都检查某个条件”，则可以通过 `spread` 把这些旧 datum 批量分发给新线程。

通俗地说，`ARA/ATRA` 就像“每个线程只有一个便签槽的自动机”。普通有限自动机只看有限标签；这里每条线程还能把一个无限域数据值先记下来，之后再判断“现在看到的是不是之前那个值”。

### 运行 / 接受 / 转移语义

对 data words，原文把 configuration 写成：

$$
\langle i,\alpha,\gamma,\Delta \rangle
$$

上式中的符号逐项解释如下：

1. `i` 是当前位置编号。
2. `\alpha` 是当前位置类型。
3. `\gamma=(a,d)` 是当前位置的标签和数据值。
4. `\Delta \subseteq Q \times D` 是当前活跃线程集合；每个线程由状态和寄存器中存着的数据值组成。

初始配置与接受条件可保守概括为：

$$
C_1 = \langle 1,\alpha_0,\gamma_0,\{(q_I,d(1))\} \rangle,\quad C_n=\langle i,\alpha,\gamma,\emptyset\rangle
$$

上式中的符号逐项解释如下：

1. `d(1)` 是 data word 第一个位置的数据值。
2. `\emptyset` 表示所有 obligation threads 都已成功消解。
3. `C_1 \Rightarrow \cdots \Rightarrow C_n` 表示由 non-moving 和 moving 转移关系构成的一条 run。

`guess` 和 `spread` 的关键语义分别是“任意选一个 `e \in D` 存入寄存器”和“对当前某组线程携带的所有数据值批量复制出新 obligation threads”。

### 语义边界

这类模型只提供一个寄存器，因此可表达的是“当前 datum 与一个被记住的 datum 的相等/不等比较”，不是任意算术或多寄存器数据程序。`ARA/ATRA` 的 alternation 增加的是义务分解和路径分叉能力，而不是概率语义。对 tree case，`ATRA` 走的是 first-child / next-sibling 导航路线，不是 bottom-up `Tree Automata` 式并行汇总。

### 关键性质与判定边界

原文最关键的可判定性结论是：

$$
\text{The emptiness problem for } \mathrm{ARA}(\mathrm{guess};\mathrm{spread}) \text{ is decidable.}
$$

同时，原文证明：

$$
\mathcal L(\mathrm{ARA}(\mathrm{guess};\mathrm{spread})) \text{ is not closed under complement.}
$$

并通过到 `ATRA(guess;spread)` 的约化得到：

$$
\text{Satisfiability of forward XPath with data tests, DTDs, and key constraints is decidable.}
$$

上面三式中的符号逐项解释如下：

1. `\mathrm{ARA}(\mathrm{guess};\mathrm{spread})` 是带 `guess/spread` 扩展的一寄存器交替 data-word 自动机。
2. `\mathcal L(\cdot)` 是该类自动机定义的语言族。
3. forward `XPath` 是文中处理的只沿 forward axes 走的 data-aware XPath 片段。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态和 alternation 是主骨架。 |
| 事件 / 触发 | 强支持 | 在线性词上逐位置推进，在树上沿 child/sibling 方向移动。 |
| 守卫 / 数据 | 强支持 | 一寄存器存储、相等/不等测试、`guess/spread` 扩展是核心。 |
| 层次 | 部分支持 | `ATRA` 支持 unranked tree 的 child/sibling 导航。 |
| 并发 / 同步 | 强支持 | alternation 通过 thread sets 表达并行义务。 |
| 时间约束 | 不支持 | 无时钟或显式时间。 |
| 连续动态 / 随机性 | 不支持 | 没有连续或概率语义。 |
| 可执行 / 可验证性 | 强理论支持 | 空性可判定，并能承载逻辑可满足性约化。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$A=\langle A,Q,q_I,\delta\rangle$` | `ARA(spread;guess)` 的有限状态骨架。 |
| 配置 | `$\langle i,\alpha,\gamma,\Delta\rangle$` | 运行状态由当前位置、当前标签/数据和线程集合组成。 |
| 数据线程 | `$\Delta \subseteq Q\times D$` | 每条线程都携带一个寄存器 datum。 |
| 空性可判定 | `$\mathrm{emptiness}(\mathrm{ARA}(\mathrm{guess};\mathrm{spread}))$ decidable` | 该扩展模型仍保持可判定分析。 |
| 非补闭包 | `$\mathcal L(\mathrm{ARA}(\mathrm{guess};\mathrm{spread}))$ not complement-closed` | 引入 `guess/spread` 后能力增强但布尔闭包变弱。 |

## 构造方式与承载格式

### 建模入口

1. 先确定对象是 data word 还是 data tree。
2. 明确哪些位置属性只看有限标签，哪些约束依赖数据值相等/不等。
3. 设计一寄存器线程状态、store/eq 分支和必要的 alternation。
4. 若需要全域式数据检查，再引入 `guess` 或 `spread`。

### 机器可处理承载方式

机器可处理承载方式是 transition grammar、thread-configuration transition system、data-tree/fcns 编码和 WSTS reachability 语义，而不是固定文本 DSL。

### 交换与互操作

该模型与 classic `Finite Automata` 的主区别在于 infinite-domain data register；与 [tree-automata/desc.md](../tree-automata/desc.md) 的 tree recognizer 路线相比，`ATRA` 更偏 child/sibling 顺序导航；与 forward `XPath` 的关系主要体现在逻辑到自动机的可满足性约化。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 data word / data tree、thread sets、one-register transitions 和 WSTS 抽象。
- 仿真/执行支持：可按配置转移系统解释运行，但原文重点不在工程执行器。
- 验证/分析支持：空性判定、逻辑可满足性约化、WSTS reachability 是重点。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：理论上直接服务 data automata、XPath/XML 静态分析和 temporal logic with registers。

## 适用场景与需求前提

### 适用场景

适合带无限域标识符/属性值的数据词或数据树语言分析，例如 XML 节点属性比较、进程序号/会话 ID 重复检测、以及 forward navigation + data equality 约束。

### 需求前提

1. 对象位置除了有限标签，还必须携带来自无限域的数据值。
2. 关键数据约束主要是“当前值是否等于/不等于某个已存值”。
3. 若是树对象，导航应可落到 child / next-sibling 方向。

### 不适用或高成本场景

如果需求需要多寄存器算术、全量数据聚合、时间约束或数值优化，这个一寄存器模型就明显不足；如果只处理有限标签语言，普通 `Finite Automata / Tree Automata` 更简单。

## 与相邻形式主义的关系

相对 [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)，它把有限标签自动机扩到 infinite-domain data setting；相对 [on-the-power-of-tree-walking-automata/desc.md](../on-the-power-of-tree-walking-automata/desc.md)，`ATRA` 也走顺序树导航路线，但核心增强点是 one-register data equality 而不是 pebbles；相对 [tree-automata/desc.md](../tree-automata/desc.md)，它不是 bottom-up tree recognizer。

## 与本研究的关系

### 对 Project 1 的价值

它能给当前演化树补出一条 `Data / Infinite-Alphabet Automata` 支线，避免 `Finite Automata` 主干只停在有限字母表和栈/计数器增强。

### 作为目标形式主义还是中间表示

更适合作为“含 ID / 参数值需求”的中间表示或理论旁支节点，而不是控制系统主线的最终建模语言。

### 对需求到模型生成的启发

如果需求文本里反复出现“同一任务 ID / 同一会话号 / 同一对象属性值”这类跨位置引用，LLM 可以考虑先生成 register automata 风格的中间模型，再判断是否需要退回普通有限状态或升级到多变量形式。

### 现实限制

原文重点是可判定性和逻辑约化，不提供工程建模语言或运行时；一寄存器限制也意味着它更适合作理论分支而不是通用控制建模终点。

## 重要的相关工作

### 奠基或前身工作

- [finite-automata-and-their-decision-problems/desc.md](../finite-automata-and-their-decision-problems/desc.md)
- [tree-automata/desc.md](../tree-automata/desc.md)

### 同类型或同家族工作

- 原文直接建立在 Demri、Lazić、Jurdziński 的 `ARA / ATRA` 工作之上，并继续扩展 `guess/spread` 与 WSTS 证明路线。

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线；forward `XPath` 是被约化分析的逻辑对象，不是该自动机的交换格式。

### 与本研究关系最紧的工作

- 它最适合补当前演化树里 `Finite Automata` 下的 `Data / Infinite-Alphabet` 子枝，并作为后续继续追 register / class-memory / data automata family 的入口。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Alternating Register Automata / Alternating Tree Register Automata (ARA / ATRA)`
- 论文角色：模型扩展
- 核心功能：用一寄存器交替自动机识别 data words/data trees，并通过 `guess/spread` 扩展保持空性可判定。
- 关键特性：infinite-domain data equality、one register、alternation、`guess/spread`、WSTS-based emptiness、forward XPath reduction。
- 构造方式：`A=\langle A,Q,q_I,\delta\rangle` + thread configurations + data-equality / spread transitions；tree 版沿 child/sibling 导航。
- 基础设施：纯理论模型，无工程标准/工具，但可承接 XPath 和 register-temporal-logic 可满足性分析。
- 适用场景：数据词/数据树语言、XML 属性相等性约束、ID/参数跨位置引用分析。
- 需求前提：输入位置需带无限域数据值，且核心数据约束能压成一寄存器相等/不等比较。
- 状态：🟢

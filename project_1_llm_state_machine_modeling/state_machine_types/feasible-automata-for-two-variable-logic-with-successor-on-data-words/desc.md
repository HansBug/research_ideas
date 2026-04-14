# 面向带后继的数据词二变量逻辑的可行自动机 / Feasible Automata for Two-Variable Logic with Successor on Data Words

## 基本信息

- 标题：Feasible Automata for Two-Variable Logic with Successor on Data Words
- 中文标题：面向带后继的数据词二变量逻辑的可行自动机
- 作者：Ahmet Kara，Thomas Schwentick，Tony Tan
- 发表：*Language and Automata Theory and Applications (LATA 2012)*, 351-362, 2012
- DOI：`10.1007/978-3-642-28332-1_30`
- 链接：https://doi.org/10.1007/978-3-642-28332-1_30
- 形式主义：`Weak Data Automata (WDA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 复杂度收束
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `WDA=(A,C)`、profile transducer `A`、以及 key / inclusion / denial 三类 class constraints。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 data word 的 profile 编码、字母到字母 transducer 输出串、以及每个数据类单独检查的约束集 `C`。

## 简报

这篇论文把 `Data Automata` 的“每个 class 跑一个自动机”进一步收紧成一个更轻量、也更易分析的模型：`Weak Data Automata`。它保留了 data-word 上“先做有限状态转写、再按数据值 class 检查”的两阶段骨架，但第二阶段不再允许任意 class-language，而只允许三类非常基础的 per-class 约束：key、inclusion 和 denial。这个变化让模型明显弱于 `Data Automata`，却换回了 `2-NEXPTIME` 的空性上界，并且刚好与 `EMSO^2(+1,\sim)` 对齐。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 主枝上的一个“可行化”子类，位于 `Data Automata` 之下，与 `Register Automata` 不可比。
- 构造方式简述：先把 data word 压成 profile 串交给字母到字母 transducer，再对每个数据类检查三类简单 class constraints，而不是对 class 子串跑一般自动机。
- 基础设施与场景简述：原文纯理论，但系统给出了 `WDA < DA`、`WDA` 与 `RA` 不可比、与 `EMSO^2(+1,\sim)` 等价，以及 `2-NEXPTIME` 空性边界。

```text
data word -> profile string -> letter-to-letter transducer -> per-class key/inclusion/denial constraints -> language acceptance
```

## 形式主义定义与核心对象

### 定义对象

`WDA` 处理的是 data words：每个位置同时带一个有限字母和一个来自无限域的数据值。与很多 register-style 模型不同，它不直接在运行过程中保存具体数据值，而是把输入先转成 profile，再把“同一数据值出现在哪些输出标签上”交给 class constraints 统一检查。

### 核心抽象

原文把 `Weak Data Automaton` 定义为：

$$
W = (A, C)
$$

上式中的符号逐项解释如下：

1. `A` 是字母到字母 transducer。
2. `C` 是定义在输出字母表上的一组 data constraints。

其中 transducer 可保守写成：

$$
A = (Q,\Sigma \times \{\top,\bot\},\Gamma,\delta,q_0,F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `\Sigma` 是输入有限字母表。
3. `\{\top,\bot\}` 是 profile 中“当前位置数据值是否与前一位置相同”的附加位。
4. `\Gamma` 是输出字母表。
5. `\delta` 是转移关系。
6. `q_0` 与 `F` 分别是初始状态与接受状态集。

`C` 中只允许三类 class constraints：

$$
\mathrm{key}(\gamma), \qquad V(\gamma)\subseteq \bigcup_{\gamma' \in R} V(\gamma'), \qquad V(\gamma)\cap V(\gamma')=\emptyset
$$

上式中的符号逐项解释如下：

1. `\mathrm{key}(\gamma)` 表示任意两个输出为 `\gamma` 的位置不能拥有相同数据值。
2. `V(\gamma)` 表示在当前 data word 中，出现在输出标签 `\gamma` 上的数据值集合。
3. inclusion 约束表示：出现在 `\gamma` 上的每个数据值，也必须出现在某个 `R` 中标签上。
4. denial 约束表示：两类标签不能共享同一个数据值。

### 一个最小例子与通俗解释

一个直观例子是“同一个会话 ID 上只允许有一个 `open`，且只要出现 `req` 就必须也出现一次 `ack`”。`WDA` 的写法不是给每个会话 ID 开一个小自动机，而是：

1. 先用 transducer 给每个位置标成 `open / req / ack / other` 之类的输出标签。
2. 再对每个数据值类检查约束：
   - `key(open)`：同一 ID 不允许两个 `open`。
   - `V(req) \subseteq V(ack)`：凡是出现 `req` 的 ID，也必须出现 `ack`。

通俗地说，`WDA` 像“先做一遍有限状态打标签，再对每个数据值的标签集合做简单账本检查”。它不关心同一 class 内标签的精细顺序，因此比 `Data Automata` 弱，但也正因此更可判定。

### 运行 / 接受 / 转移语义

设输入 data word 为：

$$
w = \binom{a_1}{d_1}\binom{a_2}{d_2}\cdots\binom{a_n}{d_n}
$$

原文的接受语义可压成：

$$
w \in L(A,C)
\iff
\exists \gamma_1\gamma_2\cdots\gamma_n \in A(\mathrm{Profile}(w))
\ \text{s.t.}\ 
\binom{\gamma_1}{d_1}\binom{\gamma_2}{d_2}\cdots\binom{\gamma_n}{d_n}
\models C
$$

上式中的符号逐项解释如下：

1. `\mathrm{Profile}(w)` 是把相邻位置的数据相等信息压成 `\top/\bot` 标记后的 profile 串。
2. `A(\mathrm{Profile}(w))` 表示 transducer 在 profile 上可能输出的所有 `\Gamma`-串。
3. `\models C` 表示诱导出的输出 data word 满足约束集 `C` 中全部约束。

### 语义边界

`WDA` 的限制非常明确：

1. 它仍然能表达“同一数据值是否出现过某些标签组合”的全局 class 性质。
2. 但它不能像一般 `Data Automata` 那样对每个 class 跑任意正则语言检查。
3. 它也不像 `Register Automata` 那样在运行中通过寄存器做逐步相等比较。

因此它恰好落在“比 `DA` 更弱、但仍保留无限数据域分析能力”的中间地带。

### 关键性质与判定边界

原文最关键的结论可压成：

$$
\mathcal L(\mathrm{WDA}) \subsetneq \mathcal L(\mathrm{DA})
$$

$$
\mathcal L(\mathrm{WDA}) \bowtie \mathcal L(\mathrm{RA})
$$

$$
\mathcal L(\mathrm{WDA}) \equiv \mathrm{EMSO}^2(+1,\sim)
$$

$$
\mathrm{emptiness}(\mathrm{WDA}) \in 2\text{-}\mathrm{NEXPTIME}
$$

上面几式中的符号逐项解释如下：

1. 第一式表示 `WDA` 严格弱于 `Data Automata`。
2. 第二式中的 `\bowtie` 表示与 `Register Automata` 不可比。
3. 第三式表示它与带 successor 和 data equality 的二变量存在单调二阶逻辑等价。
4. 第四式给出这篇论文最重要的复杂度收获。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 第一阶段仍是有限状态 transducer。 |
| 事件 / 触发 | 强支持 | 按 data-word 顺序单向扫描 profile。 |
| 守卫 / 数据 | 中等支持 | 只支持 per-class 的 key / inclusion / denial 三类简单约束。 |
| 层次 | 不支持 | 原始模型只处理线性 data words。 |
| 并发 / 同步 | 不支持 | 无显式并发组合机制。 |
| 时间约束 | 不支持 | 无时钟与时间语义。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 空性有 `2-NEXPTIME` 上界，且逻辑刻画清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$W=(A,C)$` | `WDA` 的两阶段骨架。 |
| transducer | `$A=(Q,\Sigma\times\{\top,\bot\},\Gamma,\delta,q_0,F)$` | 第一阶段只看 profile，不直接操作无限数据值。 |
| class constraints | `$\mathrm{key},\ \subseteq,\ \cap=\emptyset$` | 第二阶段只允许三类简单 per-class 约束。 |
| 表达力边界 | `$\mathcal L(\mathrm{WDA}) \subsetneq \mathcal L(\mathrm{DA})$` | 明确弱于 `DA`。 |
| 复杂度 | `$\mathrm{emptiness}(\mathrm{WDA}) \in 2\text{-}\mathrm{NEXPTIME}$` | 这是“feasible”命名背后的关键依据。 |

## 构造方式与承载格式

### 建模入口

1. 先判断需求是否可以拆成“有限状态转写 + per-class 简单约束”。
2. 若可以，再为 transducer 设计输出标签语义。
3. 最后把数据条件压成 key / inclusion / denial，而不是一般 class-automaton 或寄存器程序。

### 机器可处理承载方式

机器可处理承载方式是：

1. profile 串；
2. 字母到字母 transducer `A`；
3. 约束集 `C`；
4. 由输出标签诱导的 class-value 集合 `V(\gamma)`。

原文没有 XML、JSON 或专门 DSL。

### 交换与互操作

它与 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 中的 `Data Automata / Class-Memory Automata` 最接近，但比那条线更弱、更易分析；它与 `Register Automata` 不可比；又直接为后续 [commutative-data-automata/desc.md](../commutative-data-automata/desc.md) 提供了“commutative class condition 才带来 elementary complexity”这条比较基线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 profile 编码、transducer 输出标签与 class constraints。
- 仿真/执行支持：可按“先转写、后逐类检查约束”的两阶段语义执行。
- 验证/分析支持：空性判定、与 `EMSO^2(+1,\sim)` 的互译、向 `DA` 的翻译。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是 `Data Automata` 复杂度收敛线上的标准参考节点。

## 适用场景与需求前提

### 适用场景

适合 data-word 上那类“每个数据值类只需满足简单存在/排斥/包含约束”的模型，例如每个 ID 最多一次初始化、出现某标记后必须伴随另一标记、两类角色不能共享同一数据值等。

### 需求前提

1. 输入对象必须可压成线性 data word。
2. 关键数据关系只需要 class 级别的简单约束，而不需要 class 内的细粒度顺序语言。
3. 若同一数据值内的顺序模式很重要，就该回到 `DA` 或更强模型。

### 不适用或高成本场景

若需求需要：

1. class 内部的完整正则顺序语言；
2. 运行中逐步存取具体数据值；
3. 树结构导航；
4. 时间或连续变量，

那么 `WDA` 就不够。

## 与相邻形式主义的关系

相对 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 的 `Data Automata / Class-Memory Automata`，它把第二阶段从“一般 class language”收缩成三类简单约束；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md) 这类寄存器路线，它不在运行中携带数据值；相对 [commutative-data-automata/desc.md](../commutative-data-automata/desc.md)，它是更弱、但更基础的 class-condition 基线。

## 与本研究的关系

### 对 Project 1 的价值

它把当前 `Data Automata` 主枝补出一个真正清晰的“可行化中间层”，让 `DA -> WDA -> CDA` 这条复杂度收敛线能够稳定挂树。

### 作为目标形式主义还是中间表示

更适合作为理论中间表示或分类节点，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

当需求中的数据关系可以被压成“唯一性 / 包含性 / 互斥性”三类 per-class 约束时，LLM 没必要一上来就生成更重的寄存器自动机或一般数据自动机；先落到 `WDA` 级别往往更容易判定和比较。

## 重要的相关工作

1. [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md)：给出 `Data Automata / Class-Memory Automata` 主线。
2. [commutative-data-automata/desc.md](../commutative-data-automata/desc.md)：把 `WDA` 的 commutative 直觉继续推广。
3. [a-decidable-extension-of-data-automata/desc.md](../a-decidable-extension-of-data-automata/desc.md)：沿 class-condition 方向补出 `PCA`。

## 文献分类总结

- 形式主义：`Weak Data Automata (WDA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 复杂度收束

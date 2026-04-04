# 数据自动机的一个可判定扩展 / A Decidable Extension of Data Automata

## 基本信息

- 标题：A Decidable Extension of Data Automata
- 中文标题：数据自动机的一个可判定扩展
- 作者：Zhilin Wu
- 发表：*Electronic Proceedings in Theoretical Computer Science*, 54:116-130, 2011
- DOI：`10.4204/EPTCS.54.9`
- 链接：https://doi.org/10.4204/EPTCS.54.9
- 形式主义：`Class Automata with Priority Class Condition (PCA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 可判定性收束
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 class automaton `(A,B)`、优先级划分 `\Gamma = \Gamma_1 \uplus \cdots \uplus \Gamma_k`、以及到 priority multicounter automata 的对应。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 data word、class automaton run、0-priority regular language 与 priority multicounter semantics。

## 简报

这篇论文做的事情很明确：它不是再往 `Data Automata` 上加一个随意的新 class condition，而是瞄准 `Class Automata` 已经不可判定这一点，找出一条还能保住 emptiness decidability 的 class-based 扩展路线。作者给出的答案是 `Class Automata with Priority Class Condition (PCA)`。它比 `Data Automata` 强，因为 class condition 不再局限于最简单的 per-class 子串约束；但它又通过输出字母表的优先级分块，把 class language 限制回一类足以映射到 priority multicounter automata 的正则语言。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 主枝上的 class-based decidable extension，可视为 `Class Automata` 的收束版、`Data Automata` 的严格扩展。
- 构造方式简述：仍保持 class automaton 的“两阶段”骨架，但要求 class condition 的正则语言可按输出字母表优先级分块成若干 `0`-priority regular languages。
- 基础设施与场景简述：原文纯理论，但给出了 `PCA` 到 priority multicounter automata 的对应，从而得到 emptiness decidability，并且明确说明 `PCA` 严格强于 `Data Automata`。

```text
data word -> class automaton output -> priority-partitioned class language -> priority multicounter reduction -> emptiness analysis
```

## 形式主义定义与核心对象

### 定义对象

`PCA` 仍然处理 data words。每个位置有有限标签和无限域数据值，模型先用 transducer 产生输出串，再对每个数据类的 class string 做 class-condition 检查。与一般 `Class Automata` 的区别是：允许的 class-condition 不是任意 regular language，而是必须满足一套优先级结构。

### 核心抽象

原文把 `PCA` 建立在 class automaton `(A,B)` 之上。按照其定义，可保守写成：

$$
P = (A,B,\Pi)
$$

上式中的符号逐项解释如下：

1. `A` 是 transducer 部分。
2. `B` 是 class-condition automaton。
3. `\Pi` 是输出字母表上的优先级划分信息。

具体地，原文的关键约束是：

$$
\Gamma = \Gamma_1 \uplus \cdots \uplus \Gamma_k
$$

并要求：

$$
L(B) = L_1 \cup \cdots \cup L_k,\qquad L_i \subseteq (\Gamma_i \times \{0,1\})^*
$$

且每个 `L_i` 都是 `0`-priority regular language。

上式中的符号逐项解释如下：

1. `\Gamma` 是 class automaton 输出字母表。
2. `\Gamma_1,\ldots,\Gamma_k` 是按照优先级切出来的互不相交子字母表。
3. `L(B)` 是 class-condition automaton 接受的语言。
4. 每个 `L_i` 只在对应优先级块上工作，并满足 `0`-priority 结构限制。

### 一个最小例子与通俗解释

直观上，`PCA` 适合那种“同一数据值类里允许出现更丰富的局部模式，但模式之间仍有单向优先关系”的约束。可以把它理解成：

1. transducer 先把输入位置标成若干工作字母；
2. 每个数据类只会落进某一个优先级块 `\Gamma_i`；
3. 在该块内，class string 必须满足一台 `0`-priority finite automaton` 的语言要求。

通俗地说，它像“带分层权限的 class automaton”。相比 `Data Automata`，它允许每个 class 的正则检查更强；相比一般 `Class Automata`，它又不让 class condition 自由到足以模拟两计数器机。

### 运行 / 接受 / 转移语义

原文把 class automaton 的运行写成序列：

$$
(q^g_1,q^c_1,g_1,R_1)\cdots(q^g_{|w|},q^c_{|w|},g_{|w|},R_{|w|})
$$

上式中的符号逐项解释如下：

1. `q^g_i` 记录 transducer `A` 在第 `i` 步的全局状态。
2. `q^c_i` 记录“尚未见过的新数据值”对应的 class-condition 状态。
3. `g_i` 是第 `i` 个位置的输出字母。
4. `R_i` 把已出现过的数据值映射到 class-condition automaton 的当前状态。

`PCA` 的接受语义仍沿用 class automaton 思路：输入 data word 被 `A` 转成输出串后，每个数据值类对应的 class string 都必须落入某个优先级块上的 `0`-priority regular language。

### 语义边界

`PCA` 的边界非常清晰：

1. 它严格强于 `Data Automata`；
2. 它是一般 `Class Automata` 的真子类；
3. 决定性收获来自 priority restriction，而不是来自再弱化 transducer。

因此这条线的重点不是“如何更自然地表达数据值”，而是“class condition 强到什么程度仍然可判定”。

### 关键性质与判定边界

原文最关键的结论可压成：

$$
\mathcal L(\mathrm{DA}) \subsetneq \mathcal L(\mathrm{PCA})
$$

$$
\mathrm{emptiness}(\mathrm{PCA})\ \text{decidable}
$$

$$
\mathrm{PCA} \le \mathrm{Priority\ Multicounter\ Automata}
$$

上面几式中的符号逐项解释如下：

1. 第一式表示 `PCA` 严格扩展 `Data Automata`。
2. 第二式是本文的主结果。
3. 第三式表示 emptiness decidability 的技术基础来自到 priority multicounter automata 的规约。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | transducer + class-condition automaton 双层有限控制。 |
| 事件 / 触发 | 强支持 | 仍在 data-word 上顺序处理。 |
| 守卫 / 数据 | 强支持 | 每个数据值类都对应一条 class string，需要满足 priority class condition。 |
| 层次 | 不支持 | 原始模型只处理线性 data words。 |
| 并发 / 同步 | 不支持 | 无显式并发组合。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 通过 priority multicounter 路线恢复 emptiness decidability。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 保守元组 | `$P=(A,B,\Pi)$` | `PCA` 可理解为 class automaton 加 priority partition。 |
| 字母表划分 | `$\Gamma=\Gamma_1\uplus\cdots\uplus\Gamma_k$` | 优先级结构的核心。 |
| class language | `$L(B)=L_1\cup\cdots\cup L_k$` | 每块都需满足 `0`-priority regular language` 约束。 |
| 表达力边界 | `$\mathcal L(\mathrm{DA}) \subsetneq \mathcal L(\mathrm{PCA})$` | 严格强于 `DA`。 |
| 判定性 | `$\mathrm{emptiness}(\mathrm{PCA})$ decidable` | 本文的核心收获。 |

## 构造方式与承载格式

### 建模入口

1. 先确认问题仍是 class-based，而不是寄存器式逐步比较。
2. 再判断 class condition 是否可以按优先级块切开。
3. 只有满足优先级结构时，才值得用 `PCA`；否则要么退回 `DA`，要么升级到一般 `Class Automata` 并接受不可判定代价。

### 机器可处理承载方式

机器可处理承载方式是：

1. data word；
2. transducer `A`；
3. class automaton `B`；
4. 输出字母表优先级划分；
5. priority multicounter automata 规约。

原文没有工程 DSL 或标准交换格式。

### 交换与互操作

它与 [an-extension-of-data-automata-that-captures-xpath/desc.md](../an-extension-of-data-automata-that-captures-xpath/desc.md) 的关系最直接：`PCA` 是在 `Class Automata` 路线上加限制以恢复可判定性；与 [feasible-automata-for-two-variable-logic-with-successor-on-data-words/desc.md](../feasible-automata-for-two-variable-logic-with-successor-on-data-words/desc.md) 的 `WDA` 相比，`PCA` 允许更强的 class language；与 [commutative-data-automata/desc.md](../commutative-data-automata/desc.md) 则共同构成 `Data Automata` 之后两条不同的 decidable extension 路线。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 class automaton run、priority partition 与 `0`-priority regular languages。
- 仿真/执行支持：可以按 class automaton 的 `(q^g_i,q^c_i,g_i,R_i)` 运行语义解释。
- 验证/分析支持：到 priority multicounter automata 的规约是主要分析基础。
- 代码生成/转换支持：原文未涉及工程代码生成。
- 标准化或社区生态：是 class-condition / counter-machine correspondence 这条支线上的代表节点。

## 适用场景与需求前提

### 适用场景

适合 data-word 上那类“每个数据值类都要满足一类受优先级约束的正则模式”的问题，尤其当 `Data Automata` 太弱、而一般 `Class Automata` 又太强时。

### 需求前提

1. 输入对象需是 data word。
2. 需求仍应以 class-condition 为主，而不是运行中寄存器存值比较。
3. class language 必须可以被优先级结构收束，否则 `PCA` 的 decidability 基础就不成立。

### 不适用或高成本场景

若 class condition 的自由度已经接近一般 `Class Automata`，或需要树结构上下文、时间语义、多寄存器数据操作，那么 `PCA` 都不是合适选择。

## 与相邻形式主义的关系

相对 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 的 `Data Automata`，它让 class condition 更强；相对 [an-extension-of-data-automata-that-captures-xpath/desc.md](../an-extension-of-data-automata-that-captures-xpath/desc.md) 的 `Class Automata`，它又通过 priority restriction 缩回 decidable 区间；相对 [commutative-data-automata/desc.md](../commutative-data-automata/desc.md)，两者都在问“怎样加强 class condition 还能保住 emptiness decidability”，只是答案不同。

## 与本研究的关系

### 对 Project 1 的价值

它把当前演化树里的 class-based infinite-alphabet 路线补成了“强表达力但不可判定”与“受限但可判定”之间的一条稳定中间枝。

### 作为目标形式主义还是中间表示

更适合作为理论节点与比较基线，而不是控制系统最终建模语言。

### 对需求到模型生成的启发

当需求确实需要 class-level 正则模式，但又希望后续验证保持可判定，LLM 可以优先寻找是否存在某种 priority partition，把问题压回 `PCA` 风格。

## 重要的相关工作

1. [an-extension-of-data-automata-that-captures-xpath/desc.md](../an-extension-of-data-automata-that-captures-xpath/desc.md)：`Class Automata` 母线。
2. [feasible-automata-for-two-variable-logic-with-successor-on-data-words/desc.md](../feasible-automata-for-two-variable-logic-with-successor-on-data-words/desc.md)：更弱的 `WDA`。
3. [commutative-data-automata/desc.md](../commutative-data-automata/desc.md)：另一条 decidable class-condition 扩展线。

## 文献分类总结

- 形式主义：`Class Automata with Priority Class Condition (PCA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 可判定性收束

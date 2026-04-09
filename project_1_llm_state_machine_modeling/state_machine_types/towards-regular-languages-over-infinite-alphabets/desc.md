# 迈向无限字母表上的正则语言 / Towards Regular Languages over Infinite Alphabets

## 基本信息

- 标题：Towards Regular Languages over Infinite Alphabets
- 中文标题：迈向无限字母表上的正则语言
- 作者：Frank Neven, Thomas Schwentick, Victor Vianu
- 发表：*Mathematical Foundations of Computer Science 2001 (MFCS 2001)*, LNCS 2136, pp. 560-572, 2001
- DOI：`10.1007/3-540-44683-4_49`
- 链接：https://doi.org/10.1007/3-540-44683-4_49
- 形式主义：`Register Automata (RA) / Pebble Automata over Infinite Alphabets (PA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：家族比较 / 判定边界整理
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `RA` 的寄存器赋值 `\tau`、`PA` 的 pebble assignment `\theta`、两类 configuration 语义以及 `FO^* / MSO^*` 对比框架。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 `RA` 元组、`PA` 元组、step relation 与判定问题定义。

## 简报

这篇论文不是某一个单点模型的小修补，而是把“无限字母表上线性词的正则性应该由什么自动机来承载”系统压成了两个候选母型：`Register Automata` 和 `Pebble Automata`。它一方面明确给出两类模型的标准元组、配置与运行语义，另一方面把表达力、逻辑刻画和判定边界都摆到同一张桌面上比较，因此非常适合作为当前文库里 `Data / Infinite-Alphabet` 主枝的公开可得代表条目。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 主枝上的早期公开代表条目，同时为 `Register Automata` 与 infinite-alphabet `Pebble Automata` 两条子线提供统一参照。
- 构造方式简述：`RA` 用有限状态加 `k` 个寄存器记住少量已见数据；`PA` 用按栈纪律管理的 pebbles 在输入位置上做回看、比较和嵌套扫描。
- 基础设施与场景简述：原文是纯理论工作，但把 `RA / PA` 与 `FO^* / MSO^*`、非空性 / 全体性 / 包含性等标准问题一起整理成了稳定母线。

```text
无限字母表上的词 -> 有限控制 + 寄存器 / pebbles -> equality / freshness 风格比较 -> 语言类与判定边界
```

## 形式主义定义与核心对象

### 定义对象

原文处理的是来自无限字母表 `D` 的有限字符串。输入通常写成带左右端标记的 `\vdash v \dashv`，自动机真正能观察到的是“当前位置的数据值是否等于某个寄存器中的值”或“与某些 pebble 所在位置的数据值是否相同”，而不是数值算术。

### 核心抽象

对 `RA`，原文给出 `k`-register automaton：

$$
B = (Q, q_0, F, \tau_0, P)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `q_0 \in Q` 是初始状态。
3. `F \subseteq Q` 是接受状态集。
4. `\tau_0 : \{1,\ldots,k\} \to D \cup \{\vdash,\dashv\}` 是初始寄存器赋值。
5. `P` 是有限转移集，既包含“当前值等于寄存器 `i`”时可用的 `(i,q)\to(q',d)`，也包含“当前值不同于所有寄存器”时把该值写入寄存器 `i` 的 `q\to(q',i,d)`。

对 `PA`，原文给出 `k`-pebble automaton：

$$
A = (Q, q_0, F, T)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限状态集。
2. `q_0 \in Q` 是初始状态。
3. `F \subseteq Q` 是接受状态集。
4. `T` 是转移集合，源侧会读取“当前活跃 pebble 编号、当前符号、与更外层 pebbles 的 equality/position 关系、当前状态”，目标侧执行 `stay / left / right / place / lift` 五类动作。

`PA` 里最关键的额外观测量是：

$$
P = \{ l < i \mid \mathrm{val}_w(\theta(l)) = \mathrm{val}_w(\theta(i)) \}, \qquad
V = \{ l < i \mid \theta(l) = \theta(i) \}
$$

上式中的符号逐项解释如下：

1. `i` 是当前最内层、也就是当前活跃 pebble 的编号。
2. `\theta(i)` 是 pebble `i` 当前停留的输入位置。
3. `P` 记录有哪些外层 pebbles 看到与当前 pebble 相同的数据值。
4. `V` 记录有哪些外层 pebbles 与当前 pebble 停在同一位置。

### 一个最小例子与通俗解释

一个最小的 `RA` 例子是识别

$$
L_{\mathrm{eq2}} = \{ aa \mid a \in D \}
$$

做法很直接：第一步把首符号写进唯一寄存器，第二步要求当前值等于该寄存器后接受。

一个最小的 `PA` 直觉例子是“当前词中是否存在两个不同位置保存相同的数据值”。机器可以先把外层 pebble 放在某个位置，再让内层 pebble 向右扫描；当 `P` 显示外层 pebble 看到了同一个数据值时接受。这个能力不依赖固定的少数寄存器，而依赖“先在位置上打书签，再回看比较”。

通俗地说，`RA` 像“有限状态机外接几个记名卡槽”，而 `PA` 像“有限状态机带一摞按栈管理的位置书签”。前者擅长记住少量名字，后者擅长在整条串上做嵌套回看。

### 运行 / 接受 / 转移语义

`RA` 在输入词 `w` 上的 configuration 写成：

$$
[j,q,\tau]
$$

上式中的符号逐项解释如下：

1. `j` 是当前输入头位置。
2. `q` 是当前状态。
3. `\tau` 是当前寄存器赋值。

若 `(i,q)\to(q',d)` 可用，则自动机要求 `\mathrm{val}_w(j)=\tau(i)`；若 `q\to(q',i,d)` 可用，则要求当前位置数据值不同于所有寄存器，并把当前值写入寄存器 `i`。一步语义可压成：

$$
[j,q,\tau] \vdash [j',q',\tau']
$$

其中 `j'` 由 `d \in \{\mathrm{stay},\mathrm{left},\mathrm{right}\}` 决定，`\tau'` 要么保持不变，要么把寄存器 `i` 更新为当前位置值。

`PA` 的 configuration 写成：

$$
[i,q,\theta]
$$

上式中的符号逐项解释如下：

1. `i` 是当前活跃 pebble 的编号，也可理解为当前嵌套深度。
2. `q` 是当前状态。
3. `\theta : \{1,\ldots,i\} \to \mathrm{dom}(w)` 给出每个已放下 pebble 的位置。

一步转移同样写成

$$
[i,q,\theta] \vdash [i',q',\theta']
$$

其中：

1. `stay / left / right` 只改变当前 pebble 的位置。
2. `place` 让深度从 `i` 变成 `i+1`，新 pebble 初始放在当前 pebble 所在位置。
3. `lift` 让深度回退到 `i-1`。

接受语义两边都遵循“从初始 configuration 出发，经过若干步到达某个接受状态”的普通自动机口径。

### 语义边界

这篇论文真正清楚地区分了两种无限字母表自动机思路：

1. `RA` 的额外能力来自有限个寄存器，因此更像“有限状态 + 少量已见名字”。
2. `PA` 的额外能力来自 stack-discipline pebbles，因此更像“有限状态 + 嵌套回看位置”。
3. 两者都只做 equality-style 观察，不做算术、不做时间、不做概率。
4. `PA` 的 one-way / two-way 与 deterministic / nondeterministic 变体在表达力上比 `RA` 更稳定，更接近作者想要的“无限字母表 regularity”。

### 关键性质与判定边界

原文把 `RA` 与 `PA` 的关键边界压成一组很清晰的结论。对 `RA`，论文指出：

$$
\mathrm{MSO}^* \not\supseteq 2\mathrm{D}\text{-}\mathrm{RA}, \qquad
2\mathrm{A}\text{-}\mathrm{RA} \not\supseteq \mathrm{FO}^*
$$

上式中的符号逐项解释如下：

1. `2D-RA` 表示 two-way deterministic register automata。
2. `2A-RA` 表示 two-way alternating register automata。
3. 这两式合起来表达的不是“谁更强谁更弱”，而是 `RA` 与 `FO^* / MSO^*` 存在明显错位。

判定性方面，论文第 6 节给出：

$$
\mathrm{universality}(1\mathrm{N}\text{-}\mathrm{RA}) \text{ undecidable}
$$

$$
\mathrm{containment}(1\mathrm{N}\text{-}\mathrm{RA}) \text{ undecidable}
$$

$$
\mathrm{nonemptiness}(2\mathrm{D}\text{-}\mathrm{RA}) \text{ undecidable}
$$

$$
\mathrm{nonemptiness}(\mathrm{weak}\ 1\mathrm{D}\text{-}\mathrm{PA}) \text{ undecidable}
$$

这说明：

1. `1N-RA` 还保有某些较弱问题的可判定性，但一到全体性 / 包含性就越界。
2. `RA` 的非空性一旦允许更强双向控制，也会失去可判定性。
3. `PA` 更强，甚至弱 one-way 版本的非空性都已经不可判定。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 两类模型都保留有限控制骨架。 |
| 事件 / 触发 | 强支持 | 输入是线性词，逐位置触发转移。 |
| 守卫 / 数据 | 强支持 | `RA` 用寄存器 equality，`PA` 用 pebble equality / co-location。 |
| 层次 | 不支持 | 对象仍是线性词。 |
| 并发 / 同步 | 不支持 | 不是并发组合模型。 |
| 时间约束 | 不支持 | 无时钟和 dense time。 |
| 连续动态 / 随机性 | 不支持 | 纯离散、非概率。 |
| 可执行 / 可验证性 | 强理论支持 | 形式化定义、逻辑对比和判定边界都很清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `RA` 元组 | `$B=(Q,q_0,F,\tau_0,P)$` | 寄存器家族的标准定义。 |
| `PA` 元组 | `$A=(Q,q_0,F,T)$` | infinite-alphabet pebble 家族的标准定义。 |
| `RA` 配置 | `$[j,q,\tau]$` | 当前位置、状态与寄存器赋值。 |
| `PA` 配置 | `$[i,q,\theta]$` | 当前深度、状态与 pebble assignment。 |
| 判定边界 | `universality(1N-RA)`, `nonemptiness(2D-RA)`, `nonemptiness(weak 1D-PA)` undecidable | 说明两条家族线都不只是 regular 的轻量延伸。 |

## 构造方式与承载格式

### 建模入口

1. 若需求只需要记住有限个已见数据值，先从 `RA` 视角建模。
2. 若需求需要把“某个位置”压栈保存并稍后回看，改走 `PA` 视角。
3. 若只是 equality / repeat pattern，避免过早引入更重的数据逻辑或历史结构。

### 机器可处理承载方式

机器可处理承载方式主要就是两套元组与 configuration semantics：

1. `RA` 的寄存器赋值 `\tau` 和寄存器更新规则。
2. `PA` 的 pebble assignment `\theta` 和 `place / lift / move` 规则。
3. `FO^* / MSO^*` 对比可作为模型能力边界的验证入口。

原文没有 XML、JSON、DSL 或标准交换格式。

### 交换与互操作

这篇论文最重要的互操作，不是工程互操作，而是谱系互操作：

1. `RA` 侧能与 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md) 和后续 register-family 节点对接。
2. `PA` 侧能与 [on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md](../on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md) 以及本轮补入的 [a-note-on-two-pebble-automata-over-infinite-alphabets/desc.md](../a-note-on-two-pebble-automata-over-infinite-alphabets/desc.md) 对接。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是寄存器赋值、pebble assignment、configuration 与逻辑比较框架。
- 仿真/执行支持：两类模型都可按 step relation 直接解释运行。
- 验证/分析支持：表达力比较、逻辑对照、universality / containment / nonemptiness 分析是主线。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是后续 data words、register-family、pebble-family 与 nominal / class-memory 研究的重要早期参照。

## 适用场景与需求前提

### 适用场景

适合以下类型的问题：

1. 无限名字域上的线性词语言。
2. 只关心 equality / repetition / freshness 风格关系，而不是算术关系。
3. 需要在演化树上区分“有限寄存器记忆”和“嵌套位置回看”这两条不同母线。

### 需求前提

1. 输入必须可压成线性序列。
2. 数据值最好只以“是否相等”的方式被观察。
3. 若走 `RA`，有效记忆槽数应能压成小常数；若走 `PA`，需求应明显依赖位置书签式回看。

### 不适用或高成本场景

若需求需要数值计算、时间、树结构、概率或复杂并发，`RA / PA` 都不是终点；若只需要普通有限字母表 regular language，则退回经典 `FA` 更直接。

## 与相邻形式主义的关系

相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)，`RA` 更明确使用寄存器口径而不是 windows；相对 [history-register-automata/desc.md](../history-register-automata/desc.md) 与 [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)，这里还没有 histories / global freshness 等更强机制；相对 [on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md](../on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md)，这里的 `PA` 是更一般、更早的 infinite-alphabet pebble 母线；相对 [automata-theory-in-nominal-sets/desc.md](../automata-theory-in-nominal-sets/desc.md)，这里还未走 orbit-finite / symmetry 路线，而是停留在最直接的 equality-memory 视角。

## 与本研究的关系

### 对 Project 1 的价值

它能把 `Data / Infinite-Alphabet` 演化树从“已有很多后继条目，但缺少公开可得母线说明”推进到“`RA` 与 `PA` 的元模型、边界和对比都有稳定代表条目”的状态。

### 作为目标形式主义还是中间表示

更适合作为谱系母型和理论判断入口，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

如果需求文本里反复出现“同一 ID 是否再次出现”“是否需要暂存某个位置稍后再比较”，LLM 应先区分这是 `RA` 型的有限名字记忆，还是 `PA` 型的位置书签回看，而不是一概丢进更重的 data logic。

### 现实限制

它的强项完全在理论边界，不在工程生态；原文也没有标准文件格式或成熟工具链。

## 重要的相关工作

### 奠基或前身工作

- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)

### 同类型或同家族工作

- [a-note-on-two-pebble-automata-over-infinite-alphabets/desc.md](../a-note-on-two-pebble-automata-over-infinite-alphabets/desc.md)
- [on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md](../on-pebble-automata-for-data-languages-with-decidable-emptiness-problem/desc.md)
- [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)
- [history-register-automata/desc.md](../history-register-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具链。

### 与本研究关系最紧的工作

- 它最适合在当前主蓝本树中同时作为 `Register Automata` 与 `Pebble Automata over Infinite Alphabets` 的公开可得代表参照。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Register Automata (RA) / Pebble Automata over Infinite Alphabets (PA)`
- 论文角色：家族比较 / 判定边界整理
- 核心功能：统一比较无限字母表上线性词的两类经典自动机母型，并给出逻辑与判定边界。
- 关键特性：寄存器记忆、pebble 回看、`FO^* / MSO^*` 对比、非空性 / 全体性不可判定边界。
- 构造方式：`RA` 的 `(Q,q_0,F,\tau_0,P)` 与 `PA` 的 `(Q,q_0,F,T)` 元组加 configuration semantics。
- 基础设施：纯理论模型，无工程标准或工具；核心在于模型定义、逻辑比较和判定问题。
- 适用场景：infinite-alphabet words、ID 重复 / freshness / 位置回看模式的理论建模。
- 需求前提：输入是线性词，数据关系主要是 equality，并且确实需要 finite-register 或 nested-pebble 两种不同 memory 机制之一。
- 状态：🟢

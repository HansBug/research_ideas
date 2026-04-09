# 无限字母表上的变量自动机 / Variable Automata over Infinite Alphabets

## 基本信息

- 标题：Variable Automata over Infinite Alphabets
- 中文标题：无限字母表上的变量自动机
- 作者：Orna Grumberg，Orna Kupferman，Sarai Sheinvald
- 发表：*Proceedings of the 4th International Conference on Language and Automata Theory and Applications (LATA 2010)*, pp. 561-572, 2010
- DOI：`10.1007/978-3-642-13089-2_47`
- 链接：https://doi.org/10.1007/978-3-642-13089-2_47
- 形式主义：`Variable Finite Automata (VFA) / Deterministic Variable Finite Automata (DVFA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 确定性子类整理
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `\mathcal V=(\Sigma,A)` 对、pattern automaton、legal instance / witnessing pattern 语义与 deterministic unwinding。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是带变量标签的 pattern automaton 与由 bounded/free variables 诱导的实例化规则。

## 简报

这篇论文的核心价值，是给 infinite-alphabet automata 提供了一个比 `register automata`、`data automata` 更接近普通 `NFA` 语法的模型本体。`VFA` 不再显式维护寄存器、pebbles 或 class decomposition，而是直接允许 pattern automaton 的边带上常量、bounded variables 和一个 free variable，再由“合法实例化”把 pattern word 解释成真实无限字母表上的词。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线上的一条“语法直观型”分支，强调用变量而不是显式寄存器机制来表达 equality pattern。
- 构造方式简述：先写一个普通有限字母表上的 pattern automaton，再把其中的 bounded variable 统一赋成某个真实数据值，把 free variable 的每次出现单独赋值。
- 基础设施与场景简述：原文是纯理论工作，但系统给出了 `VFA` 与 `DVFA` 的闭包性、可判定性和 determinization 边界，并进一步推广到 `VBA`。

```text
infinite-alphabet word -> witnessing pattern -> pattern automaton run -> variable/equality constraints -> acceptance
```

## 形式主义定义与核心对象

### 定义对象

`VFA` 处理的是来自无限字母表 `\Sigma` 的有限词。它不直接把真实字母存进寄存器，而是把“哪些位置必须是同一个值、哪些位置必须和已有值不同”编码进 pattern word。

### 核心抽象

按原文定义，可把 `VFA` 保守写成：

$$
\mathcal V=(\Sigma,A),\qquad A=(\Gamma_A,Q,Q_0,\delta,F),\qquad \Gamma_A=\Sigma_A\cup X\cup\{y\}
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是无限字母表。
2. `A` 是 pattern automaton，本体上就是一个普通 `NFA`。
3. `\Sigma_A\subseteq\Sigma` 是有限个可直接出现的常量字母。
4. `X` 是有限个 bounded variables；同一个变量的所有出现位置必须实例化成同一个真实字母。
5. `y` 是唯一的 free variable；它的不同出现位置可以实例化成不同字母，但必须与常量字母和 bounded variables 当前所代表的字母区分开。

接受语义可压成：

$$
w\in L(\mathcal V)\iff \exists v\in L(A)\ \text{s.t.}\ w\ \text{is a legal instance of}\ v
$$

上式中的符号逐项解释如下：

1. `v` 是 pattern automaton 接受的 witnessing pattern。
2. `w` 是无限字母表上的真实输入词。
3. `legal instance` 表示：常量字母保持不变，同一 bounded variable 的各次出现必须映成同一真实字母，而 free variable 的每次出现都必须与常量和 bounded-variable 取值不同。

### 一个最小例子与通俗解释

原文最典型的例子，是识别“某个字母至少出现两次”的语言。可取 pattern：

$$
(x+y)^*\cdot x\cdot (x+y)^*\cdot x\cdot (x+y)^*
$$

其中 `x` 是 bounded variable，`y` 是 free variable。它的含义是：

1. 先随便读一段，其中 `x` 表示“未来想重复的那个字母”，`y` 表示“和它不同的其他字母”。
2. 中间必须至少两次命中同一个 `x`。
3. 其余位置既可以继续是 `x`，也可以是与 `x` 不同的任意新字母。

通俗地说，`VFA` 像“把无限字母表上的相等关系直接写进自动机标签里”的 `NFA`。它不告诉你“寄存器里存了什么”，而是直接说“这里和前面的某个变量同值”“那里必须不同值”。

### 运行 / 接受 / 转移语义

`VFA` 的运行仍然是 pattern automaton 上的普通 `NFA` run；复杂性来自 pattern 到真实输入的实例化关系，而不是配置图本身。也就是说：

1. 先在 `A` 上找一条接受 pattern word `v` 的 run。
2. 再检查输入词 `w` 是否能作为 `v` 的 legal instance。
3. 只要存在这样的 `v`，`w` 就被接受。

因此，`VFA` 的关键不在“运行时存储”，而在“pattern language + variable interpretation”这两层分离。

### 语义边界

`VFA` 的增强点只有 equality pattern 和变量绑定，而没有：

1. 全局 freshness history；
2. per-data-value class memory；
3. 栈、树或 nested-data 结构；
4. 时间时钟或连续变量。

它比 `register automata` 更直观，但也因此失去了某些基于显式存储的表达方式。

### 关键性质与判定边界

原文给出的核心边界可压成：

$$
\mathcal L(\mathrm{VFA})\ \text{对}\ \cup,\ \cap\ \text{封闭，但不对}\ \mathrm{complement}\ \text{封闭}
$$

$$
\mathrm{nonemptiness}(\mathrm{VFA})\ \text{是 NL-complete},\qquad \mathrm{membership}(\mathrm{VFA})\ \text{是 NP-complete}
$$

$$
\mathrm{universality}(\mathrm{VFA}),\ \mathrm{containment}(\mathrm{VFA})\ \text{不可判定}
$$

$$
\mathcal L(\mathrm{DVFA})\ \text{对}\ \cup,\ \cap,\ \mathrm{complement}\ \text{封闭}
$$

上面几式中的符号逐项解释如下：

1. `DVFA` 是语义上“每个真实输入词至多一条接受运行”的 deterministic fragment。
2. `nonemptiness`、`membership`、`universality`、`containment` 分别对应空性、成员性、普遍性和包含性问题。
3. `DVFA` 虽然保住了布尔闭包和更好的判定性，但一般 `VFA` 的 determinization 仍不可判定。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 核心骨架仍是普通有限状态自动机。 |
| 事件 / 触发 | 强支持 | 每个输入位置对应 pattern word 的一个符号。 |
| 守卫 / 数据 | 强支持 | 通过 bounded/free variables 表达 equality 与不等关系。 |
| 层次 | 不支持 | 原始模型只处理线性词。 |
| 并发 / 同步 | 不支持 | 无显式并发组合。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 infinite-alphabet 模型。 |
| 可执行 / 可验证性 | 强理论支持 | `VFA` / `DVFA` 的闭包性与判定性边界都较清晰。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$\mathcal V=(\Sigma,A)$` | `VFA` 仍以一个普通 pattern automaton 为中心。 |
| pattern 字母表 | `$\Gamma_A=\Sigma_A\cup X\cup\{y\}$` | 常量、bounded variables 和 free variable 的统一语法。 |
| 语言定义 | `$w\in L(\mathcal V)\iff \exists v\in L(A)$ 且 $w$ 是 $v$ 的 legal instance` | 真实输入词通过 witnessing pattern 被接受。 |
| `VFA` 边界 | `$\cup,\cap$ closed; complement not closed` | 保留部分正则代数操作，但失去完整布尔闭包。 |
| `DVFA` 边界 | `$\cup,\cap,\mathrm{complement}$ closed` | deterministic fragment 更适合作为分析与规范子类。 |

## 构造方式与承载格式

### 建模入口

1. 先判断需求是否主要在描述“某些位置相同、某些位置不同”的 equality pattern。
2. 再决定哪些符号应写成常量字母，哪些应写成 bounded variable。
3. 只有当“任意不同的其余符号”是一个统一类别时，才适合用单一 free variable `y`。
4. 若需求依赖显式 freshness、history 或 per-ID 最近状态，应该转向 `FRA`、`Session Automata`、`CMA` 等模型。

### 机器可处理承载方式

机器可处理承载方式就是：

1. pattern automaton `A`；
2. `\Gamma_A` 上的变量标签；
3. legal instance / witnessing pattern 解释规则；
4. 若讨论确定性，还要考虑 unwinding 构造。

原文没有 XML、JSON 或 DSL 级载体。

### 交换与互操作

它与 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)、[fresh-register-automata/desc.md](../fresh-register-automata/desc.md) 和 [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md) 处理的是同一大类 infinite-alphabet / data-word 对象，但 `VFA` 明显更偏“语法化 pattern automata”，而不是寄存器或 class decomposition。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 pattern automaton、legal instance 和 unwinding。
- 仿真/执行支持：可先在 pattern word 上运行，再做实例化一致性检查。
- 验证/分析支持：`VFA` / `DVFA` 的闭包与判定问题分析较完整。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：主要存在于 automata over infinite alphabets 的理论生态中，不是工程标准线。

## 适用场景与需求前提

### 适用场景

适合表达“某个符号重复出现”“若两个位置共享同一数据值则必须满足某种 pattern”这类 equality-pattern 驱动的无限字母表语言。

### 需求前提

1. 输入对象最好就是线性词。
2. 关键约束主要是 equality / inequality，而不是 freshness 或 history。
3. 语言结构能够被少量变量和一个 pattern automaton 压缩出来。

### 不适用或高成本场景

如果需求依赖全局 freshness、per-session 生命周期、class-level memory、nested data 或 timed semantics，`VFA` 通常不够自然；此时更合适的是 `FRA`、`Session Automata`、`CMA/CRA` 或 timed/data-logic 家族。

## 与相邻形式主义的关系

相对 [finite-memory-automata/desc.md](../finite-memory-automata/desc.md) 与 [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)，`VFA` 的好处是语法更接近普通 `NFA`，坏处是无法直接表达寄存器/history 机制；相对 [two-variable-logic-on-words-with-data/desc.md](../two-variable-logic-on-words-with-data/desc.md) 与 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md)，它更像“pattern language”而不是 class-based automaton。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Data / Infinite-Alphabet` 支线补出了一条不同于 `register / class-memory / nominal` 的语法化分支，有助于把演化树从“只剩存储机制变体”扩成“同对象上的不同建模哲学”。

### 作为目标形式主义还是中间表示

更适合作为理论母型或中间表示，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

若需求文本主要在说“某些标识必须重复出现”“同一个名字出现两次才成立”“中间其他名字都可以不同”，LLM 可以先试 `VFA` 风格的 pattern abstraction，而不必立刻引入寄存器。

### 现实限制

它缺少工程生态和标准载体，强项主要在谱系补树与模型选择。

## 重要的相关工作

### 奠基或前身工作

- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)
- `register automata` 早期路线

### 同类型或同家族工作

- [fresh-register-automata/desc.md](../fresh-register-automata/desc.md)
- [a-robust-class-of-data-languages-and-an-application-to-learning/desc.md](../a-robust-class-of-data-languages-and-an-application-to-learning/desc.md)
- [automata-theory-in-nominal-sets/desc.md](../automata-theory-in-nominal-sets/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具。

### 与本研究关系最紧的工作

- 它最适合挂到当前演化树 `Finite Automata -> Data / Infinite-Alphabet` 的 `Variable Finite Automata` 子枝。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论

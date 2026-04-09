# 数据词上的二变量逻辑 / Two-Variable Logic on Words with Data

## 基本信息

- 标题：Two-Variable Logic on Words with Data
- 中文标题：数据词上的二变量逻辑
- 作者：Mikołaj Bojańczyk，Anca Muscholl，Thomas Schwentick，Luc Segoufin，Claire David
- 发表：*Proceedings of the 21st Annual IEEE Symposium on Logic in Computer Science (LICS 2006)*, pp. 7-16, 2006
- DOI：`10.1109/LICS.2006.51`
- 链接：https://doi.org/10.1109/LICS.2006.51
- 形式主义：`Data Automata (DA)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出 / 逻辑-自动机桥接
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `DA = (A,B)` 二层骨架、marked-string projection、class string 与到 multicounter automata 的空性化简。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 base transducer、class automaton、data word 等价类分解与 Petri-net style emptiness reduction。

## 简报

这篇论文虽然标题写的是二变量逻辑，但它对文库更关键的贡献其实是正式提出并使用 `Data Automata` 这一自动机骨架：先用一个 base transducer 扫整条 data word，再把每个数据值对应的 class string 交给同一个 class automaton 检查。这样一来，`FO^2(\sim,<,+1)` 上的可满足性就被压成了一个明确的 automata model，而不是只停留在逻辑判定结论上。

- 形式主义定位：`Finite Automata -> Data / Infinite-Alphabet` 支线里，`Data Automata` 是把“无限数据值 + 只允许 equality 测试”稳定自动机化的母节点。
- 构造方式简述：`DA` 由全局 `base automaton` 和按数据类逐类运行的 `class automaton` 组成；前者决定每个位置输出什么有限标记，后者只看同一数据值抽出来的子串。
- 基础设施与场景简述：原文是纯理论工作，但给出了到 multicounter automata 的 emptiness reduction、与 `FO^2` / `EMSO^2` 的桥接，以及 finite / infinite data words 的统一入口。

```text
data word -> marked string projection -> base transducer output -> per-class string -> class automaton acceptance
```

## 形式主义定义与核心对象

### 定义对象

`DA` 面向的是 data words：每个位置既有一个来自有限字母表的标签，也有一个来自无限域的数据值。模型默认只允许对数据值做 equality 判断，不允许算术或数据值全序比较。

### 核心抽象

原文把 `Data Automaton` 定义为：

$$
D=(A,B)
$$

上式中的符号逐项解释如下：

1. `A` 是一个 nondeterministic letter-to-letter string transducer，也就是 `base automaton`。
2. `B` 是一个 nondeterministic finite automaton，也就是 `class automaton`。
3. `A` 的输入字母表是 `\Sigma \times \{0,1\}`，其中额外的 `0/1` 位来自 marked-string projection。
4. `A` 的输出字母表是某个有限字母表 `\Gamma`。
5. `B` 的输入字母表是 `\Gamma`。

设 data word 为

$$
w=(a_1,d_1)\cdots(a_n,d_n)\in(\Sigma\times D)^*
$$

则 `DA` 的接受语义可压成：

$$
w\in L(D)\iff \exists\, b_1\cdots b_n\in\Gamma^* \text{ 是 } A \text{ 在 } mstr(w) \text{ 上某次接受运行的输出，且对 } w \text{ 的每个 data class } X=\{x_1<\cdots<x_k\},\ B \text{ 接受 } b_{x_1}\cdots b_{x_k}
$$

上式中的符号逐项解释如下：

1. `mstr(w)` 是 `w` 的 marked string projection，保留有限标签并额外标出相邻位置是否发生数据类切换。
2. `b_1\cdots b_n` 是 base transducer 沿整条输入生成的有限标记串。
3. `X` 是同一数据值在 `w` 中出现位置组成的等价类。
4. `b_{x_1}\cdots b_{x_k}` 是从全局输出串中抽出的某个 class string。
5. `B` 对每个 class string 都接受，才说明整个 data word 被 `D` 接受。

### 一个最小例子与通俗解释

原文给出的直观例子是“data word 中至少有两个不同数据类都带有标签 `a`”。做法很直接：

1. base transducer 在全局扫描时 nondeterministically 选出两个 `a` 位置，并把它们输出成 `1`，其他位置输出成 `0`。
2. class automaton 检查每个数据类对应的 `0/1` 子串中至多出现一个 `1`。
3. 这样一来，只要最终成功，就说明那两个被选中的 `a` 来自两个不同的数据类。

通俗地说，`DA` 像“先在整条日志上做一次全局打标，再把每个 ID 的日志单独抽出来验一遍”的两层自动机。它不是把所有数据值都塞进寄存器，而是把“同一个数据值对应的所有位置”当成一类对象统一处理。

### 运行 / 接受 / 转移语义

`DA` 的运行分成两层：

1. `A` 在整条 `mstr(w)` 上单遍运行，产出全局有限输出串。
2. 对每个数据值 `d`，把 `w` 中所有携带 `d` 的位置投影出来，形成一个 class string，再由同一个 `B` 重复检查。

因此，`DA` 的核心语义不是单一 configuration graph，而是“全局 transducer run + 每个 class 的局部 NFA run”这一组合语义。原文之所以能把逻辑压到自动机，关键就在这里：全局顺序由 `A` 管，按数据值聚合的局部一致性由 `B` 管。

### 语义边界

`DA` 只处理“有限标签 + 无限数据值 + equality-only”这条边界。它不提供：

1. 数据值上的数值运算；
2. 数据值的线性顺序；
3. 栈、树或层次结构；
4. 时间时钟或连续变量。

也就是说，它比普通 `FA` 强在能围绕 data class 组织语义，但还没有走到 `register / history / class-memory / nested-data` 那些更强的记忆式模型。

### 关键性质与判定边界

原文给出的关键结果可压成：

$$
FO^2(\sim,<,+1)\ \leq\ \mathrm{DA}
$$

$$
EMSO^2(\sim,<,+1)\ \equiv\ \mathrm{DA}
$$

$$
\mathrm{emptiness}(\mathrm{DA})\ \leq\ \mathrm{emptiness}(\mathrm{Multicounter\ Automata})
$$

$$
\mathcal L(\mathrm{DA}) \text{ 对 } \cup,\ \cap,\ \mathrm{renaming} \text{ 封闭}
$$

上面几式中的符号逐项解释如下：

1. `FO^2(\sim,<,+1)` 是带数据值相等谓词、顺序和后继的二变量一阶逻辑。
2. `EMSO^2` 是其存在二阶闭包。
3. `\mathrm{emptiness}` 表示判断自动机语言是否为空。
4. `Multicounter Automata` 与 Petri-net reachability 紧密相关，因此 `DA` 的空性虽然可判定，但复杂度很高。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `A` 与 `B` 都是有限状态骨架。 |
| 事件 / 触发 | 强支持 | 每个 data-word 位置触发一次全局输出，并按 class 分派给 `B`。 |
| 守卫 / 数据 | 强支持 | 支持按数据值 equality 划分 class。 |
| 层次 | 不支持 | 对象仍是线性 data word。 |
| 并发 / 同步 | 不支持 | 没有显式并发组件；只提供 class-level 抽取。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | 空性可判定，并与 `FO^2/EMSO^2` 精确桥接。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$D=(A,B)$` | `Data Automata` 的标准骨架。 |
| 全局输入 | `$mstr(w)\in(\Sigma\times\{0,1\})^*$` | 给 base automaton 的输入。 |
| class 检查 | `$B(b_{x_1}\cdots b_{x_k})$` | 对每个数据类分别验证。 |
| 闭包性质 | `$\cup,\ \cap,\ \mathrm{renaming}$` | `DA` 保留基本 automata-theory 代数操作。 |
| 判定边界 | `$\mathrm{emptiness}(\mathrm{DA})$ decidable` | 通过 multicounter automata / Petri nets 化简实现。 |

## 构造方式与承载格式

### 建模入口

1. 先把对象压成 data word，而不是一般树或图。
2. 把全局顺序上的决策放进 base transducer。
3. 把“同一数据值内部必须满足的规律”放进 class automaton。
4. 如果需求需要显式记住若干活动数据值，而不是只看 class 子串，就应该转向 `RA / CMA / HRA`。

### 机器可处理承载方式

机器可处理承载方式就是：

1. `A` 的有限状态转导器；
2. `B` 的有限状态接受器；
3. data word 的 marked projection；
4. 每个数据类的 class string 抽取规则。

原文没有 XML、JSON 或 DSL 级载体。

### 交换与互操作

它与 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 的关系最紧：后者把 `DA` 重写成更直观的 `CMA`。它也构成了 [an-automaton-over-data-words-that-captures-emso-logic/desc.md](../an-automaton-over-data-words-that-captures-emso-logic/desc.md) 和 [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md) 这些后继模型的直接母型。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 marked-string projection、class extraction 与 base/class 双自动机骨架。
- 仿真/执行支持：可直接按“先全局转导、再逐类检查”的两阶段语义运行。
- 验证/分析支持：空性到 multicounter automata 的化简，逻辑到自动机的有效翻译。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：是后续 `CMA`、`CRA`、`HRA`、data-tree/XPath 路线的基准理论节点。

## 适用场景与需求前提

### 适用场景

适合 per-ID trace、XML-like data words、带无限标识符的日志语言，以及“要同时看全局顺序和按 data class 局部规律”的对象。

### 需求前提

1. 输入能压成线性 data word。
2. 关键数据关系主要是 equality，而不是算术。
3. 局部数据约束能够按“每个 data class 独立检查”来分解。

### 不适用或高成本场景

如果需求依赖有限寄存器中的活动名字、freshness、nested data、树导航或实时间语义，`DA` 就偏弱；此时更适合 `RA/FRA`、`CMA`、`ARA/ATRA` 或 timed family。

## 与相邻形式主义的关系

相对普通 `FA`，`DA` 多了“按数据类抽取并二次接受”的层；相对 [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md) 中的 `CMA`，它更偏“二层分工”而不是“每个数据值保留 last-state memory”；相对 [alternating-register-automata-on-finite-words-and-trees/desc.md](../alternating-register-automata-on-finite-words-and-trees/desc.md)，它还没有寄存器线程和 alternation，只是 equality-class 分组。

## 与本研究的关系

### 对 Project 1 的价值

它把当前演化树中的 `Data / Infinite-Alphabet` 支线补上了 `Data Automata` 母节点，使后续 `CMA / CRA / ADC / HRA` 不再是悬空分支。

### 作为目标形式主义还是中间表示

更适合作为理论母型或中间表示，而不是控制系统最终交付语言。

### 对需求到模型生成的启发

当需求文本里反复出现“同一个 ID 的所有出现位置必须满足某个局部规律，但全局顺序又要额外筛选”时，LLM 可以优先尝试 `DA` 风格的两层分解，而不是直接退回普通 `FSM`。

### 现实限制

它的主要价值是谱系和可判定性，而不是工程工具生态；原文没有公开实现和标准交换格式。

## 重要的相关工作

### 奠基或前身工作

- `FO^2` / `EMSO^2` on data words
- [finite-memory-automata/desc.md](../finite-memory-automata/desc.md)

### 同类型或同家族工作

- [on-notions-of-regularity-for-data-languages/desc.md](../on-notions-of-regularity-for-data-languages/desc.md)
- [an-automaton-over-data-words-that-captures-emso-logic/desc.md](../an-automaton-over-data-words-that-captures-emso-logic/desc.md)
- [weak-and-nested-class-memory-automata/desc.md](../weak-and-nested-class-memory-automata/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准。

### 与本研究关系最紧的工作

- 它最适合补到当前演化树 `Data / Infinite-Alphabet` 支线的 `Data Automata` 母节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论

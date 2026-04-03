# 非确定性流式字符串转导器 / Nondeterministic Streaming String Transducers

## 基本信息

- 标题：Nondeterministic Streaming String Transducers
- 中文标题：非确定性流式字符串转导器
- 作者：Rajeev Alur, Jyotirmoy V. Deshmukh
- 发表：International Colloquium on Automata, Languages, and Programming (`ICALP 2011`)
- DOI：`10.1007/978-3-642-22012-8_1`
- 链接：https://www.cis.upenn.edu/~alur/Icalp11.pdf
- 形式主义：Nondeterministic Streaming String Transducers (`NSST`)
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文不附公开实现；机器可处理入口是状态集合、copyless 赋值集合、转移集和输出函数。
- 标准/格式获取方式：原文没有 XML/JSON 标准，核心承载方式是 `NSST` 元组和 computation summary 语义。

## 简报

这篇论文做的不是把 `SST` 简单“加个 nondeterminism”而已，而是把单遍 copyless 字符串变量模型从函数提升到了 relation。它证明 `NSST` 与 nondeterministic `MSO` string transduction 等价，同时把 functional `NSST`、一般 `NSST`、`ngsm`、`2ngsm` 之间的表达力和判定性边界都重新整理了一遍。

- 形式主义定位：`SST` 的关系化扩展，是 string relation 支线上的现代单遍模型。
- 构造方式简述：每步仍是单遍读取一个输入符号并做 copyless 变量更新，但允许对下一状态和赋值选择 nondeterministic 分支。
- 基础设施与场景简述：原文没有工程工具线，但给出到 nondeterministic `MSO` transduction 的精确等价，并系统讨论 functionality 与 equivalence 问题。

```text
输入字符串 -> nondeterministic 状态迁移 + copyless 变量赋值 -> 多个可能输出 -> string relation
```

## 形式主义定义与核心对象

### 定义对象

`NSST` 的输出不是单个字符串函数值，而是一个输出集合。因此它描述的是从输入串到输出串集合的 relation，而不是 partial function。

### 核心抽象

原文第 2.2 节将 `NSST` 定义为：

$$
T = (Q, \Sigma, \Gamma, X, E, q_0, F)
$$

上式中的符号逐项解释如下：

1. `Q` 是有限非空状态集。
2. `\Sigma` 和 `\Gamma` 分别是输入与输出字母表。
3. `X` 是有限个字符串变量。
4. `E \subseteq Q \times \Sigma \times A \times Q` 是转移集。
5. `A` 是变量集 `X` 上的 copyless 赋值集合。
6. `q_0` 是初始状态。
7. `F : Q \to (X \cup \Gamma)^*` 是部分输出函数。

其中 copyless 赋值的核心限制是：

$$
\forall x \in X,\ x \text{ 在 } \{ \alpha(y) \mid y \in X \} \text{ 中至多出现一次}
$$

这说明 nondeterminism 增加的是分支选择，而不是对旧变量值的任意复制。

### 一个最小例子与通俗解释

原文给出的经典例子是关系：

$$
R_{ss} = \{ (w, u\#v) \mid u,v \text{ 都是 } w \text{ 的子序列} \}
$$

可用单状态、两个变量 `x,y` 的 `NSST` 实现。对每个输入符号 `a`，机器可以 nondeterministically 决定把 `a` 追加到 `x`、追加到 `y`、同时追加到二者，或都不追加，最终输出 `x#y`。

通俗地说，`NSST` 像一个“单遍扫输入、一路猜输出切分方案”的字符串关系生成器。它保留 `SST` 的流式和 copyless 骨架，但允许多个合法输出并存。

### 运行 / 接受 / 转移语义

原文不是直接按单一路径给语义，而是用 summary 归纳所有可能运行。记 `\mathrm{id}` 为恒等赋值，则 summary 函数可写成：

$$
\Delta(q,\epsilon) = \{(\mathrm{id}, q)\}
$$

$$
\Delta(q,wa) = \{(\alpha_w \circ \alpha, q') \mid \exists q_1,\ (\alpha_w,q_1)\in\Delta(q,w)\land(q_1,a,\alpha,q')\in E \}
$$

上式中的符号逐项解释如下：

1. `\Delta(q,w)` 收集从状态 `q` 读完串 `w` 后的所有“赋值效果 + 目标状态”对。
2. `\alpha_w` 是前缀 `w` 累积得到的变量更新效果。
3. `\alpha` 是当前这一步读取 `a` 时所选中的 copyless 赋值。
4. `\circ` 表示赋值按顺序复合。

若 `\nu_\epsilon` 把每个变量初始化为空串，则整机语义为：

$$
\llbracket T \rrbracket(w) = \{ \nu_\epsilon(\alpha_w \circ F(q)) \mid (\alpha_w, q)\in\Delta(q_0,w),\ F(q)\text{ 已定义} \}
$$

这条式子说明：同一输入可以沿不同分支走到不同 summary，因此得到多个输出串。

### 语义边界

相对 [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)，`NSST` 从函数扩展到 relation；相对 `ngsm`，它保留单遍流式约束，但变量更新更强；相对带 `\epsilon`-moves 的 transducer，它仍然坚持每次消费一个输入符号，因此整体保持 bounded-length。

### 关键性质与判定边界

论文的主结论是：

$$
\mathrm{NSST} \equiv \mathrm{NMSO}
$$

上式中的符号逐项解释如下：

1. `\mathrm{NSST}` 是 nondeterministic streaming string transducer 可定义的 relation 类。
2. `\mathrm{NMSO}` 是 nondeterministic `MSO`-definable string transduction。

原文还给出几个非常重要的边界：

$$
\mathrm{Functional\ NSST} \equiv \mathrm{DSST}
$$

$$
\forall T \in \mathrm{NSST},\ \exists c,\ \forall w,\ \forall u \in \llbracket T \rrbracket(w),\ |u| \le c|w|
$$

并证明：

1. 一般 `NSST` 的 functionality 检查在 `PSPACE` 中。
2. 一般 `NSST` 的 equivalence 不可判定。
3. functional `NSST` 的 equivalence 是 `PSPACE`-complete。

这组结果非常适合解释为什么 `NSST` 是一个“表达力更强，但分析边界也明显变化”的关系模型。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 仍以有限状态控制为核心。 |
| 事件 / 触发 | 强支持 | 每个输入符号触发一次状态分支和变量并行更新。 |
| 守卫 / 数据 | 部分支持 | 有字符串变量与 copyless 赋值，但变量主要用于构造输出而非任意测试。 |
| 层次 | 不支持 | 输入对象仍是线性串。 |
| 并发 / 同步 | 不支持 | 不是并发模型。 |
| 时间约束 | 不支持 | 无时钟、无显式时间。 |
| 连续动态 / 随机性 | 不支持 | 是 nondeterministic relation，而不是概率模型。 |
| 可执行 / 可验证性 | 强支持 | 单遍执行、bounded-length、functionality 可判定。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$T=(Q,\Sigma,\Gamma,X,E,q_0,F)$` | `NSST` 的标准骨架。 |
| summary 语义 | `$\Delta(q,wa)=\{(\alpha_w\circ\alpha,q')\mid ...\}$` | 用赋值复合表示所有可能运行效果。 |
| 输出集合 | `$\llbracket T \rrbracket(w)=\{\nu_\epsilon(\alpha_w\circ F(q))\mid ...\}$` | 同一输入可对应多个输出。 |
| 表达力等价 | `$\mathrm{NSST}\equiv\mathrm{NMSO}$` | 精确刻画 nondeterministic string transductions。 |
| functional 边界 | `$\mathrm{Functional\ NSST}\equiv\mathrm{DSST}$` | 单值子类退回确定性 `SST`。 |

## 构造方式与承载格式

### 建模入口

建模时需要：

1. 选定输入/输出字母表。
2. 定义状态集和字符串变量。
3. 枚举 copyless 赋值集合。
4. 为每个状态和输入符号写出可能的赋值-迁移分支。
5. 指定部分输出函数。

### 机器可处理承载方式

`NSST` 的机器承载方式是：

1. 转移关系 `E`。
2. copyless 赋值表 `A`。
3. 输出函数 `F`。
4. summary 语义 `\Delta`。

它仍然不是 `DSL` 或工程交换标准。

### 交换与互操作

原文给出的互操作线主要是：

1. `NSST <-> NMSO`
2. `Functional NSST <-> DSST`
3. `NSST` 与 `ngsm`、`2ngsm`、`\epsilon`-`NSST` 的表达力比较

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：以 copyless assignment、summary 与 `MSO` 编码为主。
- 仿真/执行支持：天然支持单遍逐符号执行，但需要保存多条 nondeterministic 路径。
- 验证/分析支持：functionality 可判定，functional 子类 equivalence 可判定。
- 代码生成/转换支持：原文未讨论工程代码生成。
- 标准化或社区生态：主要承担 string relation 理论母型作用，而不是工程标准载体。

## 适用场景与需求前提

### 适用场景

适合一遍扫描即可生成多个候选输出的字符串关系问题，例如子序列抽取、候选重写、非确定性字符串变换和 relation synthesis 理论分析。

### 需求前提

1. 输入对象是线性字符串。
2. 输出可以是集合而不是唯一值，或者至少需要先在 relation 口径下分析。
3. 输出构造仍应满足 copyless 单遍更新。

### 不适用或高成本场景

若需求天然是单值函数，并且更关心可执行实现或直接工程化，那么 deterministic `SST` 往往更简洁；若需要无界复制或双向读头，则应考虑其他 transducer 模型。

## 与相邻形式主义的关系

相对 [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)，它把 `SST` 从函数扩成 relation；相对 [a-characterization-of-machine-mappings/desc.md](../a-characterization-of-machine-mappings/desc.md)，它仍然是一遍式有限状态转导，但变量更新自由度更高；相对带 `\epsilon` 的 transducer，它保留每步消费一个输入符号的 bounded-length 好性质。

## 与本研究的关系

### 对 Project 1 的价值

它让当前演化树里的字符串转导主线不再停在 deterministic `SST`，而是补出了一个明确的 nondeterministic 分支，从而更完整地覆盖 automata-theory 中“函数 vs 关系”的模型分层。

### 作为目标形式主义还是中间表示

更适合作为理论中间表示和谱系节点，而不是控制系统主线的最终建模语言。

### 对需求到模型生成的启发

当需求文本本身允许多个候选结构化输出，而暂时不想过早做 disambiguation 时，relation 型模型比直接压成 deterministic 目标形式更自然。

### 现实限制

一般 `NSST` 的 equivalence 不可判定，这说明 relation 扩展虽强，但也显著抬高了后续分析成本。

## 重要的相关工作

### 奠基或前身工作

- [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)
- classical `ngsm` / `2ngsm` string transducer 路线

### 同类型或同家族工作

- [a-characterization-of-machine-mappings/desc.md](../a-characterization-of-machine-mappings/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或公共工具线。

### 与本研究关系最紧的工作

- 它最适合补当前演化树里 `Streaming String Transducers` 下的 nondeterministic 子节点。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：Nondeterministic Streaming String Transducers (`NSST`)
- 论文角色：模型扩展
- 核心功能：在单遍 copyless 字符串变量框架下定义 string relation，而不只是一元函数。
- 关键特性：nondeterministic 分支、summary 语义、与 `NMSO` 等价、bounded-length、functionality 可判定。
- 构造方式：`(Q,\Sigma,\Gamma,X,E,q_0,F)` 元组加 copyless assignment 和 summary 递推。
- 基础设施：理论上与 `MSO` 和 deterministic `SST` 紧密互操作，但无工程标准。
- 适用场景：非确定性字符串关系、候选输出生成与 string relation 理论分析。
- 需求前提：输入是线性串，输出允许多值，且仍满足单遍 copyless 更新。
- 状态：🟢

# 偏函数及其复合的双向卵石转导器 / Two-way pebble transducers for partial functions and their composition

## 基本信息

- 标题：Two-way pebble transducers for partial functions and their composition
- 中文标题：偏函数及其复合的双向卵石转导器
- 作者：Joost Engelfriet
- 发表：*Acta Informatica*, 52:559-571, 2015
- DOI：`10.1007/s00236-015-0224-3`
- 链接：https://doi.org/10.1007/s00236-015-0224-3
- 形式主义：`Two-Way Pebble Transducers / k-Pebble Transducers`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：闭包性质
- 工具/实现获取方式：原文未提供实现；机器可处理入口是 `k`-pebble transducer 元组、nested pebble configurations 和 transduction semantics。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是字符串输入带、endmarkers、状态/转移表和 pebble 栈式生命周期约束。

## 简报

这篇论文研究的是字符串上的 two-way finite-state transducer 加 nested pebbles 之后，偏函数确定化和函数复合还能做到什么程度。它证明每个由 nondeterministic `k`-pebble transducer 实现的 partial function 都可由 deterministic `k`-pebble transducer 实现，并把两个 deterministic pebble transductions 的复合压到最小 pebble 数 `(k+1)(m+1)-1`。

- 形式主义定位：字符串转导主线上的 two-way + nested-pebble 扩展，是 `2gsm`、pebble automata 和 tree-walking transducer 理论之间的桥节点。
- 构造方式简述：机器在带左右端标记的输入带上左右移动，按 nested discipline drop/lift 有限个 pebbles，并在每一步输出一个字符串片段。
- 基础设施与场景简述：原文是纯理论模型，但给出与 counting transducers / `2gsm` / `MSO` transductions 的归约联系，以及确定化与复合闭包结论。

```text
输入字符串 -> two-way finite control + nested pebbles -> 增量输出 -> partial-function transduction / composition
```

## 形式主义定义与核心对象

### 定义对象

`k`-pebble transducer 面向的是 string-to-string transduction，而不是语言接受。它的输入是带端标记的线性串，输出是一条逐步追加生成的字符串。

### 核心抽象

原文把 `k`-pebble transducer 定义为：

$$
M = (\Sigma,\Delta,Q,q_0,F,\delta)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是输入字母表。
2. `\Delta` 是输出字母表。
3. `Q` 是有限状态集。
4. `q_0 \in Q` 是初始状态。
5. `F \subseteq Q` 是终态集合。
6. `\delta` 是有限转移集。

每条转移形如：

$$
(q,\sigma,b) \mapsto (q',\varphi,w)
$$

上式中的符号逐项解释如下：

1. `q,q'` 是源状态和目标状态。
2. `\sigma \in \Sigma \cup \{\triangleleft,\triangleright\}` 是当前输入符号或端标记。
3. `b \in \{0,1\}^k` 指示哪些 pebbles 正在当前格子上。
4. `\varphi \in \{\mathrm{right},\mathrm{left},\mathrm{drop},\mathrm{lift}\}` 是头移动或 pebble 操作。
5. `w \in \Delta^*` 是本步追加到输出带的字符串片段。

核心约束是 pebble lifetime 必须 nested：任意时刻只能 drop 下一个 pebble，且只能 lift 当前最后一个 pebble。

### 一个最小例子与通俗解释

原文的 Example 1 给了一个很直观的 4-pebble 用法：用 pebbles 1 和 2 枚举输入串里的所有非空子串 `v`，用 pebbles 3 和 4 枚举所有非空子串 `w`，然后检查 `vw` 是否落在给定正则语言 `R` 中；若是，就输出 `v#w#`。这样机器虽然只有有限状态，但借助 pebbles 能系统枚举多段位置组合。

通俗地说，它像一个“会在纸带上来回扫、还能插几个书签并边扫边抄输出的有限状态转写器”。普通 `GSM/SST` 基本顺着输入往前走；two-way pebble transducer 则可以反复回看并用 pebbles 固定区间边界。

### 运行 / 接受 / 转移语义

对输入串 `u`，原文把配置写成：

$$
(q,i,\pi)
$$

上式中的符号逐项解释如下：

1. `q` 是当前状态。
2. `i` 是当前读头所在的输入格编号。
3. `\pi \in \{0,\ldots,|u|+1\}^{\le k}` 是当前 pebble configuration。

转导语义定义为：

$$
\tau_M = \{ (u,v) \in \Sigma^* \times \Delta^* \mid \exists (q,i,\pi),\ (q_0,0,\lambda,\lambda)\vdash_u^*(q,i,\pi,v),\ q\in F \}
$$

上式中的符号逐项解释如下：

1. `\lambda` 是空 pebble configuration 或空输出串。
2. `\vdash_u^*` 是在输入 `u` 上的多步计算关系。
3. `v` 是运行过程中累积输出的字符串。

当 `M` deterministic 时，`\tau_M` 是一个 partial function。

### 语义边界

相对 [a-characterization-of-machine-mappings/desc.md](../a-characterization-of-machine-mappings/desc.md) 的 `GSM`，它允许 two-way 扫描和 nested pebbles，因此能用有限控制实现更复杂的区间枚举和回看；相对 unrestricted pebble/transducer，它仍保留 nested lifetime 约束；相对 tree pebble transducers，它是 monadic-tree / string restriction。

### 关键性质与判定边界

原文第一个主结论是：

$$
\forall k \ge 0,\ \forall \tau \in \mathrm{PT}_k,\ \tau \text{ 是 partial function} \Rightarrow \tau \in \mathrm{DPT}_k
$$

第二个主结论是：

$$
\mathrm{DPT}_k \circ \mathrm{DPT}_m \subseteq \mathrm{DPT}_{km+k+m}
$$

上面两式中的符号逐项解释如下：

1. `\mathrm{PT}_k` 是 `k`-pebble transducers 定义的 transduction 类。
2. `\mathrm{DPT}_k` 是 deterministic `k`-pebble transducers 定义的 transduction 类。
3. `\circ` 是函数/关系复合。
4. `km+k+m=(k+1)(m+1)-1` 是作者证明的组合 pebble 数上界，并且是最小可达阶。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限状态控制仍是核心。 |
| 事件 / 触发 | 强支持 | 读头每步读取当前符号并触发状态/输出更新。 |
| 守卫 / 数据 | 部分支持 | 可测试当前格上 pebble presence，但没有一般数据变量。 |
| 层次 | 不支持 | 输入对象是线性串。 |
| 并发 / 同步 | 不支持 | 不是并发模型。 |
| 时间约束 | 不支持 | 无时钟。 |
| 连续动态 / 随机性 | 不支持 | 无连续或概率语义。 |
| 可执行 / 可验证性 | 强理论支持 | 有确定化、复合闭包和到 counting transducer / `2gsm` 的归约。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型元组 | `$M=(\Sigma,\Delta,Q,q_0,F,\delta)$` | `k`-pebble transducer 的有限控制骨架。 |
| 单步转移 | `$(q,\sigma,b)\mapsto(q',\varphi,w)$` | 当前符号、pebble presence、动作和输出片段共同决定一步更新。 |
| 配置 | `$(q,i,\pi)$` | 运行状态由状态、读头位置和 pebble placement 组成。 |
| 转导语义 | `$\tau_M=\{(u,v)\mid ...\}$` | 每条接受运行定义一个输入输出对。 |
| 复合闭包 | `$\mathrm{DPT}_k\circ\mathrm{DPT}_m\subseteq\mathrm{DPT}_{km+k+m}$` | deterministic pebble transductions 对复合封闭，且 pebble 上界可控。 |

## 构造方式与承载格式

### 建模入口

1. 先确定输入/输出字母表和需要实现的字符串 partial function。
2. 设计有限状态、端标记处理和每步输出片段。
3. 决定哪些位置边界需要用 pebbles 记录，并保证 drop/lift 服从 nested discipline。
4. 若要证明复合或确定化性质，再通过 counting-transducer / `2gsm` 归约线来做理论分析。

### 机器可处理承载方式

机器可处理承载方式是状态转移表、pebble 操作指令、端标记输入带和 transduction 语义，不是工程 DSL。

### 交换与互操作

原文最核心的互操作线是：

1. `k`-pebble transducer `<->` `k`-counting transducer
2. `0`-pebble transducer / `2gsm` `<->` `MSO`-definable string transduction
3. 因此把 nested-pebble transduction 接回 classic two-way transducer 理论

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：以转移表、pebble configuration 和端标记输入带为主。
- 仿真/执行支持：可按 two-way move + drop/lift + output append 直接解释运行。
- 验证/分析支持：确定化、uniformization、composition closure 和 MSO/transducer 归约是重点。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 two-way transducer / pebble automata / nested-pebble transformation 的理论支线。

## 适用场景与需求前提

### 适用场景

适合需要反复回看输入、枚举位置组合、并按有限状态规则生成输出串的理论 transduction 问题，尤其是 partial function 和 compositional transduction 分析。

### 需求前提

1. 输入输出对象必须是线性字符串。
2. 输出应可按有限控制逐步追加生成。
3. 若需要记住多个位置边界，这些书签的生命周期必须能按 nested 方式组织。

### 不适用或高成本场景

如果需求天然是树对象、需要 bottom-up 子树汇总、或需要一般数据算术/时间约束，就应转向 tree transducer、register automata 或 timed/hybrid families。

## 与相邻形式主义的关系

相对 [a-characterization-of-machine-mappings/desc.md](../a-characterization-of-machine-mappings/desc.md) 的 `GSM` 与 [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md) 的 `SST`，它放弃单遍顺扫，换取 two-way 回看和 nested pebbles；相对 [tree-transducers-l-systems-and-two-way-machines/desc.md](../tree-transducers-l-systems-and-two-way-machines/desc.md)，它是 monadic-tree/string 限制下的 pebble transducer 版本；相对 [automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md](../automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md)，这里主对象是 transduction 而不是 recognition / logic characterization。

## 与本研究的关系

### 对 Project 1 的价值

它能把字符串 transducer 支线从 `GSM/SST/NSST` 进一步补到 `two-way + nested-pebble` 方向，使演化树里的“单遍 vs 双向回看 vs pebble 边界”更完整。

### 作为目标形式主义还是中间表示

更适合作为谱系节点和字符串变换中间表示，而不是控制系统主线的最终形式主义。

### 对需求到模型生成的启发

当需求描述的是“输出要根据多个输入区间组合而成，而且区间边界需要先记住、再回看”时，LLM 可以考虑先生成 two-way pebble transducer 风格的中间结构，而不是强行压成单遍 `SST`。

### 现实限制

这类模型几乎没有工程工具生态，而且 nested-pebble 编程直觉比普通 `SST/GSM` 更重，主要价值仍在理论谱系和组合性质。

## 重要的相关工作

### 奠基或前身工作

- [a-characterization-of-machine-mappings/desc.md](../a-characterization-of-machine-mappings/desc.md)
- [tree-transducers-l-systems-and-two-way-machines/desc.md](../tree-transducers-l-systems-and-two-way-machines/desc.md)
- [automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md](../automata-with-nested-pebbles-capture-first-order-logic-with-transitive-closure/desc.md)

### 同类型或同家族工作

- [expressiveness-of-streaming-string-transducers/desc.md](../expressiveness-of-streaming-string-transducers/desc.md)
- [nondeterministic-streaming-string-transducers/desc.md](../nondeterministic-streaming-string-transducers/desc.md)

### 标准 / 格式 / 工具链工作

- 原文未提供工程标准或工具线。

### 与本研究关系最紧的工作

- 它最适合补当前演化树里 `Generalized Finite Automata / Transductions` 下的 `Two-Way Pebble Transducers` 子枝，同时在 desc 中保留到 tree-walking pebble line 的旁系关系。

## 文献分类总结

- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Two-Way Pebble Transducers / k-Pebble Transducers`
- 论文角色：闭包性质
- 核心功能：在 two-way finite-state transducer 上加入 nested pebbles，并证明 partial-function 确定化与 deterministic 复合闭包。
- 关键特性：two-way scanning、nested pebbles、incremental output、partial-function determinization、composition with minimal pebble bound。
- 构造方式：`M=(\Sigma,\Delta,Q,q_0,F,\delta)` + `(q,\sigma,b)\mapsto(q',\varphi,w)` 转移 + pebble configuration 语义。
- 基础设施：纯理论模型，无工程标准或工具。
- 适用场景：字符串 transduction、区间枚举、partial-function composition、two-way transducer 理论分析。
- 需求前提：输入输出是线性串，输出可逐步追加，位置书签可按 nested discipline 使用。
- 状态：🟢

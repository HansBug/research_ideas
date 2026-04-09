# WALi：嵌套词自动机 / WALi: Nested-Word Automata

## 基本信息

- 标题：WALi: Nested-Word Automata
- 中文标题：WALi：嵌套词自动机
- 作者：Evan Driscoll，Aditya Thakur，Amanda Burton，Thomas W. Reps
- 发表：University of Wisconsin-Madison Computer Sciences Technical Report `TR1675`，2011
- DOI：原文未提供
- 链接：https://research.cs.wisc.edu/wpis/papers/tr1675r.pdf
- 形式主义：`Nested-Word Automata / WALi-NWA / WPDS interoperability`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：technical-report-level `C++` infrastructure manual for `NWA` construction, query, serialization and `WPDS` conversion
- 工具/实现获取方式：原文明确给出 `WALi` 下载主页，并说明 `NWA` 部分是 `WALi 4.0` 的组成部分，构建说明位于发行包 `README.txt`。
- 标准/格式获取方式：主承载是 `C++` `NWA`/`NestedWord` classes、serialization format、`wali::nwa::query / construct / nwa_pds` 命名空间与 `WPDS` 转换接口；它不是通用行业交换标准。

## 简报

这篇技术报告补的是 `Nested-Word Automata` 在 Wisconsin `WALi` 工具线中的“完整工程接口层”。如果说 [OpenNWA](../opennwa-a-nested-word-automaton-library/desc.md) 更像一个会议短文级的算法库介绍，那么本文则把 `NestedWord` 类、`NWA` 类、查询接口、构造接口、serialization 格式以及 `NWA <-> WPDS` 转换细节完整固定下来，是更适合拿来做底层基础设施参考的条目。

- 形式主义定位：`NWA` 的程序化 API、serialization 与 `WPDS` 互操作基础设施。
- 构造方式简述：用户通过 `NestedWord`、`NWA`、query / construct / `nwa_pds` 命名空间操作结构化词对象与自动机，再调用空性、language inclusion、determinize、complement 和 `WPDS` 转换。
- 基础设施与场景简述：依托 `WALi`、`C++` API、serialization parser、`WeightGen` 与 `WPDS` bridge，服务程序分析、nested trace reasoning 与结构化文档语言处理。

```text
nested word / call-return structure -> WALi NWA object -> query / construct / serialization / WPDS bridge -> emptiness / inclusion / analysis backend
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. nested words。
2. nested-word automata (`NWA`)。
3. `NestedWord` 与 `NWA` 类。
4. query / construct / `nwa_pds` 三类库接口。
5. serialization 格式与 `WPDS` 互操作。

### 核心抽象

nested word 可写成：

$$
nw = (a_1 \cdots a_n,\nu)
$$

上式中的符号逐项解释如下：

1. `a_1 \cdots a_n` 是线性输入词。
2. `\nu` 是不交叉 nesting relation。
3. 若 `\nu(i,j)` 成立，则位置 `i` 与 `j` 分别对应匹配的 call 与 return。

`NWA` 骨架可保守整理为：

$$
A = (Q,Q_0,F,\delta_c,\delta_i,\delta_r)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `Q_0` 是初始状态集合。
3. `F` 是接受状态集合。
4. `\delta_c` 是 call transitions。
5. `\delta_i` 是 internal transitions。
6. `\delta_r` 是 return transitions。

本文真正补出的工程抽象，可以进一步压成：

$$
\mathcal L = (A,\mathrm{query},\mathrm{construct},\mathrm{nwa\_pds},\mathrm{ser})
$$

上式中的符号逐项解释如下：

1. `A` 是底层 `NWA` 对象。
2. `\mathrm{query}` 表示结构查询、语言判定与 `pre^\ast/post^\ast` 接口。
3. `\mathrm{construct}` 表示 union、intersection、concatenation、Kleene star、reverse、determinize、complement 等构造接口。
4. `\mathrm{nwa\_pds}` 表示 `NWA` 与 `WPDS` 互转接口。
5. `\mathrm{ser}` 表示 serialization 与 parser。

### 一个最小例子与通俗解释

一个最小例子是“函数调用-返回”结构：

1. 构造一个 nested word，其中 `call f` 与 `return f` 通过 nesting relation 配对。
2. 用 `NWA` 声明一条 call transition 进入被调用上下文。
3. internal position 正常在线性路径上移动。
4. return 时读取 matching call 上保存的状态，再决定是否接受。

通俗地说，`WALi-NWA` 不是单纯帮你“画一个自动机”，而是提供了一整套能把结构化调用关系程序化处理的库。你既能像操作普通自动机一样做并、交、补，又能把它直接接到 `WPDS` 后端去做更复杂的程序分析。

### 运行 / 接受 / 转移语义

return transition 的关键语义可写成：

$$
(q_{lin},q_{call},a,q') \in \delta_r
$$

上式中的符号逐项解释如下：

1. `q_{lin}` 是 return 位置在线性前驱上的状态。
2. `q_{call}` 是 matching call 边上保留的 call-predecessor state。
3. `a` 是当前位置输入符号。
4. `q'` 是 return 后进入的新状态。

语言判定语义可写成：

$$
L(A) = \{\, nw \mid A \text{ accepts } nw \,\}
$$

上式中的符号逐项解释如下：

1. `L(A)` 是自动机 `A` 接受的 nested-word language。
2. 本文给出 membership、emptiness、language equality 与 subset checking 等接口。

当转成 `WPDS` 时，接口层可写成：

$$
\Phi_{\mathrm{nwa\_pds}} : A \leftrightarrow W
$$

上式中的符号逐项解释如下：

1. `A` 是 `NWA`。
2. `W` 是 `WALi` 中的 weighted pushdown system。
3. `\Phi_{\mathrm{nwa\_pds}}` 表示双向转换与相关权值生成接口。

### 语义边界

1. 本文默认读者已接受 `NWA` 作为结构化词对象的核心模型。
2. 报告聚焦的是库接口与工程承载，不重新证明全部 `NWA` 理论。
3. 实现采用 weakly-hierarchical, linearly-accepting 口径，并允许 internal epsilon transitions 和 wild transitions。
4. 因而它更像工程参考手册，而不是形式语言教科书。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| nested word | `$nw=(a_1\cdots a_n,\nu)$` | 线性顺序与 nesting relation 同时存在。 |
| `NWA` 骨架 | `$A=(Q,Q_0,F,\delta_c,\delta_i,\delta_r)$` | 库的核心工作对象。 |
| return transition | `$(q_{lin},q_{call},a,q')\in\delta_r$` | return 同时读取线性状态与 call-predecessor state。 |
| language semantics | `$L(A)=\{nw \mid A \text{ accepts } nw\}$` | emptiness / membership / inclusion 的基础。 |
| `WPDS` 互转 | `$\Phi_{\mathrm{nwa\_pds}}:A\leftrightarrow W$` | `NWA` 可以直接接入 `WALi` 的 pushdown 分析后端。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 原生支持 `NWA` states 与三类 transitions。 |
| 事件 / 触发 | 很强 | call / internal / return 是模型主线。 |
| 守卫 / 数据 | 弱支持 | 主体不是富数据自动机，但支持 client information 与 weight generation 接口。 |
| 层次 | 很强 | nesting relation 是核心结构。 |
| 并发 / 同步 | 不适用 | 主要面向顺序结构化词对象。 |
| 时间约束 | 不支持 | 不属于 timed family。 |
| 连续动态 / 随机性 | 不支持 | 纯离散语言基础设施。 |
| 可执行 / 可验证性 | 很强 | query、construct、serialization 与 `WPDS` bridge 已完整工具化。 |

### 形式化问题与性质

1. 本文最重要的新增价值，是把 `NWA` 工程接口从“一个可用库”提升为“一个可复用接口族”。
2. serialization 格式让 `NWA` 不再只存在于 API 调用里，也可落成稳定工件。
3. `WeightGen` 与 `nwa_pds` 桥接说明它天然面向更大 `WALi` 生态，而不是孤立算法库。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 手工或程序化构造 `NestedWord`。
2. 通过 `NWA` 类声明状态、初态、终态和三类 transitions。
3. 用 `construct` 命名空间生成复合自动机。
4. 用 parser / serialization 在文本格式与库对象之间转换。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `NestedWord` 类。
2. `NWA` 类与相关 typedef。
3. serialization format。
4. `query / construct / nwa_pds` 命名空间接口。

### 交换与互操作

互操作重点在于：

1. `NWA` 可序列化与反序列化。
2. `NWA` 可转换到 `WPDS`，也可从 `WPDS` 构造回来。
3. `WALi` 通用 key-handling、smart pointer 与权值接口被底层复用。

## 配套基础设施

- 建模/编辑工具：主体是 `C++` API，而不是图形编辑器。
- 解析/交换/元模型支持：serialization format、parser、`NWA` class、`NestedWord` class。
- 仿真/执行支持：支持 membership、example generation 与 `pre^\ast/post^\ast` 一类分析入口。
- 验证/分析支持：emptiness、equality、subset、determinize、complement、`WPDS` queries。
- 代码生成/转换支持：重点是 `NWA <-> WPDS` 转换，而不是部署代码生成。
- 标准化或社区生态：依托 `WALi`、Wisconsin `WPDS` 工具链与 `NWA` 程序分析生态。

## 适用场景与需求前提

### 适用场景

适合程序调用返回分析、nested document 处理、结构化 trace 判定以及需要把 `NWA` 接入 `WPDS` 后端的分析任务。

### 需求前提

1. 输入对象必须存在显式的不交叉 nesting 结构。
2. 团队需要算法库级接口，而不是仅会画图的前端工具。
3. 若要使用 `WPDS` 互转，需要接受 `WALi` 权值与状态表示方式。
4. 上层应用应愿意用 `C++` API 或 serialization 工件组织分析流程。

### 不适用或高成本场景

如果对象只是普通平面字符串，或者团队只需要一个轻量理论定义而不需要工程 API，那么 `WALi-NWA` 的基础设施体量会偏重。

## 与相邻形式主义的关系

相对 [opennwa-a-nested-word-automaton-library/desc.md](../opennwa-a-nested-word-automaton-library/desc.md)，两者都属于同一条 `NWA` 工程线，但本文更像完整接口手册和 serialization/`WPDS` 参考文档；相对 [weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md](../weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md)，本文通过 `nwa_pds` 命名空间把结构化词对象直接接到 pushdown-family 后端；相对 [pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md](../pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md)，两者都偏分析底盘，但一个面向 nested-word automata，一个面向 weighted pushdown reachability。

## 与本研究的关系

### 对 Project 1 的价值

它说明“状态机类型谱系”中的很多条目并不只是理论对象，还可以被固化成一套对程序友好的 API、格式与转换接口。

### 作为目标形式主义还是中间表示

更适合作为中间表示和分析后端，而不是需求侧直接生成给领域工程师使用的前端工件。

### 对需求到模型生成的启发

1. 若需求天然带有调用返回、嵌套结构或结构化 trace，就不应粗暴扁平化成普通 `FSM`。
2. 单篇工具论文若能稳定给出 serialization 和 API 边界，对自动生成工作流非常有价值。
3. 互操作层很关键，`NWA` 是否能接到 `WPDS` 后端，直接决定它能否进入更大的验证闭环。

### 现实限制

本文的语言和接口都偏底层分析开发者，并不直接解决“如何从自然语言需求构造 `NWA`”的问题，前端建模仍需额外桥接。

## 重要的相关工作

### 奠基或前身工作

1. [adding-nesting-structure-to-words/desc.md](../adding-nesting-structure-to-words/desc.md)：`Nested Word` / `NWA` 本体母线。
2. [visibly-pushdown-languages/desc.md](../visibly-pushdown-languages/desc.md)：结构化词语言的近邻家族。

### 同类型或同家族工作

1. [opennwa-a-nested-word-automaton-library/desc.md](../opennwa-a-nested-word-automaton-library/desc.md)：会议短文级 `NWA` 库介绍。
2. `WALi` 通用 weighted automata / `WPDS` 生态。

### 标准 / 格式 / 工具链工作

1. serialization parser。
2. `WeightGen` 抽象类。
3. `query / construct / nwa_pds` 三个命名空间。

### 与本研究关系最紧的工作

1. [weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md](../weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md)：`WPDS` 母线。
2. [pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md](../pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md)：另一条 pushdown-family 工程库路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌳 树 / 文档对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Nested-Word Automata / WALi-NWA / WPDS interoperability`
- 论文角色：technical-report-level `C++` infrastructure manual for `NWA` construction, query, serialization and `WPDS` conversion
- 核心功能：把 `NWA` 的 API、serialization 与 `WPDS` 互转稳定成完整可复用的 `WALi` 基础设施。
- 关键特性：`NestedWord`/`NWA` classes、query/construct namespaces、serialization、`WeightGen`、`NWA <-> WPDS` bridge。
- 构造方式：nested word -> `NWA` object -> query/construct/serialization/`WPDS` conversion。
- 基础设施：`WALi 4.0`、`C++` API、parser、serialization format、`WPDS` tool line。
- 适用场景：程序调用返回分析、结构化 trace、nested document 与 pushdown 后端互操作。
- 需求前提：对象必须具有显式 nesting relation，且团队需要库级 API 与可序列化工件。
- 状态：🟢

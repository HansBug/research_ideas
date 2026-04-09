# WALi 用户手册 / WALi User Manual

## 基本信息

- 标题：WALi User Manual
- 中文标题：WALi 用户手册
- 作者：Nicholas Kidd
- 发表：技术手册，2008-02-18
- DOI：原文未提供
- 链接：https://research.cs.wisc.edu/wpis/wpds/wali/manual.pdf
- 形式主义：`Weighted Pushdown Systems / WALi`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：💻 软件建模与程序行为
- 论文角色：`WPDS` 库接口手册 / semiring extension framework / interprocedural-analysis programming manual
- 工具/实现获取方式：手册直接给出源码下载链接 `http://www.cs.wisc.edu/wpis/wpds/wali/WALi-latest.tar.gz`，并说明 `scons` 构建、examples 与 addons 的获取方式。
- 标准/格式获取方式：核心承载是 `C++` API、`wali::SemElem`、`WPDS` / `WFA` 对象、`Key` 机制与 XML query addon；不是独立行业交换标准。

## 简报

这份手册补出的不是新的 `WPDS` 理论，而是 Wisconsin 这条 `weighted pushdown` 工具线的可编程接口层。`WALi` 的重点在于把 semiring、规则、查询自动机、`ICFG -> PDS` 编码和 XML / `C++` 工作流固定成开发者可直接复用的库，从而把过程间数据流分析和其他栈敏感问题真正做成可编排的工程底盘。

- 形式主义定位：`Weighted Pushdown Systems` 的库级实现与扩展接口手册。
- 构造方式简述：用户先定义 semiring weight domain，再构造 `WPDS` 规则、`WFA` 查询和 `Key` 标识，最后调用库完成查询。
- 基础设施与场景简述：依托 `C++`、`SemElem` 接口、examples、XML addon 与 `WFA` 查询，服务 interprocedural dataflow analysis、call-return reachability 与程序分析原型。

```text
ICFG / stack-sensitive model -> WPDS rules + semiring domain -> WFA query -> WALi library -> weighted reachability result
```

## 形式主义定义与核心对象

### 定义对象

手册围绕以下对象组织：

1. `Weighted Pushdown System (WPDS)` 库实现。
2. `SemElem` 抽象类与 semiring 扩展点。
3. `ICFG -> PDS/WPDS` 编码方式。
4. `WFA` 查询接口。
5. XML query addon 与 `Key/KeySource` 机制。

### 核心抽象

结合手册与 `WPDS` 背景，可把库面向的加权下推系统骨架保守写成：

$$
\mathcal W = (P,\Gamma,\Delta,S)
$$

上式中的符号逐项解释如下：

1. `P` 是控制位置集合。
2. `\Gamma` 是栈字母表。
3. `\Delta` 是下推规则集合。
4. `S` 是权值 semiring。
5. 该元组是依据手册“`WALi` is an implementation of a `WPDS`”与其 API 结构做的保守整理。

手册对 weight domain 的接口最清楚，可直接压成 semiring 骨架：

$$
S = (D,\oplus,\otimes,\bar 0,\bar 1)
$$

上式中的符号逐项解释如下：

1. `D` 是权值集合。
2. `\oplus` 对应手册中的 `combine`。
3. `\otimes` 对应手册中的 `extend`。
4. `\bar 0` 对应 `zero()`。
5. `\bar 1` 对应 `one()`。

### 一个最小例子与通俗解释

手册给了一个非常合适的最小例子：过程 `f` 调用过程 `g`。

1. `f` 的控制流节点 `n4` 调用 `g`，返回点是 `n5`。
2. `WALi` 用一条规则把调用编码成把 `g` 的入口压栈，并记录返回点。
3. `g` 结束时再弹栈返回。
4. 若权值域采用手册中的 `Reach` 示例，那么 `combine` 就相当于布尔“或”，`extend` 相当于布尔“与”。

通俗地说，`WALi` 像“给程序调用栈分析准备好的积木库”。你先决定权值语义，再把调用图编码成规则，最后用库做可达性或数据流查询。

### 运行 / 接受 / 转移语义

手册给出的 semiring 偏序判定条件是：

$$
\alpha \sqsubseteq \beta \Longleftrightarrow \alpha = (\alpha \oplus \beta)
$$

上式中的符号逐项解释如下：

1. `\alpha` 与 `\beta` 是两个 semiring 元素。
2. `\oplus` 是 `combine` 运算。
3. 该式是手册直接给出的“用 `combine` 表示偏序”的判据。

手册在 `ICFG` 编码部分给出调用边规则，可写成：

$$
\langle p,n_c \rangle \hookrightarrow \langle p,e_f n_r \rangle
$$

上式中的符号逐项解释如下：

1. `p` 是唯一的控制状态。
2. `n_c` 是调用点。
3. `e_f` 是被调过程 `f` 的入口节点。
4. `n_r` 是调用返回点。
5. 该规则表示“遇到调用时，进入被调过程并把返回点压入栈顶”。

### 语义边界

1. 手册聚焦的是库编程接口，不是重新讲解全部 `WPDS` 理论细节。
2. 语义能力强依赖用户自己定义的 semiring；库不替用户决定抽象域。
3. `WALi` 更适合顺序、调用返回、栈敏感问题，不是并发或连续动力学前端。
4. XML addon 是便利接口，不等于通用事实标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `WPDS` 骨架 | `$\mathcal W = (P,\Gamma,\Delta,S)$` | `WALi` 的核心对象是带权下推系统。 |
| semiring 骨架 | `$S = (D,\oplus,\otimes,\bar 0,\bar 1)$` | `SemElem` 接口正对应 semiring 的五元骨架。 |
| 偏序判据 | `$\alpha \sqsubseteq \beta \Longleftrightarrow \alpha = (\alpha \oplus \beta)$` | 手册直接说明如何借 `combine` 判断元素偏序。 |
| 调用规则 | `$\langle p,n_c \rangle \hookrightarrow \langle p,e_f n_r \rangle$` | `ICFG` 中的调用边被编码为典型 pushdown 调用规则。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 pushdown control locations 与 stack symbols。 |
| 事件 / 触发 | 弱支持 | 主体是规则重写，不是事件驱动状态机。 |
| 守卫 / 数据 | 中等支持 | 通过用户自定义 semiring 表达数据流和抽象语义。 |
| 层次 | 很强 | 调用返回和栈层级是核心。 |
| 并发 / 同步 | 不适用 | 不是并发同步建模前端。 |
| 时间约束 | 不支持 | 手册不涉及 timed semantics。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 pushdown / semiring 路线。 |
| 可执行 / 可验证性 | 很强 | 提供库、示例、addon、XML query 和 `WFA` 查询接口。 |

### 形式化问题与性质

1. `WALi` 的核心价值，是把 `WPDS` 从论文公式变成可扩展软件库。
2. semiring 扩展点使它不仅能做 reachability，还能承载多种数据流 / 代价语义。
3. 手册特别适合作为文库里“`WPDS` 工程基础设施”的总库说明条目。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `C++` 直接构造 `WPDS` 对象。
2. 自定义 `SemElem` 子类实现抽象域。
3. `Key` / `KeySource` 定义程序点与栈符号。
4. XML query addon。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `WPDS` 规则对象。
2. `WFA` 查询自动机。
3. `SemElem` 接口及其 reference-counted 实例。
4. XML 序列化与解析。

### 交换与互操作

这条工具线的互操作重点在于：

1. `ICFG` 到 `PDS/WPDS` 的规范编码方式。
2. `WFA` 作为查询接口。
3. XML addon 让 `WPDS` 查询可以外部化。
4. 与后续 `WALi-NWA`、`WPDS++` 等 Wisconsin 生态工具天然相连。

## 配套基础设施

- 建模/编辑工具：以 `C++` API 为主，不是图形化建模器。
- 解析/交换/元模型支持：XML query addon，依赖 `xerces-c`。
- 仿真/执行支持：主体是分析库，不是运行时仿真器。
- 验证/分析支持：`WPDS + WFA` 查询、reachability、数据流分析工作流。
- 代码生成/转换支持：重点是 `ICFG -> WPDS` 编码与 XML marshalling，不主打部署代码生成。
- 标准化或社区生态：依托 Wisconsin `WPDS` 工具线、examples、addons 与程序分析研究生态。

## 适用场景与需求前提

### 适用场景

适合过程间数据流分析、调用栈敏感程序验证、规则代价传播，以及其他能自然落成 `WPDS` 的顺序程序 / 结构化控制流问题。

### 需求前提

1. 系统核心必须具有明确的 pushdown / call-return 纪律。
2. 查询目标最好能写成 `WFA` 或 regular configuration 形式。
3. 团队愿意自己定义 semiring 抽象域，而不是只使用固定分析语义。

### 不适用或高成本场景

如果问题主要是并发同步、dense time、概率博弈或连续动力学，`WALi` 不是直接入口；它更适合栈敏感顺序分析。

## 与相邻形式主义的关系

相对 [weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md](../weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md)，那篇是 `WPDS` 方法母线，本文是库手册；相对 [model-checking-x86-executables-with-codesurfer-x86-and-wpds-plus-plus/desc.md](../model-checking-x86-executables-with-codesurfer-x86-and-wpds-plus-plus/desc.md)，后者把真实二进制接到 `WPDS++` 查询链，本文更底层；相对 [pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md](../pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md)，两者都属 pushdown 基础设施，但 `PDAAAL` 更偏现代 reachability 库，本文更像 Wisconsin 经典 `WPDS` 总库接口手册。

## 与本研究的关系

### 对 Project 1 的价值

1. 它补上了文库里 `weighted pushdown` 一侧非常缺的“总库说明”锚点。
2. 这对 `project_1` 很重要，因为一旦状态机建模需要保留调用栈、上下文和过程间语义，就可能要接到 `WPDS` 后端。
3. 也说明“基础设施”不只是论文里的算法名，还包括 API、序列化、构建系统和扩展接口。

### 作为目标形式主义还是中间表示

更适合作为分析后端和中间语义承载，而不是面向领域工程师的直接建模语言。

### 对需求到模型生成的启发

1. 若需求里已有显式调用、返回和过程间上下文，扁平 `FSM` 往往不够，需要更强的栈式表示。
2. 查询接口若能直接生成成 `WFA` 或正则配置约束，会更方便接入这类后端。
3. 对可扩展验证工具链来说，“先定义统一 semiring 接口”是非常有启发的架构设计。

### 现实限制

`WALi` 偏底层库与程序分析开发者视角，不直接解决高层需求建模与自然语言到模型的前端问题。

## 重要的相关工作

1. [weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md](../weighted-pushdown-systems-and-their-application-to-interprocedural-dataflow-analysis/desc.md)：`WPDS` 数据流分析母线。
2. [model-checking-x86-executables-with-codesurfer-x86-and-wpds-plus-plus/desc.md](../model-checking-x86-executables-with-codesurfer-x86-and-wpds-plus-plus/desc.md)：可执行级 `WPDS` 工具链。
3. [pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md](../pdaaal-a-library-for-reachability-analysis-of-weighted-pushdown-systems/desc.md)：另一条现代 `weighted pushdown` 基础设施路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Weighted Pushdown Systems / WALi`
- 归类理由：这份手册的主贡献是 `WPDS` 库、semiring 扩展接口、`WFA` 查询与 XML addon 的工程基础设施说明，而不是新的状态机本体。

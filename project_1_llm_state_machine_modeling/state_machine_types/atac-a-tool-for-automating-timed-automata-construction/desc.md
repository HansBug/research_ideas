# ATAC：定时自动机构造自动化工具 / ATAC: A Tool for Automating Timed Automata Construction

## 基本信息

- 标题：ATAC: A Tool for Automating Timed Automata Construction
- 中文标题：ATAC：定时自动机构造自动化工具
- 作者：Beyazit Yalcinkaya，Ebru Aydin Gol
- 发表：*CoRR / arXiv preprint*，`1905.08169v2`，2020
- DOI：`10.48550/arXiv.1905.08169`
- 链接：https://arxiv.org/abs/1905.08169
- 形式主义：`Timed Automata / structured natural language / ATAC`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：structured-natural-language timed-automata construction and query-generation route
- 工具/实现获取方式：原文明确说明作者实现了一个 Python 程序 `ATAC`，输入系统描述和规格句子后输出 `UPPAAL` 可导入的 XML 与 query 文件；正文未给独立公开仓库链接。
- 标准/格式获取方式：输入是作者定义的 structured natural language，输出是 `UPPAAL` XML 模型与 query 文件；它不是中立交换标准。

## 简报

这篇论文补的是一个很直接的“需求句子 -> `Timed Automata` 骨架 -> `UPPAAL` 查询”方法路线。它并不试图完全自动化整个实时系统建模，而是把最容易出错、又最机械的几步先自动做掉：位置和转移生成、同步信号放置、clock allocation，以及把受限自然语言规格映射成 `UPPAAL` 查询。

- 形式主义定位：围绕 `Timed Automata` 的自动构造与验证前端，而不是新的 timed family。
- 构造方式简述：用户用受限英文句式写描述和规格；`ATAC` 解析句法后生成 locations、transitions、clocks、invariants 和 `UPPAAL` query。
- 基础设施与场景简述：依托 structured natural language grammar、automatic clock placement、clock reduction 和 `UPPAAL` XML/query export，服务实时系统早期建模和需求到时钟模型的骨架生成。

```text
structured sentences -> grammar parsing -> timed automaton skeleton -> clock reduction -> UPPAAL XML / queries
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Timed Automata` 模型；
2. description grammar；
3. specification grammar；
4. automatic clock allocation；
5. `UPPAAL` XML 与 query 输出。

### 核心抽象

原文采用标准 `TA` 骨架。可直接整理为：

$$
A = (L, l_0, \Sigma, C, I, T)
$$

上式中的符号逐项解释如下：

1. `L` 是 location 集合。
2. `l_0` 是初始 location。
3. `\Sigma` 是标签或同步动作集合。
4. `C` 是时钟集合。
5. `I` 把每个 location 映到时钟不变式。
6. `T` 是转移集合。

论文对一条转移给出如下骨架：

$$
t = (l_s, \alpha, \lambda, \varphi, l_t)
$$

上式中的符号逐项解释如下：

1. `l_s` 是源 location。
2. `\alpha` 是动作或同步标签。
3. `\lambda \subseteq C` 是该转移要 reset 的 clocks。
4. `\varphi` 是使能该转移的时钟约束。
5. `l_t` 是目标 location。

### 一个最小例子与通俗解释

论文中的 `Train-Gate` 例子最直观：

1. 句子 `Train can be Safe Appr Cross Stop Start and it is initially Safe.` 定义状态集合与初始位置。
2. 句子 `If the time spent after entering Appr is more than or equal to 10, then Train can go from Appr to Cross.` 触发 clock 创建、reset 位置推断和 guard 生成。
3. 句子 `If Stop is received ...` 则同时生成同步条件和时间条件。
4. 最终输出的不是文字说明，而是可直接导入 `UPPAAL` 的模型骨架。

通俗地说，`ATAC` 像一个“定时自动机草图编译器”。它不替你做全部设计，但会把句子里已经说清楚的 timing / synchronization 结构尽快落到机器可验证的 `TA` 上。

### 运行 / 接受 / 转移语义

对描述句子的总体映射，可保守写成：

$$
\mathcal D \mapsto A
$$

上式中的符号逐项解释如下：

1. `\mathcal D` 是满足 description grammar 的句子集合。
2. `A` 是根据这些句子生成的 `Timed Automata`。
3. 论文强调句子顺序不影响最终 `TA`，即同一集合的不同排列应映到同一模型。

对规格句子的映射，则可写成：

$$
\mathcal S \mapsto q
$$

上式中的符号逐项解释如下：

1. `\mathcal S` 是满足 specification grammar 的句子。
2. `q` 是 `UPPAAL` 查询语言中的公式。
3. 若句子隐含时间条件，`ATAC` 会额外放置所需 clocks，而不是让用户手动声明。

原文还强调初始时每个时间条件都会分配一个新 clock，随后再做 reduction。可保守写成：

$$
C_{\mathrm{raw}} \to C_{\mathrm{red}}
$$

上式中的符号逐项解释如下：

1. `C_{\mathrm{raw}}` 是按句子直接生成的原始 clock 集合。
2. `C_{\mathrm{red}}` 是 clock reduction 后的集合。
3. 这一步用于压低模型复杂度，避免“每个句子一只表”带来的 clock 数爆炸。

### 语义边界

1. 该方法依赖作者定义的受限句法，不适合开放式自然语言需求。
2. 它更像自动生成 timed skeleton，而不是完整工业模型的终态建模方法。
3. 复杂的 `UPPAAL` 特性，如数组 channel、复杂 `C` 代码片段，通常仍需人工补写。
4. 论文聚焦 discrete real-time control，不涉及连续动力学。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TA` 母型 | `$A = (L, l_0, \Sigma, C, I, T)$` | `ATAC` 生成的目标模型骨架。 |
| 转移骨架 | `$t = (l_s, \alpha, \lambda, \varphi, l_t)$` | 一条句子可能同时生成动作、guard 与 reset。 |
| 描述映射 | `$\mathcal D \mapsto A$` | description grammar 到 `TA` 的自动构造。 |
| 规格映射 | `$\mathcal S \mapsto q$` | specification grammar 到 `UPPAAL` query 的自动转换。 |
| 时钟压缩 | `$C_{\mathrm{raw}} \to C_{\mathrm{red}}$` | 自动放置的 clocks 之后还会做 reduction。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接生成 `TA` locations 与 transitions。 |
| 事件 / 触发 | 很强 | `send / receive / go from ... to ...` 句式直接决定动作与同步。 |
| 守卫 / 数据 | 中等支持 | 主要是时钟 guard；富数据不是主线。 |
| 层次 | 不支持 | 目标不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 支持同步信号与多 automata 组合，但语义仍落在 `TA` 网络。 |
| 时间约束 | 很强 | automatic clock allocation 和 invariant / guard generation 是核心。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散 timed model。 |
| 可执行 / 可验证性 | 很强 | 输出直接进入 `UPPAAL` 做建模与检查。 |

### 形式化问题与性质

1. 论文真正解决的是“如何把句子里已经明确的实时语义稳定翻到 `TA`”。
2. automatic clock placement 说明需求文本到 `TA` 的难点不只是状态图生成，还包括细粒度时钟布置。
3. query generation 让该方法不只产模型，也同时产验证入口。

## 构造方式与承载格式

### 建模入口

原文中的建模入口有：

1. 描述句子，如状态集合、初始状态、时序迁移、同步迁移；
2. 规格句子，如 safety、leads-to 和 time-bounded properties；
3. grammar 中的 entering / leaving location 语义，用于推断 reset 放置点。

### 机器可处理承载方式

机器可处理承载方式包括：

1. description grammar；
2. specification grammar；
3. `Timed Automata` internal model；
4. `UPPAAL` XML；
5. `UPPAAL` query file。

### 交换与互操作

这篇论文的互操作重点在：

1. 把自然语言前端与 `UPPAAL` 后端接通；
2. 自动把 timing requirements 变成 clocks 与 queries；
3. 最终输出仍是标准 `UPPAAL` 可读格式，而不是私有验证器。

## 配套基础设施

- 建模/编辑工具：structured natural language 输入界面与 Python `ATAC` 原型。
- 解析/交换/元模型支持：description/specification grammar 与 `UPPAAL` XML/query export。
- 仿真/执行支持：依托 `UPPAAL` 对生成模型做后续分析。
- 验证/分析支持：`UPPAAL` query generation、automatic clock placement 和 clock reduction。
- 代码生成/转换支持：重点是从需求句子到 `TA/query` 的转换，而不是部署代码生成。
- 标准化或社区生态：输出兼容 `UPPAAL`，但输入 grammar 是作者自定义前端。

## 适用场景与需求前提

### 适用场景

适合实时系统前期建模、课程/研究原型验证，以及希望尽快把结构化需求片段落成 `UPPAAL` 可检模型的场景。

### 需求前提

1. 需求能写成受限、规范的英文句式。
2. 时序信息主要体现在进入/离开状态后的时间条件。
3. 系统复杂度主要在 timed behavior，而不是复杂数据和连续动力学。
4. 团队接受先生成 skeleton、再人工补足细节的工作流。

### 不适用或高成本场景

如果需求本身高度开放、含大量领域数据结构或复杂 `UPPAAL` 扩展语法，`ATAC` 的句法前端会很快遇到上限。

## 与相邻形式主义的关系

相对 [uppaal-40/desc.md](../uppaal-40/desc.md)，本文不是 timed backend，而是 `UPPAAL` 前端自动建模入口；相对 [moby-rt-a-tool-for-specification-and-verification-of-real-time-systems/desc.md](../moby-rt-a-tool-for-specification-and-verification-of-real-time-systems/desc.md)，`Moby/RT` 更像完整实时规格工具链，而本文只聚焦从句子到 `TA` skeleton 的自动构造；相对 [transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)，后者假定已有 plan 与 `TA` 建模基础，本文则更前置。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“受限自然语言 -> 形式模型骨架”是可工程化的，而不必一步到位做自由文本全自动建模。
2. 时钟放置与 query 生成这两个细节，对 `project_1` 后续 timed extension 很有启发。
3. 如果未来需要把 LLM 生成的规范化需求句子转成 `TA`，这篇论文给了一个很直接的模板。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`ATAC` 更像需求到 `Timed Automata` 的前端构造路线，而不是新的目标形式主义。

### 对需求到模型生成的启发

1. 先把自然语言收窄成受控 grammar，比直接追求自由文本到完整模型更稳。
2. 时序模型自动化的关键不是“画出状态”，而是“把 clocks 放对地方”。
3. 生成模型的同时生成验证查询，会让闭环更容易真正跑起来。

## 重要的相关工作

- [uppaal-40/desc.md](../uppaal-40/desc.md)：`ATAC` 的主要目标后端平台。
- [moby-rt-a-tool-for-specification-and-verification-of-real-time-systems/desc.md](../moby-rt-a-tool-for-specification-and-verification-of-real-time-systems/desc.md)：更完整的实时规格与验证环境。
- [transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md](../transforming-robotic-plans-with-timed-automata-to-solve-temporal-platform-constraints/desc.md)：把既有计划约束落到 `TA` 的应用型路线。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇典型的 `Timed Automata` 前端构造路线条目，适合作为“受限自然语言 -> `TA` 骨架 -> `UPPAAL` 查询”这一建模自动化链路的直接证据入账。

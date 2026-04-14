# 使用 ITS-tools 的符号模型检查 / Symbolic Model-Checking Using ITS-Tools

## 基本信息

- 标题：Symbolic Model-Checking Using ITS-Tools
- 中文标题：使用 ITS-tools 的符号模型检查
- 作者：Yann Thierry-Mieg
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 231-237，2015
- DOI：`10.1007/978-3-662-46681-0_20`
- 链接：https://doi.org/10.1007/978-3-662-46681-0_20
- 形式主义：`ITS-tools / Guarded Action Language / symbolic model checking`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：symbolic model-checking workbench with `GAL` pivot language and multi-formalism front-ends
- 工具/实现获取方式：原文明确说明二进制、源码和用户文档可从 `http://ddd.lip6.fr` 获取。
- 标准/格式获取方式：核心承载是 `GAL` pivot language 与 `EMF` 元模型，并支持 `ETF`、`PNML`、`Promela`、`DVE`、`UPPAAL XTA` 等输入；原文未把它定义成中立行业标准。

## 简报

这篇论文的重点不是提出新的状态机母型，而是把“多种已有形式主义如何接到同一 symbolic backend”这件事做成基础设施。`ITS-tools` 的核心设计是：前端把各种模型先翻到 `GAL`，后端统一以 decision diagrams 和 `Instantiable Transition System` API 做 reachability、`CTL`、`LTL` 检查。它更像一个 symbolic verification 中间层和工作台，而不是单一语言的专用求解器。

- 形式主义定位：以 `GAL` 为 pivot 的 symbolic model-checking 工具链。
- 构造方式简述：输入模型先经 model transformation 归一到 `GAL`，再由 `libDDD/libITS` 做 symbolic state-space exploration 与 temporal-logic checking。
- 基础设施与场景简述：依托 `GAL`、`EMF`、`ITS` API、`SDD/DDD`、`Spot` 与 Eclipse 前端，服务跨语言 symbolic verification。

```text
Promela / DVE / XTA / PNML / ETF -> GAL pivot language -> ITS symbolic kernel -> reachability / CTL / LTL
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `ITS-tools` symbolic kernel。
2. `Guarded Action Language (GAL)` pivot language。
3. `Instantiable Transition System (ITS)` API。
4. `its-reach`、`its-ctl`、`its-ltl` 三类分析工具。
5. 多前端到 `GAL` 的模型转换。

### 核心抽象

论文明确说 `GAL` 的语义是一个 finite Kripke structure。可保守写成：

$$
K = (S, S_0, \to, AP, L)
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `S_0` 是初始状态集合。
3. `\to` 是转移关系。
4. `AP` 是原子命题集合。
5. `L` 是状态标记函数。

论文还把 `GAL` 的核心对象描述为“变量、数组、guarded transitions”，可保守压成：

$$
G = (V, A, T, Init)
$$

上式中的符号逐项解释如下：

1. `V` 是整数变量与定长数组集合。
2. `A` 是有限动作标签集合。
3. `T` 是带 guard 和原子更新体的 transitions。
4. `Init` 是初始赋值。
5. 这是根据正文结构做的保守整理，不是论文显式给出的统一元组。

对后端 API，论文直接说明 `ITS` 本质上是带 successor / predecessor / predicate 的 labelled transition system。可写成：

$$
\mathcal I = (S, Succ, Pred, P)
$$

上式中的符号逐项解释如下：

1. `S` 是 symbolic states 所表示的状态集合。
2. `Succ` 是后继状态函数。
3. `Pred` 是前驱状态函数。
4. `P` 是布尔谓词接口，用于状态逻辑推理。

### 一个最小例子与通俗解释

最小直觉例子就是论文里的 `GAL` guarded transition：

1. `GAL` 模型先定义若干整数变量和数组。
2. 某个 transition 带一个布尔 guard。
3. 当 guard 为真时，该 transition 的整个赋值序列以单个 atomic step 执行。
4. 若多个 transition 共享同一 label，还可以用 `call(l)` 风格描述基于 label 的同步或非确定选择。

通俗地说，`ITS-tools` 的做法像是先把各门各派语言翻成一种“足够简单但又足够表达并发”的中间语，然后再把 symbolic model checking 全压到同一个后端。这样真正难维护的就只剩一个 backend，而不是每种前端语言都单独写一套求解器。

### 运行 / 接受 / 转移语义

论文明确指出 `GAL` transition 的 firing 语义是：在某个赋值状态里，只有 guard 为真的 transition 才能触发，并且 transition body 作为一个原子步执行。可保守写成：

$$
s \xrightarrow{a} s' \iff guard_a(s) = \mathrm{true} \land s' = update_a(s)
$$

上式中的符号逐项解释如下：

1. `s` 和 `s'` 是 `GAL` 状态。
2. `a` 是某条带标签的 transition。
3. `guard_a(s)` 表示在状态 `s` 中 guard 是否成立。
4. `update_a(s)` 是执行 transition body 后得到的新状态。
5. 原文特别强调整个 body 是 single atomic step。

`ITS-tools` 的 `LTL` 路线则依赖 automata-theoretic checking，可保守写成：

$$
K \models \varphi \iff L(K) \cap L(A_{\lnot \varphi}) = \emptyset
$$

上式中的符号逐项解释如下：

1. `K` 是从 `GAL` 生成的 finite Kripke structure。
2. `\varphi` 是 `LTL/PSL` 性质。
3. `A_{\lnot \varphi}` 是由 `Spot` 生成的否定性质自动机。
4. 空交意味着模型满足性质。
5. 这对应正文中 `its-ltl` 借助 `Spot` 做 Büchi translation 与 emptiness check 的路线。

### 语义边界

1. `GAL` 是 pivot language，不是让最终用户手写的唯一母语。
2. `ITS-tools` 强调 finite-state symbolic verification，不是 hybrid / continuous semantics。
3. timed support 在文中主要通过离散时间或 essential states 变换来处理。
4. 能否支持某种外部语言，取决于是否存在到 `GAL` 的稳定转换。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| Kripke 语义骨架 | `$K = (S, S_0, \to, AP, L)$` | `GAL` 最终生成有限 Kripke 结构。 |
| `GAL` 保守骨架 | `$G = (V, A, T, Init)$` | 说明 pivot language 的核心对象是变量、动作与 guarded transitions。 |
| `ITS` API | `$\mathcal I = (S, Succ, Pred, P)$` | 统一 symbolic backend 所暴露的操作接口。 |
| 原子步语义 | `$s \xrightarrow{a} s' \iff guard_a(s) \land s' = update_a(s)$` | 解释 `GAL` 中 guard 与 body 的执行方式。 |
| `LTL` 检查 | `$K \models \varphi \iff L(K) \cap L(A_{\lnot\varphi}) = \emptyset$` | 对应 `its-ltl + Spot` 的 automata-theoretic workflow。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `GAL` 直接用变量与数组承载状态。 |
| 事件 / 触发 | 很强 | guarded transitions 与 label-based synchronisation 是核心。 |
| 守卫 / 数据 | 很强 | `GAL` 支持整数、数组与 `C` 风格表达式。 |
| 层次 | 中等支持 | kernel 本身无显式 hierarchy，但 `ITS` 层可表达组合层次。 |
| 并发 / 同步 | 很强 | 设计目标就是 symbolic checking of concurrent specifications。 |
| 时间约束 | 条件支持 | 通过 timed automata / time Petri nets 前端与离散时间假设接入。 |
| 连续动态 / 随机性 | 不支持 | 本文主线是有限并发系统的 symbolic verification。 |
| 可执行 / 可验证性 | 很强 | reachability、`CTL`、`LTL`、GUI、Eclipse 集成都已具备。 |

### 形式化问题与性质

1. 这篇论文说明“语言无关 backend”可以通过 pivot language 而不是超大一统 DSL 实现。
2. `GAL` 的价值在于足够简单，适合承载第三方语言的 operational semantics。
3. 对整个文库来说，它是 `LTSmin/PINS`、`JANI` 一类“统一中间层 / 统一后端”路线的重要对照片。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `GAL` 文本模型；
2. `Promela`；
3. `DVE`；
4. `UPPAAL XTA`；
5. `PNML` / `ETF`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `.gal`；
2. `EMF` compliant `GAL` metamodel；
3. `ETF`；
4. `PNML`；
5. `CTL/LTL/PSL` property files。

### 交换与互操作

互操作重点包括：

1. 多前端语言先转成 `GAL`。
2. `ETF` 让 `LTSmin` 生态模型也能复用 `ITS` backend。
3. `Spot` 为 `LTL/PSL` 提供 automata translation。
4. Eclipse 前端减少第三方 DSL 接入成本。

## 配套基础设施

- 建模/编辑工具：Eclipse 集成前端与基于 `XText` 的语法支持。
- 解析/交换/元模型支持：`GAL` 的 `EMF` 元模型、`ETF` adapter、第三方语言到 `GAL` 的转换。
- 仿真/执行支持：重点不是 runtime execution，而是 symbolic exploration 与 witness generation。
- 验证/分析支持：`its-reach`、`its-ctl`、`its-ltl`，以及 `Spot` 支持的 Büchi 路线。
- 代码生成/转换支持：主要是 model-to-model transformation，而不是部署代码生成。
- 标准化或社区生态：`ddd.lip6.fr`、`libDDD`、`libITS`、`Eclipse` 与 `Spot` 生态。

## 适用场景与需求前提

### 适用场景

适合需要把多种并发/协议/实时离散模型统一送进 symbolic backend，并希望复用同一套 reachability、`CTL`、`LTL` 能力的场景。

### 需求前提

1. 原模型必须能稳定翻到 `GAL` 或 `ETF`。
2. 目标系统最终仍需有限状态化。
3. 验证重点应落在 symbolic model checking，而不是 continuous reachability。
4. 团队愿意维护 front-end to `GAL` 的转换层。

### 不适用或高成本场景

如果需求本体是大规模连续动力学、复杂概率数值求解或高保真物理仿真，`ITS-tools` 不是合适主平台。

## 与相邻形式主义的关系

相对 [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)，`JANI` 更偏 quantitative interchange format，而本文是 symbolic backend + pivot language；相对 [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)，两者都强调 language-independent backend，但 `ITS-tools` 通过 `GAL` 统一前端，而 `LTSmin` 通过 `PINS`；相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，`UPPAAL` 是具体 timed-automata 平台，而本文则把 `UPPAAL XTA` 当作可接入的前端之一。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提示我们，后续若 LLM 生成的不是单一目标语言，也可以先落到一个可分析的 pivot language。
2. `GAL` 这种“变量 + guarded transitions”的中间层，对需求到状态机自动建模非常有启发。
3. 在验证闭环里，这类平台有利于快速挂接多个不同来源的模型。

### 作为目标形式主义还是中间表示

更像中间表示和工具基础设施，而不是最终交付给领域用户的目标形式主义。

### 对需求到模型生成的启发

1. 若前端需求来源异构，优先建设统一语义中间层，比直接硬对接多后端更稳。
2. 生成阶段若能落成 guarded-action 风格结构，后续 symbolic verification 更容易接上。
3. 属性层也应与中间层同步设计，而不是事后零散补接。

### 现实限制

它解决的是“怎么统一 symbolic backend”，不是“怎么自动生成正确模型”；对高维连续或 rich quantitative semantics 也不是最佳承载体。

## 重要的相关工作

1. [jani-quantitative-model-and-tool-interaction/desc.md](../jani-quantitative-model-and-tool-interaction/desc.md)：面向 quantitative 工具互操作的另一条中间层路线。
2. [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)：language-independent backend 的另一种实现思路。
3. [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：作为本文第三方前端之一的 timed-automata 工具平台。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`ITS-tools / Guarded Action Language / symbolic model checking`
- 论文角色：symbolic model-checking workbench with `GAL` pivot language and multi-formalism front-ends
- 核心功能：把多前端模型统一送入同一 symbolic backend 做 reachability、`CTL`、`LTL` 检查。
- 关键特性：`GAL`、`ITS` API、`SDD/DDD`、`Spot`、`ETF`、Eclipse 集成。
- 构造方式：third-party models -> `GAL` -> `ITS` symbolic kernel -> property checking。
- 基础设施：`ddd.lip6.fr`、`libDDD`、`libITS`、`Spot`、`EMF/XText`。
- 适用场景：多语言并发模型的统一 symbolic verification。
- 需求前提：模型需可有限化并可转换到 `GAL` / `ETF`。
- 状态：🟢 直接可用

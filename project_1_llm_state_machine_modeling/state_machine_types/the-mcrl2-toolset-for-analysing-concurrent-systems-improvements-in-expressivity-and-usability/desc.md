# mCRL2 工具集：并发系统分析平台 / The mCRL2 Toolset for Analysing Concurrent Systems

## 基本信息

- 标题：The mCRL2 Toolset for Analysing Concurrent Systems: Improvements in Expressivity and Usability
- 中文标题：mCRL2 工具集：并发系统分析平台
- 作者：Olav Bunte，Jan Friso Groote，Jeroen J. A. Keiren，Maurice Laveaux，Thomas Neele，Erik P. de Vink，Wieger Wesselink，Anton Wijs，Tim A. C. Willemse
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2019)*，pp. 21-39，2019
- DOI：`10.1007/978-3-030-17465-1_2`
- 链接：https://doi.org/10.1007/978-3-030-17465-1_2
- 形式主义：`mCRL2 / LPS / PBES`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：action-based process-algebra toolset / `LPS`-`LTS`-`PBES` verification platform
- 工具/实现获取方式：原文明确给出 `www.mcrl2.org` 作为下载入口，并给出 `https://github.com/mCRL2org/mCRL2` 作为源码入口。
- 标准/格式获取方式：原文说明 `mCRL2` 语言、`LPS`、`LTS`、`PBES`、`mcrl2ide` 与 evidence/counterexample workflow 构成主要承载；它是工具平台与语言生态，不是中立交换标准。

## 简报

这篇论文补的是一条很完整的并发验证平台路线：前端用 `mCRL2` 这种 ACP 风格进程代数语言描述并发行为，中间层把规格线性化成 `LPS`，再根据需要生成 `LTS` 或把性质和过程联立成 `PBES`，最后做等价约减、`μ`-calculus` 验证、counterexample / witness 生成和 GUI 化操作。2019 这版的重点，是把概率建模、refinement checking、诊断证据和 `mcrl2ide` 一起补进成熟工具集。

- 形式主义定位：并发 / 分布式系统的 action-based 语言与验证平台，而不是层次状态机母线。
- 构造方式简述：`mCRL2` 规格先经 linearisation 变成 `LPS`，再按需求生成 `LTS` 或 `PBES`，最后做 `μ`-calculus` / equivalence / refinement / evidence analysis。
- 基础设施与场景简述：依托 `mCRL2` 语言、`lps2lts`、`PBES` 工具、probabilistic extension、`mcrl2ide` 与 DSL back-end 应用，服务通信协议、软件产品线、接口一致性与一般并发行为验证。

```text
mCRL2 process specification -> LPS -> LTS or PBES -> equivalence / mu-calculus / refinement / counterexample -> GUI or CLI workflow
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `mCRL2` 行为规格语言；
2. `LPS`；
3. `LTS / probabilistic LTS`；
4. `PBES`；
5. refinement、counterexample 与 `mcrl2ide` 等平台级基础设施。

### 核心抽象

`mCRL2` 的线性过程规格可保守写成：

$$ P(d) = \sum_{i \in I} c_i(d) \rightarrow a_i(f_i(d)) \cdot P(g_i(d)) $$

上式中的符号逐项解释如下：

1. `d` 是过程参数向量。
2. `I` 是可选行为分支集合。
3. `c_i(d)` 是第 `i` 个分支的条件。
4. `a_i(f_i(d))` 是执行动作及其携带的数据。
5. `g_i(d)` 是执行后新的参数赋值。
6. 论文明确说明 `LPS` 本质上就是一组 condition-action-effect rules over parameters。

由此生成的显式行为对象是 labelled transition system：

$$ L = (S, Act, \to, s_0) $$

上式中的符号逐项解释如下：

1. `S` 是可达状态集合。
2. `Act` 是动作集合。
3. `\to` 是带标签转移关系。
4. `s_0` 是初始状态。
5. 论文写得很直接：`LTS` 是把 `LPS` 行为显式化之后的对象。

性质验证则下沉到 `PBES`。论文给出了参数化固定点方程的骨架：

$$ \sigma X(d : D) = \varphi $$

上式中的符号逐项解释如下：

1. `\sigma \in \{\mu,\nu\}` 是最小或最大不动点。
2. `X` 是递归谓词变量。
3. `d : D` 是带类型的数据参数。
4. `\varphi` 是一阶布尔公式，可再含其他递归变量。
5. 论文明确说 `mCRL2` 的 model checking 是把 process + modal `μ`-calculus property 一起翻成 `PBES` 再求解。

### 一个最小例子与通俗解释

论文中的 workflow 很适合用一个过滤器进程来理解：

1. 系统有一个输入动作 `in(v)` 和一个输出动作 `out(v)`。
2. 过滤器只在输入满足某条件时才继续输出，否则保持等待。
3. 用 `mCRL2` 写规格时，动作、条件和数据都在同一语言里表达。
4. 工具先把它线性化成 `LPS`，再视需求生成 `LTS` 或和 `μ`-calculus` 性质一起生成 `PBES`。

通俗地说，`mCRL2` 像把“带数据的并发状态机”写成一种数学味很强的进程语言，然后用自动流水线把它层层降到更适合验证的中间对象。

### 运行 / 接受 / 转移语义

`mCRL2` 的典型验证流水线可保守写成：

$$ Spec \xrightarrow{\text{linearisation}} LPS \xrightarrow{\text{state-space generation}} LTS $$

以及

$$ (LPS, \psi) \xrightarrow{\text{translation}} PBES \xrightarrow{\text{solving}} \{\text{true}, \text{false}\} $$

上式中的符号逐项解释如下：

1. `Spec` 是原始 `mCRL2` 规格。
2. `LPS` 是线性化后的过程规格。
3. `LTS` 是显式状态空间。
4. `\psi` 是 modal `μ`-calculus` 性质。
5. `PBES` 是把过程与性质联立后的参数化布尔方程系统。

对 probabilistic extension，论文说明可生成 probabilistic transition systems，并进行 probabilistic bisimulation 约减。保守写成：

$$ PLTS = (S, Act, \leadsto, s_0) $$

上式中的符号逐项解释如下：

1. `\leadsto` 表示概率转移关系。
2. 这不是本文的唯一主题，但 2019 版确实把 probabilistic behaviour 纳入了主语言与主工具链。
3. 论文用 Monty Hall 等例子解释了 reduced probabilistic state space 的可视化价值。

### 语义边界

1. `mCRL2` 是 action-based process algebra 路线，不是面向层次状态图的语言。
2. 性质语言以 modal `μ`-calculus` 为核心，而不是只提供轻量 `LTL/CTL`。
3. 虽然有概率扩展和许多 DSL back-end 应用，但本文主对象仍然是平台本体，而不是单个应用域 DSL。
4. 对习惯图形状态图的使用者来说，语言入口偏理论化，学习成本相对高。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 线性过程规格 | `$P(d) = \sum_{i \in I} c_i(d) \rightarrow a_i(f_i(d)) \cdot P(g_i(d))$` | `LPS` 把行为压成参数化的 condition-action-effect rules。 |
| 显式状态空间 | `$L = (S, Act, \to, s_0)$` | `lps2lts` 生成的标准 `LTS` 骨架。 |
| `PBES` 方程 | `$\sigma X(d : D) = \varphi$` | `μ`-calculus` 检查的核心中间表示。 |
| 工作流 | `$Spec \to LPS \to LTS$`、`$(LPS,\psi) \to PBES$` | 论文最核心的工具链骨架。 |
| 概率扩展 | `$PLTS = (S, Act, \leadsto, s_0)$` | 2019 版把 probabilistic behaviour 接入主工具集。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | action-based 进程行为可生成显式 `LTS`。 |
| 事件 / 触发 | 很强 | 动作是语义核心。 |
| 守卫 / 数据 | 很强 | 语言原生支持数据、条件、参数化过程。 |
| 层次 | 不支持 | 不是层次状态图路线。 |
| 并发 / 同步 | 很强 | 并发 / 分布式系统正是主对象。 |
| 时间约束 | 弱支持 | 本文主线不是 timed semantics。 |
| 连续动态 / 随机性 | 部分支持 | 概率扩展已经接入，但连续动力学不在主线。 |
| 可执行 / 可验证性 | 很强 | `LPS/LTS/PBES`、refinement、evidence、GUI 都已齐全。 |

### 形式化问题与性质

1. `mCRL2` 的真正强点，是把语言、本体中间层、性质语言和求解后端接成一条统一流水线。
2. 它不是只给一个 model checker，而是给出 `Spec -> LPS -> LTS/PBES` 这条可反复复用的语义链。
3. 2019 版尤其说明平台成熟的关键不只在算法，还在 refinement、counterexample、GUI 和 DSL back-end integration。

## 构造方式与承载格式

### 建模入口

原文给出的主要入口有：

1. `mCRL2` 文本语言；
2. `mcrl2ide` 图形化操作入口；
3. 外部 DSL 到 `mCRL2` 的翻译后端；
4. `μ`-calculus` 性质文件与项目式工作流。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `mCRL2` 规格文件；
2. `LPS`；
3. `LTS`；
4. `PBES`；
5. 诊断证据子图与 witness / counterexample artefacts。

### 交换与互操作

互操作重点在验证中间层：

1. `mCRL2` 可作为多种 DSL 的 verification back-end。
2. `LTS`、`PBES` 和 evidence objects 让不同验证任务共用一套语义中间表示。
3. 论文还明确把 `mCRL2` 与 `LTSmin`、`CADP`、`NuSMV`、`PRISM` 等工具做了横向比较。

## 配套基础设施

- 建模/编辑工具：`mcrl2ide`、文本编辑器与命令行工具链。
- 解析/交换/元模型支持：`mCRL2` 语言、linearisation、`LPS`、`LTS`、`PBES`。
- 仿真/执行支持：可视化状态空间、reduced state space 与诊断 evidence。
- 验证/分析支持：equivalence reduction、refinement checking、`μ`-calculus` model checking、symbolic quotienting、probabilistic bisimulation。
- 代码生成/转换支持：大量 DSL 都以 `mCRL2` 为 back-end；本文专门强调了 DSL integration。
- 标准化或社区生态：官网、GitHub、教程、开源许可证和长期 academic / industrial case studies。

## 适用场景与需求前提

### 适用场景

适合协议、组件交互、并发软件、接口一致性、产品线行为分析和任何能以 action-based process algebra 方式表达的分布式系统。

### 需求前提

1. 团队愿意把行为写成进程代数 / action-based 模型，而不是图形状态图。
2. 性质更偏 modal `μ`-calculus`、refinement、bisimulation 等高表达力验证需求。
3. 若使用概率扩展，需要接受 probabilistic process / transition-system 工作流。
4. 若要让其他 DSL 复用 `mCRL2`，需要稳定的前端翻译关系。

### 不适用或高成本场景

如果目标是直接产出可视化层次状态图、专用实时 automata 模型或工业标准交换格式，`mCRL2` 不是最自然的最终载体。

## 与相邻形式主义的关系

相对 [cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md](../cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md)，两者都走 action-based concurrency platform 路线，但 `mCRL2` 更强调 `LPS/PBES` 工作流与 `μ`-calculus`；相对 [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)，`LTSmin` 是语言无关后端，`mCRL2` 则同时给出语言与后端中间层；相对 [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)，后者是把 `xUML` 接到本文平台的一个具体桥接实例。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“状态机/并发模型 -> 统一线性中间表示 -> 性质方程系统”是一条非常强的验证闭环模式。
2. 对 `project_1` 来说，`LPS` 和 `PBES` 很值得作为“语义规范化层”和“求解层”的参考。
3. 若后续某些需求更适合动作交互视角，而不是图形状态图，`mCRL2` 这条线会比传统状态图工具更有伸缩性。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`mCRL2` 更适合作为高表达力验证中间表示与后端工具生态，而不是唯一的最终输出状态机语言。

## 重要的相关工作

- [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)：直接把现有状态机类 DSL 接入 `mCRL2` 的桥。
- [cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md](../cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md)：另一条 action-based 并发验证平台路线。
- [ltsmin-high-performance-language-independent-model-checking/desc.md](../ltsmin-high-performance-language-independent-model-checking/desc.md)：`mCRL2` 可对接的高性能语言无关后端。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 结论：这是一篇典型的并发验证平台条目，适合作为 `mCRL2` 语言、`LPS/PBES` 中间层、refinement / evidence / DSL back-end 生态的基础设施证据入账。

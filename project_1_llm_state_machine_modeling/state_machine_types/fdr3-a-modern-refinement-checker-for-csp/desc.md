# FDR3：现代 CSP 精化检查器 / FDR3: A Modern Refinement Checker for CSP

## 基本信息

- 标题：FDR3 -- A Modern Refinement Checker for CSP
- 中文标题：FDR3：现代 CSP 精化检查器
- 作者：Thomas Gibson-Robinson，Philip Armstrong，Alexandre Boulgakov，Andrew W. Roscoe
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 8413`，pp. 187-201，2014
- DOI：`10.1007/978-3-642-54862-8_13`
- 链接：https://doi.org/10.1007/978-3-642-54862-8_13
- 形式主义：`CSP_M / GLTS / FDR3 refinement checking`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：modern CSP refinement-checking infrastructure with GLTS compilation and parallel checking
- 工具/实现获取方式：原文引用 `FDR` 工具手册入口 `https://www.cs.ox.ac.uk/projects/fdr/manual/`，并说明前端求值器来自开源 Haskell 库 `libcspm`，入口为 `https://github.com/tomgr/libcspm`。
- 标准/格式获取方式：主承载是 `CSP_M` 文本模型、syntactic process、内部 `GLTS` 表示和 traces / failures / failures-divergences refinement；它不是中立交换标准，而是成熟 CSP 精化检查器和编译后端。

## 简报

这篇论文补的是 `CSP` 过程代数验证工具链里的现代化基础设施锚点。`FDR3` 不是重新提出 `CSP`，而是把 `CSP_M` 前端、syntactic process 求值、`GLTS` 编译、多种内部表示、specification normalisation 与并行 refinement checking 重写成一套比 `FDR2` 更可维护、更可扩展的检查器。

- 形式主义定位：`CSP` / action-based process refinement 的工具基础设施，而不是新的状态机本体。
- 构造方式简述：`CSP_M` 表达式先经 `libcspm` 求值为 syntactic process，再编译成 `GLTS`，最后对 normalized specification 与 implementation 做 refinement checking。
- 基础设施与场景简述：依托 `Explicit / Super-Combinator / Mixed / RecursiveHigh` 编译策略、parallel refinement algorithm、B-tree 缓冲和多核状态对分区，服务通信协议、并发系统和 process-algebra based verification。

```text
CSP_M specification + implementation -> syntactic processes -> GLTS compiler -> normalized spec GLTS + impl GLTS -> parallel refinement checking
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `CSP_M` 表达式与 syntactic process。
2. denotational models，包括 traces、failures 与 failures-divergences。
3. generalized labelled transition systems (`GLTS`)。
4. refinement relation 与 deadlock/livelock/determinism 的等价 refinement check。
5. `Explicit`、`Super-Combinator`、mixed-level 与 recursive high-level 编译策略。

### 核心抽象

论文把前端 `CSP_M` 求值后的 syntactic process 写成算子树，可保守整理为：

$$
P ::= Operator(P_1,\ldots,P_M) \mid N
$$

上式中的符号逐项解释如下：

1. `$P$` 是 syntactic process。
2. `$Operator$` 是 `CSP` 算子，例如 external choice、prefix、parallel composition 等。
3. `$P_1,\ldots,P_M$` 是该算子的子进程。
4. `$N$` 是 process name，由 syntactic process environment 映射到具体进程定义。

`FDR3` 检查的 refinement 关系可写成：

$$
Spec \sqsubseteq_X Impl
$$

上式中的符号逐项解释如下：

1. `$Spec$` 是规范进程。
2. `$Impl$` 是实现进程。
3. `$X$` 是所选 denotational model，例如 traces、failures 或 failures-divergences。
4. 该关系表示 `$Impl$` 的每个行为都被 `$Spec$` 在模型 `$X$` 中允许。

内部 `GLTS` 可保守整理为：

$$
G = (S, s_0, \Sigma_\tau, \to, \lambda_X)
$$

上式中的符号逐项解释如下：

1. `$S$` 是状态集合。
2. `$s_0$` 是初始状态。
3. `$\Sigma_\tau$` 是可见事件与内部 `$\tau$` 事件集合。
4. `$\to \subseteq S \times \Sigma_\tau \times S$` 是带标签迁移关系。
5. `$\lambda_X$` 是按 denotational model `$X$` 给状态附加的语义标签，例如 refusals。
6. 这是根据论文对 `GLTS` 相比普通 `LTS` 多出 state labels 的说明做的保守整理。

### 一个最小例子与通俗解释

一个最小 `FDR3` 例子可以是：

1. `Spec = a -> STOP [] b -> STOP`，表示允许事件 `a` 或 `b` 后终止。
2. `Impl = a -> STOP`，表示实现只会执行 `a`。
3. 在 traces 模型下，`Impl` 的 traces 是 `Spec` 的子集，因此 `Spec \sqsubseteq_T Impl` 成立。
4. `FDR3` 会把二者先编译成内部 `GLTS`，再用 refinement checking 算法确认没有实现侧额外行为。

通俗地说，`FDR3` 像是 `CSP` 进程模型的“行为包含检查器”。它不要求实现和规范状态图长得一样，只要求实现能做出的所有可观察行为都在规范允许范围内。

### 运行 / 接受 / 转移语义

`FDR3` 的基本检查流程可写成：

$$
Check(Spec, Impl, X) = Refines(Normalize(Compile(Spec)), Compile(Impl), X)
$$

上式中的符号逐项解释如下：

1. `$Compile$` 表示从 syntactic process 到 `GLTS` 的编译。
2. `$Normalize$` 表示对 specification `GLTS` 去除 `\tau` 并保证每个状态和每个 initial event 有唯一 successor 的 normalisation。
3. `$Refines$` 表示在模型 `$X$` 中执行 refinement checking。
4. 论文明确指出 deadlock-freedom、livelock-freedom 与 determinism 也会转成等价 refinement checks。

编译策略集合可保守写成：

$$
Strategies = \{Explicit, SuperCombinator, Mixed, RecursiveHigh\}
$$

上式中的符号逐项解释如下：

1. `$Explicit$` 直接构造标准图结构。
2. `$SuperCombinator$` 通过 component machines 与组合规则避免立即展开笛卡尔积。
3. `$Mixed$` 把非递归部分高层编译，把递归部分低层显式编译。
4. `$RecursiveHigh$` 是 `FDR3` 新增策略，允许部分递归进程也以 super-combinator 形式编译。

### 语义边界

1. `FDR3` 主体是 `CSP` / `CSP_M` refinement checking，不是 `UML` 或图形状态机编辑器。
2. 论文强调 action-based process behavior，不直接覆盖 dense-time hybrid dynamics。
3. `Timed CSP` 通过 digitisation 与 prioritisation 路线接入，但本文核心仍是 `FDR3` 的 `GLTS` 编译与 refinement checking infrastructure。
4. 作为工具论文，很多 `CSP` denotational semantics 细节依赖既有 `FDR` / `CSP` 文献，而不是本文重新完整证明。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| syntactic process | `$P ::= Operator(P_1,\ldots,P_M) \mid N$` | `CSP_M` 求值后进入编译器的结构。 |
| refinement | `$Spec \sqsubseteq_X Impl$` | `Impl` 行为被 `Spec` 在模型 `$X$` 中包含。 |
| `GLTS` 骨架 | `$G=(S,s_0,\Sigma_\tau,\to,\lambda_X)$` | `FDR3` 的内部检查载体比普通 `LTS` 多 state labels。 |
| 检查流程 | `$Check(Spec,Impl,X)=Refines(Normalize(Compile(Spec)),Compile(Impl),X)$` | 论文描述的总体工具链。 |
| 编译策略 | `$Strategies=\{Explicit,SuperCombinator,Mixed,RecursiveHigh\}$` | `FDR3` 编译器在表示选择上的主要工程空间。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `CSP` 进程会被编译为 `GLTS`。 |
| 事件 / 触发 | 很强 | action/event 是 `CSP` 与 refinement checking 的核心对象。 |
| 守卫 / 数据 | 条件支持 | `CSP_M` 前端支持表达式、类型检查与求值，但最终检查需落到有限可探索行为。 |
| 层次 | 弱支持 | 支持 syntactic process operator tree 与递归组合，但不是层次状态机语言。 |
| 并发 / 同步 | 很强 | `CSP` 的并行、通信和进程组合是主线。 |
| 时间约束 | 条件支持 | 支持 `Timed CSP` 经 digitisation / prioritisation 的接入路线。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / probabilistic 主线。 |
| 可执行 / 可验证性 | 很强 | refinement、deadlock、livelock、determinism、normalisation、compression 与并行检查都已工具化。 |

### 形式化问题与性质

1. `FDR3` 的关键价值在于把 `CSP` refinement checking 从理论算法落实为可扩展、多核和可维护的工程平台。
2. `GLTS` state labels 使 traces / failures / failures-divergences 等不同模型能复用同一内部图骨架。
3. `Super-Combinator` 与 recursive high-level 策略说明并发进程的结构不能总是粗暴展开，需要在编译层就做表示选择。

## 构造方式与承载格式

### 建模入口

原文给出的主要入口包括：

1. `CSP_M` 规格和实现表达式。
2. syntactic process environment。
3. refinement assertion。
4. deadlock-freedom、livelock-freedom 和 determinism 这类可转化为 refinement 的性质。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `CSP_M` text input。
2. `libcspm` parser、type-checker 与 evaluator。
3. syntactic process trees。
4. internal `GLTS` representations，包括 `Explicit` 与 `Super-Combinator` variants。
5. parallel work queues、B-trees 与 refinement state-pair partitions。

### 交换与互操作

互操作重点不在中立交换格式，而在 `CSP_M -> GLTS -> refinement checker` 的工具链内部：

1. 前端 `libcspm` 把语法和求值职责隔离出来。
2. 中间 `GLTS` 让多种 denotational models 与 compression 共享基础表示。
3. 后端 refinement algorithm 与 parallel scheduler 负责实际状态空间搜索。

## 配套基础设施

- 建模/编辑工具：主入口是 `CSP_M` 文本建模与 `FDR` 工具链；论文不强调图形建模器。
- 解析/交换/元模型支持：`libcspm` 提供 parser、type-checker、evaluator；内部再转到 syntactic process 与 `GLTS`。
- 仿真/执行支持：论文重点在 refinement checking，不主打控制系统 runtime execution。
- 验证/分析支持：trace / failures / failures-divergences refinement，deadlock / livelock / determinism 等性质转化，normalisation，compression，多核 refinement checking。
- 代码生成/转换支持：不以部署代码生成见长，重点是 `CSP_M` 到内部 `GLTS` 的编译。
- 标准化或社区生态：`FDR`、`CSP_M`、`Timed CSP`、`libcspm` 与 Oxford `CSP` 工具生态共同构成基础设施。

## 适用场景与需求前提

### 适用场景

适合通信协议、分布式并发系统、进程代数规格、异步交互逻辑和需要用 refinement 判断实现是否服从规范的系统。

### 需求前提

1. 系统行为需能写成 `CSP_M` 或可翻译到 `CSP_M`。
2. 验证目标最好能落成 refinement、deadlock、livelock 或 determinism 相关检查。
3. 关键数据和进程结构需能有限化到可探索状态空间。
4. 团队接受 process-algebra workflow，而不是只接受图形状态机。

### 不适用或高成本场景

如果目标主要依赖连续物理动力学、概率语义或标准 `UML` 图形交付，`FDR3` 更适合作为后端 sidecar，而不是直接前端建模语言。

## 与相邻形式主义的关系

相对 [cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md](../cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md)，二者都属于 action-based concurrency infrastructure，但 `CADP` 更像多语言工具箱，`FDR3` 更聚焦 `CSP` refinement；相对 [the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md](../the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md)，`mCRL2` 更偏 process algebra 到 `LPS/PBES` 的平台，`FDR3` 更偏 `CSP_M` 到 `GLTS` 的精化检查；相对 [the-model-checker-spin/desc.md](../the-model-checker-spin/desc.md)，`SPIN` 以 `PROMELA + LTL` 为主，`FDR3` 以 `CSP` denotational refinement 为主。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机生成后端可以不只输出普通 `FSM`，也可以输出 action-based process 规格并用 refinement 检查一致性。
2. `CSP_M -> syntactic process -> GLTS -> refinement` 的分层，对后续 LLM 生成器设计中间表示很有参考价值。
3. deadlock/livelock/determinism 到 refinement 的性质转化，也可作为“验证场景生成”阶段的模板。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`FDR3` 更适合作为并发交互模型的验证后端和中间表示目标，而不是控制工程师直接编辑的图形状态机。

### 对需求到模型生成的启发

1. 当需求侧强调协议交互、拒绝集或行为包含时，refinement 比 reachability 更自然。
2. 生成模型时应保留 specification 与 implementation 的双工件关系，以便后续自动验证。
3. 对并发控制逻辑，编译策略和内部表示选择本身会影响可验证性，不应只在自然语言层讨论。

## 重要的相关工作

1. [cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md](../cadp-2010-a-toolbox-for-the-construction-and-analysis-of-distributed-processes/desc.md)：action-based distributed-process verification toolbox。
2. [the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md](../the-mcrl2-toolset-for-analysing-concurrent-systems-improvements-in-expressivity-and-usability/desc.md)：process-algebra toolset 与 `PBES` 验证路线。
3. [the-model-checker-spin/desc.md](../the-model-checker-spin/desc.md)：异步过程模型检查和 `LTL` 反例路线对照。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`CSP_M / GLTS / FDR3 refinement checking`
- 论文角色：modern CSP refinement-checking infrastructure with GLTS compilation and parallel checking
- 核心功能：把 `CSP_M` 规格编译为 `GLTS` 并检查 traces / failures / failures-divergences refinement
- 关键特性：`libcspm`、syntactic process、`GLTS`、normalisation、parallel refinement checking、super-combinator compilation
- 构造方式：`CSP_M -> syntactic process -> GLTS -> normalized refinement check`
- 基础设施：`FDR3`、`libcspm`、`Explicit / Super-Combinator / Mixed / RecursiveHigh` 编译策略
- 适用场景：协议、分布式并发系统、process-algebra specification 与 refinement verification
- 需求前提：系统需可落成 bounded `CSP_M` 行为，目标性质适合 refinement 或其等价转化
- 状态：🟢

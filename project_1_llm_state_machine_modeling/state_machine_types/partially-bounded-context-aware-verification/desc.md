# 部分有界的上下文感知验证 / Partially Bounded Context-Aware Verification

## 基本信息

- 标题：Partially Bounded Context-Aware Verification
- 中文标题：部分有界的上下文感知验证
- 作者：Luka Le Roux，Ciprian Teodorov
- 发表：*Software Engineering and Formal Methods: 17th International Conference, SEFM 2019*，pp. 532-548，2019
- DOI：`10.1007/978-3-030-30446-1_28`
- 链接：https://doi.org/10.1007/978-3-030-30446-1_28
- 形式主义：`xGDL / partially-bounded Context-aware Verification / guide-guided reachability`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：guide-language-based decomposition and partially-bounded verification route
- 工具/实现获取方式：论文明确描述 `xGDL -> NFA -> DFA` 编译、与 closed transition system 的同步组合，以及后续对接 `CaV` 分解与 reachability 分析；正文未提供独立公开仓库。
- 标准/格式获取方式：核心承载对象是 `xGDL` guide text、编译后的 `DFA` guide、closed transition system 与 labeling function；它是验证导向 DSL，不是行业交换标准。

## 简报

这篇论文的关键贡献，不是再优化一次模型检查器内部数据结构，而是在模型检查之前先把“环境如何约束系统”单独变成一门 guide language，再只对 guide 侧做有界展开。作者把原来 `CaV` 必须手工给出 acyclic guides 的痛点放宽为“先写可以有环的 `xGDL` guide，再自动编译成 `DFA`，最后只展开 guide 到某个 bound”。这样既保留了 `CaV` 的分解优势，又把原来最难维护的 acyclic scenario 手工提取工作大幅减轻。

- 形式主义定位：环境 guide 驱动的 reachability / decomposition 方法路线，而不是新的状态机本体。
- 构造方式简述：`xGDL text -> NFA -> DFA -> guide × closed system -> guide-only bounded unrolling -> CaV-style decomposition / reachability`。
- 基础设施与场景简述：依托 `xGDL`、`DFA` guide、labeling function 和 partially-bounded procedure，服务大状态空间软件/控制系统验证。

```text
closed system + xGDL guide -> compiled DFA guide -> synchronous composition -> partial guide unrolling -> decomposed reachability analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. closed transition system；
2. interaction alphabet；
3. `xGDL` guide language；
4. 编译后的 `DFA` verification guide；
5. partially-bounded verification procedure。

### 核心抽象

论文直接给出了 `xGDL` 的抽象语法骨架。可保守整理为：

$$
C ::= ? \mid a \mid C;C \mid C \star C \mid C \parallel C \mid C? \mid C^+ \mid C^* \mid C^{\{i,j\}} \mid \{i,j\}\mathrm{of}[C_1,\ldots,C_n]
$$

上式中的符号逐项解释如下：

1. `a` 是 interaction alphabet 中的一个可观察动作。
2. `C;C` 是顺序组合。
3. `C \star C` 是非确定选择。
4. `C \parallel C` 是并行交织。
5. `C?`、`C^+`、`C^*` 和 `C^{\{i,j\}}` 对应不同的可选/重复结构。
6. `\{i,j\}\mathrm{of}[...]` 表示有限长度排列选择。

论文把 `xGDL` guide 与 closed system 通过 labeling function 同步组合。可保守写成：

$$
G \otimes S
$$

上式中的符号逐项解释如下：

1. `G` 是编译后的 `DFA` guide。
2. `S` 是 closed transition system。
3. `\otimes` 是在可观察 interaction 上同步、在 `\tau` 上允许 stutter 的组合。

同步推进可写成：

$$
(g, s) \xrightarrow{a} (g', s') \iff g \xrightarrow{a} g' \land s \xrightarrow{a} s'
$$

而内部 stutter 可保守写成：

$$
(g, s) \xrightarrow{\tau} (g, s') \iff s \xrightarrow{\tau} s'
$$

论文还明确指出有界性只施加在 guide 侧。可保守写成：

$$
b_{guide} \ge rd(G \otimes S)
$$

上式中的符号逐项解释如下：

1. `b_{guide}` 是 guide 的展开深度。
2. `rd(G \otimes S)` 是组合系统 reachability diameter 风格的 completeness threshold。
3. 论文的重点正是把 completeness 讨论转成“guide 展开多深才够”。

### 一个最小例子与通俗解释

论文的主案例是航空领域的 `Landing Gear System`：

1. 系统先被看成一个 closed transition system。
2. 环境交互序列用 `xGDL` 编写，而不再手工写死 acyclic scenario。
3. 这些 guide 会被编译成 `DFA`，再和系统同步。
4. 若直接分析仍不缩放，则继续对 guide 做结构重写和部分有界展开。

通俗地说，这条路线像“把环境约束先写成一份可编译脚本，然后让验证器只在这份脚本上做有限展开，而不是在整个系统上统一加全局 bound”。

### 运行 / 接受 / 转移语义

论文把 `xGDL` 先解释成 `NFA` 再 determinize。这个编译链可以保守整理为：

$$
xGDL \xrightarrow{\tau_1} NFA \xrightarrow{\tau_2} DFA
$$

其中：

1. `\tau_1` 由文中的 operational semantics 规则驱动。
2. `\tau_2` 是标准 automata determinization / minimization。
3. 编译后的 `DFA` guide 才是后续实际验证入口。

### 语义边界

1. 论文主线是 guide-guided reachability，不是替代任意 model checker 的通用语言。
2. 对 completeness 的保证最终仍要依赖合适的 bound 或额外证明。
3. guide 的价值主要在环境约束和问题分解，而不是表达系统内部全部语义。
4. 论文案例聚焦 safety 和 bounded-liveness 友好的 reachability 视角。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `xGDL` 语法骨架 | `$C ::= ? \mid a \mid \cdots$` | guide 的文本化表达入口。 |
| guide 与系统组合 | `$G \otimes S$` | 验证对象不是裸系统，而是 guide 约束后的组合系统。 |
| 同步规则 | `$(g,s) \xrightarrow{a} (g',s')$` | interaction 上同步、内部步上 stutter。 |
| 部分有界性 | `$b_{guide} \ge rd(G \otimes S)$` | 完备性阈值只针对 guide 展开深度。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | guide 本身最终编译为 `DFA` 状态机。 |
| 事件 / 触发 | 很强 | interaction alphabet 是整个方法的驱动核心。 |
| 守卫 / 数据 | 弱支持 | 重点在行为约束和环境交互，而不是富数据状态。 |
| 层次 | 不适用 | 不是层次状态机语义扩展。 |
| 并发 / 同步 | 中等支持 | 通过并行交织和同步组合约束环境交互。 |
| 时间约束 | 弱支持 | 本文主线不是显式时间，而是环境 guide 分解。 |
| 连续动态 / 随机性 | 不支持 | 关注离散 transition-system 级 reachability。 |
| 可执行 / 可验证性 | 很强 | 文本 guide、自动编译、同步组合和分解分析一体化。 |

### 形式化问题与性质

1. 论文真正解决的是“`CaV` 的 guide 该怎么从难维护的 acyclic 手工场景，提升到可编译、可有环的文本语言”。
2. 它把全局有界问题收缩成 guide-only 有界问题，因此比传统 `BMC` 更有结构感。
3. 对文库来说，这是很典型的“验证 profile / guide language”方法条目。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. closed transition system；
2. interaction labeling function；
3. `xGDL` guide 文本；
4. 编译后的 `DFA` guide；
5. guide 重写与部分有界展开参数。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `xGDL` 文本表达式；
2. `NFA/DFA` guide；
3. labeled transition system；
4. guide × system 的组合系统；
5. decomposition / reachability 任务。

### 交换与互操作

这条路线的互操作重点在：

1. `xGDL` 与具体系统语义通过 labeling function 解耦；
2. 编译后的 guide 可以作为一般 automata 对象进入后续验证流程；
3. 与 `CaV` 既有分解算法是互补关系，而不是替代关系。

## 配套基础设施

- 建模/编辑工具：`xGDL` guide 文本与 closed-system 建模入口。
- 解析/交换/元模型支持：`xGDL -> NFA -> DFA` 编译与 minimization。
- 仿真/执行支持：重点不是执行系统，而是 guide 驱动的 reachability 分析。
- 验证/分析支持：guide-system 同步组合、部分有界展开、`CaV` 分解与 completeness 讨论。
- 代码生成/转换支持：编译产物是 guide automaton，而非部署代码。
- 标准化或社区生态：依附 `CaV` 研究路线；原文未给独立社区标准。

## 适用场景与需求前提

### 适用场景

适合环境交互复杂、直接模型检查容易爆炸、但环境约束又可以通过 guide 结构化表达的验证任务。

### 需求前提

1. 系统可以整理成 closed transition system。
2. 环境交互能通过有限 alphabet 标注到系统迁移上。
3. 设计者愿意额外编写 verification guide。
4. 目标问题主要还是 safety / reachability / bounded-liveness 风格。

### 不适用或高成本场景

如果交互 alphabet 本身难以稳定定义，或者验证者无法提炼出可解释的 guide，这条路线的收益会下降。

## 与相邻形式主义的关系

相对 [timed-automata-verification-and-synthesis-via-finite-automata-learning/desc.md](../timed-automata-verification-and-synthesis-via-finite-automata-learning/desc.md)，那篇通过学习压缩大离散空间，这篇通过 environment guide 改写验证任务结构；相对 [improving-search-order-for-reachability-testing-in-timed-automata/desc.md](../improving-search-order-for-reachability-testing-in-timed-automata/desc.md)，那篇优化后端搜索顺序，这篇则在后端之前先做问题分解；相对 [automatic-verification-of-bpmn-models/desc.md](../automatic-verification-of-bpmn-models/desc.md)，后者把业务流程翻到 `OBP` 路线，而这里是通过 `xGDL` 限定系统环境行为。

## 与本研究的关系

### 对 Project 1 的价值

1. 这篇论文说明，仅有状态机模型还不够，很多验证任务还需要一层“验证剖面/guide”来约束环境与场景。
2. 这和博士研究中“基于模型元素生成验证场景与待验证性质”的方向高度相关。
3. `xGDL` 这类文本化 guide 语言，非常适合未来让 LLM 参与生成或修补验证场景。

### 作为目标形式主义还是中间表示

更像验证 profile / guide 的中间表示，而不是最终目标形式主义。

### 对需求到模型生成的启发

1. 场景约束最好被显式写成可分析对象，而不是埋在口头假设里。
2. guide 可以和主模型解耦，便于后续独立修补和重用。
3. 在爆炸性系统上，分解结构往往比单纯换一个更快后端更重要。

## 重要的相关工作

- [timed-automata-verification-and-synthesis-via-finite-automata-learning/desc.md](../timed-automata-verification-and-synthesis-via-finite-automata-learning/desc.md)：另一条通过结构化替代模型来缓解验证规模的方法路线。
- [improving-search-order-for-reachability-testing-in-timed-automata/desc.md](../improving-search-order-for-reachability-testing-in-timed-automata/desc.md)：偏后端搜索优化的相邻思路。
- [automatic-verification-of-bpmn-models/desc.md](../automatic-verification-of-bpmn-models/desc.md)：把高层业务流程约束接入形式验证工具链的另一类桥接条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`xGDL / partially-bounded Context-aware Verification / guide-guided reachability`
- 论文角色：guide-language-based decomposition and partially-bounded verification route
- 归类理由：论文主体是围绕 `xGDL` guide language、`DFA` 编译和部分有界展开组织验证流程，因此最适合作为验证 guide / profile 方法路线条目入账。

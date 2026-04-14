# libalf：自动机学习框架 / libalf: The Automata Learning Framework

## 基本信息

- 标题：libalf: The Automata Learning Framework
- 中文标题：libalf：自动机学习框架
- 作者：Benedikt Bollig，Joost-Pieter Katoen，Carsten Kern，Martin Leucker，Daniel Neider，David R. Piegdon
- 发表：*Computer Aided Verification*，`LNCS 6174`，pp. 360-364，2010
- DOI：`10.1007/978-3-642-14295-6_32`
- 链接：https://doi.org/10.1007/978-3-642-14295-6_32
- 形式主义：`automata learning / libalf / online-offline learning framework`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：open-source automata-learning framework with online/offline algorithms, filters and distributed interfaces
- 工具/实现获取方式：原文明确给出 `libalf` 官网 `http://libalf.informatik.rwth-aachen.de/`，并说明提供 `C++` core、Java `JNI` interface、network-based dispatcher、`liblangen` 与 `AMoRE++` 配套组件。
- 标准/格式获取方式：原文承载重点是 `teacher / knowledgebase / hypothesis` 接口、`C++` 类层次、`JNI` 与 dispatcher；不是中立交换标准，而是学习框架的程序接口和运行架构。

## 简报

这篇论文的重点，是把自动机学习从“某个算法的 proof-of-concept 实现”提升成一套可替换 learner、可重用知识库、可接分布式 teacher、还能挂 filters/normalizers 的工程框架。`libalf` 同时支持 online 与 offline learning，并把 `L*`、`NL*`、Kearns/Vazirani、Biermann、RPNI 等算法放进统一骨架里。

- 形式主义定位：automata learning 基础设施，而不是新的状态机本体。
- 构造方式简述：以 `knowledgebase` 为中心，把 teacher、learning algorithm、hypothesis model、filters 和 normalizers 解耦。
- 基础设施与场景简述：依托 `C++` core、Java `JNI`、dispatcher、`liblangen`、`AMoRE++`、logger / statistics / GraphViz，服务 formal-language learning、接口推断与验证前模型恢复。

```text
teacher / examples -> knowledgebase -> learning algorithm -> hypothesis automaton -> filters / normalizers / statistics / visualization
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. online / offline automata learning algorithms；
2. `knowledgebase`；
3. teacher / information source；
4. filters 与 normalizers；
5. `JNI`、dispatcher、`liblangen` 与 `AMoRE++`。

### 核心抽象

对 `libalf`，学习流程可以保守整理为：

$$
\mathcal{L} = (\Sigma, \mathrm{KB}, \mathrm{Teacher}, \mathrm{Alg}, H)
$$

上式中的符号逐项解释如下：

1. `$\Sigma$` 是学习字母表。
2. `$\mathrm{KB}$` 是 `knowledgebase`，负责存放 query 及其 classification。
3. `$\mathrm{Teacher}$` 是能够回答 query 的信息源。
4. `$\mathrm{Alg}$` 是具体学习算法，如 `L^\ast`、`NL^\ast`、Kearns/Vazirani、RPNI 等。
5. `$H$` 是输出的 hypothesis automaton。

论文还把 `knowledgebase` 抽象成对查询结果的存储：

$$
\mathrm{KB} : \Sigma^\ast \to C
$$

上式中的符号逐项解释如下：

1. `$\Sigma^\ast$` 是所有有限词。
2. `$C$` 是 classification 的值域；原文指出在多数算法里通常是布尔值，但框架允许是任意 `C++` 对象。
3. 这说明 `knowledgebase` 被设计成与具体 learner 解耦的外部存储层。

对 normalizer，论文明确把它理解成一个等价关系：

$$
\sim \;\subseteq\; \Sigma^\ast \times \Sigma^\ast
$$

上式中的符号逐项解释如下：

1. `$\sim$` 是 domain-specific equivalence relation。
2. 若两个 query 等价，就只需存一个 representative。
3. 这既减少内存消耗，也减少真正发送给 teacher 的查询数。

### 一个最小例子与通俗解释

最小例子可以这样理解：

1. 你有一个 teacher，能回答某个词是否属于目标语言。
2. `libalf` 把这些词和答案都存进 `knowledgebase`。
3. 你先用 `L*` 学出一个 DFA。
4. 如果想换成 `RPNI` 或 `Biermann`，往往只需改很少的代码，而不是重写整套交互逻辑。

通俗地说，`libalf` 像“自动机学习实验室的底层总线”。算法、teacher、优化器、日志和可视化都能插上去，而且彼此尽量解耦。

### 运行 / 接受 / 转移语义

论文的核心并不在某一具体 automaton 语义，而在 learner 与 teacher 的交互闭环。可保守写成：

$$
H_{i+1} = \mathrm{Learn}(\mathrm{KB}_i \cup \{(q_i, c_i)\})
$$

上式中的符号逐项解释如下：

1. `$q_i$` 是第 `$i$` 次 query。
2. `$c_i$` 是 teacher 或 filter 给出的 classification。
3. `$\mathrm{KB}_i$` 是当前知识库。
4. `$H_{i+1}$` 是根据更新后的知识库产生的新 hypothesis。

对 filters，可保守写成：

$$
\mathrm{ans}(q) =
\begin{cases}
\mathrm{Filter}(q), & \text{若领域知识足以回答} \\
\mathrm{Teacher}(q), & \text{否则}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `$q$` 是待分类 query。
2. `$\mathrm{Filter}(q)$` 表示用领域知识直接回答。
3. `$\mathrm{Teacher}(q)$` 表示需要真的向 teacher 提问。
4. 这正是论文说的“减少实际 teacher queries”的机制。

### 语义边界

这篇论文的边界也很清楚：

1. 它主要服务有限自动机及邻近学习对象，不直接处理 timed / hybrid families。
2. 它是学习框架，不是直接从自然语言需求生成状态机。
3. 它强调 learner infrastructure，而不是某个特定理论结果。
4. 更丰富的数据型学习在 2010 年版本里还不是主线。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 学习工作流 | `$\mathcal{L} = (\Sigma, \mathrm{KB}, \mathrm{Teacher}, \mathrm{Alg}, H)$` | 概括 `libalf` 的核心交互结构。 |
| 知识库存储 | `$\mathrm{KB} : \Sigma^\ast \to C$` | 说明 query/classification 独立于具体 learner 存储。 |
| normalizer 等价关系 | `$\sim \subseteq \Sigma^\ast \times \Sigma^\ast$` | 用领域等价减少内存与查询数。 |
| filter 判定分流 | `$\mathrm{ans}(q)$` 的分段定义 | 体现 domain-specific optimization 的工程价值。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 主体就是 finite-state learning infrastructure。 |
| 事件 / 触发 | 很强 | 以 query words 和 classifications 为中心。 |
| 守卫 / 数据 | 弱支持 | 2010 版主体仍偏有限自动机，不是 dataful learning 框架。 |
| 层次 | 不支持 | 不面向 hierarchical state machines。 |
| 并发 / 同步 | 间接支持 | 可学习 communicating automata 等对象，但不是原生并发建模语言。 |
| 时间约束 | 不支持 | 不是 timed-automata learning tool。 |
| 连续动态 / 随机性 | 不支持 | 不处理 hybrid / stochastic dynamics。 |
| 可执行 / 可验证性 | 很强 | `C++`、`JNI`、dispatcher、logger、statistics 与 GraphViz 全都到位。 |

### 形式化问题与性质

1. `libalf` 真正补的是“多学习算法共享同一工程骨架”。
2. `knowledgebase` 外置化让不同 learner 可以复用已有 queries，不必重复问 teacher。
3. filters 与 normalizers 是非常典型的“把领域知识灌进学习框架”的工程接口。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. online teacher queries；
2. offline labelled examples；
3. `C++` API；
4. Java `JNI`；
5. network-based dispatcher。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `knowledgebase`；
2. generic hypothesis interfaces；
3. `C++` class hierarchy；
4. filters / normalizers；
5. dispatcher-based client/server communication。

### 交换与互操作

这篇论文的互操作重点不是统一文件格式，而是统一框架边界：

1. learner 可替换。
2. teacher 可本地也可远程。
3. Java 程序可通过 `JNI` 调 `C++` core。
4. `AMoRE++` 与 `liblangen` 提供额外算法和测试支撑。

## 配套基础设施

- 建模/编辑工具：主线不是 GUI 编辑器，而是 `C++` / Java 接口、dispatcher 与实验框架。
- 解析/交换/元模型支持：`knowledgebase`、generic automata interfaces、`AMoRE++` integration。
- 仿真/执行支持：teacher / dispatcher 能驱动实际查询交互，但不面向工业控制运行时。
- 验证/分析支持：支持多种 online/offline learning algorithms、filters、normalizers、statistics 与 GraphViz 输出。
- 代码生成/转换支持：不以部署代码生成见长，重点是 hypothesis construction 与 automata manipulation。
- 标准化或社区生态：开放源码、跨平台、`JNI`、dispatcher、`AMoRE++`、`liblangen`。

## 适用场景与需求前提

### 适用场景

适合 formal-language learning、模型恢复、黑盒接口分析、算法对比实验，以及任何需要快速切换 automata learning 算法的研究环境。

### 需求前提

1. 问题能落成 query/classification learning setting。
2. 存在 teacher 或至少有 labelled sample set。
3. 团队需要的是学习框架和实验底座，而不是单篇算法的临时实现。

### 不适用或高成本场景

若目标是 rich timed / hybrid / continuous-state 模型学习，或者自然语言到状态机的正向生成，`libalf` 不是直接解法。

## 与相邻形式主义的关系

相对 [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)，`LearnLib` 更偏现代 modular active learning 框架，而 `libalf` 更早同时覆盖 online/offline learning；相对 [aalpy-an-active-automata-learning-library/desc.md](../aalpy-an-active-automata-learning-library/desc.md)，`AALpy` 更轻量、Pythonic，而 `libalf` 更强调 `C++` core、JNI 和 distributed dispatcher；相对 [scalable-tree-based-register-automata-learning/desc.md](../scalable-tree-based-register-automata-learning/desc.md)，后者是 dataful RA learning 的新算法路线，而本文提供更通用的学习框架底座。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“从已有系统行为恢复状态机”已有成熟框架，不必完全依赖需求到模型的正向生成。
2. `knowledgebase + learner + teacher` 的解耦，也适合借鉴到 LLM 驱动的闭环建模工具架构中。
3. filters / normalizers 这种领域注入点，对控制系统样本学习尤其有启发。

### 作为目标形式主义还是中间表示

更适合作为模型恢复和对照验证的基础设施，而不是最终状态机交付格式。

### 对需求到模型生成的启发

1. 正向生成与行为学习可以互为校验。
2. 统一 query 存储层比把 learner 写死在单算法里更适合长期扩展。
3. 若后续要做“生成 - 验证 - 修复”闭环，knowledgebase 风格的中间层很值得借鉴。

## 重要的相关工作

1. [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)：现代化主动自动机学习框架。
2. [aalpy-an-active-automata-learning-library/desc.md](../aalpy-an-active-automata-learning-library/desc.md)：轻量 Python 主动学习库。
3. [scalable-tree-based-register-automata-learning/desc.md](../scalable-tree-based-register-automata-learning/desc.md)：register automata 学习的可扩展新路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`automata learning / libalf / online-offline learning framework`
- 论文角色：open-source automata-learning framework with online/offline algorithms, filters and distributed interfaces
- 归类理由：论文主体是 automata learning 的统一工程框架，而不是单个 automaton family 或单一学习算法。

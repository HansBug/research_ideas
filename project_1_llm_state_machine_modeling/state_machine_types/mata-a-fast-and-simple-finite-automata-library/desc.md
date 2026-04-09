# Mata：快速而简洁的有限自动机库 / Mata: A Fast and Simple Finite Automata Library

## 基本信息

- 标题：Mata: A Fast and Simple Finite Automata Library
- 中文标题：Mata：快速而简洁的有限自动机库
- 作者：David Chocholatý，Tomáš Fiedor，Vojtěch Havlena，Lukáš Holík，Martin Hruška，Ondřej Lengál，Juraj Síč
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 14571`，pp. 130-151，2024
- DOI：`10.1007/978-3-031-57249-4_7`
- 链接：https://doi.org/10.1007/978-3-031-57249-4_7
- 形式主义：`finite automata / Mata / antichain inclusion / simulation reduction`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：finite-automata algorithm library / C++ and Python infrastructure
- 工具/实现获取方式：原文明确给出 GitHub 入口 `https://github.com/VeriFIT/mata`，并说明提供 `C++` API 与 `Python` binding，`pip install libmata` 可直接安装 Python 版本。
- 标准/格式获取方式：原文说明支持 textual automata format、regex parser、`C++` API、Python binding 与 benchmark suite；不依赖统一行业交换标准。

## 简报

这篇论文的核心贡献，是把自动机算法“做成一套真正适合研究与工程复用的库”。`Mata` 不只实现基本 `NFA/DFA` 算法，还把 antichain-based inclusion checking、fast simulation reduction、large benchmark 和 Python binding 打包成一个统一基础设施，并把“显式 transition relation 也能做到很快”这件事做得很有说服力。

- 形式主义定位：有限自动机算法基础设施，而不是新的自动机本体。
- 构造方式简述：围绕显式 `NFA` transition relation 设计三层 `Delta` 数据结构，以支持 subset construction、product construction、inclusion checking 和 simulation reduction。
- 基础设施与场景简述：依托 `C++`、STL、Python binding、benchmark suite 和 GitHub 工程化体系，服务 string solving、regex processing 与 regular model checking。

```text
regex / automata input -> Mata core data structures -> automata algorithms -> C++ / Python applications and benchmarks
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `Mata`：

1. finite automata library；
2. explicit transition relation；
3. subset construction / product construction；
4. antichain-based inclusion checking；
5. simulation-based reduction；
6. benchmark and Python binding。

### 核心抽象

论文采用的自动机骨架可整理为：

$$
A = (Q, \mathrm{post}, I, F)
$$

上式中的符号逐项解释如下：

1. `$Q$` 是状态集合。
2. `$\mathrm{post}(q,a)$` 给出从状态 `$q$` 在符号 `$a$` 下的后继集合。
3. `$I$` 是初始状态集合。
4. `$F$` 是终止状态集合。
5. 论文就是围绕这一显式 `post` 语义来设计 `Delta` 数据结构。

论文还明确给出 subset construction：

$$
\mathrm{DFA}(A) = (Q_{\subseteq}, \mathrm{post}_{\subseteq}, I_{\subseteq}, F_{\subseteq})
$$

上式中的符号逐项解释如下：

1. `$Q_{\subseteq} = \mathcal{P}(Q)$` 是宏状态集合。
2. `$I_{\subseteq} = \{I\}$` 是初始宏状态。
3. `$F_{\subseteq}$` 由与 `$F$` 相交的宏状态组成。
4. `$\mathrm{post}_{\subseteq}(S,a)=\bigcup_{s \in S}\mathrm{post}(s,a)$`。
5. 论文以此为基础说明 `Delta` 为什么能高效支持 determinization。

结合论文的数据结构描述，可把 transition relation 的实现骨架保守写成：

$$
\Delta[q] = \big[(a_1, T_1), \ldots, (a_k, T_k)\big]
$$

上式中的符号逐项解释如下：

1. `$q$` 是某个源状态。
2. `$a_i$` 是某个转移符号。
3. `$T_i$` 是该符号下的目标状态有序集合。
4. 整个 `\Delta[q]` 由按 symbol 排序的 `SymbolPost` 组成。
5. 这是论文 `Delta` 三层结构的简化表达。

### 一个最小例子与通俗解释

论文直接给出一个 Python 例子：把两个 regex 解析成 automata，再做 concatenate 与 trim。直观理解就是：

1. 先把正则 `((a+b)*a)*` 和 `aab*` 变成自动机。
2. 再在库里直接做 concatenation。
3. 最后把结果 trim 并画图。

通俗地说，`Mata` 像“自动机算法的高性能零件箱”。你不用自己再写 determinization、product、inclusion checking，只要把 automaton 交给库，它就能在 `C++` 或 Python 里快速跑这些操作。

### 运行 / 接受 / 转移语义

论文对 product construction 的描述可压成：

$$
\mathrm{post}_{\times}((q,r), a) = \mathrm{post}_1(q,a) \times \mathrm{post}_2(r,a)
$$

上式中的符号逐项解释如下：

1. `$(q,r)$` 是乘积自动机中的状态对。
2. `$\mathrm{post}_1$` 与 `$\mathrm{post}_2$` 分别来自两个输入自动机。
3. 笛卡尔积给出同步符号下的目标状态对集合。
4. 论文据此展开 product construction 的高效迭代实现。

论文还强调 inclusion checking 采用 antichain 思路。可保守写成：

$$
L(A) \subseteq L(B)
$$

上式中的符号逐项解释如下：

1. `$L(A)$` 和 `$L(B)$` 是两个自动机识别的语言。
2. inclusion checking 的目标是判断左语言是否包含于右语言。
3. 论文通过 antichain-based pruning 避免枚举大量冗余状态集。

### 语义边界

这篇论文的边界主要有：

1. 主线是 finite automata algorithms，而不是 richer state-machine families。
2. 时间、层次、连续动态和数据守卫都不在主线内。
3. 大字母表/无限字母表问题主要靠 preprocessing/mintermization，而不是核心数据结构直接承载。
4. 工具重点在算法速度和工程质量，而不是图形编辑体验。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 自动机骨架 | `$A = (Q, \mathrm{post}, I, F)$` | `Mata` 的基本工作对象。 |
| 子集构造 | `$\mathrm{post}_{\subseteq}(S,a)=\bigcup_{s \in S}\mathrm{post}(s,a)$` | determinization 的核心。 |
| 乘积构造 | `$\mathrm{post}_{\times}((q,r), a) = \mathrm{post}_1(q,a) \times \mathrm{post}_2(r,a)$` | intersection/product 的核心。 |
| 语言包含 | `$L(A) \subseteq L(B)$` | antichain inclusion checking 的判定目标。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接支持 `NFA/DFA` 级别高性能操作。 |
| 事件 / 触发 | 中等支持 | 本质上是 alphabet symbols，不是 richer event calculus。 |
| 守卫 / 数据 | 弱支持 | 依赖 preprocessing，不是原生 data automata 库。 |
| 层次 | 不支持 | 主线不在层次状态机。 |
| 并发 / 同步 | 间接支持 | 通过 product construction 组合自动机。 |
| 时间约束 | 不支持 | 不是 timed automata library。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散有限自动机。 |
| 可执行 / 可验证性 | 很强 | `C++` API、Python binding、benchmark 和 GitHub CI 全都到位。 |

### 形式化问题与性质

1. `Mata` 的重点不只是“实现了一些算法”，而是把 automata library 做到足够快、足够简洁、足够可扩展。
2. 论文证明显式 transition relation 不必天然慢，只要数据结构设计得当。
3. 对本文库而言，它补的是 classic finite-automata tooling，而不是 theoretical family 本身。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. textual automata format；
2. regex parser；
3. `C++` API；
4. Python binding。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Delta` 三层 transition relation；
2. sparse sets 与 `OrdVector`；
3. regex parsing；
4. benchmark inputs；
5. Python notebooks。

### 交换与互操作

`Mata` 的互操作重点在程序库接口而不是中立标准：

1. `C++` API 面向低层算法集成。
2. Python binding 面向快速实验与教学。
3. benchmark suite 让不同应用域的问题都能落到同一库上比较。

## 配套基础设施

- 建模/编辑工具：不是图形编辑器，核心是 `C++` API、regex parser 和 Python interface。
- 解析/交换/元模型支持：textual automata format、regex parsing、alphabet handling、mintermization。
- 仿真/执行支持：支持构造、组合和遍历自动机，但不面向控制执行 runtime。
- 验证/分析支持：antichain-based inclusion checking、simulation reduction、determinization、trim、emptiness 等。
- 代码生成/转换支持：不以代码生成为主，但高度支持 automata-to-automata transformations。
- 标准化或社区生态：GitHub、PyPI、benchmark suite、Jupyter notebooks 与 string-solver ecosystem。

## 适用场景与需求前提

### 适用场景

适合 string constraint solving、regex processing、regular model checking，以及任何需要高性能 finite-automata algorithms 的研究和工程场景。

### 需求前提

1. 问题能被压成 finite automata 操作。
2. 团队需要低层高性能库，而不是 GUI 建模工具。
3. 关注点是 inclusion、determinization、product、simulation reduction 等经典操作。
4. 若使用 Python，需要接受底层仍以 `C++` 实现。

### 不适用或高成本场景

若系统本质是 timed、hybrid、hierarchical 或带 rich data guards 的状态机，`Mata` 只能作为局部算法后端，而不是直接目标承载。

## 与相邻形式主义的关系

相对 [openfst-a-general-and-efficient-weighted-finite-state-transducer-library/desc.md](../openfst-a-general-and-efficient-weighted-finite-state-transducer-library/desc.md)，`OpenFst` 更偏加权转导器，`Mata` 更聚焦 finite automata 本体与 inclusion/simulation 算法；相对 [a-visual-and-interactive-automata-theory-course-with-jflap-40/desc.md](../a-visual-and-interactive-automata-theory-course-with-jflap-40/desc.md)，`JFLAP` 更偏教学交互，`Mata` 更偏高性能算法库；相对 [libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md](../libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md)，两者都是 `C++` 库，但 `libFAUDES` 偏 DES/control engineering，`Mata` 偏 general finite-automata algorithms。

## 与本研究的关系

### 对 Project 1 的价值

1. 它为 `project_1` 提供了一个很实用的思路：即便目标不是 classic automata，很多后端判定和比较问题仍然可以下沉到成熟 automata library。
2. 若后续要做 LLM 生成模型的 regex/automata sanity checking、language inclusion 或 counterexample-style preprocessing，`Mata` 很有价值。
3. benchmark-first 的基础设施建设方式，也值得本文库借鉴。

### 作为目标形式主义还是中间表示

更适合作为算法后端和中间处理层，而不是最终交付给控制系统建模者的前端形式主义。

## 重要的相关工作

1. [openfst-a-general-and-efficient-weighted-finite-state-transducer-library/desc.md](../openfst-a-general-and-efficient-weighted-finite-state-transducer-library/desc.md)：加权自动机/转导器算法库。
2. [a-visual-and-interactive-automata-theory-course-with-jflap-40/desc.md](../a-visual-and-interactive-automata-theory-course-with-jflap-40/desc.md)：经典自动机实验与教学工具。
3. [libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md](../libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md)：控制工程取向的 `C++` 状态机/离散事件系统库。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`finite automata / Mata / antichain inclusion / simulation reduction`
- 论文角色：finite-automata algorithm library / `C++` and Python infrastructure
- 归类理由：论文主体是高性能有限自动机算法库与配套基础设施建设，典型属于 automata tooling/infrastructure 条目。

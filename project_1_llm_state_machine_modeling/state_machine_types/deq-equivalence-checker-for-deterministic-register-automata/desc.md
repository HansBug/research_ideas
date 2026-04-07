# DEQ：确定性寄存器自动机等价检查器 / DEQ: Equivalence Checker for Deterministic Register Automata

## 基本信息

- 标题：DEQ: Equivalence Checker for Deterministic Register Automata
- 中文标题：DEQ：确定性寄存器自动机等价检查器
- 作者：Andrzej S. Murawski，Steven J. Ramsay，Nikos Tzevelekos
- 发表：*Automated Technology for Verification and Analysis*，`LNCS 11781`，pp. 350-356，2019
- DOI：`10.1007/978-3-030-31784-3_27`
- 链接：https://doi.org/10.1007/978-3-030-31784-3_27
- 形式主义：`deterministic register automata / DEQ / group-theoretic equivalence checking`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：deterministic register-automata equivalence checker / partial-permutation backend
- 工具/实现获取方式：原文明确给出源码入口 `https://github.com/stersay/deq`；实现使用 `Haskell`。
- 标准/格式获取方式：输入采用 `XML` 文件格式描述两台 `DRA`，输出是语言等价的 `YES/NO` 判定；不是行业交换标准。

## 简报

`DEQ` 补的是 `register automata` 生态里一个很重要但常被忽视的后端能力：不是“怎么学模型”，而是“学出来或写出来之后，怎么稳地做等价检查”。论文把 deterministic register automata 的语言等价问题落成命令行工具，并用 partial permutations、generating system 和 Schreier-Sims 群成员测试，避免把无限字母表模型粗暴展开成大得多的有限状态机。

- 形式主义定位：`DRA` 等价检查后端 / 基础设施，而不是新的 `RA` 子类。
- 构造方式简述：两台输入自动机先做 disjoint union，再把语言等价转成同一自动机内的 bisimilarity 检查。
- 基础设施与场景简述：依托 `XML` 输入、`Haskell` 实现、partial permutations、群成员测试与命令行判定，服务 `RA` 学习闭环、模型比对和 freshness-sensitive data-language checking。

```text
two DRA models -> disjoint union -> four-tuple exploration + generating system -> one-step bisimulation tests -> equivalence yes/no
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. deterministic register automata (`DRA`)；
2. local freshness 与 global freshness；
3. trace equivalence / bisimilarity；
4. four-tuples 与 generating system；
5. Schreier-Sims group membership backend。

### 核心抽象

论文不是重新系统定义 `RA` 元组，而是直接从转移标签语义切入。对任意状态 `$q$` 和标签 `$t$`，它考虑三类关键转移：

$$
q \xrightarrow{t,i} q', \qquad
q \xrightarrow{t,i\bullet} q', \qquad
q \xrightarrow{t,i\sim} q'
$$

上式中的符号逐项解释如下：

1. `$q \xrightarrow{t,i} q'$` 表示标签中的数据值等于当前寄存器 `$i$` 中保存的值。
2. `$q \xrightarrow{t,i\bullet} q'$` 表示标签中的数据值当前不在任何寄存器中，并在转移后写入寄存器 `$i$`。
3. `$q \xrightarrow{t,i\sim} q'$` 表示标签中的数据值是 globally fresh，即此前整个运行历史中都没出现过，并在转移后写入寄存器 `$i$`。

论文把等价检查问题压到 trace equality 上。对两台自动机 `$A_1, A_2$`，最核心的问题就是：

$$
L(A_1) = L(A_2)
$$

上式中的符号逐项解释如下：

1. `$L(A_1)$`、`$L(A_2)$` 分别是两台 `DRA` 接受的带数据 trace 语言。
2. 论文明确指出 deterministic 情况可判定，而 nondeterministic 情况不可判定。

算法内部不直接枚举所有具体配置，而是操纵四元组：

$$
u = (q_1, \sigma, q_2, h)
$$

上式中的符号逐项解释如下：

1. `$q_1, q_2$` 是两边当前待比较的状态。
2. `$\sigma$` 是 partial permutation，用来紧凑表示寄存器内容之间的匹配关系。
3. `$h$` 是与寄存器数量相关的辅助参数。
4. 论文把四元组作为 bisimulation-style search 的基本单位。

### 一个最小例子与通俗解释

论文给的“size-2 fresh stack”例子很适合解释本工具：

1. 第一台自动机允许把一个值 `d1` 压栈、弹出，再次压入同样的 `d1`。
2. 第二台自动机的 `push` 必须总是使用 globally fresh 值。
3. 因而 trace `(push,d1)(pop,d1)(push,d1)` 只被第一台自动机允许。
4. `DEQ` 就是在系统地证明或反驳这类 trace-language 等价。

通俗地说，`DEQ` 做的不是“把两个状态机逐状态文本比对”，而是“在无限多数据值里，只抓住真正有区别的寄存器对应关系”，这正是 partial permutation 和群论压缩的作用。

### 运行 / 接受 / 转移语义

论文的核心实现流程可保守整理为：

$$
u_0 \in \Delta,\qquad
u \notin \mathrm{Gen}(R) \Rightarrow
\text{1-step-test}(u)\ \land\ \Delta := \Delta \cup \mathrm{succ\mbox{-}set}(u)
$$

上式中的符号逐项解释如下：

1. `$u_0$` 是初始等价问题对应的四元组。
2. `$\Delta$` 是待检查四元组队列。
3. `$\mathrm{Gen}(R)$` 是当前 generating system 所生成的四元组集合。
4. `$\text{1-step-test}(u)$` 检查该四元组是否能通过一步 bisimulation attack。
5. `$\mathrm{succ\mbox{-}set}(u)$` 是后继四元组集合。

判定过程的关键语义边界是：

$$
\text{nondeterministic register automata} \Rightarrow \text{equivalence undecidable}
$$

这也是为什么 `DEQ` 明确只处理 deterministic 情形。

### 语义边界

1. 工具只处理 deterministic register automata。
2. 它非常强调 local freshness / global freshness，但不扩展到更强的数据运算。
3. 输入必须先整理成 `XML` 格式的 `DRA`。
4. 它是等价检查后端，不负责自动学习、自动抽取或自动生成模型。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 标签化寄存器转移 | `$q \xrightarrow{t,i} q',\ q \xrightarrow{t,i\bullet} q',\ q \xrightarrow{t,i\sim} q'$` | 区分寄存器命中、局部新值和全局新值。 |
| 语言等价 | `$L(A_1) = L(A_2)$` | `DEQ` 解决的核心问题。 |
| 搜索单位 | `$u = (q_1, \sigma, q_2, h)$` | partial-permutation 压缩后的基本检查对象。 |
| 生成系统 | `$u \notin \mathrm{Gen}(R)$` | 避免指数级重复展开的关键结构。 |
| 可判定性边界 | `$\text{DRA decidable},\ \text{NDRA undecidable}$` | 工具适用范围的硬边界。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接处理 deterministic register automata。 |
| 事件 / 触发 | 很强 | 标签由有限 tag 与无限数据值构成。 |
| 守卫 / 数据 | 很强 | 核心就是寄存器命中与 local/global freshness。 |
| 层次 | 不支持 | 不是层次状态机路线。 |
| 并发 / 同步 | 弱支持 | 主要是单自动机语言等价。 |
| 时间约束 | 不支持 | 不属于 timed family。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 data-language 工具。 |
| 可执行 / 可验证性 | 很强 | 命令行工具、XML 输入、明确的等价判定后端。 |

### 形式化问题与性质

1. `DEQ` 的代表性在于把 `DRA` 等价检查做成真正可用的后端，而不是停留在理论判定结论。
2. partial permutation + generating system 的组合，是它避免指数膨胀的核心。
3. 支持 global freshness 这一点对建模对象创建、引用分配等程序语义场景尤其重要。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 两台待比较的 deterministic register automata；
2. `XML` 模型文件；
3. 局部 / 全局 freshness 标注；
4. 命令行等价判定调用。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `XML` 形式的 `DRA`；
2. disjoint union automaton；
3. four-tuples；
4. partial permutations 与 generating system。

### 交换与互操作

1. `DEQ` 把语言等价问题转成 bisimulation-style search。
2. 它与 `RALib`、`LOIS`、`NLambda` 的主要互操作点在“都可作为 `RA` 生态中的验证或学习后端”。
3. 论文不强调通用行业格式，重点是一个能稳定消费 `DRA XML` 的工程后端。

## 配套基础设施

- 建模/编辑工具：工具本体是命令行 checker，而不是图形编辑器。
- 解析/交换/元模型支持：`XML` parser 基于 `xml-conduit`。
- 仿真/执行支持：不主打运行时执行，主打离线 equivalence checking。
- 验证/分析支持：one-step tests、successor generation、group membership tests、对比 `RALib/LOIS/NLambda`。
- 代码生成/转换支持：将双自动机等价问题转成单自动机中的 bisimilarity 问题。
- 标准化或社区生态：`Haskell` 实现，依赖 `HaskellForMaths` 提供 Schreier-Sims 群成员测试。

## 适用场景与需求前提

### 适用场景

适合 `RA` 学习后验验证、不同 data-language 模型对照、以及含 freshness 语义的接口或程序抽象模型的精确等价检查。

### 需求前提

1. 模型必须是 deterministic register automata。
2. 关键行为应能写成 tag + data 的 trace 语言。
3. 若涉及对象创建或新句柄分配，最好显式区分 local/global freshness。
4. 模型需要先落成工具支持的 `XML` 格式。

### 不适用或高成本场景

若模型含 nondeterminism、复杂算术理论或更弱的观测等价目标，`DEQ` 不是直接工具。

## 与相邻形式主义的关系

相对 [demonstrating-learning-of-register-automata/desc.md](../demonstrating-learning-of-register-automata/desc.md) 与 [combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md](../combining-black-box-and-white-box-techniques-for-learning-register-automata/desc.md)，那两篇更关心“如何学出 `RA`”，`DEQ` 关心“学出来后如何判等”；相对 [learning-register-automata-with-fresh-value-generation/desc.md](../learning-register-automata-with-fresh-value-generation/desc.md)，`Tomte` 处理 fresh-output learning，而 `DEQ` 提供 deterministic `RA` equivalence backend；相对 [the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md](../the-open-source-learnlib-a-framework-for-active-automata-learning/desc.md)，`LearnLib` 是通用学习框架，`DEQ` 则是更专门的 dataful-model equivalence checker。

## 与本研究的关系

### 对 Project 1 的价值

1. 对任何“LLM 生成状态机 -> 验证 -> 修复”闭环，等价检查都是高价值后端。
2. `DEQ` 说明带数据和 freshness 的状态机并不是只能做测试，也可以做更强的语义对比。
3. 它特别适合作为 `project_4` 修复后“新旧模型是否真正等价”的机械判断器。

### 作为目标形式主义还是中间表示

更适合作为 `RA` 生态中的验证与比较基础设施，而不是前端建模语言。

### 对需求到模型生成的启发

1. 若生成模型最终要进入自动修复闭环，就必须考虑“怎么判等”，不能只考虑“怎么生成”。
2. 对数据值和 freshness 的抽象应尽量保持与寄存器语义对齐，否则后端等价检查难以接入。
3. group-theoretic compression 提醒我们，数据型状态机的后端验证并不一定要暴力展开具体值。

## 重要的相关工作

1. `RALib`：当前最直接的 register-automata learning 生态对照对象。
2. `LOIS`、`NLambda`：论文明确对比的另外两套无限字母表框架。
3. [learning-register-automata-with-fresh-value-generation/desc.md](../learning-register-automata-with-fresh-value-generation/desc.md)：fresh-output 学习路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`deterministic register automata / DEQ / group-theoretic equivalence checking`
- 论文角色：deterministic register-automata equivalence checker / partial-permutation backend
- 归类理由：论文主体是 `DRA` 等价检查工具与其底层搜索/群论实现，最适合作为 `register-automata` 生态中的验证基础设施条目保留。

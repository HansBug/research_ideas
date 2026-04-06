# GOAL 扩展版：面向 Omega 自动机与时序逻辑的研究工具 / GOAL Extended: Towards a Research Tool for Omega Automata and Temporal Logic

## 基本信息

- 标题：GOAL Extended: Towards a Research Tool for Omega Automata and Temporal Logic
- 中文标题：GOAL 扩展版：面向 Omega 自动机与时序逻辑的研究工具
- 作者：Yih-Kuen Tsay，Yu-Fang Chen，Ming-Hsien Tsai，Wen-Chin Chan，Chi-Jian Luo
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2008)*，`LNCS 4963`，pp. 346-350，2008
- DOI：`10.1007/978-3-540-78800-3_26`
- 链接：https://doi.org/10.1007/978-3-540-78800-3_26
- 形式主义：`omega-automata / Büchi automata / temporal logic / GOAL`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：graphical and command-line omega-automata / temporal-logic research toolchain
- 工具/实现获取方式：原文明确给出 `http://goal.im.ntu.edu.tw` 作为工具入口；当前仍可从项目站获取相关说明与论文列表。
- 标准/格式获取方式：原文强调 `GOAL File Format (GFF)`、图形界面和 command-line mode；它不是外部中立标准，而是围绕 `omega` 自动机与时序逻辑实验的工具承载格式。

## 简报

这篇论文的重点，是把 `GOAL` 从“可交互操作 Büchi 自动机的教学工具”推进成“研究人员可以批量跑翻译、补全、补余、等价测试和统计实验的工具链”。它最关键的增量不是单个新算法，而是把 translation、complementation、simplification、command-line mode 和 `GFF` 真正接成一个可重复实验环境。

- 形式主义定位：`omega` 自动机与时序逻辑的操作基础设施，而不是新的自动机理论本体。
- 构造方式简述：输入 `QPTL/PTL/LTL` 公式或外部自动机，调用多种 translation/complementation/simplification 算法，再用 `GFF`、CLI 与图形界面做比较、交叉检查与统计实验。
- 基础设施与场景简述：依托 `Büchi` 自动机、`QPTL/PTL/LTL` 翻译、language inclusion / equivalence、`GFF` XML、command-line mode 和随机公式/自动机生成器，服务 automata-theoretic model checking、算法对比和教学研究。

```text
PTL / LTL / QPTL formula or automaton -> GOAL translators / complementers / simplifiers -> GFF / CLI / GUI -> equivalence check / experiment / model-checking support
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Büchi` 与更一般的 `omega` 自动机。
2. `QPTL / PTL / LTL` 公式。
3. translation algorithms。
4. complementation / simplification algorithms。
5. `GFF`、command-line mode 与实验辅助函数。

### 核心抽象

对公式翻译，可保守写成：

$$
f \mapsto A_f
$$

上式中的符号逐项解释如下：

1. `f` 是时序逻辑公式。
2. `A_f` 是与 `f` 等价的 `Büchi` 或 generalized `Büchi` 自动机。
3. 论文的一个重点，就是同一公式可以被多种 translation 算法映射到不同但语言等价的自动机。

等价检查的核心语义可整理为：

$$
L(A) = L(B) \iff L(A) \subseteq L(B) \land L(B) \subseteq L(A)
$$

上式中的符号逐项解释如下：

1. `A,B` 是两个 `omega` 自动机。
2. `L(A),L(B)` 是它们接受的 `omega` 语言。
3. `GOAL` 通过 complementation、intersection 与 emptiness 等手段实现包含和等价检查。

论文给出的“翻译算法正确性检查”流程，可保守整理为：

$$
L(A_{\neg f} \cap B) = \emptyset \land L(A_f \cap \overline{B}) = \emptyset
$$

上式中的符号逐项解释如下：

1. `A_f` 是 reference algorithm 产生的自动机。
2. `A_{\neg f}` 是公式否定的参考自动机。
3. `B` 是被测 translation algorithm 产出的自动机。
4. 若两个交都为空，则说明 `B` 与参考答案语言等价。

### 一个最小例子与通俗解释

一个最小直觉例子，是输入一个 `LTL` 公式，例如“总会再次看到 `p`”，然后让工具输出对应的 `Büchi` 自动机，再与另一种翻译算法生成的结果做等价检查。

通俗地说，`GOAL` 像一个“omega 自动机实验台”。你可以把它当作翻译器、补全器、补余器、格式转换器和交叉验算器，而不只是一个能画图的自动机编辑器。

### 运行 / 接受 / 转移语义

对 `Büchi` 接受，可保守写成：

$$
\rho \in L(A) \iff \mathrm{Inf}(\rho) \cap F \ne \emptyset
$$

上式中的符号逐项解释如下：

1. `\rho` 是自动机运行轨迹。
2. `L(A)` 是自动机接受的 `omega` 语言。
3. `F` 是接受状态集合。
4. `\mathrm{Inf}(\rho)` 表示在轨迹中被无限次访问的状态集合。
5. 论文的 translation / complementation / equivalence 功能都围绕这一类 `omega` 语义对象展开。

### 语义边界

1. `GOAL` 主体处理的是 `omega` 自动机与时序逻辑，不是完整系统前端建模。
2. 它适合操纵 formula / automaton objects，本身不负责状态空间生成。
3. 论文特别强调算法比较与 correctness cross-check，而不是单个最佳算法。
4. richer data、时钟和混成动力学都不在本文主线。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 翻译目标 | `$f \mapsto A_f$` | 时序逻辑到自动机的基本桥接。 |
| 语言等价 | `$L(A)=L(B)$` | 等价测试是 GOAL 的核心操作之一。 |
| 正确性检查 | `$L(A_{\neg f}\cap B)=\emptyset \land L(A_f \cap \overline{B})=\emptyset$` | 论文明确给出用 GOAL 交叉校验翻译算法的流程。 |
| Büchi 接受 | `$\rho \in L(A) \iff \mathrm{Inf}(\rho)\cap F \ne \emptyset$` | `omega` 自动机的基本接受语义。 |
| 承载格式 | `$GFF$` | 工具有自己覆盖 `omega` 自动机的 XML 文件格式。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强 | 操作对象就是 `omega` 自动机。 |
| 事件 / 触发 | 中等支持 | 命题标签与公式原子是核心，但不是显式控制事件语言。 |
| 守卫 / 数据 | 弱 | 重点不在 rich data guards。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 不支持 | 不生成系统并发状态空间。 |
| 时间约束 | 弱支持 | 处理 temporal logic，但不是 clocks/timed automata。 |
| 连续动态 / 随机性 | 不支持 | 不在对象范围内。 |
| 可执行 / 可验证性 | 很强 | translation、complementation、equivalence、statistics 都能直接跑。 |

### 形式化问题与性质

1. `GOAL` 的真正价值在于把多算法实验、交叉验证和格式转换统一到同一工作台。
2. `GFF` 和 command-line mode 让它从 GUI 工具升级成 research pipeline。
3. 论文明确把 correctness checking、random generation 和 statistics collection 作为一等任务。

## 构造方式与承载格式

### 建模入口

原文给出的主要入口有：

1. `QPTL`。
2. `PTL / LTL`。
3. 外部自动机工具输出。
4. 随机生成的 automata 与 temporal formulae。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Büchi` / generalized `Büchi` 自动机。
2. `GFF` XML。
3. command-line mode。
4. 图形交互界面。

### 交换与互操作

互操作重点包括：

1. 外部工具输出可转成 `GFF`。
2. command-line mode 允许 shell script 调用 GOAL 功能。
3. 工具被设计成可为其他 automata-theoretic model checkers 提供辅助。

## 配套基础设施

- 建模/编辑工具：图形交互界面与命令行模式并存。
- 解析/交换/元模型支持：`GFF`、外部格式转换、统计输出。
- 仿真/执行支持：主体不是系统执行器，而是 automata / logic 操作平台。
- 验证/分析支持：translation、complementation、simplification、equivalence / containment checking。
- 代码生成/转换支持：时序逻辑到自动机、外部自动机格式到 `GFF` 的转换。
- 标准化或社区生态：`GOAL` 项目站、相关 translation algorithms、外部 `MoDeLLa / LTL2Buchi` 工具共同构成生态。

## 适用场景与需求前提

### 适用场景

适合 `LTL/PTL/QPTL` 翻译算法研究、`omega` 自动机补余/化简、等价检查、automata-theoretic model checking 辅助与教学实验。

### 需求前提

1. 问题对象必须能落成 `omega` 自动机或时序逻辑公式。
2. 团队接受工具链式而非系统前端式工作流。
3. 关注点是算法比较、互操作和 correctness cross-check。
4. 若要验证真实系统，还需要外部状态空间前端。

### 不适用或高成本场景

如果目标是直接从控制需求生成可执行状态机或处理 rich data/timing semantics，`GOAL` 太偏后端理论工具。

## 与相邻形式主义的关系

相对 [spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md](../spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md)，`Spot` 更偏库化与 `HOA` toolchain，而 `GOAL` 更强调图形交互、交叉验证和研究实验；相对 [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)，`HOA` 是交换格式标准，而 `GOAL` 用的是自己的 `GFF` 并承担操作者角色；相对 [the-model-checker-spin/desc.md](../the-model-checker-spin/desc.md)，`SPIN` 是系统验证器，而 `GOAL` 更像 `omega` 自动机实验后端与辅助平台。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提醒我们：性质侧工具链本身也需要像模型侧工具链一样系统建设。
2. 若后续要把需求中的时序性质自动翻成 `omega` 自动机并做交叉验证，`GOAL` 这条路线很有参考价值。
3. `GFF`、CLI 和 cross-check workflow 也非常适合做 LLM 生成结果的自动化复核。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它显然是性质处理后端，而不是目标状态机语言。

### 对需求到模型生成的启发

1. 生成的性质与生成的模型都应当进入同样可脚本化的后端环境。
2. 对同一公式保留多种翻译算法，有利于做一致性校验。
3. GUI 工具只是入口之一，真正关键的是可批处理的研究接口。

## 重要的相关工作

1. [spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md](../spot-20-a-framework-for-ltl-and-omega-automata-manipulation/desc.md)：更现代的 `LTL/omega` 自动机库化路线。
2. [the-hanoi-omega-automata-format/desc.md](../the-hanoi-omega-automata-format/desc.md)：`omega` 自动机交换格式条目。
3. [the-model-checker-spin/desc.md](../the-model-checker-spin/desc.md)：`GOAL` 可作为这类 automata-theoretic model checker 的辅助工具。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：📝 序列 / 语言对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`omega-automata / Büchi automata / temporal logic / GOAL`
- 论文角色：graphical and command-line omega-automata / temporal-logic research toolchain
- 核心功能：统一 `omega` 自动机翻译、补余、化简、等价检查与实验脚本化
- 关键特性：多 translation algorithms、complementation、simplification、CLI、`GFF`
- 构造方式：temporal logic / automata inputs -> GOAL algorithms -> `GFF` / GUI / CLI outputs
- 基础设施：`GFF`、图形界面、command-line mode、random generators、统计与 cross-check workflow
- 适用场景：`omega` 自动机研究、时序逻辑翻译比较、automata-theoretic verification 辅助
- 需求前提：对象需可表成 `omega` 自动机或时序逻辑，且团队接受后端实验工具流
- 状态：🟢

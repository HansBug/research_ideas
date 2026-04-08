# CLTSA：支持计数 Fluent 的标号迁移系统分析器 / CLTSA: Labelled Transition System Analyser with Counting Fluent Support

## 基本信息

- 标题：CLTSA: Labelled Transition System Analyser with Counting Fluent Support
- 中文标题：CLTSA：支持计数 Fluent 的标号迁移系统分析器
- 作者：Germán Regis，Renzo Degiovanni，Nicolas D'Ippolito，Nazareno Aguirre
- 发表：*Proceedings of the 2017 11th Joint Meeting on Foundations of Software Engineering*，pp. 979-983，2017
- DOI：`10.1145/3106237.3122828`
- 链接：https://doi.org/10.1145/3106237.3122828
- 形式主义：`LTS / FSP / FLTL / CFLTL / CLTSA`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`LTSA` extension for counting-fluent temporal logic model checking
- 工具/实现获取方式：原文明确给出工具主页 `http://dc.exa.unrc.edu.ar/tools/cltsa`，并说明 CLTSA 直接扩展自 `LTSA`。
- 标准/格式获取方式：主承载是 `FSP` 超集、`CFLTL` 性质语法、counting fluent declarations 与 strict / non-strict limit declarations；它不是独立交换标准。

## 简报

这篇论文补的是事件驱动 `LTS/FSP` 世界里一个很实用但常被忽略的能力缺口：普通 fluent 只能表达布尔状态，而很多控制和软件约束其实关心“某类事件发生了多少次”。`CLTSA` 的做法不是把计数逻辑塞进外部脚本，而是直接扩展 `LTSA`，让 `FSP` 模型、`CFLTL` 性质、counting-expression automata 和原有的 safety / liveness model checking 工作流保持在同一语义链上。

- 形式主义定位：`LTSA/FSP` 上的 counting-fluent model-checking 基础设施，而不是新的状态机家族。
- 构造方式简述：`FSP` 模型 + counting fluent / limit declarations + `CFLTL` 公式，经过 fluent automata 与 counting automata 构造后，与系统模型做同步乘积并检查空性或 `SCC`。
- 基础设施与场景简述：依托 `LTSA`、`FSP`、`FLTL/CFLTL`、counterexample trace、animator 与 counting report，服务 reactive software、事件驱动控制逻辑和并发行为约束。

```text
FSP model + CFLTL property -> fluent automata / counting automata -> synchronous product -> safety / liveness check -> valid / invalid / inconclusive
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `FSP` 描述的系统 `LTS`。
2. propositional fluent 与 counting fluent。
3. `CFLTL` counting expressions。
4. counting automata 与 synchronous-product model checking。
5. strict / non-strict limits 与 `inconclusive` verdict。

### 核心抽象

论文沿用了 `LTSA` 的 fluent 语义，可保守写成：

$$
Fl = \langle I, T, B \rangle
$$

上式中的符号逐项解释如下：

1. `$I$` 是 activating events 集合。
2. `$T$` 是 deactivating events 集合。
3. `$B$` 是初始布尔值。
4. 这对应原始 `FLTL` 里的 propositional fluent。

对应的 counting fluent 则可整理为：

$$
CF = \langle I, D, R, v_0 \rangle
$$

上式中的符号逐项解释如下：

1. `$I$` 是 incrementing events 集合。
2. `$D$` 是 decrementing events 集合。
3. `$R$` 是 reset events 集合。
4. `$v_0$` 是初始整数值。

其逐步更新规则可保守写成：

$$
val_{k+1}(CF) =
\begin{cases}
val_k(CF) + 1, & e_k \in I \\
val_k(CF) - 1, & e_k \in D \\
0, & e_k \in R \\
val_k(CF), & \text{otherwise}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `$e_k$` 是第 `$k$` 步发生的事件。
2. `$val_k(CF)$` 是第 `$k$` 步时 counting fluent 的值。
3. 这正对应论文对 increment / decrement / reset 的解释。

论文明确说明模型检查核心仍是同步乘积空性检查，可保守写成：

$$
L(M \parallel A_{\neg \varphi}) = \emptyset
$$

上式中的符号逐项解释如下：

1. `$M$` 是系统 `LTS` 模型。
2. `$A_{\neg \varphi}$` 是由 fluent automata 与 counting automata 构成的性质自动机。
3. `\parallel` 表示同步乘积。
4. 若语言为空，则性质成立。

### 一个最小例子与通俗解释

论文给了一个非常直接的最小例子：

$$
F = \langle \{a\}, \{b\}, \{c\}, 0 \rangle
$$

并检查 counting expression：

$$
F \le 1
$$

通俗理解如下：

1. 事件 `a` 出现一次，计数加一。
2. 事件 `b` 出现一次，计数减一。
3. 事件 `c` 出现一次，计数清零。
4. `CLTSA` 会为 `F <= 1` 自动生成一台 counting automaton，再与系统同步。

论文里的 bridge 案例更接近真实控制语境：`CARS_ON_BRIDGE` 统计桥上的车数，再检查 `[](CARS_ON_BRIDGE <= C)` 是否一直成立。也就是说，它能把“桥上最多允许 `C` 辆车”这类计数安全约束直接写进性质，而不必手工重构系统状态机。

### 运行 / 接受 / 转移语义

论文明确说明 `LTSA` 的 checking 过程可视为对同步乘积的错误状态搜索或 `SCC` 搜索。保守写成：

$$
\mathrm{Check}_{safe}(M, \varphi) =
\begin{cases}
\mathrm{valid}, & \nexists \pi : \pi \leadsto ERROR \\
\mathrm{invalid}, & \exists \pi : \pi \leadsto ERROR \land \pi \text{ has no overflow} \\
\mathrm{inconclusive}, & \text{otherwise}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `$M$` 是系统模型。
2. `$\varphi$` 是 safety property。
3. `$\pi \leadsto ERROR$` 表示存在到 `ERROR` 的有限反例轨迹。
4. overflow 指 non-strict bounds 下探索到溢出状态。

liveness 情况则可保守写成：

$$
\mathrm{Check}_{live}(M, \varphi) =
\begin{cases}
\mathrm{valid}, & \nexists \mathrm{SCC}_{bad} \\
\mathrm{invalid}, & \exists \mathrm{SCC}_{bad} \land \mathrm{SCC}_{bad} \text{ has no overflow} \\
\mathrm{inconclusive}, & \text{otherwise}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `$\mathrm{SCC}_{bad}$` 是不满足 liveness 要求的强连通分量。
2. 若坏 `SCC` 不涉及 overflow，则可报告真正反例。
3. 若只探索到 overflow 痕迹，则结果只能是 `inconclusive`。

### 语义边界

1. `CLTSA` 依赖 `LTSA/FSP` 的事件驱动建模框架，不是富数据程序分析器。
2. 计数值本身可能导致无限状态，因此必须配合上下界 limits 才能落成有限模型。
3. 核心优势在事件计数，而不是时间约束或连续动态。
4. 它扩展的是性质语言与验证基础设施，不是重新定义 `LTS` 本体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| propositional fluent | `$Fl=\langle I,T,B \rangle$` | `FLTL` 原有 fluent 语义。 |
| counting fluent | `$CF=\langle I,D,R,v_0 \rangle$` | `CLTSA` 新增的计数对象。 |
| 计数更新 | `$val_{k+1}(CF)$` 的分段式 | increment / decrement / reset 语义核心。 |
| 乘积检查 | `$L(M \parallel A_{\neg \varphi}) = \emptyset$` | `LTSA` 风格 model checking 骨架。 |
| verdict 三值化 | `valid / invalid / inconclusive` | strict 与 non-strict limits 下最关键的结果口径。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心仍是 `FSP/LTS` 状态空间。 |
| 事件 / 触发 | 很强 | counting fluent 直接以事件集合定义。 |
| 守卫 / 数据 | 中等支持 | 支持整数算术表达式，但不面向一般富数据程序。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 很强 | 沿用 `LTSA` 的同步乘积和并发分析能力。 |
| 时间约束 | 不支持 | 核心是计数，不是时钟。 |
| 连续动态 / 随机性 | 不支持 | 不在本文对象范围内。 |
| 可执行 / 可验证性 | 很强 | editor、animator、counterexample 与 fluents report 已完整工程化。 |

### 形式化问题与性质

1. `CLTSA` 的关键增量不是新模型本体，而是把 counting expressions 自动编译成 automata。
2. `inconclusive` 结果口径很重要，它避免在 bounds 不够大时给出假“证明”。
3. 相比旧 prototype 的 instrumentation 路线，自动机表示让复杂 liveness 性质更可控。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `FSP` 系统模型。
2. counting fluent declarations。
3. limit declarations 与 `apply`。
4. `CFLTL` 性质公式。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `FSP` 超集文本。
2. fluent automata。
3. counting automata。
4. enhanced trace report 与 animator fluents view。

### 交换与互操作

互操作重点仍在 `LTSA` 生态内部：

1. `CLTSA` 是对 `LTSA` lexer、parser、model checking 和 animator 的直接扩展。
2. 系统模型继续使用 `FSP`。
3. 性质层从 `FLTL` 扩到 `CFLTL`，但工作流仍兼容原有 `LTSA` 分析管线。

## 配套基础设施

- 建模/编辑工具：`CLTSA` editor 直接支持 counting fluent 和 limits 语法。
- 解析/交换/元模型支持：`FSP` 超集、`CFLTL` 公式、strict / non-strict limits。
- 仿真/执行支持：animator 可逐步显示 propositional fluents、counting fluents 和 counting expressions 的值。
- 验证/分析支持：safety / liveness checking、counterexample trace、overflow-aware `inconclusive` 判断。
- 代码生成/转换支持：主要是从 counting expressions 自动生成 counting automata，而不是生成控制代码。
- 标准化或社区生态：依托 `LTSA`、`FSP`、`FLTL` 系列工具链。

## 适用场景与需求前提

### 适用场景

适合 reactive software、事件驱动控制逻辑、并发行为分析，尤其适合需要表达“某类事件不能超过多少次”“某资源占用计数始终受限”的场景。

### 需求前提

1. 系统需能落成 `FSP/LTS` 模型。
2. 关键约束应主要依赖事件计数，而非连续时间或复杂数据结构。
3. 计数上界 / 下界需能给出合理有限近似。
4. 团队接受 `valid / invalid / inconclusive` 三值结果。

### 不适用或高成本场景

如果核心问题在 dense time、连续动力学或高维数据更新，`CLTSA` 就不是最自然的目标后端。

## 与相邻形式主义的关系

相对 [graphical-animation-of-behavior-models/desc.md](../graphical-animation-of-behavior-models/desc.md)，两者都挂在 `LTSA` 生态上，但后者偏解释执行和动画桥，`CLTSA` 偏性质语言增强；相对 [ltsa-ws-a-tool-for-model-based-verification-of-web-service-compositions-and-choreography/desc.md](../ltsa-ws-a-tool-for-model-based-verification-of-web-service-compositions-and-choreography/desc.md)，`LTSA-WS` 把 `MSC/BPEL` 编译到 `FSP`，而 `CLTSA` 是在 `FSP` 层继续增强验证能力；相对 [mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md](../mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md)，`MTSA` 走 modal / controller synthesis 路线，`CLTSA` 则聚焦 counting-fluent verification。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明状态机验证侧经常需要额外的“派生性质对象”，例如 counting fluents，而不只是裸 `LTL`。
2. 对后续“验证场景与待验证性质生成”非常有启发，因为计数约束在控制需求中很常见。
3. 也提醒我们：若需求里本来就有资源 / 事件次数限制，生成模型时不一定非要把它们都内化成额外状态。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，`CLTSA/CFLTL` 更像验证侧性质与工具后端，而不是最终交付给工程师的控制状态机语言。

### 对需求到模型生成的启发

1. 需求中的“最多 / 至少 / 不超过 / 计数复位”可优先抽成 counting properties。
2. 验证工具若能保持 `inconclusive` 这种诚实口径，比强行给出真假更有价值。
3. 计数型性质生成可以独立于主状态机结构进行，不必都折叠进状态爆炸里。

## 重要的相关工作

1. [ltsa-ws-a-tool-for-model-based-verification-of-web-service-compositions-and-choreography/desc.md](../ltsa-ws-a-tool-for-model-based-verification-of-web-service-compositions-and-choreography/desc.md)：`LTSA` 生态下的 `MSC/BPEL` 验证桥。
2. [graphical-animation-of-behavior-models/desc.md](../graphical-animation-of-behavior-models/desc.md)：`LTSA + SceneBeans` 动画解释链。
3. [mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md](../mtsa-eclipse-support-for-modal-transition-systems-construction-analysis-and-elaboration/desc.md)：相邻的 Eclipse/LTS 工具线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`LTS / FSP / FLTL / CFLTL / CLTSA`
- 论文角色：`LTSA` extension for counting-fluent temporal logic model checking
- 核心功能：把 counting fluent 定义、counting expressions、automata 构造和三值 model checking 接到 `LTSA`
- 关键特性：`FSP` 超集、`CFLTL`、counting automata、strict/non-strict limits、animator fluents report
- 构造方式：`FSP + CFLTL -> fluent/counting automata -> synchronous product -> safety/liveness check`
- 基础设施：`CLTSA`、`LTSA`、editor、animator、trace report、tool homepage
- 适用场景：事件计数约束验证、资源占用上界检查、reactive software 行为分析
- 需求前提：系统需落成 `FSP/LTS`，关键性质主要依赖事件计数且可给有限 bounds
- 状态：🟢

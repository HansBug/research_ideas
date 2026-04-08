# 验证事件驱动软件的一种实用方法 / A Practical Method for Verifying Event-Driven Software

## 基本信息

- 标题：A Practical Method for Verifying Event-Driven Software
- 中文标题：验证事件驱动软件的一种实用方法
- 作者：Gerard J. Holzmann，Margaret H. Smith
- 发表：*Proceedings of the 21st International Conference on Software Engineering*，pp. 597-607，1999
- DOI：`10.1145/302405.302710`
- 链接：https://doi.org/10.1145/302405.302710
- 形式主义：`event-driven state machines / @-format / SPIN extraction`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：源码抽取式 reactive-state-machine 验证方法与 test-harness 结构
- 工具/实现获取方式：原文明确说明作者实现了 `pry` 和 `catch` 两个程序，把 `@-format` 源码抽成 `SPIN` 验证模型；提取文本未见稳定公开仓库地址。
- 标准/格式获取方式：承载方式是带 `@` 扩展的 `ANSI C`、中间 annotated state-machine format、statement map、test drivers 和 `SPIN` property models；无中立行业交换标准。

## 简报

这篇论文的关键贡献不是提出一个新状态机理论，而是把“现实中的事件驱动 `C` 代码”稳定抽成状态机模型，并围绕它构造一个可重复执行的 verification harness。其核心思想是：代码中的控制状态已经隐含在 `@-format` 标记里，模型抽取器只需要识别这些状态和事件响应，再用 map、driver 和 properties 组成测试夹具，就可以把实现拉进 `SPIN`。

- 形式主义定位：事件驱动源码到状态机验证模型的抽取与 harness 化方法。
- 构造方式简述：`@-format` 的 `ANSI C` 先由 `pry` 解析成中间状态机表示，再由 `catch` 结合 map、drivers 和 properties 生成 `SPIN` 模型。
- 基础设施与场景简述：依托 `pry/catch`、`SPIN`、statement map、test driver 和 LTL / test automata，服务电话呼叫处理等 event-driven reactive software 的实现级验证。

```text
事件驱动 C 源码 -> @-format 控制状态 -> pry/catch 抽取状态机 -> test harness -> SPIN 验证与源码级错误回映
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. `@-format` 源码；
2. mechanically extracted state machine model；
3. statement map；
4. test drivers；
5. properties；
6. `SPIN` model checker；
7. source-level error trace reconstruction。

### 核心抽象

原文把 verification harness 明确拆成三部分，可直接写成：

$$
H = (Map, Driver, Props)
$$

上式中的符号逐项解释如下：

1. `$Map$` 是 statement map，用来定义哪些语句进入模型、如何抽象。
2. `$Driver$` 是一个或一组 test drivers，用于给系统喂输入并消费输出。
3. `$Props$` 是待验证性质集合。

抽取出来的 event-driven state machine 可保守整理为：

$$
M = (S, E, \delta, s_0)
$$

上式中的符号逐项解释如下：

1. `$S$` 是由 `@` 标注控制点识别出来的控制状态集合。
2. `$E$` 是事件集合。
3. `$\delta$` 是对事件和相关抽象语句的响应关系。
4. `$s_0$` 是初始控制状态。

论文后半部分明确用 automata-theoretic 方式描述性质检查，可写成：

$$
L(M) \cap L(\neg \varphi) = \varnothing
$$

上式中的符号逐项解释如下：

1. `$L(M)$` 是抽取出的系统模型的可行执行语言。
2. `$\varphi$` 是一个 correctness property。
3. `$L(\neg \varphi)$` 是违反该性质的执行语言。
4. 交集为空时，说明模型满足该性质。

### 一个最小例子与通俗解释

论文给出的最直观例子是 `@-format` 的 sender routine：

1. `@S0:` 标记一个控制状态。
2. 预处理后它会展开成等待点 `B_S0` 和恢复点 `A_S0`。
3. 每次事件到来时，jump table 会根据 `state` 变量跳回对应恢复点。
4. 抽取器据此恢复出一个纯状态机模型，再交给 `SPIN`。

通俗地说，这个方法像“从事件驱动 `C` 代码里把埋着的状态机骨架挖出来”。程序员仍然写 `C`，但通过很薄的一层 `@` 标记，验证工具就能认出哪些地方是状态、哪些地方是事件响应、哪些地方该由环境驱动。

### 运行 / 接受 / 转移语义

`@-format` 的核心状态恢复语义可保守写成：

$$
\mathrm{dispatch}(state) = A_s
$$

上式中的符号逐项解释如下：

1. `$state$` 是当前保存的控制状态编号。
2. `$A_s$` 是该控制状态对应的恢复入口标签。
3. 这对应论文中 jump table 对 `state` 的 `switch` 恢复逻辑。

test harness 驱动下的验证问题可写成：

$$
\mathrm{Check}(M, H, \varphi) \equiv L(M_H) \cap L(\neg \varphi) = \varnothing
$$

上式中的符号逐项解释如下：

1. `$M_H$` 是系统模型 `$M$` 在 harness `$H$` 包围下的闭合模型。
2. `$\varphi$` 是一个被 formalize 到 `LTL` 或 test automaton 的性质。
3. 若交集非空，模型检查器会返回违反性质的错误执行序列。

### 语义边界

1. 该方法针对 event-driven / reactive `C` 软件，不是任意程序分析框架。
2. 抽取精度取决于 statement map 和 driver 的抽象选择。
3. 其优势是“围绕实现做形式化验证”，不是给出独立新 DSL。
4. 时间语义、连续行为和复杂对象结构都不是论文主线。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| harness 骨架 | `$H = (Map, Driver, Props)$` | 验证夹具由 map、driver、properties 三部分组成。 |
| 抽取模型 | `$M = (S, E, \delta, s_0)$` | `@-format` 源码可被还原成纯状态机模型。 |
| 状态恢复 | `$\mathrm{dispatch}(state) = A_s$` | jump table 根据保存的 state 恢复控制点。 |
| 自动机式验证 | `$L(M) \cap L(\neg \varphi) = \varnothing$` | 满足性质等价于系统语言与违性质语言无交。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `@` 标记直接定义控制状态。 |
| 事件 / 触发 | 很强 | event-driven routine 是核心对象。 |
| 守卫 / 数据 | 强 | statement map 可选择保留或抽象表达式与数据操作。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 部分支持 | 可用多个 test drivers 和进程做环境交互，但主骨架仍是事件驱动状态机。 |
| 时间约束 | 不支持 | 论文不处理 dense-time。 |
| 连续动态 / 随机性 | 不支持 | 纯离散 reactive software。 |
| 可执行 / 可验证性 | 很强 | 直接面向真实源码，并能返回源码级 error traces。 |

### 形式化问题与性质

1. 把验证模型的维护工作从“手写模型”变成“维护抽取规则和 test harness”。
2. statement map 允许从纯控制状态模型逐步向更精细的数据抽象收敛。
3. 论文清楚展示了 property、driver 和源码之间的闭环关系。

## 构造方式与承载格式

### 建模入口

1. 用带 `@` 扩展的 `ANSI C` 编写 event-driven code。
2. `pry` 解析源码并输出中间 annotated state-machine format。
3. `catch` 读取该中间格式和 statement map，生成 `SPIN` 模型。
4. 再由 test drivers 与 properties 组成完整 test harness。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `@-format` 源码；
2. annotated intermediate state-machine format；
3. text-based statement map；
4. `SPIN` 模型和 `LTL` / test automata。

### 交换与互操作

这条路线的互操作点很明确：

1. 源码和抽取模型通过 statement map 对接。
2. 环境通过 test drivers 对接。
3. 性质通过 `LTL` 或 test automata 对接。
4. 模型检查结果又能回映成 source-level traces。

## 配套基础设施

- 建模/编辑工具：普通 `C` 编辑器即可，关键是支持 `@-format`。
- 解析/交换/元模型支持：`pry` 和 `catch` 形成源代码到验证模型的转换链。
- 仿真/执行支持：主线不是仿真运行时，而是基于源码的模型抽取与错误回映。
- 验证/分析支持：`SPIN` 负责 deadlock、unspecified reception、safety/liveness 和 test-automata checks。
- 代码生成/转换支持：不主打代码生成，重点是源码到模型的提取。
- 标准化或社区生态：方法建立在 `SPIN` 和 event-driven `C` 软件工程实践上，不是行业标准格式。

## 适用场景与需求前提

### 适用场景

适合通信协议、device drivers、scheduler、call processing 和其他以消息/事件驱动的 reactive software。

### 需求前提

1. 源码能用 `@-format` 或相近方式显式标注控制状态。
2. 关键行为主要是事件响应，而不是复杂数值算法。
3. 团队愿意维护 statement map、test drivers 和 properties 数据库。
4. 需要的是实现级 verification，而不只是设计级建模。

### 不适用或高成本场景

如果系统主要是面向对象层次交互、dense-time 约束、连续控制或 heavily concurrent shared-state 程序，这条方法会变得不够自然。

## 与相邻形式主义的关系

相对 `P` 这类新语言条目，本文不是新语言本体，而是现有源码的抽取式验证路线；相对 `Spec Explorer`、`Modbat`，它更靠近源码和实现细节；相对 `TorX/JTorX/TESTOR` 这类 `IOLTS/ioco` testing 工具，它的输入不是显式规格模型，而是 event-driven `C` 实现本身。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“需求到状态机自动建模”也可以反过来做成“实现到状态机验证模型自动抽取”。
2. statement map、drivers 和 properties 的三分法，非常接近后续 verification profile 的结构化入口。
3. 对 LLM 场景来说，这类方法适合做“先抽实现骨架，再回推规格缺失”的闭环。

### 作为目标形式主义还是中间表示

更适合作为实现级验证中间链路，而不是最终状态机本体。

### 对闭环生成-验证-修复的启发

它提示我们：修复反馈最好能回映到源码和控制状态，而不只是停留在验证器内部的抽象状态上。

## 重要的相关工作

- `SPIN`
- `Spec Explorer`
- `Modbat`
- `TorX`

## 文献分类总结

- 形式主义：`event-driven state machines / @-format / SPIN extraction`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 关键词：源码抽取、事件驱动软件、`@-format`、test harness、`SPIN`

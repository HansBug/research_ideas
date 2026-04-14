# Modbat：面向事件驱动系统的模型驱动 API 测试器 / Modbat: A Model-Based API Tester for Event-Driven Systems

## 基本信息

- 标题：Modbat: A Model-Based API Tester for Event-Driven Systems
- 中文标题：Modbat：面向事件驱动系统的模型驱动 API 测试器
- 作者：Cyrille Valentin Artho，Armin Biere，Masami Hagiya，Eric Platon，Martina Seidl，Yoshinori Tanabe，Mitsuharu Yamamoto
- 发表：*Hardware and Software: Verification and Testing*，pp. 112-128，2013
- DOI：`10.1007/978-3-319-03077-7_8`
- 链接：https://doi.org/10.1007/978-3-319-03077-7_8
- 形式主义：`FSM / Modbat / Scala embedded DSL / API testing`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 论文角色：event-driven API model-based testing tool
- 工具/实现获取方式：手头 PDF 为 postprint/accepted-version 文本，原文摘录未给出公开仓库或下载 URL；论文明确说明工具名为 `Modbat`，由 Scala 编写。
- 标准/格式获取方式：原文说明模型用 Scala-based embedded DSL 表达，SUT 只要能编译到 Java bytecode 即可测试；它不是独立交换标准。

## 简报

这篇论文介绍 `Modbat`：一个面向程序库、框架和事件驱动系统 API 的模型驱动测试器。用户用 Scala embedded DSL 写有限状态机模型，`Modbat` 随机探索模型，并在探索过程中同步调用 SUT API；每条从初始到终止模型状态的转移序列构成一次 test run，若性质被违反则输出可重放的错误轨迹。

- 形式主义定位：FSM-based API testing route，而不是新的状态机本体。
- 构造方式简述：测试者用 Scala DSL 写形如 `"init" -> "active" := { ... }` 的状态转移和动作代码，再将模型编译并交给 `Modbat` 随机探索。
- 基础设施与场景简述：依托 Scala、JVM bytecode、embedded DSL、random search、SUT reset 和 error-trace replay，服务 event-driven libraries、middleware 和 non-blocking API 测试。

```text
Scala FSM model -> compiled test model -> Modbat random exploration -> SUT API calls -> error trace or replayable passing run
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. finite-state machine test model；
2. Scala-based embedded DSL；
3. transitions with executable actions；
4. random model exploration；
5. SUT API invocation；
6. test run、failure detection 和 replayable error trace。

### 核心抽象

论文没有给出完整数学元组，但明确说明模型是用 Scala DSL 表达的 finite-state machine。可保守整理为：

$$
M = (S,s_0,S_f,T,A)
$$

上式中的符号逐项解释如下：

1. `$M$` 是一个 `Modbat` 测试模型。
2. `$S$` 是模型状态集合，例如 `init`、`active`、`closed`。
3. `$s_0$` 是初始模型状态。
4. `$S_f$` 是终止或测试结束状态集合。
5. `$T \subseteq S \times A \times S$` 是带动作的转移集合。
6. `$A$` 是 Scala action blocks 集合，动作中可直接调用 SUT API。
7. 该式是根据原文“finite-state machine expressed in Scala-based DSL”做的保守归纳。

一条典型转移可写成：

$$
(s,a,s') \in T
$$

上式中的符号逐项解释如下：

1. `$s$` 是源状态。
2. `$a$` 是与该转移绑定的 Scala action block。
3. `$s'$` 是目标状态。
4. 在原文示例中，`"init" -> "active" := { c = new Component; c.start }` 就是这种带动作转移。

### 一个最小例子与通俗解释

原文给出最小 DSL 片段：

```scala
"init" -> "active" := { c = new Component; c.start }
```

这个例子可以解释为：

1. 模型从 `init` 状态出发。
2. `Modbat` 选择该转移后执行动作块。
3. 动作块创建组件 `c`，并调用 `c.start`。
4. 若调用没有违反性质，模型进入 `active` 状态。

通俗地说，`Modbat` 把状态机边变成“测试脚本片段”。随机探索状态机时，每走一条边就对真实 SUT 调一次 API，所以模型路径本身就是 API 事件序列。

### 运行 / 接受 / 转移语义

一次 test run 可写成：

$$
\pi = s_0 \xrightarrow{a_1} s_1 \xrightarrow{a_2} \cdots \xrightarrow{a_n} s_n
$$

上式中的符号逐项解释如下：

1. `$\pi$` 是一次 `Modbat` test run。
2. `$s_0$` 是初始模型状态。
3. `$a_i$` 是第 `$i$` 条转移上的 Scala action block。
4. `$s_i$` 是第 `$i$` 步后的模型状态。
5. `$s_n$` 是本次 run 的最终模型状态。
6. 原文说明初始和最终模型状态之间执行的转移序列构成 test run。

对同步 SUT 执行可保守写成：

$$
s \xrightarrow{a}_{M,SUT} s' \iff (s,a,s') \in T \land \mathrm{exec}(a,SUT)=\mathrm{ok}
$$

上式中的符号逐项解释如下：

1. `$\xrightarrow{a}_{M,SUT}$` 表示模型转移和 SUT API 动作一起执行。
2. `$(s,a,s') \in T$` 要求该模型边存在。
3. `$\mathrm{exec}(a,SUT)=\mathrm{ok}$` 表示动作块调用 SUT 后未触发失败。
4. 这是对原文“Modbat explores the model, executing the SUT in tandem”的保守语义整理。

### 语义边界

1. 本文主线是 API testing，不是完整形式验证。
2. `Modbat` 依赖随机探索，覆盖度取决于模型、搜索策略和 run 数。
3. SUT 需要能在每个 test run 后 reset 到初始状态。
4. 工具适合 JVM/Java bytecode 生态，非 JVM 系统需要额外桥接。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 测试模型 | `$M = (S,s_0,S_f,T,A)$` | `Modbat` 模型是带动作的有限状态机。 |
| 带动作转移 | `$(s,a,s') \in T$` | DSL 中的边绑定 API 调用或事件动作。 |
| test run | `$\pi = s_0 \xrightarrow{a_1} s_1 \xrightarrow{a_2} \cdots \xrightarrow{a_n} s_n$` | 一次从初始到最终状态的转移序列就是一次测试。 |
| 同步执行 | `$s \xrightarrow{a}_{M,SUT} s' \iff (s,a,s') \in T \land \mathrm{exec}(a,SUT)=\mathrm{ok}$` | 模型探索和 SUT API 调用并行发生。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接用 FSM 表达 API 生命周期和组件状态。 |
| 事件 / 触发 | 很强 | 转移对应 API 调用、事件或 I/O 触发。 |
| 守卫 / 数据 | 中等支持 | Scala DSL 可表达动作和数据生成，但论文摘录未展开丰富 guard 语义。 |
| 层次 | 不支持 | 本文不讨论层次状态机。 |
| 并发 / 同步 | 间接支持 | 适合 event-driven/non-blocking 系统，但核心模型仍是单条测试路径探索。 |
| 时间约束 | 弱支持 | 论文未把 timing 作为核心形式主义。 |
| 连续动态 / 随机性 | 弱支持 | 随机性来自测试探索策略，不是模型本体的概率语义。 |
| 可执行 / 可验证性 | 强 | 模型直接编译并执行 API 调用，失败轨迹可重放。 |

### 形式化问题与性质

1. `Modbat` 把 FSM 模型和测试代码合并在同一个 Scala DSL 中，降低了“模型和测试脚本分离”的成本。
2. 它的强项是 API-level event sequence generation，不是证明一个模型满足全局时序性质。
3. 对本文库而言，它补的是 event-driven API MBT 方法路线。

## 构造方式与承载格式

### 建模入口

原文给出的建模入口是 Scala-based embedded DSL。测试者写 FSM 状态、边和动作块，然后把模型与 `Modbat` 库一起编译。

### 机器可处理承载方式

机器可处理承载方式包括：

1. Scala source model；
2. compiled JVM bytecode；
3. `Modbat` model library；
4. generated event sequences / test runs；
5. error trace file。

### 交换与互操作

互操作重点在 JVM：

1. 任何能编译到 Java bytecode 的 SUT 都可作为目标。
2. Scala DSL 直接调用 SUT API。
3. 原文未来工作希望输出 JUnit-compatible error traces。

## 配套基础设施

- 建模/编辑工具：Scala 语言和 embedded DSL，原文未给专门 GUI。
- 解析/交换/元模型支持：Scala 编译器和 `Modbat` model library，原文未给独立交换格式。
- 仿真/执行支持：random search、test run execution、SUT reset 和 failure replay。
- 验证/分析支持：运行时性质违反检测和错误轨迹输出。
- 代码生成/转换支持：不主打独立代码生成，测试逻辑本身嵌入 Scala 模型。
- 标准化或社区生态：依托 Scala、JVM bytecode 和 API-level testing 生态。

## 适用场景与需求前提

### 适用场景

适合程序库、框架、中间件和事件驱动组件的 API 测试，尤其适合行为可以压成 FSM 生命周期并且 API 调用本身就是测试动作的系统。

### 需求前提

1. 被测对象能编译到 Java bytecode，或能通过 JVM 桥接访问。
2. 行为可抽象为有限状态、转移和动作块。
3. 每轮测试后 SUT 和模型都能回到初始状态。
4. 团队接受随机探索加错误轨迹重放，而不是一次性穷尽所有路径。

### 不适用或高成本场景

若被测系统无法 reset、接口不是 API 风格、核心性质是 dense-time 或物理连续行为，`Modbat` 的 FSM API testing 路线会比较吃力。

## 与相邻形式主义的关系

相对 [model-based-testing-of-object-oriented-reactive-systems-with-spec-explorer/desc.md](../model-based-testing-of-object-oriented-reactive-systems-with-spec-explorer/desc.md)，`Spec Explorer` 更完整地定义 model automata、scenario control 和 offline/online 测试理论，而 `Modbat` 更轻量地把 FSM 测试模型嵌入 Scala；相对 [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)，`TorX` 更偏 `IOLTS/ioco` 理论和 adapter 架构；相对 [model-based-testing-with-torxakis-the-mysteries-of-dropbox-revisited/desc.md](../model-based-testing-with-torxakis-the-mysteries-of-dropbox-revisited/desc.md)，`TorXakis` 更重视 symbolic data-aware `ioco` 测试。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 LLM 生成的 API 行为模型不一定要落成复杂图形标准，轻量 embedded DSL 也可以成为可执行测试入口。
2. `"state" -> "state" := action` 这种形式非常适合从自然语言需求抽取状态、事件和 API side effects。
3. 失败轨迹可重放这一点适合后续模型修复：错误路径可以直接转成修复提示。

### 作为目标形式主义还是中间表示

更适合作为 API 测试中间表示和方法路线，而不是通用控制系统形式主义。

## 重要的相关工作

1. [model-based-testing-of-object-oriented-reactive-systems-with-spec-explorer/desc.md](../model-based-testing-of-object-oriented-reactive-systems-with-spec-explorer/desc.md)：更完整的面向对象 model automata 测试路线。
2. [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)：早期 `IOLTS/ioco` 在线测试工具链。
3. [model-based-testing-with-torxakis-the-mysteries-of-dropbox-revisited/desc.md](../model-based-testing-with-torxakis-the-mysteries-of-dropbox-revisited/desc.md)：带数据协议的 symbolic `ioco` 测试对照项。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：💻 软件建模与程序行为
- 形式主义：`FSM / Modbat / Scala embedded DSL / API testing`
- 论文角色：event-driven API model-based testing tool
- 归类理由：论文主体是以 FSM + Scala DSL 驱动 API 测试的工具化方法路线，属于 `🛠️` 条目。

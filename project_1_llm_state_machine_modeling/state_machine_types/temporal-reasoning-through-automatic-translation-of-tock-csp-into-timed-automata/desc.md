# 通过自动翻译 tock-CSP 实现时序推理 / Temporal Reasoning Through Automatic Translation of tock-CSP into Timed Automata

## 基本信息

- 标题：Temporal Reasoning Through Automatic Translation of tock-CSP into Timed Automata
- 中文标题：通过自动翻译 tock-CSP 实现时序推理
- 作者：Abdulrazaq Abba，Ana Cavalcanti，Jeremy Jacob
- 发表：*Formal Methods: Foundations and Applications*，pp. 70-86，2021
- DOI：`10.1007/978-3-030-92137-8_5`
- 链接：https://doi.org/10.1007/978-3-030-92137-8_5
- 形式主义：`tock-CSP / Timed Automata / Uppaal translation`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：tock-CSP-to-`Uppaal` bridge / temporal-logic reasoning route
- 工具/实现获取方式：原文明确说明作者开发了翻译工具，并在参考中给出仓库入口 `https://github.com/ahagmj/TemporalReasoning.git`。
- 标准/格式获取方式：输入是 `tock-CSP` 过程模型，输出是 `Uppaal` 可读的 timed automata network、environment automaton 与配套 trace-analysis workflow；它是转换链路，不是中立交换标准。

## 简报

这篇论文补的是 `tock-CSP` 与 `Timed Automata` 之间的一条很有代表性的 bridge。`tock-CSP` 很擅长用 refinement 做离散时间建模，但某些 liveness / temporal-logic 需求并不容易直接表达。作者的做法不是放弃 `tock-CSP`，而是把它自动翻成一组小的 `Timed Automata` 网络，让 `Uppaal` 接手 temporal logic 和 liveness reasoning。

- 形式主义定位：process algebra 到 timed-automata backend 的翻译与验证桥，而不是新的时钟自动机母型。
- 构造方式简述：把每个 `tock-CSP` 事件、组合结构和时间推进拆成若干小 `TA`，再配一个 environment automaton 和 coordinating actions 接成 `Uppaal` 网络。
- 基础设施与场景简述：依托 translation rules、coordinating actions、environment TA、`FDR`/`Uppaal` trace analysis 和 Haskell 实现，服务 `tock-CSP` 模型的 temporal-logic 验证。

```text
tock-CSP process -> small TA network + environment TA -> Uppaal temporal reasoning -> trace comparison with FDR
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `tock-CSP` 过程；
2. network of small timed automata；
3. coordinating actions；
4. environment TA；
5. trace-based correctness validation。

### 核心抽象

论文把翻译结果视为一个由多个小 `TA` 组成的网络。可保守写成：

$$
\mathrm{transTA}(P) = \mathcal N_P
$$

上式中的符号逐项解释如下：

1. `P` 是输入的 `tock-CSP` 过程。
2. `\mathrm{transTA}` 是论文定义的翻译函数。
3. `\mathcal N_P` 是输出的 timed automata 网络。
4. 该网络通常还包含 environment automaton，用来协调启动、终止与 `tock` 时间推进。

论文对 correctness 给出最核心的 trace-level 主张。可直接整理为：

$$
\mathrm{traces}_{\mathrm{tockCSP}}(P) = \mathrm{traces}_{\mathrm{TA}}(\mathrm{transTA}(P))
$$

上式中的符号逐项解释如下：

1. `\mathrm{traces}_{\mathrm{tockCSP}}(P)` 是原始 `tock-CSP` 模型的行为轨迹集合。
2. `\mathrm{transTA}(P)` 是翻译后的 `TA` 网络。
3. `\mathrm{traces}_{\mathrm{TA}}` 是在移除协调动作后得到的 `TA` 行为轨迹集合。
4. 论文用实验性 trace analysis 和数学证明共同支撑这条等式。

### 一个最小例子与通俗解释

论文中的 `Automatic Door System` 很直观：

1. `Controller` 执行 `open -> tock -> close -> Controller`。
2. `Lighting` 在 `close` 同步后执行 `offLight -> Lighting`。
3. 翻译后不是一张大 `TA`，而是一组小 automata，再由 coordinating actions 把启动、同步和终止串起来。
4. 这样 `tock-CSP` 原本不方便直接表达的 “eventually offLight” 之类 liveness 需求，就可以交给 `Uppaal` 写 temporal logic 来查。

通俗地说，这篇论文是在给 `tock-CSP` 加一条“外接 `Uppaal` 的时序推理端口”。

### 运行 / 接受 / 转移语义

论文显式区分普通事件和协调动作。对去除协调动作后的可观察行为，可写成：

$$
\mathrm{traces}_{\mathrm{TA}}(A) = \{ t \setminus \mathrm{Coord} \mid t \in \mathrm{traces}'_{\mathrm{TA}}(A) \}
$$

上式中的符号逐项解释如下：

1. `A` 是翻译得到的 automata 网络。
2. `\mathrm{traces}'_{\mathrm{TA}}(A)` 是包含 coordinating actions 的原始轨迹。
3. `\mathrm{Coord}` 是 coordinating-action 集合。
4. 去掉这些动作后，才与 `tock-CSP` 原始可观察轨迹比较。

时间推进则通过专门的 `tock` 机制进入 `TA`。可保守写成：

$$
\mathrm{tick}: (s, ck) \to (s', ck')
$$

上式中的符号逐项解释如下：

1. `s` 和 `s'` 是某个小 `TA` 的位置。
2. `ck` 与 `ck'` 是翻译中用于控制 `tock` 的 clock valuation。
3. 论文用 broadcast-style `tock` action 和 environment TA 记录离散时间推进。
4. 这正是 `tock-CSP` 中时间事件 `tock` 映到 `TA` 侧的关键桥梁。

### 语义边界

1. 该方法是 bridge，不是把 `tock-CSP` 重定义成 `TA`。
2. 论文依赖受支持的 `tock-CSP` 构造子集与翻译规则。
3. 输出是多个小 `TA` 的网络，而不是单一紧凑 automaton。
4. 当前做法仍把 `tock` 当显式 action 处理，而非完全内化为 `TA` 时间流逝。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 翻译函数 | `$\mathrm{transTA}(P) = \mathcal N_P$` | `tock-CSP` 过程会变成一组小 `TA` 网络。 |
| trace 正确性 | `$\mathrm{traces}_{\mathrm{tockCSP}}(P) = \mathrm{traces}_{\mathrm{TA}}(\mathrm{transTA}(P))$` | 翻译的核心正确性目标。 |
| 去协调动作 | `$\mathrm{traces}_{\mathrm{TA}}(A) = \{ t \setminus \mathrm{Coord} \mid t \in \mathrm{traces}'_{\mathrm{TA}}(A) \}$` | 比较前要先剥离协调动作。 |
| `tock` 桥接 | `$\mathrm{tick}: (s, ck) \to (s', ck')$` | 离散时间推进通过 `TA` 侧 clock 和动作实现。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 翻译结果直接是 `TA` locations/network。 |
| 事件 / 触发 | 很强 | `tock-CSP` 事件与 coordinating actions 都是一等对象。 |
| 守卫 / 数据 | 弱支持 | 重点在控制流与时间，不在富数据。 |
| 层次 | 不支持 | 输出不是层次状态机。 |
| 并发 / 同步 | 很强 | 原过程组合和同步关系会被拆到多个小 `TA` 中。 |
| 时间约束 | 很强 | `tock` 离散时间推进与 `Uppaal` 时钟语义是核心。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散 timed reasoning。 |
| 可执行 / 可验证性 | 很强 | 输出直接面向 `Uppaal` 和 trace comparison。 |

### 形式化问题与性质

1. 论文真正解决的是“如何让 `tock-CSP` 也能更方便地吃到 temporal logic 工具链”。
2. network-of-small-TAs 的设计，是为了保留 `tock-CSP` 的组合结构，而不是简单 flatten。
3. correctness 主张直接写到 trace equality，使这条桥的语义目标非常清晰。

## 构造方式与承载格式

### 建模入口

原文中的建模入口有：

1. `tock-CSP` 进程与组合算子；
2. `tock` 时间事件；
3. synchronisation、choice、interrupt 等结构；
4. temporal reasoning 目标需求。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `tock-CSP` 文本模型；
2. Haskell translation rules；
3. small `TA` network；
4. environment automaton；
5. `FDR/Uppaal` trace analysis workflow。

### 交换与互操作

这篇论文的互操作重点在：

1. `tock-CSP` 模型可自动转到 `Uppaal`；
2. `FDR` 用于 source-side trace，`Uppaal` 用于 target-side temporal logic；
3. 协调动作和 environment TA 提供了 process algebra 到 `TA` 的稳定桥。

## 配套基础设施

- 建模/编辑工具：`tock-CSP` 建模环境与对应文本规格。
- 解析/交换/元模型支持：Haskell translation rules、coordinating actions 与 environment TA。
- 仿真/执行支持：`Uppaal` 对输出 `TA` 网络执行验证与 trace 生成。
- 验证/分析支持：`FDR` + `Uppaal` + trace analysis system。
- 代码生成/转换支持：重点是 `tock-CSP -> TA` 翻译，而不是部署代码生成。
- 标准化或社区生态：桥接 `tock-CSP` / `FDR` 与 `Uppaal` 两条成熟工具线。

## 适用场景与需求前提

### 适用场景

适合已有 `tock-CSP` 模型，但希望补上 liveness、temporal logic 或 `Uppaal` 工具体验的场景。

### 需求前提

1. 源模型需位于受支持的 `tock-CSP` 子集内。
2. 关键时间行为能通过 `tock` 事件表达。
3. 目标分析确实需要 `Uppaal` 的 temporal reasoning 能力。
4. 团队接受 bridge 带来的 coordinating actions 和 network-of-small-TAs 中间层。

### 不适用或高成本场景

如果系统主要困难在富数据、连续动力学或非常大规模 flatten 后端开销，这条桥的收益会下降。

## 与相邻形式主义的关系

相对 [fdr3-a-modern-refinement-checker-for-csp/desc.md](../fdr3-a-modern-refinement-checker-for-csp/desc.md)，本文不是 refinement checker 本体，而是把 `tock-CSP` 引到 temporal-logic backend；相对 [uppaal-40/desc.md](../uppaal-40/desc.md)，本文不是 timed backend 平台总览，而是面向 `tock-CSP` 的前端翻译桥；相对 [robochart-modelling-and-verification-of-robotic-applications/desc.md](../robochart-modelling-and-verification-of-robotic-applications/desc.md)，`RoboChart` 也依赖 `CSP/tock-CSP` 语义，但本文更聚焦于 `tock-CSP -> TA` 的 bridge。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明不同形式主义之间的桥接可以显著补全原模型的验证能力。
2. 对 `project_1` 来说，这说明未来不必在一个目标形式主义里塞进全部分析能力，必要时可以桥接到更合适的 backend。
3. trace-equality 风格的 correctness 目标，也很适合约束后续自动转换链的质量。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，它更像 process algebra 与 timed backend 之间的中间验证桥，而不是目标形式主义。

### 对需求到模型生成的启发

1. 若前端模型更适合表达组合结构，后端模型更适合表达 temporal logic，两者可以通过保守翻译连接。
2. “小 automata 网络 + 协调动作”是一种保结构的翻译思路，值得借鉴。
3. 转换正确性最好尽量落到 trace 或语言层面，而不是只靠案例演示。

## 重要的相关工作

- [fdr3-a-modern-refinement-checker-for-csp/desc.md](../fdr3-a-modern-refinement-checker-for-csp/desc.md)：`CSP/tock-CSP` 侧的主验证工具线。
- [uppaal-40/desc.md](../uppaal-40/desc.md)：目标 timed-automata backend 平台。
- [robochart-modelling-and-verification-of-robotic-applications/desc.md](../robochart-modelling-and-verification-of-robotic-applications/desc.md)：使用 `CSP/tock-CSP` 语义的机器人 DSL 路线。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇典型的跨形式主义 bridge 条目，适合作为 `tock-CSP` 向 `Uppaal`/`Timed Automata` temporal-logic reasoning 迁移的关键证据入账。

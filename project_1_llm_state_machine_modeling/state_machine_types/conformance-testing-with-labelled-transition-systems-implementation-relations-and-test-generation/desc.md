# 带标记迁移系统的一致性测试：实现关系与测试生成 / Conformance testing with labelled transition systems: Implementation relations and test generation

## 基本信息

- 标题：Conformance testing with labelled transition systems: Implementation relations and test generation
- 中文标题：带标记迁移系统的一致性测试：实现关系与测试生成
- 作者：Jan Tretmans
- 发表：*Computer Networks and ISDN Systems*，29(1)，pp. 49-79，1996
- DOI：`10.1016/S0169-7552(96)00017-7`
- 链接：https://doi.org/10.1016/S0169-7552(96)00017-7
- 形式主义：`LTS / input-output transition systems / iot / ioconf`
- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：`ioconf` conformance relation + sound test-generation mother line
- 工具/实现获取方式：原文没有给出现成工具实现；它给出的是 `conf` 与 `ioconf` 两套测试理论和可证明正确的测试生成算法，后续 `TorX / JTorX / TESTOR` 等工具线正是沿这条母线工程化。
- 标准/格式获取方式：原文承载方式是 labelled transition systems、input-output transition systems 与 `δ`-trace automata；不是交换标准论文，也没有独立文件格式规范。

## 简报

这篇论文的关键价值，不是提出另一种状态机画法，而是把“如何从状态机规格推出黑盒一致性测试”整理成一套可证明的输入输出测试理论。论文前半部分讨论对称交互下的 `conf` 测试，后半部分转向更贴近真实接口系统的 input-output transition systems，并给出后来极具影响力的 `ioconf` 思路。

- 形式主义定位：基于 `LTS / IOTS` 的 conformance-testing 理论母线，而不是新的图形 DSL。
- 构造方式简述：先把规格与实现都视为 transition-system 行为模型，再用 `δ`-trace automaton 显式表示输出静默与可观察行为，最后围绕 `ioconf` 推导 sound test cases。
- 基础设施与场景简述：它本身不是工具论文，但为 `ioco` 一致性测试、在线测试推导、adapter/explorer 架构和后续 MBT 工具提供了最关键的形式基础。

```text
formal specification -> LTS / IOTS semantics -> δ-trace automaton -> ioconf relation -> sound test case generation -> later TorX/JTorX/TESTOR tool lines
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. labelled transition system (`LTS`)。
2. deterministic finite test case 与 test suite。
3. input-output transition system (`IOTS`)。
4. `δ`-trace automaton。
5. `iot / ioconf` 这类实现关系及其测试生成算法。

### 核心抽象

论文对 `LTS` 的基础定义是：

$$
p = (S, L, T, s_0)
$$

上式中的符号逐项解释如下：

1. `S` 是可数、非空的状态集合。
2. `L` 是可观察标签集合。
3. `T \subseteq S \times (L \cup \{\tau\}) \times S` 是迁移关系。
4. `s_0` 是初始状态。
5. `\tau` 是不可观察的内部动作。

论文随后把实现约束收紧为 input-output transition systems，可保守整理为：

$$
p \in \mathrm{IOTS}(L_I, L_U) \iff L = L_I \uplus L_U \land \forall s \in S,\ \forall a \in L_I:\ a \in init(s)
$$

上式中的符号逐项解释如下：

1. `L_I` 是输入动作集合。
2. `L_U` 是输出动作集合。
3. `\uplus` 表示输入与输出标签的不交并。
4. `init(s)` 表示状态 `s` 当前可执行的可观察动作集合。
5. “所有输入始终 enabled” 是论文为黑盒实现建立 `IOTS` 假设的核心。

为了把“输出静默”也纳入观察对象，论文引入 `δ`-trace automaton。其最关键的判定关系是：

$$
i \mathrel{\mathrm{ioconf}} s \iff \forall \sigma \in traces(A_s) \cap L^*:\ out(A_i\ \mathrm{after}\ \sigma) \subseteq out(A_s\ \mathrm{after}\ \sigma)
$$

上式中的符号逐项解释如下：

1. `i` 是 implementation 的行为模型。
2. `s` 是 specification 的行为模型。
3. `A_i` 与 `A_s` 是实现与规格对应的 `δ`-trace automata。
4. `\sigma` 是规格允许的有限可观察 trace。
5. `out(A\ \mathrm{after}\ \sigma)` 表示在 trace `\sigma` 之后允许出现的输出集合，其中也显式包括 `δ` 这类输出静默。

原文对 sound / complete test suite 也给出明确定义，可压缩为：

$$
T\ \text{is sound} \iff \forall i:\ i \mathrel{\mathrm{ioconf}} s \Rightarrow i\ \mathrm{passes}\ T
$$

$$
T\ \text{is complete} \iff \forall i:\ i \mathrel{\mathrm{ioconf}} s \Leftrightarrow i\ \mathrm{passes}\ T
$$

上式中的符号逐项解释如下：

1. `T` 是测试套件。
2. `i passes T` 表示实现通过测试套件中所有测试。
3. sound 只保证“测出错就真错”。
4. complete 进一步保证“正确实现一定能通过，错误实现一定会被某测试区分出来”。

### 一个最小例子与通俗解释

论文反复使用 candy-machine 类比，非常适合作最小例子：

1. 规格允许用户投入 `shil` 后输出 `liq`，也可能输出 `choc`。
2. 若实现是一个输入输出系统，则“按按钮/投币”这类输入不能被实现拒绝。
3. 对于某个 trace `\sigma`，若实现在该上下文下给出了规格未允许的输出，或者在规格要求可观察输出时只表现为 `δ`，它就不满足 `ioconf`。

通俗地说，这条路线像一个“接口行为裁判”。它不是比实现内部代码，也不是比状态图画得像不像，而是比在每个可观察上下文里，真实系统会不会给出规格没允许的输出或错误的静默。

### 运行 / 接受 / 转移语义

论文的测试运行语义基于 tester 与 implementation 的同步组合。可保守写成：

$$
u\ \text{is a test run of}\ t\ \text{and}\ i \iff (t \parallel i)\ \mathrm{after}\ u\ \text{deadlocks}
$$

上式中的符号逐项解释如下：

1. `t` 是测试用例。
2. `i` 是实现。
3. `u` 是一条有限交互 trace。
4. `t \parallel i` 表示测试器与实现的同步组合。
5. deadlock 对应某次测试运行在无进一步可执行交互时结束。

### 语义边界

这篇论文的边界也很清楚：

1. 主线是离散输入输出交互，而不是 dense-time 或连续动力学。
2. 规格和实现都要能抽象成 transition-system 语义。
3. `ioconf` 主要关注可观察输入输出一致性，不直接处理复杂数据语义。
4. 论文中的完整测试套件通常是无限的，实际落地仍需选择策略与工具实现。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `LTS` 骨架 | `$p = (S, L, T, s_0)$` | 规格、实现和测试都以 transition-system 为基础。 |
| `IOTS` 假设 | `$p \in \mathrm{IOTS}(L_I, L_U) \iff L = L_I \uplus L_U \land \forall s,a \in L_I:\ a \in init(s)$` | 把真实实现约束成“输入永不拒绝”的接口系统。 |
| `ioconf` | `$i \mathrel{\mathrm{ioconf}} s \iff \forall \sigma \in traces(A_s)\cap L^*: out(A_i\ after\ \sigma) \subseteq out(A_s\ after\ \sigma)$` | 后续 `ioco` 系列一致性测试的核心母式。 |
| sound / complete | `$sound: i \mathrel{\mathrm{ioconf}} s \Rightarrow i\ passes\ T$`；`$complete: i \mathrel{\mathrm{ioconf}} s \Leftrightarrow i\ passes\ T$` | 区分“不会冤枉”和“理论上测得全”。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 所有对象都以 `LTS / IOTS` 状态空间表示。 |
| 事件 / 触发 | 很强 | 输入输出标签是理论中心。 |
| 守卫 / 数据 | 弱支持 | 论文主线不在富数据变量与复杂守卫。 |
| 层次 | 不适用 | 不是层次状态机语义论文。 |
| 并发 / 同步 | 中等支持 | 通过同步组合表达 tester 与 implementation 交互。 |
| 时间约束 | 不支持 | 本文不是 timed-testing 路线。 |
| 连续动态 / 随机性 | 不支持 | 主线完全在离散黑盒一致性。 |
| 可执行 / 可验证性 | 中等到强 | 给出可证明 sound 的测试生成算法，但工具化不在本文完成。 |

### 形式化问题与性质

1. 论文真正稳定下来的不是“某个工具”，而是 `ioconf` 这类输入输出一致性定义方式。
2. `δ`-trace automaton 使“静默也是一种可观察行为”被纳入统一框架。
3. 这为后续 `TorX / JTorX / TESTOR` 等 on-the-fly MBT 工具提供了可追溯的理论母线。

## 构造方式与承载格式

### 建模入口

原文的建模入口主要有：

1. 用 labelled transition systems 表达规格。
2. 把实现假设为 input-output transition systems。
3. 用 deterministic finite LTS 表示测试用例。
4. 用 `δ`-trace automaton 显式表示输出静默。

### 机器可处理承载方式

机器可处理承载方式包括：

1. graph / tree 风格的 labelled transition system；
2. 行为表达式 `a;B` 风格的 process-like syntax；
3. `δ`-trace automata；
4. pass/fail verdict 标注测试状态。

### 交换与互操作

这篇论文并不提供工程交换标准，但它定义了非常稳定的语义接口：

1. 规格与实现都可以先压成 `LTS / IOTS`。
2. 测试器只需要观察输入、输出与静默。
3. 这使后续各种前端建模语言都能通过共同的 transition-system 语义接入测试生成。

## 配套基础设施

- 建模/编辑工具：原文未给出现成建模器，重点是理论而非 IDE。
- 解析/交换/元模型支持：核心承载方式是 `LTS / IOTS / δ`-trace automata，不是文件格式标准。
- 仿真/执行支持：论文定义了 test case、test suite、test run 与 pass/fail 机制。
- 验证/分析支持：给出 `conf` 与 `ioconf` 对应的 sound / complete 测试生成理论。
- 代码生成/转换支持：不是代码生成论文。
- 标准化或社区生态：与协议一致性测试、`ioco` 理论和后续 University of Twente 工具线直接相关。

## 适用场景与需求前提

### 适用场景

适合通信协议、交互式反应系统、服务接口和其他“输入输出行为就是系统真相”的黑盒一致性测试场景。

### 需求前提

1. 规格必须能抽象成有限或至少可测试的 `LTS / IOTS` 行为。
2. 输入输出方向需要可区分。
3. 团队关心的是 conformance，而不是仅做内部实现验证。
4. 被测系统必须能以黑盒方式暴露输入刺激与输出观测。

### 不适用或高成本场景

如果系统本质上依赖复杂连续动力学、概率分布、或高维数据状态而又难以抽象成 `IOTS`，这条路线的成本会迅速上升。

## 与相邻形式主义的关系

相对 [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)，这篇论文是更早的理论母线；相对 [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)，这里给的是实现关系与测试生成定义，而不是可用工作台；相对 [testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md](../testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md)，`TESTOR` 继承的是 `ioco` / `IOLTS` testing 传统中的工具化一支。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 的价值在于，它清楚回答了“如果 LLM 生成出一个接口型状态机，后续能怎么测”。只要模型能落成带输入输出方向的状态机语义，就可以自然接到一致性测试和失败轨迹生成链路。

### 作为目标形式主义还是中间表示

更适合作为接口型状态机的语义约束与测试后端入口，而不是最终面向工程师编辑的目标 DSL。

### 对需求到模型生成的启发

1. 需求分析阶段最好尽早明确输入输出方向，否则后续测试关系无法稳定定义。
2. “静默是否允许”是需求建模中经常被漏掉的部分，而这里把它正式化成了 `δ`。
3. 若研究要闭环到验证与修复，`ioconf` 这类关系能直接提供 counterexample-oriented 后续链路。

### 现实限制

论文没有解决工具可用性和大规模工程模型管理问题，这些要靠后续 `TorX / JTorX / TESTOR` 一类基础设施补齐。

## 重要的相关工作

1. [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)：把这条 `ioco` 路线首次较完整地落到 on-the-fly 测试工具。
2. [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)：Twente 工具线的后继工作台。
3. [testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md](../testor-a-modular-tool-for-on-the-fly-conformance-test-case-generation/desc.md)：基于 `IOLTS / ioco` 传统的 CADP 模块化在线测试工具。

## 文献分类总结

- 主类：🔌 接口 / 组合 / 契约模型
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`LTS / input-output transition systems / iot / ioconf`
- 论文角色：`ioconf` conformance relation + sound test-generation mother line
- 归类理由：论文主体是输入输出 transition-system 上的一致性关系与测试生成方法，不是新工具平台，也不是应用案例。

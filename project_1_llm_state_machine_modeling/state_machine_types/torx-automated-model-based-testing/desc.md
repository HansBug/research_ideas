# TorX：自动化模型驱动测试 / TorX: Automated Model-Based Testing

## 基本信息

- 标题：TorX: Automated Model-Based Testing
- 中文标题：TorX：自动化模型驱动测试
- 作者：Jan Tretmans，Ed Brinksma
- 发表：*First European Conference on Model-Driven Software Engineering*，pp. 31-43，2003
- DOI：原文未给出 DOI
- 链接：https://ris.utwente.nl/ws/files/5524092/trej2003-torx.pdf
- 形式主义：`IOLTS / ioco / TorX`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：on-the-fly model-based testing / `ioco` test derivation and execution tool
- 工具/实现获取方式：原文明确给出 `TorX` 这一原型测试工具，并围绕 `Explorer / Primer / Driver / Adapter` 描述其架构；论文未提供今天仍可直接安装的官方源码仓库。
- 标准/格式获取方式：原文强调 `TorX` 以 labelled transition systems 为共同语义骨架，可接 `Lotos`、`Promela`、`Fsp` 与 `Aldebaran` automata，并通过 `Open/Caesar`、`Explorer` 和 `Adapter` 接口完成接入。

## 简报

这篇论文的核心价值，不在于再发明一种新的状态机本体，而在于把 `ioco` 一致性测试从“理论上可导测试集”真正落成可执行的 on-the-fly 工具链。`TorX` 把 formal specification、test derivation、test execution 和 verdict analysis 串成一个运行时循环，使测试不必先离线枚举完整测试集，而是在执行时按当前状态继续派生下一步。

- 形式主义定位：基于 `IOLTS / ioco` 的在线模型驱动测试路线，而不是新的状态机家族。
- 构造方式简述：以 labelled transition system 语义为公共底盘，用 `Explorer` 访问规格状态空间，用 `Primer` 推导 test primitives，再由 `Driver` 和 `Adapter` 驱动真实 SUT。
- 基础设施与场景简述：依托 `Lotos/Promela/FSP/Aldebaran`、`Open/Caesar`、adapter 编码层与消息序列图日志，服务协议、反应式软件和交互系统的一致性测试。

```text
formal specification -> Explorer -> Primer -> Driver + Adapter -> on-the-fly test step -> verdict/log
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `TorX`：

1. 规格与实现都抽象成 labelled transition systems。
2. `ioco` 作为实现满足规格的判定关系。
3. `Explorer / Primer / Driver / Adapter` 四个核心组件。
4. on-the-fly test generation / execution loop。
5. user-guided 或 fully automatic 两种运行模式。

### 核心抽象

论文直接给出的核心正确性关系是：

$$
i \mathrel{\mathrm{ioco}} s \iff \forall \sigma \in \mathrm{Straces}(s): \mathrm{out}(i\ \mathrm{after}\ \sigma) \subseteq \mathrm{out}(s\ \mathrm{after}\ \sigma)
$$

上式中的符号逐项解释如下：

1. `$i$` 是 implementation，也就是被测系统 `SUT` 的行为模型。
2. `$s$` 是 specification，也就是形式化规格模型。
3. `$\sigma$` 是规格允许的 suspension trace。
4. `$\mathrm{out}(x\ \mathrm{after}\ \sigma)$` 表示系统 `$x$` 在执行痕迹 `$\sigma$` 后可能产生的输出集合。
5. 子集关系表示：实现在任何规格可达上下文下都不能产生规格不允许的输出，包括 quiescence。

结合论文的工具图，可以把 `TorX` 的最小骨架保守整理为：

$$
\mathrm{TorX} = (E, P, D, A)
$$

上式中的符号逐项解释如下：

1. `$E$` 是 `Explorer`，负责暴露规格状态空间。
2. `$P$` 是 `Primer`，负责从规格派生测试原语。
3. `$D$` 是 `Driver`，负责决定下一步是刺激还是观察。
4. `$A$` 是 `Adapter`，负责把抽象动作映射到真实 SUT I/O。
5. 这是依据原文架构图做的保守抽象，而不是论文显式给出的形式化元组。

论文还强调测试集的两个关键性质，可压成：

$$
\mathrm{fail}(t,i) \Rightarrow \neg(i \mathrel{\mathrm{ioco}} s), \qquad \neg(i \mathrel{\mathrm{ioco}} s) \Rightarrow \exists t \in T_s:\ \mathrm{fail}(t,i)
$$

上式中的符号逐项解释如下：

1. `$t$` 是从规格 `$s$` 派生出的某个测试。
2. `$T_s$` 是规格 `$s$` 对应的测试集。
3. 左式对应 soundness：测出错则实现一定不满足规格。
4. 右式对应 exhaustiveness：实现若不满足规格，则测试集中存在至少一个失败测试。

### 一个最小例子与通俗解释

结合论文的 `ioco` 定义，可以把最小例子理解成：

1. 规格在输入 `coin` 之后只允许输出 `coffee` 或保持静默。
2. 实现如果在相同上下文下输出了 `tea`。
3. 则有 `tea \in \mathrm{out}(i\ \mathrm{after}\ coin)`，但 `tea \notin \mathrm{out}(s\ \mathrm{after}\ coin)`。
4. 因而该实现不满足 `ioco`，`TorX` 应给出 fail verdict。

通俗地说，`TorX` 像一个“边走边测的状态机裁判”。它不会先把所有测试脚本一次性写完，而是每走一步都看当前规格允许什么、实现做了什么，再决定下一步怎么测。

### 运行 / 接受 / 转移语义

`TorX` 的运行语义，本质上是对规格状态空间的逐步探索与对 SUT 的逐步比对。可保守整理为：

$$
c_{k+1} = \mathrm{step}(E, P, D, A, c_k, sut)
$$

上式中的符号逐项解释如下：

1. `$c_k$` 是第 `$k$` 步测试配置。
2. `$\mathrm{step}$` 表示一次 on-the-fly 测试步。
3. `Explorer` 和 `Primer` 提供当前步可选测试原语。
4. `Driver` 选择观察还是刺激。
5. `Adapter` 把抽象动作落实到真实 `SUT`。

### 语义边界

这篇论文的边界主要有：

1. 它主要面向离散、反应式、输入输出驱动的系统。
2. 规格必须能压成 transition-system 风格语义。
3. `TorX` 的能力很大程度上取决于 `Adapter` 是否能把真实系统正确接入。
4. 数据密集、连续动力学或高维时间约束并不是这篇论文的主线。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 一致性关系 | `$i \mathrel{\mathrm{ioco}} s \iff \forall \sigma \in \mathrm{Straces}(s): \mathrm{out}(i\ \mathrm{after}\ \sigma) \subseteq \mathrm{out}(s\ \mathrm{after}\ \sigma)$` | 测试到底在判什么。 |
| 工具骨架 | `$\mathrm{TorX} = (E, P, D, A)$` | `Explorer/Primer/Driver/Adapter` 是工具最小核心。 |
| soundness | `$\mathrm{fail}(t,i) \Rightarrow \neg(i \mathrel{\mathrm{ioco}} s)$` | 测出失败不会冤枉一个正确实现。 |
| exhaustiveness | `$\neg(i \mathrel{\mathrm{ioco}} s) \Rightarrow \exists t \in T_s:\ \mathrm{fail}(t,i)$` | 理论上完整测试集能覆盖所有不正确实现。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 一切都围绕 transition-system 状态空间展开。 |
| 事件 / 触发 | 很强 | 测试本质就是对输入输出动作的驱动与观察。 |
| 守卫 / 数据 | 弱支持 | 需先经前端规格语言抽象，不是富数据状态机原生工具。 |
| 层次 | 弱支持 | 论文主线不在层次状态机。 |
| 并发 / 同步 | 间接支持 | 只要前端语义能落成 LTS，就可被测试。 |
| 时间约束 | 弱支持 | 本文并非 timed testing 工具论文。 |
| 连续动态 / 随机性 | 不支持 | 主线完全在离散交互测试。 |
| 可执行 / 可验证性 | 很强 | on-the-fly generation、execution、analysis 和日志都已工具化。 |

### 形式化问题与性质

1. `TorX` 把“形式规格 -> 测试派生 -> 执行 -> verdict”做成一个连续循环，而不是多个松散阶段。
2. 它真正补的是 `ioco` 在工具层的可运行闭环，而不只是定义层。
3. 对本文库而言，它是 `JTorX` 之前更早的在线交互测试母线节点。

## 构造方式与承载格式

### 建模入口

原文给出的建模入口主要有：

1. `Lotos`
2. `Promela`
3. `Fsp`
4. `Aldebaran` automata

### 机器可处理承载方式

`TorX` 的机器可处理承载方式包括：

1. transition-system style specification semantics；
2. `Explorer` 接口；
3. `Primer` 派生出的 test primitives；
4. `Adapter` 编码后的 concrete I/O；
5. 测试日志和动态消息序列图。

### 交换与互操作

这条路线的互操作重点非常明确：

1. 不同规格语言通过 `Explorer` 被收束到统一状态空间访问接口。
2. 不同 SUT 通过 `Adapter` 被收束到统一测试执行接口。
3. `TorX` 本体更像一个“测试中枢”，前后都靠接口解耦。

## 配套基础设施

- 建模/编辑工具：`Lotos`、`Promela`、`Fsp`、`Aldebaran` 等前端规格环境。
- 解析/交换/元模型支持：`Open/Caesar`、`Explorer` 接口与 transition-system 语义桥。
- 仿真/执行支持：on-the-fly 测试执行、消息序列图日志、手动/自动双模式。
- 验证/分析支持：`ioco` 一致性判定、test purpose 驱动选择与 fail verdict。
- 代码生成/转换支持：不是代码生成工具，重点是测试派生与执行桥接。
- 标准化或社区生态：依托 `ioco` 理论、荷兰 `C^ote de Resyste` 项目和后续 Twente 测试工具线。

## 适用场景与需求前提

### 适用场景

适合协议、反应式软件、事件驱动组件和一般交互系统的模型驱动一致性测试，尤其适合需要一边执行一边派生测试步骤的场景。

### 需求前提

1. 规格能被压成 labelled transition system 语义。
2. SUT 可以通过 `Adapter` 暴露为可刺激、可观察的接口。
3. 团队关心的是输入输出一致性，而不是仅做代码覆盖率。
4. 用户接受测试驱动探索，而不是预先固定完整测试脚本。

### 不适用或高成本场景

如果系统高度依赖连续物理演化、复杂数据运算或 dense-time 约束，而又没有更强的前端抽象，`TorX` 的收益会明显下降。

## 与相邻形式主义的关系

相对 [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)，`TorX` 是更早的母线节点，核心是 `ioco` 与 `Explorer/Primer/Driver/Adapter` 骨架；相对 [t-uppaal-online-model-based-testing-of-real-time-systems/desc.md](../t-uppaal-online-model-based-testing-of-real-time-systems/desc.md)，`T-UPPAAL` 更偏 timed automata 在线测试，而 `TorX` 更偏一般 `IOLTS` 交互测试；相对 [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)，`UPPAAL TRON` 是后续实时特化工具线，`TorX` 则是更通用的 on-the-fly MBT 母框架。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明 LLM 生成出来的交互式状态机若能落成统一 transition-system 语义，就能直接接入在线测试链。
2. 它提醒 `project_1`：状态机落地不仅是“能验证”，还要考虑“能否被 Explorer/Adapter 化”。
3. 对闭环研究来说，`TorX` 展示了一个“模型 -> 测试 -> 失败轨迹”非常自然的后续环节。

### 作为目标形式主义还是中间表示

更像测试与分析基础设施，而不是最终交付的状态机本体。

## 重要的相关工作

1. [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)：`TorX` 的 Java 化后继工具线。
2. [t-uppaal-online-model-based-testing-of-real-time-systems/desc.md](../t-uppaal-online-model-based-testing-of-real-time-systems/desc.md)：timed automata 在线测试扩展线。
3. [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)：实时测试在工业案例上的落地证据。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 形式主义：`IOLTS / ioco / TorX`
- 论文角色：on-the-fly model-based testing / `ioco` test derivation and execution tool
- 归类理由：论文主体是基于 `ioco` 的在线测试派生与执行路线，主要贡献落在方法与工具闭环，而不是新的状态机本体。

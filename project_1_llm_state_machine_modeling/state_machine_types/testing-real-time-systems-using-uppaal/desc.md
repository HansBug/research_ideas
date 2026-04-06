# 基于 UPPAAL 的实时系统测试 / Testing Real-Time Systems Using UPPAAL

## 基本信息

- 标题：Testing Real-Time Systems Using UPPAAL
- 中文标题：基于 UPPAAL 的实时系统测试
- 作者：Anders Hessel，Kim G. Larsen，Marius Mikucionis，Brian Nielsen，Paul Pettersson，Arne Skou
- 发表：*Formal Methods and Testing*，`LNCS 4949`，pp. 77-117，2008
- DOI：`10.1007/978-3-540-78917-8_3`
- 链接：https://doi.org/10.1007/978-3-540-78917-8_3
- 形式主义：`timed automata / TIOTS / rtioco_e / UPPAAL-TRON`
- 主类：⏱️ 时间 / 时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed-automata-based model-based testing route with offline and online execution
- 工具/实现获取方式：原文明确依托 `UPPAAL` reachability engine 与 `UPPAAL-TRON` 在线测试器；`UPPAAL` 文档页提供该章 PDF 与 BibTeX，并说明 `TRON` 通过 adapter API 与黑盒 IUT 对接。
- 标准/格式获取方式：核心承载不是独立交换标准，而是 `UPPAAL` 风格 timed automata、observer automata、reachability queries、test automata 以及 `TRON` adapter 所消费的抽象输入/输出事件。

## 简报

这篇论文的核心贡献，不是再介绍一遍 `UPPAAL`，而是把 timed automata 真正扩成一条可执行的测试路线。它把实时系统测试拆成四层：用 `TIOTS` 和 `UPPAAL` timed automata 描述系统与环境，用 `rtioco_e` 定义“在给定环境下什么才算实现正确”，用 observer / reachability 生成离线测试，再用 `UPPAAL-TRON` 做在线测试与监控。

- 形式主义定位：围绕 timed automata 展开的实时黑盒一致性测试方法，而不是新的自动机本体。
- 构造方式简述：先把 IUT 需求与环境假设建成 `S` 与 `E` 两个 timed automata / `TIOTS`，再用 `rtioco_e` 与 observer automata 约束测试目标，最后落到 offline trace generation 或 online test execution。
- 基础设施与场景简述：依托 `UPPAAL` symbolic reachability、observer automata、test-case automata 与 `TRON` adapter，服务实时嵌入式控制器、协议栈与事件驱动反应系统的 conformance testing。

```text
系统需求 + 环境假设 -> TIOTS / timed automata -> rtioco_e + observer / reachability -> offline test cases or online TRON execution
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织整套测试语义：

1. timed input/output transition system (`TIOTS`)；
2. `UPPAAL` 风格 timed automata；
3. environment model `E` 与 system model `S` 的显式分离；
4. relativized timed conformance `rtioco_e`；
5. observer automata、coverage criteria 与 `UPPAAL-TRON`。

### 核心抽象

论文直接给出 `TIOTS` 骨架：

$$
S = (S, s_0, A_{in}, A_{out}, \rightarrow)
$$

上式中的符号逐项解释如下：

1. 第一个 `$S$` 是状态集合。
2. `$s_0$` 是初始状态。
3. `$A_{in}$` 与 `$A_{out}$` 分别是输入和输出动作集合。
4. `$\rightarrow \subseteq S \times (A_\tau \cup \mathbb{R}_{\ge 0}) \times S$` 是离散动作与时间延迟共同组成的转移关系。
5. 该关系满足 time determinism、time additivity 和 zero-delay 等约束。

论文同时给出 timed automaton 定义：

$$
M = (L, \ell_0, I, E)
$$

上式中的符号逐项解释如下：

1. `$L$` 是 location 集合。
2. `$\ell_0$` 是初始 location。
3. `$I : L \to G(X)$` 为每个 location 指定 clock invariant。
4. `$E \subseteq L \times G(X) \times A_\tau \times U(X) \times L$` 是带守卫、动作和时钟更新的边集合。
5. `$X$` 是时钟集合，`$G(X)$` 是时钟守卫，`$U(X)$` 是时钟更新。

### 一个最小例子与通俗解释

论文用触摸式灯控制器说明 timed testing 的直觉。一个最小例子可以表述成：

1. 系统有 `OFF / DIM / BRIGHT` 三个位置。
2. 用户通过 `touch?` 输入改变灯光档位。
3. 某些切换只能在 `$x < T_{sw}$` 的时间窗口内触发。
4. 测试器既要检查“灯是否最终切到正确档位”，也要检查“它是不是在允许的时间窗口里发生”。

通俗地说，这条路线像“把实时模型检查器改造成测试导演”。它不会只说模型是否可达，而是把环境、时序窗口、输入刺激和可接受输出一起编排成测试脚本。

### 运行 / 接受 / 转移语义

论文把可观测 timed trace 定义为：

$$
\mathrm{TTr}(s) = \{ \sigma \in (A \cup \mathbb{R}_{\ge 0})^\ast \mid s \xRightarrow{\sigma} \}
$$

上式中的符号逐项解释如下：

1. `$\sigma$` 是动作与时间延迟交替构成的可观测 timed trace。
2. `$\xRightarrow{\sigma}$` 是经过 `\tau` 抽象后的可达关系。
3. `$\mathrm{TTr}(s)$` 给出从状态 `$s$` 出发所有可执行的 timed traces。

其环境相对一致性关系定义为：

$$
s \;\mathrm{rtioco}_e\; t \iff \forall \sigma \in \mathrm{TTr}(e).\ \mathrm{Out}((s,e)\ \mathrm{After}\ \sigma) \subseteq \mathrm{Out}((t,e)\ \mathrm{After}\ \sigma)
$$

上式中的符号逐项解释如下：

1. `$e$` 是环境模型的某个状态。
2. `$\sigma \in \mathrm{TTr}(e)$` 表示只考察环境允许发生的 timed traces。
3. `$\mathrm{After}\ \sigma$` 表示执行 `$\sigma$` 后可能到达的状态集合。
4. `$\mathrm{Out}(\cdot)$` 给出当前状态集允许的输出动作或时间延迟。
5. 整个定义表达“实现只能做出规范在该环境下也允许的输出/延迟”。

离线测试又被落实为 test automaton 与 IUT 的组合：

$$
\mathrm{IUT\ passes}\ \lambda \iff A_\lambda \parallel A_I \not\to^\ast \mathrm{FAIL}
$$

上式中的符号逐项解释如下：

1. `$\lambda$` 是由 reachability trace 投影出来的测试序列。
2. `$A_\lambda$` 是该测试序列对应的 test-case automaton。
3. `$A_I$` 是 IUT 的抽象行为。
4. `$\not\to^\ast \mathrm{FAIL}$` 表示组合运行中无法到达失败 verdict。

### 语义边界

这条路线的边界相当明确：

1. 离线测试章节主要依赖 deterministic、weakly input-enabled、output-urgent 且 isolated-output 的 `TIOTS`。
2. 在线测试则是为 timed automata 不可确定化、且真实实现具有 timing uncertainty 的场景准备的。
3. `rtioco_e` 明确把环境建模当作第一等对象，因此它不是“对所有想象中的环境都成立”的绝对一致性。
4. 方法主体仍然是 timed / reactive 行为，不负责连续动力学或复杂概率语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TIOTS` 骨架 | `$S = (S, s_0, A_{in}, A_{out}, \rightarrow)$` | 给 timed testing 提供统一语义地基。 |
| 可观测 timed traces | `$\mathrm{TTr}(s) = \{ \sigma \mid s \xRightarrow{\sigma} \}$` | 所有测试、一致性与在线监控都围绕 trace 集展开。 |
| 环境相对一致性 | `$s \ \mathrm{rtioco}_e\ t$` | 区分“规范不允许”和“环境本来不可能发生”的行为。 |
| 离线测试 verdict | `$A_\lambda \parallel A_I \not\to^\ast \mathrm{FAIL}$` | 说明 reachability trace 如何真正转成测试执行器。 |
| 在线测试完备性 | `$\Pr(\mathrm{TestGenExe}=fail) \to 1$` | 在 digitization 假设下，随机在线测试对不一致实现最终能以概率 1 报错。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接建立在 `TIOTS` 与 timed automata 之上。 |
| 事件 / 触发 | 很强 | 输入/输出动作、同步动作和 `\tau` 都在主语义里。 |
| 守卫 / 数据 | 中等支持 | `UPPAAL` 守卫、整数变量和时钟更新都可用，但主体仍是 timed behavior。 |
| 层次 | 弱支持 | 核心路线不是层次状态机测试。 |
| 并发 / 同步 | 很强 | `UPPAAL` 网络组合、环境与系统并行组合是主线。 |
| 时间约束 | 很强 | 时间延迟、clock invariant、deadline、digitization 都是中心内容。 |
| 连续动态 / 随机性 | 不支持 | 不讨论 hybrid continuous dynamics 或概率模型。 |
| 可执行 / 可验证性 | 很强 | `UPPAAL` reachability、observer coverage、`TRON` 在线执行链都已打通。 |

### 形式化问题与性质

1. 这篇论文真正补出的不是“如何在 `UPPAAL` 里写一个模型”，而是“如何把 timed automata 规范、环境假设和测试 verdict 串成闭环”。
2. `rtioco_e` 的关键价值在于让测试只对现实环境负责，而不是对完全无约束环境负责。
3. observer automata 让 coverage / test purpose 不必直接污染原模型，这点对文库里的工具挂接尤其重要。

## 构造方式与承载格式

### 建模入口

论文中的典型入口包括：

1. `UPPAAL` network of timed automata；
2. 显式分离的 system model `S` 与 environment model `E`；
3. observer automata 或 reachability property；
4. adapter 侧抽象输入/输出事件。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UPPAAL` timed automata 模板与网络组合；
2. reachability queries；
3. observer automata；
4. test-case automata `$A_\lambda$`；
5. `TRON` 维护的 symbolic state set `$Z \subseteq S \times E$`。

### 交换与互操作

互操作重点在工具链而不在中立标准：

1. `UPPAAL` 负责 symbolic reachability 与 trace 生成。
2. `TRON` 通过 adapter API 与真实黑盒 IUT 对接。
3. monitor / emulator 可拆分成不同工具或不同机器分别执行。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` 用于 timed automata 建模、reachability 查询和 diagnostic trace 生成。
- 解析/交换/元模型支持：以 `UPPAAL` timed automata 网络、observer automata、测试序列 automata 为主；无独立行业交换标准。
- 仿真/执行支持：`TRON` 承担 environment emulation、online testing 和 monitoring。
- 验证/分析支持：离线 reachability-based test generation、coverage checking、在线 `rtioco_e` 一致性监控。
- 代码生成/转换支持：重点不在部署代码生成，而在 trace 到 test automaton 的转换及 adapter 集成。
- 标准化或社区生态：依托 `UPPAAL / UPPAAL-TRON` 研究生态，与 timed testing、model-based testing 社区相连。

## 适用场景与需求前提

### 适用场景

适合实时嵌入式控制器、协议实现、事件驱动设备以及任何可以用 timed automata 与环境假设共同描述的黑盒一致性测试场景。

### 需求前提

1. 系统与环境都能抽成 timed automata 或至少 `TIOTS`。
2. 关键正确性问题能写成 timed trace / output timing 是否允许。
3. 测试者愿意显式建环境模型，而不是默认“全宇宙所有输入都合理”。
4. 若做离线测试，规范最好满足文中对 determinism、input-enabledness 与 isolated outputs 的要求。

### 不适用或高成本场景

若系统核心是连续动力学、复杂概率语义，或输入输出时间戳难以可靠采集，这条路线的收益会明显下降；非常大的非确定 timed models 也会给在线 state-set 更新带来压力。

## 与相邻形式主义的关系

相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，这篇论文不再停留在 timed automata 建模与验证教程，而是把 `UPPAAL` 拉到 testing 语境；相对 [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)，`JTorX` 更偏一般在线 MBT 引擎，而本文专门处理 timed conformance；相对 [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)，本文是 `TRON` 路线的系统方法论母线，后者是工业案例验证。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“需求到状态机”之后，下一步完全可以不是直接做 model checking，而是先生成环境化测试工件。
2. 环境模型与系统模型分离的思想，对后续 LLM 生成状态机时如何编码假设条件很有启发。
3. observer-based coverage 也给“性质 / 场景生成”提供了很直接的接口。

### 作为目标形式主义还是中间表示

更适合作为实时验证与测试后端依赖的中间表示，而不是最终交给领域工程师的唯一前端记法。

### 对需求到模型生成的启发

1. 需求里若本身就有时限、等待窗口和环境假设，应该显式进模型，而不是留在自然语言注释里。
2. 测试目的和 coverage 不必直接写死在系统模型里，observer 方式更利于自动化生成。
3. 当目标是闭环“生成-验证-修复”时，monitor / emulator 分离是很实用的工程结构。

### 现实限制

该路线强依赖可靠的时间戳、adapter 和可执行环境模型；如果这些前提缺失，方法会迅速退化成理论上漂亮但难以落地的 testing story。

## 重要的相关工作

1. [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：`UPPAAL` timed automata 与 symbolic analysis 的通用入口。
2. [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)：在线模型驱动测试工具线。
3. [testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md](../testing-real-time-embedded-software-using-uppaal-tron-an-industrial-case-study/desc.md)：`UPPAAL-TRON` 工业落地案例。

## 文献分类总结

- 主类：⏱️ 时间 / 时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`timed automata / TIOTS / rtioco_e / UPPAAL-TRON`
- 论文角色：timed-automata-based model-based testing route with offline and online execution
- 归类理由：论文主体是在 `UPPAAL` timed automata 语义上建立实时一致性测试方法、coverage observer 和在线执行算法，典型属于 timed testing 方法路线条目。

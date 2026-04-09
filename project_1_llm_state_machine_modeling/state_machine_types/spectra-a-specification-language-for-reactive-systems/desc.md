# Spectra：面向反应式系统的规格语言 / Spectra: a specification language for reactive systems

## 基本信息

- 标题：Spectra: a specification language for reactive systems
- 中文标题：Spectra：面向反应式系统的规格语言
- 作者：Shahar Maoz，Jan Oliver Ringert
- 发表：*Software and Systems Modeling*，20(5):1553-1586，2021
- DOI：`10.1007/s10270-021-00868-z`
- 链接：https://doi.org/10.1007/s10270-021-00868-z
- 形式主义：`Spectra / GR(1) reactive synthesis / Spectra Tools`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：reactive-synthesis specification language with kernel semantics, supporting analyses, and benchmark collections
- 工具/实现获取方式：原文明确给出 `Spectra Tools` 与 language website，可通过 `http://smlab.cs.tau.ac.il/syntech/spectra/` 获取语言、工具和示例规格。
- 标准/格式获取方式：主体承载是 `Spectra` 文本 DSL、kernel grammar、扩展语法、Eclipse/CLI toolchain 与 BDD-level semantics；不是独立行业交换标准。

## 简报

`Spectra` 的贡献不只是“再做一个 `GR(1)` 前端”，而是把 reactive synthesis 真正需要的规格表达、语义下沉、调试分析和执行桥接放到同一条工程链路里。论文的核心主张是：如果只暴露裸 `GR(1)` kernel，工程师很难稳定写出复杂但可综合的规格；因此需要在保留 kernel 可判定性的同时，向上提供 predicates、monitors、patterns、bounded counters、quantified arrays、imports 等高层构造。

- 形式主义定位：面向 reactive synthesis 的文本 DSL 与工具链基础设施，而不是新的自动机母型。
- 构造方式简述：`Spectra` 文本规格先下沉到 kernel，再翻译成 `GR(1)` synthesis problem，之后由 `Spectra Tools` 做 realizability、synthesis、execution 和 unrealizability-oriented analyses。
- 基础设施与场景简述：依托 Eclipse editor、CLI、BDD-level semantic representation、自研 synthesizer 与 `SYNTECH` benchmark collections，服务反应式软件与机器人控制规格工程。

```text
structured reactive requirements -> Spectra language constructs -> Spectra kernel -> GR(1) synthesis problem -> realizability / controller synthesis / debugging / execution
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `GR(1)` synthesis problem 的结构化前端；
2. `Spectra kernel`；
3. 语言扩展构造，如 predicates、monitors、patterns、bounded counters、quantified arrays；
4. `Spectra Tools` 的分析、执行和调试链路；
5. `SYNTECH` 规格集合。

### 核心抽象

论文直接把 `GR(1)` synthesis problem 写成一组环境/系统变量、初始条件、转移约束和 justice 条件。可直接整理为：

$$
\mathcal{G} = (X, Y, \theta_e, \theta_s, \rho_e, \rho_s, \{J_i^e\}_{i=1}^n, \{J_j^s\}_{j=1}^m)
$$

上式中的符号逐项解释如下：

1. `$X$` 是环境控制的 Boolean 输入变量集合。
2. `$Y$` 是系统控制的 Boolean 输出变量集合。
3. `$\theta_e$` 与 `$\theta_s$` 分别是环境和系统的初始断言。
4. `$\rho_e$` 与 `$\rho_s$` 分别约束环境和系统的转移关系。
5. `$\{J_i^e\}_{i=1}^n$` 是环境 justice assumptions。
6. `$\{J_j^s\}_{j=1}^m$` 是系统 justice guarantees。

`Spectra kernel` 的语义就是把规格翻译成这样的 `GR(1)` 问题。论文对 strict realizability 给出如下骨架：

$$
\varphi_{sr} = (\theta_e \rightarrow \theta_s) \land (\theta_e \land G\rho_e \rightarrow ((\bigwedge_{i=1}^{n} GF J_i^e) \rightarrow (\bigwedge_{j=1}^{m} GF J_j^s)))
$$

上式中的符号逐项解释如下：

1. `$\varphi_{sr}$` 是 `Spectra` kernel 下沉后的 strict-realizability 规格骨架。
2. `$G$` 表示 always，`$GF$` 表示 infinitely often。
3. 环境只要满足初始条件和转移约束，并不断满足 justice assumptions，系统就必须满足相应保证。
4. 这一定义解释了为什么 `Spectra` 必须把高层语言构造最终翻回 `GR(1)` kernel。

论文还给出 kernel 级语义映射：

$$
m \mapsto \mathcal{G}(m)
$$

上式中的符号逐项解释如下：

1. `$m$` 是一个良构的 `Spectra` 规格。
2. `$\mathcal{G}(m)$` 是由该规格导出的 `GR(1)` synthesis problem。
3. `env` 声明映到 `$X$`，`sys` 声明映到 `$Y$`。
4. `ini / alw / alwEv` 形式的 assumptions 和 guarantees 分别映到 `$\theta$`、`$\rho$` 与 justice 集。

### 一个最小例子与通俗解释

论文最直接的例子是一个十字路口交通灯：

1. 环境变量 `carMain`、`carSide` 表示主路和支路是否来车。
2. 系统变量 `greenMain`、`greenSide` 表示两侧绿灯控制。
3. 规格要求两侧不能同时为绿，同时两侧来车后最终都应获得放行。
4. `Spectra` 允许工程师先用接近需求语言的 DSL 写这些约束，再由工具自动翻译到 `GR(1)`。

通俗地说，`Spectra` 像是“给 `GR(1)` 加了一层真正可写的工程语言”。普通 `GR(1)` kernel 像后端字节码，`Spectra` 则像带类型、宏、监视器和模式库的前端语言。

### 运行 / 接受 / 转移语义

`Spectra` 的核心语义不是“自己发明一套新执行机”，而是把所有高层构造翻回 kernel。论文明确指出：

$$
\text{monitors}, \text{patterns}, \text{counters}, \text{quantified arrays} \Rightarrow \text{Spectra kernel} \Rightarrow GR(1)
$$

上式中的符号逐项解释如下：

1. 左侧是 `Spectra` 提供给工程师使用的高层构造。
2. 中间是仅保留最小必要语义骨架的 kernel。
3. 右侧是最终求解所依赖的 `GR(1)` 语义域。

对 kernel 中 `next` 的语义，论文也给出明确说明：它把作用域内变量替换为 primed variables。因此，`Spectra` 的“运行语义”本质是标准时序逻辑和反应式博弈语义，而不是状态图解释器语义。

### 语义边界

1. `Spectra` 的 expressiveness 受制于其 `GR(1)` kernel；不是完整 `LTL` 或更一般时序逻辑语言。
2. 它擅长结构化 reactive requirements，不擅长连续动力学或 dense-time 约束。
3. 高层构造越丰富，越需要依赖工具做良构性检查、well-separation 检查和 unrealizability diagnosis。
4. 它是规格语言与 synthesis 工具链，不是最终部署时的运行时标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `GR(1)` 骨架 | `$\mathcal{G} = (X, Y, \theta_e, \theta_s, \rho_e, \rho_s, \{J_i^e\}, \{J_j^s\})$` | `Spectra` kernel 最终下沉的语义对象。 |
| strict realizability 骨架 | `$\varphi_{sr} = (\theta_e \rightarrow \theta_s) \land (\theta_e \land G\rho_e \rightarrow ((\bigwedge GFJ_i^e)\rightarrow(\bigwedge GFJ_j^s)))$` | 说明语言最终服务于可综合的 reactive-game 语义。 |
| kernel 映射 | `$m \mapsto \mathcal{G}(m)$` | 每个良构 `Spectra` 规格都要翻到 `GR(1)`。 |
| 高层构造下沉 | `$\text{constructs} \Rightarrow \text{kernel} \Rightarrow GR(1)$` | 解释 predicates/monitors/patterns 等为何可保留而不破坏底层求解器。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 间接支持 | 主要通过变量、predicates、monitors 和模式约束描述 reactive states，而不是显式状态图。 |
| 事件 / 触发 | 很强 | `env/sys` 变量、next、patterns 等直接服务事件驱动 reactive behavior。 |
| 守卫 / 数据 | 很强 | 支持 bounded integers、arithmetic、arrays、predicates、quantification。 |
| 层次 | 弱支持 | 不是 `Statecharts/UML` 风格层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 通过多个输入/输出命题和组合约束表达同步关系，而不是组件代数。 |
| 时间约束 | 弱支持 | 有时序算子、PastLTL 和 counters，但不是 timed automata。 |
| 连续动态 / 随机性 | 不支持 | 不涉及连续微分方程或概率语义。 |
| 可执行 / 可验证性 | 很强 | realizability、synthesis、execution、cores、repairs、well-separation analyses 都已工程化。 |

### 形式化问题与性质

1. `Spectra` 的关键价值是“提高可写性但不放弃 `GR(1)` 可解性”。
2. 高层构造不是直接扩展求解器，而是先翻回 kernel，因此语言工程和求解器工程相对解耦。
3. `SYNTECH` collections 让它不只是 DSL 原型，而是带基准数据集的完整研究基础设施。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Spectra` 文本 DSL；
2. kernel constructs：`env / sys / asm / gar / ini / alw / alwEv`；
3. advanced constructs：predicates、monitors、patterns、counters、arrays、imports；
4. Eclipse editor 与 CLI。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Spectra` grammar 与 abstract syntax representation；
2. kernel-level `GR(1)` representation；
3. BDD-level semantic structures；
4. generated controllers 与 execution environments；
5. `SYNTECH15/17/19/20` collections。

### 交换与互操作

1. `Spectra` 主要面向自有 DSL 和工具链，不强调跨工具中立交换格式。
2. 其重要互操作方式是“语言前端 -> synthesis backend -> execution environment”。
3. 论文明确强调可以通过 Eclipse plug-ins 和 command line 双入口使用工具。

## 配套基础设施

- 建模/编辑工具：Eclipse editor，支持 outline、syntax coloring、type checks 和 specification completion。
- 解析/交换/元模型支持：rich AST、kernel translation、BDD-level semantics；原文未强调独立 exchange standard。
- 仿真/执行支持：提供多种 execution mechanisms，可把综合得到的 controller 接到 stand-alone Java 或 Lego NXT 等环境。
- 验证/分析支持：realizability、unrealizable core、counter-strategy、symbolic repairs、well-separation、monitor checks 等。
- 代码生成/转换支持：从 `Spectra` 规格到 correct-by-construction controller，再到不同执行环境；论文重点在 synthesis/execution bridge，不在通用嵌入式代码标准。
- 标准化或社区生态：`Spectra Tools`、`SYNTECH` benchmark collections、website、Eclipse/CLI 双形态共同构成主要生态。

## 适用场景与需求前提

### 适用场景

适合 reactive software、机器人任务控制、离散交互控制逻辑，以及希望把结构化需求直接接到 synthesis backend 的项目。

### 需求前提

1. 需求需要能够拆成环境输入与系统输出。
2. 规格主体最好可压成 `GR(1)` 或其可下沉的高层变体。
3. 团队愿意使用文本 DSL 而不是纯图形状态图。
4. 若使用 monitors、patterns、quantification 等高级构造，需依赖工具做静态检查和反例分析。

### 不适用或高成本场景

若需求核心是 dense time、连续动力学、复杂数值优化或概率行为，`Spectra` 就更适合作为外层规格配方，而不是唯一建模语言。

## 与相邻形式主义的关系

相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`Slugs` 更像 `GR(1)` 综合框架，而 `Spectra` 是更贴近工程师的规格语言前端；相对 [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md) 与 [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)，后两者是 `LTL`/`GR(1)` 综合后端路线，而 `Spectra` 提供的是结构化规格输入层；相对 [owl-a-library-for-omega-words-automata-and-ltl/desc.md](../owl-a-library-for-omega-words-automata-and-ltl/desc.md) 与 [rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md](../rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md)，这些工作更偏 logic-to-automata 工具，`Spectra` 则直接面向需求工程与综合工作流。

## 与本研究的关系

### 对 Project 1 的价值

1. 它非常接近“自然语言需求 -> 结构化规格 -> 可综合模型”这条主线。
2. `Spectra` 证明了 DSL 层和 synthesis 层最好分离：前者强调可写性，后者强调可解性。
3. 它内建的 unrealizability、repair 和 well-separation 分析，对后续“生成-验证-修复”闭环特别有参考价值。

### 作为目标形式主义还是中间表示

更适合作为高价值中间表示或规格前端，而不是最终部署时的控制器表示。

### 对需求到模型生成的启发

1. `LLM` 生成状态机时，不必直接输出低层自动机；可以先输出受控 DSL。
2. 高层模式库、monitors 和 quantified arrays 说明“结构化需求模板”值得单独建模。
3. 若后续要做修复，repair 建议和 unrealizable core 能直接成为反馈信号。

### 现实限制

`Spectra` 的工程可行性建立在 `GR(1)` kernel 上；超出该边界的 richer temporal requirements 仍然需要别的后端或降级策略。

## 重要的相关工作

### 奠基或前身工作

1. `GR(1)` synthesis：`Spectra` kernel 的直接理论蓝本。
2. Dwyer specification patterns：论文明确把其作为 patterns catalog 的重要来源。

### 同类型或同家族工作

1. [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)：`GR(1)` 综合框架。
2. [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)：一般 `LTL` 综合工具。
3. [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)：显式 `DPA/parity` 综合路线。

### 标准 / 格式 / 工具链工作

1. `RATSY`、`Open Promela`、`LTLMoP`、`MTSA/SGR(1)`：论文在 related work 中逐一讨论的相邻语言/工具。
2. `SYNTECH` collections：论文明确作为 benchmark infrastructure 向社区开放。

### 与本研究关系最紧的工作

1. [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)：说明 `GR(1)` synthesis 后端如何工程化。
2. [acacia-a-tool-for-ltl-synthesis/desc.md](../acacia-a-tool-for-ltl-synthesis/desc.md)：说明 richer `LTL` synthesis 与 `GR(1)` 工程化前端之间的差别。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Spectra / GR(1) reactive synthesis / Spectra Tools`
- 论文角色：reactive-synthesis specification language with kernel semantics, analyses, and benchmark collections
- 核心功能：把结构化 reactive requirements 编写、检查、综合、执行和修复建议统一到同一 DSL/toolchain
- 关键特性：kernel translation、predicates、monitors、patterns、counters、quantified arrays、BDD-based analyses、benchmark collections
- 构造方式：文本 DSL -> kernel -> `GR(1)` synthesis problem -> controller synthesis / execution
- 基础设施：Spectra website、Eclipse editor、CLI、`Spectra Tools`、`SYNTECH` collections
- 适用场景：反应式软件、机器人控制逻辑、需求到规格的结构化中间表示
- 归类理由：尽管论文包含语言本体定义，但其主要工程价值在“语言 + 工具 + benchmark”三位一体的可用基础设施，而非单纯理论模型提出。

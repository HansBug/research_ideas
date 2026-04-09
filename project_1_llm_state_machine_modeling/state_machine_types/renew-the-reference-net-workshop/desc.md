# Renew：Reference Net 工作台 / Renew -- The Reference Net Workshop

## 基本信息

- 标题：Renew -- The Reference Net Workshop
- 中文标题：Renew：Reference Net 工作台
- 作者：Lawrence Cabac，Michael Haustermann，David Mosteller
- 发表：*Proceedings of the International Workshop on Petri Nets and Software Engineering (PNSE'15)*，pp. 313-314，2015
- DOI：原文未提供
- 链接：https://ceur-ws.org/Vol-1372/paper18.pdf
- 形式主义：`Java Reference Nets / Renew`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 论文角色：reference-net IDE / simulation and plugin environment
- 工具/实现获取方式：原文明确给出 `http://www.renew.de/`，并说明发行包与 source code 可免费获取。
- 标准/格式获取方式：承载方式是 `Java reference nets`、plugin system、editor/simulator 内部格式、`LoLA` verification integration，以及可选 `UML/BPMN` plugins；无中立交换标准。

## 简报

这篇论文的重点，是把 `reference nets / nets-within-nets` 这条高层 Petri 网路线做成了一套可扩展 IDE。`Renew` 不只是一个能画网和跑 token 的小工具，而是围绕 Java reference nets、synchronous channels、plugin architecture、debugging、verification integration 和可选建模插件形成了一个长期演进的 net-based software engineering 环境。

- 形式主义定位：reference-net family 的执行与扩展载体，而不是新的 Petri 网本体母文。
- 构造方式简述：图形 editor + simulation engine + Java inscriptions + reference-net semantics + plugin extensions。
- 基础设施与场景简述：依托 `Java reference nets`、interactive/automatic simulation、`LoLA` integration 与可选 `UML/BPMN` plugins，服务并发软件、workflow 和 agent-oriented software engineering。

```text
reference-net model -> Renew editor -> interactive/automatic simulation -> debugging / LoLA verification / plugin-based extensions
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象介绍 `Renew`：

1. `Java reference nets`。
2. nets-within-nets、synchronous channels 与 reference semantics。
3. Java inscriptions。
4. 图形 editor、simulation engine 与 plugin architecture。
5. verification、monitoring、workflow/UML/BPMN 等扩展插件。

### 核心抽象

论文没有给出完整数学 tuple；结合其对 reference nets 的结构性描述，可保守整理为：

$$
\mathcal{N}_{ref} = (P, T, F, \mathcal{O}, Ref, Chan, Inscr)
$$

上式中的符号逐项解释如下：

1. `P` 是 places 集合。
2. `T` 是 transitions 集合。
3. `F` 是 arcs 集合。
4. `\mathcal{O}` 是可被 token 引用或承载的 net instances 集合。
5. `Ref` 表示 nets-within-nets/reference semantics。
6. `Chan` 表示 synchronous channels。
7. `Inscr` 表示用 Java 编写的 inscriptions 与动作。

若从工具基础设施角度抽象，则可写成：

$$
\mathrm{Renew} = (Editor, Simulator, Plugins, Formalisms)
$$

上式中的符号逐项解释如下：

1. `Editor` 是图形化建模环境。
2. `Simulator` 是 interactive/automatic simulation engine。
3. `Plugins` 是 core 与 optional plugin 集。
4. `Formalisms` 是工具支持的网模型家族与附加建模技术。

### 一个最小例子与通俗解释

最容易理解的 reference-net 直觉是“token 自己也可以是一个可被引用的网对象”：

1. 外层网中的一个 token 不一定只是黑点，它可以代表一个正在运行的 net instance。
2. 外层 transition 触发时，不只是移动 token，还可能通过 synchronous channel 与内部 net 交互。
3. Java inscriptions 可以把对象属性、调用和条件判断写进 transition logic。
4. 最终建模效果会更像“对象化的 Petri 网系统”，而不是单层 token 流图。

通俗地说，`Renew` 像“把 Petri 网做成了支持对象、插件和 IDE 级调试的编程环境”。

### 运行 / 接受 / 转移语义

结合论文对 simulator 的说明，reference-net firing 可保守写成：

$$
M \xrightarrow{t} M' \iff pre_t \subseteq M \land guard_t(M)=true \land sync_t(M)=true
$$

上式中的符号逐项解释如下：

1. `M` 是当前 marking / net-instance configuration。
2. `pre_t` 表示 transition `t` 所需的输入 token 或引用对象。
3. `guard_t(M)` 表示 Java inscription 与普通 guard 的求值结果。
4. `sync_t(M)` 表示 synchronous channels 与 referenced nets 侧条件均满足。
5. `M'` 是 firing 后的新 marking / instance configuration。

若从工具交互角度写，可保守整理为：

$$
\mathrm{Run}_{mode}(\mathcal{N}_{ref}) \to Trace
$$

其中：

1. `mode \in \{interactive, automatic\}`。
2. `interactive` 允许用户逐步选 transition、设断点、手动控制 firing。
3. `automatic` 允许无图形或带图形反馈地执行 reference-net model。

### 语义边界

这篇论文的边界也很清楚：

1. 它是工具总览文，不是 reference nets 数学语义全文。
2. 强能力建立在 `Renew` 自身生态上，不是开放标准。
3. Java inscriptions 增强了工程表达力，也引入了实现依赖。
4. verification 通过 `LoLA` 等集成完成，但不意味着所有网模型都自动获得统一分析保证。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| reference-net 骨架 | `$\mathcal{N}_{ref} = (P, T, F, \mathcal{O}, Ref, Chan, Inscr)$` | 论文强调的是 object-like net instances、channels 与 inscriptions 共同构成的高层网。 |
| 工具骨架 | `$\mathrm{Renew} = (Editor, Simulator, Plugins, Formalisms)$` | `Renew` 的主体价值在于可扩展 IDE，而不只是一个单功能 simulator。 |
| firing 语义 | `$M \xrightarrow{t} M' \iff pre_t \subseteq M \land guard_t(M)=true \land sync_t(M)=true$` | transition firing 同时受 token、Java 条件和 channel/reference 约束。 |
| 运行模式 | `$\mathrm{Run}_{mode}(\mathcal{N}_{ref}) \to Trace$` | 同一模型既能交互式调试，也能自动执行与记录。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 主要对象仍是 net marking 与 net instances。 |
| 事件 / 触发 | 中等支持 | transition firing 与 synchronous channels 共同驱动。 |
| 守卫 / 数据 | 很强 | Java inscriptions 提供了丰富的数据与行为表达。 |
| 层次 | 很强 | nets-within-nets 与 reference semantics 是主线。 |
| 并发 / 同步 | 很强 | Petri 网并发加 synchronous channels 同时具备。 |
| 时间约束 | 部分支持 | 可通过 timed arcs 等扩展插件支持，但不是本文主轴。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散并发网。 |
| 可执行 / 可验证性 | 很强 | editor、debugging、simulation、`LoLA` verification 和 monitoring 都已落地。 |

### 形式化问题与性质

1. `Renew` 的意义，不只是“又一个 Petri 网工具”，而是 reference-net line 的长期工程承载点。
2. Java inscriptions 让它更适合 net-based software engineering，而不只是纯教学级建模。
3. plugin architecture 使它逐步吸纳了 workflow、UML、BPMN、meta-modeling 与 distributed simulation 等方向。

## 构造方式与承载格式

### 建模入口

原文中的典型建模入口是：

1. 在图形 editor 中建立 reference-net model。
2. 给 transitions 加 Java inscriptions。
3. 需要时启用 workflow、timed arcs 或其他 optional plugins。
4. 在 interactive 或 automatic simulation 模式下执行模型。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Java reference nets`。
2. referenced net instances 与 synchronous channels。
3. Java inscriptions。
4. core/optional plugins 暴露的附加 formalisms。
5. `LoLA` verification 与 monitoring integration。

### 交换与互操作

这篇论文的互操作重点在插件，而不是开放标准：

1. `Renew` 本体通过 plugin system 向多种网形式和建模技术扩展。
2. 可选 plugins 支持 workflow nets、`UML`、`BPMN` 等。
3. 还支持 remote monitoring、distributed simulation 和把 `Renew` 作为 library/service 使用。

## 配套基础设施

- 建模/编辑工具：图形 editor、syntax checking、desktop integration、file navigator、image export。
- 解析/交换/元模型支持：plugin-based formalism support；原文未给中立交换格式。
- 仿真/执行支持：interactive simulation、automatic simulation、dynamic loading、logging、remote monitoring。
- 验证/分析支持：`LoLA` integration、debugging、breakpoints、manual transitions。
- 代码生成/转换支持：论文主线不是代码生成，而是 simulation-centric IDE 与扩展性。
- 标准化或社区生态：`renew.de` 发布、source code、core/optional plugins 与长期研究社区维护。

## 适用场景与需求前提

### 适用场景

适合并发软件、workflow、agent-oriented software engineering、以及需要把高层网建模与可执行 IDE 结合起来的场景。

### 需求前提

1. 系统天然适合 Petri 网式 token/transition 思维。
2. 需要对象化、嵌套网或同步 channel，而不是只要平面 `P/T` 网。
3. 团队愿意接受 `Java` 作为 inscription language 与 `Renew` 生态。
4. 希望通过 plugins 逐步扩展能力。

### 不适用或高成本场景

如果目标只是最小、标准化、跨工具可交换的网模型，`Renew` 这种强生态绑定工具会比中立格式更重。

## 与相邻形式主义的关系

相对 [pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md](../pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md)，`Renew` 走的是 `reference nets / nets-within-nets` 路线，而不是一般 high-level PN editor；相对 [coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md](../coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md)，它更强调对象化与插件化；相对 [multi-robot-motion-planning-based-on-nets-within-nets-modeling-and-simulation/desc.md](../multi-robot-motion-planning-based-on-nets-within-nets-modeling-and-simulation/desc.md)，本文正是那条 `Renew`-based nets-within-nets 应用线的工具锚点。

## 与本研究的关系

### 对 Project 1 的价值

它证明了某些高层 Petri 网分支不仅有理论名字，还有持续维护的执行环境和插件生态。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，这更像 `Petri Net / reference net` 方向的目标执行与实验载体，而不是通用中间表示。

### 对需求到模型生成的启发

1. 若后续要生成高层网，不应只生成网结构，还要考虑 token data/object semantics 和 execution environment。
2. “一篇工具论文能否入库”的关键标准之一，就是是否把模型变成可模拟、可调试、可验证的持久载体；`Renew` 是正例。
3. 对并发系统建模，object-oriented Petri net 视角可以补足传统状态机对资源流和并发实例表达的短板。

### 现实限制

`Renew` 的表达力与工程性很强，但也更依赖其自身生态；如果研究目标是跨工具标准化交换，就需要另找 `PNML` 或更中立的承载层。

## 重要的相关工作

- [pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md](../pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md)：另一条高层 Petri 网工具锚点。
- [coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md](../coloured-petri-nets-and-cpn-tools-for-modelling-and-validation-of-concurrent-systems/desc.md)：typed-token Petri net 工具母线。
- [multi-robot-motion-planning-based-on-nets-within-nets-modeling-and-simulation/desc.md](../multi-robot-motion-planning-based-on-nets-within-nets-modeling-and-simulation/desc.md)：`Renew` 在 nets-within-nets 方向上的近期应用证据。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Java Reference Nets / Renew`
- 论文角色：reference-net IDE / simulation and plugin environment

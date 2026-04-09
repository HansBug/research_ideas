# 嵌入式 UML 模型执行：打通设计与运行时之间的语义鸿沟 / Embedded UML Model Execution to Bridge the Gap between Design and Runtime

## 基本信息

- 标题：Embedded UML Model Execution to Bridge the Gap between Design and Runtime
- 中文标题：嵌入式 UML 模型执行：打通设计与运行时之间的语义鸿沟
- 作者：Valentin Besnard，Matthias Brun，Frédéric Jouault，Ciprian Teodorov，Philippe Dhaussy
- 发表：*Software Technologies: Applications and Foundations*，pp. 519-528，2018
- DOI：`10.1007/978-3-030-04771-9_38`
- 链接：https://doi.org/10.1007/978-3-030-04771-9_38
- 形式主义：`UML State Machine / bare-metal model interpreter`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：embedded UML interpreter / design-runtime bridge
- 工具/实现获取方式：原文介绍了一套可在桌面端或微控制器上运行的 UML 模型解释器、模拟器与 trace 生成链路，并说明可配合 `Papyrus`、`tUML` 和 `PlantUML` 使用；正文未给独立公开仓库。
- 标准/格式获取方式：承载方式是 UML 模型导出的 `XMI`、转译得到的 `C struct initializer`、基于 `C` 的 action language、解释器 configuration 协议与 `PlantUML` 风格 `MSC` traces；无独立中立交换标准。

## 简报

这篇论文的核心价值，不在于再定义一种新的状态机语言，而在于把 UML 设计模型直接放到嵌入式目标上解释执行，从而避免传统代码生成带来的 design-runtime semantic gap。作者把设计阶段的 UML 模型序列化成 `C` 里的静态数据，再交给解释器按接近 `PSSM/fUML` 的语义执行，因此仿真、调试、trace 和运行时观察都仍然以 UML 元素为参照。

- 形式主义定位：`UML State Machine` 的执行载体与运行时桥接链路，而不是新的状态机本体。
- 构造方式简述：`Papyrus/tUML -> XMI -> C struct initializers + guard/effect functions -> bare-metal interpreter`。
- 基础设施与场景简述：依托解释器、configuration 协议、模拟器与 `PlantUML` 轨迹生成，为嵌入式 UML 设计模型提供 simulation、debugging、hardware-in-the-loop 和 runtime traceability。

```text
UML design model -> XMI -> interpreter runtime model -> online simulation/debugging protocol -> MSC trace / embedded execution
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织其执行链：

1. 由 active classes、state machines、guards 和 effects 组成的 UML 设计模型。
2. 设计模型导出的 `XMI` 文件。
3. 解释器中的静态模型数据与动态 configuration。
4. 用于 simulation/debugging 的 application-layer protocol。
5. 运行时 trace 与 `MSC` 图。

### 核心抽象

结合论文对“静态模型 + 动态 configuration”的说明，可把解释执行对象保守整理为：

$$
\mathcal{R} = (U, \sigma)
$$

上式中的符号逐项解释如下：

1. `U` 是由 UML 设计模型序列化得到的静态模型骨架。
2. `\sigma` 是运行时 configuration，即动态部分。
3. `\mathcal{R}` 是真正被解释器执行的 runtime model。

论文明确说明 configuration 至少包含：

$$
\sigma = (C, Q, A)
$$

上式中的符号逐项解释如下：

1. `C` 是各 active object 当前 state machine 的 current states。
2. `Q` 是各 active object 的 event pools。
3. `A` 是 attributes 的当前取值。

模型加载并不是传统代码生成，而是“只改表示、不改语义”的序列化，可保守写成：

$$
\mathrm{Ser}_{xmi\to c} : U_{xmi} \to U_{c}
$$

上式中的符号逐项解释如下：

1. `U_{xmi}` 是 `XMI` 中的 UML 模型。
2. `U_{c}` 是由 `C struct initializers` 表达的同一模型静态表示。
3. 论文强调该过程不做语义变换，只做语法适配与 compile-time loading。

### 一个最小例子与通俗解释

论文用 level crossing system 贯穿说明：

1. `Controller`、`Gate`、`TrackCircuit`、`RoadSign` 和 `Train` 这些 active objects 各自带有 UML state machine。
2. 模型被导出为 `XMI` 后，序列化成 `C` 里的静态数据。
3. 解释器运行时维护“当前在哪些状态、事件池里有什么事件、属性现在是什么值”。
4. 模拟器可以读取 configuration、列出 fireable transitions，并生成 `MSC` 来展示对象间的事件交换和状态推进。

通俗地说，这套方案像“把 UML 图直接变成可跑的数据模型”，而不是先把 UML 消化掉再重新生成另一套与 UML 脱节的手写逻辑。

### 运行 / 接受 / 转移语义

论文给出的关键在线协议接口可以形式化整理为：

$$
\mathrm{GetConfig}(\mathcal{R}) = \sigma
$$

$$
\mathrm{Fireable}(U,\sigma) = \{ t \mid enabled(t,\sigma) \}
$$

$$
(U,\sigma) \xrightarrow{t} (U,\sigma') \iff t \in \mathrm{Fireable}(U,\sigma)
$$

上式中的符号逐项解释如下：

1. `\mathrm{GetConfig}` 返回解释器当前 configuration。
2. `\mathrm{Fireable}` 收集下一步可触发的 transitions。
3. `t` 是某个 active object state machine 上的可触发 transition。
4. `\sigma'` 是执行 `t` 后得到的新 configuration。

如果从 protocol 视角描述运行时控制，则可进一步写成：

$$
\sigma' = \mathrm{SetConfig}(U,\sigma,\Delta)
$$

其中：

1. `\Delta` 表示外部对 configuration 的修改，例如写入事件、改属性值或直接替换当前状态。
2. 这就是 simulation/debugging 模式下的在线干预接口。
3. 论文说明 `diff mode` 只是优化传输粒度，不改变上述状态更新语义。

### 语义边界

这篇论文的边界也很明确：

1. 它实现的是接近 `PSSM`、基于 `fUML` 的解释语义，而不是 OMG 完整执行标准的正式实现证明。
2. guards 和 effects 被编译成 `C` 函数，因此当前不能像模型元素那样逐步调试其内部。
3. 当前 prototype 缺少真正的 breakpoint 机制。
4. 目标是 small embedded devices 上的 bare-metal 执行，复杂 OS 级运行时不是论文重点。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| runtime model | `$\mathcal{R} = (U, \sigma)$` | 运行时对象由静态 UML 模型和动态 configuration 组成。 |
| configuration | `$\sigma = (C, Q, A)$` | 当前状态、事件池和属性值是一等运行时数据。 |
| 序列化加载 | `$\mathrm{Ser}_{xmi\to c} : U_{xmi} \to U_c$` | `XMI` 到 `C` 的过程是表示转换，不是语义改写。 |
| 可触发边集合 | `$\mathrm{Fireable}(U,\sigma) = \{ t \mid enabled(t,\sigma) \}$` | 模拟器可以直接列出下一步可执行的 UML transitions。 |
| 解释执行步 | `$(U,\sigma) \xrightarrow{t} (U,\sigma')$` | 运行时步进仍以 UML transition 为最小观察单位。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | active classes 的行为直接由 UML state machines 承载。 |
| 事件 / 触发 | 很强 | event pools 与 send-event 语义是解释器核心。 |
| 守卫 / 数据 | 强支持 | guard/effect 通过 `C` 风格 action language 与 attribute valuation 落地。 |
| 层次 | 中等支持 | 依赖 UML state machine 结构本身，论文重点不在层次理论扩展。 |
| 并发 / 同步 | 中等支持 | 多 active objects 并行推进，并通过事件交互。 |
| 时间约束 | 弱支持 | 论文核心不是 timed semantics，而是 design-runtime bridge。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散 UML 执行。 |
| 可执行 / 可验证性 | 很强 | simulation、debugging、runtime execution 与 trace generation 同时具备。 |

### 形式化问题与性质

1. 论文最重要的贡献，是把“执行结果仍然直接对应设计模型元素”这件事做成了工程现实。
2. `XMI -> C struct initializer` 的路线，本质是 compile-time model loading，而不是把状态机翻译成另一种程序控制流。
3. `MSC` traces 直接以 UML active objects 和 states 呈现，是设计可追踪性的重要补点。

## 构造方式与承载格式

### 建模入口

原文中的典型建模入口是：

1. 用 `Papyrus` 或 `tUML` 建立 UML 设计模型。
2. 用 UML state machines 指定 active classes 的行为。
3. 用基于 `C` 的 action language 填写 guards 与 effects。
4. 导出 `XMI`，交给 serializer 与 interpreter。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `XMI` 导出的 UML 模型。
2. `C struct initializers` 表达的静态模型骨架。
3. guard/effect 对应的 `C` 函数。
4. configuration 协议消息与 `diff mode`。
5. `PlantUML` 风格 `MSC` trace 文本。

### 交换与互操作

这篇论文的互操作重点在“设计工具和运行时之间的低鸿沟”：

1. 设计入口兼容图形化 `Papyrus` 和文本化 `tUML`。
2. 中间承载固定为 `XMI`。
3. 运行后生成的 traces 还能继续流入 `PlantUML` 做时序/状态可视化。

## 配套基础设施

- 建模/编辑工具：`Papyrus`、`tUML`。
- 解析/交换/元模型支持：`XMI` 导出与 `C struct initializer` 序列化加载。
- 仿真/执行支持：桌面端与 bare-metal 微控制器上的 UML model interpreter。
- 验证/分析支持：simulation、configuration inspection、hardware-in-the-loop exploration 与 trace replay。
- 代码生成/转换支持：不是经典代码生成，而是静态模型序列化加解释执行。
- 标准化或社区生态：依托 `UML`、`XMI`、`PSSM/fUML` 与 `PlantUML` 周边生态；原文未给完整公开实现仓库。

## 适用场景与需求前提

### 适用场景

适合希望在设计阶段就把 UML 模型直接跑起来，并且在运行时仍然以设计模型视角观察系统行为的嵌入式开发流程。

### 需求前提

1. 行为逻辑已经稳定落到 UML active classes 与 state machines 上。
2. guards 和 effects 可以接受 `C` 风格 action language。
3. 目标平台允许解释执行开销，而不是只能接受极致优化的手写代码。
4. 团队重视 traceability、simulation、debugging 和 runtime explainability。

### 不适用或高成本场景

如果目标是极低开销、极高实时性或高度平台特化的最终固件，这种解释执行路线会比直接代码生成更重。

## 与相邻形式主义的关系

相对 [uml-251-specification/desc.md](../uml-251-specification/desc.md)，它补的是 UML 状态机如何被直接执行；相对 [safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md](../safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md)，它是从 `UML -> runtime`，而后者是从已验证 `UPPAAL -> Stateflow/implementation`；相对 [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)，它是后者的执行基础层。

## 与本研究的关系

### 对 Project 1 的价值

它说明 UML 状态机不只是“需求建模图”，也可以是实际执行和诊断时仍保留语义一致性的运行时资产。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，这更像“目标执行载体如何保持与中间表示一致”的关键证据，而不是新的中间表示候选。

### 对需求到模型生成的启发

1. 若未来让 LLM 生成 UML 状态机，仅生成图还不够，还要考虑 event pool、attribute valuation 和 guard/effect 承载方式。
2. traceability 不应只停留在离线文档层，运行时协议和 trace 格式本身也是模型闭环的一部分。
3. 设计模型若能直接进入 runtime，后续验证、修复和解释都更容易形成闭环。

### 现实限制

论文展示的是 prototype 级执行链；要进入大规模工业部署，仍需要更完整的调试语义、性能评估和开放实现。

## 重要的相关工作

- [uml-251-specification/desc.md](../uml-251-specification/desc.md)：`UML State Machine` 的标准化元模型入口。
- [statemate-a-working-environment-for-the-development-of-complex-reactive-systems/desc.md](../statemate-a-working-environment-for-the-development-of-complex-reactive-systems/desc.md)：更早的 design-to-execution integrated environment 思路。
- [safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md](../safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md)：另一条“已验证模型 -> 实现载体”的桥接线。
- [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)：把抽象/具体环境切换和部署模块化的后续工作。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML State Machine / bare-metal model interpreter`
- 论文角色：embedded UML interpreter / design-runtime bridge

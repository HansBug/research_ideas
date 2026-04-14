# BlueState：基于元模型的 UML 状态机执行框架 / BlueState: A Metamodel-based Execution Framework for UML State Machines

## 基本信息

- 标题：BlueState - A Metamodel-based Execution Framework for UML State Machines
- 中文标题：BlueState：基于元模型的 UML 状态机执行框架
- 作者：Alfredo Ortigosa，Carlos Rossi
- 发表：*ICSOFT 2011 - Proceedings of the 6th International Conference on Software and Data Technologies, Volume 2*，pp. 226-231，2011
- DOI：`10.5220/0003609202260231`
- 链接：https://doi.org/10.5220/0003609202260231
- 形式主义：`UML State Machine / BlueState class-metamodel execution framework`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：`UML` 状态机导入、代码生成、调试与监控一体化执行框架
- 工具/实现获取方式：原文明确说明 `BlueState` 包含 `XMI` parser、代码生成引擎、simulator/debugger 和 real-time visual monitoring 模块；正文未给独立公开仓库。
- 标准/格式获取方式：核心承载是 `UML` 元模型、`XMI` 文档、基于 `.NET CodeDOM` 的目标代码中间结构、event dispatcher 和 Enterprise Architect add-in；无独立中立交换标准。

## 简报

`BlueState` 的价值不在于定义一种新的状态机，而在于把 `UML State Machine` 做成可导入、可生成、可调试、可实时监控的工程执行载体。作者以类元模型为核心，把 `XMI` 中的状态图导成内存对象，再经 `CodeDOM` 生成多种目标语言代码，并补了 simulator、execution log 和 Enterprise Architect 实时可视化监控。

- 形式主义定位：`UML State Machine` 的执行与监控基础设施，而不是新的状态机语言。
- 构造方式简述：`UML/XMI -> class metamodel -> CodeDOM intermediate structure -> target language partial classes`。
- 基础设施与场景简述：依托 `XMI`、类元模型、event dispatcher、simulator/debugger 和 visual monitoring，服务真实软件开发中的状态机实现、维护与运行时追踪。

```text
UML state diagram -> XMI -> BlueState class metamodel -> code generation / simulation / monitoring -> deployed software
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML State Machine` 图。
2. 导出的 `XMI` 文档。
3. 与 `UML` 元模型对齐的 class metamodel。
4. `CodeDOM` 目标无关中间结构。
5. event dispatcher、simulator/debugger 与 visual monitoring 模块。

### 核心抽象

结合论文对执行框架的描述，可把 `BlueState` 保守整理为：

$$
\mathcal{B} = (U, X, CM, G, D, M)
$$

上式中的符号逐项解释如下：

1. `U` 是原始 `UML` 状态机模型。
2. `X` 是由建模工具导出的 `XMI` 文档。
3. `CM` 是与 `UML` 元模型对齐的 class metamodel 对象表示。
4. `G` 是目标无关的代码生成结构与生成器。
5. `D` 是确保 run-to-completion 的 event dispatcher。
6. `M` 是 simulator、debugger 与 visual monitoring 相关模块。

论文的导入主线可保守写成：

$$
\mathrm{Parse}_{xmi}(X) = CM(U)
$$

上式中的符号逐项解释如下：

1. `X` 是导出的 `XMI`。
2. `\mathrm{Parse}_{xmi}` 是 `BlueState` 的 `XMI` parser。
3. `CM(U)` 是落到内存中的 class metamodel 对象。
4. 论文强调此处还会对 `UML` 元模型约束做校验。

代码生成主线则可写成：

$$
\mathrm{CodeDOM}(CM,\ell) \to P_{\ell}
$$

其中：

1. `CM` 是导入后的元模型对象。
2. `\ell` 是目标语言，例如 `C#` 或 `Visual Basic .NET`。
3. `P_{\ell}` 是最终生成的目标语言 partial classes。
4. 论文明确说 `BlueState` 依托 `.NET CodeDOM` 保持目标语言独立性。

### 一个最小例子与通俗解释

论文给了一个典型小片段：

1. 创建 `StateB`。
2. 创建 `Transition` 并把 `Source` 设为 `StateB`。
3. 创建 `CallEvent_EVENTB`。
4. 把该事件绑定到 `EvDispatcher_ED1`。

通俗地说，`BlueState` 的想法是：先把 `UML` 图里的状态、迁移、事件都变成与元模型一一对应的对象，再由这些对象去生成代码和驱动运行时，而不是直接用手写模板把图粗暴压平成 `if-else`。

### 运行 / 接受 / 转移语义

论文明确指出，事件处理由 dispatcher 保证 run-to-completion，因此可保守写成：

$$
(s,e,\nu) \xrightarrow{D} (s',\nu')
$$

上式中的符号逐项解释如下：

1. `s` 与 `s'` 是迁移前后的活动状态。
2. `e` 是当前接收到的事件。
3. `\nu` 与 `\nu'` 是相关 guard、action 和对象属性的取值。
4. `D` 表示 `BlueState` event dispatcher 的调度语义。
5. 论文强调 dispatcher 的作用就是保证 run-to-completion。

论文还把初始化与执行封装成两个固定入口，因此可保守写成：

$$
\mathrm{Init}(CM) \to SMinit(),\quad \mathrm{Run}(CM) \to SMRun()
$$

其中：

1. `SMinit()` 对应状态机初始化。
2. `SMRun()` 对应持续执行。
3. 这是生成代码暴露给业务类的最小运行接口。

### 语义边界

`BlueState` 的边界主要有：

1. 它依赖 `UML` 状态机和 `XMI` 导出质量。
2. 它强调工程实现、维护与监控，不是形式验证理论。
3. 代码生成仍要与建模工具中 guard / operation 的命名方式协同。
4. 目标是尽量接近 `UML` 元模型，而不是发明新的状态机语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
| --- | --- | --- |
| 框架骨架 | `$\mathcal{B} = (U, X, CM, G, D, M)$` | `BlueState` 把模型、导入、生成和监控统一进一套执行框架。 |
| `XMI` 导入 | `$\mathrm{Parse}_{xmi}(X) = CM(U)$` | `UML/XMI` 被恢复成对齐元模型的对象结构。 |
| 代码生成 | `$\mathrm{CodeDOM}(CM,\ell) \to P_{\ell}$` | 同一元模型可面向不同目标语言生成代码。 |
| 运行步 | `$(s,e,\nu) \xrightarrow{D} (s',\nu')$` | dispatcher 负责事件接收和 run-to-completion 执行。 |
| 固定入口 | `$\mathrm{Init}(CM) \to SMinit(),\ \mathrm{Run}(CM) \to SMRun()$` | 生成代码对外提供统一初始化和执行接口。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
| --- | --- | --- |
| 状态 / 模式 | 强支持 | 覆盖 simple/composite states、initial/final pseudostates。 |
| 事件 / 触发 | 强支持 | call events、signals 与 dispatcher 都是核心。 |
| 守卫 / 数据 | 强支持 | guards、entry/exit/doActivity 与 target code 紧密结合。 |
| 层次 | 强支持 | 明确支持 composite states、regions 与 history pseudostates。 |
| 并发 / 同步 | 中等支持 | 支持并发执行状态机与异步/同步事件发送。 |
| 时间约束 | 不突出 | 重点是执行和监控，不是显式时钟建模。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散 `UML` 状态机。 |
| 可执行 / 可验证性 | 强执行、弱验证 | simulation、debugging 与 real-time monitoring 很强；形式验证不是重点。 |

### 形式化问题与性质

1. `BlueState` 的真正补点，是把 `UML` 状态机执行从“一次性代码生成”推进成“可维护的运行时资产”。
2. `CodeDOM + partial classes` 让生成代码与手写业务代码之间有明确分界，这对软件维护尤其重要。
3. visual monitoring 把运行时激活状态重新映回原始图，是它相对很多单纯 code generator 的明显差异。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 在熟悉的建模工具中画 `UML` 状态机。
2. 导出 `XMI`。
3. 用 `BlueState` 解析 `XMI` 并构建 class metamodel。
4. 指定目标类和目标语言，自动生成 partial classes。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `XMI` 文档。
2. 对齐 `UML` 的 class metamodel。
3. `.NET CodeDOM` 中间结构。
4. 目标语言 partial classes。
5. 监控与调试模块中的 execution log 与图形高亮信息。

### 交换与互操作

`BlueState` 的互操作重点在于：

1. 通过 `XMI` 保持对多种建模工具的独立性。
2. 通过 `CodeDOM` 保持对目标语言的相对独立性。
3. 通过 Enterprise Architect add-in 把运行时状态回显到原图。

## 配套基础设施

- 建模/编辑工具：与 `Enterprise Architect`、`MagicDraw`、`Altova UModel`、`Visual Paradigm` 等 `XMI` 导出工具兼容。
- 解析/交换/元模型支持：完整 `XMI` parser、`UML` 元模型约束校验与 class metamodel。
- 仿真/执行支持：生成代码、simulator、debugger、同步/异步事件发送。
- 验证/分析支持：execution log、real-time visual monitoring；不主打 formal verification。
- 代码生成/转换支持：`.NET CodeDOM` 支撑 `C#`、`Visual Basic .NET` 等多目标语言生成。
- 标准化或社区生态：依托 `UML`、`XMI` 与 `.NET` 生态，而不是独立标准格式。

## 适用场景与需求前提

### 适用场景

适合已经把系统行为画成 `UML` 状态机，并希望把这些图直接带入软件实现、调试与运行时监控的场景。

### 需求前提

1. 建模工具能导出足够稳定的 `XMI`。
2. guard 和 operation 命名能与目标代码对齐。
3. 团队愿意把状态机维护为持续演进的模型资产，而不是一次性文档。
4. 目标平台接受 `BlueState` 这种代码生成 + 框架运行时模式。

### 不适用或高成本场景

如果团队并不维护 `UML/XMI` 工作流，或者更需要形式验证而非执行监控，这条路线吸引力会下降。

## 与相邻形式主义的关系

相对 [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)，`BlueState` 更强调 `XMI` 导入、代码生成和调试监控，而不是把 `UML` 映到另一种验证后端；相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，它更偏桌面软件工程与代码生成，而不是 bare-metal 解释执行；相对 [towards-one-model-interpreter-for-both-design-and-deployment/desc.md](../towards-one-model-interpreter-for-both-design-and-deployment/desc.md)，它更强调生成式实现与监控，而不是单解释器统一语义。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明，若 `project_1` 最终生成的是 `UML` 状态机，后续不一定只能走“导出图片”或“手写实现”两条路，也可以直接接到一条元模型驱动的执行与监控基础设施链。

### 作为目标形式主义还是中间表示

它更像 `UML State Machine` 的执行基础设施，而不是新的中间表示。

### 对需求到模型生成的启发

1. 自动生成状态机时，最好同时考虑导出结构、代码命名和运行时可追踪性。
2. 生成结果若要长期维护，代码生成和手写代码必须有清晰边界。
3. 运行时状态回显到原图，对后续“验证-修复”闭环很有价值。

### 现实限制

它很强于软件工程落地，但对形式性质证明、时钟语义和跨平台开放交换格式支持有限。

## 重要的相关工作

1. [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)：另一条 `UML` 运行时执行基础设施路线。
2. [modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md](../modular-deployment-of-uml-models-for-v-and-v-activities-and-embedded-execution/desc.md)：更强调验证与部署模块化的一条 `UML` 工程链。
3. [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)：更偏分析/验证后端桥接的 `UML` 路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 归类理由：论文主体围绕 `XMI`、元模型、代码生成、调试和 visual monitoring 这些执行基础设施展开，明显属于 `UML` 状态机工具链条目。

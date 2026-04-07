# YAWL 系统的设计与实现 / Design and Implementation of the YAWL System

## 基本信息

- 标题：Design and Implementation of the YAWL System
- 中文标题：YAWL 系统的设计与实现
- 作者：Wil M. P. van der Aalst，Lachlan Aldred，Marlon Dumas，Arthur H. M. ter Hofstede
- 发表：*Advanced Information Systems Engineering*，pp. 142-159，2004
- DOI：`10.1007/978-3-540-25975-6_12`
- 链接：https://doi.org/10.1007/978-3-540-25975-6_12
- 形式主义：`YAWL / workflow language / YAWL system`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 论文角色：workflow language runtime / designer-engine-service architecture / XML-based workflow infrastructure
- 工具/实现获取方式：原文明确给出 `YAWL designer`、`YAWL engine`、`worklist handler`、`web services broker`、`interoperability broker` 等实现部件，并给出语言/XML syntax 入口 `http://www.citi.qut.edu.au/yawl/`；正文未给现代公开仓库。
- 标准/格式获取方式：主承载是 `YAWL` 图形模型、层次化 process definitions、XML syntax 与 XML Schema，以及服务注册所用的 XML messages；它不是中立行业交换标准。

## 简报

这篇论文补的是 workflow 形式主义里一个很关键、但此前文库还没正式挂上的语言节点：`YAWL`。它不是单纯把 `WF-net` 做成一个编辑器，而是围绕 workflow patterns 重新设计了一门带自己语义的流程语言，再把 `designer -> engine -> services` 的运行基础设施完整落地。论文最重要的两个点，一是明确说 `YAWL` 虽然受 `Petri Net` 启发，但语义并不定义成 Petri-net 宏，而是独立的 transition-system 语义；二是把 `OR-join`、multiple instances、cancellation region 这些 workflow 里最难的构件真正做进系统。

- 形式主义定位：workflow-pattern-driven `YAWL` language 及其系统级执行基础设施。
- 构造方式简述：层次化 process definitions + tasks/conditions + `OR-join` / multiple-instances / cancellation 机制，再接 `designer / engine / service-oriented` 运行架构。
- 基础设施与场景简述：依托 `YAWL designer`、`YAWL engine`、`worklist handler`、`web services broker`、`interoperability broker` 与 XML/Web-services 技术，服务业务流程、服务编排和跨系统工作流执行。

```text
workflow specification -> YAWL process definitions -> engine deployment -> cases/tasks/services -> worklist / web-service / inter-engine execution
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `YAWL` workflow specification 与层次化 process definitions。
2. conditions、atomic/composite tasks、splits/joins、multiple instances。
3. `OR-join`、cancellation region、token removal 等 workflow-pattern extensions。
4. `YAWL designer`、`engine` 与 service-oriented architecture。
5. XML syntax、XML Schema 与服务注册消息。

### 核心抽象

结合论文对语言与系统的描述，可把一份 `YAWL` 规格保守整理为：

$$
Y = (D, T, C, F, dec, mi, canc)
$$

上式中的符号逐项解释如下：

1. `D` 是 process definitions 集合。
2. `T` 是 tasks 集合，包含 atomic tasks 与 composite tasks。
3. `C` 是 conditions 集合。
4. `F` 是 flow relation。
5. `dec : T_c \to D` 把 composite tasks 关联到其 decomposition。
6. `mi` 记录 multiple-instance task 的上下界与创建模式。
7. `canc` 描述 removal-of-tokens / cancellation region 机制。
8. 这组元组是对论文中“层次 process definitions + advanced workflow patterns”结构的保守形式化整理。

论文明确强调 `YAWL` 不是简单的 `Petri Net` 宏展开，而采用独立的迁移系统语义。其核心层次关系可写成：

$$
dec : T_c \to D
$$

上式中的符号逐项解释如下：

1. `T_c` 是 composite tasks 集合。
2. `D` 是下层 process definitions 集合。
3. 每个 composite task 都引用一个 lower-level decomposition。
4. 这正是 `YAWL` 层次工作流结构的骨架。

multiple instances 机制可保守压成：

$$
mi(t) = (min_t, max_t, mode_t)
$$

上式中的符号逐项解释如下：

1. `t` 是某个 atomic 或 composite task。
2. `min_t` 与 `max_t` 分别给出实例数量下界和上界。
3. `mode_t` 表示静态、运行时可调或按数据决定的实例创建策略。
4. 论文明确讨论了 multiple instances 的上下界与动态创建控制。

`OR-join` 的语义直觉可保守写成：

$$
\mathrm{fire}_{\mathrm{or}}(j, M) \iff \exists p \in {}^\bullet j,\ M(p) > 0 \land \text{no more tokens can still arrive at } {}^\bullet j
$$

上式中的符号逐项解释如下：

1. `j` 是某个 `OR-join` task。
2. `M` 是当前 workflow marking / execution state。
3. `{}^\bullet j` 是 `OR-join` 的输入边集合。
4. 条件表达的正是论文中“`OR-join` 只有在不再可能有新输入到来时才同步”的语义。

系统实现侧，论文给出的架构可压成：

$$
\mathcal Y = (\mathrm{Designer}, \mathrm{Engine}, \mathrm{Manager}, \mathrm{Worklist}, \mathrm{WSBroker}, \mathrm{InteropBroker}, \mathrm{Services})
$$

上式中的符号逐项解释如下：

1. `Designer` 负责流程建模。
2. `Engine` 负责 process deployment、case execution 与 task lifecycle。
3. `Manager` 负责实例级管理。
4. `Worklist` 负责用户任务分派。
5. `WSBroker` 负责与外部 web services 对接。
6. `InteropBroker` 负责跨 workflow engine 的任务转包。
7. `Services` 表示自定义外部服务集合。

### 一个最小例子与通俗解释

论文里的典型例子就是带 `OR-join` 和 multiple instances 的旅行安排流程：

1. 用户注册之后，系统可能并行触发 `flight`、`hotel`、`payment` 等任务。
2. 某些任务是 composite task，会展开成下层流程。
3. 某些任务可创建多个实例，例如处理多个航段或多个服务片段。
4. `OR-join` 不像普通 `AND-join` 那样等所有输入，也不像 `XOR-join` 那样见一个过一个，而是要判断“当前激活分支里该来的都来齐了没”。

通俗地说，`YAWL` 做的是把现实流程图里那些“最像流程、最不像纯状态机”的东西正式化：可选并发、动态实例数、取消区域、服务编排和跨系统转包。这也是它比简单 `WF-net` 或一般 BPM 图更接近工程系统的一点。

### 运行 / 接受 / 转移语义

论文的执行语义重点包括：

1. workflow instance 由 `YAWL engine` 管理，并在运行时产生 cases。
2. task 的 enable/offer/start/complete 生命周期由 engine 与外部服务共同推进。
3. `worklist handler`、`web services broker`、`interoperability broker` 统一通过服务接口与 engine 交互。
4. data perspective 通过 XML/XPath/XQuery 处理复杂数据对象。

服务注册与执行链可保守写成：

$$
\mathrm{deploy}(Y) \to \mathrm{register}(T, S) \to \mathrm{createCase}(Y) \to \mathrm{offer/start/complete}(t)
$$

上式中的符号逐项解释如下：

1. `deploy(Y)` 表示部署一份 `YAWL` 规格。
2. `register(T,S)` 表示把某类 task 注册给某个 service handler。
3. `createCase(Y)` 表示创建 workflow instance。
4. `offer/start/complete(t)` 表示 task 生命周期事件。

### 语义边界

1. 论文主线是 workflow language 与 workflow system，不是一般并发系统的统一元模型。
2. `YAWL` 虽受 `Petri Net` 启发，但语义与工程目标都已明显 workflow-specific。
3. 重点是 control-flow、data 和 operational perspectives；resource perspective 在本文里不是完整主体。
4. `OR-join` 的精确实现代价较高，论文也明确承认它是系统里最贵的机制之一。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `YAWL` 骨架 | `$Y = (D,T,C,F,dec,mi,canc)$` | 层次流程、动态实例和取消机制共同构成语言核心。 |
| 分解关系 | `$dec : T_c \to D$` | composite task 挂接下层 process definition。 |
| 多实例任务 | `$mi(t) = (min_t,max_t,mode_t)$` | multiple instances 不是附属实现，而是语言级对象。 |
| `OR-join` 语义 | `$\mathrm{fire}_{\mathrm{or}}(j,M) \iff \cdots$` | 只有在不会再有新输入到来时才同步。 |
| 系统架构 | `$\mathcal Y = (\mathrm{Designer},\mathrm{Engine},\ldots)$` | 论文不是只讲语法，还落了完整基础设施。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 更像流程条件与任务生命周期，而不是传统显式状态标签。 |
| 事件 / 触发 | 很强 | task offer/start/complete 与服务交互是执行核心。 |
| 守卫 / 数据 | 很强 | 论文明确把数据 perspective 与 XML/XPath/XQuery 接入系统。 |
| 层次 | 很强 | composite tasks 与 decomposition 是语言骨架。 |
| 并发 / 同步 | 很强 | `AND/XOR/OR` 路由、multiple instances 与 cancellation 都是主轴。 |
| 时间约束 | 不支持 | 本文不是 timed workflow 语义论文。 |
| 连续动态 / 随机性 | 不支持 | 不在范围内。 |
| 可执行 / 可验证性 | 很强 | `designer + engine + services` 形成可执行工作流平台。 |

### 形式化问题与性质

1. `YAWL` 的关键价值，不是再做一份 workflow 图形记法，而是把 workflow patterns 真正做成语义与系统能力。
2. `OR-join`、multiple instances、cancellation region 这三类构件正是传统 workflow tools 最容易弱化或规避的地方。
3. 论文中的 system architecture 说明它既是语言条目，也是重要的 workflow infrastructure 节点。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 在 `YAWL designer` 中创建 process definitions。
2. 用 tasks、conditions、joins/splits 与 decomposition 表达流程。
3. 为 task decomposition 指定数据交换、服务注册与外部调用信息。
4. 把模型部署到 `YAWL engine` 并创建 cases。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `YAWL` 图形模型与层次 process definitions。
2. XML syntax 与 XML Schema。
3. 服务注册消息与执行期 XML data mappings。
4. `worklist / web-services / inter-engine` 接口消息。

### 交换与互操作

互操作重点在于：

1. `YAWL` 语言本身有 XML syntax。
2. `web services broker` 把 engine 与外部 web services 解耦。
3. `interoperability broker` 支持不同 workflow engines 间的任务分包。
4. 论文明确把 service-oriented architecture 当成 operational perspective 的主体路线。

## 配套基础设施

- 建模/编辑工具：`YAWL designer`。
- 解析/交换/元模型支持：XML syntax、XML Schema、XPath、XQuery、JDom、Xerces。
- 仿真/执行支持：`YAWL engine`、`YAWL manager`、case lifecycle 管理。
- 验证/分析支持：论文主线更偏执行与架构，而非单独模型检查器；其分析价值主要来自 workflow-pattern completeness 与严格语义。
- 代码生成/转换支持：重点在 workflow deployment 与服务集成，不主打代码生成。
- 标准化或社区生态：与 workflow patterns、BPEL/XPDL/BPML、Web services 生态强相关。

## 适用场景与需求前提

### 适用场景

适合业务流程、服务编排、跨组织工作流、审批流以及那些明显依赖动态实例数、取消区域和复杂路由同步的流程系统。

### 需求前提

1. 系统核心更像“case 在流程中的生命周期”，而不是平面控制器状态切换。
2. 任务、路由和数据依赖可较稳定地抽成 workflow definitions。
3. 团队接受 XML/Web-services 风格的工作流技术栈。
4. 需求里确实存在 `OR-join`、multiple instances 或 cancellation 这类高级 workflow patterns。

### 不适用或高成本场景

若系统主体是细粒度嵌入式控制、连续时间或复杂数值算法，`YAWL` 就不是最自然的目标形式主义；它更像流程控制和服务编排语言，而不是实时控制器 DSL。

## 与相邻形式主义的关系

相对 [application-of-petri-nets-to-workflow-management/desc.md](../application-of-petri-nets-to-workflow-management/desc.md)，`YAWL` 不再停留在 `WF-net` 这类流程网母型，而是把 workflow patterns、层次任务和执行平台统一起来；相对 [woflan-20-a-petri-net-based-workflow-diagnosis-tool/desc.md](../woflan-20-a-petri-net-based-workflow-diagnosis-tool/desc.md)，`Woflan` 更偏 `WF-net` 诊断，而 `YAWL` 更偏 workflow language/runtime；相对 [woped-an-educational-tool-for-workflow-nets/desc.md](../woped-an-educational-tool-for-workflow-nets/desc.md)，`WoPeD` 更像 `WF-net + PNML` 工作台，而 `YAWL` 更强调执行语义、服务分派和 workflow-system architecture。

## 与本研究的关系

### 对 Project 1 的价值

1. `YAWL` 说明“控制逻辑状态机”之外，还存在一条非常重要的 workflow-state-machine 近邻谱系。
2. 若后续要让 LLM 从需求生成高层业务/任务流程，`WF-net` 可能太骨感，而 `YAWL` 这种带高级路由与运行时支撑的语言更接近工程交付物。
3. 对“生成-验证-修复”闭环而言，`OR-join`、multiple instances 和 cancellation 都是极适合被当作高风险图元单独审计的对象。

### 作为目标形式主义还是中间表示

更适合作为高层流程建模语言与工作流执行载体，而不是底层实时验证后端。

### 对需求到模型生成的启发

1. 需求中若出现“若若干分支中的已激活分支都完成后再汇合”，就不应被粗暴翻成普通 `AND/XOR` join。
2. “任务可能启动若干实例”应成为一等建模对象，而不是后处理脚本。
3. 语言设计与 runtime architecture 最好同步考虑，否则很多高级语义会停留在图上而落不进系统。

### 现实限制

`YAWL` 很强于 workflow 语义与服务编排，但并不天然适合细粒度控制器、dense-time 性质或复杂程序数据流验证。

## 重要的相关工作

1. [application-of-petri-nets-to-workflow-management/desc.md](../application-of-petri-nets-to-workflow-management/desc.md)：`WF-net` 母文，给出 `YAWL` 的并发流程语义起点。
2. [woflan-20-a-petri-net-based-workflow-diagnosis-tool/desc.md](../woflan-20-a-petri-net-based-workflow-diagnosis-tool/desc.md)：workflow-net soundness 诊断工具线。
3. [woped-an-educational-tool-for-workflow-nets/desc.md](../woped-an-educational-tool-for-workflow-nets/desc.md)：`WF-net` 图形编辑、教学与交换环境。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 形式主义：`YAWL / workflow language / YAWL system`
- 归类理由：论文主体是 `YAWL` 语言与系统架构本身，而不是单一验证算法或单个 workflow case，因此按 `🔣/🏗️` 最合适；同时它确实应作为 `WF-net` 之后的 workflow-language 节点回挂到演化树中。

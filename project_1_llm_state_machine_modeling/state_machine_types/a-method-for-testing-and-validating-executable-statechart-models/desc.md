# 可执行状态图模型的测试与验证方法 / A Method for Testing and Validating Executable Statechart Models

## 基本信息

- 标题：A Method for Testing and Validating Executable Statechart Models
- 中文标题：可执行状态图模型的测试与验证方法
- 作者：Tom Mens，Alexandre Decan，Nikolaos I. Spanoudakis
- 发表：*Software & Systems Modeling*，18(2): 837-863，2018
- DOI：`10.1007/s10270-018-0676-3`
- 链接：https://doi.org/10.1007/s10270-018-0676-3
- 形式主义：`Executable Statecharts / Sismic`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：把软件工程中的 TDD / BDD / DbC / runtime verification 移植到可执行 statecharts 的方法路线
- 工具/实现获取方式：原文直接给出 `Sismic` 的 `PyPI`、文档站点和 GitHub 源码入口，并说明采用 `LGPLv3` 开源。
- 标准/格式获取方式：`Sismic` 直接支持 `YAML` 状态图导入导出，实验性支持 `AMOLA/ASEME`，并可导出 `PlantUML`。

## 简报

这篇论文的重点不是重新发明 statecharts，而是把“怎么测、怎么验、怎么在执行时监控 statecharts”做成一套系统方法。作者把 `TDD`、`BDD`、`Design by Contract` 和 property statecharts 统一进同一个流程，再由 `Sismic` 解释器在运行时自动检查契约和行为性质。

- 形式主义定位：围绕 executable statecharts 的测试与验证方法，不是新的状态图母语言。
- 构造方式简述：statechart 模型与 contracts、property statecharts、BDD scenarios、unit tests 组合后，由 `Sismic` 解释器统一执行与监控。
- 基础设施与场景简述：依托 `Sismic` Python library、`YAML`、`behave`、`PlantUML` 和运行时 meta-events，适合 reactive software 的设计期验证。

```text
executable statechart -> contracts / property statecharts / scenarios / unit tests -> Sismic interpreter -> runtime violations / test results
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. executable statecharts。
2. state / transition contracts：preconditions、postconditions、invariants。
3. property statecharts。
4. `BDD` scenarios 与 Python unit tests。
5. `Sismic` interpreter 的 macrostep 语义和 meta-events。

### 核心抽象

结合论文对 statechart、contracts 与 property statecharts 的描述，可把其方法中的运行对象保守整理为：

$$
S = (Q, E, V, T, C_s, C_t, P_s)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `E` 是外部与内部事件集合。
3. `V` 是上下文变量集合。
4. `T` 是迁移集合。
5. `C_s` 是定义在状态上的 contracts。
6. `C_t` 是定义在迁移上的 contracts。
7. `P_s` 是绑定到解释器上的 property statecharts 集合。
8. 这组元组是根据论文对象分层做的保守抽象，不是原文显式统一给出的单一形式定义。

论文明确指出 transition invariants 与 pre/post 的关系可视为：

$$
\mathrm{inv}_t \equiv \mathrm{pre}_t \land \mathrm{post}_t
$$

上式中的符号逐项解释如下：

1. `\mathrm{inv}_t` 是某条迁移上的 invariant。
2. `\mathrm{pre}_t` 是迁移执行前要满足的条件。
3. `\mathrm{post}_t` 是迁移执行后要满足的条件。
4. 论文把 transition invariants 说明为“相当于同时作为 precondition 和 postcondition 的语法糖”。

对于 property statecharts，论文的核心监控思想可压成：

$$
\delta_P^\ast(q_0, me_1 \cdots me_n) \in F_P \Rightarrow \text{violation}
$$

上式中的符号逐项解释如下：

1. `P` 是某个绑定的 property statechart。
2. `q_0` 是该 property statechart 的初始状态。
3. `me_1 \cdots me_n` 是主 statechart 执行过程中发出的 meta-event 序列。
4. `F_P` 是 property statechart 的失败终态集合。
5. 含义是：只要监控状态机在观察到这些 meta-events 后进入失败终态，就立即报告性质违反。
6. 这是对论文 “fail-fast” property monitoring 机制的符号化整理。

### 一个最小例子与通俗解释

论文的 microwave controller 是最合适的直觉例子：

1. 主 statechart 表示微波炉门、加热、计时器等行为。
2. 用 contract 写“开门时不能加热”“timer 不能小于 0”。
3. 用 BDD scenario 写“Given 门打开，When 触发加热，Then 不应进入 heating”。
4. 用 property statechart 监控“只要 door open 时收到 heating_on，就立即进入失败终态”。

通俗地说，这篇论文是在做“statechart 版测试驱动开发”。它把我们熟悉的源码测试方法，搬到了建模层，而且运行时解释器会顺便帮你盯着契约和安全性质。

### 运行 / 接受 / 转移语义

`Sismic` 的执行语义核心包括：

1. 默认采用 inner-first/source-state、run-to-completion 的 macrostep 语义。
2. eventless transitions 先于带事件迁移，internal events 先于 external events。
3. contracts 在 macrostep 生命周期的不同位置检查：state pre 在 enter 前，state post 在 exit 后，state invariant 在 macrostep 结束时，transition pre/post 围绕迁移执行前后检查。
4. property statecharts 通过 meta-events 观察主 statechart 执行。

### 语义边界

边界同样明确：

1. `Sismic` 的 property statecharts 主要面向 fail-fast 的 safety properties。
2. liveness properties 虽然理论上可表达，但工具并不原生支持“按 liveness 口径”验证。
3. 方法的有效性仍然依赖场景、contracts 和 tests 是否写得足够好。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 运行对象 | `$S = (Q, E, V, T, C_s, C_t, P_s)$` | 可执行 statechart 与 contracts / property statecharts 被统一纳入运行时。 |
| 迁移不变量 | `$\mathrm{inv}_t \equiv \mathrm{pre}_t \land \mathrm{post}_t$` | 迁移 invariant 可以看作 pre/post 的语法糖。 |
| property monitoring | `$\delta_P^\ast(q_0, me_1 \cdots me_n) \in F_P \Rightarrow \text{violation}$` | property statecharts 通过 meta-events fail-fast 地报告违规。 |
| 执行粒度 | `$\mathrm{MacroStep}(S,e)$` | 一次事件处理会携带所有后续稳定化步骤。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 主体就是 executable statecharts。 |
| 事件 / 触发 | 很强 | 事件驱动解释器、internal/external event 处理都是核心。 |
| 守卫 / 数据 | 很强 | Python action code、guards、contracts、event parameters 都直接参与执行。 |
| 层次 | 很强 | `Sismic` 明确支持 UML 2 statechart concepts。 |
| 并发 / 同步 | 中等支持 | 重点不是分布式并发语义，而是单模型执行与验证。 |
| 时间约束 | 中等支持 | 支持 simulated time 以及 `after / idle` 这类时间谓词。 |
| 连续动态 / 随机性 | 不支持 | 范围是离散 reactive statecharts。 |
| 可执行 / 可验证性 | 很强 | interpreter、contracts、property statecharts、BDD、unit tests 形成完整链路。 |

### 形式化问题与性质

1. 这篇论文真正补的是“statechart 在设计期如何像源码一样被系统地测试与验证”。
2. `BDD + contracts + property statecharts` 的组合使得不同粒度的问题都能被覆盖。
3. 工具并不追求全自动证明一切，而是强调把多种轻量但互补的方法组合起来。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 用 `YAML` 或外部编辑器定义 statechart。
2. 为状态和迁移补 contracts。
3. 写 property statecharts、BDD scenarios 和 unit tests。
4. 通过 `Sismic` API 或 CLI 执行并收集结果。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `YAML` statechart 文件；
2. `AMOLA/ASEME` 状态图；
3. Python unit tests；
4. `behave` 风格的 BDD scenarios；
5. `PlantUML` 可视化导出。

### 交换与互操作

这条线的互操作重点在于：

1. 用 `YAML` 保持模型的可编辑和版本管理友好性；
2. 用 `PlantUML`、`ASEME` 等工具辅助建模与可视化；
3. 把 statechart 执行和 Python 测试生态直接打通。

## 配套基础设施

- 建模/编辑工具：`YAML` 文本入口，实验性支持 `ASEME` 编辑器。
- 解析/交换/元模型支持：`Sismic` 的 I/O API 支持 `YAML` 导入导出，并可导出 `PlantUML`。
- 仿真/执行支持：`Sismic` interpreter 提供离散、逐步、完全可观察的执行引擎。
- 验证/分析支持：contracts、property statecharts、BDD、unit tests 和 runtime monitoring。
- 代码生成/转换支持：重点是模型执行与测试，不是部署代码生成。
- 标准化或社区生态：依托 Python 生态、`behave`、`PlantUML` 和开源 `Sismic` 项目。

## 适用场景与需求前提

### 适用场景

适合事件驱动 reactive software、嵌入式控制逻辑、以及需要把模型设计纳入持续验证流程的团队。

### 需求前提

1. 行为模型本身是可执行 statechart，而不是纯文档图。
2. 团队愿意为模型编写 contracts、scenarios 或 unit tests。
3. 关键性质更多是 safety / consistency / contract violation，而不是复杂 liveness。
4. 可以接受 Python 作为执行与测试环境的一部分。

### 不适用或高成本场景

如果模型只是静态概念图、没有可执行语义，或者团队无法维护测试资产，这套方法的收益会明显下降。

## 与相邻形式主义的关系

相对 [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)，这篇不再讨论 statecharts 是什么，而是讨论 statecharts 怎么测；相对 [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)，它更偏测试与运行时验证，而不是一口气翻到单一模型检查后端；相对 [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)，它代表 survey 中“直接操作语义 + 工程测试支持”这一支的具体落点。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文对 `project_1` 特别有启发，因为它说明：如果后续让 LLM 生成 statechart，不应只产出“图”，还应同时生成 contracts、property statecharts、BDD scenarios 或 unit tests。

### 作为目标形式主义还是中间表示

更像围绕 statecharts 的验证方法与工程工具，而不是新的目标形式主义。

### 对需求到模型生成的启发

1. 需求文本中的禁止条件、前置条件和后置条件，很适合直接转成 contracts。
2. 需求中的例程、用户故事和交互步骤，可以自然落成 BDD scenarios。
3. 对关键安全性质，生成一个 property statechart 往往比直接手写时序逻辑更贴近工程实践。

### 现实限制

它显著降低了 statechart 验证门槛，但并没有绕开“测试与契约仍需设计”的现实成本。

## 重要的相关工作

1. [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)：`UML` 状态机到模型检查后端的自动桥接路线。
2. [model-checking-of-statechart-models/survey.md](../model-checking-of-statechart-models/survey.md)：状态图验证路线的综述入口。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：`UML` 状态机自动验证和可用工具盘点。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 归类理由：论文主要贡献是围绕 executable statecharts 组织测试、契约和运行时验证流程，因此按 `🛠️` 记录最合适。

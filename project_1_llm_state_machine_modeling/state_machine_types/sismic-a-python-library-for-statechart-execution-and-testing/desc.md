# Sismic：Python 状态图执行与测试库 / Sismic---A Python library for statechart execution and testing

## 基本信息

- 标题：Sismic---A Python library for statechart execution and testing
- 中文标题：Sismic：Python 状态图执行与测试库
- 作者：Alexandre Decan，Tom Mens
- 发表：*SoftwareX*，12，100590，2020
- DOI：`10.1016/j.softx.2020.100590`
- 链接：https://doi.org/10.1016/j.softx.2020.100590
- 形式主义：`Statecharts / YAML DSL / Sismic`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：statechart execution / testing / contract / BDD library
- 工具/实现获取方式：论文直接给出源码入口 `https://github.com/ElsevierSoftwareX/SOFTX_2019_181`、运行仓库 `https://github.com/AlexandreDecan/sismic` 与文档 `https://sismic.readthedocs.io`。
- 标准/格式获取方式：原文明确说明 `Sismic` 以 `YAML` 作为主要 statechart 描述入口，并支持导出到 `PlantUML`；核心承载方式还包括 Python API、BDD scenarios 与 contract/property-statechart specifications。

## 简报

这篇论文的价值，不在于重新发明一门状态图语言，而在于把“可执行状态图 + 测试驱动 + 行为驱动 + 契约 + 运行时性质监控”做成一套轻量、可编程、可扩展的 Python 工具链。`Sismic` 让状态图不再只是画出来的行为说明，而是能直接加载、执行、测试、监控并嵌入常规 Python 开发流程的可运行 artefact。

- 形式主义定位：statechart execution and testing infrastructure，而不是新的状态机母线。
- 构造方式简述：以 `YAML` 定义状态图结构，用 `Python` 表达 action/guard，再由 `Interpreter`、contract monitor、property statecharts 与 `BDD` mapping 承担运行和验证。
- 基础设施与场景简述：依托 `YAML`、`PlantUML`、Python API、可控仿真时钟、contracts、property statecharts 与 `sismic-bdd`，服务可执行状态图开发、模型在环验证和教学。

```text
YAML statechart -> Sismic interpreter -> action / guard evaluation + controllable clock -> contracts / property statecharts / BDD scenarios -> execution trace and validation result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `Sismic`：

1. `YAML` 编写的 statechart descriptions。
2. `Interpreter` 驱动的 step-by-step execution engine。
3. `PlantUML` 可视化导出。
4. design-by-contract 风格的 states/transitions contracts。
5. property statecharts 与 `BDD` scenarios。

### 核心抽象

结合论文对导入、解释和监控流程的说明，可把 `Sismic` 中一张状态图保守写成：

$$
SC = (S, T, E, A, H, C)
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `T` 是迁移集合。
3. `E` 是事件集合。
4. `A` 是 actions / guards 所使用的代码片段。
5. `H` 是层次结构与初始/复合状态等关系。
6. `C` 是 contracts 与 properties 等约束。
7. 这是依据论文对 `YAML` statechart、contracts 与 property statecharts 的描述做的保守整理，不是原文显式统一元组。

论文给出的执行基础设施可保守抽象为：

$$
\mathcal{I}_{Sismic} = (SC, Eval, Clock, Mon, Comm)
$$

上式中的符号逐项解释如下：

1. `SC` 是待执行状态图。
2. `Eval` 是 action code evaluator。
3. `Clock` 是可控仿真时钟，支持 real time 与 simulated time。
4. `Mon` 是 contracts / property statecharts 的运行时监控器。
5. `Comm` 表示 statechart 之间以及 statechart 与普通 Python 代码之间的通信机制。

论文明确指出默认解释器采用 inner-first / source-state 优先和 run-to-completion（big-step）语义，可把一次大步执行保守整理为：

$$
(\alpha, \eta, Q, t) \xRightarrow{e} (\alpha', \eta', Q', t')
$$

上式中的符号逐项解释如下：

1. `\alpha` 是当前 active-state configuration。
2. `\eta` 是变量存储与执行上下文。
3. `Q` 是待处理事件队列。
4. `t` 是当前时钟值。
5. `e` 是当前外部或内部触发事件。
6. `\alpha'`、`\eta'`、`Q'`、`t'` 是执行大步后的新配置。
7. 这条写法是对论文所述 big-step interpreter 的保守操作化表达。

论文还给出一个很具体的 contract 示例，可直接压成：

$$
pre_{cooking}: timer > 0,\qquad post_{cooking}: received(door\_opened) \lor timer = 0
$$

上式中的符号逐项解释如下：

1. `pre_{cooking}` 是进入或执行 `cooking` 状态前应满足的前置条件。
2. `post_{cooking}` 是执行后必须满足的后置条件。
3. `received(door_opened)` 是论文 contract 语言中可用的谓词。

### 一个最小例子与通俗解释

论文给出的 microwave controller 例子很适合说明：

1. 在 `YAML` 里定义 `Simple microwave controller` 状态图。
2. `door opened` 状态在 entry 时发送 `lamp_on`，在 exit 时发送 `lamp_off`。
3. 使用 Python 代码加载模型，创建 `Interpreter`，向队列压入 `timer_inc` 和 `cooking_start`。
4. 执行一次大步后，可断言 `cooking` 位于当前 configuration 中。

通俗地说，`Sismic` 像“把状态图变成普通 Python 项目里可 import、可 test、可 assert 的模块”。它不是只把图画出来，而是让状态图真正进入开发与测试闭环。

### 运行 / 接受 / 转移语义

论文对运行语义强调了四点：

1. 解释器是 discrete、step-by-step、observable 的。
2. 默认采用 inner-first / source-state 与 run-to-completion big-step 语义。
3. action/guard 可直接写 Python。
4. contracts 与 property statecharts 在运行时同步监控。

如果从工具链角度描述状态图测试执行，可保守写成：

$$
\mathrm{Run}(SC, Test, Mon) \to (Trace, Verdict)
$$

上式中的符号逐项解释如下：

1. `SC` 是状态图。
2. `Test` 可以是单元测试、`BDD` scenario 或交互式执行驱动。
3. `Mon` 是 contracts / property statecharts monitor。
4. `Trace` 是执行痕迹。
5. `Verdict` 是 contract violation、property violation 或测试通过结果。

### 语义边界

论文也明确给出了边界：

1. `Sismic` 是纯 Python 实现，因此性能主要取决于 Python 解释器。
2. 它强调执行、测试与监控，不把工业级代码生成作为主线。
3. 支持主流 statechart 概念，但不是声称覆盖所有 statechart 语义变体。
4. 未来工作仍包括更自动的测试生成、contracts 生成和质量问题检测。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 状态图骨架 | `$SC = (S, T, E, A, H, C)$` | 对应论文中的状态、迁移、事件、代码、层次与 contracts/properties。 |
| 解释器骨架 | `$\mathcal{I}_{Sismic} = (SC, Eval, Clock, Mon, Comm)$` | 概括了 `Sismic` 的执行、求值、时钟、监控与通信组件。 |
| 大步执行 | `$(\alpha, \eta, Q, t) \xRightarrow{e} (\alpha', \eta', Q', t')$` | 对应论文所述 run-to-completion / big-step 语义。 |
| contract 示例 | `$pre_{cooking}: timer > 0,\ post_{cooking}: received(door\_opened)\lor timer=0$` | 直接来自论文给出的 microwave contract 片段。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 主体就是 executable statecharts。 |
| 事件 / 触发 | 很强 | 事件队列、timed events 与 statechart 间通信都是一等能力。 |
| 守卫 / 数据 | 很强 | guard、action、contracts 都可用 Python 表达。 |
| 层次 | 很强 | statechart 本体天然支持 hierarchy。 |
| 并发 / 同步 | 中等支持 | 支持 statechart 间通信，但论文主线不是复杂并发代数。 |
| 时间约束 | 中等支持 | 通过 controllable clock 与 timed events 支持。 |
| 连续动态 / 随机性 | 不支持 | 不在本文主线。 |
| 可执行 / 可验证性 | 很强 | 执行、单元测试、BDD、DbC、property monitoring 全部打通。 |

### 形式化问题与性质

1. `Sismic` 的关键点，不是再讲 statechart 理论，而是把多种软件测试方法直接压到可执行状态图上。
2. `YAML + Python + PlantUML` 的组合，使它在轻量性和可读性之间取得了很好的平衡。
3. contracts 与 property statecharts 的运行时监控，是它区别于很多“只能执行不能系统测试”的状态图库的关键。

## 构造方式与承载格式

### 建模入口

论文中的典型建模入口是：

1. 用 `YAML` 编写 statechart。
2. 用 `sismic.io` 导入模型。
3. 用 `Interpreter` 执行状态图。
4. 用 `PlantUML` 导出可视化图。
5. 用 `sismic-bdd` 或常规测试框架执行场景测试。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `YAML` statechart descriptions。
2. Python API。
3. `PlantUML` export。
4. contracts / property statecharts specifications。
5. `BDD` scenarios 与命令行工具。

### 交换与互操作

这篇论文的互操作重点在 Python 生态内部：

1. 状态图可以被普通 Python 代码调用，反过来也能调用 Python 代码。
2. `PlantUML` 提供图形可视化出口。
3. `BDD` 映射让领域专家可用自然语言场景驱动状态图测试。

## 配套基础设施

- 建模/编辑工具：`YAML` 编辑器、Python API、`PlantUML` 可视化。
- 解析/交换/元模型支持：`sismic.io` 负责导入导出，`PlantUML` 作为主要图形出口。
- 仿真/执行支持：默认解释器、可控时钟、statechart 间通信、Python 回调。
- 验证/分析支持：单元测试、`BDD`、DbC、property statecharts、运行时 violation monitoring。
- 代码生成/转换支持：论文主线不是代码生成，而是执行与测试。
- 标准化或社区生态：GitHub 仓库、ReadTheDocs 文档、`LGPLv3` 开源许可和 Python 社区生态。

## 适用场景与需求前提

### 适用场景

适合可执行状态图开发、模型在环测试、教学实验、工作流/业务过程支持，以及希望把状态图直接纳入 Python 测试流程的场景。

### 需求前提

1. 团队接受以 `YAML` 和 Python 组织状态图工程。
2. 目标偏执行、测试和监控，而不是工业代码生成。
3. 系统行为能自然映射为显式 statecharts。
4. 需要 contracts / BDD / runtime monitoring 这类开发期反馈能力。

### 不适用或高成本场景

如果目标是极致性能、工业级硬实时部署或重型图形化建模环境，`Sismic` 这条轻量 Python 路线就不一定最合适。

## 与相邻形式主义的关系

相对 [repast-simphony-statecharts/desc.md](../repast-simphony-statecharts/desc.md)，`Repast Simphony` 更偏 Eclipse/Java/agent simulation 工具链，而 `Sismic` 更轻量、更 Pythonic；相对 [statechart-development-beyond-wysiwyg/desc.md](../statechart-development-beyond-wysiwyg/desc.md)，后者更强调 statechart 编辑与 DSL 入口，而 `Sismic` 更强调执行、测试与 contracts；相对 [robochart-modelling-and-verification-of-robotic-applications/desc.md](../robochart-modelling-and-verification-of-robotic-applications/desc.md)，`RoboChart` 更强调形式化设计与验证链，`Sismic` 更强调开发期可执行与测试闭环。

## 与本研究的关系

### 对 Project 1 的价值

它补上了一条对 `project_1` 很实用的工具线：如果后续要让 LLM 生成状态图，不一定只能生成“最终验证模型”，也可以先生成能直接跑、能写测试、能加 contracts 的可执行 artefact，再逐步收束到更正式的后端。

### 作为目标形式主义还是中间表示

更像轻量可执行中间表示与开发期验证载体，而不是最终高可信交付形式主义。

### 对需求到模型生成的启发

1. 若状态图结果能直接写成结构化文本并立即执行，生成-验证-修复闭环会更顺畅。
2. contracts 和 property statecharts 说明“验证约束”也可以和状态图一起生成，而不是事后再补。
3. `YAML` 这类简洁承载格式对 LLM 生成非常友好。

### 现实限制

它强在开发与测试便利性，不强在大规模工业部署和最严格的形式化保证。

## 重要的相关工作

1. [repast-simphony-statecharts/desc.md](../repast-simphony-statecharts/desc.md)：另一条 statechart 执行基础设施。
2. [statechart-development-beyond-wysiwyg/desc.md](../statechart-development-beyond-wysiwyg/desc.md)：强调 statechart DSL 与编辑入口的工具线。
3. [robochart-modelling-and-verification-of-robotic-applications/desc.md](../robochart-modelling-and-verification-of-robotic-applications/desc.md)：更强调 formal design / verification 的 statechart DSL 工具链。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Statecharts / YAML DSL / Sismic`
- 论文角色：statechart execution / testing / contract / BDD library
- 归类理由：论文主体是面向可执行状态图的 Python 基础设施与测试闭环，而不是新的状态图母线。

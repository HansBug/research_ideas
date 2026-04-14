# UmpleRun：面向文本化状态机的动态分析工具 / UmpleRun: a Dynamic Analysis Tool for Textually Modeled State Machines using Umple

## 基本信息

- 标题：UmpleRun: a Dynamic Analysis Tool for Textually Modeled State Machines using Umple
- 中文标题：UmpleRun：面向文本化状态机的动态分析工具
- 作者：Hamoud Aljamaan，Timothy Lethbridge，Miguel Garzón，Andrew Forward
- 发表：*Proceedings of the 1st International Workshop on Executable Modeling (EXE 2015), co-located with MODELS 2015*，`CEUR-WS Vol. 1560`，pp. 16-20，2015
- DOI：原文未提供
- 链接：https://ceur-ws.org/Vol-1560/paper3.pdf
- 形式主义：`Umple / MOTL / UmpleRun / execution scenarios / model-level tracing`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：文本化 `UML` 状态机的动态验证、执行场景断言与模型级 trace 分析工具
- 工具/实现获取方式：原文直接给出命令行入口 `java -jar umplerun.jar model.ump exeScenario.cmd`；依赖 `Umple` 编译器、`Java` 打包与动态加载。正文未给稳定公开仓库链接。
- 标准/格式获取方式：输入包括 `Umple` 模型、execution scenario 脚本与可选 `MOTL` trace directives，输出是 validation verdict 与 execution traces；不是通用交换标准。

## 简报

这篇论文补的是 `Umple` 生态里一个非常实用、但和“只会代码生成”明显不同的环节：把文本化状态机真正跑起来，并且用一个可写断言的 execution scenario 去检查动态行为是否符合预期。它不是再定义一种新的状态机本体，而是把 `Umple` 模型、`MOTL` trace 指令、`Java` 生成产物和场景级断言接成了一个轻量动态验证闭环。

- 形式主义定位：围绕 `Umple` 文本状态机的动态分析与验证方法路线，而不是新的状态机家族。
- 构造方式简述：先把 `Umple` 模型编译成 `Java`，再打包成 `JAR`，通过 execution scenario 驱动对象构造和事件调用，并在每一步核对查询方法返回值。
- 基础设施与场景简述：依托 `Umple`、`MOTL`、execution scenario 模板、`Java` 动态加载和 `CSV`/trace 输出，服务文本化 `UML` 状态机的白盒调试、回归验证与模型级行为分析。

```text
Umple 状态机模型 -> Umple 编译器 -> Java/JAR -> execution scenario 驱动 -> verdict + model-level traces
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Umple` 文本化状态机模型；
2. `MOTL` model-level trace directives；
3. execution scenario；
4. dynamic loading / validation pipeline；
5. validation verdict 与 execution trace。

### 核心抽象

论文没有把 execution scenario 写成单独的正式元组，而是直接给出了脚本模板。按原文结构可保守整理为：

$$
ES = \langle Q,\langle c_1,\mathbf{e}_1\rangle,\ldots,\langle c_n,\mathbf{e}_n\rangle\rangle
$$

上式中的符号逐项解释如下：

1. `$Q$` 是第一行列出的 query methods 集合，表示每一步命令之后都要调用哪些查询方法。
2. `$c_i$` 是第 `$i$` 条 command，可以是构造函数调用，也可以是状态机事件调用。
3. `$\mathbf{e}_i$` 是在执行 `$c_i$` 后，对 `$Q$` 中各查询方法期望得到的返回值向量。
4. 整个 `$ES$` 对应原文给出的 `command, method_calls_after_commands ...` 模板。

论文对动态验证流程直接给出四阶段架构，可压成：

$$
J = \mathrm{package}(\mathrm{compile}(M)), \qquad s_0 = \mathrm{load}(J), \qquad s_i = c_i(s_{i-1})
$$

上式中的符号逐项解释如下：

1. `$M$` 是输入的 `Umple` 模型。
2. `$\mathrm{compile}(M)$` 表示 `Umple` 编译器把模型翻成 `Java` 系统。
3. `$J$` 是打包后的 `JAR` 容器。
4. `$s_0$` 是动态加载 `JAR` 后得到的初始运行对象状态。
5. `$s_i$` 是执行第 `$i$` 条 command 后的运行状态。

验证结论则可保守整理为：

$$
\mathrm{verdict}(ES,M)=\bigwedge_{i=1}^{n} Q(s_i)=\mathbf{e}_i
$$

上式中的符号逐项解释如下：

1. `$Q(s_i)$` 表示在第 `$i$` 步后调用所有 query methods 得到的实际值向量。
2. `$\mathbf{e}_i$` 是 scenario 中声明的期望值向量。
3. 若任一步不一致，`UmpleRun` 会报告 failed assertions。
4. 若同时启用 `MOTL`，则 verdict 之外还会产生模型级 execution trace。

### 一个最小例子与通俗解释

论文中的 car transmission 例子最适合说明工具到底在做什么：

1. `CarTransmission` 模型有 `neutral`、`reverse` 和复合状态 `drive`，其中 `drive` 下再嵌 `first/second/third`。
2. execution scenario 先创建对象，再依次触发 `selectReverse`、`selectDrive`、`reachSecondSpeed` 等事件。
3. 每一步之后都调用诸如“当前顶层状态”“当前子状态”“`driveSelected` 布尔值”这类 query methods，并核对是否与期望一致。
4. 若模型里故意注入 bug，`UmpleRun` 会直接指出哪一步断言失败，并可结合 `MOTL` trace 看见模型级行为轨迹。

通俗地说，它像是“给状态机写可执行验收脚本”。不是只看生成的代码能不能编译，而是直接问模型本身：“按这个操作顺序跑，你是不是进入了我预期的状态？”

### 运行 / 接受 / 转移语义

execution scenario 的脚本模板在论文中写成：

$$
\texttt{command,\ method\_calls\_after\_commands\ \ldots}
$$

以及随后逐行的

$$
\texttt{command\_i,\ values\_from\_method\_calls\ \ldots}
$$

上式中的符号逐项解释如下：

1. 第一行固定声明“每步执行后都要检查哪些查询方法”。
2. 后续每一行对应一条命令及其期望返回值。
3. `UmpleRun` 对命令的解释既支持对象构造，也支持状态机事件调用。
4. 这套模板本质上把模型动态行为验证压成了一个逐步断言序列。

原文给出的工具调用命令是：

$$
\texttt{java -jar umplerun.jar\ model.ump\ exeScenario.cmd}
$$

上式中的符号逐项解释如下：

1. `model.ump` 是待执行的 `Umple` 模型。
2. `exeScenario.cmd` 是 execution scenario 文件。
3. 命令行本身表明工具以“模型 + 场景”双输入工作，而不是只接收静态状态机文件。

### 语义边界

1. 论文主体面向 `Umple` 文本化状态机，而不是任意 `UML` 执行语义。
2. 验证方式主要是 scenario-driven dynamic validation，不是完全符号穷举模型检查。
3. 断言能力依赖 query methods 是否能暴露关心的状态与属性。
4. trace 输出建立在 `MOTL` 之上，若模型没写 trace directives，可观察性会弱很多。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| scenario 骨架 | `$ES = \langle Q,\langle c_1,\mathbf{e}_1\rangle,\ldots,\langle c_n,\mathbf{e}_n\rangle\rangle$` | 把场景验证固定成“命令 + 断言向量”结构。 |
| 编译-装载链 | `$J = \mathrm{package}(\mathrm{compile}(M))$` | `UmpleRun` 不是解释器，而是经过 `Java/JAR` 生成后再执行。 |
| 运行态推进 | `$s_i = c_i(s_{i-1})$` | 每一步 command 都会真正改变模型实例状态。 |
| 验证结论 | `$\mathrm{verdict}(ES,M)=\bigwedge_{i=1}^{n} Q(s_i)=\mathbf{e}_i$` | 工具核心是逐步断言验证，而不是离线证明。 |
| 命令行入口 | `$\texttt{java -jar umplerun.jar model.ump exeScenario.cmd}$` | 说明工具链的最小可执行接口。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接针对 `Umple` 文本化状态机与复合状态。 |
| 事件 / 触发 | 很强 | execution scenario 以事件调用作为主要驱动手段。 |
| 守卫 / 数据 | 中等支持 | 可检查 guard 影响下的状态变化和属性值，但不是通用约束求解器。 |
| 层次 | 很强 | 例子直接覆盖复合状态与子状态。 |
| 并发 / 同步 | 弱支持 | 本文核心展示单个类的状态机执行，不强调并发正交区。 |
| 时间约束 | 不支持 | 不是 timed-analysis 工具。 |
| 连续动态 / 随机性 | 不支持 | 面向离散、事件驱动的建模对象。 |
| 可执行 / 可验证性 | 很强 | 通过 `Umple -> Java -> JAR -> scenario` 形成直接可执行验证闭环。 |

### 形式化问题与性质

1. `UmpleRun` 的核心价值是把“文本状态机是否按预期动态工作”这件事工程化，而不是只停在代码生成。
2. `MOTL` 的加入使它不仅能给 verdict，还能保留模型级 trace，这对调试很关键。
3. 它代表了一条很适合 `project_1` 的路线：先让模型跑起来，再用结构化场景检查动态行为，再把失败点反喂给修复环节。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `Umple` 文本模型；
2. 状态机事件与对象构造命令；
3. execution scenario 脚本；
4. 可选 `MOTL` trace directives。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `.ump` 文本模型；
2. `Java` 生成代码与 `JAR` 包；
3. `.cmd` execution scenario；
4. execution trace 与 validation verdict。

### 交换与互操作

1. `UmpleRun` 依赖 `Umple` 编译器把模型翻成 `Java`。
2. `MOTL` 作为 mixin 式 trace 语言，与模型文本本身保持解耦。
3. 输出更像执行与分析工件，而不是可跨生态交换的标准格式。

## 配套基础设施

- 建模/编辑工具：`Umple` 文本化建模语言与其状态机语法。
- 解析/交换/元模型支持：`Umple` 编译器、`MOTL` trace directives、execution scenario 模板。
- 仿真/执行支持：`Java` 代码生成、`JAR` 打包、动态加载与命令驱动执行。
- 验证/分析支持：逐步断言验证、failed assertions 报告、模型级 execution trace。
- 代码生成/转换支持：`Umple -> Java` 是工具工作的前提链路。
- 标准化或社区生态：基于 `Umple`/`UML` 文本化建模生态，原文未提供独立标准化规范。

## 适用场景与需求前提

### 适用场景

适合文本化状态机建模、可执行 `UML` 原型验证、模型级回归测试，以及“先让状态机跑起来再判断行为是否符合预期”的开发流程。

### 需求前提

1. 模型需要能写成 `Umple` 状态机。
2. 关注的行为最好能转成一串可执行 commands 和可观察 query methods。
3. 若需要更细粒度调试，最好额外写 `MOTL` trace directives。
4. 团队接受 scenario-driven 的动态验证，而不是期望一上来就是全自动状态空间穷举。

### 不适用或高成本场景

若系统主要难点在 dense-time、概率、连续动力学或复杂并发同步，这篇论文给的不是直接后端。

## 与相邻形式主义的关系

相对 [enhanced-code-generation-from-uml-composite-state-machines/desc.md](../enhanced-code-generation-from-uml-composite-state-machines/desc.md)，后者更偏 `Umple` 的代码生成，而 `UmpleRun` 更偏动态验证与执行场景；相对 [towards-one-model-interpreter-for-both-design-and-deployment/desc.md](../towards-one-model-interpreter-for-both-design-and-deployment/desc.md)，那篇强调统一解释器，`UmpleRun` 更轻量，也更聚焦状态机场景断言；相对 [sismic-a-python-library-for-statechart-execution-and-testing/desc.md](../sismic-a-python-library-for-statechart-execution-and-testing/desc.md)，两者都强调 executable statecharts，但 `Sismic` 更像通用 `Python` 运行时，`UmpleRun` 则紧绑 `Umple + MOTL + Java` 工具链。

## 与本研究的关系

### 对 Project 1 的价值

1. 它证明“文本化状态机”可以直接接执行场景验证，不必等到完整模型检查后端才有反馈。
2. execution scenario 这种承载方式很适合作为 `project_2` 中验证场景生成的近邻参考。
3. 若 `LLM` 负责先生成 `Umple` 或相近文本状态机，`UmpleRun` 代表了一条低门槛的首轮动态验模路线。

### 作为目标形式主义还是中间表示

更适合作为 `UML/Statecharts` 文本化生态中的执行与验证载体，而不是新的状态机主干本体。

### 对需求到模型生成的启发

1. 生成状态机之后，立即给出“可执行场景 + 期望断言”比只给自然语言说明更有闭环价值。
2. 如果后续要做自动修复，模型级 trace 比单纯 pass/fail 更利于定位错误迁移和守卫。
3. 文本 DSL、代码生成和动态验证连成一体后，`LLM` 更容易在生成、验证、修复之间迭代。

## 重要的相关工作

1. [enhanced-code-generation-from-uml-composite-state-machines/desc.md](../enhanced-code-generation-from-uml-composite-state-machines/desc.md)：同属 `Umple` 生态中的代码生成路线。
2. [towards-one-model-interpreter-for-both-design-and-deployment/desc.md](../towards-one-model-interpreter-for-both-design-and-deployment/desc.md)：统一执行器方向的邻近条目。
3. [sismic-a-python-library-for-statechart-execution-and-testing/desc.md](../sismic-a-python-library-for-statechart-execution-and-testing/desc.md)：另一条 executable-statechart runtime / testing 路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Umple / MOTL / UmpleRun / execution scenarios / model-level tracing`
- 论文角色：文本化 `UML` 状态机的动态验证、执行场景断言与模型级 trace 分析工具
- 归类理由：论文主体聚焦 `Umple` 状态机的执行、场景验证与 trace 分析，不在定义新的语言本体，而是在补足文本化状态机生态中的动态验证方法链。

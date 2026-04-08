# 模型驱动测试脚本生成框架与工业洞见 / A Model-Based Test Script Generation Framework and Industrial Insight

## 基本信息

- 标题：A Model-Based Test Script Generation Framework and Industrial Insight
- 中文标题：模型驱动测试脚本生成框架与工业洞见
- 作者：Muhammad Nouman Zafar，Wasif Afzal，Eduard Paul Enoiu，Zulqarnain Haider，Inderjeet Singh
- 发表：*SN Computer Science*，6:294，2025
- DOI：`10.1007/s42979-025-03823-7`
- 链接：https://doi.org/10.1007/s42979-025-03823-7
- 形式主义：`EFSM / GraphWalker / TIGER`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：GraphWalker-based EFSM test-script concretization framework and industrial MBT workflow
- 工具/实现获取方式：原文给出 `TIGER` GitHub 入口 `https://github.com/MuhammadNoumanZafar/TIGER`，并说明框架基于 `GraphWalker`；正文末尾也给出 `GraphWalker` 入口。
- 标准/格式获取方式：原文说明 `GraphWalker` 使用 `GraphML` 或 `JSON` 定义模型，`GW CLI` 以 JSON 生成抽象测试步骤；`TIGER` 再结合 XML 信号映射生成 C# 测试脚本。

## 简报

这篇论文提出 `TIGER`，即基于 `GraphWalker` 的 Model-Based Test scrIpt GenEration fRamework。其重点不是重新定义 EFSM，而是把 `GraphWalker` 生成的抽象路径和 JSON test steps 具体化成工业测试平台可执行的 C# 测试脚本，并在 Alstom Rail 的列车控制与管理系统 `TCMS` SiL 平台上验证。

- 形式主义定位：基于 `GraphWalker` EFSM 的 MBT concretization / test-script generation 方法路线。
- 构造方式简述：先用 `GraphWalker Studio` 建模并验证 EFSM，再用 `GW CLI` 生成 JSON 抽象测试步骤，随后由 `TIGER` 读取 JSON 和 XML 信号映射，生成 C# 可执行测试脚本。
- 基础设施与场景简述：依托 `GraphWalker Studio/CLI/GW4E`、`GraphML/JSON`、XML logical/technical signal mapping、C# script generator 和 Alstom SiL 平台，服务工业 CPS/嵌入式软件测试脚本自动化。

```text
requirements -> GraphWalker EFSM -> JSON abstract test steps -> XML signal mapping -> TIGER concretizer -> C# test scripts -> SiL verdicts
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `GraphWalker` EFSM model；
2. states、shared states、data variables、guard conditions、actions and transitions；
3. generation algorithm and stopping condition；
4. JSON abstract test cases；
5. XML logical/technical signal mapping；
6. `TIGER` test data extractor、signal information extractor、mapping rules 和 test script generator；
7. mutation-based robustness assessment and industrial survey。

### 核心抽象

依据论文对 `GraphWalker` EFSM 的描述，可保守整理为：

$$
M_{\mathrm{EFSM}} = (Q,q_0,X,E,G,A)
$$

上式中的符号逐项解释如下：

1. `$M_{\mathrm{EFSM}}$` 是 `GraphWalker` 中表示 SUT 的扩展有限状态机模型。
2. `$Q$` 是 states 和 shared states 的集合。
3. `$q_0$` 是初始状态。
4. `$X$` 是 data variables 集合，它们在状态之间保存动态值。
5. `$E$` 是 transitions 集合。
6. `$G$` 是 guard conditions 集合，即影响模型行为的布尔条件。
7. `$A$` 是 actions 集合，即转移或元素上携带的变量更新或测试动作。
8. 该元组是根据原文对 `GraphWalker` EFSM 构件的描述做的保守归纳。

`TIGER` 的转换链可写成：

$$
\tau_{\mathrm{TIGER}}: M_{\mathrm{EFSM}} \times X_{\mathrm{sig}} \to S_{\mathrm{CSharp}}
$$

上式中的符号逐项解释如下：

1. `$\tau_{\mathrm{TIGER}}$` 是从抽象模型和信号映射到脚本的转换过程。
2. `$M_{\mathrm{EFSM}}$` 是 `GraphWalker` 模型。
3. `$X_{\mathrm{sig}}$` 是 XML 中的 logical / technical signal names、signal type 和数据类型信息。
4. `$S_{\mathrm{CSharp}}$` 是生成的 C# executable test scripts。
5. 该式对应原文中 JSON 抽象测试步骤、XML 信号文件和脚本生成器的组合流程。

### 一个最小例子与通俗解释

一个最小 TIGER 场景可以这样理解：

1. `GraphWalker` EFSM 有状态 `NoFire` 和 `FireDetected`。
2. 变量 `fire=true` 使 guard 成立，转移进入 `FireDetected`。
3. `GW CLI` 用 JSON 记录当前模型元素、变量值、actions 和 properties。
4. `TIGER` 从 JSON 中提取 logical signal 名和值，再从 XML 中找到对应 technical signal 名。
5. 生成 C# 脚本：先 force 输入信号，再在给定 `ResponseTime` 内 verify 输出信号。

通俗地说，`GraphWalker` 负责“从模型里走出一条抽象测试路径”，`TIGER` 负责“把这条路径翻译成工业平台真的能跑的信号级脚本”。

### 运行 / 接受 / 转移语义

EFSM 的一步执行可保守写成：

$$
(q,x) \xrightarrow{e} (q',x') \iff e=(q,g,a,q') \land g(x)=\mathrm{true} \land x'=a(x)
$$

上式中的符号逐项解释如下：

1. `$q$` 与 `$q'$` 是当前和目标 EFSM 状态。
2. `$x$` 与 `$x'$` 是当前和更新后的变量 valuation。
3. `$e$` 是一条转移。
4. `$g$` 是该转移上的 guard condition。
5. `$a$` 是该转移上的 action 或变量更新。
6. guard 为真时，转移可被遍历，action 更新变量。

对测试步骤的具体化可写成：

$$
\mathrm{scriptStep} = \mathrm{map}_{\mathrm{sig}}(\mathrm{jsonStep},X_{\mathrm{sig}})
$$

上式中的符号逐项解释如下：

1. `$\mathrm{jsonStep}$` 是 `GW CLI` 以 verbose JSON 生成的抽象测试步骤。
2. `$X_{\mathrm{sig}}$` 是 XML 信号信息，包括 logical names、technical names 和 signal type。
3. `$\mathrm{map}_{\mathrm{sig}}$` 是 `TIGER` 的映射规则集合。
4. `$\mathrm{scriptStep}$` 是 C# 脚本中的 force 或 verify 步骤。

### 语义边界

1. 本文重点是 test-script generation 和工业落地，不是 EFSM 语义理论的新结果。
2. `TIGER` 的 concretization 依赖目标工业平台的信号命名、XML 映射和 C# 脚本格式。
3. 论文案例基于 Alstom `TCMS` SiL 平台，外推到其他企业需要适配执行层。
4. mutation 分析用于评估脚本鲁棒性，不等于对 SUT 完整正确性的形式证明。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| EFSM 骨架 | `$M_{\mathrm{EFSM}} = (Q,q_0,X,E,G,A)$` | `GraphWalker` 模型包含状态、变量、guard、actions 和 transitions。 |
| EFSM 步进 | `$(q,x) \xrightarrow{e} (q',x') \iff e=(q,g,a,q') \land g(x)=\mathrm{true} \land x'=a(x)$` | guard 控制转移，action 更新变量。 |
| TIGER 转换 | `$\tau_{\mathrm{TIGER}}: M_{\mathrm{EFSM}} \times X_{\mathrm{sig}} \to S_{\mathrm{CSharp}}$` | 抽象模型与信号映射生成 C# 脚本。 |
| JSON 具体化 | `$\mathrm{scriptStep} = \mathrm{map}_{\mathrm{sig}}(\mathrm{jsonStep},X_{\mathrm{sig}})$` | 将抽象测试步骤转成可执行信号级步骤。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 使用 `GraphWalker` EFSM 显式表示 SUT 状态。 |
| 事件 / 触发 | 强 | 转移和生成路径对应测试场景中的动作。 |
| 守卫 / 数据 | 很强 | EFSM 包含 data variables、guard conditions 和 actions。 |
| 层次 | 弱支持 | shared states 支持跨状态机遍历，但论文主线不是层次状态机语义。 |
| 并发 / 同步 | 间接支持 | 可服务工业 CPS 测试流程，但模型核心仍是路径遍历。 |
| 时间约束 | 中等支持 | 通过 `ResponseTime` 等脚本参数表达验证时间窗。 |
| 连续动态 / 随机性 | 弱支持 | 随机性主要来自 `GraphWalker` generation algorithms，如 random walks。 |
| 可执行 / 可验证性 | 很强 | 最终生成可在 Alstom SiL 平台执行并产生 verdict 的 C# scripts。 |

### 形式化问题与性质

1. `TIGER` 的核心价值是把 EFSM 抽象测试路径具体化到 signal-level test scripts。
2. 它补的是 MBT 工业落地中“抽象测试案例不能直接执行”的中间断层。
3. 对本文库而言，这是 `EFSM/GraphWalker` 方法路线和工业测试基础设施证据，不是新模型家族节点。

## 构造方式与承载格式

### 建模入口

原文给出的入口包括：

1. `GraphWalker Studio` 创建和验证图形 EFSM。
2. `GW CLI` 生成抽象测试案例。
3. `GraphML` 或 `JSON` 模型文件。
4. generation algorithm 和 stopping condition。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `GraphML`；
2. `JSON` model/test-step output；
3. XML signal information file；
4. mapping rules table；
5. generated C# test scripts；
6. SiL execution logs and verdicts。

### 交换与互操作

互操作重点在测试流水线：

1. `GraphWalker` 提供通用 EFSM 建模和路径生成。
2. `TIGER` 把 JSON 抽象测试数据与工业信号 XML 对齐。
3. 生成脚本接入 Alstom `TCMS` SiL 平台和既有库/配置文件。

## 配套基础设施

- 建模/编辑工具：`GraphWalker Studio`、`GW CLI`、`GW4E`。
- 解析/交换/元模型支持：`GraphML`、`JSON`、XML logical/technical signal mapping。
- 仿真/执行支持：SiL execution platform，生成脚本可实际执行并产生日志/verdict。
- 验证/分析支持：模型仿真、路径覆盖、mutation-based robustness check 和工业 survey 分析。
- 代码生成/转换支持：`TIGER` test script generator 生成 C# executable test scripts。
- 标准化或社区生态：依托 `GraphWalker` 开源 MBT 生态与 Alstom 工业测试流程。

## 适用场景与需求前提

### 适用场景

适合工业嵌入式软件、列车控制系统、CPS SiL 测试和已有信号级测试平台的 MBT 脚本自动生成。

### 需求前提

1. SUT 行为能建模为 `GraphWalker` EFSM。
2. 需求中的信号名、变量和期望输出能整理成 JSON/XML 可映射结构。
3. 测试执行平台接受生成脚本语言或可适配脚本模板。
4. 工业流程允许引入建模、模型验证和脚本生成环节。

### 不适用或高成本场景

如果项目没有稳定的 logical-to-technical signal mapping，或执行平台不支持脚本化 force/verify 步骤，`TIGER` 需要较多定制；如果目标是纯理论模型检查，也不应把它当作验证后端。

## 与相邻形式主义的关系

相对 [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)，`TorX` 更偏 `ioco` 在线一致性测试，`TIGER` 更偏 EFSM 路径到工业脚本的具体化；相对 [model-based-testing-of-object-oriented-reactive-systems-with-spec-explorer/desc.md](../model-based-testing-of-object-oriented-reactive-systems-with-spec-explorer/desc.md)，`Spec Explorer` 更重视 model program 和 model automata 语义，`TIGER` 更重视 `GraphWalker` JSON 与信号脚本映射；相对 [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)，`JTorX` 是在线 derivation/execution 工具，而本文是离线抽象路径到可执行脚本的工业化路线。

## 与本研究的关系

### 对 Project 1 的价值

1. 它展示了从需求到 EFSM 后，仍然需要“抽象路径 -> 工业信号 -> 可执行脚本”的落地层。
2. 对 LLM 生成模型而言，`GraphWalker` 的 `GraphML/JSON` 和 `TIGER` 的 XML 映射提醒我们生成结果应保留可机器消费的变量、guard、action 和 signal name。
3. mutation-based 检查和工业 survey 说明模型可信度与组织采用问题必须一起考虑。

### 作为目标形式主义还是中间表示

更适合作为 `EFSM/GraphWalker` 工具链和测试脚本生成方法路线，而不是新的状态机族本体。

## 重要的相关工作

1. [torx-automated-model-based-testing/desc.md](../torx-automated-model-based-testing/desc.md)：`ioco` 在线模型驱动测试母线。
2. [model-based-testing-of-object-oriented-reactive-systems-with-spec-explorer/desc.md](../model-based-testing-of-object-oriented-reactive-systems-with-spec-explorer/desc.md)：面向对象 model automata 和测试生成路线。
3. [jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md](../jtorx-a-tool-for-on-line-model-driven-test-derivation-and-execution/desc.md)：在线测试派生与执行工具线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 形式主义：`EFSM / GraphWalker / TIGER`
- 论文角色：GraphWalker-based EFSM test-script concretization framework and industrial MBT workflow
- 归类理由：论文主体是围绕 `GraphWalker` EFSM 的测试路径生成、具体化和工业脚本落地方法，属于 `🛠️` 方法路线条目。

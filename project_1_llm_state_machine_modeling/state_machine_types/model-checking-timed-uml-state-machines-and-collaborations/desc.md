# 定时 UML 状态机与协作图的模型检验 / Model Checking Timed UML State Machines and Collaborations

## 基本信息

- 标题：Model Checking Timed UML State Machines and Collaborations
- 中文标题：定时 UML 状态机与协作图的模型检验
- 作者：Alexander Knapp，Stephan Merz，Christopher Rauh
- 发表：*Formal Techniques in Real-Time and Fault-Tolerant Systems*，pp. 395-414，2002
- DOI：`10.1007/3-540-45739-9_23`
- 链接：https://doi.org/10.1007/3-540-45739-9_23
- 形式主义：`Timed UML State Machine / time-annotated UML Collaboration / hugo/RT`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：timed UML -> UPPAAL observer-based verification route / `hugo/RT` prototype
- 工具/实现获取方式：原文明确给出 `hugo/RT` 项目入口 `http://www.pst.informatik.uni-muenchen.de/projekte/hugo/`，并说明 prototype 已实现 timed UML 与 collaboration 到 `UPPAAL` 的翻译；未给独立公开仓库。
- 标准/格式获取方式：输入承载是标准 UML 编辑器导出的 `XMI`、timed UML state machines 与 time-annotated collaborations；输出承载是 `UPPAAL` timed automata network 与 observer timed automaton。

## 简报

这篇论文的重点不是再定义一门新的状态机语言，而是给 timed UML 建了一条可执行的模型检验链：把 timed UML state machines 编译成 `UPPAAL` timed automata，把带时间约束的 UML collaborations 编译成 observer automaton，再检查系统模型是否会把 observer 推入 error state。它补的是 `UML -> verified timed automata` 的验证方法路线和工具原型，而不是新的模型本体。

- 形式主义定位：timed UML 的验证桥接方法与 `hugo/RT` 原型工具，而不是新的状态机家族。
- 构造方式简述：`XMI/UML editor -> timed UML state machines + timed collaborations -> compiled UPPAAL automata + observer -> model checking`。
- 基础设施与场景简述：依托 `hugo/RT`、`UPPAAL`、observer timed automata 与 `XMI` 输入，服务实时面向对象设计中的场景一致性检查。

```text
timed UML design -> state-machine compilation -> queue automata + observer automaton -> UPPAAL check -> scenario consistency result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织其验证链：

1. timed UML state machines。
2. 带时间约束的 UML collaborations。
3. UML 状态机的 active state configuration 与 event queue。
4. 编译得到的 `UPPAAL` timed automata network。
5. 用于描述允许/禁止场景的 observer timed automaton。

### 核心抽象

结合论文对 UML 执行语义与翻译流程的描述，可把单个 UML 状态机在编译前的运行配置保守整理为：

$$
\sigma = (\mathrm{Conf}, Q)
$$

上式中的符号逐项解释如下：

1. `\mathrm{Conf}` 是 UML 状态机当前的 active state configuration。
2. `Q` 是该状态机尚未处理的 event queue。
3. `\sigma` 表示论文在 run-to-completion 语义下分析的离散运行状态。

论文的核心翻译链可以进一步压缩成：

$$
\mathrm{Comp}_{sm}(U) = A_{ctrl}(U) \parallel A_{queue}(U)
$$

$$
\mathrm{Comp}_{col}(C_\tau) = A_{obs}(C_\tau)
$$

$$
A_{ctrl}(U) \parallel A_{queue}(U) \parallel A_{obs}(C_\tau) \models \neg error
$$

上式中的符号逐项解释如下：

1. `U` 是 timed UML state machine 模型。
2. `C_\tau` 是带时间约束的 UML collaboration。
3. `A_{ctrl}` 是表示 UML 状态配置与转移逻辑的 `UPPAAL` automaton。
4. `A_{queue}` 是表示事件队列的 `UPPAAL` automaton。
5. `A_{obs}` 是由 collaboration 生成的 observer timed automaton。
6. `error` 是 observer 中代表场景违规的错误状态。
7. 上述记号是根据论文编译流程做的保守整理，不是原文直接给出的符号系统。

论文还明确给出 timed UML 编译所依赖的三条时间假设：

$$
\mathrm{dur}(\mathrm{RTC}) = 0,\quad \mathrm{dur}(\mathrm{dispatch}) = 0,\quad \mathrm{delay}_{comm} \le \Delta
$$

上式中的符号逐项解释如下：

1. `\mathrm{RTC}` 是 UML 的 run-to-completion step。
2. `\mathrm{dispatch}` 是事件从队列中被 eager 地取出处理的动作。
3. `\mathrm{delay}_{comm}` 是对象间消息发送到接收的通信延迟。
4. `\Delta` 是用户给定的最大网络时延上界。

### 一个最小例子与通俗解释

论文的 benchmark 是 generalized railroad crossing：

1. `track` 对象向 `ctl` 发送 `enter(i)` 与 `exit(i)`。
2. `ctl` 再向 `gate` 发送 `close` 或 `open`。
3. collaboration 用时序约束说明“车来了后门必须在给定时间内关闭”“门刚打开后不能过早又关闭”等场景。
4. `hugo/RT` 把 UML 状态机和协作图一起翻成 `UPPAAL` 模型，然后检查 observer 会不会进入 error。

通俗地说，这条路线像“把 UML 场景图变成一个会盯着系统行为看的裁判自动机”。如果系统的 timed UML 状态机跑出了不该出现的消息顺序或时间间隔，observer 就会报错。

### 运行 / 接受 / 转移语义

论文强调 UML 状态机的本地运行遵循 run-to-completion：

$$
(\mathrm{Conf}, Q) \xrightarrow{e} (\mathrm{Conf}', Q')
$$

其中：

1. `e` 是当前被 dispatcher 取出的事件。
2. 先从 `Q` 中 dequeue 当前事件，再选择 maximal consistent set of enabled transitions。
3. 这些 transitions 会去激活/退出相应状态，并产生新的 `\mathrm{Conf}'` 与 `Q'`。

翻译到 `UPPAAL` 后，原文还强调两条关键执行语义：

1. 每个 UML 状态机被拆成“控制 automaton + 队列 automaton”两部分。
2. collaboration 被翻成 observer automaton，用 reachability/error 检查场景一致性。

### 语义边界

论文对方法边界说得很清楚：

1. `hugo/RT` 只支持 UML 状态机能力的一个子集。
2. history pseudostates、deferred events 仍未实现。
3. 事件不能带参数。
4. 每个类只能有单实例。
5. 论文也明确承认其翻译并非建立在完整的 timed UML formal semantics 之上，而是尽量贴合 UML 非形式化语义要求。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| UML 运行配置 | `$\sigma = (\mathrm{Conf}, Q)$` | 把 active states 与 event queue 作为本地运行状态。 |
| 状态机编译 | `$\mathrm{Comp}_{sm}(U) = A_{ctrl}(U) \parallel A_{queue}(U)$` | 每个 UML 状态机被拆成控制 automaton 与队列 automaton。 |
| 协作图编译 | `$\mathrm{Comp}_{col}(C_\tau) = A_{obs}(C_\tau)$` | 场景约束被翻成 observer timed automaton。 |
| 验证目标 | `$A_{ctrl} \parallel A_{queue} \parallel A_{obs} \models \neg error$` | 若 observer 不可达 error，则该 timed UML 设计满足场景。 |
| 时间假设 | `$\mathrm{dur}(\mathrm{RTC}) = 0,\ \mathrm{delay}_{comm} \le \Delta$` | 采用零时间 RTC 与有界通信延迟。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 UML state machines。 |
| 事件 / 触发 | 很强 | collaboration 里的消息事件与 state machine 触发是主线。 |
| 守卫 / 数据 | 中等支持 | guards 与 attribute updates 会被翻进 `UPPAAL` 变量更新。 |
| 层次 | 中等支持 | 处理 UML 的 hierarchical configuration，但最终会被 flatten 到 `UPPAAL`。 |
| 并发 / 同步 | 强支持 | orthogonal regions、对象间消息与 observer 同步都是关键。 |
| 时间约束 | 很强 | collaboration 上的时间约束与 bounded communication delay 是核心。 |
| 连续动态 / 随机性 | 不支持 | 主体是离散实时对象行为。 |
| 可执行 / 可验证性 | 很强 | 直接落到 `UPPAAL` 做模型检验。 |

### 形式化问题与性质

1. 论文的主问题不是“如何定义 timed UML”，而是“如何把 timed UML + collaboration 变成可验证的 timed automata network”。
2. observer automaton 的引入，使 collaboration 不再只是文档，而是可执行的约束裁判。
3. 这是一条典型的 `UML -> formal backend` 方法路线，与 later runtime / codegen bridges 是不同补点。

## 构造方式与承载格式

### 建模入口

原文中的典型入口是：

1. 在 UML 工具中建模 class diagram、timed state machines 与 collaborations。
2. 导出 `XMI`。
3. 由 `hugo/RT` 读取模型并编译成 `UPPAAL` timed automata。
4. 用 `UPPAAL` 检查 observer 是否进入 error。

### 机器可处理承载方式

机器可处理承载方式包括：

1. UML 编辑器导出的 `XMI`。
2. 表示状态机控制逻辑的 `UPPAAL` automata。
3. 表示事件队列的 `UPPAAL` automata。
4. collaboration 生成的 observer timed automaton。

### 交换与互操作

这篇论文的互操作重点在于：

1. `UML/XMI -> hugo/RT -> UPPAAL`。
2. 用 `UPPAAL` 作为 timed verification backend，而不是另起炉灶设计求解器。
3. 设计模型与场景属性都保留在 UML 这条统一前端上。

## 配套基础设施

- 建模/编辑工具：标准 UML 编辑器。
- 解析/交换/元模型支持：`XMI` 导入。
- 仿真/执行支持：主体不是 simulation，而是编译到 `UPPAAL` 后做 timed reachability/model checking。
- 验证/分析支持：`hugo/RT` + `UPPAAL` + observer automata。
- 代码生成/转换支持：论文不做代码生成，主线是验证翻译。
- 标准化或社区生态：`UML`、`XMI` 与 `UPPAAL` 共同构成核心生态。

## 适用场景与需求前提

### 适用场景

适合已经用 UML 做实时对象设计、同时又希望检查场景与状态机是否时间一致的系统，尤其是嵌入式/实时控制类对象交互。

### 需求前提

1. 行为逻辑已经能落成 timed UML state machines。
2. 关键正确性要求可以表达成带时间约束的 collaborations / sequence-like scenarios。
3. 团队能接受把 UML 模型进一步编译到 `UPPAAL` 进行验证。
4. 模型需落在 `hugo/RT` 当时支持的 UML 子集内。

### 不适用或高成本场景

如果需求主要是连续物理动力学、复杂多实例对象系统，或者高度依赖未支持的 UML 特性，这条路线就会变重。

## 与相邻形式主义的关系

相对 [uml-251-specification/desc.md](../uml-251-specification/desc.md)，它补的是 UML 状态机的 timed verification route；相对 [safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md](../safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md)，它是 `UML -> verifier`，后者是 `verifier -> implementation carrier`；相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，它更偏模型检验前端，而不是 runtime execution bridge。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果 `project_1` 未来选择 UML 状态机作为前端建模载体，完全可以通过翻译链把场景级需求和状态机级行为一起送进 timed model checker。

### 作为目标形式主义还是中间表示

对 `project_1` 来说，timed UML 更像需求侧或设计侧载体，`UPPAAL` timed automata 更像验证中间表示。

### 对需求到模型生成的启发

1. 不要只生成状态机本体，场景级需求也应有可执行承载。
2. 若前端是 UML，一条高价值路线是“保持 UML 前端统一，同时把验证压到成熟后端”。
3. run-to-completion、事件队列、通信延迟这类执行细节必须在桥接层显式建模。

### 现实限制

这是一篇原型级工具论文，覆盖的 UML 子集有限，且不适合作为最终工业执行载体。

## 重要的相关工作

- [uml-251-specification/desc.md](../uml-251-specification/desc.md)：`UML State Machine` 的标准母线。
- [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：总结 UML 状态机形式化与自动验证的整体路线图。
- [safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md](../safety-critical-medical-device-development-using-the-upp2sf-model-translation-tool/desc.md)：另一条“验证模型 -> 工业载体”的桥接工作。
- [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)：`UML -> runtime` 的执行载体方向。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed UML State Machine / time-annotated UML Collaboration / hugo/RT`
- 论文角色：timed UML -> `UPPAAL` observer-based verification route

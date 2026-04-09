# TURTLE：受形式验证工具链支撑的实时 UML Profile / TURTLE: A Real-Time UML Profile Supported by a Formal Validation Toolkit

## 基本信息

- 标题：TURTLE: A Real-Time UML Profile Supported by a Formal Validation Toolkit
- 中文标题：TURTLE：受形式验证工具链支撑的实时 UML Profile
- 作者：Ludovic Apvrille，Jean-Pierre Courtiat，Christophe Lohr，Pierre de Saqui-Sannes
- 发表：*IEEE Transactions on Software Engineering*，30(7): 473-487，2004
- DOI：`10.1109/TSE.2004.34`
- 链接：https://doi.org/10.1109/TSE.2004.34
- 形式主义：`TURTLE / TTool / RT-LOTOS-backed UML profile`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：实时 UML profile 与 press-button formal-validation toolchain
- 工具/实现获取方式：原文直接给出 `TTool` 与 `RTL` 两个工具入口；当前公开材料仍可从 `ttool.telecom-paris.fr` 追溯到 `TTool`、文档和示例。
- 标准/格式获取方式：核心承载是 `TURTLE` 对 `UML 1.5` 类图与活动图的扩展，语义后端是自动生成的 `RT-LOTOS` 规格。

## 简报

这篇论文的关键贡献，不只是再定义一个实时 UML profile，而是把“图形建模”和“形式验证后端”压到一条真正可操作的链路里。`TURTLE` 用 `Tclasses`、gates、组合算子和时间算子把实时任务结构化，再由 `TTool` 自动翻译成 `RT-LOTOS` 并调用 `RTL` 做仿真与可达性分析。

- 形式主义定位：面向实时嵌入式任务的 `UML 1.5` profile，强调组合结构、时间行为和隐藏式 formal backend。
- 构造方式简述：用扩展类图描述 `Tclasses` 与组合关系，用扩展活动图描述内部行为，再自动生成 `RT-LOTOS`。
- 基础设施与场景简述：依托 `TTool` 图形编辑器、`RT-LOTOS` 代码生成、`RTL` 仿真/穷举分析，适合早期实时嵌入式控制设计与设计期错误发现。

```text
UML 1.5 class/activity diagrams -> TURTLE profile operators -> RT-LOTOS translation -> RTL simulation / reachability analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Tclass` 与 gate-based communication。
2. 类图级组合算子：`Parallel`、`Synchro`、`Sequence`、`Preemption`，以及扩展后的 `Invocation`、`Periodic`、`Suspend/Resume`。
3. 活动图级同步与时间算子：deterministic delay、nondeterministic delay、time-limited offer、time capture。
4. `TTool -> RT-LOTOS -> RTL` 的自动翻译与验证链路。

### 核心抽象

结合论文对类图、活动图和组合算子的描述，可把一个 `TURTLE` 模型保守整理为：

$$
M = (\mathcal{T}, G, R, A, \Theta)
$$

上式中的符号逐项解释如下：

1. `\mathcal{T}` 是 `Tclasses` 集合，每个 `Tclass` 对应一个可组合的任务或组件。
2. `G` 是 gates 集合，用于内部动作或跨 `Tclass` 同步。
3. `R` 是类图层的组合关系集合，关系上带有 `Parallel / Synchro / Sequence / Preemption / Invocation / Periodic / Suspend` 等算子。
4. `A` 是与各 `Tclass` 绑定的活动图集合。
5. `\Theta` 是活动图中的时间与同步算子集合。
6. 这组元组是对论文结构的保守归纳，不是原文显式给出的统一单式定义。

论文直接给出 `TURTLE` 的形式语义入口是“两步翻译”：

$$
\llbracket M \rrbracket_{RT\text{-}LOTOS} = \mathrm{Step}_2(\mathrm{Step}_1(A), R)
$$

上式中的符号逐项解释如下：

1. `\mathrm{Step}_1(A)` 表示先把每个活动图翻成一个 `RT-LOTOS` 过程。
2. `\mathrm{Step}_2(\cdot, R)` 表示再根据类图中的组合关系把这些过程组合起来。
3. `\llbracket M \rrbracket_{RT\text{-}LOTOS}` 是最终交给 `RTL` 的 `RT-LOTOS` 规格。
4. 这是对论文第 4 节两步翻译算法的符号化压缩。

论文还给了一个很有代表性的组合语义例子：

$$
P_{1.2} = P_{1.1} \gg (P_{2.2} \mid[g]\mid P_{3.2})
$$

上式中的符号逐项解释如下：

1. `P_{1.1}` 是 `T_1` 活动图在第一步翻译得到的过程。
2. `P_{1.2}` 是第二步把组合关系也编进去后的过程。
3. `\gg` 表示先顺序执行 `P_{1.1}`，再执行后续结构。
4. `\mid[g]\mid` 表示 `P_{2.2}` 与 `P_{3.2}` 在 gate `g` 上同步组合。
5. 这正是论文用于解释 `Sequence + Synchro` 联合翻译的例子。

### 一个最小例子与通俗解释

一个最小直觉例子是“采样任务 + 分析任务”的实时组合：

1. `SensorTask` 周期性触发一次采样。
2. `AnalyzerTask` 等待 `SensorTask` 在 gate 上同步交付数据。
3. 如果分析需要调用某个辅助处理任务，就用 `Invocation` 把该任务插入调用流。
4. 如果某个高优先级任务到来，还可以通过 `Preemption` 或 `Suspend/Resume` 中断或挂起当前任务。

通俗地说，`TURTLE` 像是把“实时任务图”和“形式验证后端”焊在一起。建模者画的是 UML 风格图，但真正跑分析时，底层已经自动变成 `RT-LOTOS` 过程代数模型。

### 运行 / 接受 / 转移语义

运行语义的核心是：

1. `Tclass` 之间通过 gate 做 rendezvous 风格同步。
2. 活动图内部既能表达普通控制流，也能表达延迟、时间窗口与 time capture。
3. 类图层的组合算子负责决定任务之间是并发、同步、顺序、调用还是抢占/挂起关系。
4. 最终行为语义不直接由图执行，而是通过自动翻译后的 `RT-LOTOS` 过程来解释。

### 语义边界

边界也很明确：

1. `TURTLE` 不是完整 `UML 2` 状态机语义，而是基于 `UML 1.5` 类图和活动图的专门 profile。
2. 它依赖 `RT-LOTOS` 作为正式语义后端，因此表达与验证能力最终受后端可分析性限制。
3. 穷举验证只适用于有限行为或在可接受状态空间内的模型，超大系统仍会遇到 state explosion。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$M = (\mathcal{T}, G, R, A, \Theta)$` | `TURTLE` 把任务、gate、组合关系、活动图和时间算子合在一起。 |
| 语义落点 | `$\llbracket M \rrbracket_{RT\text{-}LOTOS} = \mathrm{Step}_2(\mathrm{Step}_1(A), R)$` | 形式语义依赖“两步翻译到 RT-LOTOS”。 |
| 组合示例 | `$P_{1.2} = P_{1.1} \gg (P_{2.2} \mid[g]\mid P_{3.2})$` | 顺序与同步组合被压成后端过程代数结构。 |
| 验证入口 | `$\mathrm{Reachability}(\llbracket M \rrbracket_{RT\text{-}LOTOS})$` | `RTL` 对翻译结果做仿真和可达性分析。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 更强调任务/活动流，而不是经典状态机中的状态节点语义。 |
| 事件 / 触发 | 很强 | gates 和同步动作是一等对象。 |
| 守卫 / 数据 | 中等支持 | 支持通过 gate 参数和属性交换数据，但不是重数据建模语言。 |
| 层次 | 中等支持 | 主要体现在任务结构和活动子过程，不是 Harel 式层次状态机。 |
| 并发 / 同步 | 很强 | `Parallel`、`Synchro`、`Sequence`、`Preemption` 等是核心。 |
| 时间约束 | 很强 | delay、time-limited offer、time capture、periodic、suspendable operators 都是亮点。 |
| 连续动态 / 随机性 | 不支持 | 目标是实时离散任务系统，不是混成或随机系统。 |
| 可执行 / 可验证性 | 很强 | `TTool` 和 `RTL` 提供自动翻译、仿真与穷举分析。 |

### 形式化问题与性质

1. `TURTLE` 的主价值在于让 `UML` 风格建模结果具有可验证语义落点，而不是停留在图形草图层。
2. 类图层组合算子和活动图层时间算子的分层设计，使其比直接画普通活动图更适合实时任务组织。
3. 方法链路是“图形 profile -> 自动翻译 -> 形式验证”，而不是“手工重写成另一门形式语言”。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 用扩展类图定义 `Tclasses`、gates 和组合关系。
2. 用扩展活动图描述每个 `Tclass` 的内部行为。
3. 在 `TTool` 中做语法检查。
4. 自动生成 `RT-LOTOS` 规格并提交给 `RTL`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `TTool` 内部的 `TURTLE` 图模型；
2. 组合算子的 OCL 风格门连接说明；
3. 自动生成的 `RT-LOTOS` 代码；
4. `RTL` 输出的仿真轨迹与可达图。

### 交换与互操作

这条线的互操作重点在于：

1. 前端用 `UML`-like profile 保持工程可读性；
2. 后端用 `RT-LOTOS` 获得正式语义；
3. `TTool` 负责屏蔽形式语言细节，把验证入口做成 press-button 工作流。

## 配套基础设施

- 建模/编辑工具：`TTool` 提供 `TURTLE` 类图/活动图编辑器与语法检查。
- 解析/交换/元模型支持：`TURTLE` profile 基于 `UML 1.5` 扩展，后端自动生成 `RT-LOTOS`。
- 仿真/执行支持：`RTL` 可做随机仿真并返回时间标记轨迹，`TTool` 再映射回原图。
- 验证/分析支持：`RTL` 提供 reachability graph 与 observer-based property verification。
- 代码生成/转换支持：核心是 `TURTLE -> RT-LOTOS` 自动翻译，而不是部署代码生成。
- 标准化或社区生态：依托 `UML` profile、`RT-LOTOS` 和 `TTool` 研究生态，属于“工程图形语言 + 形式后端”路线。

## 适用场景与需求前提

### 适用场景

适合实时嵌入式控制软件、任务级并发结构清晰的系统、以及希望在早期设计阶段就检查时序和逻辑错误的工程场景。

### 需求前提

1. 系统能拆成有限个显式任务或组件。
2. 任务之间的交互适合抽成 gate 同步或顺序/抢占关系。
3. 关键实时要求可写成 delay、offer、periodic、suspend 这类离散时间算子。
4. 团队愿意接受“图形前端 + 形式后端”的双层工作流。

### 不适用或高成本场景

如果系统核心是连续动力学、概率不确定性，或高度依赖复杂数据结构，`TURTLE` 的收益会明显下降；若模型过大，后端 reachability 也会很快遇到规模瓶颈。

## 与相邻形式主义的关系

相对 [uml-251-specification/desc.md](../uml-251-specification/desc.md)，`TURTLE` 更窄、更偏实时任务与形式验证；相对 [avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md](../avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md)，它更早、后端更偏 `RT-LOTOS`，而 `AVATAR` 进一步把 `UPPAAL/ProVerif` 和 safety/security 统一进来；相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，`TURTLE` 强在工程化 profile 与隐藏式后端，而 `UPPAAL` 更直接面向 timed automata。

## 与本研究的关系

### 对 Project 1 的价值

它说明一个很重要的落地方向：不一定非要让 LLM 直接生成底层形式模型，也可以先生成领域化图形 profile，再自动落到验证后端。

### 作为目标形式主义还是中间表示

更适合作为目标 DSL 或高层中间表示，而不是最终底层验证对象。

### 对需求到模型生成的启发

1. 需求里若天然存在任务、同步和时序窗口，先抽成 `Tclass + gate + composition operator` 会比直接写后端公式更稳。
2. “隐藏 formal backend” 是非常现实的工程策略，能降低对最终用户的形式方法门槛。
3. 组合算子应当被显式建模，而不是散落到普通边和注释里。

### 现实限制

它仍然依赖专用工具链与翻译器，且基于 `UML 1.5` 的 profile 设计与当前主流工业工具生态并不完全同构。

## 重要的相关工作

1. [avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md](../avatar-a-sysml-environment-for-the-formal-verification-of-safety-and-security-properties/desc.md)：同一 `TTool` 生态继续向 `SysML + UPPAAL/ProVerif` 扩展的代表条目。
2. [an-automatic-approach-to-model-checking-uml-state-machines/desc.md](../an-automatic-approach-to-model-checking-uml-state-machines/desc.md)：另一条 `UML` 行为模型到形式验证后端的自动桥接路线。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：`UML` 行为模型自动验证的系统盘点入口。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 归类理由：`TURTLE` 虽然包含 profile 本体，但这篇论文的可复用价值主要落在“`TTool + RT-LOTOS + RTL` 的隐藏式验证基础设施”与工程化工作流上，因此按 `🏗️` 记录更合适。

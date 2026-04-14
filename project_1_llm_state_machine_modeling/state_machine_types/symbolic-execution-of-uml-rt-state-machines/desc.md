# UML-RT 状态机的符号执行 / Symbolic Execution of UML-RT State Machines

## 基本信息

- 标题：Symbolic Execution of UML-RT State Machines
- 中文标题：UML-RT 状态机的符号执行
- 作者：Karolina Zurowska，Juergen Dingel
- 发表：*Proceedings of the 27th Annual ACM Symposium on Applied Computing*，pp. 1292-1299，2012
- DOI：`10.1145/2245276.2231981`
- 链接：https://doi.org/10.1145/2245276.2231981
- 形式主义：`UML-RT State Machine / FFSM / symbolic execution`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：symbolic-execution method for `UML-RT` state machines with modular action-code treatment
- 工具/实现获取方式：原文明确说明实现为 Eclipse plug-ins，可集成到 `IBM RSA-RTE`，并用于 `UML-RT` symbolic execution、分析与测试生成；正文未给稳定公开仓库 URL。
- 标准/格式获取方式：主承载是 `UML-RT` state machines、翻译得到的 `FFSM`、symbolic execution tree 与 action-code symbolic summaries；它不是交换标准。

## 简报

这篇论文补的是 `UML-RT` 线上非常有代表性的“方法层”条目。它并不是把 `UML-RT` 再翻译成另一门逻辑就结束，而是提出了一个中间形式 `FFSM`，再在 `FFSM` 上做符号执行，从而把 reachability、invariant checking、output analysis 和 test generation 串起来。论文最大的工程亮点是 action code 的模块化处理：状态机控制结构与动作代码的符号执行被刻意解耦，这让不同 action languages 能通过可插拔方式接入。

- 形式主义定位：围绕 `UML-RT State Machine` 的 symbolic-execution 方法路线，而不是新的状态机子类。
- 构造方式简述：`UML-RT State Machine -> FFSM -> symbolic execution tree`，动作代码通过 guard/update/output functions 摘要进 `FFSM`。
- 基础设施与场景简述：依托 Eclipse plug-ins、`IBM RSA-RTE` 集成、`FFSM` 翻译与 symbolic execution tree，服务早期模型分析、reachability、invariant checking 与 test generation。

```text
UML-RT state machine -> FFSM with functional labels -> symbolic execution tree -> reachability / invariant / output / test analyses
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML-RT State Machines`。
2. domains、variables 与 action languages。
3. functional finite state machines (`FFSMs`)。
4. concrete execution semantics 与 symbolic execution tree。
5. `UMLRT2FFSM` 翻译与 Eclipse 实现。

### 核心抽象

论文首先定义 domain：

$$
D = (U, F, R, X)
$$

上式中的符号逐项解释如下：

1. `U` 是取值域。
2. `F` 是可用函数集合。
3. `R` 是关系集合。
4. `X` 是变量集合。
5. 这是论文 `Definition 1` 给出的基础语义域。

`FFSM` 的核心元组为：

$$
F = (L, V, AV, A, GF, UF, OF, T, l_0, v_0)
$$

上式中的符号逐项解释如下：

1. `L` 是 locations 集合。
2. `V` 是 machine variables。
3. `AV` 是 action variables。
4. `A` 是 actions 集合。
5. `GF`、`UF`、`OF` 分别是 guard、update、output functions 集合。
6. `T` 是 transitions。
7. `l_0` 与 `v_0` 分别是初始位置和初始变量赋值。
8. 这是论文 `Definition 3` 的核心对象。

`FFSM` 的具体执行语义写成：

$$
E(F) = (S, Tr, s_0)
$$

上式中的符号逐项解释如下：

1. `S` 是 concrete states 集合。
2. `Tr` 是 concrete transitions。
3. `s_0` 是初始 concrete state。
4. 这是论文 `Definition 4` 给出的 labeled transition system 语义。

符号执行树则写成：

$$
SE(F) = (S_s, AV_s, Tr_s, s^s_0)
$$

上式中的符号逐项解释如下：

1. `S_s` 是 symbolic states 集合。
2. `AV_s` 是符号化 action variables。
3. `Tr_s` 是 symbolic transitions。
4. `s^s_0` 是初始 symbolic state。
5. 这是论文 `Definition 6` 的核心对象。

论文还给出 soundness 方向的核心结论，可保守写成：

$$
\forall p \in paths(E(F))\ \exists p_s \in paths_s(SE(F)) : p \models p_s
$$

上式中的符号逐项解释如下：

1. `paths(E(F))` 是具体执行路径集合。
2. `paths_s(SE(F))` 是符号执行路径集合。
3. `p \models p_s` 表示某条 concrete path 被某条 symbolic path 覆盖。
4. 这就是论文 `Theorem 1` 的核心含义。

### 一个最小例子与通俗解释

论文里最小示例是一个含变量 `v1`、`v2` 的 `FFSM`：

1. 转移上不再直接挂具体动作代码，而是挂 `guard / update / output` functions。
2. 当输入 action 到来时，符号执行不会立刻求所有具体值，而是把约束累积到 symbolic path 上。
3. 如果 action code 本身较复杂，就先单独做其 symbolic execution，再把结果折成函数集合塞回 `FFSM`。
4. 最终得到的 symbolic execution tree 可以直接回答某个 location 是否可达，或者某个 output 是否可能出现。

通俗地说，这套方法像是把 `UML-RT` 状态机的“控制壳”和“动作代码”拆开：外层状态机负责走图，内层动作代码只提供可组合的符号函数摘要。这样就不会把整个分析流程绑死在某一种宿主语言上。

### 运行 / 接受 / 转移语义

论文的方法链可保守写成：

$$
\mathrm{UML\text{-}RT} \xrightarrow{\mathrm{UMLRT2FFSM}} F \xrightarrow{\mathrm{FFSM2SET}} SE(F)
$$

上式中的符号逐项解释如下：

1. `UMLRT2FFSM` 负责把 `UML-RT` 状态机映成 `FFSM`。
2. `FFSM2SET` 负责构造 symbolic execution tree。
3. 最终分析对象是 `SE(F)`，而不是直接在原图上硬做符号搜索。

### 语义边界

1. 论文主线是 `UML-RT`，不是完整 `UML 2 State Machine` 全语义。
2. 它假定 action code 能被独立做 symbolic execution 或摘要。
3. 强项是模型分析与测试生成，不是最终代码部署。
4. 对复杂并发胶合、跨 capsule 组合分析，正文只给出后续工作方向。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| domain | `$D = (U,F,R,X)$` | 动作代码与变量语义的基础域。 |
| `FFSM` 骨架 | `$F = (L,V,AV,A,GF,UF,OF,T,l_0,v_0)$` | `UML-RT` 状态机被翻译后的核心对象。 |
| 具体语义 | `$E(F) = (S,Tr,s_0)$` | `FFSM` 的 concrete execution semantics。 |
| 符号执行树 | `$SE(F) = (S_s,AV_s,Tr_s,s^s_0)$` | 论文真正用于分析的工件。 |
| 覆盖性 | `$\forall p \in paths(E(F))\ \exists p_s \in paths_s(SE(F)) : p \models p_s$` | symbolic execution tree 覆盖 concrete behaviors。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 核心对象就是 `UML-RT` 状态机与其 `FFSM` 映射。 |
| 事件 / 触发 | 很强 | 输入/output actions 是 transition labels 的主体。 |
| 守卫 / 数据 | 很强 | guard/update/output functions 正是方法中心。 |
| 层次 | 中等支持 | `UML-RT` 有层次状态，但翻译时会展开成 `FFSM` locations。 |
| 并发 / 同步 | 弱到中等 | 主要分析单个 state machine；跨 capsule 组合是后续方向。 |
| 时间约束 | 不支持 | 不是 timed `UML-RT` 论文。 |
| 连续动态 / 随机性 | 不支持 | 不在范围内。 |
| 可执行 / 可验证性 | 很强 | symbolic execution tree 可直接支撑多类分析与 test generation。 |

### 形式化问题与性质

1. 本文的核心不是单纯做 symbolic execution，而是先构造一个适合承载动作摘要的 `FFSM` 中间层。
2. 模块化 action-code treatment 让工具不至于被单一 action language 锁死。
3. 这条路线也比直接 flatten 成普通 transition system 更保留工程结构。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `UML-RT` 状态机模型。
2. action code 及其宿主语言。
3. `UMLRT2FFSM` 生成的 `FFSM`。
4. `FFSM2SET` 生成的 symbolic execution tree。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `UML-RT` states/transitions/events。
2. `FFSM` 中的 guard/update/output functions。
3. symbolic states、path conditions 与 output sequences。
4. test cases 与 analysis queries。

### 交换与互操作

互操作重点在于：

1. `UML-RT` 前端并不直接决定分析算法，而是先落到 `FFSM`。
2. action code 可以通过外部 symbolic execution engine 接入。
3. 工具实现为 Eclipse plug-ins，可挂到 `IBM RSA-RTE` 环境。

## 配套基础设施

- 建模/编辑工具：`IBM RSA-RTE` 与 Eclipse plug-ins。
- 解析/交换/元模型支持：`UMLRT2FFSM` 翻译、函数摘要与 symbolic tree 构造。
- 仿真/执行支持：重点是 symbolic execution，不是普通解释执行。
- 验证/分析支持：reachability analysis、invariant checking、output analysis、test case generation。
- 代码生成/转换支持：主线是 `UML-RT -> FFSM` 翻译，不主打部署代码生成。
- 标准化或社区生态：依托 `UML-RT`、Eclipse 与工业建模工具生态。

## 适用场景与需求前提

### 适用场景

适合 `UML-RT` 设计期模型分析、嵌入式软件行为检查、早期测试用例生成，以及需要在不抛弃图形化模型的前提下做符号级推理的场景。

### 需求前提

1. 行为模型需能落成 `UML-RT` 状态机子集。
2. action code 需能被摘要成 guard/update/output functions。
3. 目标问题更偏路径、可达性、不变式与输出分析，而非连续时间。
4. 团队接受中间层 `FFSM` 的建模与分析工作流。

### 不适用或高成本场景

若系统重心在完整 UML 全语义、复杂多组件并发耦合、实时/连续行为或最终部署代码生成，这条路线就不是最直接的入口。

## 与相邻形式主义的关系

相对 [execution-of-partial-state-machine-models/desc.md](../execution-of-partial-state-machine-models/desc.md)，`PMExec` 关注不完整 `UML-RT` 模型怎样先执行起来，而本文关注完整状态机怎样做符号执行与分析；相对 [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)，`UMerL` 更偏执行/模型检查基础设施，而本文更偏 `FFSM` 上的 symbolic analysis method；相对 [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)，本文是 survey 中“direct symbolic analysis of UML-family state machines” 的代表方法条目。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明 `UML-RT` 这类工业状态机并不一定要先翻成别的验证语言，才能进入符号分析。
2. `FFSM` 这种中间层对 LLM 生成状态机后的自动验证很有启发，因为它把结构与动作摘要拆开了。
3. 对 `project_2` 和 `project_4`，symbolic paths、path conditions 与 test-case generation 都是直接可复用的思路。

### 作为目标形式主义还是中间表示

更像目标形式主义上的分析方法与中间语义层，而不是新的状态机本体。

### 对需求到模型生成的启发

1. 需求生成阶段应尽量把 guard、update、output 分开表达，避免全塞进自然语言动作块。
2. 若模型动作代码无法直接验证，可以先把其效果摘要成函数对象。
3. 中间层设计得好，后续 reachability、invariant、test generation 都能共用同一符号工件。

### 现实限制

方法很强于 `UML-RT` symbolic analysis，但对完整多 capsule 系统组合、时钟语义和最终代码执行链支持有限。

## 重要的相关工作

1. [execution-of-partial-state-machine-models/desc.md](../execution-of-partial-state-machine-models/desc.md)：`UML-RT` 上的 partial-model execution 路线。
2. [execution-and-verification-of-uml-state-machines-with-erlang/desc.md](../execution-and-verification-of-uml-state-machines-with-erlang/desc.md)：完整 `UML State Machine` 的执行/验证基础设施。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：UML 状态机形式化与自动验证全景综述。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML-RT State Machine / FFSM / symbolic execution`
- 归类理由：论文核心贡献是 `UML-RT` 的 symbolic-execution 方法与 `FFSM` 中间层，而不是新的 UML profile 或通用运行时基础设施，因此按 `🔣/🛠️` 处理更准确。

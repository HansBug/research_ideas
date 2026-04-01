# 计划执行交换语言（PLEXIL） / Plan Execution Interchange Language (PLEXIL)

## 基本信息

- 标题：Plan Execution Interchange Language (PLEXIL)
- 中文标题：计划执行交换语言（PLEXIL）
- 作者：Tara Estlin, Ari Jonsson, Corina Pasareanu, Reid Simmons, Kam Tso, Vandi Verma
- 发表：NASA Technical Memorandum `NASA/TM-2006-213483`, NASA Ames Research Center, 2006
- DOI：原文未提供
- 链接：https://ntrs.nasa.gov/citations/20060019246
- 形式主义：`PLEXIL`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：计划执行语言 / 执行载体
- 工具/实现获取方式：原文明确给出 `PLEXIL` universal executive、`CLARAty` 接口、`PLEXIL Plan Editor` 和计划验证/测试生成方向，但未提供独立公开仓库。
- 标准/格式获取方式：原文明确说明执行计划会以 `XML` 形式发送给 executive，并给出 `Node/NodeList/Command/Assignment` 语法、domain description 与 plan editor 导出 XML 示例。

## 简报

这篇论文讨论的重点不是“怎么做规划”，而是“规划结果怎样以统一、可执行、可验证的状态机式语言交给执行器”。`PLEXIL` 用分层 execution node 树描述执行逻辑，节点由 `StartCondition / EndCondition / InvariantCondition` 等条件驱动，通过 `Command` 和 `Assignment` 与真实硬件或功能层交互。它的目标是把不同 planner 产出的高层决策，统一落到同一套 plan execution language 和 universal executive 上。

- 形式主义定位：面向航天器 / 火星车自主任务的层次化计划执行语言，而不是面向求解的 planner 表示。
- 构造方式简述：以 `NodeList / Command / Assignment` 三类节点构造树形执行结构，再为每个节点附加条件、变量、接口和 domain description 中的 lookup / command 声明。
- 基础设施与场景简述：依托 `XML PLEXIL`、universal executive、`CLARAty` 功能层接口、plan editor 与后续 `Java PathFinder` 验证设想，服务 spacecraft / rover autonomy。

```text
任务需求 / planner 输出 -> PLEXIL node tree -> XML plan + domain description -> universal executive / CLARAty -> 实际命令执行 / 监控 / 验证
```

## 形式主义定义与核心对象

### 定义对象

`PLEXIL` 把一个执行计划看成一棵层次化 execution node 树。叶节点执行命令或赋值，内部节点负责控制结构。每个节点本身不是“状态图上的一个状态”，而是一个带条件、变量和接口的执行单元；真正的执行状态由 runtime 里的 node state 与 outcome 决定。

### 核心抽象

论文没有把 `PLEXIL` 压成单个数学元组，这里根据正文与 grammar 做保守整理：

$$
P = (N, n_0, child, type, attr, body, D)
$$

上式中的符号逐项解释如下：

1. `N` 是 plan 中全部 execution node 的集合。
2. `n_0 \in N` 是根节点。
3. `child \subseteq N \times N` 是父子层次关系。
4. `type : N \to \{\mathrm{NodeList}, \mathrm{Command}, \mathrm{Assignment}\}` 给出节点类型。
5. `attr(n)` 是节点 `n` 的属性集合。
6. `body(n)` 是节点主体，对应子节点列表、命令调用或赋值语句。
7. `D` 是 domain description，给出可 lookup 的状态名、command/function 声明和可选 interrupt handler。

节点属性在 grammar 中被明确写成：

$$
attr(n) = (sc, ec, pc, poc, ic, rc, pri, vars, intf)
$$

其中：

1. `sc` 是 `StartCondition`。
2. `ec` 是 `EndCondition`。
3. `pc` 是 `PreCondition`。
4. `poc` 是 `PostCondition`。
5. `ic` 是 `InvariantCondition`。
6. `rc` 是 `RepeatUntilCondition`。
7. `pri` 是优先级。
8. `vars` 是局部变量声明。
9. `intf` 是 `in / inout` 接口变量。

论文还显式给出了 node 的执行状态和值域：

$$
state(n) \in \{\mathrm{WAITING}, \mathrm{EXECUTING}, \mathrm{FINISHING}, \mathrm{FAILING}, \mathrm{FINISHED}, \mathrm{COMMAND\_FAILING}\}
$$

$$
outcome(n) \in \{\mathrm{SUCCESS}, \mathrm{FAILURE}, \mathrm{SKIPPED}, \mathrm{INFINITE\_LOOP}\}
$$

这些符号逐项解释如下：

1. `state(n)` 是节点 `n` 当前的执行阶段。
2. `WAITING` 表示尚未开始，等待触发条件成立。
3. `EXECUTING` 表示节点正在运行。
4. `FINISHING / FAILING / COMMAND_FAILING` 表示收尾或失败相关阶段。
5. `FINISHED` 表示节点已进入终止 sink state。
6. `outcome(n)` 则单独记录执行结果，不和 `state(n)` 混写。

### 一个最小例子与通俗解释

论文最直观的例子是“先驱动 rover，直到目标可见或超时，再做不同后续动作”：

1. `Drive` 节点调用 `rover_drive(10)`。
2. 若 `AbsoluteTimeWithin{10, +INF}` 触发，则执行 `rover_stop()` 并记 `timeout = true`。
3. 若 `LookupWithFrequency{target_in_view, 10} == true`，则执行 `rover_stop()` 并记 `drive_done = true`。
4. 若 `timeout == true`，执行 `take_navcam()`；若 `drive_done == true`，执行 `take_pancam()`。
5. 另一个并列节点在温度低于 `0` 时启动加热器，直到温度达到 `10`。

通俗地说，`PLEXIL` 像“给 planner 输出套上一棵可执行的条件树”。树上的每个节点都知道自己什么时候能开始、什么时候必须结束、失败时怎么处理、该向功能层发什么命令，以及要读取哪些世界状态。

### 运行 / 接受 / 转移语义

论文强调 `PLEXIL` 的执行是事件驱动且同步收敛到 quiescence 的。可将执行配置保守写成：

$$
c = (\sigma, \omega, \nu, \lambda)
$$

其中：

1. `\sigma` 给出所有节点的 `state`。
2. `\omega` 给出所有节点的 `outcome`。
3. `\nu` 是局部变量、接口变量和内部 node variables 的当前取值。
4. `\lambda` 是当前可见的 lookup / command 返回信息。

论文对执行步的核心描述可压成：

$$
c \xrightarrow{e} c'
\iff
\text{all condition changes affected by } e \text{ are processed until quiescence}
$$

上式中的符号逐项解释如下：

1. `e` 是外部事件、lookup 值变化、时间事件或内部 node state 变化。
2. 一次执行步不是只让一个节点简单跳转，而是把事件触发的 condition changes 按优先级处理到底。
3. 当所有相关节点都重新落回“等待外部事件”的稳定点时，本步才结束。

节点层面的触发则可保守写成：

$$
state(n)=\mathrm{WAITING} \land sc_n \Rightarrow state'(n)=\mathrm{EXECUTING}
$$

$$
state(n)=\mathrm{EXECUTING} \land ec_n \Rightarrow state'(n)=\mathrm{FINISHING}
$$

$$
state(n)=\mathrm{EXECUTING} \land \neg ic_n \Rightarrow state'(n)=\mathrm{FAILING}
$$

这三条规则对应论文图 6 到图 12 中 node transition diagram 的主干直觉：启动由 `StartCondition` 驱动，正常结束由 `EndCondition` 驱动，违反不变式则进入失败路径。

### 语义边界

`PLEXIL` 的语义边界也很清楚：

1. 它是执行语言，不是 planner 建模语言。
2. 它支持层次、循环、并发、时间与事件条件，但不直接建模连续动力学。
3. 它依赖 domain description 中的 world state、command 和 function 接口，不能脱离功能层独立表达完整物理系统。
4. 论文强调“给定同一测量序列时 deterministic”，因此它不是面向非确定探索的高层行为树语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 计划骨架 | `$P = (N, n_0, child, type, attr, body, D)$` | `PLEXIL` 本体是带属性和 domain description 的层次 node 树。 |
| 节点属性 | `$attr(n) = (sc, ec, pc, poc, ic, rc, pri, vars, intf)$` | 启停、约束、变量和接口都是一级对象。 |
| 节点状态 | `$state(n) \in \{\mathrm{WAITING}, \mathrm{EXECUTING}, \mathrm{FINISHING}, \mathrm{FAILING}, \mathrm{FINISHED}, \mathrm{COMMAND\_FAILING}\}$` | 运行时语义明确以 node-state machine 形式给出。 |
| 执行收敛 | `$c \xrightarrow{e} c' \iff$ 受 `e` 影响的 condition changes 被处理到 quiescence` | 一次事件会级联驱动多个节点变化，直到稳定。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 用 node state 与层次 node tree 管理执行模式。 |
| 事件 / 触发 | 强支持 | 支持 `LookupOnChange`、`LookupWithFrequency`、时间触发与内部 node event。 |
| 守卫 / 数据 | 强支持 | Boolean / temporal 条件、局部变量、接口变量和内部变量都进入控制逻辑。 |
| 层次 | 强支持 | `NodeList` 构成树形层次。 |
| 并发 / 同步 | 支持 | 同一计划中可表达并列活动，但执行语义仍按同步 quiescence 处理。 |
| 时间约束 | 强支持 | `AbsoluteTimeWithin`、`CurrentTimeWithin` 等直接进入条件。 |
| 连续动态 / 随机性 | 不支持 | 原文只覆盖离散执行控制。 |
| 可执行 / 可验证性 | 强支持 | 目标就是驱动 universal executive，并显式面向 plan verification / testing。 |

### 形式化问题与性质

1. `PLEXIL` 明确区分 `state` 和 `outcome`，这让“节点是否已经终止”和“节点执行是否成功”能分别编码。
2. command 调用不会阻塞整个执行语义，但 command node 自身会在命令完成前保持活动。
3. 只有 `LookupNow` 可用于 check conditions，而 event/frequency lookup 用于 gate conditions，这强约束了语言的可分析性。
4. 论文专门给出 context-free grammar、XML 承载和后续 model checking 计划，说明它从一开始就按“可机读、可验证”设计。

## 构造方式与承载格式

### 建模入口

建模入口分三层：

1. 计划层：`Node / NodeList / Command / Assignment` 树。
2. 约束层：`StartCondition / EndCondition / InvariantCondition / RepeatUntilCondition` 等条件。
3. 接口层：domain description 中的 `StateVariables`、`FunctionDeclaration`、`FunctionInterrupt`。

### 机器可处理承载方式

原文明确说明：

1. 人可读层是 `PLEXIL` 文本语法。
2. 机器发送给 executive 的实际载体是 `XML`。
3. 计划编辑器可把图形模型导出为 `PLEXIL XML representation`。

### 交换与互操作

`PLEXIL` 的互操作重点不是跨行业标准，而是 planner 与 executive、decision layer 与 functional layer 之间的交换：

1. 上游可由 `CASPER`、`PICO` 等 planner 生成 `PLEXIL`。
2. 下游通过 domain description 和 `CLARAty` / functional layer 对接真实命令与状态。
3. 因而它本质上是一个 execution interchange language，而不是单纯的图形状态图文件格式。

## 配套基础设施

- 建模/编辑工具：论文附录给出 `PLEXIL Plan Editor`，基于 Eclipse/GEF，支持节点编辑、属性面板和 XML 导出。
- 解析/交换/元模型支持：原文给出 context-free grammar、XML schema 方向和 domain description 机制。
- 仿真/执行支持：核心是 universal executive，与 `CLARAty` 功能层接口衔接。
- 验证/分析支持：论文明确提出 plan verification、`Java PathFinder` model checking、test plan generation。
- 代码生成/转换支持：支持从 planner 产出 `PLEXIL`，也支持 plan editor 导出 XML。
- 标准化或社区生态：生态以 NASA/JPL 自主任务和执行框架为中心，工程上清晰但开放标准色彩较弱。

## 适用场景与需求前提

### 适用场景

适合自主航天器、火星车、复杂机器人任务执行，以及任何“需要把 planner 输出稳定交给 executive 执行”的场景。

### 需求前提

1. 任务可以分解成有限个带条件的执行节点。
2. 外部世界状态可通过 lookup 读取，动作可通过 command 调用。
3. 需要显式表达时间窗、等待条件、中止条件和重复条件。
4. 希望计划既可执行又可被验证和测试。

### 不适用或高成本场景

若目标是连续控制律建模、复杂概率决策、或缺少明确 functional layer 接口，`PLEXIL` 就不自然；若只需要轻量脚本式流程控制，它也可能显得过重。

## 与相邻形式主义的关系

相对 `PDDL/HTN` 一类 planner 表示，`PLEXIL` 更靠近执行端；相对 `SCXML/UML State Machine`，它更强调 command/lookup 和任务执行条件，而不是通用交互标准；相对普通层次状态机，它多了一整套 plan-level 条件、接口和 verification-friendly 语义。

## 与本研究的关系

### 对 Project 1 的价值

`PLEXIL` 是很强的“应用侧执行载体”证据：即便上游生成的是抽象状态/任务逻辑，真正落到自主系统里时，仍然需要一个能够显式承载 start/end/invariant/time/lookup/command 的执行层状态机语言。

### 作为目标形式主义还是中间表示

它更适合作为中间表示或后端执行表示，而不是通用目标形式主义。对航天机器人等强执行导向场景，它也可以直接作为目标载体。

### 对需求到模型生成的启发

从需求生成执行模型时，不能只生成“状态 + 迁移”；还要补齐：

1. 节点级前置 / 后置 / 不变式条件。
2. 外部状态查询接口。
3. 执行动作的参数化调用。
4. 运行时失败与终止结果的区分。

## 重要的相关工作

- `CLARAty` 功能层与 executive 接口：说明 `PLEXIL` 的直接落地位置。
- `CASPER` 与 `PICO`：说明它服务的是 planner-to-executive interchange，而不是 planner 替代品。
- 本文附录中的 `PLEXIL Plan Editor` 与 `Java PathFinder` 验证方向：说明其基础设施不仅是语法，还包括编辑与分析链路。

## 文献分类总结

- 这是一篇典型的 `📦` 类条目，重点价值不在提出新的自动机表达力，而在把执行层状态机骨架、XML 承载、planner 接口和验证入口统一到同一语言里。
- 它描述的核心客体是任务执行控制逻辑，因此记为 `🎛️`；应用语境落在航天自主系统与机器人任务执行，因此记为 `🌡️`。
- 对 `project_1` 来说，`PLEXIL` 特别适合作为“需求状态机 -> 执行状态机”之间的后端承载参考。

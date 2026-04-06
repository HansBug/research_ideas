# 通过 Reactive Designs 与 Isabelle/UTP 自动验证状态机 / Automating Verification of State Machines with Reactive Designs and Isabelle/UTP

## 基本信息

- 标题：Automating Verification of State Machines with Reactive Designs and Isabelle/UTP
- 中文标题：通过 Reactive Designs 与 Isabelle/UTP 自动验证状态机
- 作者：Simon Foster，James Baxter，Ana Cavalcanti，Alvaro Miyazawa，Jim Woodcock
- 发表：*Formal Aspects of Component Software*，pp. 137-155，2018
- DOI：`10.1007/978-3-030-02146-7_7`
- 链接：https://doi.org/10.1007/978-3-030-02146-7_7
- 形式主义：`RoboChart state machines / Reactive Designs / Isabelle/UTP`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：RoboChart 状态机的 theorem-proving 验证路线 / Isabelle 工具化语义
- 工具/实现获取方式：原文明确给出 `Isabelle/UTP` 机械化仓库入口 `https://github.com/isabelle-utp/utp-main/tree/master/robochart/untimed`，并把 `RoboTool` 作为前端建模工具。
- 标准/格式获取方式：承载方式是 `RoboChart` 状态机语法、Isabelle parser/record definitions、`UTP` reactive-design semantics；原文未给独立行业交换标准。

## 简报

这篇论文的关键价值，不是再讲一遍“状态机可以验证”，而是把 `RoboChart` 这类 UML-like 状态机真正压进 theorem proving 工作流。它把状态机的静态语法、well-formedness、动态语义、迭代归纳律和 deadlock-freedom contract 全部机械化到 `Isabelle/UTP` 中，使状态机验证不再停留在 paper semantics，而变成可自动运行的证明脚本链。

- 形式主义定位：面向 `RoboChart` / diagrammatic state machines 的 theorem-proving 验证方法，不是新的工业交换格式。
- 构造方式简述：先把状态机解析成 Isabelle record 与事件 datatype，再检查 well-formedness，生成 reactive-design 语义，最后用 `rdes-refine + sledgehammer` 自动 discharge proof obligations。
- 基础设施与场景简述：依托 `RoboTool`、`Isabelle/HOL`、`Isabelle/UTP`、`reactive designs`、`nitpick` 和 `sledgehammer`，服务机器人控制器与一般 reactive state-machine 的形式验证。

```text
RoboChart state machine -> Isabelle parser + static semantics -> reactive-design dynamic semantics -> refinement proof obligations -> automated theorem proving
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `RoboChart` 的 untimed state machine 子集。
2. `UTP` 的 stateful-failure reactive designs。
3. `Isabelle/HOL` 中的 state-machine meta-model、well-formedness constraints 与 proof tactics。
4. 反应式不变量与 deadlock-freedom contracts。
5. 面向每个 non-final state 的自动化 refinement obligations。

### 核心抽象

结合论文的静态语义生成过程，可把单个状态机保守整理为：

$$
M = (\mathrm{init}, F, N, T)
$$

上式中的符号逐项解释如下：

1. `\mathrm{init}` 是初始节点标识。
2. `F` 是 final nodes 集合。
3. `N` 是节点定义集合。
4. `T` 是 transition declarations 集合。
5. 这组元组对应论文生成的 `machine = (init, finals, states, transs)` record 骨架。

论文给出的关键动态语义是：

$$
\llbracket M \rrbracket_M = actv := init_M \fatsemi do_{N \in inters_M}\ actv = nname(N) \rightarrow M \models \llbracket N \rrbracket_N\ od
$$

上式中的符号逐项解释如下：

1. `actv` 是当前 active state 标识变量。
2. `init_M` 是机器 `M` 的初始节点。
3. `inters_M` 是所有 non-final nodes 的集合。
4. `M \models \llbracket N \rrbracket_N` 是当前节点 `N` 的节点级语义。
5. `\fatsemi` 是 reactive-program sequential composition。
6. `do ... od` 是论文在 reactive-design 域里定义的 guarded iteration。

单条 transition 的语义可直接整理为：

$$
M, N \models \llbracket t \rrbracket_T = r:[cond(t) \land trig(t) \fatsemi nexit(N) \fatsemi action(t)]^+ \fatsemi actv := tgt(t)
$$

上式中的符号逐项解释如下：

1. `cond(t)` 是 transition guard。
2. `trig(t)` 是 trigger event。
3. `nexit(N)` 是离开节点 `N` 时执行的 exit action。
4. `action(t)` 是 transition action。
5. `tgt(t)` 是目标节点标识。
6. `r:[\cdot]^+` 表示把 action frame-extension 到状态机变量空间后的 reactive action。

论文还把 deadlock freedom 固定成一个反应式 contract：

$$
dlockf = [true \vdash \exists e \bullet e \notin ref \mid true]
$$

上式中的符号逐项解释如下：

1. `ref` 是 quiescent observation 下的 refusal set。
2. `\exists e \bullet e \notin ref` 表示至少有一个事件未被拒绝。
3. 该 contract 的直观意义是“系统在任意静止观察点都至少还有一个可走事件”。

### 一个最小例子与通俗解释

论文贯穿使用的 `GasAnalysis` 状态机很适合说明这条路线：

1. `InitState` 初始化 `gs`、`anl` 等变量后进入 `NoGas`。
2. `NoGas` 通过 `gas?` 事件转到 `Analysis`。
3. `Analysis` 根据分析结果，要么回到 `NoGas`，要么进入 `GasDetected`。
4. `GasDetected` 要么触发 `stop` 结束，要么触发 `turn!` 再进入 `Reading`。

通俗地说，这篇论文做的事，是把“图上的状态和箭头”改写成一段能进 Isabelle 的反应式程序，再让证明器去检查每个节点是否真的不会卡死。它不像传统 model checking 先枚举状态空间，而是把状态机变成可推理的语义对象。

### 运行 / 接受 / 转移语义

论文的工作流可压成以下验证链：

1. 解析并类型检查状态机定义。
2. 自动证明状态机满足 well-formedness。
3. 计算 denotational semantics。
4. 对每个 non-final state 生成 refinement proof obligations。
5. 用 `rdes-refine`、`rel-auto`、`sledgehammer` 自动化消解。

其关键归纳律可保守写成：

$$
S \sqsubseteq \llbracket M \rrbracket_M
$$

成立的前提是：

1. `M` 满足 well-formedness。
2. 初始节点建立不变量 `S`。
3. 每个 non-final node 在执行后保持 `S`。

### 语义边界

边界同样很清楚：

1. 本文聚焦 untimed subset，不是完整 `RoboChart`。
2. 主线是 theorem proving，不是显式状态模型检查。
3. 当前直接覆盖 sequentialised semantics；并发、层次、time、probability 仍留待扩展。
4. 自动化成功高度依赖 well-formedness、trigger productivity 和可化简的 proof obligations。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 状态机骨架 | `$M = (\mathrm{init}, F, N, T)$` | 论文把状态机先固定成可机械化的 record。 |
| 动态语义 | `$\llbracket M \rrbracket_M = actv := init_M \fatsemi do_{N \in inters_M}\ \cdots\ od$` | 状态机被顺序化成 reactive iteration。 |
| transition 语义 | `$M, N \models \llbracket t \rrbracket_T = r:[cond(t) \land trig(t) \fatsemi \cdots]^+ \fatsemi actv := tgt(t)$` | guard、trigger、action 与 target 都进入正式语义。 |
| deadlock contract | `$dlockf = [true \vdash \exists e \bullet e \notin ref \mid true]$` | 至少有一个未拒绝事件。 |
| 验证目标 | `$S \sqsubseteq \llbracket M \rrbracket_M$` | 用 contract refinement 证明状态机满足给定不变量。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 以 diagrammatic state machine 为核心对象。 |
| 事件 / 触发 | 很强 | trigger event 与 refusal set 都进入语义。 |
| 守卫 / 数据 | 强支持 | guards、entry/exit/action 与状态变量都被机械化。 |
| 层次 | 当前弱支持 | 论文未来工作才继续扩 hierarchy。 |
| 并发 / 同步 | 当前弱支持 | 当前语义采用 sequentialised semantics。 |
| 时间约束 | 当前不支持 | 本文聚焦 untimed subset。 |
| 连续动态 / 随机性 | 不支持 | 仅在 future work 中讨论 timed/probabilistic/hybrid 扩展。 |
| 可执行 / 可验证性 | 很强 | 直接落到 `Isabelle/UTP` 自动证明链。 |

### 形式化问题与性质

1. 论文真正补的是“状态机如何进入 theorem proving 工具链”，而不是另写一份自然语言语义。
2. `UTP` 的好处在于后续可沿同一语义母线继续扩 timed、probabilistic、hybrid state machines。
3. 这条路线特别适合 infinite-state 或 data-rich state machine，因为它不被显式状态枚举直接卡死。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 在 `RoboTool` 中建立状态机。
2. 序列化到 Isabelle parser 可消费的 machine syntax。
3. 自动生成 alphabet record、event datatype 与 `machine/semantics` definitions。
4. 在 `Isabelle/UTP` 中运行检查与验证 tactic。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 状态机语法声明：variables、events、states、transitions。
2. Isabelle record / datatype 定义。
3. reactive-design semantic terms。
4. 自动生成的 proof obligations。

### 交换与互操作

这条路线的互操作重点不是开放交换标准，而是：

1. `RoboTool` 前端与 Isabelle backend 的语义对齐。
2. `UTP` 理论层与具体 state-machine meta-model 的连接。
3. tactic-driven proof automation 与 graphical tool 的隐藏式集成。

## 配套基础设施

- 建模/编辑工具：`RoboTool`。
- 解析/交换/元模型支持：Isabelle parser、state-machine record、event datatype、well-formedness checker。
- 仿真/执行支持：论文重点不在 runtime execution，而在 denotational semantics 与证明。
- 验证/分析支持：`Isabelle/HOL`、`Isabelle/UTP`、`rdes-refine`、`rel-auto`、`nitpick`、`sledgehammer`。
- 代码生成/转换支持：主线是语义生成和 proof automation，不是部署代码生成。
- 标准化或社区生态：依托 `RoboChart`、`UTP` 与 `Isabelle` 社区生态；原文未给行业中立交换标准。

## 适用场景与需求前提

### 适用场景

适合机器人控制器、reactive component state machine、需要对 deadlock freedom 或更一般 reactive invariant 做高可信证明的场景。

### 需求前提

1. 状态机最好能收敛到论文支持的 untimed `RoboChart` 子集。
2. 模型需要满足清晰的 node / transition / trigger / action 结构。
3. 团队能接受 theorem proving 的 proof-obligation 心智模型。
4. 若要做自动化，well-formedness 与 contract 形式化要前置整理。

### 不适用或高成本场景

若目标只是快速跑有限状态 safety check，显式 model checking 通常更轻；若模型 heavily 依赖并发、层次、time 或 probability，而又不愿补语义收束，这条路线成本会迅速上升。

## 与相邻形式主义的关系

相对 [robochart-modelling-and-verification-of-robotic-applications/desc.md](../robochart-modelling-and-verification-of-robotic-applications/desc.md)，这篇更聚焦 theorem-proving 语义与自动证明，而不是整条 `RoboChart` DSL 的完整设计；相对 [formal-design-verification-and-implementation-of-robotic-controller-software-via-robochart-and-robotool/desc.md](../formal-design-verification-and-implementation-of-robotic-controller-software-via-robochart-and-robotool/desc.md)，它补的是 proof backend，而不是部署闭环；相对 [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)，它走 theorem proving 而不是 process-algebra model checking。

## 与本研究的关系

### 对 Project 1 的价值

它说明“需求到状态机”之后，如果目标状态机带数据甚至无限状态，仍然可以通过 theorem proving 继续做高可信验证，而不必局限在 model checking。

### 作为目标形式主义还是中间表示

更像 `RoboChart` / UML-like state machine 的验证路线，而不是新的交换格式。

### 对需求到模型生成的启发

1. 生成状态机时要尽量把 trigger、guard、entry/exit/action 分离清楚。
2. 若未来需要自动证明，well-formedness 约束应在生成阶段就显式化。
3. contract-style 性质模板适合直接成为“验证剖面”的一部分。

### 现实限制

这条路线很强，但不便宜；它擅长证明，而不擅长替代轻量建模或轻量测试。

## 重要的相关工作

1. [robochart-modelling-and-verification-of-robotic-applications/desc.md](../robochart-modelling-and-verification-of-robotic-applications/desc.md)：`RoboChart` DSL 与验证母线。
2. [formal-design-verification-and-implementation-of-robotic-controller-software-via-robochart-and-robotool/desc.md](../formal-design-verification-and-implementation-of-robotic-controller-software-via-robochart-and-robotool/desc.md)：`RoboTool` 的更完整工程闭环。
3. [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)：另一条 `UML/state machine -> formal backend` 路线。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 归类理由：论文主体虽然落在验证方法，但其核心工作是把 `RoboChart` 风格状态机语言的 meta-model、well-formedness 与 reactive semantics 机械化，并据此建立自动验证路线，因此更适合作为 `🔣/🛠️` 条目入账。

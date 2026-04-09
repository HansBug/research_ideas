# 使用 Modelica 执行 UML 状态机 / Execution of UML State Machines Using Modelica

## 基本信息

- 标题：Execution of UML State Machines Using Modelica
- 中文标题：使用 Modelica 执行 UML 状态机
- 作者：Wladimir Schamai，Uwe Pohlmann，Peter Fritzson，Christiaan J. J. Paredis，Philipp Helle，Carsten Strobel
- 发表：*3rd International Workshop on Equation-Based Object-Oriented Modeling Languages and Tools*，pp. 1-10，2010
- DOI：原文未给出
- 链接：https://ep.liu.se/en/conference-article.aspx?Article_No=1&issue=47&series=ecp
- 形式主义：`ModelicaML / executable UML behavior state machines`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：`ModelicaML` 中 `UML` 状态机执行语义与代码生成路线
- 工具/实现获取方式：原文明确说明 `ModelicaML` 的建模与代码生成工具可从项目页面下载，并以 `Modelica` 代码生成与仿真器执行为主要实现路径。
- 标准/格式获取方式：核心承载是 `ModelicaML` 这个 `UML` profile、生成的 `Modelica` algorithm sections，以及 `IsInState()`、`AFTER()` 这类 profile 级宏；原文未给独立交换标准。

## 简报

这篇论文的核心不是重新提出一种新状态机，而是解决 `UML behavior state machine` 在 `ModelicaML` 中怎样被稳定执行。作者把 `UML` 图形状态机嵌入 `ModelicaML`，再把每个状态机翻译成 `Modelica` 的 algorithm section，使同一模型既能表达事件驱动控制逻辑，也能与连续时间物理方程联仿。

- 形式主义定位：围绕 `ModelicaML` 的 `UML` 状态机执行方法，而不是新的独立状态机家族。
- 构造方式简述：`UML behavior state machine -> ModelicaML profile -> generated Modelica algorithm sections`。
- 基础设施与场景简述：依托 `ModelicaML` profile、代码生成器、`Modelica` 仿真器和 profile 宏，服务软硬件一体化、连续时间与离散事件混合建模。

```text
UML 行为状态机 -> ModelicaML profile -> Modelica algorithm sections -> 连续时间联仿 / 事件驱动执行
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织执行链：

1. `UML behavior state machines`。
2. `ModelicaML` 中承载这些状态机的 `UML` profile。
3. 由代码生成器产生的 `Modelica` algorithm sections。
4. `Modelica` 的 event iteration 与 `pre(...)` 语义。
5. 用于把离散状态激活与连续方程挂接起来的 profile 宏。

### 核心抽象

结合论文对翻译与执行语义的描述，可把单个 `ModelicaML` 状态机保守整理为：

$$
\mathcal{M} = (Q, q_0, T, V, A, E)
$$

上式中的符号逐项解释如下：

1. `Q` 是状态集合。
2. `q_0 \in Q` 是初始状态。
3. `T` 是带 trigger、guard 和 effect 的迁移集合。
4. `V` 是类变量与连续时间变量集合。
5. `A` 是生成出来的 `Modelica` algorithm section 集合。
6. `E` 是 `Modelica` 的 event iteration 机制。

论文强调一个类可以带多个状态机，并行翻译为多个 algorithm sections，因此可进一步写成：

$$
Class(C) = \{SM_1,\ldots,SM_n\},\ \forall i \neq j,\ \mathrm{writes}(Alg_i) \cap \mathrm{writes}(Alg_j)=\emptyset
$$

上式中的符号逐项解释如下：

1. `Class(C)` 是某个 `ModelicaML` 类上的全部行为状态机。
2. `SM_i` 是第 `i` 个状态机。
3. `Alg_i` 是 `SM_i` 翻译得到的 algorithm section。
4. `\mathrm{writes}(\cdot)` 表示该 algorithm section 会写入的类变量集合。
5. 这条约束来自论文对“多状态机并行执行但不能写同一变量”的明确说明。

### 一个最小例子与通俗解释

论文第一个例子是一个三状态循环：

1. 初始时位于 `State_0`。
2. 当 `[t > 1 and x < 3]` 成立时，执行迁移效果 `x := 1`，进入 `State_1`。
3. 当 `t > 1.5 and x > 0` 时进入 `State_2`。
4. 当 `x > 1` 时回到 `State_0`。

通俗地说，这条路线像是“把 `UML` 状态图译成持续被 `Modelica` 仿真器求值的离散控制片段”。控制逻辑本身仍是状态和迁移，但它不再只在事件队列里孤立运行，而是被放进连续时间仿真环境里和物理模型一起演化。

### 运行 / 接受 / 转移语义

论文把每个状态机翻成一个 algorithm section，可保守写成：

$$
\mathrm{Gen}(SM_i) = Alg_i
$$

上式中的符号逐项解释如下：

1. `SM_i` 是某个 `ModelicaML` 状态机。
2. `Alg_i` 是对应生成的 `Modelica` algorithm section。
3. 论文明确选择 algorithm 而不是方程，以便保持 exit/entry/effect 的执行顺序。

事件迭代的核心判据可直接保守整理为：

$$
pre(v) \neq v \Rightarrow \text{re-evaluate until } pre(v)=v
$$

上式中的符号逐项解释如下：

1. `v` 是在 `pre(...)` 中被观察的离散变量。
2. `pre(v)` 是事件点左极限值。
3. 若事件点上变量变化还未稳定，`Modelica` 会继续 event iteration。
4. 这正是论文把 `UML` 反应和 `Modelica` 事件语义对齐的基础。

对状态转移本身，可保守写成：

$$
(q,\nu) \xrightarrow{\tau} (q',\nu') \iff enabled(\tau,\nu)
$$

其中：

1. `q` 与 `q'` 是迁移前后的活动状态。
2. `\nu` 与 `\nu'` 是相关类变量和事件状态。
3. `\tau` 是某条迁移。
4. `enabled(\tau,\nu)` 表示 trigger 与 guard 在当前求值点成立。
5. 论文进一步说明，当前反应产生的新事件只会在本次反应完成后再继续处理，因此仍保留 run-to-completion 的核心约束。

### 语义边界

这条路线的边界很明确：

1. 论文只处理 `UML behavior state machines`，不处理 protocol state machines。
2. 它依赖 `Modelica` 的 event iteration 与 synchronous data-flow 语义，而不是通用离散事件解释器。
3. 多个状态机并行时，不能同时写同一类变量。
4. 重点是软硬件一体化可执行建模，不是独立的模型检查理论。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
| --- | --- | --- |
| 状态机骨架 | `$\mathcal{M} = (Q, q_0, T, V, A, E)$` | 状态、迁移、变量、生成代码和事件迭代共同定义执行对象。 |
| 多状态机并行 | `$Class(C) = \{SM_1,\ldots,SM_n\}$` | 一个类上允许挂多个并行状态机。 |
| 写集互斥 | `$\mathrm{writes}(Alg_i) \cap \mathrm{writes}(Alg_j)=\emptyset$` | 多个 algorithm sections 不能竞争写同一变量。 |
| 代码生成 | `$\mathrm{Gen}(SM_i) = Alg_i$` | 状态机被落实为 `Modelica` algorithm section。 |
| 事件迭代 | `$pre(v) \neq v \Rightarrow \text{re-evaluate}$` | `Modelica` 用 event iteration 保证离散反应收敛。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
| --- | --- | --- |
| 状态 / 模式 | 强支持 | 直接承载 `UML behavior state machine`。 |
| 事件 / 触发 | 强支持 | trigger、guard 和 effect 都被保留。 |
| 守卫 / 数据 | 强支持 | 状态机可直接读取和更新 `Modelica` 变量。 |
| 层次 | 中等支持 | 继承 `UML` 层次状态机骨架，但论文重点在执行语义。 |
| 并发 / 同步 | 中等支持 | 同一类可有多个并行状态机，但写集要互斥。 |
| 时间约束 | 中等支持 | 不是显式 clocks，而是借助 `Modelica` 时间与 event iteration。 |
| 连续动态 / 随机性 | 强连续、无随机 | 可以与连续时间方程联仿，但不处理随机性。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 核心价值是可执行与联仿，而非独立验证后端。 |

### 形式化问题与性质

1. 论文真正要解决的是 `UML` 状态机在 `Modelica` 里如何有稳定、可解释的执行顺序。
2. 选择 algorithm sections 而不是 equation sections，是为了保留 inter-level transitions 与 entry/exit/effect 的顺序性。
3. `IsInState()` 这类宏使连续方程与离散状态激活可以直接挂接起来，这是 `ModelicaML` 路线的重要工程补点。

## 构造方式与承载格式

### 建模入口

典型建模入口包括：

1. 在 `ModelicaML` 中定义 `UML behavior state machine`。
2. 为状态和迁移填写 guards、effects 与 action code。
3. 用 `ModelicaML` 代码生成器产生 `Modelica` 代码。
4. 在 `Modelica` 工具链中进行联仿或执行。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `ModelicaML` 这个 `UML` profile。
2. 生成后的 `Modelica` algorithm sections。
3. `IsInState()`、`AFTER()` 等 profile 宏。
4. 与连续方程共同求值的 `Modelica` 类定义。

### 交换与互操作

这条路线的互操作重点在于：

1. 前端保留 `UML` 图形建模。
2. 后端直接落到 `Modelica`，而不是先转另一套离散执行器。
3. 离散控制与连续物理模型共享同一仿真语义环境。

## 配套基础设施

- 建模/编辑工具：`ModelicaML` 建模工具与 `UML/SysML` 编辑环境。
- 解析/交换/元模型支持：`ModelicaML` profile、本体元模型与代码生成器。
- 仿真/执行支持：`Modelica` 仿真器与算法节执行语义。
- 验证/分析支持：原文重点在可执行语义澄清，不主打独立 model checking。
- 代码生成/转换支持：`UML` 状态机到 `Modelica` algorithm sections 的专门生成路线。
- 标准化或社区生态：依托 `UML`、`SysML` 与 `Modelica` 三者的交叉生态。

## 适用场景与需求前提

### 适用场景

适合同时含有连续物理动态和离散控制逻辑的系统建模，例如机电系统、嵌入式控制软件与软硬件联合仿真。

### 需求前提

1. 行为逻辑已经适合表达为 `UML` 状态机。
2. 系统还需要与连续时间物理模型联仿。
3. 团队接受 `Modelica` 作为 action language 与执行后端。
4. 多状态机并行时，行为切分能满足变量写集互斥。

### 不适用或高成本场景

如果系统只需要纯离散 GUI 状态机执行，或者必须依赖独立交换标准而非 `Modelica` 工具链，这条路线会偏重。

## 与相邻形式主义的关系

相对 [state-machines-in-modelica/desc.md](../state-machines-in-modelica/desc.md)，本文还不是把状态机提升为 `Modelica` 语言核心，而是在 `ModelicaML` 这个 `UML` profile 中解决执行语义；相对 [stategraph-a-modelica-library-for-hierarchical-state-machines/desc.md](../stategraph-a-modelica-library-for-hierarchical-state-machines/desc.md)，它强调的是 `UML` 状态机如何翻入 `Modelica`，而不是原生 `Modelica` 状态图库；相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，它更强调连续时间联仿而不是嵌入式解释执行。

## 与本研究的关系

### 对 Project 1 的价值

这篇条目直接说明：若未来 `project_1` 要把需求生成出的状态机落到 CPS 工程栈，`ModelicaML` 是一条能把 `UML` 状态机与物理模型放进同一执行语义里的后端路径。

### 作为目标形式主义还是中间表示

它更像面向 `Modelica` 生态的目标落地方法，而不是新的通用中间表示。

### 对需求到模型生成的启发

1. 若需求同时涉及模式切换和连续物理量，生成时就要考虑离散控制与连续变量的耦合点。
2. 多状态机并行切分时，写集冲突是必须显式规避的结构约束。
3. 自动生成状态机时，迁移触发、守卫和 action language 不应被混成一团自然语言描述。

### 现实限制

这条路线对 `Modelica` 工具链依赖很强，且验证能力更多来自后续生态，而不是本文自身。

## 重要的相关工作

1. [stategraph-a-modelica-library-for-hierarchical-state-machines/desc.md](../stategraph-a-modelica-library-for-hierarchical-state-machines/desc.md)：较早的 `Modelica` 状态图库路线。
2. [a-new-formalism-for-modeling-of-reactive-and-hybrid-systems/desc.md](../a-new-formalism-for-modeling-of-reactive-and-hybrid-systems/desc.md)：`Modelica_StateGraph2` 的安全层次并行扩展。
3. [state-machines-in-modelica/desc.md](../state-machines-in-modelica/desc.md)：把状态机进一步提升到 `Modelica` 语言级的后续代表条目。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 归类理由：论文主体集中在 `ModelicaML` 中 `UML` 状态机的执行与翻译问题，属于围绕领域语言执行语义展开的方法型条目。

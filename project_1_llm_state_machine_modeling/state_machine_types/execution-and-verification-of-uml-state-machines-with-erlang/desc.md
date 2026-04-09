# 用 Erlang 执行与验证 UML 状态机 / Execution and Verification of UML State Machines with Erlang

## 基本信息

- 标题：Execution and Verification of UML State Machines with Erlang
- 中文标题：用 Erlang 执行与验证 UML 状态机
- 作者：Ricardo J. Rodríguez，Lars-Åke Fredlund，Ángel Herranz，Julio Mariño
- 发表：*Software Engineering and Formal Methods*，pp. 284-289，2014
- DOI：`10.1007/978-3-319-10431-7_22`
- 链接：https://doi.org/10.1007/978-3-319-10431-7_22
- 形式主义：`UML State Machine / UMerL / Erlang`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：把 `UML State Machine` 的执行语义压到 `Erlang` 解释器，并接上 `QuickCheck + McErlang` 的执行/验证工作流
- 工具/实现获取方式：原文明确说明 `UMerL` 带源码公开，并给出入口 `https://bitbucket.org/fredlund1/umerl`；验证后端依赖 `McErlang` 与 `Quviq QuickCheck`。
- 标准/格式获取方式：输入承载是 `UML` class diagram、state-machine diagrams 与 object diagram；系统描述通过嵌入 `Erlang` 的 DSL 编写，执行对象直接映射到 `Erlang` 进程。

## 简报

这篇论文的价值，不在于提出新的 UML 子语言，而在于把一组可执行的 `UML State Machine` 语义真正落到一个能跑、能测、也能检验的后端。`UMerL` 把对象、消息、mailbox、entry/exit/do activities 和 deferral 规则解释成 `Erlang` 并发进程上的运行机制，再把同一执行模型交给 `QuickCheck` 生成环境消息序列，或者交给 `McErlang` 做 `LTL` 模型检查。

- 形式主义定位：`UML State Machine` 的执行与验证基础设施，不是新的 UML profile。
- 构造方式简述：以 `class diagram + state-machine diagrams + object diagram` 为前端，再用嵌入 `Erlang` 的 DSL 编写系统与环境，最后由 `UMerL` 解释执行。
- 基础设施与场景简述：依托 `Erlang` 并发、对象级进程、每状态机 mailbox、`QuickCheck` 随机环境与 `McErlang` 反例生成，服务嵌入式/事件驱动软件的设计期验证。

```text
UML 类图 + 状态机图 + 对象图 -> Erlang DSL / UMerL -> 可执行对象进程 + mailbox 语义 -> QuickCheck / McErlang -> trace / counterexample / LTL verification
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `UML` class diagram、state-machine diagrams 与 object diagram。
2. 每个对象对应一个 `Erlang` 进程。
3. 对象内多个状态机实例共享对象数据，但概念上各有自己的 mailbox。
4. `entry / exit / do` activities、trigger、guard、deferral 与 message ordering。
5. `QuickCheck` 生成的环境消息序列与 `McErlang` 上的 `LTL` 属性验证。

### 核心抽象

结合论文对执行器结构的描述，可把单个对象的运行配置保守整理为：

$$
\Sigma_o = (d_o,\{(c_i,Q_i)\}_{i \in SM(o)})
$$

上式中的符号逐项解释如下：

1. `o` 是某个 UML 对象。
2. `d_o` 是对象的私有数据存储，对应类属性值。
3. `SM(o)` 是附着在对象 `o` 上的状态机实例集合。
4. `c_i` 是第 `i` 个状态机当前的控制状态。
5. `Q_i` 是第 `i` 个状态机概念上的有序 mailbox。
6. 这是依据论文“每个对象映射为一个 Erlang 进程、每个状态机概念上有自己的 mailbox”做的保守整理，不是原文显式统一元组。

`UMerL` 的对象级映射也可压成：

$$
\mu : o \mapsto p_o
$$

上式中的符号逐项解释如下：

1. `o` 是 UML 对象。
2. `p_o` 是执行该对象所有状态机的 `Erlang` 进程。
3. 论文明确说明“each object to a single Erlang process”，而不是“一台状态机一个进程”。

一条迁移被执行的基本条件，可保守整理为：

$$
\mathrm{enabled}(t,m,\Sigma_o) \iff m \in Q_i \land \mathrm{oldestEligible}(m,Q_i) \land \mathrm{trigger}_t(m) \land \mathrm{guard}_t(d_o,m)
$$

上式中的符号逐项解释如下：

1. `t` 是某个状态机迁移。
2. `m` 是 mailbox 中的消息。
3. `Q_i` 是当前状态机的 mailbox。
4. `\mathrm{oldestEligible}(m,Q_i)` 表示 `m` 是最老的可执行消息，这对应论文强调的 oldest eligible message 规则。
5. `\mathrm{trigger}_t(m)` 表示消息匹配迁移触发器。
6. `\mathrm{guard}_t(d_o,m)` 表示在对象数据和消息内容上守卫成立。

迁移执行可进一步写成：

$$
(d_o,c_i,Q_i) \xrightarrow{t,m} (d'_o,c'_i,Q'_i)
$$

上式中的符号逐项解释如下：

1. `(d_o,c_i,Q_i)` 是执行前的局部对象状态。
2. `m` 是被消费的最老可执行消息。
3. `d'_o` 是执行 activity 后更新的数据存储。
4. `c'_i` 是目标控制状态。
5. `Q'_i` 是消费消息并处理 deferral/discard 语义后的 mailbox。
6. 论文把执行过程明确分成三步：处理消息、执行 activity、进入目标状态。

### 一个最小例子与通俗解释

论文的最小工程例子是列车车门系统：

1. `Door` 类有 `ClosedAndDisabled / Enabled / Opening / Opened / Closing` 等状态。
2. `TCMS` 类负责接收 `enableDoors / disableDoors / stopTrain` 等消息，并向各门广播使能/关闭命令。
3. 门对象收到 `buttonPressed` 后开门；`disableDoors` 后进入关闭流程；`TCMS` 在禁门后等待 `5` 秒再允许列车进入 `MovingTrain`。
4. 验证性质是“列车移动时门不能打开”。

通俗地说，`UMerL` 做的事像是把 UML 状态机背后那套“对象收消息、排队、挑可执行迁移、执行动作、丢弃或延迟消息”的隐式运行机制，全都翻成真正的并发程序语义。这样同一份状态机既能直接跑，又能拿去做模型检查。

### 运行 / 接受 / 转移语义

论文的执行语义重点有四个：

1. 每个对象一个 `Erlang` 进程，多个状态机共享对象数据。
2. 消息会被广播给对象内每个状态机，但每台状态机概念上维护自己的有序 mailbox。
3. 迁移采用 linearizable/atomic 风格执行，一次执行先消费最老可执行消息，再做 activity，再进入目标状态。
4. `do` activity 由独立 `Erlang` 进程承载，离开状态时会终止；`entry/exit` 被编织进进入/离开该状态的迁移动作。

关于 `do` activity，论文语义可以保守压成：

$$
\mathrm{do}(s) \mapsto p_s,\qquad \mathrm{leave}(s) \Rightarrow \mathrm{kill}(p_s)
$$

上式中的符号逐项解释如下：

1. `s` 是某个 UML 状态。
2. `p_s` 是执行该状态 `do` activity 的独立 `Erlang` 进程。
3. `\mathrm{leave}(s)` 表示有迁移离开状态 `s`。
4. 离开状态时，`do` activity 进程被终止。

### 语义边界

边界同样很明确：

1. 论文只覆盖 `UML` 的一部分图元，主要是 class diagram、state-machine diagram 和 object diagram。
2. 它重点处理异步消息、guard、entry/exit/do、deferral 和对象级并发，不追求完整 UML 规范覆盖。
3. 语义选择带有工程取舍，尤其是 message deferral 上提供 eager / lazy 两种解释。
4. 这是解释执行与模型检查路线，不是代码生成到最终生产系统。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 对象执行配置 | `$\Sigma_o = (d_o,\{(c_i,Q_i)\}_{i \in SM(o)})$` | 一个对象的核心运行状态是私有数据、各状态机控制点和各自 mailbox。 |
| 对象到进程映射 | `$\mu : o \mapsto p_o$` | 每个 UML 对象映射到一个 `Erlang` 进程。 |
| 可执行条件 | `$\mathrm{enabled}(t,m,\Sigma_o) \iff m \in Q_i \land \mathrm{oldestEligible}(m,Q_i) \land \mathrm{trigger}_t(m) \land \mathrm{guard}_t(d_o,m)$` | 执行优先级不只看触发匹配，还看 guard 和 oldest eligible message 规则。 |
| 局部执行步 | `$(d_o,c_i,Q_i) \xrightarrow{t,m} (d'_o,c'_i,Q'_i)$` | 一次迁移同时改变数据、控制状态和 mailbox。 |
| `do` activity 生命周期 | `$\mathrm{do}(s) \mapsto p_s,\ \mathrm{leave}(s) \Rightarrow \mathrm{kill}(p_s)$` | `do` activity 在实现上是真正的并发进程。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 主体就是对象内 UML 状态机。 |
| 事件 / 触发 | 很强 | 基于消息触发，消息顺序与 eligibility 是语义重点。 |
| 守卫 / 数据 | 强支持 | guard 基于消息内容和对象私有数据。 |
| 层次 | 弱到中等 | 本文主线不在复杂层次状态语义。 |
| 并发 / 同步 | 很强 | `Erlang` 对象进程、对象内多状态机与异步消息是核心。 |
| 时间约束 | 弱支持 | 案例里有 `5` 秒等待，但论文主线不是 timed UML。 |
| 连续动态 / 随机性 | 不支持 | 不在本文范围。 |
| 可执行 / 可验证性 | 很强 | 同一模型既可执行，也可用 `McErlang` 做 `LTL` 检查。 |

### 形式化问题与性质

1. 论文解决的是“如何给 UML 状态机一个能直接在并发运行时上执行的解释语义”。
2. oldest eligible message、deferral 和 mailbox ordering 是它比很多 UML-to-backend 翻译更工程化的地方。
3. `QuickCheck` 与 `McErlang` 的组合让同一模型兼具随机测试和模型检查入口。

## 构造方式与承载格式

### 建模入口

论文中的典型建模入口是：

1. `UML` class diagram 描述对象属性。
2. `UML` state-machine diagrams 描述对象行为。
3. `UML` object diagram 给出系统实例结构。
4. 使用嵌入 `Erlang` 的 DSL 写出系统与环境。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Erlang` 中的嵌入式系统描述 DSL。
2. 对象级 `Erlang` 进程和内部状态机 mailbox 表示。
3. `QuickCheck` 环境消息序列生成。
4. `McErlang` 消费的系统执行状态和 `LTL` 性质。

### 交换与互操作

这篇论文的互操作重点在于：

1. `UML` 前端模型到 `Erlang` 执行语义的桥接。
2. `UMerL` 到 `QuickCheck` 的随机环境生成接口。
3. `UMerL` 到 `McErlang` 的 `LTL` 验证接口。

## 配套基础设施

- 建模/编辑工具：原文默认输入来自 UML 图和 `Erlang` DSL，未强调特定图形编辑器。
- 解析/交换/元模型支持：核心不是 `XMI` 交换，而是把 UML 构件解释到对象进程和 mailbox 语义。
- 仿真/执行支持：`UMerL` 本体就是执行器。
- 验证/分析支持：`McErlang` 支持 `LTL` 模型检查，`QuickCheck` 支持随机生成 sensible message sequences。
- 代码生成/转换支持：更像解释执行，不是静态代码生成框架。
- 标准化或社区生态：依托 `Erlang` 并发生态和 `McErlang/QuickCheck` 工具链；`UMerL` 自身是研究型执行/验证基础设施。

## 适用场景与需求前提

### 适用场景

适合已经以对象化 `UML State Machine` 描述事件驱动软件，并且希望在不先抛弃 UML 前端的前提下，直接做执行、trace 观察和安全性质验证的场景，尤其是嵌入式控制、消息驱动软件和中等规模异步系统。

### 需求前提

1. 行为逻辑能落到论文支持的 UML 子集。
2. 系统是对象化、消息驱动的，而不是连续物理主导。
3. 团队能接受显式选择 deferral 语义和消息处理规则。
4. 目标性质适合写成 `LTL` 或用 trace 反例解释。

### 不适用或高成本场景

如果模型高度依赖完整 UML 全语法、复杂层次状态语义或精细的物理时间/连续动态，这条 Erlang 解释路线就不够自然。

## 与相邻形式主义的关系

相对 [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)，`UMerL` 不是把 UML 翻到进程代数后端，而是直接在 `Erlang` 上给出执行语义；相对 [a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md](../a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md)，它覆盖的 UML 面更窄，但更强调“能运行、能测、能检验”的工具闭环；相对 [embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md](../embedded-uml-model-execution-to-bridge-the-gap-between-design-and-runtime/desc.md)，它更偏对象消息与并发语义，而不是嵌入式解释器部署。

## 与本研究的关系

### 对 Project 1 的价值

它说明 `UML State Machine` 若要成为 LLM 输出后的可验证目标，不一定非要先翻成另一门纯形式语言；也可以先把 mailbox、dispatch 和 deferral 明确化，再直接落到可分析的执行语义上。

### 作为目标形式主义还是中间表示

更像验证/执行基础设施，而不是新的目标形式主义。

### 对需求到模型生成的启发

1. 若需求中存在对象、消息和队列，就必须把消息处理顺序写清楚，不能只画状态图。
2. `entry / exit / do` 的运行语义如果不明确，后续验证很容易失真。
3. 生成阶段最好同时产出环境消息模型，否则验证工作流会卡在“外部刺激如何进入系统”。

### 现实限制

这条路线能很好支撑执行和 `LTL` 检验，但不等于完整 UML 形式化，也不直接处理更复杂的 timed / hybrid 约束。

## 重要的相关工作

1. [towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md](../towards-model-checking-executable-uml-specifications-in-mcrl2/desc.md)：另一条 executable UML 到 formal backend 的桥接路线。
2. [a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md](../a-formal-semantics-for-the-complete-syntax-of-uml-state-machines-with-communications/desc.md)：更强调完整 UML 语义覆盖的直接形式化路线。
3. [formalizing-uml-state-machines-survey/survey.md](../formalizing-uml-state-machines-survey/survey.md)：UML 状态机形式化和工具链的综述总览。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`UML State Machine / UMerL / Erlang`
- 归类理由：主贡献是把 `UML State Machine` 接到 `Erlang` 执行、`QuickCheck` 测试和 `McErlang` 验证的基础设施闭环，而不是提出新的状态机本体。

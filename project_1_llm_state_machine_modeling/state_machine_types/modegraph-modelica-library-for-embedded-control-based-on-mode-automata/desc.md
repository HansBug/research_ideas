# ModeGraph：基于 Mode-Automata 的 Modelica 嵌入式控制库 / ModeGraph - A Modelica Library for Embedded Control Based on Mode-Automata

## 基本信息

- 标题：ModeGraph - A Modelica Library for Embedded Control Based on Mode-Automata
- 中文标题：ModeGraph：基于 Mode-Automata 的 Modelica 嵌入式控制库
- 作者：Martin Malmheden, Hilding Elmqvist, Sven Erik Mattsson, Dan Henriksson, Martin Otter
- 发表：Proceedings of the 6th International Modelica Conference, 255-267, 2008
- DOI：原文未提供
- 链接：https://elib.dlr.de/55894/
- 形式主义：ModeGraph / Mode-Automata-based Modelica Library
- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 论文角色：工具/库
- 工具/实现获取方式：论文描述了 `ModeGraph` 作为新的 Modelica library，并依赖 Modelica 语言扩展；原文未给出独立仓库下载入口。
- 标准/格式获取方式：核心承载是 Modelica library 组件、图形化 annotations 和论文提出的 `mode` 语义扩展。

## 简报

`ModeGraph` 的重点不只是又做了一套图形状态机库，而是把 `Mode-Automata` 语义塞进 Modelica 的条件执行机制里，强制同层 mode 互斥、保证 single-assignment、显式区分 delayed transition，并把 suspend/resume/history/parallel 都做成可执行库组件。它是“专门给嵌入式/混合控制系统落地的安全状态机载体”。

- 形式主义定位：面向嵌入式与混合控制的安全层次状态机执行库。
- 构造方式简述：以 `Step / Transition / Composite / Parallel` 为基本块，用 Modelica 方程和 `mode` 语义描述激活、暂停、复位与并行。
- 基础设施与场景简述：基于 Modelica，继承 `StateGraph`，但用 `Mode-Automata` 互斥与条件执行语义解决不安全连接和非确定赋值问题。

```text
嵌入式控制模式需求 -> Step/Transition/Composite 图 -> Modelica mode equations -> 安全执行 / 代码生成 / 混合控制集成
```

## 形式主义定义与核心对象

### 定义对象

论文面向的是 hybrid and embedded control systems。它想解决的不是抽象自动机判定边界，而是“控制逻辑怎样以安全、可执行、可与 Modelica 连续模型共存的状态机形式落地”。

### 核心抽象

原文没有把 `ModeGraph` 压成单一数学元组，而是通过组件和布尔方程给出语义。为了便于后续比较，这里按论文结构做一个**保守整理**：

$$
MG = (Q, q_0, \Delta, \Gamma, \mathcal{M})
$$

上式中的符号逐项解释如下：

1. `Q` 是 mode 节点集合，包含 `Step`、`Composite` 以及 `Parallel` 内部 mode。
2. `q_0` 是通过 entry port 或初始 step 确定的初始 mode。
3. `\Delta` 是 transition 集合，包括 immediate 与 delayed 两类。
4. `\Gamma` 是 transition condition 与优先级规则。
5. `\mathcal{M}` 是 ModeGraph 依赖的 Modelica `mode` 修饰语义，包括 `enable`、`enableSubBlocks`、`resetStates`、`resetOutputs` 等。

基本 `Step` 的状态由布尔量表示，论文直接给出：

$$
\mathrm{newActive} = (\mathrm{pre}(\mathrm{newActive}) \land \neg \mathrm{anyTrue}(\mathrm{outPort.fire})) \lor \mathrm{anyTrue}(\mathrm{inPort.fire})
$$

$$
\mathrm{active} = \mathrm{pre}(\mathrm{newActive})
$$

基本 transition 的 firing 条件则写成：

$$
\mathrm{inPort.fire} = \mathrm{condition} \land \mathrm{inPort.available}, \qquad
\mathrm{outPort.fire} = \mathrm{inPort.fire}
$$

### 一个最小例子与通俗解释

最小例子就是论文开头那种“两状态 + 两转移”图：

1. 系统初始在 `A`。
2. 条件 `\alpha` 为真时，从 `A` 迁移到 `B`。
3. 另一条件满足时，再从 `B` 回到 `A`。

在 `ModeGraph` 里，这不是单纯的图，而是一组 Modelica 组件：

1. `Step` 记录当前 mode 是否 active。
2. `Transition` 根据 `condition` 和前驱 `Step.available` 判断是否 fire。
3. fire 信号会让前驱 step 失活、后继 step 激活。

通俗解释是：`ModeGraph` 像把状态机电路化。每个状态和迁移都变成一个会发布尔信号的 Modelica 模块，状态切换靠方程而不是解释器黑盒完成。

### 运行 / 接受 / 转移语义

`ModeGraph` 的一个关键设计是 delayed transition，用来打断不稳定循环。论文给出的语义是：

$$
\mathrm{enableFire} = \mathrm{condition} \land \mathrm{inPort.available}
$$

$$
\mathrm{fire} = \mathrm{enableFire} \land time \ge t_{start} + waitTime
$$

其中 `t_{start}` 在 `enableFire` 首次为真时记录。这样，一个全为真条件的环若没有 delayed transition，就会形成布尔代数环并被翻译器拒绝。

对于 `Composite`，论文给出的可离开与激活条件是：

$$
\mathrm{available} = \mathrm{exit.available} \land \mathrm{allSubBlocksFinished} \land \mathrm{active}
$$

$$
\mathrm{newActive} = (\mathrm{active} \land \neg \mathrm{anyTrue}(\mathrm{outPort.fire}) \land \neg \mathrm{anyTrue}(\mathrm{suspend.fire})) \lor \mathrm{anyTrue}(\mathrm{inPort.fire}) \lor \mathrm{anyTrue}(\mathrm{resume.fire})
$$

这些公式中的符号逐项解释如下：

1. `\mathrm{pre}(\cdot)` 是 Modelica 中上一离散时刻的值。
2. `\mathrm{anyTrue}` 表示端口数组里是否至少有一个 firing 信号为真。
3. `waitTime` 是 delayed transition 的等待时间。
4. `\mathrm{suspend.fire}` 与 `\mathrm{resume.fire}` 分别对应 preemption 和 history-style re-entry。
5. `\mathrm{allSubBlocksFinished}` 是所有子块完成条件。

### 语义边界

这套语义刻意偏向安全和可实现，因此它有很强的约束：

1. 同层 `mode` 必须互斥。
2. 每个循环至少含一个 delayed transition。
3. 并行支路不能随意跨层乱连。
4. 条件执行与单赋值规则优先于“图画起来多灵活”。

因此它不是最自由的状态图库，而是显式牺牲一部分灵活性来换可编译安全。

### 关键性质与判定边界

论文最强调的性质不是经典 automata 的语言判定，而是执行安全性。核心性质可压缩为：

$$
\forall q, q' \in Q,\ q \neq q' \Rightarrow \neg(\mathrm{enable}(q) \land \mathrm{enable}(q'))
$$

这表示同层 mode 互斥，从而保证不会对同一变量发生平行冲突赋值。

论文还提出 Modelica `mode` 基类：

$$
\mathrm{mode} = (\mathrm{enable}, \mathrm{enableSubBlocks}, \mathrm{resetStates}, \mathrm{resetOutputs}, \mathrm{finished})
$$

并用翻译器把多分支赋值合并成单赋值形式，例如：

$$
y =
\begin{cases}
\mathrm{expr}_1, & A.enable \lor A.enableSubBlocks \\
\mathrm{expr}_2, & B.enable \lor B.enableSubBlocks \\
\mathrm{pre}(y), & \text{otherwise}
\end{cases}
$$

这条式子的意义是：虽然用户在不同 mode 里分别写方程，但最终代码里每个变量只在一个地方被定义，因此 deterministic variable assignment 被静态保证。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `Step` / `Composite` 明确表示 mode。 |
| 事件 / 触发 | 支持 | transition condition 与 firing 信号驱动切换。 |
| 守卫 / 数据 | 强支持 | 直接用 Modelica 作为 action language 与条件表达语言。 |
| 层次 | 强支持 | `Composite` 支持 superstate / substate。 |
| 并发 / 同步 | 强支持 | `Parallel`、preemption、synchronization 都是核心卖点。 |
| 时间约束 | 部分支持 | delayed transition 提供离散等待时间，不是显式时钟自动机。 |
| 连续动态 / 随机性 | 部分支持 | 通过 Modelica 外围连续模型实现混合控制，但 mode 本体是离散的。 |
| 可执行 / 可验证性 | 强支持 | 目标就是安全执行、避免 algebraic loop 和非确定赋值。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| Step 激活 | `$\mathrm{active} = \mathrm{pre}(\mathrm{newActive})$` | 当前 mode 是否处于活动状态。 |
| 基本迁移 | `$\mathrm{inPort.fire} = \mathrm{condition} \land \mathrm{inPort.available}$` | 当前 transition 是否触发。 |
| 延迟迁移 | `$\mathrm{fire} = \mathrm{enableFire} \land time \ge t_{start} + waitTime$` | 用时间延迟打断不稳定环。 |
| Composite 离开条件 | `$\mathrm{available} = \mathrm{exit.available} \land \mathrm{allSubBlocksFinished} \land \mathrm{active}$` | 只有子系统完成时才能正常退出 superstate。 |
| 互斥 mode | `$\forall q \neq q',\ \neg(\mathrm{enable}(q)\land\mathrm{enable}(q'))$` | 保证 single-assignment 不被同层多模式破坏。 |
| 单赋值合并 | `$y = \mathrm{expr}_1 / \mathrm{expr}_2 / \mathrm{pre}(y)$` | 翻译器把多模式赋值合并成唯一方程。 |

## 构造方式与承载格式

### 建模入口

建模入口是图形化 Modelica library：用户拖 `Step`、`Transition`、`Composite`、`Parallel`，再在状态内部写 Modelica 动作和条件。

### 机器可处理承载方式

机器可处理承载方式不是 XML，而是：

1. Modelica 类和组件连接。
2. `mode` 基类及其五个语义变量。
3. 由翻译器生成的布尔方程和互斥赋值代码。

### 交换与互操作

互操作完全依赖 Modelica 工具链。论文没有定义独立交换标准，但其优势在于可直接和现有 Modelica 物理模型、控制块、代码生成链结合。

## 配套基础设施

- 建模/编辑工具：依赖 Modelica / Dymola 风格图形建模环境。
- 解析/交换/元模型支持：基于 Modelica 类、connections 与 annotations，不提供独立元模型标准。
- 仿真/执行支持：这是论文核心目标，强调可执行的安全状态机图。
- 验证/分析支持：通过翻译时发现布尔环与不安全连接，并依靠互斥 mode 保证赋值确定性。
- 代码生成/转换支持：论文明确希望减少 code overhead、改善 generated graph performance。
- 标准化或社区生态：依附 Modelica 生态，而不是独立标准。

## 适用场景与需求前提

### 适用场景

适合嵌入式控制器、混合控制、需要层次模式和并行子控制器的工业控制逻辑。

### 需求前提

1. 需求中存在明确模式切换。
2. 控制逻辑需要与 Modelica 连续系统模型协同。
3. 需要防止并行模式对同一变量的竞争赋值。
4. 希望用图形状态机表达 preemption / history / orthogonality。

### 不适用或高成本场景

若目标只是轻量级协议或简单流程，`ModeGraph` 会显得过重；若需要形式化可判定边界而不是工具语义，它也不如 `Timed Automata` 或经典自动机那样干净。

## 与相邻形式主义的关系

相对 `StateGraph`，它更安全、更强调条件执行与互斥 mode；相对 `Statecharts`，它保留层次、并行和 preemption，但把实现落到 Modelica 方程上；相对纯 `Mode-Automata`，它更像工程执行载体而非理论核心定义。

## 与本研究的关系

### 对 Project 1 的价值

它展示了“领域专用状态机形式主义如何贴着工业建模语言落地”。这对 `project_1` 非常重要，因为目标并不只是生成抽象状态机，还要考虑最终工件如何进入现有控制建模生态。

### 作为目标形式主义还是中间表示

若研究对象是 Modelica / CPS / 嵌入式控制工具链，它可以直接作为目标工件；否则更适合作为从需求结构化状态机走向可执行控制模型的桥梁。

### 对需求到模型生成的启发

当需求强调“模式互斥”“切换安全”“并行子控制器”和“复位/恢复语义”时，`ModeGraph` 的组件化骨架比单纯 `Statechart` 更容易映射到工程实现。

### 现实限制

它高度依赖 Modelica 语言和翻译器语义，因此可移植性和跨工具交换性不如 `SCXML` 之类标准载体。

## 重要的相关工作

### 奠基或前身工作

- `FSM`
- `Statecharts`
- `Mode-Automata`

### 同类型或同家族工作

- `StateGraph`
- `Safe State Machines (SSM)`
- `Sequential Function Charts (SFC)/Grafcet`

### 标准 / 格式 / 工具链工作

- Modelica 语言与工具链。

### 与本研究关系最紧的工作

- 面向控制系统的可执行状态机载体和安全语义收束路线。

## 文献分类总结

- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 形式主义：ModeGraph / Mode-Automata-based Modelica Library
- 论文角色：工具/库
- 核心功能：在 Modelica 中实现安全的层次、并行、可 preempt 的模式状态机。
- 关键特性：single-assignment 保证、delayed transition、suspend/resume、并行与 history。
- 构造方式：Modelica 组件库 + `mode` 语义扩展 + 布尔方程翻译。

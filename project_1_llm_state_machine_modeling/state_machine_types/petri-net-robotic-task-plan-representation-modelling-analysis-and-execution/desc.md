# Petri 网机器人任务规划表示：建模、分析与执行 / Petri Net Robotic Task Plan Representation: Modelling, Analysis and Execution

## 基本信息

- 标题：Petri Net Robotic Task Plan Representation: Modelling, Analysis and Execution
- 中文标题：Petri 网机器人任务规划表示：建模、分析与执行
- 作者：Hugo Costelha, Pedro Lima
- 发表：收录于 *Autonomous Agents*, pp. 65-89, InTech, 2010
- DOI：`10.5772/9659`
- 链接：https://doi.org/10.5772/9659
- 形式主义：`Petri Net Robotic Task Plan Representation / MOPN-GSPN Framework`
- 主类：🕸️
- 描述客体：🏭
- 所属领域：🌡️
- 论文角色：机器人任务规划表示 / `Petri Net` 建模分析执行框架
- 工具/实现获取方式：原文明确实现了 `Petri net Executor`，并使用 `TimeNET` 对完整任务网做瞬态分析；论文未给独立源码仓库。
- 标准/格式获取方式：承载方式是 `MOPN/GSPN`、predicate places、macro places、full-task net expansion 与执行器；原文未给统一交换标准。

## 简报

这篇论文想解决的不是“某个单独机器人动作怎么写”，而是“机器人任务计划、动作模型和环境模型怎样放进同一张网里，既能分析又能执行”。作者把任务层、动作层和环境层统一压成 `Petri Net` 体系：任务计划用 `MOPN` 表示顺序与协调，动作模型用 `GSPN` 表示成功/失败与持续时间，环境谓词也转成 `Petri` 子网，然后通过 expansion 算法把它们拼成一张 full task net 去做性能分析和在线执行。

- 形式主义定位：这是 `Petri Nets` 主干上的应用型条目，核心价值是把机器人 task planning、action execution 与 environment predicates 统一到一套可分析、可执行的网模型框架中。
- 构造方式简述：先建立环境层、动作执行层、动作协调层和组织层四类 `Petri` 模型，再通过 macro places 和 predicate places 逐层展开为单一 full-task net。
- 基础设施与场景简述：依托 `MOPN/GSPN`、`TimeNET`、自研执行器和机器人足球任务示例，服务单机器人/多机器人任务规划、动作成功率评估与在线协调执行。

```text
task plan + action model + environment predicates -> layered Petri net models -> full-task net expansion -> reachability / performance analysis + online execution
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 表达任务顺序的 task-plan Petri nets。
2. 表达动作效果和成功/失败分支的 action-model GSPNs。
3. 表达环境状态的 predicate places。
4. 用于层次组合的 macro places。
5. 把多层模型展开成单网的 full-task net generation algorithm。
6. 用于分析与执行的 `TimeNET` 和 `Petri net Executor`。

### 核心抽象

论文首先给出了最基础的 marked ordinary Petri net 定义：

$$
PN = \langle P, T, I, O, M_0 \rangle
$$

上式中的符号逐项解释如下：

1. `P` 是 place 集合。
2. `T` 是 transition 集合。
3. `I` 是 place 到 transition 的输入弧关系。
4. `O` 是 transition 到 place 的输出弧关系。
5. `M_0` 是初始 marking。
6. 在论文框架里，task plan 主要落在这一层的 `MOPN` 上。

为表达动作持续时间和随机成功/失败，论文又使用 standard `GSPN`：

$$
PN = \langle P, T, I, O, M_0, R, S \rangle
$$

以及带权 immediate transitions 的实现形式：

$$
PN = \langle P, T, I, O, M_0, R, W \rangle
$$

上式中的符号逐项解释如下：

1. 前五项 `P,T,I,O,M_0` 与 `MOPN` 一致。
2. `R` 为 exponential transitions 的 firing-rate 函数。
3. `S` 是随机开关集合，用来给冲突 immediate transitions 指定概率分布。
4. `W` 是论文实际采用的 immediate-transition weights，用于替代一般形式的随机开关。
5. 这样一来，动作模型既能表达持续时间，也能表达不同结果分支的概率。

论文进一步把谓词环境压成成对的 predicate places。对某个谓词 `p`，可整理为：

$$
M(p) + M(\neg p) = 1
$$

上式中的符号逐项解释如下：

1. `p` 与 `\neg p` 是一对互补 predicate places。
2. `M(\cdot)` 表示当前 marking 下该 place 的 token 数。
3. 等式表示任一时刻二者中恰有一个为真。
4. 这类 place invariant 是论文保证 predicate safety 的关键。

论文在动作模型定义里又明确要求：

$$
P = P_E \cup P_R
$$

上式中的符号逐项解释如下：

1. `P_E` 是 effects 相关的 predicate places。
2. `P_R` 是 running conditions 相关的 predicate places。
3. action model 只由谓词 places 组成，从而便于和环境层、任务层做统一合成。
4. 这一结构使动作成功/失败和环境条件更新都能被标准 `Petri Net` 规则接管。

### 一个最小例子与通俗解释

论文中最容易理解的例子是 `Score_Goal` 任务：

1. 任务计划网把 `Move2Ball -> CatchBall -> Dribble2Goal -> Kick2Goal` 等动作串起来。
2. 每个动作不是一个黑盒节点，而是一个独立的 action-model `GSPN`，里面写清了成功、失败、前提谓词和效果谓词。
3. 环境层用 predicate places 表示诸如 `HasBall`、`SeeBall` 这类真值状态。
4. expansion 算法把任务层、动作层和环境层合并成 full-task net，然后就能分析成功概率、死锁和执行路径。

通俗地说，这个框架像“把机器人任务计划图、动作脚本和环境条件库都变成可拼接的网模块”。普通状态机更擅长描述单条控制流，而 `Petri Net` 在这里的优势是可以自然表达并发、资源条件、动作成功/失败以及多机器人协同。

### 运行 / 接受 / 转移语义

论文里的运行语义主要有四层：

1. task-plan `MOPN` 决定当前允许执行哪些动作。
2. action-model `GSPN` 根据 running conditions 与 effects 执行动作并更新谓词。
3. environment-layer nets 维护球、机器人、通信等外部世界状态。
4. Executor 在当前 marking 上选择 enabled transitions 并推动整网演化。

对于带权 `GSPN`，论文直接使用如下 firing-probability 语义：

$$
P_f(t_i) = \frac{w_i}{W}
$$

上式中的符号逐项解释如下：

1. `P_f(t_i)` 是 immediate transition `t_i` 的触发概率。
2. `w_i` 是该 transition 的权重。
3. `W` 是当前 marking 下所有 enabled immediate transitions 权重之和。
4. 该公式用于描述动作成功/失败等竞争分支。
5. 因此 full-task net 既可做逻辑分析，也可做性能/概率分析。

full-task net 的生成可保守整理为：

$$
PN_{full} = \mathrm{Expand}(PN_{task}, \{PN_{act}\}, \{PN_{env}\})
$$

上式中的符号逐项解释如下：

1. `PN_{task}` 是任务计划网。
2. `\{PN_{act}\}` 是动作模型集合。
3. `\{PN_{env}\}` 是环境模型集合。
4. `\mathrm{Expand}` 表示论文第 4 节给出的展开算法。
5. 该算法通过 macro places 与标签匹配，把多层模型合并成单一分析网。

### 语义边界

这篇论文的边界主要在于：

1. 主体关注离散事件层的任务规划、动作成功/失败与环境谓词，不直接求解连续控制律。
2. 环境和动作效果需要先离散化成谓词与有限事件。
3. `GSPN` 的概率/时间参数依赖人工建模或实验估计。
4. 论文以机器人足球为主要示例，但框架本身更一般。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基础 `MOPN` 骨架 | `$PN = \langle P, T, I, O, M_0 \rangle$` | 任务计划层的最基础 `Petri Net` 表示。 |
| 标准 `GSPN` 骨架 | `$PN = \langle P, T, I, O, M_0, R, S \rangle$` | 为动作模型加入持续时间和随机分支。 |
| 带权 `GSPN` | `$PN = \langle P, T, I, O, M_0, R, W \rangle$` | 论文实际采用的 immediate transition 权重形式。 |
| 谓词不变式 | `$M(p) + M(\neg p) = 1$` | 保证互补谓词在任意 marking 下保持一致。 |
| 动作模型谓词结构 | `$P = P_E \cup P_R$` | action model 只由 effects 与 running-condition 谓词组成。 |
| 冲突转移概率 | `$P_f(t_i) = \frac{w_i}{W}$` | 描述动作分支或竞争 immediate transitions 的概率。 |
| 单网展开 | `$PN_{full} = \mathrm{Expand}(PN_{task}, \{PN_{act}\}, \{PN_{env}\})$` | 把任务、动作和环境三层合成一张可分析执行的网。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 明确给出任务与环境所处阶段。 |
| 事件 / 触发 | 强支持 | transition firing、动作成功/失败和通信事件都是核心。 |
| 守卫 / 数据 | 部分支持 | 主要靠 predicate places 表示条件，不是高维数据计算。 |
| 层次 | 强支持 | macro places 和四层结构提供明确层次建模。 |
| 并发 / 同步 | 强支持 | `Petri Net` 天然支持并发动作、资源共享与同步。 |
| 时间约束 | 部分支持 | `GSPN` 可表达持续时间，但非时钟自动机式精细 deadline。 |
| 连续动态 / 随机性 | 弱连续、部分随机 | 连续部分经离散化处理，随机性通过 `GSPN` 权重/速率表达。 |
| 可执行 / 可验证性 | 强支持 | 既能做 `TimeNET` 分析，也有在线 Executor。 |

### 形式化问题与性质

1. 论文补出的不是“Petri 网能不能建机器人”，而是“如何把任务、动作、环境三层稳定拼成一张既可分析又可执行的网”。
2. predicate places 让环境状态和任务状态共用同一套 token 语义。
3. `MOPN + GSPN + expansion + executor` 的组合，使它比单纯任务图更接近工程可落地框架。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先定义环境谓词及其 predicate-place 对。
2. 为每个 primitive action 构建 `GSPN` 动作模型。
3. 用 action macro places 组织 task-plan `MOPN`。
4. 通过 expansion algorithm 合成 full-task net。
5. 用 `TimeNET` 或执行器对 full-task net 做分析和运行。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `MOPN` 与 `GSPN` 网结构。
2. predicate places、macro places 与 action models。
3. full-task net generation algorithm。
4. `TimeNET` 分析输入与 `Petri net Executor` 运行时。

### 交换与互操作

互操作重点在：

1. task-plan places 如何绑定到对应 action models。
2. action-model effects 如何回写 predicate places。
3. 多机器人通信动作如何在合成网中同步展开。

## 配套基础设施

- 建模/编辑工具：原文基于 layered `Petri Net` 框架和自研执行器。
- 解析/交换/元模型支持：有标准 `Petri Net` 结构和自定义 predicate/macro-place 约定，但无统一交换标准。
- 仿真/执行支持：提供 `Petri net Executor` 在线执行 full-task net。
- 验证/分析支持：使用 `TimeNET` 做 transient analysis，并检查 boundedness / place invariants。
- 代码生成/转换支持：有从分层模型生成 full-task net 的 expansion algorithm。
- 标准化或社区生态：依托 `Petri Nets`、`GSPN` 和性能分析工具生态。

## 适用场景与需求前提

### 适用场景

适合多机器人任务协调、机器人足球、动作成功率分析、任务计划执行器和需要统一处理任务层/动作层/环境层的离散事件机器人系统。

### 需求前提

1. 任务可拆成有限个动作与条件谓词。
2. 环境状态能离散化成 predicate places。
3. 动作成功/失败、耗时或概率可被结构化建模。
4. 系统核心难点在并发、资源条件、通信和任务协调，而不是底层连续控制。

### 不适用或高成本场景

如果系统主要依赖高维连续动力学、复杂优化控制或无法离散化的环境状态，仅靠本文这套 layered `Petri Net` 抽象会过于粗糙。

## 与相邻形式主义的关系

相对 [Petri Nets: Properties, Analysis and Applications](../petri-nets-properties-analysis-and-applications/desc.md)，本文不是 `Petri Net` 本体教程，而是一个明确面向机器人任务规划的分层应用框架；相对 [Execution Control of Robotic Tasks: A Petri Net-Based Approach](../execution-control-of-robotic-tasks-a-petri-net-based-approach/desc.md)，本文更强调 task plan representation、action/environment model 合成和性能分析；相对 [Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)，这里更系统地把 predicate places、macro places 和 full-task net expansion 说清楚。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果需求里同时出现任务步骤、动作前提、环境状态和执行结果，`Petri Net` 是一种很自然的统一表示，它能把这些层一起变成可验证、可执行的结构。

### 作为目标形式主义还是中间表示

对任务规划和执行协调，它可以直接作为目标形式主义；对更一般的控制需求链路，它也很适合作为任务层和执行层之间的中间并发表示。

### 对需求到模型生成的启发

1. 自然语言需求中的“满足条件才能执行动作、动作成功后改变环境状态、失败后走另一条分支”非常适合自动翻成 predicate places 和 action models。
2. 若系统包含多层任务抽象，生成模型时应保留 macro-place 级分层，而不是一开始就完全扁平化。
3. 性质生成时可以自动补 place invariant、boundedness 和 success-probability 一类 `Petri` 友好型指标。

## 重要的相关工作

- [Petri Nets: Properties, Analysis and Applications](../petri-nets-properties-analysis-and-applications/desc.md)：提供本文所依赖的 `Petri Net` 基础语义。
- [Execution Control of Robotic Tasks: A Petri Net-Based Approach](../execution-control-of-robotic-tasks-a-petri-net-based-approach/desc.md)：同样面向机器人任务执行，但更偏控制与重配置。
- [Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)：与本文最接近，同样展示多机器人任务/动作/环境三层的组合思路。
- [Task Planning and Formal Control of Robotic Assembly Systems: A Petri Net-Based Approach](../task-planning-and-formal-control-of-robotic-assembly-systems-a-petri-net-based-approach/desc.md)：展示 `Petri Net` 在机器人装配计划与监督控制上的另一条应用路线。

## 文献分类总结

- 这是一篇 `🕸️` 类应用型条目，核心价值是把机器人任务计划、动作模型和环境模型组织成可分析、可执行的 layered `Petri Net` 框架。
- 它描述的是并发任务、资源条件和动作流网络，因此记为 `🏭`；论文对象是带物理执行器的机器人任务系统，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它提供了一个非常强的信号：当需求里本来就有“动作前提、环境谓词、成功/失败分支、多机器人协调”时，`Petri Net` 族形式比普通单线程状态机更贴近问题本体。

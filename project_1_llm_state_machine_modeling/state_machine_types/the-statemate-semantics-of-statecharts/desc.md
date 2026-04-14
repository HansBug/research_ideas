# STATEMATE 状态图语义 / The STATEMATE Semantics of Statecharts

## 基本信息

- 标题：The STATEMATE Semantics of Statecharts
- 中文标题：STATEMATE 状态图语义
- 作者：David Harel, Amnon Naamad
- 发表：ACM Transactions on Software Engineering and Methodology, 5(4):293-333, 1996
- DOI：`10.1145/235321.235322`
- 链接：https://doi.org/10.1145/235321.235322
- 形式主义：STATEMATE Statecharts
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：工具语义
- 工具/实现获取方式：原文直接面向 `STATEMATE` 工具环境，明确说明该语义已经驱动其 simulation、dynamic tests 和 code generation 工具多年。
- 标准/格式获取方式：核心承载是 `STATEMATE` 的状态图图形语法及其 step semantics；原文未提供独立 XML/JSON/XMI 交换格式。

## 简报

这篇论文的重要性不在于再讲一次 `Statecharts` 的概念，而在于把工业上真正被执行的那套 `STATEMATE` 语义讲清楚。它明确选择“当前 step 产生的变化只能在下一 step 被感知”，并围绕 compound transition、static reaction、superstep、racing detection 和时间模型，给出一套能驱动仿真、测试和代码生成的可执行语义。

- 形式主义定位：`Statecharts` 在 `STATEMATE` 工具链中的可执行语义版本。
- 构造方式简述：配置由 OR/AND 层次状态确定，step 中先准备输入与定时，再求 enabled CT/SR，再统一提交状态与数据更新。
- 基础设施与场景简述：直接服务复杂反应式系统的仿真、动态测试、时间推进与代码生成。

```text
层次状态图 -> configuration / CT / SR / step algorithm -> simulation / tests / code generation
```

## 形式主义定义与核心对象

### 定义对象

论文核心要回答的是：当一个层次状态图里同时出现正交并发、跨层迁移、history、静态反应和定时行为时，`STATEMATE` 在一个 step 里究竟怎么执行。

### 核心抽象

原文首先把 configuration 定义为一组必须满足层次约束的状态集合。可保守整理为：

$$
\mathcal{C} \subseteq S
$$

其中配置 `\mathcal{C}` 必须满足：

1. 根状态 `R` 必须在 `\mathcal{C}` 中。
2. 若 `A \in \mathcal{C}` 且 `A` 是 OR-state，则其子状态中恰有一个在 `\mathcal{C}` 中。
3. 若 `A \in \mathcal{C}` 且 `A` 是 AND-state，则其所有子状态都在 `\mathcal{C}` 中。
4. `\mathcal{C}` 只包含由上述规则闭包强制得到的状态。

为了描述 `STATEMATE` 真正执行的对象，这里把单个模型保守整理成：

$$
SM = (S, R, E, D, CT, SR, H)
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合，包含 OR/AND 层次状态。
2. `R` 是根状态。
3. `E` 是外部事件、内部生成事件和 timeout 事件集合。
4. `D` 是 data-items 与 conditions。
5. `CT` 是 compound transitions 集合。
6. `SR` 是 static reactions 集合。
7. `H` 是 history information。

### 一个最小例子与通俗解释

论文最基础的例子是：系统当前在状态 `A`，事件 `ev` 到达后，经由 transition `t1` 进入状态 `B` 并执行动作 `act`。

这个 step 会发生的事情是：

1. `t1` 被启用并被选入当前 step。
2. `A` 被退出，`B` 被进入。
3. `exited(A)` 和 `entered(B)` 这些特殊事件会被生成。
4. 但这些新事件不会在本 step 被再次消费，而只会在下一个 step 生效。

通俗地说，`STATEMATE` 不是“边走边立即感知刚才的新变化”，而是“本 step 先统一结算，下一 step 再看结算结果”。

### 运行 / 接受 / 转移语义

论文的中心其实是 step algorithm。可压缩成如下关系：

$$
Status_{t+1} = Step(Status_t, Ext_t)
$$

上式中的符号逐项解释如下：

1. `Status_t` 是 step 开始时的系统状态，包含当前 configuration、活动列表、条件值、上一步生成事件、history 与 timeout 信息。
2. `Ext_t` 是自上一步以来环境给出的外部变化。
3. `Step` 是论文第 8 节的三阶段算法。
4. `Status_{t+1}` 是完成一个 step 后的新系统状态。

在 step 的核心阶段，执行集合可概括为：

$$
EN = MaxNonConflict(EnabledCT) \cup EnabledSR
$$

其中：

1. `EnabledCT` 是当前可触发的 compound transitions。
2. `MaxNonConflict` 表示按优先级去冲突后得到的最大非冲突集合。
3. `EnabledSR` 是在未被退出状态中仍有效的 static reactions。

论文还明确给出一个关键语义边界：

$$
\text{effects generated in step } t \text{ are sensed only in step } t+1
$$

也就是说：

1. 当前 step 里生成的事件、条件变化和数据修改不会被同一步再次观察。
2. 因而模型不能“进入某状态后又因为刚进入而立即在同一步退出”。
3. 这正是 `STATEMATE` 与许多其他 `Statecharts` 语义变体的主要分歧点。

### 语义边界

这套语义非常明确地是 `STATEMATE` 的工具语义，而不是所有 `Statecharts` 共享的唯一正统语义：

1. 它采纳“next-step visibility”而不是即时可见更新。
2. 它允许 nondeterministic choice，但交给不同工具以不同方式处理。
3. 它的时间模型围绕 step/superstep，而不是显式时钟自动机。

### 关键性质与判定边界

论文突出的是执行一致性与工程可实现性：

1. configuration 必须始终合法，不能卡在 connector 或半层次状态上。
2. CT 优先于 SR；若状态在本 step 被退出，其 SR 本 step 不执行。
3. 赋值采用“两阶段提交”，尽量减少执行顺序对结果的影响。
4. racing detection 既检查单 step 内，也检查 superstep 内的因果顺序。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | configuration、OR/AND 状态和 history 都是核心。 |
| 事件 / 触发 | 强支持 | 外部事件、内部生成事件、timeout 事件共同驱动 step。 |
| 守卫 / 数据 | 强支持 | data-items、conditions 与 transition actions 都进入语义。 |
| 层次 | 强支持 | 合法 configuration 与 compound transitions 都依赖层次结构。 |
| 并发 / 同步 | 强支持 | orthogonal components 与 superstep 是主要语义对象。 |
| 时间约束 | 部分支持 | 有 step、superstep 和两种时间模型，但无显式时钟约束语言。 |
| 连续动态 / 随机性 | 不支持 | 纯离散反应式控制语义。 |
| 可执行 / 可验证性 | 强支持 | 直接驱动仿真、动态测试与代码生成。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| configuration 约束 | `$\mathcal{C} \subseteq S$` | 当前活动状态集合必须满足 OR/AND 闭包规则。 |
| 模型骨架 | `$SM = (S, R, E, D, CT, SR, H)$` | 语义围绕状态、事件、数据、compound transitions、static reactions 与 history 组织。 |
| step 语义 | `$Status_{t+1} = Step(Status_t, Ext_t)$` | 一个 step 消费外部变化并产生新的全局状态。 |
| 执行集合 | `$EN = MaxNonConflict(EnabledCT) \cup EnabledSR$` | 先求启用 CT，再去冲突，再加入可执行 SR。 |
| next-step visibility | `$\text{effects in } t \Rightarrow \text{sensed in } t+1$` | 本步生成的事件和赋值只在下一步可见。 |

## 构造方式与承载格式

### 建模入口

建模入口是 `STATEMATE` 风格的层次状态图，包括：

1. OR/AND 状态。
2. transition segments 与 connectors。
3. compound transitions。
4. static reactions、entry/exit actions、history、timeout。

### 机器可处理承载方式

机器可处理承载是 `STATEMATE` 模型本身及其内部 step semantics。论文并未把它抽象为开放中立格式，而是把它描述成工具执行规则。

### 交换与互操作

这篇论文几乎不讨论跨工具交换，重点是“`STATEMATE` 到底怎么执行”，不是“如何互操作”。

## 配套基础设施

- 建模/编辑工具：`STATEMATE` 图形建模环境。
- 解析/交换/元模型支持：论文聚焦工具语义，不提供开放元模型。
- 仿真/执行支持：step algorithm 直接驱动 simulation tool。
- 验证/分析支持：dynamic tests tool 会枚举 nondeterministic choices，simulation tool 能检测 racing。
- 代码生成/转换支持：软件与硬件 code generators 都以内文语义为准。
- 标准化或社区生态：影响后续大量 `Statecharts/UML` 语义工作，但本身是工具实现语义而非开放标准。

## 适用场景与需求前提

### 适用场景

适合复杂反应式软件、控制逻辑、嵌入式行为建模，尤其是需要层次、正交并发和 history 的模型。

### 需求前提

1. 需求存在明确的层次状态与正交子行为。
2. 事件与模式切换是系统主轴。
3. 可接受“本步变化、下步感知”的一致 step 语义。
4. 需要仿真、动态测试或代码生成与同一语义对齐。

### 不适用或高成本场景

如果需求强调开放交换、跨平台元模型或连续物理演化，`STATEMATE` 语义并不是最低成本选择。

## 与相邻形式主义的关系

相对 1987 年的原始 `Statecharts`，这篇把工具实际执行规则写实化；相对 `SyncCharts`，它的并发与抢占更贴近通用层次状态图而非同步语言前端；相对 `SCXML`，它更偏工具内部语义而非交换载体。

## 与本研究的关系

### 对 Project 1 的价值

它说明“同一个状态图”在工程里必须有精确定义的 step semantics，否则生成和验证都不可信。

### 作为目标形式主义还是中间表示

更适合作为 `Statecharts/UML` 家族语义校准基准，而不是直接作为跨工具中立中间表示。

### 对需求到模型生成的启发

如果未来要自动生成层次状态图，生成器必须同时决定：事件何时可见、冲突如何解、compound transition 怎样成形，而不能只画图不定语义。

### 现实限制

它绑定 `STATEMATE` 工具语境，迁移到 `UML`、`SCXML` 或其他语义时仍需做对应映射。

## 重要的相关工作

### 奠基或前身工作

- `Statecharts: A Visual Formalism for Complex Systems`
- `Harel et al. 1987` 对状态图语义的早期讨论

### 同类型或同家族工作

- `SyncCharts`
- `UML State Machine`
- 各类 flattening / HRM / CRSM 状态图验证语义

### 标准 / 格式 / 工具链工作

- `STATEMATE` simulation / dynamic tests / code generation 工具线
- 后续 `UML` 形式化与模型检查工作

### 与本研究关系最紧的工作

- 所有“需求到层次状态机”的自动生成任务，都必须面对这类 step 级执行细节。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：STATEMATE Statecharts
- 论文角色：工具语义
- 核心功能：把 `STATEMATE` 中层次状态图的 step、compound transition、static reaction 与时间推进语义固定下来。

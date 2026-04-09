# 一种用于反应式与混成系统建模的新形式主义 / A New Formalism for Modeling of Reactive and Hybrid Systems

## 基本信息

- 标题：A New Formalism for Modeling of Reactive and Hybrid Systems
- 中文标题：一种用于反应式与混成系统建模的新形式主义
- 作者：Martin Otter, Martin Malmheden, Hilding Elmqvist, Sven Erik Mattsson, Charlotta Johnsson
- 发表：Proceedings of the 7th International Modelica Conference, 364-377, 2009
- DOI：`10.3384/ecp09430108`
- 链接：https://doi.org/10.3384/ecp09430108
- 形式主义：Modelica_StateGraph2
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：形式主义 / 工具库
- 工具/实现获取方式：原文给出的直接实现是开源 `Modelica_StateGraph2` 库，并说明其目标是替换 `Modelica.StateGraph`。
- 标准/格式获取方式：机器可处理承载来自 `Modelica_StateGraph2` 组件库、Modelica 3.1 语义和文中给出的 port-based formalization。

## 简报

这篇论文的重点是把 `StateGraph` 从“能用的库”提升成“更安全、更适合反应式与混成系统”的正式建模载体。作者不仅给出新库，还直接给出结构化的数学对象、解释算法和若干 safety constraints，因此它比单纯的 Modelica 控制库更接近一个可验证的专用状态机形式主义。

- 形式主义定位：面向 `Modelica` 生态的安全层次状态机 / 混成系统模式控制载体。
- 构造方式简述：Generalized Step、Transition、Parallel Step 和图形 action blocks 共同构成模型。
- 基础设施与场景简述：直接与 `Modelica` 物理模型、`Modelica_EmbeddedSystems` 和 `NuSMV` 验证流程协同。

```text
模式控制与混成需求 -> Modelica_StateGraph2 generalized steps -> interpretation algorithm -> 仿真 / 控制实现 / 模型检查
```

## 形式主义定义与核心对象

### 定义对象

论文处理的对象不是一般平面状态图，而是：

1. 可与 `Modelica` 连续模型组合的 generalized steps。
2. 带 suspend / resume 的层次并行结构。
3. 有结构安全约束的反应式 / 混成系统模式图。

### 核心抽象

论文直接把一个 `StateGraph` 模型写成：

$$
\Gamma = \langle V_c, G, T, g_I \rangle
$$

上式中的符号逐项解释如下：

1. `V_c` 是作为转移条件使用的布尔表达式集合。
2. `G` 是 generalized step 集合。
3. `T` 是 transition 集合。
4. `g_I` 是初始 generalized step。

每个 generalized step `g_i` 又被定义为：

$$
g_i = \langle I, R, O, S, \Gamma_s \rangle
$$

其中：

1. `I` 是 entry ports。
2. `R` 是 resume ports。
3. `O` 是 exit ports。
4. `S` 是 suspend ports。
5. `\Gamma_s` 是该 step 内部的子图集合。

每条 transition 为：

$$
t_i = \langle p_{IR}(t_i), p_{OS}(t_i), Condition(t_i), Delay(t_i) \rangle
$$

其中：

1. `p_{IR}(t_i)` 是后继 generalized step 的 entry 或 resume 端口。
2. `p_{OS}(t_i)` 是前驱 generalized step 的 out 或 suspend 端口。
3. `Condition(t_i)` 是布尔触发条件。
4. `Delay(t_i)` 是可选正延迟。

### 一个最小例子与通俗解释

论文给出一个非常直观的最小例子：

1. 初始 step `s1` 经过 `T1` 在 1 秒后进入并行组件 `p`。
2. `p` 内部包含两个并行分支。
3. 若输入 `u` 为真，则 `T6` 从 `p.s[1]` 触发，把整个并行组件 suspend 到 `s6`。
4. `s6` 经过 `T7` 两秒后从 `p.r[1]` 恢复并继续先前的并行执行状态。

通俗解释是：`StateGraph2` 像“带记忆的并行超状态”。它不只是说“当前在哪个状态”，还明确记录某个并行子图是正常退出、被挂起，还是从上次挂起点恢复。

### 运行 / 接受 / 转移语义

论文给出了明确的解释算法。若用保守整理的简写，某条转移 `t_i` 可触发的条件为：

$$
fireable(t_i) \iff Condition(t_i) \land Active(pred(t_i)) \land ExitReady(pred(t_i))
$$

上式中的符号逐项解释如下：

1. `Condition(t_i)` 表示转移守卫为真。
2. `pred(t_i)` 是 `t_i` 的前驱 generalized step，这里是根据原文端口定义做的保守缩写。
3. `Active(pred(t_i))` 表示前驱 step 当前激活。
4. `ExitReady(pred(t_i))` 表示该前驱内部若含子图，则所有相关 exit steps 都已满足退出条件。

论文还规定：若多个转移共享同一前驱 step，则按端口位置优先级选择，较小的 out/suspend 向量索引优先。

对安全性，原文给出一个关键结构约束：

$$
\forall \ell \in Loops(\Gamma),\ \exists t_i \in \ell.\ Delay(t_i) > 0
$$

这表示：

1. `Loops(\Gamma)` 是图中的循环集合。
2. 每个循环至少要有一条带正延迟的转移。
3. 其目的是防止无限瞬时循环和无界 event iteration。

### 语义边界

`StateGraph2` 的边界比普通状态图库更清晰：

1. 它不追求通用状态机最简理论，而是优先保证 `Modelica` 环境里的安全执行。
2. 它允许层次、并行、挂起/恢复，但严格禁止某些会制造未定义激活数增长的“穿边”连接。
3. 它的强项是与物理/混成模型组合，而不是做中立交换标准。

### 关键性质与判定边界

论文强调的关键性质包括：

1. 图结构必须一致且无 unsafe connections。
2. 解释算法能保证有限 event iterations。
3. 可把布尔部分抽取给 `NuSMV` 做死锁等性质验证。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | generalized steps 和 parallel steps 是核心对象。 |
| 事件 / 触发 | 强支持 | 转移条件与端口事件共同决定状态变化。 |
| 守卫 / 数据 | 强支持 | 守卫来自外部输入或 Modelica 模型输出。 |
| 层次 | 强支持 | step 内部可嵌套子图并支持 resume。 |
| 并发 / 同步 | 强支持 | `Parallel` 组件支持并行分支和 exit synchronization。 |
| 时间约束 | 强支持 | transition 可带显式 `Delay(t_i)`。 |
| 连续动态 / 随机性 | 部分支持 | 离散模式本体不含连续方程，但可与任意 Modelica 物理模型耦合。 |
| 可执行 / 可验证性 | 强支持 | 原文同时覆盖执行、安全检查和 `NuSMV` 验证。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型本体 | `$\Gamma = \langle V_c, G, T, g_I \rangle$` | 状态图由条件、generalized steps、转移和初始 step 构成。 |
| generalized step | `$g_i = \langle I, R, O, S, \Gamma_s \rangle$` | 一个 step 同时能承载 entry/exit、suspend/resume 与子图。 |
| 转移对象 | `$t_i = \langle p_{IR}(t_i), p_{OS}(t_i), Condition(t_i), Delay(t_i) \rangle$` | 转移直接绑定端口、条件和可选延迟。 |
| 触发判定 | `$fireable(t_i) \iff Condition(t_i) \land Active(pred(t_i)) \land ExitReady(pred(t_i))$` | 转移不仅要条件为真，还要求前驱及其子图处于可退出状态。 |
| 循环约束 | `$\forall \ell \in Loops(\Gamma),\ \exists t_i \in \ell.\ Delay(t_i) > 0$` | 每个环都要至少带一个延迟，以避免无限瞬时循环。 |

## 构造方式与承载格式

### 建模入口

建模入口是 `Modelica_StateGraph2` 组件：`Step`、`Transition`、`Parallel` 以及图形 action blocks。

### 机器可处理承载方式

机器可处理承载就是 `Modelica` 模型本身。广义步骤、端口和逻辑块都直接落在 `Modelica` 组件图和方程系统里。

### 交换与互操作

互操作重点不在开放交换标准，而在于和 `Modelica` 物理模型、嵌入式库以及验证工具的内生态协同。

## 配套基础设施

- 建模/编辑工具：`Modelica_StateGraph2` 图形建模环境。
- 解析/交换/元模型支持：依赖 `Modelica` 3.1 语义和组件结构。
- 仿真/执行支持：直接由 `Modelica` 仿真器执行。
- 验证/分析支持：原文演示了抽取布尔模型并交给 `NuSMV` 验证。
- 代码生成/转换支持：与 `Modelica_EmbeddedSystems` 方向协同。
- 标准化或社区生态：目标是并入 `Modelica Standard Library` 的后续版本。

## 适用场景与需求前提

### 适用场景

适合模式切换明显、需要与连续物理模型联立仿真的反应式系统和混成系统。

### 需求前提

1. 需求中存在清晰的模式切换、挂起/恢复和并行子逻辑。
2. 系统要与 `Modelica` 物理或控制模型协同。
3. 需要结构安全检查和一定程度的形式验证支持。

### 不适用或高成本场景

如果目标是与 `Modelica` 无关的轻量交换格式，或只需要极简离散状态机，`StateGraph2` 会显得偏重。

## 与相邻形式主义的关系

相对 `Modelica.StateGraph`，它更安全、更强调 suspend/resume 和验证；相对 `ModeGraph`，它更通用地覆盖反应式与混成系统；相对 `Stateflow`，它更开放于 `Modelica` 物理建模生态。

## 与本研究的关系

### 对 Project 1 的价值

它是一个非常现实的“工程型目标形式主义”，证明状态机可以直接嵌在物理系统建模语言里，并保持可验证性。

### 作为目标形式主义还是中间表示

对 `Modelica` 生态场景，它可以直接作为目标形式主义；对更一般的自动建模链，它也适合作为从抽象状态机投影到物理系统模型的后端。

### 对需求到模型生成的启发

当需求里既有模式控制，又要和被控对象方程联调时，生成 generalized steps + ports 的结构，比平面状态图更贴近真正的落地形式。

### 现实限制

它的表达和语义都紧耦合 `Modelica`，因此跨生态迁移不如 `SCXML` 这类开放载体。

## 重要的相关工作

### 奠基或前身工作

- `StateGraph`
- `ModeGraph`
- `Statecharts`

### 同类型或同家族工作

- `Sequential Function Charts`
- `Safe State Machines`
- `Mode-Automata`

### 标准 / 格式 / 工具链工作

- `Modelica` 3.1
- `Modelica_EmbeddedSystems`
- `NuSMV`

### 与本研究关系最紧的工作

- 可与物理系统模型直接耦合的目标状态机载体。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：Modelica_StateGraph2
- 论文角色：形式主义 / 工具库
- 核心功能：给 `Modelica` 生态提供可安全执行、可验证的层次并行状态机载体。
- 关键特性：generalized steps、suspend/resume、delay、safe graphs、`NuSMV` 验证。
- 构造方式：`Modelica_StateGraph2` 组件图 + 端口化 4 元组模型 + interpretation algorithm。

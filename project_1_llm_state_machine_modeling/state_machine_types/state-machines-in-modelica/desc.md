# Modelica 中的状态机 / State Machines in Modelica

## 基本信息

- 标题：State Machines in Modelica
- 中文标题：Modelica 中的状态机
- 作者：Hilding Elmqvist, Fabien Gaucher, Sven Erik Mattsson, Francois Dupont
- 发表：Proceedings of the 9th International Modelica Conference, 37-46, 2012
- DOI：`10.3384/ecp1207637`
- 链接：https://doi.org/10.3384/ecp1207637
- 形式主义：Modelica State Machines
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：语言扩展
- 工具/实现获取方式：论文面向 Modelica 3.3 语言与其工具实现，未单独提供独立仓库。
- 标准/格式获取方式：核心入口是 Modelica 3.3 中的 `transition`、`initialState`、`activeState` 等语言级元素。

## 简报

这篇论文做的不是“用 Modelica 画状态机”，而是把状态机真正纳入 Modelica 语言核心：状态是没有连续方程的 block，迁移是新型 connection，全部状态机语义只用 `13` 条 Modelica 方程描述。它把 `ModeGraph/StateGraph` 那类库级方案提升成语言级语义。

- 形式主义定位：Modelica 3.3 中的语言级离散状态机与层次状态机机制。
- 构造方式简述：同一层级、同一 clock 的 block 集群通过 `transition(...)` 连接形成状态机，并用 `initialState(...)` 指定初始状态。
- 基础设施与场景简述：直接作为 Modelica 语言的一部分，与同步语言原语、物理系统建模和嵌入式代码生成协同。

```text
控制系统模式需求 -> Modelica blocks + transition equations -> 13-equation semantics -> 语言级编译 / 仿真 / 嵌入式实现
```

## 形式主义定义与核心对象

### 定义对象

论文要解决的是“完整系统模型里如何内生地放入控制状态机”。因此它强调：

1. 状态机和普通 Modelica block 共享同一种语言环境。
2. 状态切换要和 clock、reset、parallel sub-state machines 一起被正式规定。

### 核心抽象

原文没有用一个元组定义全部 Modelica 状态机，而是用 transition 记录和 `13` 条方程给出语义。按论文结构可保守整理为：

$$
SM = (Q, q_0, \Theta, C, K)
$$

上式中的符号逐项解释如下：

1. `Q` 是可作为状态的 block 实例集合。
2. `q_0` 是通过 `initialState(q_0)` 标记的初始状态。
3. `\Theta` 是 transition 集合，每条 transition 带 `from`、`to`、`immediate`、`reset`、`synchronize`、`priority` 等属性。
4. `C` 是 transition condition 数组 `c[:]`。
5. `K` 是共享 clock 约束，论文要求同一状态机内所有部分必须具有相同 clock。

论文直接给出的 transition 构造是：

```modelica
transition(from, to, condition, immediate, reset, synchronize, priority)
```

### 一个最小例子与通俗解释

论文第一个例子是两状态机：

1. `state1` 激活时把 `i` 增加 `2`。
2. `state2` 激活时把 `i` 减少 `1`。
3. 当 `i > 10` 时，从 `state1` 切到 `state2`。
4. 当 `i < 1` 时，从 `state2` 切回 `state1`。

通俗解释是：在 Modelica 里，“状态”不再只是库里的组件，而是普通 block 进入某个被激活的上下文。状态机就像一组 block 在轮流拿执行权。

### 运行 / 接受 / 转移语义

论文给出的 13 条方程中，最核心的是选中状态和 fired transition 的定义。首先：

$$
\mathrm{selectedState} =
\begin{cases}
1, & \text{if reset} \\
\mathrm{previous}(\mathrm{nextState}), & \text{otherwise}
\end{cases}
$$

立即转移与延迟转移分别计算：

$$
\mathrm{immediate} = \max \{ i \mid t[i].immediate \land t[i].from = \mathrm{selectedState} \land c[i] \}
$$

$$
\mathrm{delayed} = \max \{ i \mid \neg t[i].immediate \land t[i].from = \mathrm{nextState} \land c[i] \}
$$

最后决定真正 firing 的 transition：

$$
\mathrm{fired} = \max(\mathrm{previous}(\mathrm{delayed}), \mathrm{immediate})
$$

当前活动状态为：

$$
\mathrm{activeState} =
\begin{cases}
1, & \text{if reset} \\
t[\mathrm{fired}].to, & \mathrm{fired} > 0 \\
\mathrm{selectedState}, & \text{otherwise}
\end{cases}
$$

这些语义公式中的符号逐项解释如下：

1. `previous(x)` 是上一时刻的 `x`。
2. `t[i]` 是第 `i` 条 transition 记录。
3. `c[i]` 是第 `i` 条 transition 当前条件是否成立。
4. `immediate` 对应 strong transition。
5. `delayed` 对应 weak/delayed transition。
6. `activeState` 是当前 clock tick 的活动状态编号。

### 语义边界

这套状态机是严格 clocked 的离散语义：

1. 一个状态机内所有部分必须同 clock。
2. 能成为 state 的 block 不能含 continuous-time equations 或 algorithms。
3. 立即/延迟、reset/resume、synchronize 都在语言里被显式区分。

因此它不是一般混合自动机，而是“可嵌入到更大物理系统模型中的离散控制骨架”。

### 关键性质与判定边界

论文最关键的工程性质是多状态输出的安全合并。它给出的 merged semantics 形如：

$$
v =
\begin{cases}
y_1, & \mathrm{activeState}(\mathrm{state1}) \\
y_2, & \mathrm{activeState}(\mathrm{state2}) \\
\mathrm{last}(v), & \text{otherwise}
\end{cases}
$$

这说明多个状态中的输出定义会被编译器收束成单个赋值表达式，而不是运行时靠优先级抢占，从而避免并行状态机常见的隐式赋值冲突。

论文还给出 final state 与 synchronized transition 的判断：

$$
\mathrm{finalStates}[i] = \Big(\max_j [t[j].from = i] = 0\Big)
$$

$$
\mathrm{stateMachineInFinalState} = \mathrm{finalStates}[\mathrm{activeState}]
$$

这为并行子状态机的同步退出提供了语言级依据。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 任意满足约束的 block 都可成为 state。 |
| 事件 / 触发 | 强支持 | transition condition 是状态切换核心。 |
| 守卫 / 数据 | 强支持 | condition 与状态输出直接在 Modelica 中表达。 |
| 层次 | 强支持 | 论文给出 hierarchical state machine 示例。 |
| 并发 / 同步 | 强支持 | parallel sub-state machines 与 synchronize transition 都是语言级要素。 |
| 时间约束 | 部分支持 | 通过 clocked、immediate/delayed 语义支持离散时间控制，不是显式时钟自动机。 |
| 连续动态 / 随机性 | 部分支持 | state 本身不含连续方程，但可嵌在完整物理系统模型中。 |
| 可执行 / 可验证性 | 强支持 | 语义被压成 13 条方程，便于编译和实现。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 初始/当前状态 | `$\mathrm{selectedState} = 1$ or `$\mathrm{previous}(\mathrm{nextState})$` | reset 时回初始态，否则沿上一步延续。 |
| 立即转移选择 | `$\mathrm{immediate} = \max \{ i \mid ... \}$` | 当前 tick 立即可执行的最高优先级转移。 |
| 延迟转移选择 | `$\mathrm{delayed} = \max \{ i \mid ... \}$` | 下一 tick 预备执行的 delayed 转移。 |
| 真正 firing | `$\mathrm{fired} = \max(\mathrm{previous}(\mathrm{delayed}), \mathrm{immediate})$` | immediate 和 delayed 的统一仲裁。 |
| 活动态 | `$\mathrm{activeState}$` | 当前 clock tick 的唯一活动状态。 |
| 输出合并 | `$v = y_1 / y_2 / \mathrm{last}(v)$` | 编译器把多状态输出收敛成单赋值。 |
| 最终状态 | `$\mathrm{finalStates}[i] = (\max_j[t[j].from=i]=0)$` | 判断并行子状态机是否已进入 final state。 |

## 构造方式与承载格式

### 建模入口

建模入口是 Modelica 语言本身：block、transition connection、`initialState`、`activeState` 等内建构造，不再依赖外部状态图库。

### 机器可处理承载方式

机器可处理承载方式就是 Modelica 源码和对应图形连接。论文特别强调：

1. transition 是一种新的 connection。
2. 状态机语义由 13 条方程直接定义。
3. 编译器负责编排状态输出与 reset 行为。

### 交换与互操作

互操作依赖 Modelica 生态本身。论文没有定义独立于 Modelica 的 XML/JSON 交换格式，它选择直接把状态机嵌进语言核心。

## 配套基础设施

- 建模/编辑工具：Modelica 3.3 兼容工具。
- 解析/交换/元模型支持：语言级元素意味着工具链天然可解析。
- 仿真/执行支持：这是论文核心，全部语义都面向编译和仿真执行。
- 验证/分析支持：原文重点在语义一致性与实现，不主打独立 model checking。
- 代码生成/转换支持：论文明确把嵌入式代码生成视为引入状态机的目标之一。
- 标准化或社区生态：依附 Modelica 标准演进。

## 适用场景与需求前提

### 适用场景

适合物理系统模型中的控制逻辑、嵌入式控制软件、需要把状态机和连续系统模型放在同一语言中的场景。

### 需求前提

1. 模式切换是系统行为的重要组成部分。
2. 状态逻辑希望直接用 Modelica block 表达。
3. 系统能接受统一 clock 的离散控制语义。
4. 需要 reset / resume / synchronize 等精确语义。

### 不适用或高成本场景

如果状态机必须独立于 Modelica 工具链流通，或者需要更开放的交换格式，语言级嵌入会限制可移植性。

## 与相邻形式主义的关系

相对 `StateGraph`，它是语言级而不是库级；相对 `ModeGraph`，它把 mode semantics 进一步内化到标准语言；相对 `Statecharts`，表达力相近但承载和执行更贴近同步/物理系统建模。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合回答一个现实问题：生成出来的状态机最终放哪里。对以控制系统为目标的建模链，`Modelica State Machines` 提供了一个强工程相关的落点。

### 作为目标形式主义还是中间表示

如果目标是物理系统建模或嵌入式控制实现，它可以直接作为目标形式主义；否则也可作为从抽象状态机投影到工程实现语言的后端。

### 对需求到模型生成的启发

当需求已经隐含出清晰模式和切换条件，而且后续要与物理系统模型联调时，直接生成 Modelica 状态机比先生成外部状态图库再手工嵌回系统模型更高效。

### 现实限制

它强依赖 Modelica 语言环境和时钟语义，因此不如 `SCXML` 那样适合作为通用交换标准。

## 重要的相关工作

### 奠基或前身工作

- `StateGraph`
- `Mode-Automata`

### 同类型或同家族工作

- `Statecharts`
- `SysML State Machine`
- Lucid Synchrone / LCM

### 标准 / 格式 / 工具链工作

- Modelica 3.3 语言与同步原语

### 与本研究关系最紧的工作

- 状态机如何作为控制系统建模语言的原生构件落地。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：Modelica State Machines
- 论文角色：语言扩展
- 核心功能：把状态机和层次/并行子状态机纳入 Modelica 语言核心。
- 关键特性：13 条语义方程、immediate/delayed、reset/resume、单赋值输出合并。
- 构造方式：Modelica blocks + transition equations + compiler-mediated semantics。

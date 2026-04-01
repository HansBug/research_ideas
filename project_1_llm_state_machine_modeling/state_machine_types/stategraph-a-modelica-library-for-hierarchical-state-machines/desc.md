# StateGraph：用于层次状态机的 Modelica 库 / StateGraph - A Modelica Library for Hierarchical State Machines

## 基本信息

- 标题：StateGraph - A Modelica Library for Hierarchical State Machines
- 中文标题：StateGraph：用于层次状态机的 Modelica 库
- 作者：Martin Otter, Karl-Erik Arzen, Isolde Dressler
- 发表：Proceedings of the 4th International Modelica Conference, 569-578, 2005
- DOI：原文未提供
- 链接：https://modelica.org/events/Conference2005/online_proceedings/Session7/Session7b2.pdf
- 形式主义：StateGraph
- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 论文角色：工具 / 库
- 工具/实现获取方式：论文把 `Modelica.StateGraph` 直接作为免费 `Modelica` 库发布，并给出 `ControlledTanks` 例子展示其用法。
- 标准/格式获取方式：核心承载是 `Modelica.StateGraph` 组件图和 `Modelica` 方程语义；原文未提供独立于 `Modelica` 的交换格式。

## 简报

这篇论文做的事情很务实：不是另起炉灶定义一个全新状态机，而是把 `Grafchart / Grafcet / Statecharts` 的优点压成一个能在 `Modelica` 里安全执行的层次状态机库。其关键设计选择是把“动作”从步骤内部脚本改成 `Modelica` 方程和逻辑块，由单赋值规则来强制消解很多传统状态图库里的隐式冲突。

- 形式主义定位：`Modelica` 生态中的层次状态机/顺控库。
- 构造方式简述：`Step`、`Transition`、`Parallel`、`Alternative` 与 `CompositeStep` 共同构成图。
- 基础设施与场景简述：直接挂接 `Modelica` 逻辑块和物理系统模型，适合工业顺控与监督控制。

```text
监督控制需求 -> StateGraph steps / transitions / composite steps -> Modelica equations -> 仿真 / 控制联调
```

## 形式主义定义与核心对象

### 定义对象

原文关注的是如何在 `Modelica` 里构造一个既像 `Statecharts` 又能避免动作冲突的层次状态机库。其对象包括：

1. 有 `active` 标志的步骤。
2. 带条件和可选定时器的转移。
3. `Parallel` / `Alternative` / `CompositeStep` 三类结构组件。

### 核心抽象

论文没有单独给出统一数学元组，这里按其结构做保守整理：

$$
SG = (Q, Q_0, \Delta, \Pi, \Phi)
$$

上式中的符号逐项解释如下：

1. `Q` 是步骤和复合步骤集合。
2. `Q_0 \subseteq Q` 是初始步骤集合。
3. `\Delta` 是 transition 集合。
4. `\Pi` 是并行、选择和复合结构组件集合。
5. `\Phi` 是承载执行语义的 `Modelica` 方程组。

单条 transition 的核心实现方程为：

$$
fire = condition \land inPort.available \land \neg outPort.occupied
$$

其中：

1. `condition` 是转移守卫。
2. `inPort.available` 表示前驱 step 当前 active。
3. `outPort.occupied` 表示后继 step 已激活或即将被更高优先级转移占用。

步骤激活更新则写成：

$$
newActive = anyTrue(inPort.set) \lor (active \land \neg anyTrue(outPort.reset))
$$

这里：

1. `inPort.set` 表示某个入边转移刚刚触发。
2. `outPort.reset` 表示某个出边转移刚刚触发。
3. `active` 是当前步骤上一轮是否活跃。

### 一个最小例子与通俗解释

论文第一页就给出最小例子：

1. `initialStep` 初始为活跃。
2. 一秒后 `transition1` 触发，进入 `step1`。
3. 再过一秒 `transition2` 触发，回到 `initialStep`。

通俗解释是：`StateGraph` 像“用 `Modelica` 方程实现的状态机乐高”。每个转移先算 `fire`，每个步骤再根据 `set/reset` 更新 `active`，直到这一轮没有新转移再触发为止。

### 运行 / 接受 / 转移语义

除了单个 step/transition 规则外，论文还给出并行同步的方程：

$$
split.set = fill(inPort.set, n), \qquad join.reset = fill(outPort.reset, n)
$$

$$
inPort.occupied = anyTrue(split.occupied), \qquad outPort.available = allTrue(join.available)
$$

这些式子说明：

1. 进入并行组件时，入边 `set` 会广播到所有分支。
2. 离开并行组件时，只有所有 join 位置都可用，出边才允许触发。
3. 因而并行分支的同步由 `allTrue(join.available)` 明确控制。

论文对 `CompositeStep` 还给出挂起/恢复机制，其核心思想是保存旧活动状态 `oldActive`，并在 `resume` 时恢复，而不是重启内部子图。

### 语义边界

`StateGraph` 的边界非常工程化：

1. 它依赖 `Modelica` 单赋值规则来避免动作冲突。
2. 它强调图结构执行和物理模型联调，而不是抽象判定边界。
3. 它的时间处理主要是 transition wait time 和外接 logical blocks，不是独立时钟自动机。

### 关键性质与判定边界

论文强调的关键性质包括：

1. 冲突转移通过端口顺序显式定优先级。
2. 并行与选择组件都能在方程层被确定化执行。
3. 一轮求解中持续迭代，直到没有 step 改变 `active` 为止。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `Step` / `CompositeStep` 是核心建模对象。 |
| 事件 / 触发 | 强支持 | 触发由逻辑条件和 `Modelica` 布尔信号驱动。 |
| 守卫 / 数据 | 强支持 | 转移条件可由任意 `Modelica` 逻辑表达式给出。 |
| 层次 | 强支持 | `CompositeStep` 和 `resume/suspend` 提供层次状态。 |
| 并发 / 同步 | 强支持 | `Parallel` 和 `Alternative` 是库级基本结构。 |
| 时间约束 | 部分支持 | 支持 transition `waitTime` 与外接 timer。 |
| 连续动态 / 随机性 | 部分支持 | 状态机本体离散，但可直接连接物理系统模型。 |
| 可执行 / 可验证性 | 强支持 | 直接被 `Modelica` 方程求解器执行。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 保守模型元组 | `$SG = (Q, Q_0, \Delta, \Pi, \Phi)$` | 该库由步骤、初始步骤、转移、结构组件和方程语义构成。 |
| 转移触发 | `$fire = condition \land inPort.available \land \neg outPort.occupied$` | 转移要守卫为真、前驱活跃且后继未被占用才触发。 |
| 步骤更新 | `$newActive = anyTrue(inPort.set) \lor (active \land \neg anyTrue(outPort.reset))$` | step 由入边激活、由出边复位。 |
| 并行同步 | `$outPort.available = allTrue(join.available)$` | 并行组件的出口只有在所有 join 端就绪时才可触发。 |

## 构造方式与承载格式

### 建模入口

建模入口是 `StateGraph` 库组件和 `Modelica` 逻辑块，用户以图形方式连接 steps、transitions 和 composite steps。

### 机器可处理承载方式

机器可处理承载直接就是 `Modelica` 模型和其求解方程。动作通常通过 `SetBoolean` 等逻辑组件，而不是步骤内部脚本完成。

### 交换与互操作

互操作依赖 `Modelica` 工具链本身。原文没有提供独立于 `Modelica` 的中立交换格式。

## 配套基础设施

- 建模/编辑工具：`Modelica.StateGraph` 组件库。
- 解析/交换/元模型支持：通过 `Modelica` 组件和连接器承载。
- 仿真/执行支持：由 `Modelica` 方程求解器直接执行。
- 验证/分析支持：原文重点在执行和建模，不主打独立验证器。
- 代码生成/转换支持：可与 `Modelica` 代码生成/仿真链协同。
- 标准化或社区生态：属于 `Modelica` 生态和 `Modelica Standard Library` 方向。

## 适用场景与需求前提

### 适用场景

适合工业自动化、监督控制和与物理过程联调的控制逻辑，尤其是需要图形层次结构和可复用组件的场景。

### 需求前提

1. 系统行为可拆成明确步骤和条件转移。
2. 希望控制逻辑直接嵌入 `Modelica` 模型。
3. 可以接受动作主要通过 `Modelica` 方程和逻辑块表达。

### 不适用或高成本场景

如果目标是开放交换标准或纯理论分析，`StateGraph` 的 `Modelica` 依赖会带来额外绑定成本。

## 与相邻形式主义的关系

相对 `SFC/Grafcet`，它更自然地支持层次与 `Modelica` 联调；相对 `Statecharts`，它用 `Modelica` 单赋值规则替代脚本式 entry/exit actions；相对后来的 `StateGraph2`，它更轻量但安全性和形式化程度稍弱。

## 与本研究的关系

### 对 Project 1 的价值

它提供了“状态机最终落到物理建模语言中”的一个早期而成熟的例子。

### 作为目标形式主义还是中间表示

对 `Modelica` 场景，它可以直接作为目标形式主义；对一般研究链，它也适合作为工程后端。

### 对需求到模型生成的启发

当需求最终要和物理模型联仿时，生成 `Step / Transition / CompositeStep` 结构往往比只给出抽象状态图更可执行。

### 现实限制

它的便捷性来自 `Modelica`，因此跨生态共享与独立交换能力有限。

## 重要的相关工作

### 奠基或前身工作

- `Grafcet`
- `Grafchart / JGrafchart`
- `Statecharts`

### 同类型或同家族工作

- `ModeGraph`
- `Modelica State Machines`
- `StateGraph2`

### 标准 / 格式 / 工具链工作

- `Modelica Standard Library`
- `Modelica.Blocks.Logical`

### 与本研究关系最紧的工作

- 可把控制状态机直接嵌进物理系统建模语言的工程载体。

## 文献分类总结

- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 形式主义：StateGraph
- 论文角色：工具 / 库
- 核心功能：在 `Modelica` 中提供可执行、层次化、并行化的状态机库。
- 关键特性：step/transition 方程语义、parallel/alternative、composite step、timer、single-assignment safety。
- 构造方式：`Modelica.StateGraph` 组件图 + `fire/newActive` 方程 + `Modelica` 逻辑块。

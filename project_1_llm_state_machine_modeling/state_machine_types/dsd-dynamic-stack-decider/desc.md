# DSD：动态栈决策器 / DSD - Dynamic Stack Decider

## 基本信息

- 标题：DSD - Dynamic Stack Decider: A Lightweight Decision Making Framework for Robots and Software Agents
- 中文标题：DSD：面向机器人与软件代理的轻量动态栈决策框架
- 作者：Martin Poppinga, Marc Bestmann
- 发表：*International Journal of Social Robotics*, 14(1):73-83, 2022
- DOI：`10.1007/s12369-021-00768-8`
- 链接：https://doi.org/10.1007/s12369-021-00768-8
- 形式主义：`DSD`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：行为 DSL / 轻量决策框架
- 工具/实现获取方式：原文明确给出实现仓库 `https://github.com/bit-bots/dynamic_stack_decider`，并说明支持 `ROS` 集成、`rqt` 可视化以及在 RoboCup 机器人和移动 bartender 场景中的使用。
- 标准/格式获取方式：核心承载方式是作者自定义的 `DSL`，该 `DSL` 描述 decision/action 元素及其 `DAG` 连接；原文未给行业标准格式。

## 简报

`DSD` 的关键不是再发明一种普通状态机，而是把“行为树的可重排控制流”和“状态机的状态保持性”拼到一起：控制流由 `DSL` 描述成一个 `DAG`，运行时真正的当前状态不是某个单节点，而是一条带历史的 stack。decision element 决定下一段分支，action element 像状态机状态一样持续执行；一旦前置条件变了，运行时只要从 stack 中间把失效分支切掉并换上新分支即可。这样既保留了 reactiveness，又保留了“现在到底处在什么状态”的可追踪性。

- 形式主义定位：面向机器人高层行为控制的 stack-based `DSL` 框架，而不是经典图形 `FSM` 编辑器。
- 构造方式简述：用 `DSL` 定义 decision/action elements 及其 `DAG`，运行时按 stack 自底向上重评估 decision、执行栈顶 action。
- 基础设施与场景简述：依托开源 `DSD`、`ROS/rqt` 可视化、可复用模块与中断机制，服务 RoboCup、移动机器人和软件代理行为控制。

```text
行为需求 -> DSD DSL + DAG -> decision/action modules -> runtime stack reevaluation -> ROS execution + visualization
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. decision element (`DE`)：负责判断当前应走哪条分支。
2. action element (`AE`)：负责在某个“状态”中持续执行行为。
3. `DSL`：描述所有可执行路径及其参数。
4. `DAG`：由 `DSL` 编译出的控制流图。
5. stack：保存当前激活元素与到达当前行为的决策历史。
6. reevaluation：对 stack 中部的 decision 进行前置条件重检。
7. interrupt：外部事件触发的整体重置。

### 核心抽象

根据原文对 decision/action/stack 的定义，可保守整理 `DSD` 为：

$$
D = (\mathcal{D}, \mathcal{A}, G, d_0, \Sigma, \rho)
$$

上式中的符号逐项解释如下：

1. `\mathcal{D}` 是 decision elements 集合。
2. `\mathcal{A}` 是 action elements 集合。
3. `G` 是由 `DSL` 构成的有向无环图，给出 decision outcome 到下游元素的映射。
4. `d_0 \in \mathcal{D}` 是根 decision。
5. `\Sigma` 是当前 runtime stack。
6. `\rho` 是 reevaluation 策略，决定哪些 decision 需要被持续重检。

decision 执行可保守写成：

$$
\mathrm{decide}(d, \eta) = o
$$

上式中的符号逐项解释如下：

1. `d \in \mathcal{D}` 是某个 decision element。
2. `\eta` 是当前感知与共享数据上下文。
3. `o` 是该 decision 返回的语义化 outcome，例如 `Yes`、`No`、`FieldPlayer`。

action 执行则可整理为：

$$
\mathrm{act}(a, \eta) \in \{\mathrm{stay}, \mathrm{pop}\}
$$

上式中的符号逐项解释如下：

1. `a \in \mathcal{A}` 是当前栈顶 action。
2. `\mathrm{stay}` 表示 action 继续留在栈顶，下一轮继续执行。
3. `\mathrm{pop}` 表示 action 已完成并从 stack 中弹出。

### 一个最小例子与通俗解释

论文的 `Listing 1` 给了一个极简的 RoboCup 行为：

1. 根 decision `RoleDecision` 决定机器人是 `FieldPlayer` 还是 `Goalie`。
2. 若是 `FieldPlayer`，则继续判断 `BallPositionAvailable`、`DefendAttackDecision` 等。
3. 某些路径会进入 `Kick` 子树，再由 `InKickDistance` 决定是 `KickBall` 还是 `GoToBallDirect`。
4. 真正执行的动作不是整棵树，而是 stack 顶部当前那个 `AE`。

通俗地说，`DSD` 像“带历史的行为树调用栈”：底下保存为什么走到这里，顶上保存现在正在干什么；一旦前提变了，不用重跑整棵树，只把失效那段栈切掉并换上新路径。

### 运行 / 接受 / 转移语义

论文强调的核心语义是 reevaluation。若栈中第 `k` 个 decision 的输出变了，则上方分支整体失效：

$$
\Sigma_{t+1} =
\begin{cases}
\mathrm{prefix}_k(\Sigma_t) \cdot \mathrm{branch}(o_k), & o_k \neq o_k^{prev} \\
\Sigma_t, & o_k = o_k^{prev}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `\Sigma_t` 是当前时刻的 stack。
2. `\mathrm{prefix}_k(\Sigma_t)` 是保留到第 `k` 个 decision 为止的前缀。
3. `o_k` 是本轮 reevaluation 的新 outcome。
4. `o_k^{prev}` 是上一轮 outcome。
5. `\mathrm{branch}(o_k)` 是根据新 outcome 从 `DSL/DAG` 选出的后续路径。

栈顶 action 的单轮执行可进一步写成：

$$
\Sigma_{t+1} =
\begin{cases}
\mathrm{pop}(\Sigma_t), & \mathrm{act}(a_t,\eta_t)=\mathrm{pop} \\
\Sigma_t, & \mathrm{act}(a_t,\eta_t)=\mathrm{stay}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `a_t` 是当前栈顶 action。
2. `\eta_t` 是当前上下文。
3. 若 action 完成，则从 stack 弹出。
4. 若 action 未完成，则继续留在栈顶。

外部中断则可保守整理为：

$$
\Sigma_{t+1} = [d_0]
$$

上式中的符号逐项解释如下：

1. 中断会清空整个 stack。
2. 清空后从根 decision `d_0` 重新开始行为构建。

### 语义边界

`DSD` 的边界也比较清楚：

1. 它不追求经典 `FSM` 那种显式全图状态穷举，而是把当前状态定义成整条 stack。
2. 它重在行为维护性和 reactiveness，不提供形式验证语义。
3. 时间约束不是模型内核，更多依赖 reevaluation 频率和外部系统节拍。
4. 它适合高层决策与行为调度，不替代底层控制器。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 框架骨架 | `$D = (\mathcal{D}, \mathcal{A}, G, d_0, \Sigma, \rho)$` | `DSD` 把 DAG、stack 和 reevaluation 组合成运行时骨架。 |
| decision 输出 | `$\mathrm{decide}(d,\eta)=o$` | decision 根据当前上下文选择分支。 |
| stack 重写 | `$\Sigma_{t+1}=\mathrm{prefix}_k(\Sigma_t)\cdot \mathrm{branch}(o_k)$` | 前置条件变化时只替换失效后缀。 |
| action 保持性 | `$\mathrm{act}(a,\eta)\in\{\mathrm{stay},\mathrm{pop}\}$` | action element 像状态机状态一样可以持续驻留。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 当前状态由整条 stack 定义，栈顶 action 清晰可见。 |
| 事件 / 触发 | 强支持 | reevaluation、interrupt 和外部上下文变化都会触发路径重写。 |
| 守卫 / 数据 | 强支持 | decision outcome、参数传递、黑板/外部数据获取都很核心。 |
| 层次 | 强支持 | `DSL` 中可定义子树、模块与复用路径。 |
| 并发 / 同步 | 中等支持 | 可跑多个独立 behavior stacks，但并发同步不在 DSL 核心。 |
| 时间约束 | 弱支持 | 依赖周期调用与 reevaluation，不含显式时钟语义。 |
| 连续动态 / 随机性 | 不支持 | 面向高层离散决策。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 执行、可视化、可维护性很强；形式验证未覆盖。 |

### 形式化问题与性质

1. `DSD` 最大的差异点是把“状态”从单节点扩成整条 stack。
2. `DE/AE` 分离让 decision 和长期执行动作有了清晰职责边界。
3. `DSL` 使得局部改阈值、重排分支或复用模块的成本比传统 `FSM` 低得多。
4. `do_not_reevaluate` 机制说明它也考虑了“某些动作不可被中断”的实际机器人约束。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 编写 `DSL`，定义 decision/action 元素及其连接关系。
2. 为 decision 和 action 分别实现对应的代码模块。
3. 为复用模块配置参数。
4. 运行时把 `DSL` 解析成 `DAG`，并由 stack 驱动执行。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `DSL` 文本文件。
2. 解析后形成的 `DAG`。
3. runtime stack。
4. decision 和 action 的程序模块。
5. `ROS/rqt` 的实时可视化界面。

### 交换与互操作

互操作重点在：

1. 可通过 getter/setter 与外部模块或黑板交换数据。
2. 多个独立 `DSD` 栈可并存，跨栈通信可交给 `ROS` 消息。
3. `ROS` 集成使它能接入现有机器人软件栈而不必重写执行基础设施。

## 配套基础设施

- 建模/编辑工具：当前主入口是 `DSL`；论文提出未来可加 GUI 自动生成 `DSL`。
- 解析/交换/元模型支持：`DSL` 解析为 `DAG`，支持参数传递、模块复用和 action sequences。
- 仿真/执行支持：框架已在 RoboCup humanoid、移动 bartender 和软件代理场景使用。
- 验证/分析支持：提供 stack 和替代路径的实时可视化；形式验证未见。
- 代码生成/转换支持：不强调代码生成，强调 `DSL` 与模块的快速装配。
- 标准化或社区生态：有开源实现与 `ROS` 集成，但不是通用行业标准。

## 适用场景与需求前提

### 适用场景

适合需要频繁修改行为控制流、持续检查前置条件、同时又希望明确看到“当前状态”和“到达该状态的决策历史”的机器人高层行为控制。

### 需求前提

1. 行为可以拆成 decision 和 action 两类元素。
2. 控制流适合描述成 `DAG` 而不是带大量回边的任意图。
3. 系统需要不断 reevaluate 前置条件。
4. 团队重视行为可维护性、可视化与模块复用。

### 不适用或高成本场景

若系统更关心严格形式分析、复杂并发同步语义或硬实时约束，`DSD` 不是直接答案；它更像高层行为工程框架，而不是验证导向形式主义。

## 与相邻形式主义的关系

相对经典 `FSM/HFSM`，`DSD` 明显降低了新增状态时全图重连的负担；相对行为树，它保留了明确的状态保持性与可追溯决策历史；相对 planner，它更强调 reactiveness 和局部快速改动。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明，一类专用“状态机近亲”载体可以把 `FSM` 的 statefulness 和行为树的可重排控制流结合起来，而且对需求维护非常友好。

### 作为目标形式主义还是中间表示

它更适合作为机器人行为层目标载体，而不是统一中间表示；但其中 `decision/action` 分离、reevaluation 和 stack history 很值得被中间表示吸收。

### 对需求到模型生成的启发

1. 需求生成出的状态机不一定只能是平面状态图，也可以是“路径 + 栈”的运行模型。
2. 前置条件持续重检是许多机器人需求中的一等概念，值得显式建模。
3. 若目标是工程落地，可维护的文本 `DSL` 往往比一次性画图更重要。

## 重要的相关工作

- `FSM/HFSM`：提供了 `DSD` 所继承的 statefulness。
- `Behavior Trees`：提供了其可扩展控制流和 reactiveness 的启发。
- `ROS` 生态：承担其运行时集成与可视化。

## 文献分类总结

- 这是一篇 `📦` 类行为框架条目，重点是用 `DSL + stack` 重新组织高层状态机式行为控制。
- 其描述客体是机器人行为控制逻辑，因此记为 `🎛️`；论文语境聚焦机器人与软件代理，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“状态机式行为如何通过栈与重评估机制获得更强维护性”的工程证据。

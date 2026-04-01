# XRobots 分层状态机语言概览 / An Overview of XRobots: A Hierarchical State Machine-Based Language

## 基本信息

- 标题：An Overview of XRobots: A Hierarchical State Machine-Based Language
- 中文标题：XRobots 分层状态机语言概览
- 作者：Steve Tousignant, Eric Van Wyk, Maria Gini
- 发表：Workshop on Software Development and Integration in Robotics (SDIR VI), 2011
- DOI：原文未提供
- 链接：https://hdl.handle.net/11299/217405
- 形式主义：`XRobots`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：领域特化 DSL / 机器人行为语言
- 工具/实现获取方式：原文把 `XRobots` 描述为 prototype language，并讨论 compiler 的后续工作；论文未提供公开编译器或仓库入口。
- 标准/格式获取方式：承载方式是 `Behavior` 语言语法、entry/transition/exit block 与行为参数；原文未给 XML/JSON 或行业交换标准。

## 简报

`XRobots` 是一门面向移动机器人的分层状态机 DSL，但它最特别的地方不是“又做了一门 HSM 语言”，而是把 behavior 变成一等对象：behavior 可以像参数一样被传来传去，而且既能按值传，也能按引用传。这样一来，机器人行为不只是写死在图里的状态，还可以被组合、复用和参数化。

- 形式主义定位：面向移动机器人行为编程的 HSM-based DSL。
- 构造方式简述：以 `Behavior` 为核心单元，每个 behavior 由参数、声明、entry block、transition block、exit block 组成，并支持 behavior 作为参数传递。
- 基础设施与场景简述：原文以 prototype language 和 compiler 为主，服务 obstacle avoidance、shape tracing 等移动机器人行为编程场景。

```text
机器人行为需求 -> parameterized behaviors / nested HSM -> entry / transition / exit blocks -> 机器人执行代码
```

## 形式主义定义与核心对象

### 定义对象

`XRobots` 把机器人行为写成 `Behavior`。每个 behavior 对应 HSM 里的一个状态，但又不只是状态，因为它还带参数列表、局部声明、entry/exit 代码以及可以跳向目标 behavior 的 transition block。

### 核心抽象

根据论文给出的语言结构，可保守整理为：

$$
X = (B, b_0, child, \Pi, Entry, Tr, Exit)
$$

上式中的符号逐项解释如下：

1. `B` 是全部 behaviors 的集合。
2. `b_0 \in B` 是根 behavior。
3. `child \subseteq B \times B` 是 behavior 间的嵌套层次关系。
4. `\Pi(b)` 是 behavior `b` 的参数与局部声明。
5. `Entry(b)` 是进入 `b` 时执行的语句块。
6. `Tr(b)` 是 transition block。
7. `Exit(b)` 是退出 `b` 时执行的语句块。

论文直接把一个 behavior 写成：

$$
b = (name, params, decls, entry, trans, exit)
$$

其中：

1. `name` 是 behavior 名称。
2. `params` 是形式参数列表，可含 primitive type 和 behavior type。
3. `decls` 是局部变量或 sub-behavior 声明。
4. `entry` 是进入 behavior 时执行的代码块。
5. `trans` 是一组“条件 -> 目标 behavior”的迁移规则。
6. `exit` 是退出 behavior 时执行的代码块。

论文还给出了 active behavior 的 stack 语义。可将运行配置压成：

$$
c = (stack, env)
$$

其中：

1. `stack` 是当前 active behaviors 的栈。
2. `env` 是变量、传感器、执行器值与 behavior 参数环境。

### 一个最小例子与通俗解释

论文图 1 的 `driveStraightFor(duration)` 是最直接的最小例子：

1. 进入 `driveStraightFor` 时，把左右轮速度 `rVel`、`lVel` 设为 `200.0`。
2. 计算 `newDuration = duration - 5.0`。
3. 若 `duration > 0`，则 `Apply Behavior driveStraightFor(newDuration)`，继续递归前进。
4. 若 `duration <= 0`，则跳转到 `Stop()`。
5. 退出时把左右轮速度清零。

通俗地说，`XRobots` 让“前进一段时间”“避障”“画方形”“画三角形”这些行为都变成可调用的组件。更特别的是，下一步该跳去哪个行为，也可以当作参数传进去，所以行为组合不是写死的。

### 运行 / 接受 / 转移语义

论文明确说明 active behavior 按 first-in-last-out 顺序维护，因此进入 / 退出行为可保守写成：

$$
stack' = stack \cdot b_t
$$

表示进入目标 behavior `b_t` 时把它压栈；退出时则从栈顶弹出。更关键的 transition 规则是：

$$
\text{if } cond_i = true,\ \text{choose first enabled transition } (cond_i \rightarrow b_t)
$$

并按当前 behavior 与目标 behavior 的最低公共祖先更新栈：

$$
stack' = pop_{\mathrm{lca}(b_c, b_t)}(stack) \cdot b_t
$$

上式中的符号逐项解释如下：

1. `b_c` 是当前 behavior。
2. `b_t` 是目标 behavior。
3. `\mathrm{lca}(b_c, b_t)` 是两者在层次结构中的最低公共祖先。
4. `pop_{\mathrm{lca}}(stack)` 表示把当前 active stack 中位于公共祖先以下的 behaviors 依次退出。
5. 随后把目标 behavior 压入栈，并执行其 `entry` 代码。

论文对 by-reference / by-value behavior 也给出了不同语义：

$$
\mathrm{ByRef}(b) \Rightarrow target = ref(b)
$$

$$
\mathrm{ByVal}(b) \Rightarrow target = instantiate(b)
$$

其中：

1. `ByRef` 保留目标 behavior 在原 HSM 中的静态位置。
2. `ByVal` 会把传入 behavior 的“值”动态实例化成被调用 behavior 的新 sub-behavior。

### 语义边界

`XRobots` 的边界很清楚：

1. 它是行为 DSL，不是 planner 或硬实时执行内核。
2. 它强调行为参数化和复用，不强调并发语义。
3. 它依赖传感器 / 执行器变量和外部运行环境，原文没有定义独立交换格式。
4. 论文自己承认 formal semantics 与稳定 compiler 仍是未来工作。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 行为骨架 | `$b = (name, params, decls, entry, trans, exit)$` | `Behavior` 是 XRobots 的基本单元。 |
| 运行配置 | `$c = (stack, env)$` | 活动行为以栈形式维护。 |
| 层次切换 | `$stack' = pop_{\mathrm{lca}(b_c, b_t)}(stack) \cdot b_t$` | transition 会沿 HSM 层次退出并进入目标 behavior。 |
| 参数化行为 | `$\mathrm{ByRef}(b) \Rightarrow target = ref(b),\ \mathrm{ByVal}(b) \Rightarrow target = instantiate(b)$` | behavior 既可按引用，也可按值传递。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | behavior 就是核心状态 / 行为抽象。 |
| 事件 / 触发 | 支持 | 通过 transition condition 对传感器与变量变化做反应。 |
| 守卫 / 数据 | 强支持 | transition 带 Boolean 条件，entry / exit 可读写变量、传感器和执行器。 |
| 层次 | 强支持 | behaviors 可嵌套，active stack 体现层次执行。 |
| 并发 / 同步 | 不支持 | 原文未给并发状态或同步语义。 |
| 时间约束 | 部分支持 | 可通过参数和变量实现计数 / duration 逻辑，但不是显式时间自动机。 |
| 连续动态 / 随机性 | 不支持 | 连续控制下沉到执行器更新。 |
| 可执行 / 可验证性 | 部分支持 | prototype 语言已可描述行为，但 formal semantics 与稳定 compiler 仍在后续工作。 |

### 形式化问题与性质

1. `XRobots` 最核心的增量是把 behavior 变成 first-class entity。
2. by-value behavior passing 会引入“祖先变量失活后不可访问”的静态 / 动态错误问题。
3. 由于 transition 只选择第一个满足条件的规则，行为顺序本身具有语义意义。
4. 它很适合表达机器人“行为树式思考”，但仍保留 HSM 的 entry / exit 纪律。

## 构造方式与承载格式

### 建模入口

建模入口就是 `Behavior` 语言本身：

1. `Behavior name(params) { ... }`
2. `Entry { ... }`
3. `Under Condition ... Apply Behavior ...`
4. `Exit { ... }`

### 机器可处理承载方式

机器可处理承载是 `XRobots` 的文本 DSL。原文没有给 XML/JSON，但明确说明语言会编译为可执行结果，compiler 是后续工作的中心。

### 交换与互操作

`XRobots` 的互操作主要体现在行为代码对传感器 / 执行器变量的访问，以及 prototype compiler 将 DSL 下沉到机器人程序。它不是交换标准，更像面向机器人行为编程的专用前端。

## 配套基础设施

- 建模/编辑工具：原文聚焦语言本体，没有给成熟图形编辑器。
- 解析/交换/元模型支持：prototype compiler 在文中被明确列为后续工作重点。
- 仿真/执行支持：entry / exit block 和 transition 规则直接面向机器人运行。
- 验证/分析支持：原文承认 formal semantics 仍待补齐。
- 代码生成/转换支持：编译器是论文明确提出的后续方向。
- 标准化或社区生态：更接近研究型语言原型，生态较弱。

## 适用场景与需求前提

### 适用场景

适合移动机器人中“避障、直行、画形状、跟墙”等可拆成行为组件并需要高复用的场景。

### 需求前提

1. 行为可自然分解为有限个嵌套 HSM state / behavior。
2. 行为之间需要通过参数传递配置或下一步策略。
3. 运行环境能提供传感器和执行器变量访问。
4. 更关注行为模块化与复用，而不是复杂并发。

### 不适用或高成本场景

若系统需要严格并发协调、复杂时间约束或成熟工业工具链，`XRobots` 当前形态就偏弱；若团队不熟悉高阶行为参数化，也会有学习成本。

## 与相邻形式主义的关系

相对普通 `Statecharts`，它把 behavior 参数化并提升为 first-class object；相对纯 imperative robot code，它更接近问题域中的“行为”组织方式；相对行为树，它保留了 HSM 的嵌套与 entry / exit 纪律。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：领域特化状态机语言可以不只是“换个图形”，还可以改变状态机基本构件的抽象层级，比如把 behavior 本身变成可传递对象。

### 作为目标形式主义还是中间表示

对移动机器人行为编程，它可以直接作为目标语言；在更一般的流程中，也可作为从抽象任务到机器人行为脚本之间的中间表示。

### 对需求到模型生成的启发

1. 需求中的“下一步行为”本身有时也是一等对象。
2. 行为复用不一定靠继承或复制，参数化行为是一条可行路径。
3. 若要支持高阶组合，静态作用域与变量可见性必须提前设计好。

## 重要的相关工作

- `Statecharts` 与 HSM：提供了 `XRobots` 的直接形式主义根基。
- 机器人 DSL / middleware 语言：论文专门把 reactive、imperative、middleware-based 语言作为比较背景。
- `XABSL` 一类机器人行为语言：与 `XRobots` 一样，都试图把“行为”抬升为显式编程对象。

## 文献分类总结

- 这是一篇 `📦` 类领域 DSL 条目，重点在“如何把机器人行为状态机变成一门可参数化、可组合的语言”。
- 其描述客体是机器人控制 / 反应式行为，因此记为 `🎛️`；领域落在移动机器人，因此记为 `🌡️`。
- 对 `project_1` 来说，它提供了一个很值得记录的专用模型分支：`HSM + first-class behavior`。

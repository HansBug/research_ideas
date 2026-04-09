# 面向模块化机器人控制的快速状态机装配 / Rapid state machine assembly for modular robot control using meta-scripting, templating and code generation

## 基本信息

- 标题：Rapid state machine assembly for modular robot control using meta-scripting, templating and code generation
- 中文标题：面向模块化机器人控制的快速状态机装配
- 作者：Barry Ridge, Timotej Gašpar, Aleš Ude
- 发表：*2017 IEEE-RAS 17th International Conference on Humanoid Robotics (Humanoids)*, pp. 661-668, 2017
- DOI：`10.1109/HUMANOIDS.2017.8246943`
- 链接：https://doi.org/10.1109/HUMANOIDS.2017.8246943
- 形式主义：`SMACHA / SMACH`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：状态机代码生成 / `ROS` 任务控制工具链
- 工具/实现获取方式：原文明确给出 `SMACHA` GitHub 仓库、`Baxter SMACHA` package、生成代码视频和 `SMACH` / `FlexBE` 相关工具入口。
- 标准/格式获取方式：承载方式是 `YAML` meta-scripts、`Jinja2` templates 与生成的 Python `SMACH` code；原文未给独立标准交换格式。

## 简报

这篇论文解决的不是“状态机语义不清楚”，而是另一个很现实的问题：`SMACH` 很强，但写起来太啰嗦，样板代码多，复用差。`SMACHA` 的做法不是再发明一套新运行时，而是在 `SMACH` 之上加一层 `meta-scripting + templating + code generation`，把高层任务结构写成简洁 `YAML`，再递归生成真正可运行的 `SMACH` Python 状态机。

- 形式主义定位：面向 `ROS` 任务控制的状态机装配基础设施，而不是新的运行时状态机语义。
- 构造方式简述：以 `YAML` 脚本描述 state hierarchy，再由 parser / templater / generator 递归渲染 `SMACH` container、leaf state 和 sub-script。
- 基础设施与场景简述：依托 `SMACHA` API、`Jinja2` templates、`SMACH` runtime、Baxter simulator / Gazebo / ROS 服务与 action，服务 pick-and-place、stacking、dual-arm stacking 等任务。

```text
任务控制需求 -> YAML meta-script + templates -> recursive code generation -> Python SMACH state machine -> ROS / Gazebo / Baxter execution
```

## 形式主义定义与核心对象

### 定义对象

`SMACHA` 的真正对象不是“单个运行时状态机定义”，而是“如何把状态机脚本化并自动装配成 `SMACH` 代码”。它把一个任务控制程序拆成：

1. script：描述 state hierarchy 的 `YAML`。
2. templates：定义各类 state / container 的代码骨架。
3. parser / templater / generator：把脚本递归转成可执行 `SMACH` 代码。

### 核心抽象

由于论文本身侧重基础设施而非数学定义，这里根据其 parser-templater-generator 结构做保守整理：

$$
H = (N, n_0, \kappa, \tau, \chi, \upsilon)
$$

上式中的符号逐项解释如下：

1. `N` 是脚本中的 state 节点集合。
2. `n_0 \in N` 是根 state machine / base template 节点。
3. `\kappa : N \to \{\mathrm{container}, \mathrm{leaf}, \mathrm{subscript}\}` 给出节点类型。
4. `\tau : N \to Templates` 把节点映射到模板名。
5. `\chi \subseteq N \times N` 是父子层次关系。
6. `\upsilon(n)` 是节点附带的参数、userdata remapping、transitions 等脚本变量。

`SMACHA` 的生成语义可压成：

$$
\mathrm{Gen}(n) = \mathrm{render}(\tau(n), \upsilon(n), \{\mathrm{Gen}(c) \mid c \in child(n)\})
$$

其中：

1. `\mathrm{Gen}(n)` 是节点 `n` 生成出的代码片段。
2. `\mathrm{render}` 表示模板渲染。
3. `\tau(n)` 是选中的 template。
4. `\upsilon(n)` 是传给模板的脚本变量。
5. `child(n)` 是 `n` 的子状态或子脚本。

对 sub-script state，论文的语义是先解析外部脚本，再递归拼接。因此可保守写成：

$$
\kappa(n)=\mathrm{subscript} \Rightarrow \mathrm{Gen}(n)=\mathrm{Gen}(\mathrm{Parse}(script(n)))
$$

这说明 `SMACHA` 的核心是“递归展开”和“模板继承”，而不是解释执行一个新 DSL。

### 一个最小例子与通俗解释

论文最直接的最小例子是 Baxter pick-and-place：

1. 根脚本先加载 table / block model，并移动 Baxter 到起始位。
2. 进入 `PICK_BLOCK` container state。
3. 该状态内部又展开成 hover pose、move、open gripper、下降、close gripper、返回 hover 等一串子状态。
4. 接着进入 `PLACE_BLOCK`，以同样方式展开放置流程。
5. 最终这些 `YAML` 和 sub-script 自动生成 Python `SMACH` 代码并直接运行。

通俗地说，`SMACHA` 让你不必手工把每个 `smach.StateMachine.add(...)` 都写出来，而是像拼配置一样描述“这里是一个 container，下面套两个子脚本，每个子脚本用哪个模板”，剩下的让代码生成器做。

### 运行 / 接受 / 转移语义

`SMACHA` 本身不重新定义 `SMACH` 运行时，而是生成 `SMACH` 代码。因此其关键语义在“生成”，不在“解释”。不过底层生成目标仍是层次状态机，可保守写成：

$$
T(s, o) = s'
$$

上式中的符号逐项解释如下：

1. `s` 是当前 `SMACH` state。
2. `o` 是该 state 返回的 outcome。
3. `T(s,o)=s'` 表示 outcome 决定下一 state。
4. `SMACHA` 的工作是把这一控制流关系自动渲染成 Python `SMACH` 代码。

其最核心的递归处理规则是：

1. `leaf state` 直接走 `RenderLeaf`。
2. `container state` 先递归处理子节点，再走 `RenderContainer`。
3. `sub-script state` 先 `Parse(script(n))`，再继续递归处理。

这正是论文对 code generator 的核心描述。

### 语义边界

`SMACHA` 的边界很清楚：

1. 它不是新的状态机运行时，底层仍是 `SMACH`。
2. 它强调装配、复用和生成，不强调新的验证语义。
3. 其表达能力受目标模板与 `SMACH` API 限制。
4. 如果模板设计很差，生成代码仍可能臃肿或难维护。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 脚本骨架 | `$H = (N, n_0, \kappa, \tau, \chi, \upsilon)$` | `SMACHA` 的对象是 state-machine assembly graph。 |
| 模板渲染 | `$\mathrm{Gen}(n)=\mathrm{render}(\tau(n),\upsilon(n),\{\mathrm{Gen}(c)\})$` | 节点代码由模板和子节点递归生成。 |
| sub-script 递归 | `$\kappa(n)=\mathrm{subscript}\Rightarrow \mathrm{Gen}(n)=\mathrm{Gen}(\mathrm{Parse}(script(n)))$` | 脚本可嵌套复用。 |
| outcome 控制流 | `$T(s,o)=s'$` | 生成目标仍是传统层次状态机控制流。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 底层生成的是完整 `SMACH` state machine。 |
| 事件 / 触发 | 支持 | 通过 outcomes 与 `SMACH` states 驱动。 |
| 守卫 / 数据 | 强支持 | userdata remapping、ROS 服务 / action 参数都能进入模板。 |
| 层次 | 强支持 | container states 与 sub-scripts 天然支持嵌套。 |
| 并发 / 同步 | 支持 | 核心模板包含 `Concurrence` container。 |
| 时间约束 | 弱支持 | 时间逻辑不是语言内建语义，需要状态模板自行实现。 |
| 连续动态 / 随机性 | 不支持 | 连续控制留给外部 ROS 节点与机器人接口。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 生成代码可直接运行；形式验证不是主线。 |

### 形式化问题与性质

1. `SMACHA` 通过脚本化降低了 `SMACH` 的样板代码成本，但不改变其运行时本质。
2. 模板继承和 sub-script 复用是它最关键的可维护性来源。
3. 因为生成后仍是普通 Python `SMACH` 代码，所以与现有生态兼容性很好。
4. 它特别适合“状态机结构稳定、但重复装配很多”的机器人任务。

## 构造方式与承载格式

### 建模入口

建模入口主要有三类：

1. 编写 `YAML` 脚本描述状态机层次。
2. 为特定任务或平台编写 `Jinja2` templates。
3. 使用 sub-scripts 把可复用状态机片段模块化。

### 机器可处理承载方式

机器可处理承载包括：

1. `YAML` script。
2. `Jinja2` template。
3. 生成的 Python `SMACH` code。

### 交换与互操作

`SMACHA` 没有行业交换标准；它的互操作点在于：

1. 生成结果仍是标准 `SMACH` Python 程序。
2. 模板可针对不同视觉编程系统或后端定制。
3. 与 ROS service、action、Gazebo/Baxter SDK 自然集成。

## 配套基础设施

- 建模/编辑工具：脚本编辑器、模板系统，论文未强调专用 GUI。
- 解析/交换/元模型支持：parser、templater、generator 三段式 API。
- 仿真/执行支持：Baxter simulator、Gazebo、ROS interfaces、生成后的 `SMACH` runtime。
- 验证/分析支持：主要依赖 `SMACH` / ROS 运行时观察，论文未提供 formal verification。
- 代码生成/转换支持：这是论文主贡献，支持 core templates、custom templates、sub-scripts。
- 标准化或社区生态：强依赖 `ROS`/`SMACH` 生态，自身是研究型代码生成工具。

## 适用场景与需求前提

### 适用场景

适合 `ROS` 任务控制、工业或实验室机器人 pick-and-place、stacking、双臂协同等需要快速装配大量相似状态机的场景。

### 需求前提

1. 团队已经接受 `SMACH` 作为底层控制流框架。
2. 任务结构可整理成层次 container / leaf / sub-script。
3. 主要重复成本来自模板化装配，而不是状态机语义本身。
4. 愿意维护模板库和脚本库。

### 不适用或高成本场景

若团队并不使用 `SMACH`，或任务语义更适合行为树、规划器或形式验证 DSL，`SMACHA` 的收益就会下降；若模板体系缺乏治理，反而会引入新的复杂度。

## 与相邻形式主义的关系

相对 `SMACH`，它是更高一层的装配语言；相对 `FlexBE`，它更强调模板和代码生成而不是 GUI；相对 `RAFCON`、`YASMIN`，它没有自建新 runtime，而是复用现有 `SMACH` 生态。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文提醒我们：需求到状态机自动化不一定非得直接输出“最终 DSL”，也可以先输出模板化装配脚本，再由工具生成执行状态机。

### 作为目标形式主义还是中间表示

它更适合作为中间表示或工程落地工具，而不是最终统一形式主义。

### 对需求到模型生成的启发

1. 高频重复状态机结构很适合模板化生成。
2. 生成前的脚本层表达可以比运行时模型更短、更适合自动生成。
3. 模板库本身也是形式主义基础设施的一部分。

## 重要的相关工作

- `SMACH`：是其直接目标运行时。
- `FlexBE`：是论文明确比较的可视化代码生成方案。
- `RAFCON`、`YASMIN`：与其一样面向机器人任务控制，但基础设施策略不同。

## 文献分类总结

- 这是一篇 `📦` 类工具链条目，重点在状态机装配、模板化和代码生成，而不是新语义本体。
- 其描述客体是机器人任务控制逻辑，因此记为 `🎛️`；领域落在 `ROS` 机器人系统，因此记为 `🌡️`。
- 对 `project_1` 来说，它补了“自动生成状态机代码骨架”这一条非常实用的工程化支线。

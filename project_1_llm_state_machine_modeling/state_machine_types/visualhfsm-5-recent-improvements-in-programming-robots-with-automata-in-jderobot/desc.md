# VisualHFSM 5：在 JdeRobot 中用自动机编程机器人的改进版 / VisualHFSM 5: recent improvements in programming robots with automata in JdeRobot

## 基本信息

- 标题：VisualHFSM 5: recent improvements in programming robots with automata in JdeRobot
- 中文标题：VisualHFSM 5：在 JdeRobot 中用自动机编程机器人的改进版
- 作者：Samuel Rey, José M. Cañas
- 发表：*Proceedings of the XVII Workshop of Physical Agents (WAF 2016)*, Málaga, Spain, 2016
- DOI：原文未提供
- 链接：https://gsyc.urjc.es/jmplaza/papers/waf2016-visualhfsm.pdf
- 形式主义：`VisualHFSM / JdeRobot`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：可视化层次状态机工具 / 代码生成器
- 工具/实现获取方式：原文明确说明 `VisualHFSM` 是 `JdeRobot` 框架中的 visual programming tool，可生成 C++ 或 Python `JdeRobot` 组件，并自带 runtime GUI。
- 标准/格式获取方式：承载方式是图形化 `HFSM` 编辑器、内部保存的 XML 文件、自动生成的 C++/Python 代码与配置文件；原文未给通用行业交换标准。

## 简报

`VisualHFSM` 的核心价值不是又发明一种新的机器人状态机语义，而是把 `HFSM` 变成一套真正能用的可视化开发链：开发者在画布上放 states 和 transitions，把每个 state/transition 的代码片段填进去，工具把整张层次状态机保存成 XML，再自动生成 `JdeRobot` 组件和运行时 GUI。这样一来，机器人行为开发从“手写大量框架胶水代码”变成“图形组织 + 少量局部代码”。

- 形式主义定位：面向机器人行为编程的 `HFSM` 可视化建模与代码生成载体，而不是新的理论自动机家族。
- 构造方式简述：用图形编辑器创建层次状态、转移、守卫和状态代码，保存为 XML，再生成 C++ 或 Python `JdeRobot` 组件。
- 基础设施与场景简述：依托 graphical editor、automatic code generator、runtime GUI、多线程模板与 `JdeRobot` 组件框架，服务移动机器人和无人机行为编程。

```text
机器人行为需求 -> VisualHFSM canvas + XML -> C++/Python JdeRobot component -> runtime GUI + drivers -> 执行 / 调试
```

## 形式主义定义与核心对象

### 定义对象

这篇论文描述的核心对象包括：

1. state：图形化行为节点，可包含具体执行代码。
2. transition：在状态间切换的条件和可选执行代码。
3. subautomaton：嵌套在状态内部的层次状态机。
4. XML model：图形编辑器保存的机器可处理表示。
5. generated component：自动生成的 `JdeRobot` C++/Python 组件。

### 核心抽象

原文没有给出显式数学定义，这里根据其“hierarchical finite state machine + XML + code generator”结构，保守整理 `VisualHFSM` 模型为：

$$
V = (S, s_0, T, H, X, \lambda, \gamma)
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `s_0 \in S` 是初始状态。
3. `T \subseteq S \times G \times S` 是转移集合，`G` 表示转移条件空间。
4. `H` 是层次关系，表示 state 与 subautomaton 的嵌套。
5. `X` 是 XML 持久化表示。
6. `\lambda : S \to Code` 给出每个状态对应的执行代码。
7. `\gamma : T \to Code` 给出每个转移对应的条件与转移代码。

代码生成过程可压缩成：

$$
\mathrm{Gen}(X) = \mathrm{Comp}_{\mathrm{lang}}(V)
$$

其中：

1. `X` 是图形编辑器导出的 XML。
2. `\mathrm{lang} \in \{\mathrm{C++}, \mathrm{Python}\}` 是目标语言。
3. `\mathrm{Comp}_{\mathrm{lang}}(V)` 是生成的 `JdeRobot` 组件。

### 一个最小例子与通俗解释

论文给出的最小直觉非常直接：

1. 在画布上画出状态和转移。
2. 给每个 state 填入将要执行的代码。
3. 给每条 transition 填入发生条件和转移代码。
4. 若某个 state 需要更细粒度行为，就双击进入其 subautomaton。
5. 工具自动生成真正可运行的 `JdeRobot` 组件，并在运行时用 GUI 标出当前 active states。

通俗地说，`VisualHFSM` 像“给机器人行为编程配了一张能出代码的状态机白板”：你主要在图上搭结构，真正要自己写的只剩每个状态里那一点局部逻辑。

### 运行 / 接受 / 转移语义

论文强调生成后的组件把每个 subautomaton 实现为单独线程，因此其执行可保守写成：

$$
(s, \sigma) \xrightarrow{} (s', \sigma') \iff \exists\, (s, g, s') \in T,\ g(\sigma)=\mathrm{true}
$$

上式中的符号逐项解释如下：

1. `s`、`s'` 是当前状态与后继状态。
2. `\sigma`、`\sigma'` 是程序变量与传感器/执行器相关环境。
3. `g` 是转移条件。
4. 当 `g(\sigma)` 成立时，当前活动状态切换到 `s'`。

对层次状态机，论文明确说 generated component 是“a collection of concurrent threads”，因此可保守整理为：

$$
\mathrm{Run}(V) = \parallel_{h \in H} \mathrm{Thread}(h)
$$

其中：

1. `H` 中每个层次子自动机 `h` 都对应一个线程。
2. `\mathrm{Thread}(h)` 负责该 subautomaton 的活动状态推进与 GUI 更新。
3. 这解释了为什么运行时 GUI 能同时显示多层 active states。

### 语义边界

`VisualHFSM` 的边界也很清楚：

1. 它关注的是视觉化编程、自动生成和调试，不提供 formal verification。
2. 它依赖用户填写状态和转移代码，本体并不替代底层算法。
3. 时间约束不是其原生语义重点，更多通过程序逻辑和外部组件处理。
4. 它更像行为开发工厂，而不是严格的行为数学理论。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$V = (S, s_0, T, H, X, \lambda, \gamma)$` | 图形层次状态机、XML 和代码片段共同定义行为模型。 |
| 代码生成 | `$\mathrm{Gen}(X)=\mathrm{Comp}_{\mathrm{lang}}(V)$` | 工具把 XML 直接翻成目标语言组件。 |
| 条件转移 | `$(s,\sigma)\xrightarrow{}(s',\sigma')$` | 行为推进由转移条件而非外部调度脚本控制。 |
| 层次并发执行 | `$\mathrm{Run}(V)=\parallel_{h \in H}\mathrm{Thread}(h)$` | 子自动机被实现为并发线程。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 以层次有限状态机为核心。 |
| 事件 / 触发 | 支持 | 通过 transition 条件和程序代码控制切换。 |
| 守卫 / 数据 | 强支持 | 状态和转移都可嵌入代码，Variables 菜单支持变量/函数。 |
| 层次 | 强支持 | 支持 subautomata、Tree View 与 Schema View 双视图。 |
| 并发 / 同步 | 支持 | 每个 subautomaton 可映射为线程。 |
| 时间约束 | 弱支持 | 没有专门时钟语义，时间更多依赖状态代码和外部组件。 |
| 连续动态 / 随机性 | 不支持 | 连续控制留给外部驱动与机器人组件。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 自动生成组件、runtime GUI 很强；formal verification 未覆盖。 |

### 形式化问题与性质

1. `VisualHFSM` 最重要的工程价值是把 `HFSM` 变成了 XML + codegen + runtime GUI 的完整链路。
2. 它允许开发者只写状态内和转移上的局部代码，而把组件骨架和线程结构交给模板生成。
3. Python 支持说明其目标不仅是高性能部署，也包含快速迭代和原型开发。
4. runtime GUI 与 autofocus 机制使其天然适合调试复杂行为。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 在 graphical editor 中创建 states 和 transitions。
2. 在 state/transition 上填写实际执行代码和条件。
3. 用 Tree View 和 Schema View 组织层次结构。
4. 用 Variables、Functions、Config 菜单补足运行所需元信息。

### 机器可处理承载方式

原文明确给出的承载方式包括：

1. 图形编辑器内部结构。
2. XML 文件。
3. 自动生成的 C++ `JdeRobot` 组件。
4. 自动生成的 Python `JdeRobot` 组件。
5. 自动生成的配置文件。

### 交换与互操作

互操作重点在：

1. 输出直接是 `JdeRobot` 组件，可连接具体驱动。
2. 生成组件支持 C++ 和 Python 两条语言链。
3. 可为 Pioneer、Kobuki、Nao、ArDrone 等机器人及 Gazebo 仿真接入行为控制。

## 配套基础设施

- 建模/编辑工具：`VisualHFSM` graphical editor，含 Tree View、Schema View、弹窗编辑与菜单系统。
- 解析/交换/元模型支持：XML 持久化、配置文件生成、附加库声明。
- 仿真/执行支持：生成的 `JdeRobot` 组件可直接运行于真实机器人或仿真环境。
- 验证/分析支持：runtime GUI、active state 可视化和 autofocus 用于调试；formal verification 未见。
- 代码生成/转换支持：支持 C++ 与 Python 两条生成链，且 C++ 生成后可由工具直接编译。
- 标准化或社区生态：依托 `JdeRobot`，属于框架内稳定工具，但未形成独立行业标准。

## 适用场景与需求前提

### 适用场景

适合需要快速开发层次行为逻辑、希望图形化组织复杂任务、并且愿意让工具生成组件骨架的移动机器人和无人机应用。

### 需求前提

1. 行为逻辑可以自然拆成 `HFSM`。
2. 团队愿意在 state/transition 中填入少量代码片段。
3. 系统已经使用或接受 `JdeRobot` 组件式架构。
4. 需要运行时可视化调试。

### 不适用或高成本场景

若团队需要强形式验证、跨平台标准交换格式或与非 `JdeRobot` 生态深度解耦，`VisualHFSM` 的收益会下降；它更适合作为框架内高效开发工具。

## 与相邻形式主义的关系

相对 `SMACH`，它是可视化工具而不是纯代码库；相对 `MissionLab/CfgEdit`，它也走图形状态机路线，但输出是 `JdeRobot` 组件和 XML；相对 `XABSL`，它更强调图形建模和自动生成，而不是专用文本行为语言。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文给了一个很实在的信号：即便没有极强形式语义，专用状态机载体只要把图形建模、持久化格式、代码生成和运行时可视化做全，仍然能成为机器人行为工程里的稳定基础设施。

### 作为目标形式主义还是中间表示

它更适合作为工程化目标载体，而不是抽象中间表示；其价值主要体现在“需求到图形状态机，再到可运行组件”的落地链路。

### 对需求到模型生成的启发

1. 图形状态机如果要真正落地，最好有明确的机器可处理中间格式，如 XML。
2. 自动生成出来的不只是业务代码，还应包含配置、线程骨架和调试界面入口。
3. 对机器人任务状态机，运行时 active-state 可视化本身就是重要基础设施。

## 重要的相关工作

- `SMACH`：论文明确拿来比较，指出其是代码式而非可视化工具。
- `MissionLab / CDL`：是更早的图形化任务状态机路线。
- `XABSL`、`ThinkingCap`、`Vicode`：都属于机器人行为状态机工具谱系中的邻近方案。

## 文献分类总结

- 这是一篇 `📦` 类工具链条目，重点在 `HFSM` 的图形编辑、XML 承载、代码生成与 runtime GUI。
- 其描述客体是机器人行为控制逻辑，因此记为 `🎛️`；论文落在机器人系统开发语境，因此记为 `🌡️`。
- 对 `project_1` 来说，它补的是“状态机如何以图形工具 + 中间格式 + 代码生成器的方式稳定落地”的工程证据。

# HyTech：混成系统模型检查器 / HYTECH: A Model Checker for Hybrid Systems

## 基本信息

- 标题：HYTECH: A Model Checker for Hybrid Systems
- 中文标题：HyTech：混成系统模型检查器
- 作者：Thomas A. Henzinger，Pei-Hsin Ho，Howard Wong-Toi
- 发表：University of California, Berkeley, Electronics Research Laboratory Memorandum No. UCB/ERL M97/79，1997
- DOI：原报告版未提供；对应正式论文 DOI 为 `10.1007/s100090050008`
- 链接：https://www2.eecs.berkeley.edu/Pubs/TechRpts/1997/ERL-97-79.pdf
- 形式主义：`Linear Hybrid Automata / HyTech`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：混成自动机模型检查器 / parametric-analysis tool
- 工具/实现获取方式：原文明确给出 `HyTech` home page，包含 source code、executables、online demo、user guide 与 graphical front end。
- 标准/格式获取方式：承载方式是 linear hybrid automata 的文本输入文件加 analysis-command 脚本语言；原文未提供独立于 `HyTech` 的中立交换格式。

## 简报

这篇论文的核心贡献，是第一次把 `linear hybrid automata` 真正做成可自动验证、可参数分析、还能回给你错误轨迹的工具。`HyTech` 不是简单的 “hybrid automata parser”，而是围绕 `state assertion`、`Post`、reachability、parametric analysis、clock translation 和 polyhedral operations 组织的一条完整分析母线。

- 形式主义定位：`Linear Hybrid Automata` 的经典模型检查与参数分析工具，而不是新的混成自动机理论。
- 构造方式简述：先写一组 linear hybrid automata，再配 analysis commands 脚本，用 `Post`、布尔运算、存在量化和 reachability macros 做验证。
- 基础设施与场景简述：依托 textual model、state assertions、polyhedral library、error traces 和 parametric analysis，服务控制器、协议、机器人、汽车底盘和蒸汽锅炉等混成系统。

```text
hybrid system model -> linear hybrid automata + analysis script -> Post / reachability / parametric analysis -> safe region or counterexample trace
```

## 形式主义定义与核心对象

### 定义对象

论文直接把 `HyTech` 所处理的对象固定为 `hybrid automaton`，其主要构件包括：

1. real-valued variables。
2. control modes。
3. flow conditions。
4. invariant conditions。
5. initial conditions。
6. control switches、jump conditions 与 synchronizing events。

### 核心抽象

原文直接给出了混成自动机的骨架，可写成：

$$
A = (X, V, flow, inv, init, E, jump, \Sigma, syn)
$$

上式中的符号逐项解释如下：

1. `X` 是实值变量集合。
2. `V` 是 control modes 集合。
3. `flow` 为每个 mode 指派微分约束。
4. `inv` 为每个 mode 指派 invariant。
5. `init` 为每个 mode 指派初始条件。
6. `E` 是 control switches 集合。
7. `jump` 为每个 switch 指派 jump relation。
8. `\Sigma` 是 events 集合。
9. `syn` 为每个 switch 指派同步事件。

工具层最关键的抽象不是单个 run，而是 `state assertion` 与后继算子：

$$
Post(\varphi)
$$

上式中的符号逐项解释如下：

1. `\varphi` 是 state assertion，即一类描述状态集的线性谓词。
2. `Post(\varphi)` 表示所有 jump successors 与 flow successors 组成的后继状态集。
3. `HyTech` 的 reachability、parametric analysis 和 error-trace 生成都围绕这个算子组织。

### 一个最小例子与通俗解释

论文贯穿全文使用 thermostat：

1. mode `on` 时温度按一条线性微分规律上升。
2. mode `off` 时温度按另一条线性微分规律下降。
3. 当 `x = 3` 时必须关掉加热器；当 `x = 1` 时必须重新打开。
4. `HyTech` 不只回答“会不会越界”，还能回答“参数 alpha 取什么值才安全”。

通俗地说，`HyTech` 像“会算多面体的混成状态机验证器”：你给它离散模式、线性微分和跳转条件，它就去算哪些状态可达、哪些参数安全、哪里会出错。

### 运行 / 接受 / 转移语义

论文把一个 admissible state 写成：

$$
q = (v, a)
$$

上式中的符号逐项解释如下：

1. `v` 是当前 control mode。
2. `a` 是变量取值向量。
3. 若 `inv(v)` 在 `a` 下成立，则 `q` 是 admissible。

对 reachability，工具隐含地迭代：

$$
reach_0 = init,\quad reach_{i+1} = reach_i \lor Post(reach_i)
$$

上式中的符号逐项解释如下：

1. `init` 是初始状态断言。
2. `reach_i` 是第 `i` 轮迭代得到的可达状态断言。
3. `Post(reach_i)` 计算所有一步 flow / jump 后继。
4. 当 `reach_{i+1}` 与 `reach_i` 等价时即可得到不动点。

论文还强调 `HyTech` 的强项是 parametric analysis：它不仅判断可达，还能求出使性质成立的参数区域。

### 语义边界

这篇论文的边界也很清楚：

1. `HyTech` 针对的是 `linear hybrid automata`，不是任意 nonlinear hybrid system。
2. 很多系统需要先做 clock translation 或 linear phase-portrait approximation 才能交给工具。
3. 若问题复杂度主要来自连续非线性而非离散-连续耦合，`HyTech` 不是最佳选择。
4. 针对主要是 clocks 的系统，文中明确建议优先用 `Kronos / Uppaal` 这类专用 timed-automata 工具。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 混成自动机骨架 | `$A = (X, V, flow, inv, init, E, jump, \Sigma, syn)$` | 固定 `HyTech` 的输入模型。 |
| admissible state | `$q = (v, a)$` | mode 与连续变量赋值共同定义状态。 |
| 后继算子 | `$Post(\varphi)$` | reachability 和 parametric analysis 的核心原语。 |
| 可达不动点 | `$reach_{i+1} = reach_i \lor Post(reach_i)$` | 工具通过迭代 state assertions 求可达集。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | control modes 是离散骨架。 |
| 事件 / 触发 | 支持 | control switches 与 synchronizing events 明确存在。 |
| 守卫 / 数据 | 很强 | jump conditions、state assertions 与参数都显式进入分析。 |
| 层次 | 弱支持 | 工具主线不是层次状态机。 |
| 并发 / 同步 | 部分支持 | 通过 automata collection composition 与同步事件处理。 |
| 时间约束 | 很强 | 时间是连续变量的一部分。 |
| 连续动态 / 随机性 | 强连续 / 不随机 | 支持线性连续动态，不涉及概率。 |
| 可执行 / 可验证性 | 很强 | state-space exploration、parametric analysis、error traces 全都有。 |

### 形式化问题与性质

1. `HyTech` 最重要的不是某个 UI，而是把 `state assertion + Post` 组织成可编程分析语言。
2. 它把“验证”与“参数综合”放在同一工具里，这在今天看仍然很超前。
3. clock translation 和 linear approximation 说明工具路线本身就是“模型收束 + 求解”的早期范式。

## 构造方式与承载格式

### 建模入口

原文的典型入口是：

1. 文本描述一组 linear hybrid automata。
2. 再写 analysis commands 脚本。
3. 用内建 macro 做 `reachforward`、parametric analysis、conservative approximation 或 error-trace generation。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `HyTech` input file。
2. 线性混成自动机 textual description。
3. state assertion while-language 脚本。
4. polyhedral predicates。

### 交换与互操作

这篇论文的互操作重点不是开放格式，而是分析流程互补：

1. 同一模型可以配合 clock translation / linear approximation 使用。
2. `HyTech` 输出可用于调试与参数设计。
3. 文中主动把 `Kronos / Uppaal` 等专用工具放进相邻工具谱系里比较。

## 配套基础设施

- 建模/编辑工具：文本输入为主，另有 graphical front end。
- 解析/交换/元模型支持：以 textual linear hybrid automata + analysis script 为主；无中立交换标准。
- 仿真/执行支持：主体是 symbolic analysis，不是高保真数值仿真器。
- 验证/分析支持：reachability、parametric analysis、clock translation、approximation、error traces。
- 代码生成/转换支持：不强调代码生成，但强调模型收束与抽象转换。
- 标准化或社区生态：source code、executables、online demo、user guide 和案例库构成完整工具生态。

## 适用场景与需求前提

### 适用场景

适合控制器、实时协议、机器人、机电系统等离散-连续耦合明显、且连续部分可线性化的混成系统。

### 需求前提

1. 系统可抽成 linear hybrid automata，或可通过保守近似收束到该类。
2. 连续变量和跳转条件主要是线性约束。
3. 关心可达性、参数区间、安全边界或错误轨迹。
4. 可以接受 symbolic polyhedral analysis 的建模方式。

### 不适用或高成本场景

若模型核心是强非线性连续动力学、复杂数值求解或数据离散结构，`HyTech` 会很快吃力。

## 与相邻形式主义的关系

相对 [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md) 与 [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)，本文代表的是工具母线；相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，它面向更一般的线性混成系统而非 clocks 主导系统；相对 [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)，它走的是 polyhedral symbolic analysis，而不是 simulation-driven reachtube 路线。

## 与本研究的关系

### 对 Project 1 的价值

它证明了如果未来 `project_1` 生成的状态机需要落到混成/CPS 验证后端，那么“先收束到可分析子类，再接成熟工具”是很现实的路线。

### 作为目标形式主义还是中间表示

更适合作为专门化验证后端，而不是通用最终交付格式。

### 对需求到模型生成的启发

1. 生成混成模型时必须把 flow、invariant、jump 和参数边界显式结构化。
2. 工具能否算得动，很大程度取决于是否能收束成线性可分析子类。
3. 参数综合应被视为验证闭环的一部分，而不是额外附加功能。

### 现实限制

`HyTech` 很经典，但模型类限制也很强；更宽的 hybrid 需求通常仍要先做近似或换工具。

## 重要的相关工作

- [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)：混成自动机理论母线。
- [whats-decidable-about-hybrid-automata/desc.md](../whats-decidable-about-hybrid-automata/desc.md)：可判定子类与 `HyTech` 终止性背景。
- [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：clocks 主导系统的专用工具路线。
- [c2e2-a-verification-tool-for-stateflow-models/desc.md](../c2e2-a-verification-tool-for-stateflow-models/desc.md)：Stateflow/hybrid verification 的后续工具线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Linear Hybrid Automata / HyTech`
- 论文角色：混成自动机模型检查器 / parametric-analysis tool


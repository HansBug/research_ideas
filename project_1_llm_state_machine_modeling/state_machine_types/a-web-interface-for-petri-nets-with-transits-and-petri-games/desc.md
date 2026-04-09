# 带 Transit 的 Petri 网与 Petri 博弈 Web 界面 / A Web Interface for Petri Nets with Transits and Petri Games

## 基本信息

- 标题：A Web Interface for Petri Nets with Transits and Petri Games
- 中文标题：带 Transit 的 Petri 网与 Petri 博弈 Web 界面
- 作者：Manuel Gieseking，Jesko Hecking-Harbusch，Ann Yanich
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 12652`，pp. 381-388，2021
- DOI：`10.1007/978-3-030-72013-1_22`
- 链接：https://doi.org/10.1007/978-3-030-72013-1_22
- 形式主义：`Petri Nets with Transits / Petri Games / Adam web interface`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：面向 `Petri nets with transits` 与 `Petri games` 的可视化建模、调试、模型检查与综合前端
- 工具/实现获取方式：论文明确给出在线部署入口 `http://adam.informatik.uni-oldenburg.de`，并给出 `https://github.com/adamtool/webinterface` 与 `https://github.com/adamtool/adam` 作为开源实现入口。
- 标准/格式获取方式：输入侧是 `Petri net with transits + Flow-LTL` 与 `Petri game + safety objective`；输出侧支持显示 reduction 后的网、两人博弈策略，并可导出 `PNML` 与对应 `LTL` 公式。

## 简报

这篇论文的核心价值，不是再定义一种新的 `Petri` 形式主义，而是把 `AdamMC` 与 `AdamSYNT` 这两条原本偏命令行的分析链做成可交互、可调试、可解释的统一 Web 前端。对 `Petri nets with transits`，它让用户图形化构造数据流网、查看 `Flow-LTL` 归约结果、模拟 counterexample；对 `Petri games`，它让用户图形化建模 system/environment players、查看 two-player game 的 winning strategy，并交互定位不可实现原因。

- 形式主义定位：围绕 `Petri nets with transits` 与 `Petri games` 的建模、验证、综合基础设施，而不是新的 `Petri` 母型。
- 构造方式简述：浏览器端画 places、transitions、transits 和 system/environment places，服务端分别调用 `AdamMC` 或 `AdamSYNT`，再把 reduction 结果、counterexample、strategy 和 simulation 回显给用户。
- 基础设施与场景简述：依托 `Flow-LTL`、`PNML`、`AdamMC`、`AdamSYNT`、two-player-game reduction 和前端布局/交互组件，服务异步分布式系统的数据流验证与局部控制器综合。

```text
graphical Petri editing -> AdamMC / AdamSYNT backend -> reduction / counterexample / strategy -> visual simulation and debugging
```

## 形式主义定义与核心对象

### 定义对象

论文同时围绕两类对象组织：

1. `Petri nets with transits`，用于描述异步分布式系统中的 token/data flow。
2. `Flow-LTL`，用于在全局运行与局部流链两个层面写性质。
3. `Petri games`，用于描述 environment/system players 之间的异步博弈。
4. `AdamMC` 与 `AdamSYNT` 的 reduction 结果，包括归约后的 `Petri net + LTL` 与 finite two-player game。
5. Web 前端里的 editor、simulator、strategy viewer 和 counterexample viewer。

### 核心抽象

对 `Petri nets with transits`，论文依赖的核心网对象可写成：

$$
N = (P, T, F, In, \Upsilon)
$$

上式中的符号逐项解释如下：

1. `$P$` 是 place 集合。
2. `$T$` 是 transition 集合。
3. `$F$` 是普通 `Petri` 的 flow relation。
4. `$In$` 是初始 marking。
5. `$\Upsilon$` 是 transit relation，用于显式跟踪 token 的局部流向。

论文明确说明 `Flow-LTL` 可以同时约束全局 run 与局部 flow，典型形式可保守整理为：

$$
\varphi = \varphi_{run} \rightarrow A \psi_{flow}
$$

上式中的符号逐项解释如下：

1. `$\varphi_{run}$` 是关于全局 firing run 的公式。
2. `$A$` 是“对所有流链都成立”的 flow quantifier。
3. `$\psi_{flow}$` 是单条 token/data flow 必须满足的局部 `LTL` 性质。
4. 这正是 Web 前端在 `AdamMC` 分支里展示的两层性质结构。

对 `Petri games`，论文强调 places 被划分为 system 与 environment 两类，因此核心骨架可写成：

$$
P = P_S \cup P_E,\qquad P_S \cap P_E = \emptyset
$$

上式中的符号逐项解释如下：

1. `$P_S$` 是 system places，对应 system players。
2. `$P_E$` 是 environment places，对应 environment players。
3. 每个 token 代表一个 player。
4. system 与 environment 的区分决定了综合问题的博弈语义。

对 safety-style synthesis，论文对应的目标可保守写成：

$$
\forall \rho \in \mathrm{Runs}(\sigma):\ bad \notin \rho
$$

上式中的符号逐项解释如下：

1. `$\sigma$` 是 Web 前端最终展示的某个 strategy。
2. `$\rho$` 是该 strategy 下可能出现的一条运行。
3. `$bad$` 是错误 place。
4. system players 需要保证不论 environment 如何行动，都不会走到 `bad`。

论文的工具前端本身不是一个新理论对象，但可保守压成：

$$
\mathrm{WebAdam} = (\mathrm{Editor}, \mathrm{AdamMC}, \mathrm{AdamSYNT}, \mathrm{Viz})
$$

上式中的符号逐项解释如下：

1. `Editor` 是浏览器端建模入口。
2. `AdamMC` 是 `Petri nets with transits + Flow-LTL` 的模型检查后端。
3. `AdamSYNT` 是 `Petri games` 的综合后端。
4. `Viz` 表示 reduction、counterexample、strategy 和 simulation 的可视化层。
5. 这是依据论文系统结构做的保守抽象，不是原文显式给出的形式化元组。

### 一个最小例子与通俗解释

论文里最直观的最小例子是分布式报警系统 `Petri game`：

1. 一个 environment player 先决定左侧还是右侧发生 burglary。
2. 两个 system players 分别代表两个本地控制组件。
3. system players 既要本地检测，也要相互同步“另一侧是否被入侵”。
4. 若某组件在错误的位置拉响警报，或无入侵时错误报警，就会进入 `bad` place。
5. Web 前端右侧展示出的 winning strategy，本质上就是一套不会把 token 送进 `bad` 的局部控制方案。

通俗地说，这个 Web 界面像一块“Petri 调试台”。对 `Petri nets with transits`，它让你看到 token 轨迹和 counterexample 到底在哪条 flow 上出错；对 `Petri games`，它让你看到 system players 为什么赢、为什么输，以及忘了哪种环境分支会导致不可实现。

### 运行 / 接受 / 转移语义

`AdamMC` 分支的核心语义步骤是：

$$
(N,\varphi) \leadsto (N^{>}, \varphi^{>})
$$

上式中的符号逐项解释如下：

1. `$N$` 是原始 `Petri net with transits`。
2. `$\varphi$` 是原始 `Flow-LTL` 公式。
3. `$N^{>}$` 是 reduction 后的普通 `Petri net`。
4. `$\varphi^{>}$` 是对应的普通 `LTL` 公式。
5. Web 前端既能显示输入网，也能显示 reduction 后的网和公式。

`AdamSYNT` 分支的核心语义步骤是：

$$
G_{PG} \leadsto G_{2p}
$$

上式中的符号逐项解释如下：

1. `$G_{PG}$` 是原始 `Petri game`。
2. `$G_{2p}$` 是 reduction 后的 finite two-player game with complete information。
3. Web 前端允许同时查看 `Petri game` 上的 strategy 和 two-player game 上的 strategy。
4. 这正是它比纯命令行输出更强的地方，因为用户能对照两个层面排查建模错误。

### 语义边界

1. Web 前端本身并不扩展 `Petri nets with transits` 或 `Petri games` 的理论边界，它只是把已有后端做成更可解释的工作台。
2. `Petri games` 分支当前聚焦的是“bounded number of system players + one environment player + safety objective”这类可判定子类。
3. `Petri nets with transits` 分支的核心强项是局部流链，而不是一般高层 Petri 网的所有验证任务。
4. 这条路线强依赖 `Adam` 工具生态；若脱离 `AdamMC/AdamSYNT`，Web 前端本身不是中立交换标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PNWT` 骨架 | `$N = (P, T, F, In, \Upsilon)$` | 带 transit 的网对象是数据流验证的前提。 |
| `Flow-LTL` 结构 | `$\varphi = \varphi_{run} \rightarrow A \psi_{flow}$` | 同时约束全局 run 与局部 flow。 |
| `Petri game` 玩家划分 | `$P = P_S \cup P_E,\ P_S \cap P_E = \emptyset$` | system/environment places 的分治是综合语义基础。 |
| safety 目标 | `$\forall \rho \in \mathrm{Runs}(\sigma): bad \notin \rho$` | winning strategy 的本质是永不进入坏位置。 |
| 两条 backend reduction | `$(N,\varphi)\leadsto (N^{>},\varphi^{>})$`、`$G_{PG}\leadsto G_{2p}$` | Web 前端真正可视化的是后端 reduction 的全过程。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | places、transitions、markings、strategies 都可视化。 |
| 事件 / 触发 | 很强 | firing、同步、坏位置触发与策略分支都是一等对象。 |
| 守卫 / 数据 | 弱支持 | 主体还是 `Petri` token flow，而不是富数据状态机。 |
| 层次 | 不支持 | 论文不讨论层次化网或层次化游戏。 |
| 并发 / 同步 | 很强 | `Petri` 并发与同步本来就是主角。 |
| 时间约束 | 不支持 | 本文不是 timed Petri 工具。 |
| 连续动态 / 随机性 | 不支持 | 不在对象范围内。 |
| 可执行 / 可验证性 | 很强 | 能做模型检查、综合、交互式策略分析和运行模拟。 |

### 形式化问题与性质

1. 这篇论文补的是 `Petri` 工具链里很稀缺的一环：把 reduction 结果和 counterexample 也做成可视调试对象，而不是只给 verdict。
2. 它同时补强了 `Petri nets with transits` 的 flow-sensitive verification 路线和 `Petri games` 的 distributed synthesis 路线。
3. 对本文库来说，这类条目不是新主干节点，但非常适合挂在现有 `AdamMC / ADAM / Petri-game` 工具锚点上。

## 构造方式与承载格式

### 建模入口

论文给出的建模入口有两条：

1. 图形化创建 `Petri net with transits`，包括 places、transitions、普通 arcs 和 colored transit arcs。
2. 图形化创建 `Petri game`，包括 system places、environment places、bad place 与安全约束。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Petri net with transits + Flow-LTL`。
2. `Petri game + safety objective`。
3. reduction 后的普通 `Petri net + LTL`。
4. reduction 后的 finite two-player game。
5. `PNML` 导出与 `LTL` 公式显示。

### 交换与互操作

这条路线的互操作重点在于：

1. `Petri nets with transits` 分支可把 reduction 后的网导出为 `PNML`。
2. Web 前端可继续接 `APT`、`LoLA`、`TAPAAL` 等其他 `Petri` 工具，这在论文结尾被明确列为扩展方向。
3. `Petri games` 分支同时暴露 `Petri game` 视图与 two-player game 视图，便于与其他博弈求解链比较。

## 配套基础设施

- 建模/编辑工具：浏览器端图形 editor，支持拖放布局、自动布局和节点物理参数调节。
- 解析/交换/元模型支持：`Flow-LTL` 输入、`Petri game` 输入、`PNML` 导出、`LTL` 展示。
- 仿真/执行支持：stepwise simulation、interactive state-space exploration、counterexample replay、strategy simulation。
- 验证/分析支持：`AdamMC` 的 `Flow-LTL` 检查、`AdamSYNT` 的 safety synthesis、two-player-game strategy 分析。
- 代码生成/转换支持：核心是 verification/synthesis reduction，而不是面向部署代码生成。
- 标准化或社区生态：依托 `AdamMC`、`AdamSYNT`、`APT` 与更广的 `Petri` analysis 生态。

## 适用场景与需求前提

### 适用场景

适合以下几类问题：

1. 需要显式跟踪 packet/token/data flow 的异步分布式系统验证。
2. 需要把 environment/system 对抗关系显式建成 `Petri game` 的分布式控制器综合。
3. 需要反复调试模型、解释 counterexample、向非工具作者演示 reduction 结果的研究或教学场景。

### 需求前提

1. 系统要能稳定建成 `Petri net with transits` 或 `Petri game`。
2. 性质要么能写成 `Flow-LTL`，要么能写成 safety-style bad-place objective。
3. 用户愿意在 `Adam` 生态内工作，而不是要求中立格式覆盖全部后端。
4. 若关注的是综合问题，则 system/environment 的职责边界必须明确。

### 不适用或高成本场景

1. 若系统更自然地表达为 timed automata、rich-data statecharts 或 hybrid automata，这个前端就不是最顺手入口。
2. 若团队只需要批处理 verdict，而不需要交互式调试和解释层，这个 Web 前端的价值会下降。
3. 若要处理本文未覆盖的 `Petri game` 子类或更复杂的时序逻辑，仍要回到后端研究原型。

## 与相邻形式主义的关系

相对 [adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md](../adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md)，这篇论文更偏图形化前端、counterexample 可视化和交互调试，而不是 `Flow-LTL` reduction 本体。相对 [symbolic-vs-bounded-synthesis-for-petri-games/desc.md](../symbolic-vs-bounded-synthesis-for-petri-games/desc.md)，后者聚焦 `Petri games` 综合算法与 `BDD/2-QBF` 比较，而这里聚焦 how to build/debug/view the models and strategies。相对 [building-petri-nets-tools-around-neco-compiler/desc.md](../building-petri-nets-tools-around-neco-compiler/desc.md)，`Neco` 更偏 Petri 编译与显式探索后端，而这里更偏 flow-sensitive verification 与 distributed synthesis 的人机交互层。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“状态机/网模型生成出来以后，如何让人能真正看懂和调试”同样是闭环里很关键的一环。
2. 对 LLM 生成模型来说，Web 前端展示的 intermediate reductions、counterexamples 和 strategies，正好对应“生成后验证失败时如何解释和修复”的需求。
3. 这类工具也提醒 `project_1`，若未来选 `Petri` 侧中间表示，就应同步考虑可视化与交互调试而不只是语法定义。

### 作为目标形式主义还是中间表示

更像现有 `Petri` 形式主义之上的工程基础设施，而不是新的目标形式主义。

### 对需求到模型生成的启发

1. 需求若同时包含“全局行为约束”和“局部对象流向约束”，`Petri nets with transits` 这类二层表达很有吸引力。
2. 需求若天然有 environment/system 对抗结构，则应尽早显式化 bad states 与玩家边界，便于后续转成 `Petri game`。
3. 生成系统不应只输出静态模型，还应尽量保留可供调试的中间解释对象。

### 现实限制

这条路线高度绑定 `Adam` 工具生态，且仍是研究型基础设施；但正因为绑定得深，才把 `PNWT` 与 `Petri game` 两条支线做得非常可操作。

## 重要的相关工作

1. [adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md](../adammc-a-model-checker-for-petri-nets-with-transits-against-flow-ltl/desc.md)：`PNWT + Flow-LTL` 后端本体。
2. [symbolic-vs-bounded-synthesis-for-petri-games/desc.md](../symbolic-vs-bounded-synthesis-for-petri-games/desc.md)：`Petri games` 综合算法与工具比较。
3. [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)：另一条更偏标准分析环境的 `Petri` 工具主线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 归类理由：论文主体是 `AdamMC/AdamSYNT` 的图形化建模、调试和展示基础设施，不是新的 `Petri` 本体或新语义分支，因此适合归入 `📦/🏗️`。

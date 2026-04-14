# LydiaSyft：面向 LTLf 规格的组合式符号综合框架 / LydiaSyft: A Compositional Symbolic Synthesis Framework for LTLf Specifications

## 基本信息

- 标题：LydiaSyft: A Compositional Symbolic Synthesis Framework for LTLf Specifications
- 中文标题：LydiaSyft：面向 `LTLf` 规格的组合式符号综合框架
- 作者：Shufang Zhu，Marco Favorito
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，pp. 295-302，2025
- DOI：`10.1007/978-3-031-90643-5_15`
- 链接：https://doi.org/10.1007/978-3-031-90643-5_15
- 形式主义：`LTLf synthesis / explicit DFA / symbolic DFA / LydiaSyft`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：`LTLf` 推理与综合的组合式显式/符号 `DFA` 框架及多类游戏求解基础设施
- 工具/实现获取方式：论文明确给出开源仓库 `https://github.com/whitemech/LydiaSyft`、文档 `https://whitemech.github.io/LydiaSyft/index.html` 与 `Zenodo` artifact `https://zenodo.org/records/13927906`，实现语言为 `C++`。
- 标准/格式获取方式：输入公式采用接近 `TLSF` 的 `LTLf` 语法，并支持 `GR(1)`、simple fairness、simple stability 等环境规格；输出可打印 `DOT` 策略与显式/符号 `DFA`，不是正式行业标准。

## 简报

`LydiaSyft` 的价值在于把过去分散在 `LTLf -> DFA`、symbolic automata、game solving 与环境规格扩展里的几条线真正接成一个统一框架。它一头继承 `Lydia` 的 compositional `LTLf-to-DFA` 技术，一头继承 `Syft` 的 symbolic synthesis 技术，再往上补了 explicit / symbolic `DFA` 操作、reachability / Buchi / coBuchi / coGR(1) 多类游戏库，以及 `GR(1)` 环境规格等更宽的综合场景。

- 形式主义定位：面向 `LTLf` 的 reasoning / synthesis 基础设施，而不是新的状态机母型。
- 构造方式简述：`LTLf formula -> explicit DFA -> symbolic DFA -> suitable two-player game -> winning strategy / DOT output`。
- 基础设施与场景简述：依托 compositional `LTLf-to-DFA`、`BDD/ADD/CUDD`、symbolic games、`Slugs` 与 `C++` 接口，服务 finite-trace reactive synthesis、机器人任务规划与环境规格扩展综合。

```text
LTLf requirement -> explicit DFA -> symbolic DFA -> reachability / Buchi / coGR(1) game -> winning finite-trace strategy
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `LTLf` 规格语言。
2. explicit-state `DFA`。
3. symbolic-state `DFA`。
4. 多类两方博弈对象。
5. standard `LTLf` synthesis、maximally permissive synthesis、以及带环境规格的 `LTLf` synthesis。

### 核心抽象

论文直接给出 `LTLf` 语法骨架：

$$
\varphi ::= \mathrm{tt} \mid a \mid \varphi \land \varphi \mid \neg \varphi \mid \bigcirc \varphi \mid \varphi U \varphi
$$

上式中的符号逐项解释如下：

1. `$\mathrm{tt}$` 是恒真公式。
2. `$a$` 是原子命题。
3. `$\bigcirc$` 是 `Next`。
4. `$U$` 是 `Until`。
5. 论文进一步说明 `\Diamond`、`\Box`、weak next 等都作为缩写使用。

论文给出 explicit-state `DFA` 的标准定义：

$$
A = \langle \Sigma, S, s_0, \delta, F \rangle
$$

上式中的符号逐项解释如下：

1. `$\Sigma$` 是字母表。
2. `$S$` 是有限状态集合。
3. `$s_0$` 是初始状态。
4. `$\delta : S \times \Sigma \to S$` 是总迁移函数。
5. `$F \subseteq S$` 是接受状态集合。
6. 论文强调：给定 `LTLf` 公式 `$\varphi$`，可以构造一个接受与之等价语言的 `DFA`。

symbolic-state `DFA` 则被定义为：

$$
D = (X, Y, Z, \iota, \eta, f)
$$

上式中的符号逐项解释如下：

1. `$X$` 是环境控制的布尔变量。
2. `$Y$` 是 agent 控制的布尔变量。
3. `$Z$` 是编码显式状态集合 `$S$` 的命题集合。
4. `$\iota$` 是初始状态在 `$Z$` 上的编码。
5. `$\eta$` 是以 `BDD` 形式表示的符号迁移函数。
6. `$f$` 是接受状态集合的布尔表示。

标准 `LTLf` synthesis 的目标在论文中写成：

$$
\exists \sigma_{agn}\ \forall \sigma_{env}:\ \exists k \ge 0.\ \mathrm{play}_k(\sigma_{agn}, \sigma_{env}) \models \varphi
$$

上式中的符号逐项解释如下：

1. `$\sigma_{agn}$` 是 agent strategy。
2. `$\sigma_{env}$` 是 environment strategy。
3. `$\mathrm{play}_k$` 是双方博弈在前 `$k$` 步产生的有限 trace 前缀。
4. 公式要求 agent 能保证在某个有限步长内满足 `LTLf` 目标 `$\varphi$`。

带环境规格的 `LTLf` synthesis 则进一步写成：

$$
\exists \sigma_{agn}\ \forall \sigma_{env} \triangleright env:\ \exists k \ge 0.\ \mathrm{play}_k(\sigma_{agn}, \sigma_{env}) \models \varphi
$$

上式中的符号逐项解释如下：

1. `$env$` 是环境必须满足的 `LTL` 规格。
2. `$\sigma_{env} \triangleright env$` 表示环境策略强制满足该环境规格。
3. `LydiaSyft` 支持 simple stability、simple fairness 和 `GR(1)` 环境规格，并允许附加 safety 条件。

### 一个最小例子与通俗解释

作为通俗化示意，可以考虑：

1. 环境变量只有 `req`，agent 变量只有 `grant`。
2. 目标是“在某个有限前缀内给出一次 `grant`，且 `grant` 不能凭空发生”。
3. 这类需求可以写成一个小的 `LTLf` 公式，再经 `LydiaSyft` 变成 `DFA`。
4. 若再加一个环境规格，例如“环境最终会稳定在 `req = 0`”，则可进一步构造成带环境规格的博弈。

通俗地说，`LydiaSyft` 不是直接对公式蛮力搜索策略，而是先把“有限轨迹上什么算满足”做成 `DFA`，再把“环境和系统怎么轮流出招”做成游戏，然后在游戏里算 winning strategy。

### 运行 / 接受 / 转移语义

论文把标准 `LTLf` synthesis 归约为在 `DFA` 上求 reachability game。可保守写成：

$$
G = (D_\varphi, \mathrm{Reach}(t))
$$

上式中的符号逐项解释如下：

1. `$D_\varphi$` 是由公式 `$\varphi$` 构造出的 symbolic-state `DFA`。
2. `$t$` 是接受目标状态集合。
3. `$\mathrm{Reach}(t)$` 表示 agent 需要保证最终到达接受目标。
4. 这正对应论文给出的 standard `LTLf` synthesis 路线。

对于 explicit-state 到 symbolic-state 的桥接，论文说明显式状态数 `|S|` 被编码到命题集 `$Z$` 上。可保守写成：

$$
|Z| = \lceil \log_2 |S| \rceil
$$

上式中的符号逐项解释如下：

1. `$S$` 是 explicit `DFA` 的状态集合。
2. `$Z$` 是 symbolic `DFA` 用来编码状态的布尔变量集。
3. 这说明 symbolic representation 不是换语义，而是换承载。

论文还给出带环境规格时的游戏类型扩展：

$$
\mathrm{BuchiReach},\quad \mathrm{coBuchiReach},\quad \mathrm{coGR(1)Reach}
$$

上式中的符号逐项解释如下：

1. `Buchi-Reachability game` 用于 simple stability 环境规格。
2. `coBuchi-Reachability game` 用于 simple fairness 环境规格。
3. `coGR(1)-Reachability game` 用于 `GR(1)` 环境规格与附加 safety 条件。
4. 这说明 `LydiaSyft` 不是只支持单一 synthesis setting。

### 语义边界

1. 论文对象是 finite-trace `LTLf`，不是 infinite-trace `LTL` 主后端。
2. 重点是离散布尔变量与 finite traces，不处理 clocks、连续变量或随机博弈。
3. 框架虽然支持多类环境规格，但仍以 `DFA` / symbolic game 归约为主，不是通用 DSL。
4. 论文强调 usability 与 extensibility，高峰性能不是唯一目标。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `LTLf` 语法 | `$\varphi ::= \mathrm{tt} \mid a \mid \varphi \land \varphi \mid \neg \varphi \mid \bigcirc \varphi \mid \varphi U \varphi$` | 工具的前端规格对象。 |
| explicit `DFA` | `$A = \langle \Sigma, S, s_0, \delta, F \rangle$` | `LTLf` 推理与综合的显式中间表示。 |
| symbolic `DFA` | `$D = (X, Y, Z, \iota, \eta, f)$` | `BDD` 化后的核心数据结构。 |
| 标准综合目标 | `$\exists \sigma_{agn}\forall \sigma_{env}: \exists k \ge 0.\ \mathrm{play}_k(\sigma_{agn}, \sigma_{env}) \models \varphi$` | `LTLf` synthesis 的基本语义。 |
| 环境规格综合目标 | `$\exists \sigma_{agn}\forall \sigma_{env} \triangleright env: \exists k \ge 0.\ \mathrm{play}_k(\sigma_{agn}, \sigma_{env}) \models \varphi$` | `LydiaSyft` 扩展后的更一般场景。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | `DFA` 与 symbolic-state `DFA` 都是一等对象。 |
| 事件 / 触发 | 很强 | 环境 / agent 布尔动作共同驱动有限轨迹。 |
| 守卫 / 数据 | 弱支持 | 主要是布尔命题，不是 rich data guards。 |
| 层次 | 不支持 | 不是层次状态机语法。 |
| 并发 / 同步 | 中等支持 | 通过两方博弈交互表达，不是组件并发代数。 |
| 时间约束 | 不支持 | `LTLf` 针对有限离散轨迹，不含 clocks。 |
| 连续动态 / 随机性 | 不支持 | 不属于 stochastic / hybrid synthesis。 |
| 可执行 / 可验证性 | 很强 | explicit/symbolic `DFA`、多类 game solver、`DOT` 输出与 artifact 都已具备。 |

### 形式化问题与性质

1. `LydiaSyft` 的核心贡献不是新发明一种自动机，而是把 `LTLf` 公式、`DFA`、symbolic representation 与多类 synthesis settings 接成统一平台。
2. 由 explicit `DFA` 过渡到 symbolic `DFA`，使它既保留 compositional automata construction，也兼顾后续博弈求解的紧凑表示。
3. `GR(1)` 环境规格支持非常关键，因为它把 finite-trace synthesis 与更结构化的 reactive-synthesis 传统接到了一起。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 采用接近 `TLSF` 语法的 `LTLf` 公式。
2. optional safety / fairness / stability / `GR(1)` 环境规格。
3. `CLI` 指令选择不同 synthesis setting。
4. `C++` API 调用底层 `DFA` 与 game solver。

### 机器可处理承载方式

机器可处理承载方式包括：

1. explicit-state `DFA`。
2. symbolic-state `DFA`。
3. reachability / `Buchi` / `coBuchi` / `coGR(1)` games。
4. `DOT` 格式 winning strategy。

### 交换与互操作

1. 前端语法刻意贴近 `TLSF`，降低与现有 synthesis 生态的摩擦。
2. `CUDD` 负责 `BDD/ADD` 底层表示。
3. `Slugs` 被用于 `coGR(1)` game 的求解后端。
4. `Lydia` 与 `Syft` 分别提供 compositional automata construction 与 symbolic synthesis 的核心技术来源。

## 配套基础设施

- 建模/编辑工具：`CLI` + `C++` library，而不是图形建模器。
- 解析/交换/元模型支持：`LTLf` parser、explicit/symbolic `DFA` wrappers 与 automata manipulation API。
- 仿真/执行支持：重点是综合 winning strategy，而非独立 runtime。
- 验证/分析支持：realizability preprocessing、`Reachability`、`ReachabilityMaxSet`、`BuchiReachability`、`coBuchiReachability`、`coGR1Reachability` 等库。
- 代码生成/转换支持：`LTLf -> DFA -> symbolic game -> strategy` 是全文核心转换链。
- 标准化或社区生态：`GitHub`、文档站点、`Zenodo` artifact、`TLSF` 风格输入、`CUDD` 与 `Slugs` 构成研究型生态。

## 适用场景与需求前提

### 适用场景

适合 finite-trace reactive synthesis、机器人任务规划、需要环境规格扩展的 `LTLf` 合成实验，以及面向教学和研究的 symbolic-game 框架复用。

### 需求前提

1. 需求需要能压成布尔命题上的 `LTLf` 目标。
2. 控制问题以有限轨迹完成为核心，而不是无限运行公平性本体。
3. 若加入环境规格，应能落成 simple stability、simple fairness 或 `GR(1)` 这类结构化约束。
4. 使用者接受经由 `DFA` 与 symbolic games 的两层中间表示。

### 不适用或高成本场景

若目标是 dense-time、连续控制、丰富数据域或直接输出工业控制代码，`LydiaSyft` 不是直接可用的最终后端。

## 与相邻形式主义的关系

相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`Slugs` 面向 infinite-trace `GR(1)` synthesis，而 `LydiaSyft` 面向 finite-trace `LTLf` 并在必要时把 `GR(1)` 放到环境规格侧；相对 [a-high-level-ltl-synthesis-format-tlsf-v11/desc.md](../a-high-level-ltl-synthesis-format-tlsf-v11/desc.md)，`TLSF` 是高层规格格式，而 `LydiaSyft` 是显式/符号 `DFA` 与游戏求解框架；相对 [dissecting-ltlsynt/desc.md](../dissecting-ltlsynt/desc.md)，`ltlsynt` 面向 infinite-trace `LTL` 与 `AIG` 输出，`LydiaSyft` 则聚焦 finite-trace synthesis 与多类环境规格；相对 [owl-a-library-for-omega-words-automata-and-ltl/desc.md](../owl-a-library-for-omega-words-automata-and-ltl/desc.md)，`Owl` 更偏 logic / automata manipulation，`LydiaSyft` 直接把这条线推进到 synthesis games。

## 与本研究的关系

### 对 Project 1 的价值

`LydiaSyft` 说明：如果需求更自然地表达为“有限任务何时完成”，那么 `LTLf -> DFA -> game` 是一条非常适合自动化建模的路线。它特别适合作为 LLM 生成 finite-trace 目标后接入的公开后端。

### 可复用启发

1. 需求抽取阶段可以把“任务完成型目标”与“持续反应型目标”分开，前者优先考虑 `LTLf`。
2. 中间表示不必只有显式状态机，symbolic-state `DFA` 同样可以成为稳定工作接口。
3. 环境规格不一定要和目标公式混写在一起，拆成 environment side constraints 往往更清晰。

## 重要的相关工作

1. [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)：`GR(1)` synthesis 工具线对照。
2. [a-high-level-ltl-synthesis-format-tlsf-v11/desc.md](../a-high-level-ltl-synthesis-format-tlsf-v11/desc.md)：高层综合规格格式。
3. [dissecting-ltlsynt/desc.md](../dissecting-ltlsynt/desc.md)：`LTL` synthesis pipeline 的相邻基础设施。
4. [owl-a-library-for-omega-words-automata-and-ltl/desc.md](../owl-a-library-for-omega-words-automata-and-ltl/desc.md)：logic / automata library 对照线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 关键特性：`LTLf`、explicit `DFA`、symbolic `DFA`、`BDD/ADD`、`Reachability/Buchi/coGR(1)` games、environment specifications。
- 构造方式：`LTLf formula -> compositional DFA -> symbolic game -> winning strategy`。
- 基础设施：`C++`、`CUDD`、`Lydia`、`Syft`、`Slugs`、`Zenodo` artifact。
- 对状态机族演化树而言，它是 finite-trace synthesis 与 symbolic-automata toolchain 的静态挂接口径，不形成新的主树节点。

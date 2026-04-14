# Acacia+：面向 LTL 综合的工具 / Acacia+, a Tool for LTL Synthesis

## 基本信息

- 标题：Acacia+, a Tool for LTL Synthesis
- 中文标题：Acacia+：面向 `LTL` 综合的工具
- 作者：Aaron Bohy，Veronique Bruyere，Emmanuel Filiot，Naiyong Jin，Jean-Francois Raskin
- 发表：*Computer Aided Verification*，`LNCS 7358`，pp. 652-657，2012
- DOI：`10.1007/978-3-642-31424-7_45`
- 链接：https://doi.org/10.1007/978-3-642-31424-7_45
- 形式主义：`LTL reactive synthesis / safety games / Acacia+`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：antichain-based `LTL` realizability / synthesis tool and safety-game route
- 工具/实现获取方式：原文明确给出下载与网页入口 `http://lit2.ulb.ac.be/acaciaplus`；实现采用 `Python + C`，源码按 `GNU GPL` 发布。
- 标准/格式获取方式：输入是 `LTL` 公式与输入/输出原子命题划分，兼容 `Wring` 与 `LTL2BA` 风格输入；输出为 `Verilog` 策略以及小规模 `Moore` 机 `PNG` 图，不是中立交换标准。

## 简报

`Acacia+` 补的是早期 `LTL` reactive synthesis 工具线里非常关键的一条 safety-game / antichain 路线。它不走传统“先做昂贵 determinization，再在大型 parity/Rabin 游戏上求解”的老路径，而是把 `LTL` realizability / synthesis 降到安全博弈上，再用 antichain 做增量式符号求解，从而更容易得到可落地的小型 `Moore` 策略。

- 形式主义定位：围绕 `LTL` 反应式综合的工具化方法路线，而不是新的状态机母型。
- 构造方式简述：`LTL` 公式先转成 universal co-Buchi / `K`-coBuchi 自动机，再转成安全博弈 `G(\varphi, k)`，最后从 antichain 中抽取 `Moore` 机。
- 基础设施与场景简述：依托 `Wring/LTL2BA`、`Python + C`、web UI、`Verilog` 输出与 `PyGraphviz` 绘图，服务控制器综合、不可实现规格调试和从 `LTL` 提取紧凑确定自动机。

```text
LTL specification + I/O partition -> universal co-Buchi / K-coBuchi automaton -> safety game -> antichain fixpoint -> Moore machine / Verilog strategy
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `LTL` realizability / synthesis game；
2. universal co-Buchi 与 universal `K`-coBuchi automata；
3. 安全博弈 `G(\varphi, k)`；
4. antichain-based symbolic fixed point；
5. 输出的 `Moore` strategy。

### 核心抽象

论文把 `LTL` realizability 问题写成输入玩家与系统玩家之间的无限轮对局。若原子命题集合分成输入 `$I$` 与输出 `$O$`，则一次完整交互可写成：

$$
w = (i_1 \cup o_1)(i_2 \cup o_2)\cdots(i_k \cup o_k)\cdots
$$

上式中的符号逐项解释如下：

1. `$i_j \subseteq I$` 是第 `$j$` 轮环境给出的输入赋值。
2. `$o_j \subseteq O$` 是第 `$j$` 轮系统给出的输出赋值。
3. `$w$` 是输入与输出交织形成的无限字。
4. 若 `$w \models \varphi$`，则系统玩家赢得该局。

`Acacia+` 的核心不是直接在 `$LTL$` 公式上求解，而是把它逐步下沉为安全博弈：

$$
\varphi \Rightarrow \mathcal{A}_{\mathrm{UCBW}} \Rightarrow \mathcal{A}^{K}_{\mathrm{UKCW}} \Rightarrow G(\varphi, K)
$$

上式中的符号逐项解释如下：

1. `$\mathcal{A}_{\mathrm{UCBW}}$` 是与 `$LTL$` 公式等价的 universal co-Buchi word automaton。
2. `$\mathcal{A}^{K}_{\mathrm{UKCW}}$` 是当 `$K$` 足够大时的 universal `K`-coBuchi automaton。
3. `$G(\varphi, K)$` 是由该自动机构造出来的安全博弈。
4. 增量地枚举 `$k = 0, 1, 2, \ldots$` 是工具提升实用性的关键。

工具内部还要操纵计数函数来记录自动机状态被访问的情况：

$$
f : Q \to \{-1, 0, \ldots, K, K+1\}
$$

上式中的符号逐项解释如下：

1. `$Q$` 是自动机状态集合。
2. `$f(q) = -1$` 表示状态 `$q$` 尚未到达。
3. `$0 \le f(q) \le K$` 表示与接受状态访问次数相关的计数信息。
4. 这些计数函数构成 antichain 求解中的核心状态承载。

### 一个最小例子与通俗解释

一个最小例子可以是单请求单授权控制器：

1. 输入集合只有 `req`，输出集合只有 `grant`。
2. 需求写成“只要请求反复出现，授权也必须最终出现”这类 `LTL` 公式。
3. `Acacia+` 会先把这个公式变成自动机，再变成环境对系统的安全博弈。
4. 若系统有赢法，工具就给出一个 `Moore` 机，例如“只要看到请求就输出授权”的有限控制器。

通俗地说，`Acacia+` 像是在问：“面对任何环境输入流，系统能不能一直安全地走下去并满足长期时序要求？”它把这个问题改写成一个可求解的博弈，再把赢法还原成状态机控制器。

### 运行 / 接受 / 转移语义

`Acacia+` 输出的是有限记忆 winning strategy，论文明确以 `Moore` 机承载这一策略。可保守整理为：

$$
M = (S, s_0, \Sigma_I, \Sigma_O, \delta, \lambda)
$$

上式中的符号逐项解释如下：

1. `$S$` 是控制器内部状态集合。
2. `$s_0$` 是初始状态。
3. `$\Sigma_I = 2^I$` 是输入字母表。
4. `$\Sigma_O = 2^O$` 是输出字母表。
5. `$\delta : S \times \Sigma_I \to S$` 是状态更新函数。
6. `$\lambda : S \to \Sigma_O$` 给出当前状态下的系统输出。

博弈求解语义本质上是在安全状态集合上做反向 fixed point，并用 antichain 紧凑表示所有可赢状态。论文没有把 fixed point 公式完整展开成一个新语义，而是强调从安全配置集合出发做 backward computation，并从 antichain 中提取策略。

### 语义边界

1. 这是 `LTL` 综合工具，而不是更一般博弈模型或定量优化综合器。
2. 核心收益来自安全博弈化和 antichain；若规格天然不适合这一路线，优势会下降。
3. 工具主要面向有限离散 `I/O` 命题，不直接处理连续变量和显式时钟。
4. 它能输出紧凑策略，但不意味着解决了 `LTL` 综合的双指数理论复杂度。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 交互字语义 | `$w = (i_1 \cup o_1)(i_2 \cup o_2)\cdots$` | `LTL` 规格在系统/环境博弈中的基本对象。 |
| 赢条件 | `$w \models \varphi$` | 系统是否满足规格。 |
| 自动机-博弈化链路 | `$\varphi \Rightarrow \mathcal{A}_{\mathrm{UCBW}} \Rightarrow \mathcal{A}^{K}_{\mathrm{UKCW}} \Rightarrow G(\varphi, K)$` | `Acacia+` 的核心求解路线。 |
| 计数函数 | `$f : Q \to \{-1,0,\ldots,K,K+1\}$` | antichain 中的核心状态表示。 |
| 输出策略 | `$M = (S,s_0,\Sigma_I,\Sigma_O,\delta,\lambda)$` | 最终可执行控制器的承载形式。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 最终输出有限状态 `Moore` 控制器。 |
| 事件 / 触发 | 很强 | 输入/输出原子命题分区是问题定义核心。 |
| 守卫 / 数据 | 弱支持 | 主要是布尔命题，不处理复杂数据守卫。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 中等支持 | 并发性体现在环境/系统博弈和组合规格，而非显式并发状态机。 |
| 时间约束 | 不支持 | 原文聚焦离散 `LTL` 综合。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / probabilistic 路线。 |
| 可执行 / 可验证性 | 很强 | 可输出 `Verilog` 策略与 `PNG` 状态图，并支持 unrealizability debugging。 |

### 形式化问题与性质

1. `Acacia+` 的代表性不在“再做一个综合器”，而在把 `LTL` 综合工程化成安全博弈和 antichain 求解流程。
2. 它特别强调“紧凑策略提取”，这点对控制器真正落地很关键。
3. compositional 处理 `\varphi_1 \land \cdots \land \varphi_n` 也是它与早期 monolithic 路线的重要差异。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. `LTL` 公式 `\varphi`；
2. 原子命题分区 `I / O`；
3. monolithic 或 compositional 的 automaton construction 选项；
4. backward / forward 安全博弈求解选项。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Wring` / `LTL2BA` 风格输入；
2. universal co-Buchi 与 `K`-coBuchi automata；
3. antichain of counting functions；
4. `Verilog` strategy 与小规模 `Moore` 机图。

### 交换与互操作

1. 工具可消费 `Wring` 与 `LTL2BA` 风格公式输入。
2. 输出可落成 `Verilog`，便于继续接综合或实现链路。
3. 对小策略还能直接画成 `PNG`，适合作为调试与审阅材料。

## 配套基础设施

- 建模/编辑工具：命令行与 web interface 两种入口。
- 解析/交换/元模型支持：兼容 `Wring`、`LTL2BA` 输入风格，内部承载自动机与安全博弈对象。
- 仿真/执行支持：不主打仿真平台，但输出 `Verilog` 与 `Moore` 机足以进入后续实现链。
- 验证/分析支持：realizability / unrealizability checking、counterstrategy extraction、compositional solving。
- 代码生成/转换支持：直接生成 `Verilog`，并可把小策略可视化为 `PNG`。
- 标准化或社区生态：`Python + C` 实现、开源 `GPL`、可下载或网页使用。

## 适用场景与需求前提

### 适用场景

适合从时序需求直接综合有限状态控制器、调试不可实现 `LTL` 规格，以及需要从 `LTL` 规格反推出紧凑确定自动机的场景。

### 需求前提

1. 需求必须能写成 `LTL`。
2. 输入/输出原子命题分区需要事先清晰给出。
3. 若公式是大合取，最好能利用 compositional 结构。
4. 团队接受 automata/game-based synthesis 的工程前端，而不是仅靠逻辑解释器。

### 不适用或高成本场景

若需求更接近 `GR(1)` 这类受限片段，专用综合器可能更高效；若核心问题涉及连续动力学、显式时钟或定量代价，`Acacia+` 也不是直接答案。

## 与相邻形式主义的关系

相对 [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)，`Slugs` 更聚焦 `GR(1)` 片段和工程化插件，而 `Acacia+` 面向更一般的 `LTL`；相对 [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)，`Strix` 走的是 on-the-fly `DPA + parity game` 路线，而 `Acacia+` 的代表性在 `UCBW/K-coBuchi + safety game + antichain`；相对 [rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md](../rabinizer-4-from-ltl-to-your-favourite-deterministic-automaton/desc.md) 与 [goal-extended-towards-a-research-tool-for-omega-automata-and-temporal-logic/desc.md](../goal-extended-towards-a-research-tool-for-omega-automata-and-temporal-logic/desc.md)，后两者更偏 logic-to-automata translation / manipulation，而 `Acacia+` 把这些前端直接接到控制器综合问题上。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明若需求能较稳定地组织成时序逻辑，目标工件不必停在“状态机模型”，还可以直接推进到可执行控制器。
2. safety-game 化与 antichain 表示提供了非常好的“中间结构”思路，适合后续 LLM 辅助生成和修复。
3. unrealizability debugging 也很适合作为 `project_4` 的反例驱动修复素材。

### 作为目标形式主义还是中间表示

更像面向综合后端的方法路线与执行载体，而不是前端建模语言。

### 对需求到模型生成的启发

1. 需求若天然具有 `I/O` 分区和长期时序目标，就很适合走 logic-to-game-to-controller 的链路。
2. 对不可实现需求，返回紧凑 counterstrategy 往往比只给一个 “unrealizable” 结论更有修复价值。
3. 从 `LTL` 到有限控制器的链路也提示我们：LLM 可以不只生成状态图，还可以生成规格化时序前端。

## 重要的相关工作

1. `Lily`：较早的 Safraless `LTL` synthesis 工具。
2. `Unbeast`：另一条安全博弈与符号求解路线。
3. [slugs-extensible-gr1-synthesis/desc.md](../slugs-extensible-gr1-synthesis/desc.md)：`GR(1)` 片段的工程化综合平台。
4. [strix-explicit-reactive-synthesis-strikes-back/desc.md](../strix-explicit-reactive-synthesis-strikes-back/desc.md)：较新的显式 `DPA/parity-game` 综合路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`LTL reactive synthesis / safety games / Acacia+`
- 论文角色：antichain-based `LTL` realizability / synthesis tool and safety-game route
- 归类理由：论文主体是 `LTL` 综合的工具化求解路线，核心贡献在 `UCBW/K-coBuchi -> safety game -> antichain strategy extraction` 这一工程后端链路，而不是新的状态机本体。

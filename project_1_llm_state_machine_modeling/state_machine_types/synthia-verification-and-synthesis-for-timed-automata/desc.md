# Synthia：定时自动机的验证与综合 / Synthia: Verification and Synthesis for Timed Automata

## 基本信息

- 标题：Synthia: Verification and Synthesis for Timed Automata
- 中文标题：Synthia：定时自动机的验证与综合
- 作者：Hans-Jörg Peter，Rüdiger Ehlers，Robert Mattmüller
- 发表：*Computer Aided Verification*，pp. 649-655，2011
- DOI：`10.1007/978-3-642-22110-1_52`
- 链接：https://doi.org/10.1007/978-3-642-22110-1_52
- 形式主义：`Timed Game Automata / open timed automata / Synthia`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：abstraction-refinement verifier / controller synthesizer for open timed systems
- 工具/实现获取方式：原文明确说明 `Synthia` 采用 `GNU GPL` 发布，并给出 `http://react.cs.uni-saarland.de/tools/synthia` 作为工具、格式说明和 tutorial 入口。
- 标准/格式获取方式：承载方式是工具自有 XML specification format，里面包含 plant、assumptions、guarantees 与参数；它复用了 `UPPAAL DBM` library 和 `CUDD BDD` library，但不是 `UPPAAL` 原生模型格式。

## 简报

这篇论文的关键点不只是“又一个 timed-game 求解器”，而是把**抽象细化**真正用到了开放实时系统上。`Synthia` 把 open timed system 看成 Adam / Eve 的 timed game：环境控制一类非确定性，待综合实现控制另一类非确定性；然后用 `BDD + DBM` 混合表示，在粗抽象上先识别关键控制结构，再逐步细化。

- 形式主义定位：围绕 timed game automata 的验证与控制综合方法，而不是新的 timed automata 母模型。
- 构造方式简述：把开放系统写成 XML 中的 plant + requirements，再用 timed-game semantics、attractor computation 与 may/must abstraction 做 realizability / controller synthesis。
- 基础设施与场景简述：依托 XML front-end、`CUDD`、`UPPAAL DBM` library、backward game solving 和 controller export，服务开放实时控制器综合与安全验证。

```text
open timed system -> timed game automaton -> may/must abstraction -> attractor refinement -> realizability result / controller model
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. open real-time systems；
2. timed game automata；
3. Adam / Eve 双人博弈语义；
4. attractor-based safety solving；
5. may / must abstractions 与 refinement loop。

### 核心抽象

论文的底层对象可保守整理为：

$$ G = (L, \ell_0, C, V, \Sigma_A, \Sigma_E, E, Inv) $$

上式中的符号逐项解释如下：

1. `L` 是 locations。
2. `\ell_0` 是初始位置。
3. `C` 是 clocks。
4. `V` 是 bounded integer variables。
5. `\Sigma_A` 是 Adam 控制的动作。
6. `\Sigma_E` 是 Eve 控制的动作。
7. `E` 是带 guards、updates、resets 的 timed transitions。
8. `Inv` 是 invariants。

安全综合目标可保守写成：

$$ \exists \sigma_A \ \forall \sigma_E.\ \mathrm{Runs}(G,\sigma_A,\sigma_E) \cap Bad = \emptyset $$

上式中的符号逐项解释如下：

1. `\sigma_A` 是实现方策略。
2. `\sigma_E` 是环境策略。
3. `Bad` 是 requirement-violating states。
4. 该式表达“存在控制器，使所有环境行为下都不进入坏状态”。

论文的抽象细化核心在于 may / must 抽象。对两个抽象位置 `n,n'` 与玩家 `p`，有：

$$ n \xrightarrow{may}_p n' \iff \exists \ell \in \gamma(n), \exists \ell' \in \gamma(n').\ \ell \xrightarrow{}_p \ell' $$

$$ n \xrightarrow{must}_p n' \iff \forall \ell \in \gamma(n), \exists \ell' \in \gamma(n').\ \ell \xrightarrow{}_p \ell' $$

上式中的符号逐项解释如下：

1. `\gamma(n)` 是抽象位置 `n` 覆盖的 concrete locations 集合。
2. `may` 表示“某些 concrete states 有这条边”。
3. `must` 表示“所有 concrete states 都有这条边”。
4. 这是 `Synthia` 抽象细化方法最关键的工具内核。

### 一个最小例子与通俗解释

论文用一个带两只钟 `x,y` 和整数 `i` 的小型 timed game 说明抽象细化：

1. Adam 控制动作 `c`。
2. Eve 控制动作 `u1`、`u2`。
3. 目标是避免最终进入坏位置 `\ell_1`。
4. 初始抽象先只分出初始、坏、显然安全和其他四类位置。
5. 若抽象仍判断“安全”，就继续细分使 attractor 扩大；若 attractor 吃到初始状态，就判负。

通俗地说，`Synthia` 不会一开始就把整个 timed game 展开到底，而是先问：“哪些离散控制结构对输赢真的重要？” 只有重要部分才值得继续拆细。

### 运行 / 接受 / 转移语义

坏状态 attractor 可写成：

$$ Attr_E(Bad) $$

其含义是 Eve 能强迫系统最终进入 `Bad` 的状态集合。若：

$$ Init \subseteq Attr_E(Bad) $$

则系统不可实现；反之，Adam 至少在当前抽象上仍保有希望。

论文进一步说明在抽象博弈中：

$$ Eve \text{ plays on must transitions}, \qquad Adam \text{ plays on may transitions} $$

上式中的符号逐项解释如下：

1. 这会削弱 Eve、强化 Adam。
2. 因而抽象上的 `Attr_E(Bad)` 是 concrete attractor 的 under-approximation。
3. 若抽象上已判负，则 concrete system 必然判负。

### 语义边界

1. 论文主目标是 safety realizability，不是一般 `LTL/CTL` timed games 全覆盖平台。
2. 模型假定 strong non-zenoness。
3. 语义采用 asymmetric semantics：当双方都可主动走边时，Eve 优先。
4. XML front-end 是工具自有格式，不是通用 timed-automata exchange standard。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| timed game 骨架 | `$G = (L, \ell_0, C, V, \Sigma_A, \Sigma_E, E, Inv)$` | `Synthia` 求解的基础对象。 |
| 安全综合目标 | `$\exists \sigma_A \forall \sigma_E.\ \mathrm{Runs}(G,\sigma_A,\sigma_E) \cap Bad = \emptyset$` | 判定 realizability 的核心问题。 |
| may 抽象 | `$n \xrightarrow{may}_p n'$` | 某些 concrete locations 提供该迁移。 |
| must 抽象 | `$n \xrightarrow{must}_p n'$` | 所有 concrete locations 都提供该迁移。 |
| 坏状态 attractor | `$Attr_E(Bad)$` | 抽象细化的收缩/扩张核心对象。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接围绕 timed game locations 与抽象位置工作。 |
| 事件 / 触发 | 很强 | controllable / uncontrollable actions 是核心。 |
| 守卫 / 数据 | 强支持 | guards、bounded integers、XML assumptions / guarantees 都支持。 |
| 层次 | 不支持 | 不是层次状态机工具。 |
| 并发 / 同步 | 中等支持 | 支持 parallel composition，但主卖点不在 network DSL。 |
| 时间约束 | 很强 | `DBM` zones 与 timed games 是核心。 |
| 连续动态 / 随机性 | 不支持 | 不处理 hybrid / probabilistic semantics。 |
| 可执行 / 可验证性 | 很强 | 可判 realizability，也可输出 synthesized controller。 |

### 形式化问题与性质

1. `Synthia` 的创新点在于把抽象细化从 closed-system verification 推到 open timed synthesis。
2. `BDD` 负责离散控制结构，`DBM` 负责 clocks，二者分工很清楚。
3. may / must abstraction 让它能尽早筛掉与输赢无关的大块状态结构。

## 构造方式与承载格式

### 建模入口

原文给出的建模入口有：

1. XML specification file；
2. plant + assumptions + guarantees；
3. command-line parameters 覆盖默认参数；
4. `--synth-cont` 与 `--synth-cont-plant` 导出 controller。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Synthia` XML format；
2. `BDD`-based control-structure representation；
3. `DBM`-based clock-zone representation；
4. controller / controlled-plant XML 输出。

### 交换与互操作

互操作重点体现在工具复用而非中立标准：

1. 复用 `CUDD` BDD library。
2. 复用 `UPPAAL DBM` library。
3. 控制器能再次导出成 `Synthia` 格式模型，方便串联后续分析。

## 配套基础设施

- 建模/编辑工具：主线是 XML + CLI，而不是 GUI editor。
- 解析/交换/元模型支持：tool-specific XML schema、参数覆盖、controller export。
- 仿真/执行支持：原文不主打仿真，主线是 realizability / synthesis。
- 验证/分析支持：backward game solving、attractor updates、forward zone-based refinement guidance。
- 代码生成/转换支持：支持 synthesize controller / controlled plant export，但不是代码生成器。
- 标准化或社区生态：`GNU GPL`、官网 tutorial、`CUDD` + `UPPAAL DBM` 复用生态。

## 适用场景与需求前提

### 适用场景

适合开放实时控制器综合、带环境对手的 timed safety 问题，以及需要在“模型检查”和“控制器生成”之间打通的场景。

### 需求前提

1. 系统要能明确区分 controllable 与 uncontrollable behavior。
2. 核心性质以 safety / bounded reachability 为主。
3. 数据变量需要有界，时间行为需要适合 `DBM` zone 处理。

### 不适用或高成本场景

如果需求是概率实时、连续动力学、或高度层次化的状态图语义，`Synthia` 不是最佳入口；它更适合作为 open timed synthesis 专用路线。

## 与相邻形式主义的关系

相对 [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)，两者都做 timed-game synthesis，但 `UPPAAL-Tiga` 更强调成熟 `UPPAAL` 生态与交互式策略导出，`Synthia` 更强调 abstraction refinement；相对 [uppaal-40/desc.md](../uppaal-40/desc.md)，`UPPAAL 4.0` 是主平台升级，`Synthia` 是专门的 open timed-game solver；相对 [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)，后者补的是 `PTA` 检查桥接，本文补的是非概率 timed games 的控制综合。

## 与本研究的关系

### 对 Project 1 的价值

1. 它直接对应“需求到可综合控制器”的 timed-state-machine 路线。
2. may / must abstraction 对后续做验证驱动修复也很有启发，因为它说明可以先粗后细定位真正相关的模型部分。
3. 如果未来要把开放环境假设显式写入状态机生成目标，`Synthia` 这类假设 / 保证格式值得参考。

### 局限

1. 重点在 safety 与 open timed synthesis，不是通用时序逻辑平台。
2. 输入格式偏工具私有，互操作性弱于 `UPPAAL` 主生态。

## 重要的相关工作

- [uppaal-tiga-time-for-playing-games/desc.md](../uppaal-tiga-time-for-playing-games/desc.md)：另一条 timed-game controller synthesis 工具线。
- [uppaal-40/desc.md](../uppaal-40/desc.md)：`UPPAAL` 主平台本体。
- [a-modest-approach-to-checking-probabilistic-timed-automata/desc.md](../a-modest-approach-to-checking-probabilistic-timed-automata/desc.md)：概率实时检查桥路线。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 结论：这是一篇典型的 timed-game abstraction-refinement 条目，适合作为开放实时系统综合路线的 `🛠️` 代表论文入账。

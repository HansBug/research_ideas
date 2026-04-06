# Ariadne：混成系统可达性计算框架 / Reachability computation for hybrid systems with Ariadne

## 基本信息

- 标题：Reachability computation for hybrid systems with Ariadne
- 中文标题：Ariadne：混成系统可达性计算框架
- 作者：Luca Benvenuti，Davide Bresolin，Alberto Casagrande，Pieter Collins，Alberto Ferrari，Emanuele Mazzi，Alberto Sangiovanni-Vincentelli，Tiziano Villa
- 发表：*IFAC Proceedings Volumes*，41(2):8960-8965，2008
- DOI：`10.3182/20080706-5-KR-1001.01513`
- 链接：https://ir.cwi.nl/pub/13316/13316B.pdf
- 形式主义：`Hybrid Automata / Ariadne`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：open reachability framework / hybrid analysis environment
- 工具/实现获取方式：原文明确说明 `Ariadne` 以 open source distribution 方式发布，但正文未给稳定下载 URL。
- 标准/格式获取方式：承载方式是 `Ariadne` 的 hybrid automata 表示、hybrid basic sets 与 hybrid grids；原文未给独立中立标准。

## 简报

这篇论文的关键价值，不只是又做一个 hybrid reachability tool，而是把 reachability analysis 做成一个可扩展框架。`Ariadne` 既强调 computable analysis 的严谨近似边界，也强调工程可扩展性：basic sets、denotable sets、hybrid grids、bounding sets、可替换 integrators、C++ kernel 和 Python scripting interface 一起组成了一个开放环境。

- 形式主义定位：面向 `Hybrid Automata` 的 open reachability framework，而不是新的混成自动机理论本体。
- 构造方式简述：输入 hybrid automaton、初始集、bounding set 与 hybrid grid，工具交替做 continuous evolution 与 discrete evolution，最终求 chain-reachable set 的 over-approximation。
- 基础设施与场景简述：依托 hybrid grids、affine/Euler/Lohner integrators、C++ kernel 与 Python interface，服务 water-tank monitor 等混成安全分析与算法试验。

```text
hybrid automaton -> basic sets / hybrid grid -> continuous evolution + discrete evolution -> chain-reachable over-approximation
```

## 形式主义定义与核心对象

### 定义对象

论文直接给出 `Hybrid Automaton` 的一般定义：

1. `Q` 是离散 locations。
2. `E` 是 control switches。
3. `X` 是连续状态空间。
4. `Inv`、`Dyn`、`Act`、`Reset` 分别给出 invariant、动态、触发条件与 reset。

### 核心抽象

论文中的混成自动机定义为：

$$
H = \langle Q, E, X, Inv, Dyn, Act, Reset \rangle
$$

上式中的符号逐项解释如下：

1. `Q` 是 locations 集合。
2. `E` 是 directed edges 集合。
3. `X` 是连续变量空间。
4. `Inv(q)` 是 location `q` 的不变式。
5. `Dyn(q)` 是 `q` 的连续动态关系。
6. `Act(e)` 是 edge `e` 的 activation condition。
7. `Reset(e)` 是 edge `e` 的 reset relation。

论文把 reachable-set 问题写成：

$$
\mathrm{ReachSet}_H(R)
$$

上式中的符号逐项解释如下：

1. `H` 是给定 hybrid automaton。
2. `R \subseteq Q \times X` 是初始状态集合。
3. `\mathrm{ReachSet}_H(R)` 是从 `R` 出发所有可达状态的集合。

`Ariadne` 计算的不是任意精确可达集，而是 chain-reachable set 的 over-approximation，可保守写成：

$$
\mathrm{ReachSet}_H(R) \subseteq S
$$

其中 `S` 是随着精度提高可逼近 chain-reachable set 的结果集。

### 一个最小例子与通俗解释

论文自带一个很适合讲清楚工具思路的例子：带 `2` 秒延迟的水箱水位监控器。

1. `q_0`、`q_1` 表示 pump on，`q_2`、`q_3` 表示 pump off。
2. 连续变量 `y` 表示水位，`x` 表示切换延迟计时。
3. 在不同 location 里，`y` 的导数不同；当 `y` 到达阈值时触发离散切换。
4. `Ariadne` 不是只跑一条水位曲线，而是算出在一段时间内所有可能到达的区域，并判断这些区域是否越界。

通俗地说，`Ariadne` 像“把混成系统的未来活动范围画到格子上”的框架。只要某个格子被证明可能到达，它就会被标记下来，然后继续展开。

### 运行 / 接受 / 转移语义

论文对连续语义给出：

$$
\langle v, r \rangle \xrightarrow{t}_C \langle v, s \rangle
$$

上式中的符号逐项解释如下：

1. `v` 是 location。
2. `r`、`s` 是连续状态赋值。
3. `t` 是 elapsed time。
4. 该关系表示在不离开 `v` 的前提下，系统可经过连续流从 `r` 演化到 `s`。

离散语义则写成：

$$
\langle v, r \rangle \xrightarrow{e}_D \langle u, s \rangle
$$

上式中的符号逐项解释如下：

1. `e = \langle v,u \rangle` 是一条 edge。
2. `Act(e)` 决定边是否可触发。
3. `Reset(e)` 决定跳转后连续变量如何更新。

`Ariadne` 的 reachability algorithm 交替做三步：

1. 连续演化并标记被触碰的 grid cells。
2. 做一次 discrete evolution 并标记新 cells。
3. 若没有新 cells 则到达 fixpoint。

### 语义边界

这篇论文的边界也写得很清楚：

1. 它求的是 chain-reachable set 的 over-approximation，不承诺任意精确 reachable set。
2. 算法终止性依赖 bounded region 与 finite grid。
3. lower-approximation 仍在扩展中，不是完全成熟能力。
4. 精度与效率直接受 grid 粒度、integrator 选择和 basic-set 细分策略影响。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 混成自动机骨架 | `$H = \langle Q, E, X, Inv, Dyn, Act, Reset \rangle$` | 固定 `Ariadne` 处理对象。 |
| 连续转移 | `$\langle v, r \rangle \xrightarrow{t}_C \langle v, s \rangle$` | location 内的连续演化语义。 |
| 离散转移 | `$\langle v, r \rangle \xrightarrow{e}_D \langle u, s \rangle$` | control switch 的离散语义。 |
| 可达集包络 | `$\mathrm{ReachSet}_H(R) \subseteq S$` | 工具返回 chain-reachable over-approximation。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | locations 是离散骨架。 |
| 事件 / 触发 | 强支持 | `Act` 与 `Reset` 明确给出离散切换。 |
| 守卫 / 数据 | 很强 | invariants、activation conditions 与 reset 都显式建模。 |
| 层次 | 弱支持 | 主体不是层次状态机。 |
| 并发 / 同步 | 弱支持 | 本文重心在单 automaton reachability。 |
| 时间约束 | 很强 | 连续时间流与 hybrid grids 是核心。 |
| 连续动态 / 随机性 | 强连续 / 不随机 | 支持连续演化；不涉及概率。 |
| 可执行 / 可验证性 | 很强 | over-approximation、lower-approximation 规划、脚本接口都具备。 |

### 形式化问题与性质

1. `Ariadne` 的核心创新是“开放 reachability framework”，不是单一固定算法。
2. hybrid basic sets 与 hybrid grids 让“表示精度”和“算法终止”能在同一框架里调节。
3. paper 明确区分 exact reachable set、chain-reachable set 与 lower-approximation，这一点比很多单纯工具介绍更严谨。

## 构造方式与承载格式

### 建模入口

论文中的典型入口是：

1. 给出 hybrid automaton。
2. 指定 initial set。
3. 指定 bounding set。
4. 选择 hybrid grid 与 integrator。
5. 在 continuous/discrete evolution 之间迭代。

### 机器可处理承载方式

机器可处理承载方式包括：

1. hybrid basic sets。
2. denotable sets。
3. hybrid grids。
4. basic-set integrators。
5. C++ kernel 与 Python scripting interface。

### 交换与互操作

这篇论文的互操作重点不在标准文件，而在框架可扩展性：

1. 可替换不同 integrators，例如 affine、Euler、Lohner。
2. 可扩展不同 numeric representations。
3. 同一 reachability 骨架可覆盖 discrete-time、continuous-time 和 hybrid systems。

## 配套基础设施

- 建模/编辑工具：原文强调 analysis framework，本身不是重 GUI 的 editor。
- 解析/交换/元模型支持：通过 hybrid automaton、basic sets 与 grids 做内部承载；无中立交换标准。
- 仿真/执行支持：重点是 set-based reachability，而不是单轨仿真。
- 验证/分析支持：chain-reachable over-approximation、bounded search、lower-approximation 扩展。
- 代码生成/转换支持：原文未讨论代码生成。
- 标准化或社区生态：open source distribution、C++ kernel、Python scripting interface 与可替换 integrators 构成主要生态。

## 适用场景与需求前提

### 适用场景

适合需要对 hybrid automata 做可达性分析、并且希望在同一框架里试验不同 set representation 或 integrator 的场景。

### 需求前提

1. 系统必须能写成显式 `Hybrid Automata`。
2. 分析区域需要有 bounding set。
3. 建模者愿意以 grid precision / basic-set approximation 方式控制误差。
4. 目标问题主要是 reachability / safety，而不是直接代码生成。

### 不适用或高成本场景

如果模型天然是黑盒仿真器、没有可显式写出的 hybrid automaton 结构，或者完全不能接受 grid-induced over-approximation，则 `Ariadne` 并不自然。

## 与相邻形式主义的关系

相对 [the-ddt-tool-for-verification-of-hybrid-systems/desc.md](../the-ddt-tool-for-verification-of-hybrid-systems/desc.md)，`Ariadne` 更强调开放框架与 set representation；相对 [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md) 与 [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)，它更像 experimentation-friendly reachability environment；相对 [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)，它不把主轴锁定在 Taylor-model non-linear flowpipes。

## 与本研究的关系

### 对 Project 1 的价值

它提示 `project_1` 后续若要做“一个中间模型，多种分析后端”，应当把模型表示、数值表示和求解器接口解耦，而不是把所有能力硬写死在同一后端里。

### 作为目标形式主义还是中间表示

更适合作为分析框架或验证后端，不是最终交付给领域工程师的目标语言。

### 对需求到模型生成的启发

1. 需求到模型的生成阶段必须显式产出 `Q/E/X/Inv/Dyn/Act/Reset` 六类核心对象。
2. 若想让不同 analysis backends 共用同一模型，应尽量把 continuous dynamics 与 discrete switching 分层表达。
3. 对近似分析而言，bounding region 与 precision knobs 本身也是生成阶段必须考虑的输出。

### 现实限制

`Ariadne` 很适合做框架级 experimentation，但对使用者的形式化建模能力要求不低。

## 重要的相关工作

- [the-ddt-tool-for-verification-of-hybrid-systems/desc.md](../the-ddt-tool-for-verification-of-hybrid-systems/desc.md)：更早的 hybrid reachability / synthesis tool。
- [phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md](../phaver-algorithmic-verification-of-hybrid-systems-past-hytech/desc.md)：更偏 exact / affine hybrid verification。
- [spaceex-scalable-verification-of-hybrid-systems/desc.md](../spaceex-scalable-verification-of-hybrid-systems/desc.md)：更偏 scalable support-function reachability。
- [flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md](../flowstar-an-analyzer-for-non-linear-hybrid-systems/desc.md)：更偏 non-linear hybrid analysis。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`Hybrid Automata / Ariadne`
- 论文角色：open reachability framework / hybrid analysis environment
